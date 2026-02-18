---
source: magicians
topic_id: 26001
title: All Core Devs - Testing (ACDT) #60, November 3, 2025
author: system
date: "2025-10-28"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-60-november-3-2025/26001
views: 78
likes: 0
posts_count: 4
---

# All Core Devs - Testing (ACDT) #60, November 3, 2025

### Agenda

**Fusaka**:

- Sepolia BPO fork events/updates
- Devnet status updates
- Hoodi Activation updates
- Hoodi BPO

**60M gas limit on mainnet updates**:

- State test updates
- Gas limit testing update

**Glamsterdam Testing Updates**:

- BALer updates - bal-devnet-0
- ePBS updates

**Other Topics**:

- Mainnet client releases - check client readiness
- Verify 60M gas being set by all mainnet client releases
- Testing Complexity Assessment checklist

**Meeting Time:** Monday, November 03, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1786)

## Replies

**poojaranjan** (2025-11-03):

# All Core Devs - Testing (ACDT) #60 (Quick notes)

**Next Steps:**

- Client teams to complete release candidates by Nov 5 .
- Testing complexity assessment to start on prioritized EIPs for Glamsterdam.
- Mainnet upgrade target remains Dec 3, 2025.

BarnabasBusa facilitated the call.

## Fusaka:

### Sepolia BPO fork events/updates

- Last week’s BPO 2 went smoothly overall, except for an issue involving Prysm.

Manu (Prysm)

- Summary TL;DR

Starting from Hoodi/Fusaka, a few attester nodes are struggling — producing attestations where target.epoch - source.epoch is inconsistent.
- These problematic nodes may or may not be Prysm.
- When a Prysm node receives such an attestation, it can reject it, downscore the peer, and eventually disconnect the gossiping node.

The Prysm team has identified this as an attestation node issue and is working on a fix, expected later this week.

#### Other Client Reports – Hoodi

nflaig (Lodestar):

- Currently working on the Lodestar zero proofs bug.

Tbenr / Enrico (Teku):

- Discovered some bad blob sidecars circulating in the network with incorrect KZG commitments.
- The mainnet release addressing this is in progress and expected to be out shortly.

Manu (Prysm):

- Also observed Lodestar peers passing invalid KZG proofs.
- In such cases, Prysm will not verify these proofs since validation depends on the Execution Layer (EL).

Tbenr (Teku):

- Confirmed that Teku behaves similarly to Prysm in this regard — if the issue originates from the EL, it could involve the Engine API.

nflaig (Lodestar):

- The bug fix is underway.
- Believes the “zero proof” issue stems from an internal buffer problem.
- Noted that major refactoring done a month ago might explain why it wasn’t detected earlier.

Manu (Prysm):

- Added that sometimes the problem may come from other clients, not necessarily Lodestar.
- Doesn’t appear to be critical, but worth noting since sidecar handling can occasionally trigger this issue.

#### Hoodi BPO is expected this week

## 60M gas limit on mainnet updates:

### State Test Updates

Kamil Chodola:

- Focused on stabilizing the data and testing environment — conditions are now more consistent and results are steady.
- The feedback loop has improved, enabling faster iteration.
- Currently adding a new EEST compute scenario; facing some issues generating genesis files and collaborating with Louis to resolve them.
- Working with Mario on sum repricing, aiming to identify potential repricing candidates for the Glamsterdam upgrade.

From the stateful testing perspective:

- The machine running other stateful tests needs a refresh — it’s currently down due to technical issues.
- Overall progress is solid, but metrics collection for repricing scenarios needs improvement going forward.

### Gas limit testing update

Pari:

- Noted that starting this week, the 60M gas limit is set as default.
- As the network progresses, gas limit increases should start to appear in testing results.

## Glamsterdam Testing Updates:

### BALer updates - bal-devnet-0

Stefan:

- The devnet is ready.
- Reth and Nethermind have signaled readiness; awaiting confirmation from Geth and Besu before launch.

Raxhvl:

- Shared latest BAL test results (v1.3.0):
- Overall: 98%
- Besu – 100%
- Reth – 100%
- Geth – 99%
- Nethermind – 91%
- A new release is coming soon, adding ~25 tests to cover coinbase changes.
- Results will be updated following the new release.

Stefan: Once all clients confirm readiness, the BALer devnet will go live.

Toni:

-Announced that the EIP-7928 breakout will take place on Wednesday at 14:00 UTC.

### ePBS Updates

Mario Vega:

- Shared that Justin T. provided updates on recent progress.
- There have been two new spec releases, each accompanied by a comprehensive README for better clarity and implementation guidance.
- v1.6.0-beta.2
- v1.6.0

Barnabas:

- Noted that the focus will be on completing the BALer devnet first, with the ePBS devnet targeted for late November or early December.

## Other Topics:

### Mainnet Client Releases – Check Client Readiness

Nethermind (Kamil):

- Working on a new release.
- A minimized version will be released today, with a hotfix expected in the coming days.

Erigon (Andrew):

- Fusaka mainnet release is out today with the 60M gas limit enabled.

Teku (Enrico Del Fante / tbenr):

- Release in progress, expected within a few hours.
- The 60M gas limit was already set as default in a previous Teku release.

Reth (draganrakita):

- Planning to release on Wednesday.

Lodestar (Phil Ngo):

- Working on a release but currently blocked by the zero-proofs bug.
- A release is possible today if the fix lands; otherwise, it would be incomplete.

Nethermind (Kamil Chodoła):

- Asked whether there’s a deadline for client releases for coordination or blog inclusion.
- Noted that the release might slip to tomorrow (Nov 4) in a worst-case scenario.

Barnabas:

- Deadline for release candidates (RCs) is Wednesday, Nov 5.
- The EF blog post will go out by Thursday’s ACD, confirmed by Alex S.

Prysm (Manu):

- Tentative release this week; uncertain if it will meet the Nov 5 timeline.
- If the bug fix lands today, an RC build could be ready by Wednesday.

Lighthouse:

- No new updates shared.

Lodestar (Matthew):

- Identified a bug that only appears under larger network conditions.
- Currently soak-testing, and if stable, Lodestar’s release will also be ready by Nov 5.

#### Summary:

- Barnabas: Stay on track with the Dec 3 mainnet upgrade timeline.
- Aim for all Client Releases by Wednesday, Nov 5.
- If any client isn’t ready by Thursday, the mainnet timeline will be revisited.

### Testing Complexity Assessment Checklist

Mario:

- Currently gathering information for PFI Glamsterdam.
- Tracking progress.
- The team will follow the testing complexity checklist for the Execution Layer (EL).
- Invited everyone to chime in with EIPs they believe should be prioritized.
- The testing team will prioritize assessing complexity and begin implementation for key proposals.
- If there are Consensus Layer (CL) EIPs needing prioritization, those can also be assessed subsequently.

Raúl Kripalani (Chat):

- Offered support from the networking team — happy to assist with reviews, testing, and implementation.

Mario:

- Emphasized the goal is to get a sentiment check for Glamsterdam EIP priorities.
- Based on impact and community feedback, the team will plan assessment and implementation work.

Ansgar:

- Mentioned that initial decisions on prioritized EIPs and DFIs may come during this week’s ACDE call.

Wolovim:

- Announced that the Forkcast rank page is back online for client team scoping: https://forkcast.org/rank

lightclient:

- Requested more clarity on prioritization, noting there are nearly 10 gas fee EIPs.

Marius:

- Suggested it’s best to quickly identify which EIPs to kick or deprioritize first.
- Barnabas agreed with this approach.

Mario Vega:

- Added that some proposals are under-specified, and it makes sense to exclude those first.

Barnabas:

- Asked for a Nethermind-maintained list to help other teams coordinate priorities.
- Marc confirmed this will be prepared.

lightclient:

- Reiterated that repricing EIPs are a high priority.
- Requested stronger testing team signaling to guide client focus.

Ansgar Dietrichs:

- Noted that Maria shared a document outlining bundling options for repricing proposals.
- The core EIPs in that document should be treated as highest priority within the repricing group.

Fredrik:

- Mentioned the Mainnet Upgrade & Incident Response Plan, similar to the Pectra model: Fusaka Mainnet Plan
- Encouraged client teams to start identifying coordinators and backup coordinators.

#### Summary

Barnabas:

- Echoed the request for client teams to make PRs to the plan file with coordinator details.
- Expressed hope that by Wednesday/Thursday, the plan and coordination list will be complete.
If there is any correction suggestion, please drop a comment here.

---

**system** (2025-11-03):

### Meeting Summary:

The team discussed various technical issues including problems with Prism attestation nodes and incorrect KZG proofs in the network, with fixes being developed for both. Client release plans for the upcoming hard fork were reviewed, with most teams targeting November 5th while some may need additional time, and the team confirmed the December 3rd mainnet fork date. The conversation ended with discussions about testing complexity assessment and incident response planning, including the introduction of a new checklist for EIPs and the identification of primary and backup coordinators.

**Click to expand detailed summary**

The team discussed recent physical activation activities, including BPO2 and Hudi, noting that Prism encountered issues with struggling attestation nodes. Manu explained that Prism was rejecting attestation from certain nodes, leading to disconnections and loss of peers, and mentioned a fix was being worked on. The team also mentioned that BP01 was expected to go live on Hudi later in the week.

Barnabas inquired about the status of claims release, with Manu confirming it would not be possible by the end of the day due to the need for bug fixes and soaking time. Enrico mentioned discovering incorrect KZG proofs in the network, primarily from Lodestar, and reported that a fix was being worked on, with the team planning to release it in the coming hours.

Barnabas and Enrico discussed an issue with blob sidecars containing incorrect KZG proofs, which were not detected earlier despite the invalid blocks. Enrico noted that changes in logging made the problem more evident and suggested implementing a metric to track rejections on subnets for better detection. Manu added that Lodestar was passing 0.6000 KZG cell proofs, and explained how bad proofs from the execution layer could lead to message rejections and disconnections in Prism, highlighting the need for trust in the execution layer.

The team discussed a bug related to zero proofs, where Manu reported seeing non-Lodestar clients, including Prism, occasionally producing invalid proofs. Enrico and Barnabas agreed this was not a critical issue as affected peers would be disconnected and sidecars not gossiped. Kamil provided an update on gas-submit testing, noting they had switched to 100 mega-gasz blocks for better stability and were working on EST compute scenarios and repricing branches, while facing some issues with Gnosis files.

The team discussed the status of client releases for the upcoming hard fork, with most teams aiming to release by November 5th, though some like Prysm and Lighthouse may need more time. They reviewed test results for BAL v1.3.0, which showed promising progress with most clients passing except Nethermind. The team agreed to stick to the original December 3rd mainnet fork date, with Barnabas requesting all major releases by Thursday’s AllCoreDevs meeting. Mario presented a new Testing Complexity Assessment Checklist for EIPs, which the team will use to prioritize testing efforts, particularly for repricing-related EIPs. Fredrik shared a mainnet upgrade and incident response plan, requesting client teams to identify primary and backup coordinators.

### Next Steps:

- Manu/Prism team: Fix the attestation bug and complete soaking before releasing
- Lodestar team: Fix the KZG proof bug causing zero proofs to be sent over the network
- Enrico/Nethermind: Release mainnet version in upcoming hours with KZG proof fix
- Barnabas: Check with Lodestar team about zero proof issues on Fusaka 3 devnet
- Enrico: Consider implementing metrics to track rejection rates on every subnet to catch similar issues
- Kamil/Nethermind: Work on mainnet release and address sync regression
- All client teams: Release mainnet clients with Fusaka support by November 5th  deadline
- All EL client teams: Confirm gas limit is set to 60 million by default in releases
- Geth and Besu teams: Signal readiness in Blob Access List chat for Glamsterdam devnet
- Stefan: Start Glamsterdam devnet once all client teams signal readiness
- Rahul/Testing team: Release new test suite version 1.3.0+ including Coinbase changes
- All client teams: Review and test against new consensus specs releases 1.6.0 and 1.6.0 beta 2 for ePBS
- Testing team: Prioritize repricing EIPs for complexity assessment
- Łukasz/Nethermind team: Share their EIP analysis and prioritization views in publishable form
- All client teams: Assign primary and backup coordinators for mainnet upgrade and incident response team
- Alex: Merge the mainnet upgrade and incident response team plan into upstream repo
- All client teams: Make PRs to add their coordinators to the incident response plan
- Parithosh: Reach out to community about gas limit updates once client releases are out

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =1F$xJ.6)
- Download Chat (Passcode: =1F$xJ.6)

---

**system** (2025-11-03):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=Um_f9tR-e_Q

