---
layout: default
title: "文章归档"
description: "黄金形态通APP：全部历史文章归档。"
permalink: /archive/
---

## 文章归档

{% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
{% for year in posts_by_year %}
### {{ year.name }}

{% assign posts_by_month = year.items | group_by_exp: "post", "post.date | date: '%m'" %}
{% for month in posts_by_month %}
#### {{ month.name }} 月

{% for post in month.items %}
- [{{ post.title }}]({{ post.url | relative_url }})（{{ post.date | date: "%Y-%m-%d %H:%M UTC" }}）
{% endfor %}

{% endfor %}

{% endfor %}
