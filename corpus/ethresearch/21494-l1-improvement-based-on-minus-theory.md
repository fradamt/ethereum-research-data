---
source: ethresearch
topic_id: 21494
title: L1 improvement based on Minus Theory
author: kernel1983
date: "2025-01-18"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/l1-improvement-based-on-minus-theory/21494
views: 782
likes: 11
posts_count: 5
---

# L1 improvement based on Minus Theory

# L1 improvement based on Minus Theory

## TLDR

The Minus Theory guides us to build blockchains in a new way, enabling very high TPS and asynchronous calculation of the global state. This could be used to improve existing ETH L1 or any other blockchains.

## Solution

The 'Minus’ed chain is said blockchain node should focus on achieving consensus on the messages (transactions) input to the chain, while moving verification, execution tasks, and the global state out of the blockchain node and into an indexer.

This design unlocks the ability for blockchain nodes to handle at least 10k TPS and potentially up to 200k TPS. The indexer can be continuously optimized with upcoming technologies such as parallel VMs or asynchronous calculation of the global state during traffic surges.

### Minus Theory

Minus Theory was created in January 2024. It was inspired by the popularity of inscriptions in 2023, but we developed the theory from a consensus perspective to separate verification from the consensus process. Its security is backed by state machine theory.

It doesn’t require ZK at all. Monad also shares this vision: Determined ordering implies state determinism. Similarly, based rollups design adopt a comparable approach by achieving consensus on the order of transactions on L1 while handling execution on L2. We believe that the L2 in based rollups design is equivalent to an indexer. So, why not focus on improving performance directly on L1?

Several links of Minus:



      [github.com](https://github.com/0xZentra/whitepaper/blob/7258bbf01046959f7b4c4eefde0b3b71aafac2a2/minus_theory.pdf)



    https://github.com/0xZentra/whitepaper/blob/7258bbf01046959f7b4c4eefde0b3b71aafac2a2/minus_theory.pdf

###











      ![](https://ethresear.ch/uploads/default/original/3X/4/5/454fca117c2b8893aa859fbd8b6642c36c8bd978.png)

      [Summer of Protocols – 11 Apr 24](https://forum.summerofprotocols.com/t/pig-thin-blockchain-protocol-based-on-minus-theory/850)



    ![image](https://ethresear.ch/uploads/default/optimized/3X/2/f/2fd6b1d1070b3d74853dfb8da49518433563e4a0_2_690x241.png)



###





          SoP 2024 RFC






            pig







Title Thin Blockchain Protocol based on Minus Theory  Team member names 0xKJ and Yanbo  Short summary of your improvement idea In early 2024 Dr KJ proposed the Blockchain Minus Theory showing a new direction to build the high performance...



    Reading time: 1 mins 🕑
      Likes: 2 ❤











https://mirror.xyz/0x719C8d75FAF8f1b117EA56205414892CAAb4A1b7/dI758Q-Cu22loklfSl7TQwlw31EQ33WS2TopEPGvwAg

### Zentra

After Minus Theory, we spent one year building an indexer named Zentra, which proves that the theory works in practice, not just on paper. Rather than using the EVM, Zentra brings Python to the blockchain. Zentra does not aim to be a Layer 1, so we are contributing this idea to the Ethereum community and the broader blockchain world, hoping it will help improve the blockchain infrastructure.

If the Ethereum community adopts this approach, the EVM can be moved from the node to the indexer. This shift would allow other indexers, like Zentra, to utilize L1 in a more cost-effective way while enabling the exploration of more complex applications developed in Python.

## Advantages

### Maintain  Decentralization

Minus Theory proposes moving the Virtual Machine (VM) from the blockchain node to an external indexer. This shift does not compromise the decentralization of the network because it leaves the consensus process intact and independent.

In traditional blockchain architectures, nodes are responsible for both achieving consensus and executing transactions, which often limits scalability. By relocating the execution workload to the indexer, Minus Theory ensures that nodes remain focused on consensus alone.

Since consensus is the core mechanism that ensures decentralization, this design preserves the distributed and trustless nature of the blockchain. Meanwhile, indexers can be decentralized themselves, further reinforcing the decentralized ethos.

### Higher TPS

The primary bottleneck for blockchain scalability lies in the execution of transactions within the EVM. Minus Theory addresses this limitation by introducing asynchronous execution.

By decoupling transaction execution from the consensus process, the blockchain can confirm and “freeze” a significantly larger volume of transactions without requiring additional computational resources. This design enables the network to handle higher throughput, as consensus is achieved on transaction inputs, while execution is processed separately and asynchronously.

### Cheap gas fee

One of the key benefits of the Minus Theory approach is the significant reduction in gas fees. The cost of consensus in a blockchain is generally fixed: in Proof of Work (PoW), it is determined by electricity costs, while in Proof of Stake (PoS), it is based on the interest earned from staking.

By enabling the blockchain to handle a much higher number of transactions per second (TPS), the fixed cost of consensus can be distributed across a larger pool of transactions. This reduces the per-transaction cost significantly, leading to lower gas fees for users.

### Sharding on transactions by wallet address

Blockchain sharding often encounters challenges when attempting to partition the global state, as maintaining consistency and synchronization across shards can be complex. However, sharding transactions by wallet address provides a simpler and more efficient approach.

In this model, transactions are distributed across different nodes based on wallet addresses. This reduces the burden on individual nodes, as their primary responsibility shifts to maintaining a history of transactions rather than managing the entire global state. The node are light to focus on its DA job. By focusing on transaction history, blockchain nodes become more robust and stable.

### Simplify the blockchain node design

The design of the blockchain node in Minus Theory focuses on achieving consensus for the blockchain input. By narrowing the scope of the node’s responsibilities to this critical function, the overall complexity of the node is significantly reduced.

This simplified design makes the blockchain node more robust, as it only needs to verify and agree on the validity of incoming transactions or blocks. Without the need to handle computationally expensive tasks such as execution or state management, nodes become more efficient and less resource-intensive.

### Less risk when optimizing the execution engine

In traditional blockchain architectures, a significant amount of work and logic related to transaction execution optimization is handled directly within the blockchain node. However, in the Minus Theory framework, this execution logic is offloaded to an external indexer, which decouples the execution process from the core blockchain node.

By moving the execution engine out of the node, the risk associated with optimizing and updating the execution code is substantially reduced. Making changes to the indexer’s code carries less risk than modifying the blockchain node itself, as the node remains focused on consensus and data availability, which are critical for network security and stability.

### More complex applications

One of the key limitations in traditional blockchain designs is the gas limit, which prevents smart contracts from consuming excessive computational resources. This gas limit is set to ensure that blockchain nodes can execute all smart contracts within a block before the next one is generated. However, this constraint limits the complexity and capabilities of decentralized applications (dApps) that can be built on the blockchain.

With the introduction of the indexer in Minus Theory, this limitation can be relaxed. By offloading execution to the indexer, we can gradually reduce the gas limit as the performance of the execution engine improves over time. The indexer is not bound by the same block time constraints as the blockchain node, enabling it to process more complex computations and handle more sophisticated applications.

This shift allows for the development of more resource-intensive decentralized applications, such as advanced decentralized finance (DeFi) protocols, complex gaming systems, and enterprise-level solutions, all without compromising the scalability or security of the blockchain. As the performance of the indexer improves, the range of possible applications grows, pushing the boundaries of what can be achieved in the blockchain space.

## Disadvantages

### Hard fork is required

With the transition of the global state and VM responsibilities to the indexer, blockchain nodes no longer directly track the current state of wallet balances, such as whether a wallet has enough ETH to pay for gas fees. This change introduces new challenges in how transactions and fees are validated across the network.

This shift may require further design considerations, particularly regarding whether it is necessary to maintain an ETH balance at the node level. There are numerous engineering questions that need to be addressed in this new framework, once the community agrees to adopt the Minus Theory approach.

Given these complexities, a hard fork may be required to implement the necessary changes and ensure compatibility with the new structure. This would enable a smooth transition to the new paradigm while maintaining network stability and ensuring that the system functions as expected.

### Global State Explosion problem still exists

The issue of Global State Explosion has been a persistent challenge for Ethereum and other blockchain networks. This occurs when the global state grows too large, making it more difficult for people to afford the hardware necessary to run a node. Minus Theory does not attempt to solve this problem directly.

However, in Zentra, we implement a mechanism to mitigate the abuse of global state. By using tokens, we provide a way to limit excessive interactions with the global state.

## Summary

We propose a method to enhance L1 using Minus Theory and discuss its advantages and disadvantages.

After many years of focusing on L2 scaling, the era of L1 is making a comeback.

## Replies

**zhous** (2025-01-21):

Who runs this indexer/indexers? And how to finacially support the indexer/indexers?

---

**kernel1983** (2025-01-21):

That is a great question.

In existing blockchain systems, the term typically refers to the blockchain node. The proposed “minus” blockchain system, however, includes both the node and the indexer. This proposed system is split into two components that work asynchronously: the node focuses on message/transaction consensus, while the indexer calculates the state without the time constraints.

Currently, there is no direct incentive for blockchain nodes in both the Ethereum and Bitcoin systems. If this situation remains unchanged, there would also be no incentive for indexer operators. (We don’t favor this design; we believe blockchain nodes should be profitable to cover their costs. Suggestions are welcome!)

One key difference with this proposal is that if users trust the blockchain node to fairly and decentralized produce new blocks, they might choose to run only the indexer themselves. This allows them to independently verify whether the global state (roots) matches the roots calculated by public indexers.

If the EVM is moved from the node to the indexer, the indexer may become expensive to operate due to the Global State Explosion issue. However, in Zentra, we use tokens to control the total size of the global state. This is somewhat similar to Bitcoin limiting its block size to 1MB, which ensures the blockchain node size grows linearly. Zentra applies this principle by capping the global state at a fixed size, making it feasible for regular users with limited hardware resources to run an indexer.

This proposal serves as a general direction for building a high-performance Layer 1 blockchain. Many details still need to be finalized before implementation. Nevertheless, we decided to build Zentra first, allowing us to gain hands-on experience and insights from action rather than discussion.

---

**lanyinzly** (2025-01-23):

What is the difference between based rollup and your Minus Theory? It sounds similar to the function of rollups.

---

**kernel1983** (2025-01-23):

Minus Theory shares the idea of using blockchain as the sequencer with Based Rollup. I was very exciting when first hearing Based Rollup.

Let me borrow the picture from https://x.com/2077Research/status/1879976056750502327

[![image](https://ethresear.ch/uploads/default/original/3X/d/c/dc32895a6e8b3f710faabbef732ed2a3f43f4606.jpeg)image679×253 60.3 KB](https://ethresear.ch/uploads/default/dc32895a6e8b3f710faabbef732ed2a3f43f4606)

The main difference between Based Rollup and Minus Theory is about if the node/gateway **pre-confirm the transactions**. Minus Theory suggest not to do any validation before including those transactions in a block. Once validation existing, huge EVM burden must be used for transactions, it would be impossible to achieve TPS more than 10k or even 1k like today’s situation.

This is **the key to significantly increase the performance and throughput** of a blockchain system. Because in Minus Theory the EVM execution can be delay and outside of the blockchain node. Another computer or cluster can be used to speed up, and the parallel VM technology can be used as well. Overall, people can always do the improvement to reduce the execution time with more resources under Minus Theory.

