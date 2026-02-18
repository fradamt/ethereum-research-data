---
source: ethresearch
topic_id: 17417
title: Network Shards (concept idea)
author: Nashatyrev
date: "2023-11-14"
category: Sharding
tags: []
url: https://ethresear.ch/t/network-shards-concept-idea/17417
views: 1658
likes: 4
posts_count: 3
---

# Network Shards (concept idea)

# Network Shards

> Note: this is the high level idea on how the networking might potentially be organized to meet the future data sharding needs. This idea is kind of follow up to PeerDAS and SubnetDAS proposals. In some aspects it complements and in other aspects it serves as an alternative to these proposals.

The very basic idea is to split the network onto `N` (let’s assume `N = 32` as initial approach) *Network Shards* and let every shard take care of

- disseminating (Push) of 1/N of the whole Gossip network traffic by serving as a  backbone for various subnets (e.g. attestation, sync committee and future DA sampling subnets)
- custodying and serving (Pull) of 1/N of the network data (DA samples, blob slices, blocks potentially)

## Data dissemination (Gossip subnet backbones)

This idea might be thought of as a generalized [Attnet Revamp spec PR](https://github.com/ethereum/consensus-specs/pull/3312)

Similar to [Attnet Revamp](https://github.com/ethereum/consensus-specs/pull/3312) every node in the network at any moment is assigned to a single Network Shard. A node serves as a Gossip backbone for a set of Gossip subnets statically assigned to this shard. Also similar to Attnet Revamp nodes are circulating across Network Shards in a deterministic manner.

The major advantage of this concept is the ability to uniformly and securely support Gossip subnets of a smaller sizes (even the corner case with a single publisher and a single subscriber). The concept of Network Shards also settles up another abstraction layer for push/pull data dissemination

> Note: A single Gossip subnet (topic) may potentially span several shards (the obvious example case is the beacon_block topic which spans all shards)

## Data custody

Together with serving Gossip backbones assigned to a shard the node also commits to custody and serve the data published on the shard topics. The data retention policy should be topic specific.

When a peer joins or reconnects to the network it should fill the custody gaps of missing past data to honestly fulfill its duties.

> Note: as the nodes are circulating across shards over time it’s not that straightforward to retrieve historical data as a client. Different implementation strategies could be utilized to optimize this process.

## Voluntary Shard participation

A node with high bandwidth and storage capabilities may voluntary want to join to more than one Network Shard. That could potentially be implemented by the method proposed in the [PeerDAS write up](https://ethresear.ch/t/peerdas-a-simpler-das-approach-using-battle-tested-p2p-components/16541#custody-6)

## Danksharding application

### Issues of existing approaches

- Finding and connecting to an abstract subnet is basically slow and takes unpredictable amount of time
- Small subnets are vulnerable to sybil attacks
- Pulling random samples (while catching up head) is also slow and unpredictable

### Push sampling

Let’s consider the original Danksharding DAS (Data Availability Sampling). Every slot `256K` (`512 * 512`) of data samples need to be published. Every node needs to receive just 75 of them (selected randomly by the node). Ideally a node should verify a different random subset of samples at every slot (or at least every few slots).

It is possible to have `256K` sample subnets split across all shards (e.g. `8K` subnets per shard).

A sampling node (from a ‘client’ perspective) should just maintain stable and balanced connections to nodes from all shards.

> Note: the above requirement to be connected to all shards could be relaxed for a regular node if the sampling algorithm could be relaxed: for example a node may randomly choose and slowly rotate the subset of shards, and randomly choose a sample subset from those sample subnets assigned to the chosen shards. However security properties need to be revisited for any relaxed approach.

A node would be able to *Subscribe/Unsubscribe* corresponding sample subnets almost *immediately* since there is no need to search and connect to subnet nodes

This concept meets the needs of various sampling approaches including original Danksharding, [SubnetDAS](https://ethresear.ch/t/subnetdas-an-intermediate-das-approach/17169) approach

### Pull sampling

Pulling recent samples is pretty straightforward: using a specific RPC method samples are requested from the nodes assigned to the corresponding shards.

Pulling historical samples is a bit more tricky due to shard nodes rotation. However various strategies may be used to optimize the process:

- Retrieve the samples which are available with the current connected peers while searching and connecting to the peers for missing samples
- Probably employ a more lenient sampling strategy with slightly relaxed security properties

## Open questions

- (technical) Are Gossip implementations able to handle that number (order of 10K) of topic subscriptions?

(Gossip protocol change) topic wildcards? Aka das_shard_N_sample_*
- (Gossip protocol change) topic hierarchy? Aka das/shard_N -> das/shard_N/sample_M
- (Gossip implementation change) on demand subscription? Shard nodes subscribed to a single subnet das_shard_N but if a client initiates a subscribe das_shard_N_sample_M message then the node responds back the same subscribe message

(technical) When a node (as a client) subscribes to a topic what is the probability to be included to the mesh promptly? Else a client would get message via gossip only (around 500ms of extra delay)
Add staggering to nodes rotation across shards (has being discussed while coming up with [Attnet Revamp](https://github.com/ethereum/consensus-specs/pull/3312))
Add randomness to nodes rotation across shards such that it is only possible to predict shard assignments for the next `M` epochs. This would help to mitigate sybil attacks on a single shard (a node which is live in discovery for more than `M` epochs is guaranteed to be not specially crafted for a sybil attack) (has being discussed while coming up with [Attnet Revamp](https://github.com/ethereum/consensus-specs/pull/3312))
Number of shards:

- Cons of a smaller number of shards (more nodes per shard)

Higher throughput and CPU load per node
- Larger custody storage per node

Cons of a greater number of shards (less nodes per shard)

- Less reliable
- More vulnerable to attacks (sybil/eclipse)
- Higher number of peer connections for a client node which needs to be connected to all shards (e.g. for full sampling)

## Replies

**pop** (2023-11-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/nashatyrev/48/6487_2.png) Nashatyrev:

> The major advantage of this concept is the ability to uniformly and securely support Gossip subnets of a smaller sizes (even the corner case with a single publisher and a single subscriber). The concept of Network Shards also settles up another abstraction layer for push/pull data dissemination

I have a concern on the bandwidth consumption on small subnets. Since each node is required to join some shard and there will be probably many subnets assigned to that shard, it means that the node has to consume much more bandwidth than before.

Careful analysis has to be done if we want to incorporate this into DAS, since the whole point of doing DAS is to reduce bandwidth consumption to scale L2. If we end up consuming a lot of bandwidth, it will contradict to the original goal of DAS.

For example, let’s do the analysis of full Danksharding in PeerDAS with the number of rows/columns of 512. The number of subnets is 1024 (512 rows + 512 columns). If the number of shards is 32, the number of subnets per shard is 32 (1024/32). The throughput of each subnet is 256MB/slot, so the bandwidth required for each node is 8MB/slot (32*256MB/slot). This number is far from the ideal Danksharding where each node has to download only 2 rows and 2 columns in each slot (1MB/slot = 4*256MB/slot).

---

**mkalinin** (2023-11-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> Careful analysis has to be done if we want to incorporate this into DAS, since the whole point of doing DAS is to reduce bandwidth consumption to scale L2. If we end up consuming a lot of bandwidth, it will contradict to the original goal of DAS.

The idea behind this proposal is not tight to the DAS only. It is about organising a network layer into `N (=32)` data serving primitives (shards), where each of them is responsible for serving (via gossip and upon request) `1/N` of all protocol data.

The value of `N` plays important role in sybil resistance, `32` is a number of subnets which a network relies upon in disseminating attestations today, using it as a number of network shards would not change sybil resistance properties that the network already has.

Another important property given by this solution is quick lookups and connections to the sources of required data. This is relevant for DAS where a node is required to frequently jump between DAS subnets. It is certainly a trade off between low throughput and sybil resistance with fast data lookups capability.

I see the following ways to increase throughput in a network organized in the proposed way:

- start publishing more data without changing N, requires bandwidth of an average node to be increased,
- increase N, requires bigger network to preserve the same sybil resistance level and likely network interfaces to support more connections (if we assume every node is connected to 2-4 nodes from each shard).

![](https://ethresear.ch/user_avatar/ethresear.ch/pop/48/9805_2.png) pop:

> so the bandwidth required for each node is 8MB/slot (32*256MB/slot)

The required bandwidth would be bigger as we should factor in `D(=8)` (the gossipsub mesh parameter), so it will be 64MB/slot (D*8MB/slot).

