---
source: ethresearch
topic_id: 20268
title: "A Node-Based Solution to Execution Sharding: The KRNL Protocol"
author: tahir-krnl
date: "2024-08-14"
category: Sharded Execution
tags: []
url: https://ethresear.ch/t/a-node-based-solution-to-execution-sharding-the-krnl-protocol/20268
views: 1368
likes: 2
posts_count: 1
---

# A Node-Based Solution to Execution Sharding: The KRNL Protocol

By [Asim Ahmad](https://x.com/asim_eth) and [Tahir Mahmood](https://x.com/Tahir_Mahmood) on behalf of [KRNL](https://krnl.xyz).

**1. Abstract**

The evolution of the Web3 ecosystem confronts pivotal challenges such as network fragmentation, scalability constraints, cross-chain integration complexities, and security vulnerabilities. To address these issues, we introduce the KRNL Protocol—an orchestration and verification engine that seamlessly integrates permissionless and composable functions across multiple blockchain networks within the Ethereum transaction lifecycle. By transforming both on-chain and off-chain functions into execution shards called “kernels,” KRNL offers a distributed runtime environment that optimizes resource utilization, enhances modularity, and accelerates deployment. This approach not only improves the responsiveness of decentralized applications (dApps) but also reduces their time-to-market. Our proposal positions KRNL as part of the fabric of the Web3 framework.

**2. Motivation**

The Web3 ecosystem faces several significant challenges, including fragmentation, scalability limitations, cross-chain friction, and security concerns.

**Fragmentation**: The emergence of numerous Layer 1 and Layer 2 solutions has led to the creation of isolated silos. This fragmentation impedes seamless interaction between applications and smart contracts across different environments, undermining the foundational principle of composability in decentralized systems.

**Scalability Constraints**: Ethereum grapples with network congestion and high gas fees. These scalability issues deter the widespread adoption of dApps and erode user experience.

**Cross-Chain Friction**: Facilitating interoperability between Ethereum and other blockchains often demands intricate integrations. The absence of standardized cross-chain communication protocols exacerbates development complexities, stifling innovation and efficiency.

**Security Vulnerabilities**: Ensuring transaction integrity, provenance, and security in a decentralized manner remains a challenge. The proliferation of bridges and interoperability solutions introduces novel attack vectors, heightening security risks.

To address these challenges, we reimagine the execution paradigm by introducing the concept of kernels - community-built, permissionless, monetizable, and composable execution shards across Web3. We also introduce the KRNL protocol, an orchestration and verification engine that enables smart contracts to integrate execution shards, enriching the logic and state of traditional smart contract operations without the creation of custom infrastructure. With this proposal, we aim to become an essential tool for the development of cross-chain applications.

**3. TL;DR**

Execution Sharding refers to the approach of dividing and distributing the execution of smart contracts across multiple blockchain networks, or “shards”, to enhance scalability and efficiency in blockchain systems. Instead of executing every transaction on a single chain, execution sharding allows transactions and smart contract states to be distributed across multiple chains, each handling a portion of the overall workload.

Execution sharding is critical for Ethereum’s scalability. The KRNL Protocol integrates permissionless and composable kernels (execution shards) across multiple networks, seamlessly into the native Ethereum transaction lifecycle.

KRNL manages resources to provide a secure and optimal execution environment for smart contracts. This enables a distributed runtime environment that determines transaction outcome based on selected kernels, operating across different environments. KRNL’s open framework enhances modularity, optimizes resources, ensures stable operations, and accelerates deployment, ultimately improving responsiveness and reducing time to market for applications.

**4. Introducing Kernels**

Within the KRNL Protocol framework, kernels represent execution shards. These kernels transform both on-chain and off-chain functions into modular units characterized by the following attributes:

- Statelessness: Kernels maintain no intrinsic state, ensuring flexibility and facilitating seamless migration across environments.
- Lightweight Design: To minimize computational overhead, kernels promote efficient execution.
- Resilience: Engineered to withstand operational failures, ensuring reliable performance.
- Independent Deployability: Allowing for deployment across various environments.

The defining features of kernels include:

- Infrastructure Agnosticism: Kernels are not tethered to specific infrastructures; they possess the agility to migrate across environments as necessitated.
- Enhanced Modularity and Composability: By deconstructing applications into discrete kernels, modularity is enhanced, enabling permissionless sharing across multiple applications.
- Accelerated Deployment: Simplifying the deployment process improves responsiveness and reduces time-to-market for applications.

**5. Vision**

**The Pre-Cloud Paradigm**

Before cloud computing, developers bore the burden of constructing, operating, and maintaining all requisite programs and services. This paradigm engendered prohibitive costs, scalability constraints, accessibility challenges, and resource limitations. Cloud computing revolutionized this landscape, introducing managed services where back-end infrastructures are handled by cloud providers.

[![Before and After Cloud Computing](https://ethresear.ch/uploads/default/optimized/3X/5/f/5fe5cbe3446592ada1eea874797faf006e20d182_2_690x315.png)Before and After Cloud Computing3408×1560 227 KB](https://ethresear.ch/uploads/default/5fe5cbe3446592ada1eea874797faf006e20d182)

**KRNL’s Transformative Potential**

KRNL seeks to catalyze a comparable paradigm shift within the Web3 domain—a permissionless Web3 cloud environment built by the community through contributions of monetizable kernels. This vision aligns with the Function as a Service (FaaS) model, reimagined to suit the decentralized and heterogeneous fabric of blockchain ecosystems.

[![Before and After KRNL](https://ethresear.ch/uploads/default/optimized/3X/0/3/03a9e2f49a0d71e30f39b7ce9368173d25a7b5a6_2_690x301.jpeg)Before and After KRNL1920×838 73.1 KB](https://ethresear.ch/uploads/default/03a9e2f49a0d71e30f39b7ce9368173d25a7b5a6)

**Functions as a Service (FaaS) in the Web3 Context**

FaaS is a category of cloud computing services that provide a platform enabling customers to develop, run and manage applications without the complexity of building and maintaining the infrastructure associated with developing and launching an app. Examples of a traditional FaaS include AWS Lambda, Google Cloud Functions, Microsoft Azure Functions, etc.

The conventional FaaS model does not fit well in distributed and heterogeneous blockchain environments, where each blockchain is a silo and not efficient in the context of the whole Web3 ecosystem. To adapt this concept to Web3, it is essential to ensure decentralized registry, management, and execution of kernels.

**6. Core Concepts**

**The Computing Engine**

KRNL enhances an Ethereum Remote Procedure Call (RPC) node with a verification and orchestration-enabled computing engine. This engine abstracts the intricacies associated with integrating smart contract interdependencies.

The computing engine creates an application and technology agnostic framework that offers a runtime environment to user applications in a distributed manner. It sits between a transaction initiated on any chain and its propagation into a block, determining a transaction’s outcome based on the kernels selected. This approach allows for flexible, efficient scaling and optimization of distributed applications.

**Proof of Provenance (PoP)**

PoP validates that prescribed kernels have run successfully before a transaction is executed, ensuring reliability and security of the KRNL Protocol.

The KRNL Protocol achieves this by utilizing various schemes including a decentralized token authority that issues a signature token, ERC-1271, cryptography and proof systems. The implementation requires the application developer to implement a Software Development Kit (SDK) as well as the token authority. PoP works with existing standards within the Ethereum ecosystem, combining multiple schemes to ensure an anti-fragile system.

**Decentralized Registry**

An Ethereum based registry for activating and monetizing community built kernels. This registry serves as the definitive repository, maintaining critical information about registered kernels, including their pathways, monetization schemes, and other customizable parameters. Core to the design of KRNL is the concept of a two-sided marketplace where kernels are built and monetized, while being utilized by applications across Web3.

**7. Architecture**

[![Architecture Overview of the KRNL Protocol](https://ethresear.ch/uploads/default/optimized/3X/d/2/d2b12fc5edd69ae351e74dda8a31b3f6e57a5311_2_690x388.png)Architecture Overview of the KRNL Protocol1376×774 55.9 KB](https://ethresear.ch/uploads/default/d2b12fc5edd69ae351e74dda8a31b3f6e57a5311)

**Use Case Scenario**

In a hypothetical scenario, a DeFi protocol on Ethereum would like to allow users to trade RWA assets if they are an approved user on Company 1’s RWA platform (and if not, to reject the transaction from this wallet). Say Company 1 has built an RWA platform on Blockchain 2, with dynamic off-chain metadata corresponding to approved users. Additionally, these users need to have an identity score of X as determined by a on-chain DID smart contract on Blockchain 3. In the past, implementing these solutions across various chains would have required multiple complex integrations and in many cases require direct communication with vendors. However, with KRNL, builders now only need to perform a single, one-time permissionless integration.

There is not currently any application layer that facilitates the conditional logic before state changes are executed, and this is generally built ground-up by builders. Ideally, this would be done in a plug-and-play, permissionless manner that would be reproducible by protocols that want to utilize the RWA platform and identifiers from the DID system.

[![Limitations of Existing Solutions](https://ethresear.ch/uploads/default/optimized/3X/8/6/869c6dc2fe0c134bfb17f32f1b481fadcd6e2704_2_690x323.png)Limitations of Existing Solutions5760×2700 268 KB](https://ethresear.ch/uploads/default/869c6dc2fe0c134bfb17f32f1b481fadcd6e2704)

**8. Decentralization and Security Considerations**

**Upholding Decentralization**

KRNL leverages the intrinsic decentralization of existing native blockchains. By integrating with a standard Ethereum RPC node, any Ethereum RPC node can function as a KRNL node without interfering with consensus mechanisms of the underlying network. Node operators are incentivized through the accrual of a proportion of fees generated from kernels, fostering a decentralized and participatory ecosystem.

**Mitigating Malicious Activities**

To preempt and mitigate potential malicious activities, such as replicating KRNL node code to fabricate counterfeit signatures, KRNL employs multiple cryptographic schemes that ensure security by design. The security architecture is flexible, customizable, and predominantly under the control of the dApp developer. This approach ensures that the KRNL Protocol remains permissionless, resilient, and secure.

**Explore more in our [KRNL Developer Sandbox](https://github.com/KRNL-Labs/krnl-node-sandbox-public)**

**Learn more about [KRNL](https://docs.krnl.xyz/)**

**Supporting Research Papers**

[Decentralized FaaS over Multi-Clouds with Blockchain based Management for Supporting Emerging Applications](https://arxiv.org/html/2404.08151v1)

DeFaaS is a novel decentralized Function-as-a-Service (FaaS) system proposed to address the limitations of centralized FaaS solutions. This system leverages blockchain technology and decentralized API management to create a distributed FaaS platform that offers improved scalability, flexibility, security, and reliability. DeFaaS is designed to support various distributed computing scenarios beyond FaaS, including decentralized applications (dApps), volunteer computing, and multi-cloud service mesh. The proposed system aims to mitigate issues associated with centralized FaaS, such as vendor lock-in and single points of failure.

[Multi-Service Model for Blockchain Networks](https://www.sciencedirect.com/science/article/pii/S0306457321000340?ref=pdf_download&fr=RR-2&rr=89e00464f80d773d)

Multi-service networks aim to efficiently supply distinct goods within the same infrastructure by relying on a (typically centralized) authority to manage and coordinate their differential delivery at specific prices. In turn, final customers constantly seek to lower costs whilst maximizing quality and reliability. This paper proposes a decentralized business model for multi-service networks using Ethereum blockchain features – gas, transactions, and smart contracts – to execute multiple services at different prices. By employing Ether, to quantify the quality of service and reliability of distinct private Ethereum networks, their model concurrently processes streams of services at different gas prices while differentially delivering reliability and service quality.

[Qualified Digital Certificates within Blockchain Networks](https://www.researchgate.net/publication/372662346_Orchestrating_Digital_Wallets_for_On-_and_Off-chain_Decentralized_Identity_Management)

This paper examines decentralized digital identities, which use asymmetric cryptography without centralized oversight, focusing on both on-chain (blockchain) and off-chain (self-sovereign) types. Currently, no single wallet manages both types of decentralized identities. To address this, the paper proposes an orchestration solution for a universal wallet that combines both types and validates it using a real-life use case.
