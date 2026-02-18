---
source: magicians
topic_id: 6884
title: New Token is called ERC25
author: Dream
date: "2021-08-16"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/new-token-is-called-erc25/6884
views: 733
likes: 1
posts_count: 2
---

# New Token is called ERC25

I have an idea to make a new token that is called ERC25.

But I don’t know how to do it.

I hope to do it successfully.

I haven’t any solution how to begin and how to make progress.

I want to know whether it is possible and if so, where should I begin.

Are there ERC tokens in core-go Ethereum code.

If yes, where are there.

My token protocol is following.

Ethereum Core Protocol.

-expiration

on token creation, the expiration is set to 600 for example.

When block 600 is created, baked EVM code (or validator, whichever method is used) will review the ‘deposit’ field.

if there is sufficient balance in the ‘deposit’ field. That amount is subtracted, and the expiration is increased by X (in this case, 100) to 700. And that is all.

at block 501, if clients see the token still with ‘expiration’ of 500 which has passed. it knows it is safe to ‘purge’ the data field from the local blockchain.

EVM has a similar function to this ‘purge’ called selfdestruct()



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/315/why-are-selfdestructs-used-in-contract-programming)



      [![high110](https://www.gravatar.com/avatar/7d74b22db66a2e5cc0880881ce0ee017?s=256&d=identicon&r=PG&f=y&so-version=2)](https://ethereum.stackexchange.com/users/181/high110)

####

  **contract-design, selfdestruct**

  asked by

  [high110](https://ethereum.stackexchange.com/users/181/high110)
  on [10:56PM - 21 Jan 16 UTC](https://ethereum.stackexchange.com/questions/315/why-are-selfdestructs-used-in-contract-programming)










-test

Since it requires use of Eth2 cod, “regular mining” for a test network would not work. You will have to set up an Eth2 test network."

-scenario

if a user makes an ERC-25 contract to create the mutable data tokens, i am not sure if it is possible to have an optional field for the token creation side on placing the deposit amount.

I think that would be too hard and too much work

So once a user makes the contract, and goes to make a data token.

After it is made;

We will have a special functions for all ERC-25 fungible data tokens.

1. Deposit()
any address can send funds into the deposit field. (the network will return any amount over the MAX DEPOSIT) [ MAX DEPOSIT = 2x STORAGE COST
2. Update()
the owner of the token make submit the Update() function and replace the data in the token. (This is how we make it mutable)
3. Destroy()
The owner of the token may submit to destroy() function. Any amount in DEPOSIT is sent to the owner and the EXPIRATION is set to the current block (if accepted)
-result
You should submit the daily report and also provide me the weekly report using excel file on Friday/Saturday.

## Replies

**asmbyk** (2025-07-19):

![:test_tube:](https://ethereum-magicians.org/images/emoji/twitter/test_tube.png?v=15) ERC-69: The Meme Burn Standard

## Summary

**ERC-69** is a community-driven token standard designed to introduce **transaction-based burn logic** for memecoins. It extends the ERC-20 token interface with optional hooks that apply token burns on **buys**, **sells**, and **transfers**, inspired by Ethereum’s own EIP-1559 burn mechanism.

This standard provides a simple, modular, and meme-native way to introduce **deflationary pressure** through interaction, aligning with the fast-paced, high-velocity nature of meme economies.

---

## Motivation

Ethereum’s **EIP-1559** introduced a powerful mechanism where a portion of gas fees is **burned**, resulting in **net negative issuance** of ETH. Since launch, over **400,000 ETH** has been burned, driving a narrative of **ultrasound money**.

Memecoins, however, often rely solely on speculative attention, lacking structural incentives or supply discipline. ERC-69 fills this gap by defining a lightweight, consistent **burn standard** for token interactions — ensuring that every **buy, sell, or transfer** reduces supply and rewards holders.

It is both a technical pattern and a cultural meme.

---

## Specification

###  Interface Overview

solidity

KopyalaDüzenle

```auto
interface IERC69 {
    function buyBurnRate() external view returns (uint256);      // 0-100 (%)
    function sellBurnRate() external view returns (uint256);     // 0-100 (%)
    function transferBurnRate() external view returns (uint256); // 0-100 (%)
    function isERC69Compliant() external pure returns (bool);    // returns true
}
```

> All rates are defined in whole percentages. A 5% burn would be represented as 5.

The standard is intentionally minimalist and compatible with ERC-20. Optional additions (see Extensions) may include view functions like `gm()`, `cope()`, or temporary modifiers like `69mode()`.

---

## Burn Logic Example

###  Suggested Internal Transfer Function

solidity

KopyalaDüzenle

```auto
function _transfer(address from, address to, uint256 amount) internal override {
    uint256 burnAmount;

    if (from == uniswapPair) {
        // Buy
        burnAmount = amount * buyBurnRate / 100;
    } else if (to == uniswapPair) {
        // Sell
        burnAmount = amount * sellBurnRate / 100;
    } else {
        // Transfer
        burnAmount = amount * transferBurnRate / 100;
    }

    uint256 sendAmount = amount - burnAmount;
    super._transfer(from, BURN_ADDRESS, burnAmount);
    super._transfer(from, to, sendAmount);
}
```

> uniswapPair is the address of the DEX liquidity pool; this can be extended to multiple DEXes or generalized logic.

---

## Features

### Core

- Burn on Buy/Sell/Transfer
- Designed for memecoin ecosystems
- Purely opt-in, no enforcement required by L1
- Compatible with ERC-20

### Optional Extensions (Meme Layer)

- function gm() public pure returns (string memory)

> Returns: "we vibin fr"

- function cope()

> Emits DumpEvent(address indexed seller, uint256 amount)

- function activate69mode()

> Temporarily increases all burn rates to 69% for viral events

---

## Use Cases

###  Ideal For:

- Memecoins with high volume and speculative energy
- Projects seeking controlled deflation
- DEX-launched community tokens
- Burn-based staking or gameFi ecosystems

---

## Examples in the Wild

- $FART69 – burns 6.9% on all transfers
- $MEMECOIN420 – applies 10% burn only on sells
- $COPE – reactive burn system with cope() events
- $GASLIGHT – dynamic burn rate based on block volatility

A public registry for ERC-69-compliant tokens is being developed.

---

## Benefits

| Technical | Cultural |
| --- | --- |
| Standardizes burn logic | “Burn to earn” meme |
| Modular & composable | Aligns with degeneracy |
| DEX-compatible | Deflation as entertainment |
| Open source, free to adopt | Gamifies every TX |

