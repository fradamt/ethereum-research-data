---
source: ethresearch
topic_id: 22261
title: Empowering Verifiable Data When EOAs Set a Code
author: EugeRe
date: "2025-05-05"
category: Applications
tags: [account-abstraction, signature-aggregation, transaction-privacy, zk-id]
url: https://ethresear.ch/t/empowering-verifiable-data-when-eoas-set-a-code/22261
views: 338
likes: 2
posts_count: 1
---

# Empowering Verifiable Data When EOAs Set a Code

#### TLDR

This work introduces a modular and innovative pattern that combines Ethereum Improvement Proposal [EIP-7702](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7702.md), [ERC-7715](https://ethereum-magicians.org/t/erc-7715-grant-permissions-from-wallets/20100) permission delegation, and standardized on-chain attestations such as [ERC-7812](https://eips.ethereum.org/EIPS/eip-7812). The pattern allows externally owned accounts (EOAs) to cryptographically and verifiably prove identity and authorization directly during runtime, significantly improving trust, interoperability, and user experience without requiring permanent smart account deployment. Permissions granted via ERC-7715 explicitly reference on-chain attestations, enabling seamless, transparent verification of delegated operations across decentralized applications (dApps). This integration significantly enhances trust, security, interoperability, and user experience in decentralized environments.

Special thanks to [pedrouid (Pedro Gomes) · GitHub](https://github.com/pedrouid), [AndriianChestnykh (Andriian Chestnykh) · GitHub](https://github.com/AndriianChestnykh), [mislavjavor (Mislav Javor) · GitHub](https://github.com/mislavjavor) for the engaging discussions and helping in reviewing. I hope you enjoy!

---

#### The solution: An Open Framework Verify Permission before Execute Sessions

The proposed solution integrates several standards to equip EOAs with advanced functionality and verifiable security. By leveraging EIP-7702, EOAs can temporarily embed smart contract logic into transactions, enabling dynamic, on-chain authorization checks at runtime. ERC-7715 provides a robust framework for creating granular permissions set by wallets to authorize application sessions. EIP-7702 and ERC-7715 bring important benefits in terms of UX, but still require a lot of coordination between market providers, wallets, and other applications.

So, is there a way to frame an open framework to manage wallet permissions and apps sessions to facilitate scaling and avoid market fragmentation?

Standardized attestation registries such as EAS and Privado ID anchor these permissions to verifiable identity credentials, allowing secure, auditable, and trustless verification across decentralized applications.

What if on-chain attestations could be used to seamlessly verify the validity of the permissions set before executing sessions?

Together, these standards can establish a cohesive and secure infrastructure that enhances EOAs without requiring permanent upgrades or complicating existing wallet architectures. It achieves a balanced approach that preserves the user-centric simplicity of EOAs while significantly augmenting their capabilities and security.

Let’s try to figure out a potential execution flow:

| Step | Description |
| --- | --- |
| 1 | Identity Credential Issuance: Users acquire attestations linking EOAs to Decentralized Identifiers (DIDs). |
| 2 | ERC-7715 Permission Delegation: Wallet delegates permissions explicitly referencing identity attestations. |
| 3 | EIP-7702 Authorization Embedding: EOAs temporarily adopt smart contract code referencing attestation-based authorization lists. |
| 4 | Operation Verification & Execution: dApps verify identity credential consistency before executing permitted operations. |

[![](https://ethresear.ch/uploads/default/original/3X/2/c/2c0f97937cbf6c525255a9d4716c607ffb10bf6e.png)706×354 17.3 KB](https://ethresear.ch/uploads/default/2c0f97937cbf6c525255a9d4716c607ffb10bf6e)Practical Use Case Example

Consider Alice, who owns stablecoins across multiple EOAs and wants to purchase an NFT that requires a verifiable identity. Alice first obtains a Proof of Uniqueness credential from an identity issuer like Privado ID. Her wallet then generates an ERC-7715 permission explicitly referencing this credential and defining her purchase operation scope. When Alice initiates the transaction, her wallet embeds smart validation logic via EIP-7702, temporarily granting her EOA the ability to validate permissions at runtime.

The marketplace contract independently verifies Alice’s identity credential and permission scope directly on-chain. If all verifications pass, the marketplace securely and transparently executes Alice’s NFT purchase in a single transaction. This streamlined, secure, and verifiable operation significantly enhances user experience and transaction reliability.

This use case highlights benefits in terms of benefits for different stakeholders:

| Stakeholder | Benefits |
| --- | --- |
| Users | Streamlined permission management, reduced friction, enhanced privacy, multi-EOA interactions |
| Developers & dApps | Simplified integration, increased trust, standardized identity frameworks |
| Wallet Providers | Automated permissions, enhanced UX, reduced identity fraud |
| Exchanges & Marketplaces | Regulatory compliance, cost-effective onboarding, improved security |

Technical Review

The solution uniquely provides ephemeral smart contract execution capabilities to EOAs, significantly reducing gas costs compared to persistent smart wallet deployments and avoiding long-term complexities. Cryptographic identity anchoring through standardized attestations ensures broad compatibility and heightened security. ERC-7715’s precise permission scopes and time-bound delegations significantly reduce operational risks and simplify regulatory compliance.

Upon initiating an EIP-7702 transaction, a user’s wallet references an authorization list explicitly linked to identity credentials stored in a standardized on-chain attestation registry. Permissions delegated via ERC-7715 directly reference the same identity credential. Decentralized applications validate operations securely by matching these credentials, ensuring secure, transparent, and auditable interactions. Critically, before executing EIP-7702 transactions, the apps verify that the attestation referenced for the permission matches the wallet’s attestation, confirming proof of unique identity. Essentially, when a user originates a 7702 transaction, the wallet queries the on-chain attestation registry to retrieve and validate the identity credential associated with the user’s EOA. Then the app cross-verifies this credential against the ERC-7715 permissions stored on-chain, ensuring the attestation matches exactly.

This framework can integrate with diverse, standardized on-chain attestation registries, provided they support decentralized credential issuance, cryptographic verification, and standardized referencing mechanisms.

[![](https://ethresear.ch/uploads/default/optimized/3X/f/c/fcd8e92fb3edf109883513f8bf4711677d1eb123_2_690x366.png)1600×852 109 KB](https://ethresear.ch/uploads/default/fcd8e92fb3edf109883513f8bf4711677d1eb123)

## Call to Action

Integrating standardized on-chain attestation registries like [Privado ID](https://www.privado.id/) Proof of Uniqueness, or [Ethereum Attestation Service](https://attest.org/) (EAS), but it can also reference institutional registries like [European Blockchain Service Infrastructure](https://hub.ebsi.eu/) which may have on-chain exposure. EIP-7702 transactions coordinated with ERC-7715 sessions significantly elevate the user experience to a next level of user interaction. Wallets and app services can benefit from a seamless on-chain, trustless verification logic for sessions; and in this context, decentralized identity management systems ensure transparent, verifiable, and secure permission delegation while not compromising usability and adoption. This robust solution not only simplifies interactions across stakeholders but also solidifies trust within the Ethereum ecosystem, representing a powerful evolution in decentralized identity technology.

Let’s work to combine identity with dynamic permissions on modular wallet architectures, with on chain verification. Together, we can advance towards a future where Ethereum interactions are increasingly secure, transparent, and universally accessible.
