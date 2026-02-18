---
source: magicians
topic_id: 24660
title: All Core Devs - Testing (ACDT) #42 | June 30 2025
author: system
date: "2025-06-25"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-42-june-30-2025/24660
views: 135
likes: 0
posts_count: 3
---

# All Core Devs - Testing (ACDT) #42 | June 30 2025

# All Core Devs - Testing (ACDT) #42 | June 30 2025

- June 30 2025, 14:00 UTC

# Agenda

- Fusaka updates
- Gas limit testing updates

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

[GitHub Issue](https://github.com/ethereum/pm/issues/1593)

**YouTube Stream Links:**

- Stream 1 (Jun 30, 2025): https://youtube.com/watch?v=dUCFEs0wlAA

## Replies

**system** (2025-06-30):

### Meeting Summary:

The meeting focused on addressing technical issues in Sousa Devnet 2, including bug fixes for Teku and Nethermind clients and ongoing peering problems affecting some clients. The team discussed updates on Fossippi 11.2 network issues and performance testing plans for EIP 7907, while also reviewing progress on various Devnet 2 testing activities including spam tests and MEV-boost implementation. The group concluded by discussing technical aspects of Ethereum Improvement Proposals, including code size lookups and partial responses in the execution engine API, while also addressing gas limit changes and per-transaction blob limits across different client implementations.

**Click to expand detailed summary**

The meeting begins with an update on Sousa Devnet 2. Barnabas reports that there was a non-finality issue over the weekend due to bugs in Teku and Nethermind, which have since been fixed. Several clients experienced database corruptions, and some are currently having peering problems. FLCL explains that the Nethermind bug was related to improperly calculated fork IDs, while Enrico mentions that Teku’s issue was likely caused by a cleanup commit. Gabriel from Besu suggests their sync issue may be unrelated to the blocker changes. The team is continuing to investigate the peering problems affecting some clients.

The team discusses ongoing issues with the Fossippi 11.2 network, including a Prism bug that caused a fork and has since been resolved with a new spec test. They also mention a current spamming issue affecting the network’s performance. Jochem expresses interest in conducting performance tests on the devnet to evaluate the impact of the newly introduced EIP 7907, which increases the maximum contract size. The team agrees to continue investigating these issues and to implement necessary tests in upcoming client releases.

The group discusses updates on various aspects of Devnet 2 testing. Jochem and an unknown speaker mention progress on running spamoor tests, with some issues being worked on. Bharath provides an update on MEV-boost and relay testing for Holesky, noting that transactions without blobs are working but there are issues with blob transactions in the relay payload. Parithosh shares that Prysm fixed a bug related to stale validator indices and mentions ongoing work on sync tests. Pawan and Kasey report that their teams are working on implementing backfill functionality, with progress being made but not yet merged.

The discussion focuses on technical aspects of Ethereum Improvement Proposals (EIPs) and client implementation details. Marius expresses concerns about the need for an index for code size lookups, emphasizing potential issues in a stateless world. Ansgar and others discuss the implications of having the index in or out of protocol, including pricing considerations. Jochem mentions ongoing tests to stress-test worst-case scenarios. Mario raises a question about charging for extra size during transaction entry into large contracts. The group agrees to resolve open questions for EIP-7907 and confirm costs for modexp before the upcoming All Core Devs meeting. Marco introduces a topic about allowing partial responses in the get_blobs_v2 API to improve efficiency in cases with private blobs.

The group discusses a proposed change to allow partial responses in the execution engine API. Marco explains that while partial responses are not currently useful, they could be made useful without a hard fork through a gossip sub change. This would enable future optimizations as block parameters scale. Pawan expresses hesitation about merging the change without having the optimization in place, citing concerns about increased serialization load. The group debates whether to include this change proactively for Fusaka and Devnet 3 or implement it later. They decide to create a thread on All Core Devs to collect feedback, with a deadline for the next day to decide on including it in Devnet 3. Sunny Side Lab team provides an update on their testing of Fusaka with Devnet 2 specs, including plans for network bandwidth benchmarking and constraining tests. The group agrees to plan more offensive networks for Fusaka testing after Devnet 3 specs are finalized.

The group discusses the per-transaction blob limit, with FLCL proposing to set it at 9 blobs. However, others recall a previous agreement to set it at 6 blobs. They decide to open a new PR to discuss this further, with the current consensus being to keep it at 6 blobs but make it configurable. The group also addresses gas limit changes, noting that several client teams have released updates with a 45 million gas limit default. They encourage consensus layer teams to update their gas limits accordingly. Lastly, there’s a brief discussion about potentially lowering the gas limit on devnet-1, but this requires further consultation with Jochem.

### Next Steps:

- Jochem to run performance tests on Devnet 2, including calling many contracts and testing the 7907 EIP.
- Client teams to review and provide feedback on Marco’s proposal for partial responses in get_blobs_v2 API by tomorrow.
- Sunnyside lab team to share a write-up on their Devnet 2 testing results in the interop chat.
- Client teams to plan more offensive networks and deeper reorgs testing for Devnet 3.
- FLCL to open a new PR and discussion thread regarding the per-transaction blob limit.
- CL teams to update their gas limit to 45 million, following the EL client updates.
- Pk and Jochem to discuss lowering the gas limit on Devnet 1.
- Client teams to prepare for discussing Devnet 3 specifications at the upcoming ACDE meeting.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: D$=SsLy8)
- Download Chat (Passcode: D$=SsLy8)

---

**system** (2025-06-30):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=dUCFEs0wlAA

