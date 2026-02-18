---
source: ethresearch
topic_id: 977
title: How many collations can fit in one period?
author: yhirai
date: "2018-02-01"
category: Sharding
tags: []
url: https://ethresear.ch/t/how-many-collations-can-fit-in-one-period/977
views: 1153
likes: 2
posts_count: 3
---

# How many collations can fit in one period?

In the [sharding spec](https://github.com/ethereum/sharding/blob/develop/docs/doc.md), I find no limits on the number of collations per shard per period.

Does this mean, the eligible proposer can add dozens of collations in a block of the main chain?  If yes, is `COLLATION_GASLIMIT` effective?  If no, what conditions am I failing to consider?

## Replies

**vbuterin** (2018-02-01):

One collation per shard per period.

---

**yhirai** (2018-02-01):

I saw your update!  Thanks.

