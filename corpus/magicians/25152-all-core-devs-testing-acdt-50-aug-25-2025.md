---
source: magicians
topic_id: 25152
title: All Core Devs - Testing (ACDT) #50 | Aug 25 2025
author: system
date: "2025-08-19"
category: Protocol Calls & happenings
tags: [acd, acdt]
url: https://ethereum-magicians.org/t/all-core-devs-testing-acdt-50-aug-25-2025/25152
views: 81
likes: 5
posts_count: 4
---

# All Core Devs - Testing (ACDT) #50 | Aug 25 2025

### Agenda

- Fusaka devnet status updates
- BPO Static Tests Updates
- Gas limit testing updates
- Glamsterdam testing updates: BALs and ePBS
- Sunnyside labs testnet updates

**Meeting Time:** Monday, August 25, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1692)

## Replies

**abcoathup** (2025-08-21):

### Notes



    [![](https://ethereum-magicians.org/uploads/default/original/2X/5/5dac7cbbca817547901f15be798f33185e5453a6.png)547×494 200 KB](https://ethereum-magicians.org/uploads/default/5dac7cbbca817547901f15be798f33185e5453a6)

      [All Core Devs - Testing (ACDT) #50 | Aug 25 2025](https://ethereum-magicians.org/t/all-core-devs-testing-acdt-50-aug-25-2025/25152/3) [Protocol Calls & happenings](/c/protocol-calls/63)




> Meeting Summary:
> The team discussed ongoing network issues and client stability concerns following a non-finality event, with most machines restarting but participation dropping to 36%. They addressed a bug in the state upgrade from Electra to Hulu and reviewed progress on the MEV workflow, including successful builder launches and testing improvements. The team established timelines for Devnet 5 and the mainnet release, while also discussing various technical improvements including performance …

### Recordings/Stream

- YouTube
- X Livestream [x.com/echinstitute]

### Writeups

- ACDT#50: Call Minutes + Insights by @Christine_dkim [christinedkim.substack.com]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists

---

**system** (2025-08-25):

### Meeting Summary:

The team discussed ongoing network issues and client stability concerns following a non-finality event, with most machines restarting but participation dropping to 36%. They addressed a bug in the state upgrade from Electra to Hulu and reviewed progress on the MEV workflow, including successful builder launches and testing improvements. The team established timelines for Devnet 5 and the mainnet release, while also discussing various technical improvements including performance optimizations, client tooling updates, and consensus testing developments.

**Click to expand detailed summary**

The team discussed the status of the Fussaka network after a non-finality event. Barnabas reported that while most machines had restarted and were syncing, participation had dropped to 36% with some nodes hitting rate limits. Pawan mentioned ongoing issues with the Lighthouse client’s unstable branch, which he planned to fix and update the team on. The team agreed to monitor the situation without making further changes for now, as they aimed to recover to finality within a day.

The team discovered a bug in the state upgrade from Electra to Hulu, which was fixed by Enrico’s pull request. They discussed the need for more comprehensive testing of state transitions and pending consolidations. Justin agreed to look into adding tests for pending consolidations in the spec test. Bharath reported progress on the MEV workflow, including resolving an issue with transaction retention and the successful launch of a second builder. The team also noted some concerns about block simulation failures during the transition from Electra to Hulu, which Kail is investigating.

The team discussed the Mev workflow release, with Bharath reporting that Mevboost is ready to merge to main but is waiting on attestation IOPRs. Barnabas provided an update on Devnet 5, stating that the main blocker is trunk branches and major features merging, with a target to merge all features to trunk branches by Friday and aim for a Devnet launch on Wednesday next week. The team agreed to this timeline, with Parithosh emphasizing the need for advance notice if any changes are needed. Stokes raised the possibility of coupling the Hoodie release with the mainnet release, which was discussed further, with Pawan and Fredrik suggesting a shorter gap between the releases if the testnets go smoothly.

The team discussed the timeline for Devnet 5 and subsequent releases, with Parithosh and Stokes agreeing to aim for a 12-hour interval between BPOs and to collect additional Mev-style data. They confirmed that the mainnet release date remains set for October 1, with a full spec for Devnet 5 to be released over the week. Luis provided an update on the Besu team’s work to address performance issues caused by big integer libraries in Java, stating that they plan to implement arithmetic operations directly on bytes or primitive arrays to improve efficiency.

The team discussed several key topics including benchmarks, gas optimization, and client tooling. Luis reported on work with opcodes and gas improvements, while Marius shared updates on MODX challenges and potential strategies. The group explored the possibility of implementing OpenTelemetry for better performance tracking, with some clients already supporting it. Terence provided an update on EPBS development, highlighting progress on consensus spec tests and the need for further tuning. Toni mentioned an upcoming breakout call for block-level access list discussions. Minhyuk reported on Sunnyside Labs’ work, including analyzing network issues and developing a chaos testing tool for stress testing. The conversation ended with an open floor for any additional topics.

### Next Steps:

- Client teams to merge all major features into trunk branches by this Friday for Devnet 5 preparation.
- Lighthouse team to merge fixes from unstable branch and provide updated branch information to Barnabas.
- Justin Traglia to look into adding spec tests for pending consolidation at fork transitions.
- Justin Traglia to prepare Beta 0 spec release in about a week.
- Fahil from PBS foundation to continue investigating the block simulation failure issue with the relay during Electra to Fusaka transition.
- Alex Stokes to create a written devnet and release timeline document before the next ACD call.
- Nethermind, Reth, and Aragon teams to provide a flag similar to “required block” for sync tests.
- Besu team to continue working on implementing notes from scratch in Java to address division performance issues.
- Geth team to decide on a strategy for addressing ModX performance bottleneck this week.
- Parithosh to share examples of open telemetry implementation for client teams to consider.
- Client teams to join the EPBS breakout call on Friday if working on EPBS or gun survey.
- Interested parties to join the block-level access list breakout call on Wednesday at 2 PM UTC.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: &Bhpzrh0)
- Download Chat (Passcode: &Bhpzrh0)

---

**system** (2025-08-25):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=r7bdQdnBclo

