---
source: ethresearch
topic_id: 5543
title: Simpler hash-efficient sparse tree
author: JustinDrake
date: "2019-06-02"
category: Data Structure
tags: [sparse-merkle-tree]
url: https://ethresear.ch/t/simpler-hash-efficient-sparse-tree/5543
views: 4559
likes: 0
posts_count: 17
---

# Simpler hash-efficient sparse tree

**TLDR**: We suggest a sparse Merkle key-value tree with improved simplicity, efficiency and security compared to [this recent construction](https://ethresear.ch/t/a-nearly-trivial-on-zero-inputs-32-bytes-long-collision-resistant-hash-function/5511).

**Construction**

Given 32-byte values l and r let h(l, r) = \text{sha256}(l, r) | 0b1 (i.e. hardcode the least significant bit to 1) if l, r \ne 0 and h(l, r) = \max(l, r) otherwise. Build a sparse Merkle tree where the leaf at position k has value \text{sha256}(k, v) \& 0b0 (i.e. hardcode the least significant bit to 0) for every key-value pairs (k, v), and use h to accumulate the leaves into a root.

Whenever a key-value pair (k, v) is authenticated (in particular, when modifying the tree statelessly) it suffices to validate the corresponding Merkle path from leaf to root, *as well as* check that the leaf position k is consistent with the leaf value \text{sha256}(k, v).

**Security argument**

Notice that h is not collision resistant precisely when l = 0 or r = 0, and h(l, r) = \max(l, r) = h(r, l). (Notice also that leaf values—and their accumulations with zero leaves—do not collide with h when l, r \ne 0 because of the hardcoded bit.) We argue that the construction is nevertheless secure.

Notice the collisions when l = 0 or r = 0 allow for a non-zero leaf in an otherwise zero subtree to “move” within the subtree while preserving the Merkle root. Conversely, it is easy to see (e.g. with a recursive argument) that two equal-depth Merkle trees with the same root are equivalent modulo moving non-zero leaves in otherwise zero subtrees.

As such, validating a Merkle path from leaf to root authenticates the leaf within an otherwise zero subtree. The exact leaf position is then disambiguated by checking that the key k is properly “mixed in” the leaf value \text{sha256}(k, v).

**Discussion**

The construction is comparable to [Vitalik’s](https://ethresear.ch/t/a-nearly-trivial-on-zero-inputs-32-bytes-long-collision-resistant-hash-function/5511). The main difference is the disambiguation of non-zero leaf positions within zero subtrees. Vitalik’s construction zeroes out 16 bits from the sha256 outputs and uses the extra space as “position bits”. This construction keys the leaves instead, with several benefits:

- simplicity: The accumulating function h is cleaner and simpler.
- efficiency: Vitalik’s construction has an overhead of about 256/(256-240) = 16 hashes per Merkle path due to the overflowing of position bits. There is no such overhead here.
- security: Vitalik’s construction reduces preimage resistance by 16 bits due to the zeroing of hash output bits. Only a single bit of preimage security is lost in this construction.

## Replies

**tawarien** (2019-06-03):

The construction is indeed very simple but compared to [Vitalik’s construction](https://ethresear.ch/t/a-nearly-trivial-on-zero-inputs-32-bytes-long-collision-resistant-hash-function/5511) it does not work for non-membership proofs or proof of insertion, as both of these require to show that a certain leaf is not set, meaning k is not part of the proof and as such it can not be used to resolve the collision of max(h1,h2) & max(h2,h1).

I think membership proofs are not enough if a state transition function can read leaves that are not set yet because in that case a non-membership proof is needed.

---

**JustinDrake** (2019-06-03):

> I think membership proofs are not enough

Right, we definitely want non-membership proofs ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> it does not work for non-membership proofs

Here’s a suggested fix. When aggregating two non-zero nodes l, r into the node with generalised index i, replace \text{sha256}(l, r) with \text{sha256}(l, r, i). (Notice that i is a run-time variable that does not require storage, and that \text{sha256}(l, r) and \text{sha256}(l, r, i) both hash over two 512-bit words.)

To build a non-membership proof for a key k find the lowest-depth node (with generalised index i, say) “above” the leaf at position k that aggregates two non-zero nodes. (If no such node exists then the proof is trivial.) The child of that node closest to k must then equal the unique non-zero leaf in an otherwise zero subtree, and it suffices to prove (using a proof of membership which checks i is consistent with \text{sha256}(l, r, i) and k) that this non-zero leaf has key not equal to k.

> or proof of insertion

What is a proof of insertion (as opposed to proofs of membership and non-membership)?

---

**tawarien** (2019-06-03):

I think that could work as *i* prevents moving non-zero interior nodes without changing the hash of the parents and the key prevents moving the non-zero leaves without detecting it. And non membership proofs are then simply a proof that their is a subtree with only one leaf and that this leaf has not the key k but that the leaf of k would be placed in the same subtree.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> or proof of insertion

What is a proof of insertion (as opposed to proofs of membership and non-membership)?

A proof of insertion is a proof that proofs that a key value pair can be inserted into a tree with a certain root hash but simultaneously allows to calculate the root hash after the insertion just from the old root hash and the proof. For many hash tree constructions proof of non-membership and proof of insertion look the same (except that the proof of insertion specifies the value to insert).

---

**JustinDrake** (2019-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> i prevents moving non-zero interior nodes without changing the hash of the parents and the key prevents moving the non-zero leaves without detecting it. And non membership proofs are then simply a proof that their is a subtree with only one leaf and that this leaf has not the key k but that the leaf of k would be placed in the same subtree.

Exactly, great summary ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**tawarien** (2019-06-03):

Their is another Thread about [Compact Sparse Merkle Trees](https://ethresear.ch/t/compact-sparse-merkle-trees/3741/17) where the basic idea is to get rid of all zero nodes and leaves by replacing each sub tree that contains only one non-zero leaf or only  one non-zero node / subtree with that leaf / node. I mentioning it because your hash function has actually the same effect on the hash values as this compacting approach. My last proposal in that thread uses a key prefix as extra information which actually is a unique index, that has the nice property that the unique index for a leaf is its key

---

**tawarien** (2019-06-04):

I discovered a further problem of this approach concerning the practical implementation of it. The current storage scheme assumes a collision resistant hash function. More precisely it stores each node/leaf in a key-value store using the hash as key. As the presented hash function is not collision resistant different nodes can end up with the same hash/key and thus the current storage scheme will not work with it.

---

**JustinDrake** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> it stores each node/leaf in a key-value store using the hash as key

Is the choice of key-value store keying just an implementation detail? In other words, can an implementation use a collision-resistant hash function (e.g. \text{sha256}) for internal store keying?

---

**tawarien** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Is the choice of key-value store keying just an implementation detail? In other words, can an implementation use a collision-resistant hash function (e.g. sha256\text{sha256}) for internal store keying?

If another hash is used for calculating the storage key, then we hash each node twice, once with the special hash and once with the normal hash for the key generation and all the benefits of using a special hash are lost when interacting with the storage (As proof checking does not require storage interactions the special hash would be enough their). Furthermore, because we need the key of the children of a node for the lookup and the special hash of the children for generating proofs / calculating the state root after a modification both hashes had to be stored, doubling the storage requirements. Beside the efficiency questions the question arises if it is worth the trade-off between having a simpler special hash vs having a simpler storage scheme.

---

**JustinDrake** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tawarien/48/302_2.png) tawarien:

> the benefits of using a special hash are lost when interacting with the storage

I guess the point is to minimise consensus-level complexity and overhead (as opposed to implementation-level complexity and overhead).

---

**vbuterin** (2019-06-04):

I like this approach! It does a good job of getting the benefits of key-value trees while preserving the simplicity of sparse binary trees.

Though I do think that making proofs of membership and non-membership look exactly identical would be ideal. I wonder if there’s some really clever way of doing something equivalent to initializing a tree with 2**256 elements that each have different indices, but without actually doing the 2**256 work that doing this naively would require.

---

**vbuterin** (2019-06-04):

One approach is stacking the scheme on top of itself using a smaller tree size, eg. 65536, so the total setup cost is 131071 hashes per tree * 16 for the 16 levels of the tree, but such a scheme would also require an overhead of 16 actual hashes for a proof of a 256-bit key (just like the other scheme ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=14))

---

**tawarien** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Is the choice of key-value store keying just an implementation detail? In other words, can an implementation use a collision-resistant hash function (e.g. sha256\text{sha256}) for internal store keying?

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> I guess the point is to minimise consensus-level complexity and overhead (as opposed to implementation-level complexity and overhead).

I just came up with another idea, that could keep the implementation complexity low as well. The proposed special hash still preserves that subtrees containing different key value pairs at their leaves (ignoring zero-leaves) have different hashes and thus the collision only happens for subtrees at different heights that have the same key-value pairs at their leaves (agian ignoring zero-leafes). Thus we can simply use the hash of the node concatenated with the height of the node as key for the database.

---

**tawarien** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I wonder if there’s some really clever way of doing something equivalent to initializing a tree with 2^256 elements that each have different indices, but without actually doing the 2^256 work that doing this naively would require.

If we initialize the leaves with indicies then we do no longer have a classical sparse tree and can not shortcut the hash anymore (except if we find a hash that is fast if both inputs are subtrees containing just indicies)

---

**vbuterin** (2019-06-04):

Technically my approach is still fast if we store the 2m precomputed hashes ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=14)

---

**tawarien** (2019-06-04):

Thats true, with that approach it would be as fast as a Sparse Merkle Tree but we would still need a new shortcut for H(l,r) where l or r is a precomputed hash (empty subtree) or we would not gain anything over a classical Sparse Merkle Tree or do I miss something in that construction?

---

**ChosunOne** (2019-07-10):

> can an implementation use a collision-resistant hash function (e.g. sha256) for internal store keying?

[My implementation](https://github.com/ChosunOne/merkle_bit) (currently used by [crypto.com](http://crypto.com)’s implementation of their own chain) of a similar idea (compressing chains of branches to a single node) can swap out hash functions for internal store keying and external facing hashes (they are really the same, the root is just another address in the tree).  I don’t currently have two hashing functions implemented, but I can if there is demand for it, since the implementation is trivial.

