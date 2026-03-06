---
layout: default
title: "About Anjani Kumar Muthyala — DevOps Engineer & AI Leader"
description: "Learn about Anjani Kumar Muthyala, Senior DevOps Engineer at Verizon with 8+ years experience in AWS, Kubernetes, AI automation, and cloud infrastructure."
permalink: /about/
keywords: "DevOps engineer, AWS expert, Kubernetes specialist, AI automation, cloud infrastructure, Verizon"
---

<div class="about-container">
    <header class="about-header animate-on-scroll">
        <div class="profile-avatar profile-avatar-lg">
            <div class="profile-avatar-ring">
                <img src="{{ '/assets/images/profile.jpeg' | relative_url }}" alt="Anjani Kumar Muthyala" loading="eager">
            </div>
        </div>
        <div class="section-label">About Me</div>
        <h1><span class="text-gradient">Anjani Kumar Muthyala</span></h1>
        <p class="about-role">Senior DevOps Engineer · AI Enthusiast · Cloud Architect</p>
    </header>

    <!-- INTRO -->
    <div class="about-section animate-on-scroll">
        <h2>Hello! 👋</h2>
        <p>I'm a Senior DevOps Engineer currently working at <strong>Verizon</strong>, specializing in building scalable infrastructure, implementing CI/CD pipelines, and exploring the exciting world of Agentic AI for autonomous system operations.</p>
        
        <p>With over <strong>8 years of experience</strong> in DevOps and cloud technologies, I've had the privilege of working with cutting-edge technologies and solving complex infrastructure challenges. I'm passionate about advancing AI-driven automation — particularly in autonomous planning, validation, and remediation systems.</p>

        <h3>What I Do</h3>
        <ul class="about-list">
            <li>
                <i class="fas fa-robot"></i>
                <div><strong>Agentic AI & Automation</strong> — Designing AI workflows on AWS Bedrock for autonomous infrastructure management</div>
            </li>
            <li>
                <i class="fas fa-cloud"></i>
                <div><strong>Cloud Infrastructure</strong> — AWS, GCP, Kubernetes orchestration, and container management</div>
            </li>
            <li>
                <i class="fas fa-cogs"></i>
                <div><strong>CI/CD Pipelines</strong> — Jenkins, Ansible, Terraform, and GitLab automation</div>
            </li>
            <li>
                <i class="fas fa-chart-line"></i>
                <div><strong>Monitoring & Observability</strong> — ElasticSearch, Splunk, SumoLogic, and custom alerting</div>
            </li>
        </ul>

        <h3>What You'll Find Here</h3>
        <ul class="about-list">
            <li>
                <i class="fas fa-code"></i>
                <div><strong>DevOps & Infrastructure</strong> — Real-world solutions, best practices, and lessons learned</div>
            </li>
            <li>
                <i class="fas fa-brain"></i>
                <div><strong>AI & Machine Learning</strong> — AI applications in infrastructure and automation</div>
            </li>
            <li>
                <i class="fas fa-tools"></i>
                <div><strong>Tool Reviews & Tutorials</strong> — Hands-on guides for the latest DevOps tools</div>
            </li>
            <li>
                <i class="fas fa-lightbulb"></i>
                <div><strong>Career Insights</strong> — Professional growth, certifications, and industry trends</div>
            </li>
        </ul>
    </div>

    <!-- TECH STACK -->
    <div class="about-section animate-on-scroll">
        <div class="section-label" style="justify-content:flex-start;margin-bottom:1.5rem;">Tech Stack</div>
        <h2>Technical <span class="text-gradient">Expertise</span></h2>
        <p>Technologies and tools I work with on a daily basis:</p>
        
        <div class="tech-grid">
            <div class="tech-card">
                <h4><i class="fas fa-cloud" style="margin-right:6px;"></i> Cloud & Infra</h4>
                <p>AWS · GCP · Kubernetes · Docker · Terraform</p>
            </div>
            <div class="tech-card">
                <h4><i class="fas fa-robot" style="margin-right:6px;"></i> AI & Automation</h4>
                <p>AWS Bedrock · LangFlow · Gemini · Python</p>
            </div>
            <div class="tech-card">
                <h4><i class="fas fa-rocket" style="margin-right:6px;"></i> CI/CD Tools</h4>
                <p>Jenkins · Ansible · GitLab · Spinnaker</p>
            </div>
            <div class="tech-card">
                <h4><i class="fas fa-chart-bar" style="margin-right:6px;"></i> Monitoring</h4>
                <p>ElasticSearch · Splunk · SumoLogic · Nagios</p>
            </div>
        </div>

        <div class="cert-section" style="margin-top:2rem;">
            <h3>Certifications</h3>
            <div style="display:flex;justify-content:center;gap:0.75rem;margin-top:1rem;flex-wrap:wrap;">
                <span class="cert-badge"><i class="fas fa-award"></i> Google Cloud Gen AI Leader</span>
                <span class="cert-badge"><i class="fas fa-award"></i> Red Hat — Ansible Automation</span>
                <span class="cert-badge"><i class="fas fa-award"></i> AWS Solutions Architect — Associate</span>
            </div>
        </div>
    </div>

    <!-- CONNECT -->
    <div class="about-section animate-on-scroll">
        <h2>Let's <span class="text-gradient">Connect!</span></h2>
        <p>I love connecting with fellow DevOps engineers, AI enthusiasts, and technology professionals. Feel free to reach out!</p>
        
        <div class="connect-links">
            {% if site.social.github %}
                <a href="https://github.com/{{ site.social.github }}" target="_blank" rel="noopener" class="connect-link">
                    <i class="fab fa-github"></i> GitHub
                </a>
            {% endif %}
            {% if site.social.twitter %}
                <a href="https://twitter.com/{{ site.social.twitter }}" target="_blank" rel="noopener" class="connect-link">
                    <i class="fab fa-twitter"></i> Twitter
                </a>
            {% endif %}
            {% if site.social.linkedin %}
                <a href="https://linkedin.com/in/{{ site.social.linkedin }}" target="_blank" rel="noopener" class="connect-link">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </a>
            {% endif %}
            {% if site.email %}
                <a href="mailto:{{ site.email }}" class="connect-link">
                    <i class="fas fa-envelope"></i> Email
                </a>
            {% endif %}
            <a href="{{ '/assets/Anjani_Muthyala_Resume.pdf' | relative_url }}" target="_blank" rel="noopener" class="connect-link primary-link">
                <i class="fas fa-download"></i> Download Resume
            </a>
        </div>
    </div>

    <!-- ABOUT BLOG -->
    <div class="about-section animate-on-scroll">
        <h2>About This Blog</h2>
        <p>This blog serves as a platform to share my experiences and insights from working with cutting-edge technologies in the DevOps and AI space. As someone passionate about automation and innovation, I believe in documenting the journey and sharing knowledge with the community.</p>
        
        <p>From my current work on Agentic AI workflows for autonomous infrastructure management to practical DevOps solutions, I aim to provide valuable insights that can help other professionals in their own technology journeys.</p>
        
        <div class="about-closing">
            <p><strong>Thanks for visiting!</strong> Whether you're a fellow DevOps engineer, an AI enthusiast, or someone curious about technology, I hope you find something valuable here.</p>
        </div>
    </div>
</div>
