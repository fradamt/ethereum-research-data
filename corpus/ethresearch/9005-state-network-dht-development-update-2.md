---
source: ethresearch
topic_id: 9005
title: State Network DHT - Development Update #2
author: pipermerriam
date: "2021-03-24"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/state-network-dht-development-update-2/9005
views: 4303
likes: 5
posts_count: 13
---

# State Network DHT - Development Update #2

> previous development update here: State Availability - GetNodeData DHT Approach (dev update) - #5 by pipermerriam

Another development update for the ongoing work to build out the State Network DHT for on-demand retrieval of the Ethereum State.  We have a very early draft of a specification for this network available here: [[WIP] Add first draft of state network spec by pipermerriam · Pull Request #54 · ethereum/portal-network-specs · GitHub](https://github.com/ethereum/stateless-ethereum-specs/pull/54)

## Design Goals

Our design goals are facilitating on-demand retrieval of the Ethereum “State”, meaning accounts, contract storage, and contract bytecode.  The term “on-demand” in this context means that nodes are able to retrieve any arbitrary piece of data from the recent active state in a manner that allows it to be proven against a known recent state root.

We aim to support the “wallet” use case which is loosely defined as being able to read data from the network via `eth_call` and build transactions through a combination of `eth_estimateGas` and `eth_getTransactionCount` (for nonce retrieval).

Performance requirements are that the majority of “normal” wallet operations can be performed in under the block time.

We are also aiming for resource constrained devices, meaning that clients from this network must be able to run the client on a single CPU, with <1GB of ram, <1GB of slow HDD.  Bandwidth usage must be suitable for a residential internet connection.

## High Level Network Design

The network is an overlay Kademlia DHT built on the Discovery V5 protocol that is already part of the beacon chain infrastructure and is supported by some of the core Ethereum mainnet clients as well.

Each node in the network has a `node_id` as defined in the ENR specification which dictates their *location* in the network.  The network implements its own versions of PING/PONG/FINDNODES/FOUNDNODES messages for nodes to maintain their kademlia routing tables.

## uTP for streaming data that exceeds the UDP packet size

We will be using a version of the uTP protocol.

https://www.bittorrent.org/beps/bep_0029.html

This protocol allows any two nodes in the network to establish a stream over the same UDP socket used for other DHT communication, allowing for reliable transmission of payloads that exceed the UPD paccket size.

## Provability

All nodes in the network are assumed to have access to the header chain.  The set of recent `Header.state_root` values is used by nodes to validate proofs.

## Data Storage

All data in the network has a `key` and and `id`.  We refer to these as `content_key` and `content_id`.

The `content_key` has semantic information and is the *identifier* that nodes use to request data.

The `content_id` is derived from the `content_key` and dictates where in the network the content can be found.  We use the same xor based distance function to determine the distance between a `node_id` and a `content_id`

Each node in the network has a `radius` which is a uint256 derived from the content they are storing.  Each node in the network allocates some amount of storage.  When this storage is not full, a node is considered to have a `radius` value of 2**256-1 (MAX_RADIUS).  When the nodes storage is full, the nodes `radius` value is the distance between the `node_id` and the `content_id` that is furthest from the `node_id`.  Nodes are *interested* in content that is within their radius (`distance(node_id, content_id) <= radius`) and that is not already known/stored by the node.  The Ping and Pong messages are used to communicate radius to other nodes.  We refer to the area of the network that contains mostly *interested* nodes for a given `content_id` as the “region of interest”.

Nodes in the network store content that falls within their radius.

The network stores all of the intermediate trie data for both the main account trie and the contract storage tries, as well as all of the contract bytecode.

The network explicitly **does not** deduplicate trie nodes and bytecode, storing multiple copies of any duplicated values to facilitate easy garbage collection.

## Data Retrieval

Retrieval of content is roughly equivalent to the recursive lookup that nodes use to find a specific node or the node closest to a specific node_id.  A specialized message FINDCONTENT is used to make this process slighly more efficient.  To find a piece of content, a node will first start with data from their routing table, querying the node which is closest to the `content_id` that is being retrieved, sending a FINDCONTENT message to that node.  The response to this message will be one of:

- The raw bytes of the content itself
- The uTP ConnectionID for receipt of content that exceeds the UDP packet size
- A list of ENR records that are closer to the content than node serving the response.
- An empty response indicating that the node does not have the content and does not know about any closer nodes.

Retrieval happens one trie node at a time.  This inneficiency is part of a broad set of trade-offs between total storage size, individual node responsibility, and efficiency of data retrieval.  The data being retrieved from the network is incrementally proven at each stage, initially, fetching the root node for the trie, and then walking down the trie.

## Data Ingress

As the chain progresses and new blocks are added, the network needs to learn about any new state data.  This new state data will be provided by a small set of benevolent “data providers” who have the full state, and generate the proofs for new state data from each new block.  These proofs will be against the post state root, and will only contain data that was modified or added during execution.

In almost all cases, proofs are expected to exceed the UDP packet size, and thus, will be transmitted using the uTP subprotocol.

Proofs are disceminated through two distinct mechanisms that both use the same set of base messages for communication.

1. Pushing proofs into the “region of interest” (typically originating from outside of the region)
2. Gossiping proofs within the “region of interest” (typically originating from inside the region)

Since the network stores both the leaves and the intermediate nodes of the trie, all of the nodes in these proofs will each need to be pushed to the part of the network that the `content_id` for that node maps to.  Thus, a proof for a single leaf, will also contain the full proof for all of the intermediate nodes needed to get to that leaf.  We take advantage of this property to both reduce the amount of duplicate proof data that must be sent over the wire, as well as spreading the workload for pushing new proof data into the network across a larger number of nodes.

To push data into the network, a data provider will generate the full proof.  They will then decompose that proof into a set of proofs, one for each leaf node.  They will then sort these proofs by proximity to the `content_id` of the leaf node.  Starting with the leaf proofs that are *closest*, they will perform a recursive network lookup to find nodes for whom the corresponding `content_id` falls within their advertised radius, and use the Advertise message to let that node know that the proofs are available.  If the node is interested in the advertised proof they will respond with a request for the proof, containing a `connection_id` that the sending node should use to initiate a uTP stream for transmission of the proof.  The data providers are **only** responsible for disceminating proofs for the leaves.

The responsibility for pushing the proofs for the intermediate nodes, falls to the the recipient of the leaf proofs (and subsequently to the recipients of the intermediate proofs).  Upon receiving a valid proof that the node is “interested” in, it will do two things.  First, the node will gossip the proof to other nodes sourced from its routing table for which the `content_id` falls within the node’s radius.  Second, it will extract sub-proofs for the parent trie nodes, and push those to their region of interest (the same way that data providers did for the leaf proofs).  This operation repeats recursively until it terminates at the state root.

## Garbage Collection

> This part of the network functionality is still under active research

The design of the network is currently well suited for being an “archive” node, however, the total network size necessary to store a full archive copy of the state would take widespread adoption, something that we don’t expect to achieve right away.  For this reason, we need a mechanism that allows for garbage collection of trie data that is no longer part of the *recent* state.

The scheme used for the `content_key` is designed to ensure that content that is duplicated in multiple spots in the trie is also stored in multiple spots in the network.  For example, two accounts with identical `balance/nonce/code_hash/state_root` would be identical, however, we store them at distinct locations in the network by including the trie path in the `content_key`.  This allows us to generate exclusion proofs that show the node is not present in a recent state root, allowing nodes to discard old trie data.

## Rollout and Development Plan

We are currently working on launching a very minimal prototype test network.  This network will be focused on the data retrieval portion of the protocol.  The goal of this experiment is to validate our assumptions about retrieval latency, which is a key performance number needed to validate the usability of the network for the indended use cases.

The uTP subprotocol is likely to be prioritized early, so that we can establish an independent spec for how uTP streams can be established between nodes in the discovery v5 network.

Work is underway to extend the Turbo-Geth API to support generation of the proofs that “data providers” will need to push data into the network.

After the test network experiment has been done, assuming we are indeed able to validate our projected latency numbers, we will move onto focusing on actual client development for the full protocol.  Rough projections of the work that needs to be done suggest that once development is fully underway, we should be able to have roughly full proof of concepts available in a 6-month timeline, and production clients within a 12-month timeline.

## Replies

**mkalinin** (2021-03-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Retrieval happens one trie node at a time. This inneficiency is part of a broad set of trade-offs between total storage size, individual node responsibility, and efficiency of data retrieval.

Does it mean that [state snapshots](https://github.com/ethereum/devp2p/blob/6eddaf50298d551a83bcc242e7ce7024c6cc8590/caps/snap.md) are already under your consideration?

---

**pipermerriam** (2021-03-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkalinin/48/4799_2.png) mkalinin:

> Does it mean that state snapshots are already under your consideration?

We currently are not considering syncing (or acquiring a full snapshot) of the state as a supported use case.

But maybe I’m not fully understanding your question…  If the question is whether we plan to host snapshots on the network… no we do not.

---

**mkalinin** (2021-03-25):

I am sorry, I haven’t found a description of state snapshot (as a data structure) quickly. I am asking because it seems like state snapshot is efficient in terms of data retrieval and updates but inefficient in terms of total size of the state.

IIUC, snapshot allows for accessing state slots and accounts in `O(1)` which solves the problem of increasing the cost of state access throughout a time and should decrease a number of queries in a sate network from `O(logN)` to `O(1)`. Though, this structure consumes more size than regular state database (~30% size increase).

---

**pipermerriam** (2021-03-25):

The thing standing in the way of a scheme that allows for O(1) access is the imbalanced nature of the trie.  The contract storage being separate from the main account trie makes it impossible to evenly distribute the trie data across the network without some unknown amount of complexity/coordination cost.  Myself and others have spent a decent amount of time trying to figure out a scheme that works and everything I looked into was a dead end.

When the Verkle trie work lands and we have a unified and balanced trie we, we can then relatively easy map contiguous chunks of the state to the DHT keyspace, which then allows for key/value style lookups (aka O(1) access).

The concept of snapshots however doesn’t really apply directly to the state network design since it’s a distributed environment and we don’t expect nodes to house more than maybe a few 100MB of state data

---

**wuzhengy** (2021-04-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> The uTP ConnectionID for receipt of content that exceeds the UDP packet size

I am afraid that uTP connection is not firewall/NAT friendly for nodes with 192.168 type of IP addresses. On the other side, Kademlia UDP relay based swarm network are robust overlay on various network restrictions.

Assume in stateless network, many more nodes will randomly join the state provider network, it is quite hard to ask all of them have public IP address or natpmp ability.

---

**levicook** (2021-04-03):

This is a fair concern, thanks for raising it.

From an implementation perspective, it looks like libtorrent solves for this using UDP hole punching. I can’t attest to the efficacy of this, but on first pass, it seems reasonable.

libtorrent


      [github.com](https://github.com/arvidn/libtorrent/blob/c1ade2b75f8f7771509a19d427954c8c851c4931/src/bt_peer_connection.cpp#L1421)




####

```cpp

1. int index = detail::read_int32(ptr);
2. incoming_allowed_fast(index);
3. }
4. // -----------------------------
5. // -------- RENDEZVOUS ---------
6. // -----------------------------
7. #ifndef TORRENT_DISABLE_EXTENSIONS
8. void bt_peer_connection::on_holepunch()
9. {
10. INVARIANT_CHECK;
11. if (!m_recv_buffer.packet_finished()) return;
12. // we can't accept holepunch messages from peers
13. // that don't support the holepunch extension
14. // because we wouldn't be able to respond
15. if (m_holepunch_id == 0) return;

```








I also found a Rust crate that implements NAT traversal: [GitHub - ustulation/p2p: NAT Traversal techniques for p2p communication](https://github.com/ustulation/p2p/)

I don’t know this library well, but the API/usage leads me to believe this can be implemented as an overlay that would be invisible to uTP. Sounds ideal, but needs to be confirmed/tested.

---

**wuzhengy** (2021-04-03):

The hole punching idea works smoothly from full cone to full cone NAT, and it also require STUN servers (just like bootstrap server, another centralized point), many modern ISP wants to regulate one direction on those ports, which refresh itself every couple minutes. We do not really see much success on hole punching in our network most in developing region. I think this is why IPFS adopted relay nodes than hole punching.

One hope is the stateless nodes are behind upnp/natpmp enabled nat/firewall. The initiator-free data exchange between two stateless nodes requires both nodes equipped with real ip or under upnp/natpmp.

The brilliant idea of Kademlia DHT is in fact entirely skipping uTP or TCP connection based communication. BEP005 clarifies the difference between nodes(connection-less) and peers(connection based), I personally think it makes so much sense to avoid server connections which will be target for censor. BEP44, connection-less arbitrary data protocol, basically bets on good will of relay nodes, but the unsolving issue is that “why stateless nodes are encouraged to provide data storage” and face potential UDP spam put/get requests.

I just feel if we add connectionID based idea into DHT for finding global states, grass roots stateless nodes data exchange will suffer from nat blocking in big time, in which libtorrent UDP-connection-less-DHT does not affected by NAT restriction at all. I just guess that the design goal of Kademlia 20 years ago is to be connection-free(no stun server needed) so to resist control.

I am still thinking and prototyping some solution to address pure UDP DHT data exchange with some level of incentive design, but not yet mature at this moment…

---

**pipermerriam** (2021-04-05):

[@wuzhengy](/u/wuzhengy) I want to be sure you are operating under the correct assumptions about how we plan to use uTP.

We **do not** intend to directly use the uTP protocol as it is written, aka, uTP → UDP (meaning that it’s just uTP packets sent via UDP packets).

We intend to wrap uTP in the DiscoveryV5 protocol, meaning uTP → DiscV5 → UDP.  Basically, at the networking level, a uTP packet will be indistinguishable from a normal DiscoveryV5 packet doing a PING/PONG/FINDNODES/FOUNDNODES.

So any problems that we would have with uTP we would also have with the base Kademlia protocol.

---

**wuzhengy** (2021-04-05):

I like the idea “uTP” over DiscV5, which is robust and make fast convergence of routing buckets, and it does not have NAT restriction issue. Let me call it “eth_uTP”.

So the sequence field of “eth_uTP” is the logical data series something like state item time-stamp than IP packets transmission parameter, right? In such case,  the getData responses from Kademlia DHT space will come from XOR distance closer nodes(say: set CLOSER) rather than ownership targeted nodes, which could be offline in stateless DHT system. Since, libTorrent has never solved incentive issue for nodes to serve data. How to create incentive for CLOSER(assume all DHT nodes are stateless) collectively to provide response? The CLOSER could be spammed by attacker renting a massive IPv6 pool. If CLOSER is a group of stateless nodes, being aware of such spam,  they will logically provide witness data ONLY relating to own blocks and tx, then the requestor routing table will likely mark “fail” to those XOR closer nodes, since unwillingness to serve data and the friendly-targeted nodes are XOR far away than set CLOSER. The recursive lookup effort for “serve-all” nodes will become O(N) than O(logN). Basically it becomes a full traverse in the DHT space of nodes ID, while nodes ID changes when every session restarts.

This case will be even worse for immutable data item, in case of that new protocol wants to use it. Hosting immutable data item is a bandwidth leaking item, nodes will find too expensive to serve immutable hash-value pair.

So I guess an incentive design needed for long term to complete the plan for both eco-system survive and query efficiency in stateless environment where massive number of nodes engage in random way. For short term, it is probably ok to operate without incentive.

---

**wuzhengy** (2021-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> meaning uTP → DiscV5 → UDP
> [/quote] [quote=“pipermerriam, post:9, topic:9005”]
> just uTP packets sent via UDP packets

We spent some time research how to maintain data sequence on DHT/UDP. I am still not clear how uTP can build “TCP type of sequence” on DHT, since “reply” could come from a undetermined set of nodes. A concept called [Levenshtein Distance](https://en.wikipedia.org/wiki/Levenshtein_distance) seems to be able to solve the problem.

Sender will hash each messages to 1 byte and form up a string with these bytes. E.g, if you have 3 messages: “hello”, “a beautiful”, “world”, the first byte of hash assume to be: v,w,t; then the string “vwt” is built, for Sender and receiver exchange this string and use LD to determine which messages not yet confirmed transmission by the other peer. LD turns out to have almost 0 false positive than bloom filter, because the sequence information is embedded. Therefore, exchanging LD between peer to peer, the data completeness can be established without form up connection with embedded sequence number.

Still in nutshell, hope this makes some sense.

---

**pipermerriam** (2021-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/wuzhengy/48/5741_2.png) wuzhengy:

> I am still not clear how uTP can build “TCP type of sequence” on DHT

So we have a couple of things that I think need to be unpacked to explain this.

First, we’re specifically talking about the [Discovery v5 Protocol](https://github.com/ethereum/devp2p/blob/5a53d69ac1d9780b6dcca194888f790e0dd91a2a/discv5/discv5.md).  The base protocol provides a mechanism for establishing an encrypted session between two nodes, and builds a Kademlia DHT network.  The protocol establishes a base set of messages that all nodes on the network understand:

- PING/PONG
- FINDNODES/NODES
- TALKREQ/TALKRESP

For building the uTP protocol over the DiscoveryV5 protocol we are specifically looking at TALKREQ (we ignore TALKRESP because we don’t end up needing the request/response paradigm for uTP).

The TALKREQ message is a simple 2-tuple of `(protocol_id: bytes, payload: bytes)`.

So, when I say “uTP over DiscoverV5”, I mean the same packet format as specified in [BEP29](https://www.bittorrent.org/beps/bep_0029.html), but instead of sending it in a raw UDP packet, we instead send it as the `payload` for a TALKREQ packet using the DiscoveryV5 protocol.  Each  uTP stream is only comprised of message passing between two nodes on the network.  We completely ignore the Kademlia/DHT part of the network.  We only use the session encryption and the TALKREQ message primative.

You can see a really ugly incomplete proof-of-concept here: [POC: Implement uTP protocol by pipermerriam · Pull Request #341 · ethereum/ddht · GitHub](https://github.com/ethereum/ddht/pull/341)

---

**wuzhengy** (2021-04-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> The base protocol provides a mechanism for establishing an encrypted session between two nodes, and builds a Kademlia DHT network

The risk of Sybil and Eclipse attack in DHT is still valid, although libtorrent implement IP address format and call restrictions in admitting to the routing table. The attacker vector is able to find lots of closer nodes ID than natural Nodes ID generated from normal usres private keys.

I think there is a solution in “payload” to resist routing table pollution. **Assuming that senders public key are derivable from the state trie**, the payload has to be decrypt-able by using senders public key and within certain time frame. The attacker can have closer nodes id to send you data, but not be able to relay the attacking data with right payload, since the attacker pubic key is impossible to match payload data signer. Receiver can simply reject such mismatch request to keep routing table clean.

Hope this makes sense.

Another comment is:

The current design requires stateless nodes to have public IP address or NAT-pmp ready, so that handshake process can be done. What’s the plan for nodes not having these abilities.  One vision of stateless impresses me is that state and ledger size can be reduced to flat hundreds Mbytes and POS does not burn electricity, so a smart phone or a pc can easily be a legit full miner. Most of such units falls into restricted network. Does the plan support theses user base?

