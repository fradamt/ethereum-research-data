---
source: ethresearch
topic_id: 3176
title: Cheap hash functions for zkSNARK merkle-tree proofs, which can be calculated on-chain
author: HarryR
date: "2018-09-01"
category: zk-s[nt]arks
tags: [accumulators]
url: https://ethresear.ch/t/cheap-hash-functions-for-zksnark-merkle-tree-proofs-which-can-be-calculated-on-chain/3176
views: 9659
likes: 14
posts_count: 14
---

# Cheap hash functions for zkSNARK merkle-tree proofs, which can be calculated on-chain

Recently I have been working a problem of with a difficult set of constraints, and I would welcome any input or insight into the problem.

I need to build a Merkle-tree on-chain, which later on I can prove membership of using a zkSNARK proof, this means I would be able to do a zero-knowledge proof of membership and other fun things.

The problem is: using SHA2-256 (or keccak256) is *very expensive* to prove inside a zkSNARK circuit, especially so when you need to prove 29 of them for a merkle tree path, and even moreso when you’re trying to make it run in reasonable time in WebAssembly (which is about 42x slower).

Anyway, this lead me to polynomial hash functions over GF(p), UOWHFs etc. which can be quite cheap to evaluate in EVM. e.g. the Hash127 function can compute 32 bits per loop iteration, requiring a `MODEXP` and `MULMOD` instruction each iteration (or just a `MULMOD`, is using precomputation).

However, many of the algorithms I’ve found are either ciphers or MACs which require a key, and in some cases, with the key, a collision can be found in linear time. e.g. with output f(?) = x I can find any number of inputs y where f(y) = x. This is fine if the input, say the leaf of the Merkle tree, is secured in another way, e.g. f(H(w)) = x requires you to find a collision where the input to f matches the output of another more secure function H, but chaining f together to authenticate a Merkle tree path is equivalent in security to a single f until you get to the leaf and need to find a collision between both H and f. e.g. the collision resistance is finding a specific input to the function, not a specific output.

Here are some interesting papers which discuss the topic in more detail, but they make no claims about preimage resistance or their suitability as cryptographic hash functions:

- On an almost-universal hash function family with applications to authentication and secrecy codes
- Universal and Perfect Hashing
- Strongly universal string hashing is fast
- Software-Optimized Universal Hashing and Message Authentication
- Fast Universal Hashing with Small Keys and No Preprocessing: The PolyR Construction
- COMPOSITIONS OF LINEAR FUNCTIONS AND APPLICATIONS TO HASHING
- A Fast Single-Key Two-Level Universal Hash Function

This seems to be a widely studied topic, and finding a few candidate functions with strong security guarantees which can also be computed cheaply in EVM would significantly reduce the complexity of zkSNARK circuits - making them provable on mobile devices and the web.

Potential functions:

- VSH, an Efficient and Provable Collision Resistant Hash Function / Security of VSH in the Real World
- MiMC: Efficient Encryption and Cryptographic Hashing with Minimal Multiplicative Complexity
- hash127 -  a provably secure 127-bit secret-key authenticator of an arbitrarily long message

Any ideas?

## Replies

**JustinDrake** (2018-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> in WebAssembly (which is about 42x slower)

This is an interesting metric, and points towards the limits of WASM. A 42x speed boost may be enough to justify a precompile for some basic building blocks in Ethereum 2.0.

Another side note is that in Ethereum 2.0 we want to use a STARK-friendly (and ideally SNARK-friendly) hash function at the protocol layer for things like the hash chain, Merkle trees, proofs of custody, etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> Any ideas?

I expect this question to become increasingly relevant. StarkWare (which received a large grant from the EF) is in the process of preparing a report on STARK-friendly hash functions. I suggest you look at their [STARKs paper](https://eprint.iacr.org/2018/046.pdf) for the time being which has some discussion and benchmarks. (See the Davies–Meyer hash based on the Rijndael block cipher on page 15, the tables on pages 16/17, and appendices E and F.) Eli Ben Sasson is probably the most relevant person to talk to from StarkWare.

MiMC is one of the candidates that Zcash has looked into quite some detail. See for example [this GitHub issue](https://github.com/zcash/zcash/issues/2233). Daira is leading the MiMC effort with Zcash.

Another suggestion is to contact Dmitry Khovratovich who has looked at this question quite deeply. He is an expert on hash functions generally, and SNARK/STARK-friendly hashes specifically.

---

**cdetrio** (2018-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/harryr/48/1671_2.png) HarryR:

> and even moreso when you’re trying to make it run in reasonable time in WebAssembly (which is about 42x slower).

What’s the basis for this benchmark?  is it a wasm interpreter or a wasm JIT engine?

---

**HarryR** (2018-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> What’s the basis for this benchmark? is it a wasm interpreter or a wasm JIT engine?

Using Node 8.11, which presumably uses a JIT under the hood.

It wasn’t by any means an extensive benchmark, but it compares a small handful of libsnark test programs from [ethsnarks-emscripten](https://github.com/HarryR/ethsnarks-emscripten) built with Emscripten and default compiler settings for the project.

I’m sure there may be a way to tweak compiler flags etc., but I’m doubtful that it could be reduced to even 10x native, e.g. the Cloudflare bn256 optimisations make 10x-20x improvements versus ‘slow native 64bit code’, and wasm is stuck with 32bit arithmetic and no access to native instructions or inline assembly.

---

**cdetrio** (2018-09-03):

Cool, I glanced at the repo but its not clear what program you are benchmarking. If you add a bit of documentation we’d be interested in incorporating this into ewasm benchmarks (where we’ll compare performance of various wasm engines).

But I’m confused what you mean by “calculate on-chain”. Are you more concerned with efficiently generating the snark proof, or verifying the snark proof? It sounds like you are talking about generating the proof, but I don’t see why you’d want to do that in EVM (i.e. why you’d want to meter the proof generation).

---

**HarryR** (2018-09-03):

I will add some benchmarks and more documentation, but I was using [test_hashpreimage.cpp](https://github.com/HarryR/ethsnarks/blob/master/src/test/test_hashpreimage.cpp) and [test_longsightf.cpp](https://github.com/HarryR/ethsnarks/blob/master/src/test/test_longsightf.cpp) as the benchmarks, they generate a key pair (proof key & verifcation key), then proves the circuit using the proving key, then verifies the proof using the verification key. After building the `ethsnarks-emscripten` run:

```auto
node ethsnarks/bin/test_longsightf.js         # takes about 35s
node ethsnarks/bin/test_hashpreimage.js  # takes much longer
```

It outputs debug information about how much time each step takes, e.g. verification of a zkSNARK proof takes ~0.75s, and LongsightF takes ~20s to prove (with 322 rounds), the timing can be compared to the native build of `ethsnarks` by building it separately and running the same programs - this gives me a direct comparison between native and wasm.

I’ve uploaded the .js and .wasm files to: [Releases · HarryR/ethsnarks · GitHub](https://github.com/HarryR/ethsnarks/releases)

![](https://ethresear.ch/user_avatar/ethresear.ch/cdetrio/48/254_2.png) cdetrio:

> But I’m confused what you mean by “calculate on-chain”. Are you more concerned with efficiently generating the snark proof, or verifying the snark proof?

I am building a merkle-tree on-chain that anybody can append items to. The hash algorithm used to build the merkle-tree must be computable on-chain in Solidity / EVM. Then proof of membership of that merkle tree is proved using a zkSNARK and verified on-chain.

---

**HarryR** (2018-09-10):

So, my research continues - with the Davies–Meyer construct, with an invertible function E it’s easy to find a fixed point where you control both the key and the message, likewise with the Matyas–Meyer–Oseas construct which is essentially the same but with the key and the message switched. But… there are better constructs where the computational hardness of the hash function doesn’t rely upon the computational hardness of the underlying cipher…

When operating over a Galois field any exponentiation becomes a ‘hard problem’, and it’s easy to construct a function where the subset sum problems difficulty is directly translatable, but what if we want to do better than that?

My argument is that 90% of ‘applied cryptography’ tries to make it fast in the GF(2) domain, but with zkSNARKS any optimisation for binary domains will slow things down 100x or even 200x. And even with hash functions we rely on a bit-by-bit sampling of the input as a ‘safe’ mechanism - which if you have a true UOWHF doesn’t matter - but abiding by the rules of binary computers you add far too much complexity when real prime fields are as cheap.

[@JustinDrake](/u/justindrake) can you PM or e-mail me the contacts you have for Eli Ben Sasson and Dmitry Khovratovich, I think it’s relevant that I drop them an email with my findings and to generally get in touch etc.

---

**dlubarov** (2018-09-10):

I don’t understand your concern about Davies-Meyer. One could easily find a fixed point for each Merkle node, but is that really a problem? If users are able to put arbitrary data in the leaves, then they could make a leaf’s parent have the same state as the leaf. But normally leaves are hashes of user-chosen data, and as long as the hash is preimage resistant, then finding data which hashes to the fixed point will be computationally hard.

FWIW [Katz et al.](https://eprint.iacr.org/2018/475) also use Davies-Meyer + LowMC to do Merkle proofs for ring signatures.

---

**alexpArtos** (2019-03-21):

Hi [@HarryR](/u/harryr),

have you made progress on this? I’ve only recently began looking at alternatives to SHA256 myself, so would appreciate to know if you found a solution.

I found about Pedersen Hashes in ZCash’s blog

(https://z.cash/technology/jubjub/)

Do you know of anything better?

Thanks.

---

**HarryR** (2019-03-22):

We have implementations of:

- MiMC + one-way-compression-function (davies-meyer, Miyaguchi–Preneel)
- Pedersen hash with the Baby JubJub curve

Implementations:

- https://github.com/HarryR/ethsnarks/blob/d0effc77670bb836b3ef9220b026ef7c34076ed7/src/gadgets/mimc.hpp
- https://github.com/HarryR/ethsnarks/blob/d0effc77670bb836b3ef9220b026ef7c34076ed7/src/gadgets/onewayfunction.hpp
- https://github.com/HarryR/ethsnarks/blob/d0effc77670bb836b3ef9220b026ef7c34076ed7/src/jubjub/fixed_base_mul_zcash.hpp
- https://github.com/iden3/circomlib/blob/77928872169b7179c9eee545afe0a972d15b1e64/circuits/pedersen.circom
- https://github.com/iden3/circomlib/blob/77928872169b7179c9eee545afe0a972d15b1e64/circuits/mimc.circom

There is also the knapsack hash function included in libsnark: https://github.com/scipr-lab/libsnark/blob/bd2a6ca07d4fb72f7b1174d478852234f45ce0b6/libsnark/gadgetlib1/gadgets/hashes/knapsack/tests/generate_knapsack_tests.py

---

The highly optimised Pedersen hash function, using all of the improvements discovered by the ZCash team comes out to around 1.5 constraints per bit.

The Knapsack hash from libsnark requires 1 constraint per dimension per bit, and again.

MiMC with an exponent of 7 and 91 rounds requires about 1.4 constraints per bit, however it may be acceptable to reduce it to 46 rounds which reduces it to around 0.7 constraints per bit.

However, both Pedersen hash and the Knapsack hash require you convert the input data into bits first, which if your input data is field elements will add ~254 constraints of overhead per field element of input.

MiMC works natively with field elements, so if your input data is an array of binary variables you must pack the bits into field elements - requiring only one extra constraint per ~253 bits of data.

All are currently a significant improvement over SHA2-256:

- SHA256, 448bits of input, 27k constraints
- MiMC/e7r91, 448bits of input, 730 constraints (targeting 256bit security level)
- MiMC/e7r46, 448bits of input, 370 constraints (targeting 128bit security level)
- Pedersen hash, 448bits of input, ~680 constraints (targeting 126bit security level)
- Knapsack hash, 448bits of input, 1 dimension, 448 constraints
- Knapsack hash, 448bits of input, 2 dimension, 896 constraints
- Knapsack hash, 448bits of input, 3 dimension, 1344 constraints

However, Pedersen hash is very expensive to implement on EVM, while MiMC and the Knapsack hash are relatively cheap (e.g. 10s of kgas).

---

**alexpArtos** (2019-03-22):

Thanks, Harry. This is very useful.

---

**alexpArtos** (2019-03-22):

Allow me to follow up with a question. Why do we need to convert an input into bits to use the Pedersen Hash?

I don’t fully understand the implementation yet, so I’m reasoning at a high level here. If I’m not mistaken, the Pedersen Hash takes a number of inputs (say x1,…,xn) and an array of equal length of random generators of G, and computes:

```auto
H(x1, ..., xn) = Prod_i=1^n g_i^xi
```

Because these are group operations, there does not seem to be a need to force x_i to be individual bits. Why can’t the xi simply be scalars of the field size (say around 253 bits)? Wouldn’t that avoid all those booleaness constraints?

Thanks.

---

**alexpArtos** (2019-03-25):

[@HarryR](/u/harryr)

I was thinking about this over the weekend. I guess I have found the answer. If the input to the pedersen hash is already in individual bits, then the computation just checks whether x_i is 0 and performs a multiplication by g_i.

Instead, if the input is a field element, the code will have to perform an exponentiation that ultimately will have to be brought down to the individual bits, by using a fast-exponentiation trick. So it will probably boil down to the same thing.

If that is the case, I’d favour splitting the input into bits outside the circuit, because the construction logic for the circuit should then be easier (I wouldn’t have to implement an exponentiation gadget).

Please, correct me if I’m wrong.

Thanks.

---

**HarryR** (2019-03-25):

There are four cases we need to consider, for Pedersen hashes:

1. Input is bits, multiply a hard-coded point
2. Input is bits, multiply a variable point
3. Input is a field element, multiply a hard-coded point
4. Input is a field element, multiply a variable point

When the input is bits and the base point is hard-coded, you can pre-compute the powers of 2 of the base point, then select if that should be added to the summand depending on if the input bit is 0 or 1.

When the input isn’t bits you must first convert it to bits, so you can use it in the above equation.

When the base point is variable, you need to compute the powers of two of the base point, by a sequence of doublings, and select either infinity or that result to be added to the summand for every bit of input.

If you split the number into individual bits as part of the input, or if your input is bits… then you don’t have to do the ‘unpacking’ from a field element to individual bits (and the subsequent constraints which come from that to enforce consistency).

The only problem is intermediate results, say, with a Merkle tree. The result is a field element - or multiple field elements - the X (or/and) Y coordinate of the resultant curve point, at each step you have to convert that back to bits to use as the input to the next Pedersen Hash (or other hash, which requires bit-wise inputs).

With MiMC you can avoid the bits<->field-element conversion at every step, if your initial input is bits it requires one constraint (in addition to validating that the inputs are bits), but the whole chain avoids an extra ~255 constraints at every level because no additional checks are required at each step.

