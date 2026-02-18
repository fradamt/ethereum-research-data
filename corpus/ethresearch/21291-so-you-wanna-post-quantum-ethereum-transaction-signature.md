---
source: ethresearch
topic_id: 21291
title: So you wanna Post-Quantum Ethereum transaction signature
author: asanso
date: "2024-12-18"
category: Cryptography
tags: []
url: https://ethresear.ch/t/so-you-wanna-post-quantum-ethereum-transaction-signature/21291
views: 2666
likes: 56
posts_count: 26
---

# So you wanna Post-Quantum Ethereum transaction signature

# So you wanna Post-Quantum Ethereum transaction signature

*Thanks to Vitalik Buterin, Justin Drake, Renaud Dubois, Marius Van Der Wijden and Zhenfei Zhang for fruitfull discussions.*

## Introduction

2024 will probably be remembered as one of the years marking the acceleration of the quantum computer menace. Google, under its CEO Sundar Pichai, finally unveiled its quantum chip, Willow, via a [loud tweet](https://x.com/sundarpichai/status/1866167429367468422)!

Scott Aaronson, one of the most famous quantum experts in the world, has changed his message to people asking whether they should be worried about quantum computers. He [shifted from saying](https://scottaaronson.blog/?p=8329)

> … Maybe, eventually, someone will need to start thinking about migrating from RSA, Diffie-Hellman, and elliptic curve cryptography to lattice-based crypto or other systems that could plausibly withstand quantum attacks,…

to

> Yes, unequivocally, worry about this now. Have a plan.’

Vitalik has already written about [how to hard-fork to save most users’ funds in a quantum emergency](https://ethresear.ch/t/how-to-hard-fork-to-save-most-users-funds-in-a-quantum-emergency/18901/1). Also, few days ago, he highlighted in a [podcast](https://x.com/3orovik/status/1867754730136731923) the four main Ethereum components potentially vulnerable to quantum attacks. They are:

1. Ethereum transaction signatures (notably using ECDSA)
2. BLS signatures in consensus
3. Data Availability Sampling (leveraging KZG commitments)
4. Verkle trees (if shipped with Bandersnatch)

An attentive reader might have noticed that these four points have something in common—yes, it’s my *beloved* elliptic curves. Unfortunately, the discrete logarithm problem for elliptic curves (ECDLP) is broken by Shor’s Algorithm, a famous quantum algorithm.

In this short note, we are going to analyze a possible post-quantum replacement for the first point, namely a potential **post-quantum Ethereum transaction signature**.

## Which PQ signature?

Now, a legitimate question is: *which post-quantum (PQ) signatures should we use?* Fortunately, we don’t need to overthink this too much if we had to choose right now. Zhenfei Zhang, a former Ethereum Foundation cryptographer, has already written about the [NIST Post-Quantum Cryptography Standardization Process](https://crypto.ethereum.org/blog/nist-pqc-standard). If we analyze the three possible signature choices (two of which leverage lattice-based cryptography), it’s clear (at least for now) that Falcon appears to be the most promising candidate. The computation for the verifier should be roughly the same as other lattice-based signature schemes (like Dilithium), i.e., bounded by an FFT. However, [Falcon](https://falcon-sign.info/) does have a smaller signature size.

## Ship it!!!

Now that we’ve ‘settled’ on the signature to use, the next question is: *how are we going to ship it?*  There is a big dichotomy now: one implies a hard fork, and the other doesn’t. Let’s dig a bit deeper.

### The Account Abstraction way

The first approach we will discuss, arguably the most elegant and promising, involves **Account Abstraction** (AA). It has been advocated by Justin Drake and Vitalik on various occasions.

For people not familiar with it, AA is a proposed improvement to make the Ethereum ecosystem more flexible and user-friendly by changing how transactions and accounts are managed. It shifts certain functionalities traditionally reserved for externally owned accounts (EOAs) into smart contracts, effectively “abstracting” the differences between EOAs and smart contract accounts.

Ethereum developers have introduced various proposals for implementing AA, including [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337). This is a practical solution that achieves AA without requiring a consensus-layer upgrade. It uses a mechanism called *User Operation* objects and introduces a separate *Bundler* layer to handle transactions.

Adding **Falcon as the Ethereum transaction signature in this scenario means coding a Falcon verifier contract** that is responsible for verifying the validity of *User Operation* objects before they are executed by the *Entry Point* contract.

Now, this may sound like all sunshine and rainbows, but there is at least one substantial underlying issue. Coding Falcon in Solidity might not be the best experience (and it’s probably quite gas-costly). On top of that, there are even nastier problems, such as the fact that Falcon deals with 13-bit numbers, while Solidity only supports U256. The latter is the kind of issue that could be addressed by adding [SIMD](https://eips.ethereum.org/EIPS/eip-616) and [EVMMAX](https://eips.ethereum.org/EIPS/eip-6690) to the EVM.

- Pros: It is an elegant and flexible solution.
- Cons: It is costly in terms of gas consumption.

### The hard fork way

The method we discuss here is probably the simplest technically. It is inspired by previous work done by Marius Van Der Wijden and essentially involves introducing a **new [transaction type](https://eips.ethereum.org/EIPS/eip-2718) signed with Falcon signatures** [instead of BLS signatures](https://eips.ethereum.org/EIPS/eip-7591). The biggest problem here is that, by doing so, we are tightly bound (through a new EIP) to a favored master signature scheme.

So, to recap this approach

- Pros:  Easy to code and fast.
- Cons: Not future-proof.

### Hybrid

A really tempting approach would be to take the best of the two methods above and combine them into a single one. In a nutshell, we could leverage AA in a similar way that [RIP-7212](https://github.com/ethereum/RIPs/blob/5dbad75fcc9aabf3021e176818aa8d256293d460/RIPS/rip-7212.md) does, but of course, we would need a **new RIP for Falcon**. This might provide the time to experiment with the feature in rollups and determine if Falcon is truly the way to go. However, it is important to note that this approach does not solve the original problem of introducing a new signature scheme at the L1 level.

- Pros: Easy to code and fast.
- Cons: Temporary (does not solve the L1 use case).

## Conclusion

The rise of quantum computing demands urgent action to secure Ethereum, particularly its transaction signatures vulnerable to Shor’s Algorithm. Falcon, a lattice-based signature scheme, emerges as a strong candidate due to its efficiency and compact size. Deployment strategies, including Account Abstraction, hard forks, or a hybrid approach, each offer distinct benefits and trade-offs. A careful evaluation is essential to ensure Ethereum remains robust against quantum threats while maintaining scalability and usability.

## Replies

**FabrizioRomanoGenove** (2024-12-18):

What do you mean with ‘it is costly in terms of gas consumption’ in the second method (hard fork)?

In any case replacing ECDSA with falcon will work for simple transactions I guess, BLS transactions are nice but not having them is probably not the end of the world. Do you guys have any clue about how to replace BLS at consensus level tho? That, to me, seems the hardest problem of the four you listed so far!

---

**ihagopian** (2024-12-18):

Extra data point: the Algorand blockchain has been using Falcon signatures since ~2022:

- Algorand: Pioneering Falcon Post-Quantum Technology on Blockchain | Algorand Foundation News
- Algorand’s post-quantum blockchain technology | Algorand
- GitHub - algorand/falcon

---

**zincoshine** (2024-12-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/fabrizioromanogenove/48/16390_2.png) FabrizioRomanoGenove:

> Do you guys have any clue about how to replace BLS at consensus level tho?

I am given to understand that Winternitz is being considered as a replacement for BLS in beam chain.

---

**asanso** (2024-12-18):

> What do you mean with ‘it is costly in terms of gas consumption’ in the second method (hard fork)?

Thanks for your comment it was indeed a copy cargo issue. Fixed to

- Pros: Easy to code and fast.
- Cons: Not future-proof.

> how to replace BLS at consensus level tho

yes but this is going to be discussed elsewhere

---

**rdubois-crypto** (2024-12-18):

That’s a concise and clear sum up.

Another possibility would be to introduce NTT (the name cryptographers give to FFT specialized to prime fields) rather than a specific algorithm as new EIP. NTT is the core operation both for STARK verifiers, and lattice candidates. What is called “zk-friendly” being in fact the capacity to multiply polynomials efficiently. All the previous reasoning (progressive precompile, Hard fork or RIP) being the same for this object.

Having a fast and generic NTT would benefit both ZKEVMs and Lattice based signatures.

---

**asanso** (2024-12-18):

This is a nice option indeed. I like it. I wonder if EVMMAX could also be an alternative also here

---

**pldd** (2024-12-18):

If you were to build a contract to verify ECDSA with only bigint primitives the gas price would be exhorbitant too, the cost of verification is heavily discounted when included as opcode.

Also we did deploy a smart contract Lamport wallet using account abstraction, the verification cost is actually very decent for one-time hash-based schemes.


      ![](https://ethresear.ch/uploads/default/original/3X/f/8/f8c432330b057ee9fbe2c618914eb278aba0ce77.png)

      [chromewebstore.google.com](https://chromewebstore.google.com/detail/anchor-vault/omifklijimcjhfiojhodcnfihkljeali?hl=en)



    ![](https://ethresear.ch/uploads/default/original/3X/3/d/3d139d4f20521b88e0a073558cb690ad726cef9f.jpeg)

###



A better & safer way to use Ethereum

---

**p_m** (2024-12-18):

> it’s clear (at least for now) that Falcon appears to be the most promising candidate

How is it clear? Why? To me Sphincs feels safer. Which parts of eth are not suitable for 32KB sigs (as opposed to 1KB falcon sigs)?

---

**asanso** (2024-12-19):

> To me Sphincs feels safer.

At the end of the day, Falcon is also one of the standards. That said, especially if we follow the AA approach, we do not need to limit or constrain ourselves to a single possible signature.

---

**CPerezz** (2024-12-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/asanso/48/4949_2.png) asanso:

> Falcon, a lattice-based signature scheme, emerges as a strong candidate due to its efficiency and compact size. Deployment strategies, including Account Abstraction, hard forks, or a hybrid approach, each offer distinct benefits and trade-offs.

Curious on how easy is it to prove inside of a ZK circuit. Mainly because at some point we may want to snarkify the whole ethereum. And there, this might become our archenemy as keccak was 4 years ago when all the ZKEVM work started.

Also, thanks for the detailed post [@asanso](/u/asanso) <3

> Having a fast and generic NTT would benefit both ZKEVMs and Lattice based signatures.
> Unsure this is the only bottleneck. Although it’s a cool idea. The problem with these opcodes is that:

1. They should exist within L2s as experimentation. Not in mainnet IMO.
2. These opcodes are hard to price. As they’re variadic length and ammortize depending on it on different ways. They also depend on the underlying hardware (namely cores or parallelization capabilities.)
3. One could say why not FFT? And then we yet again open Pandora’s vault.

---

**rdubois-crypto** (2024-12-19):

The SIMD EIP you referred actually potentially provides a potential better speed up. EVMMAX has been built with 256-384 bits ECC constraints in mind. This SIMD actually looks like a ‘RISC-VM’-lite and might be a good compromise between eWASM/RISCVM (large complexity but generic) and the specificity of EVMMAX.

It could be rewritten with a ARM vectorized types-like notations, which are very intuitive: uintAxB being handling B values of size A in parallel. Then any operation opAxB(u1,u2) is the parallel application of operator “op” to B elements of size A.

---

**cryptskii** (2024-12-22):

Random walks if/where possible. without  reading, the above context, just planting a seed in your minds

---

**jeroenvdgraaf** (2025-01-08):

Even though I agree we should be alert, there is no real urgency in making a decision. Quantum  computers are still ten years away, as physicists have been saying ever since Shor published his algorithm back in 1994.

So instead of choosing between Falcon and Sphincs, maybe we should await the results of the additional NIST call for PQ signatures. I find some of the underlying security assumptions more convincing, anyway we would have a wider range of options to choose from.

---

**JChanceHud** (2025-01-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/cperezz/48/9563_2.png) CPerezz:

> Curious on how easy is it to prove inside of a ZK circuit. Mainly because at some point we may want to snarkify the whole ethereum. And there, this might become our archenemy as keccak was 4 years ago when all the ZKEVM work started.

I’ve gone back and forth on this. On one hand we need to sample elements using a gaussian distribution, but on the other ~~this sampling should only occur at witness generation time, so floating point math shouldn’t be a problem.~~ Actually if we’re proving execution of an `ecsign` type opcode in the evm we would have to prove gaussian sampling ![:confused:](https://ethresear.ch/images/emoji/facebook_messenger/confused.png?v=12)

The lattice constructions should be *really* easy to prove provided we have wrong field math. iiuc they’re all purely (linear) algebraic.

![](https://ethresear.ch/user_avatar/ethresear.ch/rdubois-crypto/48/12781_2.png) rdubois-crypto:

> Another possibility would be to introduce NTT (the name cryptographers give to FFT specialized to prime fields) rather than a specific algorithm as new EIP. NTT is the core operation both for STARK verifiers, and lattice candidates. What is called “zk-friendly” being in fact the capacity to multiply polynomials efficiently. All the previous reasoning (progressive precompile, Hard fork or RIP) being the same for this object.

Instead of NTT I think we should do accelerated [finite field math](https://eips.ethereum.org/EIPS/eip-6690) as opcodes. We can implement an efficient NTT as long as we have cheap reductions/representations. Most/all cryptographic constructions use modular math at their base.

But I think we can get pretty far without evmmax by compiling math directly to Yul, especially with small field stuff. We can use lazy modular reduction + the existing mod opcode to get *fairly* cheap NTT’s. We’ve got 256 bits on every integer for free, may as well use it.

That said, the problem we have with most of this isn’t math/opcode related, it’s engineering. There’s no cross platform frontend for expressing/compiling programs in this way. Expressing such programs in Solidity is impossible because control flow dominates the gas cost.

---

**seresistvanandras** (2025-01-13):

In January, we plan to release an open-source library that implements the verification algorithm of several post-quantum secure digital signature schemes in Solidity. In the paper, we evaluate the gas costs of these verification algorithms using two verification modes: on-chain verification, where the entire signature scheme is verified on-chain, and using another, [optimistic verification mode called Naysayer verification](https://eprint.iacr.org/2023/1472.pdf). In this verification mode, on-chain, only a Merkle commitment \mathsf{com} to the signature \sigma is stored. We assume that there exists a data availability layer where the full signature is available. Subsequently, so-called, naysayers can send on-chain before a pre-defined time-out short proofs proving that the on-chain signature is *incorrect*. Proving the incorrectness of these large PQ signatures is typically much faster than verifying the entire signature. In the optimistic case, the on-chain smart contract does not do anything; it just stores the commitment \mathsf{com} in storage, though that storage slot, after the challenge period, can be overwritten.

Here are some preliminary results, just to give you an idea about the gas costs of verifying on-chain PQ signatures. MAYO is not ready yet, but it seems, it will be less efficient than the hash-based signature schemes.

[![image](https://ethresear.ch/uploads/default/optimized/3X/8/8/88b0586ebf26275dc5516da4fc3256ee7a49c877_2_690x110.png)image889×143 35.3 KB](https://ethresear.ch/uploads/default/88b0586ebf26275dc5516da4fc3256ee7a49c877)

---

**CPerezz** (2025-01-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/jchancehud/48/18762_2.png) JChanceHud:

> The lattice constructions should be really easy to prove provided we have wrong field math. iiuc they’re all purely (linear) algebraic.

I think the main issue is emulating floating-point arithmetic for polynomial rings. We can “decently efficiently” emulate prime fields.

But floating point is another type of monster. I don’t know any IEEE-compatible ZK circuit impls for floating point with standard precision.

Maybe I was under a wrong impression and floating point emulation isn’t needed? Though you seem to say the opposite.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/seresistvanandras/48/10229_2.png) seresistvanandras:

> In January, we plan to release an open-source library that implements the verification algorithm of several post-quantum secure digital signature schemes in Solidity.

[@seresistvanandras](/u/seresistvanandras) have the paper and/or lib been made public? Could you share some links if so?

---

**asanso** (2025-01-29):

here we go [Poqeth: Efficient, post-quantum signature verification on Ethereum](https://ethresear.ch/t/poqeth-efficient-post-quantum-signature-verification-on-ethereum/21554)

---

**CPerezz** (2025-01-29):

I realized yesterday! I reached out to organize a Learn & Share session already! So we’re covered! Thanks!!

I forgot to mention on my prev message, that we could actually see value on Native Stealth Address support.

There’s [some new work on PQ-stealth addr](https://eprint.iacr.org/2025/112) that would be cool to try adopting. (Though is only suitable for Kyber IIUC).

---

**rdubois-crypto** (2025-02-18):

We implemented a generic NTT in Yul, with examples provided for DILITHIUM and FALCON fields and reduction polynomial here:



      [github.com](https://github.com/ZKNoxHQ/NTT)




  ![image](https://opengraph.githubassets.com/2a38021c15f35358f675c5d03fff209a/ZKNoxHQ/NTT)



###



Generic implementation of the Number Theoretic Transform in the context of cryptography applications










Compared to available implementations, we cut FALCON gas cost from 24M to 3.6M, more optimizations being still WIP. However we are quite confident in the fact that it cannot be cut below 2M considering the number of required operations. As such going RIP/EIP is necessary for day to day transactions.

We believe that NTT has separate interest (speed up STARKS settlements, implement any lattice candidate) and proposed a related EIP:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/rdubois-crypto/48/12781_2.png)

      [NTT as PostQuantum and Starks settlements helper precompile](https://ethresear.ch/t/ntt-as-postquantum-and-starks-settlements-helper-precompile/21775)




> NTT-EIP as a building block for FALCON, DILITHIUM and Stark verifiers
> With the release of Willow cheap, the concern for quantum threat against Ethereum seems to accelerate. Posts by Asanso and PMiller summarize those stakes and possible solutions. Those solutions include use of lattice based signatures such as Dillithium or FALCON (the latter being more optimized for onchain constraints), STARKs and FHE. There is a consensus in the cryptographic research community around lattices as the future …

---

**seresistvanandras** (2025-02-18):

Super cool work on the NTT precompile [@rdubois-crypto](/u/rdubois-crypto). Just purely evaluating PQ signatures by EVM verification gas cost, I think one would choose WOTS+ (cca. 200k gas). One-time signatures (OTS) have already allowed us to survive in a post-quantum world since one can always sign the public key of the next transaction. Though, OTSs do not allow, for instance, “replace by fee” mechanism, since one would need to sign with the same secret key multiple times. Therefore, transactions could get stuck in the mempool, as this was previously observed in the Bitcoin community. I believe XMSS is on par with Falcon in terms of verification gas cost. I also think that MAYO (and possibly other 2nd round NIST contenders as well) might be good candidates given the upcoming EVM upgrades, e.g., SIMD operations for the EVM or EOF.

(lol. just realised that [@CPerezz](/u/cperezz) already brought this up above)

I want to bring in a new perspective to evaluate/benchmark PQ signature schemes that previously (at least not in this thread) were not considered in detail. It might be worthwhile to anticipate that people also want to use these signature schemes in (zero-knowledge) proof systems to prove various statements. So, it would also be interesting *to evaluate the ZK/MPC circuit-friendliness of the above-discussed verification algorithms* and, put differently, how amenable they are to proof systems. I’d assume that hash-based signatures will compose well with hash-based proof systems, while FALCON and DILITHIUM may perform better when proven with lattice-based proof systems. (???) It’d be cool to have a concrete analysis on this.


*(5 more replies not shown)*
