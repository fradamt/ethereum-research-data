---
source: magicians
topic_id: 16092
title: "ERC-7536: Multi-edition NFT Distribution"
author: henrywfyeung
date: "2023-10-15"
category: ERCs
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/erc-7536-multi-edition-nft-distribution/16092
views: 670
likes: 1
posts_count: 1
---

# ERC-7536: Multi-edition NFT Distribution

This is the discussion thread for the ERC-7536 Pull Request [PULL-7853](https://github.com/ethereum/ERCs/pull/221). It proposes a specification for distributing multiple editions of child NFTs with different rules and privileges.

## Abstract

This standard extends ERC-721 to enable conditional minting of various editions of child tokens with specific privileges attached. An edition is defined as a version of a child token that encapsulates a descriptor to the parent, the address to a validator that validates rules before minting the child token, and a set of actions that can be invoked upon obtaining the child token. Each parent token can create multiple editions, each with a different set of rules to obtain the child tokens, and with different levels of privileges attached in the form of permitted actions. Upon fulfilling the corresponding rules from a specific edition, one can obtain the child token and will be able to use the token within the boundaries set by the parent token holder.

[![ERCXXXX](https://ethereum-magicians.org/uploads/default/original/2X/c/ce5691c352b2db9ead8b2d66d755a54ab4ae7c24.png)ERCXXXX539×279 8.33 KB](https://ethereum-magicians.org/uploads/default/ce5691c352b2db9ead8b2d66d755a54ab4ae7c24)

## Motivation

Most community-based relationships can be regarded as a social structure with a community owner, and multiple tiers of community members. Each tier has its own cost and benefit of joining. This can apply to the Profile-Follower relationship, Creation-Collection relationship, Producer-Subscriber relationship, Dao-Member relationship, etc.

### The Distributor Interface

```solidity
pragma solidity >=0.8.0 =0.8.0 <0.9.0;
/**
 * @notice The Validator Interface defines rules for minting child tokens. The parent token holder registers these rules for a specific edition, identified by the edition configuration hash (editionHash). Collectors wishing to mint a child token from this edition must pass validation by successfully calling the validate function, supplying necessary information including initiator address, editionHash, and optional fulfillment data.
 */
interface IValidator {
    /**
     * @dev Initializes validator rules using the edition hash and initialization data. Decodes the data to required parameters, establishing the rules determining who can mint a copy of the edition.
     * @param editionHash The hash of the edition configuration.
     * @param initData The data bytes for initializing validation rules; parameters are encoded into bytes.
     */
    function setRules(
        bytes32 editionHash,
        bytes calldata initData
    ) external;

    /**
     * @dev Validates the fulfillment of rules set by the parent token holder, using supplied data.
     * @param initiator The party initiating validation.
     * @param editionHash The hash of the edition configuration.
     * @param conditionType The type of condition for validation.
     * @param fulfillmentData Additional data required for passing validator rules.
     */
    function validate(
        address initiator,
        bytes32 editionHash,
        uint256 conditionType,
        bytes calldata fulfillmentData
    ) external payable;
}
```

## Rationale

### Usage

The Distributor Interface enables any ERC-721 token to create multiple editions, each with distinct rules validated by the Validator Interface before minting a child token, and a set of actions available post-minting. This is advantageous for community building, with diverse use cases like:

- Copy Issuance of Unique Artwork/Content: Artists can issue multiple copies of their unique artworks with different functions and rules, providing flexibility to both creators and collectors.
- Partial Copyright Transfer: Creators can conditionally delegate varying levels of copyrights, allowing for derivative work production without selling the original copy.

Consider using this standard for:

- Selling copies of unique Art/Music NFTs while retaining control over the copies.
- Selling time-limited copies of artwork with attached copyright statements for derivative work production.
- Issuing non-transferable Graduation Certificates as NFTs, where the university retains the revocation right.
- Community Management with a Single Parent Token or a Selected Edition of Child Tokens. The default setup enables a single parent token to set editions and the corresponding validation rules. A potentially advanced setup could delegate the management role to a particular edition of child tokens.

### The Main Contract that Implements the Distributor Interface for Edition Creation

The main contract must implement both the ERC-721 and the Distributor Interface. The Distributor Interface provides functions to to setup editions and the corresponding validation rules. Optionally, the main contract may implement additional functions that are guarded by the the actions parameter, denoted as action bits (uint96) in the editions. Such a design removes the dependency of the edition based permission control on the implementation of contract functions. However, the design only enables invocation of functions using actions parameter, but it does not specify the party. It is up to the developer to set up additional ownership checks, i.e. the action bits ensure the invocation of the “revoke token” function on the child token is permitted, but it requires additional ownership check in the contract to make sure this is a parent token only function.

### Flexible Implementation of Actions

The actions that can be performed are defined in the edition as a uint96 integer. Each bit in the integer determines whether a particular function can be invoked in the contract, with a maximum of 96 functions. The actions can be implemented flexibly depending on the specific use cases. For instance, if the parent token wants to have full control over the child token, the edition, together with the function setup, can permit the parent token holder to invocate a function that transfers the child token to the parent token holder.

Actions may give the child tokens the following characteristics:

- non-transferable: An SBT that is bound to a user’s wallet address
- revokable: The creator has control over the minted copies. This is suitable for NFTs that encapsulate follower relationships, or funtions as some kind of revokable permits
- extendable: NFT is valid over a duration and requires extension. This is suitable for recurring memberships.
- updateable: Allows the child token holder to update the tokenUri when the parent token is updated
- vote: Child token holder can vote if the vote action bit is set
- external contract actions: An externally deployed contract that implements functions with permissions controlled by the action bits in the contract with the Distributor interface

### External or Internal Implementation of the Validator Interface

The Validator Interface can be implemented externally as an independent contract, or internally as part of the contract that issues the child token. The former approach is more upgrade-friendly, i.e., validation contracts can be easily swapped to a higher version, while still maintaining compatibility to past versions. More it permits multiple different validators to coexist at the same time. The latter one is less composable, but more secure, as it does not depend on third-party code. This is preferred if the validated rules are unlikely to change in the future.

### Flexible Implementation of Validation Rules

The Validator Contract can be customized to enforce rules, including:

- Fee: Requires payment to mint
- Free: No Condition to mint
- NFT Holder: Process a particular NFT to mint
- ERC-20 Holder: Process a certain amount of ERC-20 tokens to mint
- Whitelist: In the whitelist to mint.
- Limited Issuance: Fixed Maximum number of issued copies.
- Limited Time: Enables minting within a particular time frame.

Please let us know your thoughts on this.

Contact Authors: Henry Yeung [@henrywfyeung](/u/henrywfyeung), Alex Yang [alex@didhub.com](mailto:alex@didhub.com)

Type: Standards Track

Category: ERC
