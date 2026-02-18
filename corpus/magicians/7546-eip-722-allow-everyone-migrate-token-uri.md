---
source: magicians
topic_id: 7546
title: "[EIP-722] Allow everyone migrate token URI"
author: tvd12
date: "2021-11-23"
category: EIPs
tags: [nft, token, metadata]
url: https://ethereum-magicians.org/t/eip-722-allow-everyone-migrate-token-uri/7546
views: 1300
likes: 2
posts_count: 6
---

# [EIP-722] Allow everyone migrate token URI

### Introduction

Hi, I see almost NFT applications are using ERC721, so after the NFT start-up trend, there will be many companies that run out of capital and dissolve. At that time they will shutdown their servers and many of the images associated with the NFT will be inaccessible.  Should we need create a contract that allows the holder to update the image URI.

### Contract Interface

```solidity
// SPDX-License-Identifier: MIT
// From: youngmonkeys.org

pragma solidity ^0.8.0;

/**
 * @dev Required interface of an ERC722 compliant contract.
 * After the NFT start-up trend, there will be many companies that run out of capital and dissolve.
 * At that time they will shut down their servers and many of the images associated with the NFT will be inaccessible.
 * Should we create a token that allows the holder to update the image URI
 */
interface IERC722 {

    /**
    * Get the owner of the tokens
    */
    function tokensOwner() external view returns (address);

    /**
    * Get the contract created the tokens
    */
    function tokensContract() external view returns (address);

    /**
    * Get the lastest URI of the `tokenId`
    * Requirements:
    *
    * - `tokenId` must exist.
    */
    function latestTokenURI(
        uint256 tokenId
    ) external view returns (string memory);

    /**
    * Set the lastest URI of the `tokenId`
    * Requirements:
    *
    * - `tokenId` must exist.
    * - `tokenURI` must exist.
    */
    function setLatestTokenURI(
        uint256 tokenId,
        string memory tokenURI
    ) external;

    /**
    * Set the lastest URI of the `tokenId`
    * Requirements:
    *
    * - `submitter` must exist.
    * - `tokenId` must exist.
    * - `tokenURI` must exist.
    */
    function safeSetLatestTokenURI(
        address submitter,
        uint256 tokenId,
        string memory tokenURI
    ) external;
}
```

### Implementation

```solidity
// SPDX-License-Identifier: MIT
// From: youngmonkeys.org

pragma solidity ^0.8.0;

import "./IERC722.sol";

/**
 * @dev Implementation of https://eips.ethereum.org/EIPS/eip-721[ERC722] Replace URI of Non-Fungible Tokens
 */
contract ERC722 is IERC722 {

    // Owner of the tokens
    address private _tokensOwner;

    // Contract of the tokens
    address private _tokensContract;

    // Mapping from token ID to an URI
    mapping(uint256 => string) private _latestTokenURIs;

    /**
     * @dev Initializes the contract by setting a `tokensOwner` and a `tokensContract`
     */
    constructor(address tokensOwner, address tokensContract) {
        _tokensOwner = tokensOwner_;
        _tokensContract = tokensContract_;
    }

    /**
     * @dev See {IERC721-ownerOf}.
     */
    function tokensOwner() public view override returns (address) {
        return _tokensOwner;
    }

    /**
     * @dev See {IERC721-ownerOf}.
     */
    function tokensContract() public view override returns (address) {
        return _tokensContract;
    }

    /**
     * @dev See {IERC721-latestTokenURI}.
     */
    function latestTokenURI(
        uint256 tokenId
    ) public view override returns (string memory) {
        return _latestTokenURIs[tokenId];
    }

    /**
     * @dev See {IERC721-setLatestTokenURI}.
     */
    function setLatestTokenURI(
        uint256 tokenId,
        string memory tokenURI
    ) public override {
        require(_isTokenOwner(msg.sender), "You are not the token's owner.");
        _latestTokenURIs[tokenId] = tokenURI;
    }

    /**
     * @dev See {IERC721-safeSetLatestTokenURI}.
     */
    function safeSetLatestTokenURI(
        address submitter,
        uint256 tokenId,
        string memory tokenURI
    ) public override {
        require(_isTokenOwner(submitter), "Submitter are not the token's owner.");
        _latestTokenURIs[tokenId] = tokenURI;
    }

    function _isTokenOwner(address sender) internal view virtual returns (bool) {
        return _tokensOwner == sender_;
    }
}
```

## Replies

**anett** (2021-11-23):

Companies that stores NFT Metadata like IPFS and Arweave have big potential in keep running their servers especially Arweave with it’s token incentivising model for miners.

In order to create smart contact cheaper, as developer you should consider making the contract as efficient as possible. Also you want to prevent blockchain state bloat and make minting as cheap as possible which by uploading whole NFT metadata - picture is impossible and transaction would be extremely expensive.

---

**tvd12** (2021-11-23):

1. I think not everyone knows about IPFS, because there are a lot of start-ups born just for the purpose of earn money from users, then they will dissolve
2. In this situation, we will not store asset data to blockchain, I just want store tokenURI to the blockchain, example:

I have a token:

```json
{
  "contract": "contract_abc",
  "tokenId" : "1234",
  "owner"  : "address_abc",
 "tokenURI" : "https://gameabc.com/nft/ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
}
```

Now I’m hear the game publisher will dissolve, so I will download the image to my server and create an `IERC722` contract and point the token `1234` to the new url: `https://myserver.com/nft/ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad`

---

**poma** (2021-11-24):

And what we are supposed to do when someone buys a cheapest crypto punk and replaces its image URI to the rarest crypto punk? Also think about all the scam/phishing possibilities this opens.

---

**abcoathup** (2021-11-24):

Please note:

EIP numbers are generally the PR number or, if preferred by the author, the Issue # if there was discussion in the Issues section of the EIP repository about the EIP

https://eips.ethereum.org/EIPS/eip-1#eip-editor-responsibilities

---

**tvd12** (2021-11-24):

[@abcoathup](/u/abcoathup) thank for your comment, It’s first time I create a ticket, I’m reading the first PR

