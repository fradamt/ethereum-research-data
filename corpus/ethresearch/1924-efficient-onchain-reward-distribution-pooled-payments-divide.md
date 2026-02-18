---
source: ethresearch
topic_id: 1924
title: Efficient Onchain Reward Distribution (pooled payments, dividends)
author: bogdan
date: "2018-05-06"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/efficient-onchain-reward-distribution-pooled-payments-dividends/1924
views: 7953
likes: 3
posts_count: 10
---

# Efficient Onchain Reward Distribution (pooled payments, dividends)

## Goal

Efficient on chain distribution of rewards/dividends to participants according to their share/stake, including frequent distribution (daily/hourly/per block), while share/stake of individual users can change freely (like an ERC20 balance).

## Context

Many crypto projects need to disburse “dividends” to holders of staking tokens; other projects have a revenue sharing system where frequent events in their economy generate amounts that must be splitted proportionally between project backers. Examples that could use this technique: staking pools, cooperatives with fractional owning of rent generating assets, paying dividends to share holders, investment funds, recurring payments: salaries could be sent in a single transaction to all employees with any time granularity (hourly/etc); or even the reverse operation: taxing balances of all users by the same percentage, etc.

## Solution

Instead of outbound transfers of rewards, keep a clever accounting of individual ratio of rewards based on accumultated reward per unit of stake and let users withdraw their rewards at any moment (in a pull based fashion). This allows O(1) time for all operations of reward distribution or balance change (deposit/withdraw/transfer) and maintains all distribution logic onchain. The algorithm [is detailed in our 2 page paper](http://batog.info/papers/scalable-reward-distribution.pdf).

It can even be implemented inside an ERC20 compatible contract that will supplimentary expose additional methods like “distribute” and “withdraw reward”.

Note that staking token and dividends token may not be of the same type. Actually, all four combinations of using Ether or an ERC20 token for staking and dividends make sense and have useful usecases.

## Replies

**MicahZoltu** (2018-05-08):

I believe there are one or more tokens that already do this.  Unfortunately, I don’t have any links handy but I remember seeing pull based dividends implemented in tokens in the past.

---

**jamesray1** (2018-05-08):

Not sure if there’s a benefit of doing this at the protocol layer; with Ether being planned to meet ERC20 (or other) token standards you could also do this at the smart contract layer with Ether or other tokens.

---

**bogdan** (2018-05-08):

[@MicahZoltu](/u/micahzoltu) please post if you find it. True, it’s been described in other recent posts, since I started it, but I still think it’s a powerful technique that will be essential to many applications and it deserves a reference implementation. [@jamesray1](/u/jamesray1) definitely at smart contract layer.

---

**MicahZoltu** (2018-05-09):

One technique I have seen is to track all historic balance changes using something like Minime Token (https://github.com/Giveth/minime) and then when it is time to issue dividends, you have a smart contract that allows someone to pull their dividend from the smart contract based on their balance at the target address.  This action is recorded to prevent someone pulling dividends twice.

---

**MicahZoltu** (2018-05-09):

I *believe* the solution you proposed depends on an inability to transfer the asset being rewarded?  Otherwise a user could transfer the asset to another account they control after receiving the reward and thus get the reward twice?

---

**bogdan** (2018-05-14):

Indeed, the Minime approach works by taking a snapshot of all balances at a given block and the using it to award other tokens, based on these balances. This is similar to how dividends work for listed companies: it doesn’t matter how long you held the share but only who owns the share at the precise (and known) moment when dividends are awarded.

In addition to this scenario, the solution I propose allows arbitrary granularity of rewards, without needing to deploy a new contract, nor storing all historic balances. For example, if a listed company wants to award dividends in every day of a year, instead of once or 4 times a year, it’s perfectly possible. Shares can still be transfered inbetween distribution moments and all dividends are correctly accounted for, for each address.

A crypto example is revenue sharing: let’s say a mining actor raises capital (ETH) by issuing token A, spends it all on hardware and then distributes its mining revenue, each block/hour/day, proportionally, to token A holders. Token A can be fully ERC20 compatible, and thus be able to be transfered at any moment. In addition to the normal A balance this token contract holds a *reward* balance, in ETH, that is not directly owned by the token owner, but can be *withdrawn* at any moment. In this regard, yes, the rewards can not be transferred, unless first *withdrawn*. But it’s not an inability, it just needs an additional step. Like yield building up for a bank deposit (right!) needs to be first withdrawn to the checkings account to be spent.

Note that in this mining example, everything happens onchain, and so it requires less trust in the centralized part of it.

Another example, maybe better: let’s say CryptoKitties would have issued a security token that represents a part of the platform and then distribute a fraction of the fee collected from each Kittie sale, to all security token holders, proportionally. This is perfectly possible, fully on chain.

---

**HenriBrg** (2021-11-03):

Hello [@bogdan](/u/bogdan), is there any current in-production project that implements such contracts ? I would be interested regarding my needs on a on-going project.

---

**theJorge** (2021-11-20):

I found this project during my research, however its on Polygon:

https://www.superfluid.finance/home

Look for the keyword IDA

---

**Garito** (2024-02-16):

Hi

Anyone can point me to a similar paper but with dynamic stake?

Even better: is there any lib with solidity implementation of the algo?

Thanks

