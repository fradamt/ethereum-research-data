---
source: magicians
topic_id: 25786
title: "ERC-8047: Forensic Token (Forest)"
author: MASDXI
date: "2025-10-14"
category: ERCs
tags: [token, erc1155, cft, aml]
url: https://ethereum-magicians.org/t/erc-8047-forensic-token-forest/25786
views: 160
likes: 3
posts_count: 3
---

# ERC-8047: Forensic Token (Forest)

Discussion topic for ERC-8047: Forensic Token (Forest)



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/1256)














####


      `master` ← `MASDXI:master`




          opened 08:08AM - 15 Oct 25 UTC



          [![](https://avatars.githubusercontent.com/u/31649128?v=4)
            MASDXI](https://github.com/MASDXI)



          [+353
            -0](https://github.com/ethereum/ERCs/pull/1256/files)







A DAG-inspired token enabling hierarchical token traceability and efficient enfo[…](https://github.com/ethereum/ERCs/pull/1256)rcement for compliance use cases like CBDCs or regulated digital money. It introduces parent–child transaction relationships and supports O(1) enforcement across linked tokens












#### Update Log

- 2025-10-13: Initiate topic for discussion
- 2025-11-13: Update Specification and Rationale Section
- 2025-11-14: Update Specification Section (URI Schema)
- 2025-11-24: Update TL;DR
- 2026-01-16: Receive comment from EIP editor; See
- 2026-02-02: Update Specification and Rationale Section

#### External Reviews

- None as of 2025-10-13

#### Outstanding Issue

- None as of 2025-10-13

> After a pull request is created and an ERC number is assigned, all changes will be managed through pull requests. This topic provides an initial draft version to help those who are not familiar with using GitHub.
> Note: This topic will be updated over time to stay in sync with the pull request, but updates may be slow.

### TL;DR

> Current fungible token standards (like ERC-20) can’t track the lineage of individual token units, making it impossible to distinguish clean value from tainted value or apply precise enforcement. UTXO models offer per-unit traceability, but they still fail in practice because mixers and transaction batching easily break the trace chain.
> Forest provides fungible tokens with serial-number and level-based traceability plus hierarchical enforcement that mixing cannot bypass while keeping a simple ERC-1155 interface for daily e-money use.

## Abstract

Forest is a [DAG](https://www.geeksforgeeks.org/introduction-to-directed-acyclic-graph/)-inspired token model designed to enhance traceability and regulatory compliance in digital currency systems. By introducing hierarchical token tracking, it enables efficient enforcement on any token linked to suspicious activity with level/root. Enforcement actions, such as freezing specific tokens or partitioning all tokens with relational links, are optimized to operate at O(1) complexity.

## Motivation

The present-day Central Bank Digital Currency (CBDC) and Private Money concept aims to utilize the advantages of blockchain or Distributed Ledger Technology (DLT) that provide immutability, transparency, and security, and it adopts smart contracts, which play a key role in creating programmable money. However, technology itself gives an advantage and eliminates the ideal problem of compliance with the regulator and the Anti-Money Laundering and Countering the Financing of Terrorism (AML/CFT) standard, but it does not seem practical to be done in the real world and is not efficiently responsible for the financial crime or incidents that occur in the open network of economics.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Compatible implementations **MUST** implement the `IERC8047` interface and **MUST** inherit from [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) and [ERC-5615](https://eips.ethereum.org/EIPS/eip-5615) interfaces. All functions defined in the interface **MUST** be present and all function behavior **MUST** meet the behavior specification requirements below.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity >=0.8.0
Restrict all transactions with specific root `id`.

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/8/d/8dfdb9d9581e33d8cc86be4b7ca9cb42dad3ef15_2_690x355.png)image1020×525 58 KB](https://ethereum-magicians.org/uploads/default/8dfdb9d9581e33d8cc86be4b7ca9cb42dad3ef15)

### Reverse Topological Ordering of Transactions

One of the key benefits of the `Forest` is that it natively supports reverse topological traversal. Each token stores a reference to its parent token, allowing to efficiently iterate `parentOf` back to the `root` of the `DAG`.

This back-to-root traversal differs from a full `DAG` traversal. It only follows the lineage of a specific token `id` up to its `root`, rather than visiting all transactions in the `DAG`.

[![image](https://ethereum-magicians.org/uploads/default/original/3X/8/c/8c968071433634ac466b0b1d84c26c9daf0c3177.png)image276×211 13.8 KB](https://ethereum-magicians.org/uploads/default/8c968071433634ac466b0b1d84c26c9daf0c3177)

### Spendable balance via off-chain

On-chain iteration to retrieve `spendableBalanceOf` can be gas-intensive and inefficient, especially for large DAGs or multiple sets of DAGs. To address this, the current `spendableBalanceOf` account can be determined off-chain by deploying a service that subscribes to events emitted by the contract. This service calculates the spendable balance by reconciling the account’s total `balanceOf` with any tokens that have been frozen or restricted due to hierarchical or forensic rules, providing an accurate representation of the amount available for `transfer`.

## Backwards Compatibility

This standard is fully compatible with [ERC-1155](https://eips.ethereum.org/EIPS/eip-1155) and [ERC-5615](https://eips.ethereum.org/EIPS/eip-5615)

## Security Considerations

### Denial Of Service

Run out of gas problem due to the operation consuming more gas if transferring in `safeBatchTransferFrom`.

### Gas Limit Vulnerabilities

Exceeds block gas limit if the blockchain has a block gas limit lower than the gas used in the transaction.

### Data Fragmentation

The `Forest` model tracks all assets within the system, which can be represented mathematically as

```plaintext
A^d: The decimals of the asset.
A^t: The total supply of the asset.
A^s: The possible asset is represented in the id.
A^s = A^t x A^d
```

While this ensures precision, the high granularity can increase storage needs.

Traditional finance often uses simpler `decimals` like `2`, `4` or `6`, avoiding excessive detail.

Adopting similar strategies could help balance granularity with efficiency. Or limit value as `MINIMUM_AMOUNT` check before spending.

### Confidentiality

Maybe it can be linked to identity. from spending and behavior usage

### High Complexity

`Forest` may introduce potential vulnerabilities such as reentrancy or misbehavior when applied with other smart contracts.

## Standard and knowledge-based that might related to this topic

- BIS: An approach to anti-money laundering compliance for crypto assets
- Directed Acyclic Graph (DAG)
- Unspent Transaction Output (UTXO)
- What is money?
- ERC-20R and ERC-721R: Reversible Transactions on Ethereum
- Chia Clawback feature
- FATF: Asset Recovery Guidance and Best Practices

## Historical links related to this topic

- ERC-1155
- ERC-1400
- ERC-3643

#### [WIP] Reference implementation


      ![](https://github.githubassets.com/favicons/favicon.svg)

      [github.com](https://github.com/MASDXI/erc8047/tree/develop)





###



[develop](https://github.com/MASDXI/erc8047/tree/develop)



Reference implementation of ERC-8047 Forensic Token (Forest) - MASDXI/erc8047

## Replies

**zero** (2025-11-16):

Interesting, Has it already been implemented?

---

**MASDXI** (2025-11-24):

Not finish yet. still shaping/revise more.

