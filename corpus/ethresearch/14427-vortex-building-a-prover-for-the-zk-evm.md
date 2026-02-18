---
source: ethresearch
topic_id: 14427
title: "Vortex : building a prover for the zk-EVM"
author: Soleimani193
date: "2022-12-15"
category: zk-s[nt]arks
tags: [zk-roll-up]
url: https://ethresear.ch/t/vortex-building-a-prover-for-the-zk-evm/14427
views: 3587
likes: 10
posts_count: 2
---

# Vortex : building a prover for the zk-EVM

# Vortex : building a prover for the zk-EVM

*Alexandre Belling and  Azam Soleimanian,   ConsenSys R&D*

In this post, we present the recent developments of the proof system that we are using for Consensys’ zk-EVM, first presented in [this post](https://ethresear.ch/t/a-zk-evm-specification/11549) and then further expanded in [this post](https://ethresear.ch/t/a-zk-evm-specification-part-2/13903). While our proof system is still under development and will gradually be improved over time, its most recent version is described in [this paper](https://eprint.iacr.org/2022/1633.pdf).

## The structure of the prover

The proof system is mainly organized as a successive-compilation-step architecture. The “Arithmetization” is the set of constraints as expressed in the original posts. At a high level, the zk-EVM arithmetization describes the EVM as a set of registers and their values over time (e.g columns). The columns constituting the zk-EVM are bound to each other by constraints of various natures (inclusion, permutations, arithmetic constraints, etc). For more details, we advise the reader to go through the above-mentioned posts.

[![](https://ethresear.ch/uploads/default/original/2X/7/791e6b5de366a985fb341c95b3749d62595831ff.png)652×183 9.29 KB](https://ethresear.ch/uploads/default/791e6b5de366a985fb341c95b3749d62595831ff)

Thereafter, the zk-EVM arithmetization is compiled by **Arcane**, whose role is to convert the zk-EVM arithmetization into a polynomial-IOP. It mainly leverages known techniques from Halo2, Plonk, Cairo, etc. From then on, we instantiate the polynomial-IOP into a concrete proof system using **Vortex**, a polynomial commitment scheme at the core of our proof system. Vortex is a plausibly post-quantum and transparent polynomial commitment scheme based on a lattice hash function. Although Vortex has O(\sqrt{n}) proof size and verification time, it is equipped with a *Self-Recursion* mechanism which allows compressing the proof iteratively.

Once the proof is shrunk *enough* through self-recursion, we add a final compression step using an outer-proof system (today Groth16, Plonk in the future). This final compression step ensures that the proof is verifiable on Ethereum.

## Lattice-based Hash function

As mentioned in the above section, Vortex makes use of a hash function based on the Short Integer Solution (SIS) (and its usual variants). We think it offers the best tradeoffs between security, computation speed, and arithmetization-friendliness.

- Security: the collision and preimage resistance of our hash function are directly reducible to SIS. Additionally, with the recent developments of NIST-PQC contest, the research community has developed numerous frameworks to benchmark the hardness of lattice problems.
- Execution-speed on CPU: ring-SIS hash functions require computing many small FFTs for each. This makes them an order of magnitude faster than EC operations (even with MSM optimization) and other SNARK-friendly hash functions.
- The hash function can potentially work with any field (in fact, it’s not even required to have a field). This makes them easier to use for recursion.
- They are somewhat arithmetic-friendly: all that is required to verify SIS hashes in a SNARK are range-checks and linear combinations with constants.

## Status of the implementation

While the implementation work of the prover is in progress, we have already implemented a good part of it. In the current stage of the implementation we have;

- The prover relies on the bn254 scalar field all the way from the arithmetization to the outer-proof
- The SIS hash instance relies on the “original” SIS assumption (i.e. not the ring one) and uses n=2 and bound=2^3 on the bn254 scalar field. While it is in theory the slowest set of parameters that we present in the paper, it is also the simplest to optimize. With that, our hash function has a running time of ~500N ns where N is the number of field elements to hash

With the latest progress of the arithmetization and of the prover implementation, we are able to prove the execution of

- A 30M gas mainnet block,
- On a 96 cores machine with 384 GB of RAM (hpc6a.48xlarge on AWS)
- In 5 minutes (only including the inner-proof)

## Replies

**Soleimani193** (2022-12-22):

Here we present the concrete SIS parameters for Vortex. While the analysis presented in the appendix of the paper accounts for all known attacks against SIS, equation (4) was missing a factor 1/2. The correct formula is

\log \delta = \frac{1}{2m_0(k-1)} (m_0 - 1 + \frac{k(k-2)}{m_0}) \log \gamma_k \text{ with }\log \gamma_k\approx \mathbf{\frac{1}{2}}\log (k/2\pi e)

Since the concrete parameters shielding against the BKZ attack are extracted from this formula, its application led to some erroneous parameter sets. The downside of this adjustment is a potential loss in performance by a (multiplicative) factor \leq 2. The optimal set of parameters will be determined once the implementation is optimized.

[The updated version](https://eprint.iacr.org/2022/1633.pdf) of the paper is  available on eprint. In the meantime, we provide an updated table, where q denotes the modulus of the underlying field, \beta the maximal preimage value (i.e., the SIS solution should have entries no larger than [0:\beta) and n denotes the number of field elements in the hash output.

We would like to thank Zhenfei Zhang for pointing out an issue with some of the parameter sets in the initial version of the paper. Tracking down the origin of this discrepancy allowed us to identify the underlying mistake in formula (4).

| log_2(q) | log_2(\beta) | n | BKZ attack | CPW attack |
| --- | --- | --- | --- | --- |
| 64 | 2 | 32 | 182.17 | 144.0 |
| 64 | 4 | 64 | 147.31 | 305.57 |
| 64 | 6 | 128 | 166.13 | 598.14 |
| 64 | 10 | 256 | 149.93 | 1272.31 |
| 64 | 16 | 512 | 136.4 | 2741.67 |
| 64 | 22 | 1024 | 160.7 | 5967.82 |
| 254 | 2 | 7 | 157.7 | 259.03 |
| 254 | 4 | 16 | 146.1 | 270.0 |
| 254 | 6 | 32 | 164.73 | 637.0 |
| 254 | 10 | 64 | 148.63 | 1262.46 |
| 254 | 16 | 128 | 135.18 | 2720.33 |
| 254 | 24 | 256 | 133.28 | 5921.27 |
| 254 | 32 | 512 | 164.03 | 13013.8 |

