---
source: ethresearch
topic_id: 23085
title: "Community Feedback Wanted: Privacy-Focused ZK Rollup with EVM Compatibility"
author: chanderprakash20
date: "2025-09-21"
category: Layer 2 > ZK Rollup
tags: [zk-roll-up]
url: https://ethresear.ch/t/community-feedback-wanted-privacy-focused-zk-rollup-with-evm-compatibility/23085
views: 271
likes: 1
posts_count: 3
---

# Community Feedback Wanted: Privacy-Focused ZK Rollup with EVM Compatibility

[@vbuterin](/u/vbuterin) could please give your feedback

Hi everyone,

We’re building a new **ZK rollup that makes privacy as fundamental as scalability**, and we’d love to gather early feedback from the Ethereum community.

**The Problem:**

Layer 2 rollups have solved Ethereum’s throughput bottleneck but not its privacy problem. Today, balances, contract state, and transaction metadata remain public. Since Ethereum uses an account-based model, repeated activity can easily be linked to identities — opening the door to phishing, MEV extraction, reputational risk, and permanent data trails.

**Landscape today:**

Projects like **Aztec** and **Fhenix** are pushing the frontier here but leave key gaps:

- Aztec doesn’t yet support multi-user inputs and is still not  developing full EVM compatibility.
- Fhenix focuses on encrypted computation but doesn’t provide correctness proofs end-to-end, functioning more like a black box and not support privacy for every type of transaction

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

## Replies

**toml01** (2025-09-25):

Hi [@chanderprakash20](/u/chanderprakash20) ! Tom from Fhenix here.

Firstly, appreciate the feedback! I’d like to clarify and better understand some of the points you mentioned:

- The encrypted computations on Fhenix can be fully verified for correctness. The computation key (or: server key) is public and we do plan to introduce public commitments for the results, thus computations can be easily verified. Documentation about this can definitely be improved though, so point taken.
- What do you mean by “not support privacy for every type of transaction”? What exactly were you looking for that is missing?

Secondly, I’m curious why you see the need to design this as a rollup-based solution. If we already have protocols that achieve similar privacy guarantees directly at the L1 level (without the added complexity of L2 infrastructure), what’s the motivation for introducing another rollup? What does the L2 approach unlock that L1-based solutions don’t?

In any case, happy to see how more and more projects in this space, we’re growing ![:rocket:](https://ethresear.ch/images/emoji/facebook_messenger/rocket.png?v=14)

---

**chanderprakash20** (2025-09-27):

Hi Tom,

Thanks for your clarification. I’d like to elaborate on a few points:

1. FHE and verifiability: Currently, Fhenix does not implement Fully Homomorphic Encryption (FHE) with proof of correctness. While computations are private, there isn’t yet a mechanism to cryptographically prove that the computation itself was performed correctly. This is something we are actively exploring—specifically, how to combine FHE with zero-knowledge proofs to achieve both privacy and verifiability.
2. Transaction privacy limitations: Right now, simple account-to-account transactions on Fhenix are publicly visible, and bridging or asset swapping from L1 to Fhenix is also publicly observable. Our goal is to enhance the user experience by enabling privacy-preserving transactions while leveraging the existing Ethereum/EVM infrastructure, without requiring users to learn new tools or frameworks.
3. Why L2 / rollup approach: What we aim to deliver is a combination of:

 Privacy at scale,
4. Verifiability of computations, and
5. Compatibility with existing L1 tools and infrastructure.

Currently, many protocols can provide privacy **or** scale, but few can achieve **privacy with verifiable computations and scalability together** using existing tools. This is the gap we’re addressing.

