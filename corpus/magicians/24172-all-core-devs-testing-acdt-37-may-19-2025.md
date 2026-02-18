---
source: magicians
topic_id: 24172
title: All Core Devs - Testing (ACDT) #37 | May 19 2025
author: system
date: "2025-05-14"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-37-may-19-2025/24172
views: 236
likes: 2
posts_count: 4
---

# All Core Devs - Testing (ACDT) #37 | May 19 2025

# All Core Devs - Testing (ACDT) #37 | May 19 2025

- May 19, 2025, 14:00 UTC

# Agenda

- Pectra fork retro after data collection
- Fusaka-devnet-0 status
- PeerDAS testing
- Discussion about history expiry and what our plan is for rollout, releases, docs, testing

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1543)

**YouTube Stream Links:**

- Stream 1 (May 19, 2025): https://youtube.com/watch?v=d4sXq0pQLxs

## Replies

**poojaranjan** (2025-05-19):

# Quick notes

**Facilitator**: [@parithosh](/u/parithosh)

## Summary

- ModXP + BPO changes confirmed for Fusaka Devnet 0.
- EL-only BPO hardfork agreed.
- CL-side signaling discussion ongoing. Likely to avoid h/f.
- PeerDAS testing and spec PRs progressing.
- Perfnet v2 & Hoodi updates planned.

**Next Steps**:

- Terence: Create Consensus Spec Issue
- Pari: Update EIP for EL handling of BPO
- Raúl: Finalize spec structure and open Consensus Dev thread
- All clients: Prepare for Devnet 0 testing next week

## Pectra Fork Retro

- No issues reported post data collection.

## Fusaka Devnet 0 Status

- Interop EIPs for Fusaka listed on Discord.
- ModXP EIPs approved by all EL clients: Geth, Besu, Reth, Nethermind.
- Fusaka Devnet 0 spec

### BPO Proposal (Marius)

- Proposal includes scheduling explicit forks:

Example format:

```json
"bpo1": {
  "timestamp": 1747670415,
  "target": 9,
  "max": 12,
  "baseFeeUpdateFraction": 5007716
}
```

Treated as **EL-only hardfork**; CL remains unchanged.

**Discussion Points**:

- CL teams prefer avoiding unnecessary fork boilerplate.
- Marius: keep changes minimal, EL-only is cleaner.
- Potuz: prefer handshake signaling if hardfork can be avoided.
- Gajinder: handshake-only leaves room for inconsistent state.

**Next Steps**:

- Consensus Spec Issue #4331 to be created by Terence.
- EIP to be updated by Pari.
- Raúl to lead long-term spec design and create a Consensus Dev channel thread.

**Decision**: Agreement reached for Fusaka Devnet 0 with ModXP + BPO changes.

## PeerDAS Testing

- Devnet 7 is live.
- Checkpoint sync available here
- All clients actively testing codecs.

**Status**:

- Target release next week for ModXP and PeerDAS.
- BPO tests to be run on Kurtosis (confirmed by Mario).

## PeerDAS Spec Discussion

- PR: beacon-APIs #524
- Discussed local flag and validator-blinded block behavior.
- Pari to reach out to maintainers for merge.

## P2P Propagation Testing

**Discussion between Potuz and Raúl** (Zoom chat):

- Proposal to rerun PandaOps-style tests with 1000+ distributed nodes.
- Reference: EthResearch thread

## Builder Specs

- Builder spec for Fusaka updated (Barnabas, Alex Stokes confirmed).

## Devnet & Release Planning

- Pari suggested, Devnet 0 completion will trigger team prep for release.
- Perfnet v2 (mainnet-aligned) in progress – led by Kamil.

**Hoodi Testing**:

- Plan to test 60M block size and attestation slashing.

**Decision**: Proceed with Hoodi block size test plan.

## History Expiry

- No new updates.
- Portal client call scheduled post-meeting for interested teams.

This is a copy from [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#Interop-Testing-Call-37-%E2%80%93-May-19-2025).

---

**system** (2025-05-19):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

The meeting begins with a discussion about the recent Petra update, with Parithosh noting that no significant issues have been reported by client teams. The main focus then shifts to planning for Fusaka Devnet 0. Parithosh outlines the EIPs included in this devnet, which are Pierdas, MoD XP upper limit, MoD XP gas cost increase, and blob parameter only hard forks. All client teams present (including Besu, Geth, Reth, EthJS, and Nethermind) express agreement with including both MoD XP EIPs in Fusaka Devnet 0. Parithosh shares a link to the Fusaka Devnet 0 specifications and invites teams to reach out once their clients are ready for testing.

The group discusses how to handle Blob-carrying Proof of Obligation (BPO) changes in Ethereum. Marius suggests treating BPOs as normal hard forks on the execution layer, using existing mechanisms to update fork IDs and specify forks. This approach would limit the number of BPOs that can be specified but is seen as sufficient. On the consensus layer side, Potuz notes that while the peering issue is similar, they prefer to avoid a hard fork if possible, suggesting signaling changes at the handshake level instead. Raúl argues that BPO changes alter rules and break backwards compatibility, so they should be treated as hard forks for clear communication. The group considers whether to implement hard forks or explore alternative approaches for both layers.

The group discusses implementing Blob Payload Ordering (BPO) changes for the upcoming Fusaka upgrade. They agree to use a hard fork approach on the execution layer (EL) side, setting multiple BPO times in advance. On the consensus layer (CL) side, they will use a handshake approach. The participants also discuss the need to update the consensus spec regarding BPO changes and peer connections. They clarify that timestamps are not needed in the blob schedule for EL implementations.

The group discusses the format for representing values in the EIP and chain specifications, with Andrew suggesting using decimal integers instead of hexadecimal strings. Mario agrees to investigate potential issues with using decimal numbers in JSON. Parithosh confirms that Nethermind can handle non-hexadecimal formats, and the group agrees to standardize on integers rather than hexadecimal strings. The discussion then shifts to the CL side, where potuz raises concerns about how to signal different forks in the P2P layer. The group considers options for peer scoring and handshake-level signaling but ultimately decides to leave the current implementation as-is to meet the Fukuoka devnet 0 deadline.

The group discusses implementing changes to peer-to-peer networking without a full hard fork. Potuz suggests adding a configuration to the handshake message, while Raúl proposes adding a field to communicate the change on the wire separately. Terence questions whether a hard fork approach might be simpler, given the limited scope of changes. The team agrees to explore adding a protocol field to avoid the traditional hard fork machinery while still implementing the necessary changes. Raúl volunteers to help steer this effort.

The group discusses the progress of PeerDAS implementation and testing. Devnet 7 is running smoothly, with backfilling being the main focus for client teams. Barnabas asks if client teams can ship PeerDAS 0.1 images by next Monday, with at least 3 ELs and 3 CLs needed. Mario indicates that Ethereum spec tests are still in progress, particularly for PeerDAS blobs and proof verification, making next week a safer target for their release. The group agrees to reassess on Thursday whether to proceed with Fusaka devnet 0 or wait for test releases. They also decide to use Kurtosis for BPO testing initially, rather than adding it to execution spec tests immediately.

The group discusses several open issues and pull requests related to Ethereum development. Manu explains a proposed “blind and local” flag for beacon nodes to reduce data transmission between beacon and validator clients. Will brings up an open pull request that hasn’t received attention for weeks, and he plans to follow up with Francis about it. Potuz provides an update on random linear network coding for block broadcasting, noting that its application for blob propagation is still uncertain. Raúl mentions that the peer-to-peer networking team plans to help drive this work, which may require changes to meshing topologies and transport protocols.

The group discusses several topics related to Ethereum development and testing. Barnabas mentions issues with the mock builder for MEV, and Parithosh suggests pushing for more testing once basic Fusaka functionality is working. Kamil provides an update on performance testing, mentioning preparation for a second version of the performance devnet and ongoing research on opcodes. The team agrees to increase the gas limit on the Hoodie testnet to 60 million, following Sepolia’s example. Ben emphasizes the importance of implementing a 10 MB block size limit in Fusaka to prevent network issues. Parithosh notes that they plan to test Hoodie at 60 million gas with attestation slashings to ensure proper network handling.

The group discusses potentially reducing the transaction limit from 30 million to 5 million gas, as transactions above this limit are typically subdividable or related to mining. Parithosh suggests adding this topic to the ECD meeting agenda for wider discussion. The topic of history expiry is briefly mentioned, but no progress updates are provided. Parithosh notes that a portal call about history expiry will follow the current meeting.

### Next Steps:

- Mario to update the EIP and PRs to remove the timestamp inside the BPO array and instead have BPO one time, similar to other hard forks on the EL side.
- Raul to create a thread in the consensus dev channel on EthR&D to discuss the long-term solution for BPO implementation.
- Client teams to continue working on backfill testing for PeerDAS.
- Will to follow up with Francis regarding the open PR for the get blob sidecar spec (PR #524).
- Client teams to start looking at implementing the builder specs for Cancun.
- Kamil and team to prepare the second version of the performance devnet, more aligned with mainnet.
- Core developers to proceed with increasing Goerli gas limit to 60 million.
- Testing teams to test Goerli at 60 million gas limit with slashings included.
- Ben to add the transaction limit discussion as a topic for the next ACD meeting.

### Recording Access:

- Join Recording Session (Passcode: fGV1UJ.%)
- Download Transcript
- Download Chat

---

**system** (2025-05-19):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=d4sXq0pQLxs

