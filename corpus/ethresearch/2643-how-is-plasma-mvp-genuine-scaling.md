---
source: ethresearch
topic_id: 2643
title: How is Plasma MVP genuine scaling?
author: bedeho
date: "2018-07-22"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/how-is-plasma-mvp-genuine-scaling/2643
views: 1234
likes: 2
posts_count: 3
---

# How is Plasma MVP genuine scaling?

In Plasma MVP, users must download all transactions for a given child chain in order to use it. This does not appear to be an improvement over normal light client mode, where (I presume) one can download only transactions for a given contract in each block.

The definition of scaling as a goal pursued on Ethereum is that one wants to allow users to validate less than everything securely, but how does MVP actually fulfil that goal?

I know most people have moved on to Plasma Cash, which does not require this, but I suspect I am still wrong on this point some how, and would love to get some clarity.

## Replies

**kfichter** (2018-07-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/bedeho/48/3154_2.png) bedeho:

> The definition of scaling as a goal pursued on Ethereum is that one wants to allow users to validate less than everything securely, but how does MVP actually fulfil that goal?

Plasma allows the users within the Plasma chain to securely make transactions off-chain while ensuring that *everyone else* has no need to validate the Plasma chain.

![](https://ethresear.ch/user_avatar/ethresear.ch/bedeho/48/3154_2.png) bedeho:

> I know most people have moved on to Plasma Cash, which does not require this, but I suspect I am still wrong on this point some how, and would love to get some clarity.

Also, I think it’s important that Plasma Cash isn’t a magic bullet. Plasma Cash is good for non-fungible tokens. It’s not really that good at making arbitrary payments or handling exchanges. The per-coin proof sizes are (currently) quite large, so it isn’t that good at being denominated cash either.

---

**drcode1** (2018-07-22):

Plasma allows transactions to be run off-chain. While it’s true that a “light client” doesn’t need to download transactions, it still requires there to be “full clients” that process the transactions on-chain, whereas plasma transaction do not need to be processed at all by other ethereum full clients.

> but how does [plasma] MVP actually fulfill that goal?

Plasma (usually) requires nodes using the plasma chain to do a lot of heavy validation, HOWEVER nodes that don’t care about the plasma chain can ignore all of the plasma transactions and still validate the main-chain plasma contract properly, so there can potentially be many plasma chains all running independently.

The main innovation of plasma chains is that in the case that a plasma chain operator misbehaves, users of the chain have at least some limited recourse relying on only the main chain contract, in a manner that is validated by other ethereum nodes, even those that don’t care about and don’t track any of the individual plasma chain transactions. A mistreated plasma chain user can exit the plasma chain with all their $$ intact.

