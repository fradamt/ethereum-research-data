---
source: magicians
topic_id: 24306
title: EIP-7732 the case for inclusion in Glamsterdam
author: potuz
date: "2025-05-22"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7732-the-case-for-inclusion-in-glamsterdam/24306
views: 906
likes: 8
posts_count: 1
---

# EIP-7732 the case for inclusion in Glamsterdam

# ePBS: the case for Glamsterdam.

This short note follows a template designed by [@timbeiko](/u/timbeiko) to propose a headliner for a fork inclusion. I will keep it brief and as little technical as possible as I have already made a case for inclusion in Fusaka.

## Summary

ePBS, as in [EIP 7732](https://eips.ethereum.org/EIPS/eip-7732) stands for execution Payload–Block Separation. It proposes the minimal set of changes to maximally decouple the execution layer from the consensus layer validations. Both in terms of broadcasting and transmitting blocks and actual state transition logic. This feature directly enables L1 scaling by changing the time required to execute a block from the current rougly 2 seconds to 8 seconds. And it changes the time required to broadcast blobs in the network from the current roughly 2 seconds to about 9.

Please see extended not-so-technical justifications in [the case for Fusaka](https://hackmd.io/@potuz/Bkcwd5hG1x).

## Detailed Justification

The current bottleneck for ethereum validators and full nodes to keep up to the tip of the chain is on bandwidth. Validators need to

- Download the full consensus block.
- Download the full execution payload.
- Download all blobs.
- Execute the consensus state transition function
- Execute the payload.

All within 2 seconds in order to be able to attest to the block. This proposal moves all of the above to a *non hot* path, by keeping the hot path to the minimal of downloading the full consensus block (which is minimal compared to the execution block and blobs) and only performing the consensus validation. It delays the remaining part of Ethereum validation essentially until the next slot. Giving time to nodes to either run on lower spec hardware or increase the amount of data that the network carries per block and the amount of computation that the network does can perform per slot.

Secondary benefits include the removal of trust assumptions on block productions, allowing any validator to be a builder and bid for block production, without the need to be gated by relays. It allows any validator to trustlessly sell the rights to propose a payload without trusting an intermediary for the payment fulfillment.

It removes technical debt of having the same P2P networking and timelines for consensus data and execution data, enabling further upgrades to duties separations on validators, constructs like APS, ETs, etc are easier to reason about once the payload and the consensus block are separated. ZK-ification of the consensus layer and the execution layer become independent problems that can be worked out in parallel on different timelines.

It is fully and very simply compatible with other proposals like FOCIL for censor resistance, allowing for a simple plug-in implementation as opposed to more invasive options like [EIP-7886](https://eips.ethereum.org/EIPS/eip-7886)

It simplifies implementations of other ideas like [sealed transactions](https://ethresear.ch/t/auditable-builder-bids-with-optimistic-attestations-in-epbs/22224) for privacy preserving usage.

Its implementation is constrained to the consensus layer and does not require special coordination with the execution layer for testing.

In general, it simplifies implementation of any primitive that may be time sensitive in its evaluation in the execution layer.

This feature should be included right now as it is the unique feature that presents all the strong scaling properties for Ethereum L1 listed above. Other proposals like *delayed execution* lack the broadcasting properties that are crucial for scaling, specially data blob scaling, and do not achieve the full separation of concerns between consensus and execution, while at the same time are more involved and complex to implement involving both layers. In times where Ethereum has been given a clear directive by both the open community as well as EF leaders and core devs as a whole, to focus on scaling both L1 throughput as much as data availability for rollups, there isn’t a single EIP nor project that comes even close to the features that this EIP achieves.

## Stakeholder impact

For users the impact is direct: cheaper transactions both on L1 and in rollups that post to L1. For validators it means either more revenue in the form of execution gas for proposals or lower hardware requirements to follow the chain. The fact that builders are on-chain registered as validators enable trustless constructs for app development that aren’t possible today. For example staking pools do not need to worry anymore about MEV stealing, which allows for higher decentralization of the validator set. Representatives of Lido have mentioned this feature as a highly value feature from EIP 7732 to them.

Objections that I have received to the EIP have been varied throughout the last two years but have mostly settled in two:

- It changes forkchoice.
- Builders need to be staked.

The first one is a minor change to allow for empty blocks, it minimally changes forkchoice relying on current mechanisms to protect builders. As for the second one I have approached current builders and they have expressed that this it not an important problem for them. Initiatives like Flashbot’s buildernet can help mitigate this issue.

## Technical readiness

The most important change, that is the core lifting of separating the blocks broadcast and validation has been implemented already in Prysm and Teku CL clients. Given consensus on ACD, ePBS could be shipped Q1 2026, fully tested in isolation.

## Open questions

There are none, there aren’t any design decisions to be made as far as I am aware besides minor client compatibility issues with some code changes (eg Lodestar requires that fields aren’t removed from structures). Most of the open questions rely on how to further improve on this EIP to reach other targets like APS.
