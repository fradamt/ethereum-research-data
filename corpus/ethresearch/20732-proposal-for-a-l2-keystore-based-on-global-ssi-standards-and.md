---
source: ethresearch
topic_id: 20732
title: Proposal for a L2 Keystore based on global SSI standards and reference implementations
author: Therecanbeonlyone
date: "2024-10-21"
category: Layer 2
tags: [identity]
url: https://ethresear.ch/t/proposal-for-a-l2-keystore-based-on-global-ssi-standards-and-reference-implementations/20732
views: 234
likes: 3
posts_count: 2
---

# Proposal for a L2 Keystore based on global SSI standards and reference implementations

TLDR: We propose a Sidetree-based key store L2 network as a public utility deployed and operated by trusted Ethereum ecosystem entities such as L2 operators and large enterprises supporting Ethereum as a standardized cross-chain and low-cost non-custodial key management stack using W3C Decentralized Identifiers (DIDs).

**Background**

The [Ethereum Oasis Community Projects L2 Standards WG](https://github.com/ethereum-oasis-op/L2) recently published [a report](https://entethalliance.org/w3cs-did-and-vc-technology-can-help-with-ethereums-three-transitions/) " How W3C DIDs and VCs can help with Ethereum’s Three Transitions". This report aligns with the recent posts ([1](https://ethresear.ch/t/self-sovereign-identity-and-account-abstraction-for-privacy-preserving-cross-chain-user-operations-across-roll-ups/19599) and [2](https://ethresear.ch/t/enabling-standardized-on-chain-executions-through-modular-accounts/20127)) by [@EugeRe](/u/eugere). In our report, we discuss how the integration of W3C Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs) can address challenges faced by Ethereum as it undergoes its three major transitions: scaling through L2 rollups, enhancing wallet security via smart contract wallets, and advancing privacy. Ethereum’s transitions necessitate changes in how users manage identities, keys, and addresses. DIDs and VCs, core components of the decentralized identity ecosystem, offer solutions for these challenges.

We argue that DIDs provide globally unique, resolvable identifiers, while VCs enable verifiable claims about identity, attributes, or qualifications. By leveraging DIDs and VCs, Ethereum can improve identity management, key rotation and recovery, and privacy. DID documents can store addresses across various networks and facilitate key management, including social recovery. Additionally, zero-knowledge proofs can enhance privacy when using keys from DID documents in Ethereum ecosystem transactions both on and offchain.

Several DID methods, based on the [Sidetree Protocol](https://identity.foundation/sidetree/spec/), a Layer 2 DID standard with [reference implementations](https://github.com/decentralized-identity/sidetree), are suitable for the Ethereum ecosystem, offering permissionless, blockchain-anchored, scalable, and cost-effective solutions. The Sidetree Protocol was developed by the Decentralized Identity Foundation ([DIF](https://identity.foundation/)) and enables the creation and management of scalable DIDs on various blockchain networks, making it a blockchain-agnostic solution. This allows DIDs to be anchored to different distributed ledger technologies such as Ethereum Mainnet.

**Key Technical Aspects**

- Layer 2 Protocol: Sidetree operates as a layer on top of existing blockchain networks, decoupling DID operations from the base layer’s transaction limitations. This allows for improved scalability and reduced costs compared to directly interacting with the blockchain for every DID operation.
- Blockchain Agnostic: The protocol is designed to work with any blockchain that supports anchoring data, providing flexibility in choosing the underlying network. Popular implementations exist on blockchains like Bitcoin (ION) and Ethereum (Element).
- Decentralized PKI (DPKI): Sidetree leverages a decentralized public key infrastructure, where DID controllers hold the private keys associated with their DIDs. This empowers users with full control over their digital identities.
- DID Operations: The core operations supported by Sidetree are Create, Update, Recover, and Deactivate. These actions allow for the lifecycle management of DIDs and their associated DID documents.
- Content-Addressable Storage (CAS): Sidetree utilizes CAS systems like IPFS or Filecoin to store DID documents and other related data. This ensures data immutability and availability through a decentralized network.
- Batching and Anchoring: To optimize efficiency, Sidetree nodes batch multiple DID operations together and anchor them to the underlying blockchain in a single transaction. This significantly reduces transaction costs and improves throughput.
- Conflict-Free Replicated Data Types (CRDTs): Sidetree employs CRDTs to manage DID document updates and resolve conflicts in a decentralized manner. This ensures data consistency across the network.

In the Sidetree protocol, updating a DID document is a multi-step process as summarized below:

1. Generate Update Payload: The DID controller creates an update payload, which includes the following components:

- didSuffix: The unique suffix of the DID being updated.
- revealValue: The revealed value of the previous update commitment, used for verification.
- patches: An array of JSON Patch operations specifying the modifications to be made to the DID Document.
- updateCommitment: A new commitment value for the next update operation.

1. Submit to Sidetree Node: The DID controller submits the update payload to a Sidetree node.
2. Batching and Anchoring: The Sidetree node collects multiple update operations and other DID operations, batches them together into an anchor file, and anchors this file to the underlying blockchain. The anchor file contains hashes of the operations and other metadata, but not the actual operation data.
3. Store Operation Data: The Sidetree node stores the full update operation data, along with other operations, in a ‘chunk file’ and makes it available via a content-addressable storage (CAS) system like IPFS or Filecoin. The anchor file on the blockchain contains a reference to this chunk file.
4. Resolution: When another entity wants to resolve the DID and obtain the latest DID Document, they query a Sidetree node.
5. Retrieve and Apply Updates: The Sidetree node retrieves the relevant anchor files from the blockchain, follows the references to the chunk files on the CAS, and applies all the update operations in chronological order to the original DID Document to construct the latest version.

The Sidetree protocol furthermore incorporates several security measures to ensure the integrity of DID operations and mitigate potential attack vectors:

**1. Decentralized Public Key Infrastructure (DPKI)**

- DID Controller Holds Private Keys: Each DID controller possesses the private keys associated with their DIDs, giving them complete control over their identity data. This eliminates the risk of a single point of failure or compromise associated with centralized key management systems.

**2. Commitment Scheme**

- Update Commitments: Each update operation includes a commitment to the next update, cryptographically linking successive updates. This prevents unauthorized modifications or tampering with the DID Document’s history.
- Reveal Value: The reveal value associated with the previous update commitment ensures that only the DID controller with the corresponding private key can initiate a new update.

**3. Batching and Anchoring**

- Blockchain Anchoring: Batching multiple DID operations into anchor files and anchoring them to the blockchain provides a tamper-proof and auditable history of operations.
- Content-Addressable Storage (CAS): Storing operation data in a CAS like IPFS or Filecoin further enhances immutability and prevents unauthorized modification.

**4. Cryptographic Operations**

- Digital Signatures: Operations are signed using the DID controller’s private key, ensuring authenticity and non-repudiation.
- Hashing: Hash functions are used extensively for creating commitments, linking operations, and generating identifiers, adding another layer of security and integrity.

**5. Conflict-Free Replicated Data Types (CRDTs)**

- Deterministic Conflict Resolution: CRDTs enable the network to handle concurrent updates to the same DID Document and resolve conflicts in a consistent and predictable manner.

**6. Network Redundancy and Decentralization**

- Multiple Sidetree Nodes: The existence of multiple Sidetree nodes operated by different entities reduces the risk of a single point of failure or censorship.
- Peer-to-Peer Resolution: The ability to resolve DIDs by querying any Sidetree node further enhances decentralization and resilience.

**Mitigation of Attack Vectors**

- Unauthorized Updates: The commitment scheme and the requirement for the DID controller’s private key for updates prevent unauthorized modifications to the DID Document.
- Data Tampering: Blockchain anchoring and CAS storage ensure data immutability, making it difficult to tamper with past operations or DID documents.
- Censorship: The decentralized nature of the network with multiple nodes and peer-to-peer resolution mitigates the risk of censorship or denial of service attacks.
- Single Point of Failure: The distribution of private keys among DID controllers and the redundancy of Sidetree nodes reduce the risk of a single point of compromise.

**Proposal**

Given the above, we propose that a Sidetree-based L2 key store network be deployed and operated as a public utility by trusted Ethereum ecosystem entities such as L2 operators, and large enterprises supporting Ethereum as a standardized cross-chain and low-cost non-custodial key management solution without vendor-lockin in contrast to any bespoke solution currently contemplated.

We envision the following beneficial characteristics of such an approach:

1. Cross-chain DID resolution: When interacting with different Ethereum networks (mainnet, testnets, or other L2s), the user’s DID can be resolved through the L2 Sidetree network. This allows applications and smart contracts on these networks to access the user’s DID document and verify their keys.
2. Low-cost key management operations: Key rotation, recovery, and other key management operations can be performed on the L2 Sidetree network in batches significantly lowering individual transaction costs.
3. ZK proofs for privacy: Zero-knowledge proofs can be used to selectively reveal information about the user’s keys and DID document while preserving privacy. This allows for secure and private interactions across different Ethereum networks without exposing sensitive data.
4. Smart contract wallets and DIDs: Smart contract wallets can be associated with DIDs, enabling secure and decentralized key management for these wallets. The DID document can specify the controlling keys for the wallet, allowing for multi-signature and social recovery mechanisms.
5. Interoperability and standardization: By leveraging the W3C DID standard and the Sidetree protocol, the L2 Sidetree network ensures interoperability with other DID systems and applications within the Ethereum ecosystem such as Polygon ID. This promotes a seamless and user-friendly experience for managing keys and identities across different chains.
6. Avoiding Vendor Lock-In: By using global identity standards from the W3C and DIF together with open-source reference implementations and independent Sidetree node operators, the ecosystem can make cross-chain identity/key operations a public utility at very low to no costs.

We are inviting and looking forward to comments on this proposal.

## Replies

**EugeRe** (2024-10-21):

Thanks [@Therecanbeonlyone](/u/therecanbeonlyone) for mentioning in your work and I am happy to share my takeaways for the proposal.

1. Sidetree protocol enables scalable, decentralized identity management by anchoring DIDs into networks through batching. This design minimizes on-chain operations, making key management efficient and cost-effective. Sidetree supports global standards like W3C DIDs, ensuring interoperability across different platforms.
2. When integrated with smart contract accounts, Sidetree allows for programmable and automated management of keys and identities. Smart contracts can handle key rotation, recovery processes, and multi-signature schemes, even quantum resistant schemes, adding security and flexibility. These accounts enable non-custodial key management, ensuring that users retain full control of their keys while still benefiting from the automation and security features provided by smart contracts accounts. This integration also ensures that the decentralized identities managed within the smart contract accounts are interoperable across different blockchain networks setting different rules, providing a seamless experience for users and platforms alike.
3. This approach is particularly important for zk-rollup networks and zk-ID solutions, which aim to standardize user’s privacy in blockchain systems. Zk-rollups instead they aims to reduce the computational load on-chain, and Sidetree’s ability to batch identity operations off-chain fits this model perfectly, ensuring efficiency. By combining smart contract accounts with zk-ID wallets, decentralized identity solutions can offer privacy-preserving, scalable key and identity management, which is critical for secure interactions on Layer 2 networks. This synergy enhances the usability and security of zk-rollup-based platforms while ensuring compliance with decentralized identity standards.
4. A L2 keystore roll-up that integrates decentralized identity protocols, such as the Sidetree protocol, aligns perfectly with Ethereum’s broader vision of providing identity as a public good. By utilizing the scalability and efficiency of L2 roll-ups, such a solution can manage vast numbers of decentralized identities (DIDs) and their associated keys in a cost-effective and secure manner. Sidetree, with its off-chain processing and batching of DID operations, ensures that the heavy computational tasks of identity management do not burden the Ethereum base layer, maintaining scalability while preserving decentralized control .
5. This L2-based keystore solution ensures that key management, often a complex and centralized task, is now user-centric, automated, and programmable through smart contract accounts. By making identity management decentralized and non-custodial, it offers individuals full control over their digital identities while ensuring interoperability across different blockchains and applications. This decentralized framework directly supports Ethereum’s ethos of reducing reliance on centralized services and enabling users to control their assets, keys, and identities.
6. Furthermore, implementing a keystore roll-up that integrates with zk-rollups and zk-ID solutions can provide additional privacy and scalability benefits. Zero-knowledge proofs enable efficient, privacy-preserving transactions, allowing identity operations to be processed without exposing sensitive data on-chain. This is crucial for Ethereum’s long-term goal of establishing a secure, scalable infrastructure that can support identity as a public utility. By leveraging roll-ups to manage decentralized identities, Ethereum can fulfill its vision of making identity management a public good, fostering trust, privacy, and user sovereignty across the network.

