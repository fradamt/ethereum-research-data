---
source: ethresearch
topic_id: 8620
title: "PoorMe: unreasonably cheap on-chain ERC transfers"
author: kladkogex
date: "2021-02-02"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/poorme-unreasonably-cheap-on-chain-erc-transfers/8620
views: 1773
likes: 8
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

**vbuterin** (2021-02-02):

Interesting!

But how does this prevent Alice from increasing her balance by sending ETH to the PoorMeAlice account manually? If it’s through a selfdestruct the contract can’t prevent it.

---

**kladkogex** (2021-02-02):

Oops :))

It looks like the native token needs to be replaced by a smart-contract based token with cheapest possible transfer fee …

Which could use this


      ![](https://ethresear.ch/uploads/default/original/3X/e/f/ef60601f359b90de6d3e2e5c46a4f80e9333ca31.png)

      [Cointelegraph](https://cointelegraph.com/news/a-new-token-lets-you-save-on-ethereum-fees-by-storing-gas)



    ![](https://ethresear.ch/uploads/default/optimized/3X/f/e/fe51bb6e51e80f0ba8f858cd68f020bb4db68ab7_2_690x459.jpeg)

###



A new Ethereum “gas token” can help users save on fees by storing cheap gas in periods of inactivity, using a clever contract trick that refunds gas when freeing storage










https://blog.trusttoken.com/gasboost-how-tusd-uses-15-less-gas-than-every-other-stablecoin-929b6a110b27

