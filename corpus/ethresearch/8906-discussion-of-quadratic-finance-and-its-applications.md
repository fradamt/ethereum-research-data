---
source: ethresearch
topic_id: 8906
title: Discussion of Quadratic Finance and its Applications
author: mwt
date: "2021-03-12"
category: Economics
tags: []
url: https://ethresear.ch/t/discussion-of-quadratic-finance-and-its-applications/8906
views: 1708
likes: 0
posts_count: 3
---

# Discussion of Quadratic Finance and its Applications

Hi,

I wrote an in-depth blog post about quadratic finance and how it has been implemented.

https://mattwthomas.com/blog/fund-open-source/

It describes the mechanism and clears up some confusions about what it does and doesn’t do.

It also points out that implementations of QF/LR/CQF/CLR have actually implemented something entirely different from any of those mechanisms.

I hope people find it interesting.

## Replies

**kakia89** (2021-03-21):

What is so special about quadratic/square root, couldn’t it be (any) other functional form that satisfies Jensen’s inequality? From your post, it seems the only place functional form matters is to satisfy Jensen’s inequality.

---

**mwt** (2021-03-21):

Satisfying Jensen’s inequality means that it collects less revenue than you provide to the projects – i.e. that it is not self-funding. So, satisfying Jensen’s inequality is bad.

The special thing about the quadratic form is that it achieves the efficient allocation. I don’t show that it does this, but it is proven in the paper. There are other equations that satisfy this property. It’s just that the QF equation is especially simple.

