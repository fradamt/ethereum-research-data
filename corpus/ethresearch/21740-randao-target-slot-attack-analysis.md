---
source: ethresearch
topic_id: 21740
title: RANDAO target slot attack analysis
author: jtapolcai
date: "2025-02-13"
category: Consensus
tags: [random-number-generator]
url: https://ethresear.ch/t/randao-target-slot-attack-analysis/21740
views: 213
likes: 4
posts_count: 1
---

# RANDAO target slot attack analysis

We demonstrate that Ethereum’s distributed randomness beacon (RANDAO) is highly vulnerable to manipulations in its current form. For example, if a lucrative slot is foreseen, staking entities may temporarily collude to control **33%** of the validators, enabling them to execute a series of RANDAO manipulation attacks and secure the target slot with a **99.5%** (!) success rate.

The attack works as follows: several epochs before the target slot, the adversary waits for an opportunity to secure favorable slots (e.g., tail slots) or perform a forking attack near an epoch boundary to gain leverage for manipulation. From that point onward, the adversary is highly likely to retain these favorable slots across epochs until the target slot.

This attack would even be efficient for the current largest staking pool, which controls **α=28%** of the [total PoS stake](https://dune.com/hildobby/eth2-staking). This gives the pool a **65%** probability of gaining control of any given slot. Although the adversary initially needs to sacrifice a few blocks to mount the attack, it can later retain its full 28% block share. This is because these adversarial slots enable the adversary to carry on the attack across many epochs. During the attack the adversary can choose among an average of 24 RANDAO outcomes (for α=28%) and select the one that both preserves the favorable slots for the next epoch and provides additional slots to cover the required sacrifice in the following epoch.

The detection of these attacks is quite difficult. Given an average of 24 RANDAO outcomes, the adversary possesses roughly 5 bits of manipulative power, so one would expect that 2.5 (half of them) slots would be missing on average. In practice, much less suffices: with our attack strategy an average of 1.1 slots are sacrificed, while an additional 0.5 honest slot is forked out. However, a few missed slots across several epochs are often attributed to network issues, making it hard to distinguish intentional manipulation from regular disruptions.

Our approach is a follow-up to [this ethresear.ch post](https://ethresear.ch/t/forking-the-randao-manipulating-ethereums-distributed-randomness-beacon/21414). The key novelty of this approach is that we provide a recursive construction to describe all possible attacks. For each epoch, we compute a near-optimal attack policy and evaluate the attack’s effectiveness via Monte Carlo simulations. Figures 7 and 8 below show how the new attack scheme significantly lowers the threshold at which an adversary becomes a serious threat to the chain. Such an adversary can not only secure virtually any future slot—or even an entire range of slots—but also deteriorates chain quality. What is worse, the high number of reorgs increases uncertainty for the average user.

[![fig_9](https://ethresear.ch/uploads/default/optimized/3X/5/8/58096e188496a1c24fe84fb8eb4c60d96be7acc7_2_661x500.jpeg)fig_9894×676 79.1 KB](https://ethresear.ch/uploads/default/58096e188496a1c24fe84fb8eb4c60d96be7acc7)

[![fig_10](https://ethresear.ch/uploads/default/optimized/3X/0/f/0fa2c022b99e4605384f49e48360b64f1d363918_2_672x500.jpeg)fig_101046×778 140 KB](https://ethresear.ch/uploads/default/0fa2c022b99e4605384f49e48360b64f1d363918)

[![table_1](https://ethresear.ch/uploads/default/optimized/3X/5/4/545f17e604ec76725e6127e7f807f5b41280b791_2_690x356.jpeg)table_11448×748 253 KB](https://ethresear.ch/uploads/default/545f17e604ec76725e6127e7f807f5b41280b791)

E-print: [János Tapolcai, Bence Ladóczki, Ábel Nagy, “Slot a la carte: Centralization Issues in Ethereum’s Proof-of-Stake Protocol”, Cryptology {ePrint} Archive, Paper 2025/219](https://eprint.iacr.org/2025/219)
