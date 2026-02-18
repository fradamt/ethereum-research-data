---
source: magicians
topic_id: 11914
title: "EIP-6059: Parent-Governed Nestable Non-Fungible Tokens"
author: ThunderDeliverer
date: "2022-11-28"
category: EIPs
tags: [nft, token]
url: https://ethereum-magicians.org/t/eip-6059-parent-governed-nestable-non-fungible-tokens/11914
views: 5263
likes: 22
posts_count: 36
---

# EIP-6059: Parent-Governed Nestable Non-Fungible Tokens

We are proposing a Parent-Governed Nestable Non-Fungible Tokens standard, where one token can own and manage multiple other tokens. The whole concept has been outlined in the [RMRK Nestable documentation](https://docs.rmrk.app/lego1-nested) as well as our EIP:

---

## eip: 6059
title: Parent-Governed Nestable Non-Fungible Tokens
description: An interface for Nestable Non-Fungible Tokens with emphasis on parent token’s control over the relationship.
author: , , , ,
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2022-11-15
requires: 165, 721

## Abstract

The Parent-Governed Nestable NFT standard extends the [EIP-721](https://eips.ethereum.org/EIPS/eip-721) by allowing for a new inter-NFT relationship and interaction.

At its core, the idea behind the proposal is simple: the owner of an NFT does not have to be an Externally Owned Account (EOA) or a smart contract, it can also be an NFT.

The process of nesting an NFT into another is functionally identical to sending it to another user. The process of sending a token out of another one involves issuing a transaction from the account owning the parent token.

An NFT can be owned by a single other NFT, but can in turn have a number of NFTs that it owns. This proposal establishes the framework for the parent-child relationships of NFTs. A parent token is the one that owns another token. A child token is a token that is owned by another token. A token can be both a parent and child at the same time. Child tokens of a given token can be fully managed by the parent token’s owner, but can be proposed by anyone.

[![eip-6059-nestable-tokens](https://ethereum-magicians.org/uploads/default/original/2X/a/ab1528c1df36ec917374ba8268dc0827927bdee9.png)eip-6059-nestable-tokens681×233 13.9 KB](https://ethereum-magicians.org/uploads/default/ab1528c1df36ec917374ba8268dc0827927bdee9)

The graph illustrates how a child token can also be a parent token, but both are still administered by the root parent token’s owner.

## Motivation

With NFTs being a widespread form of tokens in the Ethereum ecosystem and being used for a variety of use cases, it is time to standardize additional utility for them. Having the ability for tokens to own other tokens allows for greater utility, usability and forward compatibility.

In the four years since [EIP-721](https://eips.ethereum.org/EIPS/eip-721) was published, the need for additional functionality has resulted in countless extensions. This EIP improves upon EIP-721 in the following areas:

- Bundling
- Collecting
- Membership
- Delegation

### Bundling

One of the most frequent uses of [EIP-721](https://eips.ethereum.org/EIPS/eip-721) is to disseminate the multimedia content that is tied to the tokens. In the event that someone wants to offer a bundle of NFTs from various collections, there is currently no easy way of bundling all of these together and handle their sale as a single transaction. This proposal introduces a standardized way of doing so. Nesting all of the tokens into a simple bundle and selling that bundle would transfer the control of all of the tokens to the buyer in a single transaction.

### Collecting

A lot of NFT consumers collect them based on countless criteria. Some aim for utility of the tokens, some for the uniqueness, some for the visual appeal, etc. There is no standardized way to group the NFTs tied to a specific account. By nesting NFTs based on their owner’s preference, this proposal introduces the ability to do it. The root parent token could represent a certain group of tokens and all of the children nested into it would belong to it.

The rise of soulbound, non-transferable, tokens, introduces another need for this proposal. Having a token with multiple soulbound traits (child tokens), allows for numerous use cases. One concrete example of this can be drawn from supply trains use case. A shipping container, represented by an NFT with its own traits, could have multiple child tokens denoting each leg of its journey.

### Membership

A common utility attached to NFTs is a membership to a Decentralised Autonomous Organization (DAO) or to some other closed-access group. Some of these organizations and groups occasionally mint NFTs to the current holders of the membership NFTs. With the ability to nest mint a token into a token, such minting could be simplified, by simply minting the bonus NFT directly into the membership one.

### Delegation

One of the core features of DAOs is voting and there are various approaches to it. One such mechanic is using fungible voting tokens where members can delegate their votes by sending these tokens to another member. Using this proposal, delegated voting could be handled by nesting your voting NFT into the one you are delegating your votes to and transferring it when the member no longer wishes to delegate their votes.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119.

```solidity
/// @title EIP-6059 Parent-Governed Nestable Non-Fungible Tokens
/// @dev See https://eips.ethereum.org/EIPS/eip-6059
/// @dev Note: the ERC-165 identifier for this interface is 0x60b766e5.

pragma solidity ^0.8.16;

interface INestable {
    /**
     * @notice The core struct of ownership.
     * @dev The `DirectOwner` struct is used to store information of the next immediate owner, be it the parent token,
     * an `ERC721Receiver` contract or an externally owned account.
     * @dev If the token is not owned by an NFT, the `tokenId` MUST equal `0`.
     * @param tokenId ID of the parent token
     * @param ownerAddress Address of the owner of the token. If the owner is another token, then the address MUST be
     *  the one of the parent token's collection smart contract. If the owner is externally owned account, the address
     *  MUST be the address of this account
     * @param isNft A boolean value signifying whether the token is owned by another token (`true`) or by an externally
     *  owned account (`false`)
     */
    struct DirectOwner {
        uint256 tokenId;
        address ownerAddress;
        bool isNft;
    }

    /**
     * @notice Used to notify listeners that the token is being transferred.
     * @dev Emitted when `tokenId` token is transferred from `from` to `to`.
     * @param from Address of the previous immediate owner, which is a smart contract if the token was nested.
     * @param to Address of the new immediate owner, which is a smart contract if the token is being nested.
     * @param fromTokenId ID of the previous parent token. If the token was not nested before, the value MUST be `0`
     * @param toTokenId ID of the new parent token. If the token is not being nested, the value MUST be `0`
     * @param tokenId ID of the token being transferred
     */
    event NestTransfer(
        address indexed from,
        address indexed to,
        uint256 fromTokenId,
        uint256 toTokenId,
        uint256 indexed tokenId
    );

    /**
     * @notice Used to notify listeners that a new token has been added to a given token's pending children array.
     * @dev Emitted when a child NFT is added to a token's pending array.
     * @param tokenId ID of the token that received a new pending child token
     * @param childIndex Index of the proposed child token in the parent token's pending children array
     * @param childAddress Address of the proposed child token's collection smart contract
     * @param childId ID of the child token in the child token's collection smart contract
     */
    event ChildProposed(
        uint256 indexed tokenId,
        uint256 childIndex,
        address indexed childAddress,
        uint256 indexed childId
    );

    /**
     * @notice Used to notify listeners that a new child token was accepted by the parent token.
     * @dev Emitted when a parent token accepts a token from its pending array, migrating it to the active array.
     * @param tokenId ID of the token that accepted a new child token
     * @param childIndex Index of the newly accepted child token in the parent token's active children array
     * @param childAddress Address of the child token's collection smart contract
     * @param childId ID of the child token in the child token's collection smart contract
     */
    event ChildAccepted(
        uint256 indexed tokenId,
        uint256 childIndex,
        address indexed childAddress,
        uint256 indexed childId
    );

    /**
     * @notice Used to notify listeners that all pending child tokens of a given token have been rejected.
     * @dev Emitted when a token removes all a child tokens from its pending array.
     * @param tokenId ID of the token that rejected all of the pending children
     */
    event AllChildrenRejected(uint256 indexed tokenId);

    /**
     * @notice Used to notify listeners a child token has been transferred from parent token.
     * @dev Emitted when a token transfers a child from itself, transferring ownership.
     * @param tokenId ID of the token that transferred a child token
     * @param childIndex Index of a child in the array from which it is being transferred
     * @param childAddress Address of the child token's collection smart contract
     * @param childId ID of the child token in the child token's collection smart contract
     * @param fromPending A boolean value signifying whether the token was in the pending child tokens array (`true`) or
     *  in the active child tokens array (`false`)
     */
    event ChildTransferred(
        uint256 indexed tokenId,
        uint256 childIndex,
        address indexed childAddress,
        uint256 indexed childId,
        bool fromPending
    );

    /**
     * @notice The core child token struct, holding the information about the child tokens.
     * @return tokenId ID of the child token in the child token's collection smart contract
     * @return contractAddress Address of the child token's smart contract
     */
    struct Child {
        uint256 tokenId;
        address contractAddress;
    }

    /**
     * @notice Used to retrieve the *root* owner of a given token.
     * @dev The *root* owner of the token is the top-level owner in the hierarchy which is not an NFT.
     * @dev If the token is owned by another NFT, it MUST recursively look up the parent's root owner.
     * @param tokenId ID of the token for which the *root* owner has been retrieved
     * @return owner The *root* owner of the token
     */
    function ownerOf(uint256 tokenId) external view returns (address owner);

    /**
     * @notice Used to retrieve the immediate owner of the given token.
     * @dev If the immediate owner is another token, the address returned, MUST be the one of the parent token's
     *  collection smart contract.
     * @param tokenId ID of the token for which the direct owner is being retrieved
     * @return address Address of the given token's owner
     * @return uint256 The ID of the parent token. MUST be `0` if the owner is not an NFT
     * @return bool The boolean value signifying whether the owner is an NFT or not
     */
    function directOwnerOf(uint256 tokenId)
        external
        view
        returns (
            address,
            uint256,
            bool
        );

    /**
     * @notice Used to burn a given token.
     * @dev When a token is burned, all of its child tokens are recursively burned as well.
     * @dev When specifying the maximum recursive burns, the execution MUST be reverted if there are more children to be
     *  burned.
     * @dev Setting the `maxRecursiveBurn` value to 0 SHOULD only attempt to burn the specified token and MUST revert if
     *  there are any child tokens present.
     * @param tokenId ID of the token to burn
     * @param maxRecursiveBurns Maximum number of tokens to recursively burn
     * @return uint256 Number of recursively burned children
     */
    function burn(uint256 tokenId, uint256 maxRecursiveBurns)
        external
        returns (uint256);

    /**
     * @notice Used to add a child token to a given parent token.
     * @dev This adds the child token into the given parent token's pending child tokens array.
     * @dev The destination token MUST NOT be a child token of the token being transferred or one of its downstream
     *  child tokens.
     * @dev This method MUST NOT be called directly. It MUST only be called from an instance of `INestable` as part of a
        `nestMint`, `nestTransfer` or `transferChild` to an NFT.
     * @dev Requirements:
     *
     *  - `directOwnerOf` on the child contract MUST resolve to the called contract.
     *  - the pending array of the parent contract MUST not be full.
     * @param parentId ID of the parent token to receive the new child token
     * @param childId ID of the new proposed child token
     */
    function addChild(uint256 parentId, uint256 childId) external;

    /**
     * @notice Used to accept a pending child token for a given parent token.
     * @dev This moves the child token from parent token's pending child tokens array into the active child tokens
     *  array.
     * @param parentId ID of the parent token for which the child token is being accepted
     * @param childIndex Index of the child token to accept in the pending children array of a given token
     * @param childAddress Address of the collection smart contract of the child token expected to be at the specified
     *  index
     * @param childId ID of the child token expected to be located at the specified index
     */
    function acceptChild(
        uint256 parentId,
        uint256 childIndex,
        address childAddress,
        uint256 childId
    ) external;

    /**
     * @notice Used to reject all pending children of a given parent token.
     * @dev Removes the children from the pending array mapping.
     * @dev The children's ownership structures are not updated.
     * @dev Requirements:
     *
     * - `parentId` MUST exist
     * @param parentId ID of the parent token for which to reject all of the pending tokens
     * @param maxRejections Maximum number of expected children to reject, used to prevent from
     *  rejecting children which arrive just before this operation.
     */
    function rejectAllChildren(uint256 parentId, uint256 maxRejections) external;

    /**
     * @notice Used to transfer a child token from a given parent token.
     * @dev MUST remove the child from the parent's active or pending children.
     * @dev When transferring a child token, the owner of the token MUST be set to `to`, or not updated in the event of `to`
     *  being the `0x0` address.
     * @param tokenId ID of the parent token from which the child token is being transferred
     * @param to Address to which to transfer the token to
     * @param destinationId ID of the token to receive this child token (MUST be 0 if the destination is not a token)
     * @param childIndex Index of a token we are transferring, in the array it belongs to (can be either active array or
     *  pending array)
     * @param childAddress Address of the child token's collection smart contract
     * @param childId ID of the child token in its own collection smart contract
     * @param isPending A boolean value indicating whether the child token being transferred is in the pending array of the
     *  parent token (`true`) or in the active array (`false`)
     * @param data Additional data with no specified format, sent in call to `to`
     */
    function transferChild(
        uint256 tokenId,
        address to,
        uint256 destinationId,
        uint256 childIndex,
        address childAddress,
        uint256 childId,
        bool isPending,
        bytes data
    ) external;

    /**
     * @notice Used to retrieve the active child tokens of a given parent token.
     * @dev Returns array of Child structs existing for parent token.
     * @dev The Child struct consists of the following values:
     *  [
     *      tokenId,
     *      contractAddress
     *  ]
     * @param parentId ID of the parent token for which to retrieve the active child tokens
     * @return struct[] An array of Child structs containing the parent token's active child tokens
     */
    function childrenOf(uint256 parentId)
        external
        view
        returns (Child[] memory);

    /**
     * @notice Used to retrieve the pending child tokens of a given parent token.
     * @dev Returns array of pending Child structs existing for given parent.
     * @dev The Child struct consists of the following values:
     *  [
     *      tokenId,
     *      contractAddress
     *  ]
     * @param parentId ID of the parent token for which to retrieve the pending child tokens
     * @return struct[] An array of Child structs containing the parent token's pending child tokens
     */
    function pendingChildrenOf(uint256 parentId)
        external
        view
        returns (Child[] memory);

    /**
     * @notice Used to retrieve a specific active child token for a given parent token.
     * @dev Returns a single Child struct locating at `index` of parent token's active child tokens array.
     * @dev The Child struct consists of the following values:
     *  [
     *      tokenId,
     *      contractAddress
     *  ]
     * @param parentId ID of the parent token for which the child is being retrieved
     * @param index Index of the child token in the parent token's active child tokens array
     * @return struct A Child struct containing data about the specified child
     */
    function childOf(uint256 parentId, uint256 index)
        external
        view
        returns (Child memory);

    /**
     * @notice Used to retrieve a specific pending child token from a given parent token.
     * @dev Returns a single Child struct locating at `index` of parent token's active child tokens array.
     * @dev The Child struct consists of the following values:
     *  [
     *      tokenId,
     *      contractAddress
     *  ]
     * @param parentId ID of the parent token for which the pending child token is being retrieved
     * @param index Index of the child token in the parent token's pending child tokens array
     * @return struct A Child struct containing data about the specified child
     */
    function pendingChildOf(uint256 parentId, uint256 index)
        external
        view
        returns (Child memory);

    /**
     * @notice Used to transfer the token into another token.
     * @dev The destination token MUST NOT be a child token of the token being transferred or one of its downstream
     *  child tokens.
     * @param from Address of the direct owner of the token to be transferred
     * @param to Address of the receiving token's collection smart contract
     * @param tokenId ID of the token being transferred
     * @param destinationId ID of the token to receive the token being transferred
     */
    function nestTransferFrom(
        address from,
        address to,
        uint256 tokenId,
        uint256 destinationId
    ) external;
}
```

ID MUST never be a `0` value, as this proposal uses `0` values do signify that the token/destination is not an NFT.

## Rationale

Designing the proposal, we considered the following questions:

1. How to name the proposal?

In an effort to provide as much information about the proposal we identified the most important aspect of the proposal; the parent centered control over nesting. The child token’s role is only to be able to be `Nestable` and support a token owning it. This is how we landed on the `Parent-Centered` part of the title.

1. Why is automatically accepting a child using EIP-712 permit-style signatures not a part of this proposal?

For consistency. This proposal extends EIP-721 which already uses 1 transaction for approving operations with tokens. It would be inconsistent to have this and also support signing messages for operations with assets.

1. Why use indexes?

To reduce the gas consumption. If the token ID was used to find which token to accept or reject, iteration over arrays would be required and the cost of the operation would depend on the size of the active or pending children arrays. With the index, the cost is fixed. Lists of active and pending children per token need to be maintained, since methods to get them are part of the proposed interface.

To avoid race conditions in which the index of a token changes, the expected token ID as well as the expected token’s collection smart contract is included in operations requiring token index, to verify that the token being accessed using the index is the expected one.

Implementation that would internally keep track of indices using mapping was attempted. The minimum cost of accepting a child token was increased by over 20% and the cost of minting has increased by over 15%. We concluded that it is not necessary for this proposal and can be implemented as an extension for use cases willing to accept the increased transaction cost this incurs. In the sample implementation provided, there are several hooks which make this possible.

1. Why is the pending children array limited instead of supporting pagination?

The pending child tokens array is not meant to be a buffer to collect the tokens that the root owner of the parent token wants to keep, but not enough to promote them to active children. It is meant to be an easily traversable list of child token candidates and should be regularly maintained; by either accepting or rejecting proposed child tokens. There is also no need for the pending child tokens array to be unbounded, because active child tokens array is.

Another benefit of having bounded child tokens array is to guard against spam and griefing. As minting malicious or spam tokens could be relatively easy and low-cost, the bounded pending array assures that all of the tokens in it are easy to identify and that legitimate tokens are not lost in a flood of spam tokens, if one occurs.

A consideration tied to this issue was also how to make sure, that a legitimate token is not accidentally rejected when clearing the pending child tokens array. We added the maximum pending children to reject argument to the clear pending child tokens array call. This assures that only the intended number of pending child tokens is rejected and if a new token is added to the pending child tokens array during the course of preparing such call and executing it, the clearing of this array SHOULD result in a reverted transaction.

1. Should we allow tokens to be nested into one of its children?

The proposal enforces that a parent token can’t be nested into one of its child token, or downstream child tokens for that matter. A parent token and its children are all managed by the parent token’s root owner. This means that if a token would be nested into one of its children, this would create the ownership loop and none of the tokens within the loop could be managed anymore.

1. Why is there not a “safe” nest transfer method?

`nestTransfer` is always “safe” since it MUST check for `INestable` compatibility on the destination.

1. How does this proposal differ from the other proposals trying to address a similar problem?

This interface allows for tokens to both be sent to and receive other tokens. The propose-accept and parent governed patterns allow for a more secure use. The backward compatibility is only added for EIP-721, allowing for a simpler interface. The proposal also allows for different collections to inter-operate, meaning that nesting is not locked to a single smart contract, but can be executed between completely separate NFT collections.

### Propose-Commit pattern for child token management

Adding child tokens to a parent token MUST be done in the form of propose-commit pattern to allow for limited mutability by a 3rd party. When adding a child token to a parent token, it is first placed in a *“Pending”* array, and MUST be migrated to the *“Active”* array by the parent token’s root owner. The *“Pending”* child tokens array SHOULD be limited to 128 slots to prevent spam and griefing.

The limitation that only the root owner can accept the child tokens also introduces a trust inherent to the proposal. This ensures that the root owner of the token has full control over the token. No one can force the user to accept a child if they don’t want to.

### Parent Governed pattern

The parent NFT of a nested token and the parent’s root owner are in all aspects the true owners of it. Once you send a token to another one you give up ownership.

We continue to use EIP-721’s `ownerOf` functionality which will now recursively look up through parents until it finds an address which is not an NFT, this is referred to as the *root owner*. Additionally we provide the `directOwnerOf` which returns the most immediate owner of a token using 3 values: the owner address, the tokenId which MUST be 0 if the direct owner is not an NFT, and a flag indicating whether or not the parent is an NFT.

The root owner or an approved party MUST be able do the following operations on children: `acceptChild`, `rejectAllChildren` and `transferChild`.

The root owner or an approved party MUST also be allowed to do these operations only when token is not owned by an NFT: `transferFrom`, `safeTransferFrom`, `nestTransferFrom`, `burn`.

If the token is owned by an NFT, only the parent NFT itself MUST be allowed to execute the operations listed above. Transfers MUST be done from the parent token, using `transferChild`, this method in turn SHOULD call `nestTransferFrom` or `safeTransferFrom` in the child token’s smart contract, according to whether the destination is an NFT or not. For burning, tokens must first be transferred to an EOA and then burned.

We add this restriction to prevent inconsistencies on parent contracts, since only the `transferChild` method takes care of removing the child from the parent when it is being transferred out of it.

### Child token management

This proposal introduces a number of child token management functions. In addition to the permissioned migration from *“Pending”* to *“Active”* child tokens array, the main token management function from this proposal is the `tranferChild` function. The following state transitions of a child token are available with it:

1. Reject child token
2. Abandon child token
3. Unnest child token
4. Transfer the child token to an EOA or an ERC721Receiver
5. Transfer the child token into a new parent token

To better understand how these state transitions are achieved, we have to look at the available parameters passed to `transferChild`:

```solidity
    function transferChild(
        uint256 tokenId,
        address to,
        uint256 destinationId,
        uint256 childIndex,
        address childAddress,
        uint256 childId,
        bool isPending,
        bytes data
    ) external;
```

Based on the desired state transitions, the values of these parameters have to be set accordingly (any parameters not set in the following examples depend on the child token being managed):

1. Reject child token

![eip-6059-reject-child](https://ethereum-magicians.org/uploads/default/original/2X/4/4b8b52d69ca615208e74a8143d6c6b67a72601aa.png)

1. Abandon child token

![eip-6059-abandon-child](https://ethereum-magicians.org/uploads/default/original/2X/0/09cb1ea5d73b65772eb3a491fe51038295fbf015.png)

1. Unnest child token

![eip-6059-unnest-child](https://ethereum-magicians.org/uploads/default/original/2X/0/0de9e0ea1491158c0f37bb55a1273177999c8156.png)

1. Transfer the child token to an EOA or an ERC721Receiver

![eip-6059-transfer-child-to-eoa](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b3aff4ba9e50e0a5eda166d1f731c9a61c6477db_2_690x41.png)

1. Transfer the child token into a new parent token

![eip-6059-transfer-child-to-token](https://ethereum-magicians.org/uploads/default/optimized/2X/f/f4873d7ca99efaa8a01808afffb0d5067130546e_2_690x31.png)

This state change places the token in the pending array of the new parent token. The child token still needs to be accepted by the new parent token’s root owner in order to be placed into the active array of that token.

## Backwards Compatibility

The Nestable token standard has been made compatible with [EIP-721](https://eips.ethereum.org/EIPS/eip-721) in order to take advantage of the robust tooling available for implementations of EIP-721 and to ensure compatibility with existing EIP-721 infrastructure.

## Test Cases

Tests are included in [nestable.ts](https://github.com/rmrk-team/EIPs/tree/nestable-eip/assets/eip-6059/test/nestable.ts).

To run them in terminal, you can use the following commands:

```auto
cd ../assets/eip-6059
npm install
npx hardhat test
```

## Reference Implementation

See [NestableToken.sol](https://github.com/rmrk-team/EIPs/tree/nestable-eip/assets/eip-6059/contracts/NestableToken.sol).

## Security Considerations

The same security considerations as with [EIP-721](https://eips.ethereum.org/EIPS/eip-721) apply: hidden logic may be present in any of the functions, including burn, add resource, accept resource, and more.

Caution is advised when dealing with non-audited contracts.

## Copyright

Copyright and related rights waived via [CC0](https://github.com/rmrk-team/EIPs/tree/nestable-eip/LICENSE.md).

## Replies

**Joe** (2022-12-01):

Hey it’s good idea. But why can’t I search your draft on the EIP list?



      [Ethereum Improvement Proposals](https://eips.ethereum.org/all)





###



Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

---

**ThunderDeliverer** (2022-12-01):

Hey, thank you! We are still waiting for the proposal to be merged to the EIP repository. It’s currently reachable in the PR: [Propose Parent-Governed Nestable Non-Fungible Tokens standard by ThunderDeliverer · Pull Request #6059 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/6059)

Once merged, it will be available at the https://eips.ethereum.org/EIPS/eip-6059

---

**manboy** (2022-12-15):

Nice,

here is an example of a DAO-governed NFT used for representing membership in a DAO. The NFT also “holds” other tokens. If you are interested: [GitHub - dOrgTech/passport: DAO membership representation with Passport (ERC721: Votes), Reputation (ERC20: Votes + Snapshot), and Badges (ERC1155). Passports can only be minted/moved/burned by the DAO. Other tokens will "follow" the Passport.](https://github.com/dOrgTech/passport).

In this example, the Passport is the membership NFT. Rep (reputation) is an ERC20 that is minted to/burned from the Passport.

We also have Badges, ERC1155, that can be used to mint any kind of fungable or non-fungable tokens to a Passport.

In this example, there was no use for further nesting.

Here the Rep and Badges are displayed in the Passport holder’s wallet and are moved if the Passport is moved (can only be moved by the DAO).

---

**xinbenlv** (2022-12-17):

Hi authors,

how does this EIP compare to [EIP-6150: Hierarchical NFTs, an extension to ERC-721 - #2 by xinbenlv](https://ethereum-magicians.org/t/eip-6150-hierarchical-nfts-an-extension-to-erc-721/12173/2) ?

---

**ThunderDeliverer** (2022-12-17):

I seems very similar. The approach seems to be a bit different, but not that much. I’ll take a closer look (I just managed to quickly read through it now) in the following days and provide a more structured answer.

---

**ThunderDeliverer** (2022-12-17):

This sounds like a great use case to implement this proposal. Do you have any comments on how this proposal could benefit your use case or how it limits it?

---

**xinbenlv** (2022-12-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/thunderdeliverer/48/7407_2.png) ThunderDeliverer:

> I seems very similar. The approach seems to be a bit different, but not that much. I’ll take a closer look (I just managed to quickly read through it now) in the following days and provide a more structured answer.

[@ThunderDeliverer](/u/thunderdeliverer) great to hear. I’d suggest you reach out to author of 6150 and work together or proceed as competing EIP in which case you’d elaborate the rationale and merits of 6059 over 6150 or in which type of use cases are you each better than each other.  Like-wise for EIP-6150

---

**stoicdev0** (2022-12-19):

Thanks for pointing it out. I just finished reviewing 6150 and there’s a huge difference with ours which I think is enough to avoid having EIPs linked. We’d like to avoid that so our proposal doesn’t not become dependent which would slow down the process.

EIP-6150, is limited to parent-child relationships only in the very same contract. In EIP-6059, **parents and children can be from different collections as long as they implement the interface**. This difference is huge as it implies a lot more security and sync considerations from our part.

EIP-6150 might be good enough if the use case is to nest only NFTs inside the same collection, which is completely valid. The implementation (which I did not check in detail) will very likely be much simpler and cheaper to use. If you need cross collection, then ours provides a solution.

What do you think [@xinbenlv](/u/xinbenlv)?

Lastly, shall we clarify that in the name maybe?  Something like: “Parent-Governed Cross-Collection Nestable Non-Fungible Tokens” Or would clarifying that on the proposal body be enough?

Thank you very much for your time.

---

**xinbenlv** (2022-12-19):

I think this is a good argument and can be put in your rationale as articulation of merit for your use case.

---

**ThunderDeliverer** (2022-12-19):

Thank you for the suggestion, we added this note to the Rationale. ![:ok_hand:](https://ethereum-magicians.org/images/emoji/twitter/ok_hand.png?v=12)

---

**SamWilsn** (2023-01-10):

As part of our process to encourage peer review, we assign a volunteer peer reviewer to read through your proposal and post any feedback here. Your peer reviewer is [@simondos](/u/simondos)!

If any of this EIP’s authors would like to participate in the volunteer peer review process, [shoot me a message](https://ethereum-magicians.org/new-message?username=SamWilsn&title=Peer+Review+Volunteer)!

---

[@simondos](/u/simondos) please take a look through [EIP-6059](https://eips.ethereum.org/EIPS/eip-6059) and comment here with any feedback or questions. Thanks!

---

**ThunderDeliverer** (2023-01-31):

Thank you for the introduction [@SamWilsn](/u/samwilsn)!

Nice to meet you [@simonDos](/u/simondos), we are looking forward to your feedback! ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

---

**h4l** (2023-03-21):

Thanks for this proposal, I’ve been working with NFTs owned by NFTs in a project of my own recently, and I came across this while researching what other people are doing in this area. I’ve got a few thoughts on EIP 6059.

Firstly, just a typo, this should be “supply chains”?

> One concrete example of this can be drawn from supply trains use case.

I like the general principle that an NFT from one contract can be the owner of an NFT from a different contract, so I’m pleased to see this spec using that approach. In contrast, [EIP-6150](https://ethereum-magicians.org/t/eip-6150-hierarchical-nfts-an-extension-to-erc-721/12173) seems to expect that relationships only occur within the same contract, and that limits composability between contracts unaware of each other.

I feel like EIP-6059 is on the right track, but has some implicit assumptions about the type of nesting being modelled by the spec. I think you could get to a more general spec, which is also simpler.

A lot of the spec is describing how to model an ordered list of child NFTs owned by a parent, and a way to add children to the list using a two-step propose-and-accept method, with a secondary list of pending children.

I feel that this part of the spec is describing one approach to solve a general problem. My own use case doesn’t map well to an ordered list of children, as my children are more like object properties with distinct and clear semantic relationships to the parent. Representing them as a list would introduce the problem of validating that the cardinality of the relationships is correct, and of searching the list to find the child of a particular type. The propose-approve addition model is not something I need, so supporting it would feel unnatural.

I feel that a lot of the spec deals with how to create and modify hierarchies of NFTs. Construction of the hierarchy is something that is fairly application-specific, as every application will have their own requirements for what combinations of things are valid and what permissions are required.

For me, there’s more benefit in standardising how to read/interpret a hierarchy than write a hierarchy, as reading can be done by any number of parties, and these parties need standardisation to agree on how to interpret the hierarchy. Whereas writing is a limited-scope operation by a specific party, and the details of *how* something was created don’t matter for others, so long as they can interpret the result. Standardising writing imposes constraints on how an application can work, whereas standardising reading enables applications to interoperate in ways they otherwise couldn’t.

I think there’s potential to make NFTs more composable, extensible and enable emergent behaviour using NFTs owned by NFTs.

For example, [eip-4907](https://eips.ethereum.org/EIPS/eip-4907) provides a way for NFTs to be rented to 3rd parties, without giving the 3rd party the right to transfer the NFT. But it expects that an NFT implement the spec. i.e. as well as modelling their own domain, it expects an NFT contract to also model the rental domain, which feels like an unnecessary merging of separate concerns, and limits compatibility with existing contracts that are unaware of the spec. This also doesn’t scale — we can’t expect every NFT contract to be re-written to implement a new interface in order to work with new standards (especially considering the immutable, single-identity nature of NFTs).

The same could be achieved without needing the rented NFT to know about the rental spec by using a wrapper rental NFT contract that owns the borrowed NFTs, and transferring ownership of the rental wrapper to the borrower. This allows the rental wrapper to implement arbitrary conditions on the rental (rather than the fixed time duration model used by the 4907). e.g. the wrapper could remain active as long as a superfluid stream paying into it remained solvent. The wrapper would be a proper bearer asset that can be re-sold by the borrower. And the rights of the owner and borrower are protected by the logic of the wrapper rental contract, such that the owner can’t rug-pull the renter by selling the rented NFT, and the borrower can’t transfer the rented NFT.

What’s needed is a standard way to represent semantic information about the relationship between the parent and child NFTs. (e.g. in this example, so that 3rd parties can understand that ownership of the rental NFT implies the owner has this rental agreement with the wrapped NFT.) And more generally, an NFT may not own another NFT but could still express information about it. This feels very much like the problem that Linked Data and the Semantic Web tries to solve — it wouldn’t be practical to create an EIP and specific interface for every domain in which an NFT can express a relationship with another, but it would be practical standardise a way to express such relationships generically, a bit like how EIP-165 or ERC-1820 generically define contract interface compatibility.

Sorry if this is a bit abstract, but I can point to some concrete things for this EIP.

The way `ownerOf()` is specified breaks compatibility with 721. In my opinion, it should report the contract address that owns the NFT, not the account that owns it transitively. Instead of changing the semantics of `ownerOf()` the spec should define a new function should for the indirect owner.

However, I’m not sure that such a function is needed. Because 721 already defines ownerOf() which can point to the owning contract, the only thing missing is a standard way to ask the owning contract which of its tokens owns the child NFT.

Similarly, 721’s Transfer event already communicates the transfer of ownership to the parent NFT contract, but an event listener needs to know which tokenId is the owner. Rather than having the child emit a new `NestTransfer` event, the parent contract could emit a `Receive` event, containing the tokenId that now owns the child.

This approach would allow regular 721 contracts to interoperate, without needing them to know that their owner is an NFT.

The spec mentions `INestable` and `nestMint` which are not defined in the spec.

On the security side of things, an issue I’ve considered in my own nested ownership situation is with selling the nested NFTs, or more generally, allowing other contracts to use them safely. The problem is that if a hierarchy can be modified by its current owner, the owner could list the NFT for sale, and then front-run a sale transaction by removing a child NFT that the buyer was expecting to own after the sale.

In theory this front-running and modification could be detected as part of the contract executing the sale transaction, but in practice NFT marketplaces won’t be aware of NFT nesting, so they need to rely on a hierarchy being immutable.

I address this by making the parent NFT’s tokenId a content address/hash of the child NFTs. Changing the children changes the tokenId, (burns and mints a new parent), so its not possible to be rug-pulled when buying such an NFT hierarchy, as the sale’s transfer will fail because the sold token has been burnt.

Rather than using content addressing, sequential IDs that aren’t re-used could also work, but content-addressing has the property that the same conceptual NFT can be brought back into existence by combining the same children as before.

I think at least some warning of this kind of issue should be added to the security section, even if a general remediation isn’t possible.

---

**stoicdev0** (2023-03-28):

First of all, thanks a lot for such a detailed review! There are some very interesting points, I hope I’ll cover them all.

> Firstly, just a typo, this should be “supply chains”?

Good catch, we’ll fix.

> My own use case doesn’t map well to an ordered list of children

There’s no particular order needed to keep track of the children in the spec. It needs to be a list though, we consider it important to be able to get the full list from other contracts.

> The propose-approve addition model is not something I need, so supporting it would feel unnatural.

We strongly believe this is a key component of this EIP, since not including it opens the doors for spamming. You could auto-accept the children directly on add, we’ve done this already in some implementations where we mark some trusted collections which get accepted directly.

> I feel that a lot of the spec deals with how to create and modify hierarchies of NFTs. Construction of the hierarchy is something that is fairly application-specific, as every application will have their own requirements for what combinations of things are valid and what permissions are required. (…) For me, there’s more benefit in standardising how to read/interpret a hierarchy than write a hierarchy (…)

Due to the propose-approve pattern, the accept and reject functions are needed. Besides that, we actually need the `addChild` function there because it is the entry point to create such hierarchy. We also need a way to transfer children out, since only the parent NFT should be able to manage them. So while I agree interfaces should focus on how to read rather than write, it seems unavoidable to have these minimal writing functions.

> The way ownerOf() is specified breaks compatibility with 721. In my opinion, it should report the contract address that owns the NFT, not the account that owns it transitively. Instead of changing the semantics of ownerOf() the spec should define a new function should for the indirect owner. (…) However, I’m not sure that such a function is needed. Because 721 already defines ownerOf() which can point to the owning contract, the only thing missing is a standard way to ask the owning contract which of its tokens owns the child NFT.

Current implementation of `ownerOf` is in line with `ERC721` as it signals who controls the token, be it nested or not. We feel that modifying such behavior, by returning the parent token’s contract address, might break the backwards compatibility.

Let’s use an example of access pass NFT for this. If the access pass is nested, the access would be granted to the parent token, not the root owner as intended.Additionally this would create the need for two additional methods; one for retrieving the root owner and another that would signal whether the token is nested or not and into which token it is nested.

> Similarly, 721’s Transfer event already communicates the transfer of ownership to the parent NFT contract, but an event listener needs to know which tokenId is the owner. Rather than having the child emit a new NestTransfer event, the parent contract could emit a Receive event, containing the tokenId that now owns the child.

A Receive event would need to have the information about the previous `tokenId` owner or we wouldn’t have the full picture. This information is already known when we emit the `NestTransfer`, but not on the `addChild` call.

> This approach would allow regular 721 contracts to interoperate, without needing them to know that their owner is an NFT.

We don’t expect a regular 721 to be interoperable with this interface. It simply cannot be done since those have no way to be transfererd into a Nestable token identifying the id of the parent.

> The spec mentions INestable and nestMint which are not defined in the spec.

Thanks for noticing, we will fix soon.

> On the security side of things, an issue I’ve considered in my own nested ownership situation is with selling the nested NFTs, or more generally, allowing other contracts to use them safely. The problem is that if a hierarchy can be modified by its current owner, the owner could list the NFT for sale, and then front-run a sale transaction by removing a child NFT that the buyer was expecting to own after the sale. (…)

We are well aware of this problem and agree that it should be clearly mentioned on the spec. Thanks for bringing it up!

Please let me know if I left something out.

---

**h4l** (2023-03-30):

Thanks for your reply, I appreciate you taking the time! I think I have a better understanding of your intentions and goals for this now. I can see it’s necessary to define the transfer mechanism for what you’re doing with it. Particularly when designing this kind of interface for new NFTs that are explicitly aware of nesting.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> We don’t expect a regular 721 to be interoperable with this interface. It simply cannot be done since those have no way to be transfererd into a Nestable token identifying the id of the parent.

Just to explain my approach, I use an approve-and-spend interaction, like you’d use to have a contract use an ERC20. E.g. The owner of an NFT to be wrapped approves the parent contract to operate its NFT. It then calls a function on the parent contract, which can then transfer the caller’s NFT to itself. It has the same UX problems (2 separate transactions) as ERC20s with regular EOAs though.

---

**MidnightLightning** (2023-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> We strongly believe this is a key component of this EIP, since not including it opens the doors for spamming. You could auto-accept the children directly on add, we’ve done this already in some implementations where we mark some trusted collections which get accepted directly.

This was the key area that stood out to me as not ideal for this ERC, and why I hesitate to integrate it: the concept of any token collection being “spam” is easily handled at the UI layer rather than the blockchain layer. Token collections are separate contracts, and only appear “in your wallet” if the UI layer knows of the collection contract and enumerates it. There are already robust solutions for curated token set lists that different authorities produce that wallets/galleries/tools can adhere to. Giving users the ability to ignore/remove a token from their visual wallet in the UI is gas-less and doesn’t affect legitimate tokens being transferred in.

Dealing with spam tokens by forcing **EVERY** transfer to **EVERY** parent token to need a second transaction (gas cost to the receiver) is a worse experience for every legitimate/wanted token transfer, for a benefit that seems like it could be achieved other ways. Hence, compared to a system like the (abandoned) [EIP998](https://eips.ethereum.org/EIPS/eip-998), I think this system is overly-costly to the legitimate end users.

---

**stoicdev0** (2023-04-25):

This ERC is already in final, but the behavior you see as problematic can easily be solved by having an auto accept mechanism for collections you specify and using it on the `_afterAddChild` hook. This has been used already in a few collections. Alternatively, you could just that that for all if it fits your use case better.

Here’s a snippet:

```auto
    mapping(address => bool) private _autoAcceptCollection;

    function setAutoAcceptCollection(
        address collection
    ) public virtual onlyOwner {
        _autoAcceptCollection[collection] = true;
    }

    function _afterAddChild(
        uint256 tokenId,
        address childAddress,
        uint256 childId,
        bytes memory
    ) internal override {
        // Auto accept children if they are from known collections
        if (_autoAcceptCollection[childAddress]) {
            _acceptChild(
                tokenId,
                _pendingChildren[tokenId].length - 1,
                childAddress,
                childId
            );
        }
    }
```

RE 998. It is in deed abandoned, and we did consider it before proposing our own EIP. One of the issues we found isthat it tried to solve different problems in a same EIP with 4 implementations. But the real stopper was that we discovered huge security risks when doing bottom up approaches.

This EIP works well to make any NFT from the spec available as child or parent with a single interface, always giving custody to parent.  These kind of problems can not be seen easily from just the interface, that’s why we worked for several months on testing this internally and producing a stable sample implementation before proposing for feedback.

If you’re interested, you can find a basic implementation of this ERC on the assets folder, or we also provide a convinient NPM package, very similar to what OpenZeppeling does: [@rmrk-team/evm-contracts - npm](https://www.npmjs.com/package/@rmrk-team/evm-contracts). It contains core implementations for this and other ERCs (5773 and 6220), with extensions and 3 ready to use implementations of each, for either lazy minting or preminting with ERC20 or native token. Repo is public so feel free to contribute!

---

**MidnightLightning** (2023-04-26):

Yes, logic can be added to short-circuit the approval step, but by having the propose-accept infrastructure be part of the standard and not an implementation choice adds bloat to any contract that wishes to not use it. My intent is to express feedback as a developer evaluating which standard(s) to implement in new projects; that requirement makes me more likely to skip this one in favor of an alternate “nestable” standard.

Additionally, as I’m evaluating how implementing this standard for projects that have existing token collections, I’m concerned that within the EIP-6059 definition, it sets up a requirement to not use zero as a token identifier, but also claims backward-compatibility with ERC-721:

> ID MUST never be a 0 value, as this proposal uses 0 values do signify that the token/destination is not an NFT.

> The Nestable token standard has been made compatible with ERC-721 in order to take advantage of the robust tooling available for implementations of ERC-721 and to ensure compatibility with existing ERC-721 infrastructure.

These two statements are at odds with each other. The ERC-721 standard only specifies that identifiers be `uint256` values:

> NFT Identifiers
>
>
> Every NFT is identified by a unique uint256 ID inside the ERC-721 smart contract. … While some ERC-721 smart contracts may find it convenient to start with ID 0 and simply increment by one for each new NFT, callers SHALL NOT assume that ID numbers have any specific pattern to them, and MUST treat the ID as a “black box”.

This includes zero as a valid identifier. All token collections that include a token with an identifier of zero can still be a compliant ERC-721 token (assuming it adheres to all the other requirements of that standard). By my understanding of the ERC-6059 standard, any ERC-721 token that has an identifier of zero would be unable to be set as the parent or child of any other token (attempting to add a child to token ID #0 would incorrectly try to assign the child to the ERC-721 token contract itself). Is that correct? If so, I feel it is inaccurate to claim EIP-6059 is “compatible with ERC-721” (and to make claims like “This EIP works well to make **any NFT** from the spec available as child or parent”), as it’s only compatible with *some* ERC-721 tokens.

---

**stoicdev0** (2023-05-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> having the propose-accept infrastructure be part of the standard and not an implementation choice adds bloat to any contract that wishes to not use it.

I’ve put a lot of thought into this, trying to see if we could have made the propose-accept only optional, or as an extension. It would remove the need for many methods but there would be a problem in the `ChildTransfered` event and the `transferChild` function, since they need the pending flag there. Not being able to easily extend it to propose-accept would have been a big issue for us.

On the other hand, the current ERC allows for an easy implementation which bypasses this pattern. Maybe we could add a note and even a sample implementation on how that would work. Which is basically having `addChild` send children directly to active array and emitting both `ChildProposed` and `ChildAccepted`. And have empty implementations for functions which manage pending children.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/midnightlightning/48/9529_2.png) MidnightLightning:

> “This EIP works well to make any NFT from the spec available as child or parent”

The spec here means 6059, and in deed, any 6069 implementation can work as either parent or child to any other 6059. We don’t pretend to be able to receive or send to existing 721s, that will not work and I don’t think we claim such ability.

This is compatible in the sense that any functionality that’s out there for 721s will also work for tokens implementing 6059. Not allowing for ID 0 does not change this backwards compatibility for all existing tools build for 721.

If you want to use this standard there are 2 cases:

1. You are creating a new collection. In which case, you can simply start from 1, we don’t see how this could be problematic.
2. You want to add this functionality to your existing collection. For this, you can use a wrapper which locks 721s and mints 6059. We have such tool and what we do is to map ID 0 (if existing) to max supply. This is annoyance, yes, but preventing the use of ID 0 simplified the code, reduced possibility of errors (since a mapping would default to Id). Additionally the gas and size usage was reduced by not having such checks. It was a trade-off and we feel we made the right choice.

---

**MidnightLightning** (2023-05-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/stoicdev0/48/7697_2.png) stoicdev0:

> We don’t pretend to be able to receive or send to existing 721s, that will not work and I don’t think we claim such ability.
>
>
> This is compatible in the sense that any functionality that’s out there for 721s will also work for tokens implementing 6059.

Okay, that clarifies things; the intended audience for this standard seems to be primarily aimed at new creations, and ones that won’t be interacting with ERC721 tokens as children.

I reread the “Backwards Compatibility” section and realized it does have a more full description of what the intention here is (EIP6059 works with older tooling), but to me the crux of the issue is I don’t think that is the definition of “backwards compatible”, which lead to my confusion.

I most commonly have seen that term used to indicate “old things can work in the new tool” (e.g. [What is Backward Compatible (Backward Compatibility)?](https://www.techtarget.com/whatis/definition/backward-compatible-backward-compatibility) “software system that can successfully use interfaces and data from earlier versions of the system or with other systems”). Therefore the intention of “ERC6059 tokens can masquerade as ERC721 tokens for tools that don’t know about ERC6059” is a fine goal, but is going the “wrong way around” (“new thing works in the old tool”) so I believe should be labeled something different than “Backwards Compatible”.


*(15 more replies not shown)*
