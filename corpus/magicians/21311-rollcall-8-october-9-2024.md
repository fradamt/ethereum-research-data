---
source: magicians
topic_id: 21311
title: RollCall #8, October 9 2024
author: abcoathup
date: "2024-10-09"
category: Protocol Calls & happenings
tags: [rollcall]
url: https://ethereum-magicians.org/t/rollcall-8-october-9-2024/21311
views: 117
likes: 3
posts_count: 2
---

# RollCall #8, October 9 2024

#### Agenda

[RollCall #8 · Issue #1170 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1170); moderated by [@CarlBeek](/u/carlbeek)

#### Notes



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/chloe/48/11508_2.png)

      [RollCall #8, October 9 2024](https://ethereum-magicians.org/t/rollcall-8-october-9-2024/21311/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> Notes of RollCall #8
> Pasted from hackmd: RollCall #8 Summary - HackMD
> RIP 7755 - Contract standard for cross L2-calls
>
> Presented by Wilson from the Base team
> PR link: https://github.com/ethereum/RIPs/pull/31
> The goal of this RIP is to provide low level specification for arbitrary cross-chain calls, to be maximally on chain, and to provide a proof system with minimal trust assumptions
> Discussion
>
> Andreas Freund raised the question regarding the max time duration to fulfil a call, especially for …

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/3/3a8065ea9ccabc30a2ceeba2ab34d4b9cde0c607.jpeg)](https://www.youtube.com/watch?v=VVS9XBHrH2E)

## Replies

**Chloe** (2024-10-20):

## Notes of RollCall #8

Pasted from hackmd: [RollCall #8 Summary - HackMD](https://hackmd.io/@chloezhux/ByCiD1mgJx)

## RIP 7755 - Contract standard for cross L2-calls

- Presented by Wilson from the Base team
- PR link: https://github.com/ethereum/RIPs/pull/31
- The goal of this RIP is to provide low level specification for arbitrary cross-chain calls, to be maximally on chain, and to provide a proof system with minimal trust assumptions
- Discussion

Andreas Freund raised the question regarding the max time duration to fulfil a call, especially for time-sensitive txns, and another question regarding the time frame of finalityDelaySeconds.
- Elizas Tazartes raised the question regarding the relationship of storage proof & state root, and what exactly the storage proof tries to prove.
- Another suggestion on the finality delay is to include values boundaries as an indication to the wallets.

Areas need further exploration: Standardization of the pieces needed for the proofs

- Unified way of exposing a trusted L1 block hash/ state root on L2
- Standardize where state roots live on L1
- Common way of describing pending vs finalized state roots on L1

## L1 & Pectra updates

- Presented by Ansgar
pectra1215×597 144 KB

## Other discussion

- Breakout on the Future of the EVM on L2

Link: RollCall #8.1 Breakout - EVM Equivalence on L2: Past, Present, Future · Issue #1171 · ethereum/pm · GitHub
- Date: Oct 23rd 14-15 UTC
- Topic: Update on the thinking around Rollcall, broader RIP process, the future of EVM on L2 (will be presented by Ansgar & Carl)

Breakout on the L2 transaction fee API specs

- Date: Oct 30th
- Topic: L2 transaction fee API specs (will be presented by Andreas)

