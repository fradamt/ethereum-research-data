---
source: ethresearch
topic_id: 15551
title: Selfish mining in PoS
author: mart1i1n
date: "2023-05-10"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/selfish-mining-in-pos/15551
views: 2363
likes: 3
posts_count: 6
---

# Selfish mining in PoS

# Description

Selfish mining is an important issue in the Nakamoto consensus such as Bitcoin and Eth 1.0. Eth 2.0 takes many effects to mitigate selfish mining, including proposer boost and honest reorgs. However, we find a new attack that utilizes these mitigations, thereby succeeding at a lower adversarial stake.

# Background

**Proposer Boost** To minimize an ex ante reorg attack and balancing attack, the proposer has a fork-choice “boost” equivalent to 40% of the full attestation weight. Importantly, this boost only lasts for the duration of the slot.

**Honest Reorgs** In order to help push rational behavior (delaying the block publication) towards honest behavior (on-time publishing), honest reorg is implemented. It takes the proposer boost and allows honest proposers to use it to forcibly reorg blocks that have attestation weight below 20%.

[![fig1](https://ethresear.ch/uploads/default/optimized/2X/9/97f1f446791f2a934d474ed4a962d25b24d12bce_2_690x332.png)fig13356×1619 67.2 KB](https://ethresear.ch/uploads/default/97f1f446791f2a934d474ed4a962d25b24d12bce)

# Attack scenario

Assume that the proposer is malicious in slot i and slot i+2. And in slot i and slot i+2, \beta stakes in a committee are adversarial. And the proposal boosting is 40\%. The attack is as follows:

1. In slot i, the malicious proposer delays the block i til the attestation deadline. Only \gamma percent of honest validators cast a vote on the delayed block i.  The rest 1-\gamma-\beta  percent of honest validators do not see block i when they are voting. So they attest to block i+1. The adversarial validators withhold their attestation.
2. Suppose \gamma < 20\%, this means that the honest proposer releases the block i+1 upon block i-1 due to honest reorg implementation in slot i+1. After that, the adversarial validators in slot i+1 vote on the delayed block i while honest validators vote on the block i+1.
3. In slot i+2, the adversarial validators release the votes on block i and propose a new block i+2 upon block i. Because of the proposer boost, fork A has 40\% weight.

[![fig2](https://ethresear.ch/uploads/default/optimized/2X/7/73c67b6d63978d09ed9e94a6a33e59184d82f06f_2_690x306.png)fig23739×1659 130 KB](https://ethresear.ch/uploads/default/73c67b6d63978d09ed9e94a6a33e59184d82f06f)

# Impact

According to the LMD-GHOST fork choice, chain A has a weight of \gamma +2\beta+40\% while chain B has a weight of 1-\beta. If \beta>14\%, chain A has more weight than chain B and becomes the choice of LMD-GHOST. Thus block i+1 is an orphan and its proposer lost all profits in the consensus layer and execution layer. And the proposer of block i+2 receives extra rewards. And this attack succeeds at a lower adversarial stake.

## Replies

**potuz** (2023-05-17):

This is a very interesting post! I can’t find a flaw

![](https://ethresear.ch/user_avatar/ethresear.ch/mart1i1n/48/14503_2.png) mart1i1n:

> So they attest to block i+1

I suppose here is `i-1` right?

Implementation-wise, instead of tracking all attestation seen, we could change the reorg algorithm to also check for a minimum weight of the parent of the block that will be reorged. Honest validators that have voted during i would have voted for i-1 adding to it’s weight and this is a proxy for the total number of attestations sent. As long as the committee weight of i-1 is bigger than 1+\delta  you know that at least \delta + \gamma  have indeed cast their vote during i.

---

**potuz** (2023-05-17):

Notice also that the bound on \beta is not quite right. You are assuming \gamma = 20\% in which case you get  2\beta + 0.6 > 1 - \beta which implies \beta > 0.4/3 \simeq 13.3. However, if \gamma = 20 then there is a 20% chance that the next proposer will not have seen i late and therefore would not reorg it. This needs to be taken into account. This of course without taking into account the nodes that are not reorging (eg. everyone but Lighthouse and Prysm as of today).

---

**mart1i1n** (2023-05-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> This is a very interesting post!

Thanks!

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> I suppose here is i-1 right?

That’s right. It’s a typo.

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> we could change the reorg algorithm to also check for a minimum weight of the parent of the block that will be reorged.

It’s a good fix idea. The key of the vulnerability is that the victim can not make sure whether all attesters have already voted.

---

**michaelsproul** (2023-09-12):

Just noting that the `REORG_PARENT_WEIGHT_THRESHOLD` (K = 1.6) is derived by aiming for resilience against a \beta = 0.2 attacker, who can only attempt this vote hoarding attack if the parent block weight is greater than K, i.e.

2 - \gamma - \beta > K

The minimum K is therefore K = 2 - \gamma - \beta = 1.6, for \gamma = 0.2.

---

**michaelsproul** (2023-09-12):

Something I was also thinking about is whether the attack mitigation opens up new avenues for a malicious proposer to grief (publish late blocks which remain canonical).

I think the obvious case of a griefing proposer with 2 slots in a row is only marginally worse with the mitigation. They can prevent a re-org in slot i + 2 by publishing late in both slots i and i + 1. However previously they could also guarantee at least one late block remaining canonical by e.g. skipping slot i and proposing late in slot i + 1, which causes the single-slot condition checked by the proposer of i + 2 to fail (we only re-org when the parent block is 1 slot behind the block being reorged).

