---
source: magicians
topic_id: 26530
title: "ERC-8084: Zero-knowledge proof metadata"
author: cococay
date: "2025-11-11"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-8084-zero-knowledge-proof-metadata/26530
views: 59
likes: 1
posts_count: 1
---

# ERC-8084: Zero-knowledge proof metadata

**Discussion topic for ERC-8084**

[Original PR](https://github.com/ethereum/ERCs/pull/1344)

---

## Update Log

- 2025-11-10: initial draft
- 2026-01-20: Updated

---

## External Reviews

None as of 2025-11-10.

---

## Outstanding Issues

None as of 2025-11-10.

---

## Summary

*ZKMeta* proposes a minimal, universal metadata interface for any Ethereum contract that verifies or consumes zero-knowledge proofs. Rather than standardizing proof formats, it standardizes the accompanying **metadata** required by tooling, wallets, explorers, relayers, and cross-chain systems to correctly interpret and validate proofs.

ZKMeta exposes the following components:

- proof system identifier (Groth16, Plonk, Halo2, zkVM, etc.)
- circuit identifier (content-addressed hash of the circuit artifact)
- circuit version (semver-encoded uint64)
- public-inputs schema hash
- public-inputs schema URI (content-addressed or hash-suffixed HTTPS)
- verification-key URI (content-addressed or hash-suffixed HTTPS)

This creates a foundation for a standardized “ZK ABI” layer that is needed across the ecosystem.

---

## Purpose of This Standard

ZK integration today is fragmented:

- No standard way to identify proof systems
- No versioning convention for circuits
- No uniform public-input schema format
- No deterministic way to fetch verification keys
- Each project reinvents metadata formats and tooling
- Indexers and explorers lack a clean update signal

ZKMeta addresses these gaps without constraining proving systems or proof structures.

---

## Specification Summary

The core interface:

```auto
interface IZKMetadata {
    event CircuitMetadataUpdated(bytes32 circuitId, uint64 circuitVersion, bytes4 proofSystem);

    function circuitId() external view returns (bytes32);
    function circuitVersion() external view returns (uint64);
    function publicInputsSchemaHash() external view returns (bytes32);
    function publicInputsSchemaURI() external view returns (string memory);
    function verificationKeyURI() external view returns (string memory);
    function proofSystem() external view returns (bytes4);
}
```
