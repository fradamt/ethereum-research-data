---
source: ethresearch
topic_id: 15421
title: "Voting Delay Attack: Punishing Honest Validators in POS"
author: mart1i1n
date: "2023-04-26"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/voting-delay-attack-punishing-honest-validators-in-pos/15421
views: 2492
likes: 6
posts_count: 9
---

# Voting Delay Attack: Punishing Honest Validators in POS

# Description

The reward/penalty mechanism in Proof of Stake is designed to encourage validators to vote and deter validators from misbehaving. It prevents honest validators from being framed and ensures that validators who engage in malicious behavior (e.g., wrong voting) are detectable and gain punishments. However, under our attack, we found that this mechanism in state-of-the-art implementations is not functioned well, where an attacker has a high probability of preventing honest validators from receiving rewards or even being punished. This may lead to potential security issues, as an honest validator may leave the ecosystem due to unfair treatment or no profit.

# Attack scenario

**Overview** Under the design of current implementations (e.g., in the case of Prysm), a validator modifies the justification state upon receipt of a block from the preceding epoch (see [Prysm Code](https://github.com/prysmaticlabs/prysm/blob/efdda168c501f23ac593d4433f2fefbb7d40b230/beacon-chain/forkchoice/doubly-linked-tree/unrealized_justification.go#L101)). In our attack, an attacker uses this update mechanism to deceive honest validators, causing them to transition from one chain to another, and further make those who cast their votes prior be considered to have made incorrect votes, resulting in penalties.

**Assumptions** We assume that more than 2/3 validators are honest actors who will act in the best interest of the network. It means adversaries can, at most, control 1/3 of validators. We also assume that our attack works under the partially synchronous network model. The attack begins from a situation where epoch i just ended and all validators now reach Global Stabilization Time (GST).

**How to launch our attack?** Initially, our attack requests the justification of epoch i is delayed due to the adversary withholds some votes in epoch i. The key point of attack is described as follows.

1. At first, the adversary withholds a block (dashed reddish square) in epoch i containing enough votes to justify checkpoint in epoch i. Once all validators now reach GST at the end of epoch i, chain A is considered the canonical chain for all validators.
2. In epoch i+1, the victim validator proposes on chain A.
3. Then, the adversary block (with the hidden votes) controlled by the attack is released. This triggers the update of justification to change the candidate chain for chain A to chain B.
4. After that, the victim validators who vote with checkpoint on chain A as target are punished.
fig12855×2175 154 KB

# Long-time attack

We present out our attack against the Ethereum Proof-of-Stake. The begin from a situation where epoch i just ended and all validators now reach GST. The justification of epoch i is delayed since the adversary withholds some votes in epoch i.  And chain A is consideration of the canonical chain for all validators.

1. At first, the adversary also withholds a block in epoch i containing enough votes to justify checkpoint in epoch i.
2. In epoch i+1, adversary propose blocks and cast votes on chain B whereas honest validators do so on chain A.
3. Then, the adversary block (with the hidden votes) is released at the moment when half of the honest validators have already cast their vote for chain A. This adversary block triggers the update of justification to change  the rest of honest validator view of the candidate chain from chain A to chain B.
4. Lastly, the adversary withholds some votes in the last few slots of epoch i+1.
5. Repeat the process.

| Reward | Penalty |
| --- | --- |
| 54\cdot base\_reward | 40\cdot base\_reward |

# Impact

As the attacks are continuously launched, some validators may incur more penalties than rewards. This significantly discourages the validators from participating in the staking process, eventually leading to their withdrawal from the system.

# Proposed fixes

The penalty rule right now is too strict in partial synchronous network. Considering that slashing conditions and inactivity leak have already played their roles in maintaining safety and liveness, it is suggested that a checkpoint vote with mismatched target or source should not result in penalties for the validators.

## Replies

**rick** (2023-05-09):

**thanks for contributing!**

I have some questions about the **attack**, that would be great if you could provide more details.

1. What is the likelihood that an adversary would withhold a block in epoch i that contains enough votes, considering that such a block must be in the adversary’s possession?
2. When is the expected release time for the adversary’s block (containing hidden votes)?

---

**potuz** (2023-05-09):

There are a couple of different situations in play here:

1. The adversary is the only one in control of justification, that is no one has seen enough votes to justify i during i (eg if the adversary has > 33% stake this can happen)
2. The adversary is not in control, that means there have been enough attestations seen during i to justify i, but they weren’t included during i because the last block (controlled by the adversary in this case) was not submitted, hence they weren’t included during i.

In the first case there’s absolutely nothing the network can do and I believe that attestation rewards are a minor nuance in front of nastier thing a >33% attacker can do.

In the second case, which would be the vast majority of cases, then the honest validator in chain A, during i+1 would have included the missing attestations to justify i. I would not be justified however, since in principle this would happen when we transition from i+1 to i+2. However, at the time that the attacker releases the withheld block, automatically chain A also justifies i and remains canonical because of the LMD advantage it has.

I suggest you take a look at [Fork Choice Bugfix Disclosure - HackMD](https://notes.ethereum.org/@djrtwo/2023-fork-choice-reorg-disclosure) and specifically [Witholding attack mitigation - HackMD](https://hackmd.io/a8vbgF6YR0-j6T9LpcYB3g) where this attack was described and patched.

---

**mart1i1n** (2023-05-10):

Thank you for your response!

1. We assume that the network is partially synchrony, where after some unknown Global Stabilization Time (GST), the system becomes synchronous. Before reaching GST, all adversarial validators withheld their attestations. So the probability of justifying a new checkpoint by all honest validators is very low if we assume the adversarial stake is slightly less than 1/3.
2. If the adversary wants to execute the attack for a long time, he or she should create a senario where only half of the honest validators vote on the right chain. So the adversary is expected to release the block no later than the half of epoch. Here are details about it:

During one epoch, the adversary validators (approximately 1/3) and half of the honest validators (approximately 1/3) vote with the checkpoint on chain B as the target. This gives the adversary the opportunity to delay the justification of an epoch by withholding some attestation and releasing them at the right time to make honest validators change their minds about the chosen chain during the next epoch.

The victim validators who cast votes on chain A mismatch the target and source. The attestation role of a validator is selected randomly, thus the probability of every honest validator getting punished in an epoch is 1/2. We calculate the probability of a validator having no profit according to the reward and penalty of attestation. We denote the base_reward as 64 times smaller than the base_reward in Eth spec. A validator can receive 54 \cdot base_reward in profits if they vote for the source, target, and head correctly. Also, they lose 40 \cdot base_reward in stake if the vote for the source and target is incorrect.

Suppose a validator checks their profit for 12 hours (112 epochs), the profit is 54m-40(112-m), where m is the number of epochs where the validator was not attacked. SO the number of epochs where the validator was not attacked is 48. After running the attack for 12 hours (112 epochs), the probability of an honest validator getting no profit is \sum\limits_{i=0}\limits^{48}\binom{112}{i}(\frac{1}{2})^i(\frac{1}{2})^{112-i}\approx 5%.

---

**mart1i1n** (2023-05-10):

Thanks for getting back to me! Sorry if I wasn’t clear, but I think there might be a misunderstanding about the situations.

1. We assume the adversarial stake is slightly less than 1/3. Also we assume a partially synchronous network, where after some unknown Global Stabilization Time (GST), the system becomes synchronous. Before reaching GST, all adversarial validators withheld their attestations. The honest validators’ opinion of justify a new checkpoint maybe different. It gives the adversary the opportunity to control the justification.
2. Considering that the adversary deliberately withholding their attestations in epoch i, the chain A doesn’t contain enough attestations before the adversary release their attestations. So it may be impossible for chain A to justify epoch i. But the withheld block in epoch i contains the withheld attestations, thus the withheld block justify epoch i in chain B. I’m not entirely sure if I’ve understood the withholding attack correctly, but the difference between the attack we proposed and the attack Witholding attack mitigation - HackMD may be that the honest chain A cannot justify epoch i because the attestations are withheld.

If there is some thing wrong, please let me know.

---

**potuz** (2023-05-11):

The situation you are describing is that of an attacker containing the only attestations to justify i which was situation 1. in my reply. In normal circumstances where an attacker has stake p < 33% and the remaining validators are honest and participating, then enough attestations (1-p) > 66% are seen by honest validators and then chain A will contain enough votes to justify i. If there are less than 66% of the stake seen voting for i as target, then the attacker can do much nastier things than hurting staking rewards, like generating arbitrarily long forks.

---

**rick** (2023-05-12):

**Good discussion!  I think your opinion is totally correct.**

Assuming that the attacker’s stake p is less than 33% and all other validators are honest, and actively participating, then the honest validators will observe enough attestations (1-p) > 66% to validate chain A and justify it.

This statement is predicated on the assumption of a synchronous network model, wherein all honest validators can receive messages (e.g., blocks and attestations), from their counterparts within an acceptable time frame. However, such a model in eth 2.0 systems may not be practical or desirable, as unexpected network delays can result in quadratic communication costs.

---

In my opinion, the mentioned potential attacks may be vulnerable in a partially synchronous network.

An attacker exploits the fact that candidate chain (Chain A) in a given epoch may not receive enough attestations to be validated, even if 67% of validators are honest. This is because, in an asynchronous network, honest validators cannot guarantee that they will receive all messages in a timely manner (in epoch i). As a result, justification of the chain (Chain A) may need to be postponed until the next epoch (i+1).

In the subsequent epoch (i+1), if certain validators persist in voting for such a unjustified chain (Chain A), and then the attacker decides to release the previously withheld attestations, there is a chance (depending on the network assumption) that the attacker can switch the network’s preference from Chain A to Chain B. This is due to the current justification mechanism, which allows for such a scenario. If this occurs, honest validators who have already voted for Chain A will be penalized for their “malicious” votes.

---

**mart1i1n** (2023-05-12):

Suppose that the chain in epoch i may not contain enough attestations for some reasons (such as network delay and adversarial validators withhold the attestaions). In epoch i+1, the honest validators continue to build chain A upon the only chain in epoch i. And chain A contains enough attestations to justify epoch i after a period of time. The adversary can exploit this justification delay. He or she releases the withheld block (reddish block) in epoch i before chain A can justify chain B. The withheld block contains enough attestations to justify epoch i. After that, the honest validators stop building on chain A and start to build on chain B. Thus chain A can not contain enough attestations to justify epoch i.

---

**mart1i1n** (2023-07-10):

It is easy to delay an epoch justification in a synchronous network.

Suppose there are 1/3 of total stake is adversarial. If the honest validators want to justify an epoch, all attestations should have the same target.

Consider the following forkchoice diagram:

[![step 1 & 2](https://ethresear.ch/uploads/default/optimized/2X/5/5235d668141271b907750120c652078d9eb47ae7_2_689x271.jpeg)step 1 & 22388×941 147 KB](https://ethresear.ch/uploads/default/5235d668141271b907750120c652078d9eb47ae7)

1. During epoch 1, the adversary withhold their attestation. At the end of epoch 1 (slot 63) , \frac{31}{32} honest attestations are included in the chain.
2. At the beginning of epoch 2 (slot 64), the rest \frac{1}{32} honest attestations of epoch 1 are supposed to be contained in the first block of epoch 2.
3. The first block of epoch 2 is withhold by attacker (the translucent orange block), and a block of epoch 1 which contains enough withheld attestations to justify epoch 1 is released (the red block).
4. Due to the rule, the attestations of slot 64 are supposed to be vote for the red block. Thus there are not enough honest attestations to vote on honest chain.

[![step 3 & 4](https://ethresear.ch/uploads/default/optimized/2X/d/dab79c95ca7501412feb6e85ee89beba10e4e60e_2_689x234.jpeg)step 3 & 42388×813 146 KB](https://ethresear.ch/uploads/default/dab79c95ca7501412feb6e85ee89beba10e4e60e)

