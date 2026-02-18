---
source: ethresearch
topic_id: 1893
title: Optimistic cheap multi-exit for Plasma (Cash or MVP)
author: vbuterin
date: "2018-05-01"
category: Sharding
tags: []
url: https://ethresear.ch/t/optimistic-cheap-multi-exit-for-plasma-cash-or-mvp/1893
views: 5934
likes: 6
posts_count: 5
---

# Optimistic cheap multi-exit for Plasma (Cash or MVP)

Special thanks to Karl Floersch and David Knott for helping to come up with this.

We can make exiting from Plasma cheaper in the normal case by simplifying the contents of an exit transaction; instead of actually including a Merkle proof, a transaction would simply contain a list of (block number, coin index) pairs. There would be an extra type of challenge mechanism where anyone could challenge to require you to actually provide a Merkle branch in order to complete a withdrawal.

In the normal case, this reduces the cost of a single exit to ~log(t) + log© bytes (eg. assuming one Plasma block per minute running for one year, and 1 million coins, 39 bits ~= 5 bytes); with a full Merkle proof it would have cost 640 bytes. Many exits can be batched together into a transaction with one signature.

In Plasma Cash, the extra challenge mechanism could simply exist in parallel with other challenge mechanisms; the only practical consequence is that anyone can attempt to make an invalid exit, and not just previous owners of a coin. In Minimal Viable Plasma, the only type of challenge is to provide a child UTXO proving the given TXO was spent; this could be done regardless of whether the actual TXO is provided or just an index.

## Replies

**josojo** (2018-05-02):

Nice, this cuts exit costs quite a bit. In order to optimize the gas costs for exits, we should also focus on how much data needs to be actually stored on the root-chain for each exit request, since this is the most expensive part.

Here is another proposal that includes your idea:

If one calls startExit(int []blocknumbers, int [] coinindexes,… other data), we do not store the blocknumber and coinindexes onchain. We could just log them, hash them together and store only the hash.

For challenging this withdrawal, the challenger would have to resubmit the (int []blocknumbers, int [] coinindexes) and the hash is recalculated. If the hash equals the previously stored hash, we allow the proceeding of the challenge request with these data.

This way we could make the challenge and exiting a little bit more complex, but also quite a bit cheaper.

This could be developed even further to allow several owners to store their exit requests with only one hash, if we hash their signatures of the transaction as well.

But I am not  sure whether this is in a scope of a MVP ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=9)

---

**danrobinson** (2018-05-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> We can make exiting from Plasma cheaper in the normal case by simplifying the contents of an exit transaction; instead of actually including a Merkle proof, a transaction would simply contain a list of (block number, coin index) pairs. There would be an extra type of challenge mechanism where anyone could challenge to require you to actually provide a Merkle branch in order to complete a withdrawal.

You may be able to even skip providing the block number… just the coin indexes.

I think this ends up being similar to a cryptoeconomic aggregate signature, where consent of the parties involved is assumed unless they challenge within a set time. So this idea is to “verbose” withdrawal as [Plasma XT](https://ethresear.ch/t/plasma-xt-plasma-cash-with-much-less-per-user-data-checking) is to explicit withdrawal-and-redeposit (i.e. manual on-chain checkpointing).

---

**tim** (2018-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the only practical consequence is that anyone can attempt to make an invalid exit, and not just previous owners of a coin

Can’t you restrict the ability to exit to a set of accounts that staked some ether up front and thus limiting an invalid exit to only that set?

---

**fahree** (2018-05-25):

IMNSHO, *if* exits depend on individual requests, then

1- Plasma fault recovery requires ~ k*N_{users} main chain transactions, which does not scale. I suppose this is kind of OK if the Ethereum main chain itself scales (which it doesn’t yet, but will in the future), but still sucks (load-wise and fee-wise).

2- There is no enforceable bounds to multi-spending malfeasance by the channel operator, and no penalty for misbehavior, so bad behavior may be relatively common.

My proposed solution (at https://legi.cash/) is to use a “court registry”, i.e. an oracle for public availability, so there can simply be no block withholding attack (short of a 50% attack on the court registry). Then:

1- Mass exits are possible in only ~k*N_{operators} main chain transactions, which scales.

2- Faulty operators will be caught and punished before they can do more than double-spend, so bad behavior may be close to non-existent.

