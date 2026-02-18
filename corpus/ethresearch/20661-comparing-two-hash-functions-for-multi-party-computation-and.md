---
source: ethresearch
topic_id: 20661
title: Comparing Two Hash Functions for Multi-Party Computation and Zero-Knowledge
author: burcu-yildiz
date: "2024-10-15"
category: Cryptography
tags: []
url: https://ethresear.ch/t/comparing-two-hash-functions-for-multi-party-computation-and-zero-knowledge/20661
views: 308
likes: 4
posts_count: 1
---

# Comparing Two Hash Functions for Multi-Party Computation and Zero-Knowledge

**[Comparing Two Hash Functions for Multi-Party Computation and Zero-Knowledge](https://zenodo.org/records/13739511)**

*by Burcu Yıldız (Anoma - https://anoma.network/) and Mary Maller (Ethereum Foundation - https://ethereum.foundation/)*

TL;DR; In our report [Comparing Two Hash Functions for Multi-Party Computation and Zero-Knowledge](https://zenodo.org/records/13739511), we compare hash functions Poseidon and Hydra for multi-party computation (MPC) and zero-knowledge proofs (ZKPs). Our observations suggest better efficiency using Hydra.

**MPC and ZKP**

Zero-knowledge proofs (ZKPs) and MPCs are both examples of advanced cryptographic applications that are useful for privacy and integrity. In a zero-knowledge proof, a single party demonstrates that the output of a computation has been computed correctly without revealing any secret input values. In an MPC, multiple parties compute the output of a computation without revealing any secret input values to each other. Joint use of ZKP and MPC solutions are promising for different applications, including Anoma’s private solving protocol. Main efficiency measures are the number of R1CS constraints for ZKPs and the number of rounds and multiplication triples for MPCs, all of which fundamentally depends on the number of non-linear operations. However, the exact dependency on non-linear operations, and consequently the optimizations, are different for MPCs and ZKPs.

**Hash functions**

Cryptographic hash functions are a paramount building block in cryptography and are used for numerous applications. The hash function Poseidon is widely favored for zero-knowledge applications (e.g. [FileCoin](https://github.com/filecoin-project/neptune) , [Dusk Network](https://github.com/dusk-network/Poseidon252), [LoopRing](https://tinyurl.com/y7tl537o)), and has been tailor designed for this purpose. The hash function Hydra is proposed and optimized to be computed in MPC. Hydra was presented in Eurocrypt 2023 and has less total number of rounds and transmitted data than its competitors. We answer following question in our report:

*How do the hash functions Poseidon and Hydra, which are optimized for zero-knowledge and MPC applications, respectively, perform for the other application?*

**Our techniques**

Our comparison of Poseidon and Hydra consists of theoretical and experimental components, aiming 128 bits of security on Pallas curve (a 255-bit prime field). By computing multiplicative depth and multiplicative complexities of algorithms, we theoretically estimate the efficiency of hash functions by the number of R1CS constraints for ZKP; by the number of rounds and multiplication triples required for MPC. Our experimental results include benchmarks of MPC protocols to obtain an estimate of total running times, amount of exchanged data, and CPU time of each party. We visually present our results with respect to different lengths of output, number of parties, and parameters of Poseidon, when they are applicable.

Furthermore, we investigate Poseidon and Hydra as a building block for symmetric key encryption. We consider the Duplex Sponge authenticated encryption framework for Poseidon and stream cipher for Hydra, as suggested by the paper introducing Hydra. We report similar comparisons as described in the previous paragraph.

**Results**

We observe that Hydra, in general, outperforms Poseidon for the efficiency measures of our interest. Hydra is especially efficient when the desired length for digest is long, e.g. if it is used as a PRNG. On the other hand, Hydra is limited to a certain input length while Poseidon accepts various input lengths. Poseidon’s various parameters enable optimizing the performance if the input/output lengths are fixed and known in advance; although Hydra still seems to outperform.

Hydra is more efficient to compute when a long plaintext needs to be encrypted. However, there does not exist any (theoretical or practical) implementation of authenticated encryption based on Hydra, although a way is mentioned by its paper. Our considerations for Poseidon are already for authenticated encryption.

Readers are invited to check [our report](https://zenodo.org/records/13739511) for more details on the hash functions, our setup, results and discussion (including considerations for constructing a hash function for MPC and ZKP applications).
