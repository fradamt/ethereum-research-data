---
source: ethresearch
topic_id: 1045
title: Enforcing windback consistency
author: JustinDrake
date: "2018-02-10"
category: Sharding
tags: []
url: https://ethresear.ch/t/enforcing-windback-consistency/1045
views: 1755
likes: 0
posts_count: 2
---

# Enforcing windback consistency

A key sharding security assumption is that validators perform “windback”. That is, before proposing a collation header to the VMC the corresponding validator first checks the availability and validity of the immediate `n` predecessors (e.g. `n = 25`). This windback parameter is a local policy for each validator and there is the risk that “lazy” validators using too low a windback parameter weaken overall security.

In this post we suggest a natural way to enshrine a global windback parameter in the VMC, increasing the incentives for validators to make their local windback parameter at least as large as the global windback parameter. (For a much more high-tech approach to enforcing windback see [this post](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949).)

**Construction**

Modify the `addHeader` method to return `False` (and revert) on a collation header `h` if the corresponding validator has previously called `addHeader` on a header `h'` where:

1. h' and h conflict, i.e. are on different forks
2. The parent of h' is one of the immediate GLOBAL_WINDBACK predecessors of h

**Discussion**

With this `GLOBAL_WINDBACK` rule, calling `addHeader` is:

1. Making a claim about the availability and validity of immediate predecessors
2. Accepting that future addHeader calls be consistent with that claim

Put differently, adding a collation header inconsistent with one of your previously added collations for reasons other than availability and validity is considered adversarial and prevented by the VMC.

Notice that this rule holds large validators to a stricter standard than small validators, as larger validators propose collation headers more frequently and are more likely to “get caught in their own net”. This feels like a good decentralising counterbalance against the economies of scale validator pooling may provide.

## Replies

**vbuterin** (2018-02-11):

I agree this is a strict improvement. However, I don’t think individual validators will be selected on individual shards frequently enough for this to matter. Also, large validators will just split up their deposits.

Edit: actually, how much does this really even give you? All that it says is that if you build on B, you can’t later build directly on a near ancestor of B; that’s a quite weak condition. You can make it even stronger by saying that if you build on B you can’t later build on a block that has a lower score than B. But does it do that much to significantly encourage watching what you’re building on?

