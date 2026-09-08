#!/usr/bin/env python3
"""
SRE Copilot Aggregator Service

This service provides the main FastAPI aggregator for the SRE Copilot system.

Configuration:
- SLACK_BOT_ENABLED: Set to control Slack bot startup (default: true)
  - To disable Slack bot: export SLACK_BOT_ENABLED=false
  - To enable Slack bot: export SLACK_BOT_ENABLED=true (or omit the variable)
  - Accepted values: true/false, 1/0, yes/no, on/off (case insensitive)
"""

import os
import sys
from dotenv import load_dotenv
import platform

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
if platform.system() == "Darwin":
    os.environ["CONTACTS_FILE_PATH"] = os.path.join(os.path.dirname(__file__), "utils", "POC_Details.xlsx")
else:
    os.environ.setdefault("HF_HOME", "/app/testenv/SRE-Copilot")
    os.environ["CONTACTS_FILE_PATH"] = "/app/testenv/srecopilot/SRE-Copilot/utils/POC_Details.xlsx"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from tools.jira import (
    JiraRequest, JiraResponse,
    Jira_Operations, _extract_issue_key,
    JIRA_ENABLED,
)
from tools.slack_qa import SlackHistoryQA, DEFAULT_INDEX_PATH, DEFAULT_JSON_PATH
import json
import re
import warnings
from utils import Contacts_pandas
from typing import Optional, List, Dict, Any
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import uvicorn
import asyncio
import time
from threading import Lock

# --- Import new modules ---
from stats import (
    _inc_stat, _flush_stats, get_stats_snapshot,
    get_stats_start_time, get_stats_file_path,
)
from session import (
    get_or_create_memory, conversation_sessions,
    SESSION_TTL_SECONDS, SESSION_MAX_COUNT,
    get_cached_classification, cache_classification,
)
from guardrails import (
    _normalize_response_text, _apply_response_guardrails,
)
from classification import (
    _detect_conversational_intent, fast_classify_query,
    classify_with_bart,
)
from handlers.incidents import PRDB, _enrich_with_prdb
from handlers.confluence import Confluence_Search
from handlers.general import (
    General_Information, Welcome_Message, Context_Explanation,
    CONTEXT_EXPLAINER_MODE, LOCAL_MODEL_NAME, LOCAL_CONFIDENCE_THRESHOLD,
)
from handlers.tools_info import Tools_information
from handlers.logs_search import Logs_Search
from utils.slack_handler import start_slack_bot

warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")

# ---------------------------------------------------------------------------
# Slack History QA — lazy singleton
# ---------------------------------------------------------------------------
_slack_qa: Optional[SlackHistoryQA] = None
_slack_qa_lock = Lock()

def _get_slack_qa() -> SlackHistoryQA:
    global _slack_qa
    if _slack_qa is not None:
        return _slack_qa
    with _slack_qa_lock:
        if _slack_qa is None:
            qa = SlackHistoryQA(index_path=DEFAULT_INDEX_PATH, json_path=DEFAULT_JSON_PATH)
            try:
                qa.ensure_index()
            except Exception as e:
                logger.warning(f"SlackHistoryQA index load failed: {e} — will retry on first query")
            _slack_qa = qa
    return _slack_qa


# Configuration flags
SLACK_BOT_ENABLED = os.environ.get("SLACK_BOT_ENABLED", "true").lower() in ["true", "1", "yes", "on"]

# Concurrency limiter
_INFERENCE_SEMAPHORE_LIMIT = int(os.environ.get("MAX_CONCURRENT_INFERENCES", "4"))
_inference_semaphore = asyncio.Semaphore(_INFERENCE_SEMAPHORE_LIMIT)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

_SILENT_PATHS = {"/health", "/stats"}

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in _SILENT_PATHS:
            return await call_next(request)
        logger.info(f"Request: {request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {request.method} {request.url.path} - Status: {response.status_code}")
        return response

class _HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        msg = record.getMessage()
        return not any(p in msg for p in _SILENT_PATHS)


# ---------------------------------------------------------------------------
# Proxy configuration
# ---------------------------------------------------------------------------
os.environ["http_proxy"] = "http://proxy.ebiz.verizon.com:80"
os.environ["https_proxy"] = "http://proxy.ebiz.verizon.com:80"

# ---------------------------------------------------------------------------
# ChromaDB setup
# ---------------------------------------------------------------------------
if platform.system() == "Darwin":
    CHROMA_PATH = "/Users/MUTHYAN/PycharmProjects/pythonProject/chroma_db"
    CHROMA_CACHE_DIR = "/Users/MUTHYAN/PycharmProjects/pythonProject/chroma_cache"
else:
    CHROMA_PATH = "/app/testenv/chroma_db"
    CHROMA_CACHE_DIR = "/app/testenv/chroma_db/chroma_cache"

os.environ["CHROMA_CACHE_DIR"] = CHROMA_CACHE_DIR
os.makedirs(CHROMA_CACHE_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(anonymized_telemetry=False),
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collection_outage = chroma_client.get_or_create_collection(name="outages_collection")
collection_tools = chroma_client.get_or_create_collection(name="tools_collection")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    client_type: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    source: Optional[Any] = None
    relevance: Optional[str] = None

class ConfluenceSearchRequest(BaseModel):
    query: str = Field(..., description="Search query for Confluence")
    session_id: Optional[str] = Field(None, description="Optional session ID for conversation tracking")

class ConfluenceSearchResponse(BaseModel):
    message: str
    source: List[Dict[str, str]]
    relevance: str
    session_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    username: str = Field(..., description="Name of the person providing feedback")
    user_email: str = Field(..., description="Email of the user providing feedback")
    feedback: str = Field(..., description="Feedback value: 'positive' or 'negative'")
    feedback_text: Optional[str] = Field(None, max_length=500)
    user_question: Optional[str] = Field(None)
    bot_response: Optional[str] = Field(None)

class SlackHistoryRequest(BaseModel):
    query: str = Field(..., description="Question to answer from Slack channel history")
    session_id: Optional[str] = Field(None)
    top_k: int = Field(8, ge=1, le=30)

class SlackHistoryResponse(BaseModel):
    message: str
    source: str
    relevance: str
    session_id: Optional[str] = None


# ---------------------------------------------------------------------------
# Query routing helper functions
# ---------------------------------------------------------------------------
def _extract_user_question(full_query: str) -> tuple:
    """Separate the user's actual question from prepended conversation context."""
    marker = "Based on the conversation above, the user is now asking:"
    if marker in full_query:
        parts = full_query.split(marker, 1)
        question = parts[1].strip()
        context = None
        ctx_start = parts[0].find("---")
        ctx_end = parts[0].rfind("---")
        if ctx_start != -1 and ctx_end != -1 and ctx_end > ctx_start:
            context = parts[0][ctx_start + 3:ctx_end].strip()
        logger.info(f"Extracted user question for classification: '{question[:80]}...'")
        return question, context
    return full_query, None


def _is_context_explanation_request(question: str, context: str | None) -> bool:
    """Detect if the user is asking to explain / analyze pasted content."""
    if not context:
        return False
    explain_patterns = re.compile(
        r"\b(explain|what does this mean|what happened|what is this|what'?s this|"
        r"what'?s (going on|wrong)|can you (explain|analyze|look at|check)|"
        r"help me understand|break this down|summarize|analyse|analyze)\b",
        re.IGNORECASE,
    )
    return bool(explain_patterns.search(question))


# ---------------------------------------------------------------------------
# Main query router
# ---------------------------------------------------------------------------
def QueryAnalyze(query, memory, client_type='web'):
    """Analyze the query and route to appropriate handler."""
    logger.info(f"Analyzing query: {query[:50]}... (client_type: {client_type})")

    def _guard(result_obj, category_hint: str):
        return _apply_response_guardrails(query, result_obj, category_hint)

    history = ""
    if memory.buffer:
        history = memory.buffer
        logger.info(f"Retrieved conversation history of length: {len(history)}")

    question_for_classification, conversation_context = _extract_user_question(query)

    # Priority: Jira issue key detection
    if _extract_issue_key(question_for_classification or query):
        logger.info("Jira issue key detected in query — routing directly to Jira_Operations")
        result = Jira_Operations(query, memory)
        _inc_stat("jira_operations")
        return _guard(result, "jira_operations")

    # Context explanation request
    if _is_context_explanation_request(question_for_classification, conversation_context):
        logger.info("Detected 'explain context' request — routing to Context_Explanation")
        result = Context_Explanation(question_for_classification, conversation_context, memory, collection_outage)
        return _guard(result, "context_explanation")

    # Vague "explain this" with no context
    _has_source_ref = re.search(
        r'\b(confluence|jira|wiki|logs?|kibana|splunk|grafana|dashboard|prdb|incident)\b',
        question_for_classification, re.IGNORECASE
    )
    if not conversation_context and not _has_source_ref and _is_context_explanation_request(
        question_for_classification, "placeholder"
    ):
        logger.info("Vague 'explain this' with no context — returning helpful message")
        _inc_stat("vague_explain_local")
        vague_explain_response = {
            "message": (
                "I'd be happy to help explain! But I need to see the actual content. "
                "Could you paste the error, log, or text you'd like me to explain "
                "directly in your message?"
            ),
            "source": "General Information",
            "relevance": "N/A",
        }
        return _guard(vague_explain_response, "vague_explain")

    # Curated conversational gate
    intent_name, curated_response = _detect_conversational_intent(question_for_classification)
    if intent_name and curated_response:
        curated_response = _normalize_response_text(curated_response)
        memory.save_context({"input": query}, {"output": curated_response})
        _inc_stat("curated_intent_local")
        logger.info(f"Response served by: Local curated intent | intent={intent_name}")
        return _guard({
            "message": curated_response,
            "source": f"Conversational Intent ({intent_name})",
            "relevance": "100%",
        }, f"conversational_{intent_name}")

    cleaned_query = question_for_classification.strip().lower() if question_for_classification else ""
    logger.info(f"Cleaned query for classification: '{cleaned_query}'")

    # Classification pipeline: cache -> keywords -> BART
    cached_category = get_cached_classification(question_for_classification, history)
    if cached_category:
        logger.info(f"Using cached classification: {cached_category}")
        category = cached_category
    else:
        keyword_category = fast_classify_query(question_for_classification)
        if keyword_category:
            logger.info(f"Keyword-based classification: {keyword_category}")
            category = keyword_category
            cache_classification(question_for_classification, history, category)
        else:
            logger.info("Using BART-large-MNLI for query classification")
            try:
                category = classify_with_bart(question_for_classification)
                logger.info(f"BART classification result: {category}")
                cache_classification(question_for_classification, history, category)
            except Exception as e:
                logger.error(f"Error in BART classification: {str(e)}")
                category = 'general_information'

    if category == 'greeting':
        _inc_stat("greeting_local")
        return _guard(Welcome_Message(query, memory), "greeting")

    logger.info(f"Query classified as: {category}")

    # Route to handler
    result = None
    handler_name = None
    try:
        if category == "incidents_collection":
            handler_name = "PRDB (Incidents)"
            result = PRDB(query, memory, collection_outage)
        elif category == "contacts_of_different_teams":
            handler_name = "Contacts (Pandas)"
            output_format = "slack" if client_type == "slack" else "html"
            result_str = Contacts_pandas.table_search(query, output_format=output_format, use_semantic=True)
            memory.save_context({"input": query}, {"output": "I found contact information for your query."})
            result = {"message": result_str, "source": "Team Contacts", "relevance": "95%"}
        elif category == "jira_operations":
            handler_name = "Jira Operations"
            result = Jira_Operations(query, memory)
        elif category == "logs_search":
            handler_name = "Logs Search (NextGenSearch MCP)"
            result = Logs_Search(query, memory)
        elif category == "general_information":
            result = General_Information(query, memory)
            source_check = result.get("source", "") if isinstance(result, dict) else ""
            handler_name = ("General Information (Local Model)"
                            if "Local" in source_check
                            else "General Information (VegasLLM)")
        elif category == "confluence_search":
            handler_name = "Confluence Search (VegasLLM)"
            result = Confluence_Search(query, memory)

            try:
                rel_str = result.get("relevance", "0%") if isinstance(result, dict) else "0%"
                rel_val = int(rel_str.replace("%", "").strip())
            except (ValueError, AttributeError):
                rel_val = 0

            if rel_val <= 30:
                logger.info(f"Confluence relevance too low ({rel_val}%) — falling back to General_Information")
                handler_name = "General Information (VegasLLM — Confluence low-relevance fallback)"
                result = General_Information(query, memory)
        else:
            handler_name = "General Information (VegasLLM — default fallback)"
            result = General_Information(query, memory)

    except Exception as e:
        logger.error(f"Error in category handler: {str(e)}", exc_info=True)
        handler_name = "General Information (VegasLLM fallback)"
        result = General_Information(query, memory)

    # Increment stats
    source_str = result.get("source", "") if isinstance(result, dict) else ""
    already_counted = "Local" in source_str

    if not already_counted:
        _stat_map = {
            "PRDB (Incidents)": "incidents_prdb",
            "Contacts (Pandas)": "contacts",
            "Jira Operations": "jira_operations",
            "Logs Search (NextGenSearch MCP)": "logs_search",
            "General Information (VegasLLM)": "general_information",
            "Confluence Search (VegasLLM)": "confluence_search",
            "General Information (VegasLLM — Confluence low-relevance fallback)": "confluence_low_rel_fallback",
            "General Information (VegasLLM fallback)": "general_information",
        }
        _inc_stat(_stat_map.get(handler_name, "general_information"))

    source = result.get("source", "unknown") if isinstance(result, dict) else "unknown"
    relevance = result.get("relevance", "N/A") if isinstance(result, dict) else "N/A"
    logger.info(
        f"Response served by: {handler_name} | "
        f"category={category} | source={source} | relevance={relevance}"
    )
    return _guard(result, category)


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.api_route("/query", methods=["GET", "POST", "OPTIONS"])
async def chat_endpoint(chat_message: ChatMessage):
    logger.info(f"Received request at /query endpoint with session_id: {chat_message.session_id}")
    input_text = chat_message.message
    client_type = chat_message.client_type or 'web'
    session_id, memory = get_or_create_memory(chat_message.session_id)

    if not input_text:
        response = _apply_response_guardrails(input_text, Welcome_Message(input_text, memory), "empty_input")
        return ChatResponse(message=response.get("message"), session_id=session_id, source=response.get("source"), relevance=response.get("relevance"))

    async with _inference_semaphore:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, QueryAnalyze, input_text, memory, client_type)

        return ChatResponse(message=response.get("message"), session_id=session_id, source=response.get("source"), relevance=response.get("relevance"))


@app.api_route("/confluence", methods=["GET", "POST", "OPTIONS"])
async def confluence_endpoint(confluence_request: ConfluenceSearchRequest):
    query = confluence_request.query
    session_id, memory = get_or_create_memory(confluence_request.session_id)

    if not query or not query.strip():
        return ConfluenceSearchResponse(
            message="Please provide a search query.",
            source=[], relevance="0%", session_id=session_id
        )

    response = Confluence_Search(query, memory)
    return ConfluenceSearchResponse(
        message=response.get("message", ""),
        source=response.get("source", []),
        relevance=response.get("relevance", "15%"),
        session_id=session_id
    )


@app.api_route("/jira", methods=["GET", "POST", "OPTIONS"])
async def jira_endpoint(jira_request: JiraRequest):
    query = jira_request.query
    session_id, memory = get_or_create_memory(jira_request.session_id)

    if not query or not query.strip():
        return JiraResponse(
            message="Please provide a query for Jira (e.g. 'get PROJ-123' or 'search open bugs in PROJECT').",
            source="Jira", relevance="0%", session_id=session_id,
        )

    async with _inference_semaphore:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, Jira_Operations, query, memory)

    _inc_stat("jira_operations")
    return JiraResponse(
        message=response.get("message", ""),
        source=response.get("source", "Jira"),
        relevance=response.get("relevance", "0%"),
        session_id=session_id,
    )


@app.api_route("/slack-history", methods=["GET", "POST", "OPTIONS"])
async def slack_history_endpoint(request: SlackHistoryRequest):
    logger.info(f"/slack-history query: {request.query[:80]}")
    session_id, memory = get_or_create_memory(request.session_id)
    async with _inference_semaphore:
        loop = asyncio.get_event_loop()
        try:
            qa = _get_slack_qa()
            if not qa.doc_term_freqs:
                await loop.run_in_executor(None, qa.ensure_index)
            results = await loop.run_in_executor(
                None, lambda: qa.retrieve(request.query, top_k=request.top_k)
            )
            if not results:
                return SlackHistoryResponse(
                    message="No relevant messages found in the Slack channel history.",
                    source="Slack Channel History (C040VP21E2C)",
                    relevance="0%", session_id=session_id,
                )
            answer = await loop.run_in_executor(
                None, lambda: qa.answer_with_vegas(request.query, results)
            )
            if not answer:
                snippets = []
                for msg, score in results[:4]:
                    snippets.append(
                        f"`[{msg.msg_id}]` *{msg.user_name}* ({msg.datetime}):\n{msg.text[:300]}"
                    )
                answer = "Top matching Slack messages:\n\n" + "\n\n---\n".join(snippets)
            memory.save_context({"input": request.query}, {"output": answer})
            _inc_stat("slack_history_qa")
            return SlackHistoryResponse(
                message=answer,
                source="Slack Channel History (C040VP21E2C)",
                relevance="85%", session_id=session_id,
            )
        except Exception as e:
            logger.error(f"/slack-history error: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    uptime_secs = time.time() - get_stats_start_time()
    return {
        "status": "ok",
        "uptime_seconds": round(uptime_secs, 1),
        "active_sessions": len(conversation_sessions),
        "session_limit": SESSION_MAX_COUNT,
        "max_concurrent_inferences": _INFERENCE_SEMAPHORE_LIMIT,
        "total_requests": get_stats_snapshot().get("total", 0),
        "model": LOCAL_MODEL_NAME,
        "explainer_mode": CONTEXT_EXPLAINER_MODE,
        "jira_enabled": JIRA_ENABLED,
    }


@app.get("/stats")
def request_stats():
    stats = get_stats_snapshot()
    total = stats.get("total", 0) or 1
    uptime_secs = time.time() - get_stats_start_time()
    uptime_min = round(uptime_secs / 60, 1)

    numeric_keys = {k: v for k, v in stats.items()
                    if k not in ("total", "first_recorded", "last_updated") and isinstance(v, (int, float))}
    pct = {k: round(v / total * 100, 1) for k, v in numeric_keys.items()}

    local_no_llm = (
        stats.get("greeting_local", 0)
        + stats.get("curated_intent_local", 0)
        + stats.get("vague_explain_local", 0)
    )
    local_flan_t5 = stats.get("local_flan_t5", 0)
    vegas_total = (
        stats.get("vegas_llm", 0)
        + stats.get("confluence_search", 0)
        + stats.get("confluence_low_rel_fallback", 0)
        + stats.get("incidents_prdb", 0)
        + stats.get("general_information", 0)
    )

    return {
        "uptime_minutes": uptime_min,
        "total_requests": stats["total"],
        "first_recorded": stats.get("first_recorded"),
        "last_updated": stats.get("last_updated"),
        "stats_file": get_stats_file_path(),
        "counts": numeric_keys,
        "percentages": pct,
        "summary": {
            "local_no_llm": {"count": local_no_llm, "pct": round(local_no_llm / total * 100, 1)},
            "local_flan_t5": {"count": local_flan_t5, "pct": round(local_flan_t5 / total * 100, 1)},
            "vegas_llm_total": {"count": vegas_total, "pct": round(vegas_total / total * 100, 1)},
        },
    }


# --- Feedback ---
def log_feedback_to_file(
    username: str, user_email: str, feedback_value: str,
    feedback_text: Optional[str] = None, user_question: Optional[str] = None,
    bot_response: Optional[str] = None, error_message: Optional[str] = None
):
    feedback_data = {
        "username": username,
        "user_email": user_email,
        "feedback": feedback_value,
        "feedback_text": feedback_text,
        "user_question": user_question,
        "bot_response": bot_response,
        "timestamp": datetime.now().isoformat()
    }
    if error_message:
        feedback_data["error"] = error_message
    try:
        os.makedirs("utils", exist_ok=True)
        file_path = os.path.join("utils", "feedback_log.json")
        with open(file_path, "a") as feedback_file:
            feedback_file.write(json.dumps(feedback_data) + "\n")
    except Exception as e:
        logger.critical(f"Could not write feedback to log file: {e}", exc_info=True)


@app.post("/feedback")
async def submit_feedback(feedback_data: FeedbackRequest):
    if feedback_data.feedback.lower() not in ["positive", "negative"]:
        raise HTTPException(status_code=400, detail="Invalid feedback value. Must be 'positive' or 'negative'.")
    try:
        log_feedback_to_file(
            username=feedback_data.username,
            user_email=feedback_data.user_email,
            feedback_value=feedback_data.feedback,
            feedback_text=feedback_data.feedback_text,
            user_question=feedback_data.user_question,
            bot_response=feedback_data.bot_response
        )
        return {"status": "success", "message": f"Feedback from {feedback_data.username} recorded successfully."}
    except HTTPException as http_exc:
        log_feedback_to_file(
            username=feedback_data.username, user_email=feedback_data.user_email,
            feedback_value=feedback_data.feedback, feedback_text=feedback_data.feedback_text,
            user_question=feedback_data.user_question, bot_response=feedback_data.bot_response,
            error_message=f"HTTPException: {http_exc.detail}"
        )
        raise http_exc
    except Exception as e:
        logger.error(f"Unexpected error during feedback submission: {str(e)}", exc_info=True)
        log_feedback_to_file(
            username=feedback_data.username, user_email=feedback_data.user_email,
            feedback_value=feedback_data.feedback, feedback_text=feedback_data.feedback_text,
            user_question=feedback_data.user_question, bot_response=feedback_data.bot_response,
            error_message=f"Unexpected error: {str(e)}"
        )
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")


# ---------------------------------------------------------------------------
# Shutdown hooks
# ---------------------------------------------------------------------------
import atexit
atexit.register(_flush_stats)

@app.on_event("shutdown")
def _on_shutdown():
    _flush_stats()
    logger.warning(f"Shutting down with {len(conversation_sessions)} active sessions")


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import threading

    os.makedirs("utils", exist_ok=True)

    logger.warning(
        f"SRE-Copilot starting — model={LOCAL_MODEL_NAME}, "
        f"mode={CONTEXT_EXPLAINER_MODE}, max_concurrent={_INFERENCE_SEMAPHORE_LIMIT}, "
        f"session_ttl={SESSION_TTL_SECONDS}s, session_cap={SESSION_MAX_COUNT}"
    )

    if SLACK_BOT_ENABLED:
        logger.warning("Slack bot is ENABLED - starting in separate thread")

        def start_slack_bot_thread():
            try:
                slack_handler = start_slack_bot(aggregator_url="http://localhost:8080", async_mode=True)
                logger.warning("Slack bot started successfully")
            except Exception as e:
                logger.error(f"Failed to start Slack bot: {e}")

        slack_thread = threading.Thread(target=start_slack_bot_thread, daemon=True)
        slack_thread.start()
    else:
        logger.warning("Slack bot is DISABLED - skipping startup")

    logger.warning("Starting Aggregator service on port 8080...")
    logging.getLogger("uvicorn.access").addFilter(_HealthCheckFilter())
    uvicorn.run(app, host="0.0.0.0", port=8080)
