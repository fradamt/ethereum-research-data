---
source: magicians
topic_id: 26502
title: Glamsterdam upgrade non-headliner scoping (Execution Layer)
author: abcoathup
date: "2025-11-10"
category: Protocol Calls & happenings
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/glamsterdam-upgrade-non-headliner-scoping-execution-layer/26502
views: 233
likes: 2
posts_count: 3
---

# Glamsterdam upgrade non-headliner scoping (Execution Layer)

Draft shortlist of CFI/DFI Execution Layer EIPs based on client team writeup of preferences ([Erigon](https://github.com/erigontech/erigon/wiki/Glamsterdam-PFI-stand), [Geth](https://notes.ethereum.org/@fjl/geth-glamsterdam-eip-ranking), [Nethermind](https://x.com/URozmej/status/1986040895578296825), [Reth](https://hackmd.io/@jenpaff/S1bj9gqkbe) & [Besu](https://hackmd.io/@RoboCopsGoneMad/GlamTiers)) and discussions at [All Core Devs - Execution (ACDE) #224, November 6, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-224-november-6-2025/25950/)

[@adietrichs](/u/adietrichs) is compiling an official shortlist

[@Christine_dkim](/u/christine_dkim) writeup:

- Developer Sentiment Toward Individual EIPs Proposed for Glamsterdam - Google Sheets
- X Vizualisation

This is a wikipost, please update with corrections/additions.

## EL EIPs

| Category | EIP | EIP Title | Shortlist | Geth | Erigon | Nethermind | Besu | Reth | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Repricing – Core | EIP-2780 | Reduce intrinsic transaction gas |  |  |  |  |  |  |  |
| Repricing – Core | EIP-7904 | General Repricing |  |  |  |  |  |  | Check Erigon feedback |
| Repricing – Core | EIP-7976 | Increase Calldata Floor Cost |  |  |  |  |  | - |  |
| Repricing – Core | EIP-7981 | Increase access list cost |  |  |  |  |  | - |  |
| Repricing – Core | EIP-8037 | State Creation Gas Cost Increase |  |  |  | - |  | - |  |
| Repricing – Core | EIP-8038 | State-access gas cost increase |  |  |  | - |  | - |  |
| Repricing – Recommended Additions | EIP-7778 | Block Gas Limit Accounting without Refunds |  |  |  |  |  | - |  |
| Repricing – Recommended Additions | EIP-7971 | Hard Limits for Transient Storage |  |  |  |  |  | - |  |
| Repricing – Recommended Additions | EIP-8032 | Size-Based Storage Gas Pricing |  |  |  |  |  | - |  |
| Repricing – Recommended Additions | EIP-8053 | Milli-gas for High-precision Gas Metering |  |  |  | - |  | - |  |
| Repricing – Recommended Additions | EIP-8059 | Gas Units Rebase for High-precision Metering |  |  |  | - |  | - |  |
| Repricing – Recommended Additions | EIP-8058 | Contract Bytecode Deduplication Discount |  |  |  |  |  | - |  |
| Repricing – Possible Additions | EIP-2926 | Chunk-Based Code Merkleization |  |  |  | - |  | - |  |
| Repricing – Possible Additions | EIP-7686 | Linear EVM memory limits |  | - |  | - | - | - |  |
| Repricing – Possible Additions | EIP-7923 | Linear, Page-Based Memory Costing |  |  |  | - | - |  |  |
| Repricing – Possible Additions | EIP-7973 | Warm Account Write Metering |  | - |  | - | - | - | Author simplifying |
| Repricing – Possible Additions | EIP-8011 | Multidimensional Gas Metering |  | - |  |  | - | - |  |
| Repricing – Possible Additions | EIP-8057 | Inter-Block Temporal Locality Gas Discounts |  |  |  |  | - | - |  |
| EVM Execution & Opcodes | EIP-5920 | PAY opcode |  | - |  | - | - | - |  |
| EVM Execution & Opcodes | EIP-7610 | Revert creation in case of non-empty storage |  |  |  | - |  |  | Already implemented, either reinforce rule or change rule |
| EVM Execution & Opcodes | EIP-7843 | SLOTNUM opcode |  |  |  |  | - | - |  |
| EVM Execution & Opcodes | EIP-7791 | GAS2ETH opcode |  |  |  | - | - | - |  |
| EVM Execution & Opcodes | EIP-7819 | SETDELEGATE instruction |  | - |  | - | - | - |  |
| EVM Execution & Opcodes | EIP-7979 | Call and Return Opcodes for the EVM |  | - |  | - | - | - |  |
| EVM Execution & Opcodes | EIP-8013 | Static relative jumps and calls for the EVM |  |  | - | - | - | - |  |
| EVM Execution & Opcodes | EIP-8024 | Backward compatible SWAPN, DUPN, EXCHANGE |  |  |  |  |  |  |  |
| Serialization & Data Structures | EIP-6404 | SSZ transactions |  |  |  | - |  | - |  |
| Serialization & Data Structures | EIP-6466 | SSZ receipts |  |  |  | - |  | - |  |
| Serialization & Data Structures | EIP-7688 | Forward compatible consensus data structures |  | - |  | - | - | - |  |
| Contract Deployment & Code | EIP-7903 | Remove Initcode Size Limit |  |  |  | - | - | - |  |
| Contract Deployment & Code | EIP-7907 | Meter Contract Code Size And Increase Limit |  |  |  | - | - |  |  |
| Contract Deployment & Code | EIP-7997 | Deterministic Factory Predeploy |  |  |  | - | - | - |  |
| Cryptography & Signatures | EIP-7619 | Precompile Falcon512 generic verifier |  | - | - | - |  | - |  |
| Cryptography & Signatures | EIP-7932 | Secondary Signature Algorithms |  |  |  | - |  | - |  |
| Cryptography & Signatures | EIP-8030 | P256 transaction support |  |  |  | - | - | - |  |
| Cryptography & Signatures | EIP-8051 | Precompile for ML-DSA signature verification |  | - | - | - |  | - |  |
| Transaction & Block Features | EIP-7668 | Remove bloom filters |  |  |  | - |  | - |  |
| Transaction & Block Features | EIP-7708 | ETH transfers emit a log |  |  |  | - |  |  |  |
| Transaction & Block Features | EIP-7745 | Trustless log index |  |  |  |  |  | - |  |
| Transaction & Block Features | EIP-7793 | Conditional Transactions |  |  |  | - |  | - |  |
| Transaction & Block Features | EIP-7872 | Max blob flag for local builders |  |  |  | - |  | - | Doesn’t require hardfork |
| Transaction & Block Features | EIP-7919 | Pureth - Provable RPC responses |  | - | - | - | - | - |  |
| Transaction & Block Features | EIP-7949 | Genesis File Format |  |  |  | - |  | - | Doesn’t require hardfork |
| Transaction & Block Features | EIP-8070 | Sparse Blobpool |  |  | - | - |  | - |  |

## Replies

**charles-cooper** (2025-11-10):

i want to point out that EIP-8024 has no discussions-to thread and so there is nowhere to provide feedback on it

---

**frangio** (2025-11-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png)

      [EIP-8024: Backward compatible SWAPN, DUPN, EXCHANGE](https://ethereum-magicians.org/t/eip-8024-backward-compatible-swapn-dupn-exchange/25486) [EIPs](/c/eips/5)




> Discussion topic for EIP-8024.
> This is a fork of EIP-663 without a dependency on EOF.
> Update Log
>
> 2025-09-06: initial proposal to update EIP-663
> 2025-09-15: decision to fork as new EIP
> 2025-11-04: updated encode_pair, decode_pair to fix inconsistency between spec and examples

As far as I can tell this is properly linked everywhere (EIP, Forkcast). Let me know if the link is missing somewhere.

