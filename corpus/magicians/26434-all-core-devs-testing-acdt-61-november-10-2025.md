---
source: magicians
topic_id: 26434
title: All Core Devs - Testing (ACDT) #61, November 10, 2025
author: system
date: "2025-11-05"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-61-november-10-2025/26434
views: 59
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #61, November 10, 2025

### Agenda

### Agenda

#### Fusaka:

- Hoodi BPO Activation updates
- Mainnet client releases status
- Devnet status updates

#### 60M gas limit on mainnet updates:

- State test updates
- Gas limit testing update

#### Glamsterdam Testing Updates:

- BALer updates - bal-devnet-0
- ePBS updates

#### Other Topics:

- Cancel/proceed with next two ACD-T calls

**Meeting Time:** Monday, November 10, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1797)

## Replies

**poojaranjan** (2025-11-10):

# All Core Devs - Testing (ACDT) #61 (Quick notes)

Mario Vega facilitated the call

#### Quick Summary

- Nov 17 & 24 ACD-T calls canceled
- Next call: Dec 1
- Fusaka looking very healthy
- ePBS devnet-0 by mid-Jan
- Prysm release dropping today (per Kasey)

## Fusaka:

### Hoodi BPO Activation updates

Barnabas

- No issues observed in BPO-1, but discovered a release bug in N/M.
- Mentioned a halting issue with Nimbus on Fusaka-devnet-3 — currently under investigation.
- Nearly all Nimbus nodes appear to be affected; ongoing coordination with the Nimbus team.

Marcin (N/M)

- Implemented several bug fixes and released a new Candidate Release (CR).
- Planning another release to address rare edge-case bugs.
- Snap sync is currently broken, but will be resolved soon.
- Targeting v0.2 as “good enough” for the mainnet release.

Pari

- Reported a release bug in Reth.
- BAL-related changes accidentally impacted mainnet client releases.
- Another minor (non-consensus-critical) issue identified in Lighthouse; fix to follow.
- Shared issue link: sigp/lighthouse#6837

Mario

- Summarized:
“Most things look good. The only pending task is investigating the strange RPC requests.”

Enrico (Besu)

- Nodes are detecting data columns via RPC calls (noticed within the past 10–15 minutes).
- Raised a question about potential buggy client behavior in RPC requests.

#### Devnet-3 status updates

- Several nodes ran out of resources around the 20 blocks per blob configuration.
- Additional debugging needed.

#### Mainnet Client Release Status

Jen (Reth)

- Released Fusaka patch: reth v1.9.1

Kasey (Prysm)

- Preston is preparing a new release, expected later today.
- Update: expect the release today.

## 60M gas limit on mainnet updates:

### State test updates

Benchmark Testing

Marcin

- Conducted initial benchmark testing with EIP-7904; results are working as expected.
- Next steps:

Develop a dashboard to reprice N/M and Geth, then compare results.
- Generate new payloads to extend the benchmark analysis.

Ameziane Hamlat

- Suggested including TPS (transactions per second) as an additional metric, since Mgas/s alone may not fully capture performance.
- Highlighted TPS as a potentially more insightful performance indicator.

### Gas limit testing update

- Completed two rounds of testing.
- No further Gas Repricing Breakout sessions are currently planned.

## Glamsterdam Testing Updates:

### BALer updates - bal-devnet-0

Pari

- Planning to launch a new BAL devnet soon.

Stefan

- Asked whether BAL tests are fixed.
- Inquired if client teams have executed the EVM fuzzing scenarios.

Spencer

- Confirmed that previous releases focused on BAL-specific tests.
- Shared release reference: Release bal@v1.4.0 · ethereum/execution-spec-tests · GitHub
- With the EIP-7702-related release, a patch will be issued.
- Working on fixing BPO-related configuration.
- Next release expected by Tuesday/Wednesday, alongside Hive updates.
- Shared Hive dashboard: Hive Results | Ethereum Testing Framework

Notes

- Nethermind failure reported: Discord message

TL;DR — Mario

- Check Hive for latest BAL results.
- Chime in with updates from your respective clients.
- Coordinate with Felipe, Toni, and Raxhvl for follow-ups.

### ePBS updates

Justin Traglia

Justin Tr

- Breakout call held last week — main focus: execution payment value
- Devnet-0 for ePBS expected mid-January at the earliest
- Next breakout scheduled for Dec 5

### Other Topics:

#### Upcoming ACD-T Calls

- Next week = in-person meetings, so no call
- Nov 24 call also canceled
- Back on Dec 1

#### Fusaka Readiness - Confidence Check

Saulius G.

- Asked how comfortable we feel with Fusaka progress given recent bugs

Barnabas (Chat)

- Most bugs are not Fusaka-related.
- Described it as “the smoothest upgrade so far.”

Pari

- “Smoother than the Merge  — all testnets failed during Merge testing”

Ben (N/M)

- Ambitious, but releases are lining up well

Pari

- Offered testing bandwidth for any client teams needing extra validation.

#### Next steps:

- Wait on nimbus to triage issue in devnet 3
- Then coordinate another non-finality test

#### Post-PeerDAS Metrics

Łukasz Rozmej (Chat)

- Asked if mempool stats post-PeerDAS are available.

Pari

- Sam is investigating; Sunnyside Labs dashboards will be shared soon.

#### Client-Side Concerns

Kasey asked about handling:

- Private blobs, and
- Re-org heavy scenarios

Pari: Ref: [Fix race condition by capturing version in goroutine by klim0v · Pull Request #855 · flashbots/mev-boost · GitHub](https://github.com/flashbots/mev-boost/pull/855)

For any changes, please comment [here](https://hackmd.io/@poojaranjan/ACDT59Onwards#All-Core-Devs---Testing-ACDT-61-Nov-10-2025).

---

**system** (2025-11-10):

### Meeting Summary:

The team discussed various technical issues and updates related to the BP01 activation, including bug fixes and version releases, as well as concerns about mainnet and devnet performance. They reviewed progress on benchmark testing, gas pricing, and block-level access list tests, addressing client-related challenges and planning further development and testing phases. The team also discussed upcoming releases, testing priorities, and performance concerns, deciding to cancel certain meetings and continue with planned testing and development activities.

**Click to expand detailed summary**

Mario welcomed participants to ACDT 61 on November 10th and noted that the agenda was similar to previous weeks. He inquired about significant events from the previous week’s BP01 activation, to which Barnabas responded that there were no significant events to discuss. Mario then suggested moving on to the next topic, which was the status of the BP01 activation.

The team discussed issues with BPO2 and a bug in Nethermind, which Tim was tasked to investigate. Marcin explained that they had released version 0.1 with bug fixes but it introduced worse bugs, so they reverted to version 0.2. They plan to release a new version after the mainnet fork with known optimizations and fixes, prioritizing stability over rare bug fixes. The team also mentioned a broken Snap sync due to regression in downloading block receipts and a consensus bug.

The team discussed several issues related to the mainnet release and devnets. Parithosh mentioned that MergeN changes affecting block-level access lists were released before the fork. Mario suggested reaching out to Reth to confirm if they plan another release. Enrico noted that nodes are detecting some curious RPC calls on mainnet, which Mario asked to investigate further. Barnabas reported a halt in Nimbus SuperNodes and mentioned ongoing maintenance on devnet3 to address disk space issues. The team agreed to follow up with the Nimbus team about the halt issue and to consider shutting down devnet3 once mainnet is ready.

The team discussed network blob management, with Barnabas explaining that 20 blobs per block over a 10-day period should result in approximately 640GB, though nodes were running out of disk space. Jen from Reth reported that they had released v1.9.1 on Friday to address an EVM regression bug, which was necessary for the Fusaka release. The team noted that while Prism had a mainnet strategy release, there was no update on a stable release this week.

The team discussed the status of the Prism release, with Preston working on preparing a release after weekend soak testing. They also reviewed progress on benchmark testing for the 60 million gas mainnet, where Marcin reported that initial testing with Nethermind and Geth using EIP7904 was successful, and the next step involves generating new payloads to match the updated consensus rules.

The team discussed benchmark testing and gas pricing, with Ameziane explaining that EIP-7904 might show a decrease in mgas/s due to increased transactions per gas limit, suggesting the need to include TPS metrics in the dashboard. Maria confirmed that while there were two gas repricing breakouts previously, no further breakouts are scheduled immediately due to DevConnect, though recordings of the overview sessions are available. Mario inquired about the next gas repricing call, and Francesco suggested holding another session on Wednesday to move beyond the overview stage for some EIPs.

The team discussed the status of block-level access list tests and their planned launch in DevNet. Spencer explained that recent changes in the test releases, including the addition of EVM fuzzing scenarios, have caused widespread failures across clients. The team is working on fixing these issues, with Felipe expected to address the problems either tomorrow or Wednesday. They also discussed the need for clients to better print debugging information related to block-level access list hashes.

The team discussed block-level access lists, with Mario noting that clients agreed to include both expected and generated bad blocks in the access list. They decided not to launch DevNets until Hive test failures are reduced to a manageable level. Justin provided an update on ePBS, mentioning that an off-protocol value field will be added to the Execution payload and previous RANDAO will be included in the bid. The next ePBS breakout call is scheduled for December 5th, with DevNet Zero likely to happen in mid-January.

The team discussed whether to cancel upcoming calls, with general agreement to cancel the November 24th meeting due to travel schedules and team members being offline. They also addressed concerns about bugs in the upcoming mainnet release, with Parithosh noting that while some issues were regression-related, most staking entities have redundant setups and backup systems in place to handle potential failures.

The team discussed the stability of the test network, with Barnabas noting it was smoother than previous merges and forks. Mario asked about concerns from other clients, and Ben mentioned they had released a fix for an issue 12 hours after the initial release. Parithosh inquired about testing priorities, and Saulius suggested conducting nonfinality testing on a larger network before the mainnet hard fork. The team agreed to plan this testing for after DevConnect.

The team discussed performance and reliability concerns related to blob handling in the post-peer DAS system. Parithosh confirmed that Sam is investigating potential issues, though it’s challenging to identify bugs due to the testnet infrastructure reuse. The group addressed questions about private blobs and reorg-heavy situations, with Barnabas noting no issues were observed with private blobs but reorg communications might cause problems for specific ER clients. Kasey raised concerns about the strain on nodes during reorgs, particularly when exercising blockQ code paths, and suggested testing these scenarios in testnets. Parithosh also mentioned a recently fixed bug in the MEV boost relay configuration that addressed a race condition.

The team discussed nonfinality testing on devnetri, agreeing to wait for the resolution of the Nimbus bug before proceeding. They decided to cancel the calls scheduled for the 17th and 24th, with ACDT resuming on December 1st. Casey reported that the Prism release, expected by Preston, would not be completed that day.

### Next Steps:

- Mario: Follow up with Reth team about planning another release for the mainnet bug
- Enrico: Write a message on Telegram or Discord about the columns by route request via RPC on mainnet and start a thread
- Barnabas: Continue following up with Nimbus team about the halt issue on Fusaka 3
- Barnabas: Continue reaching out to Prism team about stable release
- Marcin : Generate new payloads to match consensus rules after EIP7904 for benchmark testing
- Maria: Share recordings of gas repricing breakout calls
- Spencer: Release patch for 7702-related issue in block access list tests
- Spencer: Fix BPO-related configs in Hive for block access list tests
- All clients: Implement debug logging to print full block-level access list when hash doesn’t match expectations
- All clients: Review and fix Hive test failures for block-level access lists
- Justin: Include changes  in next ePBS spec release within 1-2 weeks
- parithosh: Plan LMD/nonfinality testing round after DevConnect
- parithosh: Share Sunnyside Labs dashboards for blob performance metrics
- Barnabas: Trigger nonfinality test on devnet3 after Nimbus bug is fixed
- Preston : Release stable Prism version today

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =Hl5f.5Z)
- Download Chat (Passcode: =Hl5f.5Z)
- Download Audio (Passcode: =Hl5f.5Z)

---

**system** (2025-11-10):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=uU4Vq7yeiGc

