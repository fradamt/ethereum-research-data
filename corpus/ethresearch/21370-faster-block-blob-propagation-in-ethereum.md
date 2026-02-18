---
source: ethresearch
topic_id: 21370
title: Faster block/blob propagation in Ethereum
author: potuz
date: "2025-01-03"
category: Networking
tags: []
url: https://ethresear.ch/t/faster-block-blob-propagation-in-ethereum/21370
views: 5592
likes: 103
posts_count: 54
---

# Faster block/blob propagation in Ethereum

# Faster block/blob propagation in Ethereum

Acknowledgements to @n1shantd, @ppopth and Ben Berger for discussions and feedback on this writeup and [@dankrad](/u/dankrad) for many useful discussions.

## Abstract

We propose a change on the way we broadcast and transfer blocks and blobs in the P2P network, by using random linear network coding. We show that we can theoretically distribute the block consuming 5% of the bandwidth and with 57% of the number of network hops (thus half the latency per message) of the time it takes on the current gossipsub implementation. We provide specific benchmarks to the computational overhead.

## Introduction

The current [gossipsub](https://github.com/libp2p/specs) mechanism for distribution of blocks roughly works as follows. The proposer picks a random subset (called its *Mesh*) of `D=8` peers among all of its peers and broadcasts its block to them. Each peer receiving a block performs some very fast preliminary validation: mostly signature verification, but most importantly not including state transition nor execution of transactions. After this fast validation, the peer rebroadcasts its block to another `D` peers. There are two immediate consequences from such a design:

- Each hop adds at least the following delay: one full block transfer from one peer to the next one (including both network ping latency, essentially bandwidth independent, plus transfer of the full block, bound by bandwidth).
- Peers broadcast unnecessarily a full block to other peers that have already received the full block.

We propose to use [random linear network coding](https://ieeexplore.ieee.org/document/1228459) (RLNC) at the broadcast level. With this coding, the proposer would split the block in `N` chunks (eg. `N=10` for all simulations below) and instead of sending a full block to ~8 peers, it will send a single chunk to ~40 peers (not one of the original chunks, but rather a random linear combination of them, see below for privacy considerations). Peers still need to download a full block, or rather `N` chunks, but they can get them in parallel from different peers. After they have received these `N` chunks that each is a random linear combination of the original chunks composing the original block, peers need to solve a linear system of equations to recover the full block.

A proof of concept [implementation](https://github.com/potuz/rlnc_poc) highlights the following numbers

- Proposing a block takes extra 26ms that are CPU bound and can be fully parallelized to less than 2ms on a modern laptop (Apple M4 Pro)
- Verifying each chunk takes 2.6ms.
- Decoding the full block takes 1.4ms.
- With 10 chunks and D=40, each node sends half the data than with current gossipsub and the network broadcasts a 100KB block in half the time with benefits increasing with block size.

## The protocol

For an in-depth introduction to network coding we refer the reader [op. cit.](https://ieeexplore.ieee.org/document/1228459) and [this textbook](https://www.amazon.com/Network-Coding-Introduction-Tracey-Ho/dp/052187310X). We here mention minimal implementation details for the proof of concepts benchmarks cited above. In the case of block propagation (~110KB), latency or number of network hops dominate the propagation time, while in the case of large messages like blobs in full DAS, bandwidth dominates the propagation time.

We consider a finite field \mathbb{F}_p of prime characteristic. In the example above we choose the Ristretto scalar base field as implemented by [the curve25519-dalek](https://doc.dalek.rs/curve25519_dalek/) rust crate. The proposer takes a block, which is an opaque byte slice, and interprets it as a vector of elements in \mathbb{F}_p. A typical ethereum block is about B = 110KB at the time of writing, given that each Ristretto scalar takes a little less than 32 bytes to encode, a block takes about B/32 = 3520 elements of \mathbb{F}_p. Dividing into `N=10` chunks, each chunk can be viewed as a vector in \mathbb{F}_p^{M}, where M \sim 352. The block is thus viewed as N vectors v_i \in \mathbb{F}^M_p, i=1,...,N. The proposer chooses a subset of D\sim 40 peers at random. To each such peer it will send one vector of \mathbb{F}_p^M together with some extra information to validate the messages and prevent DOS on the network. We explain the proposer

### The Proposer

We will use Pedersen commitments to the Ristretto elliptic curve E as implemented by the above mentioned rust crate. We assume that we have already chosen at random a trusted setup of enough elements G_j \in E, j = 1, ..., K with K \gg M. We choose a standard basis \{e_j\}_{j=1}^M for \mathbb{F}_p^M. So each vector v_i can be written uniquely as

v_i = \sum_{j=1}^M a_{ij} e_j,

for some scalars a_{ij} \in \mathbb{F}_p. To each vector v_i we have a Pedersen commitment

 C_i = \sum_{j=1}^M a_{ij}G_j \in E.

Finally for each peer in the subset of size D \sim 40 the proposer chooses uniformly random a collection of scalars b_i, i=1, ...,N and sends the following information to the peer

1. The vector v = \sum_{i=1}^N b_i v_i \in \mathbb{F}_p^M. This is of size 32M bytes and it’s the content of the message.
2. The N commitments C_i, i=1,...,N. This is 32N bytes.
3. The N coefficients b_i, i=1, ...,N. This is 32N bytes.
4. A BLS signature to the hash of the N commitments C_1 || C_2 || ... || C_N, this is 96 bytes.

A *signed message* is the collection of elements 1–4 above. We see that there are 64N \sim 640 extra bytes sent on each message as a sidecar.

### Receiving Peers

When a peer receives a message as in the previous section, the verification goes as follows

- It verifies that the signature is valid for the proposer and the hash of the receiving commitments.
- It writes the receiving vector v = \sum_{j=1}^M a_j e_j and then computes the Pedersen commitment C = \sum_{j=1}^M a_j G_j.
- The received coefficients b_i are a claim that v = \sum_{i=1}^N b_i v_i. The peer computes C'= \sum_{i=1}^N b_i C_i, and then verifies that C = C'.

Peers keep track of the messages that they have received, say they are the vectors w_i, i = 1,...,L for L < N. They generate a subspace W \subset \mathbb{F}_p^M. When they receive v, they first check that if this vector is in W. If it is, then they discard it as this vector is already a linear combination of the previous ones. The key of the protocol is that this is very unlikely to happen (for the numbers above the probability of this happening is much less than 2^{-256}). As a corollary of this, when the node has received N messages, then it knows that it can recover the original v_i, and thus the block, from the messages w_i, i=1,...,N.

Notice also that there is only one signature verification that is needed, all incoming messages have the same commitments C_i and the same signature over the same set of commitments, thus the peer may cache the result of the first valid verification.

### Sending Peers

Peers can send chunks to other peers as soon as they receive one chunk. Suppose a node holds w_i, i=1,...,L with L \leq N as in the previous section. A node also keeps track of the scalar coefficients they received, thus they know the chunks they hold satisfy

 w_i = \sum_{j=1}^N b_{ij} v_j \quad \forall i,

for some scalars b_{ij} \in \mathbb{F}_p they save in their internal state. Finally, nodes also keep the full commitments C_i and the signature from the proposer that they have validated when they validated the first chunk they received.

The procedure by which a node sends a message is as follows.

- They choose randomly L scalars \alpha_i \in \mathbb{F}_p, i=1,...,L.
- They form the chunk w = \sum_{i=1}^L \alpha_i w_i.
- They form the N scalars a_j, i=1,...,N by
 a_j = \sum_{i=1}^L \alpha_i b_{ij}, \quad \forall j=1,...,N.

The message they send consists of the chunk w, the coefficients a_j and the commitments C_i with the signature from the proposer.

## Benchmarks

The protocol has some components that are in common with gossipsub, for example the proposer needs to make one BLS signature and the verifier has to check one BLS signature. We record here the benchmarks of the operations that need to be carried in addition to the usual gossipsub operations. These are the CPU *overhead* that the protocol has on nodes. Benchmarks have been carried on a Macbook M4 Pro laptop and on an Intel i7-8550U CPU @ 1.80GHz.

Parameters for these benchmarks were N=10 for the number of chunks and the total block size was considered to be 118.75KB. All benchmarks are single threaded and all can be parallelized

### Proposer

The proposer needs to perform N Pedersen commitments. This was benchmarked to be

| Timing | Model |
| --- | --- |
| [25.588 ms 25.646 ms 25.715 ms] | Apple |
| [46.7ms 47.640 ms 48.667 ms] | Intel |

### Nodes

A receiving node needs to compute 1 Pedersen commitment per chunk and perform a corresponding linear combination of the commitments supplied by the proposer. The timing for these were as follows

| Timing | Model |
| --- | --- |
| [2.6817 ms 2.6983 ms 2.7193 ms] | Apple |
| [4.9479 ms 5.1023 ms 5.2832 ms] | Intel |

When sending a new chunk, the node needs to perform a linear combination of the chunks it has available. Timing for these were as follows

| Timing | Model |
| --- | --- |
| [246.67 µs 247.85 µs 249.46 µs] | Apple |
| [616.97 µs 627.94 µs 640.59 µs] | Intel |

When decoding the full block after receiving N chunks, the node needs to solve a linear system of equations. Timings were as follows

| Timing | Model |
| --- | --- |
| [2.5280 ms 2.5328 ms 2.5382 ms] | Apple |
| [5.1208 ms 5.1421 ms 5.1705 ms] | Intel |

### Overall CPU overhead.

The overall overhead for the proposer on the Apple M4 is 26ms single threaded while for the receiving nodes it is 29.6ms single threaded. Both processes are fully parallelizable. In the case of the proposer, it can compute each commitment in parallel, and in the case of the receiving node these are naturally parallel events since the node is receiving the chunks in parallel from different peers. Running these process in parallel on the Apple M4 leads to 2.6ms in the proposer side and 2.7ms in the receiving peer. For real life applications it is reasonable to consider these overheads as zero compared to the network latencies involved.

### Optimizations

Some premature optimizations that were not implemented consist on inverting the linear system as the chunks come, although the proof of concept cited above does keep the incoming coefficient matrix in Echelon form. Most importantly, the random coefficients for messages do not need to be in such a large field as the Ristretto field. A small prime field like \mathbb{F}_{257} suffices. However, since the Pedersen commitments take place in the Ristretto curve, we are forced to perform the scalar operations in the larger field. The implementation of these benchmarks chooses small coefficients for the linear combinations, and these coefficients grow on each hop. By controlling and choosing the random coefficients correctly, we may be able to bound the coefficients of the linear system (and thus the bandwidth overhead in sending the blocks) to be encoded with say 4 bytes instead of 32.

The simplest way to perform such optimization would be to work over an elliptic curve defined over \mathbb{F}_q with q = p^r for some small prime p. This way the coefficients can be chosen over the subfield \mathbb{F}_p \subset \mathbb{F}_q.

**Privacy considerations** the implementation in the PoC linked above considers that each node, including the proposer, picks small coefficients to compound its linear transformation. This allows a peer receiving a chunk with small coefficients to recognize the proposer of the block. Either the optimization above is employed to keep all coefficients small by performing an algorithm like Bareiss’ expansions or we should allow the proposer to choose random coefficients from the field \mathbb{F}_p.

## Simulations

We performed simulations of block propagation under some simplifying assumptions as follows.

- We choose a random network modeled as a directed graph with 10000 nodes and each node having D peers to send messages to. D is called the Mesh size in this note and was chosen varying on a large range from 3 to 80.
- Peers where chosen randomly and uniformly on the full node set.
- Each connection was chosen with the same bandwidth of X MBps (this is typically assumed to be X=20 in Ethereum but we can leave this number as a parameter)
- Each network hop, incurs in an extra constant latency of L milliseconds (this is typically measured as L=70 but we can leave this number as a parameter)
- The message size is assumed to be B KB in total size.
- For the simulation with RLNC, we used N=10 chunks to divide the block.
- Each time a node would send a message to a peer that would drop it because of being redundant (for example the peer already had the full block), we record the size of the message as wasted bandwidth.

### Gossipsub

We used the number of peers to send messages D=6. We obtain that the network takes 7 hops in average to propagate the full block to 99% of the network, leading to a total propagation time of

 T_{\mathrm{gossipsub, D=6}} = 7 \cdot (L + B/X),

in milliseconds.

[![gossipsub-total-theorical](https://ethresear.ch/uploads/default/optimized/3X/1/f/1faedd25412170c361bb4ac283ca568ae19a8939_2_690x395.png)gossipsub-total-theorical1712×982 70.6 KB](https://ethresear.ch/uploads/default/1faedd25412170c361bb4ac283ca568ae19a8939)

With D=8 the result is similar

T_{\mathrm{gossipsub, D=8}} = 6 \cdot (L + B/X),

The wasted bandwidth is 94,060 \cdot B for D=6 and 100,297 \cdot B for D=8.

For low values of B, like the current Ethereum blocks, latency dominates the propagation, while for larger values, for example propagating blobs after peer-DAS, bandwidth becomes the main factor.

### RLNC

#### Single chunk per peer

With random linear network coding we can use different strategies. We simulated a system in which each node will only send a single chunk to all of the peers in their mesh of size D, this way we guarantee that the latency incurred is the same as in gossipsub: a single latency cost of L milliseconds per hop. This requires the mesh size to be considerably larger than N, the number of chunks. Notice that for a gossipsub mesh size of D_{gossipsub} (for example 8 in current Ethereum), we would need to set D_{RLNC} = D_{gossipsub} \cdot N to consume the same bandwidth per node, this would be 80 with the current values.

With a much more conservative value of half this bandwidth, that is D=40 we obtain

T_{RLNC, D=40} = 4 \cdot \left(L + \frac{B}{10 X} \right),

with a wasted bandwidth of 29,917\cdot B. Assuming the same bandwidth as today we obtain with D=80 we get the impressive

T_{RLNC, D=80} = 3 \cdot \left(L + \frac{B}{10 X} \right),

with a wasted bandwidth of 28,124\cdot B, which is 28% of the corresponding wasted bandwidth in gossipsub.

#### Differences

For the same bandwidth sent per node, we see that the propagation time differs both by dividing the latency in two (there are 3 hops vs 6) and by propagating the block faster consuming a tenth of the bandwidth per unit of time. In addition the wasted bandwidth by superfluous messages gets slashed to 28% of the gossipsub wasted messages. Similar results are obtained for propagation time and wasted bandwidth but reducing the bandwidth sent per node by a half.

In the lower block size end, latency is dominant and the 3 hops vs 6 on gossipsub make most of the difference, in the higher block size end, bandwidth performance is dominant. For much larger blocksizes CPU overhead in RLNC gets worse, but given the order of magnitude of the transmission times, these are negligible.

[![rlnc-gossipsub](https://ethresear.ch/uploads/default/optimized/3X/a/4/a4930d31b70e75180c5165aa0bde5f686be0f527_2_690x395.png)rlnc-gossipsub1712×982 87.7 KB](https://ethresear.ch/uploads/default/a4930d31b70e75180c5165aa0bde5f686be0f527)

#### Multiple chunks per peer

In the single chunk per peer approach in production, nodes with higher bandwidth could choose to broadcast to more peers. At the node level this can be implemented by simply broadcasting to all the current peers and node operators would simply chose the number of peers via a configuration flag. Another approach is to allow nodes to send multiple chunks to a single peer, sequentially. The results of these simulations are exactly the same as the above, but with much lower D as expected. For example with D=6, which would never broadcast a full block in the case of a single chunk sent per peer. The simulation takes 10 hops to broadcast the full block. With D=10 the number of hops is reduced to 9.

## Conclusions, omissions and further work

Our results show that one expects considerable improvement in both block propagation time and bandwidth usage per node if we were to use RLNC over the current routing protocol. These benefits become more apparent the larger the block/blob size or the shorter the latency cost per hop. Implementation of this protocol requires substantial changes to the current architecture and it may entail a new pubsub mechanism altogether. In order to justify this we may want to implement the full networking stack to simulate under [Shadow](https://shadow.github.io/). An alternative would be to implement Reed-Solomon erasure coding and routing, similar to what we do with Peer-DAS. It should be simple to extend the above simulations to this situation, but [op. cit](https://ieeexplore.ieee.org/document/1228459) already includes many such comparisons.

## Replies

**MarcoPolo** (2025-01-07):

This is very cool. I really like the combination of Pedersen commitments and RLNC. I’ll try to port this to go-libp2p soon to play with it.

A couple of questions, forgive me if they are obvious:

- How hard is it to generate an fake valid chunk/vector? In other words, if I wanted to send a peer a vector v that results in a valid commitment, but is not actually generated from the source data, how hard would that be?
- Perhaps relatedly, how hard is it to have two different source blocks that have the same N commitments? Does the hash of the N commitments serve as a unique fingerprint to the data as a typical cryptographic hash does?

Thanks for sharing.

One more note: some of the Math formatting seems to not have rendered correctly in the post.

---

**potuz** (2025-01-07):

Hi! great to see someone from libp2p here. We’ll have a Go version of the poc shortly (currently clogged with other work) and hopefully we’ll be able to put on Shadow/Devnets soon. But indeed it may be better if the chunking/committing part of the broadcast is actually handled by libp2p instead of clients directly. I haven’t thought much about implementation details.

> How hard is it to generate an fake valid chunk/vector?

This is computationally hard in principle if we believe that computing logarithms is hard. That is, you can’t really find an invalid chunk that results in a valid commitment.

> Perhaps relatedly, how hard is it to have two different source blocks that have the same
> N commitments?

Same as above.

> Does the hash of the  N commitments serve as a unique fingerprint to the data as a typical cryptographic hash does?

Yes, correct, so in order to have two conflicting blocks you’d need to find two blocks whose commitments hash to the same thing. You could grind either the commitments or the block.

Notice that other data has to be added to the hash eventually, for blocks for example, we will probably need to add the slot number and even the parent block root for example.

> some of the Math formatting seems to not have rendered correctly in the post.

Thanks for this, most probably I just copied/pasted from Hackmd and ethresear.ch does not support same Latex, will go over this.

---

**Nashatyrev** (2025-01-09):

Wow, great write up! Thank you!

> chosen at random a trusted setup of enough elements

Is it correct that these generators are just randomly selected to be global constants and don’t require setup ceremony? If yes, then the ‘trusted setup’ term sounds a bit confusing to me because is usually seen in the context of ‘ceremony’

> A signed message is the collection of elements 1–4 above.

We may think of a dedicated ‘message header’ which would contain common data for all chunks. It could be commitments vector (element 2), signature (element 4), and probably other data like block slot, hash etc. The header might be included just with the first chunk sent for a specific message to a specific peer. All other chunks would need only header reference.

> If it is, then they discard it as this vector is already a linear combination of the previous ones. The key of the protocol is that this is very unlikely to happen (for the numbers above the probability of this happening is much less than 2^{-256}2−2562^{-256}

Not sure, but it seems that in a real protocol there would be more ‘duplicates’ (linear combinations) as first few chunks revealed by a publisher to the network would result in a prevailing number of their distinct  linear combinations flying around.

> further work

For me it looks like having this coding+commitment combination opens really cool perspective of developing a pubsub protocol which would approach maximal potential effectiveness.

This kind of protocol may also benefit from unreliable messaging (ether bare UDP or datagram feature inside QUIC) if it would be possible to fit a single chunk into packet size.

I was developing quite similar approach but haven’t managed to come up with the right coding+commitment scheme combination. I have a libp2p protocol implementation for that (abstracted from coding and commitment) and did some simulations with it, so I could probably adopt it to your approach and make some tests.

---

**potuz** (2025-01-09):

> Is it correct that these generators…

Yes this is correct, I don’t really know the terminology but yes, this needs to be some collection of randomly picked elements whose logarithms are not known and they are constant.

> We may think of a dedicated ‘message header’…

Yes indeed, for blocks you need the slot for sure and perhaps the parent root depending on design.

> …as first few chunks revealed by a publisher to the network would result in a prevailing number of their distinct linear combinations flying around.

Not really, even the proposer will send a different random linear combination of chunks to each one of its peers (or D many of them). There are still design decisions to be made like whether nodes send 1 chunk to 40 peers or send 2 chunks to 20 and so forth. Nodes may send a single message to their peers or send a new random linear combination every time that they receive a new valid message. At any rate, the probability of getting a linearly dependent chunk is almost zero unless you already have received the full block. This is the real power of RLNC.

> so I could probably adopt it to your approach and make some tests.

This would be amazing! We’re working on having this implemented in Prysm to test on Shadow and I think Lighthouse will test too, it shouldn’t take long to see if it’s viable for blocks. I’m confident it’s great for blobs, but the gains for blocks is not so obvious as it depends on latency.

---

**Nashatyrev** (2025-01-10):

> this needs to be some collection of randomly picked elements whose logarithms are not known and they are constant.

So it could potentially be generated with something like `hash_to_curve` function:  `G[i] = hash_to_curve("setup-domain-$i")`?

> There are still design decisions to be made like whether nodes send 1 chunk to 40 peers or send 2 chunks to 20 and so forth.

I have a [write-up](https://hackmd.io/@nashatyrev/rkXUsFD5a) where I try to come up with an optimal theoretical pubsub strategy. According to reasonings there every node needs to try sending distinct chunks to distinct peers to achieve the maximum effect. But of course in practice it may differ.

> Not really, even the proposer will send a different random linear combination of chunks to each one of its peers

Right, a proposer would send independent chunks. But let’s assume we have 0 latency (for simplicity) and some specific dissemination strategy when different chunks (random linear combinations) are transmitted to different nodes. When the proposer is transmitting  let’s say the chunk #5 (to a node-5), the chunk #0 would be already known to 16 nodes, chunk #1 would be known to 8 nodes, etc. Because when a node receives its first chunk it would better forward this single chunk than wait for one or more others. Thus you would likely have prevailing number of chunks #0, #1, and random linear combination of #0 and #1 at some point.

But I think that would definitely depend on the specific dissemination strategy and would be clearly identifiable by a simulation.

---

**potuz** (2025-01-10):

> the chunk #0 would be already known to 16 nodes, chunk #1 would be known to 8 nodes, etc. Because when a node receives its first chunk it would better forward this single chunk than wait for one or more others.

So this is part of the design decisions. This specific strategy is the one employed in the simulations and it’s already accounted for the dramatic reduction on wasted bandwidth. In fact the simulation was brutal in order to not incur twice in latency nodes simply send one message and never again. I think in real life production nodes will pick a new random linear combination to send to peers every time they import a new chunk, and probably make D be smaller then. We’ll tweak this when we have the Shadow simulation ready.

---

**potuz** (2025-01-13):

I’ve been told that there are quite a few patents regarding RLNC, [this one for example](https://patentcenter.uspto.gov/applications/13267764) covers distributed data storage, not exactly this application but there’s many there in [Google Patents](https://patents.google.com). Patent laws is not my area of expertise, someone else would have to look at this.

---

**chrmatt** (2025-01-16):

Great article! One I thing I don’t follow is how the Pedersen commitments are used. It seems one can only fully verify the validity after receiving enough junks to reconstruct the message? In that case, one can just verify the proposer signature directly without the need for commitments? I think what is desirable is that a peer can verify whether a single chunk is valid (and thus forward or not) without waiting for other chunks. Another challenge is that receiver may not be able to reconstruct the original message if too many invalid chunks are received. I also don’t see how the Pedersen commitment prevents this.

As a shameless self-promotion, I also recommend looking at this academic paper from some time ago that is based on the same idea: [Asymptotically Optimal Message Dissemination
with Applications to Blockchains](https://eprint.iacr.org/2022/1723.pdf). It works with Merkle trees instead of Pedersen commitments, which could be more efficient and more robust.

---

**potuz** (2025-01-16):

The Pedersen commitments are used to verify that a single chunk is valid before forwarding any linear combination obtained from it.  The reason being that the receiver is computing the Pedersen commitment to the supposed linear combination and checking that it coincides with the expected linear combination of the proposer signed Pedersen commitments. I don’t think Merkle proofs would work here, we need any Hash function that is additive.

---

**chrmatt** (2025-01-16):

I think verification of a single chunk is missing from the protocol description? This should be part of the “Sending Peers” section I think, but I don’t see how this verification works there.

As a related question, why do the sending peers form a new chunk via a linear combination instead of just re-sending the chunk they’ve received?

The protocol in the paper I’ve cited above roughly works as follows: The proposer generates chunks of the original message, a Merkle-tree hash of all the chunks, and for each chunk, a Merkle proof that this chunk is one of the original ones. It then sends different chunks to different peers, together with the Merkle hash and the proof for this particular chunk. When a party receives a chunk, that party can verify the Merkle proof to check that this chunk indeed is one of the original ones. In that case, it forwards the chunk to its peers. Whenever sufficiently many chunks have been received, the original message can be recovered.

---

**zincoshine** (2025-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> We propose to use random linear network coding  (RLNC) at the broadcast level. With this coding, the proposer would split the block in N chunks (eg. N=10 for all simulations below) and instead of sending a full block to ~8 peers, it will send a single chunk to ~40 peers (not one of the original chunks, but rather a random linear combination of them, see below for privacy considerations). Peers still need to download a full block, or rather N chunks, but they can get them in parallel from different peers. After they have received these N chunks that each is a random linear combination of the original chunks composing the original block, peers need to solve a linear system of equations to recover the full block.

Am I correct in assuming that this method is a variant of Rateless IBLT (https://dl.acm.org/doi/pdf/10.1145/3651890.3672219)? Would we achieve more improvement both of these are implemented together?

---

**potuz** (2025-01-17):

Honeslty I do not see how this is a variant. Both share randomness,  redundancy and encoding as methods to improve reliability in data transfer. But they seem to solve different problems. If anything perhaps IBLT could be used as you suggest in parallel to RLNC, as a replacement to RS encoding for example for blobs. I don’t know of the topic to say anything on the matter.

---

**potuz** (2025-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/chrmatt/48/15735_2.png) chrmatt:

> I  think verification of a single chunk is missing from the protocol description? This should be part of the “Sending Peers” section I think, but I don’t see how this verification works there.

The verification is in this snippet of the doc

[![fo](https://ethresear.ch/uploads/default/original/3X/6/8/680fa21903beba3aa1b0f498eb91f824e20a4bd1.jpeg)fo739×187 23.5 KB](https://ethresear.ch/uploads/default/680fa21903beba3aa1b0f498eb91f824e20a4bd1)

---

**chrmatt** (2025-01-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> The verification is in this snippet of the doc

Ah, yes, sorry. I misread “When a peer receives a message as in the previous section” to mean that this is done after receiving the full message, i.e., enough chunks…

But if this and the re-sending is done for every individual chunk, this means in particular that when a peer receive the first chunk, it will just send (a multiple of) this chunk to its peers. Hence, it is in the same subspace as the original chunk. So this will be discarded by all peers who have received the same chunk, which has much higher probability than the claimed 2^{-256}.

---

**potuz** (2025-01-19):

As discussed above there are design decisions to make as to when/how peers resubmit messages. However, notice that the proposer sends also random chunks to each peer so any rebroadcast is anyway highly probably a new message to any other peer on the first rebroadcast. By the time there is a second hop there are high chances that those nodes already have a two dimensional space. As Anton noted above, this has to be benchmarked and studied to check the best rebroadcasting tactics.

---

**jtremback** (2025-01-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> The Pedersen commitments are used to verify that a single chunk is valid before forwarding any linear combination obtained from it.

What is the underlying reason for doing this? Is it just to keep nodes from gossiping crap?

---

**potuz** (2025-01-24):

Yes, otherwise nodes could make nodes decode the wrong block and only after downloading all chunks and decoding the node would be able to find out that the data was bogus. Even worse, a single chunk could cause this so the node wouldn’t be able to even know which peer was malicious. Also since nodes rebroadcast chunks, a single malicious operator could exponentiate it’s DOS attack on the network.

---

**MedardDuffy** (2025-01-28):

It is great to see our RLNC work highlighted! RLNC is indeed optimal for gossip in terms of propagation speed, as detailed in this paper: S. Deb, M. Médard and C. Choute, “Algebraic gossip: a network coding approach to optimal multiple rumor mongering,” in *IEEE Transactions on Information Theory* , vol. 52, no. 6, pp. 2486-2507, June 2006.

Early this year, my co-authored book, *Network Coding for Engineers*, will be published by IEEE Press. It provides a detailed explanation of RLNC along with clear implementation examples. I hope the community interested in this technology finds it useful.

---

**MedardDuffy** (2025-01-28):

It is not rateless IBLT, which is an end-to-end coded hash. RLNC, like pretty much all codes, IBLT included, provides a hash.

---

**CPerezz** (2025-01-28):

Thanks so much for this nice post! It was a pleasant and interesting read! And definitely a really nice proposal!

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> A small prime field like \mathbb{F_{2^{257}}}

How is this a small field? Is almost the order of the scalar one of Ristretto or 25519 already (2^{255}-19).

I wonder if in general you have explored other commitment schemes. If the SRS (trusted setup) is a must-have, then seems only KZG is the other viable option.

- I wonder if this could be done differently to avoid using EC-based stuff in the networking layer(considering there are plans to migrate to PQ primitives). I’m thinking about Ajtai commitments mostly. But there could be other things worth exploring. Just need to be sure I understand all the properties that this requires to a commitment scheme.
- Also, worth considering using on the “Don’t care about PQ case” something like: Efficient Elliptic Curve Operations On Microcontrollers With Finite Field Extensions. This allows us to have curves that have extremely tiny fields, yet give us 128-bit security. Thus, enabling us to have all the benefits of small fields with the properties like hash-to-curve etc…

As for RLNC this is definitely a really nice option for gossiping!

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> The simulation takes 10 hops to broadcast the full block. With D=10D=10D=10 the number of hops is reduced to 9.

I think it’s also important to highlight this metric. RLNC saves us bandwidth undeniably. And it definitely seems to improve converging times. ie. time it takes to the majority of the network to be in sync on latest state sent.

Do you envision any possible improvements in that part? Is already RLNC addressing this problem too? Hence we just ignore this?


*(33 more replies not shown)*
