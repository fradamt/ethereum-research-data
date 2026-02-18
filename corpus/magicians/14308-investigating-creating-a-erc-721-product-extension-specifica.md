---
source: magicians
topic_id: 14308
title: Investigating creating a ERC-721 Product Extension specification for managing collection level metadata that characterizes tokenUri trait attributes
author: rpedersen
date: "2023-05-16"
category: EIPs
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/investigating-creating-a-erc-721-product-extension-specification-for-managing-collection-level-metadata-that-characterizes-tokenuri-trait-attributes/14308
views: 414
likes: 1
posts_count: 1
---

# Investigating creating a ERC-721 Product Extension specification for managing collection level metadata that characterizes tokenUri trait attributes

eCommerce applications, like Decentraland Marketplace and OpenSea, support facetted filtering that require the app to know details about NFT trait level data structure and value ranges and lists.  OpenSea centrally manages this type of information and makes it available via API’s.  I’m thinking of creating a specification that allows this information to be referenced on chain via a collectionURI and a standard collection metadata schema.

Here is an idea for a specification:  [Rich Canvas - ERC-721 Product Extension](https://www.richcanvas3.com/erc-721-product-extension).  I’ve created a Decentraland land sale proof-of-concept based on this approach.

Being new to this forum I’m not sure how to get these types of discussions going.  There are some standards that are close, but I cannot find anything that dictates a specific schema for a collection level metadata focused on ecommerce products.

Any help or direction is much appreciated.

Rich
