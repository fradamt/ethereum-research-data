---
source: magicians
topic_id: 5277
title: "PoorMe: unreasonably cheap on-chain ERC transfers"
author: kladkogex
date: "2021-02-02"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/poorme-unreasonably-cheap-on-chain-erc-transfers/5277
views: 704
likes: 6
posts_count: 3
---

# PoorMe: unreasonably cheap on-chain ERC transfers

*TL;DR*

We describe **PoorMe**, a smart contract-based on-chain wallet that **drastically reduces transfer fees for ERC tokens.**

The fees become similar to ETH native transfer fees (21K for a send and 10K for a multisend).

PoorMe enables **forks of dapps like Uniswap with way lower gas fees.**

*Description.*

ERC token transfer fees are much larger than ETH native transfer fee.  For example, SNX is around 100K gas to transfer and  SKL is 65K gas.

Ironically, there is an (overlooked!) method to achieve ERC token transfer fees almost identical to native ETH fees.

The method is utilizing a **dedicated on-chain wallet for each user**, as described below.

Here is how it works:

1. There are two master smart contracts :

- WalletFactory deploys wallets
- TokenBank holds all ERC tokens

1. Onboarding procedure:  Alice calls WalletFactory, which deploys a dedicated PoorMeAlice wallet contract.
2. Deposit procedure: to deposit, say, 100 SNX Alice deposits SNX  to TokenBank, and, in parallel, deposits  100 / 10^{12}  ETH to PoorMeAlice.  So PoorMeAlice holds a tiny amount of ETH proportional to SNX holdings.
3. From this moment on, the amount of ETH in PoorMeAlice is used to track how much SNX  Alice has.   Namely, to find out Alice’s holdings, one simply multiplies the holdings in PoorMeAlice by 10^{12}.
4. Token transfer procedure: Now suppose Alice wants to send 10 SNX to Bob. She simply sends 10 / 10^{12} ETH from PoorMeAlice to PoorMeBob.
5. Multisends work the same way. To send 1 SNX to each of 5 people Alice simply sends 1/10^{12} ETH from PoorMeAlice to PoorMeWallets of these people.
6. Finally, to withdraw or deposit amount X,  Alice simply withdraws/deposits from/to TokenBank, concurrently withdrawing/depositing X/10^{12} ETH into PoorMeAlice

Note, that once Alice has a PoorMe wallet, she can use it for all kinds of DeFi.  DeFi apps can use PoorMe wallets too. This means,  that you can create forks of Uniswap and other projects with way lower fees.

## Replies

**rumkin** (2021-02-08):

I love the idea and I think it should be standard behavior. Ability to emit new currency/token and transfer them as a regular transaction should be available out of the box. It seems to me same type of enhancements as contract-based on-chain wallets.

---

**lightcycle** (2021-02-17):

Does Bob need to also create a PoorMeBob and deposit (or somehow bind) SNX?

