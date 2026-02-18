---
source: magicians
topic_id: 11423
title: Global NFT URIs
author: davux
date: "2022-10-21"
category: Magicians > Primordial Soup
tags: [nft, token, standards-writing]
url: https://ethereum-magicians.org/t/global-nft-uris/11423
views: 620
likes: 2
posts_count: 2
---

# Global NFT URIs

Hello,

**TLDR:**

- urn:nft::

urn:nft:erc721:::

**Longer version:**

On the offchain-wide web, there is sometimes a need to **refer to NFTs through a unique URI**.

An NFT does have a uniqueish ID but that is normally very namespaced, typically internal to a smart contract for ERC721-based tokens. There is not a globally unique way to refer to NFTs, so people end up describing them or configuring them through multiple pieces of information (*“the NFT of type ERC721 with ID xxx on contract 0xabc on the mainnet”*) or, worse, through a centralized marketplace URL (no example here, out of decency).

To address that gap, a simple and standard approach would be to introduce URNs with an `nft` namespace, as described in TLDR#1 above. Basically, it’s `urn:nft:<method>:<identifier>`, where `<method>` is the type of NFT you’re working with, and `<identifier>` is an identifier that makes sense for that type of NFT.

As both an illustration and a serious proposal, ERC721 NFTs would be described as `urn:nft:erc721:<identifier>`, where identifier is `<chain_id>:<contract_address>:<token_id>`. See spec URL in TLDR#2 above.

Of course, it would be great to see proposals for the other types of NFTs out there.

Such URIs would be useful to improve interoperability in the NFT world, including marketplaces and wallets. Imagine copying your NFT URI from a marketplace and just pasting it quickly in your wallet to have it appear there.

**Bold CTA:**

I would really like to know your thoughts, here and/or in the repos’ issues.

## Replies

**lambdalf-dev** (2022-12-01):

I like this idea a lot, one point of concern would be about maintaining uris and how to pay for the storage of the data that is referenced. This comes at a cost that oftentimes is not a one-time payment

