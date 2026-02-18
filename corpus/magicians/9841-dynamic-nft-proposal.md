---
source: magicians
topic_id: 9841
title: Dynamic NFT Proposal
author: connectorGamefi
date: "2022-07-05"
category: Magicians > Primordial Soup
tags: [nft, token]
url: https://ethereum-magicians.org/t/dynamic-nft-proposal/9841
views: 465
likes: 2
posts_count: 1
---

# Dynamic NFT Proposal

Games using non-fungible tokens to stand for their internal objects including roles, assets etc. and there will be some dynamic data asscociated with them, e.g.

- roles in games can change their clothes color
- NPCs in games can change their skills
- properties in games will have different attributes while different roles obtain

Can we use a simple data structure to store dynamic attributes, like this:

```auto
struct AttributeData {
    uint128 attrID;
    uint128 attrValue;
}
// tokenID => attribute data
mapping(uint256 => AttributeData[]) internal _attrData;
```

And supply some interface to operate those attributes:

```auto
/**
     * @dev Attach the attribute to NFT.
     */
    function attach(uint256 tokenID, uint128 attrID, uint128 value) external;

    /**
     * @dev Attach a batch of attributes to NFT.
     */
    function attachBatch(uint256 tokenID, uint128[] memory attrIDs, uint128[] memory values) external;

    /**
     * @dev Update the attribute to NFT.
     */
    function update(uint256 tokenID, uint256 attrIndex, uint128 value) external;

    /**
     * @dev Update a batch of attributes to NFT.
     */
    function updateBatch(uint256 tokenID, uint256[] memory attrIndexes, uint128[] memory values) external;

    /**
     * @dev Remove the attribute from NFT.
     */
    function remove(uint256 tokenID, uint256 attrIndex) external;

    /**
     * @dev Remove a batch of attributes from NFT.
     */
    function removeBatch(uint256 tokenID, uint256[] memory attrIndexes) external;
```

Through the above data structures and methods, users can convert their in-game payments into on-chain assets.
