---
source: ethresearch
topic_id: 1786
title: Offchain oracles
author: kowalski
date: "2018-04-20"
category: Economics
tags: []
url: https://ethresear.ch/t/offchain-oracles/1786
views: 2431
likes: 6
posts_count: 7
---

# Offchain oracles

I’m interested if someone considered using an offchain oracle. I’m going to implement it and would like to check if perhaps someone else tried it before.

A traditional oracle works by frequently putting data feed into a smart contract. If we want to have a fairly recent data we need to spend a lot of gas and send a lot of transactions. This may not be problematic for feeds which are heavily used but doesn’t seem right if the feed is used scarcely.

The solution I’m considering is to have the oracle provide the feed value through HTTP API rather than put it on blockchain. The record  would include the current blockNumber and the signature. A transaction using this value would need to provide: `{ value, blockNumber, signature }` and the smart contract of the oracle would validate that the signer is among the trusted providers and that `blockNumber` isn’t stale (with some defined tolerance).

Comparing with a traditional oracle the history of the feed looked up on blockchain would only include the blocks in which the value was used, not every Xth block like in a traditional one. The gas costs of maintaining the feed is shifted from the data providers to feed users which is desirable in our usecase.

The whole idea is somewhat similar to how 0x protocol works. In a sense, 0x `fill()` method relies on offchain oracle (taker) to provide the data of order to fill, while the feed input is signed by the maker.

Has something like this been done before? Anyone sees week points of this design ?

## Replies

**bharathrao** (2018-04-20):

I think oracles tend to be modeled as trusted third parties and this defeats the purpose of decentralization. Oracles will be corrupted or compromised if the incentive gets big enough.

0x fill is an interesting case because the price is a result of two parties agreeing to trade at a certain value and every trade is composed of different parties acting in their own economic interests. However, its NOT an oracle, its just market data. For example, I could buy 0.00000001 eth for 1 million USD. This is an individual action by me and in no way reflects the market. A weighted average of trades can be used *as a proxy of value* however, these things do not reflect value in any accurate manner.

There wont be any rock solid Oracle model until someone figures out how to attach real world sensors to the blockchain (for example IOT devices)

---

**MicahZoltu** (2018-04-21):

It sounds like what [@kowalski](/u/kowalski) wants is a *trusted* oracle, not a trustless oracle like [@bharathrao](/u/bharathrao) is describing.  Augur is building a trustless Oracle that can get off-chain information on-chain within a well known/defined set of constraints/limitations, but it hasn’t launched yet and each data point is *expensive* to get on-chain.

The mechanism you have described seems fine, as long as you recognize that it is really just a trusted oracle.  I would swap out `blockNumber` with `timestamp` though, since I think that is really what you want.  Also, the smart contract should make sure that the value being submitted is not *older* than the most recent update the contract has seen.  If the contract already has a *newer* value, then that should be used instead of the provided one.

---

**kowalski** (2018-04-22):

Micah, by all means I’m building a *trusted* oracle. In the implementation I’m actually using `DSAuth` to have addresses:

- allowed to sign data feed
- addresses allows to change priviledges

Good point of disallowing using an older value than the contract has. I will definitely include this. Now I’m conflicted on how the contract should behave when given a stale value. It can a) `throw` b) return the newer value transparently c) provide two method with both behaviours.

As for using `timestamp` instead of `blockNumber` it’s sort of same thing. But yeah I guess `timestamp` seems more natural. Thanks.

---

**kowalski** (2018-04-22):

[@bharathrao](/u/bharathrao) as Micah has pointed out I’m building a trusted oracle.

As a matter of fact my oracles are running on RasberryPi’s making a real world measurements, so it’s very much what you are describing in the last paragraph. However I don’t see how using IOT could make it *untrusted* oracle. In the end my devices still need to push data into blockchain and if an attacker gets hold on the private key of the device he can impersonate it. So it’s far from rock solid.

Are you familiar with any research where this problem is addressed better ?

---

**MicahZoltu** (2018-04-22):

An IoT device fabricated like Intel’s SGX stuff could sort of work.  In this scenario you are trusting some single well known entity to create something that doesn’t have a back door (and presumably the final product can be audited) and trusting them to not divulge the private key generation algorithm (including no leaks in their manufacturing process.

As for behavior on call with stale value, I recommend return the newer value transparently.  Going with `throw` will result in races constantly resulting in failed transactions and wasted gas.  As long as the number on-chain is new enough (which is necessarily true if the number being supplied is not stale) then really you don’t even need to supply a new value in the first place.

---

**bharathrao** (2018-04-22):

The private key should be on a secure element that erases itself like in the Ledger hardware wallet.

My view on oracles is this:

- Multiple entities incentivized to submit accurate information is best
- Multiple entities disincentivized to submit inaccurate information is next
- Single entities are the worst

Lets say I have an IOT device that measures moisture in the soil and when the reading is low, requests more water sent through the irrigation system. Since water costs money and not getting water kills plants, the IOT device is incentivized to send accurate info.

Lets say another class of IOT devices just counts people walking into and out of a conf room. As long as the ingress and egress numbers add up, the devices get paid a flat fee. If any device sends numbers out of whack, it stops getting paid. This model disincentivizes inaccurate readings.

