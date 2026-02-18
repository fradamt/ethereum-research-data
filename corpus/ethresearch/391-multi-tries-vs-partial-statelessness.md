---
source: ethresearch
topic_id: 391
title: Multi-tries vs partial statelessness
author: JustinDrake
date: "2017-12-28"
category: Sharding
tags: [stateless]
url: https://ethresear.ch/t/multi-tries-vs-partial-statelessness/391
views: 2683
likes: 0
posts_count: 2
---

# Multi-tries vs partial statelessness

In [another post](https://ethresear.ch/t/future-compatibility-for-sharding/386) it was highlighted that two ideas (namely multi-tries and partial statelessness) share similarities beyond both reducing witness sizes in the context of stateless clients. I will quickly recap the two ideas, and then show that multi-tries are actually better than partial statelessness in every respect I can think of.

- Multi-tries: Instead of using a single state trie, use 2^n tries thereby partitioning the account space according to n-bit account prefixes.
- Partial statelessness: Instead of storing just the state trie root, store the first n levels (aka the “top layer”).

Both ideas allow to reduce witnesses by n * 256 bits. However, below are reasons why multi-tries are better than partial statelessness:

1. Implementation complexity: Multi-tries feel easier to implement than partial statelessness because a multi-trie is simply multiple instantiations of a plain trie, whereas partial statelessness requires distinguishing the top layer from the bottom layer and requires extra logic to handle the different cases.
2. Parallelism: Multi-tries allow for highly parallel trie updates, whereas partial statelessness has a sequential bottleneck (the single trie root is a sequential bottleneck).
3. Storage: Multi-tries require n * 256 bits of storage, whereas partial statelessness requires up to (2n - 1) * 256 bits of storage.
4. Future-proofness: It is possible to implement partial statelessness optimisations on top of multi-tries, but not the other way round.

**TLDR**: Multi-tries FTW ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

## Replies

**vbuterin** (2017-12-29):

justin:

> Parallelism: Multi-tries allow for highly parallel trie updates, whereas partial statelessness has a sequential bottleneck (the single trie root is a sequential bottleneck).

This is technically not true; there is an algorithm that can do k updates to an n-sized trie in time k * log(n / k) which is parallelizable once you get past the top log(k) branches.

