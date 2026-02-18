---
source: magicians
topic_id: 13568
title: "EIP-6785: ERC-721 Utilities extension"
author: otniel
date: "2023-03-27"
category: EIPs
tags: [nft]
url: https://ethereum-magicians.org/t/eip-6785-erc-721-utilities-extension/13568
views: 2089
likes: 0
posts_count: 5
---

# EIP-6785: ERC-721 Utilities extension

# ERC-6785: ERC-721 utilities extension

## Abstract

This specification defines standard functions that outline what a utility entails for a specific NFT and how it may be

used. This specification is an optional extension of `EIP-712`.

## Motivation

This specification aims to bring clarity what the utility associated with an NFT is and how to access this utility.

Relying on third-party platforms to obtain information regarding the utility of the NFT that one owns can lead to scams,

phishing or other forms of fraud.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and

“OPTIONAL” in this document are to be interpreted as described in RFC 2119.

Every contract compliant with EIP-6785 MUST implement the interface defined as follows:

### Contract Interface

```solidity
// @title NFT Utility description
///  Note: the EIP-165 identifier for this interface is 0xbcc08bd0

interface IERC6785 {

    // Logged when the utility description URL of an NFT is changed
    /// @notice Emitted when the utilityURL of an NFT is changed
    /// The empty string for `utilityUri` indicates that there is no utility associated
    event UpdateUtility(uint256 indexed tokenId, string utilityUri);

    /// @notice set the new utilityUri - remember the date it was set on
    /// @dev The empty string indicates there is no utility
    /// Throws if `tokenId` is not valid NFT
    /// @param utilityUri  The new utility description of the NFT
    /// 324a28b4
    function setUtilityUri(uint256 tokenId, string utilityUri) external;

    /// @notice Get the utilityUri of an NFT
    /// @dev The empty string for `utilityUri` indicates that there is no utility associated
    /// @param tokenId The NFT to get the user address for
    /// @return The utility uri for this NFT
    /// 438b8582
    function getUtilityUri(uint256 tokenId) external view returns (string memory);

    /// @notice Get the changes made to utilityUri
    /// @param tokenId The NFT to get the user address for
    /// @return The history of changes to `utilityUri` for this NFT
    /// af5a3ae2
    function getUtilityHistory(uint256 tokenId) external view returns (string[] memory);
}
```

All functions defined as view MAY be implemented as pure or view

Function `setUtilityUri` MAY be implemented as public or external

The event `UpdateUtility` MUST be emitted when the setUtilityUri function is called

The supportsInterface method MUST return true when called with `0xbcc08bd0`

The original metadata SHOULD conform to the “ERC-6785 Metadata with utilities JSON Schema” which is a compatible

extension of the “ERC-721 Metadata JSON Schema” defined in `ERC-721`.

“ERC-6785 Metadata with utilities JSON Schema” :

```json
{
  "title": "Asset Metadata",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Identifies the asset to which this NFT represents"
    },
    "description": {
      "type": "string",
      "description": "Describes the asset to which this NFT represents"
    },
    "image": {
      "type": "string",
      "description": "A URI pointing to a resource with mime type image/* representing the asset to which this NFT represents. Consider making any images at a width between 320 and 1080 pixels and aspect ratio between 1.91:1 and 4:5 inclusive."
    },
    "utilities": {
      "type": "object",
      "required": [
        "type",
        "description",
        "t&c"
      ],
      "properties": {
        "type": {
          "type": "string",
          "description": "Describes what type of utility this is"
        },
        "description": {
          "type": "string",
          "description": "A brief description of the utility"
        },
        "properties": {
          "type": "array",
          "description": "An array of possible properties describing the utility, defined as key-value pairs",
          "items": {
            "type": "object"
          }
        },
        "expiry": {
          "type": "number",
          "description": "The period of time for the validity of the utility, since the minting of the NFT. Expressed in seconds"
        },
        "t&c": {
          "type": "string",
          "description": ""
        }
      }
    }
  }
}
```

## Rationale

Currently, utilities that are offered with NFTs, are not captured on-chain. We want the utility of an NFT to be part of

the metadata of an NFT, and thus immutable. The metadata information would include: a) type of utility, b) description

of utility, c) frequency and duration of utility, and d) expiration of utility. This will provide transparency as to the

utility terms, and greater accountability on the creator to honor these utilities.

Instructions on how to access the utility should be available to the owner of an NFT, as it reduces the dependency on

third-party platforms and the possibility for fraud because the `utilityUri` containing the instructions can only come

from the entity that provides or facilitates the utility. Thus, the ability to set the `utilityUri` should be restricted

to the creator who’s offering the utility. Since the `utilityUri` contains information that could be restricted to some

level and is dependent on a third party platform, the creator needs the ability to modify it in the event the platform

becomes unavailable or inaccessible.

As the instructions on how to access a given utility may change over time, there should be a historical record of these

changes for transparency.

For example, if a creator sells an NFT that gives holders a right to a video call with the creator, the metadata for

this utility NFT would read as follows:

```json
{
  "name": "...",
  "description": "...",
  "image": "...",
  "utilities": {
    "type": "Video call",
    "description": "I will enter a private video call with whoever owns the NFT",
    "properties": [
      {
        "sessions": 2
      },
      {
        "duration": 30
      },
      {
        "time_unit": "minutes"
      }
    ],
    "expiry": 1.577e+7,
    "t&c": "https://...."
  }
}
```

In order to get access to the details needed to enter the video call, the owner would access the URI returned by

the `getUtilityUri` method for the NFT that they own. Additionally, access to the details could be conditioned by the

authentication with the wallet that owns the NFT.

The current status of the utility would also be included in the URI (eg: how many sessions are still available, etc.)

## Backwards Compatibility

This standard is compatible with current EIP-721 standard. There are no other standards that define similar methods for

NFTs and the method names are not used by other EIP-721 related standards.

## Test Cases

Test cases are available [here](https://github.com/OT-kthd/EIPs/blob/eip-6785/assets/eip-6785/test/ERC6785.test.js)

## Reference Implementation

A possible implementation can be the following:

```auto
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/introspection/ERC165.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./IERC6785.sol";

contract ERC6785 is ERC721, Ownable, IERC6785 {

    /*
     *     bytes4(keccak256('setUtilityUri(uint256,string)')) = 0x4a048176
     *     bytes4(keccak256('getUtility(uint256)')) = 0x0007c019
     *     bytes4(keccak256('getUtilityHistory(uint256)')) = 0xf6c3cabf
     *
     *     => 0x4a048176 ^ 0x0007c019 ^ 0xf6c3cabf == 0xbcc08bd0
     */
    bytes4 private constant _INTERFACE_ID_ERC6785 = 0xbcc08bd0;

    mapping(uint => string[]) private utilities;

    constructor(string memory name_, string memory symbol_) ERC721(name_, symbol_) {}

    /**
     * @dev See {IERC165-supportsInterface}.
     */
    function supportsInterface(bytes4 interfaceId) public view virtual override returns (bool) {
        return
        interfaceId == type(IERC6785).interfaceId || super.supportsInterface(interfaceId);
    }

    function setUtilityUri(uint256 tokenId, string calldata utilityUri) override external onlyOwner {
        utilities[tokenId].push(utilityUri);
        emit UpdateUtility(tokenId, utilityUri);
    }

    function getUtilityUri(uint256 tokenId) override external view returns (string memory) {
        uint last = utilities[tokenId].length - 1;
        return utilities[tokenId][last];
    }

    function getUtilityHistory(uint256 tokenId) override external view returns (string[] memory){
        return utilities[tokenId];
    }
}
```

## Security Considerations

There are no security considerations related directly to the implementation of this standard.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/ethereum/EIPs/blob/master/LICENSE.md)

## Replies

**SamWilsn** (2023-05-16):

Other ERC-721 getters follow the convention of `nounOf(uint256 tokenId)`, perhaps `utilityUriOf` would make sense instead of `getUtilityUri`.

---

**SamWilsn** (2023-06-02):

Generally who will be calling the `setUtilityUri` function? Is it the creator of the NFT, or the owner of the NFT?

If it is the creator, I would suggest omitting `setUtilityUri` from the standard (though you should keep the associated event.) In [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [ERC-20](https://eips.ethereum.org/EIPS/eip-20), and many other token standards the `mint`-side of the token is left implementation defined because it is so unique to each token contract.

Assuming it is the token creator that chooses the utility, I’d make the same argument here.

---

**otniel** (2023-06-05):

I think you had brought this up before in a different discussion, but what I argued at the time is that there are quite a few NFT contracts in which there are many different users that create NFTs, thus the contract owner is not necessarily the creator of the NFT. If utility is offered under such contracts, it would make sense to have a method allowing the creator (as the one who offers the utility) to modify the source of information for the utility details

---

**SamWilsn** (2023-06-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/otniel/48/9010_2.png) otniel:

> you had brought this up before in a different discussion

It’s on my checklist of things to question, so I tend to bring it up a lot ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12) Whether you choose to keep it or not is totally up to you, and keeping it won’t stop your proposal from progressing. I’m not really an expert on these things, so ignore me (on FEM) when/if it makes sense!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/otniel/48/9010_2.png) otniel:

> there are quite a few NFT contracts in which there are many different users that create NFTs

Right, like the OpenSea contracts. In these cases, would you expect the NFT creator to use OpenSea’s dapp or a third-party dapp to change the utility settings?

Personally I think that NFT creators would use the same dapp to modify their token as they did to create it, and so the function is application-specific.

---

Requiring a `setUtilityUri` function has some weird implications. What if there was a token with immutable utility metadata (maybe `data:application/json;base64,...` or `ipfs://...`)? Its `setUtilityUri` function would always revert, which isn’t particularly useful.

