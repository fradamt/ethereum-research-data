---
source: magicians
topic_id: 27511
title: All Core Devs - Testing (ACDT) #67, January 26, 2026
author: system
date: "2026-01-19"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-67-january-26-2026/27511
views: 49
likes: 2
posts_count: 5
---

# All Core Devs - Testing (ACDT) #67, January 26, 2026

### Agenda

#### Glamsterdam

- bal-devnet-2 updates

spec reference tests release
- Progress update by @qu0b: All Core Devs - Testing (ACDT) #67, January 26, 2026 · Issue #1882 · ethereum/pm · GitHub
- EIP-7778 Discussion

epbs-devnet-0 update

- Standardized ePBS Beacon API: Comment, PR Link

#### Gas Benchmarking Updates

- Updates

#### Process

- CFI → Devnet Process Discussion

#### Others

- BPO Meta EIPs

**Meeting Time:** Monday, January 26, 2026 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1882)

## Replies

**system** (2026-01-26):

### Meeting Summary:

The team discussed progress on various Ethereum clients’ implementation of new EIPs, with most clients reporting good progress and no major blockers, and agreed to aim for having three clients ready by Wednesday to launch the devnet. They decided to delay the implementation of EIP-7778 to DevNet 2 for one week to allow for receipt format changes, giving clients more time to implement necessary updates. The meeting covered updates on beacon APIs, fork choice changes, and ongoing development work, including discussions on improving the process for moving EIPs from CFI to devnet and feedback on meta EIPs for BPO upgrades.

**Click to expand detailed summary**

Mario led ACDT 67 on January 26th, 2026, and began by discussing Glamsteram, focusing on two key updates. The first was the release of a reference spec test for Block access list EIPs, which participants were encouraged to test and report issues in the ETH Discord. Mario also mentioned that Stefan or Nicole had provided a comprehensive update, but the details were not specified in the transcript.

Stefan requested to push discussions on open PRs related to BAL and reviewed the progress of clients, noting that the main blocker is the slot-nom EIP, as most clients lack engine methods to reach the Vlas Fork. He suggested merging these methods or receiving updates and emphasized the need for flags to enable or disable block-level access list optimizations, which would unblock repricing efforts. Toni mentioned that JSON RPC methods for clients were implemented to aid debugging, and the engine API method was discussed further for consensus on Wednesday’s call. Felipe explained that block-level access lists were reintegrated into blockchain tests for the 4.0.0 release, aligning with previous DAO releases.

The team discussed the status of various Ethereum clients’ implementation of new EIPs, with most clients reporting progress and no major blockers. Geth, Besu, Reth, Nethermind, and Erigon all confirmed they were making good progress, with some EIPs already merged and others in review. The team agreed to aim for having three clients ready by Wednesday to launch the devnet, with the possibility of adding more clients as they complete implementation. Mario offered to provide help with running engine-api tests for clients who need it.

The team discussed implementing EIP-7778, which affects transaction receipts and gas usage tracking. While some clients like Erigon prefer the version that doesn’t require changes to the receipt format due to implementation complexity, there was broad consensus that the version without receipt changes is ultimately better for the protocol. The team decided to delay the implementation of EIP-7778 to DevNet 2 for one week to allow for the receipt format change to be made, rather than rushing it into DevNet 2 this week. This delay will give clients like Erigon more time to implement the necessary changes.

The team discussed removing a field from the receipt for EIP implementation, with Dragan agreeing to proceed with the change. They reviewed progress on ePBS, with Stefan Starflinger committing to prepare a test release soon. Client updates were shared, with Lighthouse working on consensus changes and interop testing, Teku making progress but not much to report, and other clients like Nimbus and Pota’s making steady progress on spec functions and Beacon APIs. The team debated the timing of devnet-0 launch, with a target of February 18th mentioned, though some clients like Lighthouse may not be ready in 10 days. Dustin raised concerns about backwards compatibility issues with fork choice changes, suggesting a need to carefully consider implementation strategy.

The meeting focused on updates and discussions around the Ethereum protocol development, particularly concerning the devnet, beacon APIs, and EIPs. Nico reported on the implementation of ForkChoice and builder entity, with ongoing testing and exploration of block importing and state cache architecture. The team discussed the Beacon API changes, with a preference for option 3, which keeps the current two-step process but returns all block contents, though final feedback is still needed. Dustin raised concerns about potential consensus risks from fork-choice variations, and the team agreed to further discuss this on Discord. Justin mentioned ongoing work on specs for the next devnet (Alpha 2), with a planned release on February 13th. Kamil provided updates on gas benchmarking, including ongoing data analysis and stateful testing. The team also discussed improving the process for moving EIPs from CFI to devnet, with suggestions for clearer communication and decision-making processes. Pooja shared PRs related to BPO and requested feedback on meta EIPs for BPO upgrades.

### Next Steps:

- All clients: Test their implementations using the reference spec test release shared last week and raise any issues in the ETH Discord
- All clients: Review and provide feedback on open PRs for Block Access List, particularly the slot-nom EIP engine methods
- All clients: Implement flags to enable and disable block-level access list optimizations
- LightClient: Approve the EIP update PR regarding the comment on the Discord channel
- Felipe or Mario: Provide help to clients with consumption of engine-api tests that include seldom
- Clients : Reach out to Stefan when ready to join devnet 2
- Guru: Finalize the draft PR for EIP 7778 changes once decision is made
- Tony: Make a write-up in the Discord about EIP 7778 to ensure everyone is aligned
- All clients: Provide feedback on Beacon API options  in the PR shared by Nico
- Dustin: Bring the ForkChoice topic into the 8R on Discord for async discussion and clarification
- Louis: Create a benchmark release that supports Osaka and run benchmarks under Osaka 4
- All participants: Review Mario’s proposed CFI EIP to DevNet process and provide feedback
- All participants: Review Pooja’s PRs for BPO-related documentation, meta EIPs for BPO1 and BPO2, and provide feedback on representation preferences and estimated number of BPO upgrades per year

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: !3KFI!?k)
- Download Chat (Passcode: !3KFI!?k)
- Download Audio (Passcode: !3KFI!?k)

---

**system** (2026-01-26):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=EUhKZYGRjBw

---

**poojaranjan** (2026-01-26):

Quick recap ACDT 67: [Tweet Thread](https://x.com/poojaranjan19/status/2015853372172063099)

---

**abcoathup** (2026-01-28):

## Call details

### Video, transcript & chatlog

- All Core Devs Testing #067 - Forkcast - [Forkcast] by EF Protocol Support

### News coverage

- [Ethereal news] edited by @abcoathup
- ACD After Hours: ACDT #67 - [ACD After Hours] by @Christine_dkim
- [Etherworld] by @yashkamalchaturvedi

### Resources

- Glamsterdam Upgrade - Forkcast
- Hegotá Upgrade - Forkcast

