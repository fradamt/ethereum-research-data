---
source: magicians
topic_id: 17685
title: Extending ERC-721 Standard for Text-Based NFT Use in Social Media
author: moseiki
date: "2023-12-27"
category: EIPs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/extending-erc-721-standard-for-text-based-nft-use-in-social-media/17685
views: 955
likes: 1
posts_count: 1
---

# Extending ERC-721 Standard for Text-Based NFT Use in Social Media

- description: Aims to extend the ERC721 standard to facilitate the storage and use of text-based content as NFTs in social media.
- authors: Berk Şimşek(@SİmsekBerk), Tuğgün Asrak, Ediz Züm
- Requires: EIP-721
- created: 2023-12-27
- Github Link: link

**Abstract**

This EIP proposes an extension to the ERC721 standard, aiming to facilitate the storage and use of text-based content as NFTs, particularly on social media platforms.It is intended for use in the social media platform **Moseiki App**. This extension seeks to eliminate the need for backend queries each time by directly storing NFT metadata in smart contracts in bytes format.

**Motivation**

The current ERC721 standard typically stores NFT metadata accessible via an external URL. This approach requires additional backend infrastructure for storing and accessing metadata. Especially in the context of social media platforms, this extra step can negatively impact user experience and reduce efficiency. This EIP suggests storing metadata directly in the smart contract, aiming to simplify the process and enhance efficiency.

**Specification**

- The smart contract is based on the ERC721 standard and is defined as a contract named mos.
- The mint function allows users to create new NFTs on the Ethereum blockchain. During this process, the NFT’s metadata and copyright information are set, and a unique tokenId is assigned to each new NFT. The function stores the NFT’s metadata in bytes format and allows the NFT owner to set a percentage for copyright.
- Metadata for each NFT is stored in the smart contract in bytes format.
- The mintWithBytes function enables users to submit metadata directly in bytes format.
- The tokenURI function converts and returns the stored bytes data into a string format.
- The contract also manages royalty information for NFTs.
- The contract includes a helper function named stringToBytes, used to convert text-based data into bytes format.

**Backwards Compatibility**

This EIP is compatible with the existing ERC721 standard and is designed as an extension of this standard. Existing ERC721-based applications can operate compatibly with this extension.
