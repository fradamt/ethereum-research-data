---
source: magicians
topic_id: 22986
title: "EIP-7891: Hierarchical NFTs with Splitting and Merging"
author: nitin312
date: "2025-02-25"
category: ERCs
tags: [nft, token, evm, gas]
url: https://ethereum-magicians.org/t/eip-7891-hierarchical-nfts-with-splitting-and-merging/22986
views: 292
likes: 3
posts_count: 5
---

# EIP-7891: Hierarchical NFTs with Splitting and Merging

## Abstract

This standard extends [EIP-721](https://github.com/ethereum/ERCs/blob/07fd24df7f4dab9310ea7bdcdea93cedd0558c45/EIPS/eip-721.md) and [EIP-6150](https://github.com/ethereum/ERCs/blob/07fd24df7f4dab9310ea7bdcdea93cedd0558c45/EIPS/eip-6150.md). This introduces a structured parent-child relationship between NFTs, allowing an NFT to be fractionally split into multiple child NFTs and merged back into a single entity. It provides interfaces to retrieve an NFT’s parent, children, and hierarchical status, ensuring flexible ownership management. This standard is particularly useful for applications in fractional ownership, asset distribution, and composable digital assets, opening new possibilities in fields like real estate, gaming, and decentralized finance.

## Motivation

This eip introduces hierarchical NFTs with splitting and merging capabilities, allowing assets to be dynamically restructured. This proposal is crucial for fractional ownership, gaming assets, and financial instruments, where assets need to be split or merged.

1. Splitting: One of the key limitations of EIP-6150 is its rigid hierarchy, where NFTs are permanently assigned to a parent without the ability to restructure ownership. In many real-world scenarios, assets need to be split into smaller, independent units. This eip introduces a standardized way to split an NFT into multiple child NFTs, enabling dynamic asset management. For example, in financial markets, a share NFT can be split into multiple fractional share NFTs, allowing investors to own and trade smaller portions of a share.
2. Merging: Just as assets need to be split, there are scenarios where multiple NFTs should be combined into a single entity. The proposed eip enables a merging mechanism, allowing child NFTs to be consolidated into a single parent NFT, allowing asset management and transactions. For instance, in finance, fractional share NFTs can be merged back into a full share NFT, enabling seamless ownership consolidation. This is particularly useful for investors who gradually accumulate fractions of a stock and later want to own a full share.
3. Share Distribution: This eip introduces ownership share management, allowing NFTs to track and distribute fractional ownership among multiple stakeholders. This solves fractional ownership tracking within parent-child NFT structures. This also allows dynamic adjustments of ownership based on splitting and merging actions. For example, a real estate NFT representing a building can have multiple owners with different share percentages. When the NFT is split, the new NFTs retain a proportion of the original ownership share. When merged, the system redistributes the shares accordingly. This Enables multi-party ownership in digital assets.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Interface Definition

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
/**
* @title: Hierarchical NFTs with Splitting, Merging, and Share Management
* @dev This interface extends ERC-6150 for hierarchical NFTs with share-based ownership management.
*/
interface IERC7891 /* is IERC6150, IERC721 */ {

/**
* @dev Mints a new parent NFT.
* @param _tokenURI URI for the NFT metadata
* @return tokenId, the minted token ID
*/
function mintParent(string memory _tokenURI) external payable returns (uint256 tokenId);

/**
* @dev Mints a new child NFT from a parent NFT with a share allocation.
* @param parentId, the ID of the parent NFT
* @param _share Share percentage assigned to the child
* @return tokenId, the minted child NFT ID
*/
function mintSplit(uint256 parentId, uint8 _share) external payable returns (uint256 tokenId);

/**
* @dev Merges multiple child NFTs into a new token under the same parent.
* @param parentId, the parent NFT ID
* @param _tokenIds Array of child token IDs to be merged
* @return newTokenId, the ID of the newly minted merged NFT
*/
function mintMerge(uint256 parentId, uint256[] memory _tokenIds) external payable returns (uint256 newTokenId);

/**
* @dev Transfers share ownership from one NFT to another.
* @param to, Token ID receiving the share
* @param from, Token ID sending the share
* @param _share Share percentage to transfer
*/
function sharePass(uint256 to, uint256 from, uint8 _share) external; }
```

Optional Extensions: Burnable

```auto
interface IERC7891Burnable is IERC7891 {
/**
* @dev Burns an NFT and transfers its share back to the parent NFT.
*/
function burn (uint256 tokenId) external;
}
```

## Rationale

### How the proposed EIP Improves Over Existing Standards

| Feature | EIP-721 | EIP-1155 | EIP-6150 | EIP (Proposed) |
| --- | --- | --- | --- | --- |
| Unique NFTs |  |  |  |  |
| Fungible & Non-Fungible |  |  |  |  |
| Hierarchical Structure |  |  |  |  |
| Parent-Child Relationship |  |  |  |  |
| NFT Splitting |  |  |  |  |
| NFT Merging |  |  |  |  |
| Fractional Ownership |  |  |  |  |
| Ownership Redistribution |  |  |  |  |

## Backwards Compatibility

The proposed EIP extends [EIP-721](https://github.com/ethereum/ERCs/blob/07fd24df7f4dab9310ea7bdcdea93cedd0558c45/EIPS/eip-721.md) and [EIP-6150](https://github.com/ethereum/ERCs/blob/07fd24df7f4dab9310ea7bdcdea93cedd0558c45/EIPS/eip-6150.md), making it backward compatible.

## Reference Implementation

A Solidity implementation of the proposed EIP standard is provided below.

```auto
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;
import "./ERC6150.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ERC7891 is ERC6150 {
using Counters for Counters.Counter;
Counters.Counter private _tokenIds;
mapping(uint256 => string) private _tokenURIs;
mapping(uint256 => uint8) public share;

constructor() ERC6150("ERC7891", "NFT") {}

function mintParent(string memory tokenURI) external returns (uint256) {
_tokenIds.increment();
uint256 tokenId = _tokenIds.current();
_safeMintWithParent(msg.sender, 0, tokenId);
share[tokenId] = 100;
_tokenURIs[tokenId] = tokenURI;
return tokenId;
}

function mintSplit(uint256 parentId, uint8 _share) external returns (uint256) { require(share[parentId] >= _share, "Insufficient parent share");
_tokenIds.increment(); uint256 childId = _tokenIds.current();
_safeMintWithParent(msg.sender, parentId, childId);
share[parentId] -= _share;
share[childId] = _share;
_tokenURIs[childId] = _tokenURIs[parentId];
emit NFTSplit(parentId, childId, _share);
return childId;
 }

function mintMerge(uint256 parentId, uint256[] memory tokenIds) external returns (uint256) {
 uint8 totalShare = 0;
for (uint256 i = 0; i < tokenIds.length; i++) {
require(parentOf(tokenIds[i]) == parentId, "Not a child of the same parent");
totalShare += share[tokenIds[i]];
_burn(tokenIds[i]);
}
_tokenIds.increment();
uint256 newParentId = _tokenIds.current();
_safeMintWithParent(msg.sender, parentId, newParentId);
share[newParentId] = totalShare;
emit NFTMerged(newParentId, tokenIds);
return newParentId;
}
}
```

## Security Considerations

No security considerations were found.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/ethereum/ERCs/blob/07fd24df7f4dab9310ea7bdcdea93cedd0558c45/LICENSE.md).

## Replies

**nitin312** (2025-04-11):

Hi everyone,

I’m reaching out regarding [ERC-7891: Hierarchical NFTs with Splitting and Merging](https://ethereum-magicians.org/t/eip-7891-hierarchical-nfts-with-splitting-and-merging/22986), which has been submitted as a pull request ([#930 on GitHub](https://github.com/ethereum/EIPs/pull/930)).

The proposal extends ERC-721 and ERC-6150 to introduce a structured parent-child relationship for NFTs, enabling fractional splitting and merging of tokens. This design is particularly useful for applications involving fractional ownership, digital asset management, etc.

All automated checks have passed.

The PR has been open for a while and is currently **awaiting code owner review** before it can move forward.

I would greatly appreciate it if any editors or reviewers could take a moment to review the draft and provide feedback or approval. If any updates or changes are needed, I’m happy to accommodate.

Thanks in advance for your time and consideration!

---

**nitin312** (2025-04-11):

Title: Issue with Auto Review Bot Failing on PR #930 — “No artifacts found”

Hi everyone,

I’m currently working on [PR #930](https://github.com/ethereum/EIPs/pull/930) and noticed a problem with the `eip-review-bot`. After leaving a follow-up comment to request a review, the Auto Review Bot triggered but failed almost immediately with the message:

> Run failed: Auto Review Bot - master (a23375b)
> Error: no artifacts found

The GitHub Actions log shows that the `auto-review-bot.yml` ran for just 3 seconds before failing. No artifacts were created, and it seems like the job didn’t have the necessary inputs to proceed.

Has anyone encountered this before? Could it be related to a misconfiguration or recent GitHub workflow updates? Any guidance on how to proceed or who to tag would be appreciated!

Thanks in advance ![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=12)

---

**SamWilsn** (2025-04-15):

You may want to explore adding [ERC-165](https://eips.ethereum.org/EIPS/eip-165) support.

You also may want to add some events to your interface that are emit when tokens are merged/split?

---

**nitin312** (2025-04-17):

Thanks for your feedback

