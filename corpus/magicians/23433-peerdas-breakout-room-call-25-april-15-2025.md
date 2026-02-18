---
source: magicians
topic_id: 23433
title: PeerDAS Breakout Room - Call #25 | April 15, 2025
author: system
date: "2025-04-08"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/peerdas-breakout-room-call-25-april-15-2025/23433
views: 74
likes: 0
posts_count: 1
---

# PeerDAS Breakout Room - Call #25 | April 15, 2025

# PeerDAS Breakout Room - Call 25 | April 15, 2025

- Apr 15, 2025, 14:00 UTC
- Duration in minutes : 60

### Resources

- Zoom Link
- Ethereum Protocol Call calendar
- PeerDAS-PM.md
- Google Doc Meeting Notes
- Previous call
- Facilitator email: will@ethreum.org
- Facilitator Telegram: @corcoranwill

# Agenda Overview

A.  Client Updates

B.  Devnet / Testing Updates

C.  Spec / EIP Discussion

D.  Open Discussion

# Agenda Details

## Client Updates

### CL Client Teams

| Team | Active ICs | Call 24 Update |
| --- | --- | --- |
| Lighthouse | Jimmy + Sunnyside Labs IC | Fixed node instability bug with DA check; implemented cell proof computation and distributed blob publishing for full nodes. |
| Prysm | Manu & Terence + Francis & Niram from Base | Completed validation pipeline for data; ready for getBlobsV2/getPayloadV5 integration; testing with Smokeping. |
| Teku | Dmitrii + Jerone Ost from Soneium | Updated distributed blob recovery per spec; working on cell proof implementation; fixed canonical/non-canonical sidecar API bug. |
| Nimbus | Agnish & Dustin | Paused custody work for getBlobsV2; improved column syncer with full node reconstruction syncing working reliably. |
| Lodestar | Matt K, Katya + Derek & Hugh from Base | Completed validator custody implementation with PR ready; working on backfilling and planning getBlobsV2/getPayloadV5 implementation. |
| Grandine | Hangleang & Saulius Grigaitis | Testing cell proof integration; fixing runtime crash with >30 blobs; adding support for multiple KZG backends. |

### EL Client Teams

| Team | Active ICs | Call 24 Update |
| --- | --- | --- |
| Geth | Felix, Marius, Lightclient | Transitioning getBlobsV2 and cell proof calculation from proof-of-concept to robust implementation; new image available. |
| Nethermind | FCLC, Marcin | Fixed API bug; participating in custody testing; planning efficiency improvements for engine API getBlobsV2. |
| Besu | tbd | No update provided. |
| Erigon | tbd | No update provided. |
| Reth | Roman | Merged implementation PR; fixed blob schedule and multi-blob transaction handling bugs; supporting meeting time consolidation. |
| ethereumjs | Gajinder | Waiting on PRs; implementing new transaction wrapper this week; working on getBlobsV2 and payload/blobs bundle changes. - Open PR: tx: add peerdas blob transactions support |

## Devnet / Testing Updates

### PandaOps Updates

- peerdas-devnet-6 is now live  (replacing peerdas-devnet-5 )
- Spamoor Configuration Discussion

Review PR: github.com/ethpandaops/spamoor/pull/30
- Topic: Configuring Spamoor to generate blob transactions
- Issue: User experiencing difficulties with blob generation configuration
- Proposed solution: Use modified version with incremental blob count functionality

Specific branch adds parameter: --throughput-increment-interval=600
- Gradually increases blob counts over time
- Potential value for future BPO fork testing

### Sunnyside Updates

- 04/08 Update
- Proposal for Unified EL Metrics

#### Sunnyside Plan for This Week

1. Begin with 04/08 baseline metric for CL working without getBlobs
2. Conduct similar testing with additional ELs beyond Geth and Nethermind

Focus on varying blobpool performance
3. Identify additional timing metrics for PeerDAS
4. Compare performance with vs. without getBlobs optimizations

## Spec / EIP Discussions

### Open Specs & Discussions

- Consensus: Remove placeholder MAX_BLOBS_PER_BLOCK_FULU (link)
- Consensus: Implement BPO fork blob limit logic (link)
- Engine API: Add EIP-7594 (PeerDAS) related change (link)
- Builder: Add EIP-7594 (PeerDAS) related change (link)

#### Builder Spec Discussion

- Current Team Consensus:

Prefer removing full responses
- Return only revealed execution payloads
- Leverage existing getBlobs function

**Implementation Timing Options:**

- Wait until after main feature completion
- Include in Fusaka-devnet-0

**Next Steps:**

- Consult stakeholders from MEV ecosystem before finalizing

### Draft Specs & Discussions

- Update EIP-7594: Add blob count per tx limit via blobSchedule (link)
- Update EIP-7594: Polish EIP, expand rationale (link)

### Discussion Item 01 | BPO Blob Schedule Config

#### EL Clients

- Four options for EL BPO blob schedule config
- Key questions:

Use of named forks
- Inclusion of timestamps in fork structs
- Treatment of BPO changes as hard forks with new fork hashes

#### CL Clients

- Two options for CL BPO blob schedule config
- Key questions:

Naming convention scalability
- Parsing considerations for BPO*_{EPOCH,MAX_BLOBS} format
- Parameter specification for error handling and ordering rules

### Discussion Item 02 | Naming Convention Request

Request to rename the PRs with `Add PeerDAS related changes` titled prs to `BeaconAPI: <the same thing repeated again>`, in general `Name of the repo/module: ` the peerDAS related changes happen within?

- This helps keep the PRs more easily distinguishable as multiple items that need ot be tracked.

### Discussion Item 03 | Review High-Level Schedule

| Date(s) | Item |
| --- | --- |
| April 9th | peerdas-devenet-6 live! |
| May ~5th | Pectra Mainnet |
| ~June 1st | fusaka-devnet-0 (w/ BPO) |
| June 8-14 | EL / CL Interop |
| Post June 14 | Audits: KZG libraries (c-kzg-4844, rust-eth-kzg, go-eth-kzg) |

[GitHub Issue](https://github.com/ethereum/pm/issues/1441)
