---
source: magicians
topic_id: 8671
title: Help with optimising gas fees for on chain NFTs
author: pentasir
date: "2022-03-21"
category: Uncategorized
tags: [nft, gas]
url: https://ethereum-magicians.org/t/help-with-optimising-gas-fees-for-on-chain-nfts/8671
views: 890
likes: 1
posts_count: 2
---

# Help with optimising gas fees for on chain NFTs

Is there a way to optimise gas fees when uploading metadata and images directly to the blockchain? Uploading metadata to IPFS is a very Web2 solution and is not the right direction to take. The only problem with uploading directly to the chain is the costly gas price. Is there a way to minimise/cap the gas fees when minting?

I am new around here so thank you for your patience.

## Replies

**mvillere** (2022-03-24):

Check out how I did on-chain metadata for Solidarity for Ukraine, a project that we did with the artist JR.

The main contract is here: https://etherscan.io/address/0x53142464F2FaeCE413aaf1886e9f21D6113D1257#code

The metadata contract is here:

https://etherscan.io/address/0x7397f20b4b2ebcd385860718082f6d3e59c1654d#code

This approach worked because the project only features two art variants. The reason why I did it with on-chain metadata is because it is an open edition, and it could potentially have 10s or 100s of thousands of sales (for charity of course), and uploading really large folders to IPFS can get glitchy. Pinata web interface only likes up to 50k or so files.

The gas cost of the main contract was about 3.5M gas. The gas cost of the metadata contract was about 1.5M gas. The only function that uses the metadata was the tokenURI function, which is almost always called off-chain, so the gas cost of that function isn’t applicable.

Good luck. If you have questions, you can find me in the NFTCulture discord in developer home channel, or dm me on twitter, @NiftyMike.

