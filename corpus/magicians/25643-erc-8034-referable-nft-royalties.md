---
source: magicians
topic_id: 25643
title: "ERC-8034: Referable NFT Royalties"
author: richard620
date: "2025-10-02"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-8034-referable-nft-royalties/25643
views: 51
likes: 0
posts_count: 1
---

# ERC-8034: Referable NFT Royalties

## Abstract

This ERC proposes Royalty Distribution, a standalone royalty distribution for Referable Non-Fungible Tokens (rNFTs). It enables royalty distribution to multiple recipients at the primary level and referenced NFTs in the directed acyclic graph (DAG), with a single depth limit to control propagation. The standard is independent of ERC-2981 and token-standard-agnostic, but expects ERC-5521 rNFTs, which in practice build on ERC-721 ownership semantics. It includes a function to query fixed royalty amounts (in basis points) for transparency. Royalties are voluntary, transparent, and configurable on-chain, supporting collaborative ecosystems and fair compensation.

## Motivation

ERC-5521 introduces Referable NFTs (rNFTs), which form a DAG through “referring” and “referred” relationships. Existing royalty standards like ERC-2981 do not account for this structure or support multiple recipients per level. This EIP addresses the need for a royalty mechanism that:

- Supports multiple recipients per royalty level (e.g., creators and collaborators).
- Distributes royalties to referenced NFTs in the DAG.
- Limits royalty propagation with a single reference depth.
- Provides a function to query fixed royalty amounts without a sale price.
- Provides a function to query fixed royalty amounts with a sale price.
- Operates independently of ERC-721 or ERC-2981.
- Ensures transparency for marketplaces and users.
- Is discoverable via ERC-165 supportsInterface.
- Supports optional EIP-712 signature-based configuration to streamline marketplace or owner-driven updates.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

### Interface

The IRNFTRoyalty interface defines the royalty distribution for rNFTs and MUST inherit IERC165 so that supporting contracts can advertise compliance via ERC-165:

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

interface IRNFTRoyalty is IERC165 {
    struct RoyaltyInfo {
        address recipient; // Address to receive royalty
        uint256 royaltyAmount; // Royalty amount (in wei for sale-based queries, basis points for fixed queries)
    }

    struct ReferenceRoyalty {
        RoyaltyInfo[] royaltyInfos; // Array of recipients and their royalty amounts
        uint256 referenceDepth; // Maximum depth in the reference DAG for royalty distribution
    }

    event ReferenceRoyaltiesPaid(
        address indexed rNFTContract,
        uint256 indexed tokenId,
        address indexed buyer,
        address marketplace,
        ReferenceRoyalty royalties
    );

    function getReferenceRoyaltyInfo(
        address rNFTContract,
        uint256 tokenId,
        uint256 salePrice
    ) external view returns (ReferenceRoyalty memory royalties);

    function getReferenceRoyaltyInfo(
        address rNFTContract,
        uint256 tokenId
    ) external view returns (ReferenceRoyalty memory royalties);

    function setReferenceRoyalty(
        address rNFTContract,
        uint256 tokenId,
        address[] memory recipients,
        uint256[] memory royaltyFractions,
        uint256 referenceDepth
    ) external;

    function setReferenceRoyalty(
        address rNFTContract,
        uint256 tokenId,
        address[] memory recipients,
        uint256[] memory royaltyFractions,
        uint256 referenceDepth,
        address signer,
        uint256 deadline,
        bytes calldata signature
    ) external;

    function supportsReferenceRoyalties() external view returns (bool);

    function royaltyNonce(address signer, address rNFTContract, uint256 tokenId) external view returns (uint256);
}
```

### ERC-165 requirement.

- Implementations MUST return true for supportsInterface(type(IRNFTRoyalty).interfaceId).
- Additional interfaces (e.g., AccessControl) SHOULD be forwarded via super.supportsInterface(interfaceId) when using inheritance.

### Signature-Based Configuration

To support gas-efficient and flexible configuration, implementations MUST support the following semantics for the signature overload:

- Authorization: The recovered EIP-712 signer MUST satisfy one of:

Has CONFIGURATOR_ROLE, or
- Is IERC5521(rNFTContract).ownerOf(tokenId) at verification time.
- Anti-replay: The message MUST include a nonce; the contract MUST track, verify, and increment a nonce to prevent replay.
- Typed Data: Use EIP-712 domain and struct as below (reference implementation provided).
- Deadline MUST be compared against block.timestamp; signatures with block.timestamp > deadline MUST be rejected.

Recommended EIP-712 Domain

- name = “RNFTRoyalty”, version = “2”, chainId, verifyingContract = address(this)

Recommended Typed Struct

```auto
SetReferenceRoyalty(
  address rNFTContract,
  uint256 tokenId,
  bytes32 recipientsHash,        // keccak256(abi.encode(recipients))
  bytes32 royaltyFractionsHash,  // keccak256(abi.encode(royaltyFractions))
  uint256 referenceDepth,
  address signer,
  uint256 deadline,
  uint256 nonce
)
```

### Key Components

#### Structs

- RoyaltyInfo:

recipient: The address to receive the royalty payment.
- royaltyAmount: The royalty amount, in wei for getReferenceRoyaltyInfo with salePrice, or basis points (e.g., 100 = 1%) for getReferenceRoyaltyInfo without salePrice.

ReferenceRoyalty:

- royaltyInfos: An array of RoyaltyInfo for multiple recipients at the primary level and referenced NFTs.
- referenceDepth: A single value limiting royalty distribution to referenced NFTs in the DAG.

#### Functions

- getReferenceRoyaltyInfo(address rNFTContract, uint256 tokenId, uint256 salePrice):

Returns a ReferenceRoyalty struct with royalty amounts in wei, calculated from the salePrice.
- Includes primary-level royalties and referenced NFT royalties up to referenceDepth.
- MUST return zero amounts if no royalties are configured or if salePrice is zero.

getReferenceRoyaltyInfo(address rNFTContract, uint256 tokenId):

- Returns a ReferenceRoyalty struct with fixed royalty amounts in basis points (e.g., 100 = 1%).
- Includes primary-level royalties and referenced NFT royalties up to referenceDepth.
- MUST return the configured royalty fractions without sale price calculations.

setReferenceRoyalty(address rNFTContract, uint256 tokenId, address recipients, uint256 royaltyFractions, uint256 referenceDepth):

- Configures royalties for the specified rNFT.
- recipients and royaltyFractions (in basis points) define primary-level royalties.
- referenceDepth limits royalty distribution to referenced NFTs.
- MUST be restricted to authorized parties (e.g., rNFT contract owner).
- MUST enforce a total primary-level royalty cap of ≤ 1000 basis points (10%).

setReferenceRoyalty(address rNFTContract, uint256 tokenId, address recipients, uint256 royaltyFractions, uint256 referenceDepth, address signer, uint256 deadline, bytes signature):

- Signature-based configuration per EIP-712.
- MUST verify signer authorization, nonce, and enforce deadline to reject expired signatures.
- The signer parameter specifies which address is expected to have signed the message, enabling relayer execution.

supportsReferenceRoyalties():

- Returns true if the contract implements this standard. Discovery MUST rely on ERC-165.

royaltyNonce(…):

- Returns the current nonce used for EIP-712 signatures.

#### Events

- ReferenceRoyaltiesPaid: Emitted when royalties are paid, logging the rNFT contract, token ID, buyer, marketplace, and ReferenceRoyalty details (with royaltyAmount in wei).

### Royalty Distribution Model

- Primary Royalties: The rNFT’s royaltyInfos array specifies multiple recipients and their fractions (e.g., 5% total, split as 3% and 2%).
- Reference Royalties: At each hop, a total forwarded share equal to REFERRED_ROYALTY_FRACTION (e.g., 200 bps / 2%) is carved out and distributed across all referenced NFTs at that depth proportional to their configured weights (fallback: evenly if all weights are zero).
- Total Royalty Cap (Primary Level): The 10% (1000 bps) cap applies to the primary-level configured royaltyFractions. Propagated/reference-level flows are governed separately by REFERRED_ROYALTY_FRACTION and referenceDepth.
- Depth Limit: Implementations MUST cap referenceDepth; this reference implementation enforces

getReferenceRoyaltyInfo(0xABC, 1):

- Returns:
 { royaltyInfos: [ {recipient: creator, royaltyAmount: 300}, {recipient: collaborator, royaltyAmount: 200}, {recipient: tokenA_owner, royaltyAmount: 100}, {recipient: tokenB_owner, royaltyAmount: 100} ], referenceDepth: 2 }.

Sale for 100 ETH:

- getReferenceRoyaltyInfo(0xABC, 1, 100 ether) returns:
 { royaltyInfos: [ {recipient: creator, royaltyAmount: 3 ether}, {recipient: collaborator, royaltyAmount: 2 ether}, {recipient: tokenA_owner, royaltyAmount: 1 ether}, {recipient: tokenB_owner, royaltyAmount: 1 ether} ], referenceDepth: 2 }.

## Rationale

- Fixed Royalty Query: The new getReferenceRoyaltyInfo function without salePrice allows users to inspect fixed royalty fractions (in basis points), improving transparency.
- Multiple Recipients: The RoyaltyInfo array supports collaborative projects.
- Single Depth Limit: Simplifies configuration and reduces gas costs.
- Standalone Design: Ensures compatibility with any ERC-5521 contract.
- Voluntary Royalties: Aligns with marketplace practices.
- Transparency: On-chain storage and fixed-amount queries enable verifiable royalties.
- ERC-165 Discoverability: Marketplaces and wallets can reliably detect support via supportsInterface, avoiding ad-hoc feature flags.
- EIP-712 Signatures: Off-chain approvals enable safe, gas-efficient configurations.

[Add ERC: Royalty Standard for Referable NFTs](https://github.com/ethereum/ERCs/pull/1227)
