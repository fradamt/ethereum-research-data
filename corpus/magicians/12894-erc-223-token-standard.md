---
source: magicians
topic_id: 12894
title: ERC-223 Token Standard
author: Dexaran
date: "2023-02-09"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-223-token-standard/12894
views: 3402
likes: 2
posts_count: 13
---

# ERC-223 Token Standard

---

ERC-223 hub. Here you can track the progress and find all the necessary resources about ERC-223 standard: https://dexaran.github.io/erc223/

---

## eip: 223
title: ERC-223 Token
description: Token with event handling and communication model
author: Dexaran ()
status: Review
type: Standards Track
category: ERC
created: 2017-05-03

## Simple Summary

A standard interface for tokens with definition of `communication model` logic. I am creating this issue here because I want to submit a final PR to the EIPs repo and it requires a link to this forum now.

Old discussion thread with 600+ comments from developers can be found under EIP223

This alternative token standard is designed to solve the security problems of ERC-20.

ERC-20 standard violates two of the core software security principles - (1) it doesn’t allow for error handling and (2) it violates the principle of failsafe defaults.

As the result, Ethereum token users are suffering financial damage. Since 2017 $108,000,000 worth of ERC-20 tokens were lost because of this security flaws in the standard, here is the script that calculates and displays this data:


      ![](https://dexaran.github.io/erc20-losses/static/favicon.ico)

      [dexaran.github.io](https://dexaran.github.io/erc20-losses/)





###



ERC-20 token standard contains a security flaw in its transferring workflow. As the result a user can lose their funds.










ERC-20 approve & transferFrom pattern was designed to make tokens unaffected by 1024-call-stack-depth EVM bug in 2015. That bug was fixed in 2017 so the approve & transferFrom pattern is currently redundant and poses a direct threat to users safety. $4,1B worth of ERC-20 tokens were lost due to permit & approval scams in 2024.

Explanation of the approvals problem: [Re-add ERC-223 to token standards. · Issue #10854 · ethereum/ethereum-org-website · GitHub](https://github.com/ethereum/ethereum-org-website/issues/10854#issuecomment-1679275590)

ERC-223 standard eliminates approvals and solves security problems of ERC-20 which caused users to lose $108M to lack of error handling and $4.1B to approval scams in 2024.

## Abstract

The following describes standard functions a token contract and contract working with specified token can implement. This standard introduces a communication model which allows for the implementation of event handling on the receiver’s side.

## Motivation

1. This token introduces a communication model for contracts that can be utilized to straighten the behavior of contracts that interact with tokens as opposed to ERC-20 where a token transfer could be ignored by the receiving contract.
2. This token is more gas-efficient when depositing tokens to contracts.
3. This token allows for _data recording for financial transfers.

## Rationale

This standard introduces a communication model by enforcing the `transfer` to execute a handler function in the destination address. This is an important security consideration as it is required that the receiver explicitly implements the token handling function. In cases where the receiver does not implements such function the transfer MUST be reverted.

This standard sticks to the push transaction model where the transfer of assets is initiated on the senders side and handled on the receivers side. As the result, ERC223 transfers are more gas-efficient while dealing with depositing to contracts as ERC223 tokens can be deposited with just one transaction while ERC20 tokens require at least two calls (one for `approve` and the second that will invoke `transferFrom`).

- ERC-20 deposit: approve ~53K gas, transferFrom ~80K gas
- ERC-223 deposit: transfer and handling on the receivers side ~46K gas

This standard introduces the ability to correct user errors by allowing to handle ANY transactions on the recipient side and reject incorrect or improper transactions. This tokens utilize ONE transferring method for both types of interactions with tokens and externally owned addresses which can simplify the user experience and allow to avoid possible user mistakes.

One downside of the commonly used ERC-20 standard that ERC-223 is intended to solve is that ERC-20 implements two methods of token transferring: (1) `transfer` function and (2) `approve + transferFrom` pattern. Transfer function of ERC20 standard does not notify the receiver and therefore if any tokens are sent to a contract with the `transfer` function then the receiver will not recognize this transfer and the tokens can become stuck in the receivers address without any possibility of recovering them.

ERC223 standard is intended to simplify the interaction with contracts that are intended to work with tokens. ERC-223 utilizes “deposit” pattern similar to plain Ether depositing patterns - in case of ERC-223 deposit to the contract a user or a UI must simply send the tokens with the `transfer` function. This is one transaction as opposed to two step process of `approve + transferFrom` depositing.

This standard allows payloads to be attached to transactions using the `bytes calldata _data` parameter, which can encode a second function call in the destination address, similar to how `msg.data` does in an Ether transaction, or allow for public loggin on chain should it be necessary for financial transactions.

## Specification

Token

Contracts that works with tokens

### Methods

NOTE: An important point is that contract developers must implement `tokenReceived` if they want their contracts to work with the specified tokens.

If the receiver does not implement the `tokenReceived` function, consider the contract is not designed to work with tokens, then the transaction must fail and no tokens will be transferred. An analogy with an Ether transaction that is failing when trying to send Ether to a contract that did not implement `function() payable`.

#### totalSupply

```js
function totalSupply() constant returns (uint256 totalSupply)

```

Get the total token supply

#### name

```js
function name() constant returns (string _name)

```

Get the name of token

#### symbol

```js
function symbol() constant returns (bytes32 _symbol)

```

Get the symbol of token

#### decimals

```js
function decimals() constant returns (uint8 _decimals)

```

Get decimals of token

#### standard

```js
function standard() constant returns (string _standard)

```

Get the standard of token contract. For some services it is important to know how to treat this particular token. If token supports ERC223 standard then it must explicitly tell that it does.

This function **MUST** return “erc223” for this token standard. If no “standard()” function is implemented in the contract then the contract must be considered to be ERC20.

#### balanceOf

```js
function balanceOf(address _owner) constant returns (uint256 balance)

```

Get the account balance of another account with address _owner

#### transfer(address, uint)

```js
function transfer(address _to, uint _value) returns (bool)

```

Needed due to backwards compatibility reasons because of ERC20 transfer function doesn’t have `bytes` parameter. This function must transfer tokens and invoke the function `tokenReceived(address, uint256, bytes calldata)` in `_to`, if _to is a contract. If the `tokenReceived` function is not implemented in ` _to` (receiver contract), then the transaction must fail and the transfer of tokens should be reverted.

#### transfer(address, uint, bytes)

```js
function transfer(address _to, uint _value, bytes calldata _data) returns (bool)

```

function that is always called when someone wants to transfer tokens.

This function must transfer tokens and invoke the function `tokenReceived (address, uint256, bytes)` in `_to`, if _to is a contract. If the `tokenReceived` function is not implemented in ` _to` (receiver contract), then the transaction must fail and the transfer of tokens should not occur.

If `_to` is an externally owned address, then the transaction must be sent without trying to execute ` tokenReceived` in `_to`.

`_data` can be attached to this token transaction and it will stay in blockchain forever (requires more gas). `_data` can be empty.

NOTE: The recommended way to check whether the `_to` is a contract or an address is to assemble the code of ` _to`. If there is no code in `_to`, then this is an externally owned address, otherwise it’s a contract.

### Events

#### Transfer

```js
event Transfer(address indexed _from, address indexed _to, uint256 _value)

```

Triggered when tokens are transferred. Compatible with ERC20 `Transfer` event.

#### TransferData

```js
event TransferData(bytes _data)

```

Triggered when tokens are transferred and logs transaction metadata. This is implemented as a separate event to keep `Transfer(address, address, uint256)` ERC20-compatible.

## Contract that is intended to receive ERC223 tokens

```js
function tokenReceived(address _from, uint _value, bytes calldata _data)

```

A function for handling token transfers, which is called from the token contract, when a token holder sends tokens. `_from` is the address of the sender of the token,` _value` is the amount of incoming tokens, and `_data` is attached data similar to` msg.data` of Ether transactions. It works by analogy with the fallback function of Ether transactions and returns nothing.

NOTE: `msg.sender` will be a token-contract inside the `tokenReceived` function. It may be important to filter which tokens are sent (by token-contract address). The token sender (the person who initiated the token transaction) will be `_from` inside the` tokenReceived` function.

IMPORTANT: This function must be named `tokenReceived` and take parameters` address`, `uint256`,` bytes` to match the [function signature](https://www.4byte.directory/signatures/?bytes4_signature=0xc0ee0b8a) `0xc0ee0b8a`.

## Security Considerations

This token utilizes the model similar to plain Ether behavior. Therefore replay issues must be taken into account.

## Copyright

Copyright and related rights waived via CC0

## Replies

**SamWilsn** (2023-02-10):

[Original discussion thread](https://github.com/ethereum/eips/issues/223)

---

**bear2525** (2023-08-09):

Doesn’t ERC-777 already address the issues raised in this EIP, while also remaining backwards compatible with ERC-20?

---

**Mani-T** (2023-08-10):

But its status shows that “This EIP is in the process of being peer-reviewed”. ([ERC-223 Token Standard](https://ethereum-magicians.org/t/erc-223-token-standard/12894))

---

**bear2525** (2023-08-10):

Yes, and I’m wondering what you can do with this standard that you can’t already do with ERC-777 and a bunch of other similar ones?

---

**Dexaran** (2023-08-13):

ERC-223 token is designed to behave identical to plain ether. Ether is not prone to ERC-20 problems i.e. you can’t lose token due to lack of transaction handling because transaction handling is implemented in ether transfers.

ERC-777 does not work similar to ether. It works in a different way (that I would call centralized).

---

**guotie** (2023-11-14):

This is very useful, especially for payments.

For example, If merchants want to receive USDT payment,  they cannot distinguish who have paid.

with `transfer(address to, uint amount, bytes calldata data)` method, user can fill data with orderId, so the merchants can easily confirm which order have paid.

It is a big step for crypto payments!

---

**guotie** (2023-11-14):

Also, for central instructions, like exchange, they give every user a unique address for deposit, when user deposited, the transfer assets from the user’s deposit address to their hot/cold wallet address.

If use `transfer(address to, uint amount, bytes calldata data) ` method, the param data can be user’s ID, so they just use one or several address for all user’s deposit, this will save many many transactions, and save many many gas!

---

**matejcik** (2023-12-18):

While you’re designing a new token standard, it would be nice to take into account the spam issues. In particular, disallow zero-token transfers out of other users’ wallets.

The ERC20 spec explicitly requires that zero-token transfers are allowed, which is fine, but they should be restricted to (a) the owner of the source address or (b) contracts with non-zero allowance. The current state leads to users’ wallet histories being spammed with address poisoning transfer that they didn’t make.

Not sure how far a *spec* can go in this direction, but adding it explicitly and implementing it in the reference implementation would be nice.

(While we’re at it, another item on my wishlist is committing to token symbol & decimals in the transaction signature. That would allow a hardware wallet to just ask the untrusted host to tell it tokens & decimals, and if the host computer is lying, the signed transaction will fail. But I don’t see a way to accomplish that in a spec either, so just throwing it out there.)

---

**KK779** (2024-12-23):

ERC223 doesn’t have the spam issue you’re talking about because the spam is related to `transferFrom()`. The entire point is to not use `transferFrom()` and to have the token make the call.

As for embedding token metadata into the transaction, any token can have the same metadata as another token. Only the contract address has any use as an identifier.

I’m currently trying to implement this token standard but I still want it to work as an ERC20. I understand the purpose is to prevent losses due to the design of ERC20 but I think it’s more dangerous to change a spec once it’s already finalized. More specifically, rejecting a `transfer(address,uint)` if the recipient is a contract and doesn’t implement `tokenReceived()`. Again I understand this was probably the author’s main purpose for this standard but I think even without this, this token has many benefits over ERC20:

1. ERC20 approves my tokens for ANY of the functions within the contract not just one. ERC223 means my tokens only go to the specified function. Now that contracts are expensive to deploy, I’m seeing protocols heavily dump all functions into one contract and it scares me.
2. ERC20 even with PERMIT2 still requires additional SLOAD and SSTORE. (maybe this is less of an issue with TLOAD and TSTORE if we’re using it for permit2. If anyone has implemented this please let me know). Solady’s ERC20 implementation has infinite approval but that also sounds dangerous.
3. ERC20 with PERMIT2 still requires two signatures for most implementations unless we start letting the owner of our recipient contracts handle the second transaction. Is this what we really want? I feel like for cases where we don’t have to, we shouldn’t and just use ERC223 because there’s less variables to deal with. (also again, I don’t like that permit() doesn’t include the function signature)

---

**Dexaran** (2024-12-23):

> While you’re designing a new token standard, it would be nice to take into account the spam issues. In particular, disallow zero-token transfers out of other users’ wallets.

Transfers of zero tokens must be considered valid. This is critical for introspection - if a contract doesn’t know if some token is ERC-20 or ERC-223 then it can transfer 0 tokens and if the `tokenReceived` function was invoked then the transferred token was ERC-223. Otherwise it was ERC-20. This is the only reliable method of introspection because ERC-165 only takes into account the function signatures while the difference between ERC-20 and ERC-223 tokens is in the logic of the transfer, even though function signatures can be the same.

---

**Dexaran** (2024-12-23):

> The entire point is to not use transferFrom() and to have the token make the call.

Yes, this is correct.

> rejecting a transfer(address,uint) if the recipient is a contract and doesn’t implement tokenReceived()

This is absolutely necessary to implement a token in a secure way. ERC-20 is an insecure standard.

In long term a global financial system can not be settled on top of an inherently insecure technology that violates two of the most basic software security principles (“error handling” and “failsafe defaults”) and as the result entails financial damage to customers ($108M were lost due to lack of error handling in 2024 [ERC-20 Losses Calculator](https://dexaran.github.io/erc20-losses/) and $4.1B were lost to approval-related problems since 2017).

All ERC-20 compatible tokens are insecure. It’s impossible to design a secure token without asserting the failsafe behaviour of the transferring mechanism.

If you want a ERC-223-like token that doesn’t require handling of the `transfer(address, uint)` function then it will not be ERC-223 compatible. It is possible to implement a token this way but it must be called a modification of ERC-223. Like there was ERC-721A.

---

**KK779** (2024-12-24):

Thanks for your suggestion. I never understood why it was called ERC-721A but now I do. I will go ahead and rename my implementation ERC-223L. The L will stand for the name of my protocol: Lindy Protocol.

I understand ERC-20’s issues and certainly your solution would prevent them but at what cost? What if I *want* to transfer the token to a contract that hasn’t implemented `tokenReceived()`? I *could* create another function for this purpose but I would say it’s more intuitive that `transfer()` would do what I want and I very well might have a contract that automatically assumes that behavior.

What if instead of solving it on-chain, we warn/block the transfer at a higher level (rpc provider, wallets, or api) and not on-chain? I also think the ERC-20 page needs to either add or link to a “Security Considerations” section.

