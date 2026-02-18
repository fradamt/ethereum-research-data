---
source: magicians
topic_id: 14935
title: "EIP-7280: NFT Metadata Extension like JSON-LD"
author: yoheinishikubo
date: "2023-07-05"
category: EIPs
tags: [nft, token, semantic, json-ld]
url: https://ethereum-magicians.org/t/eip-7280-nft-metadata-extension-like-json-ld/14935
views: 1177
likes: 2
posts_count: 1
---

# EIP-7280: NFT Metadata Extension like JSON-LD

I am now working with an airline company to mint NFTs as proofs of carbon-offset flights and trying to expand the project to all companies in the industry.

In terms of the nature of blockchains, we would like to have a long-living and flexible standard for semantic data structure with metadata of NFTs to be used from computers.

On the other hand, I think the basic concept for metadata of NFT should be free.

I found this agenda is like the relationship among HTML and JSON-LD.

So, I designed a loose standard for metadata of NFTs.

Add a new property called `linked_data` to the top of the tree of NFT metadata JSON.

`linked_data` contains a array of objects which have both `schema` and `data` properties.

I knew that the similar specification is already proposed as ERC-4955.

However, it is not so handy because of its type is `object`. The future developers should know the entity keys of the object in advance.

In addition, the property name `linked_data` could make it more clear how to be used.

Pull Request URL is the following:

https://github.com/ethereum/ERCs/pull/417
