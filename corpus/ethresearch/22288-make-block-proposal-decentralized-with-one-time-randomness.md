---
source: ethresearch
topic_id: 22288
title: Make Block Proposal Decentralized With One-Time Randomness
author: killroy192
date: "2025-05-08"
category: Proof-of-Stake > Block proposer
tags: [proposer-builder-separation]
url: https://ethresear.ch/t/make-block-proposal-decentralized-with-one-time-randomness/22288
views: 159
likes: 0
posts_count: 1
---

# Make Block Proposal Decentralized With One-Time Randomness

## Intro

This proposal introduces a decentralized and incentive-aligned enhancement to Ethereum’s Proposer-Builder Separation (PBS). The goal is to diversify block builders, reduce censorship risk, and improve the profitability of honest and decentralized participants. Currently, ~80% of blocks are built by just two entities—an unsustainable trend that endangers Ethereum’s censorship resistance and neutrality.

## Proposal Summary

Under the existing model, Ethereum calculates base rewards using:

`base_reward = effective_balance * (base_reward_factor / (base_rewards_per_epoch * sqrt(sum(active_balance))))`

This proposal introduces a builder_factor, modifying the formula to:

`base_reward = effective_balance * builder_factor * (base_reward_factor / (base_rewards_per_epoch * sqrt(sum(active_balance))))`

`0 < builder_factor ≤ 1`

---

## How It Works

### 1. Builder Registration

- A block builder registers by committing a random seed (committed_seed) and staking ETH into a smart contract.

### 2. Builder Factor Per Block

For every block being considered for proposal, the builder’s effectiveness is determined dynamically using the static commitment and the live block_hash:

`builder_weight = uint256(keccak256(committed_seed, prev_block_hash))`

`builder_factor = builder_weight / builder_weight_max`

- This ensures that although builders commit randomness only once, the final score is block-specific due to the inclusion of prev_block_hash.
- Builders cannot precompute or game this value in advance, adding unpredictability without requiring continuous commitments.

---

## Benefits

###  Efficient Yet Randomized

- Builders commit randomness once, reducing overhead.
- Including prev_block_hash makes builder selection randomized (aka lottery).

###  Sybil Resistance

- Staking requirements limit spam registrations and ensure skin in the game.

###  Censorship Resistance

- Builders who exclude transactions risk being outscored by others and lose yield.

###  Confidential mempools

- Users and searchers know in advance who will be possibly the best builder is for the next block, potentially enabling more confidential mempools.

---

## System Flow

```plaintext
+------------------------------+
|  Block Builder               |
|  - Commits random_seed once  |
|  - Stakes ETH                |
+------------------------------+
          |
          v
+--------------------------+
|  For each new block:     |
|                          |
|  builder_weight =        |
|  uint256(keccak256(      |
|    random_seed,          |
|    prev_block_hash       |
|  ))                      |
|                          |
|  builder_factor =        |
|  builder_weight /        |
|  builder_weight_max      |
+--------------------------+
          |
          v
+--------------------------------------------+
|  Adjusted Block Reward:                     |
|                                            |
|  base_reward =                              |
|  effective_balance * builder_factor *       |
|  (base_reward_factor /                      |
|  (base_rewards_per_epoch *                  |
|  sqrt(sum(active_balance))))                |
+--------------------------------------------+
          |
          v
+--------------------------------------------+
|  Block Proposer Selects Most Profitable     |
|  Builder Based on Final Reward & MEV Yield  |
+--------------------------------------------+
```
