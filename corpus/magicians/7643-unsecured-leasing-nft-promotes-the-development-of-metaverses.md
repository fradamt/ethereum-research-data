---
source: magicians
topic_id: 7643
title: Unsecured Leasing NFT Promotes the Development of Metaverse's Sharing Economy
author: kkimos
date: "2021-12-01"
category: Magicians > Primordial Soup
tags: [erc, nft, token]
url: https://ethereum-magicians.org/t/unsecured-leasing-nft-promotes-the-development-of-metaverses-sharing-economy/7643
views: 1023
likes: 2
posts_count: 3
---

# Unsecured Leasing NFT Promotes the Development of Metaverse's Sharing Economy

This standard adds a new right of Non-Fungible Token that the right to use. Through this standard, you can achieve :

- Separation of the right to use and ownership of Non-Fungible Token
- Non-secured lease Non-Fungible Token
- You can continue to use it after you mortgage the Non-Fungible Token
- Metaverse sharing economy

It is precisely because of the separation of ownership and use right that the utilization rate of assets can be greater. You must distinguish between the rights of the user and the owner.

Different from 2615, we only added a right to use, so that we can get all the functions of 2615, and reduce many unnecessary operations in 2615. The explanation is as follows:

- The owner should not use some of the ownership rights when mortgage NFT, such as transfer, AXS-like breeding or weapon upgrade, because it is likely to change the status of the original NFT, so when the user mortgages the NFT, the ownership must be mortgaged in the contract middle.
- In the case of mortgage or transaction, the owner has the right to continue to use it before returning the ransom or selling it

This is the result of my implementation, you can refer to [cryptosharing (cryptosharing) · GitHub](https://github.com/cryptosharing)

## Replies

**wvans123** (2021-12-01):

Nice proposal for future metaverse sharing economy, wish a new era come

---

**Daniel-K-Ivanov** (2022-02-25):

Hi [@kkimos](/u/kkimos)

I think that you can check [ERC-4400: ERC-721 Consumer Extension](https://ethereum-magicians.org/t/erc-4400-erc721consumer-extension/7371) and see if it can be of use to your use-case.

