---
source: magicians
topic_id: 10236
title: "EIP-5283: A Semaphore for Parallelizable Reentrancy Protection"
author: sergio_lerner
date: "2022-08-03"
category: EIPs > EIPs core
tags: [precompile, scaling]
url: https://ethereum-magicians.org/t/eip-5283-a-semaphore-for-parallelizable-reentrancy-protection/10236
views: 2417
likes: 1
posts_count: 4
---

# EIP-5283: A Semaphore for Parallelizable Reentrancy Protection

Hi! I’d like to open the discussion over [EIP-5283](https://github.com/ethereum/EIPs/pull/5283/files).

## Replies

**moodysalem** (2022-08-04):

Re your comment [here](https://github.com/ethereum/EIPs/pull/5283#discussion_r937198229):

> yes, transient opcodes are better from the EVM “purity” standpoint. But I haven’t heard of any use for the transient opcodes apart from mutexes. I will add the discussions tag, where we should be chatting.

There are many use cases, which are discussed in the [discussion thread of EIP-1153](https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553). [Here is one of them from Arbitrum](https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553/47). [Here is the primary motivation](https://ethereum-magicians.org/t/eip-1153-transient-storage-opcodes/553/45), which is much more than just reentrancy locks. Another use case is communicating information from nested callbacks (we do this in the Uniswap V3 router to return the computed amount in for exact output swaps, which are executed in reverse and involve nested callbacks).

IMO this EIP has no advantages over transient storage.

---

**sergio_lerner** (2022-08-04):

I also prefer transient opcodes over my proposal (edit: the new EIP-1153 does interact with reverts).

But EIP 1153 was created 4 years ago. There is a high chance it is activated in another 2 years, and maybe it is never activated. There are many drawbacks pointed out in EIP-1153 discussion thread. Meanwhile, everybody is creating contracts that are not scalable with fine-grained parallel transaction processing.

My proposal is to do something very simple and low risk now to improve the blockchain forever. Not having a better mutex mechanism now will have a negative impact in millions of future transactions.

It’s not a technical trade-off, but a community trade-off.

---

**moodysalem** (2022-08-04):

> But EIP 1153 was created 4 years ago. There is a high chance it is activated in another 2 years, and maybe it is never activated. Meanwhile, everybody is creating contracts that are not scalable with fine-grained parallel transaction processing.

Please help advocate to have transient storage included in Shanghai! I think the benefits to parallelization have been so far under-emphasized.

Also, work to implement this everywhere is already being done or contracted by Uniswap Labs, tracked publicly [here](https://github.com/orgs/Uniswap/projects/24). Hopefully come Shanghai there is no reason not to include it.

