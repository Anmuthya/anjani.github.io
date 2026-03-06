---
layout: default
title: "Blog Archive — Anjani Kumar Muthyala | DevOps, AI & Cloud Articles"
description: "Browse all blog posts by Anjani Kumar Muthyala on DevOps, AWS, Kubernetes, Terraform, AI automation, and cloud infrastructure."
permalink: /archive/
keywords: "Anjani Kumar Muthyala blog, DevOps articles, AWS tutorials, Kubernetes guides, AI automation posts"
---

<div class="archive-container">
    <header class="archive-header animate-on-scroll">
        <div class="section-label">All Posts</div>
        <h1>Blog <span class="text-gradient">Archive</span></h1>
        <p>All articles, organized by date</p>
    </header>

    {% if site.posts.size > 0 %}
        {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
        
        {% for year in posts_by_year %}
            <section class="archive-year animate-on-scroll">
                <div class="archive-year-header">
                    <h2>{{ year.name }}</h2>
                    <span class="year-count">
                        {{ year.items.size }} post{% if year.items.size != 1 %}s{% endif %}
                    </span>
                </div>
                
                <div class="archive-list">
                    {% for post in year.items %}
                        <article class="archive-item">
                            <div class="archive-item-content">
                                <h3>
                                    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                                </h3>
                                
                                <div class="archive-item-meta">
                                    <time datetime="{{ post.date | date_to_xmlschema }}">
                                        <i class="fas fa-calendar-alt"></i>
                                        {{ post.date | date: "%B %d, %Y" }}
                                    </time>
                                    
                                    {% if post.category %}
                                        <span>
                                            <i class="fas fa-folder"></i>
                                            {{ post.category }}
                                        </span>
                                    {% endif %}
                                    
                                    {% if post.tags.size > 0 %}
                                        <span>
                                            <i class="fas fa-tags"></i>
                                            {% for tag in post.tags limit:2 %}{{ tag }}{% unless forloop.last %}, {% endunless %}{% endfor %}{% if post.tags.size > 2 %}…{% endif %}
                                        </span>
                                    {% endif %}
                                </div>
                                
                                {% if post.excerpt %}
                                    <p class="archive-item-excerpt">
                                        {{ post.excerpt | strip_html | truncate: 180 }}
                                    </p>
                                {% endif %}
                            </div>
                            
                            <div class="archive-item-action">
                                <a href="{{ post.url | relative_url }}" class="btn btn-primary" style="padding:0.5rem 1rem;font-size:0.78rem;">
                                    Read <i class="fas fa-arrow-right" style="font-size:0.65rem;"></i>
                                </a>
                            </div>
                        </article>
                    {% endfor %}
                </div>
            </section>
        {% endfor %}
        
        <div class="archive-end animate-on-scroll">
            <h3>Thanks for Reading!</h3>
            <p>
                That's all {{ site.posts.size }} post{% if site.posts.size != 1 %}s{% endif %} so far.
                New content is published regularly — check back soon!
            </p>
            <div class="archive-end-links">
                <a href="{{ '/' | relative_url }}" class="btn btn-primary">
                    <i class="fas fa-home"></i> Back to Home
                </a>
                <a href="{{ '/about' | relative_url }}" class="btn btn-outline">
                    <i class="fas fa-user-astronaut"></i> Get in Touch
                </a>
            </div>
        </div>
    {% else %}
        <div class="empty-state animate-on-scroll">
            <i class="fas fa-pen-fancy"></i>
            <h3>No posts yet!</h3>
            <p>This blog is just getting started. The first posts will appear here soon!</p>
            <div style="margin-top:1.5rem;">
                <a href="{{ '/' | relative_url }}" class="btn btn-primary">
                    <i class="fas fa-home"></i> Back to Home
                </a>
            </div>
        </div>
    {% endif %}
</div>
