---
source: magicians
topic_id: 2958
title: Unitrie, a replacement of the state trie in Eth 1.0 (or 2.0)
author: sergio_lerner
date: "2019-03-21"
category: EIPs
tags: [storage-rent, trie, fast-sync, garballe-collection]
url: https://ethereum-magicians.org/t/unitrie-a-replacement-of-the-state-trie-in-eth-1-0-or-2-0/2958
views: 2025
likes: 5
posts_count: 3
---

# Unitrie, a replacement of the state trie in Eth 1.0 (or 2.0)

I’ve been working since 2016 on storage rent and other improvements to the EVM, mainly for use in RSK, but also for Ethereum. This week I posted an article about the **Unitrie**, a special kind of radix-2 Patricia Trie that reduces memory consumption, storage, CPU load, bandwidth, complexity, provides DoS protection for fast-warp-sync, enables simpler garbage collection, storage rent and data hibernation.

You can find the article here https://www.rsk.co/noticia/towards-higher-onchain-scalability-with-the-unitrie/

The Unitrie is specified in RSKIPs but I’m willing to create associated EIPs if this proposal is of the interest of the Ethereum community.

You can go directly to the RSKIP repository and read [RSKIP16](https://github.com/rsksmart/RSKIPs/blob/master/IPs/RSKIP16.md), RSKIP107, RSKIP108, RSKIP109, RSKIP112, RSKIP113, RSKIP116, RSKIP117, but I highly recommend the article as the starting point.

## Replies

**vbuterin** (2019-03-22):

So the current approach for eth2 is that contracts are fixed-size (in part to make rent simpler, but also for other reasons, including to make yanking, hibernation and waking simpler), and we use a simple binary sparse Merkle tree at consensus level (with [optimizations at client level](https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751) to achieve the performance we’re used to).

The idea of using `top80bits(h(addr)) + addr` instead of `h(addr)` as the key is definitely interesting and does solve one of the significant objections to the current trie structure that I know about.

Using binary sparse trees is nice because they support [optimal Merkle multiproofs](https://github.com/ethereum/eth2.0-specs/blob/ced6208d55d26d63f532d4bb031869740b2a111c/specs/light_client/merkle_proofs.md) of exactly the same form as we use for simple Merkle trees.

What concrete differences and benefits are in the Unitrie aside from this?

---

**sergio_lerner** (2019-03-23):

The SMT approach is interesting from the formal point of view: you can very easily describe it mathematically and prove properties about it. However moving complexity to the client side does not mean that complexity is gone. On the contrary, the complexity grows, as it requires specific algorithms and data structures for storing on disk, for storing on memory, for membership proving, and for compressing prefixes to prevent a 20X space blowup.

Storing the size of the sub-tree in each node (or in the SMT case, it’s equivalent to the number of non-empty child nodes) allows to download the state knowing the completion percentage at all times, which is something that Ethereum lacks right now. The overhead is low, and the benefit from the usability perspective could be huge. Also, it enables partitioning the state in non-overlapping chunks, starting at different byte offsets, that you can request to different peers in parallel, but verify correctness independently.

You also assume that full nodes will pack the SMT nodes into small 2^k trees (and extend the hash function accordingly) to reduce space consumption and disk access. And each implementation may choose a different k. This however prevents a peer to request a specific tree node by hash, so either every client opts to store the tree in the same way, or there will be different and incompatible state synchronization schemes. So you’ll need to keep a map of every node hash to the tree it belongs. More complexity and space. It’s simpler if every one agrees of a single k. Therefore, the potential benefit of free choice of radix-packing may not materialize in practice.

All the remaining properties of the Unitrie can be emulated for the SMT using client-side code, but again, you will need interoperability, so that at the end you may have to pick just one scheme for all full node implementations.

