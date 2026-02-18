---
source: magicians
topic_id: 20939
title: "ERC-7729: Token with Metadata"
author: fewwwww
date: "2024-09-02"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7729-token-with-metadata/20939
views: 209
likes: 3
posts_count: 5
---

# ERC-7729: Token with Metadata

## Abstract

This standard extends the ERC-20 standard to include a `metadata` function interface and a JSON schema for metadata.

## Motivation

Memecoins have demonstrated the value of associating tokens with visual metadata. By standardizing a way to include metadata in ERC-20 tokens, developers can create more engaging and interactive tokens, fostering community engagement.

## Specification

The keywords “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

**Every compliant contract must implement the `IERCX`, and `ERC20` interfaces.**

This standard includes the following interface:

```solidity
pragma solidity ^0.8.0;
interface IERC20Metadata is IERC20 {
    /// @dev Returns the metadata URI associated with the token.
    ///  The URI may point to a JSON file that conforms to the "ERCX Metadata JSON Schema".
    function metadata() external view returns (string memory);
}
```

This is the “ERCX Metadata JSON Schema” referenced above.

```json
{
    "title": "Token Metadata",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Identifies the asset to which this token represents"
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this token represents"
        },
        "image": {
            "type": "string",
            "description": "A URI pointing to a resource with mime type image/* representing the asset to which this token represents."
        }
    }
}
```

## Backwards Compatibility

This standard is backward compatible with the ERC-20 as it extends the existing functionality with new interfaces.

## Reference Implementation

```solidity
pragma solidity ^0.8.0;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
interface IERCX is IERC20 {
    function metadata() external view returns (string memory);
}
contract ERCX is ERC20, IERCX {
    string _metadata = "ipfs://QmakTsyRRmvihYwiAstYPYAeHBfaPYz3v9z2mkA1tYLA4w";
    function metadata() external view returns (string memory) {
        return _metadata;
    }
}
```

## Copyright

Copyright and related rights waived via CC0.

## Replies

**tinom9** (2024-10-22):

I think it’s only positive to standardize this.

What are your thoughts on adding guidelines for links and other keys?

I’m thinking memecoins currently have, more or less, the following fields:

- name,
- ticker or symbol,
- description,
- image or video,
- links to social sites and website (X, Telegram, etc…). It could be implemented with reverse dot notation mirroring ENSIP-5.

Leaving a JSON schema looking something like this.

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ERC20Metadata",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "description": "Identifies the asset to which this token represents"
    },
    "symbol": {
      "type": "string",
      "description": "Symbol, ticker or short name"
    },
    "description": {
      "type": "string",
      "description": "Describes the asset to which this token represents"
    },
    "image": {
      "type": "string",
      "description": "A URI pointing to a resource with mime type image/* representing the asset to which this token represents."
    },
    "video": {
      "type": "string",
      "description": "An optional URI pointing to a resource with mime type video/* representing the asset to which this token represents."
    },
    "website": {
      "type": "string",
      "description": "An optional URI pointing to the asset's website."
    },
    "org.telegram": {
      "type": "string",
      "description": "An optional URI pointing to the asset's Telegram channel."
    }
  },
  "required": ["name", "symbol", "description", "image"],
  "additionalProperties": true
}
```

---

**fewwwww** (2024-11-16):

Thanks for the feedback!

My initial thought of creating this EIP is to standardize the creation of memecoin.

I think the json you posted can definitely be an example format for this standard. Will add it in next iteration.

---

**tinom9** (2024-11-16):

Great, what about implementing ERC-165? I think it also makes sense to make it mandatory.

For example:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity 0.8.26;

import { ERC20 } from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

interface IERC7729 {
  function metadata() external view returns (string memory);
}

contract Token is ERC20, IERC7729 {
  string private _metadata;

  constructor(
    string memory name_,
    string memory symbol_,
    string memory metadata_
  ) ERC20(name_, symbol_) {
    _metadata = metadata_;
  }

  function metadata() public view override returns (string memory) {
    return _metadata;
  }

  function supportsInterface(
    bytes4 interfaceId
  ) public pure returns (bool) {
    return interfaceId == type(IERC7729).interfaceId; // bytes4(0x392f37e9)
  }
}
```

---

**shubh-ta** (2024-11-17):

I think, rather than adding the metadata info within ERC20 contract storage, it would be better to store new metadata contract address and that metadata contract associated with ERC20 token can have all requisite information for ERC20 token.

