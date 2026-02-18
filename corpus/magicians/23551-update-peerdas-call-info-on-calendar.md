---
source: magicians
topic_id: 23551
title: Update PeerDAS call info on calendar
author: system
date: "2025-04-15"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/update-peerdas-call-info-on-calendar/23551
views: 43
likes: 0
posts_count: 1
---

# Update PeerDAS call info on calendar

Hi!  It seems that there is a link discrepancy on the calendar.  Can we update that to match the one in the break-out room issue.



      [github.com/ethereum/pm](https://github.com/ethereum/pm/issues/1441)












####



        opened 08:02PM - 08 Apr 25 UTC



        [![](https://avatars.githubusercontent.com/u/94402722?v=4)
          will-corcoran](https://github.com/will-corcoran)





          Breakout


          PeerDAS


          DA







# PeerDAS Breakout Room - Call 25 | April 15, 2025

- [Apr 15, 2025, 14:00 UTC]([…]()https://savvytime.com/converter/utc/apr-15-2025/2pm)
- Duration in minutes : 60

### Resources
- [Zoom Link](https://ethereumfoundation.zoom.us/j/82343923303?pwd=aGLyX8xtcVeaDni8mhQi7NNIkzwuUT.1&jst=2)
- [Ethereum Protocol Call calendar](https://calendar.google.com/calendar/u/0?cid=Y191cGFvZm9uZzhtZ3JtcmtlZ243aWM3aGs1c0Bncm91cC5jYWxlbmRhci5nb29nbGUuY29t)
- [PeerDAS-PM.md](https://github.com/ethereum/pm/blob/master/Breakout-Room-Meetings/PeerDAS/PeerDAS-pm.md)
- [Google Doc Meeting Notes](https://docs.google.com/document/d/1Ng2IrCe28kTt1BnIsjtMlKHq2MHgaja24LhFXSvqfJQ/edit?tab=t.0#heading=h.2za2utdyu31m)
- [Previous call](https://github.com/ethereum/pm/issues/1425)
- Facilitator email: [will@ethreum.org](mailto:will@ethreum.org)
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
|------|------------|----------------|
| [Lighthouse](https://github.com/sigp/lighthouse/issues?q=is%3Aissue%20state%3Aopen%20label%3Adas) | Jimmy + Sunnyside Labs IC | Fixed node instability bug with DA check; implemented cell proof computation and distributed blob publishing for full nodes. |
| [Prysm](https://github.com/prysmaticlabs/prysm/pull/14129) | Manu & Terence + Francis & Niram from Base | Completed validation pipeline for data; ready for getBlobsV2/getPayloadV5 integration; testing with Smokeping. |
| [Teku](https://github.com/Consensys/teku/issues/9274) | Dmitrii + Jerone Ost from Soneium | Updated distributed blob recovery per spec; working on cell proof implementation; fixed canonical/non-canonical sidecar API bug. |
| [Nimbus](https://github.com/status-im/nimbus-eth2/pulls?q=is%3Apr+is%3Aopen+fulu+) | Agnish & Dustin | Paused custody work for getBlobsV2; improved column syncer with full node reconstruction syncing working reliably. |
| [Lodestar](https://github.com/ChainSafe/lodestar/issues/7429) | Matt K, Katya + Derek & Hugh from Base | Completed validator custody implementation with PR ready; working on backfilling and planning getBlobsV2/getPayloadV5 implementation. |
| [Grandine](https://github.com/grandinetech/grandine/pull/55) | Hangleang & Saulius Grigaitis | Testing cell proof integration; fixing runtime crash with >30 blobs; adding support for multiple KZG backends. |

### EL Client Teams
| Team | Active ICs | Call 24 Update |
|------|------------|----------------|
| [Geth](https://github.com/ethereum/go-ethereum/pulls) | Felix, Marius, Lightclient | Transitioning getBlobsV2 and cell proof calculation from proof-of-concept to robust implementation; new image available. |
| [Nethermind](https://github.com/NethermindEth/nethermind/pull/8417) | FCLC, Marcin | Fixed API bug; participating in custody testing; planning efficiency improvements for engine API getBlobsV2. |
| [Besu](https://github.com/hyperledger/besu/pulls) | tbd | No update provided. |
| [Erigon](https://github.com/erigontech/erigon/pulls) | tbd | No update provided. |
| [Reth](https://github.com/paradigmxyz/reth/pull/15534) | Roman | Merged implementation PR; fixed blob schedule and multi-blob transaction handling bugs; supporting meeting time consolidation. |
| [ethereumjs](https://github.com/ethereumjs/ethereumjs-monorepo/pulls) | Gajinder | Waiting on PRs; implementing new transaction wrapper this week; working on getBlobsV2 and payload/blobs bundle changes.<br> - Open PR: [tx: add peerdas blob transactions support](https://github.com/ethereumjs/ethereumjs-monorepo/pull/3976) |

## Devnet / Testing Updates
### PandaOps Updates
- `peerdas-devnet-6` is now live 🚀 (replacing `peerdas-devnet-5` ☠️)
- **Spamoor Configuration Discussion**
  - Review PR: [github.com/ethpandaops/spamoor/pull/30](https://github.com/ethpandaops/spamoor/pull/30)
  - Topic: Configuring Spamoor to generate blob transactions
  - Issue: User experiencing difficulties with blob generation configuration
  - Proposed solution: Use modified version with incremental blob count functionality
    - Specific branch adds parameter: `--throughput-increment-interval=600`
    - Gradually increases blob counts over time
    - Potential value for future BPO fork testing

### Sunnyside Updates
- [04/08 Update](https://testinprod.notion.site/Sunnyside-Devnet-Updates-04-08-1ce8fc57f546803eb68af80d5d9842c8)
- [Proposal for Unified EL Metrics](https://testinprod.notion.site/Proposal-for-Unified-EL-metrics-1d28fc57f54680f2a3cbfe408d7db4b8)

#### Sunnyside Plan for This Week
1. Begin with 04/08 baseline metric for CL working without `getBlobs`
2. Conduct similar testing with additional ELs beyond Geth and Nethermind
   - Focus on varying blobpool performance
3. Identify additional timing metrics for PeerDAS
4. Compare performance with vs. without `getBlobs` optimizations

## Spec / EIP Discussions

### Open Specs & Discussions
- Consensus: Remove placeholder MAX_BLOBS_PER_BLOCK_FULU ([link](https://github.com/ethereum/consensus-specs/issues/4266))
- Consensus: Implement BPO fork blob limit logic ([link](https://github.com/ethereum/consensus-specs/issues/4267))
- Engine API: Add EIP-7594 (PeerDAS) related change ([link](https://github.com/ethereum/execution-apis/pull/630))
- Builder: Add EIP-7594 (PeerDAS) related change ([link](https://github.com/ethereum/builder-specs/pull/117))

#### Builder Spec Discussion
- **Current Team Consensus:**
  - Prefer removing full responses
  - Return only revealed execution payloads
  - Leverage existing getBlobs function
- **Implementation Timing Options:**
  - Wait until after main feature completion
  - Include in Fusaka-devnet-0
- **Next Steps:**
  - Consult stakeholders from MEV ecosystem before finalizing

### Draft Specs & Discussions
- Update EIP-7594: Add blob count per tx limit via blobSchedule ([link](https://github.com/ethereum/EIPs/pull/9623))
- Update EIP-7594: Polish EIP, expand rationale ([link](https://github.com/ethereum/EIPs/pull/9588))

### Discussion Item 01 | BPO Blob Schedule Config

#### EL Clients
- Four options for EL BPO blob schedule config
- Key questions:
  - Use of named forks
  - Inclusion of timestamps in fork structs
  - Treatment of BPO changes as hard forks with new fork hashes

#### CL Clients
- Two options for CL BPO blob schedule config
- Key questions:
  - Naming convention scalability
  - Parsing considerations for BPO*_{EPOCH,MAX_BLOBS} format
  - Parameter specification for error handling and ordering rules

### Discussion Item 02 | Naming Convention Request

Request to rename the PRs with `Add PeerDAS related changes` titled prs to `BeaconAPI: <the same thing repeated again>`, in general `Name of the repo/module: ` the peerDAS related changes happen within?
- This helps keep the PRs more easily distinguishable as multiple items that need ot be tracked.

### Discussion Item 03 | Review High-Level Schedule

| Date(s) | Item |
|------|-----------|
| April 9th | peerdas-devenet-6 live! |
| May ~5th | Pectra Mainnet |
| ~June 1st | fusaka-devnet-0 (w/ BPO) |
| June 8-14 | EL / CL Interop |
| Post June 14 | Audits: KZG libraries (c-kzg-4844, rust-eth-kzg, go-eth-kzg) |












Link on calendar:


      ![image](https://us06st1.zoom.us/zoom.ico)

      [Zoom](https://ethereumfoundation.zoom.us/j/87225793361?pwd=Pe0H4sFMX9wr1HFRLfQo3yrDB6a4hk.1)



    ![image](https://us06st3.zoom.us/static/6.3.34004/image/thumb.png)

###



Zoom is the leader in modern enterprise cloud communications.










Link on issue:


      ![image](https://us06st1.zoom.us/zoom.ico)

      [Zoom](https://ethereumfoundation.zoom.us/j/82343923303?pwd=aGLyX8xtcVeaDni8mhQi7NNIkzwuUT.1&jst=2)



    ![image](https://us06st3.zoom.us/static/6.3.34004/image/thumb.png)

###



Zoom is the leader in modern enterprise cloud communications.










[GitHub Issue](https://github.com/ethereum/pm/issues/1474)
