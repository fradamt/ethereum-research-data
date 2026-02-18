---
source: magicians
topic_id: 9773
title: NFT Minimum Sales Price Standard
author: marco
date: "2022-06-28"
category: Magicians > Primordial Soup
tags: [nft]
url: https://ethereum-magicians.org/t/nft-minimum-sales-price-standard/9773
views: 498
likes: 0
posts_count: 1
---

# NFT Minimum Sales Price Standard

My team and I would like to introduce a new ERC standard to set a **minimum price** for an NFT.

Example:

1. Company releases collection A and user mint token B at a price chosen by A.
2. User wants to resell token B through a NFT marketplace.
3. The marketplace, however, must (as works for royalties with ERC-2981) check whether the NFT has a minimum selling price imposed by the creator of the contract. If it does, the user will not be able to list it for less.

This ERC can be used to sell real objects whose value can never drop in price but only increase over time.

Feedback, discussions, and comments are welcome.
