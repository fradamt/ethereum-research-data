---
source: magicians
topic_id: 18613
title: Why does MLOAD cause memory expansion?
author: kladkogex
date: "2024-02-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/why-does-mload-cause-memory-expansion/18613
views: 450
likes: 1
posts_count: 1
---

# Why does MLOAD cause memory expansion?

In EVM MLOAD outside of the current memory range causes memory to expand, and charges the user.

Does anyone know why was this choice made ? It seems that EVM implementation could simply return zero and not expand memory.

Operating systems in similar situations do not allocate physical memory unless a nonzero write happens.
