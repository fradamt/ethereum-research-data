---
source: ethresearch
topic_id: 3894
title: State commitments/stateless validation using algebraic vector commitments
author: musalbas
date: "2018-10-23"
category: Uncategorized
tags: [stateless]
url: https://ethresear.ch/t/state-commitments-stateless-validation-using-algebraic-vector-commitments/3894
views: 1703
likes: 4
posts_count: 3
---

# State commitments/stateless validation using algebraic vector commitments

Meanwhile proposing different ways to commit to state has been a hot topic lately (RSA accumulators, Sparse Merkle tree, etc), I came across [this paper](https://eprint.iacr.org/2018/968) that proposes doing so using algebraic vector commitments that I think may be worth discussing.

The crux of the paper is that if you commit to the state using algebraic vector commitments, and you want to achieve stateless validation, then you can make it possible for Alice to send money to Bob, and only provide the proof of Alice’s balance. With a Merkle tree, you’d also need to provide proof of Bob’s balance. This may be nice, because that means everyone one needs to store their own state; Alice doesn’t need to know Bob’s state. However, it appears to require a trusted setup.

Here’s the crux of it:

[![image](https://ethresear.ch/uploads/default/original/2X/4/4af58e39a95593966d1febaa40ee1445a7d496fb.png)image562×439 70.6 KB](https://ethresear.ch/uploads/default/4af58e39a95593966d1febaa40ee1445a7d496fb)

## Replies

**MihailoBjelic** (2018-10-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> you can make it possible for Alice to send money to Bob, and only provide the proof of Alice’s balance

Can’t we do the same with Sparse Merkle trees? I was thinking that’s exactly how original Plasma Cash works - leafs represent all possible IDs of coins, and coins just change owners? In this model, one only needs to keep the history of his own coin(s), and that’s all that is needed for a coin to get a new owner, i.e. to be transferred?

---

**eolszewski** (2018-10-25):

Somewhat - in pcash, you just have a bunch of nfts that get passed around whereas in this case, you have an fungible account-based model.

People ain’t super bullish on trusted setup tho, with all this research into class groups 'n such

