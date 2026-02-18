---
source: ethresearch
topic_id: 7421
title: "Open problem: ideal vector commitment"
author: vbuterin
date: "2020-05-14"
category: Cryptography
tags: [polynomial-commitment, vector-commitment]
url: https://ethresear.ch/t/open-problem-ideal-vector-commitment/7421
views: 18604
likes: 20
posts_count: 28
---

# Open problem: ideal vector commitment

We’re looking for a commitment scheme to commit to a list of N values (think `N ~= 2**28`) which has the following properties:

1. The commitment should be small (fixed size or polylog)
2. The commitment should be (computationally) binding, ie. a commitment c constructed from one vector V = [v1 ... vN] should not match against any other feasibly-discoverable vectors. (We don’t care about hiding properties)
3. For any given set of positions x1 ... xk where 1 <= xi <= N, there should be an efficient (ie. quasilinear time to calculate, sublinear proof size) way to prove that the values V[x1], V[x2] … V[xn] are part of the vector committed to by c
4. There should be an efficient (ie. ideally O(k) but O(k * log^c(n) is okay too) way to compute such a proof for any x1 ... xk. Requiring O(n) or even slightly larger precomputation before you receive the coordinates is okay.
5. Given a set of updates (x1, y1) ... (xk, yk) to a vector there should be:

(i) an efficient (ie. ideally O(k), but O(k * log^c(n)) is okay too) way to update c
6. (ii) an efficient (ie. ideally O(k), but O(k * log^c(n)) is okay too) way to update any precomputed tables required to generate proofs (that’s updating the entire precomputed table needed to generate all witnesses, not updating a single witness)

Note that we have constructions that *almost* satisfy these goals:

- Merkle trees: satisfy everything but the crucial requirement (3) for a k-element proof to be sublinear in k
- Kate commitments: satisfy everything but (5. ii) efficient witness updating (witness updating is O(n * min(k, log(n))) because the value of each witness depends on every element)
- SNARK proofs over Merkle trees using MIMC/Pedersen: satisfy everything but generating a SNARK to compress many Merkle branches is ~1-2 orders of magnitude too expensive
- RSA accumulators: no efficient witness updating (5. ii)

The goal is to have a ready construction that can be used for state storage constructions, eg. [Multi-layer hashmaps for state storage](https://ethresear.ch/t/multi-layer-hashmaps-for-state-storage/7211)

### Construction based on not-yet-existent moon-math cryptography

As a proof-of-concept to show that a construction could conceivably exist, consider the case where we had high-degree graded encodings, ie. a primitive even stronger than multilinear maps, where (i) given `x` you can compute `encode(x)`, and (ii) given `encode(x)` and `encode(y)` you can compute `encode(x*y)` and (iii) you can check encodings against each other for equivalence.

Let `h` be a hash function that outputs fairly long values (sufficiently long that given `n` outputs with very high probability no output will be a factor of the product of all `n-1` other outputs). To commit to `V = [v1, v2 ... vn]`, compute `commitment = encode(h(2**256 + v1)) * encode(h(2**256 * 2 + v2)) * ... * encode(h(2**256 * n + vn))`.

To prove that set of key/value pairs `S = {(i1, v[i1]) ... (ik, v[ik])}` is inside the commitment, use the product of all `encode(h(2**256 * i + v[i]))` values *not* in `S` as a witness; the verifier would recompute the encodings of the key/value pairs in `S`, multiply them by the witness, and check that they get the same value as the original commitment.

Note that if the prover precomputes and stores a tree, containing the encodings for the subsets `{v1}, {v2} ... {vn}, {v1,v2}, {v3,v4} ... {v[n-1], vn}, {v1..v4} ... {v[n-3] ... vn} ... {v1...vn}`, then any proof for `k` elements can be constructed in `k*log(n)` time by multiplying together the appropriate sister nodes in the tree, and any single update to the vector would only require updating `log(n)` elements in this tree.

One possible path to finding a solution is taking this tree-structure-based approach, but to get to a construction feasible today one would replace multiplication with some other operation, where multiple “sister nodes” in the tree can somehow be aggregated.

## Replies

**alinush** (2020-05-14):

So, to put things in a slightly different terminology:

(1) and (2) are basic tenets of VCs: *succinctness* and *binding*.

(3) requires computing all n proofs in roughly n\log{n} time (This can be done using the [Feist-Khovratovich (FK)](https://github.com/khovratovich/Kate/blob/66aae66cd4e99db3182025c27f02e147dfa0c034/Kate_amortized.pdf) technique for KZG-based VCs).

(4) requires computing any I-subvector proof in O(|I|) time, where I=\{x_1, x_2,\dots, x_k\}. (This can be done by precomputing all witnesses via FK and then using aggregation to compute any I-subvector proof.)

(5, i) Requires the commitment be updatable in O(k) time after k updates, which is the case for KZG-based VCs.

(5, ii) Requires that the *auxiliary information* used to speed up (3) and (4) be updatable in O(k) time after k updates to the vector.

This auxiliary information could be the proofs themselves, which seems to be the case when you say: " **Kate commitments**: satisfy everything  *but*  (5. ii) efficient witness updating (witness updating is  O(n \cdot \min\{k, \log{n}\}) because the value of each witness depends on every element).

I’m assuming here you are referring to updating all n witnesses, and the \min\{k, \log{n}\} arises because you could either do O(k) work for each witness leading to O(nk) time, or recompute all n witnesses from scratch in O(n\log{n}) time, when k > \log{n}.

Indeed, doing (5, ii) with KZG is a very interesting challenge.

---

**dankrad** (2020-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> This auxiliary information could be the proofs themselves, which seems to be the case when you say: " Kate commitments : satisfy everything but (5. ii) efficient witness updating (witness updating is O(n⋅min{k,logn})O(n \cdot \min{k, \log{n}}) because the value of each witness depends on every element).

Yeah. If you don’t precompute the proofs in Kate, then you can’t satisfy 4.

---

**vbuterin** (2020-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/alinush/48/10069_2.png) alinush:

> I’m assuming here you are referring to updating all nn witnesses

Yep, exactly! And you’re quite right that (5, ii) is the sticking point. So far my main intuition for how to achieve it is to come up with auxiliary information that is in some kind of tree structure, so only the branch going down to a changed element would need to be updated (this is why Merkle trees work). But how to do this with KZG is a challenge…

---

**alinush** (2020-05-15):

Indeed. The closest thing to a tree structure for KZG proofs is [our AMT technique](https://alinush.github.io/2020/03/12/towards-scalable-vss-and-dkg.html#authenticated-multipoint-evaluation-trees-amts), which computes all n **log-sized** proofs in O(n\log{n}) time (for a degree n-1 polynomial).

Unfortunately, AMT proofs are not aggregatable, which means subvector proofs have to be computed from scratch in O(n\log{n}) time. They are also much larger than ideal.

One way to make them aggregatable (and also solve the “efficient proof update” problem) is to figure out if a log-sized AMT proof can be somehow compressed into a constant-sized KZG proof.

---

**Pratyush** (2020-05-15):

What about a Merkle tree where each node is a KZG-style accumulator?  You can use this to greatly increase the arity of the tree, thus reducing depth. To get scaling that’s sublinear in k, you can use a SNARK cheaply.

---

**ben-a-fisch** (2020-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> RSA accumulators : no efficient witness updating (5. ii

In the vector commitment based on RSA accumulators with batching, witnesses can be updated efficiently. The opening of an element of the vector is a combination of a batched RSA membership witness and a batched non-membership witness. Both can be updated in time independent of N. Updating the commitment value requires deletes from the accumulator, which cannot be done efficiently in general. However, it can be done efficiently if all the updates also include the witnesses for the current values in the VC. One other detail is that the batched non-membership witness (compressed proof) cannot be updated directly, updating requires the individual non-membership witnesses for each of the zero-bits of the element.  Non-membership updates are described in https://www.cs.purdue.edu/homes/ninghui/papers/accumulator_acns07.pdf.

That said, the scheme based on RSA accumulators does have high concrete overhead, so you may be looking for something more efficient.

---

**dankrad** (2020-05-15):

OK, I think we need to clarify on this point 5.ii: The cost per witness is of course small in both Kate and RSA accumulators. However, if you want to satisfy point 4, then you need to precompute all the witnesses (for all n points); Updating this full set of witnesses take O(n) or longer, this is the problem.

---

**denett** (2020-05-19):

I think we can do better with RSA accumulators than O(n) in the case that we do not need the full set of witnesses after every update, but only a small subset of the witnesses. I guess a lot of applications fall in this category.

The trick is to split the values in \sqrt{n} groups and calculate a base witness per group. This is the part that all witnesses in the group have in common.  For every update we only need to update these O(\sqrt{n}) base witnesses. To generate a witness for a set of values from a single group we need O(\sqrt{n}) time, because we can use the base witness as a starting point.

---

**secparam** (2020-05-19):

[@vbuterin](/u/vbuterin) I think we are missing a pretty fundamental requirement:  I shouldn’t need linear  O(K) data to update my witness or someone else should be able to calculate all such updates in less than O(k^2) time and give me the witness.

Otherwise, it seems if we scale Eth2 to say, all of Amazon EC2, then for me to update my toy ERC20 contract, I’d need to go through all of O(K) updates that happened on the entirety of EC2.  Thats way too much data for my client to handle. In fact thats too much for most end users in Eth1 today. We’ve created validators that don’t need to store blocks, but at the cost of making end users see and process every block.

As far as I know, Merkle trees are the only thing that stops this, requiring roughly log(k) data to update a witness. This seems to scale well. But they fail requirement 3).

Is 3) a necessary requirement? For account based payments, Alice should be able to payBob (i.e. update his account) while only knowing the witness to her account and her balance. Merkle tree’s fail this requirement. But for a smart contract call from contract A to B,  we need to know the state of B to execute the contract. So why do we care ?

---

**vbuterin** (2020-05-19):

I think that’s covered by the other requirements; you can just ping one of the nodes that has the “auxiliary information” (which by the other requirements is required to be efficiently updateable) and ask it for an updated proof. But yeah, the ability to maintain a smaller amount of auxiliary info to maintain a partial state and keep it updated in less time would be nice.

---

**dankrad** (2020-05-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/pratyush/48/4986_2.png) Pratyush:

> What about a Merkle tree where each node is a KZG-style accumulator? You can use this to greatly increase the arity of the tree, thus reducing depth. To get scaling that’s sublinear in k, you can use a SNARK cheaply.

I actually think this should be taken seriously: The proof size for this “KZG verkle tree” construction is not sublinear, but still way smaller than for Merkle trees. All the KZG proofs can actually batched together into a single one; the only thing that needs to be transmitted is the intermediat KZG commitments that these need to be checked against. Proof size is therefore something like \log_k n - 1 group elements, where r is the verkle branching factor. In practice e.g. r=2^{16} and n=2^{30}, so we realistically only need one additional group element per proven position. That’s about 20x better than Merkle trees!

In terms of updating witnesses, an update does not touch all the commitments, so for each update only k \log_r n have to be updated. So using the KZG precomputation/updating techniques from [this paper](https://eprint.iacr.org/2020/527) would allow efficient proofs and updates as per 5.(ii)

Even though they don’t fulfill all the criteria, I actually now feel that verkle trees are better than what we have considered so far. In addition, they provide another elegant construction for key-value stores in the form of “verkle tries”.

Thanks to [@Pratyush](/u/pratyush) for pointing out these properties on the twitter thread!

[Edit: I noticed I was using k to describe two different values. I now changed it so that k is the same as previously (number of reveals), and r is the verkle branching factor]

---

**vbuterin** (2020-05-22):

What do you mean by “verkle branching factor” here? The number of KZG commitments? The branching factor of the top-level Merkle tree? I’m confused as to how such a small proof at the top is possible; seems to me like if there 2^{30} elements in 2^{16} trees, then the tree proof for k accounts would still be of size k * (16 - log(k)).

---

**dankrad** (2020-05-22):

Sorry I think I might have confused this by using k to mean two different things – corrected above.

The proof for k accounts would be

1. The KZG commitments of all the intermediate layers to be proven – that’s k (\log_r(n) - 1) group elements
2. One single proof that all elements and intermediate commitments were decomitted correctly – this can be aggregated into a single KZG proof, so another group element.

---

**vbuterin** (2020-05-22):

I’m still confused by (1). Is there a Merkle tree at the top, or something else? If it’s a Merkle tree, where are the hashes? Or is it just a commitment to a set of values each of which are themselves commitments?

---

**dankrad** (2020-05-22):

The whole thing is an r-ary Merkle tree, but instead of a hash if its children, each node is a KZG commitment of its children.

---

**vbuterin** (2020-05-22):

Ah, I see. So it functions like a Merkle tree, except instead of proofs having length (r-1) * log_r(n) it’s just log_r(n). Got it. Witness update costs *would* be on the order of r * log_r(n) though, correct?

---

**dankrad** (2020-05-22):

Yes, that’s correct. But that’s already much less than O(n) for full KZG.

---

**robin7** (2020-05-30):

If `n ~= 2**28` then maybe we can encode a compact vector commitment using prime number indices and an RSA accumulator.

Suppose there’s a function `p(k)` returning the k-th prime for k<2^{32} (e.g. the [Meissel Lehmer Algorithm](https://en.wikipedia.org/wiki/Meissel%E2%80%93Lehmer_algorithm)). Then we can encode a pair `(key, value)` into a single prime number:

`pair = p( key * p(value + 2**28) )`.

(This assumes the value is also in the ballpark \text{value} < 2^{28}).

We can update an accumulator as usually: `A1 = A0^t` where `t = pair_1 * pair_2 * pair_3 * ... `. Difference is that now the pairs are about 4 bytes instead of the 32 bytes when using the conventional approach of hashing into primes. That makes updating witnesses 8 times more efficient. The scheme also becomes more simple than regular RSA VC.

Further techniques regarding batching and efficient witness updates have been mentioned here by [@ben-a-fisch](/u/ben-a-fisch) .

---

**vbuterin** (2020-05-30):

How fast are the witness update techniques? Is there a way to adjust the construction so that you can update *all* the data needed to compute *any* witness after one update in log(n) time?

---

**denett** (2020-05-31):

I do not understand how the pairing works. If both key and value are 28 bits, then key * p(value + 2^{28}) will be larger than 2^{32} so you can not apply the p-function on it again.


*(7 more replies not shown)*
