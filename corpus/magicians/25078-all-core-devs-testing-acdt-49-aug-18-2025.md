---
source: magicians
topic_id: 25078
title: All Core Devs - Testing (ACDT) #49 | Aug 18 2025
author: system
date: "2025-08-12"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-49-aug-18-2025/25078
views: 157
likes: 4
posts_count: 5
---

# All Core Devs - Testing (ACDT) #49 | Aug 18 2025

### Agenda

- Fusaka devnet status updates
- BPO Static Tests Updates
- Gas limit testing updates

60M gas pre-Fusaka

Sunnyside labs testnet updates
Safe-head discussion: [All Core Devs - Testing (ACDT) #45 | July 21 2025 · Issue #1624 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1624#issuecomment-3088955383)

**Meeting Time:** Monday, August 18, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1680)

## Replies

**abcoathup** (2025-08-13):

### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png)

      [All Core Devs - Testing (ACDT) #49 | Aug 18 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-49-aug-18-2025/25078/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACD Testing Call #49 - Aug 18, 2025 (Quick Notes)
> Facilitator: Mario Vega
> Fusaka devnet status updates
> Mario
>
> Devnet 4 is currently down.
>
> Barnabus
>
> Devnet 3 remains online and will continue running for now.
> Devnet 5 is targeted for launch next Tuesday, expected to be with no further spec clarifications needed. It will be pretty big.
>
> Conclusion: Progress looks strong. The only pending step for clients is merging into the main branch—no other concerns have been reported.
> BPO Static Tests Upd…

### Recordings/Stream

- YouTube
- X Livestream [x.com/echinstitute]

### Writeups

- Quick recap by @poojaranjan
- ACDT#49: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**poojaranjan** (2025-08-18):

# ACD Testing Call #49 - Aug 18, 2025 (Quick Notes)

Facilitator: Mario Vega

## Fusaka devnet status updates

Mario

- Devnet 4 is currently down.

Barnabus

- Devnet 3 remains online and will continue running for now.
- Devnet 5 is targeted for launch next Tuesday, expected to be with no further spec clarifications needed. It will be pretty big.

**Conclusion**: Progress looks strong. The only pending step for clients is merging into the main branch—no other concerns have been reported.

## BPO Static Tests Updates

Mario:

- New release is ready.
- Testing includes Devnet 4 scenarios.
- Tests will be run against all clients to verify the BPO issue.
- Hive updates will follow as soon as possible.

## Gas Limit Testing Updates

### 60M Gas Pre-Fusaka

- Discussion raised by Ben regarding moving to 60M gas limit.
- Besu concerns:

Justin (Besu) expressed hesitancy about the move.
- Current blockers include ecrecover performance, which remains a concern post-fork.

Kamil’s updates:

- Geth work-in-progress with integrated EEST and benchmark tests.
- In contact with the Besu team; new scenarios now available.
- Working on stateful testing and deeper issue analysis.
- Observed that EC performance is slow on Besu, while other clients perform well.

Tim Beiko (chat) asked if unchanged ecrecover pricing in Fusaka is still a blocker → Justin (Besu): Yes. Known issue: multiple opcodes at 45–60M gas range cause performance bottlenecks.

Action Items:

- Kamil to document all areas under investigation and to share resources with Besu team.

References:

- Besu Benchmarking approach
- Grafana benchmarking results

### Other Updates

- No additional concerns raised by other client teams.
- Marius: Called for more benchmarking, especially regarding state.
- Marius (chat): All clients failed snap sync on perf/devnet4.
- Barnabas (chat): Shared failed test run – link.
- Mario: New EEST tests being added to catch potential bugs.
- Kamil: ecrecover performing well at 60M gas for all clients except Besu.
- Encouraged all clients to align on EEST benchmarking instead of developing separate tools.
- Ben: Reported Nethermind has no issues with 60M gas.
- Louis (chat): Shared EEST benchmark reference for ecrecover.

## – Ready for Merge

- Barnabus brought up in the call
- CL devs are requested to review.
- If no objections, we should move forward with merging.
- Alex Stokes: “Seems fine to me.”
- Pawan (chat): “Looks good to me.”

Others: Please review, comment, and approve the PR.

## Sunnyside Labs Testnet Updates

- Minhyuk: No major updates this week, aside from the report shared last week.

## Safe-Head Discussion

- All Core Devs - Testing (ACDT) #45 | July 21, 2025 #1624 (comment)
•	Mikhail raised the topic last week and added it for follow-up this week.
•	No additional thoughts or discussion today.

**Conclusion** (Gas Benchmarkin): Review benchmark results and continue discussion in next week’s ACDT.

PS: This is quick note following the livestream. If you have any corrections/improvement suggestions, please add [here](https://hackmd.io/@poojaranjan/InteropTestingNotes2#ACD-Testing-Call-49---Aug-18-2025).

---

**system** (2025-08-21):

### Meeting Summary:

The team reviewed the status of DevNet environments and discussed plans for upcoming releases, including new image rollouts and testing schedules. Performance and benchmarking concerns were extensively discussed across different Ethereum clients, with particular focus on gas limits, sync times, and client-specific issues that need addressing. The team agreed to share benchmarking results, investigate performance optimizations, and follow a standardized approach for future testing scenarios to ensure compatibility across clients.

**Click to expand detailed summary**

The team discussed the status of DevNet 4 and plans for DevNet 5, with Barnabas reporting that DevNet 3 remains online and that they are rolling out new images for client teams to merge into their master branches. The team plans to launch DevNet 5 next week Tuesday, aiming for a 2-3 week testing period. Mario provided an update on VPO site tests, noting that a new release of EAT has been tagged and is currently building, with plans to run tests against all clients to verify fixes for the BPO issue that occurred in DevNet 4.

The team discussed gas limit testing updates, particularly regarding the proposed increase to 60 million gas. Ben raised the question of going to 60 million gas, and Justin from the Besu team expressed concerns about performance issues between 45 and 60 million gas. Kamil mentioned ongoing work on improving worst-case scenarios and integrating ESD tests and benchmark tests, which revealed some slow scenarios for Besu. The team agreed to share results and conduct further analysis to address performance issues, with Kamil planning to share data on the Besu team’s Discord channel.

The team discussed benchmarking challenges across different Ethereum clients, with a focus on snap sync failures and gas performance issues. Marius reported that Def Net 2 outline failed to snap sync within 70 hours, highlighting a need for clients to investigate their specific implementations. The group explored the current state of benchmark testing, where Mario explained they are working to unify tests into execution spec tests, though stateful tests in EEST remain challenging. Kamil noted that ecrecover benchmarks showed consistent performance of 60 megagas per second across clients, while Justin emphasized concerns about MOD exp precompile opcodes that are below 20 million gas, suggesting these should be addressed before considering gas limit increases.

The team discussed benchmarking results and performance concerns across different Ethereum clients. Kamil highlighted that Besu’s worst-case scenario of 19 megagases per second needs improvement, with a target to keep worst-case performance under 3-4 seconds. The team agreed to follow the firstst approach for new benchmarking scenarios to ensure compatibility across clients. Barnabas raised a PR regarding block number limitations in the minimal preset, which the team approved to include in full releases. Minhyuk from Sunnyside Labs shared a report on devnet updates. The team also discussed concerns about safe head behavior on Ethereum clients, which Justin and others will investigate further. Finally, Marius noted that Klaytn and Aragon were performing at 30-33 million gas for point evaluation precompile, which the team will review for potential optimization opportunities.

### Next Steps:

- Client teams to merge their changes into main branches before next week’s Devnet 5 launch
- Kamil to share Besu benchmark test results with the team on Discord
- Kamil to share specific EC recover tests with the team for implementation in East
- Client teams to review and comment on Barnabas’s PR regarding bloated numbers testing
- Kamil to investigate point evaluation precompile performance issues with Keith and Aragon clients
- Client teams to analyze and address snap sync failures within 70h window
- East team to unify stateful tests in the benchmarking framework
- Client teams to consider using East benchmarking approach for new scenarios and tools
- Client teams to review and optimize performance for 9 opcodes and Modex precompile below 20 million gas
- Client teams to investigate and address performance issues for 60 million gas limit scenarios

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: *Zrg%L2B)
- Download Chat (Passcode: *Zrg%L2B)

---

**system** (2025-08-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=KuAtOO46Bxs

