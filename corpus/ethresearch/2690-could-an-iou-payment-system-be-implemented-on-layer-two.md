---
source: ethresearch
topic_id: 2690
title: Could an IOU payment system be implemented on layer two?
author: decentralicious
date: "2018-07-25"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/could-an-iou-payment-system-be-implemented-on-layer-two/2690
views: 1014
likes: 2
posts_count: 3
---

# Could an IOU payment system be implemented on layer two?

If you don’t know what IOU systems are, there’s a good explanation [here](https://archive.fo/qrsdW) (read the section titled ‘The Concept’).

The ontology of money in Bitcoin, Ether etc. is focused on the tokens, and that’s a very slow and computationally expensive way to do things.

By contrast, systems like Ripplepay (not to be confused with Ripple) or [the mutual-credit currencies the holochain people talk about](http://ceptr.org/whitepapers/mutual-credit) have an ontology centred around user accounts, and the credit:debit balances in the accounts. This is much more lightweight as it does not require universal consensus.

IOU systems are appropriate for a lot of payments, and I’m thinking it would be interesting to do these off-chain and then check in with the main chain every so often.

This idea has been bouncing around my coconut for the past two days. Has anyone thought more deeply about this or started building?

## Replies

**kfichter** (2018-07-27):

[Trustlines](https://trustlines.network/) is basically something like this (IOU payment channels).

---

**decentralicious** (2018-07-27):

I looked into it, and I think Trustlines is on the main chain. (PS: Definitely on main chain; they just confirmed it to me on Telegram.)

Interesting stuff, as it offers a way to obtain cryptocurrency without using a fiat exchange, but not aimed at the same use-cases as payment channels.

