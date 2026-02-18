---
source: ethresearch
topic_id: 5691
title: Layer 2 state schemes
author: vbuterin
date: "2019-07-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/layer-2-state-schemes/5691
views: 7712
likes: 11
posts_count: 8
---

# Layer 2 state schemes

*Special thanks to Karl Floersch and Ben Jones for ideas around Plasma with on-chain publication*

An interesting class of constructions that is starting to appear for eth2 is that where the blockchain is used as a data and computation layer, but there is not a trivial direct mapping between the blockchain state and the actual state (eg. account balances) that users care about.

One example of this is [A layer 2 computing model using optimistic state roots](https://ethresear.ch/t/a-layer-2-computing-model-using-optimistic-state-roots/4481), where we create a higher-layer scheme to pretend that cross-shard transactions happen much more quickly than they actually “settle” by storing dependency graphs as part of the state and letting clients figure out what the state *will* resolve to when all the dependencies settle.

[![Screenshot_2019-07-03%20%E8%B7%A8%E5%88%86%E7%89%87%E4%BA%A4%E6%98%93](https://ethresear.ch/uploads/default/optimized/2X/3/35ad25edb2c92337ed8de738e9f854f903867c08_2_690x261.png)Screenshot_2019-07-03%20%E8%B7%A8%E5%88%86%E7%89%87%E4%BA%A4%E6%98%931157×439 31.2 KB](https://ethresear.ch/uploads/default/35ad25edb2c92337ed8de738e9f854f903867c08)

In this example, someone sends 5 coins to Bob, but the Merkle root that the receipt depends on for validity will not reach the bottom shard for three blocks. To get around this, Bob’s state is stored as a conditional value, storing the balance if R is correct and the balance if R is not correct, and transactions operate on the conditional values. Eventually, the bottom shard learns about R and “collapses the superposition”. Bob and Charlie’s *clients* can have private knowledge about the top shard, and can predict early on that R is the correct root, so they can hide the complexity and simply show to the user the expected balances immediately.

### On-Chain Plasma

A more radical construction looks more similar to Plasma Cash. Imagine a system where a smart contract stores assets, and this contract processes an “exit game” with the following rules:

- Anyone can start the process to exit some asset A by providing a Merkle proof of a transaction T in which they become the recipient of A.
- An exit-in-progress can be challenged by providing a transaction T’ that was included in the chain later than T and that references T as a parent. This challenge immediately cancels the exit.
- An exit-in-progress can be challenged by providing a transaction T’ that was included in the chain earlier than T and that touches A. This challenge can in turn be challenged by providing a child of T’ that was still included in the chain earlier than T (or that equals T itself).

Transactions can be included on any shard (or we could restrict to a specific set of shards for each asset).

[![Screenshot_2019-07-03%20%E8%B7%A8%E5%88%86%E7%89%87%E4%BA%A4%E6%98%93(1)](https://ethresear.ch/uploads/default/optimized/2X/c/cc7e83560e9cc1ccf109c669019cb78a86c96f61_2_690x195.png)Screenshot_2019-07-03%20%E8%B7%A8%E5%88%86%E7%89%87%E4%BA%A4%E6%98%93(1)1159×329 12.3 KB](https://ethresear.ch/uploads/default/cc7e83560e9cc1ccf109c669019cb78a86c96f61)

Here, we have a scheme where are using the chain to provide near-instant initial-confirmation guarantees for transactions, and we are using it for data availability (and for computation if there are many exit games at the same time), but we are not really storing the current owner of any asset on chain. Notice that this scheme is easily extensible to synchronous cross-shard transactions: you can just have one transaction that touches any two assets, and simply put that transaction on any shard.

So how would clients know what the application state is? Either they could scan all of the shards on which transactions could legally appear and locate all the transactions relevant to assets that they might own, or they could use a light-client protocol where they ask servers to provide them Merkle proofs of transactions that touch accounts that they care about.

I expect that such schemes are likely to proliferate for several reasons:

- They can provide near-instant cross-shard transactions even if the underlying chain does not provide this functionality
- They can provide synchronous cross-shard transactions
- They can potentially have ~O(log(N)) times more scalability, due to the absence of any need for on-chain Merkle proofs in the normal case
- They can allow near-instant block times due to the ability to send a transaction on one of multiple shards

### Fee market issues

But these schemes pose a significant challenge: they complicate the fee market. Particularly, unless block producers are aware of how all of these layer-2 state schemes work (unlikely; there are just too many possible designs), if someone attempts to pay fees inside of one of these schemes then the block producer has no way to determine whether or not a fee is actually being paid.

Another possible alternative is out-of-band fee payment: anyone wishing to send transactions must also have unencumbered coins that they send to the block producer separately from the transaction they want included. But this is unacceptable because it breaks privacy (eg. see discussion here https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475).

The solution that survives is a *relayer market*: an actor that understands some layer 2 state scheme packages others’ transactions, claiming fees from them inside of the scheme, and sends along the package as a regular transaction, with a fee paid using unencumbered state.

## Replies

**dankrad** (2019-07-03):

The staggered on-chain plasma is amazing! I think it would be a game-changing application. Is there a way to make it programmable, i.e. allow for general state execution?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> An exit-in-progress can be challenged by providing a transaction T’ that was included in the chain earlier than T and that touches A. This challenge can in turn be challenged by providing a child of T’ that was still included in the chain earlier than T (or that equals T itself).

I had another idea for those schemes that allow spending money on any of the shards: What if you added in a mechanism that immediately burns the money if it was double spent? It would basically eliminate any incentive for someone to try and cheat by reverting one chart and getting their double-spending transaction in earlier.

---

**vbuterin** (2019-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> The staggered on-chain plasma is amazing! I think it would be a game-changing application. Is there a way to make it programmable, i.e. allow for general state execution?

You could imagine the scheme running in a way where *almost every transaction* touches multiple accounts, referencing what it thinks is the previous transaction that touched those accounts. Then you basically have something equivalent to an EVM with mandatory access lists.

> I had another idea for those schemes that allow spending money on any of the shards: What if you added in a mechanism that immediately burns the money if it was double spent? It would basically eliminate any incentive for someone to try and cheat by reverting one chart and getting their double-spending transaction in earlier.

Interesting! I can see how that would be an improvement. So basically as soon as you send someone money you are precommitting to either send it to them or burn it. I like it!

---

**Mikerah** (2019-07-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> What if you added in a mechanism that immediately burns the money if it was double spent? It would basically eliminate any incentive for someone to try and cheat by reverting one chart and getting their double-spending transaction in earlier.

This sounds like a generalized form of scorched earth contracts ([List of primitives useful for using cryptoeconomics-driven internet / social media applications](https://ethresear.ch/t/list-of-primitives-useful-for-using-cryptoeconomics-driven-internet-social-media-applications/3198) and https://blog.oleganza.com/post/58240549599/contracts-without-trust-or-third-parties#_=_). I suspect that this would have an effect on the total supply of ETH. Also, it changes some incentives quite a bit.

---

**vbuterin** (2019-07-03):

I think the effect on the total supply of ETH would be minor; after all, the only case where any ETH would be burned is that where at least one actor is either malfunctioning or dishonest.

---

**musalbas** (2019-07-04):

The state execution model where the chain is only being used for data availability is similar to one described [here](https://ethresear.ch/t/a-data-availability-blockchain-with-sub-linear-full-block-validation/5503). One optimization to allow light clients to know that they’re being served the complete set of transactions for accounts they care about, is to use a Merkle tree where intermediate nodes are labelled with the range of accounts which there are transactions for in all the leafs that can be reached from that intermediate node.

The exit game described is interesting because it allows for an application A to “read” state from an application B, without requiring the users of A to read the entire state of B.

> But these schemes pose a significant challenge: they complicate the fee market. Particularly, unless block producers are aware of how all of these layer-2 state schemes work (unlikely; there are just too many possible designs), if someone attempts to pay fees inside of one of these schemes then the block producer has no way to determine whether or not a fee is actually being paid.

In [LazyLedger](https://arxiv.org/abs/1905.09274), I use a scheme where you can pay block producers in any arbitrary currency application/contract that the block producer recognizes. You submit a fee transaction using that currency application, such the transaction is only valid if some other transaction corresponding to a specified hash is included in the same block’s Merkle root of transactions, since we only care about the data availability of that transaction. The block producer must compute the state of the currency application they’re accepting fees in to check that the fee transaction is valid.

> I had another idea for those schemes that allow spending money on any of the shards: What if you added in a mechanism that immediately burns the money if it was double spent? It would basically eliminate any incentive for someone to try and cheat by reverting one chart and getting their double-spending transaction in earlier.

Wouldn’t the fact that you can burn other people’s money at any time in the future mean that you can blackmail people to sending you more money or otherwise you’ll burn it? The longer you wait, the more transactions would have been made on top of your transactions, and the more money you can burn. As you also have to burn the money that your recipient sent, and so on, otherwise you have a money inflation vulnerability. If money changes hands a lot, then in the future you might be able to burn the entire supply.

---

**dankrad** (2019-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> Wouldn’t the fact that you can burn other people’s money at any time in the future mean that you can blackmail people to sending you more money or otherwise you’ll burn it? The longer you wait, the more transactions would have been made on top of your transactions, and the more money you can burn. As you also have to burn the money that your recipient sent, and so on, otherwise you have a money inflation vulnerability. If money changes hands a lot, then in the future you might be able to burn the entire supply.

Well you would only be able to burn it until it is crosslinked, so until the end of the current epoch (6.4 minutes). You can blackmail the recipient during that period, but that is unlikely to be successful given the shortness of time.

If you’re buying a house, you might want to wait until the end of the epoch, but for medium sized transactions (say a few 100$), this would give the recipient very high chance that they actually get their money even before it is crosslinked.

---

**vbuterin** (2019-07-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> One optimization to allow light clients to know that they’re being served the complete set of transactions for accounts they care about, is to use a Merkle tree where intermediate nodes are labelled with the range of accounts which there are transactions for in all the leafs that can be reached from that intermediate node.

Interesting! So basically validate a Plasma Cash-style Merkle tree inside of the block, so light clients can do a O(log(n)) sized query per block if that’s what they want to do.

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> The block producer must compute the state of the currency application they’re accepting fees in to check that the fee transaction is valid.

This is something I am trying hard to avoid. The point of abstraction is to simplify consensus code and allow consensus nodes to be simple and dumb even if the applications running on top are really complex, but that’s of limited value if the code that block proposers need to run to figure out what transactions to accept to get fees is complex and requires understanding all of these layer-2 schemes anyway.

Relayer markets seem to be the most general-purpose approach unfortunately…

