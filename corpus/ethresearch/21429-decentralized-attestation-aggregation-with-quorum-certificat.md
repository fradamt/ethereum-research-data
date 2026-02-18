---
source: ethresearch
topic_id: 21429
title: Decentralized Attestation Aggregation with Quorum Certification based Single-Slot-Finality
author: AmbitionCX
date: "2025-01-12"
category: Consensus
tags: [single-slot-finality]
url: https://ethresear.ch/t/decentralized-attestation-aggregation-with-quorum-certification-based-single-slot-finality/21429
views: 481
likes: 1
posts_count: 1
---

# Decentralized Attestation Aggregation with Quorum Certification based Single-Slot-Finality

Written by [@AmbitionCX](/u/ambitioncx) from Panta Rhei and [@Keccak255](/u/keccak255) from Titania Research. This proposal is a preliminary idea evaluation for another SSF (Single Slot Finality) solution.

## Introduction

In the current Ethereum consensus protocol, validators responsible for a specific slot are divided into different (maximal 64) committees. Within each committee, individual attestations are disseminated across a subnet, then collected and aggregated by an average of 16 aggregators.

EIP-7549, according to Pectra Upgrade, will move `committee index` outside of attestation structure. The subnet of attestation dissemination will be extended to all committees for one slot, 64 times larger than before. ~1024 aggregators are responsible to aggregate attestations in a slot. This EIP could be considered as a small step towards final SSF algorithm.

This post takes a step further by including all validators (of 32 slot) in a single slot scope, and every validator are able to become an aggregators (parallel aggregation). The subnet of validator scale is 32 times larger than EIP-7549. In another word, try to include attestations from all 1 million validators as many as possible.

For any SSF algorithm, refer to this [post](https://notes.ethereum.org/@vbuterin/single_slot_finality) from Vitalik, they have to consider how to process so many attestations in a single time slot. A algorithm have to answer the question:

- How many attestation are you going to collect and decide if a block can be finalized or not?
- Who is eligible to participate in the consensus process?

For example, Orbit SSF is going to build a small set of *“super committee”*, and validators with higher staking amount are more likely to participate in the super committee after EIP-7251. In this post, we answer the question with **Decentralized Attestation Aggregation** and **Quorum Certification based Finality**:

- Decentralized Attestation Aggregation: We allow all validators to be an aggregator, and attestations are grouped as a Quorum. Same quorum are merged together by different aggregator in parallel, and after multiple consolidation, attestations are compressed into beacon block body. If an aggregated attestation contains more than \frac{2}{3} of validator signatures, the block is considered finalized.
- Quorum Certification based Finality: Attestations in a finalized block receive rewards for their timely and accurate attestations. The remaining attestations are discarded. Therefore, becoming an aggregator and participating in the aggregation process can significantly increase the possibility of earning benefits.

### Decentralized Attestation Aggregation

- In current stage, attestations are disseminated in the scope of a subnet of committee, up to 2048 validators. After EIP-7549, attestations are disseminated in the scope of a slot, the length of aggregation_bits will become 2^{17}. If we simply turn the consensus protocol to single slot finality, where each epoch contain only one slot, The consensus have to deal with attestations from all validators, which currently is over one million, in a 12-second time slot.
- Compressing so many attestations in 12 seconds is a huge work and will put tremendous pressure on the underlying P2P network. No one can guarantee that this can be completed within the time limit. So, one option is to select a small group of validators in turn, and others can raise objections, but our main consideration is to include as many attestations as possible, and block will be finalized if the number of attestation exceeds a certain threshold.
- In this proposal we let all validator participate in the aggregation process, where every 32 attestations are merged together as a First-Level Group, and every 32 First-Level group merge together as a Second-Level Group (which contain up to 1,024 individual attestations). 32 Second-Level group merge together to form a Third-Level Group (up to 32,768 individual attestations) . Likewise, 32 Third-Level Group further merged into a single Fourth-Level Group (up to 1,048,576 individual attestations).
- From individual attestations to Fourth-Level Group, the attestation are collected and aggregated by every validator, and generate a final result of a single aggregated attestation.

### Quorum Certification based Finality

- As defined in Sync HotStuff consensus, Quorum Certification (QC) is “a set of signed votes on a block from a quorum of replicas in the same view.” A QC in HotStuff is collected by leader and represent that \frac{f+1}{2f+1} replicas hold the same opinion.
- In Ethereum, we define that a block finality can be achieved by a supermajority (2/3 of all validators). So, to Finalize a block, the Fourth-Level Group contain more than 700,000 individual attestations:

an attestation contain only GHOST votes (header selecting) for 1-slot finality case
- an attestation contain GHOST (header selecting) and Casper (previous block considering) for 3-slot finality case

A Fourth-Level Group with a *supermajority* is called a **Quorum Certification (QC)**, which is the proof a finality of a block

## Conclusion

The proposed approach of **Decentralized Attestation Aggregation** and **Quorum Certification based Finality** presents a scalable and inclusive solution for achieving SSF in Ethereum. By enabling all validators to participate in the aggregation process and leveraging a hierarchical grouping mechanism, the protocol can efficiently handle attestations from over one million validators within a 12-second slot. The introduction of Quorum Certification ensures that block finality is achieved through a supermajority consensus, aligning with Ethereum’s security and decentralization principles.

If you have any questions or suggestions, please feel free to reply, or contact me by [chenxuanamazing@gmail.com](mailto:chenxuanamazing@gmail.com)
