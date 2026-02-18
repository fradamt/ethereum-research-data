---
source: ethresearch
topic_id: 1599
title: Non-interactive data availability proofs
author: musalbas
date: "2018-04-02"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/non-interactive-data-availability-proofs/1599
views: 3582
likes: 7
posts_count: 3
---

# Non-interactive data availability proofs

Prerequisite: https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding

Similar to how [Schnorr NIZK proofs](https://tools.ietf.org/html/rfc8235) work, instead of the light client providing a set of random coordinates for chunks to the node sending the the block, the node sending the the block could generate the set of coordinates seeded from a precomputed challenge specific to each light client, e.g. H(blockHeader || clientID).

What’s the security implication of letting miners possibly only release blocks that cause light clients to sample chunks that the miner wants? If a miner wanted to only fool a small set of light clients (the “only releasing individual bits of data as clients query for them” attack), then the miner might want to create a block such that those light clients don’t sample chunks that contain provably bad transactions, if your fraud proof generation mechanism is fine-grained enough to generate fraud proofs from incomplete blocks. However, this is already very unlikely anyway with an interactive data availability proof mechanism, since a bad transaction can be hidden in 1 of the 4096 chunks for a 1MB block.

## Replies

**vbuterin** (2018-04-02):

This does seem a little too prone to allowing malicious nodes to generate blocks that fool individual clients. Remember that in the long term I think that clients should generate their random coordinates and then send out challenges separately using onion routing, so a malicious block proposer would not even be able to tell which challenges come from the same user.

---

**musalbas** (2018-10-22):

Here’s a way you could do non-interactive data availability proofs that also prevents the selective share disclosure attack, using Tor hidden services so that block producers can’t tell which sample requests came from the same users.

**Registration**

Suppose the user makes s samples per challenge. The user sets up s hidden services, and registers the addresses of these hidden services with different random full nodes in the network. It is important that these registrations aren’t linkable to each other, thus they could be sent over a mix net.

**Proof phase**

Now, suppose a new block is produced. When a full node receives a new block, it sends to each hidden service that has registered with it the sample in that block corresponding to the index seeded from H(blockHeader||hiddenServiceAddress). Note that hidden service addresses are random strings, and here we assume that blockHeader contains a random nonce that is difficult or expensive to influence by the block producer.

Because the hidden services are anonymous and - if the registration was done correctly - unlinkable with each other - this prevents malicious nodes from fooling individual clients.

This scheme has two advantages over simply sending requests over onion routing:

- You only need to worry about your requests being unlinkable to each other once (in the registration phase), rather than every time a new block comes along.
- Light clients can accept new blocks immediately, rather than having to wait for some delay so that everyone can send their requests at the same time.

