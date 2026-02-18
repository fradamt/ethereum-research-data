---
source: magicians
topic_id: 7300
title: Distribute ERC20 inside ERC721
author: nft
date: "2021-10-20"
category: Uncategorized
tags: [erc-721, gas, eth1x, erc-20]
url: https://ethereum-magicians.org/t/distribute-erc20-inside-erc721/7300
views: 939
likes: 0
posts_count: 2
---

# Distribute ERC20 inside ERC721

Say I have an ERC721 contract (contract A). I want to build another ERC721 (contract B) that can

1. Generate an ERC20 tokens (contract C) over time, like 1 token a day, for contract B’s owners.
2. Can let all owners of contract A to mint 1:1 token from their # of Contract A’s tokens owned for free and charge non owners X ETH fee.
3. Can assign X amount of contract C’s tokens to claim for free for contract A’s owners. Even better if the more rare contract A’s token is, the more tokens owners can claim for Contract C.
4. Enable contract C token to be swapped on Uniswap pairing with WETH and have its own logic for auto staking, tax penalty for swapping the tokens (Like Safemoon).
5. Can be listed on Opensea.io

The goal here is to provide value for owners of Contract A being able to get Contract B tokens for free, get free and earn tokens of Contract C over time. Contract C’s token can be traded on Uniswap as any other ERC20.

The priorities here are quick implementation, less approval for low gas and low complexity as possible. Preferably some off-the-shelf contract to base on.

What would be the optimal solution for this use case. I’d love to discuss about pros and cons of using ERC1155, ERC721 with an ERC20 child as property, ERC998, etc…? Thanks

## Replies

**nft** (2021-10-21):

Anyone has a lead here?

