---
source: magicians
topic_id: 25250
title: All Core Devs - Testing (ACDT) #51 | Sep 1 2025
author: system
date: "2025-08-26"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-51-sep-1-2025/25250
views: 81
likes: 3
posts_count: 5
---

# All Core Devs - Testing (ACDT) #51 | Sep 1 2025

### Agenda

- Fusaka devnet status updates
- Syncing issues on devnet-3
- Gas limit testing updates
- Glamsterdam testing updates: BALs and ePBS
- Sunnyside labs testnet updates

**Meeting Time:** Monday, September 01, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1703)

## Replies

**abcoathup** (2025-08-27):

### Notes

[Add links to notes]

### Recordings/Stream

- YouTube
- X Livestream [x.com/echinstitute]

### Writeups

- Quick recap by @poojaranjan
- by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**poojaranjan** (2025-09-01):

# ACD Testing Call #51 - Sep 01, 2025 - Quick notes

Facilitator: Mario Vega

**EthPandaOps** (pk910):

- Unfinality observed, but recovered.
- Finality lost again ~30 minutes ago.

#### Client teams update:

**Prysm** (Manu):

- 3 nodes down.
- Reth and Erigon issues ongoing.
- Invalid block reported → under investigation.
- Memory issue also reported in Prysm.
- For prysm-{erigon,reth}-1: wiping DBs may solve the issue, but awaiting EL inputs to avoid masking underlying problems.

**Lighthouse** (Pawan):

- Progress made on new sync algorithm.
- 1–2 edge cases remain to be fixed.
- New sync strategy likely to be merged soon.
- Will also investigate offline nodes.
- Request: Once finality is recovered on Devnet 3, schedule a planned chain split (similar to last week) with prior notice. This would allow client teams to monitor logs and metrics in real time.

**Lodestar** (Matthew):

- All nodes in sync.
- Only Reth is running optimistically → will be resolved.
- Client  was stable on Devnet 3 earlier, now investigating what caused the regression.

**pk910**: Acknowledged chain split request — will coordinate.

**Mario**:

- Syncing issues are starting to dissipate.
- Continue monitoring Devnet 3 before moving forward.
- Asked about timeline for Devnet 5.

pk910: Tentatively next week, pending fixes.

## Syncing Issues on Devnet-3

**Mario**

- Lodestar and Lighthouse have already provided input.
- Asked if there were additional comments.
- Matthew agreed with the request for advance notice on chain splits, to better monitor metrics.
- Findings from Non-finality

No major issues reported.
- Everything went fine during the recovery.

### Summary

- Devnet-5 is expected to launch next week.

pk910 (chat)

- Will ping offline devnet-3 nodes shortly; also observed the unfinality.
- Regarding the split test: it will be redone, but only once the chain stabilizes. Splitting again without stability would not be useful.

## Gas Limit Testing Updates

**Kamil**

- Last week: worked on a stateful scenario using the existing database.
- Currently collaborating with Jochem B. on a new testing scenario.
- Developing generic tests.
- Default setup uses the EEST scenario.
- Addressed questions from the Besu team; they will investigate the current bottleneck.

**Besu** (Ameziane)

- Team assigned a developer to improve various arithmetic opcodes.
- Implementation is new; testing will require more time.

**Mario**

- Preparing a new EEST version, expected this week.
- This will support further testing.
- Plans to coordinate with Besu once the new EEST is ready.

### On 60M Gas Limit

- Kamil: Increasing to 60M can only be considered after Besu’s fixes are complete.
- Once all issues are resolved, discussion on 60M can proceed.

### ModExp on Geth

- Marius: Progressing gradually; a PR is open on Geth.
- This remains a priority.
- Will provide an update next week on timeline and next steps.

## Glamsterdam Testing Updates: BALs and ePBS

**BALs** (Toni)

- No major updates on his side.
- Testing (Felipe):

Spec side has been cleaned up and is passing tests.
- Codebase merging is in progress; once completed, things look good to move forward.

**ePBS** (Terence)

- Working on spec tests in the Consensus spec repo.
- Tests are already available.
- For anyone implementing the new spec: tests exist—please reach out to Terence with questions.

**Note**

[Consensus Spec v1.6.0-alpha.6](https://github.com/ethereum/consensus-specs/releases/tag/v1.6.0-alpha.6) has been released, fixing the bug reported last week. Client teams are encouraged to check and update.

## Sunnyside Labs Testnet Updates

**Sunnyside** (J)

- Preparing for Devnet-5 launch next week.
- Continuing interim testing in the meantime.

## Meeting Summary

- Finality issues on Devnet-3 are being addressed.
- Teams will sync up next week for the Devnet-5 launch.

PS: These are quick notes captured during the live call. Any necessary edits or suggestions can be made [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-51---Sep-01-2025).

---

**system** (2025-09-01):

### Meeting Summary:

The team discussed ongoing issues with Devnet 3, including finality problems and execution payload challenges across different clients, while also reviewing progress on syncing algorithms and testing capabilities. They agreed to conduct chain split testing on Devnet 3 after implementing recent fixes and planned to launch non-finality testing the following week. The team also covered updates on stateful scenarios testing, gas limit considerations, and preparations for Devnet 5, with various team members providing progress reports on their respective areas of work.

**Click to expand detailed summary**

The team discussed the status of Devnet 3, where they recovered from an unfinity test but are now experiencing finality issues. Manu reported that Prism has issues with execution payloads for RUST and Erigon, while Pawan mentioned progress on a new sync algorithm for Lighthouse. Matthew noted that Lodestar has made significant progress with syncing, though they have an optimistic ref node. The team agreed to investigate the recent degradation of the network and discussed the need for a planned shutdown of Devnet 3 before moving to Devnet 5.

The team discussed plans for chain split testing, agreeing to notify each other before conducting future tests to allow monitoring of logs and metrics. They decided to reproduce the chain split test on Devnet 3 once fixes are merged, rather than on Devnet 5, to assess the effectiveness of recent improvements. Mario confirmed that non-finality testing for Devnet 3 would likely launch the following week, with the team planning to discuss it further in the next meeting. Kamil provided an update on gas limit testing, noting progress on stateful scenarios testing with existing databases and chains.

The team discussed progress on stateful scenarios and testing, with Kamil reporting success in executing and consuming transactions, and working with Jochem on maintenance-specific scenarios. They addressed issues with Besu team testing and agreed to use a combination of Ethereum tests and the latest eest release for full coverage. The group also discussed gas limit considerations, with Kamil noting that 60 million could be considered once fixes from Besu and Gav are implemented and stateful testing outputs are available. Finally, they touched on Glamsterdam testing updates, consensus specs, and Sunnyside Labs’ preparation for Devnet 5, with J mentioning they would start preparing for the launch early next week.

### Next Steps:

- pk910 to monitor Devnet 3 nodes regarding the current non-finality issues.
- pk910 to organize another chain split test on Devnet 3 with prior notice to client teams.
- Client teams to prepare for Devnet 5 launch next week.
- Kamil to polish and document EST integration and merge it this week for gas benchmarks.
- Kamil to execute compute scenarios on mainnet data to check for differences.
- Besu team to continue testing and implementing improvements for arithmetic opcodes .
- Marius to provide an update next week on GET’s progress with modexp improvements and Go Standard Library upstream.
- Client teams to review the new consensus specs release.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: kRt^2c@v)
- Download Chat (Passcode: kRt^2c@v)

---

**system** (2025-09-02):

### Meeting Summary:

The team discussed ongoing issues with Devnet 3, including finality problems and execution payload challenges across different clients, while also reviewing progress on syncing algorithms and testing capabilities. They agreed to conduct chain split testing on Devnet 3 after implementing recent fixes and planned to launch non-finality testing the following week. The team also covered updates on stateful scenarios testing, gas limit considerations, and preparations for Devnet 5, with various team members providing progress reports on their respective areas of work.

**Click to expand detailed summary**

The team discussed the status of Devnet 3, where they recovered from an unfinity test but are now experiencing finality issues. Manu reported that Prism has issues with execution payloads for RUST and Erigon, while Pawan mentioned progress on a new sync algorithm for Lighthouse. Matthew noted that Lodestar has made significant progress with syncing, though they have an optimistic ref node. The team agreed to investigate the recent degradation of the network and discussed the need for a planned shutdown of Devnet 3 before moving to Devnet 5.

The team discussed plans for chain split testing, agreeing to notify each other before conducting future tests to allow monitoring of logs and metrics. They decided to reproduce the chain split test on Devnet 3 once fixes are merged, rather than on Devnet 5, to assess the effectiveness of recent improvements. Mario confirmed that non-finality testing for Devnet 3 would likely launch the following week, with the team planning to discuss it further in the next meeting. Kamil provided an update on gas limit testing, noting progress on stateful scenarios testing with existing databases and chains.

The team discussed progress on stateful scenarios and testing, with Kamil reporting success in executing and consuming transactions, and working with Jochem on maintenance-specific scenarios. They addressed issues with Besu team testing and agreed to use a combination of Ethereum tests and the latest eest release for full coverage. The group also discussed gas limit considerations, with Kamil noting that 60 million could be considered once fixes from Besu and Gav are implemented and stateful testing outputs are available. Finally, they touched on Glamsterdam testing updates, consensus specs, and Sunnyside Labs’ preparation for Devnet 5, with J mentioning they would start preparing for the launch early next week.

### Next Steps:

- pk910 to monitor Devnet 3 nodes regarding the current non-finality issues.
- pk910 to organize another chain split test on Devnet 3 with prior notice to client teams.
- Client teams to prepare for Devnet 5 launch next week.
- Kamil to polish and document EST integration and merge it this week for gas benchmarks.
- Kamil to execute compute scenarios on mainnet data to check for differences.
- Besu team to continue testing and implementing improvements for arithmetic opcodes .
- Marius to provide an update next week on GET’s progress with modexp improvements and Go Standard Library upstream.
- Client teams to review the new consensus specs release.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: kRt^2c@v)
- Download Chat (Passcode: kRt^2c@v)

