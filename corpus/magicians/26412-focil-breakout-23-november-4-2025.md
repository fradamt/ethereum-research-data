---
source: magicians
topic_id: 26412
title: FOCIL Breakout #23, November 4, 2025
author: system
date: "2025-11-04"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/focil-breakout-23-november-4-2025/26412
views: 54
likes: 0
posts_count: 5
---

# FOCIL Breakout #23, November 4, 2025

### Agenda

- Development updates
- FOCIL in Glamsterdam

**Meeting Time:** Tuesday, November 04, 2025 at 14:00 UTC (60 minutes)

[GitHub Issue](https://github.com/ethereum/pm/issues/1793)

## Replies

**system** (2025-11-04):

### Meeting Summary:

The team reviewed development progress across multiple projects including spec testing, ePBS implementation, and metrics implementation, with various team members reporting on their respective work streams. The discussion then focused on prioritizing EIPs for Glamsterdam, with particular attention to Fossil and ePBS implementation timelines, including debates about potential delays and testing challenges. The conversation ended with discussions about the compatibility and implementation of ePBS with shorter slots and FOCIL, exploring various approaches to censorship resistance and testing methodologies.

**Click to expand detailed summary**

The team discussed development updates, including Jihoon’s work on a spec PR rebasing fossil onto CLAIS, Pelle’s progress on spec testing moved from EST to ELS with 9 test cases passing, and both Lodestar and Teku’s focus on ePBS implementation. They also touched on an Eragon PR implementing Fossil by Fahil, which Pelle is helping with interop testing. The team noted that Katya is away but has made progress on metrics implementation for Reth, with some naming conventions still to be addressed. Finally, they agreed to use the breakout session to share thoughts on fossil in GLAM, though no definitive conclusions were reached.

The team discussed the prioritization of EIPs for Glamsterdam, with a consensus to support Fossil as the next EIP to be SFI’d, pending a working implementation of ePBS. Mehdi emphasized that ePBS should be the headline EIP, but if it introduces significant complexity, they might reconsider. Soispoke raised concerns about delaying ePBS with Fossil, suggesting that any delay should be clearly defined and not exceed a reasonable timeframe. Jihoon proposed a 3-month delay as a potential threshold for acceptable delays. The Nethermind team expressed support for Fossil but noted the need to balance it with potential delays to ePBS.

The team discussed the inclusion of the Fossil EIP in the upcoming hard fork, with opinions split between shipping it immediately and delaying it for important features. Justin from the BASE team emphasized that Fossil and gas-pricing EIPs are different in complexity and implementation, and he would prioritize Fossil over gas repricing. Marc noted potential interactions between block access lists and gas pricing in testing efforts, while Jihoon and others debated the feasibility of overlapping testing surfaces. Potas highlighted the urgency of including Fossil in the protocol and acknowledged the non-trivial interactions with ePBS and future slot time changes. The team acknowledged the uncertainty in testing and implementation timelines, agreeing that Fossil’s implementation is still in the early stages, and client teams are already working on it regardless of the final decision on inclusion.

The meeting focused on discussing the compatibility and implementation of ePBS (efficient proposer building system) with shorter slots and FOCIL (Foo’s censorship resistance mechanism). Participants debated the potential challenges and trade-offs of integrating these systems, including concerns about freshness of inclusion lists and attestation propagation. Mehdi emphasized that FOCIL meets the criteria for SFI (soft fork implementation) status and argued against further delays, while Potuz proposed implementing certain FOCIL components in EL (Execution Layer) clients even if FOCIL itself is not accepted. The group also discussed alternative approaches to censorship resistance, including a default mechanism for blacklisting builders identified as censoring transactions.

### Next Steps:

- Jihoon: Review the spec PR that rebases fossil onto cloas
- Pelle: Clean up the 9 test cases and add them to the PR
- Pelle: Work with Fahil to get Eregon implementation into interop testing
- Pelle and Reth team: Try interop testing between Reth and Eragon
- Jihoon: Work on the spec PR
- Pelle and Katya: Finalize EL metrics list and Reth implementation, addressing naming conventions
- Teku team : Share final thoughts on fossil inclusion before the next ACDC call
- All CL teams: Provide feedback on fossil inclusion decision for the ACDC call on November 13th
- potuz: Consider writing an EIP for the censorship detection component in the Engine API
- Jihoon: Share summary of the call

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: oV#KY4bf)
- Download Chat (Passcode: oV#KY4bf)

---

**system** (2025-11-04):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=aT3icQlOtbQ

---

**jihoonsong** (2025-11-11):

To FOCIL or not to FOCIL, that’s the question.

### FOCIL in Glamsterdam

#### FOCIL landscape

- Teku is fine with SFI’ing FOCIL. As soon as Teku has a working ePBS implementation, they could further voice this opinion.
- Lodestar published a blog post when choosing the headliner for Glamsterdam and supported both ePBS and FOCIL. Since there are many proposed EIPs for Glamsterdam, Lodestar needs to review them to see if their opinion has changed. It’s not expected to have changed much though.
- Nethermind supports FOCIL for Glamsterdam.
- Most opinions at the EF are to ship FOCIL for the H* fork. One of the reasons is to ship forks on a regular cadence, which is not a technical one. We should decide based on technical reasons, not political ones.
- The community has strongly signaled preferences for FOCIL inclusion. Some people are against it because it touches both layers, delays the fork, etc. However, the same argument applies to the H* fork as well. The later we try to ship it, the more difficult it will become.

#### FOCIL and gas repricings

- Gas repricings and FOCIL are not very comparable. They provide very different things and are difficult in different ways.
- Gas repricings consist of many EIPs, and there are many different ways to group them. As these groups interact with each other in hard-to-reason-about manners, they create scheduling and testing burdens. Gas repricings were advocated for Glamsterdam as it is a scaling hard fork, but scaling has had developers’ attention for the past three years.
- Gas repricings and ePBS are orthogonal. In other words, having gas repricings before or after ePBS won’t matter much.
- Gas repricings and BALs have overlapping testing efforts that could add some complexity. For example, in BALs construction, creating a list of state accesses is intertwined with gas repricings.

#### The added complexity by FOCIL

- The added complexity by FOCIL should not be underestimated. Even the ePBS spec is not finalized yet, and both ePBS and FOCIL set deadlines within a slot, which should be run in testnets to make sure that they work in a decentralized manner.

#### People have been working on FOCIL and will be

- Client teams are already working on FOCIL and will continue working on it regardless of delay. There were more people implementing FOCIL than ePBS just a few weeks ago. FOCIL will be implemented on top of ePBS anyway.
- Originally, a working implementation was required to be SFI’d. FOCIL meets this requirement more than any other EIP proposed for Glamsterdam.

### Implementation Updates

- A PR rebasing FOCIL onto Gloas has re-opened.
- Lodestar has no update. Mostly focused on ePBS.
- Teku has no update. Mostly focused on ePBS.
- Reth has worked on the spec tests. Currently, 9 test cases are passing.
- Erigon has just finished the initial implementation and will work on interop with other EL clients.

### Metrics

- Lodestar has already implemented the beacon metrics, and both the execution metrics and Reth’s implementation are nearly complete.

### Links

- A PR rebasing FOCIL onto Gloas

---

**jihoonsong** (2025-11-11):

### Recording

- YouTube
- X Stream

### Summary

- X Thread
- Full Summary

