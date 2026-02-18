---
source: magicians
topic_id: 25807
title: All Core Devs - Execution (ACDE) #223, October 23, 2025
author: system
date: "2025-10-14"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-223-october-23-2025/25807
views: 120
likes: 2
posts_count: 5
---

# All Core Devs - Execution (ACDE) #223, October 23, 2025

### Agenda

- Fusaka

testnet updates by @barnabasbusa

Sepolia BPO1 recap
- upcoming: Sepolia BPO2, Hoodi

[mainnet dates confirmation request](https://github.com/ethereum/pm/issues/1764#issuecomment-3412633683) by [@ralexstokes](/u/ralexstokes)

- document with candidate dates
- alternative BPO timing
- comment by @abcoathup: wait with official date setting until after testnets

Glamsterdam

- devnet updates?
- non-headliner EIP process proposal by @ralexstokes and @adietrichs
- repricing topics by @misilva73

temperature check: best approach for increased gas precision
- proposal for breakout calls

EIPs to potentially remove from PFI:

- EIP-7667 because of lack of champion
- EIP-6873 because of Verkle dependency

[EIP-8058 presentation](https://github.com/ethereum/pm/issues/1764#issuecomment-3436742283) by [@CPerezz](/u/cperezz)
open discussion

**Meeting Time:** Thursday, October 23, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1764)

## Replies

**abcoathup** (2025-10-14):

### Summary

*[link to [@adietrichs](/u/adietrichs) summary]*

### Recordings/Stream

- All Core Devs Execution #223 - Forkcast
- Live stream on X and Spotify: [x.com/ECHInstitute]

### Writeups

- ACDE #223: Call Minutes + Insights] by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE #223 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]
- Testnet schedule;  Holešky Oct 1,  Sepolia Oct 14, Hoodi Oct 28; mainnet proposed for December 3 (Fusaka & BPO timelines - HackMD); proposed mainnet date setting process change

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners are being proposed for inclusion: deadline for proposal is October 30; client teams to provide writeups on high level preferences by November 6; EIP champions should be available to answer questions
- Presentations: Rounding Errors in Compute Opcodes (solutions: rebase vs milli-gas) & EIP-8058: Contract Bytecode Deduplication Discount

[Holešky shutting down](https://blog.ethereum.org/2025/09/01/holesky-shutdown-announcement) Oct 31st

---

**poojaranjan** (2025-10-23):

Tweet summary: https://x.com/poojaranjan19/status/1981359963722129901

---

**system** (2025-10-23):

### Meeting Summary:

The meeting covered updates on testnets and mainnet timelines, including discussions about upgrading schedules and node migration requirements. The team reviewed and prioritized Ethereum Improvement Proposals (EIPs) for the Glamsterdam event, establishing deadlines and processes for proposal reviews and client feedback. Technical discussions focused on gas pricing solutions, contract deployment mechanisms, and the removal of certain EIPs from the PFI list, with the meeting concluding after brief consideration of a max-blobs limit proposal.

**Click to expand detailed summary**

The meeting began with greetings and agenda updates from Ansgar, who mentioned last-minute additions and a change in the order of topics. Barnabas provided updates on the Sepolia and Goerli testnets, noting smooth progress and upcoming events, including the retirement of the Goerli testnet. Alex discussed mainnet dates for the Fusaka upgrade, proposing December 3rd for the mainnet, December 9th for BPO 1, and January 7th for BPO 2, with a reminder about an adjusted time for BPO 1. Participants were encouraged to update their nodes and migrate infrastructure from the Goerli testnet to Sepolia or Goerli as needed.

The team discussed and agreed to move the BPO1 proposal from December 17th to December 9th due to concerns about the original date falling close to Christmas. They confirmed that client releases would be scheduled for November 3rd, one month before the proposed mainnet date, pending successful completion of the Hoodi finalization next week. The team also debated the language around mainnet update requirements, with Barnabas proposing to clarify that maintenance should not have an upgraded set until all testnets have been upgraded, though this discussion was deferred to an async PR to allow further consideration of Potuz’s concerns about client configuration changes and advertising.

The team discussed the deadline for proposing EIPs for the Glamsterdam event, agreeing that the intent to propose should be signaled within one week, while the actual EIP and proposal should be merged within two weeks. They decided that a PR to the EIP repo would suffice for the initial deadline, and clients were asked to provide lists of EIPs and opinions by November 6th to help prioritize proposals. The team also noted progress on devnets, with Stefan mentioning that a BAL devnet would be available soon.

The team discussed the review process for 30-31 proposed EIPs, with 3 CL-side EIPs and 27-28 EL-side EIPs. They agreed to have a first round of opinions formed over the next two weeks, focusing on EL EIPs, with CL teams invited to participate if they find it useful. The group decided to use extra time in future ACDC calls to discuss EL EIPs after completing the initial review period, rather than trying to fit everything into the two-week timeline. They also discussed ways to make EIPs more legible, including having client teams highlight proposals they absolutely don’t want to spend time on.

The meeting focused on several key topics related to Ethereum Improvement Proposals (EIPs) and gas pricing. Maria presented two potential solutions for addressing rounding errors in gas pricing: a 1000x rebase of all gas values and a fractional gas proposal. The group discussed the pros and cons of each approach, with some members expressing concerns about the impact on existing contracts and tooling. Carlos presented EIP 8058, which proposes a deduplication mechanism for contract deployments using access lists. The team also decided to remove two EIPs (7667 and 6873) from the PFI list, as they were not relevant for the Glamsterdam fork. The conversation ended with a brief discussion of EIP 7872, which proposes to make the max-blobs limit a meta-EIP rather than a core consensus change.

### Next Steps:

- Maria to schedule two breakout calls on Wednesdays at 3 UTC  to discuss repricing EIPs.
- All EIP champions to make themselves available over the next two weeks to answer questions about their EIPs.
- All client teams to prepare documents with their opinions on the proposed EIPs by November 6th .
- Ansgar to remove EIP 7667 and EIP 6873 from the PFI list.
- Guillaume to create a write-up on code chunking compatibility with EIP 8058.
- All client teams to discuss internally whether to keep or remove the ACDE call during DevCon week and be ready to share their decision at the next call.
- Barnabas to update the mainnet dates document with BPO1 on December 9th .
- Client teams to prepare for client releases on November 3rd .

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: Jf@2P#5#)
- Download Chat (Passcode: Jf@2P#5#)

---

**system** (2025-10-23):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=In1-paNfjzQ

