---
source: magicians
topic_id: 8157
title: Request for feedback - delegating proof of ERC-721 token ownership to another wallet
author: ethanj.eth
date: "2022-01-31"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/request-for-feedback-delegating-proof-of-erc-721-token-ownership-to-another-wallet/8157
views: 457
likes: 1
posts_count: 1
---

# Request for feedback - delegating proof of ERC-721 token ownership to another wallet

### Motivation

People use hot wallets and cold wallets. Especially in the case of NFT, the expensive NFTs will be stored in a cold wallet. However, in order to verify you hold a certain NFT, you have to log in with your cold wallet as well. This creates a lot of mental burden for the actual owner of the wallets.

For example, someone may use their hardware/cold wallet to store an expensive Artblocks NFT, and another project may need to verify the ownership of the expensive NFT, the owner will have to connect to their hardware wallet, which conflicts with the purpose of making the wallet cold.

### Idea

The idea will be creating an interface for delegating the ownership of NFTs from one wallet to another, thus applications can just verify the delegation, instead of the actual ownership.

This is my first opened issue, would love to hear feedbacks!
