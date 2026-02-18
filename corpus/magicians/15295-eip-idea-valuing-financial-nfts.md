---
source: magicians
topic_id: 15295
title: "EIP Idea: Valuing Financial NFTs"
author: 0xTraub
date: "2023-07-31"
category: EIPs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/eip-idea-valuing-financial-nfts/15295
views: 445
likes: 1
posts_count: 1
---

# EIP Idea: Valuing Financial NFTs

As DeFi continues to expand into new use-cases, the complexity of representing various financial positions can no longer be accomplished solely with fungible [ERC-20](https://github.com/Revest-Finance/EIPs_WIP/blob/master/eip-20.md) tokens. New financial NFTs (FNFTs) have no agreed upon standard for calculating their value on-chain. These financial positions tokenized as NFTs which cannot be valued cannot be used in DeFi. As a result a new standard is needed to be able to universally value these increasingly-complex financial instruments. Revest Finance proposes an extension ERC to ERC-721 and ERC-1155 to solve this problem.

Examples:

1. Velodrome Staking FNFTS
2. Revest Finance Vesting FNFTs
3. Liquid-Wrappers around Ve-Positions
4. JPEG’d FNFTs

The goal would be an EIP that allows an application (on or off chain) to easily determine the value of an FNFT in a specified asset through an easily auditable formula.

```auto
interface IValuableFNFT is IERC721/IERC1155 {
    // @notice      This function MUST return whether the asset which the FNFT is valued in terms of
    // @param       id  The token id of which to check the existence
    // @return      The address of the ERC-20 token to value the FNFT in.
    function getAsset(uint id) external view returns (address);

    // @notice      This function MUST return the number of tokens with a given id. If the token id does not exist, it MUST return 0.
    // @param       id The token id of which to fetch information
    // @return      Suggested market value of the FNFT in specified in units of "asset"
    function getBalance(uint id) external view returns (uint);
}
```

Possible Example: A staking FNFT worth 100 MockERC20 has a linear vesting period of 1 year and accumulates 5% APY. The value of the FNFT would be returned as `staked_tokens * (1 - time_remaining / total_lock_period) + staking_rewards`. This reflects that the NFT should trade at a discount since they are currently illiquid, with discount trending to zero as the lock matures, and also the increased value accrued from staking rewards.

Potential Applications Include:

1. More accurate FNFT lending
2. More accurate price-discovery on exchanges
3. Accurate valuing as collateral for ERC20-lending

The creators of the FNFT would be responsible for properly building out the functionality to value the FNFTs that they create.
