---
source: ethresearch
topic_id: 7158
title: "\"Merry Go Round\" sync"
author: pipermerriam
date: "2020-03-20"
category: Execution Layer Research
tags: [chain-sync]
url: https://ethresear.ch/t/merry-go-round-sync/7158
views: 4121
likes: 3
posts_count: 4
---

# "Merry Go Round" sync

Here I propose a new approach to syncing the Ethereum state data that I’m tentatively naming: “Merry-Go-Round Sync”, or MGR sync.  MGR aims to provide a new mechanism for syncing the Ethereum state that exhibits bittorrent style swarming behavior, and mitigates against other uses of the state syncing network primatives.

At a high level, MGR operates by enumerating the full state in a predetermined order and gossiping this data among the clients which are actively syncing.  For a client to fully sync it needs to “ride” one full rotation of the merry-go-round.

This is aimed at just being a rough write-up.  It doesn’t get into specifics in many places, mainly because there are no firm specifics at this stage, only the high level concept and rough ideas of how it would work.

### State Enumeration

MGR requires a well defined way to enumerate the state data such that:

1. Minimize duplication:  During a single revolution of the MGR there should be very little or near zero duplication of data.
2. Zero coordination: There should be no coordination required for clients to know what part of the state is being distributed at any given time.
3. Flexible with-respect-to state size:  For a chain with a very small state, each revolution of the MGR should be very quick.  For a chain with very large state, each revolution of the MGR would be longer.

No obvious solution has been posed that fits both of these criteria well.  Here is my best idea thus far.

#### Use the block hash

In this model we would have some concept of a sync epoch.  At each epoch boundary, the block hash of the boundary block would determine what location in the trie enumeration should begin at.  The state data would be enumerated starting at that location in the trie and working outwards until the next epoch boundary.

Mitigating against re-sending duplicate data when there are two epochs with block hashes that are close together in the trie would require something like tracking and broadcasting what ranges of the trie each client has fully synced.

This approach does not require any coordination for determining where to enumerate the trie, but it does require some level of coordination for clients to keep track of which of their peers has which data.  This might be acceptable.

This approach seems to scale well with different state sizes.

> One point of note is that under this model there may not be a clear definition of “one revolution” because two clients may be able to ingest data at different rates, meaning that they would take different amounts of time to fully enumerate the trie since the slower client would make less progress during each epoch.  This might actually be a good thing.

### Networking

This likely belongs in a separate protocol than the existing DevP2P `ETH`.  For the sake of simplicity we’ll assume this is a new DevP2P protocol `MGR`.  Currently we would require the benevolent participation of fully synced nodes.

We would need something like the following commands.

#### Status

Allow clients to broadcast information to each other.  This should probably contain `forkid` as well as meta data about what parts of the state the client has already synced

#### StateData

A data packet that includes a provable chunk of the state.  Assuming we use the [witness spec](https://github.com/ethereum/stateless-ethereum-specs/pull/1), it may be that the “top” level of the tree is only sent around occasionally and that sub-trees are the primary unit of distribution in between re-broadcasting of the top levels of the tree

This message would be gossiped around the network…

### Getting a full picture of the state

One problem that arises with any state syncing approach is that the state is constantly changing which makes it difficult to get a full picture of the state within the garbage collection window that most clients use to discard old trie data.

Beam sync addresses this, however, for clients to rely on beam sync we will need witnesses propagating around the network.

## Replies

**pipermerriam** (2020-03-20):

I haven’t done a lot of thinking about how the state data is disseminated into the network.  To limit the scope of this a bit I’ll be operating under the assumption that we are using the block hash based approach to determining the current location in the tree that state data would be synced from.

In addition, I’ll be working under the assumption that the client is beam syncing so that they always the newest state data from the newest blocks.

### Synced Ranges

As part of the meta data that clients pass around, they would include a list of paths into the state tree for which they have fully synced the data.

- []: empty list signals that the client is not synced.
- [0x0000, 0x8888]: indicates the client has synced everything from the tree which has a path starting with either value.
- [0x]: indicates that you have all of the state.

As a client syncs data it would maintain this list of ranges and would update their connected peers on a regular interval (like maybe once each epoch?)

### Sync Epochs

Under the block hash model we would define a constant `N` for how many blocks are in an epoch.  At each block such that `Block.number % N == 0`, all nodes would transition into a new sync epoch.  We’ll call this an epoch boundary and respectively, a boundary block.

### Client behavior

Using the block hash from the boundary block, a client would inspect their state database at that location and begin enumerating the state outwards from that location, putting together a set of proofs for that state.  The client would check the latest status messages for each of it’s connected peers and broadcast proofs for the state data that the client is missing based on the client’s last broadcasted sync ranges.

Upon receiving a proof for a section of the state, a client should also relay that information to any of their connected peers who also need that data.

I believe this simple approach would efficiently disseminate the state data to the peers in the network that need it, even in the case where there are only a few nodes that have all of the state data.

---

**AlexeyAkhunov** (2020-03-20):

Thank you so much for this write up, and for giving this a good name. I will try to describe my (currently **FLAWED**) idea on how the state can be enumerated and split up into parts to satisfy the three requirements you listed above. I will repeat them for easier reading, and will refine the second, “zero coordination” requirement:

1. Minimize duplication: During a single revolution of the MGR there should be very little or near zero duplication of data.
2. Zero coordination: There should be no coordination required for clients to know what part of the state is being distributed at any given time. Refinement: Only seeders (node that already have the entire state) will have zero-coordination requirement. The knowledge of the state will be used as a substitution for the ability to coordinate.
3. Flexible with-respect-to state size: For a chain with a very small state, each revolution of the MGR should be very quick. For a chain with very large state, each revolution of the MGR would be longer. Refinement I have not figured out how to make this happen yet, but it should be possible to specify too.

Each seeder will maintain (in their database) two instances of the data structure, which I will call “tree enumeration”. The specific items stored in this structure are implementation dependent. They have a form “key prefix => number of leaves with such prefix”. Implementations do not need to have an item for each possible prefix, but, for example only consider prefixes with even number of nibbles, or similar approaches (needs to be tested). Such data structure should be easy to maintain as the state data get modified. Each insertion or deletion of state key-value pair will result in the update of logarithmic number of prefixes (most of which would be cached in memory).

One of the instances of such tree enumeration structure always tracks the current state, as the chain progresses. Another instance of tree enumeration is “frozen” at the beginning of each Merry-Go-Round cycle. For example, if the chosen cycle length is chosen to be 4000, then the second instance of the tree enumeration will be frozen as of every block number which is multiple of 4000.

The “frozen” tree enumeration is used by seeders to calculate which part of the state needs to be synced at which block interval. Since it will be “frozen” for the entire duration of the cycle, the seeders can calculate (and arrive at the same result without extra coordination) how many state leaves need to be synced at each block interval. Once the cycle is over, the first, “current” enumeration is copied (**THIS THE FLAW** - I do not know how to copy enumeration efficiently) into the second, “frozen” enumeration, and the cycle starts over.

In order to prevent the state data from getting stale during the Merry-Go-Round cycle, we always combine state piece for the current block interval with the block witness for the corresponding block. That way, all the state data gets automatically “patched” at the leechers persist the packets they receive.

Some rough thoughts on possible issues:

1. What if block intervals are too short for the state piece? The simplest solution is for the seeders to start sending the new piece once the previous piece has been sent.
2. How to adjust the algorithm to the increasing state size? Currently I am thinking of not making the cycle duration (in number of blocks) the algorithm’s parameter, but instead the number of state leaves that are supposed to be synced during one block interval, and calculate the duration from it. This however, has an “arithmetic” problem of overlapping sync cycles. For example, when we transition from cycle duration 4000 to 4001, for example, the number which is 0 (mod 4000) and which is 0 (mod 4001) could be quite far apart. Do we need to make the state un-syncable while we get to the block 0 (mod 4001)?

---

**pipermerriam** (2020-03-20):

One concept that I think will probably apply well across any number of different methods for enumerating the state is how to package up and transmit the data for that state.

This approach depends on the [witness spec](https://github.com/ethereum/stateless-ethereum-specs/pull/1#).

For a given key prefix, we need a standard way to package up the data under that prefix.  We assume that we know nothing about how much data is under the prefix meaning that this mechanism needs to allow for chunking of the data.  We also need to be sure that each *chunk* of the data is individually provable.

My current thinking is that it would be done roughly like this:  For any tree of data that a client wishes to transmit to a peer, we define a rough maximum number of trie nodes that the witness can contain.  This is similar to the `GetNodeData` cap of 384 trie nodes.  This provides an out-of-protocol way to ensure that the packets don’t get too large to transmit.  So for a given witness we would have the following values:

- state_root: the state root under which this data  is associated
- prefix: the path into the tree that the witness is for
- proof: the actual witness

> I’m currently not sure that the prefix/state_root differentiation is necessary but it doesn’t really matter that much at this point.  We do however need to ensure we have a way to anchor the data that is being transmitted to a state root.

So a *“seeder”* who is transmitting data to a peer would build the witness and then chunk it into some set of pieces.  These pieces would then be transmitted in order to peers.  It also seems that we’d want some way of linking all of the chunks for a witness into the same bucket so that a peer can know how many total chunks there are so they can gauge their progress and definitively know they are done syncing a given section of the trie.

Another thing to think about under this model is whether we can define an algorithm for chunking such that two seeders transmitting data about the same `prefix` under the same `state_root` always produce the same chunk packets.

