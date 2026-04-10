---
layout: default
title: "文章归档"
description: "黄金形态通APP：全部历史黄金（XAU/USD）行情分析文章归档，按时间倒序。"
keywords: "黄金文章归档,XAUUSD,黄金形态通"
permalink: /archive/
---

## 文章归档

{% assign sorted_posts = site.posts | sort: "date" | reverse %}

共 **{{ sorted_posts.size }}** 篇。

<ul class="archive-list">
{% for post in sorted_posts %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    <span class="archive-meta">（{{ post.date | date: "%Y-%m-%d %H:%M UTC" }}）</span>
  </li>
{% endfor %}
</ul>
