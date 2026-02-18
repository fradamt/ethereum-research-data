---
source: ethresearch
topic_id: 5538
title: "genSTARK: a JavaScript zk-STARK generation framework"
author: bobbinth
date: "2019-06-01"
category: zk-s[nt]arks
tags: [library]
url: https://ethresear.ch/t/genstark-a-javascript-zk-stark-generation-framework/5538
views: 7019
likes: 22
posts_count: 15
---

# genSTARK: a JavaScript zk-STARK generation framework

I’ve put together a JavaScript library that can help people generate STARK-based proofs of computation. The goal is to take care of as much boilerplate code as possible, and make creating new STARKs simple and “easy.”

The library is in this [GitHub repo](https://github.com/GuildOfWeavers/genSTARK) and it is also published on [NPM](https://www.npmjs.com/package/@guildofweavers/genstark). It is largely based on Vitalik Buterin’s [zk-STARK/MiMC tutorial](https://github.com/ethereum/research/tree/master/mimc_stark) - but it is highly generalized. For example, defining a MiMC STARK takes just 10 lines of code:

```auto
const mimcStark = new Stark({
    field: new PrimeField(2n ** 256n - 351n * 2n ** 32n + 1n),
    tFunction: 'out: $r0^3 + $k0',
    tConstraints: '$n0 - ($r0^3 + $k0)',
    tConstraintDegree: 3,
    constants: [{
        values  : roundConstants,
        pattern : 'repeat'
    }]
});
```

Defining a STARK to prove Fibonacci computation is only 11 lines:

```auto
const fibStark = new Stark({
    field: new PrimeField(2n**32n - 3n * 2n**25n + 1n),
    tFunction: `
        a0: $r0 + $r1;
        out: [a0, a0 + $r1];
    `,
    tConstraints: `
        a0: $r0 + $r1;
        out: [$n0 - a0, $n1 - (a0 + $r1)];
    `,
    tConstraintDegree: 1
});
```

(here, we need to set up 2 registers because the framework is limited to 2 consecutive states, but Fibonacci sequences requires 3 consecutive states to validate).

Once you’ve defined a STARK, you can use it to make proofs and verify computations like so:

```auto
const inputs = [3n];
const steps = 2**13;
const result = 95224774355499767951968048714566316597785297695903697235130434363122555476056n;
const assertions = [
    { step: 0, register: 0, value: inputs[0] },         // value at first step is equal to input
    { step: steps - 1, register: 0, value: result }     // value at last step is equal to result
];

let proof = mimcStark.prove(assertions, steps, inputs);     // create a proof
let result = mimcStark.verify(assertions, proof, steps);    // verify the proof
console.log(result); // true
```

The project is in its infancy right now, and there are still many things to fix and optimize (see the [issues](https://github.com/GuildOfWeavers/genSTARK/issues) in the repo). So, would appreciate any feedback, help, and support.

## Replies

**khovratovich** (2019-06-03):

The idea is really great, but the version of MiMC with 64 round constants is insecure, it is vulnerable to tons of attacks as it were 64 rounds only.

There must be as many different constants as many rounds

---

**bobbinth** (2019-06-07):

Thanks! Regarding MiMC - absolutely, this is just an example of how to use the library.

I’m actually working on a STARK for [Rescue](https://eprint.iacr.org/2019/426.pdf) hash function [here](https://github.com/GuildOfWeavers/genSTARK/pull/9). Should have it done fairly soon.

---

**vbuterin** (2019-06-07):

Excellent work! Look forward to seeing this continue to be improved.

---

**skilesare** (2019-06-10):

Are the constraints limited to addition and subtraction? How would you do something like check a hash for a signature?

I’ve been waiting for something like this for a long time. Awesome work!

---

**vbuterin** (2019-06-10):

Theoretically, a hash is just a bunch of additions and multiplications. In practice, that requires a pretty expressive language…

The main challenge I see is that the number of state variables could get large (unless you’re using an arithmetically simple hash function like MiMC or the newer ones), and the proof verification for this kind of STARK is still linear in the number of state variables.

---

**vbuterin** (2019-06-10):

I wonder how expressive this design is… for example could it be used to implement the “minimal mixer” design at https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/rJj9hEJTN? Theoretically that just requires proving a Merkle branch so it’s just a series of hashes. Basically, depositing would consist of adding a value x = H(x_1, x_2) to a tree (where x_1 is a constant that you randomly generate and x_2 is your withdrawal address), and the constraints would be as follows (assuming the current root of the tree is R and the depth is 32):

- v_0 = [public value: the withdrawal address]
- v_1 = H(s_0, v_0) (where s_0 is a hidden “sister node”, in this level the blinding value and in future levels the sister node in the main Merkle tree)
- v_2 = H(s_1, v_1)\ OR\ v_2 = H(v_1, s_1) (also writable as (H(s_1, v_1) - v_2) * (H(v_1, s_1) - v_2) = 0)
- v_3 = H(s_2, v_2)\ OR\ v_3 = H(v_2, s_2)
- …
- v_{33} = H(s_{32}, v_{32})\ OR\ v_{33} = H(v_{32}, s_{32})
- v_{33} = R [public value: the current root of the tree]

This proves that v_0 actually is a value that was included in the tree (as part of a hash x = H(s_0, v_0) that was added as a leaf to the tree) without revealing its position in the tree. So the constraints being proven are not all that complex, just a series of hash functions. Is this system powerful enough to do it? If so this could serve as a useful alternative to the same scheme being implemented with SNARKs.

---

**vbuterin** (2019-06-10):

My immediate instinct is that you should be able to do the above with four state registers; at exact multiples of the MIMC hash round count registers 0 and 2 would represent v_{i+1} = H(s_i, v_i) and v_{i+1} = H(v_i, s_i) and registers 1 and 3 would represent claimed sister leaves s_{i+1} (we would constrain that at these heights registers 0 must equal registers 2 and likewise for 1 and 3), and then between exact multiples of the MIMC hash round count registers 0 and 1 would be used to compute H(s_{i+1}, v_{i+1}) and registers 2 and 3 would be used to compute H(v_{i+1}, s_{i+1}). Just need to figure out a secure construction for a 2-to-1 version of MIMC (what I implemented in my original STARK prover was 1-to-1 field element). The best I can think of is that if you have two versions of MIMC H1 and H2 with two different sets of round constants then you could do H(x, y) = H1(x) + H2(y).

---

**bobbinth** (2019-06-10):

Actually, as a part of [this PR](https://github.com/GuildOfWeavers/genSTARK/pull/9) I’ve created a much more expressive language for constraints. The prototype is not fully finished yet, but here is a draft description: [Arithmetic Script](https://github.com/GuildOfWeavers/genSTARK#arithmetic-script).

My plan is to finish implementation of Rescue hash function. This is mostly done: here is a [toy example](https://github.com/GuildOfWeavers/genSTARK/blob/master/examples/rescue/hash2x64.ts) with 2 registers and a more [“real-life” example](https://github.com/GuildOfWeavers/genSTARK/blob/master/examples/rescue/hash4x128.ts) with 4 registers. And then use this hash function as the basis for a STARK that can prove membership of a value in a Merkle tree.

I agree, the constraints for something like this should be relatively simple, and with Arithmetic Script, they shouldn’t be too difficult to write up. But there are a also a couple of things that I haven’t figured out yet.

---

**bobbinth** (2019-06-12):

I’ve just published a new version of the library. The main changes are:

- Added example STARKs for Rescue hash function here.
- Completed first implementation of Arithmetic Script. Now transition functions and constraints are expressed using this script.

Just to show the power of Arithmetic Script, here are the constraints for Rescue from the whitepaper:

\left\{ \sum_{j=1}^{m} M[i,j](S[j]^3+K_{2k-1}[i]^3) - (\sum_{j=1}^{m} M^{-1}[j,j](S'[j]-K_{2(k+1)-1}[j]))^3
\vert i \in [m] \right\}

And here is how this can be expressed using Arithmetic Script:

```auto
S: [$r0, $r1, $r2, $r3];
S_P: [$n0, $n1, $n2, $n3];
K1: [$k0, $k1, $k2, $k3];
K2: [$k4, $k5, $k6, $k7];

M: ${inline.matrix(mds)};
M_INV: ${inline.matrix(invMds)};

T1: M # S^3 + K1;
T2: (M_INV # (S_P - K2))^3;

out: T1 - T2;
```

This is actually fewer lines of code than it would take me to write this out in JavaScript. Here is how to read it:

1. The first 4 lines define vectors that hold values from registers. This STARK has 4 mutable registers and 8 constant registers.
2. The next 2 lines define 2 variables that are matrixes. The inline part just inlines the text containing the actual matrixes into the text.
3. The next two lines perform operations on the matrixes and vectors. The # is actually matrix multiplication.
4. The last line is the output of the script which is a vector of 4 values.

---

**vbuterin** (2019-06-12):

Yay! Any interest in writing up the constraints for the length-32 Merkle branch verification as above?

Would be interesting to get stats for proof length etc.

---

**vbuterin** (2019-06-12):

Also what kind of Merkle proofs are you using? Do you have the maximally optimized Merkle branches as in https://github.com/ethereum/research/blob/f196808fff509c2e6c47c8b6091bf149438ad536/merkle_tree/merk.py ? I added that fairly recently (~2 months ago) and it gave a further ~25% size decrease.

---

**bobbinth** (2019-06-12):

Yep - that’s something I’ll tackle next. I need to make some updates to the library to support something like this, and I’ve already started working on them in [this PR](https://github.com/GuildOfWeavers/genSTARK/pull/11). One issue you pointed out earlier is hashing of two elements into a single element. Rescue hash function supports this, but I’d either have to double the number of steps or double the number of registers. Need to think this through a bit more.

For Merkle proofs I’m using a [small library](https://github.com/GuildOfWeavers/merkle) I’ve built. It also does proof batching. The algorithm is loosely based on the Octopus algorithm from [this paper](https://eprint.iacr.org/2017/933.pdf). In my very informal benchmarks, the proof size is reduced by between 40% and 60% vs. the naive approach (no batching). I haven’t benchmarked it against your approach - but your code looks considerably simpler.

---

**moses5407** (2021-04-17):

I just found this thread on the path of checking out ZK-Stark proofs of merkle tree values.

Are you still around? Is there further work on this?

---

**bobbinth** (2021-04-17):

This works kind of evolved into [Distaff VM](https://github.com/GuildOfWeavers/distaff). The VM has two instructions for generating STARK proofs for Merkle paths:

- smpath - where both the path and index are supplied via a private witness.
- pmpath - where the path is supplied via a private witness but index is a public input.

Both instructions are described in some detail [here](https://github.com/GuildOfWeavers/distaff/blob/fad92ce592921e671e72f93cd0078e867350860d/docs/assembly.md#merkle-authentication-path).

