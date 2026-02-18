---
source: ethresearch
topic_id: 5040
title: WASM compatible Miximus in Rust
author: drstone
date: "2019-02-22"
category: Applications
tags: []
url: https://ethresear.ch/t/wasm-compatible-miximus-in-rust/5040
views: 1777
likes: 2
posts_count: 6
---

# WASM compatible Miximus in Rust

[Rust-miximus](https://github.com/drewstone/rust-miximus)

I built an MVP version of [Miximus](https://github.com/barryWhiteHat/miximus) in Rust using bellman and tools from Matter Labs. Happy to share it with the community as a means of providing more implementations of applications and circuits in Rust.

In particular this exposes WASM functions that can be used to interact with the zkSNARK though I have not written this part of the application and will most likely will not. Happy to discuss for anyone interested though! This was largely inspired by work done by Kobi Gurk at Qedit in this [repo](https://github.com/kobigurk/wasm_proof/) and of course [@barryWhiteHat](/u/barrywhitehat).

One thing that is particularly questionable that I am unsure of is using this utility to do proofs of membership in an incremental merkle tree. Since generating the zkSNARK proof parameters requires knowing the depth of the merkle tree/length of the authentication proof, when this updates is it any risk to continuously regenerate the parameters over new depths? Assuming we have access to tamperproof randomness, I presume not but I’m curious to hear thoughts if anyone has some to share. It certainly makes the case for using sparse merkle trees so that parameter generation only needs to happen once, over a depth 32 SMT.

## Replies

**barryWhiteHat** (2019-02-26):

> One thing that is particularly questionable that I am unsure of is using this utility to do proofs of membership in an incremental merkle tree. Since generating the zkSNARK proof parameters requires knowing the depth of the merkle tree/length of the authentication proof, when this updates is it any risk to continuously regenerate the parameters over new depths? Assuming we have access to tamperproof randomness, I presume not but I’m curious to hear thoughts if anyone has some to share. It certainly makes the case for using sparse merkle trees so that parameter generation only needs to happen once, over a depth 32 SMT.

So the way i solved this problem is letting people withdraw from an older state. And then we use nullifiers to prevent double withdraws which works fine. Is that what you were asking?

---

**drstone** (2019-02-26):

I understand allowing one to make proofs over past states but that is not my concern.

In bellman for example, one has to generate enough powers of tau for a given circtui (as someone mentioned to me). This requires generating parameters over a dummy circuit that still has the *SAME* number of computation i.e. the same depth as the tree you’re proving things over because you pass these parameters into the proof and the verify functions.

To that extent, if you are incrementally building a merkle tree, one would need to continuously regenerate the parameters over trees of a target depth. My question/confusion stems from not knowing if this poses an attack vector in any way since it reduces to having to generate verifiable randomness multiple times along the way. One way around this of course is to use a sparse merkle tree which has at the onset a fixed depth. This way parameters only need to be generated once.

---

**barryWhiteHat** (2019-02-26):

We always use merkle trees of fixed depth. When you do the trusted setup you have to have a circuit that is not changeable. You can do things like if loops but you end up encoding both branches of the if loop in the circuit.

---

**drstone** (2019-02-26):

Ok so I am wrong to think that incrementally building a merkle tree means increasing its depth incrementally as well. The only thing that happens realistically is a recomputation of the root as nodes are added. What separates what you built from a sparse merkle tree or is it that?

---

**barryWhiteHat** (2019-02-26):

It is that. You treat the merkle tree as if its 32 layers all the time.

Lets say that you have a 32 layer merkle tree inside the snark. And you want to do a single deposit.

1. hash(x, hash(0))
2. hash(1 ,  hash(hash(0))))
…
3. hash(hash31 , hash(hash(hash…hash(0)))))…))

You can see this in code https://github.com/barryWhiteHat/miximus/blob/e774ef8524ba947285c671b946ce56f64b48c116/contracts/MerkelTree.sol#L83

Plus a little extra compleixity to decide weather a leaf is on the left hand side or the right hand side.

