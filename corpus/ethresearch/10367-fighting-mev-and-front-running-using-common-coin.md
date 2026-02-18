---
source: ethresearch
topic_id: 10367
title: Fighting MEV and Front Running using Common Coin
author: kladkogex
date: "2021-08-19"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/fighting-mev-and-front-running-using-common-coin/10367
views: 2294
likes: 7
posts_count: 7
---

# Fighting MEV and Front Running using Common Coin

At SKL we are impelementing on a Threshold-Encryption based protection mechanism for MEV.

While we working on it, one of our engineers [@D2](/u/d2) came up with a simpler scheme.

Essentially you execute transactions in a block according to ordering specified by a Common Coin - an unpredictable, random number.

In our case, since each block is already signed by a Threshold Signature, which is a Common Coin, implementing this mechanism is really simple.

For other blockchains, Common Coin can be derived through VDF,  which may delay execution a bit …

## Replies

**MicahZoltu** (2021-08-19):

Random transaction ordering incentivizes “shotgun” MEV, which is where you just submit dozens or hundreds of transactions and rely on probability getting your transaction at the head of the block.  This results in network spam, which arguably is worse than the problem it is trying to solve.

---

**pipermerriam** (2021-08-19):

This also has complexity in the case where there are two transactions from the same sender within a block, requiring special rules to either disallow this case or to ensure that the two transactions are ordered respective of their nonces.  This isn’t a deal breaker but it does have to be taken into account.

---

**kladkogex** (2021-08-20):

This one is not hard to solve - you order transactions by

HASH(sender | common coin)

And for the same sender you sort by nonce …

---

**kladkogex** (2021-08-20):

Interesting point …

By isnt it going to cost lots of gas ?

---

**MicahZoltu** (2021-08-21):

All transactions except the first fail fast, which means they use a bit over 21,000 gas.  When compared to the financial gain from winning this sort of auction, it definitely comes out EV+ in many situations to spam out a dozen or even a hundred transactions in order to have a high probability of inclusion near front of block.

---

**SebastianElvis** (2021-08-22):

Does this mechanism require some synchrony assumption on the nodes’ mempools?

For example, the adversary may select a list of preferred txs and executes them in a block. Although there exists other txs interleaved with the adversary’s list of txs, the adversary can claim it does not receive those txs. Such claims cannot be verified as the adversary ignoring txs is indistinguishable with the adversary not receiving txs on time.

If this assumption is required, then does this assumption imply zero-block confirmation (as nodes have agreed on tx ordering before agreeing on tx execution), as analysed in [Cryptology ePrint Archive: Report 2021/139 - Order-Fair Consensus in the Permissionless Setting](https://eprint.iacr.org/2021/139)?

