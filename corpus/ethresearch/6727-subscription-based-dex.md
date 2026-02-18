---
source: ethresearch
topic_id: 6727
title: Subscription-based DEX
author: kladkogex
date: "2020-01-06"
category: Economics
tags: []
url: https://ethresear.ch/t/subscription-based-dex/6727
views: 974
likes: 0
posts_count: 2
---

# Subscription-based DEX

tldr;

I have an interesting idea of a subscription-based DEX, which may be more fair and scaleable than regular DEXes. This exchange uses streams instead of transactions /order books.

How it works:

- you want to exchange, say 1 ETH into DAI
- you create a stream that sends 1 ETH over 24 hours into a smartcontract
- you get back a stream that sends DAI to you over 24 hours.

At any given moment in time,  the exchange rate E(t) is determined as the ratio of total incoming ETH stream volume to total DAI stream volume.  The money you ultimately get is an integral over 24 hours of E(t).

An exchange like this would have some really great properties:

- it would be fair since everyone would get the same rate
- it would be much better protected against front running, since only a small portion of money is exchanged at any given moment of time
- it would be way more scaleable than regular exchanges, since you would not need to  maintain order books or split your transaction into many small transactions  to average out.

Note, that if the exchange rate becomes out of sync with the exchange rate on other markets, presumably there would be lots of arbitrage agents willing to fix this.

The question becomes how to implement this efficiently in Solidity …

## Replies

**pinkiebell** (2020-01-07):

Interesting, especially how the exchange rate would turn out.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The question becomes how to implement this efficiently in Solidity …

Rough idea is to use `buckets` for the token pairs and `stream` them out later ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) .

On every `deposit` or `withdraw` by the users, the contract can update `E(t)` over the course for the last 24 hours by the `difference` (increasing or decreasing demand) of the supply for the two buckets (token pairs).

