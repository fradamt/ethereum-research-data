---
source: magicians
topic_id: 22463
title: ERC-XXXX:Improved ERC3643 with EAS
author: auqib
date: "2025-01-09"
category: ERCs
tags: [token]
url: https://ethereum-magicians.org/t/erc-xxxx-improved-erc3643-with-eas/22463
views: 364
likes: 2
posts_count: 2
---

# ERC-XXXX:Improved ERC3643 with EAS

**Authors**

1.**Ricardo Santos**

[ricore77@hotmail.com](mailto:ricore77@hotmail.com)

VP Engineering,

Parfin London

2. **Dr. Auqib Hamid Lone**

[auqib92@gmail.com](mailto:auqib92@gmail.com)

Assistant Professor CSE,

GCET Kashmir, India

This whitepaper introduces a novel approach to enhance the ERC-3643 standard using Ethereum Attestation Services (EAS). By exploiting the features of EAS such as referenced attestations, delegated attestations**, and **off-chain attestations** the scalability and privacy are greatly improved while tokenizing RWAs using ERC3643, this paper outlines how ERC-3643 can achieve a more streamlined, flexible, and privacy-preserving compliance verification system. We also present specific use cases and include visual diagrams illustrating these features in action.

**Introduction**

ERC-3643 defines security tokens that represent real-world assets, facilitating regulatory-compliant transfers and ownership management. This paper demonstrates how these features can be used to streamline regulatory compliance for security tokens under ERC-3643. **EAS** provides a flexible attestation framework, incorporating features like off-chain attestations, delegated attestations, and referenced attestations, each of which enhances scalability, privacy, and efficiency. EAS is an open standard for structuring and signing arbitrary data with EVM wallets. It’s permissionless, open-source, and free to use. It’s used as an infrastructure tool by leading protocols and teams like Coinbase, Optimism, Scroll, Base, Arbitrum, and others. You can read more about EAS at https://attest.org.

**Core Concepts of Ethereum Attestation Services (EAS)**

- Schemas : Define the structure for attestations, providing interoperability.
- On-Chain vs. Off-Chain Attestations : Utilize on-chain attestations for immutability or off-chain attestations for cost efficiency.
- Privacy & Zero-Knowledge Proofs : Allow private compliance checks using ZKPs.
- Delegated Attestations : Attestations issued by third parties on behalf of users.
- Referenced Attestations : Allow bundling multiple attestations into one, reducing complexity.
- Resolver Contracts: Adds a resolver contract that acts as a hook for a schema. It ensures that attestations adhere to certain rules or conditions before they’re finalized.
- Revocation : Ability to revoke attestations when conditions change.
- Timestamping : To verify the time of issuance for attestations.

**Why Replace ONCHAINID with EAS?**

ONCHAINID’s limitations, such as limited interoperability, inflexible claim structures, lack of granular access control, reliance on centralized claim issuers, high gas costs, privacy concerns, and complex compliance management, make it less adaptable to evolving blockchain and regulatory landscapes. In contrast, EAS addresses these challenges by offering off-chain attestations to reduce gas costs, enhanced privacy through off-chain sensitive data verification, dynamic and scalable compliance rules, greater composability across DeFi platforms, and features like expiration, revocation, and historical evidence retention. This flexibility and interoperability enable EAS to provide a more efficient, adaptable, and cost-effective identity and compliance framework, making it a superior alternative to ONCHAINID for modern blockchain ecosystems.

**Table 1: Comparison of Existing OnchainID Approach and EAS-Based Replacement for ERC3643 Use Cases**

[![Table-ERCXXXX](https://ethereum-magicians.org/uploads/default/original/2X/7/754b75541147f271231623a6bc6860f21ad26440.png)Table-ERCXXXX625×793 29 KB](https://ethereum-magicians.org/uploads/default/754b75541147f271231623a6bc6860f21ad26440)

**Use Cases and Flow Diagrams**

**1. Use Case: Tokenized Real Estate with Referenced Attestations, Off-Chain Verification, and Delegated Attestation**

**Scenario** : A real estate token issuer wants to ensure that only eligible investors can purchase fractions of a property token. The compliance requirements include KYC, AML, and jurisdictional eligibility. To manage this, a referenced attestation is created, which combines multiple compliance checks into one bundled attestation. The attestation process involves a delegated entity (a KYC/AML provider) that issues attestations on behalf of investors, and all attestations are created off-chain to enhance privacy and reduce gas costs.

[![USECASE1](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b717e1b0a428c76e0011cd0e46b9201d9baf790c_2_690x456.png)USECASE11116×739 40.8 KB](https://ethereum-magicians.org/uploads/default/b717e1b0a428c76e0011cd0e46b9201d9baf790c)

**2. Use Case: Corporate Bonds and Delegated Attestations**

**Scenario** : Corporate bonds are tokenized and issued under the ERC-3643 standard, requiring investors to meet stringent compliance checks including jurisdictional rules, accredited investor status, and AML compliance. Delegated entities handle the compliance checks and issue attestations on behalf of investors. Each attestation is issued off-chain, allowing for scalability while ensuring privacy

[![USECASE2](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c35c5548447601e1e2f3ec673f164970bc679062_2_690x456.png)USECASE21116×739 43.1 KB](https://ethereum-magicians.org/uploads/default/c35c5548447601e1e2f3ec673f164970bc679062)

**3. Use Case: Seamless Access to Tokenized Real-World Assets (RWAs) via Regulated Bank Attestations**

This proposal utilizes a hierarchical attestation framework to provide secure, compliant, and scalable access to tokenized Real-World Assets (RWAs). The system combines attestations issued by regulated banks to users with referenced attestations issued by central banks to their regulated subsidiary banks. This approach ensures robust authentication and compliance across various jurisdictions. EAS features, particularly Referenced Attestations, enable ERCXXX to provide smooth and secure access to tokenized Real-World Assets (RWAs) through attestations from regulated banks. These attestations act as reusable credentials, ensuring users comply with regulatory frameworks such as KYC and AML . This approach not only protects user privacy but also facilitates cross-border participation in tokenized asset markets

[![USECASE3](https://ethereum-magicians.org/uploads/default/optimized/2X/0/0728c623626089ce380016d5a066001b2113c625_2_690x287.png)USECASE31600×667 105 KB](https://ethereum-magicians.org/uploads/default/0728c623626089ce380016d5a066001b2113c625)

**Solidity Code for ERC-XXXX and Attester Resolver Contracts**

Below is an example of how ERC-XXXX can be implemented with Ethereum Attestation Services (EAS) for compliance verification, including separate contracts for ERC-3643 and an Attester Resolver to validate an attestation.

1. ERC-XXXX Token Contract

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

interface IResolver {
    function validateAttestation(bytes32 attestationId) external view returns (bool);
}

contract ERCXXXX is ERC20, AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    event AttestationValidated(address sender, address recipient, uint256 amount);
    event AttestationValidationFailed(string reason);

    IResolver public resolver;
    mapping(address => bool) public frozen;

    uint256 public maxSupply;

    constructor(address resolverAddress) ERC20("ERCXXXXToken", "EXXXX") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(ADMIN_ROLE, msg.sender);

        // Initialize the resolver
        resolver = IResolver(resolverAddress);

        // Set the maximum supply and mint tokens
        maxSupply = 10_000_000_000_000_000;
        _mint(msg.sender, maxSupply);
    }

    function freezeAccount(address account) external onlyRole(ADMIN_ROLE) {
        frozen[account] = true;
    }

    function unfreezeAccount(address account) external onlyRole(ADMIN_ROLE) {
        frozen[account] = false;
    }

    // Function to transfer tokens with attestation checks
    function easTransfer(address recipient, uint256 amount, bytes32 attestationId) public returns (bool) {
        require(!frozen[msg.sender], "Sender account is frozen");
        require(!frozen[recipient], "Recipient account is frozen");
        require(attestationId != bytes32(0), "No attestation ID provided");

        // Delegate attestation validation to the Resolver contract
        bool isValid = resolver.validateAttestation(attestationId);
        require(isValid, "Attestation validation failed");

        emit AttestationValidated(msg.sender, recipient, amount);
         bool successTransfer = super.transfer(recipient, amount);

    return successTransfer;
    }
}

```

1. Attester Resolver Contract
The Attester Resolver contract is responsible for validating attestations for a given transfer. It ensures that each attestation is valid and all necessary checks are satisfied

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "hardhat/console.sol";

interface IEAS {
    struct Attestation {
        bytes32 uid;
        bytes32 schema;
        uint64 time;
        uint64 expirationTime;
        uint64 revocationTime;
        bytes32 refUID;
        address recipient;
        address attester;
        bool revocable;
        bytes data;
    }

    function getAttestation(bytes32 uid) external view returns (Attestation memory);
}

contract OurResolver {
    IEAS public eas;

    struct SuitabilityData {
        address IssuedBy;
        bool AmlCompliant;
        string CountryOfResidency;
        uint8 SuitabilityRiskScore;
        uint64 ExpiryDate;
    }

    constructor(address easAddress) {
        eas = IEAS(easAddress);
    }

    // Function to fetch and decode attestation data
    function getDecodedAttestationData(bytes32 attestationId)
        public
        view
        returns (
            address IssuedBy,
            bool AmlCompliant,
            string memory CountryOfResidency,
            uint8 SuitabilityRiskScore,
            uint64 ExpiryDate
        )
    {
        // Fetch the attestation struct from EAS
        IEAS.Attestation memory attestation = eas.getAttestation(attestationId);

        require(attestation.data.length > 0, "Attestation data is empty");

        console.log("Fetched attestation data:");
        console.logBytes(attestation.data);

        // Decode the attestation data using the expected structure
        (IssuedBy, AmlCompliant, CountryOfResidency, SuitabilityRiskScore, ExpiryDate) = abi.decode(
            attestation.data,
            (address, bool, string, uint8, uint64)
        );

        // Log the decoded data for debugging
        console.log("Decoded Data:");
        console.log("IssuedBy:", IssuedBy);
        console.log("AmlCompliant:", AmlCompliant);
        console.log("CountryOfResidency:", CountryOfResidency);
        console.log("SuitabilityRiskScore:", SuitabilityRiskScore);
        console.log("ExpiryDate:", ExpiryDate);

        return (IssuedBy, AmlCompliant, CountryOfResidency, SuitabilityRiskScore, ExpiryDate);
    }

    // Function to validate an attestation based on certain criteria
    function validateAttestation(bytes32 attestationId) public view returns (bool) {
        // Fetch the attestation struct from EAS
        IEAS.Attestation memory attestation = eas.getAttestation(attestationId);

        require(attestation.data.length > 0, "No attestation data found");

        // Decode the data from the attestation payload
        (
            address IssuedBy,
            bool AmlCompliant,
            string memory CountryOfResidency,
            uint8 SuitabilityRiskScore,
            uint64 ExpiryDate
        ) = abi.decode(attestation.data, (address, bool, string, uint8, uint64));

        // Log the decoded data for debugging
        console.log("Decoded Data:");
        console.log("IssuedBy:", IssuedBy);
        console.log("AmlCompliant:", AmlCompliant);
        console.log("CountryOfResidency:", CountryOfResidency);
        console.log("SuitabilityRiskScore:", SuitabilityRiskScore);
        console.log("ExpiryDate:", ExpiryDate);

        // Perform validation checks
        require(
            keccak256(bytes(CountryOfResidency)) == keccak256(bytes("UK")),
            "Investor Not From UK"
        );
        require(AmlCompliant, "AML not compliant");
        require(block.timestamp = 7, "Insufficient suitability score");

        return true;
    }
}

```

**Conclusion**

By integrating **Ethereum Attestation Services (EAS)** with **referenced attestations**, **off-chain attestations**, and **Attester Resolvers** into the ERC-XXXX framework, we present a more efficient, scalable, and privacy-preserving solution for managing security tokens. Bundling multiple compliance attestations into a single reference reduces operational complexity and improves transaction flows. This approach is precious for tokenized real estate, corporate bonds, and cross-jurisdictional securities, offering a robust solution for managing compliance and regulatory requirements in a decentralized environment. This whitepaper highlights how **EAS** can revolutionize ERC- XXXX by utilizing its core features to address modern compliance challenges effectively. This would provide the blockchain ecosystem with a next-generation, efficient, and privacy-focused security token framework.

## Replies

**Atenika.Protocol** (2025-01-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/auqib/48/14200_2.png) auqib:

> ERC-3643 extending with Ethereum Attestation Services

Isn’t that alredy done maybe not us EIP / ERC but somer  services ?

wolfcraig they tried that with whisky

onchain Atest is as strong as community/or organization behind it, and every act of onchain attestation need some law framework to attach to it. As it is no longer anonymous or semi anonymous / decentralized.

I think that bridges and layer 2 is good cost effective reduction already .

, but this privacy issue is addressed in few upcoming ERCs and proposals, as “enhanced privacy through off-chain sensitive data verification,” is nice to have feature

