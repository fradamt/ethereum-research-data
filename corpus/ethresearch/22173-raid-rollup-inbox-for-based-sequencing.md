---
source: ethresearch
topic_id: 22173
title: Raid - Rollup inbox for based sequencing
author: jvranek
date: "2025-04-17"
category: Layer 2
tags: [based-sequencing]
url: https://ethresear.ch/t/raid-rollup-inbox-for-based-sequencing/22173
views: 147
likes: 3
posts_count: 1
---

# Raid - Rollup inbox for based sequencing

*Thanks to the Nethermind and Taiko teams for discussions and feedback.*

### TL;DR

Raid (“Retroactive Attestation of Inbox Data”) is a set of contracts that rollup inboxes can adopt to enable preconf-compatible based sequencing. Raid employs multiple levels of on-chain filtering to ensure that only blobs submitted by preconfers are considered canonical by rollup nodes. This is accomplished *without* an on-chain view of the beacon chain lookahead or modifications to the L1 like [EIP-7917](https://ethereum-magicians.org/t/eip-7917-deterministic-proposer-lookahead/23259) that would make this vastly simpler.

A post with more context can be found [here](https://eth-fabric.github.io/website/research/raid).

### Problem

Rollups need an L1 entry-point for blobs to be published.

The OP Stack uses a random `batchInbox` EOA address and filters for canonical blobs by verifying that all blob transactions were signed by the dedicated `batchSubmitter` during their rollup’s derivation. Instead of a fixed address, based sequencing requires a dynamic `batchSubmitter` address to rotate between the L1 proposers.

In Taiko, anyone can permissionlessly publish blobs to the `TaikoInbox` contract which saves metadata necessary for proving in later stages. This is sufficient for based sequencing, but because *anyone* can publish at anytime, preconfers cannot make credible commitments about contentious state. Any preconfer issuing L2 execution preconfs is guaranteed to break their commitment if an adversary changes the rollup’s state before they publish.

What’s needed is a way to grant the preconfer a write-lock on the rollup up until their slot. The prevailing thought has been to expose a view of the beacon lookahead to the inbox contract and use it to filter blob proposals. While EIP-7917 addresses this in the future, the lookahead is currently a function of the beacon state and therefore is not directly provable via Merkle proofs against the EIP-4788 beacon block root. Instead, trustlessly exposing the lookahead on-chain requires pessimistically ZK-proving the beacon chain function or optimistically posting it and then slashing via fraud proof as in [Nethermind’s approach](https://github.com/NethermindEth/Taiko-Preconf-AVS/blob/004d407105578a83c4815e7ec2c55ec467b9ed3f/SmartContracts/src/avs/PreconfTaskManager.sol#L174).

### Proposal

Raid addresses this problem with today’s tools but comes with one tradeoff: it is not compatible with real-time settlement and thus can be thought of as a pragmatic short-term solution until EIP-7917 is live.

- The Raid inbox tracks an unsafeHead and safeHead, which are references to blob publications
- Anyone can permissionlessly publish to the inbox and specify if they want to replace or advance the unsafeHead
- The inbox will first ensure that the contract caller is a preconfer that satisfies all preconditions (e.g., sufficient collateral / opted in to preconf protocol / etc)
- The inbox will verify a validatorProof - a Merkle proof against the EIP-4788 beacon block root that proves who the L1 proposer was during the last unsafeHead’s publication
- If the contract caller tried to replace, the validatorProof proves the sender of unsafeHead did not publish during their L1 slot, then replaces the unsafeHead with their own
- If the contract caller tried to advance, the validatorProof proves the sender of unsafeHead did publish during their L1 slot, then promotes the unsafeHead to the safeHead and replaces the unsafeHead with their own
- Rollup nodes use the historical safeHeads when deriving the rollup’s state

### Example Flow

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/c/bc6bb7c07b75b100d29d07a655afcdd1f2da7402_2_690x398.jpeg)image1920×1110 132 KB](https://ethresear.ch/uploads/default/bc6bb7c07b75b100d29d07a655afcdd1f2da7402)

**Slot N**

- We assume the rollup starts in it’s genesis state
- blobProposer_0 is a valid preconfer that publishes B_0 with replaceUnsafeHead = true
- B_0 is published to the PublicationFeed contract and returns a publicationId_{B_0}
- Since replaceUnsafeHead is true and there is no previous unsafeHead, publicationId_{B_0} becomes the new unsafeHead
- Rollup nodes don’t update their state as there’s no new safeHead

**Slot N+1**

- blobProposer_1 is an invalid preconfer so publishing B_1 reverts
- blobProposer_2 is a valid preconfer that publishes B_2 with replaceUnsafeHead = false
- Since replaceUnsafeHead is false, blobProposer_2's validatorProof proves that publicationId_{B_0} was indeed submitted during blobProposer_0's slot
- Assuming validatorProof is valid, publicationId_{B_0} is promoted to the safeHead, and publicationId_{B_2} becomes the new unsafeHead
- Rollup nodes receive a NewSafeHead event and process B_0 to update their local L2 state

**Slot N+2**

- blobProposer_3 is a valid preconfer that publishes B_3 with replaceUnsafeHead = true
- Since replaceUnsafeHead is true, blobProposer_3's validatorProof proves that it was not blobProposer_2's slot when they published B_2
- Assuming validatorProof is valid, publicationId_{B_2} is replaced by publicationId_{B_3} as the unsafeHead
- Rollup nodes don’t update their state as there’s no new safeHead

**Slot N+3**

- blobProposer_4 is a valid preconfer that publishes B_4 with replaceUnsafeHead = false
- Since replaceUnsafeHead is false, blobProposer_4's validatorProof proves that publicationId_{B_3} was indeed submitted during blobProposer_3's slot
- Assuming validatorProof is valid, publicationId_{B_3} is promoted to the safeHead, and publicationId_{B_4} becomes the new unsafeHead
- Rollup nodes receive a NewSafeHead event and process B_3 to update their local L2 state

### Assumptions

- since each publication either replaces or promotes the previous unsafeHead, only one publication can be added per block to allow time for the beacon block root to become available on-chain
- following the previous assumption, a rational L1 proposer would ensure only their publication transaction lands
- publications must happen at least daily to ensure consecutive proposals can access the required beacon block roots (only the last 8091 are accessible on-chain).
