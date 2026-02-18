---
source: ethresearch
topic_id: 6973
title: The Data Availability Problem under Stateless Ethereum
author: pipermerriam
date: "2020-02-17"
category: Execution Layer Research
tags: [stateless, data-availability]
url: https://ethresear.ch/t/the-data-availability-problem-under-stateless-ethereum/6973
views: 7797
likes: 23
posts_count: 19
---

# The Data Availability Problem under Stateless Ethereum

# The Ethereum Data Availability Problem

This document covers what I have been thinking about as the *data availability problem*. I will cover the basics of how data flows around the Ethereum network today, and why the network continues to function despite having what appears to be a fundamental design flaw.  This flaw, lies in the combination of a basic network level reliance on the availability of full nodes from which data can be retrieved, combined with exposing APIs for on-demand state retrieval which can be used to create stateless clients.  I assert that stateless clients will naturally trend towards the majority on the network, eventually degrading network performance for all nodes.

After establishing a concrete definition of the problem, I then cover some solutions that are unlikely to work, followed by a proposal which is intended to be a starting point from which we could iterate towards a proper solution.

## Data availability in the current network.

In the current state of the Ethereum mainnet we have a single type of client, the full node.

> We ignore the LES protocol for simplicity, but it is covered a bit later in this document.

In the current network, all `ETH` nodes are assumed to operate as full nodes and to make available the entirety of the chain history (headers, blocks & receipts) and the state data (accounts from the account trie and the individual contract storage tries).

The only mechanism available for a node to adverstise what data it makes available is the [Status](https://github.com/ethereum/devp2p/blob/e54f53081a305c36a9251f14d77620462a657db0/caps/eth.md#status-0x00) message which supports advertising your `best_hash`.  This value indicates the latest block the client has. In theory, a client should not be asked for data that occurs later in the chain than the block referenced by `best_hash` since that client has signaled that their view of the chain does not include that data.

The `ETH` protocol is very forgiving allowing empty responses for the majority of data requests.  Typically a client which does not have a piece of data will respond with an empty response when asked for data they do not have.

The current most common mechanism for a node to join the network is using “fast sync”.  This involves fetching the full chain of headers, blocks, and receipts, and then directly pulling the entirety of the state trie for a recent block.

A client who is in the process of “fast” syncing must choose how to represent themselves on the network while their sync is in progress.

If Alice chooses to advertise to Bob that her `best_hash` is the current head of the header chain she has synced, then Bob will not be able to know Alice is missing the state data for that block since she has only partically synced the chain state.  This means when Bob sends Alice a [GetNodeData](https://github.com/ethereum/devp2p/blob/e54f53081a305c36a9251f14d77620462a657db0/caps/eth.md#getnodedata-0x0d) request, Alice is unlikely to be able to provide a complete response.

If Alice instead decides to be conservative and wait until she finishes syncing, then she would choose to advertise to Bob that her `best_hash` is the genesis hash.  In this model, Bob’s view is that Alice is stuck at the genesis of the chain and has no chain data.  In this case it is likely that Bob may disconnect from Alice, deeming her a “useless peer”, or simply never issue her any requests since Bob may assume she has none of the chain data.

These two cases are meant to demonstrate the lack of expressivity in this protocol.  In reality, clients seem to have chosen to use slighly more advanced heuristics to determine whether to issue a request for data to a connected peer. The lack of expressivity of `best_hash` results in it largely only being usable as an imperfect hint as to what data a peer *might* be capable of providing.

With the current network dominated by Geth and Parity, this has not proven to be incredibly problematic. According to `ethernodes.org` the mainnet network contains 8,125 nodes, 26% of which are in the process of syncing, and 74% which are fully synced.

So, despite not being able to reliably identify which nodes should have which data, in practice nodes can sync quite reliably. I attribute this to there being a majority of nodes which have all of the data meaning that simply randomly issuing requests to connected peers has a high probability of success.

## A Partial Problem statement

It is my assertion that the reliability of this network is heavily dependent on the assumption that all nodes are either full nodes, or in the process of syncing to become a full node, with a very small minority of disfunctional nodes (such as a node that has malfunctioned and is no longer syncing and stuck at an old block).  If the topology of the network were to change such that these assumptions were no longer correct, I believe that the process of syncing a full node will become increasingly difficult.

RESEARCH: play with the numbers to maybe provide some extra insight into how changing the distribution of full nodes, to nodes missing data would change sync times…

One way that this may come to pass is through broader adoption of the “beam” sync approach to client UX.  A client that is syncing towards being a full node can be viewed as triggering some accumulation of “debt” on the network, as they are requesting more data than they are providing to the network.  The network can handle some finite volume of this behavior.  Under the assumption that all nodes eventually become full nodes, most nodes eventually pay back this network debt by providing data to other nodes.

Suppose a client implements beam sync without the background sync to fill in the full state.  Such a client will continually take from the network by continually requesting data on-demand.  If the population of the network is sufficiently dominated by such a client, then it would eventually surpass the overall networks ability to supply the demand created by these clients.  It is unclear exactly how this would effect the network as a whole as well as individual clients, but my intuition is that both the offending beam syncing nodes and the network’s full nodes would suffer.  The full nodes would be overwhelmed by the beam syncing node requests, preventing other nodes who are in the process of syncing from being able to sync.  Similarly, the beam syncing nodes would suffer degraded performance as they are unable to find full nodes who are able to provide the necessary data.

- New nodes attempting to sync would have problems finding peers who have the data they need.
- The bad “beam” syncing nodes would no longer function well because they would be unable to find nodes that have the needed data.
- Full nodes would be unable to serve the demand, likely degrading the performance of the node under the heavy request load.

My intuition is that this is a problem with the network architecture, rather than the nodes.  While it is easy to view the “bad” beam syncing nodes as doing some irresponsible, we have chosen to operate on a permissionless network and thus we cannot reasonably expect all network participants to operate in the manner we deem appropriate.  The only two options available to address this problem are to address it at the protocol level, or to attempt to address this at the client level.  The client level fixes are likely to ultimately be a sort of “arms” race, so we’ll ignore that option and focus on the protocol aspect.

## Enter “Stateless Ethereum”

“Beam” sync can be viewed as a highly inneficient stateless client.  The mechanism by which it fetches state data on-demand via the `GetNodeData` primative requires traversal of the state trie one node at a time.  Naively this means issuing requests for single trie nodes to a peer as the client steps through EVM execution, encountering missing state data.  Some basic optimizations like parrallel block processing and optimistic transaction lookahead processing provide the improvements that make this approach viable, but these improvements are tiny compared to proper “witnesses”.

The “Stateless Ethereum” roadmap is designed to modify the protocol to formally support stateless clients in the most efficient manner possible.  This is likely to involve:

- Protocol changes to reduce witness sizes (binary tries, merklizing contrac tcode)
- Protocol changes to bound witness sizes (gas accounting for witness sizes)

Both of these improve the efficiencly of a stateless client, and thus should reduce the overall load that a stateless client places on the network.  The best case for stateless client is small efficient witnesses for block verification.  Alternatively any protocol that allows for syncing of the state also allows for on-demand construction of witnesses.  Both of these approaches rely on full nodes to be data providers.

Current thinking is that a very small number of full nodes should be able to support providing witnesses to an arbitrarily large number of stateless nodes due to the ability to use gossip protocols to have stateless clients assist with the dissemination of witnesses.  This is akin to bittorrent style swarming behavior.

However, for stateless clients to provide a useful user experience, they will need more than witnesses from the network.  For stateless clients to be viable for a broad set of use cases, they need to be able to have reliable on-demand access to the full chain and state data.

Examples in the JSON-RPC APIs.

- eth_getBalance: Needs proofs about account state
- eth_call: Needs proofs about account state, contract state, and the contract bytecode.
- eth_getBlockByHash: Request block and header data
- eth_getTransactionReceipt: Request block, header, and receipt

While all of the data above can be requested via the `ETH` devp2p protocol, it doesn’t seem like the full nodes on the network would be able to support the request load, not to mention the other forementioned negative effects that too many leeching peers would trigger.

# Narrowing in towards a solution

At this stage you should have a decent picture of the problem.  Stated concisely.

- Any protocol that supports syncing towards a full node appears to also support inneficient stateless clients
- A sufficiently high number of these stateless clients will overwhelm the full nodes.
- Any attempt to mitigate this at the client level is likely to be innefective against a motivated client developer since differentiating between a leeching node and a node which is in the process of a full sync is expected to be imperfect.
- Changes to the protocol to support stateless clients in the most efficient ways possible will only provide temporary mitigation.
- In the stateless paradigm we expect stateless nodes to far outnumber full nodes.

We cannot support a large population of stateless nodes on the current `ETH` protocol, nor can we do it on an improved `ETH` protocol that supports witnesses, and we also cannot prevent stateless clients from being created.

It is also worth noting that stateless clients are likely to have a better UX than the current status quo (until they crush the network and then none of the clients work very well)

## Solutions that probably wont work

### Asymetric protocol participation

`LES` seems to demonstrate that an asymetric protocol does not scale without incentives.  For such a network we’ll refer to the ones who have the data as the *providers* and the ones who need the data as the *consumers*.  Networks with this provider/consumer hierarchy seems to have a natural limit at which an imbalance in the ratio of providers to consumers causes the providers to be overwhelmed by the consumers and inherently suffers from a tragedy of the commons problem.

### Incentives

A commonly presented solution for the provider/consumer model is to introduce (economic) incentives.  This approach is problematic as it places a high barrier to entry on node operators and is non trivial to bootstrap (requiring people acquire currency and fund an account before even being able to sync a node).  Given that one of the goals is for our network to be easy to join, requiring node operators to fund their clients will likely have an adverse effect on adoption.

### Treating this as a discovery problem

One way to view the problem is to treat it as a discovery problem.

I previously outlined that the current mainnet would suffer if the assumption that all nodes are full nodes were to be sufficiently wrong, resulting in clients having increased difficulty in finding the data they need.

One might try to fix this by improving the expressiveness of the client’s ability to specify what data it makes available. My intuition for this model is that it could serve to bolster the current network, allowing the network to continue to operate to a higher threshold of imbalance between nodes that have the data and nodes that do not.  However, such a mechanism would also serve as a way for nodes to discriminate against less statefull nodes, resulting in stateless nodes having similar problems to the current issuse `LES` nodes face.

This problem would likely be exhaserbated since we cannot rely on nodes to be honest, allowing stateless nodes to mascerade as stateful nodes.  If the scaling mechanism of the network relys on the accuracy of this data, then my intuition says that we end up in the same situation that the network exists in today, where clients rely on imprecise heuristics to determine the usefullness of clients, resulting in this broadcast information being nothing more than a potentially helpful hint that still must be verified.

## Node type definitions

Lets take a moment to define the different node types more precisely.

All node types track the header chain but potentially might not keep the full history.  Note that the Syncing node and the Stateless node have roughly the same requirements.

### Full Nodes:

Defined as a node which has the full state for their head block and some amount of historical chain data.

> Note this is explicitely changing the expectation that a full node does not necessarily have all blocks and receipts

- gossip of new headers/blocks/witnesses
- gossip of pending transactions
- on demain retrieval of blocks, headers, receipts that they do not actively track

> Note that the block/header/receipt retrieval is not needed if the node keeps the full history.

### Syncing node

Defined as a node which has an incomplete copy of state for their head block and some amount of historical chain data.  This node type keeps data, building towards a full copy of the state, and a full copy of the historical chain data for the historical chain data they choose to retain.

- gossip of new headers/blocks/witnesses
- gossip of pending transactions
- retrieve blocks, headers, receipts on demand.
- retrieve state on demand
- retrieve contract code on demand

### Stateless node

Defined as a node which does not retain a full copy of the state or the chain data.  The extreme version of this is retaining none of the data.

- gossip of new headers/blocks/witnesses
- gossip of pending transactions
- retrieve blocks, headers, receipts on demand.
- retrieve state on demand
- retrieve contract code on demand

## Deriving network topology from client needs and expected rational behavior

There are multiple participants in the network who have economic incentives to run full nodes.

- Miners get paid to produce blocks, and need the full state to do so.
- Centralized data providers like “infura” have a business model built around having this data available for parties willing to pay for it.
- Businesses building blockchain based products need infrastructure to connect to the blockchain.  While not all use cases will require the full chain state, many will.

I don’t believe there is reason to be concerned about “losing” the state.  However, it is reasonable to expect these nodes to be *selfish* as this behavior will be necessary for self preservation.  Full nodes will be unable to support the demand for data that a large number of stateless nodes would create.  It is also reasonable to expect there to be fewer full nodes on the network as hardware requirements increase and less hardware intensive clients become available.

It is also important to note that from the perspective of a full node, differentiation between a node which is syncing towards becoming a full node and a stateless node mascerading as a syncing node is likely to be imprecise and an “arms race”.  Thus, it seems reasonable to expect this need for a new way to access the chain and state data to be an issue for both stateless nodes and nodes which are syncing towards becoming a full node.

So, in this new network, we expect the topology to have the following properties.

- Full nodes restrict their resources primarily for other full nodes or potentially.
- All node types participate in the gossip protocols for new headers/blocks/witnesses

This has the following implications:

- all nodes should be interconnected for the gossip protocol.
- all nodes will need access to the chain data, but that full nodes are unlikely to be able to reliably provide it since some may choose to prune ancient chain cdata.
- both stateless and unsynced full nodes will need access to the state data.

# A Possible Solution

What follows is the best idea I have to address the problems above.  It is meant to be a starting off point and would require broad buy-in and much more research and development to be viable.

First, a protocol that is explicitely for gossip.  All nodes would participate in this protocol as equals, assisting in gossiping the new chain data as it becomes available.  We already have this embedded within the current DevP2P `ETH` protocol, however in the current form it is not possible to participate in only this part of the protocol.

Second, a protocol where all nodes can participate as equals to assist in providing access to the full history of the chain data and the full state for recent blocks. While some nodes might have the full data set, most nodes would only have a piece of it (more on this below)

> The term “protocol” is meant to be vauge.  It could be a new DevP2P protocool, something on libp2p, etc.  At this point I’m focused on defining the functionality we need after which we can bike shed over implementation details.

## Distributed Storage Network of Ethereum Data

This is a concept to fill the need that all nodes will exhibit for reliable access to the full historical chain data and recent state data.

### Data Types

This network will provide access to the following data, likely through something akin to the DevP2p `ETH` protocols various `GetThing/Thing` command pairs.

- Headers
- Block Bodies (uncles and transactions)
- Receipts
- Witnesses
- State Trie Data (both accounts and contract storage)
- Contract Code

In addition to this it may be beneficial if we can find ways to store the various reverse indices that clients typically construct (see section below about “extra functionality beyond the standard ETH protocol”)

### Basic Functionality Requirements

#### Finding Peers

Nodes need to be able to join the network and find peers that are participating in their chain.  The recent [“ForkID”](https://eips.ethereum.org/EIPS/eip-2124) seems to be the best candidate to efficiently categorize peers into subgroups where all nodes are operating on the same data set.

#### Data Ingress

The network needs a mechanism for new data to be made available.  The forementioned gossip network is a provider of this data.  A simple bridge between these networks might be adequate.

While it might be tempting to combine the gossip and state network, I believe this would be incorrect.  A valid use case which needs gosip bup does not need any of the data retrieval APIs is a full node which also stores all of the historical chain data.  Such a node has no need for the data retrieval APIs and should be allowed to limit participation to the gossip protocol.

#### Data Storage

I believe what I am describing below is just a DHT, maybe a special purpose one.

We need the network as a whole to store the entirety of the chain data and state data, while allowing individual network participants to only store a subset of this data.  Nodes could either all store a fixed amount of data, or nodes could choose how much data they store.  It is not yet clear what implications these choices might have.

There needs to be deterministic mechanism by which a node can determine “where” in the network a piece of data can be found.  For example, if I need the block `#1234`, a node should be able to determine with some likelihood which of the peers it is connected to is most likely to have that data.  This implies some sort of function which maps each piece of data to a location in the network.  Nodes would store data that is “close” to them in the network.

We may need some concept of radius, where a node stores and advertises the radius in which it stores data.

Nodes who are joining the network would also need a mechanism to “sync” the historical data for their portion of the network.

As new headers/blocks/receipts/witnesses propogate through the network as the chain progresses, nodes keep the ones that are their responsibility to store, and discard the rest.

#### Data Retrieval

One of the main differences to this network as opposed to the current DevP2P `ETH` protocol is that we likely need routing.  Data needs to be reliably retrievable, and we only expect any given node to have a subset of the data.  For this reason, we can expect that there will be pieces of data that are not avialable from any of your connected peers, even for very well connected nodes in this network.

Routing is intended to make requests for data reliable.  A node receiving a request for data that they do not have would forward that request on towards their peer(s) which are most likely to have the requested data, forwarding an eventual response back to the original requester.

#### Extra functionality beyond the standard ETH protocol APIs

The following functionality is exposed by the standard JSON-RPC API, however, it requires a client to have a full picture of the chain history to serve responses.  For example, the only way to retrieve transactions that are part of the canonical chain is to retrieve the block body of the block the transaction was included.  The standard behavior of clients is to create a reverse index which allows clients to query the block number-or-hash for a given transaction hash which then allows retrieval of the transaction from the block body some clients may differ but the high level take away is the `ETH` protocol has no mechanism for retrieving a transaction by hash.

- Ability to lookup the canonical block hash for a transaction referenced by the transaction hash.
- Ability to lookup the canonical block hash for a given block number.
- Ability to lookup the receipts for a given block hash

### Network Design Principles

#### Homogenous

The networks should have a single homogenous node type.  This should reduce asymetry between nodes.

- reduce incentives for nodes to be selfish by making all nodes usefull to all other nodes and making node behavior simple.
- reduce ability for nodes to discriminate by making all nodes behave in a similar manner.

#### Minimal hardware requirements

If we want broad participation then the hardware requirements for running a node should be as small as possible.  I would propose using something like a raspberry pi as a possible baseline.

A starting point for hardware goals:

- ability to run the node with <500MB of available ram
- nodes can be ephemeral, operating purely from memory, persisting minimal data between runs, and not persisting any network data between runs.
- nodes can easily validate the content of the data they store against the header chain with a single CPU core.

#### Inherent load balancing

The network should contain a mix of full nodes, nodes with partial state, and nodes that only have ephemeral state.  It would be ideal if the protocol could exhibit basic load balancing across the different participants.

For example, ephemeral nodes may be able to handle more of the routing, while full nodes can handle a larger quantity of the actual data retrieval.

#### Bittorrent swarming behavior when possible

We should aim for bittorrent style swarming behavior whenever possible.  Some of this can be accomplished simply by having well documented conventions.

Example: Naive implementation of state sync is to walk the state trie from one side to the other, fetching all of the data via this simple iterative approach. We can alter this approach by using the block hash of every `Nth` block to determine the path in the state trie where clients would start traversing the trie.  This produces emergent behavior that all clients which are currently syncing the state will converge on requesting the same data which better utilizes the caches of the nodes serving the data as well as allowing partially synced nodes to more reliably be able to serve other partially synced nodes.

This approach should be able to be replicated across other node behaviors and the simple process of documenting “best practices” should go a long way.

Another option would be ensuring that requests are easy to cache which lets nodes which have recently routed a request to cache the result and return it on a subsequent request for the same or similar data.

### Likely problems and issues that need to be thought about.

#### Header Chain Availability

Ideally, every participant of this network would store the full header chain, however, the storage requirements may be too steep for the types of nodes we expect to participate in this network.

Thus, we may need a mechanism to efficiently prove that a given header is part of the canonical chain, assuming that all nodes track some number of recent headers.

It may be *ok* to require all participants to sync the entirety of the header chain and do some sort of data processing on it, but allow them to then discard the data.  Can we do something fancy here?

TODO: Look into Eth2 research on how they do this for their light protocol. Something like a set of nested merkle tries which allow for a tuneable lightweight mechanism, though it appears it would require nodes to either trust someone to provide this data for them upon joining the network, or to fully process the canonical header chain to produce these merkle tries since they are not part of the core protocol.

#### Eclipse Attacks

A simple attack vector is to create multiple nodes which “eclipse” a portion of the network, giving the attacker control over the data for that portion of the network.  They could then refuse to serve requests for that data.

#### DOS Attacks

We may need some mechanism to place soft limits or throttling on leeching peers.  The ideal state of the network is to have a very large number of participants which are all both regularly requesting and serving data.  We however should not rely on this naturally occuring since there is a natural tragedy of the commons problem that arrises from any node behavior which requests significantly more data than it serves.

#### Lost Data

It is more likely that this network could fully lose a piece of data.  In this case the network needs a mechanism to heal itself.  Intuition suggest a single benevolent full node could monitor the protocol for missing data and then provide that data.

## Replies

**quickBlocks** (2020-02-18):

One thing you said above strikes me as familiar:

> There needs to be deterministic mechanism by which a node can determine “where” in the network a piece of data can be found. For example, if I need the block  #1234 , a node should be able to determine with some likelihood which of the peers it is connected to is most likely to have that data. This implies some sort of function which maps each piece of data to a location in the network. Nodes would store data that is “close” to them in the network.

This to me sounds almost exactly the same thing as a content-addressable data store such as IPFS.

Weird thought: In the header of each block, carry content-addressable hashes of the data (tx, block, receipt, state). Then, hash those hashes together and quite literally make that resulting hash THE block hash. Full nodes could operate almost as they do now, the hash they report for each block would serve an identical purpose as it does now, but unlike now, the hash would also have a ‘meaning’ and that meaning would be an answer to the question “Where can I get the data?”

---

**pipermerriam** (2020-02-18):

[@quickBlocks](/u/quickblocks)

My work last year trying to bridge the Ethereum and Swarm networks to make the Ethereum chain data available via Swarm gave me some intuition in this area as well as just identifying concrete problems with this approach.

First, for the “state” data (accounts, contract storage), I know of no reasonable way to get a content address that would work for a storage network.  The state root isn’t a content address, and it isn’t feasible to compute an actual content address for a 12gb file every 15 seconds.  Chasing a middle option of sub-dividing the state into smaller chunks might work, but then you need to figure out how to have content addresses for those chunks as part of the protocol.  My conclusion was ultimately that for the state, it is very difficult to retrieve it from a network that does naive content addressed storage, because you really need the network to be aware of the data structure so that it can make the various efficiency shortcuts needed to facilitate efficient retrieval.

Another issues is that even if we could bake some content addressable hashes into the protocol for things like headers or transactions which both lend themselves “ok” towards being stored and retrieved this way, we wouldn’t have this data available for old blocks that occurred before the change.

The generalized version of this issue is that the way we bake in mechanisms to have all of the data from the chain be verifiable is often not suitable for use for the purposes of retrieving the content, and that in some cases, it may not be feasible to have the mechanism do both things well.

---

**musalbas** (2020-02-19):

To avoid confusion, I think we should be careful about the name used for this problem. The phrase “[data availability problem](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding)” is currently used to refer to the problem of verifying that data behind a block header was even published in the first place. The problem you’re describing seems to be about how efficiently light clients can retrieve that data, if only very few nodes are distributing that data. I propose that we call that problem the data distribution problem.

I strongly agree with the approach of allowing each node to contribute a small amount of storage to the network, creating a peer-to-peer BitTorrent-like data sharing network. This is the approach we’ve taken in the [LazyLedger proposal](https://ethresear.ch/t/a-data-availability-blockchain-with-sub-linear-full-block-validation/5503), and [other researchers](https://arxiv.org/abs/1805.00860) have taken this approach too.

While this is fairly simple to do for distributed block data storage, I’m not sure how it can be efficiently done for the computed state of the chain, because it changes every block. Do you have any thoughts about this? I suppose if the state was committed as a Sparse Merkle tree, clients could download “diffs” of the subtree they are storing.

---

**pipermerriam** (2020-02-19):

Agreed on finding a new name for this.  I will find a new name before publishing anything new on the topic.

As for the issue you mention about the state data and how it changes differently.  If we assume clients have an EVM available (which isn’t an assumption I like), then the witness + executing a block will allow clients to compute a state diff and update the state they are storing.  This however is not ideal since EVM execution is inherently heavy and I’d very much *like* participation in this network to not hinge on having EVM execution available.  It is my understanding/intuition that a witness is not sufficient to update an existing proof of the state.  It would be ideal if there was a way for clients to compute/receive/something state diffs in a provable manner.  Curious if anyone has any deeper insight into this concept/approach.

---

**musalbas** (2020-02-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> It is my understanding/intuition that a witness is not sufficient to update an existing proof of the state. It would be ideal if there was a way for clients to compute/receive/something state diffs in a provable manner. Curious if anyone has any deeper insight into this concept/approach.

If you represent the state as a Sparse Merkle tree, you definitely can update the state root purely using a witness, even if you’re storing a small part of the state. I implemented this [here](https://github.com/musalbas/smt/blob/aa7630b2df3b201df847978c9b7504d3ed970fe8/deepsubtree.go) using a concept I call a “deep Sparse Merkle subtree”. Example usage [here](https://ethresear.ch/t/data-availability-proof-friendly-state-tree-transitions/1453/23). You can store only a subset of the state tree, which you represent as a subtree, and recompute the state root of the entire tree by updating the subtree with witnesses. What I haven’t implemented yet is recomputing the root of the tree by updating the roots of the subtrees you’re not storing, but that’s doable.

Light clients that just want to participate in state data distribution don’t need to re-execute the transactions in the block to recompute the state root, if they just use witnesses from the new (already computed) state root, so I don’t think you need to assume that they have the EVM available. They can assume that new blocks and their new state roots are valid, and update their tree accordingly with witnesses.

---

**lithp** (2020-02-21):

I think you’re being a little unfair here. Maybe nobody’s tried to pitch statelessness to you yet?

> It is a solution in search of a problem IMO

The problem is pretty clear: it’s difficult to run an ethereum node and it’s only getting more difficult over time. I’ve talked about statelessness with multiple people at Coinbase, for example, and they’ve all been pretty excited about it. They spent a lot of time building a fancy system to build and maintain backups of their geth nodes so they don’t need to re-sync from scratch every time they start a node. Sometimes they have to re-sync from scratch anyway, and leave a machine sitting around and syncing for a day before it becomes useful.

Aren’t you annoyed that you have to buy a fancy nvme ssd in order for the nodes you run to have reasonable performance? Or that you can’t run more than a few nodes at once on the same machine?

I’m annoyed! [Trinity](https://trinity.ethereum.org/) has been a few steps away from finished for over a year now. The missing piece is a decent user experience during initial sync. And it’s not just Trinity who’s having a hard time. Maybe Parity would have stuck around if it was easier to support Ethereum; it’s an interesting coincidence that they stopped working on their client soon after the state trie grew so large that [Warp Sync stopped working](https://github.com/paritytech/parity-ethereum/issues/11071).

I’m not sure how many DAPP developers are annoyed but I’m sure at least some of them are. The high cost of state means at least some of them have to redesign their apps to use less state. Wouldn’t it be nice if they only had to pay the miners to store their state? Right now they have to pay an amount which accounts for the fact that their state burdens the entire network.

It’s a stretch too far to say statelessness isn’t trying to solve a real problem. From what I can tell, this is **the** problem.

> If moving to stateless clients makes the entire system harder to program and understand

I understand the concern about complication, I’m very interested in making the spec so simple that it definitely works. There’s a quote of [questionable provenance](https://quoteinvestigator.com/2012/04/28/shorter-letter/), maybe it’s from Mark Twain: “I didn’t have time to write you a short letter, so I wrote you a long one”. Currently, stateless ethereum is in the middle of being researched, we haven’t had enough time yet to even show that it works. Once that happens we’ll have the time to make it simple.

---

**adlerjohn** (2020-02-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> lets find a way to pay each of them $10,000 a year

Do you have a concrete proposal on how to do this that isn’t isomorphic to the status quo? I’d guess any solution for this challenge would introduce more complexity than any stateless client proposal ever could.

---

**dankrad** (2020-02-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> The way I see the stateless client concept, it is a tradeoff between nodes doing more storage and more computation and making the system much more complex by introducing witnesses etc. Since storage and computation are cheap and getting cheaper, a better solution imo is simply find a way to incentivize nodes to have more storage and more computational power.

We all agree that the problem is not storage itself and total availability of computation. The problem is serial computation (and serial access of storage/memory), where progress has very nearly ground to a halt.

Compared to that, witnesses only add to bandwidth requirements. Bandwidth still increases loads year on year.

And by using the stateless concept, it turns out we can parallelize a lot more. Because now anyone can jump in at any point in any computation and verify its correctness.

---

**lithp** (2020-02-25):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> We have I think several thousand non-mining nodes in the network, lets find a way to pay each of them $10,000 a year, it is peanuts comparing to billions that miners make.

I wonder if you can talk about this some more. Do you have a more concrete idea we could all talk about?

Just working off of what you have here, I have a few objections.

1. Sybil attacks: If you’re paying me $10k/yr per node, I’m going to spin up as many nodes as I can. The entire point of ethereum is that anyone can run a node, so I’m not sure where the money to pay for the inevitable millions of nodes come from.
2. It seems backwards to pay nodes for participating in the network; they’re not providing any service to it. When I run a node in my house so that I can have a local JSON-RPC endpoint and run DAPPs against it, I’m not really doing anything for Ethereum. It’s the opposite, I’m consuming some of the network’s resources! It’s kind of strange that I would be given $10k/yr to make other nodes send me blocks and forward my transactions.
3. This proposal enables an inefficiency that it would be better to remove entirely. Every time a machine runs a transaction or fetches some state from disk it expends some energy which has a real economic cost. Asking every single node to run every transaction magnifies the costs of each transactions by the number of nodes, something which will show up as either increased inflation or increased txn fees. Somehow, somebody has to pay for it. Stateless ethereum reduces the number of nodes which need to do the expensive work of looking for and fetching state from disk, something which makes the network much cheaper to run than paying every node $10k per year would do.

---

**lithp** (2020-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Agreed on finding a new name for this. I will find a new name before publishing anything new on the topic.

Maybe this name is too similar, but in my own notes I’ve been calling it state retrieval. Somehow, network participants need to be able to retrieve state.

---

**cburgdorf** (2020-02-25):

> It seems backwards to pay nodes for participating in the network; they’re not providing any service to it. When I run a node in my house so that I can have a local JSON-RPC endpoint and run DAPPs against it, I’m not really doing anything for Ethereum. It’s the opposite, I’m consuming some of the network’s resources!

Can you help me understand this point? If I run a node at home (which I do!) I’m also *serving* to other nodes so I have a hard time following the argument that I’m actually bad for the health of the network.

> Stateless ethereum reduces the number of nodes which need to do the expensive work of looking for and fetching state from disk

Another way to frame it is that the network is becoming more centralized because miners will be the only ones to hold on to the state (unless the state is highly accessible through other means for all the other nodes e.g. a DHT). In a world where only miners hold the state aren’t we much more at risk that the network gets captured by miners and everyone else has to play by their rules?

---

**lithp** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/cburgdorf/48/683_2.png) cburgdorf:

> Can you help me understand this point? If I run a node at home (which I do!) I’m also serving to other nodes so I have a hard time following the argument that I’m actually bad for the health of the network.

This answer is too long, sorry! But I wrote out something short and realized this was something worth thinking about more. My original phrasing was a little too strong, I don’t fully believe that you’re bad for the health of the network (even though that’s the way I’ll conclude below), but I do believe that you’re not providing much of a service, and I think the network would prefer to have a certain number of full nodes. Too few is harmful, and too many is also harmful.

There’s an easy case, your node is certainly harmful when you first start running it! For as long as you’re fast syncing you’re asking other nodes to do quite a lot of work for you, fetching state off their disks. However, once your node has been running long enough it’ll have helped enough new nodes to join the network that everything balances out.

Once you’ve finished syncing, though, you’re still not doing much for the network. There are two sets of actors, each of whom want slightly different things:

**Miners** care that their blocks are quickly sent to other miners. This means their blocks are less likely to be uncled, and they make more money. Really, everybody cares about this! Lower uncle rates mean the network is more secure.

**Users** (including Dapps and exchanges) care about being able to see the current state of the blockchain. They want to be able to fetch and validate blocks as soon as those blocks are created. Weakly, everyone kind of also wants this for other users; the easier Ethereum is to use the more usage it will see.

From the miner’s perspective, a miner only sends you blocks because that miner hopes you’re also a miner! If you’re not a miner (from the outside it’s kind of hard to tell) the miner is hoping that you can at least send the block to other miners. However, even if you can do so, the two miners you’re connecting would prefer to be directly connected to each other! Your node adds a small amount of delay to block propagation, which ever so slightly increases the uncle rate. Again, *everybody* would prefer that your node wasn’t in the way! If the Ethereum network contained *only* miners then block propagation would be faster and the network would be more secure and we the gas limit might even be higher.

From the user’s perspective it’s complicated, because again, they’re happy to receive blocks from you but they would prefer that you weren’t there at all, that you weren’t adding a delay to the time it takes them to notice blocks. However, given that there are going to be a lot of peers trying to read and validate the chain, everyone’s kind of happy that you’re taking some load off of the miners, that you can forward blocks instead of making miners do all the forwarding. You’re also acting as a bit of a shield, you’re making it a little harder to find miners and attack them.

Both of those effects, taking some load off the miners and obscuring their locations, are effects which only take some full nodes in order to be realized. I don’t know what the “right” number would be, but it cant be much larger than 100. However, the ill effect, the delays that new full nodes add to block propagation, only get worse the more full nodes there are! Adding a new full node, when we already have 8000, does nothing but slow down the network just a little more.

---

Edit to add: the largest miners are already directly connected to each other, so when you run a full node which adds a block propagation delay you’re hurting the smaller mining pools, which aren’t directly connected to the others, more than you’re hurting the larger mining pools. So, you’re increasing the incentive to join a larger mining pool.

---

**lithp** (2020-02-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/cburgdorf/48/683_2.png) cburgdorf:

> Another way to frame it is that the network is becoming more centralized because miners will be the only ones to hold on to the state (unless the state is highly accessible through other means for all the other nodes e.g. a DHT). In a world where only miners hold the state aren’t we much more at risk that the network gets captured by miners and everyone else has to play by their rules?

As a class miners already have most of the power! They can choose to run whatever rules they’d like (assuming they can agree among themselves), and if it’s a choice the community doesn’t agree with then we’ll have to fork and run our own miners.

---

**cburgdorf** (2020-02-26):

Thanks, I haven’t thought much about how non-mining full nodes at time to the block propagation times between miners. Thankfully POS under ETH2 will change that and I should be able to run a validator at home.

> As a class miners already have most of the power!

I’m in full agreement. The question is, would this concentrated power even increase further?

> and if it’s a choice the community doesn’t agree with then we’ll have to fork and run our own miners.

Correct! And today every full node can theoretically turn into a mining node quite easily (if we ignore mining hardware for now). But what if miners become the only ones who have easy access to the state? How would the community fork and run their own miners if they can’t easily obtain the state?

---

**pipermerriam** (2020-02-26):

Here is a write up on a more “middle-of-the-road” approach to mitigating this issue which I’m now referring to as the “Data Retrieval Problem”.

Here I pose an approach which:

- Attempts to limit the ability to create stateless clients via “abuse/misuse” of the on-demand state retrieval primitives which are aimed at facilitating full node syncing.
- Greatly improve the overall efficiency of the network with respect to syncing the state (unlocking the data prison)
- Facilitate the creation of stateless clients which expose limited user facing functionality (they would be unable to handle arbitrary eth_call type requests which touch arbitrary state).

## First class stateless clients via witnesses

First, we need to allow stateless clients to exist in a first class way via witnesses.  We can theoretically do this *now* without any of the efficiency improvements that binary tries and code merklization provide.  Care would need to be taken to be sure that “attack” block which produce huge witnesses don’t effect the traditional network.

This would involve coming to a “final” version of the [witness spec](https://github.com/ethereum/stateless-ethereum-specs/pull/1#) and ideally including a hash reference to the canonical witness in the block header.  We *might* need to include a “chunking” mechanism in there somewhere to ensure that retrieval of large witnesses can be done in a manner that allows incremental verification but I believe the current witness spec actually already provides this.

By formalizing witnesses and placing them in the core networking protocol we allow beam syncing and stateless clients to exist on the network without *abusing* the state retrieval mechanisms that nodes which are working to become full nodes are using.

## State sync scalability via swarming behavior

Next, we aim to improve the efficiency of nodes which are working towards being full nodes by syncing the state.  Alexey has used the term “data prison” to refer to the ?fact? that fast sync mostly works because it pulls state from multiple peers.  Attempting to pull the full state from a single peer tends to run up against hard drive limitations to read the data fast enough.

To accomplish this we need to come up with an agreed upon algorithm that nodes syncing the state will use to determine which parts of the state they fetch at a given time.  This approach needs to have the following properties.

- Zero active coordination.  This needs to be emergent behavior based on publicly available information.
- Swarming.  Two nodes who are both in the process of syncing the state will converge on requesting the same data.

There are likely many ways to do this.  I pose the following approach as a simple example that has the desired properties as a starting point from which we can iterate from.

First we treat the key space of the state tree as a continuous range `0x0000...0000 -> 0xFFFF...FFFF` (the range wraps around at the upper end back to the lower end).   Nodes which are syncing the state use an out of protocol agreed upon “epoch” length.  For the purposes of this post we will use `EPOCH_LENGTH = 256`.  We define epoch boundaries to be `BLOCK_NUMBER % 256 == 0`.  At each epoch boundary, a node which is syncing the state will “pivot”.  A node that is just coming online will use the last epoch boundary as their starting point.

At each “pivot” a syncing node looks at the block hash for the boundary block.  Supposing the block hash was `0x00001...00000` the node would begin iterating through the state trie in both direction from that key, fetching missing values as they are encountered.

This approach results in uncordinated swarming behavior, allowing nodes which are only partially synced to more reliably serve the requests of other syncing nodes.

## Limiting the abuse of state sync protocols

This builds from the previous point which adds uncoordinated swarming behavior to nodes that are syncing the state.

A full node *may* decide to not serve requests for state that are far enough away from the current or most recent epoch boundaries.  Supposing the latest epoch boundary was `0x5555...5555`, a node may choose to refuse to serve a request for state under the key `0xaaaa...aaaa` since that key is very *far away* from the current place where it would expect nodes to be requesting the state.

A full node could choose to implement more advanced heuristics such as keeping track of the keys for which a node has recently requested and refusing to serve requests that hit widely disparate key locations.

The goal here is to provide full nodes with heuristics which are reliable enough to both allow them to reliably descriminate against nodes which are not following the swarming behavior as well as making it more difficult for nodes to abuse the state retrieval mechanisms to implement the types of stateless client functionality that the network is unable to broadly support.

More research is needed to more reliably determine whether this approach to discrimination would be effective or whether it would be easily circumvented.

# Summary

The proposal above hinges on retiring `GetNodeData` and replacing it with a primative which allows the serving node to know the key in the state trie that a given request falls under.  This is required for full nodes the properly discriminate against clients which are abusing the protocol.

This plan **does not** allow for stateless clients which expose full client functionality.  In order for the network to support stateless clients that can expose the full JSON-RPC API we will need to figure out a scalable approach for on demand retrieval of arbitrary state.

This plan also **does not** address the desire to allow nodes to forget ancient chain data.  The network will still be dependent on nodes with the full chain history to serve it to others who do not yet have it, **and** the network will still be subject to abuse by nodes which choose to forget ancient chain data and merely retrieve it on demand from the network.  Intuition suggest this is a less of a problem than on-demand retrieval of arbitrary state.

---

**carver** (2020-02-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Supposing the latest epoch boundary was 0x5555...5555 , a node may choose to refuse to serve a request for state under the key 0xaaaa...aaaa since that key is very far away from the current place where it would expect nodes to be requesting the state.

Cool, that’s pretty interesting as a resistance to state leechers. The refusal heuristics seem to place an upper bound on how quickly a node can sync the full state. It would be nice to consider that upper bound when choosing “refusal to serve” heuristics.

For example, if state must be within ~5% of the epoch key, then it would take at least 20 epochs (but probably more) to finish syncing. That’s about 21 hours at 15s block times and 256-block epochs. If you widen the allowable range to ~10% and cycle every 100 blocks, that drops to ~4 hours. (Obviously, this comes at the cost of more read I/O for serving peers).

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> At each epoch boundary, a node which is syncing the state will “pivot”. A node that is just coming online will use the last epoch boundary as their starting point.
>
>
> At each “pivot” a syncing node looks at the block hash for the boundary block.

Tiny nit: can we use a different name than “pivot” here? Cycle? Re-seed? It would be nice to avoid name collision with the other usage of pivot in Fast Sync and Beam Sync.

---

**pipermerriam** (2020-02-27):

I’m going to go with the term “state trie index” or just “index” to refer to the key path in the trie from which a state sync iterates from, and “re-index” as the term used when a client stops iterating the state trie from their previous index and chooses a new index from which to iterate the state trie.

This is aimed at removing the “pivot” name collision since the term pivot is used to describe when we change to iterating the state tree from a completely new state root in a completely new block.

---

**kladkogex** (2020-03-16):

Well, I do have a non-isomorphic proposal John! The simplest way is to publish a puzzle from time to time solving which requires computational intense operation on the entire state storage. The puzzle needs to be done in such a way, that each time a different set of nodes has a priority, these are details that can be figured out.

