---
source: ethresearch
topic_id: 1310
title: Seigniorage shares using Casper feasible?
author: SRALee
date: "2018-03-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/seigniorage-shares-using-casper-feasible/1310
views: 2352
likes: 2
posts_count: 7
---

# Seigniorage shares using Casper feasible?

I am working on a stablecoin project which is similar to [Robert Sams’ seigniorage shares](https://bravenewcoin.com/assets/Whitepapers/A-Note-on-Cryptocurrency-Stabilisation-Seigniorage-Shares.pdf) system. My question is if it would be feasible to use something like Casper TFG as the byzantine method if we modeled the “seigniorage shares” as the staking token for block proposal and block order/finality.

Do any Casper experts see any clear broken security guarantees in this setup?

One of the main issues I am having trouble overcoming is using a Schelling point scheme for the expansion and contraction signals in a full proof of stake system. Would be interested in Casper researchers opining. Thank you for your time!

## Replies

**vbuterin** (2018-03-06):

Why build seignorage shares as a blockchain, instead of as a mechanism on top of an existing blockchain?

---

**SRALee** (2018-03-06):

I’m actually looking into building it as a plasma chain (that’s why I asked about Casper as the chain’s Byzantine method), but if you mean the entire system as a smart contract inside ETH, then I am very open to seeing any proposals. The issue is that I **REALLY** don’t like oracles/off chain trust (even if the oracles are “voted in by token holders blah blah”), so I have been mainly thinking about Schelling point signals to either expand or to contract cash supply which is what a price feed is supposed to be a means to an end to anyway. I don’t see how to make that conception as a pure smart contract and have good cryptonomics for the system given the gas costs required to report Schelling signals and other limitations. What exactly did you have in mind?

---

**vbuterin** (2018-03-06):

I would recommend using Schelling votes to change coin supply, and then if the votes go wrong then you can just hard fork the contract (ie. make a copy and carry over all of the balances).

I’d recommend building it as a smart contract on-chain as that’s the best way to make the coin maximally useful to all other ethereum dapps; it would become automatically eligible for plasma or any other scaling solution that appear, and you could even run your own plasma chain for it separately.

---

**k26dr** (2018-03-06):

Schelling point votes on the main chain with transaction fees have a negative expected value. How would you incentivize voters to participate?

---

**SRALee** (2018-03-06):

I’ve thought about that before and if you discount the tx fees and other issues, it has certain advantages. For example, maybe it is possible to auction off the stable tokens for other assets on the ETH mainnet such as ETH itself or other tokens (these tokens would then be held inside the contract). Then people who hold seigniorage share tokens can not only place bids to receive newly printed cash in the next expansion but place bids for different assets inside the smart contract. Something like that would mimic a real central bank (which buys and holds different assets and not just its own equity). The downside of this would be that it would be very difficult to “fork the contract” as you mentioned since it would not carry over the assets the old contract controls.

---

**kladkogex** (2018-03-09):

[@SRALee](/u/sralee) - our startup is developing a scaling network that will run alongside Ethereum  and help scale smartcontracts.  It will run an augmented version of EVM. We are looking for a small number of closed beta participants - if you are interested let me know, we  will help you to develop you DApp then ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

