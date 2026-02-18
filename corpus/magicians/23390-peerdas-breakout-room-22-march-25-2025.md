---
source: magicians
topic_id: 23390
title: PeerDAS Breakout Room #22 | March 25, 2025
author: system
date: "2025-04-05"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/peerdas-breakout-room-22-march-25-2025/23390
views: 46
likes: 0
posts_count: 1
---

# PeerDAS Breakout Room #22 | March 25, 2025

# PeerDAS Breakout Room | Call 22 | March 25, 2025

**Date/Time:** [Mar 25 (Tues), 2025, 10:00 UTC](https://savvytime.com/converter/utc/mar-25-2025/10am)

**Duration:** 60 minutes

**[Zoom link](https://ethereumfoundation.zoom.us/j/81645423396?pwd=hL37Lys5NdrKNUxgE13OAUqihgXaTP.1)**

**[Ethereum Protocol Call calendar](https://calendar.google.com/calendar/u/0?cid=Y191cGFvZm9uZzhtZ3JtcmtlZ243aWM3aGs1c0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t)**

**[Notes](https://docs.google.com/document/d/1Ng2IrCe28kTt1BnIsjtMlKHq2MHgaja24LhFXSvqfJQ/edit?tab=t.0#heading=h.2za2utdyu31m)**

**[Previous call](https://github.com/ethereum/pm/issues/1364)**

## Agenda

1. Client updates

Feature Completeness

Validator Custody
2. Distributed Blob Publishing
3. Move Cell Proof Computation to Tx Sender

implemented by one EL client req’d for devnet-6
4. getBlobsV2 Implementation
5. Cell Proof PoC by Francis

Prysm PoC
6. Geth PoC
7. Source of Truth link (please review below, validate or provide)
8. Devnet updates

peerdas-devnet-5
9. peerdas-devnet-6
10. Spec discussion

See below for EIP and Spec-related questions
11. Open discussion

TEMP CHECK: Ship peerdas-devnet-6, be feature-complete (PeerDAS* and EOF) and ship fusaka-devnet-0  by June 1.

> *Distributed Blob Publishing and E.L. Cell Proof Computation

## Agenda Supplements

[PeerDAS Roadmap GoogleDoc](https://docs.google.com/document/d/1MXf5zTU58mRj0Yq88EPBP1gCJzWTY9FRfUdpZjcfgqw/edit?tab=t.0)

### Client-related Items

Having a single ‘source of truth’ for others to track your progress on PeerDAS-related implementation would be quite helpful. If you could either provide a link (if one is not listed below for your team) or validate the link (if one is shown) for your team prior to Call 23, that would be great.

#### CL Team PeerDAS Progress Sources of Truth

| Team | Source of Truth | Active Contributors |
| --- | --- | --- |
| Prysm | TODO | Manu, Niran |
| Lighthouse | TODO | Jimmy, Pawan, Dapplion, ethDreamer |
| Teku | TODO | Dmitrii |
| Nimbus | - | Agnish |
| Lodestar | TODO | Matthew Keil, Katya, g11tech, Derek G |

#### EL Team PeerDAS Progress Sources of Truth

| Team | Source of Truth | Active Contributors |
| --- | --- | --- |
| Geth | - | Marius, Lightclient |
| Nethermind | - | ?? |
| Reth | - | ?? |
| Besu | - | ?? |
| Erigon | - | ?? |

#### Others (not exhaustive, just for reference)

| Team / Org | Active Contributors | Key Responsibilities |
| --- | --- | --- |
| Base | Francis, Hugh C | research and implementation |
| Sunnyside Labs | Mininny, J, Taem, Tei | Max Blobs Analysis & Data Collection |
| ethPandaOps | Pari / Barnabas | Devnet coordination & testing |
| ethPandaOps | Sam / Matty / Andrew | Data collection & analysis |
| ethPandaOps | pk910 / Rafael | Tooling |
| EFR - Consensus R&D | Francesco | Validator Custody Spec |
| EFR - Protocol Security | Justin Traglia | Consensus Spec |
| EFR - Research Ops | Will | Coordinator |

### Testing Items

#### Tooling Updates

| Team | Item | Discussion Topic |
| --- | --- | --- |
| ethPandaOps | Spamoor & tx spammer | Status on new tx format implementation? |
| ethPandaOps | p2p testing tool | Progress on tool for client <> RPC reliability testing? |
| ethPandaOps | checkpointz | Update on implementation for devnet-6? |
| Sunnyside Labs & Sam | Root Cause Analysis | Status on investigation of 10-blob performance failure? |
| Sunnyside Labs & Sam | Random Configuration Testing | Progress on network failure analysis? |

#### Misc Testing Discussion Items

| Category | Item | Discussion Topic |
| --- | --- | --- |
| Testing Configuration | Deploy at least one node with “withhold column” flag for testing | Status? |
| Testing Configuration | Verify all nodes are properly configured as full nodes | Status? |
| Testing Configuration | Pre-mine node keys to ensure coverage across all column subnets | Status? |
| Testing Configuration | Implement flag to advertise false CGC count (to trick other nodes into thinking the false flag belongs to a supernode, but not serve RPC requests) | Status? |
| Networking | Address inode limitation issue for Prysm (currently working on fix to include all subnets in one file) | Status? |
| Networking | Consider implementing batch publishing columns optimization | Status? |

### Spec-related Items

| Item | Status / Discussion Items |
| --- | --- |
| EIP-7594 | PeerDAS, championed by FrancescoAppears to be comment free and ready to merge - any updates on the status of this EIP? |
| EIP-7892 (draft) | BPO Harkforks, drafted by ethDreamerWhat is the current status of this? Considered for Inclusion in Fusaka? |
| EIP-7870 (draft) | Hardware and Bandwidth Recommendation for Validators and Full Nodes, Pari(?)Discuss: potential impact on PeerDAS & likelihood of being SFI for Fusaka. |
| EIP-7872 (draft) | Max Blob Flag for Local Builders, Francesco(?)Discuss: potential impact on PeerDAS & likelihood of being SFI for Fusaka. |

| Type | Item | Contributor | Status / Discussion Items |
| --- | --- | --- | --- |
| consensus | Basic Validator Custody | Francesco | Done, confirm |
| consensus | make validator custody static for beacon node run session | g11tech | Ready for review - minor, open comment |
| consensus | Complete validator custody specs | GabrielAstieres | Pending review from Stokes |
| consensus | Add note about using getBlobs with DataColumnSidecar in Fulu | Justin Traglia | Open issue, discuss |
| consensus | Add Distributed Blob Publishing to Fulu networking spec | Jimmy | New (s/o Jimmy) appears to be ready to merge, discuss |
| consensus | Update BlobsBundle for Fulu | Justin Traglia | Working through some comments with g11tech |
| execution | Update the type for blob_gas_used | Shashwat-Nautiyal | Working through some comments with Guru |
| execution tests | feat(tests): peerdas tracking issue | dancertopz | Tracking issue for the required testing coverage for the EL for PeerDAS |
| builder | Add EIP-7594 (PeerDAS) related changes | Francis | New (s/o Francis) - cell proof-related - appears to be ready to merge |
| execution api | Add EIP-7594 (PeerDAS) related changes | Francis | Updated (s/o Francis) - cell proof-related - appears to be ready to merge |
| beacon api | Add EIP-7594 (PeerDAS) related changes | Francis | New (s/o Francis) - cell proof-related - appears to be ready to merge |
| beacon metrics | PeerDAS metrics: add data column, kzg, custody metrics | Katya | Appears to be being maintained as needed |

## Old Issues (consensus spec)

> Please review this list and close any old issues that are no longer active.

- Consider Blob Sidecar slashing conditions
- reverse_bits_limited helper for polynomial-commitments-sampling.md
- How is MIN_EPOCHS_FOR_BLOB_SIDECARS_REQUESTS guaranteed?
- EIP-7594: PeerDAS open questions
- EIP-7594: Ask for recommandation about sampling
- Enable typecasts for EIP-7594 fork
- Demonstrate adding EIP7594_MAX_BLOBS_PER_BLOCK and EIP7594_TARGET_BLOBS_PER_BLOCK

[GitHub Issue](https://github.com/ethereum/pm/issues/1401)
