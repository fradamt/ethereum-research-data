---
source: ethresearch
topic_id: 22477
title: Accelerating blob scaling with FullDASv2 (with getBlobs, mempool encoding, and possibly RLC)
author: cskiraly
date: "2025-05-27"
category: Networking
tags: [data-availability, p2p, layer-2, scaling]
url: https://ethresear.ch/t/accelerating-blob-scaling-with-fulldasv2-with-getblobs-mempool-encoding-and-possibly-rlc/22477
views: 497
likes: 6
posts_count: 1
---

# Accelerating blob scaling with FullDASv2 (with getBlobs, mempool encoding, and possibly RLC)

# TL;DR

- FullDAS is a 2D erasure code based DAS construct with cell-level messaging, aiming to scale blob count to the 200+ range. It is based on two pipelined phases: dispersal to custody, and sampling from custody, minimising diffusion delay in both components.
- FullDASv2 is showing how to combine FullDAS with EL blob diffusion (getBlobs), EL blob encoding, and RLNC coding.
- FullDASv2 with getBlobs improves local building and bandwidth efficiency further, allowing reconstruction even in case of a sharded or segmented mempool. The combination also allows blocks mixing both private and public blobs to benefit from getBlobs.
- We propose a new version of getBlobs (v3) with a streaming interface to make the synergies even better.
- EL blob encoding has the same effect as in PeerDAS, removing some of the computational burden from the block builder and from nodes using getBlobs.
- The use of RLNC (Random Linear Network Coding), instead of the 2D RS code is an option, but it comes with compromises, as we could loose the benefits of row/column repair, the latency benefits of cell-level pipelining from custody to sampling, or even that possibility of using p2p redistribution efficiently. We discuss several design alternatives, with their respective pros and cons.
- Finally, we analyse potential networking bottlenecks in scaling DAS blob count to the 200+ range, arriving to the conclusion that raw bandwidth is not the main concern. Rather, it is per-message processing and signalling overhead that we should be concerned about.

# Introduction

About a year ago we published our [FullDAS design](https://ethresear.ch/t/fulldas-towards-massive-scalability-with-32mb-blocks-and-beyond/19529), based on 2D erasure codes, targeting 32MB data (256 blobs) per slot, with the following ingredients:

1. An efficient protocol for dispersal to custody, using

cell-level messaging
2. bitmap-based row/column/cell ID gossip
3. In-network on-the-fly erasure code based recovery
4. cross-forwarding between rows and columns to achieve availability amplification
5. batch publishing to reduce or eliminate bandwidth overhead at the publisher
6. Push-pull phase transition to reduce or eliminate the bandwidth overhead in the p2p network, while still keeping delay low and still distributing the load
7. A fast and lightweight protocol for sampling from custody, using

cell-level messaging
8. local randomness for improved sampling security
9. fast sample delivery from custody
10. improved and adaptive sampling with LossyDAS
11. A new peer discovery structure based on row and column IDs to eliminate connection delays

In fact, several parts of the design were in the making since 2022, first [presented at EthereumZurich’2023](https://www.youtube.com/results?search_query=csaba+kiraly+data+availability).

Since our post, a few of the techniques have been implemented (in-network repair, batch publishing), some are gaining popularity (push-pull in GossipSub, cell-level messaging), while others still need to be debated, and prove themselves useful, or be replaced with something else. The goal of this post is to provide an update, hopefully contributing to **accelerating the blob-scaling timeline**.

We focus on four key aspects:

1. connecting blob diffusion paths in the EL and CL through getBlobs (also proposing changes for getBlobs v3)
2. the utility of cell-level messaging, also in light of getBlobs
3. blob encoding, right in the mempool
4. the 2D encoding itself, the advantages of using Reed Solomon (RS) codes, and possible alternatives such as RL(N)C

Finally, we close this writeup by considerations on networking related **bottlenecks to scaling** in the EL and in the CL.

# GetBlobs, and even better GetBlobs (v3?)

Since our original post on FullDAS, the `getBlobs` engine API call was introduced to connect the diffusion paths of blobs in the EL (mempool gossip) and in the CL (DAS diffusion). This improves our FullDAS scheme as well, as we discuss below.

In the DAS encoding scheme, blobs become rows, while columns are “cross-cutting” all blobs included in a block. The current version of PeerDAS (which is essentially a SubnetDAS) is based on **column-level messages**, meaning the unit seen by the networking layer is an entire column. GetBlobs is instead row oriented. This **mismatch** creates two inefficiencies in the system:

- No column reconstruction: While a node implementing PeerDAS can get rows from the EL using getBlobs, it can only create an entire column if the corresponding EL node has all the blobs in its mempool. While in the current mempool this is almost always the case for blocks with public blobs, as we show in our mempool analysis, this will most probably not be the case as blob count increases. If the EL misses just one blob, the column can’t be created, and getBlobs is rendered useless.
- No reconstruction of individual rows: a node can only reconstruct row-wise if it has K cells of the row. But since it can only get cells as part of entire columns, it can only reconstruct if it has K columns, which is the whole data. In other words, only “supernodes” can participate in the reconstruction.

## Introducing getBlobs based column reconstruction

In our FullDAS design, instead, nodes can pull blobs from the EL, even a single one, and start gossiping cells of it on column topics (also on row topics, but that’s less important now). Depending on a node’s custody columns, this might take two forms (but this is just a further optimization):

- If the node is subscribed to a column topic, it can push the cell to its neighbours directly. Contrary to popular belief, this will not create extra overhead in the system compared to the baseline case of receiving the cell over GossipSub and forwarding it.
- If the node is not subscribed to a column topic, it can still push the cell, or at least gossip the availability of the cell. We think this latter is a better choice, enabling extra network recovery paths at a low cost.

As a results, **columns can be reconstructed even if there are no nodes that have all the blobs**.

## getBlobs and private blobs

Some might say, yeah, but there are **private blobs** (blobs that never hit the mempool, since their blob carrying transaction was coming from a private transaction feed of the builder). In this case, column reconstruction would not be possible without the 2nd dimension of the erasure coding. If, however, the block builder starts publishing cells from the erasure coded rows (lower half), **getBlobs becomes useful even with some private blobs in the block**.

## No need for “supernodes”

In the current PeerDAS design, erasure code-based recovery is only possible if a node has half of all the columns. While such nodes are available in testnets and on the current mainnet, the protocol would be much more robust without the need for such nodes. Our design with cell-level messages **supports recovery without “supernodes”**. In fact, any node that custodies a single row or column actively does erasure code-based recovery as part of its normal activity.

## A better getBlobs (v3?)

While the current getBlobs design seems sufficient to supply these use cases, we can make it even better. The information that a particular blob is needed becomes available to the CL when the block arrives (there are also proposals to move this information to the block header). At the same time, the state of the EL node’s mempool regarding that specific blob might be several:

- Maybe it already arrived
- Maybe the EL already knows about it, requested it (note that blob-carrying transactions are not pushed, but announced requested in mempool), but it didn’t arrive
- Maybe the EL already knows about it, but didn’t yet request it
- Maybe the EL never heard about it.

Since the CL does not know anything about these details, it has the problem of deciding when to call getBlobs. Here we enter into the semantics of the getBlobs API call. Ideally, the EL would take note of the CL’s request, and satisfy it in “streaming”, sending the blobs as soon as they arrive (or as an alternative, notifying the CL about the arrival). We tentatively call such a streaming interface **getBlobs v3**.

The EL can do even more, handling the requested blobs with higher priority, and fetching them from its peers.

# Blob encoding, right in the mempool

Another important change that happened is that blobs are now directly encoded in the mempool, more precisely when they are submitted to the mempool. This has several positive implication:

- First, the load on the builder is reduced. Compared to the 1D case of PeerDAS, we should still do the second dimension of the extension, but it is now less computation to prepare the DAS data structure.
- Second, when nodes get rows from the EL using getBlobs, most of the computation can be avoided.

Besides these immediate advantages, a deeper structural change might also be possible. By moving the erasure code to the mempool, the mempool itself might also become erasure code aware, and we can start thinking of vertical sharding and EC-based sampling right in the mempool.

# Why (not) use RL(N)C or some other code instead of RS?

Our 2D RS-based erasure coding uses a bivariate polynomial to encode the data, with each cell derived as a function of its row and column coordinates. This is just to say in a complicated way that we erasure code twice. Once, when submitting a blob-carrying transaction to the mempool, and once again, when composing the block and its blob matrix.

This structure, with the 2D RS code, allows us to repair a **single column**, a **single row**, and to **cross-forward** between rows and columns even before repair was taking place, **achieving fast availability amplification**.

A year ago, in our writeup, we also alluded to using other codes, highlighting some of the properties of 2D RS we use, but without going into much detail on alternatives. Since [other codes, especially RLC are gaining in popularity recently (for large message diffusion, not yet for DAS)](https://ethresear.ch/t/faster-block-blob-propagation-in-ethereum/21370/37), it is time to explore this aspect.

The key difference between broadcasting large-messages to many nodes (what we need with blocks), and dispersal to custody (what we do in FullDAS), is that in the former, every node needs all the data, while in the latter, each node has its own interest, the subset of the data it wants to get.

RLC, as used for large messages, is focusing on a broadcast service. It does not have the aforementioned properties of local repair and cross-forwarding. In baseline RLC the random coefficients are determined by the sender. This is what allows RLNC, where a sender can randomly combine previous combinations, as part of multi-hop multi-path forwarding. Leaving the randomness to the sender, however, could easily be tricked at the sender side by generating linearly dependent combinations, which would then hinder or even make impossible decoding. If the goal is to decode, nodes notice such problem. But if the goal is just to collect pieces like in the case of DAS, this might remain unnoticed.

A simple remedy to overcome this linear dependency problem is to **make the receiver select the random coefficients**. Either interactively, in a query (let’s call this **I-RLC**), or in its non-interactive version by deriving the random coefficients from the receiver’s ID (**NI-RLC**). Such a setup, however, makes on-the-fly recombination (the N in RLNC) impossible. Nodes can only generate new combinations once they received enough pieces to decode, decoded the data, and then recombined as needed.

Another problem is that with random coefficients spread over the whole cell ID space, there is no partial repair. A node would need to collect (at least) as many linear combinations of the original cells as there are cells in the structure. This is why many codes based on linear combinations (or even simple XORs) restrict the number and scope of original elements (cells) from which combinations are built. One can imagine this as most coefficients being forced to 0, and only a few allowed to be randomly selected. This enables partial repair at the cost of a slight efficiency decrease of coding efficiency. As an example, LT codes use this trick to enable efficient decoding. We call this concept **Resticted RLC (R-RLC)**.

Similarly, **we could restrict RLC to the column** (or to the row), using linear combinations only from cells of the given column, and send such combinations to nodes having that column in custody. That would allow nodes to do recovery as soon as they have enough cells from the column, a kind-of partial recovery. However, we would still **not be able to cross-forward** between rows and columns, because a linear combination of column cells does not help the row distribution. Even after decoding the column, cross-forwarding would be limited: nodes that decode the same colum would all have the same element of a row, and not different linear combinations.

Another option that could come to mind is to use linear combinations similar to a 2D RS code, having a pre-defined expansion factor and making the coefficients depend on a row and column IDs … however with this we would basically replicate what our Reed-Solomon code does.

So what can we do with RLC? Here we list a few options from the design space, with their pros and cons. Note that this is **still work in progress**, so don’t expect a clear solution better than our baseline, the 2D RS coding.

## RLC-based design no.1

We keep row and column distribution as is, using the 2D RS code, but we change sampling to get linear combinations. The idea here is to **empower sampling nodes to do more in case of recovery**.

**Pros:**

The individual sample is now more useful in case of an eventual reconstruction. It is not just a cell, but a random linear combination of all the cells of a given column (or row). This means we need less samples to recover a column, or the whole block, because no two samples are the same. It is easy to build the probabilistic model for this (we leave this for later), but even more importantly, it is harder to fool the nodes. In the RS case we can select 255 (or N-K-1) cells, and distribute as many copies of these as we want, still, reconstruction is not possible. In RLC case, Once 256 NI-RLC copies are distributed, the deconding is guaranteed.

**Cons:**

One of the reasons sampling was fast in our v1 FulDAS design is that custody nodes could forward cells as soon as they receive it. This made sampling “lag” just a 1-hop latency behind dispersion to custody, at the cell level. With the new design, samples could only be sent once the a node has the whole column (or row) in custody. This is slower.

## RLC-based design no.2

We keep the row and column-based distribution, but we use RLC to do it. The block builder sends restricted and verifiable NI-RLCs to nodes interested in the custody of a column (or row), and these get forwarded in a p2p fashion, e.g. using GossipSub.

Then we do RLC-based sampling as in design no.1.

**Pros:**

- We are not mixing RS and RLC.

**Cons:**

- As in design no.1, we slow down sampling.
- RLC-based row/column distribution means we cannot cross-forward between rows and coluns, which leads to slower diffusion and less availability amplification.

## RLC-based design no.3

In this design we change the notion of custody and sampling for everyone, including validator and full nodes.

In our original design, nodes **custody** entire rows and columns of the blob data. However, to have the probabilistic guarantees, it doesn’t have to be like this. **Linear combinations with verifiable destination-dependent randomness can fulfill the same role**.

The problem with this design is that someone should create these combinations, and only the block builder, or a node having all the blobs, has the data to do this. So we would **loose p2p redistribution**, and have a client server model. Clearly not what we want.

**Pros:**

- we have stronger individualized samples, without overlap. This is stronger than what a 2D-RS gives us, meaning we need to collect less pieces from the network to recombine the original data.

**Cons:**

- We loose the p2p network effect, the block builder is basically serving the whole network as a server.
- Nodes only have linear combination, but no one has actual pieces of the original data. While this in theory is enough, in practice having the data itself (as in systematic codes such as RS) has its advantages.

Since there is no p2p redistribution, this is not really a viable option, just a prelude to option no.4

## RLC-based design no.4

Can we combine RLC-based probabilistic guarantees, destination-enforced linear combinations, and p2p redistribution better?

We think we can, by constructing a hierarchical structure of restricted linear combinations (R-RLC), but for this we plan to have a a dedicated writeup.

# Scaling blob count to 256, gradually

So how could we get from 6 to 256?

By **identifying bottlenecks** and **introducing techniques** that overcome them, **gradually**. A possible path was already outlined in [this post](https://ethresear.ch/t/from-4844-to-danksharding-a-path-to-scaling-ethereum-da/18046), but now we can maybe add more detail.

## Is the bottleneck in EL mempool?

It is often assumed that the public mempool is a bottleneck to scaling. In the public mempool we use pure gossip (not to be confused with GossipSub) based distribution for blob-carrying transactions. A Node having a blob carrying transaction advertises the transaction ID to its peers, and then transactions are pulled by peers that still need them. There is no push, like in GossipSub, and thus there are no duplicates. While this is slower than push-based techniques, we can afford this because the **diffusion in the mempool is less time-critical**. Still, diffusion is **very fast**, as we’ve shown in [our mempool analysis](https://ethresear.ch/t/is-data-available-in-the-el-mempool/22329#p-54281-blob-transactions-spreading-in-the-mempool-16).

If we now take a blob, which is 128 KB, and a slot, which is 12 seconds, it is easy to see that **a blob costs approximately 11 KB/sec** (plus some overhead) to each node receiving it, both in ingress, and **on average**, also **in egress**. It is easy to see that there is **ample space in the mempool to scale blob count**.

Even if some nodes can’t afford such egress, the **mempool gossip system is adaptive**, shifting egress traffic to nodes that have the uplink capacity, leading to a better **utilization of the aggregate uplink capacity in the system even in case of node heterogeneity**.

But even if nodes can’t afford such egress traffic, what would happen is that blobs would not be 100% diffused in the mempool, which is not a problem, just a reduction of the efficiency of getBlobs. What is important to see here is that **with getBlobs, we only need a few nodes** that can help start the CL diffusion. We don’t need 90% of the nodes, not even 10% or 1%, just a handful of nodes.

Without cell-level messaging in the CL, we would still have a possible issue, as the number of nodes having all blobs of a block could become very low as we scale blob count. But with **cell-level messaging**, we overcome this issue as well.

## How we overcome bottlenecks in the CL, where latency is critical?

The key point to highlight here is the difference between a bandwidth bottleneck at the source, and a general bandwidth scarcity during the p2p diffusion.

### The block builder’s uplink bottleneck

If we take the naive solution, where the block builder has to send out multiple copies of every cell of every blob, bandwidth requirements quickly escalate.

Fortunately, we have a few tools at our disposal to solve this:

- For blobs hitting the public mempool, the EL gossip acts as a pre-seeding, and this comes free, not even consuming the block builder’s bandwidth, since it is not the original source of the blob, which most probably entered the mempool at another node.
- The block builder should also not send out multiple copies, or at least it should not start with that. The combination of batch publishing and erasure coding is solving this issue as well.
- With RLC, or fountain codes, one could try to optimize this even further. But the difference compared to the 2D RS based design might be small at the end, also because to reach the optimal performance with these codes, one also needs a feedback loop stopping the generation of new pieces, and we don’t (yet) have such feedback to the builder.

The block builder uplink can be a bottleneck, but if a block builder **relies on the public mempool**, and we use the previously discussed techniques, we can make **even low-bandwidth nodes create blocks with many blobs**. If instead someone uses private transaction feeds, the burden becomes bigger.

### The p2p bottleneck

Here by p2p we mean the **actual p2p forwarding** part, where the uplink bandwidth of nodes other than the source is being utilized.

The most important thing to clarify in this context is that the **aggregate uplink bandwidth** requirements of DAS dispersal are well below that of a p2p message broadcast (such as block diffusion). While we send out a 32 MB block, and with erasure coding we make it even bigger, a full node  with base custody requirements only downloads ~512 KB of it as row/column sampling, and another ~50 KB as cell sampling. And these numbers are per slot, so we are speaking of ~50 KB/sec overall.

To put it simple, bandwidth is not the main issue in the DAS p2p redistribution, except maybe if we have to deal with lots of duplicates.

Of course, there is the GossipSub overhead, but push-pull techniques, as discussed [here](https://ethresear.ch/t/pppt-fighting-the-gossipsub-overhead-with-push-pull-phase-transition/22118) and [here](https://ethresear.ch/t/doubling-the-blob-count-with-gossipsub-v2-0/21893), can reduce this overhead by a factor of 2 or even more, without significantly increasing delay.

### So where is the bottleneck?

The most likely bottleneck with the cell-based model is to be found in per-message overhead. This includes processing overhead, such as message validation and erasure coding, as well as network overhead, such as headers and message ID gossip.

For the latter, we proposed the **use of structured message IDs** and IHAVE/IWANT **bitmaps**. This is yet to be specified and implemented.

For the processing overhead, instead, we should review our networking stacks and improve things like **batch verification**. We might also end up having to use multiple-cell messages instead of single-cells as a compromise. **Mixed models, where both column-level and cell-level messages are used** are also being discussed.

# Conclusions

FullDAS is still in evolution, and the design will most probably change, but we already have a series of techniques we can introduce gradually to incrementally scale the blob count. Many of these are orthogonal changes, allowing multiplicative gains in the numbers of blobs we can support, allowing us to quickly scale Ethereum blob count.
