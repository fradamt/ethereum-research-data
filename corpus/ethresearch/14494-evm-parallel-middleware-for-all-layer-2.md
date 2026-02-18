---
source: ethresearch
topic_id: 14494
title: EVM Parallel Middleware for all Layer 2
author: wiger
date: "2022-12-27"
category: Sharding
tags: []
url: https://ethresear.ch/t/evm-parallel-middleware-for-all-layer-2/14494
views: 2699
likes: 0
posts_count: 6
---

# EVM Parallel Middleware for all Layer 2

An EVM parallel middleware for all Layer 2

# What

Transactions can be executed in parallel

# Why

Increase TPS over 1000%+

# How

## State Verification Machine

For each transaction, find out which on-chain data needs to be modified without actually executed.

e.g.,

Input:

- Txn 1: {0xaaa → 100 ETH → 0xbbb},
- Txn 2: {0xbbb → 50 ETH → 0xccc},
- Txn 3: {0xeee → 30 BTC → 0xfff},

Output:

- SV(Txn 1) = {0xaaa.eth.balance, 0xbbb.eth.balance},
- SV(Txn 2) = {0xbbb.eth.balance, 0xccc.eth.balance},
- SV(Txn 3) = {0xeee.btc.balance, 0xfff.btc.balance}.

So SV(Txn 1) ∧ SV(Txn 2) ≠ ∅, SV(Txn 1) ∧ SV(Txn 3) = ∅, SV(Txn 2) ∧ SV(Txn 3) = ∅,

state verification machine will return the DAG: {{Txn 1, Txn 2}, {Txn 3}}.

All the DAG graph construction are done off-chain, 1,000,000,000 transactions in 1 second.

## DAG Graph

Get all possibilities of parallel transactions through DAG.

## Synchronous Build

Transactions are placed in blocks synchronously by multiple sequencers.

## Replies

**wiger** (2022-12-27):

Middleware Feature

- Parallel transaction: Design the first EVM-compatible parallel transaction system, with at least a 3-fold increase in TPS of Layer 2.
- Elastic scaling: Reasonable resource allocation mechanism, making it friendlier to high and low-occupancy dApps of Layer 2.
- Decentralized Sequencer: Resistant to MEV arbitrage, and prevent 51% attacks, providing a fair and reasonable environment for traders.
- Compatible with OP => Compatible with ZK: Could be converted into middleware, compatible with fraud-proof Layer 2s first, eventually fully compatible with zk-proof Layer 2s.

---

**wiger** (2022-12-27):

## Constructing DAG Graph

The transactions are constructed as vertices in the graph

The order of transactions is constructed as edges.

## Graph Partition Components

Using partitioning algorithms, the graph is constructed as multiple independent subsets that can be parallelized.

## Separating Construction Nodes and Execution Nodes

To prevent construction nodes and execution nodes from being the same node and thereby behaving maliciously, we separate their functions, similar to the way PBS does.

## Group Execution Module

Multiple non-conflicting groups of transactions are input to multiple groups of peer nodes, with each group having one sequencer for execution and multiple peer nodes for voting.

## Block Synchronization

Using the execution timestamps of different groups to construct a timeline, while also introducing bias to achieve ordered Nonce and Block height.

## Converting Unordered Blocks to Linear

Using batch-committer to convert parallel results to linear, returning to the normal settlement process of Layer 2 and Layer 1, while preserving the structure and process of the State Root.

---

**wiger** (2022-12-30):

## Example

[![image](https://ethresear.ch/uploads/default/original/2X/c/c82860591281e9cbdaf7dc0dcff08f28015b99e5.png)image640×480 15 KB](https://ethresear.ch/uploads/default/c82860591281e9cbdaf7dc0dcff08f28015b99e5)

[![image](https://ethresear.ch/uploads/default/original/2X/0/05a5b5bc2db9a4dc6d3d194e9abcd9b19fae3bfc.png)image640×480 17.5 KB](https://ethresear.ch/uploads/default/05a5b5bc2db9a4dc6d3d194e9abcd9b19fae3bfc)

---

**high_byte** (2023-01-01):

> For each transaction, find out which on-chain data needs to be modified without actually executed.

But to find out which on-chain data is needed, then the transaction needs to be executed, with the latest chain data.

A low hanging fruit way to do this is just by looking at accounts accessed, this includes storage, balance and code. Start by parallel executing all transactions, find any transactions that access same accounts, if any then re-execute the transaction(s) with higher transaction id.

---

**wiger** (2023-01-01):

Thanks for such a thoughtful response, we are looking for solution this way.

Similar to memory address. We run an simplified EVM to get all address, find any transactions that access same address lol.

```auto
S0  SEGMENT STACK
    DW  30 DUP(?)
TOP LABEL   WORD
S0  ENDS

S1  SEGMENT
TIP DB  "INPUT", 0DH, 0AH, 24H
ARY DW  20 DUP(0)
CRLF    DB  0DH, 0AH, 24H
N   DW  0
S1  ENDS
```

