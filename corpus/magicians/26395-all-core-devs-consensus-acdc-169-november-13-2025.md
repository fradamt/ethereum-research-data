---
source: magicians
topic_id: 26395
title: All Core Devs - Consensus (ACDC) #169, November 13, 2025
author: system
date: "2025-11-03"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-169-november-13-2025/26395
views: 118
likes: 1
posts_count: 4
---

# All Core Devs - Consensus (ACDC) #169, November 13, 2025

### Agenda

- Fusaka

hoodi bpo2 update, any other updates on testnets
- how to describe BPOs with (meta)EIPs, link

Glamsterdam

- updates on ePBS spec/devnets
- non-headliner EIP selection

7805 (FOCIL)
- 7688 (Forward compatible consensus data structures)
- 8045 (Exclude slashed validators from proposing)
- 8061 (Increase exit and consolidation churn)
- 8062 (Add sweep withdrawal fee for 0x01 validators)
- 8068 (Neutral effective balance design)
- 8071 (Prevent using consolidations as withdrawals)

**Meeting Time:** Thursday, November 13, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1790)

## Replies

**abcoathup** (2025-11-03):

### Summary

*[link to [@ralexstokes](/u/ralexstokes) summary]*

### Recordings/Stream

- Protocol Calls - Forkcast
- Live stream on X: [x.com/ECHInstitute]

### Writeups

- by @Christine_dkim [christinedkim.substack.com]
- by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade (December 3):

Upgrade dates: mainnet December 3, BPO1 December 9, BPO2 January 7 2026
- Testnet upgrades;  Holešky Oct 1,  Sepolia Oct 14,   Hoodi Oct 28;
- Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam) (2026):

- Headliners: consensus layer: EIP7732 ePBS & execution layer: EIP7928 Block-level Access Lists
- Non-headliners proposed for inclusion
- Mascot needed for Glamsterdam upgrade

---

**system** (2025-11-13):

### Meeting Summary:

The meeting focused on updates and discussions related to the Fusaka and Glamsterdam projects, including successful deployments, documentation methods, and implementation progress. The team discussed plans for a devnet release in mid-December, with a focus on interop testing and bug fixes, while also addressing various Ethereum Improvement Proposals (EIPs) and their potential inclusion in the Glamsterdam fork. The group explored the prioritization and implementation of FOCIL and ePBS in the HECA fork, discussing concerns about delays, credible commitments, and the need for further contemplation on how to balance technical and social considerations.

**Click to expand detailed summary**

The meeting focused on updates and discussions related to the Fusaka and Glamsterdam projects. The team reviewed the successful deployment of BPO2 on Hoodie, noting no significant issues, and discussed high blob fees, which were confirmed to be functioning as intended. A key topic was the need to establish a clear documentation and specification method for BPOs, with a consensus forming around using an “InterFork meta-EIP” approach. The team also touched on the progress of Glamsterdam, including the need to finalize the scope and select non-headliner EIPs for the fork, while noting that EVBS is already confirmed as a headliner. Implementation progress for Glamsterdam was noted as early-stage, with no DevNet Zero yet available.

The team discussed plans for a devnet, aiming for a target release in mid-December, with a focus on interop testing and bug fixes. Potuz reported progress on client implementations, noting that Teku is closest to being compatible with Kurtosis, while EngineAPI changes may be postponed for a later devnet. Ryan argued for keeping Glamsterdam scoped down to ship ePBS quickly, as he sees the L1+L2 model as being on the cusp of public acceptance. The team agreed to discuss other EIPs after addressing the FOCIL proposal, which was deemed contentious and potentially time-consuming.

The meeting focused on discussing various EIPs and their potential inclusion in the Glamsterdam fork. Several client teams, including Lighthouse, Lodestar, Nimbus, and Teku, provided their views on EIPs such as 7688, 8045, 8061, 8071, and FOCIL. There was general support for FOCIL, though with some concerns about implementation complexity and timeline impacts. The teams debated the merits of different approaches to handling consolidations and exits. The discussion highlighted the need to balance adding new features with maintaining the project’s timeline and scope. Sophia raised a key question about the credibility of committing to scheduling FOCIL for the H fork, prompting further discussion on how to proceed.

The group discussed the inclusion of FOCIL in the H-star fork, with mixed opinions on whether to prioritize fork cadence or feature implementation. Barnabé highlighted the cost of delaying the fork and the risk of explosive complexity, while others argued for the importance of FOCIL as a feature. The team debated the feasibility of making long-term commitments for multiple forks, with some suggesting a more predictable cadence. Vitalik emphasized the need to balance technical and social considerations, advocating for commitments that align with Ethereum’s goals while remaining flexible. The discussion concluded with a call for further thought on how to balance these competing priorities.

The team discussed the timeline and commitment for implementing FOCIL and ePBS in the HECA fork. Sophia expressed concerns about delays in FOCIL and its impact on the scaling roadmap, advocating for a mid-2027 timeline. The group agreed on the importance of credible commitments and discussed potential methods to ensure these, including SFI and CFI processes. Nixo suggested taking a week or two to consider how to credibly commit to these changes, with Lodestar emphasizing the need for a clear commitment to build organizational capacity for faster, smaller releases.

The meeting focused on the prioritization and implementation of FOCIL for the H4k fork, with concerns raised about the compatibility of 6-second slots and the need for a credible commitment to CFI. Participants agreed that FOCIL should be given higher priority, but there was a consensus that a decision on FOCIL should not be rushed, and further discussion was needed to ensure a fair and well-considered process. It was decided to explore options for integrating FOCIL into the HECA fork and to revisit the decision in the next ACDC meeting, allowing time for further contemplation and alignment. The conversation ended with a plan to address other EIPs and continue discussions on fork planning.

The meeting focused on discussing several Ethereum Improvement Proposals (EIPs) related to staking and protocol mechanics. The team decided to move forward with EIP-8068, which addresses effective balance calculations, while deferring a decision on EIP-8062. For EIP-8061 and 8071, which aim to fix issues with churn limits and consolidations, the group agreed to further evaluate the options, particularly the simpler churn-sharing mechanism proposed by Francesco as an alternative to 8071. The team also discussed EIP-8045, which would exclude slashed validators from the proposer sequence, with Potuz raising concerns about potential implementation challenges. Finally, regarding EIP-7688, which adds stable containers for generalized indices, the group acknowledged its importance for some teams but expressed mixed support, deciding to revisit the decision in the next meeting.

### Next Steps:

- kev : Check the config to confirm if blob spamming at higher limits has started on Hoodie testnet
- stokes: Reach out to POTUS after the call regarding the attestation issue
- Client teams : Aim for a devnet  around mid-December
- POTUS: Discuss Engine API changes with EL Devs, probably at ACDT
- stokes: Grab some time on next week’s ACD  to discuss proposals for credible commitment to FOCIL, if there are 5 minutes available
- stokes: Reach out to 6-second-slot EIP authors to prepare for potential discussion about H-star headliners
- stokes: Propose options for how to credibly commit to FOCIL in H-star fork before the next ACDC
- Francesco: Consider splitting the churn-sharing mechanism from EIP-8061 into a separate EIP as an alternative to EIP-8071
- Client teams : Refine their positions on CL EIPs for Glamsterdam scope based on today’s discussion, to be finalized at the next ACDC in 2 weeks
- All participants: Make final CFI/DFI decisions on CL EIPs at the next ACDC call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: C$u5+1+W)
- Download Chat (Passcode: C$u5+1+W)
- Download Audio (Passcode: C$u5+1+W)

---

**system** (2025-11-13):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=W-uqWQskV9o

