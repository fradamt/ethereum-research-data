---
source: ethresearch
topic_id: 23907
title: A small step towards data-driven protocol decisions - Unified SlowBlock metrics across clients
author: CPerezz
date: "2026-01-21"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/a-small-step-towards-data-driven-protocol-decisions-unified-slowblock-metrics-across-clients/23907
views: 89
likes: 1
posts_count: 1
---

# A small step towards data-driven protocol decisions - Unified SlowBlock metrics across clients

# Cross-Client Execution Metrics Specification

**Original Proposal doc & spec by [@rjl493456442](/u/rjl493456442)**: [Standardized Ethereum Performance Metrics - HackMD](https://hackmd.io/dg7rizTyTXuCf2LSa2LsyQ)

This was initiated by [Gary, when he implemented Slow block logging in Geth](https://github.com/ethereum/go-ethereum/pull/33442). From there, I thought this would be super useful for a lot of things as listed below and collaborated with him on standarizing this and bringing this vision forward.

In my mind this could help repricings and ScaleL1 tracks as well as bloatnet (my current focus). **Though I think we can do a lot more than that.**

---

## 1. Introduction & Motivation

### Why This Initiative Exists

Ethereum’s multi-client philosophy is a core strength—but it creates a challenge: **how do we compare performance across implementations?**

Standardized execution metrics solve this by enabling:

- Cross-client performance comparison — Fair, apples-to-apples benchmarking
- Network health monitoring — Identify execution bottlenecks before they impact consensus
- Data-driven protocol research — Validate EIP proposals with real execution data
- Anomaly detection — Detect unusual blocks (high gas, complex state access patterns)

### Real-World Example: EIP-7907 Analysis

The [EIP-7907 analysis](https://ethresear.ch/t/data-driven-analysis-on-eip-7907/23850) demonstrates exactly why standardized execution metrics are critical.

Using Geth metrics, I measured:

- Code read latency: 107ms to 904ms depending on bytecode size
- Per-call overhead scaling: 5.9µs to 49.9µs (8.5x increase from smallest to largest contracts)
- Block execution breakdown: Isolating code reads, account reads, EVM execution, and database writes

All of these insights helped taking a much more informed decision. Thus streamlining the ACD decision-making process a lot.

## 2. Core Metrics

Metrics are organized into categories covering the block execution lifecycle:

| Category | JSON Path | Description |
| --- | --- | --- |
| Block Info | block.* | Block number, hash, gas used, transaction count |
| Timing | timing.* | Execution, validation, commit, and total time in milliseconds |
| Throughput | throughput.* | Mgas/sec processing rate |
| State Reads | state_reads.* | Account, storage, and code read operations |
| State Writes | state_writes.* | Account and storage mutations |
| Cache | cache.* | Hit/miss rates for account, storage, and code caches |

### Metric Definitions

| Metric | Type | Description |
| --- | --- | --- |
| block.number | int64 | Block height |
| block.hash | string | Block hash (0x-prefixed) |
| block.gas_used | int64 | Total gas consumed |
| block.tx_count | int32 | Number of transactions |
| timing.execution_ms | int64 | Time spent executing transactions |
| timing.state_read_ms | int64 | Time spent on state read (accounts, storage slots and contract codes) |
| timing.state_hash_ms | int64 | Time spent on state rehashing |
| timing.total_ms | int64 | Total block processing time |
| throughput.mgas_per_sec | float64 | Gas throughput (gas_used / execution_time / 1e6) |
| state_reads.accounts | int64 | Account data loads (balance, nonce, code hash) |
| state_reads.storage_slots | int64 | Storage slot reads |
| state_reads.code | int64 | Contract bytecode reads |
| state_reads.code_bytes | int64 | Total bytes of code read |
| state_writes.accounts | int64 | Account state updates |
| state_writes.storage_slots | int64 | Storage slot writes |
| state_writes.code | int64 | Contract bytecode writes |
| state_writes.code_bytes | int64 | Total bytes of code write |
| cache.{type}.hits | int64 | Cache hits for account/storage/code |
| cache.{type}.misses | int64 | Cache misses (required DB reads) |
| cache.{type}.hit_rate | float64 | Hit percentage: (hits / (hits + misses)) * 100.0 |

## 3. Slow Block JSON Format

When block execution exceeds a configurable threshold (default: 1000ms), clients output a structured JSON log:

```json
{

"level": "warn"
"msg": "Slow block"
"block": {
    "number": 19234567
    "hash": "0x1234...abcd"
    "gas_used": 29500000
    "tx_count": 234
  }
"timing": {
    "execution_ms": 1250
        "state_read_ms": 320
    "state_hash_ms": 150
    "commit_ms": 75
    "total_ms": 1475
  }
"throughput": {
    "mgas_per_sec": 23.60
  }
"state_reads": {
    "accounts": 5420
    "storage_slots": 12340
    "code": 890
    "code_bytes": 456000
  }
"state_writes": {
    "accounts": 234
    "storage_slots": 1890
  }
"cache": {
    "account": { "hits": 4800, "misses": 620, "hit_rate": 88.60 }
    "storage": { "hits": 10200, "misses": 2140, "hit_rate": 82.68 }
    "code": { "hits": 870, "misses": 20, "hit_rate": 97.75 }
  }
}

```

### Field Requirements

| Field | Required | Notes |
| --- | --- | --- |
| level, msg |  | Must be "warn" and "Slow block" |
| block.* |  | All block info fields required |
| timing.execution_ms |  | Core timing metric |
| timing.state_read_ms |  | Time spent reading state from DB/cache |
| timing.state_hash_ms |  | Time spent on Merkle trie rehashing |
| timing.commit_ms |  | Time spent persisting state to storage |
| timing.total_ms |  | End-to-end block processing time |
| throughput.mgas_per_sec |  | 2 decimal places |
| state_reads.* |  | All read counters |
| state_writes.* |  | All write counters |
| cache.* |  | Nested structure with hits/misses/hit_rate |

## 4. Implementation Status

| Client | Status | PR |
| --- | --- | --- |
| Geth | Complete | #33655 |
| reth | Complete | #21237 |
| Besu | Complete | #9660 |
| Nethermind | Complete | #10288 |

## 5. Further Improvements

Mid-term goals for more fine-grained performance analysis:

| Improvement | Description | Rationale |
| --- | --- | --- |
| Per-transaction metrics | Timing and state access per individual tx | Identify specific transactions causing slowdowns |
| EVM opcode counts | SLOAD, SSTORE, CALL, CREATE, EXTCODECOPY | Understand execution patterns, detect DoS vectors |
| Unique access tracking | Unique accounts, storage slots, contracts | Measure state access diversity and working set size |
| Precompile breakdown | Per-precompile timing (ecrecover, sha256, modexp) | Identify expensive cryptographic operations |
| Merkleization timing | Account tree vs storage tree re-hashing | Pinpoint state root computation costs |
| Memory/allocation stats | Peak memory usage, allocations per block | Track memory pressure for resource planning |
| Trie depth statistics | Average/max trie traversal depth | Understand state bloat impact |
| Parallel execution metrics | Thread utilization, contention stats | For parallel EVM implementations |
| Witness size | Verkle/stateless witness data size | Preparation for stateless clients |
| Cold vs warm access | Distinguish first-access vs cached access | EIP-2929 gas analysis |

This post doesn’t only want to inform about this, but it wssentially seeks feedback. We want to know what else would be interesting for teams, researchers and anyone else to be able to extract/know. Internal data from clients hard to collect for them etc..

Also, we would like to know what we could do with this, we have some ideas, and here we listed some more goals. But we belive people will have a lot more ideas than just us.

Thanks.
