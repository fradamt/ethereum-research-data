---
source: ethresearch
topic_id: 5064
title: On malicious nodes and verifications in a shard
author: daniel-tung
date: "2019-02-27"
category: Sharding
tags: []
url: https://ethresear.ch/t/on-malicious-nodes-and-verifications-in-a-shard/5064
views: 1160
likes: 1
posts_count: 2
---

# On malicious nodes and verifications in a shard

What if a malicious user performs a Sybil attack of verification (not mining) - spawning a large number of non-mining nodes that verify and approve malicious transactions within a shard.

It does not cost much to create a lot of non-mining nodes, and if the number is huge enough it is very likely that a shard is full of them.

## Replies

**musalbas** (2019-02-27):

If they are not participating in the consensus, then what damage do you expect them to do? They would only be ‘approving’ invalid transactions for themselves.

