---
source: magicians
topic_id: 20761
title: "ERC-7753: Algorithmically generated NFT"
author: chen4903
date: "2024-08-09"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7753-algorithmically-generated-nft/20761
views: 221
likes: 3
posts_count: 5
---

# ERC-7753: Algorithmically generated NFT

A non-fungible token standard that uses mathematical algorithms to draw and store images without any servers or storage space.

The current NFT solutions store images on IPFS or third-party servers, consuming storage space and being separate from the blockchain. Our goal is to represent image information using mathematical algorithms stored in smart contracts, tightly integrating with the blockchain. This approach uses no storage space and allows anyone to render the image information at any time based on the algorithm stored in the smart contract.

Here’s an [example](https://www.desmos.com/calculator/vvgkvwzvkq?lang=en) of using mathematical algorithms to draw dynamic flames.

https://github.com/ethereum/ERCs/pull/584

## Replies

**abcoathup** (2024-08-09):

The proposal doesn’t cover that onchain NFTs using data URIs have existed for some time.


      ![](https://ethereum-magicians.org/uploads/default/original/2X/4/4b049fb6d2c20af9319b4f9ef69ae0c1b6832b84.png)

      [simondlr.com](https://home.simondlr.com/posts/flavours-of-on-chain-svg-nfts-on-ethereum)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/b/be9924a83644ea2f5351b88fed096342953909f3_2_690x423.jpeg)

###



NFTs, as unique items on the blockchain, has a URI that points to data containing the metadata & the corresponding visuals. This URI can be an HTTP link, pointing to a video or image hosted on a normal server, or other services like IPFS...










What should be returned by `tokenURI`?

ERCs don’t need to include admin methods e.g. `setTokenAlgorithm`

---

**chen4903** (2024-08-10):

Storing SVG files often requires writing a large amount of data, which can significantly increase gas consumption. However, by using mathematical algorithms, a large number of different images can be represented through just a few simple formulas and variables, resulting in minimal storage requirements (only a few formulas and variables). Moreover, representing images through mathematical algorithms has a modular nature, allowing for significant changes to an image by adding, removing algorithms, or altering variables.

I think we could: instead of traditionally using URLs(`tokenURI`) to point to images, we can switch to pointing to mathematical algorithms.

---

**bestape** (2024-08-18):

Have a look at [iNFT](https://ape.mirror.xyz/FjUVEcUrDmQISEmcVarGEDHt6mLK9VOjLbxXgFy4edE) as a proof-of-concept example that uses a base64 onchain-stored wrapper of IPFS-stored JavaScript that generates SVG tessellations.

Would this solution work for your math as well?

---

**SamWilsn** (2024-10-14):

I am going to echo [@abcoathup](/u/abcoathup)’s comment that ERCs shouldn’t include functions that are only going to be called by the contract’s owner. The owner already knows how to interact with their contract, and over-specifying interfaces hurt flexibility.

I’d also suggest renaming the event to `AlgorithmChange`, and the getter to just `algorithmOf` to match ERC-721’s naming convention.

