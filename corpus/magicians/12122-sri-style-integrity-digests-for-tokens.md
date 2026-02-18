---
source: magicians
topic_id: 12122
title: SRI-style Integrity Digests for Tokens
author: tim-cotten
date: "2022-12-13"
category: Magicians > Primordial Soup
tags: [nft, gas, security, hashing, integrity]
url: https://ethereum-magicians.org/t/sri-style-integrity-digests-for-tokens/12122
views: 616
likes: 1
posts_count: 2
---

# SRI-style Integrity Digests for Tokens

In the games industry I have a lot of discussions with traditional Web 2.0 devs about Web3 & NFTs. When we debate utility of tokens often we call back to the “degraded blockchain” problem that Lars Doucet talks about coupled with Moxie Marlinspike’s take on ERC-721 & ERC-1155 lacking any form of integrity digest for the JSON metadata that NFTs might point to. ([Moxie Marlinspike >> Blog >> My first impressions of web3](https://moxie.org/2022/01/07/web3-first-impressions.html))

Has there been any work on this?

I implemented a simple scheme as an example in this contract: https://etherscan.io/address/0x0e20655885c38b1b5cedfff5b15289b76f3cdefc#code

The minting function requires at the time of minting that the contract owner attest a SHA-256 hash representing the contents of the JSON metadata that the tokenId points to. (There’s some additional logic in there to allow minting and burning singular instances of the token, and when burned the contract owner can re-mint with new metadata/new digest. Only if the current owner voluntarily burns their token though: it’s sort of a mutual-consent upgrade path).

It’s implemented using a getIntegrity(tokenId) method that returns a string of form {algo}-{digest} where {algo} is baked into the method itself (to save space, rather than store a uint256 pair for algo/digest) and relies on another mapping called _integrities.

This causes each mint to take an additional ~20k gas, but allows off-chain validation of the pointed to metadata in the same way SRI does it for Web 2.0.

The relevant lines in the single file compilation are 2223 - 2321.

Reinventing the wheel? Is this already a standard somewhere and I just missed it?

## Replies

**tim-cotten** (2022-12-13):

BTW, the W3C’s spec is here: [Subresource Integrity](https://www.w3.org/TR/SRI/)

An example implementation in HTML5 looks like:

```auto

```

