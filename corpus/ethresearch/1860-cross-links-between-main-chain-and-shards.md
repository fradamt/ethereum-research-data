---
source: ethresearch
topic_id: 1860
title: Cross-links between main chain and shards
author: vbuterin
date: "2018-04-28"
category: Sharding
tags: [crosslinks]
url: https://ethresear.ch/t/cross-links-between-main-chain-and-shards/1860
views: 8511
likes: 9
posts_count: 8
---

# Cross-links between main chain and shards

The [minimal sharding spec](https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650) is relatively simple: for every 5-block main chain period, the start of that period is used as a source of randomness to select proposers and notary committees, and the committees need to publish their signatures into the main chain by the end of the period. The dependency graph looks like this:

![image](https://ethresear.ch/uploads/default/original/3X/4/c/4c9ba80a99d6dd40e37b51701ab17e03f4fc2210.svg)

However, this results in a fairly slow shard collation time. Suppose that we want to speed up shard collations to, say, four seconds. Then, we can do this:

![image](https://ethresear.ch/uploads/default/original/3X/3/4/3465df935c920c7dd0076eebbb7f403e46a39344.svg)

However, this creates a gaping hole, where shard collations cannot be processed during the time between when they are included into the main chain, and when the next period begins.

We can mitigate this by switching into a different paradigm, which I call *chain cross-linking*. Explaining with a diagram:

![image](https://ethresear.ch/uploads/default/original/3X/d/f/df346315634c2c7cad2c8fb4d60a76aba1e07440.svg)

The idea is that there are two types of cross-links, one going from the main chain to shards, and the other going from shards to the main chain. A shard-to-main-chain link must be signed off on by a committee, and the committee’s responsibility is to attest to the availability of all shard blocks since the last cross-link that was made for that shard (alternatively, in the meta-committee approach, a single meta-committee attests to the fact that for every shard, a committee has attested to the validity of some particular hash). Once an S2MC link is made, the validity of the main chain from that point depends on the validity of that shard chain; if a main chain contains a link to an invalid shard chain block, then that entire main chain past that point is to be considered invalid.

An S2MC link also establishes shard fork choice, using the “U rule”. To find the head of a shard chain:

- Start from the head of the main chain.
- Walk back to the latest main chain block that contains an S2MC link to that shard.
- Go to the shard collation referenced in that S2MC link.
- Walk forward to the head of the shard using that shard collation as a starting point / root, using the shard’s fork choice rule.

A main-chain-to-shard link can be signed off on by a single proposer in a shard; a proposer creating a collation on a shard can reference a main chain block, and that shard collation would then be dependent on both its direct parent and that main chain block for validity and for fork choice (that is, is the linked main chain block is not part of the canonical main chain, the shard collation cannot be part of the canonical shard chain). Notice that in both cases, the main chain drives the fork choice rule.

A not yet fully solved challenge is determining how to incentivize and when to allow cross-links.

## Replies

**NicLin** (2018-05-03):

> However, this creates a gaping hole, where shard collations cannot be processed during the time between when they are included into the main chain, and when the next period begins.

Can you elaborate more on this? Is the gap here referring to the time between M2 and S4*?

What are the shard collations that can not be processed during this gap, S3* or S1*~S3*?

And what is the reason that they can not be processed?

---

**vbuterin** (2018-05-03):

> Can you elaborate more on this? Is the gap here referring to the time between M2 and S4*?

The time between S3 and S4, to be precise. No new collations can be made during that interval.

---

**NicLin** (2018-05-05):

Can I say that tight coupling would then be combining these two links into one?

---

**vbuterin** (2018-05-05):

Tight coupling is making the dependency relationship in the second kind of cross-link (S2MC) enforceable (ie. if a shard collation is invalid, the blocks that contain it actually are also invalid).

---

**NicLin** (2018-05-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Once an S2MC link is made, the validity of the main chain from that point depends on the validity of that shard chain; if a main chain contains a link to an invalid shard chain block, then that entire main chain past that point is to be considered invalid.

So I guess S2MC is already enforceable in cross-link which means implementing cross-link would imply implementing tight coupling?

---

**xianfeng92** (2018-07-17):

[@vbuterin](/u/vbuterin) How to should  ensure the security  of S3 to S5 in Cross-links？

---

**vbuterin** (2018-07-17):

S51 and S52 have not received an inbound link from a main chain block that contained a crosslink from S31 and S32, so you can’t do something in S51 or S52 that depends on something done in S32 or S32.

