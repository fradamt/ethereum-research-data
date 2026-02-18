---
source: ethresearch
topic_id: 21753
title: Combining on-chain identifiers and proof system to streamline data processing across modular networks
author: EugeRe
date: "2025-02-15"
category: Layer 2
tags: [account-abstraction, signature-aggregation, transaction-privacy, identity, roll-ups]
url: https://ethresear.ch/t/combining-on-chain-identifiers-and-proof-system-to-streamline-data-processing-across-modular-networks/21753
views: 1261
likes: 2
posts_count: 1
---

# Combining on-chain identifiers and proof system to streamline data processing across modular networks

**TLDR**

The post dives into the correlation between on chain identifiers on modular networks with different proofs systems for providing a chain abstracted experience for Ethereum. Finally suggests a path forward to achieve an improved user and developer experiences.

**Credits**

I wanted to thanks to many people into the EF and EVM family for reviewing the ideas and many projects (see reference below) that inspired the work [@emmanuel-awosika](/u/emmanuel-awosika) and all the team [@2077research](https://x.com/2077research?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@tabascoweb3](https://x.com/tabascoweb3?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@pedrouid](https://x.com/pedrouid?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@keepitprivado](https://x.com/keepitprivado?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@alexanderchopan](/u/alexanderchopan) [@andreolf](/u/andreolf) [@chaals](https://x.com/chaals?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@obrezhinev](https://x.com/obrezhniev?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@kopy-kat](/u/kopy-kat) [@ox_shaman](https://x.com/2077research?s=21&t=B5hMAQ6gIb6zJdtD0AxWrw) [@yoavw](/u/yoavw) [@SnapCrackle2383](/u/snapcrackle2383)

**Abstract**

This work represents in some sense a second part of my first blog “[Self-Sovereign Identity and Account Abstraction for Privacy-Preserving cross chain user operations across roll ups](https://ethresear.ch/t/self-sovereign-identity-and-account-abstraction-for-privacy-preserving-cross-chain-user-operations-across-roll-ups/19599)”. Here, I delve into chain abstraction, explaining how the market is implementing its intent to solve market fragmentation and deliver the smoothest possible multichain simplified experience, but still presents issues of network fragmentation due to modularity, different technical approaches, and risk or trust assumptions.

This work explores the integration of decentralized identifiers (DIDs) and proof systems to harmonize data processing and reduce fragmentation across modular blockchain networks. Chain abstraction is identified as a key innovation to overcome network fragmentation, streamline user and developer experiences, and enhance interoperability. By leveraging standardized on-chain identifiers—such as UserIDs, ContractIDs, ChainIDs, and ValidatorIDs—alongside Merkle proofs, zero-knowledge proofs (ZKPs), and fraud proofs, the proposed framework fosters trustless data validation and enables seamless cross-chain operations.

The integration reduces redundancies, ensures privacy, and enhances scalability through modular design. Furthermore, keystore contracts and agentic orchestration are introduced as critical components for secure key management, dynamic transaction execution, and automated cross-chain interaction. By abstracting technical complexities, this work provides a unified and scalable solution to facilitate the mass adoption of blockchain technology while preserving core principles of decentralization, security, and user sovereignty.

### Call to Action

Let’s work together to establish a way to standardize off-chain verifiable data on-chain, so enabling and efficient coordination across Ethereum networks. This will enable projects to develop services that integrate diverse on-chain identity types, combining them with smart contracts designed to process multiple harmonized proofs across an EVM-compatible modular stack. By standardizing data processing, we can harmonize the handling of transactional data across multiple layers and networks, driving greater interoperability, efficiency, and trust in decentralized ecosystems

Key Objectives:

1. Interoperability: Establish standardized on-chain identifiers and proof logic to unify data processes across Layer 1, Layer 2 roll-ups, and EVM-compatible chains.
2. Efficiency: Minimize redundancies in verification and execution, saving computational resources and improving transaction throughput.
3. Scalability: Foster modular public infrastructure that supports higher transaction volumes without sacrificing decentralization.
4. Trust and Privacy: Strengthen the network’s integrity with trustless verification mechanisms while protecting user data through privacy-enhancing technologies.

Intro: The emergence of the narrative for “Chain Abstraction”

Since Ethereum’s inception, network scalability has been a pivotal challenge, impeding both throughput and cost-effectiveness. Early solutions attempted to mitigate congestion through on-chain optimizations and off-chain channels, but it was the introduction of Layer 2 roll-up technologies that truly marked a shift in Ethereum’s strategy. Roll-ups—whether Optimistic or Zero-Knowledge (ZK)—bundle large volumes of transactions off-chain, and periodically commit succinct transaction proofs back to the Ethereum mainnet. This design not only frees valuable on-chain space and reduces transaction costs, but also preserves core Ethereum security assumptions. Over time, Ethereum’s roadmap solidified around the idea that the main chain would act as a robust, trust-minimized settlement layer, while the bulk of user activity and computational workloads would migrate to roll-ups. The result is a layered ecosystem where Ethereum’s base layer guarantees finality and shared security, and various roll-up chains handle high-throughput execution.

Parallel to the shift toward roll-up scalability, the Ethereum community recognized that a truly scalable ecosystem also requires seamless interoperability. In practice, this means ensuring that transactions and smart contracts can move fluidly among various Layer 2 solutions and the Ethereum mainnet. A concerted effort to unify data formats, bridge designs, and token standards has emerged, driving the adoption of cross-chain communication protocols. Standardized message-passing frameworks, bridging solutions that include atomic swaps or canonical bridges, and unified token specifications (e.g., ERC-20 cross-roll-up variants) aim to minimize friction and risk. By defining how data and assets are structured and transferred across different execution environments, Ethereum has laid the groundwork for a cohesive, multi-layer network that provides end users with a smoother experience. This collective push for harmonization ensures that Layer 2 solutions do not become isolated silos, but rather extensions of the same interoperable Ethereum network.

As Layer 2 adoption accelerates and inter-chain operations become routine, a new narrative has gained traction in the Ethereum ecosystem: “Chain Abstraction.” This concept posits that the technical complexities of distinct chains—be they roll-ups, sidechains, or even shards—should ultimately be invisible to end users. Instead of interfacing with a patchwork of chain-specific mechanics, users and developers should experience a unified, abstracted view of the network. Ethereum’s scaling journey thus converges on the idea that application and user experiences transcend the specifics of individual layers, allowing developers to design products that automatically leverage the best available chain resources without sacrificing security or interoperability. Chain abstraction fundamentally redefines how participants perceive the ecosystem, viewing it as a seamlessly interconnected, modular platform rather than a collection of discrete blockchains. Chain abstraction solutions aim to simplify interactions across different blockchains, enhancing usability for both developers and users by hiding the underlying complexities. This is critical for scaling decentralized applications and fostering mass adoption by making blockchain technology more accessible and user-friendly.

[![](https://ethresear.ch/uploads/default/optimized/3X/d/b/dbde48ff1a74097caf59ae83e01ce5cc46b2dfe7_2_567x500.png)1065×938 40.7 KB](https://ethresear.ch/uploads/default/dbde48ff1a74097caf59ae83e01ce5cc46b2dfe7)

Chain abstraction can be systematically understood and classified by the persistent use of several critical product features and infrastructural primitives. One cornerstone is the contract account model, where smart contract wallets and account abstraction frameworks allow flexible signature schemes and more user-friendly transaction flows that manage underlying chain orders also in combination with relayers structures. Another key feature is the use of Onchain identifiers, for instance decentralized identifiers (DIDs) help unify user identity and asset ownership across multiple layers, enabling consistent, chain-agnostic interactions.

Additionally, aggregation proofs in ZK roll-ups reinforce security while minimizing overhead, contributing to an infrastructure where zero-knowledge computations can happen behind the scenes. Finally, modular network systems underscore the architectural shift by decomposing execution, settlement, and data availability, effectively enabling specialized layers that seamlessly interoperate. Collectively, these product features and infrastructural primitives form the backbone of chain abstraction, enabling an ecosystem where end users and developers operate as though interacting with a single, cohesive network.

By streamlinning transactional data, chain abstraction significantly enhances usability and drives growth and adoption in Web 3, taking away from users any worry in regards to any chain they are using and any asset liquidity anchored to specific networks. Those properties facilitate network participation by improving user and developer experience and thus support network growth.

User experience is abstracted from the complexity in a way that the user can execute multiple operations bundled in one transaction time; developer experience is abstracted in a way that the complexity of building a multichain environment is simplified and made efficient for network optimization (scaling). Specifically, complexity of user and developer experience is not extracted from the network for centralization benefits but leverages trustless services to attest to network participant interactions.

For chain abstraction to work effectively, consistent use of decentralized identifier standards is necessary, lets look into details how it may look like.

| Identifier Type | Description | Impact |
| --- | --- | --- |
| Universally Unique IDs (UUIDs), Decentralized Identifiers | Establish authenticated off and on chain user, agent identifier for a specific transaction on a network. | Enhances user recognition in off chain data (PID, OID) or on chain data, that in the context of Ethereum network. could also frame EOA, or wallet address. |
| Contract IDs: .ERC-721, NFT Token IDs , ERC20 token address, Roll Up ContractID | Establish on chain contract address as asset identifier across networks. | Facilitate reliable asset generation on the network and transfers. |
| Chain ID: (EIP-155), EIP3220 Crosschain Identifiers, and ERC-3770 Chain specific addresses, ERC7828 using ENS. | Establish on chain network identifier for harmonizing settlement of transactions across networks and prevents replay attack. | Allows cross chain communication. Also chain specific addressed should be considered to facilitate cross chain services. |
| Validator ID | in the SSLE Single Secret Leader Election mechanism a blinded validator is able to generate a valid proof to generate the block | Ensure that each validator can be uniquely tracked and audited, enhancing accountability and trust in network operations. Reduce network predictability, MEV issues. |

Into the details of Chain abstraction, different functional approaches, risks to a multichain experience but still a fragmented experience

In the chain abstraction world DID documents express ownership of specific data properties, can elaborate signed messages (intents) interacting with service applications, request the execution of the messages as form of User Operations to minting, burning, and transferring tokens interacting with:

1. Wallet Abstraction layer: Solutions that simplify the wallet experience, in terms of onboarding process, and unify wallet experiences by abstracting the management of multiple blockchain accounts into a single interface.
2. Account abstraction layer: Solutions that remove the need for users to manage private keys directly, reducing security risks and improving usability unbounding transaction to one operation only, aggregating signatures and executions under execution environment but still preserving different validating rules.
3. Orchestration layer: Solutions that orchestrate the order flow (user messages as intent or user operations) enabling harmonization of executions on a multi chain environment reducing the complexity for users and developers. Orchestrators route order flow to different roll ups allowing sequencers to execute batches efficiently. Help to coordinate cross-chain activities, enabling seamless multi-chain operations.
4. Roll-up, Shared Sequencer: Solutions that improve scalability by bundling transactions and submitting them to Layer 1 for finality by aggregating and validating proofs of data batches to roll up contract based on pre confirmations. These systems aim to reduce costs and increase transaction throughput, but their use is typically limited to their parent chain.
5. Interoperability Protocols and L1: Solutions that facilitate communication of data messages and signatures between different blockchains, implementing contract account functionalities natively at protocol level and providing cross-chain messaging as relayers, and decentralized oracle services. These protocols standardize data exchange, enabling smart contracts on one chain to interact with others, which is essential for building a truly interconnected onchain ecosystem. They facilitate settlement of execution and the reaching of a finality state.

[![](https://ethresear.ch/uploads/default/optimized/3X/7/4/743a486fa0da9e37e27a7e465b0faab10e59ff56_2_690x467.png)1214×823 70.6 KB](https://ethresear.ch/uploads/default/743a486fa0da9e37e27a7e465b0faab10e59ff56)

On the other side, functional approaches still have security design concerns and here are main areas of risks that should evaluated and provided with a balanced trade-off decision for a technical implementation.

1. Trust Assumptions in Abstraction Layers: Security issues arise when abstraction layers rely on specific assumptions about trust, which shift from networks to providers. These layers handle order flow and authorization, and any vulnerability can lead to manipulation of transaction intent or unauthorized actions. Misalignment in state and consistency assumptions between layers and underlying chains also introduces risks, as discrepancies in interpreting state data can impact transaction integrity.
2. Game-Theoretic Attacks in Solver Networks: Solver networks, which often manage cross-chain transaction executions, may be vulnerable to incentive-based attacks. Solvers may exploit or collude to influence transaction flows, sometimes to their advantage, potentially misdirecting transactions or delaying actions for profit. Such manipulation undermines trust and fairness, especially within decentralized networks where solvers have a high degree of control.
3. Race Conditions in Cross-Chain Transfers: Atomicity issues are common risks in cross-chain data or liquidity transfers. This is due to the lack of harmonization in the block time across chains. This creates timing gaps that attackers can exploit to disrupt transactions or initiate unauthorized fund transfers. Without atomicity, partially completed transactions can lead to asset loss, making robust synchronization essential for cross-chain security.
4. Settlement Challenges and Fund Security: Cross-chain settlements face consistency issues due to varying finality times and fee structures, increasing the risk of failed transactions. Inconsistent finality can lead to unsettled transactions, where funds may become stranded or subject to potential exploitation. Proper handling of settlement failures and ensuring liquidity stability across chains are essential to prevent fund losses and maintain system reliability. Here preconfirmation can play an important role.

Different approaches, risks, layers of networks, and so modularity creates network fragmentation, limiting the impact of the abstraction on market services. In the following part, I will try to explain a personal view of how the combination of using on chain identifiers and proof systems could potentially embed into the Ethereum community a trustless verification logic supporting the data process coordination across Ethereum networks and rationalize a multichain experience into a unified one for users and developers.

Combining decentralized identifiers of modular networks with a standardized proofs system for a unified user and developer experience.

The integration with UUID (like PID, or OID) representing on chain decentralized identifiers (DIDs) with robust proof systems within the Ethereum community represents a transformative approach to harmonizing transactional data processes and fostering a truly interconnected, chain-abstracted experience. This work aims to reposition identity of user and softwares as public good for harmonizing and verifying decentralized interactions on networks.

The synergistic value of combining standardized identifiers—such as Unique User Identifiers (UUIDs), Token IDs, and Rollup IDs—with Merkle proofs, zero-knowledge (zk) proofs, and fraud proofs. Together, these elements create a cohesive framework that addresses critical challenges in cross-chain interactions, data verification, and scalability, ultimately paving the way for mass adoption of blockchain-based services.

DIDs provide a persistent and verifiable means of identifying users, assets, and transactions across different onchain identifiers environments.

- on DIDs offers a unified on chain identity framework that simplifies user verification and authorization, enhancing the security and interoperability of multi-chain operations.
- on ContractIDs (ERC-721 TokenID, ERC-20 contract address) ensure consistent and accurate asset tracking, reducing the complexity and risks associated with cross-chain transfers. Other examples may be roll up contracts IDs (Roll up ID) which enable transparent and verifiable transaction sequencing, reinforcing the integrity of Layer 2 solutions and facilitating scalable transaction throughput.
- on ChainIDs ensure settlement finalization and prevents transaction replay attacks between different networks. In addition to that, chain-specific addresses can facilitate the intercomunication across L2s.
- on potential ValidatorIDs enable specific validator to uniquely verify which is entitled to perform a specific action, proposing a block.

Identifiers standardize the way data is managed and recognized across different chains, serving as a critical foundation for seamless cross-chain interactions.

The integration of proof systems further strengthens the value of this standardized identification framework.

- Merkle proofs enable efficient and lightweight data inclusion verification, allowing users and decentralized applications to validate states and transactions with minimal data exposure. This capability is crucial for cross-chain asset transfers and decentralized finance, where the integrity of data and transactions must be preserved without imposing unnecessary overhead.
- Storage proofs prove the existence of a specific piece of data in a storage system, (e.g., a key-value pair in a smart contract’s storage). They often combine Merkle proofs with additional metadata to verify the state of a particular “slot” or “address” in storage. A concrete example may be verifying state data in account-based blockchains like Ethereum (e.g., verifying that an account’s balance or contract storage matches what is claimed).
- Zero-knowledge proofs (zk proofs) elevate this paradigm by enabling privacy-preserving verification of data validation computation. By allowing computations and transactions to be verified without disclosing sensitive data, zk proofs facilitate secure, scalable, and private interactions, particularly in zk rollup implementations that enhance transaction throughput and reduce costs.
- Fraud proofs complement these mechanisms by providing a means to detect and challenge invalid state computations through optimistic roll-ups, ensuring transaction integrity and protecting user assets from potential manipulation.

UUIDs uniquely identify user-verifiable data off chain, this verification framework enable network participants to set DID as on chain indetifier representation, offering a mechanism to trace user ID-specific interactions on the chain and personalize access control without disclosing sensitive private information.

When combined with Merkle proofs, DIDs allow users to prove membership or data inclusion within a given state without exposing the full underlying data, enhancing data verification and security. Additionally, UserID can be integrated with zero-knowledge proofs to demonstrate user compliance with specific rules or state conditions while maintaining privacy, such as proving the possession of certain credentials without disclosing their full content. In fraud-proof systems, UserIDs ensure user-specific accountability by linking disputed actions or transactions directly to a particular user, thus reinforcing security and transparency.

ContractIDs, such as token ID or Roll Up ID, play a crucial role in decentralized networks by uniquely identifying smart contracts and facilitating traceable interactions across decentralized applications. Smart contracts can use Merkle proofs to validate data against stored states or root hashes, ensuring data consistency and trustless verification. For instance, a contract may rely on a Merkle root to prove membership of data, and new states or interactions can be validated using corresponding proofs. Zero-knowledge proofs offer another dimension by enabling contracts to verify complex computations or data authenticity without revealing sensitive information, thus maintaining both security and privacy during verification. Fraud proofs, when tied to ContractIDs, establish boundaries for challenging invalid state transitions or interactions within a decentralized system, ensuring operational integrity.

ChainIDs provide a unique identifier for each blockchain network, distinguishing them from one another and preventing replay attacks across different chains. Integrating EIP-155, EIP-3220, and ERC-3770 offers substantial value in streamlining transactional data processes across networks by establishing a unified and secure framework for cross-chain interactions. In that context, prooving systems enhances trustless verification by establishing network-specific contexts for data and transactions. For example, cross-chain operations can be verified using Merkle proofs or zero-knowledge proofs that include ChainIDs to prove the data’s network origin, mitigating cross-chain data manipulation. ChainIDs also play a crucial role in fraud-proof mechanisms by anchoring validation processes to specific networks, preventing fraudulent operations that exploit network-specific differences.

ValidatorIDs uniquely identify validators participating in network consensus, providing a mechanism to verify and track which entities validate specific state transitions. Validator IDs ensure accountability and trust within decentralized consensus processes, where validators’ actions can be verified using cryptographic proofs. By incorporating ValidatorIDs into Merkle proofs, a network can demonstrate validator signatures or approvals in an efficient, verifiable manner, strengthening trust in validation processes. Zero-knowledge proofs can be used to enable validators to demonstrate compliance with consensus rules or to prove certain operational properties without revealing sensitive data, enhancing security while maintaining transparency. Fraud proofs tied to Validator IDs ensure that any malicious behavior by validators is challenged and rectified, preserving network integrity and trust.

Here’s a chart summarizing the integration of DIDs (UserIDs, ContractIDs, ChainIDs, and ValidatorIDs) with various proof systems for trustless verification logic in decentralized networks. This combined logic interaction of identifiers and proof system could form the backbone of harmonized networks in Ethereum and EVM community, merging like a glue decentralized identity systems, cross-chain interoperability protocols, scalable Layer-2 solutions, and more.

[![](https://ethresear.ch/uploads/default/optimized/3X/b/4/b431db4dca3eeac6ba7966b9fe6bc4a6c6793f62_2_690x337.png)1600×782 114 KB](https://ethresear.ch/uploads/default/b431db4dca3eeac6ba7966b9fe6bc4a6c6793f62)

In the following chart, I try to provide a vision on how different network identifiers integrated with proof systems to enable a trustless verification logic for decentralized networks. Each identifier plays a specific role, and its integration with proof mechanisms such as Merkle proofs, zk proofs, and fraud proofs ensures data security, verifiability, privacy, and network integrity through combined modular networks made by execution, consensus, and data availability functions.

| Layer | Decentralized Identifier | Proof System | Verification Service |
| --- | --- | --- | --- |
| Execution Layer | User ID | Zero-Knowledge Proof | Prove identity attributes without revealing sensitive details. |
|  |  | Storage Proof | Verify the existence of identity credentials in external storage. |
|  | Token ID | Zero-Knowledge Proof | Prove compliance or token lifecycle events (e.g., minting or burning). |
|  |  | Storage Proof | Confirm token balances or state updates using external data storage. |
|  |  | Fraud Proof | Detect unauthorized token operations or invalid state transitions. |
|  | Rollup ID | Zero-Knowledge Proof | Verify batch correctness or pre-confirmation execution. |
|  | Chain ID | Zero-Knowledge Proof | Validate cross-chain interactions and ensure chain-specific execution logic. |
|  |  | Fraud Proof | Detect invalid cross-chain calls or misaligned chain-specific operations. |
|  |  | Storage Proof | Verify state commitments for rollups stored off-chain. |
| Consensus Layer | Rollup ID | Fraud Proof | Identify invalid rollup batch commitments or transactions. |
|  |  | Merkle Proof | Confirm rollup batch commitments within the consensus. |
|  |  | Storage Proof | Verify consistency between rollup state and on-chain commitments. |
|  | Chain ID | Merkle Proof | Validate the inclusion of chain-specific state or rules in consensus. |
|  |  | Fraud Proof | Detect invalid chain-specific state transitions or proposals. |
|  | Validator ID | Merkle Proof | Prove validator inclusion in a staking or consensus pool. |
|  |  | Fraud Proof | Report incorrect validator behavior or invalid proposals. |
|  |  | Zero-Knowledge Proof | Verify validator compliance with consensus rules. |
|  |  | Storage Proof | Prove validator stake or activity history stored off-chain. |
| Data Availability Layer | User ID | Merkle Proof | Verify identity registry inclusion. |
|  |  | Storage Proof | Prove data inclusion for identity credentials in external databases. |
|  | Token ID | Merkle Proof | Verify token inclusion in state registry and contract compliance. |
|  |  | Storage Proof | Confirm token state data stored in decentralized databases. |
|  | Rollup ID | Merkle Proof | Validate transaction inclusion in rollup batches. |
|  |  | Storage Proof | Prove rollup batch data availability in off-chain storage. |
|  | Chain ID | Merkle Proof | Confirm the availability of chain-specific data (e.g., configurations, state roots). |
|  |  | Storage Proof | Verify the storage of chain configuration or state commitments off-chain. |

In modular networks, proof systems ensure data integrity, correctness, and compliance. These systems provide a trustless mechanism for empowering decentralized identifiers (DIDs) across different operational layers on the networks and rolling out different verification services.

1. Identity Verification is fundamental to ensure that users are authentic while maintaining their privacy and meeting compliance requirements. Merkle Proofs are utilized to confirm a user’s inclusion in a trusted registry without exposing sensitive data, while ZKPs enable selective disclosure of identity attributes, without revealing additional personal details. Fraud Proofs are less applicable in this context as they are typically used for detecting invalid state transitions.
2. Contract Existence Verification, particularly for token lifecycle and compliance, involves validating key operations such as minting, transferring, and burning of tokens, alongside ensuring adherence to compliance frameworks. Merkle Proofs validate the inclusion of tokens or contract terms in state registries. ZKPs allow for private compliance verification, such as KYC/AML requirements, or enforcing specific lifecycle constraints like minting limits. Fraud Proofs, on the other hand, play a critical role in identifying unauthorized state transitions or invalid token operations, enhancing security and trust.
3. Transaction Inclusion Verification ensures that transactions are properly recorded within a rollup state. Merkle Proofs allow for efficient inclusion verification, enabling light clients to confirm transactions without processing the entire state. ZKPs validate the correctness of transaction execution pre-confirmation, such as ensuring sufficient balance or compliance before inclusion. Fraud Proofs detect invalid transactions within rollup batches, resolving disputes through targeted verification of discrepancies.
4. Transaction Settlement Verification ensures that transactions are correctly executed and finalized. Merkle Proofs confirm the inclusion of state transitions in the ledger, while ZKPs provide privacy-preserving verification of transaction settlement, such as confirming atomic swaps without revealing sensitive details. Fraud Proofs help resolve disputes arising from incorrect state transitions, ensuring the integrity of the settlement process.

The combination of verification services enhanced by DIDs and proof systems is even more impactful whether combined with keystore contracts, which are smart contracts designed to securely manage cryptographic keys on-chain. By acting as secure, decentralized storage for cryptographic keys, they enable enhanced identity management, seamless interaction with proof systems, and robust security across modular network layers.

DIDs empower users with self-sovereign identity control, and keystore contracts are integral to this framework by ensuring private keys tied to these identifiers are securely stored. This makes identity systems more resilient and user-centric. Additionally, modular networks allow keystore contracts to operate across execution, consensus, and data availability layers, enabling interoperable identity verification. For example, keystore contracts can validate Merkle proof-based claims to confirm identity attributes while integrating Zero-Knowledge Proofs (ZKPs) for privacy-preserving verification. Fraud Proofs further strengthen these systems by providing a mechanism to detect and report compromised keys or invalid operations.

The integration of keystore contracts with proof systems enables secure and programmable interactions. They facilitate proof aggregation, combining Merkle proofs, ZKPs, and Fraud Proofs to streamline verification processes for DIDs across modular layers. Credential issuance is also more scalable, as issuers can deploy licenses or certificates directly to user-controlled keystore contracts. These credentials can then be verified on-chain through Merkle proofs or ZKPs without compromising user privacy. Keystore contracts also support automated compliance verification, such as KYC or AML checks, enhancing adherence to regulations while preserving confidentiality.

Keystore contracts enhance security by incorporating advanced mechanisms like multi-signature authorization and social recovery, reducing risks of key loss or theft. Their tamper-resistant storage ensures keys remain secure even in adversarial conditions. These features are particularly beneficial for modular networks, where keys must remain accessible yet secure across various layers and environments.

By associating keys with DIDs, users can be uniquely identified without revealing personal information, thus enhancing privacy and personalized access control. Contract IDs allow for the precise identification and interaction with specific keystore contracts, facilitating seamless integration with other smart contracts and decentralized applications. Chain IDs help distinguish between different networks, enabling keystore contracts to operate securely across Ethereum and various L2s. Validator IDs can authenticate validators responsible for key management operations, adding an extra layer of trust and accountability.

Essentially, keystores become a perfect data container embedding user signing powers and routing onchain identifiers that are verified as inclusion and computation, streamlining network aggregation process.

The integration with proof systems further strengthens keystore contracts. Merkle proofs enable efficient and secure verification of keys without exposing the entire dataset, as users can prove the inclusion of their key in a Merkle tree stored within the keystore contract. Zero-knowledge proofs allow users to demonstrate possession of a secret key or authorization to access certain functionalities without revealing the key itself, thereby maintaining privacy and security. Fraud proofs can be employed to challenge and verify any unauthorized access or key misuse, ensuring that only legitimate operations are executed within the keystore contract.

[![](https://ethresear.ch/uploads/default/optimized/3X/9/9/9976ad69c3ebb51a3af7cda333623421df117e41_2_690x341.png)1600×793 118 KB](https://ethresear.ch/uploads/default/9976ad69c3ebb51a3af7cda333623421df117e41)

Solving Cross chain UX: embedding a trustless verification logic for bridging to streamline agentic network’s data process through harmonization into a unified experience

So far I have been investigating from “micro” perspective potential features that may enable Chain abstraction, but in order to conclude this investigation I belive it is necessary to answer at least two question:

- How all this tech can coexist together?
- Can Ethereum enable Chain abstraction for the EVM compatible community? and how does it fit with the current rollup / interoperability strategy?

Lets start from the first point..

The proposed framework for integrating decentralized identifiers (DIDs), proof systems, and keystore contracts can create a robust foundation for deploying contract accounts across multiple modular blockchain networks. These contract accounts can benefit from a unified system that streamlines the complexities of managing transactions across diverse execution, consensus, and data availability layers, ensuring seamless interoperability and enhanced user experiences.

Following the same account type model, Contract Accounts entry points may be deployed on multiple chains across L2 following ERC4337- 7560/62 etc, and landing to Main-net with EIP 7701.

Assuming that blockchain networks adopt compatible decentralized identity standards, the system places on-chain identifiers at its core. These identifiers serve as digital IDs for each contract account. By embedding decentralized identifiers (DIDs) into these accounts, every user and contract is recognized uniformly across different networks. This unified identity approach assumes that all participating networks support the same DID protocols or have mechanisms to interoperate with them. As a result, it removes the need to manage multiple, isolated identity systems and allows secure, decentralized interactions without relying on any central authority.

The framework also relies on on-chain credentials and zero-knowledge (ZK) attestations to verify actions without exposing sensitive information. For example, a contract might prove that a user completed a specific action on one network while keeping private details confidential. This process presupposes that the underlying blockchain infrastructures are capable of generating and verifying ZK proofs and on-chain credentials. In turn, this enhances overall trust in the system by ensuring that interactions remain both secure and private.

Overall, the design creates an interconnected environment in which smart contract accounts can operate seamlessly across multiple blockchain networks. It simplifies transaction management by combining the benefits of Layer 2 (L2) scalability with the robust security of the main chain. This aspect of the framework assumes that advanced cryptographic tools and cross-chain interoperability standards are mature and uniformly implemented, thereby offering a consistent and user-friendly experience.

A vital component of this system is the use of keystore contracts. These contracts provide a secure, tamper-resistant environment for managing cryptographic keys associated with DIDs, enabling dynamic key rotation across wallets. They also support advanced security features like multi-signature authorization, threshold signatures, and social recovery mechanisms. For instance, a keystore contract tied to a DID could autonomously verify a user’s intent and sign transactions, streamlining complex multi-chain operations such as token bridging or compliance verification. This functionality is built on the assumption that smart contracts can reliably handle advanced cryptographic operations and that blockchain networks can support such sophisticated features.

Leveraging keystore contracts further allows wallet applications to store on-chain credentials for use across multiple chains. This means that a single execution environment can facilitate operations on various networks, assuming that both the wallet applications and the underlying blockchain infrastructures are designed for cross-chain interoperability and maintain high security standards.

Additionally, the framework integrates several proof systems—such as Merkle proofs, zero-knowledge proofs, and fraud proofs—to validate transactional data across modular blockchain layers. These proofs help ensure that data validation is efficient and trustless, assuming that each blockchain layer (execution, consensus, and data availability) can produce and verify these proofs effectively. By harnessing these proof systems, contract accounts can autonomously verify and execute transactions, confirming inclusion in the data availability layer, proper execution in the execution layer, and adherence to consensus rules, all within one unified system. This integration minimizes operational friction and enhances the reliability of cross-chain transactions.

Considering a very high number of interactions, contract calls may be required in order to manage efficiently the user flow across all the different layers of the modular stack, agents may represent a concrete interface solution to coordinating the underlying data process.

[![](https://ethresear.ch/uploads/default/optimized/3X/0/a/0ad1a9143e9dbfd45ef4df00b33843f618ff92d1_2_690x378.png)1600×877 115 KB](https://ethresear.ch/uploads/default/0ad1a9143e9dbfd45ef4df00b33843f618ff92d1)

Into this framework, agents serve as “intelligent servant” user interfaces with an onchain presence orchestrating user data flow, and aiming the fulfillment of multiple network intents by solvers that abstract the complexities of multi-chain environments.

Agents, which can be represented as non-fungible tokens (NFTs), serve as intelligent orchestrators and executors of user intents. These intents, such as token swaps, staking, or compliance verifications, are translated by agents into actionable tasks that abstract the complexities of multi-chain environments. Agents are directly linked to keystore contracts, which provide the cryptographic foundation necessary for securing and managing private keys associated with user agent’s decentralized identifiers (DIDs). By binding agents’ operational logic to their keystore, the framework ensures that every action executed by an agent NFT is securely authorized and compliant with user-defined parameters.

The agent NFT acts as both a representation of ownership and a functional interface, allowing users to manage their intents and interact with decentralized systems securely. Keystore contracts, serving as the backbone of this system, maintain the integrity and privacy of the cryptographic keys required for operations. These contracts enforce secure authentication, multi-signature authorization, and optional social recovery mechanisms. By anchoring agent NFTs to keystores, the framework enables agents to inherit these security properties, ensuring that operations initiated by an agent are both tamper-resistant and self-sovereign.

Proof systems, including Merkle proofs, Zero-Knowledge Proofs (ZKPs), and Fraud Proofs, further enhance this agentic-driven framework. These systems validate the correctness and compliance of transactions across modular layers. For instance, Merkle proofs confirm the inclusion of user credentials or token data in identity registries, while ZKPs enable privacy-preserving compliance verification, such as proving adherence to KYC/AML requirements without exposing sensitive data. Fraud Proofs act as a safeguard, detecting and resolving invalid state transitions or unauthorized actions, thus strengthening the security and trustworthiness of multi-chain operations.

The agents’ ability to dynamically orchestrate these proof systems transforms a fragmented multi-chain experience into a unified process. By leveraging AI, agents optimize execution paths based on real-time network conditions, such as transaction costs, liquidity availability, or finality times. They interact seamlessly across the modular layers—executing smart contract logic, ensuring consensus validation, and verifying data availability commitments. This layered interaction allows agents to maintain consistency and efficiency in executing user intents, even when the underlying networks differ significantly in their design or performance.

Furthermore, agents facilitate cross-layer and cross-chain interoperability, ensuring that user intents are fulfilled without manual intervention. For example, an agent tasked with executing a token swap may analyze multiple chains to identify the most cost-effective and timely route, leveraging proof aggregation to validate transactions efficiently across the involved networks. In case of disruptions, such as network congestion or failed transactions, the agent can adapt dynamically, rerouting the intent through alternative chains or liquidity sources. This adaptability not only ensures the continuity of operations but also enhances the overall user experience by abstracting the complexities of multi-chain interactions.

By integrating keystore contracts, agents secure and manage cryptographic keys while automating interactions with proof systems. These contracts underpin the agents’ ability to verify Merkle root commitments, validate ZKPs, and enforce compliance policies autonomously. They also provide advanced features like multi-signature authorization and social recovery, mitigating risks of key loss or theft. Together, agents and keystore contracts establish a unified interface for users to interact with decentralized applications across chains, further reducing complexity and enhancing usability.

Agents leveraging DIDs and proof systems provide the cornerstone for a streamlined, scalable, and privacy-preserving multi-chain ecosystem. By unifying identity management, automating transaction validation, and dynamically orchestrating execution paths, users through delegated agents transform the fragmented nature of multi-chain environments into a cohesive framework. This approach not only simplifies user interactions but also supports modular blockchain networks in achieving their potential for interoperability and standardization. As blockchain technology continues to evolve, the integration of these components will play a crucial role in fostering a unified and inclusive digital ecosystem.

[![](https://ethresear.ch/uploads/default/optimized/3X/2/1/21e6d3bf7847d88a1b8bcfd57adb99839067f0c6_2_690x252.png)1600×586 125 KB](https://ethresear.ch/uploads/default/21e6d3bf7847d88a1b8bcfd57adb99839067f0c6)

Now coming to the second point, what kind of impact chain abstraction may have for the future of Ethereum as a community?

It’s difficult to say precisely and many scenarios are possible, but it’s my personal opinion to share a positive view on it. The work determined many factors to assume that chain abstraction is a key innovation to standardize the operations across the specific EVM-compatible chains. In that sense, it is undoubtedly supporting the development of the interoperability roadmap and the execution of the roll-up strategy.

I try to display here a personal think-through road map of improvements for Ethereum standardization, abstracting rollups, execution, and consensus improvements to derive a unified experience.

[![](https://ethresear.ch/uploads/default/optimized/3X/3/7/37f3ece684be15b0d08497eef6aacead92b8d111_2_690x476.png)1204×830 90.5 KB](https://ethresear.ch/uploads/default/37f3ece684be15b0d08497eef6aacead92b8d111)

Cross-chain intent will be enabled by native smart contract accounts relying on multiple wallets; in that context, chain-specific addresses may facilitate settlement across different rollups. The ethreum execution layer, powered by EOF, benefits from EVM being able to handle structured codes, facilitating running smart contract validation, execution, and testing under common language. Essentially, EOF lays the groundwork for an execution environment that adapts to a variety of chains. This flexibility is key to realizing a unified experience and a future where multiple, interconnected chains operate harmoniously, allowing for scalability, specialized execution environments, and ultimately a richer ecosystem for decentralized applications.

Finally, on the consensus layer, I can foresee elements in the end game beam chain that, for instance on chain identifiers can leverage zk-based attestations to empower validator operations, at the same time pre-confirmation can support syncronism of communication with the execution layer.Contract accounts relying on aggregated proofs determine a “snarkification” process flow that may play a key role in determining a streamlined data process in the execution and validation of network services.

To conclude, I wanted to write those lines because I believe that firstly is ethereum is a community first, even than code, built over a pathway of values such as sovereignty, empowerment, and decentralization, where proposals and standards should reinforce our values and commitment to deliver.

**List of references**

### Ethereum / Roll Up Improvement Proposals (E/RIPs)

- EIP-155: Simple Replay Attack Protection
EIP-155: Simple replay attack protection
Introduces chain IDs to prevent replay attacks across different Ethereum forks or networks.
- EIP-721: Non-Fungible Token Standard
ERC-721: Non-Fungible Token Standard
Defines unique, on-chain identifiers for assets, essential for tracking individual tokens.
- EIP-1155: Multi-Token Standard
ERC-1155: Multi Token Standard
Enhances asset representation, allowing a single contract to manage fungible and non-fungible tokens.
- EIP-2981: Royalty Standard
ERC-2981: NFT Royalty Standard
Facilitates royalty payments for NFT creators, potentially applicable in licensing and compliance contexts.
- EIP-712: Typed Structured Data Hashing and Signing
EIP-712: Typed structured data hashing and signing
Standardizes data structures for signing off-chain and verifying on-chain operations.
- EIP-3770: Chain-Specific Address Format
ERC-3770: Chain-specific addresses
Standardizes the inclusion of chain IDs in addresses to improve cross-chain interoperability.
- EIP-4337: Account Abstraction via Entry Point Contract
ERC-4337: Account Abstraction Using Alt Mempool
Implements account abstraction without requiring changes to the Ethereum protocol, enabling enhanced functionality for smart contract wallets.
- EIP-3220: Cross-Chain Message Identifiers
EIP-3220: Crosschain Identifier Specification
Specifies unique identifiers for cross-chain communication to ensure message traceability and integrity.
- EIP-7441 Upgrades the block proposer election mechanism to Whisk EIPs/EIPS/eip-7441.md at 8118bf127b15abe60530e939ec56654d6f19a7d6 · ethereum/EIPs · GitHub
More in general on SSLE: Secret leader election | ethereum.org
- EIP-7683: Cross chain Intents
ERC-7683: Cross Chain Intents
Defines standard API for cross-chain value-transfer systems.
- RIP-7212: Precompile for secp256r1 Curve Support
Proposal to add a precompiled contract that performs signature verifications in the “secp256r1” elliptic curve.
RIPs/RIPS/rip-7212.md at eedf04cdeeb4feb141a271cede23260eb66d03b8 · ethereum/RIPs · GitHub
- EIP-7702: Set EOA Account Code
https://eips.ethereum.org/EIPS/eip-7702
Allows Externally Owned Accounts (EOAs) to set their code based on existing smart contracts, enhancing account abstraction capabilities.
- EIP-7701: Native Account Abstraction with EOF
https://eips.ethereum.org/EIPS/eip-7701
Proposes a variation of native account abstraction design, relying on features of the EVM Object Format (EOF).
- EIP-7560: Native Account Abstraction
https://eips.ethereum.org/EIPS/eip-7560
Introduces a native account abstraction design, enabling smart contract wallets to separate validation and execution code.
- EIP-7579: Minimal Modular Smart Accounts
https://eips.ethereum.org/EIPS/eip-7579
Outlines minimally required interfaces and behavior for modular smart accounts to ensure interoperability.
- EIP-7662: AI Agents NFT
A specification for NFTs that represent AI Agents
ERC-7662: AI Agent NFTs

---

### Ethereum Request for Comments (ERCs)

- ERC-20: Fungible Token Standard
ERC-20: Token Standard
The foundational standard for fungible tokens, vital for representing assets and conducting transactions.
- ERC-721: Non-Fungible Token Standard
ERC-721: Non-Fungible Token Standard
Defines unique token identifiers essential for asset management.
- ERC-165: Interface Detection Standard
ERC-165: Standard Interface Detection
Enables smart contracts to declare and detect implemented interfaces.
- ERC-1271: Signature Validation
ERC-1271: Standard Signature Validation Method for Contracts
Specifies a standard for signature validation, enhancing wallet interactions with contracts.
- ERC-5762: Batch Execution for Wallets
https://eips.ethereum.org/EIPS/eip-5762
Enables batch execution capabilities for wallet transactions, improving efficiency.
- ERC-7828 Chain Specific Addresses using ENS
https://ethereum-magicians.org/t/erc-7828-chain-specific-addresses-using-ens/21930

A unified chain-specific address format that allows specifying the chain on which that account intends to transact.

---

### Additional Reference

W3C Decentralized Identifiers (DIDs)

https://www.w3.org/TR/did-core/Provides the foundational framework for decentralized identity systems, integrating off-chain and on-chain identity data.

List of protocols and solutions inspired the work:

- Iden3 Protocol
https://iden3.io/
- Particle Network
https://www.particle.network/
- Near Foundation
https://near.org/
- Privado ID
https://www.privado.ai/
- Ethereum Name Service (ENS)
https://ens.domains/
- Polygon Labs
https://polygon.technology/
- ZKSync
https://zksync.io/
- Optimism
https://optimism.io/
- WalletConnect
https://walletconnect.com/
- Safe (formerly Gnosis Safe)
https://safe.global/
- Rhinestone
https://rhinestone.org/
- Biconomy
https://www.biconomy.io/
- Uniswap
https://uniswap.org/
- Celestia
https://celestia.org/
- Avail
https://www.availproject.org/
- LayerZero
https://layerzero.network/
- Across Protocol
https://across.to/
- Herodotus
https://herodotus.dev/
- Gevulot
https://gevulot.io/
