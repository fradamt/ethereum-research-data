---
source: ethresearch
topic_id: 4382
title: A sketch for a STARK-based accumulator
author: vbuterin
date: "2018-11-26"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/a-sketch-for-a-stark-based-accumulator/4382
views: 5308
likes: 4
posts_count: 13
---

# A sketch for a STARK-based accumulator

We can define a version of MIMC that works as follows: SimplifiedMiMCHash(x, d) = f^{512}(x), where f(x) = x^3 + d; that is, we apply the permutation x \rightarrow x^3 + d 512 times.

Security claim: partial collision resistance - if y = SimplifiedMimChash(....SimplifiedMiMCHash(SimplifiedMiMCHash(x, d1), d2)...dn) it is infeasible to find (d1', d2' ... dn') \ne (d1, d2 .. dn) such that y = SimplifiedMimChash(....SimplifiedMiMCHash(SimplifiedMiMCHash(x, d1'), d2')...dn')

**[NOTE: I think there are better ways to do this that more directly lean on traditional collision resistance properties of these arithmetically cheap hash functions…]**

We now define the accumulator as follows. The accumulator A starts at 0, and then every time a value v is added we set A := SimplifiedMiMCHash(A, v).

For proofs of inclusion or exclusion, we set up a STARK with three tapes: the accumulator state A, the witness W consisting of a sequence of 512-value repeats of values that get added to the accumulator, a loop progress counter M which starts at 1 and a product trace P which starts at 1. Let \omega be a 512th root of unity, and x be the value you want to prove inclusion or exclusion of. We add the following constraints:

- M[i] = 1 or W[i] = W[i-1] (ie. W is only allowed to change at multiples of 512)
- M[i] = M[i-1] * \omega (incrementing M; note that it loops around to 1 every 512 steps)
- A[i] = A[i-1]^3 + W[i]
- P[i] = P[i-1] * (x - W[i-1])

We check the boundary conditions (i) A[0] is the starting accumulator, (ii) A[n] is the ending accumulator, (iii) P[0] = 1. The goal is that P will stay nonzero as long as x is never used in the witness, and will permanently become zero if x is used in the witness even once.

The STARK construction is very simple, with only 4 state objects to worry about; it should not be difficult to convert the [existing MIMC-STARK code](https://github.com/ethereum/research/tree/master/mimc_stark) to implement this construction. Note that it should be fairly straightforward to replace MIMC in this construction with [Jarvis](https://www.esat.kuleuven.be/cosic/jarvis-and-friday-stark-friendly-cryptographic-primitives/). This means that we can use STARKs for proving history inside of Plasma, and even potentially to prove contract non-double-resurrection for sharding, more quickly than a fully complete STARK system that supports more complicated operations.

## Replies

**khovratovich** (2018-11-27):

OK let’s break it.

A collision in a binary field:

MiMCHash(1,1)=MiMCHash(1,0)=1.

---

**khovratovich** (2018-11-27):

A collision in a prime field F.

MiMCHash(1,0) = MiMCHash(MiMCHash(1,0),0)=1.

Finding a collision on inputs of the same length is less trivial but I am pretty sure is doable because of repetitive structure of the function.

---

**bharathrao** (2018-11-27):

Can this be fixed by adding a simple boundary condition and/or field definition which excludes 0 and 1

---

**khovratovich** (2018-11-27):

Many things can be fixed, but cryptographic design produces best outputs in a different way. If one needs a secure hash function, it is better to start with requirements.

---

**bharathrao** (2018-11-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> W consisting of a sequence of 512-value repeats of values

Is this a fixed set of values such as the first 512 prime numbers? Does this mean the accumulator can only accommodate 512 entries?

---

**vbuterin** (2018-11-27):

The goal here is to have a secure hash function of the form h(x, y) = z, which can be calculated arithmetically ideally with one state object, though 2 state objects or slightly more would also work too.

The nice thing about such a primitive is that it is also useful for Merkle branches.

I absolutely agree that coming up with something for which we try to establish traditional collision resistance properties is the right approach here.

---

**khovratovich** (2018-11-27):

A hash function of the form `h(x,y) = z` can be any hash function `H(u) = z` by setting `u=x||y`. Here `H` can be Jarvis, MiMC, InversionHash, or any STARK-friendly design, so there are many of them.

Is there any other specific property you want to have here?

---

**khovratovich** (2018-11-27):

Also if you want an iterative hash function that takes arbitrary long inputs, then there are basically two ways to do that:

1. Take a STARK-friendly secure permutation and use it in the sponge mode. It must be sufficiently wide to provide 128-bit collision and preimage resistance, but we know how to design such permutations.
2. Take a STARK-friendly secure compression function and use it in the Merkle-Damgard or Haifa mode. The compression function itself can be based on a blockcipher (like Jarvis, SHA-2) or built from scratch (like Groestl or MD6).

---

**vbuterin** (2018-11-27):

> can be any hash function H(u) = z by setting u=x||y .

How do you do `||` in a field?

---

**khovratovich** (2018-11-27):

Depends on the size of `x` and `y` and the field size and the structure of the function. The simplest case is when both `x` and `y` are field elements and the hash function operates in the same field, then I do not see a problem.

---

**vbuterin** (2018-11-27):

Let’s suppose `x` and `y` are field elements, and we want to output a field element `hash_input = x || y`. How do you do that?

Also note that if your answer is “Merkle-Damgard construction”, then note that requires as a building block a function f(x, y) \rightarrow z which can then be applied many times to get a function f(x_1, x_2, x_3 ... x_n) \rightarrow z so it still requires solving the original problem.

---

**khovratovich** (2018-11-27):

No I mean if `x` and `y` are field elements and the internal state of H is a tuple of field elements (say a pair, but can be a quadruple or else) then you can do that trivially.

How to build H over a tuple of field elements? Like AES, for example, or Groestl. In the [Inversion Hash](https://drive.google.com/open?id=1LEAe5yjoIBo1aOUqHLIPcofZ0a5bawCk) we use an MDS matrix to mix the field elements with each other and an inversion S-box for degree saturation. Then you get a permutation, but it can be also used for a block cipher, then with MD/MP/MMO you get a compression function then a full hash function. But the latter is more complicated I think.

