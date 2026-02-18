---
source: magicians
topic_id: 25483
title: "EIP-8022: Calldata run-length encoding scheme"
author: Vectorized
date: "2025-09-16"
category: EIPs
tags: [eip, compression]
url: https://ethereum-magicians.org/t/eip-8022-calldata-run-length-encoding-scheme/25483
views: 71
likes: 4
posts_count: 1
---

# EIP-8022: Calldata run-length encoding scheme

## Motivation

At the time of writing, Ethereum calldata often contains long sequences of zero bytes. This arises primarily from the Solidity ABI specification, which pads values to 32-byte words, and is further reinforced by common data patterns such as sparse vectors, Merkle proofs, and cryptographic arguments.

This proposal standardizes a simple, deterministic run-length encoding (RLE) scheme tailored for calldata. Establishing a canonical encoding ensures that future work can rely on a common reference implementation. Potential applications include, but are not limited to:

- Transaction compression schemes.
- Automatic packing of calldata and storage values.
- Precompiles to efficiently compress and decompress data.

By providing a minimal and bounded codec, this standard enables experimentation and lays the groundwork for more efficient use of Ethereum bandwidth and storage.

## Implementation

Reference implementations are available:

- JavaScript (hex-encoded strings)
- Solidity (bytes)

Reference implementation in some other language TBD.

## Rationale

This RLE scheme was chosen for its simplicity, predictability, and bounded runtime:

- O(n) worst-case cost (compute and memory), with expansion bounds that can be inferred in constant time. No risk of “zip bomb” style exploits.
- Streaming-friendly: can be encoded/decoded in a single pass without allocating large buffers.
- Not CPU-bound: processing will be dominated by network, memory, and storage bandwidth, which are the true bottlenecks in calldata-heavy systems.

### Bitwise negation of the first 4 bytes

The first 4 bytes of calldata are used as function selectors. By negating these 4 bytes, compressed calldata will naturally route to the contract’s `fallback` function. The fallback can then decompress and forward the call back to the intended function via `DELEGATECALL`.

This adds only a minuscule O(1) compute cost, and can be left in place even for applications that do not require this feature. A single canonical format improves code reuse and avoids confusion.

### Up to 128 consecutive 0x00 bytes

The EVM provides a convenient way to zeroize memory regions by copying out-of-bounds calldata or code. On the processor level, most CPUs also have dedicated micro-ops for zeroing memory.

For this RLE scheme, runs of up to 128 consecutive `0x00` bytes are supported. In the control byte, 1 bit denotes the run type (`0x00` vs `0xFF`), and the remaining 7 bits encode the run length (`0b1111111 + 1 = 128`).

### Up to 32 consecutive 0xFF bytes

Unlike zeros, the EVM does not provide a convenient way to fill memory with `0xFF`. The most efficient method is `MSTORE`, which writes 32 bytes per operation. Therefore, the maximum run length for `0xFF` is capped at 32.

We select `0xFF` as the second RLE-eligible byte because it has semantic meaning in many applications: maximum unsigned integer values are often used as sentinels or to represent “infinite approvals”.

### No other RLE-eligible bytes

Allowing arbitrary non-zero bytes to be RLE-compressed would complicate the encoding and reduce its expected efficiency. Limiting RLE to `0x00` and `0xFF` strikes a balance between compression gains and implementation simplicity.

### Rationale for an EIP

While the codec itself could be an ERC-level convention, the intended applications include precompiles and new transaction types, both of which require changes clients. ERCs cannot define such changes, and RIPs are limited to rollups. As an EIP, this specification provides a stable reference for both L1 and L2, with a path to protocol integration.
