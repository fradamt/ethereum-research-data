---
source: magicians
topic_id: 15222
title: "EIP-7410: Decrease Allowance By Spender"
author: zakrad
date: "2023-07-26"
category: EIPs
tags: [erc20]
url: https://ethereum-magicians.org/t/eip-7410-decrease-allowance-by-spender/15222
views: 1970
likes: 14
posts_count: 12
---

# EIP-7410: Decrease Allowance By Spender

## Abstract

This extension adds a update allowance mechanism to ERC-20 allowances, in which a spender can revoke or decrease a given allowance by a specific address. This EIP extends EIP-20.

## Motivation

Currently, ERC-20 tokens offer allowances, enabling token owners to authorize spenders to use a designated amount of tokens on their behalf. However, the process of decreasing an allowance is limited to the owner’s side, which can be problematic if the token owner is a treasury wallet or a multi-signature wallet that has granted an excessive allowance to a spender. In such cases, reducing the allowance from the owner’s perspective can be time-consuming and challenging.

To address this issue and enhance security measures, this EIP proposes allowing spenders to decrease or revoke the granted allowance from their end. This feature provides an additional layer of security in the event of a potential hack in the future. It also eliminates the need for a consensus or complex procedures to decrease the allowance from the token owner’s side.

### Interface implementation

```solidity
pragma solidity ^0.8.0;

/**
 * @title ERC-20 Update Allowance By Spender Extension
 * Note: the ERC-165 identifier for this interface is 0x2d474b5c
 */
interface IERC20ApproveBySpender is IERC20 {

    /**
     * @notice Updates any allowance by `owner` address for caller.
     * Emits an {IERC20-Approval} event.
     *
     * Requirements:
     * - `owner` cannot be the caller.
     * - `amount` should be less than or equal to current allowance of `owner` for caller.
     */
    function approveBySpender(address owner, uint256 amount) external;

}
```

The `approveBySpender(address owner, uint256 amount)` function MUST be either `public` or `external`.

The `Approval` event MUST be emitted when `approveBySpender` is called.

The `supportsInterface` method MUST return `true` when called with `0x2d474b5c`.

## Rationale

The name “EIP-20 Approval By Spender Extension” was chosen because it is a succinct description of this EIP. Spenders can decrease or revoke their allowance by `amount` from `owner`s.

By having a way to approve and revoke in a manner similar to EIP-20, the trust level can be more directly managed by spender:

- Using the approveBySpender function, spenders can revoke or decrease their allowance to spend an amount.

The EIP-20 name patterns were used due to similarities with EIP-20 approvals.

## Backwards Compatibility

This standard is compatible with EIP-20.

## Replies

**RenanSouza2** (2023-07-26):

if I have allowance couldnt I just transferfrom(from, from, amount)?

---

**zakrad** (2023-07-27):

Yes, but in that case the `from` should have `amount` in his balance. `amount` can be greater than owner balance.

---

**radek** (2023-07-30):

I understand the use case.

Yet, I am not in favour of this form.

The ERC 20 approve of the absolute value was a  mistake resulting in losses.

The suggested workaround is to first set allowance to 0, then to new value , or by having extension providing increaseAllowance / decreaseAllowance - i.e. working with deltas.

I suggest this ERC would be changed to decreaseAllowanceBySpender(owner, amount), where whatever amount larger than current allowance would effectively revoke allowance. This would be reflected also for amount = type(uint256).max which would nullify commonly used unlimited approval when set to max uint.

---

**radek** (2023-07-30):

“Decrease” allowance in the EIP name  would also make it semantically clear that this function cannot set allowance arbitrarily ( as could be understood using “Update” word.

---

**zakrad** (2023-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/radek/48/16714_2.png) radek:

> decreaseAllowanceBySpender

I agree. This improve clarity for the name.

---

**radek** (2023-08-10):

This has another impact - you are effectively doing transfer and emitting Transfer event.

This might not be desired by the use case.

---

**radek** (2023-08-10):

thanks for the update.

Additionally, Is this validation really required?

```
 * Requirements:
 * - `owner` cannot be the caller.
```

ERC20 standard does not have such limitation. So no validation code is required.

---

**radek** (2023-08-10):

I would reflect my above mentioned points replacing this

```auto
* - `subtractedValue` should be less than or equal to current allowance of `owner` for caller.
```

with

```auto
* - when `subtractedValue` is equal or higher than current allowance of spender the new allowance is set to 0.
* Nullification also MUST be reflected for current allowance being type(uint256).max.
```

---

**zakrad** (2023-08-10):

Thanks for your feedback again, updated.

---

**asghaier** (2023-11-30):

I am not sure I am following on the use case and how applicable it will be in different scenarios. since the spender is the one to call the ‘decreaseAllowanceBySpender’ function that means another call to be paid for by the spender which in most cases is not a desirable approach for the spender and will result in few cases where this is going to be used (the spender is another wallet that is related to the approver).

I think this same use case be solved with hooks that will ensure that every transferFrom is triggering decreasing the allowance amount by how much was transferred. I think OZ v.4 used the _afterTokenTransfer hook which is now _update, so extending that hook to decrease the allowance will ensure that this will take place as the token amount being transferred and become decreased from the allowance amount and will require no extra txn by the spender (gas for that extra logic will still be accounted for in that same transaction where the spender was motivated in most cases to pay gas at first place).

---

**zakrad** (2023-12-01):

This functionality primarily addresses scenarios where the owner has granted an excessive allowance, necessitating consensus for any transaction and the gas might not be an issue compared to the effort. The proposed solution using `transferFrom` as mentioned above encounters a issue where the `from` address must have a sufficient balance, which may not always be the case. This functionality mitigates the risk of potential attacks on the owner’s wallet if the spender’s wallet is exposed. Moreover, the emitted Transfer events in the suggested approach could be misleading.

