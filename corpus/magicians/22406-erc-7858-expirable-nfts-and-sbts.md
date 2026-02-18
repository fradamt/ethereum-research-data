---
source: magicians
topic_id: 22406
title: "ERC-7858: Expirable NFTs and SBTs"
author: MASDXI
date: "2025-01-04"
category: ERCs
tags: [erc, nft, token, sbt, expirable]
url: https://ethereum-magicians.org/t/erc-7858-expirable-nfts-and-sbts/22406
views: 329
likes: 2
posts_count: 2
---

# ERC-7858: Expirable NFTs and SBTs

#### Discussion topic for ERC-7858: Expirable NFTs and SBTs



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/pull/841)














####


      `master` ← `parametprame:master`




          opened 08:45AM - 09 Jan 25 UTC



          [![](https://avatars.githubusercontent.com/u/43013637?v=4)
            parametprame](https://github.com/parametprame)



          [+1606
            -0](https://github.com/ethereum/ERCs/pull/841/files)







An extended interface to enables non fungible token (ERC-721) and soulbound toke[…](https://github.com/ethereum/ERCs/pull/841)n (SBTs) to possess expiration capabilities, allowing them to expire after a predetermined period of time.












#### Update Log

- 2025-01-04: Initiate Idea, received from @Arvolear #16, #18
- 2025-01-06: Update section Specification
- 2025-01-09: Update section Specification
- 2025-02-25: Update section Specification commit fix comment from @alexroan
b10c573
- 2025-02-26: Update section Security Considerations commit a3a27bb
- 2025-02-26: Update section Specification commit 91bdd1b
- 2025-04-21: Update resolve some comments from EIP Editor commit 450f579 and 816f06e
- 2025-05-14: Update Status Move to Review #1023
- 2025-08-02: Remove epochType because it seems to be redundant; use expiryType only more simply and avoid type inconsistency commit 94fc1ff
- 2025-08-06: Update Status Move to Last Call #1138
- 2025-09-09: Update Status Move to Final #1178

#### External Reviews

- 2025-02-25: Receive comment from @alexroan about verb/grammar on function name.
- 2025-08-02: Receive comment from offiline, type of expiryType and epochType can be inconsistent and can make the interface specification misbehave, e.g., the epoch expired, but the token in the epoch is not expired. fix in commit 94fc1ff
- 2025-08-06: Receive comment from offiline, interface Id of the epoch extension and the args type in the optional function are incorrect. Change from uint256 to address . fix in PR #1153

#### Outstanding Issue

- 2025-02-26: Non-existent token can return startTime and endTime fix in commit 91bdd1b

> All changes will be managed through pull requests. This topic provides an initial draft version to help those who are not familiar with using GitHub.

> Author Opinion
> In the past, plenty of ERCs have tried adding an “expiration” feature to NFTs and SBTs as part of their use case. But honestly, most smart contracts or protocols probably just need to know if the token (or contract) can expire—it doesn’t matter if it’s for subscriptions, rentals, or synthetic use cases. Credit to the original idea. ERC-5007 but this proposal focuses more on “expirable” behavior. allowing other use cases to be built on top of this foundational feature. while ERC-6147 serves as an external restriction layer with expirable guards (focusing on permission control), it’s about who can transfer and who can change the guards, while ERC-7858 defines when tokens become invalid

## Simple Summary

An extended interface enables Non-Fungible Tokens (NFTs) and Soulbound Tokens (SBTs) to possess expiration capabilities, allowing them to expire after a predetermined time.

## Abstract

Introduces an extension for [ERC-721](https://eips.ethereum.org/EIPS/eip-721) Non-Fungible Tokens (NFTs) and Soulbound Tokens (SBTs) that adds an expiration mechanism, allowing tokens to become invalid after a predefined period. This additional layer of functionality ensures that the expiration mechanism does not interfere with existing NFTs or SBTs, preserving transferability for NFTs and compatibility with current DApps such as NFT Marketplace. Expiration can be defined using either block height or timestamp, offering flexibility for various use cases.

## Motivation

Introduces an extension for [ERC-721](https://eips.ethereum.org/EIPS/eip-721.md) Non-Fungible Tokens (NFTs) and Soulbound Tokens (SBTs), which facilitates the implementation of an expiration mechanism.

Use cases include:

- Access and Authentication

Authentication for Identity and Access Management (IAM)
- Membership for Membership Management System (MMS)
- Ticket and Press for Meetings, Incentive Travel, Conventions, and Exhibitions (MICE) when using with ERC-2135 or ERC-7578.
- Subscription-based access for digital platforms.

Digital Certifications, Contracts, Copyrights, Documents, Licenses, Policies, etc.
Loyalty Program voucher or coupon
Governance and Voting Rights
Financial Product

- Bonds, Loans, Hedge, and Options Contract

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Interface

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity >=0.8.0 =0.8.0 <0.9.0;

/**
 * @title ERC-7858: Expirable NFTs and SBTs
 * @notice epoch expiry extension
 */

// import "./IERC7858.sol";

// The EIP-165 identifier of this interface is `0xaaf87b24`.
interface IERC7858Epoch /** is IERC7858 */ {
    /**
     * @dev Retrieves the balance of a specific `epoch` owned by an account.
     * @param epoch The `epoch for which the balance is checked.
     * @param account The address of the account.
     * @return uint256 The balance of the specified `epoch`.
     * @notice "MUST" return 0 if the specified `epoch` is expired.
     */
    function balanceOfAtEpoch(uint256 epoch, address account) external view returns (uint256);

    /**
     * @dev Retrieves the current epoch of the contract.
     * @return uint256 The current epoch of the token contract,
     * often used for determining active/expired states.
     */
    function currentEpoch() external view returns (uint256);

    /**
     * @dev Retrieves the duration of a single epoch.
     * @return uint256 The duration of a single epoch.
     * @notice The unit of the epoch length is determined by the `validityPeriodType` function.
     */
    function epochLength() external view returns (uint256);

    /**
     * @dev Returns the type of the epoch.
     * @return EXPIRY_TYPE  Enum value indicating the unit of an epoch.
     */
    function epochType() external view returns (EXPIRY_TYPE);

    /**
     * @dev Checks whether a specific `epoch` is expired.
     * @param epoch The `epoch` to check.
     * @return bool True if the token is expired, false otherwise.
     * @notice Implementing contracts "MUST" define and document the logic for determining expiration,
     * typically by comparing the latest epoch with the given `epoch` value,
     * based on the `EXPIRY_TYPE` measurement (e.g., block count or time duration).
     */
    function isEpochExpired(uint256 epoch) external view returns (bool);

    /**
     * @dev Retrieves the balance of unexpired tokens owned by an account.
     * @param account The address of the account.
     * @return uint256 The amount of unexpired tokens owned by an account.
     */
    function unexpiredBalanceOf(address account) external view returns (uint256);

    /**
     * @dev Retrieves the validity duration of each token.
     * @return uint256 The validity duration of each token in `epoch` unit.
     */
    function validityDuration() external view returns (uint256);
}
```

- balanceOfAtEpoch MUST return the balance of tokens held by an account at the specified epoch,If the specified epoch is expired, this function MUST return 0. For example, if epoch 5 has expired, calling balanceOfByEpoch(5, address) returns 0 even if there were tokens previously held in that epoch.
- unexpiredBalanceOf MUST return only unexpired or usable tokens.
- currentEpoch MUST return the current epoch of the contract.
- epochLength MUST return duration between epoch in blocks or time in seconds.
- epochType MUST return the type of epoch used by the contract, which can be either BLOCKS_BASED or TIME_BASED.
- validityDuration MUST return the validity duration of tokens in terms of epoch counts.
- isEpochExpired MUST return true if the given epoch is expired, otherwise false.

### Additional Potential Useful Function

These **OPTIONAL** functions provide additional functionality that might be useful depending on the specific use case.

- getEpochBalance returns the amount of tokens stored in a given epoch, even if the epoch has expired.
- getEpochInfo returns both the start and end of the specified epoch.
- getNearestExpiryOf returns the list of tokenId closest to expiration, along with an estimated expiration block number or timestamp based on epochType.
- getRemainingDurationBeforeEpochChange returns the remaining time or blocks before the epoch change happens, based on the epochType.

## Rationale

### First, do no harm

Introducing expirability as an additional layer of functionality ensures it doesn’t interfere with existing use cases or applications. For non-SBT tokens, transferability remains intact, maintaining compatibility with current systems. Expired tokens are simply flagged as unusable during validity checks, treating expiration as an enhancement rather than a fundamental change.

### Expiry Types

Defining expiration by either block height (`block.number`) or block timestamp (`block.timestamp`) offers flexibility for various use cases. Block-based expiration suits applications that rely on network activity and require precise consistency, while time-based expiration is ideal for networks with variable block intervals.

## Backwards Compatibility

This standard is fully compatible with [ERC-721](https://eips.ethereum.org/EIPS/eip-721), [ERC-5484](https://eips.ethereum.org/EIPS/eip-5484) and other SBTs.

## Security Considerations

No security considerations were found.

## Historical links related to this standard

ERC that mentions “*expiration*” includes:

[ERC-4907](https://ethereum-magicians.org/t/eip4907-erc-721-user-and-expires-extension/8572): ERC-721 User And Expires Extension (Final)

[ERC-5007](https://ethereum-magicians.org/t/eip-5007-eip-721-time-extension/8924): ERC-721 Time Extension (Final)

[ERC-5334](https://ethereum-magicians.org/t/eip-5334-erc-721-user-and-expires-and-level-extension/10097): ERC-721 User And Expires And Level Extension (Draft)

[ERC-5643](https://ethereum-magicians.org/t/eip-5643-subscription-nfts/10802): Subscription NFTs (Stagnant)

[ERC-5727](https://ethereum-magicians.org/t/eip-5727-semi-fungible-soulbound-token/11086): Semi-Fungible Soulbound Token (Draft)

[ERC-6036](https://ethereum-magicians.org/t/eip-6036-subscribeable-nft-extension/11940): Subscribable NFT Extension (Draft)

[ERC-6147](https://eips.ethereum.org/EIPS/eip-6147): Guard of NFT/SBT, an Extension of ERC-721 (Final)

[ERC-6785](https://ethereum-magicians.org/t/eip-6785-erc-721-utilities-extension/13568): ERC-721 Utilities extension (Draft)

## Replies

**MASDXI** (2025-07-18):

Example usage rental use case.



      [github.com](https://github.com/fiit-ba/bnb)




  ![image](https://opengraph.githubassets.com/4548fa6193ab9477759ad9eaf53e2705/fiit-ba/bnb)



###



Contribute to fiit-ba/bnb development by creating an account on GitHub.










[lukacoff](https://github.com/lukacoff) and [LukyGregor](https://github.com/LukyGregor), “bnb,” GitHub repository, [Online]. Available: [GitHub - fiit-ba/bnb](https://github.com/fiit-ba/bnb).

