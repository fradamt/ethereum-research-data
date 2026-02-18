---
source: ethresearch
topic_id: 13357
title: Full nodes behind TOR and other proxies
author: p_m
date: "2022-08-12"
category: Networking
tags: []
url: https://ethresear.ch/t/full-nodes-behind-tor-and-other-proxies/13357
views: 1879
likes: 3
posts_count: 2
---

# Full nodes behind TOR and other proxies

Currently it’s impossible to run full node behind censorship-resistant proxies such as tor. This poses a problem for nodes; and even bigger trouble for stakers.

As far as I understand, TOR doesn’t support UDP while it’s required for current gossip. What’s needed to be kept in mind while designing an alternative networking protocol? How feasible is this, at all?

## Replies

**Dormage1** (2022-08-13):

LLARP (Low-Latency Anonymous Routing Protocol) and it’s reference implementation Lokinet supports UDP.

