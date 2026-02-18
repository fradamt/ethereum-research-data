---
source: ethresearch
topic_id: 23682
title: Staircase Unrestricted Uncle Maker Attack
author: JingansiHandsomeman
date: "2025-12-17"
category: Economics
tags: [consensus-incentives]
url: https://ethresear.ch/t/staircase-unrestricted-uncle-maker-attack/23682
views: 114
likes: 2
posts_count: 2
---

# Staircase Unrestricted Uncle Maker Attack

[@Nakamoto-JJ](/u/nakamoto-jj)

**Abstract**

Nakamoto consensus is the most widely adopted decentralized consensus mechanism in cryptocurrency systems. Since its proposal in 2008, many studies proposed incentive attacks, where the adversary tries to earn higher profit than its fair share.

One notable example is the recent Riskless Uncle Maker (RUM) attack to timestamp-based Nakamoto consensus such as Ethereum 1.x. The RUM attack shows that an adversary with 25% relative hash power can achieve extra profit share of 26.12%.

**Our approach**

We provide a more comprehensive definition of *risk* in Nakamoto consensus. Specifically, in RUM, risk denotes the the block difficulty risk that arises when a miner pre-selects blocks with different difficulties. That is, if a miner chooses to mine a block with a higher difficulty, the probability of generating a new block per unit time becomes lower. We call such risk *attack cost*, i.e., the decrease in this probability of block generation per unit time. Our crucial finding in this paper is that the attack cost cannot fully capture the risk in attacks on timestamp-based Nakamoto consensus, because it only defines the pre-mining block generation cost.  Another aspect of risk comes from the fact that newly generated blocks after mining may lead to an increase in the mining difficulty. As the mining difficulty continues to rise, honest miners with the same hash rate will gradually produce fewer blocks per unit of time. In this way, the adversary may gain lower profit. In this work, we call the risk of difficulty growth after mining as *difficulty risk*. Based on the notion of difficulty risk, we find that the RUM attack is not fully risk-free, as it suffers from the difficulty risk.

In this work, we provide an approach called *minimal risk control*. Minimal risk control aims to precisely calibrate the block timestamps to minimize the long-term difficulty growth risk. Under the guidance of minimal risk control, we present two new incentive attacks in timestamp-based Nakamoto consensus called UUM attack and SUUM attack. Both attacks have

significantly higher expected profit than existing works while not significantly increasing the risk. By taking the definition of *attack cost* only, our attacks are also *cost-free*.

**UUM**

The UUM attack, as an extension of RUM, relaxes the attack triggering conditions in RUM and expands the strategy apace for the adversary. By doing so, for an UUM adversary with a relative hash power of 25%, the expected reward share reaches 28.41%. Through minimum difficulty risk control, we prove that the UUM attack is cost-free, and the difficulty risk is guaranteed to be strictly less than 0.18. Although UUM has a slightly higher difficulty risk than RUM (which is 0.07), UUM is more profitable.

**SUUM**

We further provide a non-trivial extension of UUM called SUUM. SUUM provides a more careful control on the timing the withheld blocks should be released. By doing so, an SUUM adversary with a relative hash power of 25% can achieve an expected reward share of 33.30%. We also prove that the SUUM attack is cost-free, and that its difficulty risk is strictly less than 0.21.

**Experimentation and Real-Data Analysis**

We validate our results via both simulation and on-chain data analysis. For simulation, we use a discrete-event simulator of a timestamp-based Nakamoto-style blockchain. Our experimental results match our theoretical analysis.

Additionally, we have conducted real-data analysis using three mainstream ETH 1.x-style blockchains: Ethereum 1.x (block heights 15505647–15535776), Ethereum Classic (23232147–23242146), and Ethereum PoW (22905613–22915612). Ethereum 1.x has been deprecated since September 2022 due to the migration to Proof-of-Stake. We thus collect about 30,000 blocks in September 2022. For Ethereum Classic and Ethereum PoW, we collected the data for 10,000 blocks in October 2025. In total, we have collected about 50,000 blocks for our analysis. Our analysis shows the following results:

- It is highly likely that four mining pools are conducting timestamp manipulation attacks, including one mining pool on Ethereum 1.x (0x829bd8…), one on Ethereum PoW (0x9205c2…), and two on Ethereum Classic (0x406177… and 0x35aa26…).
- All four mining pools seem to exploit the timestamp manipulation, an approach similar to our minimum difficulty risk control mechanism. Jumping ahead, as shown in Figure \ref{Exp}.(f)-(g), the timestamp differences of the mainchain blocks exhibit abrupt surges or absences within specific intervals. Our closer analysis shows that it is likely  that the attackers are taking strategies similar to our SUUM attack.

![Attack flowchart of RUM, UUM and SUUM attacks in timestamp-based Nakamoto-style blockchains.](https://ethresear.ch/uploads/default/original/3X/b/b/bba0e8f7a2c6600700f5bc43fe2b99a7e06c09b4.svg)

Fig. 1. Attack flowchart of RUM, UUM and SUUM attacks in timestamp-based Nakamoto-style blockchains.

[![Fig. 2. Results of Our Work. (a) Steady-state Probability. (b) Comparison of Adversary Relative Rewards. (c)  Comparison of Honest Participant Relative Rewards. (d) Comparison of Minimal Difficulty Risk. (e) Comparison of Forking Rates. (f) The Distribution of Mainchain Blocks in Ethereum 1.x, Ethereum PoW, and Ethereum Classic. (g) Four Malicious Mining Pools. (h) UUM State Transition. (i) SUUM State Transition.](https://ethresear.ch/uploads/default/optimized/3X/2/8/2881a1c25a0239a9c622d7249f77e084bcce406f_2_670x500.png)Fig. 2. Results of Our Work. (a) Steady-state Probability. (b) Comparison of Adversary Relative Rewards. (c)  Comparison of Honest Participant Relative Rewards. (d) Comparison of Minimal Difficulty Risk. (e) Comparison of Forking Rates. (f) The Distribution of Mainchain Blocks in Ethereum 1.x, Ethereum PoW, and Ethereum Classic. (g) Four Malicious Mining Pools. (h) UUM State Transition. (i) SUUM State Transition.4222×3147 1.05 MB](https://ethresear.ch/uploads/default/2881a1c25a0239a9c622d7249f77e084bcce406f)

Fig. 2. Results of Our Work. (a) Steady-state Probability. (b) Comparison of Adversary Relative Rewards. (c)  Comparison of Honest Participant Relative Rewards. (d) Comparison of Minimal Difficulty Risk. (e) Comparison of Forking Rates. (f) The Distribution of Mainchain Blocks in Ethereum 1.x, Ethereum PoW, and Ethereum Classic. (g) Four Malicious Mining Pools. (h) UUM State Transition. (i) SUUM State Transition.

## Replies

**SylviaHuang0701** (2025-12-17):

Sounds interesting. Getting a 33% reward share with just 25% hash power through the SUUM attack is honestly terrifying. It’s even crazier that you guys found actual mining pools on ETC and ETHW already doing this in the wild. Great job on the disclosure.

