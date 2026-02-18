---
source: ethresearch
topic_id: 15754
title: Slashing Leads to Slashing
author: mart1i1n
date: "2023-05-30"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/slashing-leads-to-slashing/15754
views: 1325
likes: 1
posts_count: 4
---

# Slashing Leads to Slashing

# Description

Slashing conditions are used to ensure safety. However, the adversary can use the slashing condition to punish honest validators. The key idea of the attack is that the adversary deliberately violate slashing conditions to make honest validators violate slashing conditions too. Though EIP-3076 has been used to protect honest validators from violating slashing conditions, the adversary can utilize it to attack liveness and also punish honest validators using leaking.

# Attack scenario

The attack starts at a special epoch. We denoted as epoch 1. Epoch 1 is not justified because of adversarial attestation delay and network problem. The last block of epoch 1 (block 63) is adversarial. This block contains enough adversarial attestations to justify epoch 1. This block is also withheld. The adversary is waiting for a proper time to release it. The detail is as follows:

[![figsl1](https://ethresear.ch/uploads/default/optimized/2X/8/80645b7d1cc5f06885188bad185b209cd0b700b8_2_690x284.png)figsl11596×657 46.8 KB](https://ethresear.ch/uploads/default/80645b7d1cc5f06885188bad185b209cd0b700b8)

1. For slot 64 to slot 77, epoch 1 is not justified. The honest validators and adversary vote on 0\rightarrow2 (denote as blue).
2. At slot 78, the block 63 is released. Epoch 1 is justified. The honest validators vote on 1\rightarrow2 (denote as purple). The adversary validators withhold their attestations.
3. At slot 95, the adversary deliberately violate slashing conditions. Some the attestations contains in the block 63 can not justify epoch 1. So the last justified epoch becomes epoch 0 again.
4. During epoch 3, the purple validators vote on 0\rightarrow3. They violate slashing condition 2 and are punished.

# Analysis

Finally, \frac{17}{32} of honest validators violate the slashing condition 2. In reality, the beacon node uses EIP-3076 to prevent honest validators from violating slashing condition. But the adversary can use this implementation to punish validators. The validator will check the attestation and block before broadcast. During epoch 3, the purple validators try to release attestations that violate the slashing condition2. All of them are prevent because of EIP-3076. At most 64.4% validators can vote on epoch 3. Epoch 3 can not be justified. This scenario will last for many epochs. During the scenario, the system will enter inactive condition. The purple validator are punished because of inactive actions.

# Split the Views

But we find that the current design has a flaw. The justified checkpoint only update when the the new justified checkpoint is higher than the old justified checkpoint. Suppose the epoch i is justified at first. So the last justified epoch become epoch i. Then the validators who vote on epoch i are slashed. This lead to that some attestations are invalid. The rest attestations are not enough to justify epoch i. But the last justified epoch will not become i-1. It will still become epoch i. By using this flaw, the adversary can split the views of honest validators using the following strategy: Let half of the validators receive the block that contains justified epoch i first while the other half of validators receive the block that contains slashing imformation first. So the first half validators denote epoch i as last justified checkpoint while the last half denote epoch i-1 as last justified checkpoint. This leads to that  the view of validators splits and causes a liveness attack.

## Replies

**MicahZoltu** (2023-05-30):

My understanding is that you only get slashed for double signing, and validators go to great lengths to ensure the client never double signs under any conditions.  If an external actor can cause a client to sign two different blocks at the same height, then that is a bug in the client as that should be impossible.

Note: Signing the *wrong* block (the block that doesn’t become canonical) is not a slashing condition.

---

**fradamt** (2023-05-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/mart1i1n/48/14503_2.png) mart1i1n:

> At slot 95, the adversary deliberately violate slashing conditions. Some the attestations contains in the block 63 can not justify epoch 1. So the last justified epoch becomes epoch 0 again.

This is not how justification works. Once a chain is justified, it cannot be unjustified because of new conflicting attestations being revealed. A valid attestation does not get invalidated by a conflicting one.

---

**mart1i1n** (2023-06-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/fradamt/48/6474_2.png) fradamt:

> A valid attestation does not get invalidated by a conflicting one.

I guess that I understand it. So it means that if two chains are both justified with 1/3-slashable in a network partition condition, (even though there will be 1/3-validators are slashed) both chain are still justified.

