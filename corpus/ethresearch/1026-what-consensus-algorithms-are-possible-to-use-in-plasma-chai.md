---
source: ethresearch
topic_id: 1026
title: What consensus algorithms are possible to use in plasma chains?
author: ethrbn
date: "2018-02-08"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/what-consensus-algorithms-are-possible-to-use-in-plasma-chains/1026
views: 2514
likes: 4
posts_count: 7
---

# What consensus algorithms are possible to use in plasma chains?

Simple question really. For example, Ripple and Stellar are fast and cheap but are generally considered less decentralized as far as I know. This sounds like a perfect fit for plasma, since users can withdraw in case of fraud but still benefit in terms of speed and price of transactions. Does plasma place any restrictions on what types of consensus algorithms can be use (or which ones are cheap to use in terms of root chain transactions needed)?

## Replies

**drcode1** (2018-02-08):

I believe you can support all three types of consensus:

- Proof of Authority (i.e., just trusting some entity)
- Proof of Stake
- Proof of Work

However, the third option (Proof of Work) is somewhat problematic because the whole raison d’être of Plasma is that you can support the chain with a lot fewer computational resources than the full public chain, but POW isn’t really practical for small chains (since a big mining entity could arbitrarily switch its POW power to your chain and destroy the consensus)

Therefore, POA and POS seem like the only options that are really practical.

---

**vbuterin** (2018-02-09):

PoW is hard because it’s not finality-bearing, and plasma does require a notion of finality. You could do something like “PoW plus 6 confirmations on main chain means finality” though that would not be quite the same thing. PoS and PoA are indeed the only practical options.

---

**hank** (2018-02-13):

Is anyone working on a PoS plasma chain implementation currently? I know David & OMG intend to eventually have PoS, but my understanding is that the mvp will be PoA.

---

**EazyC** (2018-02-13):

Correct me if I’m wrong, but I am under the impression that a plasma chain can use any open source PoS in its implementation, meaning that when full Casper (aka TFG) codebase is live, anyone can incorporate Vlad and Vitalik’s work into a plasma chain for their own projects. So this basically means that work on Ethereum’s base PoS implementation translates to more options for plasma chains. As for OMG, I believe they are using Honte implementation first but will later move to more sophisticated (read: secure) version of PoS once available. Again, please correct me if wrong, this is just my understanding of the current state.

---

**hank** (2018-02-14):

Yes, it would be interesting to use the full casper logic and port it to a more simple UTXO-based chain. I guess that’s mainly my question, if anyone is working on something like that.

---

**vbuterin** (2018-02-14):

You can replace the PoA with an M-of-N signature scheme, and use any BFT consensus algo internally to determine which block everyone signs.

