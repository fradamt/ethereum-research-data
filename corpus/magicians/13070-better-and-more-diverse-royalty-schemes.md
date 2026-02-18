---
source: magicians
topic_id: 13070
title: Better and More Diverse Royalty Schemes
author: 5cent-AI
date: "2023-02-27"
category: Uncategorized
tags: [nft]
url: https://ethereum-magicians.org/t/better-and-more-diverse-royalty-schemes/13070
views: 650
likes: 1
posts_count: 2
---

# Better and More Diverse Royalty Schemes

# Better and More Diverse Royalty Schemes

## Abstract

By using modern tax theory, various royalty schemes are proposed to better fit the diversity of NFTs and industry development. Through research, most of the royalty schemes can be implemented without any improvements to EIP2981.

## Royalty Scheme

We replace the `_salePrice` in EIP2981 with the `taxablePrice`.

That is, the expression of

`function royaltyInfo( uint256 _tokenId, uint256 _salePrice ) external view returns ( address receiver, uint256 royaltyAmount )`

is transformed to

`function royaltyInfo( uint256 _tokenId, uint256 taxablePrice ) external view returns ( address receiver, uint256 royaltyAmount )`;

### Scheme 1: Value-Added Royalty (VAR)

Only tax the portion of the seller’s profit. If the seller does not generate a profit during the period of holding the NFT, then no tax is imposed. Alternatively, tax only the difference between the highest price and the previous high price when the NFT price hits a new high.

`taxable price = max (current sale price - last sale price, 0)`

or

`taxable price = max (current sale price - historical highest sale price, 0)`

The previous royalties were collected based on trading volume. A certain percentage of the trading volume was the royalty for the project. For the NFT holders, their profits were based on sale price, and they could make a profit if the selling price is higher than the purchase price. For a holder who hold the NFT and sold it at a loss, the previous royalty scheme is not ideal, and it it has caused a certain degree of disconnection between the interests of the project and the holders. Through the above scheme, the project can only receive royalty income when the NFT price hits a new historical high, thus maintaining the consistency of the interests of the project and the holders.

Suitable for art NFTs, collectible NFTs, etc.

### Scheme 2: Capped Royalty（CR）

The royalties paid for each trading cannot exceed a certain limit.

`taxable price = min (current sale price, cap price)`

### Scheme 3: Fixed Royalty

The royalties paid for each transaction is a fixed value.

`taxable price = constant`

### Scheme 4: Sale Royalty

Charge a certain percentage of the sale price as royalties.

`taxable price = this sale price`

Note: this is the royalty scheme that was commonly used before.

### Scheme 5: Annuity

Charge royalty on an annual basis. For example, the charging strategy adopted by ENS.

This is suitable for some utility NFTs. For utility NFTs, in order to maintain their continuous utility, it may be necessary for the project to have sustained expenditures, hence an annuity approach can be adopted to maintain the project’s operations.

## How to Implement Mandatory Royalties

The competition between centralized entities in the current NFT market shows that the collection of NFT royalties cannot rely on their moral level. Only when NFT itself realizes NFT trading functions in the contract can mandatory royalties be implemented. Therefore, we propose [EIP-6105](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-6105.md) to achieve intermediary-free NFT trading.

### Discussions-to



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5cent-ai/48/8079_2.png)

      [Final: EIP-6105: No Intermediary NFT Trading Protocol With Mandatory and More Diverse Royalty Schemes](https://ethereum-magicians.org/t/eip6105-no-intermediary-nft-trading-protocol-with-mandatory-and-more-diverse-royalty-scheme/12171) [EIPs](/c/eips/5)




> No Intermediary NFT Trading Protocol With More Diverse Royalty Schemes
> Abstract
> Add a marketplace functionality to ERC-721 to enable non-fungible token trading without relying on an intermediary trading platform. At the same time, implement a mandatory, more diverse royalty scheme.
> Motivation
> Most current NFT trading relies on an NFT trading platform acting as an intermediary, which has the following problems:
>
> Security concerns arise from authorization via the setApprovalForAll function. The…

At the same time, If deemed necessary to better protect the interests of the project team and community, they may consider adding a blocklist to their implementation contracts to prevent NFTs from being traded on platforms that do not comply with the project’s royalty scheme.

## Other

There is currently no consensus on what the optimal royalty rate should be, and it must be said that the royalty rates of most projects lack scientific justification. On the one hand, excessively high royalties can harm the liquidity of NFTs and hinder the development of the industry. On the other hand, if a project or community loses royalty income in the early stages of industry development, they will lack the funds to sustain project operations. The recommended royalty rate should be decided through joint discussion among project teams, community members, and trading markets, but the plan must be aimed at promoting the further development of the industry, rather than just satisfying the interests of one party.

Meanwhile, projects should also actively consider expanding their revenue sources rather than relying solely on royalty income.

## Replies

**dievardump** (2023-02-28):

We’ve already talked about a bunch of those during the discussions for 2981.

That was the idea: make an interface that can easily answer to all/almost all of those scheme.

