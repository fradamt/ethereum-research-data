---
source: magicians
topic_id: 21624
title: "ERC-7812: ZK Identity Registry"
author: Arvolear
date: "2024-11-08"
category: ERCs
tags: [zkp, identity, registry]
url: https://ethereum-magicians.org/t/erc-7812-zk-identity-registry/21624
views: 3366
likes: 37
posts_count: 25
---

# ERC-7812: ZK Identity Registry

UPDATE June 2025:

The proposal has been moved to the “Review” stage!

UPDATE February 2025:

1. The ERC-7812 has been merged as a draft!
2. The contracts have been deterministically deployed on Mainnet and Sepolia. The registry is available at 0x781246D2256dc0C1d8357c9dDc1eEe926a9c7812 .

---

Hello Magicians, I am excited to share our latest work with you!

## Abstract

This EIP introduces an on-chain registry system for storing abstract statements, where the state of the system can be proven in zero knowledge without disclosing anything about these statements. Developers may use the singleton `EvidenceRegistry` contract to integrate custom business-specific registrars for statement processing and proving.

## Motivation

The standardization and aggregation of provable statements in a singleton on-chain registry significantly improves reusability, scalability, and security of the abundance of zero knowledge privacy-oriented solutions. The abstract specification of the registry allows custom indentity-based, reputation-based, proof-of-attendance-based, etc., protocols to be implemented with little to minimal constraints.

The given proposal lays the important foundation for specific solution to build upon. The more concrete specifications of statements and commitments structures are expected to emerge as separate, standalone EIPs.

## Specification

Check out the full specification on GitHub:

https://github.com/ethereum/ERCs/pull/710

The complete reference implementation can be found [here](https://github.com/rarimo/evidence-registry).

---

Would love to see an insightful discussion rolling!

## Replies

**0xsimka** (2024-12-01):

How might the ERC-7812 standard address interoperability challenges among different privacy-oriented protocols while maintaining strict data privacy guarantees?

---

**Arvolear** (2024-12-01):

Hey, thanks for the question!

The EIP is designed to provide a unified provable on-chain storage for all the protocols that integrate with the `EvidenceRegistry`. For example, there may be a `Registrar` that manages the ICAO masters list (for on-chain national passport verification). Any protocol that wants to prove the validity of a passport will be able to reference the evidence registry and prove that one of the masters has signed a passport.

The specific business use cases and their implementation are outsourced to the registrars. This means there may be general-purpose “social”, “passport”, and “POAP” registrars that standardize how to manage and prove their data. We think that the behavior of registrars may even be described as separate EIPs.

Every registrar is expected to provide their own means of secure data proving (e.g. on-chain ZK verifier).

Hope that helps!

---

**EugeRe** (2024-12-05):

Hey [@Arvolear](/u/arvolear)  that’s very interesting! Let’s connect, I would be happy to share some views, and see whether I can contribute!![:slightly_smiling_face:](https://ethereum-magicians.org/images/emoji/twitter/slightly_smiling_face.png?v=12)

I am working on the smart wallet 4337 angle.

---

**Andriian** (2024-12-06):

Hey [@Arvolear](/u/arvolear)

Is the SMT implementation limited to 64 levels max? That would mean some key path collision probability. That would be big enough but for “public good” singleton is something to consider.

Also, are there any mechanism supposed to migrate existing statements from other protocols? ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

---

**Arvolear** (2024-12-08):

The SMT collision bits are algorithmically limited to 256 bits and will be set to 80 bits during deployment. We tested that the EVM throws runtime “stack too deep” errors at the depths of 96 and more. To be clear, 80 bits is 2^80=1,209*10^24 elements which is practically impossible to reach.

The existing protocols can potentially push their state commitments (e.g. IMT roots in case of Semaphore) into the registry for the later proving. Migrating the entire state will definitely be too expensive, so suggestions are warmly welcome.

---

**Andriian** (2024-12-11):

[@Arvolear](/u/arvolear) thanks for the clarification. There if 80 depth limit which I overlooked

But the number of nodes in the tree still looks limited to 2^64 according to some struct field types like `uint64 nodesCount;` `uint64 childLeft;` and `uint64 childRight;`

Am I missing something how the SMT implementation works?

Yes, existing protocols can push their state commitments into the registry. It’s more easy doing that from the beginning but may be tricky to switch if a protocol already has it’s own SMT-based registry implementations up and running.

The solution for the former case may be introducing some **constant timestamp** after which the custom protocol starts writing to the EvidenceRegistry. The essential drawback is protocol complication with some logic, which will “fallback” to legacy SMT implementations, so we may need more solutions…

---

**Arvolear** (2024-12-11):

Indeed. The `uint64 nodesCount` just slipped out of my mind.

So there are two limits:

1. The overall nodes count of 2^64 ~= 1.84*10^19.
2. The nodes collision limit of 80 bits prefix.

In a degenerate case (if no randomization is used) it is fairly easy to reach the second limit. One just needs to push two very similar keys to the tree. However, since every element is hashed (by the `EvidenceDB._getIsolatedKey()` function) before being inserted, I am not sure which one of the limits is more likely anymore.

---

**Andriian** (2024-12-11):

The second limit should be more likely.

By the Birthday Problem formula **Pcol ≈ 1 − e ^ −n(n−1)/2T** there is ~40% chance of at least one collision for 2^40. For 2^42 it is practically guaranteed.

But generally SMT is fine as for 2^36 (~69 billions) nodes it is only 0.1951% of collision and probability drops exponentially (or something similar) if less nodes.

---

**Andriian** (2024-12-13):

[@Arvolear](/u/arvolear) another question just came to my mind.

Have you considered not to store `nodeHash` in this struct to save another 20K gas per each node?

```auto
    struct Node {
        NodeType nodeType;
        uint64 childLeft;
        uint64 childRight;
        bytes32 nodeHash;
        bytes32 key;
        bytes32 value;
    }
```

Yes, this is something that you the `getProof` function needs. However, are there any on-chain clients expected, which call this function?

Usually the one, who picks proofs of existence/non-existence of  a key need to do it anonymously so it’s likely just an API call with no transaction. Thus, you can generate hashes for siblings right in the getProof function or return key/values/nodeTypes to generate proofs off-chain on some client.

---

**Andriian** (2024-12-13):

[@Arvolear](/u/arvolear) in case of eliminating hashing out of `add`, `update` and `remove` node transactions you may save gas even more.

E.g. Poseidon hash implementation in `circomlibjs` for 2 and 3 `uint256` elements take 54K and 70K gas respectively. If I’m not missing something the hash recalc is done for each of those 3 methods up to (!) the root. Then, gas saving may be essential, unless the hash function is very cheap or introduces as EVM precompile.

---

**Arvolear** (2024-12-14):

Thanks for proposing that!

We have actually thought of such optimizations but there is a problem: you need to anchor to the SMT root on-chain. Without these hashes the on-chain verification integration will be extremely expensive. Currently the `getRoot()` method just performs a single `SLOAD`.

P.S.

We are working on an alternative to SMT which we call Cartesian Merkle Tree (CMT). CMT has similar properties to SMT but under some conditions (when the cost of a hash function is low) cheaper by up to ~20%.

Currently, on-chain SMT with poseidon wins. However certain off-chain applications may see some benefit as CMT takes ~50% less space.

For more information, check out the Solidity reference implementation [here](https://github.com/dl-solarity/solidity-lib/blob/master/contracts/libs/data-structures/CartesianMerkleTree.sol).

---

**Andriian** (2024-12-14):

[@Arvolear](/u/arvolear) thanks for the prompt and the CMT link ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

Yes, the root always need all tree branch recalculation, so not good for on-chain verification

---

**CPerezz** (2025-01-28):

Hey that’s cool work!

This has the potential of unlocking lots of things. Not just passports. Ideally this could be similar to a DID container at the end.

Wanted to mainly ask 3 things:

- Have you considered that bytes32 might not be (I think for sure will not) enough space for PQ-primitives which are usually much larger than EC points.
- I imagine that vs quantum adversary, we’re screwed (as is normal ofc). Could this include some contingency plan? ie. a functionality that allows an upgrade and maybe a shutdown/halt?
- I’m curious on why the hashing (isolation) needs to be done on-chain. Specially if we consider that Poseidon is what has been implemented. Wouldn’t it make more sense to allow the user to hash by himself? And if there’s any security risk on allowing that, why not choosing a hash that is pre-compile friendly? Thus lowering significantly the gas cost?

Thanks!

---

**Arvolear** (2025-01-28):

Hey, thanks for taking a look!

- About post-quantumness. Currently, the whole Ethereum protocol is screwed due to ECDSA not being PQ secure. The bytes32 key/values were chosen because 1) they occupy a single storage slot; 2) the individual registrars may hash arbitrary data and easily pack it in 32 bytes.
- Unfortunately, this would introduce some centralized entity that “governs” the registry. I would like to avoid that at all costs.
- The isolation is done on-chain to avoid collisions within the SMT. If isolation is delegated to registrars, an adversary may remove data they shouldn’t access. The poseidon is chosen because it is de facto the standard in the ZK world. Precompile sha2 and opcode keccak are cheaper on-chain but MUCH more expensive (in terms of constraints and complexity) in ZK.

Hope that clarifies some things.

---

**Arvolear** (2025-02-07):

Quick update: the ERC has been merged as a draft. Will be pushing the proposal to review soon. Thanks to everyone involved!



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7812)





###



Singleton registry system for storing abstract private provable statements.

---

**Arvolear** (2025-02-18):

Update: deployed the registry deterministically both to [Mainnet](https://etherscan.io/address/0x781268D46a654D020922f115D75dd3D56D287812) and [Sepolia](https://sepolia.etherscan.io/address/0x781268D46a654D020922f115D75dd3D56D287812) networks. The address is computed to be `0x781268D46a654D020922f115D75dd3D56D287812` (starts and ends with 7812).

Check out the full deployment script [here](https://github.com/rarimo/evidence-registry/blob/main/scripts/deploy.ts).

---

**namncc** (2025-03-04):

Great work [@Arvolear](/u/arvolear)!

Considering that statement often carries randomness within itself (e.g. you committed to your id with some salt for privacy), current design hints that duplicates of encapsulated value (within statement) may exist within the registry (the isolation with sender+statement cannot detect this), does that constitute some potential problem?

---

**Arvolear** (2025-05-07):

Hey, apologies for the long reply. I am not sure this approach manifests any problems. If individual `Registrars` allow such behavior of “duplicate” preimages to exist, then it is their concern to implement this logic correctly. The registry design here merely acts as a provable database. Or am I missing something?

---

**Arvolear** (2025-05-14):

UPD: During the integration with the `EvidenceRegistry`, several issues were encountered due to `getIsolatedKey()` function not being public. It was decided to update the interface and redeploy the contract to the new address `0x781246D2256dc0C1d8357c9dDc1eEe926a9c7812`.

New deployment is available on the [mainnet](https://etherscan.io/address/0x781246D2256dc0C1d8357c9dDc1eEe926a9c7812) and [sepolia](https://sepolia.etherscan.io/address/0x781246D2256dc0C1d8357c9dDc1eEe926a9c7812).

The [EIP](https://eips.ethereum.org/EIPS/eip-7812) is already updated to the latest spec.

---

**lucy_sha256** (2025-05-21):

Hi,

We’re building a ZK-based identity protocol that derives cryptographic keys from biometric data in a non-storage, reproducible manner.

We’re exploring how to integrate Tunnel ID as a registrar on top of ERC-7812. The registry structure aligns really well with our design, especially the use of Poseidon-based SMT, commitment isolation, and the delegated ZK verifier model.

We had a few questions to ensure we’re implementing this correctly and future-proofing our registrar integration:

### 1. For inputs that may slightly vary between sessions (but still map to the same identity or key via ZK verification), is it acceptable to:

- Always register a fixed commitment, and let ZK proofs handle verification of equivalence/proximity?
- Or are registrars expected to allow updating/replacing commitments when drift is anticipated?

We’re asking this to determine whether the registry should act as a persistent anchor or a periodically rotated state point.

### 2. Can the value field in addStatement(key, value) be used by registrars to encode auxiliary metadata, such as circuit versioning, verification parameters, or commitment type identifiers?

Or is it assumed that all semantic information is handled off-chain by the ZK proof and verifier logic?

### 3. Is there a canonical pattern for linking specific verifier circuits to a registrar or statement type?

For example, if different registrars use different verification semantics (e.g., proof-of-ownership, proof-of-age, proof-of-proximity), how should dApps or wallets know:

- what circuit applies to which commitment?
- what inputs or public signals are expected?

### 4. Should this be externalized via IPFS, ENS, or would it make sense to suggest a verifier registry pattern in a future spec?

How should registrars handle users who want to register **multiple statements** (e.g., different modalities or backup factors) that all represent the same identity?

Should this be modeled via:

- One commitment per modality (e.g., key1, key2) and an external linkage circuit?
- Or a Merkle tree of sub-commitments as the stored value?

### 5. Credential Refresh & Recovery

In scenarios where a user loses access to the original input used to generate their statement (e.g., hardware change, sensor drift, or theft of auxiliary material), what is the **recommended pattern** for refreshing or recovering their credential?

- Should registrars implement a replaceStatement() flow with ZK linkability to the previous statement?
- Or is the expectation that the user simply registers a new statement, and recovery or linkage is handled off-chain?
- Is there scope in the registry to formally support “rotatable credentials” or mark older statements as revoked/expired?

We’re asking this in the context of identity systems where users may not be able to reproduce the exact statement, but can still prove linkage to the original in zero-knowledge.

### 6. Backup & Recovery Patterns

For identity systems where users generate their commitments from **private, non-stored inputs**, what are the best practices for supporting **backup and recovery**?

Specifically:

- Is it advisable for registrars to allow a user to register multiple recovery commitments under their namespace (e.g., main, backup1, backup2)?
- Should recovery be handled via a ZK proof of linkage to the original statement (e.g., same preimage, same derived key)?
- Is there value in formalizing a recovery framework (e.g., a substandard for credential fallback and delegation)?

We’re designing with the assumption that **no original input is stored**, so we want to ensure users can securely reassert their identity or keys in case of device loss or corruption.


*(4 more replies not shown)*
