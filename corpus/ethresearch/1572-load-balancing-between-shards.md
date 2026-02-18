---
source: ethresearch
topic_id: 1572
title: Load balancing between shards
author: cspannos
date: "2018-03-30"
category: Sharding
tags: []
url: https://ethresear.ch/t/load-balancing-between-shards/1572
views: 3151
likes: 4
posts_count: 2
---

# Load balancing between shards

The [Sharding phase 1 spec](https://ethresear.ch/t/sharding-phase-1-spec/1407) notes that Super-quadratic sharding and load balancing is currently an active area of research and seems to prioritize all other areas above it (ie load balancing is the final phase of 6 phases). Is that because load balancing is considered the least difficult problem to solve and so it is listed last? What is the tradeoff for leaving it later?

Assuming that collator shuffling for every period relies on pseudo random generation and that `shard_count=100`, how does the Sharding Manager Contract actually determine the effective distribution of collations among shards? I have in mind this image from the very useful [Sharding Infograph](https://www.icloud.com/keynote/05Q0CUa8WRPrvPx0tVgLTri_A#Ethereum%5FSharding%5FInfographic):

[![shuffling](https://ethresear.ch/uploads/default/original/2X/f/f67d417801d753860d4eb7e368960cf05baca165.jpg)shuffling756×810 91.8 KB](https://ethresear.ch/uploads/default/f67d417801d753860d4eb7e368960cf05baca165)

To what extent does storage rent, currently prioritized at Phase 2, and [state size per shard](https://ethresear.ch/t/a-simple-and-principled-way-to-compute-rent-fees/1455), impact the need to solve load balancing sooner? If these areas do not necessitate solving the problem earlier what about the cross-shard transactions of Phase 4?

It’s not that I’m a cheerleader for load balancing, as important as it will eventually be. I’m just curious ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

Thanks,

Chris

## Replies

**vbuterin** (2018-03-31):

The reason why we’re delaying it is basically that it’s relatively low value with relatively high complexity. It’s worth it eventually, but having any scaling at all is priority #1.

