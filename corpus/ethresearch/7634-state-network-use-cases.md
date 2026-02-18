---
source: ethresearch
topic_id: 7634
title: State Network use cases
author: pipermerriam
date: "2020-07-03"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/state-network-use-cases/7634
views: 1860
likes: 2
posts_count: 9
---

# State Network use cases

I’d like to spend a minute to explore the use cases for the “State Network”.  I’ll start with a short description of what I mean by “State Network” and then will do my best to enumerate the various use cases, providing basic context for each of them.

The purpose is to establish a common ground from which we can determine the specifics of the network architecture and actually start building something.

# What is the “State Network”

A special purpose decentralized storage network that is capable of serving the Ethereum chain history *and* state.  At this stage we are agnostic about whether this is a DHT, LibP2P, DevP2P, whatever…

## Network Participants

The network design should assume a wide range of network participants, likely with the following rough shape.

- Leechers

nodes that jump on and offline quickly (a few minutes or less), leeching a small amount of data from the network.
- such nodes might be part of a CLI that reads data on demand but doesn’t operate as a long lived process.

Ephemeral

- nodes that stay on the network for short periods of time (a few minutes up to maybe a few hours) and who may primarily leech but which are capable of also serving data and will do so if it is easy.
- such a node might be integrated into something like MyCrypto or other wallets and only active while the app is open.

Long Lived, Low Resource

- nodes that stay on the network reliably for many hours or days which act as data providers but have low resources (1 CPU, storage measured in the 100’s of MB)
- such a node might be integrated into an ethereum client.

Long Lived, High Resource

- same as the “low resource” counterpart, but these nodes have more CPU and storage, maybe serving the entire state or entire history.
- there would likely be very few of these
- such a node would likely be run by a benevolent enthusiast

This lets us define some minimal resource targets since we want nodes with minimal CPU and storage to be able to operate on this network as first class citizens.

## Use Cases: High Level

At a high level we want to support the following use cases.  These are the core of of what the network needs to do.

- Syncing the full chain history (not the state)
- Facilitating on-demand retrieval of chain history to allow clients to forget about some of the history.
- Facilitating on-demand reads of the state to allow clients without access to the state to do things like sending transactions (and the implicit gas estimation that goes with them).
- Serve the JSON-RPC API with a few exceptions without need of a full client.

Another requirement is that all retrieved data be provable.  I won’t get into details on this because the method for proving each piece of data is likely different, though they all likely link back to the header chain.

What follows is a more granular breakdown of exact capabilities necessary to fulfill these use cases.

## Use Cases: Chain History

All of this data is easy to manage.  Historical data doesn’t change so it is a simple dataset that simply grows over time with a mostly constant rate that new data is added.

### Header Chain

- Retrieve block headers by hash

This can be used for:

- A client syncing the header chain
- Serving JSON-RPC endpoints like eth_getBlockByHash

### Block Bodies

- Retrieve the ordered set of transactions and uncles by block hash

This can be used for:

- A client syncing the block chain
- Serving JSON-RPC endpoints like eth_getBlockByHash

### Receipts

- Retrieve the ordered set of receipts for a block by block hash

This can be used for:

- A client syncing the block chain
- Serving JSON-RPC endpoints like eth_getTransactionReceipt

also requires the chain index for txn_hash -> block_hash lookups.

### Canonical Chain Index

- Given a block number lookup the canonical block hash

This use case likely requires adding a header accumulator to the Eth1 protocol which would allow for inclusion proofs.  Without this, verification of this data would require a local copy of the header chain which is multiple GB in size which violates the minimum resource requirements.

Given a transaction hash, lookup the canonical block hash in which it was included.

This can be used for:

- Serving JSON-RPC endpoints like eth_getBlockByNumber, eth_getTransactionByHash, eth_getTransactionReceipt

## Use Case: State

The state data is divided up into millions of small pieces.  Some pieces change often.  Some pieces rarely or maybe never change.  The data is all anchored to a state root.  Most data should be accompanied by an inclusion proof against a state root.

### Account State

This data is evenly distributed across a trie that is somewhat straight forward to shard and distribute evenly without coordination.

- Ability to do on-demand lookups of individual accounts from the state trie and an accompanying proof for a recent state root

unclear whether this can be a little flexible on the proof state root, or whether this needs to be anchored to a specific state root.

Ability to retrieve the account bytecode associated with the account code hash.

This can be used for:

- Patching up a local state database.
- Serving JSON-RPC endpoints like eth_getBalance, eth_getTransactionCount, eth_getCode, etc.

This *is not* intended to be used for syncing the full state.  We would rely on SNAP or MGR for such things.  This **could** be use to augment or assist in syncing the full state.

### Contract State

This data is unevenly distributed and varies widely in shape and size depending on the account.

- Ability to do on-demand reads of arbitrary contract state with an accompanying proof for a recent state root.

unclear whether this can be a little flexible on the proof state root, or whether this needs to be anchored to a specific state root.

This can be use for:

- Patching up local state database
- Serving JSON-RPC endpoints like eth_call, eth_estimateGas
- Stateless block execution without a witness (beam sync)

## Use Case: Eth2

I need help filling this section in as I know this type of network is desired for Eth2 but I’m unclear on exactly what needs Eth2 has.

## Replies

**pipermerriam** (2020-07-03):

I realize I forgot to include witnesses.

A witness would need to be

- Retrievable by block hash

Likely not feasible without also having a reference to the witness hash in the header.  Without this the retrieved data would not be provable.

---

**vbuterin** (2020-07-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> ### Receipts
>
>
>
> Retrieve the ordered set of receipts for a block by block hash

There’s another really important use case, which is receive a set of receipts that match a particular topic. For that we have my cryptoeconomic ideas from [Special-purpose light clients for old receipts and transactions - Ethereum 1.x Ring - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/special-purpose-light-clients-for-old-receipts-and-transactions/3711) though we could also try other approaches…

> A witness would need to be … Retrievable by block hash

I’ll add that technically having a list of accessed accounts and storage keys be hashed into a block would also suffice, as if you know that then you know what accounts the witness is representing and you can reconstruct the subtree and verify it against the state root. This approach may be better as it allows us to avoid having the witness serialization format be in-consensus (which makes upgrading the format and potentially even replacing it with a SNARK easier over time).

---

**pipermerriam** (2020-07-09):

I’m inclined to keep logs out of this for now.  Assuming we can reliably make all of the historical block data (including receipts) reliably available, it is relatively trivial to write stand-alone ETL applications which handle exposing log filtering APIs.

I wrote [this application](https://github.com/ethereum/cthaeh) in just a little under 2 weeks.  It uses the JSON-RPC API to load historical chain data into an ORM and exposes the JSON-RPC APIs for log filtering.  It is incredibly simple.  One thing I like about this pattern is that it removes this functionality from being the responsibility of the ethereum client into a specialized tool focused more on dapp use cases.

---

**vbuterin** (2020-07-12):

I definitely think that logs are higher priority than state though. The reason is basically that (i) logs are easier to deal with as they’re an append-only list and so you don’t have to design around trees that keep changing, and (ii) the total data size of logs is larger than the total size of state. So it seems like higher gain for lower effort to handle those first.

---

**pipermerriam** (2020-07-13):

[@vbuterin](/u/vbuterin) I think we’re talking about two things.  I’m already proposing we support historical receipts, which means that we are supporting logs in the sense that they are append only and all of the log data would be available through the network.

What I’m hesitant to support is the logging API which requires maintaining an “database index” for fast queries to find logs matching certain criteria.  I’m certainly not opposed to supporting this if there is a reasonable scheme to do so but I’m very hesitant to go in the direction you suggest in the linked magicians post that involves incentives…

---

**vbuterin** (2020-07-13):

The challenge is that many dapps do search for historical logs by topic, and this is an important functionality for them. And if we want to make it possible for nodes to exist without storing history, relying on this network instead to fetch it on-demand, which means that we need the by-topic kind of on-demand search as well…

---

**pipermerriam** (2020-07-13):

I think we’re in agreement then.  I’m ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=14) on any system that facilitates serving the functionality that is exposed by the JSON-RPC logging APIs, but right now I’m not sure how to do that at the networking level.  Consider it an open topic of research.

---

**vbuterin** (2020-07-13):

I do think that we will need to take the leap into incentivized network protocols at *some* point, and receipts-by-topic are a good well-compartmentalized place to start.

