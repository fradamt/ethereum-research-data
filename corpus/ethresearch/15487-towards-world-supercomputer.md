---
source: ethresearch
topic_id: 15487
title: Towards World Supercomputer
author: fewwwww
date: "2023-05-04"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/towards-world-supercomputer/15487
views: 5302
likes: 20
posts_count: 9
---

# Towards World Supercomputer

> Idea originally from Xiaohang Yu

## TL;DR

- Ethereum’s vision has always been building a World Computer.
- World Supercomputer supports Ethereum’s vision for a World Computer and in addition high-performance computation like machine learning. Thus, we face the trilemma of consensus ledger, computing power, and storage capacity.
- We solve the World Supercomputer trilemma by linking three topologically heterogeneous P2P networks with zero-knowledge proof.

Consensus: Ethereum will act as the consensus ledger for the World Supercomputer, providing the underlying consensus and using the block interval as the clock cycle for the entire system.
- Storage: Storage rollup will act as a storage network for the World Supercomputer, storing large amounts of data and providing a URI standard to access the data.
- Computation: zkOracle network will serve as the computation network for the World Supercomputer, running resource-intensive computations and generating verifiable proofs of computations.
- Data Bus: Zero-knowledge proof technology will act as the data bus for the World Supercomputer, connecting various components and allowing data and consensus to be linked and verified.

## 0. World Computer Concept

[![Ethereum: the World Computer](https://ethresear.ch/uploads/default/optimized/2X/d/d5d802e400ac610f0cba5e8f4e688123c67e9ef2_2_690x204.jpeg)Ethereum: the World Computer1788×530 114 KB](https://ethresear.ch/uploads/default/d5d802e400ac610f0cba5e8f4e688123c67e9ef2)

Ethereum was founded on the goal of building a world computer. This vision has [remained unchanged](https://web.archive.org/web/20230000000000*/https://www.youtube.com/@EthereumProtocol) for the past seven years.

[![Blockchain Trilemma](https://ethresear.ch/uploads/default/original/2X/7/74d5678fa02020e628922e25a256e872a0fd59c1.png)Blockchain Trilemma464×358 9.72 KB](https://ethresear.ch/uploads/default/74d5678fa02020e628922e25a256e872a0fd59c1)

According to [Vitalik’s definition of the classic blockchain trilemma](https://vitalik.ca/general/2021/04/07/sharding.html), Ethereum prioritizes decentralization and security over scalability (i.e. performance).

In reality, we need a P2P network as a world computer that solves truly general-purpose intensive computing (especially machine learning and oracle) while preserving the full decentralization of the base layer blockchain.

## 1. World Computer Difficulty

### a) World Computer Trilemma

To create a world computer, we encounter a trilemma based on the basic blockchain network trilemma.

[![World Computer Trilemma](https://ethresear.ch/uploads/default/optimized/2X/4/4575b957b5630e67b05ba7017d3875525756a761_2_690x387.jpeg)World Computer Trilemma2704×1520 163 KB](https://ethresear.ch/uploads/default/4575b957b5630e67b05ba7017d3875525756a761)

Different priorities result in different trade-offs:

- Strong Consensus Ledger: Inherently requires repetitive storage and computation and therefore is not suitable for scaling storage and computation.
- Strong Computation Power: Needs to reuse consensus while performing a lot of computation and proof tasks and therefore is not suitable for large-scale storage.
- Strong Storage Capacity: Needs to reuse consensus while performing frequent random sampling proofs of storage and therefore is not suitable for computation.

### b) Computation Demand for World Computer

To meet the demand and purpose of a world computer, we expand on the concept of a world computer as described by Ethereum and aim for a World Supercomputer.

World Supercomputer first and foremost needs to do what computing can do today and in addition in a decentralized manner. In preparation for large-scale adoption, developers, for instance, require the World Supercomputer to accelerate the development and adoption of decentralized machine learning for running model inference and verification.

Large models, like [MorphAI](https://www.morphstudio.xyz/), will be able to use Ethereum to distribute inference tasks and verify the output from any third party node.

In the case of a computationally resource-intensive task like machine learning, achieving such an ambition requires not only trust-minimized computation techniques like zero-knowledge proofs but also larger data capacity on decentralized networks. These are things that cannot be accomplished on a single P2P network, like classical blockchain.

### c) Solution for Performance Bottleneck

In the early development of computers, our pioneers have faced similar performance bottleneck in computer as they made trade-offs between computational power and storage capacity. Consider the smallest component of a circuit as an illustration.

We can compare the amount of computation to lightbulbs/transistors and the amount of storage to capacitors. In an electrical circuit, a lightbulb requires current to emit light, similar to how computational tasks require computational volume to be executed. Capacitors, on the other hand, store electrical charge, similar to how storage can store data.

There may be a trade-off in the distribution of energy between the lightbulb and the capacitor for the same voltage and current. Typically, higher computational volumes require more current to perform computational tasks, and therefore require less energy storage from the capacitor. A larger capacitor can store more energy, but may result in lower computational performance at higher computational volumes. This trade-off leads to a situation where computation and storage cannot be combined in some cases.

[![trade-off](https://ethresear.ch/uploads/default/optimized/2X/5/55d104423bfb3081c4279d69fd0c03c8f71c8e7e_2_690x387.png)trade-off2704×1520 108 KB](https://ethresear.ch/uploads/default/55d104423bfb3081c4279d69fd0c03c8f71c8e7e)

In the von Neumann computer architecture, it guided the concept of separating the storage device from the central processor. Similar to decoupling the lightbulbs from the capacitors, this can solve the performance bottleneck of the system of our World Supercomputer.

[![von Neumann](https://ethresear.ch/uploads/default/optimized/2X/9/9dd3acb903b80454acbdea7136f67b8d2ccaf006_2_690x387.png)von Neumann2704×1520 118 KB](https://ethresear.ch/uploads/default/9dd3acb903b80454acbdea7136f67b8d2ccaf006)

In addition, traditional high-performance distributed database uses a design that separates storage and computation. This scheme is adopted because it is fully compatible with the characteristics of a World Supercomputer.

## 2. World Supercomputer Components

The final World Supercomputer will be made up of three topologically heterogeneous P2P networks: a consensus ledger, computation network, and storage network connected by a trust-minimized bus (connector) such as zero-knowledge proof technology. This basic setup allows the World Supercomputer to solve the world computer trilemma, and additional components can be added as needed for specific applications.

It’s worth noting that topological heterogeneity goes beyond just differences in architecture and structure. It also encompasses fundamental differences in topological form. For example, while Ethereum and Cosmos are heterogeneous in terms of their layers of network and internet of networks, they are still equivalent in terms of topological heterogeneity (blockchains).

[![topological heterogeneity](https://ethresear.ch/uploads/default/optimized/2X/2/209f0d3833c045044cdfcf6fa8beb505ecbed483_2_690x387.jpeg)topological heterogeneity2704×1520 192 KB](https://ethresear.ch/uploads/default/209f0d3833c045044cdfcf6fa8beb505ecbed483)

Within the World Supercomputer, a consensus ledger blockchain takes the form of a chain of blocks with nodes in the form of complete graph, while a network like Hyper Oracle network is a ledgerless network with nodes in the form of cyclic graph, and the network structure of storage rollup is yet another variation with partitions forming sub-networks.

We can have a fully decentralized, unstoppable, permissionless, and scalable World Supercomputer by linking three topologically heterogeneous peer-to-peer networks for consensus, computation, and storage via zero-knowledge proof as data bus.

## 3. World Supercomputer Architecture

Similar to building a physical computer, we must assemble the consensus network, computation network, and storage network mentioned previously into a World Supercomputer.

Selecting and connecting each component appropriately will help us achieve a balance between the Consensus Ledger, Computing Power, and Storage Capacity trilemma, ultimately ensuring the decentralized, high-performance, and secure nature of the World Supercomputer.

The architecture of the World Supercomputer, described by its functions, is as follows:

[![architecture](https://ethresear.ch/uploads/default/optimized/2X/4/4d1a49b51ed5643f9faa5571cf8429bd99b6da01_2_690x388.png)architecture2704×1522 263 KB](https://ethresear.ch/uploads/default/4d1a49b51ed5643f9faa5571cf8429bd99b6da01)

The nodes of a World Supercomputer network with consensus, computation, and storage networks would have a structure similar to the following:

[![nodes](https://ethresear.ch/uploads/default/optimized/2X/6/6049041d7cca54ea140682273ef967d81b742767_2_690x388.jpeg)nodes2704×1522 171 KB](https://ethresear.ch/uploads/default/6049041d7cca54ea140682273ef967d81b742767)

To start the network, World Supercomputer’s nodes will be based on Ethereum’s decentralized foundation. Nodes with high computational performance can join zkOracle’s computation network for proof generation for general computation or machine learning, while nodes with high storage capacity can join EthStorage’s storage network.

The above example depicts nodes that run both Ethereum and computation/storage networks. For nodes that only run computation/storage networks, they can access the latest block of Ethereum or prove data redundancy/availability of storage through zero-knowledge proof-based buses like zkPoS and zkNoSQL, all without the need for trust.

### a) Ethereum for Consensus

Currently, World Supercomputer’s consensus network exclusively uses Ethereum. Ethereum boasts a robust social consensus and network-level security that ensure decentralized consensus.

[![consensus network](https://ethresear.ch/uploads/default/optimized/2X/9/9336eaf8f773bd6f55cd35537af3ac49d6f3324a_2_690x388.png)consensus network2704×1522 172 KB](https://ethresear.ch/uploads/default/9336eaf8f773bd6f55cd35537af3ac49d6f3324a)

World Supercomputer is built on a consensus ledger-centered architecture. The consensus ledger has two main roles:

- Provide consensus for the entire system
- Define the CPU Clock Cycle with Block Interval

In comparison to a computation network or a storage network, Ethereum cannot handle huge amounts of computation simultaneously nor store large amounts of general-purpose data.

In World Supercomputer, Ethereum is a consensus network that reaches consensus for computation and storage networks and loads critical data so that the computation network can perform further off-chain computations.

### b) Storage Rollup for Storage

Ethereum’s Proto-danksharding and Danksharding are essentially ways to expand the consensus network offering temporal availability for large amount data. To achieve the required storage capacity for the World Supercomputer, we need a solution that is both native to Ethereum and supports a large amount of data storage persisted forever.

[![storage network](https://ethresear.ch/uploads/default/optimized/2X/a/a5887da8c0a1cc7af8fae36c39aaa42e6581fb2a_2_690x388.png)storage network2704×1522 155 KB](https://ethresear.ch/uploads/default/a5887da8c0a1cc7af8fae36c39aaa42e6581fb2a)

Storage Rollup, such as EthStorage, is essentially scaling Ethereum for large-scale storage.

Furthermore, as computationally resource-intensive applications like machine learning require a large amount of memory and storage to run on a physical computer, it’s important to note that Ethereum cannot be aggressively scaled in both aspects. Storage Rollup is necessary for the “swapping” that allows the World Supercomputer to run compute-intensive tasks.

Additionally, EthStorage provides a web3:// access protocol ([ERC-4804](https://eips.ethereum.org/EIPS/eip-4804)), similar to the native URI of a World Supercomputer or the addressing of resources of storage.

### c)  Network for Computation

The computation network is vital in a World Supercomputer as it determines the overall performance. It must be able to handle complex calculations such as oracle or machine learning, and it should be faster than both consensus network and storage network in accessing and processing data.

[![computation network](https://ethresear.ch/uploads/default/optimized/2X/5/59bcd3834eefa9313cb3c0018dd60caf9e4f2a87_2_690x388.png)computation network2704×1522 175 KB](https://ethresear.ch/uploads/default/59bcd3834eefa9313cb3c0018dd60caf9e4f2a87)

zkOracle Network is a decentralized and trust-minimized computation network that is capable of handling arbitrary computations. Any running program generates a ZK proof, which can be easily verified by consensus (Ethereum) or other components when in use.

Hyper Oracle, a zkOracle Network, is a network of ZK nodes, powered by zkWASM and EZKL, which can run any computation with the proof of execution traces.

A zkOracle Network is a ledgerless blockchain (no global state) that follows the chain structure of the original blockchain (Ethereum), but operates as a computational network without a ledger. The zkOracle Network does not guarantee computational validity through re-execution like traditional blockchains; rather it gives computational verifiability through proofs generated. The ledger-less design and dedicated node setup for computing allow zkOracle Networks, like Hyper Oracle, to focus on high-performance and trust-minimized computing. Instead of generating new consensus, the result of the computation is output directly to the consensus network.

In a computation network of zkOracle, each compute unit or executable is represented by a zkGraph. These zkGraphs define the computation and proof generation behavior of the computation network, just like how smart contracts define the computation of the consensus network.

**I. General Off-chain Computation**

The zkGraph programs in zkOracle’s computation can be used for two major cases without external stacks:

- indexing (accessing blockchain data)
- automation (automate smart contract calls)
- any other off-chain computation

These two scenarios can fulfill the middleware and infrastructure requirements of any smart contract developer. This implies that as a developer of a World Supercomputer, you can create a completely decentralized application through an end-to-end decentralized development process, which includes on-chain smart contracts on the consensus network as well as off-chain computation on the computation network.

**II. ML/AI Computation**

In order to achieve Internet-level adoption and support any application scenario, World Supercomputer needs to support machine learning computing in a decentralized way.

Also through zero-knowledge proof technology, machine learning and artificial intelligence can be integrated into World Supercomputer and be verified on Ethereum’s consensus network to be truly on-chain.

zkGraph can connect to external technology stacks in this scenario, thus combining zkML itself with World Supercomputer’s computation network. This enables [all types of zkML applications](https://www.canva.com/design/DAFgqqAboU0/4HscC5E3YkFRFk3bB64chw/view#6):

- User-privacy-preserving ML/AI
- Model-privacy-preserving ML/AI
- ML/AI with Computational Validity

To enable the machine learning and AI computational capabilities of World Supercomputer, zkGraph will be combined with the following cutting-edge zkML technology stacks, providing them with direct integration with consensus networks and storage networks.

- EZKL: doing inference for deep learning models and other computational graphs in a zk-snark.
- Remainder: speedy machine learning operations in Halo2 Prover.
- circomlib-ml: circom circuits library for machine learning.

### e) ZK as Data Bus

Now that we have all the essential components of the World Supercomputer, we require a final piece that connects them all. We need a verifiable and trust-minimized bus to enable communication and coordination between components.

[![data bus](https://ethresear.ch/uploads/default/optimized/2X/7/7351541cbab7dcec7adf713a90c3227c8cd116b7_2_690x388.png)data bus2704×1522 159 KB](https://ethresear.ch/uploads/default/7351541cbab7dcec7adf713a90c3227c8cd116b7)

For a World Supercomputer that uses Ethereum as its consensus network, Hyper Oracle zkPoS is a fitting candidate for zk Bus. zkPoS is a critical component of zkOracle; it verifies consensus of Ethereum via ZK, allowing Ethereum’s consensus to spread and be verified in any environment.

As a decentralized and trust-minimized bus, zkPoS can connect to all components of World Supercomputer with very little verification computation overhead with the presence of ZK. As long as there is a bus like zkPoS, data can flow freely within World Supercomputer.

When Ethereum’s consensus can be passed from the consensus layer to the Bus as World Supercomputer’s initial consensus data, zkPoS with state/event/tx proofs can prove it. The resulting data can then be passed to the computation network of zkOracle Network.

As a decentralized and trust-minimized bus, zkPoS can connect all components of World Supercomputer with minimal verification computation of ZK. With a bus like zkPoS, data can flow freely within World Supercomputer.

In addition, for storage network’s bus, EthStorage is developing zkNoSQL to enable proofs of data availability, allowing other networks to quickly verify that BLOBs have sufficient replicas.

### f) Workflow

[![workflow](https://ethresear.ch/uploads/default/optimized/2X/f/fb5140a29b0e636b278a42f7edcfbc80fb1ee2b9_2_690x388.jpeg)workflow2704×1522 91 KB](https://ethresear.ch/uploads/default/fb5140a29b0e636b278a42f7edcfbc80fb1ee2b9)

Here’s an overview of the transaction process in Ethereum-based World Supercomputer, broken down into steps:

- Consensus: Transactions are processed and agreed upon using Ethereum.
- Computation: The zkOracle Network performs relevant off-chain calculations (defined by zkGraph loaded from EthStorage) by quickly verifying the proofs and consensus data passed by zkPoS acting as a bus.
- Consensus: In certain cases, such as automation and machine learning, the computation network will pass data and transactions back to Ethereum or EthStorage with proofs.
- Storage: For storing large amounts of data (e.g. NFT metadata) from Ethereum, zkPoS can act as an optional trust-minimized messenger between Ethereum and EthStorage.

Throughout this process, the bus plays a vital role in connecting each step:

- When consensus data is passed from Ethereum to zkOracle Network’s computation or EthStorage’s storage, zkPoS and state/event/tx proof generate proofs that the recipient can quickly verify to get the exact data such as the corresponding transactions.
- When zkOracle Network needs to load data for computation from storage, it accesses the addresses of data on storage from consensus network with zkPoS, then fetches actual data from storage with zkNoSQL.
- When data from zkOracle Network or Ethereum needs to be displayed in the final output forms, zkPoS generates proofs for the client (e.g., a browser) to quickly verify.

## 5. Conclusion

Bitcoin has established a solid foundation for the creation of a [World Computer v0](https://coingeek.com/bitcoin-as-a-world-computer/), successfully building a “World Ledger”.

Ethereum has subsequently demonstrated the “World Computer” paradigm by introducing a more programmable smart contract mechanism.

The World Supercomputer is designed to extend and advance the existing decentralized network. We envision it unlocking the potential of Ethereum and enabling exploration of new scenarios.

## Replies

**fewwwww** (2023-05-10):

During Financial Cryptography, we talked to a lot of people irl, and it was common for people to have some initial questions about the difference between World Supercomputer and L2 Rollup (or Modular Blockchain).

The main difference between modular blockchain (including L2 Rollup) and world computer architecture lies in their purpose:

- Modular Blockchain: Designed for creating a new blockchain by selecting modules (consensus, DA, settlement, and execution) to put together into a modular blockchain.
- World Computer: Designed to establish a global decentralized computer/network by combining networks (base layer blockchain, storage network, computation network) into a world computer.

---

**ToddZ0952611** (2023-05-12):

Awesome writing, completely agree!

What are the current bottlenecks in implementing this solution? e.g. the performance of zk algorithms

---

**jethrokwy** (2023-05-12):

solid piece ser! had a couple of questions for you!

1. How does the zkGraph define the computation and proof generation behavior of the computation network?
2. How does the zkOracle Network handle indexing and automation scenarios without external stacks?
3. How can developers create a completely decentralized application through an end-to-end decentralized development process using the zkOracle Network and the consensus network?

---

**fewwwww** (2023-05-12):

For now, the performance of the data bus of the whole system may become a bottleneck. Since we need to [use zk to prove the whole Ethereum consensus](https://mirror.xyz/hyperoracleblog.eth/lAE9erAz5eIlQZ346PG6tfh7Q6xy59bmA_kFNr-l6dE), we need to do additional optimization of hardware acceleration and proof system to reduce the proof time to something like 12 seconds or less, to make the data bus work seamlessly.

---

**fewwwww** (2023-05-12):

For the first two questions, you can read [Hyper Oracle’s white paper](https://mirror.xyz/hyperoracleblog.eth/qbefsToFgFxBZBocwlkX-HXbpeUzZiv2UB5CmxcaFTM), which describes zkGraph in more detail; you can also check out [our ethresearch post on the definition of zkOracle](https://ethresear.ch/t/defining-zkoracle-for-ethereum/15131).

For the third question,

![](https://ethresear.ch/user_avatar/ethresear.ch/jethrokwy/48/12048_2.png) jethrokwy:

> How can developers create a completely decentralized application through an end-to-end decentralized development process using the zkOracle Network and the consensus network?

Our idea is that the original DApp actually needs a smart contract + middleware (complex off-chain computation such as oracle/indexing/automation/machine learning…) + front-end page architecture. In World Supercomputer, developers can build the application in a more “one-stop way”, and the above three components can be implemented in consensus network + computation network + storage network. And those three are connected by zk data bus in a trust-minimized way.

---

**xhyumiracle** (2023-05-13):

Adding more thoughts:

Essentially, the value of zk/snarks on the scalability side actually comes from breaking the tradeoff between data consistency (security) and resource utilization efficiency (scalability), i.e. satisfying both sides at the same time, while maintaining decentralization. Yes, a solution to a well known classic issue - the “impossible triangle”.

Let’s walk through the underlying theory again: (under decentralization assumption)

1. strong consensus ensures data consistency, as a cost it requires high replication of work, which requires high consumption of resource (which is the reason for high gas cost)
2. to improve scalability and reduce cost, the ultimate way is to reduce the replication degree, but it can make consensus vulnerable and harm the data consistency.
3. but with snark proof, the verification secures the data correctness in diverse work and the succinctness ensures low replication work. Therefore, it satisfies both high data consistency and high scalability at the same time.

zk rollup solutions made a valuable attempt, it satisfied both the scalability and data consistency, but it still requires consensus to maintains the consistency among sequencers in the future, therefore replication work is still inevitable, which requires high cost and may reduce scalability again. Otherwise, it has to sacrifices decentralization and keep the number of nodes small to stay low cost. In other word, the low gas cost of zk rollups mainly comes from sacrificing a certain degree of decentralization, the value of zk/snark is not fully realized. Rollups are still trapped by the “impossible triangle” (for op rollup it sacrifices certain level of security, but we won’t dive into the details)

So is the World Supercomputer a different thing?

Yes, it can fully release the value of zk/snark. Why?

One of the key points of World Supercomputer architecture is keeping the sequencer only in the consensus network (CSN), other than in functional networks, e.g. computation network (CPN) and storage network (STN) does not maintain their own sequencer. Therefore, CPN/STN can achieve scalability by focusing only on low replicated work, so that even when the number of nodes grows, the cost won’t increase.

Because we are not trying to reduce the workload of sequencer, which belongs to CSN, we are trying to reduce the workload of tasks that should be scalable.

In short, CSN == decentralization + data consistency, CPN/STN == decentralization + scalability, and use snarks to connect the data without losing any ‘angle’, to achieve WSC == decentralization + data consistency + scalability.

If we took a deeper look at the “impossible triangle”, decentralization actually is the strictest requirement, it requires ZERO centralization in any component of the whole architecture. Sacrificing decentralization to reduce cost is definitely a user-friendly solution, but it doesn’t help to solve “impossible triangle”. So the true challenge for Ethereum and even the web3 is how to bridge the scalability and data consistency UNDER the assumption of decentralization, the red line of web3.

Previously we thought this dilemma cannot be broke, but thanks to zk protocols for enabling it, the World Supercomputer architecture has become a promising theory to solve “impossible triangle”.

There is still a lot of work on both research and engineering sides, if you share the same ambition, let’s build the wsc together, the wsc needs your idea, comments and contributions. Thanks.

---

**fewwwww** (2023-05-21):

[Vitalik expresses](https://vitalik.ca/general/2023/05/21/dont_overload.html) that some of the ultimate oracle, restaking, and L1-driven recovery of L2 projects should be discouraged and resisted, because they may stretching and overloading Ethereum consensus. A related example on Ultimate Oracle: [Enshrined Eth2 price feeds](https://ethresear.ch/t/enshrined-eth2-price-feeds/7391/), 3 years ago, Justin Drake proposed to embed price feeds oracle in Eth2, which Vitalik opposed.

This is why the goal and approach of World Supercomputer has always been to integrate Ethereum as a consensus network with other computing and storage network components without affecting the original design of Ethereum consensus.

---

**flyq** (2023-05-23):

Vitalik was rejected when he expected to improve BTC, and now it is his turn ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12).

Such a grand vision may not be able to be completed by tinkering with the existing system, and it needs to start all over again·

