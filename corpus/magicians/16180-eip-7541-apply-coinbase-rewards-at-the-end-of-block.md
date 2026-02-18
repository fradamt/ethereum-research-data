---
source: magicians
topic_id: 16180
title: "EIP-7541: Apply Coinbase Rewards At The End Of Block"
author: rkrasiuk
date: "2023-10-20"
category: EIPs > EIPs core
tags: [evm, core-eips]
url: https://ethereum-magicians.org/t/eip-7541-apply-coinbase-rewards-at-the-end-of-block/16180
views: 1267
likes: 4
posts_count: 5
---

# EIP-7541: Apply Coinbase Rewards At The End Of Block

We want to introduce the EIP to apply coinbase rewards at the end of the block.

https://github.com/ethereum/EIPs/pull/7880

**Abstract:**

The proposal suggests that instead of applying transaction fees to the coinbase account’s balance after each transaction, they should be added cumulatively at the end of the block.

**Why this change?**

The current mechanism introduces a subtle dependency between transactions within a block. By shifting the transaction reward to the end of the block, we can potentially allow for new and simpler abstractions around the parallel execution of transactions without having to handle the edge case of coinbase balance read within the block.

**Implications and Considerations:**

This change will have implications for block builders and transaction bundles. For instance, block builders must accumulate transaction fees when evaluating block value. Additionally, this EIP imposes a balance requirement on the builders to be able to pay for the built block in advance, before receiving the coinbase rewards. All implications have been outlined in the `Backwards Compatibility` and `Security Considerations` sections of the EIP.

Looking forward to an enlightening discussion!

## Replies

**shemnon** (2023-10-21):

I would like to see quantified how much of a difference this makes.

- If the coinbase is an EOA, how often are transactions created or considered to be created when that EOA would show up in the same transaction
- If the coinbase is a contract, how often is the contract called within the same block it receives fees?
- for both of the above, how often do the fees received within the block make a difference?

Corollary, block building logic could act today as if this EIP were implemented and still produce valid blocks correct? Or are there occasion where the specific balance is queried and flushed out?

How much of this would influence future block builders if they couldn’t rely on fees being passed in immediately?
Couldn’t block builders just track balance deltas within the transactions they are making and assert sufficient balance while the TXes are assembled?

Clearly based on these questions I am skeptical.  Furthermore, code would need to be written to handle both post tx and post block handling within the client software for as long as we want to re-execute previous blocks, so for some clients effectively forever.  I would want to see a meaningful improvement to the ecosystem before such complexity is imposed.  I don’t see this change *in isolation* being useful for anything beyond block builders and I don’t think the impact there is sufficient to change the downstream complexity.  I may be wrong on this, which is where quantifying where it impacts or outlining other scenarios where it becomes valuable would be useful

---

**rkrasiuk** (2023-10-25):

[@shemnon](/u/shemnon) thanks for your feedback! All of your questions are valid and must be answered before proceeding with this EIP. collecting metrics for the first two questions will take some time. meanwhile, I will provide any immediate answers below.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Corollary, block building logic could act today as if this EIP were implemented and still produce valid blocks correct? Or are there occasion where the specific balance is queried and flushed out?

This EIP would not have impact on the block building routine as defined in the [Execution APIs specification](https://github.com/ethereum/execution-apis/blob/main/src/engine/paris.md#payload-building).

Regarding block builders that participate in MEV boost auction, based on the available open-source implementations, I can say that the only required change is a modification to the calculation of the block value. I cannot answer for all MEV boost block builders due to the closed source code.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> How much of this would influence future block builders if they couldn’t rely on fees being passed in immediately?

The impact was exhaustively described in the `Block Building` section under `Security Considerations`.



      [github.com](https://github.com/ethereum/EIPs/blob/fa693bc8c2b8c3fc066e9774d40b235cb3698a59/EIPS/eip-7541.md?plain=1#L119)





####



```md


1. Sender A Balance After Block: 0.7 ETH
2. Coinbase Balance After Block: 10.3 ETH
3. ```
4.
5. ## Security Considerations
6.
7. ### Double Spending
8.
9. The sender is still charged at the start of the transaction and receives the refund at the end to avoid double spending.
10.
11. ### Block Building
12.
13. **Favoring Builders With Higher Balances**
14.
15. By imposing an additional balance requirement on builders, the protocol inherently gives preference to those with more substantial balances. Builders can now bid up to their entire balance since they would receive the coinbase reward only after the payout, functioning as a refund.
16.
17. For demonstration purposes, let’s assume that we have a set of transactions in the public mempool that results in a block with value `3 ETH`  and all builders use the equivalent ordering algorithms.
18.
19. Given Builders A, B and C with respective balances `4 ETH`, `3 ETH` and `2 ETH`, Builder A is guaranteed to outbid the remaining two builders by placing a bid of `3 ETH 1 wei`.
20.
21. **Reward Distribution Between Builder And Proposer**


```










![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Couldn’t block builders just track balance deltas within the transactions they are making and assert sufficient balance while the TXes are assembled?

Correct, I believe that’s what most builders do today. The balance requirement only impacts the highest bid they can place in the auction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Furthermore, code would need to be written to handle both post tx and post block handling within the client software for as long as we want to re-execute previous blocks, so for some clients effectively forever.

Agree, the same as with most changes in the behavior of the protocol. Without arguing the complexity of keeping the client codebases backwards compatible, I would say that the implementation of this change and support of pre-EIP behavior is low effort.

---

**shemnon** (2023-10-25):

A security consideration is not a motivation or rationale.  Security considerations are what will/may happen if the EIP is adopted.  Security considerations also describe bad things that may happen, and motivation as bad things that are happening that would be fixed.  So I am quite confused by this analysis of the impact.

I also fail to see how this addresses the problem of builders with larger balance.  The extra incremental Ether available to smaller and “honest” block builders is still available to larger (and presumably dishonest?) miners.  Nothing about moving where the balance is accounted for alters this appeal against plutocracy as it is equally accessible regardless of balance, the builder would just need to adapt to the new accounting standard.

---

**rkrasiuk** (2023-10-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> A security consideration is not a motivation or rationale.

Absolutely agree. The `Security Considerations` section outlines the consequences (both intended and unintended) to various areas of the protocol as well as important protocol counterparts (MEV Boost in this case). This EIP is not different in that regard.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> I also fail to see how this addresses the problem of builders with larger balance. The extra incremental Ether available to smaller and “honest” block builders is still available to larger (and presumably dishonest?) miners.

The EIP does not address the problem but rather introduces it in the context of MEV Boost auctions. Hence it is described under `Security Considerations` section. As an unintended consequence of EIP being adopted, the extra incremental Ether becomes unavailable to either of the builders.

Respectfully, I think some parts of the EIP or its impact on the builder market have been misunderstood, so I would be glad to answer any requests for clarifications you have regarding the EIP and modify the original proposal to reflect that.

