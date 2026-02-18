---
source: ethresearch
topic_id: 7710
title: Decouple transaction pool from the rest of Ethereum node
author: AlexeyAkhunov
date: "2020-07-19"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/decouple-transaction-pool-from-the-rest-of-ethereum-node/7710
views: 2152
likes: 12
posts_count: 6
---

# Decouple transaction pool from the rest of Ethereum node

Based on some explanations given here: [Difference between Stateless Ethereum and ReGenesis regarding transaction pool](https://ethresear.ch/t/difference-between-stateless-ethereum-and-regenesis-regarding-transaction-pool/7709) I will propose a hypothetical architecture of Ethereum node that decouples transaction pool handing from most of other things that happen in it. This decoupling means that we could create a special type of Ethereum nodes, called “Transaction Pool nodes”, and their task would be exclusively to receive, verify, and propagate, transactions around the network. One of the main reasons to propose this is that if transaction pool nodes can be separated, engineering work on them can be performed by people specialising in this subject area, and they can add functionality and optimise within the confines of the protocol, and later on, suggest and implement improvements to the protocol.

The main idea is to make the **merkle proofs of `sender` accounts (which includes balance and nonce, those are required for basic anti-spam measures) mandatory** in the transactions. This will make transactions larger (3k more if we do not switch state to binary merkle tree, and 1k more if we do switch state to binary merkle tree), and it will also make transactions harder to produce. **The question is - will this be an acceptable tradeoff?**

If this is done, it will be just the first step towards gradually shifting the burden of maintaining the state from the core of the network (relaying nodes and mining nodes) to the perimeter (nodes that create and inject transactions). I believe that it will make the whole system more incentive compatible with further growth.

## Replies

**AlexeyAkhunov** (2020-07-19):

And here is how I think this can be achived operationally.

1. Create a separate p2p network for transaction pool. In this separate network, all transactions will need to be accompanied by the mandatory merkle proofs of their sender account.
2. Some Ethereum full nodes will start connecting to both eth p2p network and the transaction pool network, and act as bridges. They will always add merkle proofs when passing transactions from eth network to txpool network, and remove merkle proofs when passing transactions from txpool to eth network.
3. Given critical mass of such full nodes acting as bridges, specialised tx pool nodes can be added on, with greater capacity, connectivity, and some extra features for eviction and handling things like EIP-1559 transactions.
4. If the project is sucessful the transactions will start getting injected primarily into the txpool network directly, and not via eth network.

---

**carver** (2020-07-20):

What is the incentive to run a dedicated txpool node?

One of the benefits of bundling functionality is that the costs and benefits are bundled: if you want any benefit of the network, you pay all the costs of supporting it (at least by default). If we split out the costs of running the network, it seems like the incentives to run the node get diluted as well, and there will be less altruistic/default support of network features. With fewer bundled nodes, it becomes even more enticing to do something like: run a txpool node with the goal of matching IP addresses to transaction broadcasts and selling that data.

---

**AlexeyAkhunov** (2020-07-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/carver/48/150_2.png) carver:

> What is the incentive to run a dedicated txpool node?

As now, they can be run altruistically, but at lower cost. Mining pools might want to run more tx pool nodes than eth nodes. Also, some of the popular dapps.

![](https://ethresear.ch/user_avatar/ethresear.ch/carver/48/150_2.png) carver:

> One of the benefits of bundling functionality is that the costs and benefits are bundled: if you want any benefit of the network, you pay all the costs of supporting it (at least by default). If we split out the costs of running the network, it seems like the incentives to run the node get diluted as well, and there will be less altruistic/default support of network features. With fewer bundled nodes, it becomes even more enticing to do something like: run a txpool node with the goal of matching IP addresses to transaction broadcasts and selling that data.

Bundling can still happen, but at different level. Instead of bundling happening on the software level (by presenting a monolithic piece, the bundling can happen on the level of things like DappNode. The more components you’ve got, the harder it is for an ordinary user to configure them, so bundling will be happening. Think of it as Linux Distributions - most users still go for default settings, it just get easier to customise. I think there is a golden middle, where you can get enormous benefits of modularity (and therefore fostering third party development in the ecosystem) and bundling (through container and package providers).

---

**AFDudley** (2020-07-22):

To Carver’s point, it makes sense to me for this to be an option in geth. Maybe it makes geth too multifaceted, but at the start of the experiment, it seems reasonable.

---

**AFDudley** (2020-07-24):

I thought folks interested in this topic would be interested in Peter’s comment here:



      [github.com/ethereum/go-ethereum](https://github.com/ethereum/go-ethereum/pull/21358#issuecomment-663375644)














#### Comment by
         -


      `master` ← `hendrikhofstadt:fix/tx-sort-time`







Another potential idea could be to have a `types.TimestampedTransaction` (just t[…](https://github.com/ethereum/go-ethereum/pull/21358)hinking out aloud here for a debate, not sure it's a good idea), then the pool and miner could use that object, whereas the remainder of the code would remain oblivious. This would also be clean-ish API wise because you'd know that there's something funky going on in the txpool/miner, it's not just boring txs. Not sure though that such a wrapper is best placed in the `types` package or `core` package. Maybe we should finally separate the `txpool` out already from `core`.

