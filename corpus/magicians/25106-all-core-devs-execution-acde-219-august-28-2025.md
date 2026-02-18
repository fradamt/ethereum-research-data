---
source: magicians
topic_id: 25106
title: All Core Devs - Execution (ACDE) #219, August 28, 2025
author: system
date: "2025-08-14"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-219-august-28-2025/25106
views: 160
likes: 2
posts_count: 7
---

# All Core Devs - Execution (ACDE) #219, August 28, 2025

### Agenda

- Fusaka

Devnet updates

Non-finality testnets
- Pending PRs

feat: update osaka style blob schedule by barnabasbusa · Pull Request #129 · eth-clients/holesky · GitHub
- feat: update osaka style blob schedule by barnabasbusa · Pull Request #110 · eth-clients/sepolia · GitHub
- feat: update osaka style blob schedule by barnabasbusa · Pull Request #19 · eth-clients/hoodi · GitHub
- feat: update osaka style blob schedule by barnabasbusa · Pull Request #10 · eth-clients/mainnet · GitHub

Next steps / timeline

Holesky shut down
Gas Limit updates
Glamsterdam

- Block Access List Updates
- Repricings Meta EIP
- PFI proposals reviews

Besu Preferences
- Author-proposed EIPs:

EIP-2926
- EIP-7793
- EIP-7843
- EIP-8012
- EIP-8014

**Meeting Time:** Thursday, August 28, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1687)

## Replies

**abcoathup** (2025-08-14):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #219, August 28, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-219-august-28-2025/25106/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE TL;DW
> Fusaka
>
> devnet-3 expected to finalize today, CL teams working on fixes for sync issues
> Next week, once CL fixes are out, we’ll do another non-finality test. If things go well, we’ll launch devnet-5. Optimistic ETA EONW.
> Barnabas will merge the following PRs if no objections in the next day:
> feat: update osaka style blob schedule eth-clients/holesky#129
> feat: update osaka style blob schedule eth-clients/sepolia#110
> feat: update osaka style blob schedule eth-clients/hoodi#19
> feat: upd…

### Recordings/Stream

- YouTube
- Live stream on X: [x.com/ECHInstitute]
- Podcast (audio only)

### Writeups

- Tweet thread by @poojaranjan
- ACDE #219: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]
- Highlights from the All Core Developers Execution (ACDE) Call #219 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]
- Upgrade process

Gas limit increase [blockers for 60M](https://github.com/NethermindEth/eth-perf-research/blob/main/README.md#60-mgas)
[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners:

EIP2926 chunk-based code Merkleization presentation

---

**timbeiko** (2025-08-28):

**ACDE TL;DW**

**Fusaka**

- devnet-3 expected to finalize today, CL teams working on fixes for sync issues
- Next week, once CL fixes are out, we’ll do another non-finality test. If things go well, we’ll launch devnet-5. Optimistic ETA EONW.
- Barnabas will merge the following PRs if no objections in the next day:
- feat: update osaka style blob schedule eth-clients/holesky#129
- feat: update osaka style blob schedule eth-clients/sepolia#110
- feat: update osaka style blob schedule eth-clients/hoodi#19
- feat: update osaka style blob schedule eth-clients/mainnet#10
- For the fork rollout, we’ll propose both a timeline that matches the process doc we went with post-Pectra and reach out to the major stakeholders affected by the rollout to gauge their preferences

**Holesky**: agreed to shut it down a few weeks after Fusaka activates on it. Blog post coming next week to formally announce this.

**Gas Limit:** teams are working on addressing bottlenecks, hoping to get to 60M before Fusaka. Here is the list of blockers: https://github.com/NethermindEth/eth-perf-research/blob/main/README.md#60-mgas, Nethermind and PandaOps are working on better docs for the various dashboards and benchmarking test suites.

**Glamsterdam PFI discussions:** we’ll prioritize EIPs that client teams want to see discussed on the call. [Besu shared some today](https://github.com/ethereum/pm/issues/1687#issuecomment-3233422166) which I’ll try and line up for the next call.

We also discussed a handful of EIPs that people had put on the agenda. The goal isn’t to make decisions about inclusion, but to share context and answer questions raised by client teams.

---

## LLM Summary

### Action Items

1. Fusaka

- Devnet-3: aim to finalize today; CL teams (e.g., Lighthouse, Prysm, Teku, Nimbus) continue syncing fixes.
- Non-finality testing: once the CL fixes are out next week, we’ll run another non-finality test; if recovery looks good, we’ll bring up Devnet-5 (fix-only scope).
- Blob-schedule PRs (merge after ~24h if no objections):

Holesky: feat: update osaka style blob schedule by barnabasbusa · Pull Request #129 · eth-clients/holesky · GitHub
- Sepolia: feat: update osaka style blob schedule by barnabasbusa · Pull Request #110 · eth-clients/sepolia · GitHub
- Hoodi: feat: update osaka style blob schedule by barnabasbusa · Pull Request #19 · eth-clients/hoodi · GitHub
- Mainnet: feat: update osaka style blob schedule by barnabasbusa · Pull Request #10 · eth-clients/mainnet · GitHub

Fork-rollout planning (two-track approach):

- Prepare a “default” schedule that follows the post-Pectra process doc for testnets (ordering, spacing, and comms milestones).
- In parallel, proactively poll major stakeholders (L2s, infra/app providers, staking operators) on preferred activation sequencing and lead-time. Items to clarify: (i) which testnet should carry the “app-staging” role and remain last; (ii) how much time to reserve between devnet validation and each testnet; (iii) change-freeze/holiday windows; (iv) gating criteria (e.g., non-finality recovery, sync health) before scheduling each step.

1. Holesky

- Agreement to retire Holesky a few weeks after Fusaka activates there. A blog post with timelines/migration notes is planned for next week.

1. Gas limit (toward 60M)

- Teams continue removing bottlenecks with a shared measurement plan; goal is to raise to 60M (ideally before Fusaka).
- Tracking list: https://github.com/NethermindEth/eth-perf-research/blob/main/README.md#60-mgas
- Nethermind and PandaOps will publish clearer docs for dashboards and benchmarking suites; client teams are encouraged to add measurements.

1. Glamsterdam (PFI pipeline)

- We’ll prioritize EIPs that client teams request for the call. Besu shared the first batch; aim to review those next time:
All Core Devs - Execution (ACDE) #219, August 28, 2025 · Issue #1687 · ethereum/pm · GitHub
- Repricings Meta EIP (discussion; no decisions): https://github.com/ethereum/EIPs/pull/10206

Purpose: group repricing work (opcodes/precompiles) under a single framing, define shared rationale and measurement methodology, and avoid one-off repricings without coordinated evidence.
- Client feedback requested: worst-case justifications, reference implementations or test vectors, and rollout cadence aligned with 60M-gas goals and devnet capacity.
- Today’s outcome: keep iterating in the PR; bring concrete perf data and test plans back to ACDE.

PFI EIPs reviewed (context-setting only): EIP-2926, EIP-7793, EIP-7843, EIP-8012, EIP-8014.

---

### Summary

#### Fusaka

Devnet-3 is targeted to finalize today while CL teams finish sync fixes. After those land next week, we’ll rerun non-finality; if recovery looks solid, we’ll spin up Devnet-5 (fix-only, to validate stability before talking dates). Blob-schedule alignment moves forward via the Osaka-style PR set (Holesky/Sepolia/Hoodi/Mainnet), which will be merged after ~24h if there’s no pushback. For the rollout, we’ll produce a default timeline that mirrors the process doc, and, in parallel, survey major stakeholders on preferred testnet order, lead-time, and change-freeze windows—so we can reconcile “process-clean” vs. “operationally-ideal” plans before scheduling.

#### Holesky

Consensus to deprecate Holesky a few weeks after Fusaka activates there; a public post will outline timing and migration guidance.

#### Gas limit

Work continues toward a 60M target. Teams will document deltas using shared dashboards/suites; Nethermind and PandaOps will improve the public docs so client teams can contribute comparable perf data.

#### Glamsterdam

PFI time on future calls goes first to client-requested items. The Repricings Meta EIP is the proposed umbrella for cost-model updates (opcodes/precompiles), with alignment on evidence, test vectors, and rollout planning. Author-queued PFIs (EIP-2926/7793/7843/8012/8014) were reviewed for context; no inclusion decisions today.

---

**system** (2025-08-28):

### Meeting Summary:

The team prepared for a YouTube presentation stream and discussed the status of non-finality testing on Devnet 3, with plans to finalize it by the end of the day. They reviewed an updated timeline for Fusaka and discussed the upcoming Ethereum fork, including the 30-day agreement with L2s for testnet releases and potential timeline adjustments. The team also covered various technical implementations and EIP proposals, including gas limit changes, block access lists, and code chunking in the MPT, while emphasizing the importance of maintaining discipline in the release process and ensuring proper stakeholder communication.

**Click to expand detailed summary**

The team held a brief meeting to prepare for streaming a presentation on YouTube. Tim and Akash coordinated to ensure the live stream was set up properly, with Akash confirming readiness to go live. The conversation ended with Tim giving the final okay to start the stream.

The team discussed the status of non-finality testing on Devnet 3, where Barnabas reported 50-55% participation and syncing issues across multiple clients. They agreed to aim for finalizing Devnet 3 by the end of the day, with fixes from client teams expected by mid-next week. The team also reviewed an updated timeline for Fusaka, with Alex presenting a schedule that includes trunk branches by the end of the week, Devnet 5 launch next week, and mainnet releases planned for early October. There was some discussion about maintaining a 30-day period between client releases and testnet forks, as previously agreed in the protocol upgrade process.

The team discussed the timeline for the upcoming Ethereum fork, focusing on the 30-day agreement with L2s for testnet releases and the importance of adhering to this commitment. They debated whether the 30-day timeline was necessary, with some arguing for a more compressed rollout to meet the end-of-year target, while others emphasized the need for a predictable and secure upgrade process for L2s. The group also touched on the potential impact of delays on the broader Ethereum ecosystem and the need for better communication and planning in the future.

The team discussed the timeline for the testnet release and the process of integrating changes into trunk branches. Tim proposed two paths forward: basing the ready schedule on the current process or adjusting it to accommodate community preferences for an earlier release. The group debated the urgency of the January 1st versus January 15th release dates, with some stakeholders expressing a preference for more time to integrate changes. Stokes agreed to reach out to rollups and other affected parties to gather feedback on the proposed timeline changes. Lightclient emphasized the importance of maintaining discipline in the release process and avoiding frequent changes to agreed-upon deadlines.

The team discussed timeline preferences for software releases, with a current agreement of 30 days in the documentation that will be maintained unless stakeholders indicate otherwise. They agreed to check with affected stakeholders about their timeline preferences while preparing the schedule according to the existing document. The team also confirmed plans to deprecate Polesky after the fork, with an announcement expected in the coming weeks, and Luis reported progress on gas limit work for Besu, which now has a working implementation for MoD and Dev that will be tested soon.

The team discussed the process for implementing a 60 million gas limit change, agreeing to wait until all major clients have releases that can handle it, rather than forcing an immediate update. Tim suggested making the 60 million gas limit the default in testnet releases before Fushaka’s mainnet launch, while Ansgar emphasized the importance of quick upgrade capability for any potential issues. The team also addressed concerns about Zen’s compatibility and discussed the possibility of CLs querying ELs for gas limit information, though Felix noted this could be implemented through existing RPC APIs without requiring an engine API change.

The team discussed updates on block access lists and gas price repricing EIPs. Toni reported that client teams are busy implementing EIP-7732, with progress being made toward a first step. Ansgar and Maria proposed creating a meta EIP to track gas price repricing EIPs, which would serve as a version-controlled document for early devnets. The team agreed to give this approach a try, with Ansgar and Maria taking the lead on research in this area. Roman inquired about the status of gas limit testing efforts, which Tim and the team discussed briefly.

The team discussed managing a large number of proposed EIPs for an upcoming fork, with concerns about reviewing 20-30 EIPs in a timely manner. They agreed to have teams pre-review the list and flag the most important ones for discussion, with a focus on async communication through Magicians threads and potentially using a tier ranking feature in Forkcast. Tim proposed following up with teams to gather more EIP preferences before the next ACDE meeting, where some presentations would be scheduled.

Guillaume presented EIP-2129/26, which introduces code chunking in the MPT to enable larger contracts without waiting for binary trees implementation. He explained that the change requires a simple transition and adds two extra fields to contract accounts: code size and code root, while maintaining compatibility with existing EOA accounts. Tim and others discussed potential benefits and downsides, including performance improvements for zk proofs and increased gas costs. Marc then presented two additional EIPs: EIP-7843, which introduces a new feature for the “EIP” (EIP) system, and EIP-7843, which adds a slot number opcode to facilitate future slot length changes.

The meeting focused on discussions about conditional transactions and their implementation complexity, with Marius expressing concerns about the amount of work they would add to the mempool. Tim and Marc agreed to further discuss these issues with Marius. Potuz presented two EIPs aimed at separating execution from consensus, proposing to reuse the existing consolidations contract to pass arbitrary data to the consensus layer. Felix supported the idea of making the mechanism more generic, but noted that the current system contracts are not extensible and would need to be replaced if more data storage is required. The group agreed to continue discussions on these proposals.

### Next Steps:

- PenOps team: Help Devnet 3 reach finalization by end of tomorrow.
- Client teams: Review and approve the blob schedule PRs by end of day tomorrow.
- Barnabas: Merge the blob schedule PRs after 24 hours if no complaints are received.
- All client teams: Continue working on fixes for syncing issues on Devnet 3 by mid-next week.
- Lighthouse team: Provide fix for non-finality issue by mid next week.
- PenOps team: Trigger another non-finality test next week after fixes are implemented.
- All teams: Test syncing fixes once available next week.
- PenOps team: Schedule Devnet 5 launch for end of next week if Devnet 3 issues are resolved.
- All teams: Prepare for Devnet 5 launch after client fixes are deployed and tested.
- Barnabas: Continue monitoring Devnet 3 recovery and participation rates.
- All teams: Discuss slow sync theories in Monday’s testing call.
- Alex: Update the Fusaka timeline based on the current state of devnets.
- Alex: Create an updated Fusaka timeline following the process document requirements.
- Alex: Reach out to rollups and other stakeholders to confirm their preferences regarding the timeline between releases and testnet forks.
- Client teams: Prepare for shadow forks on Holesky, Sepolia, Goerli, and Mainnet.
- Tim: Prepare an announcement in the next week about Polesky deprecation after Fusaka goes live.
- Besu team: Test their improved implementation for Mod and Division opcodes in the next few days.
- Client teams: Continue working on performance improvements to support 60 million gas limit before Fusaka.
- Client teams: Consider including 60 million gas limit as default in testnet releases when ready.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: wiGn6z?*)
- Download Chat (Passcode: wiGn6z?*)

---

**system** (2025-08-28):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=S4p0Ha_M_oE

---

**system** (2025-08-29):

### Meeting Summary:

The team prepared for a YouTube presentation stream and discussed the status of non-finality testing on Devnet 3, with plans to finalize it by the end of the day. They reviewed an updated timeline for Fusaka and discussed the upcoming Ethereum fork, including the 30-day agreement with L2s for testnet releases and potential timeline adjustments. The team also covered various technical implementations and EIP proposals, including gas limit changes, block access lists, and code chunking in the MPT, while emphasizing the importance of maintaining discipline in the release process and ensuring proper stakeholder communication.

**Click to expand detailed summary**

The team held a brief meeting to prepare for streaming a presentation on YouTube. Tim and Akash coordinated to ensure the live stream was set up properly, with Akash confirming readiness to go live. The conversation ended with Tim giving the final okay to start the stream.

The team discussed the status of non-finality testing on Devnet 3, where Barnabas reported 50-55% participation and syncing issues across multiple clients. They agreed to aim for finalizing Devnet 3 by the end of the day, with fixes from client teams expected by mid-next week. The team also reviewed an updated timeline for Fusaka, with Alex presenting a schedule that includes trunk branches by the end of the week, Devnet 5 launch next week, and mainnet releases planned for early October. There was some discussion about maintaining a 30-day period between client releases and testnet forks, as previously agreed in the protocol upgrade process.

The team discussed the timeline for the upcoming Ethereum fork, focusing on the 30-day agreement with L2s for testnet releases and the importance of adhering to this commitment. They debated whether the 30-day timeline was necessary, with some arguing for a more compressed rollout to meet the end-of-year target, while others emphasized the need for a predictable and secure upgrade process for L2s. The group also touched on the potential impact of delays on the broader Ethereum ecosystem and the need for better communication and planning in the future.

The team discussed the timeline for the testnet release and the process of integrating changes into trunk branches. Tim proposed two paths forward: basing the ready schedule on the current process or adjusting it to accommodate community preferences for an earlier release. The group debated the urgency of the January 1st versus January 15th release dates, with some stakeholders expressing a preference for more time to integrate changes. Stokes agreed to reach out to rollups and other affected parties to gather feedback on the proposed timeline changes. Lightclient emphasized the importance of maintaining discipline in the release process and avoiding frequent changes to agreed-upon deadlines.

The team discussed timeline preferences for software releases, with a current agreement of 30 days in the documentation that will be maintained unless stakeholders indicate otherwise. They agreed to check with affected stakeholders about their timeline preferences while preparing the schedule according to the existing document. The team also confirmed plans to deprecate Polesky after the fork, with an announcement expected in the coming weeks, and Luis reported progress on gas limit work for Besu, which now has a working implementation for MoD and Dev that will be tested soon.

The team discussed the process for implementing a 60 million gas limit change, agreeing to wait until all major clients have releases that can handle it, rather than forcing an immediate update. Tim suggested making the 60 million gas limit the default in testnet releases before Fushaka’s mainnet launch, while Ansgar emphasized the importance of quick upgrade capability for any potential issues. The team also addressed concerns about Zen’s compatibility and discussed the possibility of CLs querying ELs for gas limit information, though Felix noted this could be implemented through existing RPC APIs without requiring an engine API change.

The team discussed updates on block access lists and gas price repricing EIPs. Toni reported that client teams are busy implementing EIP-7732, with progress being made toward a first step. Ansgar and Maria proposed creating a meta EIP to track gas price repricing EIPs, which would serve as a version-controlled document for early devnets. The team agreed to give this approach a try, with Ansgar and Maria taking the lead on research in this area. Roman inquired about the status of gas limit testing efforts, which Tim and the team discussed briefly.

The team discussed managing a large number of proposed EIPs for an upcoming fork, with concerns about reviewing 20-30 EIPs in a timely manner. They agreed to have teams pre-review the list and flag the most important ones for discussion, with a focus on async communication through Magicians threads and potentially using a tier ranking feature in Forkcast. Tim proposed following up with teams to gather more EIP preferences before the next ACDE meeting, where some presentations would be scheduled.

Guillaume presented EIP-2129/26, which introduces code chunking in the MPT to enable larger contracts without waiting for binary trees implementation. He explained that the change requires a simple transition and adds two extra fields to contract accounts: code size and code root, while maintaining compatibility with existing EOA accounts. Tim and others discussed potential benefits and downsides, including performance improvements for zk proofs and increased gas costs. Marc then presented two additional EIPs: EIP-7843, which introduces a new feature for the “EIP” (EIP) system, and EIP-7843, which adds a slot number opcode to facilitate future slot length changes.

The meeting focused on discussions about conditional transactions and their implementation complexity, with Marius expressing concerns about the amount of work they would add to the mempool. Tim and Marc agreed to further discuss these issues with Marius. Potuz presented two EIPs aimed at separating execution from consensus, proposing to reuse the existing consolidations contract to pass arbitrary data to the consensus layer. Felix supported the idea of making the mechanism more generic, but noted that the current system contracts are not extensible and would need to be replaced if more data storage is required. The group agreed to continue discussions on these proposals.

### Next Steps:

- PenOps team: Help Devnet 3 reach finalization by end of tomorrow.
- Client teams: Review and approve the blob schedule PRs by end of day tomorrow.
- Barnabas: Merge the blob schedule PRs after 24 hours if no complaints are received.
- All client teams: Continue working on fixes for syncing issues on Devnet 3 by mid-next week.
- Lighthouse team: Provide fix for non-finality issue by mid next week.
- PenOps team: Trigger another non-finality test next week after fixes are implemented.
- All teams: Test syncing fixes once available next week.
- PenOps team: Schedule Devnet 5 launch for end of next week if Devnet 3 issues are resolved.
- All teams: Prepare for Devnet 5 launch after client fixes are deployed and tested.
- Barnabas: Continue monitoring Devnet 3 recovery and participation rates.
- All teams: Discuss slow sync theories in Monday’s testing call.
- Alex: Update the Fusaka timeline based on the current state of devnets.
- Alex: Create an updated Fusaka timeline following the process document requirements.
- Alex: Reach out to rollups and other stakeholders to confirm their preferences regarding the timeline between releases and testnet forks.
- Client teams: Prepare for shadow forks on Holesky, Sepolia, Goerli, and Mainnet.
- Tim: Prepare an announcement in the next week about Polesky deprecation after Fusaka goes live.
- Besu team: Test their improved implementation for Mod and Division opcodes in the next few days.
- Client teams: Continue working on performance improvements to support 60 million gas limit before Fusaka.
- Client teams: Consider including 60 million gas limit as default in testnet releases when ready.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: wiGn6z?*)
- Download Chat (Passcode: wiGn6z?*)

---

**system** (2025-08-29):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=S4p0Ha_M_oE

