---
source: magicians
topic_id: 12173
title: "EIP-6150: Hierarchical NFTs, an extension to ERC-721"
author: fewwwww
date: "2022-12-16"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-6150-hierarchical-nfts-an-extension-to-erc-721/12173
views: 4010
likes: 19
posts_count: 18
---

# EIP-6150: Hierarchical NFTs, an extension to ERC-721

## Abstract

This standard is an extension to ERC-721. It proposes a multi-layer filesystem-like hierarchical NFTs. This standard provides interfaces to get parent NFT or children NFTs and whether NFT is a leaf node or root node, maintaining the hierarchical relationship among them.

## Motivation

This EIP standardizes the interface of filesystem-like hierarchical NFTs and provides a reference implementation.

Hierarchy structure is commonly implemented for file systems by operating systems such as Linux Filesystem Hierarchy (FHS).

[![linux-hierarchy](https://ethereum-magicians.org/uploads/default/original/2X/8/8969a7094d8c423f6bf81b2555454b2e06744bd8.png)linux-hierarchy531×307 6.95 KB](https://ethereum-magicians.org/uploads/default/8969a7094d8c423f6bf81b2555454b2e06744bd8)

Websites often use a directory and category hierarchy structure, such as eBay (Home → Electronics → Video Games → Xbox → Products), and Twitter (Home → Lists → List → Tweets), and Reddit (Home → r/ ethereum → Posts → Hot).

A single smart contract can be the `root`, managing every directory/category as individual NFT and hierarchy relations of NFTs. Each NFT’s `tokenURI` may be another contract address, a website link, or any form of metadata.

The advantages and the advancement of the Ethereum ecosystem of using this standard include:

- Complete on-chain storage of hierarchy, which can also be governed on-chain by additional DAO contract
- Only need a single contract to manage and operate the hierarchical relations
- Transferrable directory/category ownership as NFT, which is great for use cases such as on-chain forums
- Easy and permissionless data access to the hierarchical structure by front-end
- Ideal structure for traditional applications such as e-commerce, or forums
- Easy-to-understand interfaces for developers, which are similar to Linux filesystem commands in concept

The use cases can include:

- On-chain forum, like Reddit
- On-chain social media, like Twitter
- On-chain corporation, for managing organizational structures
- On-chain e-commerce platforms, like eBay or individual stores
- Any application with tree-like structures

In the future, with the development of the data availability solutions of Ethereum and an external permissionless data retention network, the content (posts, listed items, or tweets) of these platforms can also be entirely stored on-chain, thus realizing fully decentralized applications.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Every EIP-6150 compliant contract must implement the EIP-6150, EIP-721 and EIP-165 interfaces.

```solidity
pragma solidity ^0.8.0;

interface IERC6150 /* is IERC721, IERC165 */ {
    /**
     * @notice Emitted when `tokenId` token under `parentId` is minted.
     * @param minter The address of minter
     * @param to The address received token
     * @param parentId The id of parent token, if it's zero, it means minted `tokenId` is a root token.
     * @param tokenId The id of minted token, required to be greater than zero
     */
    event Minted(
        address indexed minter,
        address indexed to,
        uint256 parentId,
        uint256 tokenId
    );

    /**
     * @notice Get the parent token of `tokenId` token.
     * @param tokenId The child token
     * @return parentId The Parent token found
     */
    function parentOf(uint256 tokenId) external view returns (uint256 parentId);

    /**
     * @notice Get the children tokens of `tokenId` token.
     * @param tokenId The parent token
     * @return childrenIds The array of children tokens
     */
    function childrenOf(
        uint256 tokenId
    ) external view returns (uint256[] memory childrenIds);

    /**
     * @notice Check the `tokenId` token if it is a root token.
     * @param tokenId The token want to be checked
     * @return Return `true` if it is a root token; if not, return `false`
     */
    function isRoot(uint256 tokenId) external view returns (bool);

    /**
     * @notice Check the `tokenId` token if it is a leaf token.
     * @param tokenId The token want to be checked
     * @return Return `true` if it is a leaf token; if not, return `false`
     */
    function isLeaf(uint256 tokenId) external view returns (bool);
}
```

Optional Extension: Enumerable

```solidity
interface IERC6150Enumerable is IERC6150 /* IERC721Enumerable */ {
    /**
     * @notice Get total amount of children tokens under `parentId` token.
     * @dev If `parentId` is zero, it means get total amount of root tokens.
     * @return The total amount of children tokens under `parentId` token.
     */
    function childrenCountOf(uint256 parentId) external view returns (uint256);

    /**
     * @notice Get the token at the specified index of all children tokens under `parentId` token.
     * @dev If `parentId` is zero, it means get root token.
     * @return The token ID at `index` of all chlidren tokens under `parentId` token.
     */
    function childOfParentByIndex(
        uint256 parentId,
        uint256 index
    ) external view returns (uint256);

    /**
     * @notice Get the index position of specified token in the children enumeration under specified parent token.
     * @dev Throws if the `tokenId` is not found in the children enumeration.
     * If `parentId` is zero, means get root token index.
     * @param parentId The parent token
     * @param tokenId The specified token to be found
     * @return The index position of `tokenId` found in the children enumeration
     */
    function indexInChildrenEnumeration(
        uint256 parentId,
        uint256 tokenId
    ) external view returns (uint256);
}
```

Optional Extension: Burnable

```solidity
interface IERC6150Burnable is IERC6150 {
    /**
     * @notice Burn the `tokenId` token.
     * @dev Throws if `tokenId` is not a leaf token.
     * Throws if `tokenId` is not a valid NFT.
     * Throws if `owner` is not the owner of `tokenId` token.
     * Throws unless `msg.sender` is the current owner, an authorized operator, or the approved address for this token.
     * @param tokenId The token to be burnt
     */
    function safeBurn(uint256 tokenId) external;

    /**
     * @notice Batch burn tokens.
     * @dev Throws if one of `tokenIds` is not a leaf token.
     * Throws if one of `tokenIds` is not a valid NFT.
     * Throws if `owner` is not the owner of all `tokenIds` tokens.
     * Throws unless `msg.sender` is the current owner, an authorized operator, or the approved address for all `tokenIds`.
     * @param tokenIds The tokens to be burnt
     */
    function safeBatchBurn(uint256[] memory tokenIds) external;
}
```

Optional Extension: ParentTransferable

```solidity
interface IERC6150ParentTransferable is IERC6150 {
    /**
     * @notice Emitted when the parent of `tokenId` token changed.
     * @param tokenId The token changed
     * @param oldParentId Previous parent token
     * @param newParentId New parent token
     */
    event ParentTransferred(
        uint256 tokenId,
        uint256 oldParentId,
        uint256 newParentId
    );

    /**
     * @notice Transfer parentship of `tokenId` token to a new parent token
     * @param newParentId New parent token id
     * @param tokenId The token to be changed
     */
    function transferParent(uint256 newParentId, uint256 tokenId) external;

    /**
     * @notice Batch transfer parentship of `tokenIds` to a new parent token
     * @param newParentId New parent token id
     * @param tokenIds Array of token ids to be changed
     */
    function batchTransferParent(
        uint256 newParentId,
        uint256[] memory tokenIds
    ) external;
}
```

Optional Extension: Access Control

```solidity
interface IERC6150AccessControl is IERC6150 {
    /**
     * @notice Check the account whether a admin of `tokenId` token.
     * @dev Each token can be set more than one admin. Admin have permission to do something to the token, like mint child token,
     * or burn token, or transfer parentship.
     * @param tokenId The specified token
     * @param account The account to be checked
     * @return If the account has admin permission, return true; otherwise, return false.
     */
    function isAdminOf(uint256 tokenId, address account)
        external
        view
        returns (bool);

    /**
     * @notice Check whether the specified parent token and account can mint children tokens
     * @dev If the `parentId` is zero, check whether account can mint root nodes
     * @param parentId The specified parent token to be checked
     * @param account The specified account to be checked
     * @return If the token and account has mint permission, return true; otherwise, return false.
     */
    function canMintChildren(
        uint256 parentId,
        address account
    ) external view returns (bool);

    /**
     * @notice Check whether the specified token can be burnt by specified account
     * @param tokenId The specified token to be checked
     * @param account The specified account to be checked
     * @return If the tokenId can be burnt by account, return true; otherwise, return false.
     */
    function canBurnTokenByAccount(uint256 tokenId, address account)
        external
        view
        returns (bool);
}
```

## Rationale

As mentioned in the abstract, this EIP’s goal is to have a simple interface for supporting Hierarchical NFTs. Here are a few design decisions and why they were made:

### Relationship between NFTs

All NFTs will make up a hierarchical relationship tree. Each NFT is a node of the tree, maybe as a root node or a leaf node, as a parent node or a child node.

EIP-6150 standardizes the event `Minted` to indicate the parent and child relationship when minting a new node. When a root node is minted, parentId should be zero. That means a token id of zero could not be a real node. So a real node token id must be greater than zero.

In a hierarchical tree, it’s common to query upper and lower nodes. So EIP-6150 standardizes function `parentOf` to get the parent node of the specified node and standardizes function `childrenOf` to get all children nodes.

Functions `isRoot` and `isLeaf` can check if one node is a root node or a leaf node, which would be very useful for many cases.

### Enumerable Extension

EIP-6150 standardizes three functions as an extension to support enumerable queries involving children nodes. Each function all have param `parentId`, for compatibility, when the `parentId` specified zero means query root nodes.

### ParentTransferable Extension

In some cases, such as filesystem, a directory or a file could be moved from one directory to another. So EIP-6150 adds ParentTransferable Extension to support this situation.

### Access Control

In a hierarchical structure, usually, there is more than one account has permission to operate a node, like mint children nodes, transfer node, burn node. EIP-6150 adds a few functions as standard to check access control permissions.

## Replies

**xinbenlv** (2022-12-17):

Love to hear how does the author consider the relationship between this EIP and

- EIP-6059: Parent-Governed Nestable Non-Fungible Tokens
- EIP-3525: Semi-Fungible Token

---

**fewwwww** (2022-12-20):

Thanks for bringing up these two EIPs! They are both great extensions to EIP-721.

- EIP-6059 is more focusing on Nestable ownership of an NFT and the ability that an NFT can be owned by another NFT. In EIP-6150, we also have similar design, but on a bigger picture, we are focusing on the hierarchy of the whole collection, and its direct benefits to the application design like websites and forums.
- EIP-3525 is combining EIP-20 and EIP-721. The combination creates more use cases such as bond, or vesting plans as semi-fungible token. We do see some potential that we can pair EIP-6150 with EIP-3525 (like setting up several EIP-6150 slots for different posts of one forum on the same topics; or setting up multiple identical but parallel EIP-6150 teams in an organization’s corporate structure), so that both EIPs can be extended.

---

**Pandapip1** (2022-12-20):

What is the advantage of this EIP over EIP-5219?

---

**fewwwww** (2022-12-20):

EIP-5219 is similar to EIP-4804 that defines some standard for requesting on-chain resources.

EIP-6150 is not defining the requesting and querying process, but standardizing the smart contract structure of hierarchy NFTs (which will make it easier for building the rest of the application). The smart contract itself can be extended by EIPs like 5219 and 4804 for creating the front-end or other additional services.

---

**leo** (2022-12-22):

Love the idea of hierarchical NFTs and we are actually thinking of similar idea for a tree-like structure.

How to prevent a loop in the structure?

---

**leo** (2022-12-22):

Also I feel the “Enumerable” extension is important for this structure, but “Burnable”, and “ParentTransferable”, “Access Control” are too much for this ERC.  I suggest keeping a simpler ERC instead of put everything into one ERC. Other extensions can be pluggable extensions, not necessarily part of the main proposal.

---

**Pandapip1** (2022-12-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/leo/48/7855_2.png) leo:

> How to prevent a loop in the structure?



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Bloom_filter)





###

A Bloom filter is a space-efficient probabilistic data structure, conceived by Burton Howard Bloom in 1970, that is used to test whether an element is a member of a set. False positive matches are possible, but false negatives are not – in other words, a query returns either "possibly in set" or "definitely not in set". Elements can be added to the set, but not removed (though this can be addressed with the counting Bloom filter variant); the more items added, the larger the probability of false ...

---

**stoicdev0** (2022-12-22):

The way we do it on 6059 (nestable NFTs among different collections, but hierarchy is not the focus) is to get the parent iteratively until we find an owner which is not an NFT, checking that we did not find the same token on the process. This could become really expensive so we added a limit of checks.

I think same approach could be applied here.

---

**fewwwww** (2022-12-22):

Yes, I agree.

Including all those extension into one EIP is too much, so that we describe `Enumerable`, `Burnable`, `ParentTransferable`, and `Access Control` as optional extension to our EIP-6150.

Those are considered as add-ons to hierarchy NFT (nice to have for full functionality, but not mandatory).

---

**fewwwww** (2022-12-23):

For preventing a loop in the structure, the core issues when minting are:

- parentId exists before
- Newly added tokenId does not exist before

You can also take a look at our [demo implementation](https://github.com/ethereum/EIPs/tree/master/assets/eip-6150/contracts) with all those checks.

---

**fewwwww** (2023-01-05):

EIP-6150 is now in `review` status. Any review and suggestion is great for this proposal’s exploration!

---

**sullof** (2023-01-08):

This is very interesting. I was looking for something like this without finding anything, then I wrote this code



      [github.com](https://github.com/cruna-cc/DS-protocol)




  ![image](https://opengraph.githubassets.com/004e795a9759b72d72558e98c2c9777d/cruna-cc/DS-protocol)



###



A protocol to handle dominant and subordinate NFTs










and discussing it I get a link to your proposal.

The difference I think is in scope. Your proposal wants to manage a large number of cases, being very generic and powerful. My proposal wants to solve a single problem with the simplest solution possible.

While I will study your proposal, to see if I can use for what I need, I would appreciate your comments on mine. Thanks.

---

**fewwwww** (2023-01-08):

Thanks for sharing this!

Your implementation of erc721subordinate really implements the subordinate and dominant hierarchical structure with simplicity.

I think if you want to make it compatible with this proposal, the dominant token will be the `root` token, and the subordinate token will be the `leaf` tokens.

---

**sullof** (2023-01-10):

That makes sense for new contracts.

However, the problem I am trying to solve is how to bind a new NFT to an existing NFT that has been deployed a while ago and is immutable (i.e., there is not way to make it a root).

---

**keegan** (2023-01-11):

We have appended [more implementations](https://github.com/ethereum/EIPs/tree/master/assets/eip-6150/contracts) for EIP-6150, including all interfaces, more discussion is welcome.

---

**leo** (2023-01-20):

Is it possible to combine isRoot and isLeaf together, to return the number of children? So we know if number of children is 0, it is a leaf nodes.  In this case, the number of children is also useful in applications.

---

**keegan** (2023-01-23):

No need to combine isRoot and isLeaf, optional extension *IERC6150Enumerable* has the *childrenCountOf* function to get the number of children. And isLeaf is more efficient on many cases, use childrenCountOf to check that if it is a leaf, you need to check the number == 0 yourself, that’s not so smooth.

