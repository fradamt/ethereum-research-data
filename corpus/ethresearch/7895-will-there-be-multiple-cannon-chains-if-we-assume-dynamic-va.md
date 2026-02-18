---
source: ethresearch
topic_id: 7895
title: Will there be multiple cannon chains if we assume dynamic validators?
author: lucian
date: "2020-08-24"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/will-there-be-multiple-cannon-chains-if-we-assume-dynamic-validators/7895
views: 1232
likes: 3
posts_count: 3
---

# Will there be multiple cannon chains if we assume dynamic validators?

The papers [Casper the Friendly Finality Gadget](https://arxiv.org/abs/1710.09437v4) and [Combining GHOST and Casper](https://arxiv.org/abs/2003.03052) have proved the safety: there is only one canon chain in any view.

But they assume there is only one global static validators set, while in the implementation, the validators are dynamic, which results in: at a specific time, different validators can see different validator sets instead of a global validator set.

In this case, we may have multiple canon chains without 1/3 validators get slashed. A simplified example is shown below:

[![casper_multiple_finalized_blocks](https://ethresear.ch/uploads/default/optimized/2X/2/29e11137df9a41b0490b88f13c7e0e4552551892_2_424x500.png)casper_multiple_finalized_blocks617×727 16.8 KB](https://ethresear.ch/uploads/default/29e11137df9a41b0490b88f13c7e0e4552551892)

The blocks are the epoch boundary blocks. All the arrows are justifications(since 2/3 validators vote). v2, v3 joined(or called “activated”) at Block<2a>. We can see Block<2a> and Block<3b> are finalized, and they are in different branches, while there is no validator slashed.

It rarely happens in the real situation, but it seems feasible in theory, so maybe it will happen in some tricky cases?

One of a naive solution to fix this I can figure out for now is not to let  active validators update util a block is finalized.(Some disadvantages are for example, some validators can not exit in time even when they are not able to be functional etc)

## Replies

**vbuterin** (2020-08-25):

> One of a naive solution to fix this I can figure out for now is not to let active validators update util a block is finalized.

This is actually the recommendation in the Casper FFG paper.

We do something somewhat different; we put a fairly low limit on how quickly validators can rotate in and out. See [annotated-spec/phase0/beacon-chain.md at d8c51af84f9f309d91c37379c1fcb0810bc5f10a · ethereum/annotated-spec · GitHub](https://github.com/ethereum/annotated-spec/blob/d8c51af84f9f309d91c37379c1fcb0810bc5f10a/phase0/beacon-chain.md#misc) and scroll down to **`CHURN_LIMIT_QUOTIENT`** for the explanation.

---

**kladkogex** (2020-08-26):

Also this

https://github.com/ethereum/eth2.0-specs/issues/1776

