---
source: ethresearch
topic_id: 5633
title: Sparse merkle trees with Bulletproofs
author: lovesh
date: "2019-06-19"
category: Cryptography
tags: [sparse-merkle-tree]
url: https://ethresear.ch/t/sparse-merkle-trees-with-bulletproofs/5633
views: 2354
likes: 4
posts_count: 4
---

# Sparse merkle trees with Bulletproofs

This is a request for review of sparse merkle tree membership check using using [dalek’s Bulleptoofs implementation](https://github.com/dalek-cryptography/bulletproofs).  There are some working tests.

I have 2 variations of the naive sparse mekle tree as described [here](https://ethresear.ch/t/optimizing-sparse-merkle-trees/3751), binary and 4-ary.

Implementation of the [naive binary sparse merkle tree](https://github.com/lovesh/bulletproofs-r1cs-gadgets/blob/ef3f991f619b12213338dd3534454550e0deee26/src/gadget_vsmt_2.rs#L36) and its [constraints](https://github.com/lovesh/bulletproofs-r1cs-gadgets/blob/ef3f991f619b12213338dd3534454550e0deee26/src/gadget_vsmt_2.rs#L171).

Implementation of the [naive 4-ary sparse merkle tree](https://github.com/lovesh/bulletproofs-r1cs-gadgets/blob/ef3f991f619b12213338dd3534454550e0deee26/src/gadget_vsmt_4.rs#L40) and its [constraints](https://github.com/lovesh/bulletproofs-r1cs-gadgets/blob/ef3f991f619b12213338dd3534454550e0deee26/src/gadget_vsmt_4.rs#L199).

I am using the [Poseidon hash function](https://eprint.iacr.org/2019/458). There are 2 variations of it, one that hashes 2 inputs in a call and another hashes 4 inputs in a single call. I use the former for binary tree and latter for 4-ary tree.

I am more interested in the review of sparse merkle tree constraints.

I have an [optimized sparse merkle tree implementation](https://github.com/lovesh/bulletproofs-r1cs-gadgets/blob/ef3f991f619b12213338dd3534454550e0deee26/src/gadget_osmt.rs#L40) but in that merkle proof are of variable number of nodes hence the proof size of Bulletproofs will change which might give the verifier an idea of where the leaf is in the tree. Is there an alternate approach?

## Replies

**khovratovich** (2019-06-20):

It seems difficult to have a constant-time prover for a variable-size circuit. Probably the best we can do is to have always the worst-case proof.

---

**bharathrao** (2019-08-03):

Is there any reason why you wouldn’t use a sparse Merkle tree?

---

**lovesh** (2019-08-04):

I will use a full merkle tree (like i was already using). The merkle tree being sparse or not does not seem to add any advantage when proving knowledge of a leaf in the circuit.

