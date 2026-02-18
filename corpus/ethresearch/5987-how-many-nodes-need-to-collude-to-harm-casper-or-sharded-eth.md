---
source: ethresearch
topic_id: 5987
title: How many nodes need to collude to harm Casper or Sharded Eth?
author: Equilibrium94
date: "2019-08-16"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/how-many-nodes-need-to-collude-to-harm-casper-or-sharded-eth/5987
views: 1542
likes: 1
posts_count: 4
---

# How many nodes need to collude to harm Casper or Sharded Eth?

How many and can you explain why? (I’m familiar with big O notation) Thanks!

## Replies

**adlerjohn** (2019-08-17):

2/3+1 of 128 *i.e.*, 86 validators, of 32 ETH each.

How committee size for shards is determined:

https://medium.com/@chihchengliang/minimum-committee-size-explained-67047111fa20

How to bribe said committee:

https://nearprotocol.com/blog/how-unrealistic-is-bribing-frequently-rotated-validators/

---

**Equilibrium94** (2019-08-17):

Thanks! And and are the validators chosen pusdo randomly? And how often are they rotated out?

---

**vbuterin** (2019-08-18):

They are rotated once per epoch, with a lookahead period of one epoch.

