---
source: ethresearch
topic_id: 2302
title: Artificial beacon chain penalties
author: JustinDrake
date: "2018-06-20"
category: Sharding
tags: []
url: https://ethresear.ch/t/artificial-beacon-chain-penalties/2302
views: 1827
likes: 4
posts_count: 3
---

# Artificial beacon chain penalties

**TLDR**: We suggest a strategy to centralise validator penalties in the beacon chain via an artificial penalty scheme. The accounting trick simplifies the enforcement of [interest on margin and the forced ejection of validators](https://ethresear.ch/t/fixed-size-deposits-and-rewards-penalties-quad-leak/2073).

**Construction**

Let `SHARDS_MAX_PENALTY_PER_EPOCH` be the maximum penalty a validator is liable to within one epoch across all shards. Instead of applying shard penalties we apply a default penalty of `SHARDS_MAX_PENALTY_PER_EPOCH` per epoch in the beacon chain. To compensate for this artificial penalty every shard is awarded `SHARDS_MAX_PENALTY_PER_EPOCH / NUM_SHARDS`.

(For concreteness, if the only shard penalty is `2^-20 ETH` for every missed attestation on a canonical shard block, `NUM_SHARD = 2^7`, and there are `2^7` periods per shard, then `SHARDS_MAX_PENALTY_PER_EPOCH = 2^-6 ETH`.)

**Discussion**

The above accounting trick means that penalties accrue in the beacon chain only, i.e. shard balances cannot go negative. This makes it especially easy to charge interest on “margin” (any balance deficit below the 32 ETH deposit) and kick out validators if the margin grows too large.

Assuming the expected profit in the beacon chain (e.g. from crosslink and FFG rewards) for an active validator surpasses this artificial worst-case penalty then beacon chain balances can stay afloat.

If shards balances could go negative we would likely need a mechanism for the shards to inform the beacon chain when their balances get too low. This communication protocol would come at the cost of increased design complexity and beacon chain overhead.

## Replies

**vbuterin** (2018-06-20):

This seems reasonable, though I’d say giving award in *every* shard is excessive; you want to give rewards just in the places where the validator contributed.

---

**JustinDrake** (2018-06-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> you want to give rewards just in the places where the validator contributed

Yes that makes more sense ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

