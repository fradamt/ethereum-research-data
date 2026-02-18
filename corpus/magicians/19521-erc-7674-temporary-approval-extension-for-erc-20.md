---
source: magicians
topic_id: 19521
title: "ERC-7674: Temporary Approval Extension for ERC-20"
author: xshape
date: "2024-04-03"
category: ERCs
tags: [erc-20, transient-storage]
url: https://ethereum-magicians.org/t/erc-7674-temporary-approval-extension-for-erc-20/19521
views: 1412
likes: 11
posts_count: 13
---

# ERC-7674: Temporary Approval Extension for ERC-20

Among all cases of `ERC-20` token transactions, a popular one is when smart contracts approve token spending to other contracts. Often tokens are approved for only one transaction.

Following the `ERC-20` standard, if a smart contract wants to approve the spending of tokens to another smart contract for only one transaction, this causes the allowance saved in storage to be updated and retrieved.

Token allowances utilising `EIP-1153` transient storage are a cheaper alternative to the regular storage allowances.

We suggest adding a new `ERC-7674`: [GitHub PR](https://github.com/ethereum/ERCs/pull/358).

[Proposed implementation](https://github.com/byshape/transient-token/blob/main/contracts/TransientToken.sol)

## Replies

**wjmelements** (2024-04-03):

> Slot MAY be derived as keccak256(spender . keccak256(owner . p)) where . is concatenation and p is keccak256 from the string uniquely defining transient allowances in the namespace of the implementing contract.

I have a preference for the transient allowance using the same slot as stored allowance to reduce the number of necessary hashes. Hash operations are likely to cost more gas in the future.

---

**ownerlessinc** (2024-04-04):

Hey [@xshape](/u/xshape)

I reviewed the contract files you submitted, nice work!

If I may suggest a few changes and also ask you the ‘why’ of the way some things were composed:

`msg.sender` is never the zero address, so [L28](https://github.com/byshape/transient-token/blob/202e4d01c8410af3bab52e1fa2a938cdccde9f2f/contracts/TransientToken.sol#L28) can be removed. I see you used vm.prank(address(0) and such context is only valid by manipulating the VM but it can’t happen on mainnet.

When calling the name of a function as in [L42](https://github.com/byshape/transient-token/blob/202e4d01c8410af3bab52e1fa2a938cdccde9f2f/contracts/TransientToken.sol#L42), I believe the industry standard asks you to write the name of the contract upfront like {ERC20-approve}

There was a particular reason to choose the following formula to generate the unique slot hash?

`keccak256(spender . keccak256(owner . p))`

I recommend using the same order as the input parameters of the `_getTransientSlot` function, reducing the hash into `keccak256(owner . spender))`. Since `spender` and `owner` are unique to their transaction contexts and since there is only one available spender for each owner, I don’t think the constant is necessary.

The function named `_getTransientSlot` might be misleading. Its purpose is purely to generate the hash, while the functions named `_getTransientAllowance` and `_setTransientAllowance` are the ones storing/loading from the transient storage. I recommend changing the getter/setter function names from `TransientAllowance` into `TransientSlot` and the `_getTransientSlot` into something related to the hash generation.

The function `_getTransientAllowance` returns an uint256 but the variable is named `allowed`, to avoid misleading nomenclature I recommend changing it into `value`.

In [L46](https://github.com/byshape/transient-token/blob/202e4d01c8410af3bab52e1fa2a938cdccde9f2f/contracts/TransientToken.sol#L46) it’s been checked if `transientAllowance` equals to max uint256. This verification already occurs inside `Math.tryAdd` where, in case it overflows (because it is max uint256) the Math lib will return false, which will set the return as max unit256 because of the ternary validating the returned boolean. I recommend deleting L46, L47, L48 as it seems they are not doing anything.

Let me know if I can be more helpful ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**xshape** (2024-04-04):

I think the best option is to leave this decision to those implementing the standard. Do you have a version of the wording that would be more appropriate in this case?

---

**xshape** (2024-04-04):

Hi, thank you for your feedback.

> msg.sender is never the zero address, so L28 can be removed. I see you used vm.prank(address(0) and such context is only valid by manipulating the VM but it can’t happen on mainnet.

This is a sanity check to filter out clearly incorrect return of the `_msgSender` function that can be overridden.

> I recommend using the same order as the input parameters of the _getTransientSlot function, reducing the hash into keccak256(owner . spender)).

Because in the proposed version the slot index depends only on `owner` and `spender`, the probability of collision is increased. Unrelated functionality can use exactly the same approach to derive the slot index for its needs. Adding a unique `p` helps reduce the risk of collision.

> I recommend changing the getter/setter function names from TransientAllowance into TransientSlot and the _getTransientSlot into something related to the hash generation.

As you pointed out above in the message, the getter and setter functions are getting/setting the value from/to the slot, not the slot id. `_getTransientSlot` function calculates the slot id. The fact that it uses hash is an implementation detail and can be concealed.

> The function _getTransientAllowance returns an uint256 but the variable is named allowed, to avoid misleading nomenclature I recommend changing it into value.

The variable name `allowed` may suggest a boolean data type, it may be worth using `amount`/`value` instead, agree.

> I recommend deleting L46, L47, L48 as it seems they are not doing anything.

If the temporary allowance is `type(uint256).max`, there is no point in doing an extra `sload` to get an overflow.

---

**SamWilsn** (2024-06-10):

Bit of bikeshedding but instead of `temporaryApprove`, how about `temporarilyApprove`? It’s a bit more natural sounding, since “approve” is a verb so the describing word should be an adverb.

---

**SamWilsn** (2024-06-10):

In the function:

> ```auto
> function temporaryApprove(address spender, uint256 value) public returns (bool success)
> ```

why return a `bool`? Hasn’t that been a problem with ERC-20 forever (necessitating, for example, [SafeERC20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/utils/SafeERC20.sol))?

I’d just specify that the function reverts on failure, and not return anything.

---

**SamWilsn** (2024-06-10):

I don’t know how feasible it would be, but for smart contract wallets implementing batch functionality, would it be possible to have a `clearAllTemporaryApprovals` function that emulates ending the transaction?

---

**Amxx** (2024-07-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Hasn’t that been a problem with ERC-20 forever

The problem is not the standard asking for a return value. The problem is some (important) implementation not following the standard, and not returning anything.

Having a function that doesn’t return anything is possibly an issue if the contract that implements it also has some receive/fallback that doesn’t revert (and possibly does nothing)

---

**SamWilsn** (2024-07-22):

Good point. IMO it would make sense to return a constant and revert on failure then.

---

**xshape** (2025-01-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> It’s a bit more natural sounding, since “approve” is a verb so the describing word should be an adverb.

While `temporarilyApprove` is grammatically more correct, `temporaryApprove` simpler, shorter and less prone to typos. I lean towards keeping it as `temporaryApprove`, even though it’s not the perfect grammatical form.

---

**xshape** (2025-01-12):

We can always consider such extensions later if there’s proven demand from smart contract wallet implementations.

---

**MASDXI** (2025-01-13):

I think it’d be good to mention that this function works more like a Just-In-Time (JIT) system, where approvals happen right when needed. It’d help make it clear that `temporaryApprove` is different from `permit` and the regular `approve`.

