---
source: ethresearch
topic_id: 3179
title: A trivial way for a Plasma Cash operator to exit "inflated" coins?
author: MihailoBjelic
date: "2018-09-01"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/a-trivial-way-for-a-plasma-cash-operator-to-exit-inflated-coins/3179
views: 1660
likes: 0
posts_count: 3
---

# A trivial way for a Plasma Cash operator to exit "inflated" coins?

In Plasma Cash, users don’t need/aren’t required to download and validate the whole Plasma chain, but only the proofs related to the coins they own, as explained in the original Plasma Cash post:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Plasma Cash: Plasma with much less per-user data checking](https://ethresear.ch/t/plasma-cash-plasma-with-much-less-per-user-data-checking/1298/1)

> Hence, a Plasma operator could simply maintain connections with each user, and every time they create a block they would publish to them only the proofs, not any data related to coins that they do not own.

Let’s say I’m an operator and I send a small amount of ETH (A) to the Plasma Cash contract and generate a coin of the same value (A) on the Plasma chain. What stops me form simply changing that coin’s value to a much higher one (B) and submit an exit? No one should challenge me, because everyone keeps track only of their own coins, and this coin is mine?

What am I missing?

## Replies

**sourabhniyogi** (2018-09-01):

In our implementation, when deposit A is made through calling [deposit](https://github.com/wolkdb/deepblockchains/blob/0d83413a6ea795748f574a19c31f8bf55a0ee1c1/Plasmacash/contracts/RootChain/plasmacash.sol#L95), the Layer 1 contract will store it in a `depositBalance` array; when an exit is initiated [right after the deposit (via depositExit)](https://github.com/wolkdb/deepblockchains/blob/0d83413a6ea795748f574a19c31f8bf55a0ee1c1/Plasmacash/contracts/RootChain/plasmacash.sol#L109) or [after some token transfer](https://github.com/wolkdb/deepblockchains/blob/0d83413a6ea795748f574a19c31f8bf55a0ee1c1/Plasmacash/contracts/RootChain/plasmacash.sol#L134), even if no one challenges you, only the [original domination A could be sent back to you](https://github.com/wolkdb/deepblockchains/blob/0d83413a6ea795748f574a19c31f8bf55a0ee1c1/Plasmacash/contracts/RootChain/plasmacash.sol#L215) when the exit is finalized, using the original amount recorded in the  `depositBalance` array.  No one can change the value of the  `depositBalance` array from A to a much higher value, and we have the 64-bit [tokenID hash](https://github.com/wolkdb/deepblockchains/blob/0d83413a6ea795748f574a19c31f8bf55a0ee1c1/Plasmacash/contracts/RootChain/plasmacash.sol#L93) composed of the original depositor (msg.sender), unique deposit index, and the original depositAmount (A), which is useful to verify the very first transaction as being valid.

---

**nginnever** (2018-09-01):

Ran into the same issue from a state-channels perspective while implementing a hub-and-spoke virtual channel payment network. The issue being that all users of the hub share the same contract and thus any state update could collude and drain other channels.

We prevent this in the same way as [@sourabhniyogi](/u/sourabhniyogi) does by tracking [deposits](https://github.com/finalitylabs/set-virtual-channels/blob/master/contracts/LedgerChannel.sol#L84) and [withdrawals](https://github.com/finalitylabs/set-virtual-channels/blob/master/contracts/LedgerChannel.sol#L229) on-chain in some storage of the parent contract. This way the contract would simply check that the operator never deposited ether to cover the inflated off-chain state.

