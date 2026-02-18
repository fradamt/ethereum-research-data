---
source: magicians
topic_id: 19027
title: "ERC-7646: Metadata Management for NFTs"
author: Kureev
date: "2024-03-03"
category: ERCs
tags: [erc, nft, erc-721, metadata]
url: https://ethereum-magicians.org/t/erc-7646-metadata-management-for-nfts/19027
views: 1055
likes: 2
posts_count: 3
---

# ERC-7646: Metadata Management for NFTs

Hi Magicians,

I’d like to propose an approach to manage metadata for NFTs (by the owner and authorized parties). In many cases (provenance tracking, game assets etc) it would be beneficial to be able to update metadata for existing NFT. I believe it will open door to many interesting applications related to dynamic nature of underlying NFT (IP, real estate, supply chains etc).

Here is the PR: [Add ERC: Metadata Management for NFTs by Kureev · Pull Request #293 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/293)

And here is the copy of the idea:

### Simple Summary

This ERC proposes a standard for managing metadata of NFTs that allows owners and authorized addresses to update the metadata of their tokens.

### Abstract

The MetadataManager contract provides a mapping for storing metadata of NFTs. It also provides a mechanism for authorizing other addresses to update the metadata of a token. This contract can be used in conjunction with any NFT contract that implements the ERC721 or ERC1155 standard.

### Motivation

Currently, the metadata of an NFT is immutable once it has been minted. This is problematic for use cases where the metadata of an NFT needs to be updated afterwards. For example, an NFT representing a digital artwork might need to have its metadata updated to reflect changes in the artwork’s ownership or provenance.

### Specification

The MetadataManager contract provides the following functions:

- updateMetadata(address tokenAddress, uint256 tokenId, string memory newURI): Updates the metadata of a token. The sender must be the owner of the token or authorized to update the metadata.
- getMetadata(address tokenAddress, uint256 tokenId): Returns the metadata of a token. If the metadata is not stored, it will try to fetch it from the NFT contract.
- authorize(address tokenAddress, uint256 tokenId, address authorizedAddress): Authorizes an address to update the metadata of a token. Only the owner of the token can call this function.
- revokeAuthorization(address tokenAddress, uint256 tokenId, address authorizedAddress): Revokes the authorization of an address to update the metadata of a token. Only the owner of the token can call this function.

### Rationale

This ERC provides a flexible and decentralized way to manage the metadata of NFTs. It allows the metadata of an NFT to be updated after it has been minted, and it allows the owner of an NFT to delegate the ability to update the metadata to other addresses.

### Backwards Compatibility

This ERC is fully backwards compatible with existing NFT standards. It can be used in conjunction with any NFT contract that implements the ERC721 or ERC1155 standard.

### Test Cases

TBD

### Implementation

```jsx
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

interface INFT {
    function ownerOf(uint256 tokenId) external view returns (address owner);
    function tokenURI(uint256 tokenId) external view returns (string memory);
}

contract MetadataManager {
    // tokenAddress => tokenId => URI of the metadata
    mapping(address => mapping(uint256 => string)) public tokenMetadata;

    // tokenAddress => tokenId => authorizedAddress => bool
    mapping(address => mapping(uint256 => mapping(address => bool))) public isAuthorized;

    // Emits when the metadata of a token is updated.
    event MetadataUpdated(address indexed tokenAddress, uint256 indexed tokenId, string newUri);

    // Emits when an address is authorized to update the metadata of a token.
    event AuthorizationGranted(address indexed tokenAddress, uint256 indexed tokenId, address indexed authorizedAddress);

    // Emits when an address is revoked from updating the metadata of a token.
    event AuthorizationRevoked(address indexed tokenAddress, uint256 indexed tokenId, address indexed authorizedAddress);

    // Throws if the sender is not the owner of the token.
    modifier onlyTokenOwner(address tokenAddress, uint256 tokenId) {
        INFT nftContract = INFT(tokenAddress);
        if (msg.sender != nftContract.ownerOf(tokenId)) {
            revert NotOwner();
        }
        _;
    }

    /**
     * Updates the metadata of a token.
     * The sender must be the owner of the token or authorized to update the metadata.
     * Emits a {MetadataUpdated} event.
     */
    function updateMetadata(address tokenAddress, uint256 tokenId, string memory newURI) public {
        INFT nftContract = INFT(tokenAddress);

        if (msg.sender != nftContract.ownerOf(tokenId) || !isAuthorized[tokenAddress][tokenId][msg.sender]) {
            revert NotAuthorized();
        }

        tokenMetadata[tokenAddress][tokenId] = newURI;
        emit MetadataUpdated(tokenAddress, tokenId, newURI);
    }

    /**
     * Returns the metadata of a token.
     * If the metadata is not stored, it will try to fetch it from the NFT contract.
     * If the NFT contract does not have a tokenURI function, it will revert.
     */
    function getMetadata(address tokenAddress, uint256 tokenId) public view returns (string memory) {
        string memory metadata = tokenMetadata[tokenAddress][tokenId];

        if (bytes(metadata).length == 0) {
            try INFT(tokenAddress).tokenURI(tokenId) returns (string memory uri) {
                return uri;
            } catch {
                revert NoMetadata();
            }
        } else {
            return metadata;
        }
    }

    // Authorizes an address to update the metadata of a token.
    function authorize(address tokenAddress, uint256 tokenId, address authorizedAddress) public onlyTokenOwner(tokenAddress, tokenId) {
        isAuthorized[tokenAddress][tokenId][authorizedAddress] = true;
        emit AuthorizationGranted(tokenAddress, tokenId, authorizedAddress);
    }

    // Revokes the authorization of an address to update the metadata of a token.
    function revokeAuthorization(address tokenAddress, uint256 tokenId, address authorizedAddress) public onlyTokenOwner(tokenAddress, tokenId) {
        isAuthorized[tokenAddress][tokenId][authorizedAddress] = false;
        emit AuthorizationRevoked(tokenAddress, tokenId, authorizedAddress);
    }

    error NotAuthorized();
    error NotOwner();
    error NoMetadata();
}
```

### Example usage

```jsx
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./MetadataManager.sol";

contract MyNFT is ERC721 {
    MetadataManager public metadataManager;

    constructor(address _metadataManager) ERC721("MyNFT", "MNFT") {
        metadataManager = MetadataManager(_metadataManager);
    }

    error NotOwner();

    modifier onlyOwner(uint256 tokenId) {
        if (ownerOf(tokenId) != msg.sender) {
            revert NotOwner();
        }
        _;
    }

    function mint(address to, uint256 tokenId) public {
        _mint(to, tokenId);
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        return metadataManager.getMetadata(address(this), tokenId);
    }

    function updateMetadata(uint256 tokenId, string memory newURI) public onlyOwner(tokenId) {
        metadataManager.updateMetadata(address(this), tokenId, newURI);
    }

    function authorize(address authorizedAddress, uint256 tokenId) public onlyOwner(tokenId) {
        metadataManager.authorize(address(this), tokenId, authorizedAddress);
    }

    function revokeAuthorization(address authorizedAddress, uint256 tokenId) public onlyOwner(tokenId) {
        metadataManager.revokeAuthorization(address(this), tokenId, authorizedAddress);
    }
}
```

### Security Considerations

The MetadataManager contract relies on the `ownerOf` function of the NFT contract to determine the owner of a token. If the NFT contract does not implement this function correctly, it could lead to security issues.

## Replies

**sullof** (2024-03-18):

In the ERC721 ecosystem there is no restriction blocking metadata from changing. For example, it is quite common to change them when there is an after sale reveal.

Did you see [ERC-4906: EIP-721 Metadata Update Extension](https://eips.ethereum.org/EIPS/eip-4906) ?

---

**Kureev** (2024-03-18):

![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12)! Thanks for the feedback! I haven’t seen EIP-4906 beforehand, but it seems that it relies on overriding tokenURI which might be suboptimal if it is important to keep history of the metadata changes. Of course, you can keep a link to the previous metadata within the new metadata file (basically, a linked list), but since storing data off chain might not be 100% reliable, storing references/history on the smart contract side seems more reliable (even if  historical metadata is not fully available, you can still guarantee partial integrity of the system).

However, I think it will be beneficial to add EIP-4906 events to this proposal so it will be fully compatible with the established standard ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

