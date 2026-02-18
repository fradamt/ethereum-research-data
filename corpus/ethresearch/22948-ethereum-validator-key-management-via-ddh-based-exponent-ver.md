---
source: ethresearch
topic_id: 22948
title: Ethereum Validator Key Management via DDH-Based Exponent Verifiable Random Functions (eVRF)
author: BonyaO
date: "2025-08-21"
category: Cryptography
tags: []
url: https://ethresear.ch/t/ethereum-validator-key-management-via-ddh-based-exponent-verifiable-random-functions-evrf/22948
views: 247
likes: 2
posts_count: 1
---

# Ethereum Validator Key Management via DDH-Based Exponent Verifiable Random Functions (eVRF)

# Ethereum Validator Key Management via DDH-Based Exponent Verifiable Random Functions (eVRF)

*Authors: Yecheke Bonya Oryn Bonya and Antonio Sanso*

As Ethereum and other blockchain platforms evolve towards more scalable and secure consensus mechanisms, the demand for **verifiable randomness** becomes increasingly critical. In Proof-of-Stake (PoS) systems, randomness drives validator selection, leader election, and committee formation—processes that must be both unpredictable and publicly verifiable to maintain system integrity.

A **Verifiable Random Function (VRF)** allows a prover to generate a pseudorandom output together with a proof that this output was correctly computed from a given input and secret key. The proof can be verified publicly without revealing the secret key.

A recent variant, the **Exponent VRF (eVRF)**, introduced by [Boneh et al. (2025)](https://link.springer.com/chapter/10.1007/978-3-031-91098-2_8), outputs randomness “in the exponent” of a cryptographic group, enabling enhanced privacy, threshold capabilities, and algebraic composability.

In this post, we focus on **DDH-based eVRFs**, whose security relies on the Decisional Diffie-Hellman (DDH) assumption, alongside an efficient **zero-knowledge proof** protocol for proving correct eVRF evaluations without leaking any secret information.

Our implementation uses two elliptic curves:

- BLS12-381 – a widely adopted pairing-friendly curve used in Ethereum’s validator signature scheme, offering strong security (128-bit) and efficient pairing operations essential for aggregate signatures and other advanced cryptographic protocols…
- Bandersnatch – an elliptic curve defined over the BLS12-381 scalar field, optimised for fast scalar multiplication via the GLV endomorphism.

By combining these curves, we achieve both **efficient computations** and **compatibility** with existing Ethereum cryptographic infrastructure.

---

## Background: VRFs and eVRFs

### Verifiable Random Functions (VRFs)

A VRF is a tuple of polynomial-time algorithms (PPGen, KGen, Eval, Verify) with the following specifications:

- PPGen(1^\lambda) → pp: Public parameter generation algorithm that takes a security parameter \lambda and outputs public parameters pp
- KGen(1^\lambda) → (sk, pk): Key generation algorithm that outputs a secret/public key pair
- Eval(sk, x) → (y, \pi): Evaluation algorithm that takes the secret key and input x, producing:

y: A pseudorandom output
- \pi: A proof of correct computation

**Verify(pk, x, y, \pi) → \{0, 1\}**: Verification algorithm that accepts or rejects the proof

The VRF must satisfy four critical security properties:

1. Correctness: For all honestly generated keys and inputs, verification always succeeds on honestly computed outputs and proofs
2. Uniqueness: For any input x and public key pk, there exists at most one value y for which a valid proof can be constructed
3. Pseudorandomness: The output y is computationally indistinguishable from random for any input not previously queried
4. Verifiability: No adversary can produce a valid proof for an incorrect output

VRFs are already deployed in production blockchain systems. Algorand uses them for cryptographic sortition in committee selection, while Cardano employs them in their Ouroboros Praos consensus protocol for leader election. Chainlink’s Verifiable Random Function (VRF) service is a verifiable random number generator (RNG) that creates provably random outputs for decentralised Apps and other applications needing on-chain randomness. VRFs are also used for Aggregator selection in Ethereum.

### Exponent VRFs (eVRFs)

The eVRF represents a fundamental modification to the VRF output format with significant implications for privacy and composability:

Let \mathbb{G} be a group of prime order q with generator G. An exponent VRF (eVRF) consists of polynomial-time non-uniform algorithms (PPGen, KGen, Eval, Verify) where:

- PPGen(1^\lambda) → pp: Public-parameters generation algorithm
- KGen(1^\lambda) → (sk, pk): Key generation outputs secret key sk and public key pk
- Eval(sk, x) → (y, Y, \pi) where:

y ∈ \mathbb{Z}_q: The actual pseudorandom value (kept private)
- Y = y · G ∈ \mathbb{G}: The output “in the exponent”
- \pi: Zero-knowledge proof of correct computation

Verify(pk, x, Y, \pi) → \{0, 1\}: Verification checks the proof without learning y

The security properties for eVRFs parallel those of standard VRFs, with additional considerations:

1. Simulatability: There exists a simulator that can produce indistinguishable proofs without knowledge of the secret key

The key distinction lies in the output format: while standard VRFs reveal y directly, eVRFs only reveal Y = y · G, keeping the actual random value y hidden “in the exponent.”

---

## Mathematical Constructions

We present two DDH-based eVRF constructions: the basic construction and the full construction. The basic construction provides efficient operation but covers approximately half of the group elements in the domain. The full construction extends coverage to all group elements through the application of the leftover hash lemma, ensuring complete domain coverage at the cost of additional computational overhead.

In our implementation, Bandersnatch serves as the source curve (\mathbb{G}_S) while BLS12-381 is used as the target curve (\mathbb{G}_T), leveraging the compatibility between these curves where the scalar field of BLS12-381 equals the base field of Bandersnatch.

### 1. Basic DDH-Based eVRF

Let (\mathbb{G}_S, \mathbb{G}_T) be a group pair with |\mathbb{G}_S| = s, |\mathbb{G}_T| = q, and \ell = \lfloor \log_2 \min(s, q) \rfloor - 1.

Let G_{T,1}, G_{T,2} be generators of G_T.

Let H : \mathcal{X} \times \mathbb{G}_T \to \mathbb{G}_S^* be a hash-to-curve function.

**Key Generation**

k \xleftarrow{\$} [2^{\ell+1} - 1], \quad Q = k \cdot G_{T,1}

Output sk = k, vk = Q.

**Evaluation**

1. Q \gets k \cdot G_{T,1}
2. X \gets H(x, Q) \in \mathbb{G}_S^*
3. P \gets k \cdot X with P = (x_P, y_P) \in \mathbb{F}_q^2
4. y \gets x_P \in \mathbb{F}_q
5. Y \gets y \cdot G_{T,2} \in \mathbb{G}_T
6. Produce proof \pi for relation:

R_{\text{eDDH}} = \{ (Q, X, Y) : k \ |\ Q = k \cdot G_{T,1},\ Y = x_P \cdot G_{T,2},\ P = k \cdot X \}

**Verification**

Check \pi validates (Q, H(x, Q), Y) \in R_{\text{eDDH}}.

---

### 2. Full DDH-Based eVRF

Extends the basic construction with an additional scalar k' and two hash points.

Let H_1, H_2 : \mathcal{X} \times \mathbb{G}_T \to \mathbb{G}_S^* be independent hash functions.

**Key Generation**

k \xleftarrow{\$} [2^{\ell+1} - 1], \quad k' \xleftarrow{\$} \mathbb{F}_q, \quad Q = k \cdot G_{T,1}

Output sk = (k, k'), vk = (Q, k').

**Evaluation**

1. Q \gets k \cdot G_{T,1}
2. X_1 \gets H_1(x, Q), X_2 \gets H_2(x, Q) \in \mathbb{G}_S^*
3. P_1 \gets k \cdot X_1, P_2 \gets k \cdot X_2
4. y \gets k' \cdot x_{P_1} + x_{P_2} \in \mathbb{F}_q
5. Y \gets y \cdot G_{T,2} \in \mathbb{G}_T
6. Produce proof \pi for relation:

R^*_{\text{eDDH}} = \{ (Q, k', X_1, X_2, Y) : k \ |\ Q = k \cdot G_{T,1},\ Y = y \cdot G_{T,2},\ y = k' x_{P_1} + x_{P_2} \}

**Verification**

Check \pi validates (Q, k', H_1(x, Q), H_2(x, Q), Y) \in R^*_{\text{eDDH}}.

---

## Proof Protocol

To prove correct eVRF evaluation without revealing secret information, we implement a zero-knowledge proof system based on **Bulletproofs for R1CS** with [Segev’s](https://eprint.iacr.org/2025/327) refinement. Our protocol compiles both relations R_{\text{eDDH}} and R^*_{\text{eDDH}} into structured constraint systems.

### The R1CS Framework

The foundation of our proof system is the refined R1CS relation for Bulletproofs. Bulletproofs were originally introduced by Benedikt Bünz et al. in [2018](https://eprint.iacr.org/2017/1066.pdf) as a significant advancement in zero-knowledge proof systems, offering logarithmic-sized proofs without requiring a trusted setup. At their core, Bulletproofs are based on the inner-product argument, which allows proving knowledge of vectors through an elegant recursive approach that reduces the dimension of the vectors in each round.

A R1CS instance is defined by matrices A, B, C \in \mathbb{Z}_q^{m \times n} and a witness vector z \in \mathbb{Z}_q^n that must satisfy:

Az \circ Bz = Cz

where \circ denotes the Hadamard (element-wise) product. The R1CS relation captures the precise set of instances for which both completeness and soundness hold without compromising performance.

### Schnorr Proof Integration

To establish the discrete logarithm relationships that underpin the eVRF security model, we employ Schnorr proofs at two critical points in our protocol. The first Schnorr proof, denoted \pi_Q, establishes that the prover knows the secret key k such that Q = k \cdot G_{T,1}. This proof is essential for binding the public key to the secret used in the eVRF evaluation, ensuring that only the legitimate key holder can generate valid proofs. The second Schnorr proof, \pi_Y, demonstrates knowledge of the value y such that Y = y \cdot G_{T,2}, directly linking the eVRF output to the computed result. These Schnorr proofs follow the standard three-move protocol structure but are rendered non-interactive through the Fiat-Shamir transformation, where challenge values are generated using a cryptographic hash function applied to the commitment and public parameters.

### Bulletproof Protocol Execution

The core of our proof system implements the refined Bulletproofs protocol for R1CS*, which provides the zero-knowledge argument for constraint satisfaction.

The execution begins with a setup phase where public parameters are established, including the group \mathbb{G} of prime order q and generators \mathbf{G}, \mathbf{H} \in \mathbb{G}^{n+m} along with additional generators G, H \in \mathbb{G}. The prover holds an instance (T, A, B, C) representing the commitment and constraint matrices, along with a witness (x, x', y, y', \eta) that satisfies the R1CS* relation requirements with z = (x||y) and  z' = (x'||y').

In the commitment generation phase, the prover samples randomness

r \xleftarrow{\$} \mathbb{Z}_q

and constructs the commitment:

S = \langle ((x' \| y) \| Az), \mathbf{G} \rangle + \langle (0^n \| Bz), \mathbf{H} \rangle + r \cdot H

The prover then uses Fiat-Shamir’s transformation and generates the challenges \alpha, \beta, \gamma, \delta deterministically from the commitment and public parameters using a cryptographic hash function which are used to create linear combinations of the constraint equations.

The protocol proceeds through a sophisticated inner product argument that recursively reduces the dimensionality of the proof. This recursive structure achieves logarithmic proof size O(\log n) where n represents the number of constraints, making the system practical even for complex eVRF constructions with hundreds of constraints.

The final verification step confirms that all constraints are satisfied through a single inner product check, completing the zero-knowledge argument. The entire protocol maintains security through careful randomisation at each step, ensuring that no information about the witness leaks to the verifier while providing confidence in the correctness of the eVRF evaluation.

Our implementation combines these three proof components—the discrete logarithm Schnorr proofs and the R1CS* Bulletproof—into a unified argument \pi = \{\pi_Q, \pi_Y, \pi_{BP}\} that provides complete verification of eVRF correctness with logarithmic communication complexity and no trusted setup requirements.

---

## BLS Validator Key Generation

In Ethereum’s Proof-of-Stake consensus mechanism, each validator must operate with a unique **BLS12-381 key pair** to participate in the network’s consensus process. These cryptographic keys are fundamental to the security architecture because they are used to sign critical consensus messages including attestations (votes on blockchain state), block proposals, and validator duties assignments. The integrity of the entire validator set depends on the secure generation, storage, and proper usage of these keys.

With Ethereum’s updated staking requirements, validators can now stake between **32 ETH and 2,048 ETH per validator identity**, supporting both individual solo validators and large institutional operators running extensive validator sets. This flexibility enables institutions to efficiently manage capital allocation while encouraging broader validator participation across different scales of operation.

However, this design creates significant operational challenges for large-scale validator operators. Staking pools, exchanges, and institutional validators running hundreds or thousands of validators must manage correspondingly large numbers of BLS keys. This scenario introduces critical vulnerabilities:

1. Key Management Overhead — Securely storing, backing up, and tracking thousands of private keys requires sophisticated infrastructure and increases operational complexity exponentially. Each key must be individually secured, creating logistical challenges in key rotation, backup procedures, and access control systems.
2. Attack Surface Expansion — Each additional private key represents a potential compromise point. If any single validator key is leaked or compromised, the operator faces immediate risks including slashing penalties (automatic reduction of staked ETH for protocol violations), potential loss of validator status, and reputational damage that could affect their entire operation.
3. Operational Risk Amplification — Traditional key management approaches scale poorly, with the risk of human error, system failures, or security breaches increasing proportionally with the number of keys managed.

To address these challenges, our implementation introduces a **deterministic validator key derivation scheme** that leverages the mathematical properties of DDH-based eVRFs to transform key management from an O(n) complexity problem to an O(1) solution.

We employ a hierarchical key derivation architecture that reimagines validator key management. Instead of generating independent keys for each validator, we use a single Bandersnatch master key as the cryptographic root of trust, from which all validator keys are deterministically derived using the eVRF evaluation function.

### Master Key Generation and eVRF-Based Derivation

The derivation process begins with the generation of a **Bandersnatch master keypair**. Let (\mathbb{G}_s, \mathbb{G}_T) be the group pair where |\mathbb{G}_s| = s and |\mathbb{G}_T| = q, with \ell = \lfloor \log_2 \min(s, q) \rfloor - 1.

**Master Key Generation:**

k \xleftarrow{\$} [2^{\ell+1} - 1], \quad Q = k \cdot G_{T,1}

where sk_{\text{master}} = k and vk_{\text{master}} = Q.

**Deterministic Validator Key Derivation:** The system employs the eVRF evaluation function to deterministically map validator indices to cryptographically secure seeds for BLS12-381 key generation. For a validator with index i, the derivation process works as follows:

1. Index Encoding: The validator index is encoded as a 4-byte big-endian integer:

x = \text{encode}(i) \text{ where } i \in [0, 2^{32}-1]
2. eVRF Evaluation: The master key and encoded index are input to the eVRF evaluation function:

y, Y, \pi \gets Eval(sk_{\text{master}}, x)
3. Cryptographic Seed Generation: The eVRF output y is processed through SHA-256 to ensure uniform distribution across the BLS12-381 scalar field:

\text{seed} = \text{SHA256}(\text{encode}_{32}(y))

1. BLS Key Computation: The final BLS validator keys are computed as:
sk_i = \text{bytes_to_int}(\text{seed}) \bmod r_{\text{BLS}}

pk_i = sk_i \cdot G_{\text{BLS}}

where r_{\text{BLS}} is the scalar field order of BLS12-381 and G_{\text{BLS}} is the generator point used in Ethereum’s validator signature scheme.

### Verification Process

The verification process ensures that for any validator index i, the derived BLS key pair (sk_{\text{BLS},i}, pk_{\text{BLS},i}) was correctly computed from the master key without revealing sk_{\text{master}}:

**eVRF Verification:** First, verify the eVRF proof components:

\mathsf{Verify}(vk_{\text{master}}, x, Y, \pi)

**BLS Key Verification:** Then verify the BLS key derivation:

sk'_i = \text{bytes_to_int}(\text{SHA256}(\text{encode}_{32}(y))) \bmod r_{\text{BLS}}

pk'_i = sk'_i \cdot G_{\text{BLS}}

\text{Verify: } pk'_i \stackrel{?}{=} pk_i

This verification process provides mathematical certainty that keys were generated according to the protocol while maintaining zero-knowledge properties.

### Impact and Real-World Benefits

**Enhanced Security Posture:** By eliminating the need to store multiple private keys, the system dramatically reduces the attack surface while maintaining cryptographic independence between validators.

**Compliance and Auditability:** The verifiable nature of the derivation process enables comprehensive audit trails without compromising security, addressing regulatory requirements for institutional adoption.

**Disaster Recovery:** The deterministic generation ensures reliable key recovery capabilities. Given the master key sk_{\text{master}} and index i, the validator key can always be reconstructed.

**Scalability:** The system scales efficiently to support large validator operations without proportional increases in security infrastructure, operational complexity, or compliance overhead.

This DDH-based eVRF approach represents a shift in blockchain validator key management, providing the simplicity required for large-scale deployment while maintaining the cryptographic security guarantees essential for protecting significant financial stakes and network integrity.

---

## Conclusion

This work demonstrates that **DDH-based eVRFs** can be implemented efficiently with practical zero-knowledge proofs for blockchain use. By leveraging **BLS12-381** and **Bandersnatch**, we achieve strong security, fast computation, and compatibility with Ethereum’s validator infrastructure.

Our codebase provides:

- A proof-of-concept eVRF implementation with proofs which can be found here.
- A framework for validator key derivation and management.
