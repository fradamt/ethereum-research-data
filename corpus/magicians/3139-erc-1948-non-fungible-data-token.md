---
source: magicians
topic_id: 3139
title: "ERC-1948: Non-fungible Data Token"
author: johba
date: "2019-04-15"
category: EIPs
tags: [nft, erc-1948]
url: https://ethereum-magicians.org/t/erc-1948-non-fungible-data-token/3139
views: 3845
likes: 8
posts_count: 4
---

# ERC-1948: Non-fungible Data Token

tl;dr;

Some use-cases require to have dynamic data associated with a non-fungible token that can change during its live-time. Examples for dynamic data:

- cryptokitties that can change color
- intellectual property tokens that encode rights holders
- tokens that store data to transport them across chains

The existing meta-data standard does not suffice as data can only be set at minting time and not modified later.

## Abstract

Non-fungible tokens (NFTs) are extended with the ability to store dynamic data. A 32 bytes data field is added and a read function allows to access it. The write function allows to update it, if the caller is the owner of the token. An event is emitted every time the data updates and the previous and new value is emitted in it.



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/1948)














####


      `master` ← `leapdao:master`




          opened 09:40AM - 18 Apr 19 UTC



          [![](https://avatars.githubusercontent.com/u/659301?v=4)
            johba37](https://github.com/johba37)



          [+159
            -0](https://github.com/ethereum/EIPs/pull/1948/files)







A proposal to standardize on tokens with dynamic data. Data that can be modified[…](https://github.com/ethereum/EIPs/pull/1948) during a token's live-time enables novel use-cases for NFTs:
- cryptokitties that can change color.
- intellectual property tokens that encode rights holders.
- tokens that store data to transport them across chains.

## Replies

**axic** (2019-05-17):

Copied from the draft:

> Non-fungible tokens (NFTs) are extended with the ability to store dynamic data. A 32 bytes data field is added and a read function allows to access it. The write function allows to update it, if the caller is the owner of the token. An event is emitted every time the data updates and the previous and new value is emitted in it.

```auto
pragma solidity ^0.5.2;
interface IERC1948 {
  event DataUpdated(uint256 indexed tokenId, bytes32 oldData, bytes32 newData);
  function readData(uint256 _tokenId) public view returns (bytes32);
  function writeData(uint256 _tokenId, bytes32 _newData) public;
}
```

Interesting, this is very similar to what we ([@decanus](/u/decanus) [@lrettig](/u/lrettig) @amyjung & me) did with Radical Bodies: [protocol/contracts/IERC721VariableMetadata.sol at master · RadicalBodies/protocol · GitHub](https://github.com/RadicalBodies/protocol/blob/master/contracts/IERC721VariableMetadata.sol)

We called it “variable metadata”, another hash URL to variable data:

```auto
pragma solidity ^0.5.0;
interface IERC721VariableMetadata {
  // Retrieve the currently set variable metadata.
  function variableMetadataURI(uint256 tokenId) external view returns (string);
  // Replace the variable metadata.
  function replaceVariableMetadataURI(uint256 tokenId, string metadataURI) external;
}
```

I wonder if it would be possible to reconcile the two proposals by introducing a “data type” field?

---

**johba** (2019-05-22):

good to see that there are more use-cases for variable data. I think that is a great idea to merge these.

i’m not particularly keen about the string data type, as it is not represented efficiently, and i don’t want to use the chain to store data. how about this proposal:

```auto
interface IERC721VariableData {
  event DataUpdated(uint256 indexed tokenId, bytes32 oldData, bytes32 newData, uint256 dataType);
  function getDataType(uint256 _tokenId) external view returns (uint256);
  // Retrieve the currently set variable data.
  function readData(uint256 _tokenId) external view returns (uint256 type, bytes32 data);
  // Replace the variable data.
  function writeData(uint256 _tokenId, bytes32 _newData) external;
}
```

Here I assume:

- data type is set at token minting, and does not change after.
- I see 3 types we could use right away:

type 0 - pure data, the token stores a single uint256, or sha256 hash
- type 1 - the token stores a hash of a string (to implement the URI). string needs to be provided in msg.Data and verified against hash
- type 2 - the token stores the root of a merkle tree, proofs need to be provided with msg.data

---

**HenryRoo** (2025-08-20):

This is becoming relevant again, especially now with the rise of AI. The conversation has shifted from simply allowing tokens to carry mutable state to leveraging that token data to feed AI systems while also enabling dynamic data stack updates and iterative enhancements to the data set.

