---
source: ethresearch
topic_id: 5511
title: A nearly-trivial-on-zero-inputs 32-bytes-long collision-resistant hash function
author: vbuterin
date: "2019-05-25"
category: Data Structure
tags: [sparse-merkle-tree]
url: https://ethresear.ch/t/a-nearly-trivial-on-zero-inputs-32-bytes-long-collision-resistant-hash-function/5511
views: 8022
likes: 24
posts_count: 34
---

# A nearly-trivial-on-zero-inputs 32-bytes-long collision-resistant hash function

**Problem statement**: for use cases like [Optimizing sparse Merkle trees](https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751), create a hash function H(l, r) = x where l, r and x are 32 byte values that is (i) collision-resistant and (iii) trivial to compute if l = 0 or r = 0. This ensures that sparse trees with 2^{256} virtual nodes only require log(N) “real” hashes to be computed to verify a branch or make an update to an average N-node tree, all while preserving the very simple and mathematically clean interface of a sparse Merkle tree being a simple binary tree where almost all of the leaves are zero.

### Algorithm

1. If l \ne 0 and r \ne 0, return 2^{240} + sha256(l, r)\ mod\ 2^{240} (ie. zero out the first two bytes of the hash)
2. If l = r = 0 return 0
3. If l \ge 2^{255} or r \ge 2^{255} or l < 2^{240} or r < 2^{240}, return 2^{240} + sha256(l, r)\ mod\ 2^{240}
4. Otherwise let x be the nonzero input and b be 1 if r is nonzero else 0. Return 2 * x + b

### Collision resistance argument

- If h = 0, then it can only have come from case (2) as preimage resistance of f(x) = sha256(x)\ mod\ 2^{240} implies that finding l and r that hash to zero is infeasible so cases (1) and (3) are ruled out, and case 4 is ruled out because either value being nonzero makes 2 * x + b nonzero.
- Outputs 1 \le h <2^{240} are outright impossible as none of the four cases can produce them
- Outputs 2^{240} \le h < 2^{241} can only have come from cases 1 or 3 (as for them to come from case 4, an input x \in [2^{239}, 2^{240}) would be required, which cannot happen as case 3 catches that possibility). Collision resistance of f(x) = sha256(x)\ mod\ 2^{240} implies that there is at most one discoverable solution.
- Outputs 2^{241} \le h can only have come from case 4. floor(\frac{h}{2}) identifies the only possible value for the nonzero input, and h\ mod\ 2 identifies which of the inputs was nonzero.

### Properties

At the cost of a 16-bit reduction in preimage resistance and 8-bit reduction in collision resistance, we get the property that hashing a sparse tree with one element with depth d only requires about 1 + \frac{d}{16} “real” hashes.

## Replies

**Econymous** (2019-05-27):

Would you say that the code associated with this scaling solution is 1000x(dramatically significantly) more “involved”/complicated than the code that already runs Ethereum?

I’ll be honest, I’m guessing. But it just seems like there’s a lot of elaborate techniques that seem to have weaknesses themselves and require further elaborate patching.

---

**vbuterin** (2019-05-28):

Huh? This hash function can be used to improve the performance of sparse binary Merkle trees, which can be used to replace Ethereum’s current Patricia trees but are ~5x simpler and ~4x more space-efficient. This is *complexity-reducing*.

---

**Econymous** (2019-05-28):

Okay. Yeah. This is way over my head. I thought this was part of the scaling solution. I should have asked in a more general setting.

---

**TheCookieLab** (2019-05-29):

It seems this is a significant improvement over the status quo. As someone lacking any background or context I’m curious if this “discovery” was a sudden *a-ha* development or if it’s just the latest step in a long cycle of evolutionary iterations?

Are there a bunch of *known* but promising data structures out there just waiting to be vetted for production readiness, or are we (you) blazing new trails in computer science as we speak?

---

**vbuterin** (2019-05-29):

It’s definitely an a-ha development. We knew how to do this for months at the cost of making the hash function 64 bytes long instead of 32, which was unacceptable as it would have doubled the lengths of the proofs, so this is a big step toward binary SMTs for storing large key-value stores being practical.

To help provide a layman’s understanding for why SMTs are better than Patricia Merkle trees (what ethereum currently uses to store state data), just look at the relative complexity of the code for the update function. Here’s SMTs:


      [github.com](https://github.com/ethereum/research/blob/ba690c0307504c78e432f1723d54c47486bdf441/sparse_merkle_tree/new_bintrie.py#L54)




####

```py

1. v = root
2. path = key_to_path(key)
3. for i in range(256):
4. if (path >> 255) & 1:
5. v = db.get(v)[32:]
6. else:
7. v = db.get(v)[:32]
8. path > 255) & 1:
17. sidenodes.append(db.get(v)[:32])
18. v = db.get(v)[32:]
19. else:
20. sidenodes.append(db.get(v)[32:])
21. v = db.get(v)[:32]

```








Yes, that 23 line function is it. Now here’s the current hexary Patricia tree:


      [github.com](https://github.com/ethereum/pyethereum/blob/9a23b0fa75fe1c82be932e207c21959eb18109f1/ethereum/trie.py#L282)




####

```py

1. return node[1] if key == curr_key else BLANK_NODE
2.
3. if node_type == NODE_TYPE_EXTENSION:
4. # traverse child nodes
5. if starts_with(key, curr_key):
6. sub_node = self._decode_to_node(node[1])
7. return self._get(sub_node, key[len(curr_key):])
8. else:
9. return BLANK_NODE
10.
11. def _update(self, node, key, value):
12. """ update item inside a node
13.
14. :param node: node in form of list, or BLANK_NODE
15. :param key: nibble list without terminator
16. .. note:: key may be []
17. :param value: value string
18. :return: new node
19.
20. if this node is changed to a new node, it's parent will take the
21. responsibility to *store* the new node storage, and delete the old

```








(Keep scrolling down! There’s lots there!)

---

**tawarien** (2019-05-29):

I tried to understand it and got stuck on the first two cases as from my understanding they do already cover the whole input space: If both are 0 case 2 is used, and if at least one input is not 0 then case 1 is used.

**Update:**

After looking a bit deeper into the cases I assume that some typos made their way into the formulas. I think the first case should have a *and* instead of a *or* in its condition. In the fourth case a *+ 2^240* is missing. Is this correct?

---

**vbuterin** (2019-06-02):

You’re right I made a mistake! In the first case, it should be “and” not “or”. Fixed now.

---

**tawarien** (2019-06-02):

To the last case (4): if the inputs come from the same hash function it is given that x is bigger then *2^240* but if I can manufacture inputs  I can create a collision between case 1 and 4 (you hinted this in your analysis):

h1 = H(l1,r1)  where l1 != 0 and r1 != 0

h2 = H(l2,r2)  where l2 = h1/2 and r2 = 0 if h1 mod 2 == 0

or

h2 = H(l2,r2)  where l2 = 0 and r2 = h1/2 if h1 mod 2 == 1 (integer division)

Because l2, r2 triggers case 4 even if the inputs are smaller then *2^240*, h1 would be equal to h2.

So it is only a collision resistant hash function if the inputs are outputs from the same hash function.

It may be a problem in Merkle trees in case of proofs where the nodes can easily be manufactured. I could for example create a proof of non membership for something that is in the tree by using the 0 side of the collision to proof that a key ends on an empty node

One easy solution against this is to always check that the inputs are bigger than *2^240* and produce an error otherwise. Another solution would be to add *+ 2^240* to case 4 results.

---

**vbuterin** (2019-06-02):

Ah yes, you’re right that if the interval [1, 2^{240}) is not excluded from the domain, then you could have some value x \in [2^{239}, 2^{240}) where H(a, b) = x*2. Added another fix, (3) is now:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> if \ ge 2^{255} or r \ge 2^{255} or l < 2^{240} or r < 2^{240}, return 2^{240} + sha256(l, r)\ mod\ 2^{240}

---

**skilesare** (2019-06-02):

This is great! Interested to see how this affects gas when proving a witness on chain. I have an old stateless coin example that I may have to run through this.

Maybe an off topic question, and I’m still trying to really understand these things, but is this a zk optimal hash?

With roll ups and lots of other zk applications coming down the road it would seem to make sense to focus on hash functions that are optimal for running in circuits. (not to discount the savings this provides…just more of a meta direction question)

---

**vbuterin** (2019-06-02):

Unfortunately this is not ZK optimal naively; the problem is that inside of ZK contexts you have to run the prover over the entire circuit; even if a specific input uses some “fast path” in the circuit, you would have to run the prover over the slow path as well. You might be able to avoid this though if you add a *public* input stating which of the hashes you’re running are fast-paths.

---

**khovratovich** (2019-06-03):

This function is not preimage resistant: preimages for almost all 256-bit values can be easily found by division by 2.

---

**tawarien** (2019-06-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> This function is not preimage resistant

A Cryptographic Hash function for a Merkle Tree does only need to be collision resistant and second-preimage resistant. preimage resistance is not a requirement.

---

**burdges** (2019-06-03):

Is there anything wrong with collisions between intermediate hashes located at different depths?  If not, then I doubt you need the bit shifting, and even so collisions sound impossible.  I’d expect an SMTs to start at a fixed depth too.

Also, there is an easy 34.5 byte version consisting of a normal 32 byte hash, a 2 byte “history”, and half a byte depth for the history.  I believe this version works with a Pedersen hash too, making it compatible with SNARKs.

---

**khovratovich** (2019-06-03):

If a function is not a preimage resistant, it is not a cryptographic hash function anymore.

Anyway, preimage resistance was claimed in the original post.

---

**khovratovich** (2019-06-03):

For a tree with just one non zero entry ‘x’ the output is just ‘(x<<16) +position’ for certain x.

One can do better by just having ‘y=H(pos||treesize||x)’.

---

**tawarien** (2019-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/khovratovich/48/2531_2.png) khovratovich:

> Anyway, preimage resistance was claimed in the original post.

Your right, the last sentence claims that, I missed that some how, the propsed algorithm can only claim second-preimage resistance and not preimage resistance.

But I realized that the loss of preimage resistance is actually an advantage in the proposed use case as tree nodes that trigger case 4 do not have to be stored in the database we can easely detect if a hash was generated by case 4 (h > 2^241) and if so get the input by calculating the preimage instead of looking it up in the key-value store

---

**vbuterin** (2019-06-04):

I asked [@EliBenSasson](/u/elibensasson) and his impression was that it should be possible to get the efficiency savings inside a ZK-SNARK if you publicly reveal which hashes are fast paths (a totally reasonable thing to do for the block Merkle tree use case).

---

**dlubarov** (2019-06-06):

Would that involve a separate circuit for each slow path depth? With a single circuit it seems like we would need to support the worst case of 256 slow hashes (unless it’s recursive).

---

**musalbas** (2019-06-20):

The [Libra whitepaper](https://developers.libra.org/docs/assets/papers/the-libra-blockchain.pdf) released yesterday also suggests a strategy for preventing the need to compute 256 hashes per Merkle proof in a sparse Merkle tree. Basically, subtrees consisting of exactly one leaf are replaced with a single node.

[![image](https://ethresear.ch/uploads/default/original/2X/2/2d81f265f235526bcbf9fe24be15c417a68ef566.png)image273×115 4.19 KB](https://ethresear.ch/uploads/default/2d81f265f235526bcbf9fe24be15c417a68ef566)

This does arguably does increase the complexity of the sparse Merkle tree interface; their [implementation](https://github.com/libra/libra/blob/5ec3f69bae1a15f4ccc67fcdce8d0441b47e2539/storage/scratchpad/src/sparse_merkle/mod.rs) is 460 lines of code.


*(13 more replies not shown)*
