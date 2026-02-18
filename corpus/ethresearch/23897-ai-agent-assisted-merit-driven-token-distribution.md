---
source: ethresearch
topic_id: 23897
title: AI Agent assisted merit driven token distribution
author: Citrullin
date: "2026-01-20"
category: Economics
tags: []
url: https://ethresear.ch/t/ai-agent-assisted-merit-driven-token-distribution/23897
views: 116
likes: 0
posts_count: 1
---

# AI Agent assisted merit driven token distribution

The way we handle token distributions right now is broken.

Most DAO projects follow a depressing, predictable cycle.

They launch with **massive hype**, get swamped by engagement theatre and professional airdrop farmers. once incentives run out, they just **collapse**.

We like to pretend **DeFi** is different from TradFi, but in many ways, it’s actually **worse**.

In **TradFi**, the distribution of new money favors a tiny established **elite**.

In **crypto**, we just swapped those elites for **airdrop farmers, malicious actors, VC elite and insiders.**

Arguably, the extractive destruction of the system has become a little more decentralized.

History shows when **distribution gets out of hand**, it leads to destruction, low trust, and eventually, **total system failure**.

You can’t build a house on a weak foundation. Let’s fix the foundation.

**TinyMeritRank** tries to address this in antoher way.

It’s not just another airdrop tool. It’s a protocol designed to replace attention farming with **verifiable advancement farming**.

## Soulbound Agents & Directed Trust

Instead of letting bots run wild, we give every human exactly **one soulbound AI agent.**

These agents handle the heavy lifting in the DAO operation.

Monitoring activity, proposing contributions (like Microblock sets shared on social media or Tinyblock), and evaluating contributions.

The idea is heavily influenced by the [MeritRank paper](https://arxiv.org/pdf/2207.09950v2), which proves that Sybil-resistant reputation can be achieved.

By using **Personalized PageRank (PPR)**, the system ensures that reputation doesn’t just appear out of nowhere.

It flows along explicit, on-chain directed trust relationships.

The reputation R_{i}(j) that agent i assigns to agent j looks like this:

R_{i}(j)=(1-d)\cdot s_{i}(j)+d\cdot\sum_{k\rightarrow j}\left(\frac{w_{kj}}{out_{k}}\right)\cdot R_{i}(k)

**Damping factor (d):** Fixed at 0.85 (the probability of following a trust link).

**Teleport probability (1-d):** 0.15 probably to jump back to the seed set. In order to be not stuck in a cluster.

**Endorsement Weight (w_{kj}):** Based on your history of agreeing with others in committees.

**Outgoing Endorsement Weight:** total outgoing endorsement weight of k (Σ w_{k·})

## The Merit Epoch

Every 30 days (the epoch length), the system calculates rewards.

Agents must submit a Merkle root of their reputation vector to stay eligible.

The tokens an agent receives (T_{i}^{\tau}) depend on their own work, the network’s total work, and how much the network trusts them:

T_{i}^{\tau}=E^{\tau}\times\left(\frac{M_{i}^{\tau}}{\sum_{j}M_{j}^{\tau}}\right)\times R_{i}^{\tau}(i)

E^{\tau}: Total tokens minted this epoch.

M_{i}^{\tau}: Your raw merit points, earned by having your contributions evaluated.

\sum_{j}M_{j}^{\tau}: The network-wide total merit points.

R_{i}^{\tau}(i): Your verified self-reputation.

### System Resiliance

This system isn’t aiming for a perfect system because humans aren’t perfectly rational actors.

Instead, it can be built with several safety valves:

**Reward Locking:** The DAO can decide to lock epoch distributions for a specific time.

This allows the community to peer-review the epoch and slash past distributions if malicious behavior is discovered after the fact.

**Adjustable Decay:** If there’s a rampant rise in attackers, the DAO can adjust the decay mechanisms to make attacking the network even more expensive.

**Evidence-Based:** Any adjustment or slashing must be based on provable evidence of attacks on the network.

## Decay mechanism

1. Connectivity decay
κ(i,j) = max node-disjoint paths from i to j
if κ(i,j) ≤ 2 ⇒ Rᵢ(j) ← 0.90 · Rᵢ(j)
2. Monthly temporal decay (once per epoch)
Rᵢ(j) ← (1−γ) · Rᵢ(j) + ΔR_n γ = 0.05
3. Slashing decay
Proven malice leads to large multiplicative penalty (up to zero). See table.

## Two-Stage Evaluation

To ensure we reward real advancement, every contribution goes through two stages:

1. Stage 1 (Relevance Filter):  A 7-member committee (stratified sampled) checks if a proposal (an IPFS CID) is actually worth the network’s time.
It needs a 5-of-7 threshold signature to be committed on chain.
2. Stage 2 (Deliberative Scoring):  This expands to up to 200 agents. Depending on needs.
They engage in gossip rounds via Ceramic streams, providing both a score (0-100) and natural-language reasoning.
The evaluation only stops when the scores converge (standard deviation \le 5\% of the mean) or maximum rounds are reached without consensus. Contribution can be picked up again by another commitee.

## Example Tokenomics

| Allocation | Share | Notes |
| --- | --- | --- |
| Total supply cap | 1B | Hard cap. |
| Community epochs reserve | 25% | Distributed via the T_{i}^{\tau} formula. |
| DAO treasury | 25% | Allocated for grants and ongoing operations. |
| Team / early seeds | 20% | Subject to a 4-year linear vesting schedule. |
| Liquidity infrastructure | 30% | Dedicated to network liquidity. |
| Post-cap inflation | 2% p.a. | Can be adjusted by the DAO once the cap is hit. |

## Making Malice Unprofitable

The goal is to create a **self-healing system**. By making malicious acts expensive and identifying them through merit evaluation, we turn the system into a trap for bad actors.

| Violation | Penalty |
| --- | --- |
| Abandoning committee | 2% to 100% escalating slash. |
| Same 7-tuple >10 consecutive evaluations | 10% slash and a forced rotation of the committee. |
| Cartel formation (>20% meta-assessments) | 25–100% slash and a total reputation freeze. |
| Faking deletion / content availability | Full slash resulting in R=0. |
| Missing or late Merkle root publication | Exclusion from rewards and committees for the current epoch. |
| Provably incorrect PageRank vector | 10–100% slash triggered via the challenge game. |
| Sybil (multiple agents per human) | Burn of all tokens and all associated soulbound identities. |

TinyMeritRank is just one pillar of the Tinyblock ecosystem, but a critical one.

It **addresses the emotional, greedy nature of humans at distribution** level by making it more profitable to build than to destroy.
