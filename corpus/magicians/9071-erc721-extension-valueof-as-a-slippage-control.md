---
source: magicians
topic_id: 9071
title: "ERC721 Extension: `valueOf` as a slippage control"
author: shung
date: "2022-04-28"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc721-extension-valueof-as-a-slippage-control/9071
views: 506
likes: 0
posts_count: 1
---

# ERC721 Extension: `valueOf` as a slippage control

NFTs are more and more being used as financial instruments. This necessitates a standardized way of “slippage control”. I propose an extension that requires each token to have an inherent value defined. A single external function would suffice for this purpose:

`function valueOf(uint256 tokenId) external view returns (uint256);`

Using this standard, NFT marketplaces can employ slippage checks. Let me illustrate the problem and the solution with an example.

Let’s say there is an ERC721 contract in which each token represents a balance of an ERC20 token deposited. Let’s say someone has `tokenId: 3`, which holds 100 WETH tokens. And let’s say that the ERC721 contract has a function that allows you to withdraw WETH tokens represented in the NFT. You go on a marketplace, and intend to buy `tokenId: 3`. But the owner of `tokenId: 3` is a miner and frontruns your transaction, withdrawing all the WETH before your buy transaction goes through. Now you have paid a lot of money for nothing. The lack of slippage control can even cause problems inadvertently, because most NFT marketplaces do not update metadata live.

The solution would’ve been to use `valueOf`. If the aforementioned ERC721 contract had a `valueOf` function that showed the balance in each NFT, then the NFT marketplace contract could have used that standard method to ensure 0% slippage on trades.
