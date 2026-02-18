---
source: ethresearch
topic_id: 13926
title: Parallel txs processing with chunked Merkle Patricia Trie(s)
author: ivan-homoliak
date: "2022-10-12"
category: EVM
tags: []
url: https://ethresear.ch/t/parallel-txs-processing-with-chunked-merkle-patricia-trie-s/13926
views: 2343
likes: 3
posts_count: 3
---

# Parallel txs processing with chunked Merkle Patricia Trie(s)

I assume just a single shard with one global account state represented by one Merkle-Patricia Trie (MPT), as originally proposed in the yellow paper. I am aware of Verkle tries, and this idea seems orthogonal to it. Also, I am pretty familiar with Aleph C++ implementation (currently deprecated), while I checked geth only very briefly.

**Idea**

The global state as an instance of MPT  is a data structure with exclusive access - meaning that only a single tx can be processed at one time. Processing of a single tx is expensive regarding storage/memory accesses - descending to a leaf node with an account state to update it might require several storage accesses (even though the caching might help to some extent) + the same number of write modifications. From some of my experiments made within a small research project [Aquareum](https://arxiv.org/pdf/2005.13339), this looked as the biggest bottleneck of EVM execution. Anyway, I was thinking why not to replace a single exclusive MPT by a number of independent MPTs that would enable parallel processing of txs, while all these small MPTs could be aggregated by a standard binary Merkle tree after all txs of a block have been processed in EVM already - root hash would be stored in a header instead of MPT root, so light clients would not lose any integrity information.

**Details**

The number of such MPT should respect requirements for parallelization (no. of cores/threats, distribution of no. of txs modifying more account states, etc). For example, it could consume 3 nibbles of the original key to a single global MPT, representing 2^12 = 4096 small MPTs, while the path in small MPTs would start addressing from the 4th nibble of the key. In this way, txs modifying just a single account state could be heavily parallelized but txt modifying more than 1 account state would need a lock on all account states being modified. They could be known beforehand (w/o executing tx), in which case the planning should be trivial but in some cases, they might be known only dynamically (while executing tx’s code). In the latter, dynamic synchronization primitives of process scheduling could be used and probably it would involve some small overhead which, however, should be compensated for still interesting parallelization.

## Replies

**laurentyzhang** (2022-10-13):

In fact, the Merkle tree is probably the single biggest bottle of Ethereum right now. A simple lookup involves multiple DB reads. You have to travel through multiple non-leaf entries to get to the leaf. As the states grow, it only gets worse.

We came up with a similar idea a couple years ago. Now we have implemented the parallel Merkle Tree in Arcology Network. It worked pretty well.

---

**ivan-homoliak** (2022-10-14):

Thanks for the reaction. Just to clarify - I believe that by saying Merkle tree, you mean MPT. Anyway I am surprised that Ethereum foundation did nothing about the optimization of MPT access so far – Geth seems to use the serial version of MPT - [https://github.com/agiletechvn/go-ethereum-code-analysis/blob/62e359d65ef1fc5f1fe6b0672a5fb9397db503c4/trie-analysis.md](https://github.com/agiletechvn/go-ethereum-code-analysis/blob/master/trie-analysis.md). Would be good if someone from Ethereum would see it.

BTW, I briefly checked the project **Arcology** and post https://ethresear.ch/t/introducing-arcololgy-a-parallel-l1-with-evm-compatibility/13883. Will put my comments there.

