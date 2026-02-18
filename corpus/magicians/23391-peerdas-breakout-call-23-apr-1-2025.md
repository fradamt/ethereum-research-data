---
source: magicians
topic_id: 23391
title: PeerDAS Breakout Call #23 | Apr 1, 2025
author: system
date: "2025-04-05"
category: Protocol Calls & happenings
tags: [peerdas]
url: https://ethereum-magicians.org/t/peerdas-breakout-call-23-apr-1-2025/23391
views: 39
likes: 0
posts_count: 1
---

# PeerDAS Breakout Call #23 | Apr 1, 2025

[Apr 1 (Tues), 2025, 14:00 UTC](https://savvytime.com/converter/utc/apr-1-2025/2pm)

Duration: 60 minutes

[Zoom link](https://ethereumfoundation.zoom.us/j/89262256299?pwd=hAYw0AjbgMYbqPUK1VPC6fqyWiS6jx.1)

[Ethereum Protocol Call calendar](https://calendar.google.com/calendar/u/0?cid=Y191cGFvZm9uZzhtZ3JtcmtlZ243aWM3aGs1c0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t)

[Notes](https://docs.google.com/document/d/1Ng2IrCe28kTt1BnIsjtMlKHq2MHgaja24LhFXSvqfJQ/edit?tab=t.0#heading=h.2za2utdyu31m)

[Previous call](https://github.com/ethereum/pm/issues/1401)

Homepage: [DAS.wtf](https://efdn.notion.site/das-wtf)

# Agenda Overview

A.  Client Updates

B.  Devnet / Testing Updates

C.  Spec / EIP Discussion

D.  Open Discussion

# Agenda Details

## Client Updates

> PRIORITY: All teams to focus on implementing getBlobsV2 and running across clients

### CL Client Teams

| Team | Link | Call 22 Updates | Timely Discussion Topics |
| --- | --- | --- | --- |
| Prysm | link | • Worked on redesigning the database to fix issues with data column storage• Added missing unit tests for PeerDAS• Worked w/ Francis from Base worked on getBlobV2 and equivalent API when proposing a block | • Provide an update on the status of bug |
| Lighthouse | link | • Created spec PR for distributed publishing• Working on making Lighthouse compliant with the spec | • Update on sync issues • Update on: ethpandaops/lighthouse:peerdas-devnet-6-089338d |
| Teku | link | • Released validator custody, started testing with DevOps• Added new PeerDAS metrics with help from Katya• Working to resolve various bugs | - |
| Lodestar | link | • Made progress with refactoring and unit testing• Onboarding a new contributor to help with validator custody• Addressing peer management issues to ensure there are peers listening to all subnets• Looking at improving how peers connect to those listening to correct topics | - |
| Nimbus | - | • Working to improve getBlobsV1 performance (empty & partial responses from EL)• Worked with Sunnyside to accommodate up to 24 blobs• Finished independent column syncer, starting testing ASAP• Improved peer pool and peer mgmt | • FOCUS FOR WEEK: finish validator custodry, start on getBlobsV2 |
| Grandine | - | - | • Completed cell_proofs integration based on spec with the compute_cells methods just implemented by the team• Refactored on reconstruction and block acceptance flow to reconstruct after block accepted• Added withhold-data-columns-publishing flag |

### EL Client Teams

| Team | Link | Call 22 Updates | Timely Discussion Topics |
| --- | --- | --- | --- |
| Geth | - | • Open pull request about encoding, limited progress due to vacation schedules | • Update on bloobpool implementation status |
| Nethermind | - | • Has proof of concept branch with API methods implemented, ready to join DevNet as execution layer client | • Execution Engine Error: Nethermind encountered array length errors when processing engine_getPayloadV5 requests during block production with Lighthouse• Root Cause Identified: Error stemmed from incompatible blob transaction proof formats - client encountered proof-type-v1 transactions (Deneb format) when expecting proof-type-v2 (PeerDAS format with 128 proofs per blob)• Implemented Solution: Modified Nethermind to ignore older proof-format transactions when building Osaka/Fulu blocks (may result in temporarily empty blocks during testing)• Specification Update: Confirmed that new proof types should use wrapper_version 0x01 instead of 0x02 as previously implemented |
| Reth | - | • All types implemented, waiting for specs to be locked in, 1-2 days from being ready | - |
| Besu | - | - | - |
| Erigon | - | - | - |

## Devnet / Testing Updates

`peerdas-devnet-6` ([specs](https://notes.ethereum.org/@ethpandaops/peerdas-devnet-6))

### Devnet-6 Open Question:

- Devnet-6: Who is going to work on EELS/EEST for proof computation to tx sender?

### STEEL Updates

1. EL changes are limited to the network wrapper that encapsulate blob transaction information and blob data into a gossipable object between peers.  This can be tested via Hive’s Engine simulator.  Tests will be added / updated here.
2. As there are no changes to the EVM or EL block header, noo changes are required to EELS execution-specs or EEST’s consensus test set.  Therefore:

- No peerdas-devnet-6 specific release will be made from EEST
- EL clients can proceed with testing using the latest develop release (provided their branches are based on Prague) without waiting for a specific peerdas-devnet-6 release from EEST.

### Sunnyside Updates

**Sunnyside Devnet Updates - 04/01** ([link](https://testinprod.notion.site/Sunnyside-Devnet-Updates-04-01-1c78fc57f5468066ad6cccecc5b79ba5))

**Findings from this week:**

- Different consensus clients show varying blob throughput capacities with Lighthouse handling up to 40 blobs/block, Teku 30 blobs/block, while Prysm and Lodestar manage 25 blobs/block, and Grandine 20 blobs/block.
- The main bottleneck appears to be declining getBlobs hit rates from execution clients, causing increased column reconstruction work and network instability.
- Most consensus clients are performing adequately without relying on getBlobsV2.
Testing strategy for next week:
- Investigate implementation differences causing throughput variances between clients
- Continue debugging Geth’s blobpool behavior
- Test performance with distributed blob publishing
- Conduct tests without EL blob gossiping to measure getBlobs impact
- Run comparative tests with other execution clients using unlimited blobpool sizes.
- Work on standardizing metrics across clients to enable better cross-client performance comparisons.

## Spec / EIP Discussions

### P0 : Open Spec PRs

- EIP | Update EIP-7594: include cell proofs in network wrapper of blob txs (one last comment)
- consensus-specs | Transition period from 4844-style blob transactions to PeerDAS-style blob transactions (link)
- cell proof computation | Add EIP-7594 (PeerDAS) related changes (beacon-api) (builder-specs) (engine-api)
- execution-spec-tests | feat(tests): peerdas tracking issue (guessing this is not a blocker, just for tracking)
- beacon-api | produceBlock and publishBlock: Remove blobs and KZG proofs (link)

### P1 : Draft Spec PRs

- beacon-metrics | PeerDAS metrics: add data column, kzg, custody metrics (link)
- execution-specs | More post Prague re-factors (link)

### Spec Updates:

- Consensus Specs: v1.5.0-beta.4 is scheduled for release Wed April 2nd ( @jtraglia )

## Open Discussion

### Discussion Item #1: BPO Blob Schedule

Proposal: Blob schedule for Fusaka ([here](https://hackmd.io/@ralexstokes/blob-acc-2025#Blob-schedule-for-Fusaka)) by [@ralexstokes](/u/ralexstokes)

| Step | Increase | Blob count |
| --- | --- | --- |
| T = 0 | 1x | (6, 9) |
| T = 2 weeks | 2x | (12, 18) |
| Previous T + 2 months | 2x | (24, 36) |
| Previous T + 2 months | 2x | (48, 72) |

### Discussion Item #2: Beacon API getBlobsSidecar Discusussion

[summary here](https://hackmd.io/@willcorcoran/SJKlKPOakx)

[GitHub Issue](https://github.com/ethereum/pm/issues/1415)
