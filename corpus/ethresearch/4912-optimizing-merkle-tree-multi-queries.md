---
source: ethresearch
topic_id: 4912
title: Optimizing Merkle tree multi-queries
author: Recmo
date: "2019-01-29"
category: Data Structure
tags: [data-structure]
url: https://ethresear.ch/t/optimizing-merkle-tree-multi-queries/4912
views: 6361
likes: 13
posts_count: 10
---

# Optimizing Merkle tree multi-queries

Consider a Merkle tree of depth n where we want to proof m leaf values. The naive solution requires m \times n hashes and m \times n values. We can do better:

Motivating example: Consider two sibbling leafs. In the first step, we hash them together. In subsequent steps we hash this value back to the root. We need n hashes and n-1 values instead of 2n.

In general, all leafs will eventually merge. Where they merge we have left and right branch already available and don’t need a value. From that point on, we only need a single Merkle path to the root saving values and hashes corresponding to the depth.

The actual number of hashes required depends on where the queried indices are. In general the closer together they are, the better.

Reference implementation of optimal Merkle de-commitments in Python and Solidity is here: https://gist.github.com/Recmo/0dbbaa26c051bea517cd3a8f1de3560a

Credits for the idea and algorithm go to Starkware!

## Replies

**ZacMitton** (2019-02-11):

I’ve been working on merkle-patricia-tree proofs for a while, and I have found that the correct *data format* for a proof, is actually a merkle-patricia-tree itself. This tree can be built by batching all the node values of the proof into the underlying db at their keccak as key. The ones that you describe above will simply be duplicates and not be rewritten. Now, the *verification* takes place by simply using this tree that you built, *as if it were the real merkle-patricia-tree*. You can do *any* operations on it that you would normally do to the main one. The only subtlety, is that `iff` at any point during traversal of said tree, it tries to “step in” to a hash value that it cant find in the underlying db, this means the proof is missing pieces and is invalid.

This will correctly even handle `null` leaves. When performing `get()` on a value that is null, it will find its target node index (of the 17) that contains an empty byte array. This means the key corresponded to null. You can still even do `put`, because you will again arrive at an empty byte array and knowing that anything the rest of the way down said path was not initialized,  can put the extension node to the new value and then hash each node back to the root as usual.

Anyway. just my thoughts. It’s pretty cool, we can pretty easily replay and succinctly prove entire blockchain transitions. Planning to make a PR to the js tree module for this.

---

**vbuterin** (2019-02-14):

I think I accidentally re-invented this two days ago without seeing this thread ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=9)


      [github.com](https://github.com/ethereum/research/blob/7db6b87cf8642a8671dd9890909586912a0929c9/mimc_stark/merkle_tree.py#L37)




####

```py

1. for p in proof[1:]:
2. if index % 2:
3. v = blake(p + v)
4. else:
5. v = blake(v + p)
6. index //= 2
7. assert v == root
8. return int.from_bytes(proof[0], 'big') if output_as_int else proof[0]
9.
10. # Make a compressed proof for multiple indices
11. def mk_multi_branch(tree, indices):
12. # Branches we are outputting
13. output = []
14. # Elements in the tree we can get from the branches themselves
15. calculable_indices = {}
16. for i in indices:
17. new_branch = mk_branch(tree, i)
18. index = len(tree) // 2 + i
19. calculable_indices[index] = True
20. for j in range(1, len(new_branch)):
21. calculable_indices[index ^ 1] = True

```








Your version does seem to have more compact code, though some of my version’s complexity has to do with making the proof generation algorithm not technically take O(N) time (the ` for i in range(2**depth - 1, 0, -1):` loop and the space complexity of the `known` array).

This reduced the size of the MIMC STARK from ~210kb to ~170kb and removed the need for the ugly wrapper compression algorithm.

Also a possibly dumb question:

```python
        # The merkle root has tree index 1
        if index == 1:
return hash == root
```

Doesn’t this make the verification return true if the *first* branch is correct, regardless of whether or not subsequent branches are correct? Or is it guaranteed that the “merging” via ` queue = queue[1:]` will bring the checking down to one node by the time it hits the leaf?

---

**vbuterin** (2019-02-14):

> I’ve been working on merkle-patricia-tree proofs for a while, and I have found that the correct data format for a proof, is actually a merkle-patricia-tree itself

The problem with this approach is that it’s not optimally efficient, because there is redundancy between h(child) being part of a parent node and the child itself. You *could* use a custom compression algorithm to detect this and remove most of the inefficiency, and I actually implemented this a couple of years back, though it does make the proofs substantially more complicated.

---

**tawarien** (2019-02-14):

I have made an implementation for compact multi merkle proofs as well. it has Optimal proof size as well (No duplicated nodes and no unused nodes) . In addition it has optimal verification time & memory usage (in respect to hashes computed & stored).

https://github.com/tawaren/MultiMerkleTreeProofs

It is just a proof of concept in Rust that transforms a vector of (leaf_index, authentication_path) into a compressed proof and then allows to calculate the root hash from a compressed proof. Also the constant overhead of the proof is minimal: It is 2 Words (to store two array lengths), theoretically it could be reduced to one Word (but that would make it more complex and is not worth it). It uses a lot of bit manipulating to find out which nodes have to be stored where in which order.

If someone is interested in how it works i plan to add a Readme to the repo in the next days.

---

**ZacMitton** (2019-02-14):

> h(child) being part of a parent node and child itself

Yes, but I was only suggesting the abstraction to use, not the serialization format.

Serialization could be very simple: It should be all the treenode’s *values* in an array rlp encoded. The order does not mater *exept* that the root node should be at index[0].

Then the consuming code would build a tree by looping through it and generating the keys as hashes of each item. Set the root and you’re done. i.e:

```auto
  Tree.fromProof(proofString, cb){
    let proofNodes = rlp.decode(proofString)
    let proofTrie = new Trie()

    proofNodes.each((node)=>{
      proofTrie.db.put(keccak(node), node)
    })
    proofTrie.root = proofNodes[0] || keccak()
  }
```

As for discussion of *optimal verification* time. Oddly enough this step can be completely eliminated, because the resulting tree should just be used to lookup keys by the consuming app only as needed/when necessary. It may never even use all the values. If the proof is invalid/insufficient for any specific key, its *lookup* attempt will return a “Missing proof node” error.

---

**tawarien** (2019-02-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/zacmitton/48/3197_2.png) ZacMitton:

> As for discussion of optimal verification time. Oddly enough this step can be completely eliminated, because the resulting tree should just be used to lookup keys by the consuming app only as needed/when necessary. It may never even use all the values. If the proof is invalid/insufficient for any specific key, its lookup attempt will return a “Missing proof node” error.

I do not see how this helps, as soon as a single value is needed the root hash is needed meaning all the nodes in the proof are needed to calculate it (if that is not the case then the proof had more then the minimal required amounts of nodes in it from the beginning, which can be a worthwhile trade-off if we do not optimize for proof compactness but for some other property).

---

**ZacMitton** (2019-02-14):

[@tawarien](/u/tawarien) Conceptually we have a *prover* and a *verifier* and the *transmission* of a proof between the 2.

We want/need all of the following stages to be as efficient as possible:

P1) Generation of proof (from full tree).

P2) Serialization of proof for transmission.

3) Transmission

V4) Deserialization

V5) Verification

V6) Consumption

P1 Prover returns a stack of nodes that are “touched” while `get`ing the requested value. We can extend this to state-transitions, by recording all nodes that were touched during a state transition.

P2 Described in my last post: put the desired nodesvalues into an rlp encoded array with the root as index 0

3 Use any transmission method (you have raw bytes)

V4 Verifier uses the code I wrote above to deserialize into a consumable data-store (a mini tree)

V5 & V6 Use the existing Tree API to both verify and consume the data at the same time (looking up data in the mini tree simultaneously verifies it, because an insufficient proof will render “missing node” Error).

This abstraction is very extensible to features we haven’t even thought of yet: The verifier can add more nodes to its tree’s db easily without risk of corruption. It can also `put` data into its tree. This means the EVM will be runnable on this mini-tree. I light client can verify the state transition having only the *former* proof values, and calculate the resulting merkle-root itself. As it runs, maybe it will request proofs and add them to its tree efficiently.

---

**tawarien** (2019-02-14):

@[ZacMitton](https://ethresear.ch/u/ZacMitton)

Thanks for the detailed explanation of your approach.

P1 is pretty inefficient as not all touched nodes in a traversal need to be transmitted to reconstruct the tree root on the other side. I assumed you eliminated not required nodes because that was the premise of the first post. With your note in parantheses (from full tree), as well as the whole V6, I agree that this is applicable for blockchain state proof applications but it is not in general. For example in the merkle signature scheme the whole tree is never stored and the size of the stored part is one of the core problem (merkle tree traversal problem), this is important as it influences the private key size. I do not know about other applications like STARK but i doubt that an efficient implementation will ever materialize the whole tree.

---

**ZacMitton** (2019-02-15):

We’re probably mostly talking about 2 different things. The Ethereum 1.0 trees have 17-item “branch” nodes. Therefore the optimization of excluding certains nodes (because they can be recreated from hashes of other nodes), is mostly irrelevant (could only compress at most by 1/17). With binary trees the compression could reduce the size by up to 1/2. I’m not sure the use case you are talking about (relating to key-sizes).

