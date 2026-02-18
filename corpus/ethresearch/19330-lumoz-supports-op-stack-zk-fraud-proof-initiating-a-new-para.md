---
source: ethresearch
topic_id: 19330
title: Lumoz supports Op Stack + ZK Fraud Proof, Initiating a New Paradigm in L2 Architecture
author: nanfengpo
date: "2024-04-18"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/lumoz-supports-op-stack-zk-fraud-proof-initiating-a-new-paradigm-in-l2-architecture/19330
views: 1206
likes: 5
posts_count: 1
---

# Lumoz supports Op Stack + ZK Fraud Proof, Initiating a New Paradigm in L2 Architecture

After completing a total of tens of millions of dollars in financing, the modular computing layer Lumoz continues to make strides in the Layer 2 (L2) space. This week, Lumoz announced that its Modular Compute Layer will support the Op Stack + ZK Fraud Proof Layer 2 architecture, initiating a new paradigm in L2 architecture.

**The Modular Compute Layer will Support Op Stack + ZK Fraud Proof**

[![](https://ethresear.ch/uploads/default/optimized/3X/b/0/b0b5f7ce38af9467e9977533e24818eda89ca787_2_690x293.jpeg)2592×1104 89.6 KB](https://ethresear.ch/uploads/default/b0b5f7ce38af9467e9977533e24818eda89ca787)

The Op Stack + ZK Fraud Proof architecture is a new design that integrates zero-knowledge proof-based validity proofs into the Optimistic Rollup technology. When challengers point out that the sequencer has submitted incorrect data, they submit a challenge to L1. The Sequencer must generate the corresponding ZK Proof within a limited challenge period and submit it to the Layer 1 contract for verification. If the verification results show that the data is valid, the challenge is invalid; otherwise, the challenge is successful.

This illustration demonstrates the specific process of handling fraud proofs within Layer 2 technology under the Op Stack and ZK Fraud Proof architecture. In this architecture, the Op Stack module undertakes the core functions of Layer 2, including handling the basic functions of the Layer 2 blockchain and the responsibility of submitting Batches to Layer 1. Meanwhile, the ZK Fraud Proof module focuses on handling the challenges of fraud proof.

The process details are as follows:

1. Challenge Initiation: Validators initiate the challenge for fraud proof.
2. Information Synchronization: Lumoz Verify Nodes synchronize challenge information to prepare for the next step of verification.
3. Obtaining Zero-Knowledge Proof Inputs: Verification nodes obtain the required zero-knowledge proof input data from the Op Stack module, which includes block trace, batch info, etc.
4. Generating Zero-Knowledge Proof: Lumoz will then request the modular compute layer to generate the required zero-knowledge proof.
5. Proof Submission: Once the zero-knowledge proof is generated, Lumoz Verify Nodes submit the proof to Layer 1 for verification.

Through the aforementioned process, the challenge and verification process of ZK Fraud Proof is completed.

It is well known that Optimistic Rollup has lower costs but longer withdrawal waiting times; whereas ZK Rollup allows for almost immediate withdrawals, but at a higher cost. This solution combines the advantages and disadvantages of both Optimistic Rollup and ZK Rollup, not only maintaining the characteristics of low cost but also effectively reducing the waiting time.

[![](https://ethresear.ch/uploads/default/optimized/3X/6/e/6e3ba0242b7c25f4ab218f3dbdb445df38df2a96_2_616x500.jpeg)1930×1566 103 KB](https://ethresear.ch/uploads/default/6e3ba0242b7c25f4ab218f3dbdb445df38df2a96)

**Modular Compute Layer**

Lumoz provides a modular computation layer that offers stable and reliable computing power support for blockchains utilizing the Op Stack + ZK Fraud Proof architecture. When Layer 2 submits Batch data, if there are challengers initiating challenges, then the modular computation layer will rely on its computing services to generate the corresponding proof data (Proof). This process requires the computing services of the modular computation layer to submit the correct Proof within a specified time frame. If this is achieved, it is considered that the challenger has failed the challenge; otherwise, the challenger is deemed to have succeeded in the challenge.

The role of Lumoz’s modular computation layer in the Op Stack + ZK Fraud Proof architecture:

[![](https://ethresear.ch/uploads/default/optimized/3X/3/7/37e5580daf5e81c98795809ea463ab41c25f1787_2_419x500.jpeg)2246×2680 172 KB](https://ethresear.ch/uploads/default/37e5580daf5e81c98795809ea463ab41c25f1787)

In conclusion, the Lumoz ZK Prover Network, through decentralized miner participation in ZKP computations, extensive circuit support, and a comprehensive proof verification process, provides a high-performance modular computation layer for the Optimistic+ZK Fraud Proof architecture. Combined with Lumoz’s trustless native cross-Rollup communication technology, it not only securely shares liquidity among all Rollups but also offers robust multi-Rollup interoperability, opening new possibilities for decentralized applications and DeFi protocols.

**Conclusion**

Lumoz’s Modular Compute Layer, supported by Optimistic Rollup and ZK Fraud Proof, has pioneered a new Layer 2 architecture model. This solution fills the gap in the current market for a mixed solution of ZK and OP, achieving effective technical integration. By combining the advantages of Optimistic Rollup and ZK Rollup, we can significantly reduce costs and shorten verification wait times. As pioneers in this field, Lumoz will continue to leverage its strengths and constantly optimize its technology solutions. At the same time, we also hope more people will pay attention to and contribute to the development of this hybrid architecture of Optimistic Rollup and ZK Fraud Proof, contributing to the industry’s development!
