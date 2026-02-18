---
source: magicians
topic_id: 25315
title: All Core Devs - Testing (ACDT) #52 | Sep 8 2025
author: system
date: "2025-09-02"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-52-sep-8-2025/25315
views: 60
likes: 1
posts_count: 4
---

# All Core Devs - Testing (ACDT) #52 | Sep 8 2025

### Agenda

- Fusaka devnet status updates

fusaka-bugs - HackMD
- shadowfork testing - current issues with geth/erigon due to blob schedule fields

Devnet 5 timeline
Gas limit testing update
Glamsterdam testing updates: BALs and ePBS

**Meeting Time:** Monday, September 08, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1710)

## Replies

**poojaranjan** (2025-09-08):

# ACD Testing Call #52 - Sep 08, 2025 - Quick notes

Facilitator: Barnabas Busa

## Fusaka Devnet – Status Updates

Barnabas

- Devnet 3 participation remains high at 82%
- A few issues reported with Nimbus and Erigon
- Fixes from both clients are expected by tomorrow

**Erigon** (Andrew A.)

- No fixes yet; identified a flaw in Erigon logic
- Debugging continues — the issue is tricky and requires more time
- Positive: Batch created to fix Fusaka Devnet 5 Hive dashboard
- Barnabas Busa: Note - Hive testnet should be covered by all clients

**Teku** (Enrico)

- Working on one syncing issue
- Merged PR for a rejection issue
- Investigating a memory issue in RETH (unrelated to earlier memory issue)

**RETH** (Roman)

- Investigating an issue with the pair
- Preparing a new release soon
- Issue has not occurred in previous devnets; will be addressed in Devnet 5

### Summary

- All known bugs were discussed
- Barnabas Busa: Looking for a  from every client to confirm trunk branches are ready

References:

- Syncing Bugs Notes
- Validator Summary (Devnet 3)
- Dora

## Devnet 5 – Timeline & Readiness

**Grandine** (Saulius)

- All syncing issues fixed
- Devnet 3 is syncing properly

**Prysm** (Manu)

- Missing feature: backfill
- Ready for Devnet 5 on the develop branch

**Teku** (Enrico)

- Current state looks fine
- Bug discussed is not a blocker

**Lighthouse** (Pawan)

- PR open with a different sync strategy
- No blockers at the moment

**Lodestar** (Matthew)

- Identified a bug → hoping to fix tonight
- Refactor in progress, cleanup to be merged ASAP
- No blockers for Devnet 5, can be run locally.

**Nimbus** (Agnish)

- Blocking issue: bug in block validation pipeline for super node
- Fixes expected in the next few hours
- Team discussing another non-finality test for Devnet 3
- Devnet 5 readiness: trunk branch updates should be ready by early morning

**Geth** (lightclient)

- Ready for Devnet 5, no blockers

**Reth** (Roman)

- Ready

**Nethermind** (Lukasz)

- Fine, no blockers

**Erigon** (Andrew)

- Bug identified, investigation ongoing
- Main branch is ready

**Teku** (Justin)

- Ready

### Summary

- Most clients are ready or near-ready for Devnet 5
- Remaining blockers: Nimbus (super node bug), Erigon (under investigation)
- Devnet 5 can be scheduled for the second half of this week

## Shadowfork Testing

Barnabas Busa

- Main blocker: Geth and Erigon – issues due to blob schedule fields
- Shadowforks currently not possible on these two clients
- Geth (Matt): still investigating a regression noted in the syncing bugs doc; issue is related to the state history feature, not Fusaka.

## Client Releases for Holesky

Barnabas Busa

- Target: By next Monday?
- Nethermind: Yes
- Timestamp: Not yet decided → can be set async and shared on Thursday’s call
- Erigon: Difficult due to other client releases; one week is too soon, two weeks would be better

From chat

- Roman: I don’t mind. It would be close to our current release, but this shouldn’t impact the decision to proceed quickly with the Holesky fork.
- Pawan: Need to check with the rest of the team as well.
- Matt: Need to check with the team

### Summary

- Barnabas Busa: Will accelerate Devnet 5
- A full release for Holesky is not expected
- Targeting CR by 22 Sept
- BPO value still to be determined — once set, everything will be ready

## Gas Limit Testing Update

Nethermind (Marcin):

- Running EEST test
- Tooling available to run stateful tests
- Completed experiment with Hoodi
- Next step: Jochem to run the test

## Glamsterdam Testing Updates: BALs & ePBS

### BALs

Jared:

- BALs Testing team made an initial release
- Two issues found with EELS implementations of the spec, currently being addressed
- Timeline: Geth readiness very soon; unclear if other teams are aligned

Nethermind (N/m):

- Prototype available

Filipe:

- Specs need updates, currently under review
- Another release is expected this week

Mario Vega: [BAL Release v1.0.0](https://github.com/ethereum/execution-spec-tests/releases/tag/bal%40v1.0.0)

EEST (Spencer):

- Released EEST v5.0.0
- Clients are aware; see release notes
- Future test releases will come from EELS

General State Tests:

- Updated post-Cancun
- Refilled general state tests → recommended running fixture tests
- Ensure all clients are passing
- More info in release notes; reach out with questions

### ePBS

Barnabas

- Consensus specs are still under review
- Will circle back once updated

That concludes today’s agenda.

(PS: This is a quick note from the call. If there is any correction, please share [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-52---Sep-08-2025))

---

**system** (2025-09-08):

### Meeting Summary:

The team reviewed the status of Devnet 3 and discussed plans for Devnet 5, with most clients reporting readiness despite some pending issues that need to be addressed. They discussed shadow forks for testnets and the timing of releases for various components, including Holesky and execution specifications. The conversation ended with updates on gas limit testing, block level access lists, and plans to merge execution specs with Eels, along with discussions on timelines for devnet 0 launch and ongoing testing efforts.

**Click to expand detailed summary**

The team discussed the status of Devnet 3, which has an 82% participation rate, but faces issues with clients like Nimbus and Ergon. Andrew explained that Ergon is still investigating a flaw in its logic for long unwinds, and a fix is not expected today. Enrico reported that Teku has made progress but is experiencing memory issues with Reth 2, which is behind in synchronization. Roman mentioned that a reorg-related bug fix is ready in the main branch of Reth, and including it in Devnet 5 should be sufficient. The team agreed to proceed with Devnet 5 finalization later today or by tomorrow, pending fixes from affected clients.

The team discussed the readiness of various clients for Devnet 5, with most clients reporting they are prepared, though some have pending issues like missing features or bugs that are not blockers. Barnabas proposed organizing a nonfinality event by the end of the day to test recovery, followed by scheduling Devnet 5 for the second half of the week. The team agreed to announce the Devnet 5 schedule once confirmed, aiming for a large network similar to Devnet 4.

The team discussed plans for shadow forks for testnets, noting that Gas and Ergon currently cannot override blob schedule values, which is a blocker. Andrew mentioned that a fix for Gas is in progress, and Barnabas requested it by the end of the week. The team also debated the timing of releases for Holesky, with Barnabas suggesting a pre-release by next Monday, but Andrew and others agreed this timeline was too soon. They decided to aim for a release by September 22nd, allowing time to determine BPO values and align with Erigon’s schedule.

The team discussed updates on gas limit testing, block level access lists, and the release of new execution specification tests. Enrico mentioned that gas limit testing updates would be ready by Wednesday, while Jared reported that testing against Geth revealed some issues with block level access lists that are being addressed. Felipe confirmed a pre-release for block level access lists was re-released, and Spencer-TB announced the release of EEST v5.0.0. The team also discussed timelines for devnet 0 launch and the need for further review and updates of the block access list specifications.

Spencer discussed plans to merge execution specs with Eels, explaining that test releases will continue to come from Eels, but Python tests and the framework will move to Eels. He also outlined the use of test fixtures, recommending the use of the “fixtures develop” tarball for Osaka tests, and noted changes to transaction gas limit cap tests. Barnabas mentioned that instances specs were still under review and testing was ongoing, with plans to follow up next week. The conversation ended with no additional updates or discussions.

### Next Steps:

- Nimbus team to fix the bug in the block validation pipeline for super nodes by tonight.
- Erigon team to investigate and fix the issue with long reorgs logic.
- Erigon team to implement the override for blob schedule values by the second half of this week.
- Geth team to complete the fix for overriding blob schedule values.
- Client teams to prepare for Devnet 5 launch in the second half of this week.
- Client teams to aim for releases by September 22nd with BPO values determined.
- Nethermind team to continue gas limit testing with tooling and test on top of Mainnet.
- EL teams to review the block level access list implementation and address spec issues.
- Testing team to release updated block level access list tests this week after spec review.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: qD4h*DS&)
- Download Chat (Passcode: qD4h*DS&)

---

**system** (2025-09-09):

### Meeting Summary:

The team reviewed the status of Devnet 3 and discussed plans for Devnet 5, with most clients reporting readiness despite some pending issues that need to be addressed. They discussed shadow forks for testnets and the timing of releases for various components, including Holesky and execution specifications. The conversation ended with updates on gas limit testing, block level access lists, and plans to merge execution specs with Eels, along with discussions on timelines for devnet 0 launch and ongoing testing efforts.

**Click to expand detailed summary**

The team discussed the status of Devnet 3, which has an 82% participation rate, but faces issues with clients like Nimbus and Ergon. Andrew explained that Ergon is still investigating a flaw in its logic for long unwinds, and a fix is not expected today. Enrico reported that Teku has made progress but is experiencing memory issues with Reth 2, which is behind in synchronization. Roman mentioned that a reorg-related bug fix is ready in the main branch of Reth, and including it in Devnet 5 should be sufficient. The team agreed to proceed with Devnet 5 finalization later today or by tomorrow, pending fixes from affected clients.

The team discussed the readiness of various clients for Devnet 5, with most clients reporting they are prepared, though some have pending issues like missing features or bugs that are not blockers. Barnabas proposed organizing a nonfinality event by the end of the day to test recovery, followed by scheduling Devnet 5 for the second half of the week. The team agreed to announce the Devnet 5 schedule once confirmed, aiming for a large network similar to Devnet 4.

The team discussed plans for shadow forks for testnets, noting that Gas and Ergon currently cannot override blob schedule values, which is a blocker. Andrew mentioned that a fix for Gas is in progress, and Barnabas requested it by the end of the week. The team also debated the timing of releases for Holesky, with Barnabas suggesting a pre-release by next Monday, but Andrew and others agreed this timeline was too soon. They decided to aim for a release by September 22nd, allowing time to determine BPO values and align with Erigon’s schedule.

The team discussed updates on gas limit testing, block level access lists, and the release of new execution specification tests. Enrico mentioned that gas limit testing updates would be ready by Wednesday, while Jared reported that testing against Geth revealed some issues with block level access lists that are being addressed. Felipe confirmed a pre-release for block level access lists was re-released, and Spencer-TB announced the release of EEST v5.0.0. The team also discussed timelines for devnet 0 launch and the need for further review and updates of the block access list specifications.

Spencer discussed plans to merge execution specs with Eels, explaining that test releases will continue to come from Eels, but Python tests and the framework will move to Eels. He also outlined the use of test fixtures, recommending the use of the “fixtures develop” tarball for Osaka tests, and noted changes to transaction gas limit cap tests. Barnabas mentioned that instances specs were still under review and testing was ongoing, with plans to follow up next week. The conversation ended with no additional updates or discussions.

### Next Steps:

- Nimbus team to fix the bug in the block validation pipeline for super nodes by tonight.
- Erigon team to investigate and fix the issue with long reorgs logic.
- Erigon team to implement the override for blob schedule values by the second half of this week.
- Geth team to complete the fix for overriding blob schedule values.
- Client teams to prepare for Devnet 5 launch in the second half of this week.
- Client teams to aim for releases by September 22nd with BPO values determined.
- Nethermind team to continue gas limit testing with tooling and test on top of Mainnet.
- EL teams to review the block level access list implementation and address spec issues.
- Testing team to release updated block level access list tests this week after spec review.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: qD4h*DS&)
- Download Chat (Passcode: qD4h*DS&)

