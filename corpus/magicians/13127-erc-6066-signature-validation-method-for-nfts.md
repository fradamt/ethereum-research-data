---
source: magicians
topic_id: 13127
title: "ERC-6066: Signature Validation Method for NFTs"
author: jpitts
date: "2023-03-02"
category: ERCs
tags: [nft, token, signatures]
url: https://ethereum-magicians.org/t/erc-6066-signature-validation-method-for-nfts/13127
views: 469
likes: 4
posts_count: 2
---

# ERC-6066: Signature Validation Method for NFTs

As [@boyuanx](/u/boyuanx) gave an lightning EIP talk today I am posting this here so we can discuss it.



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-6066)





###



A way to verify signatures when the signing entity is an ERC-721 or ERC-1155 NFT

## Replies

**stoicdev0** (2023-03-03):

Really interesting idea!

One doubt: why are you using a `bytes4` return of a magic value instead of a simple boolean?

