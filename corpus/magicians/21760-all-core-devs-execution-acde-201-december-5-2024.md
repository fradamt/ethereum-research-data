---
source: magicians
topic_id: 21760
title: All Core Devs - Execution (ACDE) #201, December 5 2024
author: abcoathup
date: "2024-11-19"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-201-december-5-2024/21760
views: 320
likes: 2
posts_count: 3
---

# All Core Devs - Execution (ACDE) #201, December 5 2024

#### Agenda

[Execution Layer Meeting 201 · Issue #1197 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1197) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #201, December 5 2024](https://ethereum-magicians.org/t/all-core-devs-execution-acde-201-december-5-2024/21760/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Action Items
>
>  EIP-7623 is Scheduled for Inclusion in Pectra
>
>  On next Monday’s testing call, determine whether it should be in scope for devnet-5 or as part of a separate devnet.
>
>
>  @MarekM25 to propose final gas changes for EIP-2537 based on worst-case numbers for production clients
>  Gather feedback from Rollups about EIP-7762 and assess testing +implementation overhead before next week’s ACDC
>  We agreed to merge the Declined for Inclusion addition to EIP-7723
>
>
>  Going forward, non-core EIPs w…

#### Recording

  [![image](https://img.youtube.com/vi/Umh7ZKukmtY/maxresdefault.jpg)](https://www.youtube.com/watch?v=Umh7ZKukmtY&t=83s)

#### Additional info

- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

## Replies

**timbeiko** (2024-12-05):

# Action Items

- EIP-7623 is Scheduled for Inclusion in Pectra

 On next Monday’s testing call, determine whether it should be in scope for devnet-5 or as part of a separate devnet.

 [@MarekM25](/u/marekm25) to propose final gas changes for EIP-2537 based on worst-case numbers for production clients
 Gather feedback from Rollups about EIP-7762 and assess testing +implementation overhead before next week’s ACDC
 We agreed to merge the `Declined for Inclusion` addition to [EIP-7723](https://github.com/ethereum/EIPs/pull/9056)

- Going forward, non-core EIPs will also be listed on Meta EIPs, with the network upgrade activation time reflecting the latest date by which clients should have deployed a non-core EIP.

### ACD Holiday Schedule

- Testing call on Dec 23
- Cancel ACDE on Dec 26
- Cancel testing call on Dec 30
- Replace ACDC by testing call on Jan 2

# Call Summary

## Pectra

###

- Mostly stable, 97% participation rate
- Grandine fixed outstanding issues, EthereumJS & Nimbus still working on fixes
- Focus shifting to devnet-5

###

- EIP-7691 was missing from the Pectra Meta EIP (fixed), latest changes for devnet-5 have been merged in the EIP.
- Teams discussed whether we could make devnet-5 the last Pectra devnet and/or launch it before the holidays. There were concerns about the increased scope with additional EIPs added.

### EIP updates

#### EIP-7702

- Some progress on transaction pool implementations, conversation to continue in #interop discord channel

#### EIP-2537

- Nethermind proposed changes to the BLS precompile pricing (PR).
- There were some concerns about performance by evmone maintainers, but no client uses it in production (although Erigon is considering switching to it in the next year). Besu did not have someone on the call who could confirm that the proposal works for them.
- We agreed to move forward with the worst-case gas costs for production clients for now, even if they may be too aggressive for evmone. Note that this may be due to evmone’s ecrecover implementation, against which the BLS gas costs are benchmarked.
- We may choose a more granular pricing scheme if it can be agreed upon in the next few days.

#### EIP-7623

- A new PR addressed concerns raised by @shemnon
- While there were concerns about the testing overhead, client teams were in favor of including the change in Pectra. On next Monday’s testing call, we’ll discuss how to best handle devnet rollouts.

#### EIP-7762

- There was contentious discussion about whether to include this EIP. I recommend watching the livestream for the full context.
- @adietrichs and @MaxResnick argued the EIP was very important as rollups struggle with the frequent first price auctions that emerge as a result of blobs coming in and out of periods of price discovery. In addition, they believe this is a relatively minimal change that would not add too much overhead to the fork.
- @matt argued that the EIP was a premature intervention in the nascent blob market, and that we should revisit the idea in the next fork if this is still problematic.
- A few EL teams were weakly in support of the EIP, but the testing and devops teams had concerns about the additional overhead and delays this would impose.
- There was back and forth about making a decision now vs. gathering more input on next week’s testing and RollCall.
- There wasn’t enough consensus to include the EIP now. I will propose we revisit the topic on next week’s ACDC after gathering more input.

## History Expiry

- @pipermerriam shared an implementation plan for EIP-4444
- There was extensive back and forth around whether a new eth protocol should be used to advertise that a node no longer serves pre-merge data.  No consensus reached on the topic. Recommend watching the livestream for the specifics!
- Piper will write up a summary of the conversation and next steps.

## EIP-4803

- @axic proposed that EIP-4803 be retroactively activated from genesis. It does not change existing behavior, and he believes geth already adds this constraint to the transaction gas limit.
- While the change does not require clients to do anything, it does require extra tests. With the testing team being focused on Pectra, we agreed to not to the change now.
- There were minor concerns about using 2^64-1 vs. 2^63-1 as the bound, but general agreement around the change.
- @axic opened a PR to add this change to EIP-7675, which we’ll revisit once Pectra implementations are farther along.

## ACD Process Improvements

- We agreed to merge the Declined for Inclusion addition to EIP-7723
- We agreed that, going forward, non-core EIPs will also be listed on Meta EIPs, with the network upgrade activation time reflecting the latest date by which clients should have deployed a non-core EIP.
- Not enough time to discuss the CFI/SFI status & devnet linkage.

---

**poojaranjan** (2024-12-06):

> We agreed that, going forward, non-core EIPs will also be listed on Meta EIPs, with the network upgrade activation time reflecting the latest date by which clients should have deployed a non-core EIP.

Changes to the Meta EIP represent a significant change to the existing EIP documentation process. As I understand, we haven’t yet gathered input from the EIP editors on this proposal. Personally, I would prefer to discuss this proposed change with the editors in the upcoming [EIPIP meeting](https://github.com/ethcatherders/EIPIP/issues/365) before presenting it to the broader community.

