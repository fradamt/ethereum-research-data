---
source: magicians
topic_id: 23835
title: All Core Devs - Execution (ACDE) #211, May 8
author: system
date: "2025-04-24"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-211-may-8/23835
views: 373
likes: 2
posts_count: 3
---

# All Core Devs - Execution (ACDE) #211, May 8

# All Core Devs - Execution (ACDE) 211

- May 8, 2025, 14:00-15:30 UTC
- Stream
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Pectra Mainnet Deployment
- Fusaka

PeerDAS → ACDT
- SFI’ing EIP-7935: Set default gas limit to XX0M

RLP Execution Block Limit
- EIP-7938

Removal of dynamic jumps in EVM
State Growth Metrics

- Data collection points for "BloatNet" - HackMD
- Artificial State growth notes - HackMD

[Community Consensus, Fork Headliners & ACD Working Groups](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088)
[For an ACD platform](https://ethereum-magicians.org/t/for-an-acd-platform/24098)
[EIP-7636](https://eips.ethereum.org/EIPS/eip-7636) feedback

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : false #
- Already on Ethereum Calendar : false #
- Need YouTube stream links : true #
- Facilitator email: tim@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1500)

## Replies

**abcoathup** (2025-04-30):

### Summary

*[Main action items by [@timbeiko](/u/timbeiko) copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1370061549498011667)]*

1. We agreed to SFI EIP-7935, with the implication that other EIPs related to increasing the gas limit will be added to Fusaka
2. In that vein, we agreed to CFI EIP-7934
3. On Monday’s call, we’ll agree to the scope for fusaka-devnet-1 . Client teams, please review the SFI list and prepare your “sorted preferences” for CFI → SFI by the call: EIP-7607: Hardfork Meta - Fusaka

The testing team will also review the CFI list and share their thoughts on the testing burden for each EIP before then.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #211, May 8](https://ethereum-magicians.org/t/all-core-devs-execution-acde-211-may-8/23835/4) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE #211 Summary
> Action Items
>
> We agreed to SFI EIP-7935, implying that other gas-limit-related EIPs will be added to Fusaka.
> In line with the above, we agreed to CFI EIP-7934.
> On Monday’s call, we’ll finalize the scope for fusaka-devnet-1. Client teams are encouraged to review the current CFI list and prepare their sorted preferences for EIPs they’d like to promote from CFI → SFI.
>
>
> Summary
> Pectra Mainnet Wrap-Up
>
> Pectra activated smoothly on mainnet on May 7, 2025, with no significant issues …

### Recordings

  [![image](https://img.youtube.com/vi/Y7j8FdRkSrA/maxresdefault.jpg)](https://www.youtube.com/watch?v=Y7j8FdRkSrA&t=170s)



      [x.com](https://x.com/EthCatHerders/status/1920482268117680461)





####

[@](https://x.com/EthCatHerders/status/1920482268117680461)



  https://x.com/EthCatHerders/status/1920482268117680461










### Writeups

- Highlights of Ethereum’s All Core Devs Meeting (ACDE) #211 by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Community Consensus, Fork Headliners & ACD Working Groups
- All Core Devs - Testing (ACDT) #36 | May 12 2025 [call covers Fusaka implementation]

---

**timbeiko** (2025-05-09):

## ACDE #211 Summary

### Action Items

1. We agreed to SFI EIP-7935, implying that other gas-limit-related EIPs will be added to Fusaka.
2. In line with the above, we agreed to CFI EIP-7934.
3. On Monday’s call, we’ll finalize the scope for fusaka-devnet-1. Client teams are encouraged to review the current CFI list and prepare their sorted preferences for EIPs they’d like to promote from CFI → SFI.

---

### Summary

#### Pectra Mainnet Wrap-Up

- Pectra activated smoothly on mainnet on May 7, 2025, with no significant issues reported. Client teams and users are encouraged to closely monitor network behavior post-upgrade.
- This fork introduced several significant changes, notably EIP-7702 (EOA account code setting), EIP-7251 (MAX_EB), and the EIP-2537 BLS precompile. Client teams highlighted improved testing processes and encouraged ongoing feedback.

#### Fusaka Planning

- Fusaka implementation discussions will shift exclusively to the weekly ACDT call moving forward.
- The immediate next step is finalizing fusaka-devnet-1 scope on next Monday’s ACDT call, after client teams provide their prioritized preferences for EIPs moving from CFI → SFI.
- As of this call, we’ve SFI’d EIP-7935 (default gas limit adjustment) and previously EIP-7594 (PeerDAS). Additionally, we’ve CFI’d EIP-7934 (RLP execution block size limit) and several repricing EIPs (notably EIP-7823 and EIP-7883 related to MODEXP). However, these repricing EIPs remain pending full consensus and test coverage before they can move to SFI.

#### Gas Limit and State Growth Discussion

The discussion around raising the gas limit (EIP-7935) dominated the call, highlighting clear areas of alignment and remaining uncertainties:

- Agreed upon :

SFI EIP-7935, setting a default gas limit (likely around 150M), to provide a concrete baseline for testing and performance validation. This agreement explicitly implies that related repricing EIPs, notably EIP-7934 (10 MB RLP execution block size limit), will need to accompany this change to manage resource usage effectively.

**Open discussions and considerations** :

- Extensive debate about resource implications of higher gas limits. Specific bottlenecks highlighted include increased disk requirements, state-sync performance degradation, and elevated RAM usage (potentially necessitating 32+ GB nodes).
- Teams highlighted that EIP-7938 (exponential auto-increase mechanism) remains ambitious. Several participants emphasized the necessity of robust empirical validation before pursuing automated gas limit increases.
- Broad acknowledgment that repricing EIPs (EIP-7823 and EIP-7883, potentially EIP-7918) should precede substantial gas limit increases. Current statuses of these repricing EIPs are still CFI, with client teams expected to confirm their readiness and testing status by Monday.
- Further, there’s general alignment that gas-limit scaling must be carefully coordinated with progress on history expiry and better pricing of state IO operations, though these discussions remain ongoing.

Given the complexity and depth of technical trade-offs, stakeholders and implementers are strongly encouraged to review the call [recording](https://www.youtube.com/watch?v=Y7j8FdRkSrA) and chat transcript for full context.

#### AllCoreDevs Process Improvement

- Due to time constraints and extensive discussion around the gas limit topic, we did not cover previously planned conversations on ACD process improvements or the proposed ACD platform during this call. Interested parties should continue participating asynchronously via the Ethereum Magicians threads:

Community Consensus & Fork Headliners
- ACD Platform proposal

#### EVM & Additional Topics

- A brief discussion around removing dynamic jumps occurred, concluding that substantial changes to EVM functionality (e.g., static vs. dynamic jumps) should likely be addressed through a longer-term EVM roadmap rather than immediate inclusion in Fusaka. Participants expressed interest in structuring this conversation more explicitly in future calls.

#### Closing Shout-Outs

- Contributors to the recent Pectra upgrade are invited to submit feedback and experiences for the Pectra Pages.
- The second Protocol Research Call is scheduled for next Wednesday, focusing on short-term EL scaling strategies targeting Glamsterdam and future forks.

---

### Next Steps

- Client teams encouraged to carefully review the current CFI EIPs list, preparing their ranked preferences and testing statuses for Monday’s call, where the final scope for Fusaka’s next devnet will be determined.

