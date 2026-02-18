---
source: ethresearch
topic_id: 15059
title: "Wisp: ZK-based Cross-Rollup-Communication Protocol"
author: Daniel-K-Ivanov
date: "2023-03-15"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/wisp-zk-based-cross-rollup-communication-protocol/15059
views: 2714
likes: 10
posts_count: 4
---

# Wisp: ZK-based Cross-Rollup-Communication Protocol

# Wisp: Cross-Rollup-Communication Protocol

Daniel, Architect at LimeChain (blockchain development company) and part of LimeLabs - R&D Divison.

## Abstract

The following aims to describe an enshrined Cross-Rollup-Communication protocol for data transfer between rollups, completely aligned with Ethereum’s rollup-centric future and supporting the Ethereum community.

The draft [paper](https://limelabs.tech/blog/publications/introducing-wisp) elaborates on the economic incentives for the actors participating in the protocol, presents a CRC message flow, and reviews the security and scalability implications of the protocol.

## How it works

Wisp is (1) an on-chain SNARK-based light client and (2) a verification mechanism for the storage of a rollup. The on-chain light client makes sure that the destination rollup can trust and reason about a specific execution state root at a specific height of Ethereum L1. Based on this root, smart contracts can reason about the inclusion (or not) of a certain piece of information inside any rollup anchoring with Ethereum L1. The way that the data inclusion reasoning happens will be specific for each source rollup.

The proposed system includes relayers as actors who transfer data from a source rollup into a destination rollup. A successful data transfer requires:

1. Ethereum executionStateRoot posted on the Destination Rollup
2. Merkle Inclusion Proof (from Ethereum L1) of the root of the Source Rollup
3. Merkle Inclusion Proof (from Source Rollup) of the storage slots that must be proven and for the Destination rollup to verify the integrity of the data transfer.

**Proving the L1 Execution State Root**

The CRC protocol incorporates an on-chain light client that follows the [Ethereum Sync Protocol](https://github.com/ethereum/annotated-spec/blob/98c63ebcdfee6435e8b2a76e1fca8549722f6336/altair/sync-protocol.md) and updates its head through the usage of ZK-SNARKs. The ZKP proves that the majority of the SyncCommittee has signed a given block header.

**Proving the Rollup State Root**

The `root` of the Source rollup is posted on the Rollup’s L1 Contract address. Merkle Inclusion Proof of the storage key holding the Source Rollup state is provided to the CRC contract on the destination network. Using the `executionStateRoot` already proven from the last step, the contract verifies the state root of the source rollup.

**Proving the Data to be transferred**

Merkle Inclusion Proof of the storage key holding the data inside the Source Rollup is provided to the CRC contract on the destination network. Using the already proven source rollup state, the contract verifies the raw data that must be transferred.

## Alpha Version

There is a live alpha version of the protocol that uses a SNARK similar to [Proof-of-Consensus](https://github.com/succinctlabs/eth-proof-of-consensus) to prove the L1 Execution State Root (step 1).

- Draft Paper - Introducing Wisp - a Cross-Rollup Communication Protocol
- Demo Application - https://demo.wispprotocol.com/
- Docs - https://docs.wispprotocol.com/

## How is this different from other initiatives?

- Ethereum rollup centric - Wisp is specifically focused on the Ethereum ecosystems and its rollups. It recognizes the nuances of the rollup-centric vision of Ethereum and is not designed nor intended to become a “cross-chain” initiative.
- Open-source public good. A cross-rollup communication protocol should be 1) open-source (non-negotiable), 2) public good and ideally 3) built in the open with contributions (or at least input) from different teams. A public good does not exclude having a sustainable revenue stream, but it does exclude rent-seeking behaviour, centralization and optimizing for profit (rather than impact).
- Security. Absolutely crucial. The ideal CRC solution must provide security beyond crypto-economics and incentives. A preferable approach here would step on the security of L1 Ethereum and complement that with additional cryptography (zk proofs). Wisp does this through SNARKs rather than economical incentives.
- Decentralization. There is no multi-sig controlling a bridge. Anyone can participate as a relayer in the Wisp protocol. No actor is special or permissioned - anyone can assume any of the protocol roles. The protocol’s decision-making should also decentralize over time if it becomes a key part of the ecosystem.
- Neutrality. The protocol should facilitate interoperability in the Ethereum ecosystem and avoid servicing certain rollups or applications at expense of others.

## An always-open invitation to join and contribute

Wisp is intended to be completely permissionless and built-in public. We’ve modelled our approach by the work of the Flashbots initiative - being a public good and completely in line with Ethereum. For Wisp to be permissionless and neutral, it would require multiple diverse parties to join the initiative. Below are some top-of-mind ways to join and contribute.

## Feedback and support

We are still early in the development and hope to get feedback from the Ethereum community and the Ethereum thought leaders. Any critical feedback and improvement suggestions are welcomed and appreciated. Feel free to comment here or reach out in [discord](https://discord.gg/kqudMyWbws).

## A shortlist of topics to further explore and collaborate

Here are some unexplored or underoptimized aspects of Wisp. We would love to see collaborators and suggestions in these or any other aspects of the protocol.

- Fast-tracking Ethereum finality - how not to need to wait 12 minutes for block finality
- Dealing with rollups finality - how to deal with the (not)finalized state of a rollup.
- Optimizing and combining the state relay proofs - this could mean completely moving away from Circom and Groth16 if needs be.
- Optimizing the multiple Merkle inclusion proofs - for the Ethereum execution root or the storage inclusion in a rollup
- Moving away from the sync protocol committee and basing on the wider validator set - is this needed and beneficial?

## Supporting rollups

We would love to support all rollups. At the moment we support Optimism Bedrock-style rollups. We’ve explored several other rollups but would need closer collaboration with the roll-up teams in order to support them. This is mainly due to differences in the state management of most ZK rollups. We would like to invite any interested rollups to get in touch - we would love to align with you and add as many rollups as possible.

## Building on top of Wisp

Protocol, without applications on top of it, is worth nothing. We’ve started exploring building sample applications on top of it (much like the demo one). If you are interested in being a cross-rollup app developer please get in touch. We would love to make it so that is super convenient and easy for your dapp to live multi-rollup.

## Replies

**ralexstokes** (2023-03-15):

you mention bedrock-style rollups and it looks like you can just query for the latest L1 blockhash in the `L1Block` contract linked here: [Differences between Ethereum and Optimism | Optimism Docs](https://community.optimism.io/docs/developers/build/differences/#opcode-differences-2)

instead of needing to include an on-chain light client (and moreover prove/verify a SNARK of the transition), you can just prove whatever source rollup state this way blockhash->state root->source rollup contract->source rollup storage key(s)

it seems like if you go this route you don’t even need any relay actor…

the downside here is that you have to wait for the next L1 block and we may want to message cross-rollup regardless of the L1 activity – here we could explore having on-chain light clients where the source rollup and destination rollup are light clients of each other

this is basically the IBC construction from cosmos but again if you are just trusting an honest majority of a committee, we have a relatively weak trust model as corruption of that committee means authorization of arbitrary messages that seem to be coming from the source rollup – to get around this, we need some kind of fault proving scheme, e.g. optimistic or validity proofs run inside the rollup

---

**Daniel-K-Ivanov** (2023-03-16):

Thank you for the feedback [@ralexstokes](/u/ralexstokes)! Getting feedback on the optimal construction for the model is the most important thing at the moment, so we greatly appreciate it.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/r/bcef8e/48.png) ralexstokes:

> you mention bedrock-style rollups and it looks like you can just query for the latest L1 blockhash in the L1Block contract linked here: Differences between Ethereum and Optimism | Optimism Docs
>
>
> instead of needing to include an on-chain light client (and moreover prove/verify a SNARK of the transition), you can just prove whatever source rollup state this way blockhash->state root->source rollup contract->source rollup storage key(s)
>
>
> it seems like if you go this route you don’t even need any relay actor…

You are correct! There is the option of using the Optimism system contract for accessing the L1 Blockhash and it would provide a faster transfer of CRC messages for the Bedrock-based `destination` rollups. Our mental model so far was that:

1. Execution State Root of L1 (step 1) should always be derived from the SNARK-based on-chain light client
2. MIPs of Rollup state and Source roll-up storage (steps 2 and 3) are custom to the source rollup for which an adaptor will be required

Based on your comment, it seems that we must change our model for the execution state root to:

> Execution State Root may be retrieved from an adapter (e.g accessing the L1Block contract in the case of Optimism), but if such a thing is not present within a Rollup (we want this protocol to support as many rollups as possible), we can always fallback to a SNARK based on-chain light client, for which the only requirement of the destination rollup is to support ECADD, ECMUL and ECPAIRING for verifying the ZKP.

Generally speaking, we were targeting a more reusable solution that could work on as many rollups possible. It’s just the case that we selected Bedrock-based rollups. F.e if we are to add Arbitrum, zkSync, Starknet or others, this would not be possible since not all rollups have on-chain access to the L1 blockhash.

> if you are just trusting an honest majority of a committee, we have a relatively weak trust model as corruption of that committee means authorization of arbitrary messages that seem to be coming from the source rollup – to get around this, we need some kind of fault proving scheme, e.g. optimistic or validity proofs run inside the rollup

Wisp Alpha version uses SyncCommittee honest majority assumption ([Proof-of-Consensus](https://github.com/succinctlabs/eth-proof-of-consensus)), however, there are projects like [DendrETH](https://github.com/metacraft-labs/DendrETH), which are working on a full validator set ZKP. Their approach would provide the strongest trust model from the options available.

---

**Perseverance** (2023-03-18):

Based on the feedback gathered publicly and privately, I wanted to highlight and post for discussion the following possible improvement points of the protocol. They should further align the ecosystem together and utilize existing infrastructure.

## Aggregating Public State Relay

While the initial version of the protocol highlights state relayers as actors running the software for generating SNARK_{L1State} and submitting it towards C_{L1LightClient}, this also introduces a software risk - a bug inside this software can cause complete failure of the whole system.

Furthermore, this positions Wisp as a competitor inside the “Onchain Light Client” space, rather than the aligning initiative it strives to be.

As a means, to address this risk, Wisp can move into “State Relay Aggregation”. Public State Relayers can be delivering their L1 state proofs to the destination rollups and the protocol can start using these and utilizing these. Due to the deterministic nature of the Sync Protocol, the aggregation of multiple Light client sources will further enhance the security, lower the trust assumptions and lower the risk for the system.

In addition, the State Relay fees will now be flowing back to the community and to the actors doing the state relay work. This creates a new revenue stream for these actors and aligns the whole system together.

## Utilizing Available Anchors

Thanks [@ralexstokes](/u/ralexstokes)

The proposed protocol specifies the Light client-based, state relay phase as a necessary phase for the communication to occur. While this is generally correct, there are cases like Optimism Bedrock and Taiko, where the L1 state is immediately available.

In these cases, it makes sense for the protocol to use them as a source of the L1 state rather than forcing the existence (and the costs) of running onchain L1 Light Client.

## Optimising Delivery Message

The biggest cost factor for most rollups is the size of the calldata they need to anchor inside L1. With this in mind, the Delivery Message transaction is quite a bulky one and almost all of it eventually goes to L1. This makes the message delivery a costly process and risks the scalability of the system.

A possible improvement is the creation of Computational Integrity Proof to minimize the calldata footprint inside the L2s and respectively the L1s. Moving into ZK proving system (f.e. Groth16) that produces a minimally sized proof will enable the overhead of Wisp to be as little as possible.

