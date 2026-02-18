---
source: ethresearch
topic_id: 11854
title: Avalanche Attack on Proof-of-Stake GHOST
author: jneu
date: "2022-01-24"
category: Consensus
tags: []
url: https://ethresear.ch/t/avalanche-attack-on-proof-of-stake-ghost/11854
views: 6217
likes: 6
posts_count: 4
---

# Avalanche Attack on Proof-of-Stake GHOST

*Authors: Joachim Neu, Ertem Nusret Tas, David Tse*

*Special thanks to Danny Ryan and Aditya Asgaonkar for feedback and discussions.*

**This attack was subsequently published in: [“Two More Attacks on Proof-of-Stake GHOST/Ethereum”](https://dl.acm.org/doi/10.1145/3560829.3563560)**

**TL;DR:** We describe a generic attack on PoS GHOST variants. This points to conceptual issues with the combination of PoS and GHOST. PoS Ethereum as-is is not susceptible to this attack (due to LMD, which comes with its own problems, see [here](https://ethresear.ch/t/balancing-attack-lmd-edition/11853)). Still, we think this attack can inform the fork choice design and help projects that (consider to) use similar consensus protocols.

We assume basic familiarity with GHOST (see [Gasper](https://arxiv.org/abs/2003.03052) and the [GHOST paper](https://eprint.iacr.org/2013/881)). Knowledge of the beacon chain [fork choice specification](https://github.com/ethereum/consensus-specs/blob/2232d767352c72653467ecef62d88647fd4cd2ef/specs/phase0/fork-choice.md) and [earlier](https://ethresear.ch/t/a-balancing-attack-on-gasper-the-current-candidate-for-eth2s-beacon-chain/8079) [attacks](https://ethresear.ch/t/attacking-gasper-without-adversarial-network-delay/10187) won’t hurt, either.

## High Level

The Avalanche Attack on PoS (Proof-of-Stake) GHOST (Greedy Heaviest Observed Sub-Tree) combines *selfish mining* with *equivocations*. The adversary uses withheld blocks to displace an honest chain once it catches up in sub-tree weight with the number of withheld adversarial blocks. The withheld blocks are released in a flat but wide sub-tree, exploiting the fact that under the GHOST rule such a sub-tree can displace a long chain. Only two withheld blocks enter the canonical chain permanently, while the other withheld blocks can subsequently be reused (through equivocations) to build further sub-trees to displace even more honest blocks. The attack exploits a specific weakness of the GHOST rule in combination with equivocations from PoS, namely that an adversary can reuse ‘uncle blocks’ in GHOST, and thus such equivocations contribute to the weight of multiple ancestors. Formal security proof of PoS GHOST seems doomed.

A proof-of-concept implementation for vanilla PoS GHOST and Committee-GHOST is provided [here](https://github.com/tse-group/pos-ghost-attack). By “vanilla PoS GHOST” we mean a one-to-one translation of GHOST from proof-of-work lotteries to proof-of-stake lotteries. In that case, every block comes with unit weight. By “Committee-GHOST” we mean a vote-based variant of GHOST as used in PoS Ethereum, where block weight is determined by blocks (and potentially a [proposal](https://notes.ethereum.org/@vbuterin/lmd_ghost_mitigation) [boost](https://github.com/ethereum/consensus-specs/pull/2730)). Subsequently, we first illustrate the attack with an example, then provide a more detailed description, and finally show plots produced by the proof-of-concept implementation.

## A Simple Example

We illustrate the attack using a slightly simplified example where the adversary starts with k=6 withheld blocks and does not gain any new blocks during the attack. In this case, the attack eventually runs out of steam and stops. (In reality, the larger the number of withheld blocks, the more likely the attack continues practically forever, and even for low k that probability is not negligible.) Still, the example illustrates that k=6 blocks are enough for the adversary to displace 12 honest blocks—not a good sign.

First, the adversary withholds its flat-but-wide sub-tree of k=6 withheld blocks, while honest nodes produce a chain. (Green/red indicate honest/adversarial blocks, and the numbers on blocks indicate which block production opportunity of honest/adversary they correspond to.)

**Figure 1:**

[![example-step1_300x](https://ethresear.ch/uploads/default/original/2X/a/a243982ab89b862bb9af5b69bcee1d842cb102c6.png)example-step1_300x300×300 10.2 KB](https://ethresear.ch/uploads/default/a243982ab89b862bb9af5b69bcee1d842cb102c6)

Once honest nodes reach a chain of length k=6, the adversary releases the withheld blocks, and displaces the honest chain.

**Figure 2:**

[![example-step2_300x](https://ethresear.ch/uploads/default/original/2X/b/b0a781fdd15d6b4ce4578db8d1de4ec39096108f.png)example-step2_300x300×354 13.1 KB](https://ethresear.ch/uploads/default/b0a781fdd15d6b4ce4578db8d1de4ec39096108f)

Note that the adversary can reuse blocks 3, 4, 5, 6. Honest nodes build a new chain on top of 2 → 1 → Genesis. Once that new chain reaches length 4, the adversary releases another displacing sub-tree.

**Figure 3:**

[![example-step3_300x](https://ethresear.ch/uploads/default/original/2X/6/69653025479938e903959b99691af6fb375a3b56.png)example-step3_300x300×353 19.7 KB](https://ethresear.ch/uploads/default/69653025479938e903959b99691af6fb375a3b56)

Finally, note the adversary can reuse blocks 5, 6. Honest nodes build a new chain on top of 4 → 3 → 2 → 1 → Genesis. Once the new chain reaches length 2, the adversary releases the last displacing sub-tree.

**Figure 4:**

[![example-step4_300x](https://ethresear.ch/uploads/default/original/2X/4/4e9eccfdd3b4fea596eb527efe6d254e6129a490.png)example-step4_300x300×407 23 KB](https://ethresear.ch/uploads/default/4e9eccfdd3b4fea596eb527efe6d254e6129a490)

Honest nodes now build on 6 → 5 → 4 → 3 → 2 → 1 → Genesis. All honest nodes so far have been displaced. Overall, the adversary gets to displace O(k^2) honest blocks with k withheld adversarial blocks.

## Attack Details

Selfish mining and equivocations can be used to attack PoS GHOST (using an ‘avalanche of equivocating sub-trees rolling over honest chains’—hence the name of the attack). The following description is for vanilla PoS GHOST, but can be straightforwardly translated for Committee-GHOST. Variants of this attack work for Committee-GHOST with Proposal Weights as well.

Suppose an adversary gets k block production opportunities in a row, for modest k. The adversary withholds these k blocks, as in *selfish mining* (cf Figure 1 above). On average, more honest blocks are produced than adversary blocks, so the developing honest chain eventually ‘catches up’ with the k withheld adversarial blocks.

In that moment, the adversary releases the k withheld blocks. However, not on a competing adversarial chain (as in selfish mining for a Longest Chain protocol), but on a competing adversarial sub-tree of height 2, where all but the first withheld block are siblings, and children of the first withheld block. Due to the GHOST weight counting, this adversarial sub-tree is now of equal weight as the honest chain—so the honest chain is abandoned (cf Figure 2 above).

At the same time, ties are broken such that honest nodes from now on build on what was the second withheld block. This is crucial, as it allows the adversary to reuse in the form of *equivocations* the withheld blocks 3, 4, …, k on top of the chain Genesis → 1 → 2 formed by the first two withheld adversarial blocks, which is now the chain adopted by honest nodes.

As an overall result of the attack so far, the adversary started with k withheld blocks, has used those to displace k honest blocks, and is now left with equivocating copies of k-2 adversarial withheld blocks that it can still reuse through equivocations (cf Figure 3 above). In addition, while the k honest blocks were produced, the adversary probably had a few block production opportunities of its own, which get added to the pool of adversarial withheld blocks. (Note that the attack has renewed in favor of the adversary if the adversary had two new block production opportunities, making up for the two adversarial withheld blocks lost because they cannot be reused.)

The process now repeats (cf Figure 4 above): The adversary has a bunch withheld blocks; whenever honest nodes have built a chain of weight equal to the withheld blocks, then the adversary releases a competing sub-tree of height 2; the chain made up from the first two released withheld blocks is adopted by honest nodes, the other block production opportunities can still be reused in the future through equivocations on top of it and thus remain in the pool of withheld blocks of the adversary.

If the adversary starts out with enough withheld blocks k, and adversarial stake is not too small, then the adversary gains 2 block production opportunities during the production of the k honest blocks that will be displaced subsequently, and the process renews (or even drifts in favor of the adversary). No honest blocks enter the canonical chain permanently.

## Proof-of-Concept Implementation Results

For illustration purposes, we plot a snapshot of the block tree (adversarial blocks: red, honest blocks: green) resulting after 100 time slots in our proof-of-concept implementation. The attack is still ongoing thereafter, and as long as the attack is sustained, no honest blocks remain in the canonical chain permanently.

### PoS GHOST

- Adversarial stake: 30%
- Initially withheld adversarial blocks: 4

[![](https://ethresear.ch/uploads/default/optimized/2X/4/474a4c5fe8385ec20af1eb309561cdf00653ad19_2_463x500.png)2823×3048 563 KB](https://ethresear.ch/uploads/default/474a4c5fe8385ec20af1eb309561cdf00653ad19)

### Committee-GHOST

- Adversarial stake: 20%
- Initially withheld adversarial blocks: 12

[![](https://ethresear.ch/uploads/default/optimized/2X/a/a6f1b271b62c5cb9222ee8b5721acc31fe9c5ce5_2_690x197.jpeg)7377×2114 997 KB](https://ethresear.ch/uploads/default/a6f1b271b62c5cb9222ee8b5721acc31fe9c5ce5)

## Applicability to PoS Ethereum

PoS Ethereum’s LMD (Latest Message Driven) aspect interferes with this attack, but comes with its own problems, see [here](https://ethresear.ch/t/balancing-attack-lmd-edition/11853).

## Replies

**kladkogex** (2022-01-25):

Some time ago, when ETH foundation requested security vulnerability comments to ETH2 specification, I submitted several security bugs, all of them were successfully ignored.

One of them was about block proposer submitting potentially unlimited number of fake proposals.

A proposer can be slashed for proposing and signing more than one block proposal, but slashing is limited to the security deposit of the proposer (32ETH), which is non-essential for the attacker.

So a single proposer can propose zillions of fake block proposals in a single block, which could make any attack even more dangerous, including the one described above.

I think it would be logical for the ETH foundation to announce an adversarial competition to let people break the network by controlling a small number of validators. I personally would be happy to participate. I feel there are a number of security vulnerabilities that one could try exploiting.

The fact that ETH2 has not been attacked so far is partially because there is little real money in play. This will change dramatically once the merge happens.

It seems logical that before ETH2 merge happens such a competition takes place.

---

**djrtwo** (2022-01-26):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> which could make any attack even more dangerous, including the one described above.

It’s important to note that the theoretical attack in this post hinges upon counting equivocations which the beacon chain spec does not do. So “creating zillions” of fake block proposals is not made worse by the above.

---

[Apologies for hijacking the thread. Such an attack *if* double counting equivocations in LMD GHOST is a very valid and viable threat]

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> all of them were successfully ignored.

All of these reported issues were responded to. The particular issue you noted here was with respect to DoS attacks to which the DoS protection measures found in the p2p spec were referenced. The approximate number of DoS blocks you could get onto the network is approximately a function of the count of honest nodes on the network (assuming you can deliver a unique block to each honest node before it has seen another block forwarded from another honest node), so “a zillion” is not the bound on the DoS attack.

Also noted, is that with simply an equivocation block DoS attack, subsequent honest proposals would quickly coalesce on a single chain (barring some more sophisticated balancing attack).

There is an ongoing bug-bounty program if that interests you – [Ethereum Bug Bounty Program](https://ethereum.org/en/eth2/get-involved/bug-bounty/)

Additionally, testnets or private networks are a good place to attempt attacks before submission to the bug bounty program.

---

**luthlee** (2022-05-25):

I am a bit confused about the description about this attack.

1. I thought there is only one proposer per slot. So should the 2nd honest block (green block with number 2) actually be a block at slot 7 in this example?
2. Are equivocating blocks allowed in Gasper. Would the proposer slash condition, i.e., distinct blocks from the same proposer in the same epoch, rejects the reused block and slash the corresponding adversary validator? Therefore, is this attack practical in Beacon Chain?

Thanks.

