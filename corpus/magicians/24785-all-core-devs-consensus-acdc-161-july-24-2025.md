---
source: magicians
topic_id: 24785
title: All Core Devs - Consensus (ACDC) #161, July 24 2025
author: system
date: "2025-07-11"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-161-july-24-2025/24785
views: 534
likes: 5
posts_count: 6
---

# All Core Devs - Consensus (ACDC) #161, July 24 2025

# All Core Devs - Consensus (ACDC) #161, July 24, 2025

- Jul 24, 2025, 14:00 UTC

# Agenda

- Fusaka

devnet-2
- devnet-3 launch
- proposal: assuming devnet-3 stability soon, start hardening work, agree to intent to have release candidates out by end of August
- any other open issues?

Glamsterdam

- headliner discussion

shorter slot times - update
- epbs - “free option problem”
- progress on headliner selection

Specs

- SSZ spec question: All Core Devs - Consensus (ACDC) #161, July 24 2025 · Issue #1614 · ethereum/pm · GitHub

Facilitator emails:

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : acdc
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- display zoom link in invite : false

[GitHub Issue](https://github.com/ethereum/pm/issues/1614)

## Replies

**abcoathup** (2025-07-18):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #161, July 24 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-161-july-24-2025/24785/6) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #161 summary
> ACDC #161 Action Items
>
> fusaka-devnet-3 is live! Continue monitoring (and debugging issues as they arise) to progress towards mainnet.
> The following EIPs have been CFI’d for Glamsterdam to signal potential CL headliners
>
> EIP-7732 (ePBS)
> EIP-7782 (Six second slots)
> EIP-7805 (FOCIL)
>
>
> Outcome of next ACDE and the prior list will be used to make a final call on the CL headliner on the next ACDC on 7 August.
> Community input: please add here Soliciting stakeholder feedback on Glams…

### Recordings/Stream

- https://www.youtube.com/live/U_oFzvFrqwY?t=173s
- Eth Cat Herders:

Live stream on X: [x.com/ethcatherders]

### Writeups

- Tweet thread by @poojaranjan
- ACDC #161: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- Highlights from the All Core Developers Consensus (ACDC) Call #161 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Ideally targeting mainnet November 5-12 (before Devconnect)
- Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Consensus layer headliner short list, decide headliner at ACDC August 8, Stakeholder feedback wanted:

EIP7732 ePBS
- EIP7782 Six second slots
- EIP7805 FOCIL

Presentations:

- EIP7782 Six second slots: Slot timings preliminary results
- EIP7732 ePBS: Free option problem

---

**poojaranjan** (2025-07-24):

Quick Tweet thread - https://x.com/poojaranjan19/status/1948382665415004260

---

**system** (2025-07-24):

### Meeting Summary:

No summary available. Could not retrieve summary.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: $#g7z=D0)
- Download Chat (Passcode: $#g7z=D0)

---

**system** (2025-07-24):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=U_oFzvFrqwY

---

**ralexstokes** (2025-07-24):

# ACDC #161 summary

**ACDC #161 Action Items**

- fusaka-devnet-3 is live! Continue monitoring (and debugging issues as they arise) to progress towards mainnet.
- The following EIPs have been CFI’d for Glamsterdam to signal potential CL headliners

EIP-7732 (ePBS)
- EIP-7782 (Six second slots)
- EIP-7805 (FOCIL)

Outcome of next ACDE and the prior list will be used to make a final call on the CL headliner on the next ACDC on 7 August.
Community input: please add here [Soliciting stakeholder feedback on Glamsterdam headliners](https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885) if you’d like to signal support for or against one of the above headliner candidates.

**ACDC #161 Summary**

Fusaka

- fusaka-devnet-2

Running various test scenarios, some syncing issues in clients

fusaka-devnet-3

- Launched ~24 hours ago, will fork to Fusaka soon
- Looks good from initial assessement
- Working on MEV workflow implementation
- Implementing rate limiters on full nodes:

100 Mbps down / 50 Mbps up on 70% of full nodes
- 30% super nodes with potentially 1 Gbps limit (from 10 Gbps)
- Previous devnets had no rate limiting

Proposal for timelines

- August for hardening work
- Release candidates by end of August
- Target mainnet launch before DevConnect
- Process requires 30 days between testnet fork and mainnet date

Timeline considered ambitious but not impossible

Glamsterdam

- Series of updates to inform headliner conversation:

Shorter Slot Times Research Update

- Maria presented preliminary results on slot timings:

Metrics measured:

Block propagation (excluding timing games)
- Attestation arrival time (including block propagation, execution, validation)
- Pure attestation propagation for missed slots

Data shows:

- Block propagation 95th percentile under 1 second for well-connected nodes
- Full attestation processing 95th percentile of 95th percentile below 4.5 seconds
- Identified shift in distribution around 1.5s mark where last 10% take longer

Next research steps:

- Collect more data from other relays
- Analyze blobs and aggregates
- Investigate locally built blocks and small blocks
- Research late arrivals to understand contributing factors

Update on ePBS Free Option Problem

- Christoph and Bruno from Flashbots presented:

Problem: Winning builders can invalidate blocks if unhappy with market changes
- 8-second window gives builders option to fail to send blobs
- Option value increases with:

Market volatility
- On-chain liquidity
- Time window length

Potential solutions:

- Shorten free option window
- Implement slashing penalties
- “Block-listing” (not preferred as reduces permissionlessness)
- Separate blobs from transactions with independent fee market

Needs further analysis around mitigations and impact

Another ePBS update

- OPINION: The case against EIP-7732 for Glamsterdam
- Argues to focus on pipelining parts of EIP-7732 and not pursue MEV market changes

Community input

- Highlighted community input from Christine Kim

https://x.com/christine_dkim/status/1948042067566838249
- Support for some kind of pipelining, and also 6 second slots

Headliner selection

- Given that, we discussed how to proceed.
- Decided to CFI three EIPs with the understanding that we would select one as a  headliner:

EIP-7732 (ePBS)
- EIP-7782 (Six second slots)
- EIP-7805 (FOCIL)

This helps narrow scope for next ACDE so a headliner decison can be made there
Given this and results of next ACDE, a decision will be made for the CL headliner on the next ACDC
One important point of the discussion was how to best capture community input to help guide headliner selection. If you’d like to make a case for one of the above as headliner, please add it here: [Soliciting stakeholder feedback on Glamsterdam headliners](https://ethereum-magicians.org/t/soliciting-stakeholder-feedback-on-glamsterdam-headliners/24885)

Spec Question: SSZ Types for Pureth

- Etan requested adding additional SSZ types to consensus-specs repo as optional but help unblock prototyping for Pureth proposal
- https://github.com/ethereum/consensus-specs/pull/4445
- No objections from call participants, existing  precedents around other types like SSZ union
- Agreed to proceed with this PR; will work async there to get to a place for merging

