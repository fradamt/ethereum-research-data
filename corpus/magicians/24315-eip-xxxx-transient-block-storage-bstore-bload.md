---
source: magicians
topic_id: 24315
title: "EIP-XXXX: Transient Block Storage (`BSTORE`, `BLOAD`)"
author: EricForgy
date: "2025-05-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-xxxx-transient-block-storage-bstore-bload/24315
views: 94
likes: 0
posts_count: 1
---

# EIP-XXXX: Transient Block Storage (`BSTORE`, `BLOAD`)

This post introduces a proposed new EVM feature: **Transient Block Storage** - a block-scoped key-value store that:

- Persists across all transactions within a single block
- Is automatically cleared at the end of the block
- Enables native onchain coordination between multiple transactions
- Complements EIP-1153’s transient storage (which is tx-scoped)

We propose two new opcodes:

- BSTORE(bytes32 key, bytes32 value) - sets a value for the current block
- BLOAD(bytes32 key) returns (bytes32) - retrieves a value (returns 0 if unset)

### Motivation

EIP-1153 introduced transient storage for ephemeral intra-transaction state. However, many advanced protocols require ephemeral state that **spans multiple transactions in the same block**, but is still **cleared at block end**. Transient Block Storage offers a native mechanism for:

- Aggregating multi-user intents across a block
- Executing batched or netted finalizations only once per block
- Coordinating protocols in a gas-efficient, onchain-native way
- Enabling Application-Specific Sequencing (ASS) to combat MEV

Today, these goals require costly or centralized workarounds:

- Persistent storage (gas-heavy, requires cleanup)
- Offchain mempools or relays (introduce trust and censorship risk)
- Rollup-native sequencers (fragmented and L2-specific)

Transient Block Storage fills this gap at the base layer.

### Key Use Cases

#### MEV Resistance via Application-Specific Sequencing

Protocols can implement **Application-Specific Sequencing** using Transient Block Storage:

1. Users submit signed intents via public registerIntent() calls
2. Intents are recorded in transient block storage
3. At the end of the block, the protocol deterministically processes the full set via finalizeBlock():

Canonical order (FIFO, gas price, reputation, etc.)
4. Netting, batching, matching

This eliminates frontrunning and sandwich attacks by **deferring execution until after intent collection is complete** - without any offchain infra or special builder privileges.

#### Multi-Asset Batching (Multiswap)

In [Multiswap](https://caval.re/docs/introducing-multiswap/overview), a multi-asset AMM, users trade multiple tokens into and out of a shared pool. To minimize slippage and maximize capital efficiency:

- Users submit swap intents throughout the block
- The protocol aggregates all intents in transient block storage
- A finalizer calls finalizeBlock() at block end, solving a single master equation for all trades
- The net trade is executed atomically across all assets

**All users receive execution at the same fair prices**, determined by the global value-preserving equation. There is no opportunity for frontrunning or preferential execution, since pricing is based on the aggregate net flow rather than transaction order.

Transient Block Storage enables this by holding intents onchain during the block without polluting persistent storage or incurring high gas costs.

### Semantics

- Key-value storage (bytes32 => bytes32)
- Shared across all contracts and transactions in the current block
- Cleared at block end by client implementation
- Not persisted to the state trie
- Not eligible for gas refunds
- Opcodes:

BSTORE(key, value)
- BLOAD(key)

### Design Considerations

- Cost: Read/write gas costs should be lower than SSTORE and similar to TSTORE
- Client requirements: Requires block-local memory structure, flushed at block finalization
- Abuse prevention: Recommend key hashing and namespaces to avoid cross-contract collisions
- Finalization: Execution of stored intents can be permissioned, decentralized, or randomized

### Update Log

- 2025-05-22: Initial draft, [GitHub PR link TBD]

### External Reviews

None as of 2025-05-22.

### Outstanding Issues

None as of 2025-05-22.
