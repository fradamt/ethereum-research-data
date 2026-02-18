---
source: magicians
topic_id: 12553
title: Integrating cryptographic proof of NFT metadata veracity on-chain
author: tim-cotten
date: "2023-01-13"
category: Magicians
tags: [nft, cryptography]
url: https://ethereum-magicians.org/t/integrating-cryptographic-proof-of-nft-metadata-veracity-on-chain/12553
views: 435
likes: 0
posts_count: 1
---

# Integrating cryptographic proof of NFT metadata veracity on-chain

I wrote about this vaguely in a primordial soup a month ago, but I’ve since solidified the ideas in a blog post.

Problem: When NFT’s point to optional metadata stored off-chain there is no on-chain mechanism that a browser/wallet can use to validate that the metadata hasn’t been tampered with.

Solution: In Web 2.0 the W3C standardized Subresource Integrity (SRI) which allows resources in HTML to declare their integrity digests & hashing algorithm so the browser can download the resource, hash it, compare it with the declared integrity digest, and then pass/fail the resource. We can do the same on-chain by providing a simple interface for getIntegrity(tokenId) that returns the SRI-formatted hashing-algorithm + base64-encoded integrity digest.

Caveat: browsers/wallets will have to adopt both checking for the interface and validating off-chain metadata, but this can be a powerful tool against future malicious NFT projects.

Full details here:

https://blog.futureofgaming.wtf/making-metaverse-nfts-a-little-more-trustworthy-5e7dd254256

Looking for contributors to help us draft an EIP.

Previous topic where I first thought about the idea: [SRI-style Integrity Digests for Tokens](https://ethereum-magicians.org/t/sri-style-integrity-digests-for-tokens/12122)
