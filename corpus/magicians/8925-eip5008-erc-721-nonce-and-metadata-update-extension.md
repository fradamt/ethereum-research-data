---
source: magicians
topic_id: 8925
title: "EIP5008: ERC-721 Nonce and Metadata Update Extension"
author: 0xanders
date: "2022-04-15"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip5008-erc-721-nonce-and-metadata-update-extension/8925
views: 3412
likes: 0
posts_count: 10
---

# EIP5008: ERC-721 Nonce and Metadata Update Extension

---

## eip: 5008
title: ERC-721 Nonce and Metadata Update Extension
description: Add a nonce property to ERC-721 tokens.
author: Anders (), Lance (), Shrug
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-04-10
requires: 165, 721

## Abstract

This standard is an extension of ERC-721. It proposes adding a `nonce` property and `MetadataUpdate` event to ERC-721 tokens.

## Motivation

Some orders of NFT marketplace has been attacked and the NFTs have been sold in a lower price than market floor price. One reason is that users transfer NFT to another wallet and then, after a certain period of time, transfer it back to the original wallet, and the order becomes valid again.

This EIP proposes adding an `nonce` property to ERC-721 tokens, and the `nonce` will be changed when transfer. If `nonce` is added to an order, the order can be checked to avoid attacks.

Many ERC-721 contracts emit their custom event when metadata changed. It is easy to update metadata of one NFT by specific event, but it is difficult for third-party platforms such as NFT marketplace to update metadata of many NFTs based on custom events.

Having a standard `MetadataUpdate` event will make it easy for third-party platforms to timely update metadata of many NFTs.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY” and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

```solidity
interface IERC5008  {
    /// @dev This event emits when the metadata of a token is changed.
    /// So that the third-party platforms such as NFT market could
    /// timely update the images and related attributes of the NFT
    event MetadataUpdate(uint256 tokenId);

    // Logged when the nonce of a NFT is changed
    /// @notice Emitted when the `nonce` of an NFT is changed
    event UpdateNonce(uint256 tokenId, uint256 newNonce);

    /// @notice Get the nonce of an NFT
    /// Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to get the nonce for
    /// @return The nonce of this NFT
    function nonce(uint256 tokenId) external view returns(uint256);
}
```

The `nonce(uint256 tokenId)` function MAY be implemented as `pure` or `view`.

The `UpdateNonce` event MUST be emitted when the nonce of a NFT is changed.

The `MetadataUpdate` event MUST be emitted when the metadata of a token is changed.

## Rationale

At first `transferCount` was considered as function name, but there may some case to change the `nonce` besides transfer, such as important properties are changed, then we changed `transferCount` to `nonce`.

Different NFTs have different metadata, and metadata generally has multiple fields. `bytes data` could be used to represents the modified value of metadata.  It is difficult for third-party platforms to identify various types of `bytes data`, so there is only one parameter `uint256 indexed _tokenId` in `MetadataUpdate` event. After capturing the `MetadataUpdate` event, a third party can update the metadata with information returned from the `tokenURI(uint256 _tokenId)` of ERC721.

## Backwards Compatibility

This standard is compatible with current ERC-721 standards.

## Test Cases

### Test Contract

```solidity
pragma solidity 0.8.10;
import "./ERC5008.sol";

contract ERC5008Demo is ERC5008{
    mapping(uint256 => uint256) private _tokenData;

    constructor(string memory name_, string memory symbol_)ERC721WithNonce(name_, symbol_){
    }

    /// @notice mint a new NFT
    /// @param to  The owner of the new token
    /// @param tokenId  The id of the new token
    function mint(address to, uint256 tokenId) public {
       _mint(to, id);
    }

    /// @notice update the data of the NFT
    /// @param id  The id of the token
    /// @param data  The data of the token
    function update(uint256 tokenId, uint256 data) public {
        require(_exists(tokenId), "Error: nonexistent token");
        _tokenData[tokenId] = data;
        emit MetadataUpdate(tokenId);
    }
}

```

### Test Code

run in terminal: `npm hardhat test`

```TypeScript
import { expect } from "chai";
import { ethers } from "hardhat";

describe("Test ERC5008 ", function () {

    let [alice, bob] = await ethers.getSigners();

    const ERC5008Demo = await ethers.getContractFactory("ERC5008Demo");

    let contract = await ERC5008Demo.deploy();

    let tokenId = 1;
    await contract.mint(alice.address, tokenId);

    expect(await contract.nonce(tokenId)).equals(1);

    await contract.transferFrom(alice.address, bob.address, tokenId);

    expect(await contract.nonce(tokenId)).equals(2);

});
```

## Reference Implementation

```solidity
// SPDX-License-Identifier: CC0
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./IERC5008.sol";

contract ERC5008 is ERC721, IERC5008 {
    mapping(uint256 => uint256) private _tokenNonce;

    constructor(string memory name_, string memory symbol_)ERC721(name_, symbol_){
    }

    /// @notice Get the nonce of an NFT
    /// Throws if `tokenId` is not a valid NFT
    /// @param tokenId The NFT to get the nonce for
    /// @return The nonce of this NFT
    function nonce(uint256 tokenId) public virtual override view returns(uint256) {
        require(_exists(tokenId), "Error: query for nonexistent token");

        return  _tokenNonce[tokenId];
     }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId
    ) internal virtual override{
        super._beforeTokenTransfer(from, to, tokenId);
        _tokenNonce[tokenId]++;
        emit UpdateNonce(tokenId, tokenNonce[tokenId]);
    }

    /// @dev See {IERC165-supportsInterface}.
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
        return interfaceId == type(IERC5008).interfaceId || super.supportsInterface(interfaceId);
    }
}
```

## Security Considerations

No security issues found.

## Replies

**SamWilsn** (2022-04-22):

Couple non-formatting related points:

- Will UpdateNonce be emitted for every transfer, as well as the transfer event itself?
- How would you feel about a standardized bumpNonce (with a better name) function for owners?
- Does MetadataUpdate need to be emitted when a token is first minted?
- Is it possible to make this compatible with EIP-1155 as well?

---

**0xanders** (2022-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Will UpdateNonce be emitted for every transfer, as well as the transfer event itself?

I have removed  `UpdateNonce` from interface.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Is it possible to make this compatible with EIP-1155 as well?

It will be more complex.

---

**wong2** (2022-07-31):

Do you know that most NFT projects update token metadata all at once with something like a baseTokenURI? How would `MetadataUpdate(tokenId)` suite here?

---

**ashhanai** (2022-09-20):

Can you provide more use cases for the `nonce` property?

I don’t think this standard is needed if the primary purpose is to fix broken marketplaces, which can be done by showing all orders and forcing buyers to set an expiration. It is also easier to fix one marketplace than implement a new standard and then update the marketplace to use the new property.

---

**0xanders** (2022-10-18):

It is mainly for dynamic NFTs , for example  ENS .  There is a expiry time and an avatar  for ENS NFT.

---

**0xanders** (2022-12-09):

Another dynamic NFT case: Decentraland  ESTATE, an ESTATE can be created by several LANDs, and the  owner can remove all the lands from the ESTATE. If the buyer did not notice this, the buyer may buy an empty ESTATE.

---

**fubuloubu** (2023-01-06):

No opinion on this EIP, just wanted to note that it is compatible with [EIP-4494: Permit for ERC-721 NFTs](https://eips.ethereum.org/EIPS/eip-4494), which is another helpful use case for a nonce

---

**mpeyfuss** (2023-07-27):

How would marketplaces be forced to use the nonce property? It seems like they could continue with their current code since this EIP is backwards compatible.

---

**mpeyfuss** (2023-07-27):

I don’t quite follow the rationale here as it’s not referenced in the EIP. Can you expand on this?

