---
source: magicians
topic_id: 11744
title: Parallel txs processing with chunked Merkle Patricia Trie(s)
author: ihomoliak
date: "2022-11-15"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/parallel-txs-processing-with-chunked-merkle-patricia-trie-s/11744
views: 704
likes: 0
posts_count: 7
---

# Parallel txs processing with chunked Merkle Patricia Trie(s)

I assume just a single shard with one global account state represented by one Merkle-Patricia Trie (MPT), as originally proposed in the yellow paper. I am aware of Verkle tries, and this idea seems orthogonal to it. Also, I am pretty familiar with Aleph C++ implementation (currently deprecated), while I checked geth only very briefly.

**Idea**

The global state as an instance of MPT is a data structure with exclusive access - meaning that only a single tx can be processed at one time. Processing of a single tx is expensive regarding storage/memory accesses - descending to a leaf node with an account state to update it might require several storage accesses (even though the caching might help to some extent) + the same number of write modifications. From some of my experiments made within a small research project [Aquareum](https://arxiv.org/pdf/2005.13339), this looked as the biggest bottleneck of EVM execution. Anyway, I was thinking why not to replace a single exclusive MPT by a number of independent MPTs that would enable parallel processing of txs, while all these small MPTs could be aggregated by a standard binary Merkle tree after all txs of a block have been processed in EVM already - root hash would be stored in a header instead of MPT root, so light clients would not lose any integrity information.

**Details**

The number of such MPT should respect requirements for parallelization (no. of cores/threats, distribution of no. of txs modifying more account states, etc). For example, it could consume 3 nibbles of the original key to a single global MPT, representing 2^12 = 4096 small MPTs, while the path in small MPTs would start addressing from the 4th nibble of the key. In this way, txs modifying just a single account state could be heavily parallelized but txt modifying more than 1 account state would need a lock on all account states being modified. They could be known beforehand (w/o executing tx), in which case the planning should be trivial but in some cases, they might be known only dynamically (while executing tx’s code). In the latter, dynamic synchronization primitives of process scheduling could be used and probably it would involve some small overhead which, however, should be compensated for still interesting parallelization.

**Original post:**

https://ethresear.ch/t/parallel-txs-processing-with-chunked-merkle-patricia-trie-s/13926

## Replies

**matt** (2022-11-16):

Tons of prior art on this from the sharding days. I don’t think we’ll ever make this change in the core protocol because it is invasive and is essentially what is happening with L2s. They are posting data to the L1 chain and maintaining their own trie separately.

---

**bipedaljoe** (2025-12-15):

Doesn’t a patricia merkle trie shard perfectly to start with? For example, 16 shard on each of the first 16 branches. Then they just submit their “sub-roots” and the coordinator calculates the state account trie root?

There is many other problems in sharding contracts. Ethereum assumes all transactions are processed in sequence. You would need to distinguish between parallel and sequential contract calls somehow, and assume all transactions are processed in parallel and then force those who do sequential calls to be sequential only they.

Ethereum was designed to be “single-threaded”. It made many things shardable such as by using Patricia Merkle Tries but it was not designed to be doing things in parallel.

As far as I see. Scaling ideas in general also tend to not understand Nakamoto consensus game theory.

---

**ihomoliak** (2025-12-15):

Sharding and parallel processing are two different things from the performance point-of-view. If you have multiple shards, each of them has its own state trie and works fast if transactions “do not need” account states outside of the current shard. However, these situations are very rare, and the reality is that most of the transactions require access to account states of various shards, and thus state tries. The overhead of such inter-shard transactions is substantially higher and thus impedes scalability.

However, parallel processing can be made even within a single shard with integrity-preserving parallel access to the global state trie, as I outline above. It just needs to remain deterministic, so all other consensus nodes can re-execute it deterministically to validate the correctness of execution. This might be tricky, but there were a few proposals on this topic.

---

**bipedaljoe** (2025-12-15):

I don’t at all see what your vision is. There is probably good ways to organize things to make it easy to parallelize regardless of what terms are used. The “single exclusive PMT” you mean is just an agreement on if it is exclusive or not. I can be in a team of 32 people and we can agree to deal with 1/32th of the account trie, and that I would exclusively get access to a certain branch, and then we collaborate to assemble the account trie root. Whether or not anything is exclusive is just an internal agreement. People seem to be chasing “trustless sharding” but validator attestation is not trustless, it is trust-based, and to me that seems to be where a lot of the confused ideation comes from. Or maybe your vision is great, I do not at all see what it is, but could be it is me who is just unable to understand it. Peace

---

**bipedaljoe** (2025-12-16):

One way I see benefit of multiple tries is to distinguish between sequential and parallel storage tries. The privileges to those need to be split differently (by the “kernel” of the “team” operating as “validator”). For the sequential, all contract calls have to go via a single shard (also need to somehow store proof of what sequence of events was) and they would control the full storage trie. But for parallel, you benefit from a trie where you split over shards by ranges of keys in it. And shards collaborate to assemble the tree root. Two different types of storage tries by access-rights. It seems two types of storage tries could be beneficial, one shards for sequential processing (the full trie under one shard) and one for parallel (branches of trie per shard). Maybe this is similar in some way to your vision.

---

**bipedaljoe** (2025-12-21):

Seems to me two storage tries are a good approach, one sequential and one parallel. The sequential is the current account trie (external accounts and contracts), and the contracts contain current storage trie for sequential data. Then, you have a “parallel” data type (by definition some kind of mapping or array-like that can be operated on in parallel) that is in the “parallelized storage trie”. These two storage tries shard differently. The sequential one (account) shards by account. The parallelized one, shards by keys in the nested trie under the storage slots. It can store pointers to slots in itself as values for nested keys (thus arbitrary nesting). It is flat (contract address hashed with the storge slot key).

One data type possible with this is “deferred ordering array”, where it remains unordered as it is appended to, and then it orders once appends are finished. You can use this to, for example, register 10 billion people for a video pseudonym event, and then shuffle those 10 billion people. First, do an unordered array and register everyone. Then, hash each key and move it to a new trie. Then, order the new trie.

Important here is the “sharding” is “internal” to the validator. There is no consensus on number of shards. A validator can do zero shards, or 4096. It is up to them. This is in contrast to what you seem to suggest ihomaliak as you seem to consider fixed number of “chunked tries” for fixed number of shards. But I think people have misunderstood how to shard (as I go through in my other post Principles of Scaling a World Computer), specifically the “trust-based bottleneck” has been neglected (it was assumed trustless pre-maturely).

