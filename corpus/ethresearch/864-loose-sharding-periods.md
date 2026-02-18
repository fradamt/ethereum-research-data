---
source: ethresearch
topic_id: 864
title: Loose sharding periods
author: JustinDrake
date: "2018-01-23"
category: Sharding
tags: []
url: https://ethresear.ch/t/loose-sharding-periods/864
views: 1722
likes: 0
posts_count: 5
---

# Loose sharding periods

The current sharding spec has fixed-length periods of 5 blocks during which validators can add collation headers to the VMC. There’s a tradeoff with period length:

- Nominal shard pace: Smaller periods increase the nominal shard pace.
- Hit rate: Larger periods increase the probability of validators hitting their periods.

The *actual* shard pace is the product of nominal shard pace and hit rate, and is something we want to optimise for. The *adversarial* hit rate is also important to optimise for security (to deal with e.g. main shard censorship, offchain DoS attacks, high network latency).

We suggest a collation proposal mechanism that relaxes the notion of period to improve actual shard pace and adversarial hit rate.

**Construction**

We call “strict periods” the old notion of fixed-length periods and build “loose periods” with two new rules:

1. Left extension: If a header is added in its respective strict period the next validator is allowed to add the next header in that same strict period.
2. Right extension: A validator that misses its respective strict period is allowed to add a header before the next header is added. In case conflicting headers are added in the same strict period, the fork choice rule gives precedence to the most recently selected validator.

## Replies

**vbuterin** (2018-01-23):

justin:

> Hit rate: Larger periods increase the probability of validators hitting their periods.

This is not the only reason to have longer period lengths; the other is to reduce the gas cost of the scheme (or, alternatively, increase the number of shards while keeping the same gas cost). A 2x longer period means a 2x more favorable tradeoff between main chain gas cost and total gas/sec of the shard layer (keeping gas/sec of each shard constant).

---

**denett** (2018-01-23):

For larger sharding periods, the block times in the shards also get longer. To get faster confirmation times in the shard, would it be possible to allow the active validator to propose multiple collations during his sharding period and only send the combined collation header to the main chain?

---

**vbuterin** (2018-01-23):

> To get faster confirmation times in the shard, would it be possible to allow the active validator to propose multiple collations during his sharding period and only send the combined collation header to the main chain?

The problem is that if the same validator makes all N collations, then the validator has the ability to easily revert any of them until the header is published, so it’s actually equivalent in terms of level of security to just making one big collation at the end.

---

**denett** (2018-01-23):

My idea was that the collations are signed and spread on the shards gossip channel. If the validator publishes a header on the main chain that does not contain all transactions of the signed collations, other validators could challenge him.

