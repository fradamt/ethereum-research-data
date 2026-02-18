---
source: magicians
topic_id: 20910
title: All Core Devs - Execution (ACDE) #195, August 29 2024
author: abcoathup
date: "2024-08-29"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-195-august-29-2024/20910
views: 336
likes: 3
posts_count: 2
---

# All Core Devs - Execution (ACDE) #195, August 29 2024

#### Agenda

[Execution Layer Meeting 195 · Issue #1142 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1142) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #195, August 29 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-195-august-29-2024/20910/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDE Call Summary
> Action items & next steps
>
>
> Pectra implementations:
>
> EL teams should focus on pectra-devnet-3@v1.4.0 tests prior to devnet-3’s launch, including the recent change to SELFDESTRUCT behaviour during 7702 transactions (PR#8832)
>
>
>
> Pectra EIP additions:
>
> @timbeiko to update EIP-7600 using EIP-7723 standards to track EIPs Proposed, Considered and Scheduled for Inclusion in Pectra. Client teams should review and share their preferred next steps prior to next ACDE.
> EIP-7742 was CFI’d…

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/8/89604e441f078f8618e3dfa7d95ad161ff055a76.jpeg)](https://www.youtube.com/watch?v=HJ9WxAOwTTA&t=73s)

## Replies

**timbeiko** (2024-08-29):

# ACDE Call Summary

## Action items & next steps

- Pectra implementations:

EL teams should focus on pectra-devnet-3@v1.4.0 tests prior to devnet-3’s launch, including the recent change to SELFDESTRUCT behaviour during 7702 transactions (PR#8832)

**Pectra EIP additions**:

- @timbeiko to update EIP-7600 using EIP-7723 standards to track EIPs Proposed, Considered and Scheduled for Inclusion in Pectra. Client teams should review and share their preferred next steps prior to next ACDE.
- EIP-7742 was CFI’d for Pectra
- @MaxResnick to draft an EIP proposing a new blob gas price floor (context)

**Potential devnet-4 additions, pending more async reviews**:

- Update EIP-7702: Change `MAGIC` from `0x05` to `0x1a` by etan-status · Pull Request #8835 · ethereum/EIPs · GitHub
- Update EIP-7702: Restrict chain_id to chain's id or zero by rakita · Pull Request #8833 · ethereum/EIPs · GitHub
- https://github.com/ethereum/consensus-specs/pull/3882

**Misc.**

- EOF: keep the current spec as a target for devnet-4 and discuss potential mitigations to these issues in next implementers’ call.
- CL teams should review and approve the 7251 penalty fix.
- EL + CL teams should review Engine API PR#565.

## Recap

*Note: this is based on my rough, imperfect notes. For the full context/nuance, please watch the recording.*

### Pectra Devnets

- devnet-2 found several client bugs, with many still being worked on by client teams. The devnet won’t be restarted, but instead teams should focus on static tests and getting ready for devnet-3.
- A new EL static test suite was released for teams to test against prior to devnet-3 launching. Additions largely focus on EIP-7702. Reth and EthereumJS both pass the full suite.
- Once most teams pass these tests, devnet-3 will be launched, hopefully within the next week.

### EIP-7702

Three open PRs to the EIP were discussed:

1. Update EIP-7702: selfdestruct opcode behaviour change in eip-7702 by sudeepdino008 · Pull Request #8832 · ethereum/EIPs · GitHub

This change was already incorporated in the latest EL test suite, it will be added to devnet-3
2. Update EIP-7702: Change `MAGIC` from `0x05` to `0x1a` by etan-status · Pull Request #8835 · ethereum/EIPs · GitHub

Moderate support for the change, but no urgency. Consider adding in devnet-4.
3. Update EIP-7702: Restrict chain_id to chain's id or zero by rakita · Pull Request #8833 · ethereum/EIPs · GitHub

@matt had concerns about making the validity of full transactions dependent on non-serialization validity conditions for authorizations.
4. @yoavw shared these concerns, especially in the case where several transactions sharing the same authorization could be invalidated by a single one.
5. We’ll continue discussing this change and potentially include it in devnet-4 if accepted.

### EOF

- @frangio shared concerns about EOF’s lack of EXTCODESIZE or EXTCODEHASH and restrictions on DELEGATECALL. He emphasized on the call that these restrictions could affect compatibility with NFT standards, and also risk making some contracts unusable if upgraded incorrectly.
- @shemnon agreed with the concerns, but added that EOF’s design goal was to remove as much as possible to both minimize complexity of initial deployment and avoid the challenges around deprecating existing functionality.
- Teams still don’t have implementations of the current spec that pass all EOF tests. After some back and forth, we agreed to maintain EOF’s scope as-is for its initial inclusion on devnets, continue discussing solutions to the issues raised by @frangio and, once EOF is live on devnets, re-evaluate whether we’d want to make further changes in this fork.

### EIP-7251

- General support for the proposed penalty fix, CL teams should ideally review & approve so that it can be merged into the specs.

### Engine API

- No live comments on the call about PR#565, teams should review async

@tersec left a comment right at the start of ACD.

### Pectra EIP Additions

Three proposed Pectra additions were on the agenda, along with those discussed in past calls. Inclusion decisions are not urgent and client teams should consider all of the candidate changes, rather than just the ones discussed today. To that end, we decided to **not** make decisions about Pectra inclusion on this call.

Instead, I will update the [Pectra Meta EIP](https://eips.ethereum.org/EIPS/eip-7600) using the format in [EIP-7723](https://eips.ethereum.org/EIPS/eip-7723) to reflect EIPs that have been Proposed, Considered and Scheduled for Inclusion in the Pectra fork. On the next ACDE, we will discuss potential additions to the fork.

### EIP-7623

- @Nerolation came on to re-state his desire to see the EIP in Pectra. Several client developers and researchers support it, especially given its impact on large block spam.
- The change is relatively simple to implement (old Geth prototype PR) and, unlike a blanket CALLDATA cost increase, leaves most transactions’ costs unchanged. See an old impact analysis.

### EIP-7742

- @ralexstokes proposed this EIP to decouple the maximum blob count from the EL. Having this parameter exclusively set by the CL allows the blob throughput to be adjusted without an EL fork.
- The EIP had general support for it, but we chose to not make decisions about inclusion on this call about inclusion and instead moved the EIP to CFI.

### Increasing the blob reserve price

- @MaxResnick proposed increasing the blob gas reserve price from 1 to 160217286 wei. The goal of this change is to reduce the time it takes for blobs to enter price discovery, lowering volatility.

@adietrichs added that the rationale for originally setting it to 1 wei was that we expected to only enter price discovery once, and then remain above the floor. In practice, we’ve gone in and out of price discovery based on volatile usage patterns.
- The current floor price requires a long time to reach even the relatively low new floor proposed, leading to increased bandwidth stress on the network, which impacts node operators, especially solo-stakers.

There was broad support for the proposal and Max will draft an EIP in the coming days.

