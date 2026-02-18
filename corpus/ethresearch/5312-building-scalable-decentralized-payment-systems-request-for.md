---
source: ethresearch
topic_id: 5312
title: Building Scalable Decentralized Payment Systems - Request for Feedback
author: adlerjohn
date: "2019-04-16"
category: Layer 2
tags: []
url: https://ethresear.ch/t/building-scalable-decentralized-payment-systems-request-for-feedback/5312
views: 5166
likes: 1
posts_count: 3
---

# Building Scalable Decentralized Payment Systems - Request for Feedback

Hello researchers,

I’ve recently uploaded a paper, co-authored with [@Mikerah](/u/mikerah), found here: [[1904.06441] Building Scalable Decentralized Payment Systems](https://arxiv.org/abs/1904.06441). If any of you could find the time to do a peer-review of the paper, or provide any insightful constructive criticisms, that would be much appreciated. Abstract below.

> Increasing the transactional throughput of decentralized blockchains in a secure manner has been the holy grail of blockchain research for most of the past decade. This paper introduces a scheme for scaling blockchains while retaining virtually identical security and decentralization, and discusses requirements for deploying such a solution in practice. We propose a layer-2 scaling technique using a permissionless side chain with merged block production similar to merged mining. The side chain only supports functionality to transact UTXOs and transfer funds to and from a parent chain in a practically trustless manner. Optimized implementation and engineering of client code, along with improvements to block propagation efficiency versus currently deployed systems, allow this side chain to scale well beyond the capacities exhibited by contemporary blockchains. Finally, a discussion on navigating the complex political landscape of the present-day blockchain space is explored in order to develop compelling steps towards deploying such a side chain in real-world conditions.

## Replies

**DZack** (2019-05-03):

Needs a name!

Unclear to me what the particular contribution is here compared to previous sidechain constructions — can we get a tldr?

---

**adlerjohn** (2019-05-03):

I personally call it Ethereum Cash (Ethereum Cash *is* Ethereum, but more scalable), though [@Mikerah](/u/mikerah)  hates that name.

I guess the novel-ness over the many many previous side chain ideas comes from the “merged consensus” mechanism. We note that single-operator Plasma is not permissionless, and that block withholding creates big problems (*i.e.*, mass exits for Plasma M[ore]VP). If we had a permissionless consensus protocol that discouraged block withholding, [we wouln’t need mass exits](https://ethresear.ch/t/pos-plasma-cash-with-sharded-validation/1486) and problem solved—moreso if the consensus protocol had similar guarantees as the parent chain’s consensus. To that end, we can take [merged mining](https://github.com/namecoin/wiki/blob/17a7956cad7c4f8f1aabf6e148d23a13b34988ed/Merged-Mining.mediawiki), cut out re-using proofs of work, and just allow miners (or, more generally, validators) to create both parent chain and side chain blocks in unison. Security is borrowed from the parent chain since what I just described is a commit chain. Essentially, we can use the parent chain as a timestamping server to prevent mining of long hidden chains, which is an endemic problem with merged mining.

An obvious criticism is that the scheme, if scaled to large blocksizes on the side chain, prohibits home users from full validating the chain. I don’t see this as a problem, as the same can be said for sharding: scalability is only achieved in a sharding context because not every client validates every transaction and instead relies on light-client proofs. In other words, the scheme we present makes no stronger assumptions than sharding.

As a bonus, the scheme can be improved by incorporating the [data availability of zk-roll_up](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477) (*i.e.*, just post all the data to a shard chain), but [unlike zk-roll_up it only needs the execution engine to support hashing, not hashing + verification of SNARKs](https://ethresear.ch/t/phase-one-and-done-eth2-as-a-data-availability-engine/5269).

As another bonus, the scheme can support any number of parallel side chains (let’s call them parachains for short) using the Ethereum chain to relay information between side chains. Heterogeneous sharding in a PoW context, if you will.

