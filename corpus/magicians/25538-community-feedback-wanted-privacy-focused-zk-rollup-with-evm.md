---
source: magicians
topic_id: 25538
title: "Community Feedback Wanted: Privacy-Focused ZK Rollup with EVM Compatibility"
author: chanderprakash20
date: "2025-09-21"
category: Uncategorized
tags: [evm]
url: https://ethereum-magicians.org/t/community-feedback-wanted-privacy-focused-zk-rollup-with-evm-compatibility/25538
views: 51
likes: 0
posts_count: 1
---

# Community Feedback Wanted: Privacy-Focused ZK Rollup with EVM Compatibility

Hi everyone,

[@vbuterin](/u/vbuterin)

We’re building a new **ZK rollup that makes privacy as fundamental as scalability**, and we’d love to gather early feedback from the Ethereum community.

**The Problem:**

Layer 2 rollups have solved Ethereum’s throughput bottleneck but not its privacy problem. Today, balances, contract state, and transaction metadata remain public. Since Ethereum uses an account-based model, repeated activity can easily be linked to identities — opening the door to phishing, MEV extraction, reputational risk, and permanent data trails.

**Landscape today:**

Projects like **Aztec** and **Fhenix** are pushing the frontier here but leave key gaps:

- Aztec doesn’t yet support multi-user inputs and is still not developing full EVM compatibility.
- Fhenix focuses on encrypted computation but doesn’t provide correctness proofs end-to-end, functioning more like a black box and not have privacy for every type  transaction .

**Our Approach:**

We’re developing a **privacy-preserving ZK rollup** that is fully EVM-compatible, supports multi-user input, and proves correctness without revealing transaction details. Instead of exposing balances or metadata, we commit encrypted state and ZK proofs back to Ethereum — ensuring finality and security while keeping user data shielded.

**Where we’d love your input:**

1. What tradeoffs do you see between privacy-by-default and data-availability in rollups?
2. Would you prefer privacy as default or opt-in when using L2 applications?
3. Which use cases most urgently need this (DeFi, DAOs, cross-chain apps, payments)?
4. What design pitfalls should we avoid when keeping privacy while maintaining Ethereum composability?

We want to build *with* the community, not in isolation. Your insights will help us validate assumptions and shape the right developer and user experience.

Looking forward to your thoughts!

—

Chanderprakash
