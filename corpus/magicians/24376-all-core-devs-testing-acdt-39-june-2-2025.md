---
source: magicians
topic_id: 24376
title: All Core Devs - Testing (ACDT) #39 | June 2 2025
author: system
date: "2025-05-29"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-39-june-2-2025/24376
views: 251
likes: 3
posts_count: 4
---

# All Core Devs - Testing (ACDT) #39 | June 2 2025

# All Core Devs - Testing (ACDT) #39 | June 2 2025

- June 2 2025, 14:00 UTC

# Agenda

- Gas limit retro
- Fusaka-devnet-0 status
- PeerDAS testing
- Discussion about history expiry and what our plan is for rollout, releases, docs, testing

Other comments and resources

The zoom link will be sent to the facilitator via email

Facilitator emails: XXXXX, YYYYY

 **🤖 config**

- Duration in minutes : 60
- Recurring meeting : true
- Call series : All Core Devs - Testing
- Occurrence rate : weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1561)

**YouTube Stream Links:**

- Stream 1 (Jun 02, 2025): https://youtube.com/watch?v=pxjlmW-Sc0M

## Replies

**poojaranjan** (2025-06-02):

# ACD Testing Call #39 – June 02, 2025

#### Summary

- Gas Limit Increase to 60M Accepted:
Client teams aligned on raising the gas limit to 60 million. Any increase beyond 60M should be gradual.
- Fusaka Devnet 0 Stable:
All clients successfully tested BPOs. Devnet 0 is looking promising. Sync testing and tool integration (eth-das-guardian) are next.
- Fusaka Devnet 1 Launch on June 9:
Will include implementation of EIP-7917 and Validator Custody. PR #4190 needs review from all client teams.
- Validator Custody in Progress:
Most clients are implementing or finalizing custody features. Targeting readiness by Devnet 1. PR #4320 reviewed as canonical reference.
- Metrics Inclusion Approved for Devnet 1:
Both CL and EL side metrics will be added. A tracking repo for metric changes will be created.
- Column Sidecar Improvements Coming:
Custom implementation in Teku; plan to propose changes for wider client support via PR.
- Next week’s ACDT (Interop) call is cancelled.

## Quick Notes

**Parithosh J** lead the call.

- Retrospective post on EIP-7691 is out
TL;DR:

Estimations were accurate
- Bring further discussions to the ACDT issue

## Gas Limit Retrospective

**Pari:**

- Hoodi gas limit: 60 million gas
- Suggests slowly increasing limit in future.

**Barnabas:**

- Should we move in two phases? (e.g., signal to 48M first, then 60M)

**Kamil:**

- Decent percentage of validators already signaling 60M
- 60M seems reasonable
- Smaller incremental steps (e.g., 15–20M) are unlikely
- 60M is a no-brainer

**Barnabas:**

- Doubling gas limit is a significant change

**Ben:**

- 60M seems fine
- Above that, be more cautious

**Justin F.:**

- 48M step seems unnecessary

**Decision:** Client teams are okay with a move to 60M. Future increases should be gradual.

**Next Step:**

Focus on max CL size this week.

**Toni Wahrstätter:**

> If max CL size is 2.5 MiB, 65M gas may reach the 10min limit. 60M is safe.

## Fusaka Devnet 0 Status

[PeerDAS & Fusaka Devnet Updates](https://github.com/ethereum/pm/issues/1561#issuecomment-2927893242) by Will C.

**Pari:**

- PeerDAS testing channel and PeerDAS Devnet 7 will be deprecated
- Moving forward PeerDAS testing will happen on Fusaka testing stream
- Fusaka Devnet 0 is the new focus
- Communication moved to Fusaka Interop channel. Suggested to keep in thread.

**Barnabas:**

- Fusaka Devnet 0 started out with Genesis.
- Max blob cout at 9 on epoch 256.
- Increased the max blob cout to 12 with the first BPO and at the second BPO, it is increased to 15 than to 18 and then went down to 9. Will be increased to up to 20.
- All BPOs functioning well.
- All clinet successfully upgrading and downgrading
- No forks reported to BPO.

**Pari:** Devnet 0 is looking promising!

Note: ProbeLab team’s tool - [eth-das-guardian](https://github.com/probe-lab/eth-das-guardian) is now open source.

will be integrated to testing stack. Clients Teams should check if their node is live.

**Next Steps (Barnabas):**

- Repeat Sync testing planned to check if clients are able to backfill.
- Building UI for integrating the new tool

## PeerDAS Validator Custody Updates

### Client’s update

**Prysm (Manu):**

- Implemented validator custody
- Backfill still in progress

**Lighthouse (Pawan):**

- WIP, expected by end of week
- Backfill not yet implemented
- Tricky implementation wise, yet on track for interop

**Nimbus (Agnish):**

- No backfill required at Nimbus
- Validator custody can change within slot start

**Francis:**

- Encourages everyone to review the PR Merged
- Addresses concerns with backfill and custody changes

**Justin:**

- PR was made to address frequent custody changes

**Agnish:**

> For multi-Beacon Node setups, it’s better to act as a “super node”

**Q&A:**

- Pawan: What endpoint does Prysm use to find attached validator node?
- Manu: Beacon proposer from API
- Kasey: Validator registration via Beacon API
- Agnish: Could non-enforcement of custody lead to network partitioning?

**Raul:**

> Some edge cases require deeper analysis – discussion to continue offline.

**Next Step:** Target validator custody for next week.

**Barnabas:** Will add PR to Devnet 0.

## Fusaka Devnet 1 Plans

**EIP-7917:**

- PR #4190
- Launch planned for June 9, 2025
Fusaka Devnet 1 Notes

**Client Updates for EIP-7917:**

- Justin: PR open, clients should review
- Prysm: In progress
- Lodestar (Phil): In progress

**Decision:** Devnet 1 will focus on:

- Validator custody
- EIP-7917 implementation

## getBlobsV2 Metrics (EL Side)

**Updates:**

- Besu (Gabriel): On track
- Reth, Erigon, Nethermind: On track
- Geth: Check async

## BPO Networking Updates

**Raul:**

- Adding a key to ENR to signal next upgrade
- EIP incoming, tweaks expected
- No network partition observed yet
- May delay until Devnet 2

**Justin T.:**

- Suggests keeping it for Devnet 2
- It will allow time to add more tests in Devnet 2 for BPO

Other links

- EIP PR #9840
- Consensus Specs PR #4346

## Metrics Implementation

**CL side metrics**

**Katya:**

- Added metrics; potential spec change needed
- Lodestar is testing
- PR still in progress

**EL side metrics**

**SunnySide (J):**

- Discord Reference
- Reth, N/M, EthJS implemented original version
- Awaiting EL feedback

**Decision:**

Include metrics changes in Devnet 1 and create a repo to track them.

## SunnySide Labs Testing Update

[Update – May 30, 2025](https://testinprod.notion.site/Sunnyside-Devnet-Updates-05-30-Internal-2008fc57f54680ea81cde6acaa6d55fc)

- Ran 7 devnets
- Blob count more stable
- Focused on bottlenecks
- LH: Up to 53 blobs per block
- Prysm: Also high
- Grandine: Failed beyond 10 blobs due to old image

**Findings:**

- Grandine sometimes succeeded with retries
- Column processing and gas combos might affect getBlobs
- LH: Reported many column failures

**Next Step:**

J (Sunny side) will create thread on Interop channel for client by client analysis.

## Column Sidecar

**Dimitri:**

- Not available in Beacon API yet
- Teku: Custom implementation exists

**Pari:**

- Will propose PR to add this event

## Meeting Scheduling Notes

- Next week’s ACDT (Interop) call: Cancelled

---

**system** (2025-06-02):

### Meeting Summary:

No summary overview available

**Click to expand detailed summary**

The team discussed the success of the Petra retrospective blog post, which accurately estimated the network’s blob count. They agreed to proceed with increasing the gas limit to 60 million, with client teams tasked to monitor metrics and signal the change asynchronously. The group decided to move all PRDOS testing to the Fusaka testing stream, with all relevant chat conversations to be moved to the interop chat channel. Barnabas provided updates on Fusaka Devnet 0, detailing the changes in maximum drop count across different epochs.

The team discussed the implementation status of validator custody and data availability features across different client implementations. Barnabas reported successful BPO testing with no issues found, while Parithosh introduced a new probe tool for network testing. Client teams provided updates on validator custody implementation, with Lighthouse expecting completion before the interop event and Members having validated custody but discussing potential issues with dynamic DA changes. Justin presented a merged PR that simplifies the custody specification by allowing implementers to wait until the custody period is passed before making changes, addressing concerns about network stability and backfilling requirements.

Manu discussed the challenges node operators face when switching between beacon nodes to minimize IP loss, highlighting that the current setup limits a node to serving only four data clubs, which undermines the purpose of validator custody. Justin Traglia suggested changing the “should not backfill” specification to “may not,” acknowledging that this could be an implementation detail. Pawan and Agnish explored the practicality of a static custody model and discussed endpoint usage in Prism for determining validator attachments, with Manu clarifying the relevant API endpoint. The group debated the pros and cons of shifting to a static custody model, with concerns raised about the impact on supernode availability and network performance.

The team discussed concerns about the accuracy and enforceability of validator custody counts in multi-BN setups, with Agnish raising questions about potential risks and attacks. Francesco explained that while custody is important for ensuring a baseline of super nodes, it’s not strictly enforceable and can be influenced by node operators’ setups. The team agreed to take the issue offline for further analysis, with Raúl and Francesco planning to collaborate on a deeper examination of edge cases. They decided to implement a MAY functionality as a temporary solution, with the goal of having a final solution for validator custody in place by next week.

The team discussed the upcoming Fusaka devnet 1 launch on Monday, June 9th, which will include EIP-7917 for deterministic proposer look-ahead and validator custody changes. They agreed to postpone the BPO networking changes and metrics implementation to devnet 2, as these changes would require more time for review and testing. Client teams reported progress on implementing the necessary changes, with most clients on track for the devnet release. The team also discussed the need for sales teams to review and approve the EIP-7917 specification.

The team discussed metrics implementation, with Barnabas taking lead on merging metrics PRs and addressing Justin’s question about BPO fork schedules. Parithosh agreed to add EL metrics changes to devnet and create a repository for EL metrics to share PRs and discuss implementation. The Sunnyside Lab team provided an update on their testing progress, having conducted 7 dead notes over the past 10 days.

The team analyzed the impact of get blob enablement on different CEOs and found interesting results. Without get blobs, block time was more stable but block counts were lower. With get blobs enabled, block counts increased by 15% for Lighthouse and 3% for Prism. They discovered that Grandine requested multiple get blobs when failing, while other CEOs requested only once. The team also found that disabling get blobs reduced data column failures on Lighthouse, leading them to suspect get blobs might be handling wrong columns. They plan to test this with Russ to confirm. Additionally, they noted that column processing time was inversely proportional to the number of requests, with Grandine having the most requests and shortest time, and Teku having the least requests and longest time.

The team discussed technical issues related to local size and CPU RAM, with J suggesting an increase in local size to 42.6 MB due to blob size concerns. Parithosh proposed creating threads on the interop chat for further discussion with respective teams. The group also confirmed migrating to the Fusaka devnet 0 spec for the next version of the net. Parithosh announced the cancellation of next week’s call due to an in-person interop event and ACD meeting. Finally, they discussed adding column site calls to the Beacon API event stream, with Dmitrii noting its absence in the backend API but presence in a Telco customer implementation.

### Next Steps:

- Client teams to review and implement validator custody changes, including the new PR discussed.
- Research team (Francesco, Raul, Justin) to analyze edge cases for validator custody changes and update the specification accordingly.
- Barnabas to add the updated validator custody PR to the Fusaka devnet 1 specification once available.
- Client teams to implement EIP-7917 (deterministic proposal look-ahead) for Fusaka devnet 1.
- Justin to merge approved PRs and create a release/tag for client teams to use for testing by Tuesday.
- Barnabas to ensure metrics PRs are merged for both CL and EL sides.
- Sunnyside Lab team to create threads in the interop chat for discussing their testing results with respective client teams.
- Parithosh to organize a repository for EL metrics similar to the CL metrics repository.
- Client teams to migrate to the Fusaka devnet 0 specification for the next version of testing.
- Parithosh to make a PR to add column sidecars to the Beacon API event stream.
- Parithosh to post a message on AllCoreDevs regarding the potential cancellation of next week’s call due to the in-person interop event.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =2i6pLQo)
- Download Chat (Passcode: =2i6pLQo)

---

**system** (2025-06-02):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=pxjlmW-Sc0M

