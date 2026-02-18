---
source: ethresearch
topic_id: 6802
title: Storing (almost) all contract state on Swarm INSTEAD of the Blockchain
author: nagydani
date: "2020-01-18"
category: Data Structure
tags: []
url: https://ethresear.ch/t/storing-almost-all-contract-state-on-swarm-instead-of-the-blockchain/6802
views: 1898
likes: 4
posts_count: 5
---

# Storing (almost) all contract state on Swarm INSTEAD of the Blockchain

This proposal is *not* introducing any changes to Ethereum; it merely outlines a novel way to write contracts in a way that would result in their on-chain state consisting of a single 256-bit value. Any contract can be algorithmically transformed (i.e. compiled) into this proposed form. Since storing data on the blockchain is expensive and its cost can be expected to be internalized by the introduction of state rent, this proposal can be regarded as a scalability improvement, as it allows Ethereum contracts to manipulate arbitrarily large state without having to store all of it on the blockchain.

**Swarm**, for the purpose of this proposal, is just a distributed preimage archive that allows the retrieval of fixed-sized chunks of data based on their crypgoraphic hash, which is (relatively) cheap to compute in EVM.

**Contract state** is a 256 bit to 256 bit map.

Contract state can be represented as a Merkleized binary PATRICIA trie in which every inner node (representing a subtrie) contains a bit offset of the branching (i.e. the length of the common prefix of keys of the subtrie in bits) and references to the two subtries.  Leaves are simply (K,V) mappings. Note that the number of inner nodes is always exactly one less than the number of mappings. Each insertion except the first one results in adding exactly one inner node and one leaf; conversely, each deletion except the last one removes one of each. Note that there are ways of representing binary PATRICIA tries in such a way that each node contains one mapping, one bit offset and only one reference to another node; the actual implementation of the proposal might opt for using such a representation.

If the reference to a node is its hash value, then an insertion or a deletion can alter at most 255 nodes, irrespective of the size of the map. In practice, keys in the state are typically hashes of the actual values used as keys, which makes the trie representation balanced and its depth the logarithm of the map’s size. In this typical case, insertions and deletions alter a logarithmic number of nodes.

Thus, one can replace SSTORE and SLOAD opcodes by subroutines that perform the corresponding operations on an externally stored Merkleized map, using the root reference stored in the contract’s onchain state and additional data with Merkle proofs supplied in transaction data. The replacement of SLOAD will return the value supplied in transaction data, but will also verify the Merkle proof that the K,V mapping (including implicit K,0 mappings) is, indeed, present in the map with the on-chain root reference. The replacement of SSTORE will update the on-chain root reference.

Note, furthermore, that the pre-image oracle necessary for the use of such contracts can be instantiated using only transaction history, though in practice it is, of course, much more convenient if an efficient Swarm-like content-addressed storage network performs this role.

It is also important ot note that in this model, at most one of concurrently submitted transactions altering the state can succeed; the ones that fail need to be re-submitted with Merkle proofs calculated from the state updated by the successful transaction.

Essentially, this proposal virtualizes the stateless client model on top of current EVM, thus reducing the on-chain contract state to a single Swarm-reference.

## Replies

**vbuterin** (2020-01-18):

Are there any *consensus-layer* differences between this and “just doing stateless clients”? Whether contract state is stored in Swarm, or 10% of full nodes, or Infura, is just a layer-2 choice that can be swapped out, no?

---

**nagydani** (2020-01-20):

The answer to the second question is a resounding “yes”. This is partially what I meant by the paragraph about the pre-image oracle (third from bottom). Should I spell it out more explcitly in the proposal?

The answer to the first one is a bit more nuanced. “Just doing stateless clients” can certainly be done in a very similar fashion, by supplying the Merkle proofs for all state access together with transactions. Whether the fact that in case of “just doing stateless clients” these are verified by the client in an operation that is not part of the consensus while in the above proposal they are verified by EVM counts as a consensus-layer difference, I am not sure.

While the proposal was very obviously inspired by stateless clients and with the exception of the aforementioned difference the *consensus-layer* architecture is very similar, there are other important differences with stateless clients, albeit not in the consensus-layer. One such difference is that unlike “just doing stateless clients”, it requires no change in the network protocol, as the Merkle proofs are supplied as part of transaction data, not in addition to it, so the current Ethereum network can handle such contracts as it is. This implies that this proposal can be implemented by users that can benefit from it independently of anyone else (even other such users), simply by writing and operating contracts following this pattern of state access and update.

---

**vbuterin** (2020-01-20):

Aaah, I see, I think this approach has been called “stateless contracts” in the literature. Basically doing the same thing as stateless clients, but writing it out as EVM code. I think the main challenge there is that it’s harder to handle cases where multiple people want to interact with some contract at the same time (though there *are* ways to support `k` simultaneous interactions with `O(k * log(N))` storage!). Definitely a good design pattern!

Arguably optimistic rollup and zk rollup are also a type of stateless contract.

---

**nagydani** (2020-01-20):

It is an *almost* stateless contract, as it does have a 256-bit onchain state, but yes, ZK rollups and optimistic rollups are in many ways similar. The proposal is about a systematic way of transforming any Ethereum contract to this paradigm. Rollups are slightly different, as they require operators and they scale Ethereum along the tx/s axis, whereas this proposal is about radically reducing onchain state. In fact, I believe that the two are somewhat orthogonal and can even be combined.

Concurrency is, indeed, somewhat of a problem, as all but one concurrently submitted transactions changing the state will fail, somewhat expensively and will need to be resubmitted with the new state root. It can be (to some extent) mitigated by a client strategy that cleverly re-submits transactions that are going to fail with the same nonce but an updated state root (and maybe a higher gas price), while they are still in the mempool. Thus, the failing tx won’t get into the blockchain.

