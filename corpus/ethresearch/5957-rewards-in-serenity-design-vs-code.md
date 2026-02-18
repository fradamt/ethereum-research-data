---
source: ethresearch
topic_id: 5957
title: "Rewards in Serenity: design Vs code"
author: jgm
date: "2019-08-12"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/rewards-in-serenity-design-vs-code/5957
views: 1341
likes: 2
posts_count: 3
---

# Rewards in Serenity: design Vs code

I spent a bit of time looking at the psudeo-code in the eth2 specs as well as at the Serenity design rationale and noticed a discrepancy I hope someone could clear up.

It regards the reduction in reward depending on how quickly the attestation is included.  The [design rationale](https://notes.ethereum.org/9l707paQQEeI-GPzVK02lA#Base-rewards) states the reward is “full if included after 1 slot, 1/n of the full reward if after n slots”, but it looks like [the code](https://github.com/ethereum/eth2.0-specs/blob/469f3d84a36a72453db503d32c5f2d370b401a1c/specs/core/0_beacon-chain.md#rewards-and-penalties-1) is using (64-n)/64 of the reward, where n is the number of slots delayed.  Obviously the latter is far less severe than the former, but I’m wondering which of these two is the canonical formula.

Related, I’m trying to marry the information supplied in https://github.com/ethereum/eth2.0-specs/pull/971 regarding the maximum annual Ether issuance with the formulae used to calculate it.  Taking an example from the PR if there are 30,000,000 Ether validating it lists maximum annual issuance as 991,483 Ether, but going through the maths gives me:

`per-epoch reward (GWei) = 64 * 30,000,000 * 10^9 // int(sqrt(30,000,000*10^9))`

`= 11,085,125,215`

`yearly reward (Eth) = per-epoch reward * 82,181.25 // 10^9`

`= 910,989`

so I’m about 9% below the expected number.  I assume I’m missing a piece of the reward system to make up the difference, but unsure what it may be.  Any explanation here would be greatly appreciated.

## Replies

**vbuterin** (2019-08-13):

> The design rationale states the reward is “full if included after 1 slot, 1/n of the full reward if after n slots”, but it looks like the code  is using (64-n)/64 of the reward, where n is the number of slots delayed. Obviously the latter is far less severe than the former, but I’m wondering which of these two is the canonical formula.

I looked into this; there was a change that got into the phase 0 spec to change the reward from 1/delay to (64-delay)/64. Though the latter approach *does* have a weakness in that it means that there is not enough disincentive against delaying publication of your own attestations to wait until a later slot in which you’re a proposer so you can claim the proposer reward from them, so I’d switching back to what was there before or some intermediate alternative.

---

**jgm** (2019-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Though the latter approach does have a weakness in that it means that there is not enough disincentive against delaying publication of your own attestations to wait until a later slot in which you’re a proposer so you can claim the proposer reward from them

Is this true, though?  If I’m the block proposer I gain 1/8 of all attestations included in my block, so surely my optimum play would be to publish my attestation immediately so it can be included as soon as possible (avoiding as much time delay penalty as I can) and when it’s my turn to be block proposer include the highest-paying attestations available (plus my attestation, if it hasn’t been included already).

Although that brings me to another question: when producing a block, if my inclusion share is 1/8 of the included attestation doesn’t it be to my advantage to pick the attestations by the validators with the largest balances by preference?  Is this the behaviour we want to encourage?  Would it make more sense to have a flat inclusion share (for example, 1/8 of the base reward of an “average” validator, which would net out the same but reduce favouritism for larger validators)?

(“average” above would mean that inclusion reward would be based on a simple sigma(D)/n, ignoring the attesting validator’s balance)

