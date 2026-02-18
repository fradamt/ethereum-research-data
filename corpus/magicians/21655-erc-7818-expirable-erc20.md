---
source: magicians
topic_id: 21655
title: "ERC-7818: Expirable ERC20"
author: MASDXI
date: "2024-11-12"
category: ERCs
tags: [erc, token, erc20, expirable]
url: https://ethereum-magicians.org/t/erc-7818-expirable-erc20/21655
views: 941
likes: 15
posts_count: 22
---

# ERC-7818: Expirable ERC20

#### Discussion topic for ERC-7818

https://github.com/ethereum/ERCs/pull/718

#### Update Log

- 2024-11-14: Link to pull-request
- 2024-11-18: Update moving away from a library-based structure
- 2024-11-20: Update in section Security Considerations
- 2024-11-24: Update in section Specification
- 2024-11-27: Update resolve some comments from EIP Editing Office Hour 47 commit e5e4a60
- 2024-11-29: Update in section Specification and Rationale commit 5446318
- 2024-11-30: Update in section Motivation and fix typo
- 2024-12-04: Update in section Specification
- 2024-12-09: Update in section Specification (additional function) commit e754bb8
- 2024-12-11: Update in section Specification following merge pull-request
- 2025-01-04: Update in section Historical links related to this standard
- 2025-01-07: Update Status Move to Review #826
- 2025-01-25: Update Status Move to Last Call #840
- 2025-02-18: Update Status Move to Final #844

#### External Reviews

- 2024-12-31: “Decoding ERC-7818: Expirable ERC-20 Tokens”, by Sandesh B Suvarna, article
- 2025-01-03: “ERC-7818: Redefining Token Functionality with Expirable ERC-20 Tokens”, by Rajai Nuseibeh, article
- 2025-01-06: “EIP-7818: Expirable ERC-20 Tokens Customisation”, by Mohit Kapadiya, article
- 2025-01-11: “Introducing ERC-7818: Expirable Tokens for Ethereum”, by Tantrija, article
- 2025-02-18: " [ERC7818] ERC20トークンに有効期限を持たせる仕組みを理解しよう！", by Cardene, article

#### Outstanding Issue

- None as of 2025-02-25

> All changes will be managed through pull requests. This topic provides an initial draft version to help those who are not familiar with using GitHub.

## Simple Summary

An extended interface enables fungible tokens to possess expiration capabilities, allowing them to expire after a predetermined period.

## Abstract

Introduces an extension for [ERC-20](https://github.com/ethereum/ercs/blob/master/ERCS/erc-20.md) tokens, which facilitates the implementation of an expiration mechanism. Through this extension, tokens have a predetermined validity period, after which they become invalid and can no longer be transferred or used. This functionality proves beneficial in scenarios such as time-limited bonds, loyalty rewards, or game tokens necessitating automatic invalidation after a specific duration. The extension is crafted to seamlessly align with the existing [ERC-20](https://github.com/ethereum/ercs/blob/master/ERCS/erc-20.md) standard, ensuring smooth integration with the prevailing token smart contract while introducing the capability to govern and enforce token expiration at the contract level.

## Motivation

This extension facilitates the development of [ERC-20](https://github.com/ethereum/ercs/blob/master/ERCS/erc-20.md) standard compatible tokens featuring expiration dates. This capability broadens the scope of potential applications, particularly those involving time-sensitive assets. Expirable tokens are well-suited for scenarios necessitating temporary validity, including

- Bonds or financial instruments with defined maturity dates
- Time-constrained assets within gaming ecosystems
- Next-gen loyalty programs incorporating expiring rewards or points
- Prepaid credits for utilities or services (e.g., cashback, data packages, fuel, computing resources) that expire if not used within a specified time frame
- Postpaid telecom data package allocations that expire at the end of the billing cycle, motivating users to utilize their data before it resets
- Tokenized e-Money for a closed-loop ecosystem, such as transportation, food court, and retail payments
- Insurance claim credits, which are time-sensitive credits issued to policyholders that can be used to offset deductibles or excess charges, and expire after a defined period (e.g., 6 months)

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Epoch Mechanism

**Epochs** represent a specific period or block range during which certain tokens are valid. They can be categorized into two types

- block-based Defined by a specific number of blocks (e.g., 1000 blocks).
- time-based Defined by a specific duration in seconds (e.g., 1000 seconds).

Tokens linked to an `epoch` remain valid as long as the `epoch` is active. Once the specified number of `blocks` or the duration in `seconds` has passed, the `epoch` expires, and any tokens associated with it are considered expired.

### Balance Look Back Over Epochs

To retrieve the usable balance, tokens are checked from the **current epoch** against a **past epoch** (which can be any ***n*** epochs back). The past epoch can be set to any value **n**, allowing flexibility in tracking and summing tokens that are still valid from previous epochs, up to **n** epochs back.

The usable balance is the sum of tokens valid between the **current epoch** and the **past epoch**, ensuring that only non-expired tokens are considered.

#### Example Scenario

| epoch | balance |
| --- | --- |
| 1 | 100 |
| 2 | 150 |
| 3 | 200 |

- Current Epoch: 3
- Past Epoch: 1 epoch back
- Usable Balance: 350

Tokens from **Epoch 2** and **Epoch 3** are valid. The same logic applies for any ***n*** epochs back, where the usable balance includes tokens from the current epoch and all prior valid epochs.

Compatible implementations **MUST** inherit from [ERC-20](https://github.com/ethereum/ercs/blob/master/ERCS/erc-20.md)’s interface and **MUST** have all the following functions and all function behavior **MUST** meet the specification.

```solidity
// SPDX-License-Identifier: CC0-1.0
pragma solidity >=0.8.0

Question/Discuss about *“expirable”*

- Ethereum stack exchange question #27379
- Ethereum stack exchange question #63937

## Replies

**0xTraub** (2024-11-20):

I like the use cases. My concern is that at the point that the core transfer and balance method signatures are being changed from ERC20, why this wouldn’t make more sense as ERC-1155 extension, especially since there’s identifiers being used. `balanceOf` is the same siganture in `ERC1155` as well

---

**MASDXI** (2024-11-21):

Hi [@0xTraub](/u/0xtraub), Thanks for your feedback and your concern about the function signature of overloading `balanceOf` with the identifier did you think it should be changed to something like `balanceOfByIdentifier` borrowing style form `ERC-1400`



      [github.com](https://github.com/ndaxio/ERC1400/blob/6279d1ca640490fe192b9dfcd04e88a34e3cc81f/contracts/token/ERC1400Partition/IERC1400Partition.sol#L14C14-L14C34)





####



```sol


1. function balanceOfByPartition(bytes32 partition, address tokenHolder) external view returns (uint256); // 1/10


```










The reason I am not proposing this as an extension to the `ERC-1155`. The specification would need to spread down into multiple behaviors and may become more complicated when implemented, I think `ERC-7818` is more fungible because the expiration date becomes a shared, uniform trait across tokens.

- ERC20 can be split into 2 characteristics (Fungible Token) (Uniform)

 BulkExpire All tokens have the same expiration date. very straight forward

Example: seasonal loyalty points, bonds, or simple governance rights issued in limited amounts, which expire together under a single rule. In such cases, the
ability to mint new tokens continuously may not be suitable.

> Behavior: All tokens expired after block x

`IndependentExpire` Each `token` has an individual expiration date.

- Example: Common loyalty points, commodities have a life span, data packages, or e-money where each token can have a unique expiration, allowing more flexibility in managing user rewards.

> Behavior: Each token is valid for n blocks

---

- ERC721 can be split into multiple characteristics (Non-Fungible Token) (Unique)

 BulkExpire All tokenId have the same expiration date.

Example: seasonal coupons, vouchers, and rights, intended for services that affect a broad user base, where a uniform expiration is necessary.

> Behavior: All tokens were minted on the different blocks but expired at block  x (same block)

`IndependentExpireByTokenId` Each `tokenId` has an individual expiration date.

- Example: Very special coupon, or privileges  tailored to individual users, where each token can expire independently.

> Behavior:
> tokenId 1 minted on block a and expired at block x
> tokenId 2 minted on block b and expired at block y
> tokenId 3 minted on block c and expired at block z

`IndependentExpire` Each `tokenId` has an individual expiration date but has the same valid period or duration.

- Example: a very special coupons, vouchers, or rights can’t be stack

> Behavior: Each tokenId is valid for n blocks

---

- ERC1155 can be split into multiple characteristics (Semi-Fungible Token) (Mixed)

 BulkExpire All tokenId under the same smart contract has the same expiration date.

Example: vouchers, coupons, docs, or event tickets multiple types,s in the same contract, where all tokens within the same smart contract expire simultaneously.

> Behavior: All tokens of tokenId1, tokenId2, and tokenId3 expired at block x (same block)

`BulkExpireByType` All tokens under the same type `Id` have the same expiration date.

- Example: limited quantity coupons, vouchers, and time-limited game items for events e.g. for loyalty use cases is Black Friday or Flash Sales, all tokens of a specific type (same id) expire simultaneously.

> Behavior:
> All tokens of token type Id 1 are valid for n1 blocks
> All tokens of token type Id 2 are valid for n2 blocks

`IndependentExpireByType` Each token under the same `tokenId` has an individual expiration date.

- Example: casual coupon, voucher, and temporary access right within the same category can expire at different times.

> Behavior:
> Each token of token type Id 1 are valid for n1 blocks
> Each token of token type Id 2 are valid for n2 blocks,

---

**wjmelements** (2024-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/masdxi/48/14155_2.png) MASDXI:

> identifier

erc20 are fungible. They do not have identifiers. So you should not be extending ERC20.

---

**MASDXI** (2024-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> MASDXI:
>
>
> identifier

erc20 are fungible. They do not have identifiers.

All tokens are fungible, with `identifiers` used to manage expiration. While `ERC-1155` can support this, if the type `Id` in `ERC-1155` has a `balanceOf` of 1, it could behave like an NFT due to the [Natural Non-Fungible Tokens Approach](https://github.com/ethereum/ERCs/blob/b0573d36d07cdff90783a33959de4fece930deae/ERCS/erc-1155.md?plain=1#L682-L684), potentially adding complexity if adopting the [Split ID Bits Approach](https://github.com/ethereum/ERCs/blob/b0573d36d07cdff90783a33959de4fece930deae/ERCS/erc-1155.md?plain=1#L656-L680). `ERC-7818` offers a simpler, more focused solution for fungible tokens.

Ideally, change to `identifiers` to `epoch`

- Resolve collisions in function signatures with ERC-1155.
- Avoid confusion with Id in ERC-1155.

```Solidity
function transferByEpoch(uint256 epoch address to, uint256 value) external returns (bool);

function transferFromByEpoch(uint256 epoch, address from address to, uint256 value) external returns (bool);

function balanceOfEpoch(uint256 epoch, address account) external returns (uint256);
```

---

**wjmelements** (2024-11-21):

That the tokens are categorized by epoch/identifier means they are not fungible. The base methods of ERC20 are rendered meaningless. `transfer` and `transferFrom` in particular. They don’t make sense if the tokens are not fungible.

> Avoid confusion with Id in ERC-1155.

Why? Perhaps you should be extending ERC-1155 instead of ERC20.

---

**MASDXI** (2024-11-22):

[@wjmelements](/u/wjmelements) Any suggestion or solution if using a mix of expirable NFT and FT in the same contract?

---

**MASDXI** (2024-11-22):

```auto
// To ensure compatibility with both Fungible Tokens (FT) and Non-Fungible Tokens (NFT) in the same contract,
//The implementation requires s a clear linkage between the token ID and its associated epoch.
mapping(uint256 => uint256) private _tokenEpochRegistry;
// Alternative way
mapping(uint256 id => mapping(uint256 epoch => mapping(address account => uint256))) private _balances;
```

> ERC-1155
> safeTransferFrom and safeBatchTransferFrom MUST retrieve the epoch associated with the given token Id and verify whether it has expired internally before transfer. Transfers MUST be permitted only for tokens that are still valid (i.e., unexpired).
>
>
> balanceOf and balanceOfBatch MUST retrieve the epoch associated with the given token type Id verify whether it has expired internally and return the only valid balance. Expired tokens MUST NOT be included in the returned balance, ensuring the result reflects only actively usable tokens.
>
>
> duration() → durationOfToken(uint256 id)  The duration of each token type id MUST be independently managed to accommodate support for both Non-Fungible Tokens (NFT) and Fungible Tokens (FT) in the same smart contract.
>
>
> New → epochOfToken(uint256 id)
> Return the epoch associated with the given token type Id
>
>
> expired → tokenExpired Check whether a specific token type Id has expired. If the given token type Id has expired, it MUST return true; otherwise, it MUST return false.

[@0xTraub](/u/0xtraub) , [@wjmelements](/u/wjmelements)  Can this be applied across all token types?

**Implementation on `ERC20`**

`balanceOf`, `transfer`, and `transferFrom` **NOT REQUIRED** identifiers or require additional arguments. Instead, their internal logic **MUST** ensure that only tokens valid at the current `epoch` are processed.

`epoch` **MAY** not be exposed externally, as there is no need to make it accessible outside the other contract.

`duration` and `expire` **MUST NOT** be implemented, since all tokens technically share the same lifespan. Each token’s value is tied to its own expiration date, much like topping up a transport card. For instance, if you add 10 bucks today, those tokens will expire after a set time. If you top up again tomorrow with another 10 bucks, that amount will have a different expiration date, separate from yesterday’s.

Recap, this is conceptually similar to a rebase token system, where the total supply or balance of tokens adjusts periodically based on internal rules (e.g., expiration) but without external visibility or intervention. The core `ERC20` functions like `balanceOf`, `transfer`, and `transferFrom` **MUST NOT** expose any additional complexity (such as `identifiers` or other arguments) to the user, as the expiration handling is managed internally.

> Require metadata to flag tokens with expiration mechanisms, warning of risks on DEX platforms?

**Implementation on `ERC721`**

> for expirable ERC721 should move to ERC-5007



      [gist.github.com](https://gist.github.com/MASDXI/80a7ee4d4166cb37c0e8e36255dd9a95)





####



##### draft-IERC7818.sol



```
// SPDX-License-Identifier: CC0-1.0
pragma solidity >=0.8.0 <0.9.0;

/**
 * @title ERC-7818: Expirable ERC1155 or ERC721
 * @author sirawt (@MASDXI), ADISAKBOONMARK (@ADISAKBOONMARK)
 * @dev Interface for ERC1155 or ERC721 tokens with expiration functionality.
 */

// import "./IERC1155.sol";
```

   This file has been truncated. [show original](https://gist.github.com/MASDXI/80a7ee4d4166cb37c0e8e36255dd9a95)










`approve` **MUST** only allow approval for valid tokens. It **MUST** internally retrieve the `epoch` associated with the given token `id` and verify whether the token has expired. Expired tokens **MUST** NOT be approved.

** no need to change behavior on `setApprovalForAll` cause transfer handling the expiration check before the transfer

`safeTransferFrom` and `transferFrom` shared the same behavior as in the `ERC1155`

`durationOfToken(uint256 id)` shared the same behavior as in the `ERC1155`

`epochOfToken(uint256 id)` shared the same behavior as in the `ERC1155`

`expire` → `tokenExpired` shared the same behavior as in the `ERC1155`

`ERC1155` and `ERC-721` required `ERC165` support `IERC7818`

All the above implementations support various [expiration characteristics](https://ethereum-magicians.org/t/erc-7818-expirable-erc20/21655/3), whether they are managed independently or in bulk.

---

**0xTraub** (2024-11-22):

Definitely an improvement. A few things

1. I think the epoch() function should probably return when it started and when it ends, so return (uint256, uint256, uint256) or at least there needs to be some way to get when the epoch started and when it ends.
2. Validity period, is it representing the amount of time remaining for it being valid, or just how long the validity period is in general?
3. should validityPeriodType() not take an identifier or is it assumed that all identifiers are on the same time-based system.
4. Can you describe a situation in which the epoch of the contract would need to be different than the epoch of an individual token and in which both of those would be useful and relevant for different purposes?

---

**MASDXI** (2024-11-23):

1. epoch → (uint256 start, uint256 end)

start returning the block number or timestamp (UNIX)
2. end returning the block number or timestamp (UNIX)

> return the current epoch→ currentEpoch or return as args 0 of epoch
> return start and end should → getEpochInfo additional function

1. validityDuration represents the time validity duration in epoch counts.
2. When the contract is initialized it’s applied in all tokens, the reason why the opened block and time cause some L2 networks not create empty block.
3. getEpochOfToken can be additional useful if combined with epochLength and validityDuration, which can help the application cache the token and calculate if it’s expired off-chain → MAY over-engineer.

---

**0xTraub** (2024-11-23):

Which of these three things is the validityPeriod

1. A length of time/blocks the token is valid for until expiration (i.e 100 blocks).
2. The amount of time/blocks remaining before the token becomes expired (deadline - block.number)
3. The time/block at which the token will expire

---

**MASDXI** (2024-11-23):

Definitely 1.

but 2. and 3. can be done but should it be mandated?

---

**0xTraub** (2024-11-25):

I think the problem i’m having is that there’s both this notion of `epochs` and `periods` both of which have discrete time intervals. I think you need to pick one or the other perhaps because it’s confusing what the interplay between them is.

---

**MASDXI** (2024-12-11):

I’m addressing this now using only `epoch` and the balance tied to the `epoch` not the `periods`

---

**Arvolear** (2024-12-31):

Genuinely like this. Have you thought of expanding the approach to SBTs as well?

I see huge potential in expiring SBTs. For instance, access tokens, proof-of-human with forced reverification, subscription based benefits, etc.

---

**MASDXI** (2024-12-31):

Have you looked into ![:mag:](https://ethereum-magicians.org/images/emoji/twitter/mag.png?v=12) [ERC-5727](https://eips.ethereum.org/EIPS/eip-5727)? It might cover some of the ideas you’re mentioning.

---

**Arvolear** (2024-12-31):

I did. Also currently there is no “minimal SBT” standard. Pretty much all of them inherit basic ERC-721 token which has a lot of redundant functions for an SBT. Like why do you need approve and transfer methods when the token is ideologically non-transferable?

We actually took a one step further and implemented this minimal SBT contract [here](https://github.com/dl-solarity/solidity-lib/blob/master/contracts/tokens/SBT.sol).

However, this does not provide the “automatic expiry” use case which I think has a lot of potential.

---

**MASDXI** (2025-01-01):

Okay, I see. I’ve been reviewing various ERC proposals, including [ERC-5007](https://ethereum-magicians.org/t/eip-5007-eip-721-time-extension/8924), which introduces a time expiration that can be used as an expiration mechanism for NFTs, but I found it to be overly generalized and unclear, particularly when applied to specific use cases like SBT. However, I am still exploring ways to expand the expirable mechanism to make it work seamlessly for both [ERC-721](https://eips.ethereum.org/EIPS/eip-721) tokens (NFTs) and SBTs

---

**MASDXI** (2025-02-26):

An additional use case for ERC-7818:

It can serve as a strategy tool for ERC-20 tokens with a capped supply that want to remove tokens from circulation. Instead of simply burning non-expirable tokens, projects can burn them and mint an equivalent amount of ERC-7818 tokens for use within a DApp. This approach enables a non-linear burning mechanism.

---

**JamesB** (2025-07-27):

Hi, how is the progress on 7818? Is the contract ready for use? Has it been audited?

I am interested in using it in relation to a subsection of my project, for time-gated loyalty tokens. I did start my own design before finding yours and see that you’ve solved all the issues & nuances that usage of such a token would need to consider.

---

**MASDXI** (2025-07-28):

[@JamesB](/u/jamesb) The ERC `status` is now `final`; the reference implementation was developed to fully meet the specification, but ‘*just work*’ means it wasn’t optimized. If you want to use it, I recommend checking out this  [library](https://github.com/Kiwari-Labs/kiwari-labs-contracts). , It’s ready to but please note:

- The current version does not support upgradeable tokens.
- The epoch configuration (which determines timing/duration) is fixed at deployment and cannot be changed later.

So, if you need to upgrade the token or modify the epoch settings after deployment, the existing version does not support that yet. e.g. if the network changes the block time and you want to change the block or second per epoch.

The code isn’t audited yet but has been thoroughly tested across many scenarios.

We built this with open-source in mind and warmly welcome contributions. Your project sounds interesting—feel free to connect if you want to collaborate or need support from us.



      [github.com](https://github.com/Kiwari-Labs/kiwari-labs-contracts)




  ![image](https://opengraph.githubassets.com/9f0d19c45c3dff4e05b5ceaf665e267f/Kiwari-Labs/kiwari-labs-contracts)



###



 A Solidity library for expirable tokens with time or block-based expiration


*(1 more replies not shown)*
