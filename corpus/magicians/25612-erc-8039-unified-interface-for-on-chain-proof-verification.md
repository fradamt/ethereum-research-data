---
source: magicians
topic_id: 25612
title: "ERC-8039: Unified interface for on-chain proof verification"
author: khemiriwalid
date: "2025-09-28"
category: ERCs
tags: [erc, zkp]
url: https://ethereum-magicians.org/t/erc-8039-unified-interface-for-on-chain-proof-verification/25612
views: 332
likes: 7
posts_count: 6
---

# ERC-8039: Unified interface for on-chain proof verification

**Abstract**

Proof system protocols—such as SNARKs and STARKs—are emerging as the fundamental way to exchange state and computation between computer programs(fact or properties around private state, computation on private or public state, etc) in a trust-minimized manner secured by cryptography on the internet. It provides a cryptographic way for computer programs to exchange attestations about state and computation.

In the coming years, proofs will become first-class citizens on the internet, much like web documents are today. It is crucial to establish standards for proof systems to ensure strong interoperability.

Proofs act as interoperability primitives. Just as HTTP standardized the exchange of documents on the internet( like the exchange of data between computers using JSON or XML format over the HTTP protocol in the web paradigm), proof systems will standardize the exchange of *`verifiable states`* secured by cryptography(trust minimization). To make proofs first-class citizens in a standardized manner, several layers must be addressed:

- Proof objects: canonical serialization formats for inputs, outputs, and verification keys.
- Verification interfaces: on-chain (EVM, WASM), off-chain APIs exposing uniform isValidProof semantics across proof systems.
- Proof transport: protocols for transmitting proofs across domains (e.g., cross-chain messaging, client-server APIs). We must address the question of how proofs are transported securely and efficiently from off-chain environments to on-chain verifiers.
- Composability: standards for recursive verification, proof aggregation, and succinct proofs of multiple systems.

Without these standards, interoperability will fragment: a proof generated in one system may not be consumable elsewhere, and applications will remain siloed. With them, proofs become the standardized verifiable state computation, enabling trust-minimized interoperability across blockchains, web applications, and distributed systems.

**Problem & Motivation**

*On-Chain Proof Verification: A Heterogeneous Landscape*

Zero-knowledge proofs are now integral to blockchain scalability, privacy, and interoperability — but the way they are verified on-chain is far from uniform. Each proof system carries its own verification model, leading to a heterogeneous ecosystem:

- Groth16 (used by Circom/snarkjs, gnark) produces constant-size proofs that are checked with a small number of pairings over the bn254 curve. Verification is cheap and battle-tested, but every circuit requires its own hard-coded verifying key.
- PLONK and Plonkish systems (Halo2, Plonky2, etc.) rely on polynomial commitments (KZG or IPA). On Ethereum, these verifiers either target bn254 pairings (like Groth16) or the newer BLS12-381 KZG precompile (EIP-4844). Proofs are larger and gas costs higher, but a universal SRS allows reuse across many circuits.
- zkVM receipts (RISC Zero, SP1) represent whole virtual-machine executions. Their native STARK proofs are far too large for direct L1 verification, so receipts are usually compressed into smaller SNARKs (Groth16 or PLONK). The contract then enforces higher-level semantics such as programId and journalHash embedded in the public inputs.

This heterogeneity shows up across multiple dimensions — proof size, field/curve choice, precompiles used, *`verifier contract structure`*, and setup assumptions. The result is a fragmented developer experience.

In the Ethereum ecosystem, on-chain proof verification is a fundamental activity and has become a critical primitive for applications. Co-processors, wallets, bridges, verifiable applications (vApps), identity & credential/attestation systems, zkML, and trustless agents all submit proofs on-chain. The key question is whether there exists an abstracted smart-contract interface that can be called to verify proofs, regardless of the underlying system. Since proof verification is becoming a core activity on Ethereum, it is essential that we move toward standardization.

In these workflows, one smart contract typically calls another to perform proof verification. What is missing is a standardized, transparent way to manage proofs on-chain. We need a well-defined interface that governs how proof verification calls are handled between contracts, ensuring consistency and composability. Moreover, the verifier contract itself must expose its verification capability in a clear, interoperable manner.

Efforts are emerging to smooth this landscape with ERC-style standards (mirroring ERC-1271 for signatures) that define a universal isValidProof interface, backed by a registry of schemas and adapters. Such an abstraction speeds up proofs to be first-class citizens on the Blockchain: composable, interoperable, and accessible to any smart contract regardless of the underlying cryptography.

ERC-1271 standardized “*`Can this contract validate a signature?`*” for authentication. What we’re missing is the sibling question for attestation/claims: “*`Can this contract validate a proof of a statement?`*” A clean, minimal interface lets wallets, paymasters, bridges, and dApps plug in any proof system (SNARKs/STARKs/zkVM receipts) without bespoke adapters.

In the context of smart contracts, it is crucial to define an interface for their capability to verify proofs. It is a serious and fundamental discussion that needs to be had to decide on a unified interface for standardizing the on-chain proof verification layer.

Can we define a **proof-system-agnostic** smart-contract interface for on-chain proof verification—decoupled from Groth16/PLONK/zkVM and their underlying cryptographic specifics?

**Unified interface for exposing ZK proof verification by smart contracts**

A generalized abstract interface used by any smart contract that exposes proof verification capability.

It is an interface to be used by a smart contract that will make a call to verify a proof without thinking about any details about the proof verification process. This ensures strong on-chain interoperability and clear on-chain proof verification. It will be part of the on-chain proof management standardization and let proofs, first-class on-chain citizen.

The interface can be the entry point for verifying proofs within multiple circuits of the same entity, statements using different proof systems(protocols and their production frameworks/libraries), or multiple circuits versions of the same statements.

The ERC is designed to provide a unified interface for on-chain proof verification. Any smart contract or protocol that has proof verification capabilities must be implemented and exposed using the unified standardized interface for strong interoperability.

The suggested interface can be paired and adapted for proof verification within a smart contract that manages:

- Relations
- Relations and instances
- Different proof system protocols or their production framework/library, different circuit/program versions

A protocol or registry that governs trust-minimized provable statements management (i.e., relations and their instances or only relations) MUST expose proof verification via this interface.

Application protocols whose business logic depends on such statements MAY delegate verification by invoking the standardized smart-contract interface defined herein.

A provable statement is defined by a relation R and a public instance X such that the verifier accepts a proof π attesting ∃W:(X,W)∈R. Conforming contracts MUST identify R by schema/relationId and accept publicInputs encoding X.

In practice, a trust-minimized protocol (or a shared verification registry) implements this ERC so that other applications can offload ZK proof verification. Any application whose state transitions imply a particular statement calls *`isValidProof(schema, publicInputs, proof)`* and proceeds only if the call returns the interface’s magic value.

The smart contract can manage only relations. Then, you pass the relation via the schema and pass the instance via public inputs.

The smart contract can manage relations and instances. In this case, pass the relationId via the schema parameter and reference to the instance via the public input parameters.

The circuit is something programmable. It is crucial to handle the circuit evolution: bug fixes, business-logic changes, or security updates, etc. The scheme(we can refer to as relationId) parameter is responsible for handling the circuit programmability evolution.

[ERC Draft](https://github.com/ethereum/ERCs/pull/1238)

What feedback I’m seeking

Is the verification interface sufficiently abstract—i.e., independent of specific proof systems and implementations?

Interface shape: Does schema + bytes32 publicInputs + bytes proof cover your SNARK/STARK/zkVM/Recursion integration needs without extra parameters?

Lane discipline: Any objections to requiring fixed lane order, big-endian numeric interpretation, and (if applicable) pre-reduction to the target field?

Domain separation: Are chainId, verifyingContract, nonce, expiry (or your equivalents) sufficient and practical as public signals?

zkVM receipts: Is exposing programId and journalHash as bytes32 lanes workable across existing zkVM toolchains?

Error semantics: Any concerns with “return magic value on success; otherwise any other value; do not revert on invalid proofs”?

Interoperability risks: Are there proof systems or popular verifier contracts that would struggle with bytes32 lanes?

Versioning via schema: Is minting a new schema ID on layout change acceptable for ecosystem evolution?

## Replies

**Ankita.eth** (2025-10-07):

This proposal is a crucial step toward unifying on-chain ZK proof verification. The abstraction using `schema + publicInputs + proof` is elegant, but I’d like to highlight a few nuanced points:

1. Circuit & Proof Evolution: Relying solely on a schema identifier is fine for static circuits, but for complex zkVM or recursive SNARK/STARK setups, it may be valuable to include versioning or an optional metadata hash. This ensures that schema evolution (bug fixes, optimizations, or logic updates) doesn’t break dependent contracts or cross-chain integrations.
2. Gas & Verification Optimization: For PLONKish systems and zkVM receipts compressed into SNARKs, the interface should consider exposing “lightweight verification hints” as optional fields. For instance, partial public inputs or precomputed commitments could reduce on-chain verification gas without compromising trustlessness.
3. Composability & Recursive Proofs: One key challenge is recursive verification across heterogeneous proof systems. The interface could be extended to optionally support aggregated proofs or chained verification receipts. This would enable a single call to isValidProof to verify complex, multi-layered statements without requiring bespoke adapters.
4. Cross-Chain & Domain Separation: Including chainId, verifyingContract, nonce, and expiry as public signals is excellent. It could also be worth formalizing a minimal domain separator hash for multi-chain workflows, ensuring proofs aren’t accidentally replayed or misinterpreted on L2s or bridges.
5. zkVM Program Semantics: Exposing programId and journalHash is minimal and effective. For future-proofing, allowing optional multiple lanes or structured metadata could make it compatible with evolving VM toolchains or stateful proofs.

Overall, a standardized ERC interface like this could transform proofs into composable, interoperable, and trust-minimized first-class citizens on Ethereum. The key to adoption will be **flexibility without sacrificing minimality**, ensuring it works for simple SNARK circuits and complex zkVM pipelines alike.

---

**khemiriwalid** (2025-10-12):

Hello Ankita,

Your feedback is very valuable.

1/ The scheme acts as a unique on-chain identifier of a provable statement within their ZK protocol and technical stack info.

In the first draft, the suggested scheme is computed:

### Schema Identifier

The `schema` parameter uniquely identifies the proving **relation** (circuit/program + verifier layout + rules).

Implementations **SHOULD** compute `schema` as a collision-resistant digest over fixed-width, versioned components, anchored by a human-readable name:

- Recommended construction (fixed-width fields):

```auto
schema = keccak256(
    abi.encode(
        keccak256("name of the circuit or program"),  // e.g., "age-merkle-threshold", "zkvm:transfer-v2"
        uint32(circuitOrProgramVersion),               // semantic version of the relation
        vkHashOrProgramId,                             // bytes32: verifying key hash (SNARK/STARK) or programId (zkVM)
        layoutHash                                     // bytes32: hash of lane order & field rules for publicInputs
    )
);
```
- Groth16 circuit:

```auto
schema = keccak256(
    abi.encode(
        keccak256("age-merkle-threshold"),
        uint32(1),
        vkHash,        // bytes32
        layoutHash     // bytes32, commits to [root, threshold, subjectHash, chainId, ...]
    )
);
```

2/ I suggest adding an optional method/interface that supports hints and keeping the base interface without hints.

```auto
function isValidProof(
    bytes32 schema,
    bytes32[] calldata publicInputs,
    bytes calldata proof,
    bytes calldata hints   // e.g., partial commitments, batching indices, MSM schedules
  ) external view returns (bytes4);
```

To support ERC-8039, you must at least implement the base interface.

3/ I think also adding an optional method/interface for supporting such needs. What is your suggestion about such an interface?

My suggestion:

```auto
/// @param schemas         length = N
  /// @param packedPI        concatenation of all publicInputs lanes
  /// @param piOffsets       byte offsets into packedPI; length = N+1 (sentinel)
  /// @param packedProofs    concatenation of all proofs
  /// @param proofOffsets    byte offsets into packedProofs; length = N+1 (sentinel)
  /// @return magicValue     selector on “all valid”; else 0x00000000 or revert
  function isValidProof(
    bytes32[] calldata schemas,
    bytes calldata packedPI,
    uint32[] calldata piOffsets,
    bytes calldata packedProofs,
    uint32[] calldata proofOffsets
  ) external view returns (bytes4 magicValue);
```

4/ Very good idea. Can you formalize a minimal domain separator hash(your suggestion)?

5/ Yeah, you have reason. It will meet the exponential needs for using zkVMs.

What is your suggestion for this?

We also attend to the community feedback.

---

**microbecode** (2025-10-15):

I think this is a very cool standard.

I have a few notes and questions:

- Get rid of the “A” in the header. It’s good to keep headers short and 100% grammar isn’t so relevant there. This is just according to my experience with ERCs.
- Have you looked if similar suggestions/standards exist? How are they related? Is this a competing standard or builds on top of other stuff?
- In general this seems to be a huge standard. I think you will need more people seriously involved in designing this.
- Related: have you considered making this standard into something smaller first and then build on top of that with another standard? I’ve seen too many big standard stagnate due to the lack of time/interest/whatever. It’d also be much easier to understand this standard if it was smaller. Although I don’t have good ideas how to chop this.
- Have you talked with teams who would actually use/need this? What’s the feedback? Or what’s your background in starting this standard?

---

**khemiriwalid** (2025-10-19):

There are similar and related uncompleted standards. They are in “Stagnant” status.

ERC-1922: zk-SNARK Verifier Standard

ERC-1923: zk-SNARK Verifier Registry Standard

Today, we can have different representations of provable statements on-chain. It is a discussion within the ecosystem to decide whether one standard for representing provable statements on-chain or it will be multiple ones, which are domain-specific.

But having one clear interface for verifying proofs on-chain will lead to an interoperable ecosystem where application protocols use a standardized interface to verify proof.

During my research, I found two ERCs that are related to provable statement representation:

ERC-8035: MultiTrust Credential (MTC) — Core

ERC-7812: ZK Identity Registry

Yeah, this is a huge standard and critical for the ecosystem. I’m open to working with other people to have a working standard adopted by the ecosystem.

I tried to make the standard much smaller than that, and I reduced the scope of it to the application-level provable statement, not an infrastructure-level provable statement(such as within zk-rollups).

I developed a wallet-related provable statements for having a more user-friendly on-chain and self-custody experience while maintaining strong security guarantees(smart accounts, ERC-4337, ERC-7579, etc). Many questions were discussed, such as:

Is there a standard for representing provable statements on-chain that can be used by application protocols?

Is there a standard for verifying proofs on-chain within smart contracts to be used by application protocols(something similar to on-chain signature verification by smart contracts, ERC-1271)?

Is there a standard to organize the smart account-wallet-provable statement relationship(provable statements allowed to be used by the smart account—Relations, public inputs—Instance within the smart account, proving phase in wallet—which protocol or framework to generate proof, etc)?

---

**Ankita.eth** (2025-10-22):

Thank you, [@khemiriwalid](/u/khemiriwalid), for the detailed clarifications — this makes the proposal much more concrete and developer-friendly. I really like how the schema construction now anchors the circuit name, version, verifier key, and layout hash together — it gives a strong, deterministic identity to each provable statement while still being human-readable and traceable across versions.

A few thoughts on the follow-ups:

**1. Schema Design & Versioning**

This new construction is clean and future-proof. It balances semantic clarity (`name`, `version`) with cryptographic binding (`vkHash`, `layoutHash`). For zkVM-based systems, I’d suggest explicitly allowing `programHash` or `programMerkleRoot` as interchangeable with `vkHash` to accommodate evolving VM architectures. It might also be worth including a reserved metadata field for optional “relation type” (e.g., zkML, identity, bridge), purely for registry and discovery purposes.

**2. Hints Interface Extension**

The optional `hints` parameter feels like the right approach — modular without complicating the base ERC. This could unlock significant gas optimizations for recursive or batched proofs. I’d recommend defining a minimal TLV (Type-Length-Value) structure for hints, so ecosystems can extend without breaking the base ABI.

**3. Batched Verification Interface**

The batched `isValidProof` you suggested is great for composability and bridges well into zkML or zkVM pipelines that produce multiple receipts per transaction. One potential addition could be an optional `aggregate` boolean flag — allowing implementations to signal whether proofs are verified independently or recursively aggregated before the magic value check.

**4. Domain Separator Hash**

For the minimal domain separator, one flexible approach could be:

```auto
domainSeparator = keccak256(
  abi.encode(
    keccak256("ERC8039_DOMAIN"),
    block.chainid,
    verifyingContract,
    keccak256(abi.encodePacked(schema, publicInputs))
  )
);
```

This keeps it minimal yet resistant to cross-domain replay — and works uniformly for SNARKs, STARKs, or zkVM receipts.

**5. zkVM Extensions & Ecosystem Alignment**

As zkVM adoption grows, your inclusion of programId and journalHash remains critical. I’d also propose formalizing a small “zkVM context struct” in the registry — e.g., `{programId, journalHash, version}` — so client libraries can reference proof semantics consistently across VMs (RISC Zero, SP1, etc.) without needing ad-hoc mapping.

Overall, the revised structure strikes a strong balance between abstraction and practicality. By keeping the base ERC minimal and optional extensions modular (`hints`, `batching`, `domainSeparator`), ERC-8039 can evolve incrementally without fragmentation — much like ERC-1271 did for signature validation.

This feels like a solid foundation for making proofs truly *interoperable primitives* on Ethereum. Excellent work advancing this — I can see this becoming one of the key standards powering the next generation of verifiable applications.

