---
source: ethresearch
topic_id: 23017
title: Gossipsub's Partial Messages Extension and Cell Level dissemination
author: MarcoPolo
date: "2025-09-03"
category: Networking
tags: [data-availability]
url: https://ethresear.ch/t/gossipsubs-partial-messages-extension-and-cell-level-dissemination/23017
views: 459
likes: 8
posts_count: 3
---

# Gossipsub's Partial Messages Extension and Cell Level dissemination

# Gossipsub’s Partial Messages Extension and Cell Level dissemination

*or how to make blob propagation faster and more efficient*

Thanks to Raúl Kripalani, Alex Stokes, and Csaba Kiraly for feedback on early drafts.

## Overview

Gossipsub’s new Partial Message Extension allows nodes to upgrade to cell level dissemination without a hard fork. Increasing the usefulness of data from the local mempool (getBlobs).

There is a draft PR that specifies how Consensus Clients make use of the Partial Message Extension here: https://github.com/ethereum/consensus-specs/pull/4558.

## Introduction

Fusaka introduces PeerDAS with [EIP-7594](https://eips.ethereum.org/EIPS/eip-7594). As explained in the EIP, erasure coded blobs are disseminated as columns of cells. The columns are typed as [DataColumnSidecar](https://github.com/ethereum/consensus-specs/blob/cd92a897acd4c9c4918cb0cda5744be62ad9e0c4/specs/fulu/das-core.md#datacolumnsidecar). These columns are propagated via gossipsub to the network. If a node already has all the referenced blobs in a column from its local mempool, it can derive the DataColumnSidecar itself without waiting for Gossipsub propagation. It then also propagates the column to help with rapid dissemination. The IDONTWANT message of Gossipsub serves to supress these pushes from a peer that already has the IDONTWANT message.

In the case that all referenced blobs of a block appear in the the majority of nodes’ mempool, then reaching the custody requirement is fast. The data is already local. However, if even a single blob is missing then nodes must wait for the full columns to be propagated through the network before reaching their custody requirement.

Ideally we would disseminate *just* the cells that are missing for a given row. Allowing a node to make use of data it already has locally. That’s what Gossipsub’s Partial Message Extension does.

The Partial Message Extension allows nodes to send, request, and advertise cells succinctly. It is a change in the networking layer that does not require consensus changes, can be deployed in a backwards compatible way, and does not require a hard fork.

## Partial Message extension, an overview

The full draft spec can be found at [libp2p/specs](https://github.com/libp2p/specs/pull/685).

Partial Messages behave similar to normal Gossipsub messages. The key difference is that instead of being referenced by a hash, they are referenced by a Group ID. The Group ID is application defined, and must be derivable without requiring the complete message. With a Group ID and a bitmap, a Node can efficiently specify what parts it is missing and what parts it can provide.

For PeerDAS, the Group ID is the block root. It is unique per topic. A full column is a complete message, and the cell is the smallest partial message. A cell is uniquely and succinctly identified by the subnet topic (the column index), Group ID (block root), and position in the bitmap. A node can start advertising and requesting cells as soon as it receives the block. Which is the soonest possible because the block declares the included blobs.

Cell-level dissemination with normal gossipsub messages is tricky at best. Each cell would have to be referenced by its full message ID (20 bytes), and nodes cannot request missing cells a priori; they must first know how a cell maps to its corresponding message ID. In contrast, with partial messages, nodes reference each cell with a bit in a bitmap, and can exchange information of what they can provide and what they need with partial `IHAVE`s and partial `IWANT`s.

Partial messages can be eagerly pushed to a peer without waiting for the peer to request parts, or they can be provided on request.

Gossipsub Partial Messages require application cooperation, as the application knows how messages compose and split. Applications are responsible for: - Encoding available and missing parts (e.g. a bitmap). - Decoding a request for parts, and responding with an encoded partial message. - Validating an encoded partial message. - Merging an encoded partial message.

## Hypothetical example flows

To help build an intuition for how partial messages will work in practice, consider these two examples. The first example uses eager pushing to reduce latency, the second example waits for a peer request which can reduce duplicates at the expense of latency (1/2 RTT in this example).

For both examples, assume:

- Peer P is the proposer of a block. It knows about all blobs in a block.
- Peer A and B are validators.
- The first blob in the block was not shared publicly to A and B before hand, so they are both missing this single blob from their local mempool.
- P is connected to A is connected to B. P  A  B

### Eager pushing

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│        P         │   │        A         │   │        B         │
└──────────────────┘   └──────────────────┘   └──────────────────┘
 ┌────────────────┐             │                      │
 │Proposes Block B│             │                      │
 └───────┬────────┘             │                      │
         │   ┌──────────────┐   │                      │
         ├───│Forwards block│──▶│   ┌──────────────┐   │
         │   └──────────────┘   ├───│Forwards block│──▶│
         │   ┌──────────────┐   │   └──────────────┘   │
         │   │  Eager push  │   │  ┌──────────────┐    │
         ├───│cell at idx=0 │──▶│  │  Eager push  │    │
         │   └──────────────┘   ├──│cell at idx=0 │──▶ │
         │                      │  └──────────────┘    │
         │                      │                      │
         │                      │                      │
         │                      │                      │
         ▼                      ▼                      ▼
```

### Request/Response

```
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│        P         │   │        A         │   │        B         │
└──────────────────┘   └──────────────────┘   └──────────────────┘
         │                      │                      │
 ┌───────┴────────┐             │                      │
 │Proposes Block B│             │                      │
 └───────┬────────┘             │                      │
         │   ┌──────────────┐   │                      │
         ├───│Forwards block│──▶│   ┌──────────────┐   │
         │   └──────────────┘   ├───│Forwards block│──▶│
         │   ┌──────────────┐   │   └──────────────┘   │
         │   │    IWANT     │   │   ┌──────────────┐   │
         │◀──│    idx=0     │───│   │    IWANT     │   │
         │   └──────────────┘   │◀──│    idx=0     │───│
         │   ┌──────────────┐   │   └──────────────┘   │
         │   │ Respond with │   │   ┌──────────────┐   │
         ├───│  cell@idx=0  │──▶│   │ Respond with │   │
         │   └──────────────┘   ├───│  cell@idx=0  │──▶│
         │                      │   └──────────────┘   │
         ▼                      ▼                      ▼
```

Note that peers request data before knowing what a peer has. The request is part of the peer’s IWANT bitmap, which is sent alongside its IHAVE bitmap. This means data can be received in a single RTT when the peer can provide the data. In contrast, an announce, request, respond flow requires 1.5 RTT.

## Publishing strategy

Eager pushing is faster than request/response, but risks sending duplicate information.

The publishing strategy should therefore be:

*Eager push when there is confidence that this will be the first delivery of this partial message.*

In a scenario with private blobs, it’s reasonable for a node to forward with an eager push when it receives a private blob.

In a scenario with sharded mempools, it’s reasonable for a node to eagerly push cells it knows a peer would not have due to its sharding strategy.

Some duplicate information is expected and required as a form of resiliency. The amount of duplicates can be tuned by adjusting the probability of eager pushing and the probability of requesting from a peer.

However, even a simple naive strategy should significantly outperform our current full-column approach by leveraging local data from the mempool. Duplicate partial messages would result in duplicate cells rather than duplicate full columns.

## Devnet Proof of Concept

There is a work-in-progress [Go implementation of the Partial Message Extension](https://github.com/libp2p/go-libp2p-pubsub/pull/631). There is also a [patch to Prysm](https://github.com/OffchainLabs/prysm/compare/fusaka-devnet-3...MarcoPolo:marco%2FpeerDAS-partial?body=&expand=1) that uses partial messages.

As a proof of concept, we created a Kurtosis devnet using the patched Prysm clients connected to patched geth clients (to return partial blobs in the getBlobs call). Some nodes would build blocks with “private” blobs. When this happened other nodes would request only the missing “private” cells, and fill in the rest of the column with blobs from their local mempool.

To get a rough sense of bandwidth savings we also created a smaller kurtosis network of just two “super” nodes, nodes that receive and send all columns. One of the nodes proposes private blobs. The means that getBlobs will fail to return a full column for the other node when the aforementioned node proposes.

We measured data sent for `DataColumnSidecar` messages without and with Partial Messages. The results show with Partial Messages, nodes send 10x less data. There are two reasons for this:

1. The current Prysm implementation of Partial Messages never eagerly pushes. Nodes wait to see a request before responding with data.
2. Only the requested parts are sent. If a column had a single private blob, we only send that one blob.

In this low latency environment (running locally with Kurtosis), IDONTWANTs are not effective. Hence we see a large benefit in simply not eagerly pushing data.

However, in the cases where there are private blobs, IDONTWANT would not be applicable, so the performance benefits here are still representative of higher latency more realistic environments.

Graphs:

[![Screenshot 2025-08-22 at 10.42.38 PM690x448](https://ethresear.ch/uploads/default/optimized/3X/e/7/e70cd3a8d9344fb694f1f0ceb05076a8a9f22764_2_690x448.jpeg)Screenshot 2025-08-22 at 10.42.38 PM690x4483248×2112 474 KB](https://ethresear.ch/uploads/default/e70cd3a8d9344fb694f1f0ceb05076a8a9f22764) [![Screenshot 2025-08-22 at 10.42.49 PM690x448](https://ethresear.ch/uploads/default/optimized/3X/3/0/302861fe80bf27922b8fdb3316748d3b7015b5e5_2_690x448.jpeg)Screenshot 2025-08-22 at 10.42.49 PM690x4483248×2112 471 KB](https://ethresear.ch/uploads/default/302861fe80bf27922b8fdb3316748d3b7015b5e5)

This is an experiment with just two peers, but each pairwise interaction in a mesh with more peers should behave the same. The is the bandwidth used for disseminating data columns.

## Mempool sharding

Future directions of mempool sharding will only make it more likely that nodes are missing some cells, and thus require some form of cell level dissemination.

## “Row” based dissemination

Note that if a node is missing a cell at some index in one column, it’s likely missing cells at the same position in all other columns. One future improvement could be to allow nodes to advertise full rows to its mesh peers. The benefit is that a node fills all its missing cells for a row at once. The downside is the risk of larger duplicate messages.

## Next steps

- Specify the getBlobs V3 api that supports returning partial blobs.
- Implement the Partial Message Extension in Rust libp2p. (in progress)
- Specify the partial message encoding of DataColumnSidecars. In Progress
- Integrate into CL clients.
- Deploy on testnets
- Deploy on mainnet
- scale blob count

## Replies

**MedardDuffy** (2025-09-05):

There are two aspects here:

a/ pull is more effective than push in gossip - in a pull case, one node does not request something that node does not want

b/ finer granularity is useful.

This is useful but does not achieve perfect pipelining. RLNC achieves perfect pipelining to actually optimize, see

Bernhard Haeupler. 2011. Analyzing network coding gossip made easy. In Proceedings of the forty-third annual ACM symposium on Theory of computing (STOC '11). Association for Computing Machinery, New York, NY, USA, 293–302.

The difference between the sharding and coding can best be understood as the difference between reducing the size (smaller granularity) and improving instead the throughput (coding). The latter is much more powerful than the first. Of course coding and finer granularity can be done together to get the combined benefit, but to compare them, let us do some simple networking math. Let us compare reducing the size of a shard by 2 versus actually speeding up by a factor of 2.

You can skip the math and just look at the example at the end.

To do our simple math model, let us use Pollaczek-Khinchin (let us abbreviate to PK) for M/G/1 queues (fairly general)

D = \frac{1}{2 (1 - \rho)} \lambda E [X^2]

where

D is mean delay, that includes the queueing until a shard is successfully delivered.

\lambda is the arrival rate of shards

X is the random variable that represents the service (completion) of delivery of a shard

\mu, the service rate, is defined to be the inverse of the expectation (E), so \mu = \frac{1}{  E [X] }

\rho is the load factor of the system, defined by \rho = \frac{\lambda}{\mu}, which can be interpreted as the ratio of how fast shards are coming into the system versus how fast they can be delivered. For the system to be stable, it is necessary to have \rho <1.

Note that in the denominator there is the E [X^2]  term. This is the variance of X plus \frac{1}{\mu}^2. The more variable the service time, for the same average service time, the longer the delay.

Let us consider the simple example where we halve a shard.

1/ Original shard, original speed

from PK

D_1 = \frac{1}{2 (1 - \rho_1)} \lambda_1 E [X_1^2]

\rho_1 = \frac{\lambda_1}{\mu_1}

2/ Shard by a half

\mu_2 = 2 \mu_1, twice as fast service

E [X_2^2] = E [X_1^2]/4 halving means the square is divided by 2

but for the same amount of traffic, if we halve the shard, we send half the amount of data, so to keep the total amount of data the same, it means that we double the arrival rate (twice as often we have an arrival, each or half as much)

\lambda_2 = 2 \lambda_1, hence

\rho_2 = \frac{\lambda_2}{\mu_2} = \rho_1 = \frac{\lambda_1}{\mu_1}

So

D_2 = \frac{1}{2 (1 - \rho_2)} \lambda_2 E [X_2^2] = \frac{1}{2 (1 - \rho_1)} \frac{2}{4} \lambda_1 E [X_1^2] = \frac{D_1}{2}

so that we have one half the delay - this is not magic, it is PK.

3/ Speed by a factor of 2

\mu_3 = 2 \mu_1, twice as fast

E [X_3^2] = E [X_1^2]/4 halving means the square is divided by 2

But

\lambda_3 = \lambda_1 as we are not changing the arrival rate so

\rho_3 = \frac{\lambda_3}{\mu_3} = \frac{\rho_1}{2} = \frac{\lambda_1}{2 \mu_1}.

---

Here comes the example.

Suppose that \rho_1 = 0.8, then \rho_3 = 0.4.

So

D_1 = \frac{5}{2} \lambda_3 E [X_1^2]

And

D_3 = \frac{5}{6} \lambda_3 E [X_3^2] = \frac{5}{6} \frac{1}{4} \lambda_1 E [X_1^2] = \frac{D_1}{12}

so the benefit is 12 X in delay in case 3 rather than 2 X in case 2. Speeding by a factor of 2 improves six-fold over just sharding by a factor of 2. Of course, both coding and sharding is the way to go.

---

**MarcoPolo** (2025-09-09):

Thank you for the comments Professor Médard, very happy to see queuing theory brought up!

> a/ pull is more effective than push in gossip - in a pull case, one node does not request something that node does not want

Agreed, but there’s the aspect of latency. The push case will save 1/2 RTT compared to the pull case. Of course, this is useless if a node receives data it doesn’t want which is why pushing is only recommended when there is confidence it is useful, as is the case with private blobs.

> but for the same amount of traffic, if we halve the shard, we send half the amount of data, so to keep the total amount of data the same, it means that we double the arrival rate (twice as often we have an arrival, each or half as much)

This isn’t exactly the correct way to think about this proposal, and I apologize for not being clearer in the introduction. We don’t need to send the same amount of data, we only need to send the parts that a node hasn’t received. Let me clarify.

Data availability checks happen against columns of cells from blobs included in a block. Each column contains a cell (a 2KiB part of data) from each of the blobs included in the block. For example, the first column contains the first 2KiB of every erasure encoded blob in the block.

Blobs may be propagated through the mempool *before* being included in a block. This is the most common path for blobs and they are often referred to as “public” blobs.

Consensus Clients can query the mempool to see if it already has the blobs necessary for its data availability check. If a block only includes blobs that are already in the local mempool, then the node does not need anything from the network before it can complete its data availability check. However, in the current design, if even a *single* blob is missing from its local mempool then the node needs the receive the *whole* column from the network. The utility of the local mempool in the current design is all or nothing.

This proposal is about enabling the exchange of *just* the missing cells. If a single blob is missing from our local mempool, with this proposal, only the cells pertaining to that blob are transmitted.

To extend your shard example, it would be as if we sharded the data *and* the other node already had all but one of the shards.

> Of course, both coding and sharding is the way to go.

Completely agree.

There is a lot more we can do with coding, even as a small extension to this proposal. One could imagine coding eager pushes in such a way to remove redundancy when receiving an eager push from multiple peers.

The underlying GossipSub extension itself is generic to the specific encoding of message parts. So the application has a lot of flexibility in how it encodes messages.

