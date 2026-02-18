---
source: ethresearch
topic_id: 20098
title: What is "RealTPS" in Blockchain
author: rrhlrmrr
date: "2024-07-19"
category: Tools
tags: []
url: https://ethresear.ch/t/what-is-realtps-in-blockchain/20098
views: 2522
likes: 5
posts_count: 3
---

# What is "RealTPS" in Blockchain

Authors: [@Kyungmin](https://x.com/Kyungmin7984) [@bicoCrypto](https://github.com/bicoCrypto) [@solmingming](https://github.com/solmingming) Members of [@DecipherGlobal](https://x.com/DecipherGlobal) SNU Blockchain Research Center

## TL;DR

The current concept of TPS (Transactions Per Second) in blockchain is being disclosed in an ambiguous and opaque manner, conflicting with blockchain’s core value of transparency. This article reconsiders the definition of transactions in blockchain, compares theoretical figures with actual measurements, evaluates existing measurement tools, introduces our self-developed tool, and proposes a more accurate and transparent TPS measurement method.

## Problem

The biggest change in the transition from Web2 to Web3 is decentralization. This has led to improved system accessibility and increased information transparency. However, there is still opaque information in the blockchain ecosystem, with TPS being a prime example.

In transaction processing systems, especially financial systems, TPS is a crucial performance indicator. However, the TPS information currently provided in blockchain is limited to simple figures, with detailed information about measurement methods and processes remaining opaque.

While blockchain smart contracts are operated transparently through verification and auditing, we still rely on the foundation’s system for the blockchain nodes themselves, lacking verification procedures similar to smart contracts.

## TPS in traditional Web2

When discussing blockchain TPS, VISA’s processing capability is often mentioned as a comparison. [VISA officially announced a processing capability of 24,000 TPS](https://www.reddit.com/r/nanocurrency/comments/82438o/visa_is_capable_of_performing_24000_transactions/), but [this has been questioned](https://news.bitcoin.com/no-visa-doesnt-handle-24000-tps-and-neither-does-your-pet-blockchain/):

In centralized Web2 systems, it’s difficult to verify such issues. However, blockchain (Web3) systems are decentralized and their code is managed as open source, making it possible to verify TPS.

## TPS in Web3

In blockchain systems with public nodes and permissionless nodes, anyone can participate in the network, operate nodes, and access the system. Even without connecting to the mainnet or testnet, the source code is publicly available, allowing independent network construction or modification after forking.

Ethereum and most EVM-compatible blockchains publish high TPS figures. For example, Avalanche C-Chain is introduced as capable of achieving 4,500 TPS. However, information on how this figure was measured is not provided.

[![Image](https://ethresear.ch/uploads/default/optimized/3X/7/4/748ee3c646e8c2964dd294eefe5aa1491ce65b45_2_690x378.jpeg)Image1200×658 61.5 KB](https://ethresear.ch/uploads/default/748ee3c646e8c2964dd294eefe5aa1491ce65b45)

## Time to Define Transaction

In EVM blockchains, the term “Transaction” is used in various contexts:

- SendTransaction: Simply refers to the act of sending a transaction, without guaranteeing the final state or completeness of the transaction.
- PendingTransaction: The state where a transaction is waiting in the node’s memory pool (Mempool).
- QueuedTransaction: Similar to Pending, waiting in the node’s memory pool, but distinguished in the serialization process through Nonce.
- ConfirmedTransaction: The state where a transaction receipt has been issued, indicating the transaction has succeeded or failed.

We believe that TPS should be calculated based on ConfirmedTransactions when measuring. Based on this, we propose the following formula for calculating TPS:

TPS = BlockGasLimit / (TxGasUsed * BlockCreationTime)

Currently, Avalanche C-Chain’s BlockGasLimit is 15,000,000

[![Tx Gaslimit](https://ethresear.ch/uploads/default/optimized/3X/c/9/c909ced7994a754fc7875e8dd1730093faedad3e_2_690x225.png)Tx Gaslimit2984×976 173 KB](https://ethresear.ch/uploads/default/c909ced7994a754fc7875e8dd1730093faedad3e)

Even assuming the simplest transaction (TxGasUsed = 21,000) and the shortest block creation time (BlockCreationTime = 1 second), the theoretical maximum TPS is 715. This shows a significant difference from the officially announced 4,500 TPS. (The actual measured value would naturally be even lower)

We speculate that this difference may occur due to:

- The transaction standard used in TPS calculation may not be ConfirmedTransaction
- The Avalanche version that achieved 4,500 TPS may differ from the version currently used in public nodes
- Differences in TPS measurement methods and methodologies

Such opaque information raises questions about the reliability and accuracy of TPS figures.

Monad has published a critical analysis of these limitations of blockchain TPS: [WTF is TPS?](https://www.monad.xyz/wtf-is-tps)

## TPS Benchmark Tools

There are currently two main blockchain TPS benchmark tools in use:

1. Hyperledger Caliper: Developed by the Hyperledger Foundation
2. ChainHammer: Recommended by Quorum (a private blockchain developed by ConsenSys)
Note: ChainHammer’s most recent commit was 2 years ago, making it essentially outdated.

Caliper is written in JavaScript and is a highly complete project. However, there are doubts about whether it is optimized for measuring “blockchain” TPS:

1. TPS measurement on a single node:
Figure21246×704 24.1 KB

The core of blockchain is distributed storage of data through consensus. However, Caliper only conducts TPS measurements on a single node, which can measure the TPS of individual nodes but does not accurately reflect the TPS of the entire blockchain network. (The transaction propagation process is not considered)

1. Limitation of measurement from a single account:
In EVM, EOA (Externally Owned Account) has a Nonce value, causing transactions to be processed sequentially.
While 2024 was predicted to be the era of parallel EVM, current parallel processing technology still proceeds in an optimistic manner, requiring re-execution in case of conflicts. (Cases requiring re-execution can hardly be considered true parallel execution.)
Therefore, execution from a single account versus multiple accounts can have a significant impact on TPS.

## AnTPS(An-ti TPS)

To improve these limitations, we have developed our own blockchain benchmark tool, AnTPS, using Golang: [Github](https://github.com/decipherhub/AnTPS)

Features include:

[![image](https://ethresear.ch/uploads/default/optimized/3X/f/0/f0cff11ba6f328b500e85b78f194763580ca940c_2_690x283.png)image3324×1364 176 KB](https://ethresear.ch/uploads/default/f0cff11ba6f328b500e85b78f194763580ca940c)

- Transparently providing measurement environment/results.
- Conducting measurements on at least two or more nodes.
- Supporting measurement cases for both single and multiple accounts.
- Supporting various scenarios during measurement (ERC20/721/1155/NativeToken).
- Supporting not only local environment measurements but also Cloud environments through IaC.

Our goal is to overcome the limitations of existing tools while providing information transparently.

We welcome your opinions and feedback. Thank you.

## Replies

**r4f4ss** (2024-07-19):

Thanks for this post, it is new to me this questioning about TPS measures and seems beneficial to have some standard.

![](https://ethresear.ch/user_avatar/ethresear.ch/rrhlrmrr/48/16210_2.png) rrhlrmrr:

> We believe that TPS should be calculated based on ConfirmedTransactions when measuring. Based on this, we propose the following formula for calculating TPS:

![](https://ethresear.ch/user_avatar/ethresear.ch/rrhlrmrr/48/16210_2.png) rrhlrmrr:

> Conducting measurements on at least two or more nodes

Since ConfirmedTransactions are written in the blockchain and are irreversible and synchronized among all nodes of the network (I am not considering reorgs), why use two nodes to measure?

---

**rrhlrmrr** (2024-07-19):

As you know, the reason for measuring with two nodes is that blockchain is a distributed ledger system. If we measure with just one node, we’re only measuring the TPS of that node, which can hardly be considered as measuring the TPS of the blockchain system.

In a situation where there’s no volume backup for a single node, if that node faults, all the data would be lost.

For these reasons, we conducted our measurements using two or more nodes.

