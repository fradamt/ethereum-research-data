---
source: ethresearch
topic_id: 1181
title: Plasma MVP and fraud proof examples?
author: alex-miller-0
date: "2018-02-21"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-mvp-and-fraud-proof-examples/1181
views: 3038
likes: 2
posts_count: 4
---

# Plasma MVP and fraud proof examples?

I have been looking into the [Plasma MVP](https://github.com/omisego/plasma-mvp) with a specific interest in the fraud proofs of this initial system. It appears to me that the following is occurring (if I am wrong please let me know and I will update the topic):

1. User makes deposit on mainnet. This somehow triggers a UTXO being generated on the plasma chain (the mechanics of this are unclear to me from the code)
2. User starts a withdrawal on the mainnet of a specific plasma UTXO belonging to him. For the MVP it looks like this must be the initial UTXO generated from the deposit in step 1.
3. If the user has spent this TXO (in a plasma block which has been checkpointed), someone can provide that signed plasma transaction as a challenge and block the withdrawal.

A few questions arise:

1. Am I interpreting this UTXO fraud proof correctly? i.e. a user may only withdraw based on the original UTXO and anyone may prove that a malicious deposit with a signed transaction spending that UTXO?
2. How would a user withdraw a split UTXO? i.e. if I deposit 5 ETH into a plasma chain and spend 2, how could I withdraw the remaining 3? Would I include a new UTXO and similarly allow anyone to prove that I had spent that particular UTXO?
3. How does this fraud proof extend to an account-based deposit/withdrawal? i.e. is there an example of a reasonably compact fraud proof for an EVM plasma chain?

## Replies

**vbuterin** (2018-02-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/alex-miller-0/48/11967_2.png) alex-miller-0:

> User makes deposit on mainnet. This somehow triggers a UTXO being generated on the plasma chain (the mechanics of this are unclear to me from the code)

In MVP, if you make a deposit on the mainnet, then the Plasma contract creates a new block of the plasma chain with one single transaction, which creates the UTXO in the plasma chain “out of nowhere”.

> User starts a withdrawal on the mainnet of a specific plasma UTXO belonging to him. For the MVP it looks like this must be the initial UTXO generated from the deposit in step 1.

Not necessarily; for example, A could deposit, then A can send to B, then B can exit.

> How would a user withdraw a split UTXO? i.e. if I deposit 5 ETH into a plasma chain and spend 2, how could I withdraw the remaining 3? Would I include a new UTXO and similarly allow anyone to prove that I had spent that particular UTXO?

If you deposit 5 ETH and “spend” 2, that means that there are now two UTXOs, one 2 ETH UTXO owned by someone else, and one 3 ETH UTXO owned by you. You can exit your 3 ETH UTXO as normal.

> How does this fraud proof extend to an account-based deposit/withdrawal? i.e. is there an example of a reasonably compact fraud proof for an EVM plasma chain?

This is trickier. I recommend fully wrapping your head around UTXO-based MVP before seriously thinking about this. It is possible, but it requires some compromises.

---

**alex-miller-0** (2018-02-21):

Thanks for the reply.

> the Plasma contract creates a new block of the plasma chain with one single transaction

Does this mean there is an authority who must be authorized to make child blocks? Otherwise how does the system prevent users from triggering blocks from fake deposits? Also, don’t you need the receipt as well? (in order to prove the tx was actually included in the mainnet)

> A could deposit, then A can send to B, then B can exit

Okay, so a follow up: how does the child chain dispose of the UTXO that has been withdrawn? Maybe a similar question to the authority one.

> This is trickier

Yes, I figured ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12). Are you aware of any resources where the model has been discussed? Would love to get a glimpse.

---

**vbuterin** (2018-03-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/alex-miller-0/48/11967_2.png) alex-miller-0:

> Does this mean there is an authority who must be authorized to make child blocks?

Yes. Though keep in mind that the “authority” could easily be a decentralized mechanism, eg. something running on an M-of-N scheme or PoS or whatever.

> Okay, so a follow up: how does the child chain dispose of the UTXO that has been withdrawn? Maybe a similar question to the authority one.

The child chain operator looks at the main chain, and refuses to include transactions spending a UTXO that has been withdrawn or is being withdrawn.

