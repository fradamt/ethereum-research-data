---
source: magicians
topic_id: 12
title: About the EIPs category
author: jpitts
date: "2018-02-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/about-the-eips-category/12
views: 2288
likes: 3
posts_count: 2
---

# About the EIPs category

Discussions about specific EIPs (improvement propsals), and general proposals which may become EIPs. If applicable, specify the EIP issue # in the topic title.

## Replies

**arkhen** (2025-08-19):

**Abstract:** This EIP proposes a framework for post-quantum cryptography in Ethereum based on the principle of individuation, focusing on preserving unique identity through the transition to quantum-resistant algorithms, while leveraging quantum indistinguishability properties for optimization.

**Motivation:** The threat posed by quantum computers requires a transition to post-quantum cryptography in Ethereum. However, this transition must preserve the unique identity of accounts and transactions, not just replace algorithms. The principle of individuation offers a philosophical framework to guide this transition meaningfully.

**Specification:**

1. Haecceity Preservation Layer (HPL)

- An abstract layer that preserves the “thisness” of each Ethereum identity, regardless of the underlying cryptographic algorithm.
- Implementation using immutable unique identifiers that persist through migration.
- Bidirectional mapping between current ECDSA addresses and future post-quantum addresses.

1. Quantum Indistinguishability Optimization (QIO)

- Mechanisms that leverage quantum indistinguishability to optimize batch verifications and signature aggregations.
- Implementation of verification schemes based on quantum statistics (Fermi-Dirac, Bose-Einstein) for transactions with similar characteristics.
- Use of conceptual quantum entanglement for compression of correlated signatures.

1. Processual Individuation Protocol (PIP)

- A dynamic transition protocol that treats migration as a continuous individuation process.
- Phases:

Pre-Individual Phase: Coexistence of classical and post-quantum systems
- Individuation Phase: Gradual migration with identity preservation
- Post-Individual Phase: Fully post-quantum system with preserved identities

1. Metastable State Compression (MSC)

- Algorithms that exploit metastable states to optimize quantum data compression.
- Implementation using Simondon’s notion of potentiality and tension resolution.
- Dynamic adaptation based on quantum state characteristics.

**Technical Implementation:**

1. Extension of EIP-7932:

- Incorporate haecceity and individuation concepts as guiding principles
- Add support for the Haecceity Preservation Layer
- Implement optimizations based on quantum indistinguishability

1. Integration with ZKnox’s work:

- Utilize the already developed NTT optimizations
- Extend to support the new individuation concepts
- Implement the Processual Individuation Protocol using smart contracts

1. New EVM Opcodes:

- HAECCEITY_VERIFY: Verification based on preservation of unique identity
- QUANTUM_COMPRESS: Compression based on quantum indistinguishability
- INDIVIDUATE_MIGRATE: Facilitate dynamic migration between cryptographic systems

**Expected Benefits:**

1. Identity Preservation: Maintain the unique identity of accounts and transactions through the cryptographic transition
2. Resource Optimization: Leverage quantum properties to reduce gas costs and improve efficiency
3. Smooth Transition: Framework for gradual migration that minimizes disruptions
4. Philosophical Foundation: Robust conceptual basis to guide technical decisions

**Challenges and Considerations:**

1. Conceptual Complexity: Translating abstract philosophical concepts into concrete technical implementations
2. Compatibility: Ensuring compatibility with existing systems during transition
3. Performance: Ensuring that new abstractions do not introduce significant overhead
4. Adoption: Gaining community consensus on this philosophically grounded approach

