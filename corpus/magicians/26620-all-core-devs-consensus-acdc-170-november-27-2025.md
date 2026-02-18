---
source: magicians
topic_id: 26620
title: All Core Devs - Consensus (ACDC) #170, November 27, 2025
author: system
date: "2025-11-19"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-170-november-27-2025/26620
views: 118
likes: 3
posts_count: 4
---

# All Core Devs - Consensus (ACDC) #170, November 27, 2025

### Agenda

- Fusaka

updates from testnets, mainnet shadow forks?
- pm/Fusaka/fusaka-mainnet-plan.md at master · ethereum/pm · GitHub
- anything else?

Glamsterdam

- any devnet updates?
- call out for trustless payments discussion
- continue fork scoping

7805 (FOCIL)
- 7688 (Forward compatible consensus data structures)
- 8045 (Exclude slashed validators from proposing)
- 8061 (Increase exit and consolidation churn)
- 8062 (Add sweep withdrawal fee for 0x01 validators)
- 8071 (Prevent using consolidations as withdrawals)
- 8080 (Let exits use the consolidation queue)

Heka / Bogotá

- portmanteau: Boka?

**Meeting Time:** Thursday, November 27, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1812)

## Replies

**system** (2025-11-27):

### Meeting Summary:

The team reviewed progress on various forks, including successful shadow fork tests and bug fixes, while discussing plans for the Fusaka mainnet and incident response coordination. Multiple clients reported progress on ePBS implementations for Glamsterdam, with discussions around trustless payments and the inclusion of FOCIL in different forks. The team evaluated several EIPs related to consensus mechanisms and validator improvements, making decisions on their inclusion in various forks while acknowledging the need for further discussion on some proposals.

**Click to expand detailed summary**

The team discussed updates on the upcoming Fusaka fork, with Barnabas reporting successful shadow fork tests showing 100% participation. Dustin provided an update on the Nimbus client bug fix, which is expected soon. The team reviewed the Fusaka mainnet plan and discussed incident response coordination. For Glamsterdam, various clients reported progress on ePBS implementations, with some aiming for late December or early January for devnet testing. The team also touched on the topic of trustless payments in relation to EIP-7732, with Alex noting some community questions about its implications.

The team discussed the inclusion of FOCIL in the Glamsterdam fork and its potential commitment for the HECA fork. While some members advocated for SFI’ing FOCIL for HECA, others expressed concerns about making early commitments and the need to follow the headliner process. The group also debated the current EIP scoping process, with Barnabas suggesting a need to rethink how they decide which EIPs make it into which fork, particularly given plans for two forks per year. The team agreed to continue discussions on FOCIL’s inclusion and the overall EIP scoping process, with further decisions to be made asynchronously.

The team discussed the inclusion of Fossil in Glamsterdam and H-star, agreeing that CFI (Candidate For Inclusion) is the most appropriate path forward given the current process and timeline constraints. They determined that SFI (Softly For Inclusion) would dilute the meaning of the process, while CFI provides a clear path for Fossil to potentially be included in H-star, though not guaranteed. Ansgar emphasized that the core developers’ agreement to include Fossil in H-star is more important than finding the perfect process tool, as any changes to the inclusion would require significant justification.

The meeting focused on the inclusion of FOCIL in the Glamsterdam and HECA events. The group decided to proceed with DFI (Definitely For Inclusion) for Glamsterdam, while leaving the decision for HECA open. They agreed to move forward with the headliner process for HECA in a few months, with FOCIL as a priority. The team also discussed other CL EIPs for Glamsterdam and the need to start testing FOCIL soon.

The team discussed three EIPs related to staking mechanics. They agreed to CFI 8080, which fixes the consolidation queue issue, and to DFI 8071. The decision on whether to also implement 8061, which includes changes to the churn limits, was deferred to a future call. The team also discussed EIP 8062, which proposes a 5 BIPS withdrawal fee for OX01 validators during withdrawals. While some members expressed concerns about the timing and potential negative impact on solo stakers, others suggested waiting until after the Glamsterdam upgrade to consider such changes.

The meeting focused on discussions about validator consolidation and fast finality in Ethereum. Anders emphasized the need for a smaller validator set to improve finality, while Dima and others debated the feasibility of incentivizing consolidation without rewarding larger validators. The group agreed to defer a decision on custom ceilings for 0x02 validators, but Enrico and others expressed concerns about the impact of improved 0x02 features on fast finality. The conversation ended with a proposal to DFI EIP 8062, with the understanding that further work is needed to improve 0x02 and address the challenges of validator consolidation.

The meeting focused on discussing several EIPs related to Ethereum’s consensus and client implementations. The team decided to move forward with CFI (Consensus Finality Improvement) for Fossil and DFI (Distributed Finality Improvement) for Glamsterdam. They also discussed EIP 7688, which adds stable containers to the SSZ spec, and leaned towards including it but decided to take more time to assess its full complexity. The team agreed to revisit the decision on EIP 7688 in the next ACDE call. Additionally, there was some confusion and debate about whether to SFI (Soft Finality Improvement) or CFI Fossil for Heka, which was left unresolved and will be discussed further in the next ACDE meeting.

### Next Steps:

- Nimbus team: Release version 25.11.1 to fix the specific issue found during testing
- stokes: Update the EF blog post once Nimbus releases the new version
- All client teams: Make a PR to the Fusaka mainnet plan for coordinated incident response to specify who is responsible for what
- Stefan: Test block-level access lists in Kurtosis this week
- Alex: Organize the next ePBS breakout call on December 5th to discuss trustless payments and 7732 variants
- stokes: Make a PR to the Hecca Bogota meta-EIP for FOCIL  in the next week
- stokes: Reach out to Etan to ensure he attends the next ACDC call to make a stronger case for EIP-7688
- Client teams: Review and provide better sense of total complexity for EIP-7688 before next ACDC call
- Designated people : Vet that the proposer look-ahead works for EIP-8045, even when syncing from a branch
- stokes: Coordinate to ensure someone is assigned to verify the security concern for EIP-8045
- All teams: Decide between EIP-8061 and EIP-8080  by the next ACDC call in two weeks
- stokes: Take FOCIL SFI/CFI discussion to next week’s ACDE call to get EL input
- stokes: Leave a summary of decisions on Discord after this call
- All teams: Start thinking about a name for Hecca Bogota fork

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: S@cpa+3S)
- Download Chat (Passcode: S@cpa+3S)
- Download Audio (Passcode: S@cpa+3S)

---

**system** (2025-11-27):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=1IA-NZa4VZ8

---

**abcoathup** (2025-12-02):

## Summary

*Summary by [@ralexstokes](/u/ralexstokes) copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1445207488801669201)*

Summary of key decisions from last ACDC ([All Core Devs - Consensus (ACDC) #170, November 27, 2025 · Issue #1812 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1812)) to facilitate scoping decisions for Glamsterdam

- FOCIL

interest to schedule for Heka/Bogota, core devs undecided if we should write as CFI or SFI

CFI: follows established processes, not as strong a signal as SFI
- SFI: strong signal (reflecting community demand), but would be getting ahead of ourselves in terms of Heka/Bogota scoping as we have not started headliner selection for this fork yet
- will make final call on next ACDC

client teams, please come prepared with a team preference on how to scope FOCIL in Heka / Bogota

7688

- need to do due diligence on complexity; demand for feature exists for Glam, but could imply larger than expected implementation cost, along with more testing/review and potential audits
- will make final call on next ACDC

8045

- CFI, some questions around complexity raised but due diligence has been done here; possibility to not SFI if cost becomes higher than currently expected

8061

- see summary for 8080

8062

- DFI

8071

- DFI, in favor of 8080/8061

8080

- lean CFI, but want to better understand if we should do 8061 instead
- main thing here is deeper security review of changing weak subjectivity periods
- will make final call on 8080/8061 route on next call

draft PR to meta-eip here: [Update EIP-7773: update glamsterdam scope by ralexstokes · Pull Request #10861 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/10861)

