---
source: magicians
topic_id: 11441
title: "Idea: NFT Royalty - Capital gain basis"
author: Liz
date: "2022-10-24"
category: EIPs
tags: [nft, royalty]
url: https://ethereum-magicians.org/t/idea-nft-royalty-capital-gain-basis/11441
views: 773
likes: 2
posts_count: 2
---

# Idea: NFT Royalty - Capital gain basis

Hey there,

We (Liz, Vick-v3, lyxann, 0x50fc, bestysh,T-Matrix) are proposing an alternative standard interface for contract to calculate NFT royalty fee. The royalty is based on a percentage of the appreciation of the subject NFT relative to a percentage applied on the sale price. This concept is similar to Capital Gain Tax that is widely imposed in many countries.

## Motivation

In the ongoing debate of NFT royalties, advocates extoll how beneficial royalties are for an NFT ecosystem’s organic growth but detractors assert that royalties are exploitative and unnecessary. The reason why this debate arises is because the existing royalty structure is expressed as a rate (specified by the creator) of the sale price (hereinafter referred to as “fixed-rate royalty fee) and levied in the event of exchange of hands of the underlying NFT. This results in a misalignment of interests between the creator and the holder.

**Cons of fixed-rate royalties:**

1. it increases friction in transactions: the royalties paid by the holder is actually included in the sale price and higher royalty fees result in higher sale prices but less buyers.
2. the royalties paid to creators are unfair and extractive for holders, especially in a bear market where the NFT sale proceeds upon deduction of royalty fees may be even lower than the original purchase price.

On the flipside, removing royalties would hurt the very artists and creators who first turned to NFTs as a more profitable medium of selling their work. It’s not beneficial for the NFT ecosystem in the long run. Hence, here at [Hunter Club], we believe a hybrid approach, which aligns the interest of both the creator and the holder, is the solution.

## How does Capital Gain Royalty Fee work?

**Capital gain royalty fee = (Sale price - Last purchase price) * Royalty rate**

A. If Sale price < Last purchase price, Royalty Fee = 0

B. If the last purchase price is not available,

1. If the latest royalty fee is available, we will use the latest one
2. If the latest royalty fee is not available, we propose another parameter defined by creator: Baseline rate (usually will be lower than royalty rate)

Royalty fee = Sale price * Baseline rate

## Example

Case 1:

Last purchase price: 1 ETH

Sale price: 2 ETH

Royalty rate: 5%

Capital gain royalty fee: (2-1) * 5% ETH = 0.05 ETH

Fixed-rate royalty fee: 2* 5% ETH = 0.1 ETH

Case 2:

Last purchase price: 1 ETH

Sale price: 0.8 ETH

Royalty rate: 5%

Capital gain royalty fee: 0

Fixed-rate royalty fee: 0.8* 5% ETH = 0.04 ETH

Case 3:

Last purchase price: unknown

Sale price: 1 ETH

Royalty rate: 5%

Baseline rate: 2.5%

Capital gain royalty fee: 0

Fixed-rate royalty fee: 1* 2.5% ETH = 0.04 ETH

## Implementation

```auto
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.7.0) (token/ERC721/ERC721.sol)

pragma solidity ^0.8.0;

import "./IERC721.sol";

interface ERCxxx /* is ERC165 */  {

    function _caculateCGR() private retruns (uint256) {
        uint256 res;
        /* caculate rate
         * r1: Royalty rate
         * r2: Baseline rate
         */
        res = min(r1, r2);
        return res;
    }

    function _royaltyPayment(address from, address to) private virtual {
        // record the last tax levy: last_tax = res;
        // Complete tax transactions...
        return safeTransferFrom(from, to, tokenId);
    }
}
```

Because this standard is fully EIP-721 compliant and is extended from ERC-721, existing protocols will be able to facilitate the implementation of CGR NFTs out of the box.

## Further Discussion

Royalty rate can be regressive

## Replies

**nth-commit** (2022-12-31):

I mostly just want to say that I think that the propagation of a capital gains tax over a sales tax would be super productive for the ecosystem, so having it standardized to the same level as royalties currently are makes a lot of sense to me.

Are you also aware of this proposal? [EIP-2981: NFT Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)

It might be worth thinking about how the two interact.

