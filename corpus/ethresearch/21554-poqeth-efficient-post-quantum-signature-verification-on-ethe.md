---
source: ethresearch
topic_id: 21554
title: "Poqeth: Efficient, post-quantum signature verification on Ethereum"
author: seresistvanandras
date: "2025-01-22"
category: Cryptography
tags: [post-quantum]
url: https://ethresear.ch/t/poqeth-efficient-post-quantum-signature-verification-on-ethereum/21554
views: 466
likes: 4
posts_count: 1
---

# Poqeth: Efficient, post-quantum signature verification on Ethereum

**TL,DR:** We anticipate a future with account abstraction and quantum computers. In this, perhaps not-so-distant future, post-quantum signatures will be verified by on-chain contracts. In this new work, we implement and evaluate the gas cost of verifying four post-quantum signatures on-chain:  WOTS+, XMSS, SPHINS+, and MAYO. We invite the community to review, extend, and collaborate with us on **poqeth**, an open-source library that implements these verification algorithms in Solidity. We expect massive gas-cost improvements in the future. PRs, issues, comments and questions are welcome!

**poqeth** *Eprint*: https://eprint.iacr.org/2025/091.pdf

**poqeth** *Github repo*: [GitHub - ruslan-ilesik/poqeth: poqeth: Efficient, post-quantum signature verification on Ethereum](https://github.com/ruslan-ilesik/poqeth/)

[![image](https://ethresear.ch/uploads/default/original/3X/8/1/81e8aea5ed0b25904bf0022ce180712120568550.png)image926×180 13.6 KB](https://ethresear.ch/uploads/default/81e8aea5ed0b25904bf0022ce180712120568550)

**How to choose an appropriate post-quantum signature scheme for Ethereum transactions?**

Choosing the right digital signature for Ethereum is non-trivial as the blockchain context has completely different limitations than, say, TLS. Large public keys are a no-go in the context of Ethereum. For more discussion, see the intro of our paper or [Antonio’s latest ethresear.ch post](https://ethresear.ch/t/falcon-as-an-ethereum-transaction-signature-the-good-the-bad-and-the-gnarly/).

One thing for sure: “The proof of the pudding is in the eating”; that is, we need to implement these signature schemes’ verification algorithms to get a real sense how fast they can be in the EVM.

This is exactly what we did in **poqeth**.

**Two evaluated verification modes**

We considered two verification modes: 1) on-chain verification, when the full signature is verified by the contract 2) [Naysayer verification mode](https://eprint.iacr.org/2023/1472.pdf).

In the Naysayer verification mode, the contract only needs to check the signature if the signature is faulty, and even in that case, the contract only needs to be convinced about the *incorrectness of the signature*, which can be done much faster than verifying the entire signature.

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/0/b0eeb89814ecf68e52fc83df25bb65757c2edeb9_2_690x265.png)image1419×547 101 KB](https://ethresear.ch/uploads/default/b0eeb89814ecf68e52fc83df25bb65757c2edeb9)

**poqeth**: *an extendible contract library for post-quantum signature verification on Ethereum*

We decided to implement and evaluate three hash-based signature schemes (WOTS+, XMSS, and SPHINCS+) and a multivariate-quadratic signature scheme, MAYO. For each scheme, we propose optimal parameter choices that minimize the on-chain verification cost at NIST security level 1.

*Future directions and open research problems:*

- Precompile contracts in the EVM for PQ signature verification: shall we enshrine some signature verification algorithms in the EVM? There are already two EIPs advocating for this in the case of Falcon. See EIP-7592 and EIP-7619. Or the protocol should just be more modular and only support, say SIMD operations, that would significantly speed up multivariate-quadratic signatures, such as MAYO.
- Succinct proofs of signature verification. maybe in the future, we should just use very on-chain STARK proofs that attest to the validity of a bunch of PQ signatures. This approach can effectively amortize the verification cost of numerous PQ signatures. A similar approach is taken in a recent paper by Drake, Khovratovich, Kudinov and Wagner. See also this great work.
- Benchmarking more post-quantum signature algorithms: it’d be cool to extend the poqeth library with the implementation and evaluation of more PQ signatures. Please hit us up, if you are interested in working together on this topic.
