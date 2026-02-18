---
source: magicians
topic_id: 25017
title: All Core Devs - Testing (ACDT) #48 | Aug 11 2025
author: system
date: "2025-08-05"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-48-aug-11-2025/25017
views: 171
likes: 2
posts_count: 3
---

# All Core Devs - Testing (ACDT) #48 | Aug 11 2025

# Agenda

- Fusaka updates
- Gas limit testing updates

**Meeting Time:** [Aug 11 2025, 14:00 UTC](https://savvytime.com/converter/utc/aug-11-2025/2pm) (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1662)

## Replies

**abcoathup** (2025-08-06):

### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png)

      [All Core Devs - Testing (ACDT) #48 | Aug 11 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-48-aug-11-2025/25017/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACD Testing Call #48 - Aug 11, 2025 - Quick Notes
> Facilitator: Parithosh Jayanthi
> Fusaka Update
> Parithosh shared updates:
>
> Devnet-3 has been running for 10 days, with two non-finality experiments conducted last week.
> Experiment 1: Took out full nodes → ~1 hour of non-finality before recovery in the following epoch.
> Experiment 2: Subset of supernodes removed → ~half a day of non-finality, but finality regained within 20–30 minutes, showing rapid recovery.
> Results analysis showed no major issues…

### Recordings/Stream

- YouTube
- X Livestream [x.com/echinstitute]

### Writeups

- Tweet thread by @poojaranjan
- ACDT#48: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Fusaka upgrade:

Current devnets:

fusaka-devnet-4 [specs] 1.5k nodes with 43.5k validators, ~10% size of mainnet
- fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**poojaranjan** (2025-08-11):

# ACD Testing Call #48 - Aug 11, 2025 - Quick Notes

Facilitator: Parithosh Jayanthi

## Fusaka Update

Parithosh shared updates:

- Devnet-3 has been running for 10 days, with two non-finality experiments conducted last week.
- Experiment 1: Took out full nodes → ~1 hour of non-finality before recovery in the following epoch.
- Experiment 2: Subset of supernodes removed → ~half a day of non-finality, but finality regained within 20–30 minutes, showing rapid recovery.
- Results analysis showed no major issues; bandwidth limits appear fine and overall network health is good.

### Next step:

Test with a subset of nodes (especially supernodes) capped at 1–2 Mbps bandwidth to simulate unreliable supernode participation. This is planned for next week.

## Private Mempool Update

- Bharat shared that there’s a way to directly send transactions to builders, which is useful for private mempool testing.

### Next step:

- Pari will set up spam testing for the private mempool.
- Once the force transition issue is resolved, Bharat will focus more on spamming tests.

## More on Devnets

### Devnet 3

Pari shared more updates:

- A fork of Prysm with a hook feature (allows changes) has been live on the network for 2 hours with no issues reported.
- Hooks can be extended for more scenarios — share your ideas here.

### Devnet 4 Setup

- Setup coordinated with Sunnyside Labs, with additional testing planned here.
- Network is running fine; next BPO is scheduled in the next 2 hours to assess performance.
- Grafana dashboard available for monitoring.
- Nimbus encountered issues — Dustin is investigating, some details shared by Pari on the call.
- Pari clarified to Pawan that Devnet 4 has no non-finality tests planned but could add them if needed.
- Pawan suggested exploring client behavior under longer finality delays.

### Next step:

- Parithosh will arrange a smaller devnet at the end of Devnet 4.

## Holesky Release & Client Timeline

Parithosh shared updates

- Community feedback indicates no major issues with ad-hoc client releases for Holesky validators.
- James He relayed Preston’s note: “Releasing to holesky off develop isn’t difficult, but it messes with normal flow for releases”.

### Next step:

- will be brought to the next ACD for further discussion.

Pari:

- One EIP-related PR pending: ethereum/execution-apis#678 — comments welcome before merging.

## Gas Limit Testing Updates

- Progress can be tracked here: Syncoor Dashboard
- Mario shared the plan of another benchmark release this week.
- Further on updates, Mario shared that With the updated tool, the Nethermind team can pull the genesis, run benchmarks, and report results.
- Plans to extend benchmarking with another release expected soon.

## Glamsterdam Updates

**BALs**

- No BALs devnet yet, though specs are ready and built on top of Fusaka.

### Next Steps

- Toni & Pari will coordinate on setting up a devnet, possibly using Kurtosis.
- Further discussion planned for ACD on Thursday.

**ePBS**

- Local testing is available via a local branch.
- Ansgar: No strong value in combining ePBS, BALs, and repricing in the same devnet.

### Next Steps

- Pari invited feedback on preferred Fusaka devnet setup.
- Justin Traglia: Plans to merge consensus-specs PR #4476 soon.

## Sunnyside Labs Update

- No major updates today; another report expected tomorrow.

On Gas repricing

- Toni: Highlighted EIP-7904, EIP-7778, EIP-7981, and multidimensional gas EIPs for consideration.
- Pari: Asked if there’s a Meta EIP for gas pricing.
- Ansgar: Confirmed they can create one.
- Pari: Said a Meta EIP would be more useful than referencing individual EIPs.

## Consensus Issues Found with Fusaka

- Marius raised consensus-related concerns for discussion.
- Mario: For EIP-7883, an update will be included in the next EEST release.
- Justin Traglia shared Related PR (in chat): ethereum/execution-spec-tests#1993
- Reth: Issues explained by Dragan are now resolved.
- Marius mentioned: Two issues found for ModExp gas cost, but they are unrelated.
- Pari asked if test coverage is sufficient.
- Mario: Extra coverage would be good; will prepare another devnet release for testing.
- Related PR: ethereum/execution-spec-tests#2005.

## EIP-7825 Discussion

pk910: Asked if the transaction gas limit should also apply to eth_call and which clients have implemented it. Suggested directly adding the limit for checking.

- Marius(in chat): In Geth, the limit is configurable.
- Pari: Agreed to leave it as is for now and revisit the discussion later.

PS: This quick note is based on my following the call live and documenting it simultaneously. If you notice any missing updates or corrections, please share them [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-48---Aug-11-2025).

