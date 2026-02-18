---
source: magicians
topic_id: 24284
title: All Core Devs - Testing (ACDT) #38 | May 26 2025
author: system
date: "2025-05-20"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-38-may-26-2025/24284
views: 189
likes: 1
posts_count: 2
---

# All Core Devs - Testing (ACDT) #38 | May 26 2025

# All Core Devs - Testing (ACDT) #38 | May 26 2025

- May 26, 2025, 14:00 UTC

# Agenda

- Fusaka-devnet-0 status
- PeerDAS testing
- History expiry updates and what our plan is for rollout, releases, docs, testing

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : ACDT
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1554)

## Replies

**poojaranjan** (2025-05-28):

# Interop Testing Call #38 – May 26, 2025 (Quick notes)

**Call led by:** Mario Vega

## Summary

- Fusaka-devnet-0

Devnet-0 to be launched tomorrow with Fulu activation following the next day.

**BPO & Config**

- BPO is live on devnet-0, but the final version of the EIP is still being discussed and will go live in devnet-1 or devnet-2.
- Future devnets will align on genesis dates.

**Devnet 1**

- EIP-7918 confirmed for inclusion.

**CL Spec PR #4323**

- Mixed client feedback on usefulness.
- Decision: Keep open; await further client input.

**PeerDAS Testing**

- Decision: Use PeerDAS Devnet 7 for Electra → Fulu blob testing.
- Malicious EL block tests planned to validate CL rejection behavior.

1. History Expiry

No updates on rollout, testing, or documentation.

## Fusaka-devnet-0 Status

### Test Status

**Mario**

- Latest EEST release includes Fusaka SFI EIPs.
- Hive instance is running, but only Go-Ethereum is currently live.
- Other clients should reach out to Pari or EthPandaOps for access.
- Simulator not ready yet due to significant EEST changes; expected soon.

**Parithosh**

- Fusaka Devnet 0 hive instance: Hive Dashboard

**Barnabas**

- Devnet-0 to be launched tomorrow with Fulu activation following the next day..

### Client Updates

- Erigon (EL): WIP branch exists, not reviewed by Barnabas yet.
- Nimbus (CL): Testing an image internally.
- Lodestar & Lighthouse: No updates.

### Devnet 0 – BPO & Config Discussion

**Pawan**

- BPO EIP is available.

**Pari**

- Live on devnet 0. Specs still in flux; final version may be included in Devnet 1 or 2.

**ethDreamer (Mark)**

- Question on whether the BPO config includes blob schedule.

**Barnabas**

- Yes, genesis includes blob schedule (but only Electra blobs, not Fulu).
- Reference: config.yaml#L194
- Future devnets will align on genesis date.

## Devnet 1 Planning

**SFI’d EIPs:**

- Includes EIP-7918
- Could be slightly delayed to align with Interop in Berlin

**Anders**

- Updated EIP-7918 specs recently: Discussion

**Decision:** EIP-7918 will be included in Devnet 1.

### Demitri’s CL Specs – PR Discussion

**Parithosh**

- CL spec PR 4323 still open.

**Pawan (Lighthouse)**

- Not useful for LH currently, unsure if it helps bandwidth.

**Gajinder (Lodestar)**

- Could reduce latency during multiple peer requests.
- Not useful if most clients use gossip pools.
- Favor of closing this PR

**Manu (Prysm)**

- Doesn’t currently use it but plans to. Wants the PR merged for future readiness.

**Decision:** Wait for more client feedback before closing the PR.

## PeerDAS Testing

### Client Updates

**Manu (Prysm)**

- Development is progressing well on PeerDAS testing.

**Pawan (Lighthouse)**

- BPO implementation is still in progress for Devnet 0.
- Merged a few synchronization-related fixes.
- Resolved a bug with getblock; the fix has been merged.
- Expected to be ready for the Fulu fork on Devnet 0.

**Sunnyside Labs**

- Conducted PeerDAS testing last week: Test Report – May 20
- Setup: 60 nodes with Execution Layer (EL) + Consensus Layer (CL).
- Focus: Assess number of blobs that can be reached; current goal is to reach 72 blobs per block.

#### Observations

- Bottlenecks identified in getblobs v2.
- No significant performance difference observed between enabling and disabling getblobs.
- Grandine was requesting blobs multiple times.
- Grandine tested in standalone configuration.
- Lighthouse and Prysm were performing better with or without getblobs enabled.
- Further analysis and findings will be shared in the Discord channel.

#### Discussion & Troubleshooting

**Pawan**

- Asked if fresh sync tests were done with current parameters.

**Sunnyside**

- Yes, syncing was challenging:

Multiple nodes failed to start.
- Required manual force-syncs and full network restarts.

**Francesco**

- Asked about high CPU usage on supernodes.

**Finding**

- High CPU usage was only observed on Lodestar supernode, not other clients.

### Additional Testing Requests

**Parithosh**

- Asked if any client teams had specific scenarios they want tested for PeerDAS.

**Manu**

- Suggested testing:

Syncing in both finalizing and non-finalizing networks.
- Running a few hours of blob transactions from Electra to Fulu.

**Pari**

- Recommended using PeerDAS Devnet 7, which already contains Fulu.
- Agreed on basic sync testing.

**Manu**

- Confirmed Electra can be run on PeerDAS Devnet 7 for testing purposes.

### Malicious Block Testing

**Marius**

- Proposed creating an EL block with invalid/cell block transactions to ensure:

It gets correctly rejected by CL clients.

**Pari**

- Acknowledged the need for a malicious block and that Marius can assist with its creation.

**Pawan**

- Compared the testing with the rejection scenario to a deserialization failure over the Engine API.

### EEST Testing Opportunity

**Mario**

- Mentioned a new testing type in EEST that could support this use case.

**Marius**

- Clarified that getblobs tests are different; this is focused more on consensus-level block validation.

**Mario**

- Acknowledged the distinction.

## History Expiry

No updates shared.

