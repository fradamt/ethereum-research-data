---
source: ethresearch
topic_id: 3016
title: Exiting invalid tx in omg mvp?
author: Equilibrium94
date: "2018-08-20"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/exiting-invalid-tx-in-omg-mvp/3016
views: 2085
likes: 1
posts_count: 5
---

# Exiting invalid tx in omg mvp?

I’m looking at the omg plasma code and am wondering what happens if a validator creates a transaction where the inputs and outputs don’t add up. i.e. Creates a transaction where it creates money of out thin air.

I can’t seem to figure out how this problem is prevented? I would guess that the RootChain.sol contract check for tx validity before a withdraw is allowed?

Sorry if the answer is obvious, but I cant seem to figure it out.

## Replies

**kfichter** (2018-08-20):

The contract doesn’t prevent validators from including this type of transaction. However, once a transaction like that is included, everyone on the Plasma MVP chain needs to exit within a specified period of time (~1 week).

Basically it doesn’t matter if we do the check or not. The contract can check that the transaction is valid (inputs >= outputs), but the validators can just spend the invalid UTXO and create a transaction that appears to be valid.

---

**MihailoBjelic** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> The contract can check that the transaction is valid (inputs >= outputs), but the validators can just spend the invalid UTXO and create a transaction that appears to be valid.

Can you elaborate this please? Who are the validators? Thanks. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kfichter** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Who are the validators?

Well in the basic version we’re just talking about a single validator (the operator). In theory, this can be extended to lots of PoS validators.

Imagine the operator creates an invalid UTXO and tries to exit - the contract could easily check that the inputs aren’t valid or that input amount < output amount. Instead, the operator could just spend that UTXO to themselves a bunch of times (100s of times). Now the final UTXO looks entirely valid, except that some UTXO in its history is invalid. The contract would need to see the entire history to know the UTXO is valid, and that’s just way too much data.

---

**MihailoBjelic** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Well in the basic version we’re just talking about a single validator (the operator). In theory, this can be extended to lots of PoS validators.

Oh, that’s what you meant.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Imagine the operator creates an invalid UTXO and tries to exit - the contract could easily check that the inputs aren’t valid or that input amount  the validators can just spend the invalid UTXO

