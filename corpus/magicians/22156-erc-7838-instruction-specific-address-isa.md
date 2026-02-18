---
source: magicians
topic_id: 22156
title: "ERC-7838: Instruction Specific Address (ISA)"
author: ss-sonic
date: "2024-12-10"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7838-instruction-specific-address-isa/22156
views: 506
likes: 9
posts_count: 9
---

# ERC-7838: Instruction Specific Address (ISA)

The Instruction Specific Address (ISA) standard introduces a mechanism for approval-less interactions with decentralised applications (DApps) through dynamically generated single-use contract addresses. This standard enables seamless and secure DApp interactions without requiring wallet connections, approvals, or plugin dependencies, enhancing usability, security, and accessibility.

PR:



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/762)














####


      `master` ← `router-protocol:master`




          opened 06:58PM - 10 Dec 24 UTC



          [![](https://ethereum-magicians.org/uploads/default/original/2X/1/171116128f4f5b48c91e33b57805efd5458b45e7.png)
            ss-sonic](https://github.com/ss-sonic)



          [+454
            -0](https://github.com/ethereum/ERCs/pull/762/files)







**ERC-7838: Instruction Specific Address (ISA)**

The Instruction Specific Add[…](https://github.com/ethereum/ERCs/pull/762)ress (ISA) standard introduces a mechanism for approval-less interactions with decentralized applications (DApps) through dynamically generated single-use contract addresses. This standard enables seamless and secure DApp interactions without requiring wallet connections, approvals, or plugin dependencies, enhancing usability, security, and accessibility.

## Replies

**wjmelements** (2024-12-11):

> // Emit event for failed transaction

If you’re reverting, the event won’t persist.

---

**ss-sonic** (2024-12-11):

The transaction does not revert in the `processCallOps` function itself. Instead, it gracefully handles the failed call and explicitly emits the ExecutionFailed event.

Since the emit statement is outside the reverted call’s context, it is part of the main transaction’s execution and will be recorded in the transaction logs.

---

**wjmelements** (2024-12-12):

```auto
        if (!success) {
            // Emit event for failed transaction
            // Revert with the original error data
            assembly {
                let ptr := mload(0x40)
                let size := returndatasize()
                returndatacopy(ptr, 0, size)
                revert(ptr, size)
            }
        }
```

that comment appears in a block that reverts.

---

**ss-sonic** (2024-12-12):

True, need to handle this properly. These are just examples of philosophy that ERC is trying to expand on, but point noted.

---

**chaandflower** (2024-12-16):

Could ISAs render traditional wallet-based UX paradigms obsolete, what new UX standards might emerge as a result?

---

**radek** (2024-12-17):

> Self-Destruction:
>
>
> After execution or refund, the ISA self-destructs to free resources and ensure it cannot be reused.

> ```
>     selfdestruct(payable(refundRecipient));
> ```

I assume it is in conflict with the roadmap wrt selfdestruct.

---

**ip11** (2024-12-17):

does ERC-7838 ensure ISAs can’t be reused if selfdestruct is removed?

---

**ss-sonic** (2024-12-19):

The ISA does not rely on `selfdestruct`. It uses it for gas refunds during contract creation, but it would still function without it, though it would result in slightly higher gas fees for the relayer.

