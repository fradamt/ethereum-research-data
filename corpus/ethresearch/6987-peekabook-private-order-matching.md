---
source: ethresearch
topic_id: 6987
title: "PeekABook: Private order matching"
author: barryWhiteHat
date: "2020-02-19"
category: Cryptography > Multiparty Computation
tags: []
url: https://ethresear.ch/t/peekabook-private-order-matching/6987
views: 3836
likes: 11
posts_count: 8
---

# PeekABook: Private order matching

Barry Whitehat , Kobi Gurkan

## Intro

We can post order on chain. But there is no way to advertise an order such that only a person who has a matching order can see the order.

This is a problem because people who see you want to make an order can use that information to move the market before your order is processed.

Therefore its interesting to find a way to match orders without publishing them.

The socialist millionaire problem solves this by allowing us to check if two values match privately. If not we do not gain any information about them.

Where we use this to privately search orders that match

## Solution

I adversities on chain that I have an order on a certain pair. People who are looking to execute their orders on the same pair contact me directly.

I have my order a. my counter party has their order b. We then enter the following protocol together. a and b are encoded as bits where the

first 64 bits denote the amount and the next 64 bits denote the price.

We then run the socialist millionaires protocol as described https://en.wikipedia.org/wiki/Socialist_millionaires#Off-the-Record_Messaging_protocol

## Attacks

1. An attacker can not follow the protocol and make it appear that orders do not match when they do.

We can use a zkps to prevent this. There are ZKP that are much lighter than snarks that we can use to do this.

1. State space enumeration attack

An attacker can guess what your order is and repeat millions of times until they get it right. We need to limit the rate of requests. This would require strong proof of individuality / anti Sybil in order to prevent this.

## Conclusion

The order is not committed to on chain so you just have a chance to

1. Legitimately find someone who will match you order
2. Try and guess someones order.

The key point is that if someone lies they get one chance to guess your order. In the current implementation everything is public. In the worst case this devolves to the status quo with a bunch of extra steps. Using reputation systems and bonds seem like a good way to prevent users from abusing this.

We can also use reputation systems to limit the rate of requests.

## Replies

**HAOYUatHZ** (2020-03-02):

Hi [@barryWhiteHat](/u/barrywhitehat) , in my opinion it’s not the biggest concern.

Centralized exchanges suffer from this problem but they are still popular.

Such a design might affect volume and liquidity, because people cannot easily adjust their orders accordingly. It’s harder to find a match.

---

**barryWhiteHat** (2020-03-02):

[@haoyuathz](/u/haoyuathz) thanks for your comment. I am not sure I understand what you mean. What is not the biggest concern ?

---

**HAOYUatHZ** (2020-03-02):

[@barryWhiteHat](/u/barrywhitehat) Sorry I should make it more clear.

I mean making the order price private.

---

**mhchia** (2020-03-12):

It’s an cool idea! Thanks for sharing. I have some questions accordingly:

![](https://ethresear.ch/user_avatar/ethresear.ch/barrywhitehat/48/4436_2.png) barryWhiteHat:

> I adversities on chain that I have an order on a certain pair.

1. Are the only things on chain are these advertisements?
2. May I assume the “advertisement” is just some kind of contact information like an ip:port pair?
3. Am I understand it correctly: If a user wants to find a matching order, he/she needs to run smp with the contacts in all advertisements on chain?

> Using reputation systems and bonds seem like a good way to prevent users from abusing this.
> We can also use reputation systems to limit the rate of requests.

Bonds or some kind of membership system sound an important way to prevent bad guys from flooding the users. We can also perform rate limit based on ip.

---

**lsankar4033** (2020-03-12):

The advertisement consists of the pair you’re interested in trading and some type of contact info (like `ip:port`).

A user will want to run smp on advertisements that match the pair he/she is interested in trading. One downside of the smp approach is that it requires an *exact match* of orders to result in a trade. I.e. you wouldn’t be able to do limit orders this way.

---

**gMoney** (2021-02-23):

Do the price:amount pairs have to match exactly with the SMP protocol?

---

**ethgcm** (2021-02-23):

[@barryWhiteHat](/u/barrywhitehat) So in a sense we would advertise the pair in question on blockchain, but then leverage an interactive offchain PSI protocol (something as simple as ECDH PSI or EC ElGamal PSI) ?

Here is some unfinished volunteer [research work](https://github.com/AmitShah/ECDH-PSI-2Server/blob/e717ff6df253a728d27ea8a6578be8a7d5a2e17d/ContactTracing.pdf) regarding private trajectory tracing.  The paper introduces the concept of 3rd party servers that act as upload servers and allow the uploading agent to go offline.  The upload servers are held accountable via data bond on their keys. There are problems in the implementation re: server availability but allows clients to go offline

