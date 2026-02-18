---
source: magicians
topic_id: 22692
title: Dynamic ERC1155 with Asset Creation and Swapping
author: 0x1codegod
date: "2025-01-28"
category: ERCs
tags: [token, evm, erc1155]
url: https://ethereum-magicians.org/t/dynamic-erc1155-with-asset-creation-and-swapping/22692
views: 53
likes: 1
posts_count: 2
---

# Dynamic ERC1155 with Asset Creation and Swapping

## Simple Summary

An extension to ERC1155 enabling dynamic token creation, token swapping, and metadata support.

## Abstract

This proposal enhances ERC1155 by enabling dynamic creation of new token types and direct token swapping, while maintaining compatibility with existing wallets and marketplaces. The changes aim to support dynamic game assets, modular digital collectibles, and flexible financial instruments, ensuring scalability and adaptability for multi-asset environments.

## Motivation

The need for dynamic token management in multi-asset environments is growing. Current standards lack mechanisms for creating new token types post-deployment and swapping tokens directly. This proposal addresses these gaps, enabling scalable use cases such as dynamic game assets, modular collectibles, and flexible DeFi instruments.

## Specification

### Contract

The `DynamicERC1155` contract is built on top of the ERC1155 standard. It introduces:

- Dynamic Asset Creation: Allows creating new token types during the contract lifecycle.
- Token Swapping: Facilitates direct exchange of one token type for another.
- Metadata URI Handling: Supports unique metadata URIs for each token.

### Methods

#### _createNewAsset(uint256 tokenId)

Allows the creation of a new token type.

- Parameters:

tokenId (uint256): The ID of the new token.

**Requirements:**

- Token ID must not already exist.

#### _exchange(uint256 fromTokenId, uint256 toTokenId, uint256 amountToBurn, uint256 amountToMint, bytes memory data)

Enables swapping of tokens by burning one type and minting another.

- Parameters:

fromTokenId (uint256): Token ID to burn.
- toTokenId (uint256): Token ID to mint.
- amountToBurn (uint256): Amount of fromTokenId to burn.
- amountToMint (uint256): Amount of toTokenId to mint.
- data (bytes): Additional data for minting.

**Requirements:**

- Both token IDs must exist.

#### mint(address account, uint256 id, uint256 amount, bytes memory data)

Mints a specified amount of a token to an account.

#### burn(address account, uint256 id, uint256 value)

Burns a specified amount of a token from an account.

#### uri(uint256 tokenId)

Generates a metadata URI for a token ID.

### Events

#### AssetCreated(uint256 tokenId)

Emitted when a new token is created.

#### AssetsSwapped(address user, uint256 fromTokenId, uint256 toTokenId, uint256 amountToBurn, uint256 amountToMint)

Emitted when tokens are swapped.

## Rationale

Dynamic asset creation and swapping are essential for scalable and modular blockchain applications. By adhering to ERC1155 standards, this proposal ensures compatibility with existing tools and platforms while introducing advanced functionalities. Events like `AssetCreated` and `AssetsSwapped` enhance off-chain indexing and analytics.

## Backwards Compatibility

This proposal is fully compatible with the ERC1155 standard. Existing wallets, marketplaces, and tools can interact with this contract seamlessly.

## Test Cases

### Dynamic Asset Creation for DeFi

1. Call _createNewAsset with a new tokenId.
2. Verify exists[tokenId] is true.
3. Verify AssetCreated event is emitted.

### Token Swapping in Gaming

1. Mint tokens for fromTokenId and toTokenId.
2. Call _exchange with valid parameters.
3. Verify balances are updated correctly.
4. Verify AssetsSwapped event is emitted.

## Implementation

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

import {ERC1155} from "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";

abstract contract DynamicERC1155 is ERC1155 {
    mapping(uint256 => bool) public exists;
    string public name;
    string public symbol;
    string private _uri;

    event AssetCreated(uint256 tokenId);
    event AssetsSwapped(
        address indexed user,
        uint256 indexed fromTokenId,
        uint256 indexed toTokenId,
        uint256 amountToBurn,
        uint256 amountToMint
    );

    constructor(string memory uri_, string memory name_, string memory symbol_) ERC1155(uri_) {
        _uri = uri_;
        name = name_;
        symbol = symbol_;
    }

    function _createNewAsset(uint256 tokenId) public virtual {
        require(!exists[tokenId], "Token ID already exists");
        exists[tokenId] = true;
        emit AssetCreated(tokenId);
    }

    function _exchange(
        uint256 fromTokenId,
        uint256 toTokenId,
        uint256 amountToBurn,
        uint256 amountToMint,
        bytes memory data
    ) public virtual {
        require(exists[fromTokenId] && exists[toTokenId], "Invalid token IDs");
        burn(msg.sender, fromTokenId, amountToBurn);
        mint(msg.sender, toTokenId, amountToMint, data);
        emit AssetsSwapped(msg.sender, fromTokenId, toTokenId, amountToBurn, amountToMint);
    }

    function mint(
        address account,
        uint256 id,
        uint256 amount,
        bytes memory data
    ) public virtual {
        _mint(account, id, amount, data);
    }

    function burn(
        address account,
        uint256 id,
        uint256 value
    ) public virtual {
        _burn(account, id, value);
    }

    function uri(uint256 tokenId) public view override returns (string memory) {
        return string(abi.encodePacked(_uri, Strings.toString(tokenId), ".json"));
    }
}
```

## Security Considerations

- Implement strict access control to prevent unauthorized minting, burning, or asset creation.
- Validate input parameters rigorously to avoid vulnerabilities like reentrancy or integer overflow.
- Ensure off-chain metadata remains accessible and consistent if _uri is updated.

## References

- ERC1155: Multi Token Standard
- OpenZeppelin Contracts Library

## Replies

**0x1codegod** (2025-01-28):

[@abcoathup](/u/abcoathup) check this out please.

