---
source: ethresearch
topic_id: 23414
title: QSort - Fair Validator Selection through Quadratic Sortition and Aging Boost
author: alonmuroch
date: "2025-11-09"
category: Consensus
tags: []
url: https://ethresear.ch/t/qsort-fair-validator-selection-through-quadratic-sortition-and-aging-boost/23414
views: 160
likes: 1
posts_count: 2
---

# QSort - Fair Validator Selection through Quadratic Sortition and Aging Boost

## Summary

**QSort** introduces a new way to select validator committees that balances fairness, decentralization, and security — without the drawbacks of traditional delegated proof-of-stake (dPoS) systems.

It combines:

- Quadratic weighting (√stake) — to dampen whale dominance.
- Aging boost — to increase validators’ chances of selection over time.
- Verifiable random sortition — to ensure transparency and unpredictability.
- ⅔ coverage rule — to guarantee Byzantine fault-tolerant security.
- Delegation and un-staking queues — to keep stake changes smooth and predictable.

The result is a **stake-aware, time-fair, randomness-driven election mechanism** that ensures *everyone eventually gets a turn* — while preserving the same security guarantees as classical BFT systems.

## Challenges Of Delegated-PoS(dPos)

Most modern PoS networks rely on **Delegated Proof of Stake (dPoS)** systems, where token holders delegate voting power to a limited set of validators.

It’s simple and scalable — but comes with deep structural flaws:

[![Screenshot 2025-11-09 at 17.32.52](https://ethresear.ch/uploads/default/optimized/3X/0/1/01d5642676743c809c948b62c53afd14fbc66e1d_2_690x271.png)Screenshot 2025-11-09 at 17.32.521364×536 148 KB](https://ethresear.ch/uploads/default/01d5642676743c809c948b62c53afd14fbc66e1d)

These issues lead to *oligopolies* — validator sets that barely change, controlled by a handful of entities.

Even when randomness is added (e.g., via lotteries), without proper weighting and fairness mechanisms, these systems either:

- Overcompensate and destabilize (too random), or
- Undercompensate and stagnate (too deterministic).

## QSort

### Design Goals

1. Stake matters, but doesn’t dominate — large validators still secure the network, but with diminishing returns on influence.
2. Fairness compounds over time — each validator’s probability of selection increases the longer they’ve been out of committee.
3. Validator rotation is continuous and verifiable, driven by publicly verifiable randomness.
4. Stake movement doesn’t destabilize consensus, thanks to bounded activation and exit queues.
5. Security is provable — each committee always represents ≥⅔ of total stake, the same threshold used by Byzantine Fault Tolerant protocols to guarantee both safety and liveness.

### Delegation — The Foundation of Trust

Token holders delegate stake to validators they trust.

Delegation defines the **economic backing** behind each validator, but does not automatically translate to power.

Instead, it feeds into a *weighted random selection process* that determines committee membership each epoch.

When new delegations or withdrawals happen, they enter queues (explained later) to avoid destabilizing rapid validator turnover.

## Quadratic Votes — Diminishing Returns for Whales

Traditional stake weighting gives large validators linear power:

more stake → more influence → permanent dominance.

QSort introduces **quadratic weighting**:

[![Screenshot 2025-11-09 at 17.33.33](https://ethresear.ch/uploads/default/optimized/3X/8/b/8b6d17ff2ee5cee5187ac5c86d9cbc15329d5833_2_689x273.png)Screenshot 2025-11-09 at 17.33.331346×534 90.4 KB](https://ethresear.ch/uploads/default/8b6d17ff2ee5cee5187ac5c86d9cbc15329d5833)

This transformation introduces **diminishing returns**:

- Doubling stake only increases selection weight by ~41%.
- Smaller validators remain statistically relevant.
- Whales can’t fully monopolize committee spots.

Quadratic voting preserves stake as the main source of security while softening its centralizing effects.

## Aging Boost — Temporal Fairness

In pure random systems, some validators may get unlucky and never be selected.

QSort introduces **Aging Boosts** — a fairness correction that increases selection odds the longer a validator stays unselected.

Each epoch:

[![Screenshot 2025-11-09 at 17.33.55](https://ethresear.ch/uploads/default/optimized/3X/4/b/4b27633bcc50bd7ec76e37ff5983f4d8589702ed_2_690x347.png)Screenshot 2025-11-09 at 17.33.551328×668 152 KB](https://ethresear.ch/uploads/default/4b27633bcc50bd7ec76e37ff5983f4d8589702ed)

When selected, a validator’s aging counter resets.

Over time, this ensures that *every validator’s chance of inclusion rises predictably* — no one gets stuck on the sidelines forever.

## Sortition — Verifiable Random Shuffling

Each epoch begins with a **verifiable, deterministic random seed** derived from any unbiased randomness beacon or pseudo-random function (e.g., RANDAO, drand, VRF aggregation).

Using that seed, the protocol **shuffles all active validators** into a random order — this is called **sortition**.

[![Screenshot 2025-11-09 at 17.34.16](https://ethresear.ch/uploads/default/optimized/3X/5/d/5d8ae7340e2b986418ad11fa8b9484f7b6aa09db_2_690x194.png)Screenshot 2025-11-09 at 17.34.161354×382 133 KB](https://ethresear.ch/uploads/default/5d8ae7340e2b986418ad11fa8b9484f7b6aa09db)

This is a deterministic **[Fisher–Yates shuffle](https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle)** using the random seed.

Anyone can recompute it and verify that the selection order is honest and tamper-proof.

## Replies

**MicahZoltu** (2025-11-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/alonmuroch/48/4817_2.png) alonmuroch:

> Quadratic Votes — Diminishing Returns for Whales

What stops validators from just spreading out over many keys?  If you punish validator consolidation, then you are incentivizing validators spreading out.  I believe this comes with costs to the network and in general we would prefer they consolidate along lines of decision making power.  At least when they are consolidated, we can see the problem.

