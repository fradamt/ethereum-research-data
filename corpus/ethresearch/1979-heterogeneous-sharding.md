---
source: ethresearch
topic_id: 1979
title: Heterogeneous Sharding
author: elihanover
date: "2018-05-11"
category: Sharding
tags: []
url: https://ethresear.ch/t/heterogeneous-sharding/1979
views: 5065
likes: 1
posts_count: 2
---

# Heterogeneous Sharding

Heterogeneous sharding can be used to allow higher gas transactions on certain

shards without affecting other shards’ collation frequency.

Under the current Phase 1 implementation, we have collation body sizes of each shard

fixed at 1MB.  By allowing different shards different (but fixed) collation sizes,

we can allow higher gas transactions on certain shards, without altering period

length.

Instead of altering period length, we can instead grant notaries the ability to

submit collation headers up to floor(collation_size/1MB) - 1 periods ahead.

Additionally, we need to reward notaries proportional to the collation size of

the shard they have been assigned to to account for the additional time to download

and vote on the collation.

We also need to set the notary burst overhead to be proportional to the collation

size as well in order to give notaries time to download and vote on collation headers.

The main issue at hand is whether this interferes with random sampling from the

notary registry and consequently allows coordinated attacks on shards.

Another concern of heterogeneous sharding is dealing with preferences for accounts

on certain shards.  A contract that doesn’t require high gas transactions would

be better off on a low collation body size shard that will be verified every

period.  Assuming cross shard transactions, however, this should not be a problem,

as we can model the shard properties and determine the appropriate collation sizes

for an appropriate distribution of shards.  For example, the example above suggests

that we most likely would want to keep a significant majority of shards at the 1Mb

size such that they can be verified every period.

Determining the properties of shards also raises larger questions about governance

over the properties of shards.

## Replies

**jamesray1** (2018-05-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/elihanover/48/1336_2.png) elihanover:

> The main issue at hand is whether this interferes with random sampling from the
> notary registry and consequently allows coordinated attacks on shards.

My thoughts exactly. Generally, heterogenous sharding is more complicated, it is not even on the [sharding roadmap](https://github.com/ethereum/wiki/wiki/Sharding-roadmap), although I just added it. As you touched on, it increases the time to finality. We could also go the other way and have shards with a lower collation body size, which would increase time to finality, and would be appropriate for applications such as debit card payments. Generally, it will require careful design and analysis.

