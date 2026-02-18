---
source: ethresearch
topic_id: 21512
title: "Falcon as an Ethereum Transaction Signature: The Good, the Bad, and the Gnarly"
author: asanso
date: "2025-01-20"
category: Cryptography
tags: []
url: https://ethresear.ch/t/falcon-as-an-ethereum-transaction-signature-the-good-the-bad-and-the-gnarly/21512
views: 1365
likes: 21
posts_count: 10
---

# Falcon as an Ethereum Transaction Signature: The Good, the Bad, and the Gnarly

This is **Part 2** of a blog series exploring the feasibility of implementing a **post-quantum signature** scheme for Ethereum. In [Part 1](https://ethresear.ch/t/so-you-wanna-post-quantum-ethereum-transaction-signature/21291/1), we introduced the fundamental challenges and considerations involved in transitioning Ethereum to a quantum-resistant future. In this installment, we’ll dive deeper into Falcon, a promising post-quantum signature algorithm, examining its strengths, weaknesses, and the practical hurdles of integrating it into Ethereum’s transaction framework.

## Falcon Signature Scheme - Technical Overview

[Falcon](https://falcon-sign.info/) (*Fast-Fourier Lattice-based Compact Signatures over NTRU*) builds upon the lattice-based signature framework of Gentry, Peikert, and Vaikuntanathan ([GPV](https://eprint.iacr.org/2007/432)). It applies this framework to NTRU lattices and employs a “fast Fourier sampling” trapdoor sampler. The scheme relies on the Short Integer Solution (SIS) problem over [NTRU](https://en.wikipedia.org/wiki/NTRU) lattices, which is considered computationally hard to solve in the general case, even with quantum computers, as no efficient solving algorithm is currently known.

### Core Components

Falcon is based on the **hash-and-sign** paradigm and is an evolution of the traditional RSA signature scheme. However, instead of relying on number-theoretic problems, it leverages the hardness of lattice-based problems. Falcon’s security is based on the hardness of finding short vectors in NTRU lattices, leveraging **Gaussian sampling** techniques for generating trapdoor bases with reduced norms. This ensures efficient key generation and signing.

1. Key Generation:

Given an NTRU polynomial ring ( \mathbb{Z}[X] / (X^n + 1)), a private key consists of two short polynomials ( f, g ) satisfying the NTRU equation.
2. The public key is derived as ( h = g / f ) in the ring ( \mathbb{Z}_q[X] / (X^n + 1) ).
3. Signing Process:

A message is hashed into a challenge vector in the lattice domain.
4. A short solution is sampled using fast Fourier sampling, ensuring a compact signature size while maintaining security against lattice reduction attacks.
5. The signature consists of the short lattice vector satisfying the challenge.
6. Verification:

The verifier checks whether the signature satisfies the public key relation in the lattice ring.
7. Verification involves computing norms and ensuring the validity of the lattice basis under modular arithmetic.

Falcon is designed to offer a robust post-quantum signature solution, combining lattice-based cryptography with efficient sampling techniques. While its security benefits are clear, like any cryptographic system, it presents certain trade-offs in terms of complexity and implementation challenges. Now, let’s break down the highlights, potential pitfalls, and some of the more challenging aspects of Falcon.

## The Good

Aside from the well-known benefits highlighted by NIST, such as **Compact Signatures**, **Fast Operations** (efficient key generation and verification via FFT techniques), and **Security Proofs** (relying on lattice reductions and worst-case hardness assumptions). Falcon also provides Ethereum-specific advantages. Notably, it has a well-defined **worst-case running time**, making it particularly useful for the Ethereum Virtual Machine (EVM), where predictable performance and execution times are essential for scalability and reliability.

## The Bad

Falcon’s reliance on **floating-point arithmetic** and specialized number-theoretic transforms (NTT/FFT) can lead to **implementation complexity** and sensitivity to side-channel vulnerabilities during **signing**. However, this is **NOT** a significant concern for Ethereum, as signing occurs off-chain, where performance is less critical. The main focus is on optimizing the verification process, which happens on-chain, ensuring efficient and secure execution.

## The Gnarly

There has been ongoing research into efficiently aggregating Falcon signatures, such as the work presented in this [paper](https://eprint.iacr.org/2024/311). Assuming the aggregation will be efficient enough, using Falcon in the consensus layer to replace the BLS signature (instead of the [alternative proposal](https://eprint.iacr.org/2025/055.pdf) based on Hash-Based Multi-Signatures) would help maintain a more homogeneous stack across the Ethereum network.

## Conclusion

Falcon is a strong candidate for post-quantum cryptography applications, including blockchain systems like Ethereum, where signature size and verification efficiency are critical. In Part 3 of the series, we will begin implementing the hybrid approach introduced in [Part 1](https://ethresear.ch/t/so-you-wanna-post-quantum-ethereum-transaction-signature/21291/1), initially focusing on **Account Abstraction** and a **Solidity contract for Falcon verification**, bridging the gap between post-quantum security and Ethereum’s current infrastructure.

## Replies

**JChanceHud** (2025-01-20):

Nice writeup, do you have an opinion on Falcon vs Crystals-Dilithium? Crystals is essentially Falcon without gaussian sampling. From an implementation perspective it’s much more simple with slightly larger keys/sigs.

Re LaBRADOR signature aggregation: just want to mention the verification complexity is linear for these proofs (proof sizes are sublinear though).

---

**rdubois-crypto** (2025-01-21):

Gaussian sampling is the signer problem. The signature verifier implementation of FALCON is easy. In all aspects FALCON verifier is superior: time, bandwidth (3.5), key size. Having the signer handling the complexity is the natural choice. Like we do with ZK, signer has larger capacity than the verifier. https://s.itho.me/ccms_slides/2024/5/23/4414254e-124d-4bbd-8a41-579706b59401.pdf

---

**arikg** (2025-01-22):

What are your thoughts about the candidates in the “Post-Quantum Cryptography: Additional Digital Signature Schemes”?

I know that they did not publish results yet, but are you tracking any of the schemes in there as possible alternatives to Falcon?

Do you see a reasonable chance that one of them gives you better overall tradeoffs and will become a leading alternative candidate?

---

**asanso** (2025-01-22):

The good thing about using Account Abstraction is that it provides flexibility in the choice of the signature.

I am, of course, following the ‘Post-Quantum Cryptography: Additional Digital Signature Schemes’ process, and some interesting signatures on my radar are Hawk, SQISign, and MAYO. But well, let’s see.

---

**mratsim** (2025-01-28):

Are there been reviews of SQSign suitability? https://sqisign.org/

Key sizes are really small

> NIST round Ⅴ parameters, pubkey: 128 bytes, signatures:335 bytes

I’m quite concerned about primitives in Falcon:

- sampling, having a good RNG is already a problem in cryptography, this was the whole reason of RFC6979 - Deterministic ECDSA as many many implementations had RNG/sampling bugs. On the Ethereum side ourselves, we spent a lot of time trying to get cryptographic shuffling right, see p19 and 20 of my 2019 talk
p191920×1080 186 KB
p202000×1125 165 KB
- double-precision: the non-determinism makes it very hard to prove in a SNARKS. Furthermore hardware accelerating it, if needed in the future for large aggregation for example, is painful as consumer GPUs issue fp64 instructions at 1/64 the fp32 rate see nvidia doc: CUDA C++ Programming Guide (Legacy) — CUDA C++ Programming Guide

> 64 FP32 cores for single-precision arithmetic operations in devices of compute capability 8.0 and 128 FP32 cores in devices of compute capability 8.6, 8.7 and 8.9,
> 32 FP64 cores for double-precision arithmetic operations in devices of compute capability 8.0 and 2 FP64 cores in devices of compute capability 8.6, 8.7 and 8.9
> Compute capability X.0 are datacenter cards (Tesla) while 8.6, 8.7, 8.9 are consumer GPUs, and consumer GPUs have 128 FP32 cores for 2 FP64 cores.

---

**CPerezz** (2025-01-28):

First of all, this series of 2 posts has been awesome to read. Thanks [@asanso](/u/asanso)

![](https://ethresear.ch/user_avatar/ethresear.ch/asanso/48/4949_2.png) asanso:

> Notably, it has a well-defined worst-case running time, making it particularly useful for the Ethereum Virtual Machine (EVM)

This is extremely interesting! I did not think about it!

The main concern that this article doesn’t account for is that even aggregation is fast, you’re trading off by bandwidth, not just total size of stored data on-chain.

Aggregation would need to be so fast, that even needing to send multiple packets in order to transmit a single signature is worth vs the speed of signing + aggregating.

And I think this is an interesting and important metric to obtain in order to evaluate things like the replacement of Bls sigs.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/jchancehud/48/18762_2.png) JChanceHud:

> Re LaBRADOR signature aggregation: just want to mention the verification complexity is linear for these proofs (proof sizes are sublinear though).

Even if pairing with Greyhound, this is still a good point. It will still probably require to generate a SNARK that verifies it. But to date, this proof would be even bigger than the signature. At the benefit of a succint verifier. Thus trading off even more bandwidth.

It definitely looks like a nice option. But I yet fail to see if ticks all boxes (or the most important ones). I don’t see any doing it BTW. It’s not just this one.

This brings me to this point from Mamy:

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> double-precision: the non-determinism makes it very hard to prove in a SNARKS

And I agree 100%. Except lattice-based proving systems/PCSs (which are few and not really good atm) any other SNARK/STARK will just not be able to prove this at a reasonable cost.

And this is a major concern. Specially if we plan to reach Snarkification of EL/CL at some point in the future.

(Although via Acount Abstraction, we could avoid some stuff for sure).

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> Are there been reviews of SQSign suitability? https://sqisign.org/

I think the main point here is that we would loose the aggregatability. Which definitely defeats the purpose of minimizing data stored on chain. And which is also the “standard” way for Beacon Chain to work. (This makes me wonder why don’t we try the same for EL with some trick for DA but whatever…)

---

If not being ZK-provable isn’t an issue, why don’t we use Isogenies then? Their sigs are tiny and the speed isn’t bad. Specially for the case of Beacon Chain. Where everyone can sign at the same time and aggregate or pass a message when it’s their turn. Do you have any thoughts [@asanso](/u/asanso) ?

---

**asanso** (2025-01-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> Are there been reviews of SQSign suitability? https://sqisign.org/

as you know my area of research is isogeny based cryptography so of course SQISign is something I follow. It’s a bit too early though to judge. The good thing about using Account Abstraction though is the flexibility, so we can always include new solutions.

About the sampling and floating precision is a signer problem that is off chain no ?

---

**asanso** (2025-01-29):

> First of all, this series of 2 posts has been awesome to read.

Appreciate your feedback !

> The main concern that this article doesn’t account for is that even aggregation is fast, you’re trading off by bandwidth, not just total size of stored data on-chain.

As specified in Part 1 of the post here we are tacking the execution part of Ethereum. The aggregation part is a “consensus problem” and there we have the Beam Chain project. True I mentioned aggregation in the gnarly part of this post (that’s why gnarly :)).

> If not being ZK-provable isn’t an issue, why don’t we use Isogenies then?

as mentioned above is too early to think about using SQiSign or PRISM (https://eprint.iacr.org/2025/135.pdf) for now .

---

**JChanceHud** (2025-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> I don’t see any doing it BTW. It’s not just this one.

We have to stop comparing PQ schemes to elliptic curve ones. IMO ECC is a detour in history, its properties are incredibly good *because* it’s not quantum secure. Isogenies are good but don’t get close to dlog based ecdsa/bls/groth16.

I imagine the PQ paradigm will be multiple schemes that are good at different things. Instead of having a single scheme that is great in all dimensions we’ll need more schemes to build things and more engineering effort/complexity.

I just don’t buy linear proving and constant communication+verification complexity. It’s simply too good. Happy to be proven wrong though.

