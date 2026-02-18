---
source: magicians
topic_id: 26515
title: All Core Devs - Execution (ACDE) #225, Dec 4, 2025
author: system
date: "2025-11-11"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-225-dec-4-2025/26515
views: 143
likes: 1
posts_count: 4
---

# All Core Devs - Execution (ACDE) #225, Dec 4, 2025

### Agenda

- Fusaka

incidents following the fork
- current status

Housekeeping (urgent)

- ACD timings

ACDC Dec 25: canceled
- ACDE Jan 01: keep?

[FOCIL: status for Heka / Bogota?](https://github.com/ethereum/pm/issues/1808#issuecomment-3599524331)

Glamsterdam

- CFI / DFI candidate EIPs
- Open Questions

Repricing: Core / Gas

unbundle / regroup?

Repricing: Core / State Growth

- which approach?
- writeup by @anderselowsson

Contracts / Size

- which approach?

Utility / Transaction & Block Features

- EIP-7745 updates

Cryptography / PQ Precompiles

- Glamsterdam the right time?

Other / Process

- what to do with EIPs that don’t change protocol?

Housekeeping (not urgent)

- H-Star name
- minimum hard fork testnets & mainnet rollout timeline

**Meeting Time:** Thursday, December 04, 2025 at 14:00 UTC (90 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1808)

## Replies

**system** (2025-12-04):

### Meeting Summary:

The meeting covered updates on Ethereum fork developments, including bug fixes and meeting schedule changes, followed by a detailed discussion of EIP selection processes and decisions for both Heka and Glamsterdam forks. The team made various implementation decisions for multiple EIPs, with some being assigned to CFI (Candidate For Implementation) while others were DFI (Deferred For Implementation) or postponed for further review. The conversation ended with discussions about Glamsterdam scope and cryptography-related EIPs, including decisions to DFI certain proposals and plans for future review of non-protocol-changing EIPs.

**Click to expand detailed summary**

The meeting focused on two main issues: a review of the Ethereum fork (Fusaka) and scoping for Glamsterdam. Terence provided an update on a Prysm-related bug that affected attestation participation, which has been resolved temporarily with a feature flag and a long-term fix in development. The team discussed the cancellation of AllCoreDevs meetings on December 25th and January 1st due to holidays, with a decision to cancel January 1st and explore potential replacements. Nicolas inquired about safe RPC issues on OP chains, which Ansgar confirmed were being addressed.

The meeting focused on the process for selecting EIPs (Enhanced Identity Proposals) for the Heka fork, with discussions centered around whether to use the standard headliner process or special treatment for specific proposals like FOCIL. Participants agreed that while there was strong community support for FOCIL, it should go through the regular headliner process to ensure fairness and maintain consistency with established procedures. The group also discussed the need to update documentation, including EIP-1, to reflect the new headliner process and ensure clarity for new contributors. Additionally, there was a brief discussion about PQ precompiles and the importance of having a viable emergency solution in place.

The team discussed several EIPs for potential CFI (Community Funded Implementation) or DFI (Developer Funded Implementation) decisions. They agreed to make a CFI decision for EIP-7778 (block gas limit accounting without refunds) as it had universal support. For EIP-7971 (hard limit for transient storage), they decided to postpone the decision due to unresolved concerns about abstraction compatibility. The team also discussed EIP-8011 (multidimensional gas metering), which was DFI’d due to concerns about complexity, and EIP-8032 (size-based storage gas pricing), which was postponed due to migration concerns. Barnabas suggested DFI’ing all questionable EIPs, but the team agreed to be selective and postpone decisions on some EIPs for further review.

The team discussed several EIPs and made decisions on their fate. They agreed to revisit two EIPs in two weeks due to concerns about the transition process. For EIPs 8053 and 1859, they decided to default to DFI as there was no strong opposition. EIP 8057, which had strong client support, was also assigned to DFI. In the contract section, they decided to postpone making a CFI decision on EIP 7903, which removes the init code size limit, due to concerns about its impact. They also discussed the potential contradiction between EIP 7903 and EIP 7907, which increases the contract size limit. In the utility section, they noted strong support for EIP 7668, which removes bloom filters, but decided to wait for more active support before making a CFI decision.

The team discussed several EIPs, making decisions to CFI (Candidate For Implementation) EIP-7708 for ETH transfer logs and EIP-7791 for gas to ETH, while DFI (Deferred For Implementation) EIP-7819 for set delegate and EIP-7843 for slot-num opcode. The team also considered EIP-7797 for call and return opcodes, with Łukasz arguing it could enable easier bytecode translation to different architectures like RISC-V, though the decision was left pending further discussion. The conversation ended with agreement to make clear individual EIP decisions rather than deferring them, as this would help with the overall process.

The meeting discussed several EIPs and their potential inclusion in the Glamsterdam scope. Greg Colvin expressed frustration with ongoing delays and advocated for immediate consideration of EIP-7979, which was agreed upon. A breakout room was proposed to continue discussions on EIP-7979, with Protocol Support offering to facilitate. The team also decided to DFI EIP-7619 (Falcon) for Glamsterdam, while postponing decisions on other cryptography-related EIPs. Concerns were raised about the complexity and prioritization of certain EIPs, but no major opposition was voiced against DFIing them.

The meeting focused on reviewing and deciding the status of various Ethereum Improvement Proposals (EIPs) for the upcoming hard fork, Glamsterdam. The group decided to DFI (Delay Forever Indefinitely) several EIPs, including 7932 and 8030, due to lack of priority and alignment with the post-quantum strategy. They also CFI (Client Frozen Indefinite) several EIPs, such as the sparse blob pool proposal, conditional on further review by the CL side. The team discussed the handling of non-protocol-changing EIPs and agreed to revisit these decisions in two weeks. Open questions remain on repricing, contract size increase, and cryptography post-quantum precompiles, which will be addressed in future discussions. The conversation ended with a reminder to decide on the H-star name and clarify minimum hard fork testnet and mainnet rollout timelines.

### Next Steps:

- Prysm team : Release formal post-mortem for the Prysm attestation issue by next week
- Prysm team : Release long-term fix for the Prysm issue by next week
- Ansgar: Look into potential replacement candidates for the cancelled January 1st ACDE call and make decisions on ACDE in two weeks
- ACDC participants: Make decision on FOCIL special treatment process  on next ACDC call
- EIP7971 champion: Address account abstraction concerns regarding hard limit for transient storage before next call
- EIP8032 champion: Address migration complexity concerns for size-based storage gas pricing before next call
- Protocol support : Facilitate breakout room for EIP7979  to keep conversation going
- Ansgar and repricing champions: Prepare proposal to regroup core gas repricing bundle in more palatable form by next ACDE
- All participants: Review Anders’ write-up comparing different state growth approaches before next call
- All participants: Review Zolt’s updates on EIP7745 before next call
- All participants: Review H-star name decision link in agenda and provide input
- Ansgar: Coordinate with people before next call to ensure good basis for decisions on open questions
- Ansgar: Update EIP1 and main EIP page to reflect new headliner process
- ACDC participants: Double-check Engine API concerns for sparse blob pool  on next ACDC call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: BE3?KK4&)
- Download Chat (Passcode: BE3?KK4&)
- Download Audio (Passcode: BE3?KK4&)

---

**system** (2025-12-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=2KU93ZHf-ww

---

**yashkamalchaturvedi** (2025-12-05):

![image](https://etherworld.co/content/images/size/w256h256/2023/03/new-logo--3--2.png)

      [EtherWorld.co – 4 Dec 25](https://etherworld.co/2025/12/04/highlights-from-the-all-core-developers-execution-acde-call-225/)



    ![image](https://etherworld.co/content/images/2025/12/EW-Thumbnails-1.png)

###



A comprehensive breakdown of ACDE #225 detailing Fusaka incident analysis, Glamsterdam scoping decisions, FOCIL process debates, and the roadmap toward the Heka upgrade.

