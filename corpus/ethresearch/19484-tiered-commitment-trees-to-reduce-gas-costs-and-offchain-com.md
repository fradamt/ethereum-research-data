---
source: ethresearch
topic_id: 19484
title: Tiered Commitment Trees to reduce gas costs and offchain complexity
author: rymnc
date: "2024-05-07"
category: Applications
tags: []
url: https://ethresear.ch/t/tiered-commitment-trees-to-reduce-gas-costs-and-offchain-complexity/19484
views: 1669
likes: 1
posts_count: 1
---

# Tiered Commitment Trees to reduce gas costs and offchain complexity

Discussion post for: [Verifying RLN Proofs in Light Clients with Subtrees | Vac Research](https://dev.vac.dev/rlog/rln-light-verifiers/)

cross-posted to: [Light RLN Verifiers using a Tiered Commitment Tree - Vac Rearch Blog Posts - Vac](https://forum.vac.dev/t/light-rln-verifiers-using-a-tiered-commitment-tree/290)

tl;dr: Implementation of a technique to decrease gas fees associated with a sparse Merkle tree on-chain, while simultaneously minimizing client-side requirements. This solution leverages the segmentation of root computation into subtrees. Notably utilized by projects like Penumbra and Polygon Miden, this approach also facilitates trustless availability of the Merkle tree root on-chain, even when using a zk-friendly hash function that is more costly within the EVM environment.

Can be used for Semaphore/RLN.
