---
source: magicians
topic_id: 16790
title: "ERC-7565 Proposal: Perpetual contract NFT for DeFi composability"
author: HSKim
date: "2023-11-28"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-7565-proposal-perpetual-contract-nft-for-defi-composability/16790
views: 1182
likes: 1
posts_count: 1
---

# ERC-7565 Proposal: Perpetual contract NFT for DeFi composability

Discussion thread of [ERCs PR](https://github.com/ethereum/ERCs/pull/127)

Reference Implementation and test: [Repository](https://github.com/HyoungsungKim/ERC-proposal-implementation)

Draft: [draft](https://github.com/HyoungsungKim/ERCs/blob/master/erc-7565.md)

For an academic article, please visit [IEEE Xplore](https://ieeexplore.ieee.org/document/9967987/).

## Abstract

This ERC proposes a mechanism where a person (referred to as the “Asset Owner”) can collateralize NFTs that represent locked deposits or assets, to borrow funds against them. These NFTs represent the right to claim the underlying assets, along with any accrued benefits, after a predefined maturity period

## Motivaion

The rapidly evolving landscape of DeFi has introduced various mechanisms for asset locking, offering benefits like interest and voting rights. However, one of the significant challenges in this space is maintaining liquidity while these assets are locked. This ERC addresses this challenge by proposing a method to generate profit from locked assets using ERC-721 and ERC-4907.

In DeFi services, such as Uniswap v3, liquidity providers contribute assets to pools and receive NFTs representing their stake. These NFTs denote the rights to the assets and the associated benefits, but they also lock the assets in the pool, often causing liquidity challenges for the providers. The current practice requires providers to withdraw their assets for urgent liquidity needs, adversely affecting the pool’s liquidity and potentially increasing slippage during asset swaps.

Our proposal allows these NFTs, representing locked assets in liquidity pools, to be used as collateral. This approach enables liquidity providers to gain temporary liquidity without withdrawing their assets, maintaining the pool’s liquidity levels. Furthermore, it extends to a broader range of DeFi services, including lending and trading, where asset locking is prevalent. By allowing the collateralization of locked asset representations through NFTs, our approach aims to provide versatile liquidity solutions across DeFi services, benefitting a diverse user base within the ecosystem.

The concept of perpetual contract NFTs, which we introduce, exploits the idea of perpetual futures contracts in the cryptocurrency derivatives market. These NFTs represent the rights to the perpetual contract and its collateral, enabling them to be used effectively as collateral for DeFi composability. The perpetual contract NFT offers a new form of NFT that enhances the utility of locked assets, providing a significant advantage in DeFi applications by offering liquidity while retaining the benefits of asset locking.
