---
source: magicians
topic_id: 24919
title: All Core Devs - Consensus (ACDC) #162, August 07 2025
author: system
date: "2025-07-25"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-162-august-07-2025/24919
views: 293
likes: 3
posts_count: 6
---

# All Core Devs - Consensus (ACDC) #162, August 07 2025

# All Core Devs - Consensus (ACDC) #162, August 07, 2025

- Aug 07, 2025, 14:00 UTC

# Agenda

- Fusaka
- Glamsterdam
-

Other comments and resources

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

[GitHub Issue](https://github.com/ethereum/pm/issues/1638)

**YouTube Stream Links:**

- Stream 1 (Aug 07, 2025): https://youtube.com/watch?v=RU4DgyH662c

## Replies

**abcoathup** (2025-07-29):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #162, August 07 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-162-august-07-2025/24919/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #162 Action Items
>
> fusaka-devnet-4  is live! Focus on performance to identify any places to harden PeerDAS.
> Active discussions are under way to find the right Fusaka timelines. Expect updates here soon. There is general agreement to proceed with Holesky in September.
> Focus all effort on preparation for Fusaka releases — the main blocker right now seems to be merging in feature branches.
> EIP-7732 (ePBS) has been selected as the Glamsterdam headliner and moved to SFI.
>
> ACDC #162 Summary
> Fus…

### Recordings/Stream

- https://www.youtube.com/live/RU4DgyH662c?t=242s
- Eth Cat Herders:

Live stream on X: [x.com/ECHInstitute]

### Writeups

- Tweet thread by @poojaranjan
- by @Christine_dkim [christinedkim.substack.com]
- Highlights from the All Core Developers Consensus (ACDC) Call #162 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade:

Current devnet: fusaka-devnet-3 [specs]

[Glamsterdam upgrade](https://forkcast.org/upgrade/glamsterdam):

- Stakeholder feedback summary
- Headliners selected:

Execution layer: EIP-7928 Block-level Access Lists
- Consensus layer: EIP7732 ePBS

FOCIL: [presentation](https://docs.google.com/presentation/d/1KmRsdpDNQpxOlWF0ThqZNRTBDWMV8RuCNLsMjDf9XRo/edit) + [How to Implement FOCIL in the CL - HackMD](https://hackmd.io/@jihoonsong/rJX-fxADxl) + [How to Implement FOCIL in the EL - HackMD](https://hackmd.io/@jihoonsong/BJpcaudvex)
[Slot timings - short update](https://docs.google.com/presentation/d/1QNlJbwDirIFI1V9eKwZXciYtEKFnHRiwVJzo_gWZz3g/edit)

---

**poojaranjan** (2025-08-07):

Tweet thread - https://x.com/poojaranjan19/status/1953456098188627974

---

**ralexstokes** (2025-08-09):

**ACDC #162 Action Items**

- fusaka-devnet-4  is live! Focus on performance to identify any places to harden PeerDAS.
- Active discussions are under way to find the right Fusaka timelines. Expect updates here soon. There is general agreement to proceed with Holesky in September.
- Focus all effort on preparation for Fusaka releases — the main blocker right now seems to be merging in feature branches.
- EIP-7732 (ePBS) has been selected as the Glamsterdam headliner and moved to SFI.

**ACDC #162 Summary**

Fusaka

- fusaka-devnet-3 showing excellent participation with successful testing

Non-finality test with 40% network offline - network healed in under one epoch
- Current test: most super nodes offline with submitted exits for self-healing validation

`fusaka-devnet-4` launching tomorrow to simulate mainnet-like scale

- ~10% of mainnet size
- Testing blob scaling from 8 to 48-72 blobs
- One day data collection per step to inform PeerDAS scaling limits

BPO Schedule Discussion

- https://notes.ethereum.org/@jtraglia/fusaka_scheduling
- Proposed 3 BPOs for a gradual rollout along with Fusaka launch

BPO 1: December 15, 2025
- BPO 2: January 14, 2026
- BPO 3: February 10, 2026
- Target: 21 blobs with 32 blob limit after phase 1

Alternative compressed timeline suggested

- November 24 → December 15 → January 14
- Following the same trajectory gets to 8x scaling by March 2026

`fusaka-devnet-4` testing will validate actual target/max numbers
Point made that realistic spacing is 4 weeks for observation and reaction periods, 3 weeks is doable but tight
Agreement: ship fork with data informed by `fusaka-devnet-4` to parameters we know are safe to lock in; will adjust via subsequent BPOs pending mainnet analysis

Timeline Concerns from Client Teams

- Lodestar, Prysm, and Nimbus requesting 4-week delay with the following concerns:

Major concern: code not on master branches yet
- Lots of code across three clients that needs trunk integration
- No devnets with spec-frozen code on production branches

Specific technical gaps also identified

- Limited private mempool testing without GetBlobs v2
- Testing for “perfect PeerDAS” configuration and backfill implementations

Technical concerns were addressed on the call

- GetBlobs v2 has in fact been tested with no issues, miscommunication there
- Acknowledgement of “perfect PeerDAS” and backfill but these are client specific and we are working to mitigate the concerns; these features round out a client against specific edge cases but given implementations in some clients not having them in all clients is not a strict blocker

To move forward, we agreed to schedule Holesky in September without requirement for a formal release from clients (we have precedent for this with Holesky already).
I’m discussing timelines with clients to find a solution that strikes the right tradeoff between speed and security. Will update on further ACDs.

Beacon API Updates

- PR for consumers of blobs from beacon APIs

Add getBlobs endpoint by nflaig · Pull Request #546 · ethereum/beacon-APIs · GitHub
- Can simplify API to focus on what consumers likely want (just the blobs, instead of other metadata)
- Call for L2 teams to provide input on the PR

Glamsterdam Fork Planning

- Touched on a PR to refactor slot timings in the specs which will facilitate upcoming EIPs

Replace INTERVALS_PER_SLOT with explicit slot component times by jtraglia · Pull Request #4476 · ethereum/consensus-specs · GitHub
- Agreement to merge soon, please direct feedback to the PR

Quick presentation on FOCIL complexity to inform headliner selection

- See links to slides here or watch recording: All Core Devs - Consensus (ACDC) #162, August 07 2025 · Issue #1638 · ethereum/pm · GitHub

Update on 6-second slots data improvements

- See slides here or watch recording: Slot timings - short update - Google Präsentationen

Community stakeholder feedback summary from variety of groups to inform headliner selection

- Notion
- Strong support for ePBS
- FOCIL support but concerns about blob coverage gaps
- 6-second slots support but viewed as under-researched

Given the above, we decided to select EIP-7732 (ePBS) as the Glamsterdam headliner, and leave FOCIL as CFI’d.

- In order to derisk overscoping the fork, we agreed work should focus on ePBS and only upon stabilization in devnets will we revisit FOCIL inclusion

Glamsterdam Implementation Timelines

- To close the call, we discussed potential timelines for Glamsterdam given ePBS as the headliner, along with the interplay with other EIPs including FOCIL

estimates on the CL side for ePBS converged around March/April ’26 for the bulk of implementation work (not mainnet!), with FOCIL adding 1-2 months to those timelines

Consensus anchored on a phased approach: stabilize SFI EIPs first, then consider CFI EIPs

edit: updated comment on Glamsterdam timelines to clarify this was not a date for mainnet

---

**system** (2025-08-21):

### Meeting Summary:

The team reviewed and approved a VPO schedule for the Fusaka upgrade, with discussions around shipping timelines and testing requirements. Concerns were raised about the aggressive timeline for the September 1st release, leading to a proposal for extending the timeline to the end of September to allow for additional testing and code stabilization. The team also discussed various feature implementations including Fossil and EPBS, with decisions made on shipping timelines and integration approaches while considering community feedback and technical requirements.

**Click to expand detailed summary**

The team discussed the VPO schedule for the Fusaka upgrade, with Justin presenting a proposal for three BPO forks approximately one month apart, targeting 21 BPOs with a limit of 32 BPOs per block. They agreed to move the dates forward slightly, with BPO 1 on November 24, BPO 2 on December 15, and BPO 3 on January 14, 2026. The team decided to proceed with shipping the VPOs even if the throughput numbers are lower than expected, as it would provide valuable data on scaling capabilities. They also briefly touched on testing updates for node synchronization and custody backfill features.

Matthew expressed concerns on behalf of Prism and Nimbus teams about the aggressive timeline for the September 1st release, highlighting the need for more testing and the fact that the code is not yet on the master branch. He emphasized the importance of having a stable devnet with no spec changes and all code on the trunk branch, as well as private mempool testing and exercising code paths on the trunk branch. The teams are advocating for an additional 4 weeks to the timeline, aiming for the end of September, to ensure a successful rollout.

The team discussed testing clients without the help of Cablock v2, noting that Devnet became stable after its introduction. They observed that private main pool testing was limited due to non-finality testing and circuit breaker triggers. Matthew expressed concern about unmerged code paths and the need for early and aggressive merging of feature branch changes, emphasizing the importance of avoiding issues that caused problems in previous testnets. Dustin added that achieving stability was challenging due to rapid changes in Defnet 1 and Defnet 2.

The team discussed the timing of merging code for the Mainnet release, with Matthew proposing a 4-week delay to the end of September to allow for additional testing and a devnet on trunk branches. Dustin and Manu agreed that more time would be beneficial for code stability, with Manu emphasizing the need for a final devnet on trunk branches before the Mainnet release. The team considered the possibility of conducting the Mainnet rollout at Dev Connect, though concerns were raised about attendance and the potential for issues during the rollout.

The team discussed the timing and implementation of the Holoski release, with Barnabas confirming a 2-month lead time and emphasizing that Mainnet is still planned for November. Matthew raised concerns about the need for non-finality testing and backfill functionality, suggesting that while trunk branch alignment is important, it might not be critical for a devnet. The team agreed to target Holoski for September, with Stokes proposing to focus on getting code onto trunk branches as a next step, while NFLaig presented a PR regarding beacon node API implementation and filtering options for consumers.

The team discussed the status of roll calls, which have been temporarily paused, and reviewed a PR related to slot and spec structure that deprecates the intervals per slot variable and defines explicit durations for deadlines as a percentage of total slot duration. Justin Traglia explained that merging this PR soon would allow work on Glancer down specs to proceed, as it’s needed for EIPs 778 and 782. The team agreed to merge the PR sooner than after Fusaka, despite Carl’s suggestion to wait 2 weeks, with Mark expressing concern about the costs of further delays.

Nixo presented a summary of stakeholder feedback on various EIPs, highlighting concerns about slot pipelining and the need for adequate notice for engineering costs. The feedback showed strong support for EIP-805 (Fossil) in conjunction with other options, with EIP-732 receiving the most support as a primary option. Jihoon then provided an update on Fossil, explaining its complexity for both CL and EL and demonstrating how it can be implemented and rebased on top of PBS.

Jihoon explained the implementation of Inclusion List (IL) transactions in a blockchain system, detailing how testers and builders handle IL transactions, and how validators and CL (Consensus Layer) enforce IL compliance. He described the process of validating IL transactions, checking gas availability, and handling equivocation. Justin Florentine asked about the implications of missing transactions and gas costs, to which Jihoon clarified that they check if transactions could have been appended to the payload based on gas availability and affordability.

The team reviewed performance metrics for block propagation and attestation times, with Maria reporting improvements due to a table correction and a fixed validator configuration at Klaytn. The 95th percentile block propagation time was reduced to 865ms, and the 95th percentile attestation time for missed slots improved from 2.5 seconds to 1.8 seconds. The team then confirmed PPS as the leading candidate for the Amsterdam headliner, with SFI and El selected as CEO and EL headliners respectively, which will unlock the first step of Glen scoping.

The team discussed the status and implementation of the Fossil and EPBS features, with broad community support for including Fossil despite its demotion from headliner status. Terence, who implemented both features, suggested that combining EPBS and Fossil in the initial fork would not be problematic, as their interactions are mostly orthogonal. Ansgar emphasized the importance of not delaying the Glamsterdam fork, proposing that CL headliners should not hold up the fork, even if CL headliners are not ready. The team agreed to proceed with implementing both features while continuing to evaluate their integration and potential impact on the fork timeline.

The team discussed the timeline for shipping features, with Terence suggesting early next year for SFI and potentially March or April, while Ansgar raised concerns about the EPBS implementation timeline. They decided to SFI EPBS 7.7.3.2 and CFI Fossil, with Justin explaining this would involve renaming the feature spec and rebasing 7.8.0.5. Ansgar expressed concerns about the EPBS readiness, but the team agreed to focus on Fossil for now and keep the option open to decouple the features later if needed.

### Next Steps:

- Client teams: Continue working on merging Fusaka code to trunk branches.
- Client teams: Prepare for a potential 4-week delay in the Fusaka release timeline.
- Parithosh and testing teams: Continue running devnets and testing, including private mempool testing, until mainnet release.
- Client teams: Prepare for a potential Holesky testnet deployment in September using feature branches if trunk branches are not ready.
- Client teams: Aim for a devnet with all code on trunk branches before mainnet release.
- Justin Traglia: Refine the BPO schedule based on feedback and testing results.
- PandOps: Conduct experiments to validate BPO numbers and inform the schedule.
- Client teams: Prepare for potential interop testing at Devconnect.
- stokes: Reach out to Layer 2 teams for feedback on the beacon API PR for exposing blobs.
- All participants: Review and provide feedback on Justin Traglia’s PR for restructuring slot intervals in the consensus specs.
- Client teams: Target Holesky testnet launch for September.
- stokes and core devs: Continue discussions with client teams on Fusaka timeline and potential adjustments.
- Client teams: Prioritize additional testing and hardening of Fusaka code in the coming weeks.
- DevOps team: Plan for a devnet with all code on trunk branches after client releases are done in September.
- Client teams: Focus on getting Cancun/Deneb code onto trunk branches by September 1st.
- Carl: Ask in the L2 chat for feedback on the beacon API PR for exposing blobs to consumers.
- Core devs: Review the community feedback synthesis provided by Nixo on EIPs for Cancun/Deneb.
- Core devs: Make a decision on the Cancun/Deneb headliner EIP based on updates and community feedback.
- Core developers: Make a decision on including Fossil in Amsterdam fork alongside PBS.
- Client teams: Continue work on implementing and testing PBS as the primary headliner for Amsterdam.
- Development teams: Continue empirical analysis and optimizations for 6-second slots proposal.
- Core developers: Schedule future discussions on non-headliner EIPs for Amsterdam fork.
- Development teams: Continue work on integrating Fossil with PBS and assess implementation complexity.
- Core developers: Clarify the status and prioritization of Fossil in relation to PBS for the Amsterdam fork timeline.
- Justin Traglia: Rename EIP-7732 feature spec to Glamsterdam spec.
- Justin Traglia: Rebase EIP-7805 off of the Glamsterdam spec.
- Ethereum developers: Focus on finalizing Cancun before prioritizing work on Glamsterdam.
- Ethereum developers: Proceed with spec and devnet development for SFI’d EIPs before considering elevating CFI’d EIPs to SFI status.
- Ethereum developers: Continue monitoring and evaluating the potential timeline gap between EL and CL readiness for Glamsterdam, with the possibility of decoupling if the gap becomes too large.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: =P?uL2E2)
- Download Chat (Passcode: =P?uL2E2)

---

**system** (2025-08-21):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=RU4DgyH662c

