---
source: ethresearch
topic_id: 19770
title: The contention between preconfs and ePBS
author: potuz
date: "2024-06-09"
category: Architecture
tags: [preconfirmations]
url: https://ethresear.ch/t/the-contention-between-preconfs-and-epbs/19770
views: 4270
likes: 4
posts_count: 7
---

# The contention between preconfs and ePBS

This quick note is motivated by a question of [@Hasu.research](/u/hasu.research) regarding the compatibility of ePBS with the different mechanisms for preconfirmations that are being proposed by independent groups [1](https://ethresear.ch/t/the-preconfirmation-sauna/19762) [2](https://ethresear.ch/t/blob-preconfirmations-with-inclusion-lists-to-mitigate-blob-contention-and-censorship/19150) [3](https://chainbound.github.io/bolt-docs/) [4](https://docs.google.com/presentation/d/1a-0rP2knM11g59UmnKn7I7NH8BlFM5wNhczH35sbkSo/edit#slide=id.g2731bc99d1b_0_0) [5](https://docs.primev.xyz/get-started/introduction). The only purpose of this note is to leave a quick written record of the fundamental contention between the enshrinements of preconfirmations and the [current proposal for ePBX](https://github.com/potuz/consensus-specs/pull/2).

## Overloading inclusion lists.

Even in the very first post on [based preconfirmations](https://ethresear.ch/t/based-preconfirmations/17353), the idea of using [forced inclusion lists](https://eips.ethereum.org/EIPS/eip-7547) was put forward as a way for proposers to signal their intent of honoring preconfirmations, forcing builders to include these transactions. An extrapolation of this idea led, in one of the original designs for ILs, to propose that inclusion lists may essentially include a complete list of transactions the proposer has in its current mempool. One of the problems with these ideas is that the full list of transactions would need to be broadcast over the P2P network twice: once when the inclusion list is broadcast, and the second time within the payload itself. In all known designs for inclusion lists, validators attest for the existence of the full executable transaction list. This implies in particular that

1. The list must be available at the beacon block validation time.
2. The list must be executed at the beacon block validation time.

This section is not meant to be read as *inclusion lists aren’t compatible with ePBS* but rather any preconfirmation system (and next block forced inclusion lists by definition are such a system) that relies on the execution and distribution of the transactions at the consensus block validation time, necessarily clashes with the main optimization from ePBS.

## ePBS validation optimization

The above two points are in direct opposition with the main optimization that ePBS brings to block processing, that is that the only hot path to validation is that of the consensus block that has to be fully verified before the attestation deadline. All other validations, like transaction execution, data availability, etc. are deferred to the remainder of the slot and into the next slot.

[![ePBS slot](https://ethresear.ch/uploads/default/optimized/3X/8/f/8f3daa474ae131dfbee7c96cfd9f2a7e4035c06a_2_690x364.jpeg)ePBS slot3224×1703 176 KB](https://ethresear.ch/uploads/default/8f3daa474ae131dfbee7c96cfd9f2a7e4035c06a)

While ePBS is compatible with inclusion lists, their addition inherently stresses this optimization. Broadcasting a small list of 16 transactions that can be immediately executed in microseconds is not the same as broadcasting a full block, and presumably, even blob transactions as some based rollups would require.

## The centralized nature of preconfs

There is no current design (that I am aware of) of preconfirmations, that does not rely on a centralized entity. This is natural to expect in the absence of an encrypted public mempool, users can’t send their transactions in the open to the next proposer (although they could *encrypt the transactions to the public BLS address of the next proposer*), and we can’t enshrine an RPC provider, all systems thus make use on existing centralized entities (for example relays) to act as a preconfer. Decentralization comes in that it is ultimately the proposer who enforces these preconfirmations, by forcing the builder to fullfil them.

Thus, in all proposed systems for preconfirmations, either of L1 transactions or for based rollups, there exist a centralized entity that at the very least is responsible for gathering the transactions and giving out the preconfirmations. Systems differ on how is that these preconfirmations are enforced, they range from new L1 slashing proposals, to restaking proposals (moving the slashing to a separate layer), etc. The point is that preconfirmations can be enforced by the protocol itself, or by a somewhat decentralized party like the subset of validators participating in the preconfirmation scheme. In summary, there is a plethora of options for enforcing the (or penalizing the lack of) inclusion of preconfirmations, in decreasing level of trustlessness:

- The L1 protocol itself enforces inclusion. For example, forced ILs, with proposer level slashings on missed slots, preconf equivocations, etc.
- Some separate committee enforces them. For example a subset of the L1 validators also participate in a sidechain by restaking, and the enforcement/punishment is carried in that sidechain.
- A centralized entity enforces them. For example the relay itself only sends bids from builders that have satisfied the required preconfs.

## A viable way compatible with ePBS: staked builders as preconfirmers.

Any approach with a full payload being broadcast with the consensus block for preconfirmation enforcement clashes directly with the main scaling optimization of ePBS with regard to block validation. As thus, it seems difficult to expect a working design in which the proposers are in charge of sending and enforcing preconfirmations. The second and third approaches above are fully compatible with ePBS.

One of the features that preconfirmation systems can leverage when ePBS is in place, is that builders themselves are staked validators, thus they can be subject to the same rules that these systems currently require from proposers. For example, those systems that rely on slashings on a restaking scheme could simply add conditions on participating builders. That is, the proposer set participating in the scheme only take bids from builders that are participants of the scheme. The builders and proposers are required to be restaked. There are new penalty conditions for

- A proposer that does not include a block.
- A proposer that includes a block with a commitment to a non-participating builder.
- A builder that does not include the payload
- A builder that includes a payload does not satisfies the preconf list.

## A separate note on restaking

ePBS also presents a challenge on any restaking scheme: builders can transfer funds in the same payload that they commit a slashable offense. L1 protocol can deal with this by immediately deducting the bid from the builder’s balance at the time of CL block processing, but delaying the credit to the proposer. In case the builder commits a slashable offense, the buffer allows the L1 protocol to implement penalization procedures that can impact those delayed funds accordingly. If the builder is restaked however, the restaking chain does not have access to these funds.

## Replies

**Nero_eth** (2024-06-09):

So, the problem is that ILs (thus preconfs) could be too large to be propagated in time?

Simply speaking, under ePBS, validators would use the time until 2" to braodcast a small committment (committment to builder bid) but with unlimited size ILs they’d basically have to broadcast something in the size of a block which will not make it until the attestation deadline?

Could we move the IL validation to a later time in the slot such that it can be invalid at the attestation time and then let the PTC vote on timeliness of the payload PLUS validity of IL.

---

**potuz** (2024-06-09):

I don’t think that’s possible. Validity of the IL requires an on-chain vote because it enforces validity of the payload. As such the vote needs to be by a large committee not a small one. Besides this we’re thinking on moving the payload reveal time earlier and the PTC vote as close to it as possible (to avoid timing assymetry for builders) and this also puts pressure on the PTC.

I think the idea of exploiting the fact that builders will be staked validators for preconfirmations is unexplored and should lead to satisfactory designs.

---

**Evan-Kim2028** (2024-06-11):

What might be some differences between staked builders and staked proposers?

- Are they separate entities? E.g. different slashing conditions and different collaterals
- Would builders need to stake on the beacon chain as well?

---

**potuz** (2024-06-11):

There are no differences, builders are just validators, but they act at different times of block processing, and preconfirmations can be enforced easily on the later parts.

Yes, builders will be staked on the beacon chain.

---

**Evan-Kim2028** (2024-06-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> There are no differences, builders are just validators, but they act at different times of block processing, and preconfirmations can be enforced easily on the later parts.

wouldn’t a builder/validator entity be proposing every block, whereas validators without builders are only proposing once in a blue moon when they are picked?

---

**meridian** (2024-06-12):

You missed the preconfirmations enabled by https://docs.xga.com

This is literally live on mainnet Ethereum right now.

