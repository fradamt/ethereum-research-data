---
source: ethresearch
topic_id: 13100
title: Implementing native rollups with precompiled contracts
author: nanfengpo
date: "2022-07-20"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/implementing-native-rollups-with-precompiled-contracts/13100
views: 2991
likes: 2
posts_count: 2
---

# Implementing native rollups with precompiled contracts

The definition of [enshrined rollups](https://www.reddit.com/r/ethereum/comments/vrx9xe/comment/if7auu7/) suggests to ZK-SNARK everything, including the execution layer. Here we propose an alternative design that launches a specific number (like 64) of rollups on the execution layer by using precompiled contracts. We call it [native rollups](https://ethresear.ch/t/rollup-as-a-service-opportunities-and-challenges/13051), which will bear part of the advantages of enshrined rollups.

## Precompiled Contracts & Rollup Slots

There are 64 pre-deployed contracts as “rollup slots,” which will be called directly by batch & proof transactions from rollups. These slots will call a precompiled contract for proof verification and update local state roots if successful. The precompiled contract can accelerate the verification of zero-knowledge proofs with optimizations in binary codes.

[![流程图](https://ethresear.ch/uploads/default/optimized/2X/f/f69b6515f11e15d1cade29f052664bd0d45b66e0_2_690x383.jpeg)流程图1167×649 54.5 KB](https://ethresear.ch/uploads/default/f69b6515f11e15d1cade29f052664bd0d45b66e0)

## Settlement Priority & Batch Reward

Batch & proof transactions successfully updating the state roots in rollup slots will be rewarded (to the block producer) with coins so that they will have a higher priority in the mempool and settle immediately. If not successful, they will be charged with gas, which is relatively low due to using the precompiled contract.

## Replies

**shakeib98** (2022-11-13):

Is this a kind of setllement rollup? And does your design also supports arbitrary code execution through any SC language?

