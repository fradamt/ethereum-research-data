---
source: ethresearch
topic_id: 3751
title: Optimizing sparse Merkle trees
author: vbuterin
date: "2018-10-09"
category: Data Structure
tags: [data-structure, sparse-merkle-tree]
url: https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751
views: 26126
likes: 25
posts_count: 30
---

# Optimizing sparse Merkle trees

A sparse Merkle tree (SMT) is a data structure useful for storing a key/value map which works as follows. An empty SMT is simply a Merkle tree with 2^{256} leaves, where every leaf is a zero value. Because every element at the second level of the tree is the same (z2 = hash(0, 0)), and every element at the third level is the same (z3 = hash(z2, z2)) and so forth this can be trivially computed in 256 hashes. From there, we can add or remove values by modifying values in place in the sparse Merkle tree, eg. to add the value 42 at position 3, we modify the second value the second level to v2 = hash(0, 42), the first value at the third level to v3 = hash(0, v2), the first value at the fourth level to v2 = hash(v3, z3) (since at this point, the left subtree represents keys 0…3 and the right subtree represents keys 4…7 which are still all empty), and so forth up to the top.

We don’t need to store any level in a literal array; we can simply store a hash map of parent \rightarrow (leftchild, rightchild), and in general the map will grow by at most 256 elements for each item we add into the tree. Adding, updating or removing any element takes 256 steps, and a Merkle proof of an element takes 256 hashes, if done naively.

Sparse Merkle trees are conceptually elegant in their extreme simplicity; from a mathematical perspective, they really are just Merkle trees. In simplest form, the `get` function is literally ten lines of code:

```python
def get(db, root, key):
    v = root
    path = key_to_path(key)
    for i in range(256):
        if (path >> 255) & 1:
            v = db.get(v)[32:]
        else:
            v = db.get(v)[:32]
        path <<= 1
    return v
```

But they are seemingly less efficient: for a tree with N non-empty elements, a more specialized key/value tree, eg. a Patricia tree or Merklix tree or AVL tree, requires log(N) operations to read or write a value, and a Merkle branch has length \approx 32 * log_2(N) optimally, whereas in a sparse Merkle tree, it seems like we require 256 operations to read or write, and a Merkle branch has length 32 * 256 = 8192 bytes.

However, **these inefficiencies are largely illusory**; it turns out that it is possible to optimize away most of the inefficiencies by building more complex client-side algorithms on top of sparse Merkle trees. First, we can cut down the Merkle branch size to 32 + 32 * log_2(N) (actually lower overhead than my [earlier implementation of a binary Patricia tree](https://github.com/ethereum/research/tree/master/trie_research/bintrie1)), by using a simple trick. If a sparse Merkle tree has N nonzero nodes, then once the branch goes deeper than log(N) levels into the tree, it is likely that there is only one nonzero node in the remaining subtree. At this point, every time you go one level further down, the subtree that does not contain the node will be the zero subtree for that given level. Since there are only 256 possible values for a zero subtree, we can calculate and store these once, and simply omit them from the proof. We can prepend 32 bytes to the proof to show the client at what indices we omitted a zero subtree value. Here’s the algorithm:

```python
def compress_proof(proof):
    bits = bytearray(32)
    oproof = b''
    for i, p in enumerate(proof):
        if p == zerohashes[i+1]:
            bits[i // 8] ^= 1 << i % 8
        else:
            oproof += p
    return bytes(bits) + oproof

def decompress_proof(oproof):
    proof = []
    bits = bytearray(oproof[:32])
    pos = 32
    for i in range(256):
        if bits[i // 8] & (1 << (i % 8)):
            proof.append(zerohashes[i+1])
        else:
            proof.append(oproof[pos: pos + 32])
            pos += 32
    return proof
```

But we can go further. Although we will not be able to reduce the number of *hashes* required to update a value to less than 256, we can reduce the number of *disk reads* required to log_2(N), or even log_{16}(N) (ie. same as the current Patricia tree). The algorithm is to simply change the way that we store Patricia tree nodes, in some cases grouping multiple nodes together in a DB entry. If there is a subtree with only one element, we can simply store a record saying what the value is, what the key is, and what the hash is (to avoid having to recompute it). I do this in this sample implementation:

https://github.com/ethereum/research/blob/master/trie_research/bintrie2/new_bintrie_optimized.py

Notice that this ends up looking somewhat similar to an implementation of a Patricia tree, except the Patricia-tree-like structure exists only at the database level, not at the hash computation level, where it is still a sparse Merkle tree. The same keys and values put into the tree will still give the same hash.

And here is an implementation that pretends that the binary tree is a hexary tree, using H(H(H(H(i0, i1), H(i2, i3)), H(H(i4, i5), H(i6, i7))), H(H(H(i8, i9), H(i10, i11)), H(H(i12, i13), H(i14, i15)))) as the hash function. This once again does not affect hash computation, so the same keys and values put into the tree will continue to give the same hash, but it reduces the number of database reads/writes required by a factor of ~3-4 relative to the previous binary tree implementation.

https://github.com/ethereum/research/blob/master/trie_research/bintrie2/new_bintrie_hex.py

The decoupling between hash computation format and database storage format allows different clients to have different implementations, making it much easier to optimize implementations over time.

## Replies

**gakonst** (2018-10-10):

I believe the compression part of your proposal is same thing that’s been proposed in [Plasma Cash with Sparse Merkle Trees, Bloom filters, and Probabilistic Transfers](https://ethresear.ch/t/plasma-cash-with-sparse-merkle-trees-bloom-filters-and-probabilistic-transfers/2006).

We’ve had this implemented for a while in multiple languages:

- https://github.com/loomnetwork/plasma-cash/blob/master/server/contracts/Core/SparseMerkleTree.sol (credits to the Wolk team for this initial impl)
- https://github.com/loomnetwork/plasma-cash/blob/master/server/test/SparseMerkleTree.js
- https://github.com/loomnetwork/mamamerkle/blob/master/sparse_merkle_tree.go
- https://github.com/loomnetwork/plasma-cash/blob/b10cc02c9316506d66329b05a1c2e3112a32e3fb/plasma_cash/utils/merkle/sparse_merkle_tree.py

Does the further design you describe require changing the on-chain verifier?

---

**vbuterin** (2018-10-10):

> Does the further design you describe require changing the on-chain verifier?

No. The consensus rules are 100% the same, the hashes are 100% the same, the proofs are 100% the same, it’s a purely voluntary client-side change that different clients can implement differently. This is precisely why this is interesting.

---

**sourabhniyogi** (2018-10-12):

[@vbuterin](/u/vbuterin) How would you approach a “EphemDB STARK proof” now?  That is, if `get(k)`, `put(k,v)`, `delete(k)` are transactions in a “Ephem” blockchain (just as you have it in `EphemDB`… and nothing more) where each block has an evolving SMT root representing k-v pairs , what raw computational trace should the STARK prover generate that we can put through recursive FRI and have fast STARK verification?

Should it involve registers that reference nibble traversals and/or database lookups on those nibbles?   Is the appropriate STARK proof included in this Minimal EphemDB blockchain to really start from the genesis block with an empty SMT root, or the previous block?

---

**vbuterin** (2018-10-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/sourabhniyogi/48/808_2.png) sourabhniyogi:

> @vbuterin How would you approach a “EphemDB STARK proof” now? That is, if get(k) , put(k,v) , delete(k) are transactions in a “Ephem” blockchain (just as you have it in EphemDB … and nothing more) where each block has an evolving SMT root representing k-v pairs , what raw computational trace should the STARK prover generate that we can put through recursive FRI and have fast STARK verification?

This is just a different client-side implementation of SMTs. You can also add client-side code that generates the Merkle proofs for any specific key/value, and these Merkle proofs would look exactly the same as they would if produced by a “naive” implementation of the SMT. So from a SNARK/STARK perspective, there is no difference from using an SMT naively.

---

**jbaylina** (2018-10-14):

In IDEN3 we are using exactly those trees and the optimisation you mention plus an extra one that we see very convenient especially when checking merkle proofs onchain.  That is: we force the root of any empty tree or any empty subtree to be zero.  That is z1 = z2 = z3 =  … zN = 0.

The format for merkle proofs that we are using is:

1.- One first word that is a bitmap of the siblings that are not zero.

2.- The non zero sibblings sorted bottom-up.

This has the advantage:

1.- Not having to initialize the lists with zN.  The root of an empty list is zero, the default EVM value.

2.- Not having to worry of zX values. This saves SLOAD and SSTOREs a lot, and the onChain merkle proof is much cheaper.

3.- The implementation code is much more clean.  You don’t have to handle z values.

---

**vbuterin** (2018-10-15):

Agree that setting H(0, 0) = 0 is an optimization!

Another thing I am thinking about is, is there an ultra-simple hack that can allow us to avoid having to do a hash call for H(x, 0) or H(0, x) as well? Unfortunately it seems like you can’t do it at least with the same domain (32 byte values) as the hash function, because if the function is invertible, then defining H^{-1}_{0L}(x) such that H_{0L}^{-1}(x) = y implies H(0, y) = x (and similarly for H_{0R}^{-1} for the 0 in the right position), then given any a = H(b, c), a = H(0, H_{0L}^{-1}(a)) = H(H_{0R}^{-1}(a), 0).

If there isn’t I don’t think that’s a big deal; hash functions are quite cheap and fast these days, so doing 256 hashes instead of 32 isn’t too big a deal, especially since it’s only needed for writes and not reads (and for multi-branch updates the work is parallelizable!), but something really clean and simple would be nice.

---

**ldct** (2018-10-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> First, we can cut down the Merkle branch size to 32 + 32 * \log_2(N) (actually lower overhead than my earlier implementation of a binary Patricia tree ), by using a simple trick. If a sparse Merkle tree has N nonzero nodes, then once the branch goes deeper than log(N) levels into the tree, it is likely that there is only one nonzero node in the remaining subtree.

Can’t you replace subtrees which only contain one element by the element itself? You don’t get the exact same root hash as the equivalent SMT but it seems like you can still do correct inclusion and exclusion proofs into this tree.

---

**vbuterin** (2018-10-15):

Yes, this is exactly what [@jbaylina](/u/jbaylina) suggested above.

---

**ldct** (2018-10-15):

Is it equivalent? Suppose the tree contains one element x; my suggestion is for the root to be H(x) but if H(0,0) = 0 is the only constraint then it seems like the root is H(0, something) or H(something, 0), which is necessarily different from H(x).

---

**vbuterin** (2018-10-15):

But then that doesn’t distinguish between x existing at different positions…

---

**ldct** (2018-10-16):

I was speaking in terms of an SMT that commits to unordered sets, in which case it never makes sense to place the same value at different paths. Here is one way to do it for a key-value mapping.

Let the key-value map be \{(k_i, v_i) | i \in I\} where and i \ne j \implies k_i \ne k_j). Let H be keccak-256. Create a complete binary merkle tree of depth 256 and store (k_i, v_i) at the H(k_i)-th leaf from the left. Replace each subtree which contains exactly one non-empty leaf with the leaf itself. This results in a binary tree that is not complete. Replace empty leaf with 0 and each non-empty leaf x with (1, x). Replace every non-leaf node by the hash of its two children, forming a merkle tree.

An inclusion proof that k maps to v is a merkle inclusion proof of (1, k, v), whose path is some prefix of H(k), i.e., an integer t \le 256, a path p \in \{0,1\}^{t} and t intermediate nodes of type `bytes32`; the checker verifies this proof by starting with the value (1, k, v) hashing with the provided intermediate nodes either on the left or right as directed by p, and comparing it to the root. An exclusion proof is either a merkle inclusion proof of 0 or an inclusion proof of (1, k', v') whose path is some prefix of k and where k' \ne k.

---

**paouvrard** (2018-10-21):

Hi everyone,

I’d like to share 2 implementations that I hope you might find useful as they seem similar to ideas expressed above : a standard SMT and a modified SMT of height log(N)

https://github.com/aergoio/SMT

This is a standard binary SMT implementation of height 256 with the following characteristics :

- Node batching (1 db transaction loads 30 nodes : ie a subtree of height 4 with 16 leaves). Batch nodes are loaded into an array and can be concurrently updated.
- Reduced data storage (if a subtree contains only 1 key then the branch is not stored and the root points to the KV pair directly
- Parallel update of multiple sorted keys

https://github.com/aergoio/aergo/tree/master/pkg/trie

This implementation modifies the SMT in the following way : the value of a key is not stored at height 0 but instead at the highest subtree containing only that key.  The leaf node of keys is [key, value, height].

The benefit here is that the tree height is log(N) and updating a key requires log(N) hashing operations (256 hashing operations becomes too slow if the tree is used to update thousands of keys/sec).

It also has node batching and parallel updates like the standard SMT implementation.

The size of a proof of inclusion and non-inclusion is log(N).

A proof of non-inclusion can be of 2 types :

- A proof that another key’s leaf node is already on the path of the non-included key
- Or a proof that an empty subtree is on the path of the non-included key

Optimization to come : using H(0,0) = 0

---

**vbuterin** (2018-10-21):

I actually think that this is equivalent to a simple sparse Merkle tree using the following hash function:

H(0, 0) = 0

H(0, (k,  v)) = (k+``1", v)

H((k,  v), 0) = (k+``0", v)

H(x \ne 0, y \ne 0) = sha3(x, y)

When putting values into the tree, a value v is replaced by (``", v). This hash function is collision-resistant, which you can prove piecewise and then finish by showing domain independence (cases 2 and 3 clearly cannot collide with each other, cases 2/3 cannot collide with case 4  because they give outputs longer than 32 bytes,and case 1 cannot collide with anything because cases 2 and 3 can’t give a 0 because by preimage resistance finding a value that hashes to 0 is infeasible.

The only argument I have against it is that it’s somewhat uglier, because the values aren’t cleanly 32 bytes anymore, instead they go up to 64 bytes, and because we need to deal with encodings for arbitrary-bit-length strings. I guess it depends on just how expensive hashes are.

---

**paouvrard** (2018-10-23):

Agreed, although the update algorithm is different because when adding a key in the aergo trie implementation if an empty subtree is reached, a **Leaf** = Hash(**key**,**value**,height) is created and there is no need to iterate the branch.

**key** and **value** are stored in place of the imaginary left and right subtree roots of the **Leaf** node for easy serialization

The readme has diagrams ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2018-10-23):

Is it different? The result of iterating the branch is simple, it’s just (binarystring(key), value). So I suppose you just get an additional shortcut over doing ~256-log(N) loops.

---

**updogliu** (2019-01-02):

Would this tweaked hashing still fit for non-membership proving?

---

**vbuterin** (2019-01-02):

Yep! Don’t see why not.

---

**lovesh** (2019-06-19):

[@vbuterin](/u/vbuterin)  I understand that this would allow for the mekle proof to be of variable number of nodes.

So if i use a Bulletproofs circuit to prove knowledge of a leaf in the tree, the proof size can give an approximate idea of where the leaf can be in tree. Am i wrong on this?

---

**vbuterin** (2019-06-20):

Actually this makes it so that you can have a Merkle proof always have the exact same number of nodes (256), using compression at a higher layer to bring the scheme back to O(log(N)) efficiency.

---

**lovesh** (2019-06-20):

[@vbuterin](/u/vbuterin) I think you are referring to using `compress_proof` and `decompress_proof` on a naive sparse merkle tree. I was referring to implementations in new_bintrie_optimized.py and new_bintrie_hex.py.


*(9 more replies not shown)*
