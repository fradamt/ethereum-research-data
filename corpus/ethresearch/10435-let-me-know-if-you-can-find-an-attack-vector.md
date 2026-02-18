---
source: ethresearch
topic_id: 10435
title: Let me know if you can find an attack vector
author: Econymous
date: "2021-08-27"
category: Economics
tags: [governance, dao, sidechain]
url: https://ethresear.ch/t/let-me-know-if-you-can-find-an-attack-vector/10435
views: 1505
likes: 1
posts_count: 3
---

# Let me know if you can find an attack vector

So this has been coded. The resolve token mentioned is what I’m asking people to attack. It’s the asset that governs the oracle/DAO (potentially sidechain).

[![](https://ethresear.ch/uploads/default/original/2X/d/d56104a2ca876570a30cbbc673973f9a1de92306.jpeg)469×270 46.1 KB](https://ethresear.ch/uploads/default/d56104a2ca876570a30cbbc673973f9a1de92306)

We first start with something that is a blatant pyramid. A user can buy into the smart contract and receive bonds. Those who buy early, get bonds cheaper than those who buy later on.

[![](https://ethresear.ch/uploads/default/original/2X/c/c0be63b7e948da68a177a450db277dd919fe8560.png)245×345 74.4 KB](https://ethresear.ch/uploads/default/c0be63b7e948da68a177a450db277dd919fe8560)

The money spent on bonds and the time they were purchased is recorded within the smart contract.

When a user sells back to the smart contract, the price of bonds decreases.

When bonds are sold, the user get an amount of ether back along with a secondary “resolve” token.

The amount of resolve tokens a user receives is based on a “loss” & “hodl” multiplier. The more the bonds depreciate, the greater the loss multiplier. The longer the bonds were held (relative to current holdings in the contract), the greater the hodl multiplier.

> resolve tokens = investment * (investment / return) * ( hodl / average hodl )

This way of minting resolve tokens harnesses market forces to drive their fair distribution. Only those that have sacrificed the most money and time get the most resolve tokens.

These tokens can then be used to back watchers that run the oracle. The oracle must respond to request tickets within a set time window.

Resolve tokens also have a deflationary component to “tighten” the ring of their distribution. They can be staked back into the contract to earn from the dynamic “friction fee”.

> friction fee = resolve tokens outside contract / total resolve tokens

The slope of the pyramid’s bonding curve should also be dynamic.

> slope = ether in dividends / ether in pyramid

If someone attacks the resolve supply, the pyramid will steepen as people sell bonds to meet the demand for resolve tokens.

## Replies

**andy** (2021-08-28):

Just a few questions:

1. (Investment/Return) piece for resolve tokens how does this reward you if you make more money. It seems the more you make the lower the ratio becomes?
2. How is the average hodl calculated. If I just buy and sell one bond with many different accounts quickly could I drastically reduce the hodl value?

---

**Econymous** (2021-08-28):

1. yes, instead of a “loss multiplier”,  you get a “gains divider”
2. sock puppet accounts won’t work. it’s calculated by the weight of ETH

