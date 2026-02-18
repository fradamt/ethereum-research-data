---
source: magicians
topic_id: 27652
title: "Hegota Headliner: Partial Reconstruction and 2D PeerDAS"
author: leobago
date: "2026-02-04"
category: Magicians > Primordial Soup
tags: [hegota, headliner-proposal]
url: https://ethereum-magicians.org/t/hegota-headliner-partial-reconstruction-and-2d-peerdas/27652
views: 60
likes: 0
posts_count: 2
---

# Hegota Headliner: Partial Reconstruction and 2D PeerDAS

## Summary

This Headliner proposes advancing Hegota’s Data Availability Sampling (DAS) architecture by enabling **row-level data dissemination and partial reconstruction via cell-level messaging and two-dimensional (2D) PeerDAS**. Together, these changes significantly improve robustness, decentralization, and bandwidth efficiency of data availability under realistic network conditions.

The proposal builds on successful local row reconstruction in 1D PeerDAS and extends these capabilities to a native 2D design that supports fine-grained sampling, symmetric participation, and strong security guarantees per unit bandwidth.

Today’s dissemination structure at the CL is literally orthogonal to the way the data is disseminated at the EL. This mismatch is done on purpose to maximize sampling efficiency, but it also requires two complete dissemination phases. The proposal seeks to better integrate CL custody with EL blob dissemination and to leverage data already on the local node, both for custody-data dissemination and sampling.

The proposal does **not** require full 2D vertical expansion (i.e., erasure-code into the same number of blobs); it can start by just expanding into two or more rows, and then later on expand the erasure code into more rows using a strategy similar to how we do blob-parameter only (BPO) changes today.

## What is new

To help visualize what this change involves, in comparison to the current (Fusaka BPO2) state-of-the-art design, here we enumerate the extra steps:

1. Replace column custody by column-AND-row custody

Column data is disseminated the same way as of today (Full columns)
2. Row data can be acquired using getBlobsV3, then extend it (About 90% of blobs in mempool).
3. If the blob is not available locally, then get it through the network (Full rows)
4. This requires adding row gossipsub topics
5. We could keep a similar sampling strategy (columns and rows)
6. Vertical extension is done out of the fork-choice critical path

Full nodes extend their custody columns after receiving all the data they have to custody
7. Cell-level dissemination for extended rows

Full nodes disseminate the cells of their extended columns in the corresponding row topic

---

## Primary Benefits

### Native Partial Reconstruction

2D PeerDAS enables nodes to reconstruct subsets of data (i.e., individual rows and columns) without full-column custody. This:

- Reduces reliance on high-bandwidth “supernodes”
- Improves liveness under partial data withholding
- Allows availability recovery to scale with node capacity

Partial reconstruction becomes a first-class system property rather than an emergent behavior.

### Strong Security Under Low Bandwidth

By enabling **cell-level sampling and dissemination** and **efficient EL-CL interactions**, 2D PeerDAS improves **security per unit of network bandwidth**:

- Finer sampling granularity
- Harder-to-hide adversarial withholding
- Higher detection probability without increasing total network load

This yields more realistic and defensible availability guarantees than column-based approaches.

### More Symmetric Participation

2D PeerDAS reduces structural asymmetries by:

- Allowing heterogeneous nodes to contribute meaningfully
- Decreasing the need to store or transmit large column objects
- Supporting decentralized reconstruction without coordination bottlenecks

This aligns DAS more closely with Ethereum’s decentralization goals.

---

## Secondary Benefits

### Improved Mempool and Retrieval Compatibility

Row custody and dissemination paired with cell-level messaging integrate naturally with enhanced blob retrieval mechanisms (e.g., EIP-8077) and future sharded blob mempool strategies, improving:

- Recovery from missing or delayed blobs
- Resilience to nonce gaps and propagation failures
- Data availability UX for higher-layer protocols

### Cleaner Evolution Path for DAS

The transition from enhanced 1D partial reconstruction to full 2D PeerDAS establishes a clear architectural progression, reducing long-term protocol complexity and avoiding ad-hoc extensions to 1D designs.

---

## Why Now?

Several developments make this the right moment to advance DAS:

- Cell-level messaging is now viable and actively implemented
- Enhanced blob retrieval mechanisms are being explored and validated
- Data throughput requirements continue to rise
- Existing 1D PeerDAS designs are approaching practical limits

Delaying a principled move toward partial reconstruction and 2D sampling risks accumulating technical debt and locking in bandwidth-inefficient assumptions.

---

## Stakeholder Impact

### Positive

- Lower bandwidth and storage pressure
- More flexible and decentralized participation in reconstruction
- Improved resilience to adversarial withholding
- More reliable blob availability
- Stronger availability guarantees
- Faster recovery from partial failures

### Negative / Trade-offs

- Increased protocol complexity compared to baseline 1D PeerDAS
- Additional networking primitives for cell-level dissemination
- More involved encoding (2D) and sampling logic

These costs are mitigated by improved robustness, scalability, and long-term simplicity.

---

## Technical Readiness

- 2D erasure coding and sampling techniques are well understood
- Full DAS sampling strategies have been [analyzed](https://ethresear.ch/t/full-das-sampling-analysis/20912)
- Cell-level messaging has already solid [specs](https://github.com/ethereum/consensus-specs/pull/4558) and ongoing [implementation]( GitHub - libp2p/go-libp2p-pubsub: The PubSub implementation for go-libp2p )
- Blob mempool sharding strategies have been [studied](https://ethresear.ch/t/a-new-design-for-das-and-sharded-blob-mempools/22537)
- Enhanced blob retrieval mechanisms have been [proposed]( EIPs/EIPS/eip-8077.md at master · ethereum/EIPs · GitHub ) and [studied](https://ethresear.ch/t/eip-8077-nonce-gap-simulation-report/23687)
- Designs remain compatible with existing PeerDAS assumptions

This represents an incremental but decisive evolution, not a speculative redesign.

---

## Conclusion

Partial reconstruction and 2D PeerDAS represent a natural next step in the evolution of data availability for Hegota. By combining proven cell-level techniques with principled 2D constructions, this approach delivers stronger security, better decentralization, and improved bandwidth efficiency—while remaining aligned with Ethereum’s broader scaling roadmap.

## Replies

**cskiraly** (2026-02-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/leobago/48/16417_2.png) leobago:

> The proposal does not require full 2D vertical expansion (i.e., erasure-code into the same number of blobs); it can start by just expanding into two or more rows, and then later on expand the erasure code into more rows using a strategy similar to how we do blob-parameter only (BPO) changes today.

I think this part needs more explanation. Support for row-based reconstruction does not need 2D encoding. What it does need is:

- a row encoding: we already have that
- a row-wise communication method: we have that currently in the EL, but there are a few details that need to be fixed. We could also introduce it at the CL-level, as we’ve done in FullDAS.
- to make it really useful as the means to avoid relying on supernodes, we also need the results of these row-based roconstructions to feed back into the column channels. This is however easy, low-overhead, and in-fact the nim-lib2p based 2D FullDAS code always operated this way.

Where the 2D encoding comes in is allowing cheaper sampling. And, as you highlighted, this doesn’t even have to be on the critical path. I can easily imagine cell-based sampling serving delayed sampling needs. However, it is also to be said that cell-level samping can be implemented fast. We’ve implemented it in the FullDAS prototype.

Another note on the second dimension of encoding: it is not really about having to have a second Reed-Solomon encoding. The essence of it is to have an encoding once it is clear which blobs belong to the same block. It provides a code over the whole DA content bound to a block, enforcing all-or-nothing semantics, and allowing cheaper sampling at the same time.

Besides the second RS dimension, there are other constructs we can use. For example, I’ve published an RLC-based variant in the second FullDAS post.

