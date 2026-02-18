---
source: magicians
topic_id: 21185
title: "ERC-XXXX: Dimensional Token Standard (DTS)"
author: aekiro
date: "2024-09-25"
category: ERCs
tags: [erc, nft, token, wallet, erc-721]
url: https://ethereum-magicians.org/t/erc-xxxx-dimensional-token-standard-dts/21185
views: 1792
likes: 3
posts_count: 2
---

# ERC-XXXX: Dimensional Token Standard (DTS)

ERC: 4D

Author: ækiro

Type: Standards Track

Category: ERC

Status: Draft

Created: 2024-09-24

Requires: 20, 721, 1155, 6551, 404

---

## Abstract

ERC-4D introduces dimensional tokens that combine ERC-20 and ERC-6551, creating tokens that function both as tradable assets and wallets. Each token holds assets within its account, enabling multi-layered assets, recursive token structures, and cyclic ownership. This standard adds liquidity to various asset classes while providing advanced management capabilities.

## Motivation

Current token standards like ERC-20 and ERC-721 have paved the way for diverse use cases in the blockchain space, but they operate independently with limited interaction. As decentralized applications evolve, we need a token standard that can handle more complex scenarios. ERC-4D introduces a multi-dimensional approach, merging fungible and non-fungible behaviors. This enables each ERC-4D token to function both as a tradable asset and as a multi-layered asset container. It unlocks new possibilities for asset management, liquidity, and innovative financial instruments.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

1. Dual-Root Structure: Each ERC-4D token has both an ERC-20 root and an ERC-6551 root.

ERC-20 Root: Enables traditional fungible token behavior.
2. ERC-6551 Root: ERC-721 NFT serving as a wallet with its own token account.
3. Multi-Layered Assets (Dimensions): ERC-4D can hold other assets, including
other tokens, NFTs, or even more ERC-4D tokens.
4. Cyclical Ownership: The ERC-6551 token account is designed to own the original ERC-20 token that created it. This creates a loop in ownership, adding complexity and novel functionalities to the token’s behavior.
5. Deque Architecture: The ERC-6551 root allows double-ended queue operations, enabling flexible asset management through both LIFO and FIFO approaches.

Some core functionalities can be defined as follows:

```auto
// Creates an account of a specific NFT. If the account exists, returns the address
function createAccount(address implementation, bytes32 salt, uint256 chainId, address tokenContract, uint256 tokenId) external onlyOwner returns (address)

// Excludes an account from the ownership of NFTs. If the account possesses NFTs they are sent to the contract
function setERC721TransferExempt(address account, bool value) external onlyOwner

// Withdraws an NFT from addresses whose balance drops below the threshold
function withdrawAndStoreERC721(address from) internal virtual

// Mints an NFT to addresses whose balance exceeds a predefined threshold
function retrieveOrMintERC721(address to) internal virtual
```

## Rationale

By combining the capabilities of ERC-20 and ERC-6551, ERC-4D creates a new standard that facilitates more complex asset interactions, addressing the limitations of existing token models in managing nested or recursive assets.

## Applications

Including, but not limited to:

1. Multi-layered Asset Management: Recursive ownership of assets, enabling advanced portfolio or index tokenization.
2. Liquid Wallets: Tradable wallets containing multiple assets.
3. RWA Tokenization: Real-world asset tokenization for easier trade and management.
4. On-Chain Artifacts: Can be utilized to hold digital data or on-chain artifacts such as intellectual property or historical data.
5. Security Protocols: Self-owning tokens introduce automated governance mechanisms.

## Backward Compatibility

ERC-4D remains fully compatible with existing ERC-20 and ERC-721 standards.

---

> This spec is a WIP and will be updated as implementation progresses.

## Replies

**abcoathup** (2024-09-29):

Please note, ERC numbers are manually assigned by ERC editors & associates, you don’t get to pick your own.

Also there is no ERC numbered 404.

