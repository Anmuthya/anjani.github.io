---
layout: default
title: "Home"
---

<!-- ═══ HERO ═══ -->
<section class="hero animate-on-scroll">
    <div class="hero-content">
        <div class="profile-avatar">
            <div class="profile-avatar-ring">
                <img src="{{ '/assets/images/profile.jpeg' | relative_url }}" alt="Anjani Kumar Muthyala" loading="eager">
            </div>
        </div>
        <div class="hero-badge">
            <span class="status-dot"></span>
            Available for collaboration
        </div>
        <h1>
            Hi, I'm <span class="text-gradient">Anjani Kumar</span>
        </h1>
        <p class="hero-subtitle">
            Senior DevOps Engineer crafting scalable cloud infrastructure, CI/CD pipelines, and AI-driven automation systems at <strong style="color:var(--text-0);">Verizon</strong>.
        </p>

        <div class="terminal-window">
            <div class="terminal-bar">
                <span class="terminal-dot red"></span>
                <span class="terminal-dot yellow"></span>
                <span class="terminal-dot green"></span>
                <span class="terminal-title">zsh — anjani@cloud</span>
            </div>
            <div class="terminal-body">
                <div class="terminal-line">
                    <span class="terminal-prompt">❯</span>
                    <span class="terminal-cmd">whoami</span>
                </div>
                <div class="terminal-line">
                    <span class="terminal-arg" id="typewriter" data-words='["DevOps Engineer", "Cloud Architect", "AI Enthusiast", "Problem Solver"]'>DevOps Engineer</span><span class="terminal-cursor"></span>
                </div>
                <div class="terminal-line" style="margin-top:4px;">
                    <span class="terminal-prompt">❯</span>
                    <span class="terminal-cmd">cat</span>
                    <span class="terminal-flag">--stack</span>
                    <span class="terminal-arg">AWS · K8s · Terraform · Bedrock</span>
                </div>
                <div class="terminal-line">
                    <span class="terminal-prompt">❯</span>
                    <span class="terminal-cmd">echo</span>
                    <span class="terminal-comment"># deploying innovation...</span>
                </div>
            </div>
        </div>

        <div class="hero-actions">
            <a href="{{ '/about' | relative_url }}" class="btn btn-primary">
                <i class="fas fa-user-astronaut"></i> About Me
            </a>
            <a href="{{ '/assets/Anjani_Muthyala_Resume.pdf' | relative_url }}" target="_blank" class="btn btn-outline">
                <i class="fas fa-file-alt"></i> Resume
            </a>
            <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener" class="btn btn-ghost">
                <i class="fab fa-github"></i> GitHub
            </a>
        </div>
    </div>
</section>

<!-- ═══ STATS ═══ -->
<div class="stats-grid animate-on-scroll">
    <div class="stat-card">
        <span class="stat-number" data-count="8">0+</span>
        <span class="stat-label">Years Experience</span>
    </div>
    <div class="stat-card">
        <span class="stat-number" data-count="3">0+</span>
        <span class="stat-label">Certifications</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">AWS</span>
        <span class="stat-label">GCP · Azure</span>
    </div>
    <div class="stat-card">
        <span class="stat-number">AI</span>
        <span class="stat-label">GenAI · Agentic</span>
    </div>
</div>

<!-- ═══ EXPERTISE ═══ -->
<section class="animate-on-scroll">
    <div class="section-header">
        <div class="section-label">What I Do</div>
        <h2 class="section-title">Areas of <span class="text-gradient">Expertise</span></h2>
        <p class="section-desc">Building the future of infrastructure with AI-powered automation and cloud-native architecture</p>
    </div>

    <div class="features-grid">
        <div class="feature-card blue animate-on-scroll delay-1">
            <div class="feature-icon"><i class="fas fa-robot"></i></div>
            <h3>Agentic AI & Automation</h3>
            <ul>
                <li>AWS Bedrock workflows for autonomous infra management</li>
                <li>GenAI SRE assistants with RAG over process docs</li>
                <li>LangFlow pipelines for infrastructure automation</li>
            </ul>
        </div>

        <div class="feature-card green animate-on-scroll delay-2">
            <div class="feature-icon"><i class="fas fa-cloud"></i></div>
            <h3>Cloud Infrastructure</h3>
            <ul>
                <li>AWS & GCP cloud architecture and optimization</li>
                <li>Kubernetes orchestration & container management</li>
                <li>Infrastructure as Code with Terraform & Ansible</li>
            </ul>
        </div>

        <div class="feature-card purple animate-on-scroll delay-3">
            <div class="feature-icon"><i class="fas fa-cogs"></i></div>
            <h3>DevOps Excellence</h3>
            <ul>
                <li>CI/CD pipeline design and optimization</li>
                <li>Monitoring with ElasticSearch, Splunk, SumoLogic</li>
                <li>Configuration management and automation</li>
            </ul>
        </div>
    </div>
</section>

<!-- ═══ CERTIFICATIONS ═══ -->
<div class="certs-bar animate-on-scroll">
    <span class="cert-badge"><i class="fas fa-award"></i> Google Cloud Gen AI Leader</span>
    <span class="cert-badge"><i class="fas fa-award"></i> Red Hat — Ansible Automation</span>
    <span class="cert-badge"><i class="fas fa-award"></i> AWS Solutions Architect — Associate</span>
</div>

<!-- ═══ RECENT POSTS ═══ -->
<section class="posts-section animate-on-scroll">
    <div class="section-header">
        <div class="section-label">From The Blog</div>
        <h2 class="section-title">Recent <span class="text-gradient">Posts</span></h2>
        <p class="section-desc">Insights on DevOps, AI automation, and cloud infrastructure</p>
    </div>

    {% if site.posts.size > 0 %}
        <div class="posts-grid">
            {% for post in site.posts limit:3 %}
                <article class="post-card animate-on-scroll delay-{{ forloop.index }}">
                    {% if post.category %}
                        <span class="post-card-category">{{ post.category }}</span>
                    {% else %}
                        <span class="post-card-category">Blog</span>
                    {% endif %}
                    <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
                    <div class="post-meta">
                        <time datetime="{{ post.date | date_to_xmlschema }}">
                            <i class="fas fa-calendar-alt"></i> {{ post.date | date: "%B %d, %Y" }}
                        </time>
                        {% if post.tags.size > 0 %}
                            <span><i class="fas fa-tag"></i> {{ post.tags | first }}</span>
                        {% endif %}
                    </div>
                    <p class="post-excerpt">{{ post.excerpt | strip_html | truncate: 150 }}</p>
                    <a href="{{ post.url | relative_url }}" class="read-more">
                        Read more <i class="fas fa-arrow-right"></i>
                    </a>
                </article>
            {% endfor %}
        </div>
        
        <div style="text-align:center;margin-top:2rem;">
            <a href="{{ '/archive' | relative_url }}" class="btn btn-outline">
                <i class="fas fa-layer-group"></i> View All Posts
            </a>
        </div>
    {% else %}
        <div class="empty-state">
            <i class="fas fa-pen-fancy"></i>
            <h3>More posts coming soon!</h3>
            <p>This blog will feature deep dives into DevOps, AI automation, and cloud infrastructure.</p>
        </div>
    {% endif %}
</section>

<!-- ═══ CTA ═══ -->
<section class="cta-section animate-on-scroll">
    <div class="cta-content">
        <h2>Let's Build Something <span class="text-gradient">Together</span></h2>
        <p>Interested in DevOps, AI automation, or cloud infrastructure? Let's connect and share ideas.</p>
        <div class="cta-links">
            {% if site.email %}
                <a href="mailto:{{ site.email }}" class="cta-link cta-link-primary">
                    <i class="fas fa-envelope"></i> Email Me
                </a>
            {% endif %}
            {% if site.social.linkedin %}
                <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener" class="cta-link cta-link-ghost">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </a>
            {% endif %}
            {% if site.social.github %}
                <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener" class="cta-link cta-link-ghost">
                    <i class="fab fa-github"></i> GitHub
                </a>
            {% endif %}
            <a href="{{ '/assets/Anjani_Muthyala_Resume.pdf' | relative_url }}" target="_blank" class="cta-link cta-link-ghost">
                <i class="fas fa-download"></i> Resume
            </a>
        </div>
    </div>
</section>
