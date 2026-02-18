---
source: ethresearch
topic_id: 332
title: Account abstraction, miner data and auto-updating witnesses
author: JustinDrake
date: "2017-12-16"
category: Sharding
tags: []
url: https://ethresear.ch/t/account-abstraction-miner-data-and-auto-updating-witnesses/332
views: 3319
likes: 0
posts_count: 4
---

# Account abstraction, miner data and auto-updating witnesses

[Account abstraction](https://github.com/ethereum/EIPs/blob/bd136e662fca4154787b44cded8d2a29b993be66/EIPS/abstraction.md) is a powerful idea that allows e.g. for a cleaner EVM, better multisig, post-quantum secure signatures, and transaction expiry. It turns out account abstraction is general enough to allow for “miner data”, and this is very helpful for auto-updating witnesses in the context of stateless clients.

I call “miner data” transaction data provided by the miner during block creation. Instead of being signed by the transaction sender, miner data is constrained differently by the account abstraction init script. Below are examples of miner data constraints:

1. No miner data (minerData.length == 0): This is how transactions are processed today.
2. Miner-updated witnesses: From the stateless client proposal, “we put the witness outside the signed data in the transaction, and allow the miner that includes the transaction to adjust the witness as needed before including the transaction”. Using account abstraction for witnesses is cool for a couple reasons:

It means we don’t need to design an ad-hoc mechanism to include updated witness data, keeping the EVM clean.
3. It means “fancy accumulator schemes” can be first-class citizens! See the discussion here: “you can totally make your own contract that uses some fancy accumulator scheme, and it’ll be almost first-class (almost because you won’t get the benefit of miners auto-updating the witness if multiple actors send a transaction to modify the same accumulator at the same time)”
4. Miner-updated market data: Market data (e.g. stock prices) included in transactions can become stale between when the transaction is sent and when the transaction is mined. Miner-updated market data could “fill the latency gap”, and improve upon expire-and-rebroadcast schemes that suffer from more coordination with the miner, and higher bandwidth and latency.
5. Miner discrimination: It is possible to give exclusive mining rights for a transaction to a specific miner by having the init script require a signature of that specific miner in the miner data. This is possible today (broadcast your transaction to just one miner) but would add cryptographic guarantees.
6. Arbitrary miner data: This may be useful, e.g. to add entropy.

## Replies

**vbuterin** (2017-12-17):

justin:

> Instead of being signed by the transaction sender, miner data is constrained differently by the account abstraction init script.

I’d be interested in hearing more about this. Is the idea that the account can specify a script which checks the miner data provided with a transaction, and can reject any transaction that has invalid miner data, incentivizing miners to update the miner data of a transaction in place?

If so, then note that the account abstraction proposal as it stands already allows you to include or elide whatever data you want when computing the sig hash, so I don’t think we need further protocol changes for this to be possible.

---

**vbuterin** (2017-12-17):

Now that I think about it, if we combine this idea with partially stateless clients (namely, clients would store the entire top layer, but not contract storage), this could make rent much more feasible to implement. Users could either create objects in the top-level of the trie, for which they would have to pay ongoing upkeep fees, or they could use the abstracted possibly-miner-updateable witness scheme and thereby only have to pay upkeep for 32 bytes for an entire application.

Account storage could just be limited to 32 bytes; for anything larger, an updateable witness scheme would have to be used.

I potentially like this ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**JustinDrake** (2017-12-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is the idea that the account can specify a script which checks the miner data provided with a transaction, and can reject any transaction that has invalid miner data, incentivizing miners to update the miner data of a transaction in place?

Yes that’s exactly right.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I don’t think we need further protocol changes for this to be possible

Yes, very fortunate! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I tried to convey that when writing “It turns out account abstraction is general enough to allow for “miner data””. Incentivised miner data was hiding in plain sight all along.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Account storage could just be limited to 32 bytes; for anything larger, an updateable witness scheme would have to be used.

To my mind partially stateless clients make a lot of sense. They provide very significant storage sublinearity, potentially enough to remove any practical storage bottleneck. With rent it is likely the top-level of the trie can be stored entirely in RAM, removing the I/O bottleneck. We also want to engineer transactions to be minimally sized, and storing the top-level goes a long way towards reducing the witness sizes for applications with small amounts of storage.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Account storage could just be limited to 32 bytes; for anything larger, an updateable witness scheme would have to be used.

I briefly touched upon [“accumulator sharding” with several accumulators to allow for parallelism](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287/3). In order to unlock that for applications with easily parallelisable storage needs, my instinct would tend towards account storage being limited to a small array of 32 byte strings (instead of just one 32 byte string). We could incentivise the array to be super small simply by having large storage rent.

Having a small configurable storage array also gives more breathing space for application developers to make use of the tradeoff between storage and witness sizes. Imagine the following scenario, where a contract has 1,000,000+ infrequently-read accumulators objects and 100 extra-frequently-read accumulator objects. It would make sense to put those 100 extra-frequently-read objects in a segregated accumulator to benefit from small witnesses.

