---
source: magicians
topic_id: 21355
title: All Core Devs - Execution (ACDE) #199, October 24 2024
author: abcoathup
date: "2024-10-12"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-199-october-24-2024/21355
views: 263
likes: 5
posts_count: 2
---

# All Core Devs - Execution (ACDE) #199, October 24 2024

#### Agenda

[Execution Layer Meeting 199 · Issue #1177 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1177) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #199, October 24 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-199-october-24-2024/21355/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
>
> EIP-7742 is Scheduled for Inclusion in Pectra, teams to review @g11in’s proposed change.
> BLS MSM Repricings: @chfast will propose a new lookup table for costs and EL teams should run benchmarks with these. Further discussion planned on Monday’s testing call.
> EIP-7685 Empty Requests: EL + CL teams to review @fjl’s PRs by next ACDC, ideally merge before the call.
> EIP-7702 & EXTCODE* : @frangio to update his PR to return a constant value rather than the delegation designator when call…

#### Recording

  [![image](https://img.youtube.com/vi/3Y8X9_W9ecg/maxresdefault.jpg)](https://www.youtube.com/watch?v=3Y8X9_W9ecg&t=49s)

#### Additional info

[Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-199/) by [@Christine_dkim](/u/christine_dkim)

## Replies

**timbeiko** (2024-10-24):

# Action Items

- EIP-7742 is Scheduled for Inclusion in Pectra, teams to review @g11in’s proposed change.
- BLS MSM Repricings: @chfast will propose a new lookup table for costs and EL teams should run benchmarks with these. Further discussion planned on Monday’s testing call.
- EIP-7685 Empty Requests: EL + CL teams to review @fjl’s PRs by next ACDC, ideally merge before the call.
- EIP-7702 & EXTCODE* : @frangio to update his PR to return a constant value rather than the delegation designator when calling EXTCODE*.
- eth_* API  Revert Error Codes: teams to review @fjl’s proposal to standardize revert error codes.

# Scheduling Notes

- DST will start in some regions prior to the next ACDE, check your local time.
- The last pre-devcon ACD is ACDE#200 (!!) and first post-devcon ACD will be ACDC#146. More explicitly we will:

Cancel 11/14 ACDC
- Cancel 11/11 and 11/18 Pectra Interop Testing Calls
- Replace 11/21 ACDE by a Pectra Interop Testing Call

# Call Summary

##

- Good participation rate on the network
- Issues with Erigon, EthereumJS (investigating), and Grandine (WIP fix)
- Bad block generation has started, currently running on 1 node, plan to increase to 4 soon

## Pectra Spec Changes

### EIP-2537:

- Keep subgroup checks: community outreach revealed that many STARK-based projects are unlikely to switch to BLS12-381 due to the lack of infrastructure support, and no project expressed a strong desire to have the non-subgroup-checked versions of the precompiles. Additionally, further investigation into the BLS libraries showed that it would require non-trivial changes there to separate subgroup checks out. We’ll keep the subgroup checks in the precompiles.
- MSM Repricings: there was no consensus on the MSM repricing values. @chfast plans to propose a new lookup table for costs and EL teams will run benchmarks based on these. More conversations to follow in next week’s testing call.

### EIP-7685

- @fjl proposed excluding empty items from requests_hash commitments (PR), to keep the empty requests independent of the fork schedule, simplifying genesis configurations in clients.
- EL clients supported the change, with some tentative support from CL teams. It was added to the devnet-5 spec. If there are still issues by next week’s ACDC, we’ll discuss them there.

### EIP-7702

- @frangio opened a PR to address delegation concerns related to EXTCODE* raised on EthMagicians
- There was some support for the change on the call, but @adietrichs proposed that instead of operating on the delegation designator itself, the calls to EXTCODE* return a constant value.
- @frangio will open a PR incorporating the changes

### EIP-7742

- EL teams agreed to move the EIP to SFI (PR.
- @g11in proposed a change to the EIP, but due to mic issues & call attendees not having properly reviewed, we’ll review async

## Validator Bandwidth Concerns

- No one on the call to discuss, no updates beyond what was shared on ethresearch

## EIP-7790

*Note: this was a contentious topic with a lot of back and forth, please watch the livestream for the full nuance.*

- @Giulio2002 proposed EIP-7790 to suggest values to use as part of the EIP-7783 gradual gas limit proposal: going from 30m → 60m gas over a 2 year period.
- Since the last call, Giulio opened PRs for EIP-7783 on Reth, Erigon and Geth, while the Nethermind team has begun work on their own implementation.
- @Giulio2002 shared that he’d reached out to client teams to get their feedback on the 7790 numbers. He said that Nethermind and Erigon were onboard, @karalabe had expressed some support (although others in Geth opposed on the call) and Besu had concerns.
- On the call, several concerns were raised about the proposal, including:

The risks of raising the gas limit before implementing EIP-7623
- Its impact on history growth  (although somewhat mitigated post-4844)
- Potential integration concerns with mev-boost
- Concerns that a gradual raise may lead to “silent failures”, as opposed to our current approach of “step function” increases
- Questions about whether 60M over 2 years was the right number of aim for
- Concerns about pre-committing to long-term increases

While there is value in client teams being aligned on their approaches here, it is worth noting that the gas limit is **not** controlled by clients/hard forks, but by validators when they propose a block. This means that client teams can suggest different defaults, which block proposers may or may not adhere to.

## Adding a Revert Error Code to eth_* APIs

- @fjl proposed adding a standard error code for reverts in eth_* APIs (PR), mirroring Geth’s behavior since 2022.
- There was broad support, conversation to continue on the PR

