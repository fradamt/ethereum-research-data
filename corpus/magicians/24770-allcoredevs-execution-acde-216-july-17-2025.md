---
source: magicians
topic_id: 24770
title: AllCoreDevs - Execution (ACDE) #216 (July 17, 2025)
author: system
date: "2025-07-09"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/allcoredevs-execution-acde-216-july-17-2025/24770
views: 719
likes: 5
posts_count: 6
---

# AllCoreDevs - Execution (ACDE) #216 (July 17, 2025)

# AllCoreDevs - Execution (ACDE) #216 (July 17, 2025)

- Jul 17, 2025, 14:00 UTC
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Fusaka

devnet updates
- Upgrade timelines

After Pectra, we agreed to have a 30 day window between client releases and both the first testnet fork and mainnet.
- Assuming we followed this and wanted to deliver Fusaka before Devconnect, this implies:

Mainnet ~> Nov 5-12
- Last testnet ~> Oct 6-10
- First testnet ~> Sep 22 - Oct 3
- Client testnet releases ~> Week of Aug 25

```
- Is this realistic?
   - [@ralexstokes counter-proposal](https://github.com/ethereum/pm/issues/1610#issuecomment-3075167383)
   - [PeerDAS todos](https://github.com/ethereum/pm/issues/1610#issuecomment-3075401629)
   - Holesky fork?
```

- EIP-7907
- https://github.com/ethereum/EIPs/pull/9986

[Glamsterdam Planning](https://ethereum-magicians.org/t/eip-7773-glamsterdam-network-upgrade-meta-thread/21195)

- Next 2 ACDE focused on headliner discussions

Client team preferences

Geth
- Reth
- Erigon
- Nethermind
- Besu
- Lighthouse
- Prysm
- Grandine
- Lodestar
- Teku

Most important open questions
Scheduling live discussions
Broader community input

EIP PFI deadline?

- August 21 (end of headliner selection)?
- Sep/Oct?
- Fusaka shipping?

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : acde
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : true
- Already on Ethereum Calendar : true
- Need YouTube stream links : true
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1610)

## Replies

**abcoathup** (2025-07-16):

### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [AllCoreDevs - Execution (ACDE) #216 (July 17, 2025)](https://ethereum-magicians.org/t/allcoredevs-execution-acde-216-july-17-2025/24770/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
> Fusaka
>
> Remove EIP-7907 from Fusaka
> Launch devnet-3 by July 23
>
> Glamsterdam
>
> Continue headliner discussions on next ACDE calls (July 31 & August 14)
> Finalize headliners by August 21
>
>
> Summary
> Fusaka Devnet Updates
>
> Devnet-2 running stable with minor issues mainly from Consensus Layer clients:
>
> Lighthouse: Incorrect suggested value, payload leak.
> Lodestar: Excessive polling leading to peer bans.
> Nimbus: Node overloaded and crashing due to requests.
> Prysm: Missing metadata field, inco…

### Recordings/Stream

- https://www.youtube.com/live/dkIQxIHX56E?t=198s
- Eth Cat Herders:

Live stream on X: live stream [x.com/ethcatherders]

### Writeups

- Tweet thread by @poojaranjan
- ACDE #216: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- Highlights from ACDE) Call #216 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Fusaka upgrade [overview]:

Tight timeline if targeting mainnet November 5-12 (before Devconnect)
- EIP7907 (increase contract code size) removed (Denied for Inclusion)
- fusaka-devnet-3 targeting July 23

Glamsterdam upgrade [[overview](https://forkcast.org/upgrade/glamsterdam)]:

- Proposed headliners & client team perspectives:

Execution layer client teams favor block level access lists (BALs) (+ repricing)
- Consensus layer client teams favor ePBS, potentially with FOCIL
- Create your own shareable rank

Non-headliner EIPs can be proposed for inclusion now

---

**poojaranjan** (2025-07-17):

[Tweet thread](https://x.com/poojaranjan19/status/1945845950859084276)

---

**timbeiko** (2025-07-17):

# Action Items

## Fusaka

- Remove EIP-7907 from Fusaka
- Launch devnet-3 by July 23

## Glamsterdam

- Continue headliner discussions on next ACDE calls (July 31 & August 14)
- Finalize headliners by August 21

---

# Summary

## Fusaka Devnet Updates

- Devnet-2 running stable with minor issues mainly from Consensus Layer clients:

Lighthouse: Incorrect suggested value, payload leak.
- Lodestar: Excessive polling leading to peer bans.
- Nimbus: Node overloaded and crashing due to requests.
- Prysm: Missing metadata field, incorrect block schedule (PR fix available).

Client teams comfortable proceeding to devnet-3 by July 23.

## EIP-7907

- Decision: Removed from Fusaka due to significant unresolved complexity and timeline risks.
- Simplified alternatives (like EIP-7903) discussed but rejected to avoid additional delays.
- General agreement to defer significant contract size changes to Glamsterdam or future forks.

## Fusaka Timeline and Audit Concerns

- Current proposed timeline is tight if targeting delivery before Devconnect (~Nov 5-12 Mainnet).
- Uncertainty remains around achieving sufficient testnet stability and allowing enough time for audit competition and bug bounty.
- Holesky upgrade could provide early indicator of readiness without extensive user disruption.

## Glamsterdam Headliner Selection

- Execution Layer (EL) leaning strongly toward Block-Level Access Lists, paired with significant gas repricing to achieve meaningful scaling improvements.
- Consensus Layer (CL) strongly favors EPBS, with wide but not unanimous support.
- FOCIL is popular but seen as potentially conflicting with EPBS in terms of implementation complexity and scope. Consensus to evaluate further on upcoming calls.

- See client’s writeupts at Glamsterdam Upgrade - Forkcast

## Timeline for other Glamsterdam EIPs

- Deadline for regular (non-headliner) EIPs will be set after headliners are finalized (Aug 21 tentative).
- Clients prefer focusing on Fusaka for now, delaying broader EIP considerations slightly.

## Next Steps

- Clearly define priorities between FOCIL and EPBS in upcoming Consensus Layer discussions.
- Determine community stakeholders needed for headliner feedback.
- Further clarify testing requirements and audit timelines for Fusaka.

---

**system** (2025-07-17):

### Meeting Summary:

The team discussed the timeline and process for the Fusaka upgrade, including the removal of EIP-7907 and plans for Devnet 3 deployment. They debated potential headliners and scaling themes for the Glamsterdam fork, considering options such as block access lists, ePBS, and fossil. The group also addressed implementation challenges, timeline considerations, and the need for community input in finalizing proposals for upcoming forks.

**Click to expand detailed summary**

The team discussed the timeline and process for the Fusaka upgrade, aiming to ship before the end of the year. They agreed on a target launch date for Devnet 3 of July 23rd, 2025, with client releases planned for late August or early September. The group also discussed the need for longer windows between client releases and testnet forks to allow for security audits and bug bounty programs. Parithosh emphasized the importance of having a stable Devnet 3 with no spec changes after that, as well as the need for large network testing and analysis of BPO values.

The team discussed removing EIP-7907 from the Fusaka fork to accelerate its release, as there was uncertainty about its implementation and testing. They agreed to proceed without the EIP, focusing on shipping Peer-to-Peer as quickly as possible. The group also considered a simpler code size increase for future forks like Glamsterdam, with some suggesting a 50% bump or Giulio’s EIP proposal to increase the limit to 32kB. Testing bandwidth and the need for a spec freeze were highlighted as key concerns.

The team discussed the timeline for the devnet 3 deployment, aiming for July 23rd, and debated the rollout schedule for the upcoming hard fork. Fredrik explained the rationale behind the 30-day periods between client release and testnet, and between last testnet and mainnet, emphasizing the need for security and audit competitions. The group considered shortening the testnet timeline due to community feedback about testnet stability, but agreed to aim for early September for the mainnet release. They also discussed the need for quick testing of the Holeski upgrade, given its impending sunset.

The team discussed headliner candidates for Glamsterdam, with block level access list and fossil emerging as the two most frequently mentioned preferences on the EL side. Ben Adams noted that block level access list aligns best with the strategic focus of Amsterdam, while Roman raised a question about potentially temporary storage of block access lists. The team agreed that block access lists could be rebuilt from blocks if needed, though the exact storage approach needs further consideration.

The team discussed scaling themes for Glamsterdam, with Ansgar emphasizing the importance of repricing for scaling on the El side, while Justin challenged the idea of separate headliners for El and Cl, arguing that censorship resistance could be a unifying theme. Roman supported Ansgar’s view on headliners, suggesting that block access lists (BALs) might be too small for headliner status. The team also debated the distinction between headliners and regular EIPs, with some questioning the arbitrary nature of the one-theme-per-layer constraint.

The team discussed block access lists (BALs) and scaling proposals, with Ben highlighting their importance for handling larger blocks and Łukasz noting potential scaling issues with snap sync healing. Tim emphasized the need to determine whether code chunking or recontractor pricing should be pursued, and Som expressed Erigon’s focus on implementing block-level access lists as a headliner, while acknowledging the need for parallel execution implementations. The team debated the merits of ePBS and FOCIL, with concerns raised about combining them in a single fork, and Justin requested links to current code chunking designs to inform the viability of an EIP.

The team discussed the implementation sequence of various Ethereum Improvement Proposals (EIPs), particularly focusing on ePBS, fossil, and block access lists. There was agreement that ePBS should be implemented before fossil, with Tim noting that client teams view ePBS as a higher priority. The group expressed uncertainty about whether all these changes could be bundled into a single fork, with Tim suggesting they might need to choose between ePBS and fossil. Potuz emphasized that block access lists and ePBS should remain separate implementations, with fossil being a CL-focused proposal that doesn’t need to be highlighted as an EL headliner.

The team discussed the complexity and implementation challenges of combining EIPs like FOCIL and ePBS, with Tim suggesting that headliners could be complex and should be evaluated on a case-by-case basis. They debated the feasibility of including multiple EIPs in a single fork, considering the potential impact on development time and testing. The group agreed that block-level access lists and repricing could be included in a fork, as these features are less complex and can be implemented independently. They also discussed the importance of client adoption and testing of new features, with Toni emphasizing that clients may need time to implement and use new consensus features for scaling purposes.

The team discussed the timeline and process for finalizing proposals for the upcoming fork, focusing on the need for community and client team input. They agreed to remove EIP-7907 from the current fork (Fusaka) and to continue gathering input on potential headliners, particularly EIPs for block access lists and scaling. The team also debated the inclusion of EIP-7903 as an alternative, but decided against it due to potential complications and the need to finalize the scope of the current fork. They plan to revisit the headliner decision in the next CL call and to continue gathering community input over the next few weeks.

### Next Steps:

- Client teams: Continue work on Devnet 3, aiming for deployment on July 23rd.
- Tim: Update the Meta EIP to remove EIP-7907 from Fusaka.
- All: Prepare to make a final decision on Amsterdam headliners at the next ACD call.
- Client teams: Prepare for discussions on Amsterdam headliners, focusing on block-level access lists and EIP-4844.
- All: Consider and prepare input on the timing and scope of the next fork for the next call.
- CL teams: Prepare for a more in-depth discussion on EIP-4844 vs. Fossil for the next CL call.
- All: Identify and reach out to relevant stakeholders for input on potential Amsterdam EIPs before the next call.
- Client teams: Consider allocating resources to start work on EIP-4844 and block-level access lists in parallel with Fusaka development.

### Recording Access:

- Join Recording Session
- Download Transcript (Passcode: eCSMt4j+)
- Download Chat (Passcode: eCSMt4j+)

---

**system** (2025-07-17):

**YouTube Stream Links:**

- Stream 1: https://youtube.com/watch?v=dkIQxIHX56E

