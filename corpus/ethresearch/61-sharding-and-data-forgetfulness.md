---
source: ethresearch
topic_id: 61
title: Sharding and data forgetfulness
author: BenMahalaD
date: "2017-08-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/sharding-and-data-forgetfulness/61
views: 2711
likes: 3
posts_count: 4
---

# Sharding and data forgetfulness

So I’ve read and watched a lot of discussion about the data availability problem  where an attacker holds on to some data at time of creation, but I don’t remember seeing any discussion about making sure that the data is evenly distributed across all nodes for all time (just only at the start).

What I mean is, if you have a large number of shards (~1000+), for which most clients only download some small fraction of the total data, how can you be sure some of data isn’t permanently lost if all clients eventually have to clear their data and re-download or prune to save space. I’m thinking on the decades to centuries timescale.

I guess a small number of archival nodes might be setup purely by altruistic people. Is this a threat to the network? In a highly sharded network, don’t you need the history to rebuild the state to act on it? For popular parts of the state, I can see some always sticking around, but what if there are parts of the history that haven’t been touched in a very long time. Like someone wants to make a transaction to a contract that hasn’t been used in decades.

I know you can use eraser codes to regenerate parts of blocks, but what if whole blocks (or the shard equivalent of blocks) get forgotten? It could create usability or consistency issues for long range contracts.

## Replies

**vbuterin_old** (2017-08-31):

So far the only answer we have is the statistical one: design the system so that, on average, well over a thousand people are storing the full state and history of each shard; that should be enough to ensure that the data does not get lost.

---

**BenMahalaD** (2017-08-31):

I’d be happy with a statistical argument if there was some incentive to make sure validators downloaded random parts of the state, but in order to process transactions they only need to download parts of the state that are affected by the transactions. So if there is some part of the state that isn’t used for a long time there isn’t any incentive to keep old transactions that only effect this part of the state up to date, and they could eventually be lost.

At least if my understanding is correct, I might be wrong here.

---

**vbuterin_old** (2017-09-03):

One idea we have that solves this problem is the introduction of *guaranteed scheduled calls*. Basically, someone can make an operation of the form “send a call from X to Y with details Z, 45 blocks from now”, and the creator of the block 45 blocks in the future would be required to create a block containing that call; if they do not then the block is invalid (OR they get penalized X ETH, and the next block maker would be required to add the block; X could start at 1 wei and double per block if desired). Note that these calls are fully dynamic, ie. any transaction could create scheduled calls to any account. Hence, nodes that wish to avoid getting penalized would need to either have the entire state of that shard themselves, or know that enough other nodes do that they can fetch it if needed. This could lead to a stable equilibrium.

