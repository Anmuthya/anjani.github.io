---
layout: default
title: "Home"
---

<div class="hero">
    <div class="hero-content">
        <h1>Welcome to My Blog</h1>
        <p>Exploring the intersection of DevOps, Cloud Infrastructure, and AI-Driven Automation</p>
        <a href="{{ '/about' | relative_url }}" class="hero-cta">
            Learn More About Me
            <i class="fas fa-arrow-right"></i>
        </a>
    </div>
</div>

<section style="margin-bottom: 4rem;">
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 class="text-gradient">About Me</h2>
        <p style="color: var(--text-secondary); max-width: 700px; margin: 1rem auto;">
            I'm <strong>Anjani Kumar Muthyala</strong>, a Senior DevOps Engineer at Verizon with over 8 years of experience in cloud infrastructure, automation, and emerging AI technologies.
        </p>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-bottom: 3rem;">
        <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); padding: 2rem; border-radius: var(--border-radius-lg); border: 1px solid var(--primary-lighter);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: var(--primary-color); color: white; border-radius: var(--border-radius-md); margin-bottom: 1rem;">
                <i class="fas fa-robot" style="font-size: 1.5rem;"></i>
            </div>
            <h3 style="color: var(--primary-dark); margin-bottom: 1rem;">Agentic AI & Automation</h3>
            <ul style="color: var(--text-secondary); line-height: 1.8; padding-left: 1.25rem;">
                <li>AWS Bedrock workflows for autonomous infrastructure management</li>
                <li>GenAI SRE assistants with RAG over process documentation</li>
                <li>LangFlow pipelines for infrastructure automation</li>
            </ul>
        </div>

        <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); padding: 2rem; border-radius: var(--border-radius-lg); border: 1px solid rgba(16, 185, 129, 0.3);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: var(--accent-color); color: white; border-radius: var(--border-radius-md); margin-bottom: 1rem;">
                <i class="fas fa-cloud" style="font-size: 1.5rem;"></i>
            </div>
            <h3 style="color: var(--accent-dark); margin-bottom: 1rem;">Cloud Infrastructure</h3>
            <ul style="color: var(--text-secondary); line-height: 1.8; padding-left: 1.25rem;">
                <li>AWS and GCP cloud architecture and optimization</li>
                <li>Kubernetes orchestration and container management</li>
                <li>Infrastructure as Code with Terraform and Ansible</li>
            </ul>
        </div>

        <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); padding: 2rem; border-radius: var(--border-radius-lg); border: 1px solid var(--border-color);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: var(--text-secondary); color: white; border-radius: var(--border-radius-md); margin-bottom: 1rem;">
                <i class="fas fa-cogs" style="font-size: 1.5rem;"></i>
            </div>
            <h3 style="color: var(--text-primary); margin-bottom: 1rem;">DevOps Excellence</h3>
            <ul style="color: var(--text-secondary); line-height: 1.8; padding-left: 1.25rem;">
                <li>CI/CD pipeline design and optimization</li>
                <li>Monitoring and observability with ElasticSearch, Splunk, SumoLogic</li>
                <li>Configuration management and automation</li>
            </ul>
        </div>
    </div>

    <div style="background: var(--bg-secondary); padding: 2rem; border-radius: var(--border-radius-lg); text-align: center; border: 1px solid var(--border-color);">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary);">🎓 Certifications</h3>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span class="badge badge-primary">Google Cloud Gen AI Leader</span>
            <span class="badge badge-primary">Red Hat Certified Specialist in Ansible Automation</span>
            <span class="badge badge-primary">AWS Certified Solutions Architect - Associate</span>
        </div>
    </div>
</section>

<section>
    <div style="text-align: center; margin-bottom: 3rem;">
        <h2 class="text-gradient">Recent Posts</h2>
        <p style="color: var(--text-secondary);">Latest insights from DevOps, AI automation, and cloud infrastructure</p>
    </div>

    {% if site.posts.size > 0 %}
        <div class="posts-grid">
            {% for post in site.posts limit:3 %}
                <article class="post-card">
                    {% if post.category %}
                        <span class="post-card-category">{{ post.category }}</span>
                    {% else %}
                        <span class="post-card-category">Blog</span>
                    {% endif %}
                    
                    <h3>
                        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                    </h3>
                    
                    <div class="post-meta">
                        <time datetime="{{ post.date | date_to_xmlschema }}">
                            <i class="fas fa-calendar-alt"></i>
                            {{ post.date | date: "%B %d, %Y" }}
                        </time>
                        
                        {% if post.author %}
                            <span>
                                <i class="fas fa-user"></i>
                                {{ post.author }}
                            </span>
                        {% endif %}
                        
                        {% if post.tags.size > 0 %}
                            <span>
                                <i class="fas fa-tags"></i>
                                {{ post.tags | first }}
                            </span>
                        {% endif %}
                    </div>
                    
                    <p class="post-excerpt">
                        {{ post.excerpt | strip_html | truncate: 150 }}
                    </p>
                    
                    <a href="{{ post.url | relative_url }}" class="read-more">
                        Read More
                        <i class="fas fa-arrow-right"></i>
                    </a>
                </article>
            {% endfor %}
        </div>
        
        <div style="text-align: center; margin-top: 3rem;">
            <a href="{{ '/archive' | relative_url }}" class="hero-cta">
                View All Posts
                <i class="fas fa-arrow-right"></i>
            </a>
        </div>
    {% else %}
        <div style="background: var(--bg-secondary); padding: 3rem; border-radius: var(--border-radius-lg); text-align: center; border: 1px solid var(--border-color);">
            <i class="fas fa-edit" style="font-size: 3rem; color: var(--text-light); margin-bottom: 1rem;"></i>
            <h3 style="color: var(--text-primary);">More posts coming soon!</h3>
            <p style="color: var(--text-secondary);">
                This blog will focus on DevOps, AI automation, and cloud infrastructure insights.
            </p>
        </div>
    {% endif %}
</section>

<section style="margin-top: 5rem; padding: 3rem; background: linear-gradient(135deg, var(--primary-color), var(--accent-color)); border-radius: var(--border-radius-xl); text-align: center; color: white;">
    <h2 style="color: white; margin-bottom: 1rem;">Let's Connect</h2>
    <p style="color: rgba(255, 255, 255, 0.9); margin-bottom: 2rem; font-size: 1.125rem;">
        Interested in DevOps, AI automation, or cloud infrastructure? Let's connect and share ideas!
    </p>
    
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
        {% if site.email %}
            <a href="mailto:{{ site.email }}" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 1.5rem; background: white; color: var(--primary-color); border-radius: var(--border-radius-md); text-decoration: none; font-weight: 600; box-shadow: var(--shadow-lg); transition: var(--transition-smooth);">
                <i class="fas fa-envelope"></i>
                Email Me
            </a>
        {% endif %}
        
        {% if site.social.linkedin %}
            <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 1.5rem; background: rgba(255, 255, 255, 0.2); color: white; border: 2px solid white; border-radius: var(--border-radius-md); text-decoration: none; font-weight: 600; backdrop-filter: blur(10px); transition: var(--transition-smooth);">
                <i class="fab fa-linkedin"></i>
                LinkedIn
            </a>
        {% endif %}
        
        {% if site.social.github %}
            <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 1.5rem; background: rgba(255, 255, 255, 0.2); color: white; border: 2px solid white; border-radius: var(--border-radius-md); text-decoration: none; font-weight: 600; backdrop-filter: blur(10px); transition: var(--transition-smooth);">
                <i class="fab fa-github"></i>
                GitHub
            </a>
        {% endif %}
        
        <a href="{{ '/assets/AnjaniKumar_Muthyala_Resume.pdf' | relative_url }}" target="_blank" style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.875rem 1.5rem; background: rgba(255, 255, 255, 0.2); color: white; border: 2px solid white; border-radius: var(--border-radius-md); text-decoration: none; font-weight: 600; backdrop-filter: blur(10px); transition: var(--transition-smooth);">
            <i class="fas fa-download"></i>
            Resume
        </a>
    </div>
</section>

<style>
.hero-cta:hover,
a[href*="Email Me"]:hover,
a[href*="LinkedIn"]:hover,
a[href*="GitHub"]:hover,
a[href*="Resume"]:hover {
    transform: translateY(-2px);
    text-decoration: none !important;
}

a[href*="Email Me"]:hover {
    box-shadow: 0 20px 30px rgba(0, 0, 0, 0.2) !important;
}

a[style*="rgba(255, 255, 255, 0.2)"]:hover {
    background: rgba(255, 255, 255, 0.3) !important;
}

@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem !important;
    }
    
    .hero p {
        font-size: 1rem !important;
    }
}
</style>
