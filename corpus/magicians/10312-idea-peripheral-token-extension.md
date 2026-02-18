---
source: magicians
topic_id: 10312
title: "IDEA: Peripheral Token Extension"
author: mshuaic
date: "2022-08-10"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/idea-peripheral-token-extension/10312
views: 589
likes: 0
posts_count: 1
---

# IDEA: Peripheral Token Extension

## Abstract

The extension allows an ERC-721 token *Y* to be attached to another ERC-721 token *X*. The peripheral token *Y* has two states: `attached` and `detached`. *Y* is **only** transferable and free to attach to any token when `detached`. In a nested attachment (*Z* → *Y* → *X*),  only *X*’s owner can set *Y* and *Z* to `detached`.

## Motivation

This EIP introduces a new tokenomics hierarchy, a unidirectional relationship from a peripheral token *Z* to an intermediate host/peripheral token *Y* to a root host token *X*. The simplified unidirectional relationship opens many opportunities for peripheral token designers and enhances the functionalities of the existing and future tokens. In particular, the peripheral token designers have complete flexibility in creating digital assets without any action required from the host token sponsors.

For example, in a decentralized RPG GameFi world, the blacksmith can create weapons and armors (token *Y*) autonomously for characters (token *X*), and the gem maker can carve stones (token *Z*) to enhance weapons and armors (token *Y*) without any intervention from the blacksmith. This EIP intentionally ignores a top-down (centralized) relationship where the host token dictates the attached token’s specification. In true decentralization, the peripheral token extension facilitates user-generated content creation and enriches the host token’s functionalities and desirability.

Furthermore, this EIP unleashes the value of individual creators. Users can create a series of NFTs, for example, in-game items, and associate them with existing NFTs. This is done by assigning previously existing NFTs as host tokens to the user-generated series of NFTs. Using the RPG GameFi mentioned above as an example, every individual creator can become a blacksmith and create weapons and armor (NFTs) and airdrop to a character designed by the GameFi, which in this case, will be the host token. Once the dApp approves this relationship, the weapons and armor (NFT airdrops) can be pulled from the smart contract and be revealed in-game, with a unidirectional relationship.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

**Every ERC-721Peripheral compliant contract must implement the ERC721 and ERC165 interfaces.**

```auto
// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

/// @title ERC-721Peripheral Token Extension
/// @dev Required interface of an ERC721Peripheral compliant contract.
///   interfaceId == 0x59b7613c
///  The contract MUST maintain the token's state
interface IERC721Peripheral is IERC165, IERC721 {

    /// @dev This emits when a peripheral token attaches to another token by any mechanism.
    /// @param _tokenId is the peripheral token.
    /// @param _host The token that receives the child token.
    event Attach(uint256 indexed _tokenId, Host indexed _host);

    /// @dev This emits when a peripheral token detaches by any mechanism.
    /// @param _tokenId is the peripheral token.
    /// @param _newOwner is the token's new Owner
    event Dettach(uint256 indexed _tokenId, address indexed _newOwner);

    struct Host{
        address _address;
        uint256 _tokenId;
    }

    /// @dev Attaches a peripheral token `_tokenId` to a host token `_host`.
    ///   The contract MUST check if `Hosts` mapping has a `_tokenID` entry
    ///   (a.k.a the token has been attached to a host), and MUST check if
    ///   `msg.sender == ERC721(this).ownerOf(_tokenId)`
    ///   The contract MUST set the owner of the token to the encoded address of `_host`
    /// @param _tokenId is the peripheral token.
    /// @param _host The token that receives the child token.
    function attach(uint256 _tokenId, Host calldata _host) external;

    /// @dev Dettaches a peripheral token `_tokenId`
    ///  If _host._address is not ERC721Peripheral by checking `supportsInterface`,
    ///  the contract MUST check if the `msg.sender` == `ERC721(_host._address).ownerOf(_host._tokenID)`,
    ///  else if _host is ERC721Peripheral, the contract MUST recursively check
    ///  its _host until _host._address is is not ERC721Peripheral.
    ///  The contract MUST delete the entry from `Hosts`, and MUST assign
    ///  the ownership to `newOwner`.
    /// @param _tokenId is the peripheral token.
    /// @param _newOwner is the new owner of the peripheral token.
    function detach(uint256 _tokenId, address _newOwner) external;
}
```

Borrowing the idea from World of Warcraft, there are two variances of peripheral token: **tradable** and **soulbound**. For simplicity, we define the tradable peripheral token as the generalized specification, and the soulbound peripheral token is the special case.

### soulbound

```auto
function detach(uint256 tokenId) public override {
    revert("This is a soulbond token.");
}
```

## Rationale

The EIP intentionally ignores a top-down relationship where the host token can actively attach a  peripheral token for the following reasons:

- It is almost impossible to alter the existing host token’s implementation to extend the attachability.
- The dictated specification from the host token misaligns our belief in decentralization.
- Introducing two ideas in a single EIP is not recommended in EIP-1.

The EIP is also a generalization of soulbound token-to-token. As demonstrated in the previous section,  the EIP becomes a soulbound token-to-token with shielded `detach()`.

## Test Cases

## Reference Implementation

## Backwards Compatibility

This EIP is fully backward compatible with EIP-721

## Security Considerations

In `attach()`, the contract MUST set the token’s owner to the encoded address of _host. An example implementation may be `address(ripemd160(abi.encode(_host)))`. The address space is still considered large enough to avoid a collision. The security guarantee is the same as creating a new address.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/ethereum/EIPs/blob/LICENSE.md).
