---
source: magicians
topic_id: 23222
title: "ERC-7909: Margin Token Wrapper: Make Any Token Lockable"
author: hellohanchen
date: "2025-03-21"
category: ERCs
tags: [erc-721, erc-20, erc-1155]
url: https://ethereum-magicians.org/t/erc-7909-margin-token-wrapper-make-any-token-lockable/23222
views: 99
likes: 0
posts_count: 1
---

# ERC-7909: Margin Token Wrapper: Make Any Token Lockable

I am proposing to use a singleton wrapper contract to convert any ERC20/721/1155 token into a wrapped version that

- The wrapped token still follows ERC1155 standard
- Freely mint or redeem
- Lockable, with lock expiration

## Motivation

“Margin” is a widely used concept in trading, it is the collateral that an investor has to deposit with their broker or exchange to cover the credit risk the holder poses for the broker or the exchange. In centralized crypto exchanges, the exchanges will just lock part of users’ balances to use as margin. But on blockchain, with decentralized exchanges (DEX), users always need to transfer tokens to a smart contract, then use part of those tokens as margin. There is little interoperability across different DEX protocols and the assets transferred out will not show up on the user’s address balance.

There are existing ERC proposals that suggest a lockable version of tokens. However, those might not be applicable to existing tokens and also each of them is still individual token contracts, the interoperability is still limited. In this proposal, we are defining a wrapper contract that can wrap any token into a “margin token” and can be used across multiple DEX as collaterals.

## Spec

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Margin Token Wrapper Contract

The `MarginTokenWrapper` contract will be an ERC-1155 contract implementing these core functionalities:

- GetTokenId: ERC-1155 requires each token to have an uint256 id,

For ERC-20, we will just use uint256(uint160(tokenAddress)) as id, in which tokenAddress is the token’s smart contract address, so that it is guaranteed to be unique.
- For ERC-721 and ERC-1155, we can use tokenAddress || tokenId as id.

**Mint**: The `owner` needs to approve the contract to `transferFrom`, when minting, the contract will pull tokens from `sender`’s balance and mint the corresponding wrapped token with the same amount to the `owner`.
**ApproveLock**: To use the wrapped token as margin, the `owner` needs to approve another address, marked as `locker`, to lock assets, the lock approval will come with

- tokenAddress or id: only 1 type of wrapped token is approved
- limit: the maximum amount the locker can lock
- expiration: a timestamp when the lock will be automatically released, this is refreshed everytime a new approval is effective

**PermitLock**: A signature version of **ApproveLock**, following 712 sign typed data standard.
**Lock**: Once locking is approved, the `locker` can lock a specific amount of the `owner` of the specific token. Lock operation will consume the `limit` defined in the approval.
**Unlock**: `locker` can unlock anytime
**Liquidate**: Liquidation is transferring locked token, there are 2 scenarios:

- locker can transfer the locked assets anytime
- owner can transfer the locked assets if the expiration of a locker is reached

The following functions will only be applicable to unlocked balances:

- Approve: the same as common implementation
- Transfer: the same as common implementation but only able to transfer unlocked balances
- TransferFrom: the same as common implementation
- Burn: the owner can always burn any unlocked balances to get the corresponding unwrapped token back

## Github Pull Request



      [github.com/ethereum/ERCs](https://github.com/ethereum/ERCs/blob/9d6dea5ec9ced0a8494c19870da0365fc2a02dce/ERCS/erc-margin-token.md)





####

  [9d6dea5ec](https://github.com/ethereum/ERCs/blob/9d6dea5ec9ced0a8494c19870da0365fc2a02dce/ERCS/erc-margin-token.md)



```md
---
eip: unassigned
title: Margin Token Wrapper
description: A general wrapper to convert any token to a lockable token.
author: Han Chen (@hellohanchen)
discussions-to: TODO
status: Draft
type: Standards Track
category: ERC
created: 2025-03-16
requires: 20, 165, 721, 1155
---

## Abstract

This proposal defines a token wrapper contract that can convert any [ERC-20](./erc-20.md), [ERC-721](./erc-721.md), [ERC-1155](./erc-1155.md) token to corresponding "margin token", which is an [ERC-1155](./erc-1155.md) token and is lockable.

## Motivation

"Margin" is a widely used concept in trading, it is the collateral that an investor has to deposit with their broker or exchange to cover the credit risk the holder poses for the broker or the exchange. In centralized crypto exchanges, the exchanges will just lock part of users' balances to use as margin. But on blockchain, with decentralized exchanges (DEX), users always need to transfer tokens to a smart contract, then use part of those tokens as margin. There is little interoperability across different DEX protocols and the assets transferred out will not show up on the user's address balance.
```

  This file has been truncated. [show original](https://github.com/ethereum/ERCs/blob/9d6dea5ec9ced0a8494c19870da0365fc2a02dce/ERCS/erc-margin-token.md)
