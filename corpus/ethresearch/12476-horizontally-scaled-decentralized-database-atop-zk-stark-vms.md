---
source: ethresearch
topic_id: 12476
title: Horizontally scaled decentralized database, atop ZK-STARK VM's
author: liamzebedee
date: "2022-04-22"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/horizontally-scaled-decentralized-database-atop-zk-stark-vms/12476
views: 4345
likes: 8
posts_count: 11
---

# Horizontally scaled decentralized database, atop ZK-STARK VM's

**Objective**: design a database which is horizontally scalable and decentralized

**Properties**:

- Horizontally scalable. The database scales by adding more nodes, which incurs linear cost.
- Decentralized. The database architecture is trust-minimized. The node operators cannot “mint money”.

### Design.

Let’s build a traditional distributed database. The database system is composed of a master node and a cluster of tablet nodes (a simplification of [BigTable’s architecture](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf)). The database is sharded, whereby each tablet node is responsible for a slice of the database. To add more storage capacity, you add more tablet nodes.

Users send `INSERT` and `SELECT` tranasctions to the master, who routes them to the tablet nodes.

This isn’t decentralized, because the computation is not verified. If this database tracked money, a tablet node could easily print money by modifying their balance. We need to verify the computations.

The problem with scaling blockchains is that verifying transactions is O(n) cost (where `n` is computational steps, ie. *gas*). It’s prohibitive. We can’t expect the master node to run every transaction themselves to verify.

However, what if we used a ZK-VM? The cost of proving a ZK-VM’s execution is polylogarithmic, roughly  O(log^2 n) . This scales much better. Cairo is a production-ready ZK-VM based on ZK-STARKS, and there are [other designs](https://ethresear.ch/uploads/short-url/3DM8kjFfIG6PHXu4qpYpmujXgme.pdf) based on EVM too.

Imagine that the master node and tablet nodes both ran their database (sqlite.exe) atop a Cairo VM. Then we could verify the computation was done.

New design - the master node distributes work via messages to the tablet nodes. The tablet node does the work, and generates a proof, which it sends back to the master node.

1. What about state growth? Well, Cairo program can employ nondeterministic programming. We don’t have to prove the entire database table shard in the computation, we only have to prove we’re modifying it according to some rules! Simply put - imagine the database shard was merklized, and running an INSERT tx is proving the assertion that the row was inserted into the merkle tree correctly. Using a Sparse merkle tree, we can construct an ordered map of (index→item), which is efficient to prove adjacent leaves of.
2. What if a tablet node is byzantine and decides to “rollback” the transaction? How do we ensure they only ever advance? Simple, we make every node a Cairo blockchain. Instead of messages, nodes communicate via transactions. Each transcation increments the node’s clock T+1, and naturally, references the previous block so that they form an immutable chain. The master node keeps track of every tablet node’s latest clock in their state too, which binds everything together.

Now we have a system where the tablet nodes are verifiably doing their job, the database state is sharded in a cryptographically authentifiable way, and the master node only incurs O(log^2 t) cost to verify these things are happening.

The last and easy part is now decentralizing the master node. The master node is mostly a coordinator - it distributes work to different tablet nodes and verifies they did their work. We can put this program on Cairo’s CPU. This is **recursive proofing** in an async context - while the master node is generating its own proof of its computation, it is awaiting the tablet node’s proof.

## Replies

**liamzebedee** (2022-04-22):

This architecture is probably best described as verifiable RPC between chains. This involves async cross-chain [message passing](https://ethresear.ch/t/cross-shard-messaging-system/6201) inside the chain’s VM, where the receipts contain validity proofs of the remote chain’s state transition. This is somewhat similar to some of the ideas in [optimistic receipt roots](https://ethresear.ch/t/fast-cross-shard-transfers-via-optimistic-receipt-roots/5337), though a lot simpler since we don’t rely on optimism in our security model.

---

**MicahZoltu** (2022-04-22):

Unless I’m bmissing something, you still have to solve the data availability problem, which is arguably the hardest part.

---

**liamzebedee** (2022-04-24):

Not missing something - how is it a hard problem though? Most L1 chains have the same approach, where data is available only because the ecosystem finds incentive to retain it (e.g. block explorers, API providers widely replicate the chain data).

Another idea - there’s a tonne of data availability providers nowadays. Think ETH 2.0, Filecoin, and some new rollup-specific designs like Celestia and Laconic. Not sure how you’d do the payment as part of the chain but certainly possible.

---

**MicahZoltu** (2022-04-24):

“The data availability problem” usually refers to the short term problem of ensuring that the data shows up on the network initially and is broadcast to all connected clients.  This is separate from the long term data storage problem of ensuring people who show up later can arqeire historic data.

The short term problem is much worse because an attacker can make a claim about some bit of data, but you cannot punish them for not providing the data because there is no way to prove they didn’t give the data.

This problem is a key part of the scaling problem because the solutions generally all depend on *everyone* on the network having access to *all* data initially (even though some will prune it).  So even if you can scale execution, you still have to shuffle around huge amounts of data to everyone which can end up being the bulk of the work.

---

**liamzebedee** (2022-04-26):

Ah right - thanks, you’ve actually cleared up my definition of DA. Data unavailability is a problem when verifying a blockchain, because without the data how can we verify the state machine is transitioning correctly.

Coming back to your question -

> Unless I’m bmissing something, you still have to solve the data availability problem, which is arguably the hardest part.

I wasn’t clear on how this design employs blockchains, so I will clarify (hell it wasn’t even clear in my mind before I started writing it, but this is how I imagine it could work).

In this architecture, **every application node runs an independent blockchain**, and achieves the same as Ethereum 1.0 in terms of data availability. This includes the master node, which distributes work to the tablet nodes, and tablet nodes, which actually store a shard of the database state, process queries/insertions, build the index, etc.

You can picture it best as something like the TCP/IP stack. In TCP/IP, you have the transport layer (TCP) and the application layer (HTTP). The transport layer gives any application the ability to reliably transport data. Similarly, in this model - there is the blockchain layer (Cairo CPU+Tendermint) and the application layer (database). The blockchain layer gives any application the ability to reliably delegate computation in a way which is horizontally scalable (due to the ZK validity proofs + async Cairo CPU).

The stack looks something like:

```auto
db-tablet | db-master node              # Application layer
Cairo VM                                #
Tendermint Blockchain/Consensus         # Blockchain layer
```

I’m using Tendermint here but it could be any finality/consensus mech. The main bit is that the state machine is cryptographically authentifiable, and fault-tolerant in a decentralized way (eg. block producer selection is decentralized).

---

**liamzebedee** (2022-04-26):

To use an example. Say this is a database of 1B rows. There is 1 master node, and 10 tablet nodes which each keep 100M rows each. A user runs a transaction to insert a row, which is sent to the master node, who sends it to tablet node #9 for completion, as it will only affect a single shard.

Tablet node #9 processes the transaction as such:

1. Receive blockchain tx, verify origin is from master node.
2. Begin executing tx.
i. Run the database query, insert the new row.
ii. Recompute merkle root of shard state.
iii. Generate merkle proof that state was updated correctly.
3. Generate ZK-VM proof of the blockchain’s state transition.
4. Mine the “block” - which includes this validity proof and the transaction.
5. Await finality on tx from consensus algorithm (Tendermint).
6. Send back the receipt to the master node - which includes the validity proof and new block tip.

---

**MicahZoltu** (2022-04-26):

Scaling by moving each application to its own “chain” is definitely a potential solution to the scaling problem, as only users of a given app need to store data about that app.  I have long lobbied for this as a general solution, rather than the current solution of monolithic chains.

The problem historically is that there is a desire to have assets fungible across applications.  People want to be able to do a single swap on Uniswap, then buy one NFT, then stake once on something else, update one ENS record, etc.  If you have every app on its own chain, then a user has to on/off to each application chain before each of their operations, which can potentially end up costing more than if they just did the operations on L1.

For particularly complex operations, off ramping, then doing work, then on ramping may be cheaper than doing it on L1 so this can still be a win.  For particularly low complexity transactions though (like Uniswap swaps), this can end up being a net negative solution.

---

**liamzebedee** (2022-04-26):

> People want to be able to do a single swap on Uniswap, then buy one NFT, then stake once on something else, update one ENS record, etc

Yeah, monolithic chains give you synchronous composability (that is, a call to another contract is always O(1) in time) at the expense of a very real ceiling on scalability due to the O(n) cost in verifying every tx. Even with ETH 2.0, we all recognise that cross-chain interactions is going to require some form of asynchronous composability, whether it be [yanking](https://ethresear.ch/t/cross-shard-contract-yanking/1450), some rollup bridges, etc.

What’s interesting however - is that this is exactly how web 2.0 API’s work, under-the-hood. Facebook, Reddit etc. are composed of many hundreds of interacting microservices and API’s in the backend. A call to an API to post may touch a caching system (Redis), a load balancer (nginx), an API backend (Django) and a database system (Cassandra) - all asynchronously during one call. And because there is no concern about verifiable computation, all of this can happen in under a second. I think it’s entirely reasonable a decentralized system could function the same way, with comparable UX.

> If you have every app on its own chain, then a user has to on/off to each application chain before each of their operations, which can potentially end up costing more than if they just did the operations on L1.

But what if this decentralized database was the backend to one single, horizontally scalable chain? e.g. all `sstore` and `sload`’s were just interfacing with this database specifically? This is entirely possible if the database can scale its capacity linearly by adding more nodes. In which case, users would only be transacting with one system. Remember - L1 is never going to handle more than 1000 tokens transacted at once, which is kinda flat in the grand scheme of things.

---

**fattyg** (2022-05-02):

Is flow control an issue If everything is still routed through one node?

If there is consensus on who owns what keys, then any node should also be able to route messages.

---

**liamzebedee** (2022-05-04):

Minor correction on my original post (I didn’t realise Ethresearch disables edits after a certain while) - the master server is NOT a bottleneck. This design is based on Google’s BigTable. They summarise it well:

> clients communicate directly with tablet servers for reads and writes. Because Bigtable clients do not rely on the master for tablet location information, most clients never communicate with the master. As a result, the mas- ter is lightly loaded in practice

