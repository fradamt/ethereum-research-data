---
source: ethresearch
topic_id: 1806
title: As-fast-as-possible shard chains with notarization
author: vbuterin
date: "2018-04-23"
category: Sharding
tags: []
url: https://ethresear.ch/t/as-fast-as-possible-shard-chains-with-notarization/1806
views: 2908
likes: 3
posts_count: 2
---

# As-fast-as-possible shard chains with notarization

The following is an example for a structure that could be used to enable fast shard chain collations.

Background:

- Proof of Activity: hybrid proof of work and proof of stake where for a block to be valid to build on top of, >=M out of a randomly selected N PoS validators need to vote on it.
- Sequential proof of work, specifically this latest protocol by Bram Cohen

Consider a PoA-like model where a collation can be made by a proposer, and then for it to be eligible for the next proposer to build on top of, the collation needs to be approved by at least 4 of a random sample of 7 notaries. The randomness is sourced from (i) a recent main chain block hash, and (ii) a hash preimage revealed by the proposer. For any collation, there is an infinite sequence of proposers that can make collations on top of it; that is, for every integer x >= 0, there is a proposer P. For a proposal by proposer P to be valid, it must contain sequential proof of work with difficulty factor D * x; D is adjusted via an on-chain game, targeting toward five seconds.

The intention is that collations on shards would normally come as fast as network latency, in a graph like this:

![image](https://ethresear.ch/uploads/default/original/3X/f/e/fe65788e6e28e0ebc7941ae219b8c4df7efb3c39.svg)

And if at any point proposer 0 for the next collation is missing, then the chain would stop for ~5 seconds, at which point proposer 1 would be able to make a collation.

The notarizations would serve three purposes:

- Directly notarizing the collations they are building on top of
- Being a de-facto committee approving the shard chain (the main chain meta-committee would listen to the longest chain in this mechanism)
- Being Casper votes in the main-chain Casper FFG cycle

## Replies

**jamesray1** (2018-04-24):

Interesting! I read up to p. 12 of the first paper, it has interesting implications for incentivization, e.g. with [EIP-908](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-908.md). One question that naturally arises is how to get fast shard chain collations in the context of full PoS with Casper CBC. You need another randomness source.

