---
source: magicians
topic_id: 23329
title: PeerDAS Breakout Call #23, Apr 1, 2025
author: system
date: "2025-03-31"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/peerdas-breakout-call-23-apr-1-2025/23329
views: 44
likes: 0
posts_count: 1
---

# PeerDAS Breakout Call #23, Apr 1, 2025

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

| Team | Link | Call 22 Updates |
| --- | --- | --- |
| Prysm | link | NOTE: Status of bug• Worked on redesigning the database to fix issues with data column storage• Added missing unit tests for PeerDAS• Worked w/ Francis from Base worked on getBlobV2 and equivalent API when proposing a block |
| Lighthouse | link | • Still addressing sync issues• Created spec PR for distributed publishing (see below)• Working on making Lighthouse compliant with the spec |
| Teku | link | • Released validator custody, started testing with DevOps• Added new PeerDAS metrics with help from Katya (see below)• Working to resolve various bugs |
| Lodestar | link | • Made progress with refactoring and unit testing• Onboarding a new contributor to help with validator custody• Addressing peer management issues to ensure there are peers listening to all subnets• Looking at improving how peers connect to those listening to correct topics |
| Nimbus | - | - |

| Team | Link | Call 22 Updates |
| --- | --- | --- |
| Geth | - | NOTE: Status of implementation requiring updates (noted by @parithosh )• Open pull request about encoding, limited progress due to vacation schedules |
| Nethermind | - | NOTE: Discuss status of implementation and testing status• Has proof of concept branch with API methods implemented, ready to join DevNet as execution layer client |
| Reth | - | • All types implemented, waiting for specs to be locked in, 1-2 days from being ready |
| Besu | - | - |
| Erigon | - | - |

## Devnet / Testing Updates

`peerdas-devnet-6` ([specs](https://notes.ethereum.org/@ethpandaops/peerdas-devnet-6))

#### Devnet-6 Open Question:

- Devnet-6: Who is going to work on EELS/EEST for proof computation to tx sender?

#### STEEL Updates:

1. EL changes are limited to the network wrapper that encapsulate blob transaction information and blob data into a gossipable object between peers.  This can be tested via Hive’s Engine simulator.  Tests will be added / updated here.
2. As there are no changes to the EVM or EL block header, noo changes are required to EELS execution-specs or EEST’s consensus test set.  Therefore:

- No peerdas-devnet-6 specific release will be made from EEST
- EL clients can proceed with testing using the latest develop release (provided their branches are based on Prague) without waiting for a specific peerdas-devnet-6 release from EEST.

## Spec / EIP Discussions

### P0 : Open Spec PRs

- EIP | Update EIP-7594: include cell proofs in network wrapper of blob txs (one last comment)
- consensus-specs | Transition period from 4844-style blob transactions to PeerDAS-style blob transactions (link)
- cell proof computation | Add EIP-7594 (PeerDAS) related changes (beacon-api) (builder-specs) (engine-api)
- execution-spec-tests | feat(tests): peerdas tracking issue (guessing this is not a blocker, just for tracking)

### P1 : Draft Spec PRs

- beacon-metrics | PeerDAS metrics: add data column, kzg, custody metrics (link)
- execution-specs | More post Prague re-factors (link)

### Spec Updates:

- Consensus Specs: v1.5.0-beta.4 is scheduled for release Wed April 2nd ( @jtraglia )

## Open Discussion

Proposal: Blob schedule for Fusaka ([here](https://hackmd.io/@ralexstokes/blob-acc-2025#Blob-schedule-for-Fusaka)) by [@ralexstokes](/u/ralexstokes)

| Step | Increase | Blob count |
| --- | --- | --- |
| T = 0 | 1x | (6, 9) |
| T = 2 weeks | 2x | (12, 18) |
| Previous T + 2 months | 2x | (24, 36) |
| Previous T + 2 months | 2x | (48, 72) |

[GitHub Issue](https://github.com/ethereum/pm/issues/1415)
