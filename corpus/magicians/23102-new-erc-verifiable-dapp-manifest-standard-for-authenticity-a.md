---
source: magicians
topic_id: 23102
title: "New ERC: Verifiable dApp Manifest Standard for Authenticity and Transparency"
author: yoheinishikubo
date: "2025-03-10"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-verifiable-dapp-manifest-standard-for-authenticity-and-transparency/23102
views: 104
likes: 0
posts_count: 3
---

# New ERC: Verifiable dApp Manifest Standard for Authenticity and Transparency

Hello Ethereum Magicians,

I’d like to propose a new Ethereum Improvement Proposal (EIP) to establish a standard for verifying the authenticity of decentralized applications (dApps) and enhancing transparency around their associated smart contracts.

In the rapidly growing dApp ecosystem, trust and user security are paramount. Users need reliable ways to ensure they are interacting with legitimate applications and understand the smart contracts that underpin them. This EIP aims to address these critical needs by introducing a verifiable dApp manifest standard.

This proposal outlines a mechanism leveraging Verifiable Credentials (VCs) and a dedicated `AppManifest` smart contract to cryptographically link a dApp’s web presence to its on-chain smart contracts. By hosting a `manifest.json` VC at the dApp’s root URL and requiring managed contracts to explicitly acknowledge the `AppManifest` contract, we can create a robust and transparent system for dApp verification.

A working demo: https://app-manifest.3am.center/

I believe this standard can significantly improve user confidence and security within the Ethereum ecosystem. I’m eager to hear your feedback and discuss how we can refine and advance this proposal.

I look forward to your comments and suggestions!

Best regards,

Yohei Nishikubo

Below is the detailed draft of the EIP for your review:

## Abstract

This Ethereum Improvement Proposal (EIP) introduces a novel standard for establishing trust and transparency in decentralized applications (dApps) through a robust verification mechanism. It defines a method for verifying the authenticity of dApps and transparently managing their associated smart contracts. At its core lies the `AppManifest` smart contract, complemented by the strategic use of Verifiable Credentials (VCs). This VC cryptographically links a dApp’s URL to its deployed smart contract address. By hosting a VC (`manifest.json`) at the dApp’s root URL and referencing the dApp URL within the `applicationURI` field of the `AppManifest` contract, users can independently verify a dApp’s legitimate origin and ensure its integrity. **Critically, the process is secured by verifying that managed contracts explicitly grant the `MANIFEST_ROLE` to the AppManifest contract, thereby binding their association on-chain.**

## Motivation

In the rapidly expanding landscape of decentralized applications, establishing the genuine authenticity of a dApp and clearly defining its relationship with deployed smart contracts is crucial for user security and trust. Users demand assurance that they are interacting with the intended application rather than a deceptive or malicious imitation. Furthermore, the ability for users and developers to readily discover and manage interconnected smart contracts within a dApp ecosystem is highly beneficial.

This EIP addresses these needs by offering a standardized approach to:

- Confidently Verify dApp Authenticity:
Leveraging a Verifiable Credential (VC) hosted at the dApp’s root URL, users can verify the dApp’s origin. The VC’s digital signature and the mandatory applicationURI claim serve as robust safeguards against impersonation and phishing attacks.
- Streamline Smart Contract Discovery and Management:
The AppManifest contract serves as a centralized, on-chain registry for a dApp’s associated smart contracts. The managedContractAddresses function allows for efficient retrieval of contract addresses that have explicitly opted in by granting the MANIFEST_ROLE to the AppManifest.
- Elevate Trust and Transparency:
This standard enhances trust in dApps by linking the web identity (via the VC) with on-chain data and by ensuring that only contracts that have explicitly granted the MANIFEST_ROLE are considered part of the dApp ecosystem.

## Specification

This EIP introduces the following components and specifications to achieve verifiable dApp authenticity and streamlined smart contract management:

### 1. Verifiable Credential (VC) - manifest.json

- Location:
The VC file, named manifest.json, MUST be located in the root directory of the dApp’s URL to ensure easy discovery. For example, if the dApp’s URL is https://example.dapp/, the VC MUST be accessible at https://example.dapp/manifest.json. Alternatively, a  tag using the x-app-manifest attribute may specify a different filename.
- Format:
The manifest.json file MUST be a valid JSON document conforming to the Verifiable Credential standard (e.g., W3C Verifiable Credentials Data Model 1.1).
- Content:
The VC MUST include the following essential claims:

 @context:
MUST include https://www.w3.org/2018/credentials/v1 and MAY include additional context URIs for enhanced semantic clarity.
- type:
MUST include VerifiableCredential and a specific type identifier (e.g., CertifiedDeployment) for this dApp verification scheme.
- issuer:
MUST specify the Decentralized Identifier (DID) of the authorized VC issuer. Crucially, trust in the issuer is derived from their possession of the CERTIFIED_ROLE within the associated AppManifest contract. In practice, this issuer might be a transient, one-time wallet generated by a CI/CD process. The issuer MUST follow the format pkh:eip155:${Chain ID}$:${Account Address}.
- issuanceDate:
Specifies the date and time of VC issuance.
- expirationDate:
(Optional) Specifies when the VC expires.
- credentialSubject:
Contains key dApp information:

id:
MUST be the DID of the AppManifest contract, following the format pkh:eip155:${Chain ID}$:${Contract Address}.
- applicationURI:
MUST be the dApp’s root URL (e.g., https://example.dapp/). This claim is critical to establish an unambiguous link between the VC and the dApp’s web address.
- description:
(Optional) Provides a human-readable description of the dApp.

**`proof`:**

Contains a cryptographic proof validating the VC’s authenticity, signed by the `issuer`. The `type` **MUST** be `EcdsaSecp256k1VerificationKey2019`, and the `verificationMethod` **MUST** correspond to the issuer’s DID.

**Example `manifest.json`:**

```json
{
  "@context": [
    "[https://www.w3.org/2018/credentials/v1](https://www.w3.org/2018/credentials/v1)",
    "[https://www.w3.org/2018/credentials/examples/v1](https://www.w3.org/2018/credentials/examples/v1)"
  ],
  "id": "urn:uuid:c1fe902b-c9d9-4513-a296-58d2f29b4a9e",
  "type": ["VerifiableCredential", "CertifiedDeployment"],
  "issuer": "pkh:eip155:421614:0x3b98f3c6B1Ebb573CC5757E2E199F82D31b11422",
  "issuanceDate": "2025-03-09T22:09:36Z",
  "expirationDate": "2125-03-09T22:09:36Z",
  "credentialSubject": {
    "id": "pkh:eip155:421614:0x0aD4Ed6DE2fa0845424738f171a6d11Fd8E09cCA",
    "chainId": 421614,
    "applicationURI": "[https://app-manifest.3am.center/](https://app-manifest.3am.center/)",
    "description": "This credential proves that the deployer is a certified signer 0x3b98f3c6B1Ebb573CC5757E2E199F82D31b11422 who holds the CERTIFIED_ROLE in 0x0aD4Ed6DE2fa0845424738f171a6d11Fd8E09cCA. The field proof.signatureValue should be omitted when verifying the signature. The applicationURI must match the value returned by applicationURI() in the contract 0x0aD4Ed6DE2fa0845424738f171a6d11Fd8E09cCA."
  },
  "proof": {
    "type": "EcdsaSecp256k1VerificationKey2019",
    "created": "2025-03-09T22:09:36Z",
    "verificationMethod": "pkh:eip155:421614:0x3b98f3c6B1Ebb573CC5757E2E199F82D31b11422",
    "proofPurpose": "assertionMethod",
    "signatureValue": "0xcea1b97c5218ae78639195d07321894134440632e24596135ad4293c354699c210a6d219efee8492cfe4ef18834458de2fe12a0eef38a5fc3f998700580b717d1b"
  }
}
```

### 2. AppManifest Smart Contract

- Contract Address:
Each distinct dApp deployment SHOULD have a unique AppManifest contract address deployed on the target EIP-155 network to ensure unambiguous identification.
- Functionality:
The AppManifest contract MUST implement the following functions and role-based access controls:

 Roles:

CERTIFIED_ROLE: Granted to entities authorized to certify dApp deployments (e.g., CI/CD processes, security auditors).
- MANIFEST_ROLE: Granted by managed smart contracts to the AppManifest contract.
- UPGRADER_ROLE: (Optional) Granted to entities authorized to update some properties of the AppManifest contract.

**Constant Variables for Roles:**

- CERTIFIED_ROLE: bytes32 public constant CERTIFIED_ROLE = keccak256("AppManifest.CERTIFIED_ROLE");
- MANIFEST_ROLE: bytes32 public constant MANIFEST_ROLE = keccak256("AppManifest.MANIFEST_ROLE");

*Note: The `AppManifest.` prefix prevents collisions with roles in other contracts.*

**State Variables:**

- _applicationUri: Stores the dApp’s root URL. This value MUST exactly match the applicationURI claim in the manifest.json VC.
- _managedContractAddresses: A dynamically managed set of addresses representing the dApp’s managed contracts.

**Functions:**

- applicationURI() external view returns (string memory): Returns the stored applicationURI.
- setApplicationURI(string memory applicationUri_) external onlyRole(UPGRADER_ROLE): Updates the stored applicationURI. MUST emit an ApplicationURIUpdated event.
- addManagedContractAddresses(address[] memory addresses) external onlyRole(UPGRADER_ROLE): Adds new smart contract addresses to the managed set, emitting a ManagedContractAddressAdded event for each.
- removeManagedContractAddresses(address[] memory addresses) external onlyRole(UPGRADER_ROLE): Removes addresses from the managed set, emitting a ManagedContractAddressRemoved event for each.
- managedContractAddresses() external view returns (address[] memory): Returns an array of managed contract addresses. Critically, this function performs an on-chain check to ensure each returned address has been explicitly granted the MANIFEST_ROLE by the AppManifest contract.

### 3. Contract under Management

- Implementation Requirement:
Managed smart contracts MUST implement AccessControlEnumerable from OpenZeppelin Contracts or an equivalent role-based access control mechanism supporting enumerable roles.
- Role Requirement:
Managed smart contracts MUST grant the MANIFEST_ROLE to the AppManifest contract’s address. This explicit role assignment serves as an on-chain declaration that the contract is part of the dApp ecosystem managed by the AppManifest.

### 4. Verification Process: Ensuring dApp Authenticity and Contract Association

To verify dApp authenticity and its linked smart contracts, follow these steps:

1. Obtain Contract Address of Asset:
Retrieve the asset’s contract address via trusted channels.
2. Retrieve AppManifest Contract Addresses:
Use getRoleMember(bytes32 role, uint256 index) to enumerate addresses that have been granted the MANIFEST_ROLE (as granted by managed contracts).
3. Query dApp URI:
Call applicationURI() on the AppManifest contract to obtain the dApp’s root URL.
4. Fetch the Verifiable Credential (VC):
Retrieve manifest.json from the dApp’s root URL.
5. Verify the VC Signature & Issuer Authorization:

Signature Verification:
Cryptographically validate the VC’s digital signature using the issuer’s Ethereum address as specified in the proof section.
6. Issuer Authorization Check:
On-chain, verify that the VC issuer (from the issuer field) holds the CERTIFIED_ROLE in the AppManifest contract (as identified by credentialSubject.id).
7. Match applicationURI:
Ensure that the applicationURI claim in the VC exactly matches both the URL from which the VC was fetched and the value returned by applicationURI() on the AppManifest contract.
8. Confirm Managed Contract Association:
Validate that the managed contracts have explicitly granted the MANIFEST_ROLE to the AppManifest contract. This on-chain check confirms that the association between the dApp and its managed contracts is deliberate and verifiable.

## Rationale

- Verifiable Credentials: Standardized and Interoperable Security:
Using VCs provides a standardized, interoperable, and cryptographically secure method for verifying dApp deployments.
- manifest.json Placement: Simple Discoverability:
Hosting manifest.json at the dApp’s root directory simplifies discovery and verification.
- applicationURI Claim and Contract Variable: Cryptographic Linkage:
The inclusion of the applicationURI claim in both the VC and the AppManifest contract creates a verifiable link between the dApp’s web identity and its on-chain data.
- AppManifest Contract Roles: Flexible and Secure Access Control:
Role-based access control, particularly via the CERTIFIED_ROLE and the explicit granting of MANIFEST_ROLE, ensures that only authorized entities can certify and manage the dApp ecosystem.
- Managed Contract Association:
Requiring managed contracts to grant the MANIFEST_ROLE to the AppManifest contract provides clear on-chain evidence of association, enhancing security and transparency.

## Backwards Compatibility

This EIP is a new standard designed to enhance dApp security and transparency. It introduces no backwards compatibility issues with existing Ethereum protocols or standards. New dApps can adopt this standard from the outset, and existing dApps can integrate it incrementally without disruption.

## Security Considerations

- VC Issuer Authorization, Ephemeral Signers, and CI/CD Process Integrity:
The security model relies on verifying that the VC issuer holds the CERTIFIED_ROLE in the AppManifest contract. Ephemeral, one-time signing keys (often generated in CI/CD processes) minimize the risk of private key compromise. However, the CI/CD pipeline must be rigorously secured with strict access controls and continuous monitoring.
- DNS Integrity and Manifest Accessibility:
Since the VC (manifest.json) is hosted at the dApp’s root URL, ensuring the integrity of the DNS infrastructure is critical. Secure DNS configurations and regular audits are required to prevent hijacking or redirection attacks.
- Compromised Keys: Mitigated Impact and Swift Revocation:
While transient keys reduce risk, robust key management practices remain essential. On-chain role-based access controls allow for swift revocation in case of a compromise.
- AppManifest Contract Security:
The AppManifest contract must be developed, deployed, and maintained following the highest security standards, including regular independent audits.
- Front-running setApplicationURI:
Although protected by role-based access, front-running attacks on setApplicationURI remain a potential risk. Such attacks are mitigated by secure CI/CD practices and DNS integrity.
- VC Availability and Hosting Security:
Continuous availability and integrity of manifest.json are crucial. Developers must ensure that the VC is hosted securely and redundantly to maintain uninterrupted verification.

## Copyright Waiver

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).

## Replies

**MASDXI** (2025-03-10):

Have you checked this [ERC-7734: Decentralized Identity Verification (DID)](https://eips.ethereum.org/EIPS/eip-7734), and your work can potentially extending form this?

---

**yoheinishikubo** (2025-03-11):

Thanks for your question.

Actually, it’s not directly related to ERC-7734.

I guess some aspects of this spec *could* be implemented using ERC-7734, but we really wanted to keep things simple and stick to well-established, widely-used libraries like OpenZeppelin for this one.

