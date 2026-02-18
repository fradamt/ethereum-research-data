---
source: magicians
topic_id: 10427
title: "EIP 5496: Multi-privilege Management Extension for ERC-721"
author: wnft
date: "2022-08-18"
category: EIPs
tags: [nft, erc-721, clone, privilege, right]
url: https://ethereum-magicians.org/t/eip-5496-multi-privilege-management-extension-for-erc-721/10427
views: 2460
likes: 0
posts_count: 4
---

# EIP 5496: Multi-privilege Management Extension for ERC-721

eip: 5496

title: ERC-721 Multi-privilege Management Extension

description: Standard interface for creating sharable multi-privilege NFTs for ERC-721

author: wnft dev@wnft.one

discussions-to:

status: Draft

type: Standards Track

category: ERC

created: 2022-7-30

requires: 721

---

## Abstract

This specification defines standard functions that extends current [ERC-721] standard providing sharable multiple privileges for a NFT collection. The privileges could be the 1) on-chain ones, such as voting rights, or to claim a targeted airdrop; 2) or off-chain ones, such as a coupon in Amazon, or a discount in a local New York restaurant, or even a VIP lounge access in the airport.  There could be multiple privileges attached to one NFT and each privilege holder of an NFT can transfer the privilege to others. The ownership of the privileges is verifiable. On top of the multiple-privilege extension, this standard also contains methods to give the provider to specify the privilege non-sharable or sharable. Sharable privileges can be done by simply cloning a privilege, furthermore, the provider would be able to adjust the details of privileges according to the spreading path. Expiration period can also be set to each privilege. The proposal depends on and extends the existing [ERC-721].

You can find a draft of the system here: GitHub - [ERC721-P: A contract to manage sharable multi-privilege NFTs](https://github.com/wnft/ERC721P)

## Motivation

Many NFTs have functions other than just being used as profile pictures or collection of art works, they may have real utilities in different scenarios. For example, a fashion store may give a discount for its own NFT holders; a DAO member NFT holder can vote for the proposal of how to use their treasury; some dApp may create an airdrop event to attract a certain group of people like some bluechip NFT holders to claim; Walmart can issue its membership card on chain(NFT) and give certain privileges when the members shop at the Walmart stores, etc. There are cases when people who own NFTs do not necessarily want to / not being able to use privileges. By providing additional data recording different privileges a NFT collection has and interfaces to manage them, users can now transfer or sell privileges without losing their ownership of the NFT.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and

“OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Every contract compliant to the `ERC721P` extension MUST implement the `IERC721P` interface. The **

sharable multi-privilege extension** is OPTIONAL for ERC-721 contracts.

```solidity
/// @title ERC-721P multi-privilege extension

///  Note: the ERC-165 identifier for this interface is 0x953c8dfa

interface IERC721P /* is ERC721 */ {

    /// @notice Emitted when `owner` changes the `privilege holder` of a NFT.

    event PrivilegeAssigned(uint256 tokenId, uint256 privilegeId, address user, uint256 expires);

    /// @notice Emitted when `privilege holder` changes the `holder` of a privilege

    event PrivilegeTransfered(uint256 tokenId, uint256 privilegeId, address from, address to);

    /// @notice Emitted when `contract owner` changes the `total privilege` of the collection

    event PrivilegeTotalChanged(uint256 newTotal, uint256 oldTotal);

    /// @notice set the privilege holder of a NFT.

    /// @dev expires should better be less than 30 days

    /// Throws if `msg.sender` is not approved or owner of the tokenId.

    /// @param tokenId The NFT to set privilege for

    /// @param privilegeId The privilege to set

    /// @param user The privilege holder to set

    /// @param expires For how long the privilege holder can have

    function setPrivilege(uint256 tokenId, uint256 privilegeId, address user, uint256 expires) external;

    /// @notice Check if a privilege has expired

    /// @param tokenId The identifier of the queried NFT

    /// @param privilegeId The identifier of the queried privilege

    /// @return Whether a user has a certain privilege

    function privilegeExpires(uint256 tokenId, uint256 privilegeId) external view returns(uint256);

    /// @notice Check if a user has a certain privilege

    /// @param tokenId The identifier of the queried NFT

    /// @param privilegeId The identifier of the queried privilege

    /// @param user The address of the queried user

    /// @return Whether a user has a certain privilege

    function hasPrivilege(uint256 tokenId, uint256 privilegeId, address user) external view returns(bool);

}

```

Every contract implementing the `ERC721P` SHOULD set a maximum privilege number before setting any privilege, the privilegeId MUST NOT be greater than the maximum privilege number.

The `PrivilegeAssigned` event MUST be emitted when `setPrivilege` is called.

The `PrivilegeTransfered` event MUST be emitted when `transferPrivilege` is called.

The `supportsInterface` method MUST return `true` when called with `0x076e1bbb`.

```solidity
/// @title ERC-721P Cloneable extension - Optional

interface IERC721PCloneable {

    /// @notice Emitted when set the `privilege ` of a NFT cloneable.

    event PrivilegeCloned(uint tokenId, uint privId, address from, address to);

    /// @notice set a certain privilege cloneable

    /// @param tokenId The identifier of the queried NFT

    /// @param privilegeId The identifier of the queried privilege

    /// @param referrer The address of the referrer

    /// @return Whether the operation is sucessful or not

    function clonePrivilege(uint tokenId, uint privId, address referrer) external returns (bool);

}

```

The `PrivilegeCloned` event MUST be emitted when `clonePrivilege` is called.

## Rationale

### Multiple privileges

Current ERC-721 standard only record the ownership and its transfer, the privileges of an NFT are not recorded on-chain. This extension would allow merchants/projects to give out a certain privilege to a specified group of people, and owners of the privileges can manage each one of the privileges independently. This facilitates a great possibility for NFTs to have real usefulness.

### Sharable privileges

The number of privilege holders is limited by the number of NFTs if privileges are non-sharable. A sharable privilege means the original privilege holder can copy the privilege and give it to the others, not transferring his/her own privilege to the others. This mechanism greatly enhances the spread of privileges as well as the adoption of NFTs.

## Backwards Compatibility

ERC721PA is compatible to any kind of NFTs that follow ERC-721 standard. It only adds more functions and data structures without interfering with original ERC-721 standard.

## Test Cases

Test cases are implemented in the reference implementation

repository.

## Reference Implementation

The following is a snippet for reference implementation of the `ERC721P` extension. The full repository can be

found in github.

```solidity
// SPDX-License-Identifier: CC0-1.0

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

import "./IERC721P.sol";

contract ERC721P is ERC721, IERC721P {

    struct PrivilegeRecord {

        address user;

        uint256 expiresAt;

    }

    struct PrivilegeStorage {

        uint lastExpiresAt;

        // privId => PrivilegeRecord

        mapping(uint => PrivilegeRecord) privilegeEntry;

    }

    uint public privilegeTotal;

    // tokenId => PrivilegeStorage

    mapping(uint => PrivilegeStorage) public privilegeBook;

    mapping(address => mapping(address => bool)) private privilegeDelegator;

    constructor(string memory name_, string memory symbol_)

    ERC721(name_,symbol_)

    {



    }

    function setPrivilege(

        uint tokenId,

        uint privId,

        address user,

        uint64 expires

    ) external virtual {

        require(_isApprovedOrOwner(msg.sender, tokenId) || _isDelegatorOrHolder(msg.sender, tokenId, privId), "ERC721: transfer caller is not owner nor approved");

        require(expires =  block.timestamp ){

            return privilegeBook[tokenId].privilegeEntry[privId].user == user;

        }

        return ownerOf(tokenId) == user;

    }

    function privilegeExpires(

        uint256 tokenId,

        uint256 privId

    ) public virtual view returns(uint256){

        return privilegeBook[tokenId].privilegeEntry[privId].expiresAt;

    }

    function _setPrivilegeTotal(

        uint total

    ) internal {

        emit PrivilegeTotalChanged(total, privilegeTotal);

        privilegeTotal = total;

    }

    function getPrivilegeInfo(uint tokenId, uint privId) external view returns(address user, uint256 expiresAt) {

        return (privilegeBook[tokenId].privilegeEntry[privId].user, privilegeBook[tokenId].privilegeEntry[privId].expiresAt);

    }

    function setDelegator(address delegator, bool enabled) external {

        privilegeDelegator[msg.sender][delegator] = enabled;

    }

    function _isDelegatorOrHolder(address delegator, uint256 tokenId, uint privId) internal virtual view returns (bool) {

        address holder = privilegeBook[tokenId].privilegeEntry[privId].user;

         return (delegator == holder || isApprovedForAll(holder, delegator) || privilegeDelegator[holder][delegator]);

    }

    function supportsInterface(bytes4 interfaceId) public override virtual view returns (bool) {

        return interfaceId == type(IERC721P).interfaceId || super.supportsInterface(interfaceId);

    }

}

```

## Security Considerations

Implementors of the `ERC721P` standard must consider thoroughly who has the permission to set or clone privileges.

## Copyright

Copyright and related rights waived via [CC0].

## Replies

**poojaranjan** (2022-10-25):

To learn more about the proposed standard, check out the talk [PEEPanEIP #86: EIP-5496: Multi-privilege Management NFT Extension](https://youtu.be/AD0Qc6julhU) with Allister Capati & Jeremy Z.

  [![image](https://i.ytimg.com/vi/AD0Qc6julhU/hqdefault.jpg)](https://www.youtube.com/watch?v=AD0Qc6julhU)

---

**peersky** (2023-05-12):

Hi there.

I am wondering if it would make sense for you to define smart contract access privileges based on a function semantic meaning?

I’ve described this idea in my blog

https://peersky.xyz/blog/token-id-matching-to-msg-sig/

as well as here [on the forum](https://ethereum-magicians.org/t/method-signature-as-token-identificator/13632/5)

---

**shifa_j22** (2025-02-07):

This is a great usecase. This could take the NFT game to the next level.

