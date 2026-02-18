---
source: magicians
topic_id: 16642
title: "EIP-7557: Block-level Warming"
author: alex-forshtat-tbk
date: "2023-11-14"
category: EIPs
tags: [gas]
url: https://ethereum-magicians.org/t/eip-7557-block-level-warming/16642
views: 1621
likes: 8
posts_count: 14
---

# EIP-7557: Block-level Warming

A mechanism for a fair distribution of the gas costs associated with access to addresses and storage slots among multiple transactions with shared items in their `accessList`.

https://github.com/ethereum/EIPs/pull/9428

Old PR link:

https://github.com/ethereum/EIPs/pull/7968

## Replies

**Mani-T** (2023-11-15):

Could you please provide further elaboration on that?

---

**xinbenlv** (2023-11-15):

This sounds like an interesting direction, and economically makes sense! Love to collaborate if it helps

---

**alex-forshtat-tbk** (2023-11-16):

[@Mani-T](/u/mani-t) Sure, I updated the message with a link to the pull request with the EIP itself.

[@xinbenlv](/u/xinbenlv) thanks!

---

**Mani-T** (2023-11-17):

Great idea. Attempting to pave the way for a fairer system.

---

**sm-stack** (2023-11-18):

Great work! This will enhance the fairness of the whole Ethereum network, and also reduce gas cost significantly.

I have two questions here:

1. Is this inspired by zkSync fee refunds? I think there are slight differences, but the motivations seem to be similar.
2. In the pseudo code of reimbursement of priority fee, why do the two most expensive transactions have the same contribution to the reimbursement?

---

**PixelCircuits** (2023-11-28):

I love this. I think it’s necessary and overall fair for smart contract wallets to survive.

---

**alex-forshtat-tbk** (2025-02-28):

Note that there is now a second EIP with the same title:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nerolation/48/8553_2.png)

      [EIP-7863: Block-level Warming](https://ethereum-magicians.org/t/eip-7863-block-level-warming/22572) [EIPs](/c/eips/5)




> Discussion topic for EIP-7863
> Find an initial analysis of the EIP in the following:
>
> Update Log
>
>
> 2025-01-16 Initial Commit
>
>
> External Reviews
> None as of 2025-01-18.
> Outstanding Issues
> 2025-01-18: Clarify if block-level warming or directly move to multi-block warming
> 2025-01-18: Clarity warm-warm-for-all vs. one-warms-and-gets-refunded (costs distributed among transactions or accesses)

---

**shemnon** (2025-02-28):

I think the specification needs to clarify the timing of the reimbursement, the impact on  executing code, and the timing of funds availability.

- Does execution follow the same costing rules as before? Cold cost is the same and the same 2929/2930 warming rules apply to that cost?
- When do the accounts get their re-imbursement?  At the end of the block?  Durring the TX, right after the TX?  I think the only safe place is after all TXes occur, collectively.
- For transactions in the block after transaction, is the value that account holds going to remain the pre-reimbursement amount?  This follows directly from depositing after all transactions, but the implications may need to be called out somewhere.

I don’t think there is a sensible way other than to keep current charging rules and re-imburse at the end.  It would be possible to set up transactions that resolve differently if the marginal refund is done before the end of the block, and so a tx would resolve differently, and in ways that could impact the marginal share of warming.

---

**wminshew** (2025-03-01):

seems I missed this eip/thread – cross-posting my thoughts from the other: [EIP-7863: Block-level Warming - #16 by wminshew](https://ethereum-magicians.org/t/eip-7863-block-level-warming/22572/16)

[@alex-forshtat-tbk](/u/alex-forshtat-tbk) in your proposal, what is the benefit of taking the priority fees into account vs the ~simpler gas reduction?

---

**alex-forshtat-tbk** (2025-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> What is the benefit of taking the priority fees into account vs the ~simpler gas reduction?

It seems to me that not taking the priority fee into consideration can create a set of problems in itself. This is of course only important when the priority fee can be a significant part of the transaction’s total gas price.

In this case, not considering the priority fee and simply dividing the nominal **gas cost** of an access by the number of accesses with that address/slot may create a situation where adding a cheap transaction in the end of the block **reduces** the total earnings of the block builder.

In this case block builders may prefer to leave more gas in a block unused to avoid splitting the cold access fees, or censor certain kinds of transactions they deem “unproductive”.

What are our options regarding the priority fee in your opinion?

---

**alex-forshtat-tbk** (2025-03-03):

Thank you [@shemnon](/u/shemnon)

I tried to elaborate on some things in the EIP as well as here.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> Does execution follow the same costing rules as before?

Yes, nothing observably changes in the context of a transaction.

This helps us avoid potential problems, for example one transaction during its execution cannot “check” whether some other storage slot has already been touched in the current block by a different transaction.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> When do the accounts get their re-imbursement? At the end of the block?

Exactly. They are reimbursed as the last state change occurring in a block by a “system transaction”, and can only be observed in the next block. This prevents the refunds in one transaction affecting other transactions, which as you mentioned potentially creates a circular dependency.

---

**wminshew** (2025-03-03):

> In this case block builders may prefer to leave more gas in a block unused to avoid splitting the cold access fees, or censor certain kinds of transactions they deem “unproductive”.

without doing any kind of historical analysis, my instinct is that this is a very very rare edge case and worth accepting for the simpler execution

> What are our options regarding the priority fee in your opinion?

tbh i haven’t thought about this nearly as much as you … will marinate on it a bit

---

**alex-forshtat-tbk** (2025-03-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wminshew/48/4658_2.png) wminshew:

> my instinct is that this is a very very rare edge case and worth accepting for the simpler execution

Yes, it isn’t a significant concern for the Ethereum L1 right now, but this may theoretically change in the future or on some L2s. We didn’t want to add any additional constraints on the priority fee.

