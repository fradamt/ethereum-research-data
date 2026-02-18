---
source: ethresearch
topic_id: 23966
title: "zkFOCIL: Implementation & Benchmarking Report"
author: shreyas-londhe
date: "2026-01-28"
category: Cryptography
tags: [censorship-resistance]
url: https://ethresear.ch/t/zkfocil-implementation-benchmarking-report/23966
views: 166
likes: 6
posts_count: 1
---

# zkFOCIL: Implementation & Benchmarking Report

*by [Shreyas Londhe](https://x.com/shreyas_twts) and [Suyash Bagad](https://x.com/BagadSuyash).*

## Motivation

We implemented and benchmarked the Linkable Ring Signature scheme proposed in [zkFOCIL](https://ethresear.ch/t/zkfocil-inclusion-list-privacy-using-linkable-ring-signatures/21688). By providing a privacy-preserving mechanism for the Inclusion List committee, this work explores a path toward enhancing Ethereum’s censorship resistance without exposing individual validators to coercion.

The [FOCIL](https://eips.ethereum.org/EIPS/eip-7805) proposal (EIP-7805) intends to enhance Ethereum’s censorship resistance by forcing the block proposer to include a set of transactions published by a small set of validators called Includers. Since the Includers are known to the block proposer, it can threaten them to censor some transactions. The zkFOCIL proposal addresses this by using a Ring-signature based approach to maintain anonymity of the Inclusion Iist Committee.

Our goal was to implement and benchmark the SNARK-based instantiation of the LRS scheme as described in zkFOCIL, comparing prover and verifier performance across different proof systems and commitment schemes. The benchmarking results with Barretenberg give us some hope of making zkFOCIL practical, but there is work still needed to bring down the verification times and proof sizes to an acceptable level.

## Overview

We implemented the zkFOCIL circuit in Barretenberg (C++) using the UltraHonk proof system with IPA as the polynomial commitment scheme. **We use IPA (transparent setup) to avoid introducing any new trusted setup for validators.**

The implementation uses the BN254 curve for validator keys. In practice, validator keys are on the BLS12-381 curve, but since Barretenberg does not currently support BLS curves, we use BN254 for this initial version. This is an important caveat: actual performance with BLS12-381 keys will differ due to the different field sizes.

For completeness, we also benchmarked using Noir (with both Barretenberg and Provekit backends) which supports BLS12-381, though with higher proving times due to non-native field arithmetic[[1]](#footnote-58123-1).

## SNARK Circuit Design

Let N be the total number of validators and \mathbb{V} denote the set of public keys of all validators. The set \mathbb{V} is public.

\mathbb{V} = \{ P_1, P_2, P_3, \ \dots \ , P_N \}

Suppose validator P_j for some j \in [N] was chosen as an Includer in slot t. The validator computes its key-image K_j for slot t and publishes the tuple (K_j, \textsf{IL}_j) where \textsf{IL}_j is its Inclusion list[[2]](#footnote-58123-2). From the key-image K_j, the block proposer can check if this validator was indeed chosen as a member of the IL committee in slot t. However, the validator still needs to prove to the block proposer that:

- The key-image K_j was correctly computed, and indeed corresponds to P_j,
- It is an active validator, i.e., P_j \in \mathbb{V}.

The validator does so by generating a SNARK proof with the following structure:

**Private inputs**:

1. Validator’s secret key s_j \in \mathbb{F}_q
2. Validator’s public key P_j \in \mathbb{G}
3. Merkle path at index j in the tree of validator public keys

**Public inputs**:

1. The key-image K_j
2. The slot t
3. Merkle tree root

**Constraints**:

1. Check if the validator public key is correct: s_j \cdot G \stackrel{?}{=} P_j
2. Check if the key-image is correct: H_1(s_j, t) \cdot G \stackrel{?}{=} K_j
3. Check if the Merkle path from index j (corresponding to P_j) to the root is correct

## Circuit Structure

The total circuit size is **55,554 gates** (dyadic circuit size is 2^{16}). The circuit size with existing barretenberg backend was 111,227 (dyadic circuit size 2^{17}. We implemented several optimisations to the barretenberg backend to bring down the circuit size to 2^{16}.

The dominant cost in the circuit is due to the scalar multiplication (non-native arithmetic). Below is the breakdown of gate-count:

| Component | Gate Count | % of Total |
| --- | --- | --- |
| Input witnesses and setup | 3,928 | 7.07% |
| Public key verification (scalar mul) | 21,508 | 38.73% |
| Blake2s hash (key image secret) | 3,288 | 5.92% |
| Key image verification (scalar mul) | 21,499 | 38.71% |
| Blake2s hash (leaf value) | 3,275 | 5.90% |
| Merkle path verification (Poseidon2) | 1,601 | 2.88% |
| Total | 55,554 | 100.00% |

The two scalar multiplications contribute to **~77% of the total gate count**. Both scalar multiplications involve the group generator G. We implemented a series of optimisations in the Barretenberg backend to reduce the gate-count of one scalar multiplication to ~21,500 gates. It seems difficult to further reduce the cost of a scalar multiplication without changing the gate width (which will increase prover costs).

## Benchmarking Results

We benchmarked the Barretenberg implementation on the following machine: Intel(R) Xeon(R) CPU @ 2.20GHz, 8-core (16 vCPU), 64GB RAM[[3]](#footnote-58123-3).

| Parameter | Value |
| --- | --- |
| Curve (for validator keys) | BN254 |
| Trusted setup | No |
| Circuit size (gates) | 55,554 |
| Proof size (bytes) | 7,744 |
| Proof generation (ms) | 1,314 |
| Witness generation (ms) | 235 |
| Proof verification (ms) | 55.7 |

### Gap Analysis

zkFOCIL with Barretenberg (IPA) is not yet practical, but the path forward is clear. The table below summarises the gaps against the [performance requirements](https://ethresear.ch/t/zkfocil-inclusion-list-privacy-using-linkable-ring-signatures/21688#p-52756-performance-requirements-13) from the original zkFOCIL proposal:

| Metric | Current | Target | Status |
| --- | --- | --- | --- |
| Prover time | ~1.5s | <12s |  |
| Verification time | ~50ms | <20ms |  |
| Proof size | ~7.7kB | <1.5kB |  |

**Prover Time**: The prover time of ≈1.5 seconds is acceptable given Ethereum’s 12-second block time.

**Verification Time (Main Bottleneck)**: The verification time of ≈50 milliseconds is 2.5x slower than our target of 20 milliseconds. Since all validators must verify 16 zkFOCIL proofs per slot, this is the critical bottleneck. The slower verification with IPA stems from its linear verification costs.

**Proof Size**: The proof size of ≈7.7 kB is ~5x larger than the permissible 1.5 kB.

### Prover and Verifier Time Breakdown

The UltraHonk prover algorithm is executed in three phases:

1. Witness generation: fills the circuit trace table
2. Oink phase: commits to all trace polynomials, computes other witness polynomials (like grand product polynomial) and commits to them
3. Decider phase: proves those commitments satisfy UltraPlonk constraints via sumcheck + openings (using polynomial commitment scheme)

For a total prover time of 1387 ms, here’s the prover breakdown:

| Component | Time (ms) | % of Total |
| --- | --- | --- |
| Witness generation | 103.0 | 7.4% |
| Oink phase (commit) | 130.7 | 9.4% |
| Decider phase (Sumcheck and PCS) |  |  |
| \quad\circ Sumcheck | 109.3 | 7.9% |
| \quad\circ Gemini (multi-variate to univariate) | 146.3 | 10.5% |
| \quad\circ IPA (univariate evaluation) | 868.2 | 62.6% |
| Total | 1387.0 | 100.0% |

Clearly, the decider phase dominates the prover costs. Specifically, the PCS (Gemini and IPA) contributes to ~73% of the prover runtime. Proving univariate evaluation with IPA is costly because of the \mathcal{O}(\textsf{log}(n)) scalar multiplications.

The verification algorithm is also dominated by the scalar multiplication required by the IPA verifier. The verifier profiling, with total verification time of ~59.4 ms, is as follows:

| Component | Time (ms) | % of Total |
| --- | --- | --- |
| OinkVerifier | 0.4 | 0.7% |
| Sumcheck verify | 2.1 | 3.5% |
| Shplemini (batch opening claim) | 0.8 | 1.4% |
| IPA verify | 55.7 | 93.8% |
| Total | 59.4 | 100.0% |

Here, the IPA verification is the dominant component with a 94% share in verifier runtime.

## Comparison with Other Approaches

For completeness, we also benchmarked using KZG (which requires a trusted setup), Noir with its default Barretenberg backend, and Provekit (a Spartan+WHIR-based proving system):

| Parameter | Noir + BB | Noir + Provekit | BB (KZG) | BB (IPA) |
| --- | --- | --- | --- | --- |
| Curve (for validator keys) | BLS12-381 | BLS12-381 | BN254 | BN254 |
| Trusted setup | Yes | No | Yes | No |
| Circuit size | 411,284 | 641,466 (R1CS) | 55,554 | 55,554 |
| Proof size (bytes) | 3,456 | 528,000 | 6,688 | 7,744 |
| Proof generation (ms) | 22,074 | 5,120 | 434 | 1,314 |
| Witness generation (ms) | 6,281 | 913 | 265 | 235 |
| Proof verification (ms) | 64.9 | 92.5 | 9.8 | 55.7 |

**Key observations**:

- KZG verification (9.8 ms) meets our target of

1. Barrentenberg also uses non-native arithmetic to do BN254 Scalar Mults but it uses an optimised CRT based algorithm which results in much lower gate count compared to naive algorithms used in Noir. ↩︎
2. An Inlcusion List is a list of transactions curated by an Includer by looking at their local mempool. ↩︎
3. This is the reference machine used by validators as mentioned in the Ethereum Staking guide. ↩︎
