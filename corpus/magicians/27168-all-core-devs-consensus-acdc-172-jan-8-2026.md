---
source: magicians
topic_id: 27168
title: All Core Devs - Consensus (ACDC) #172, Jan 8, 2026
author: system
date: "2025-12-15"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-172-jan-8-2026/27168
views: 93
likes: 0
posts_count: 3
---

# All Core Devs - Consensus (ACDC) #172, Jan 8, 2026

### Agenda

- Happy 2026, last ACDC: #1825
- Announcements

New breakout on FCR: All Core Devs - Consensus (ACDC) #172, Jan 8, 2026 · Issue #1844 · ethereum/pm · GitHub
- All Core Devs - Consensus (ACDC) #172, Jan 8, 2026 · Issue #1844 · ethereum/pm · GitHub

Fusaka

- BPO2 status

Glamsterdam

- EL lean to CFI EIP-8070 (Sparse blobpool), final call
- EIP-7688 update to tree shape: All Core Devs - Consensus (ACDC) #172, Jan 8, 2026 · Issue #1844 · ethereum/pm · GitHub
- local censoring signal proposal: All Core Devs - Consensus (ACDC) #172, Jan 8, 2026 · Issue #1844 · ethereum/pm · GitHub

Heze

- Headliner process

NOTE: overview of process and timelines
- Short discussion on fork focus/theme
- Open headliner submission, proposals must be made BEFORE 5 Feb 2026.

**Meeting Time:** Thursday, January 08, 2026 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1844)

## Replies

**system** (2026-01-08):

### Meeting Summary:

The team discussed several technical implementations including a fast confirmation rule and BPO 2 event performance, while also reviewing developments in Glamsterdam and addressing concerns about EIP 8070. The meeting covered various proposals and technical discussions around CIP per-slot pools, tree structure modifications, and an Engine API change for builder censorship tracking. The team concluded with discussions about proposal submission processes, network resilience considerations, and the balance between feature development and technical debt management.

**Click to expand detailed summary**

The meeting began with New Year greetings and technical issues with audio. The team discussed the fast confirmation rule, with Mikhail explaining that a production-ready implementation is expected by March, and bi-weekly breakout calls will start on January 20th. They reviewed the BPO 2 event, noting that while 21-blob blocks were harder to find due to lower transaction volumes during the holidays, the protocol performed well. The team also discussed Glamsterdam, where Lodestar DAI and CFI DIPs are being developed, and concluded with a discussion about EIP 8070, which the EL side wanted to confirm should be CFI’d back to the CL side.

The team discussed two main topics: a CIP per-slot pool that has some CL elements, which Ansar brought up for potential CL concerns before moving to CFI, and Etan’s proposal to modify the tree shape for stable containers in EIP7688. Etan explained the benefits of the proposed tree structure change for incremental tree construction, though it would make multi-proof slightly more challenging. The team agreed to take feedback to the PR and discuss further in the SSZ channel on Discord, with Etan planning to proceed if there’s no opposition in a week.

The meeting discussed a proposal to add a boolean in the Engine API to indicate censorship by builders, which would allow clients to track and potentially blacklist builders. Tony expressed concerns about the implications of this change due to differences in mempool implementations across clients. The group also reviewed the process for scoping Hagota, including a proposal period and the introduction of headliner proposals similar to the process used for Glamsterdam. The conversation ended with a brief discussion on the theme for the fork, with Ansgar suggesting to wait for headliner proposals before finalizing the theme.

The meeting focused on the process of submitting proposals for the EthMagicians post and presenting them on an ACD call by February 5th. Ansgar emphasized the need to be open to hard forks that align with integrated themes, such as Glamsterdam, but noted that it’s unclear if Edge will follow this path. Marius and Potuz discussed the importance of CL hardening and resilience, highlighting the need for social coordination and infrastructure to handle scenarios like invalid finalized checkpoints, which could lead to chain splits. The group agreed on the necessity of testing and exercising these code paths to ensure network stability.

The team discussed the trade-off between developing new features and addressing technical debt, with Saulius emphasizing that small teams may struggle to find time for non-feature development due to time constraints. Mikhail highlighted ongoing work on fork-choice compliance testing, noting plans to integrate these tests with ePBS changes, while Potuz raised concerns about potential bugs in the ePBS protocol, particularly regarding builder validators and deposit handling. The group agreed to keep these considerations in mind as they move forward with scoping and testing in the new year.

### Next Steps:

- Mikhail and Will: Host bi-weekly breakout calls on fast confirmation rule starting January 20 at 2pm UTC
- Mikhail and team: Complete tests with decent coverage for fast confirmation rule by end of January/beginning of February
- Mikhail and team: Have production-ready implementations of fast confirmation rule in CL clients by beginning of March
- All interested parties: Review and provide comments on Champion notion document PR in the PM repo
- All interested parties: Provide feedback on EIP 7688 tree shape change in SSZ channel within one week
- Etan: Proceed with EIP 7688 tree shape change if no opposition received in SSZ channel after one week
- Potuz: Propose censoring detection boolean in Engine API on ACDE call
- All interested parties: Continue discussion on censoring detection in ePBS channel
- All interested parties: Submit Hagota headliner proposals with EthMagicians post and ACD presentation by February 5th
- All interested parties: Add comments on Hagota fork theme/focus to the EthMagicians post
- Prysm team: Implement recovery from non-finalized checkpoint syncing
- All CL client teams: Schedule devnet to test checkpoint syncing from non-finalized checkpoint and social recovery scenarios
- Mikhail and team: Update fork-choice compliance testing suite with ePBS changes
- All CL client teams : Integrate fork-choice compliance testing suite into their clients
- Mikhail and team: Apply model-based testing to PBS scope for stage position

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: rZp!#3b^)
- Download Chat (Passcode: rZp!#3b^)
- Download Audio (Passcode: rZp!#3b^)

---

**system** (2026-01-08):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=ZXxk3cV7Tjw

