---
source: magicians
topic_id: 13891
title: ERC-6909-multi-token-standard
author: jtriley-eth
date: "2023-04-19"
category: ERCs
tags: [erc, nft]
url: https://ethereum-magicians.org/t/erc-6909-multi-token-standard/13891
views: 8234
likes: 53
posts_count: 80
---

# ERC-6909-multi-token-standard

---

## eip: 6909
title: Multi-Token Standard
description: A minimal specification for managing multiple tokens by their id in a single contract.
author: Joshua Trujillo (@jtriley)
discussions-to:
status: Draft
type: Standards Track
category: ERC
created: 2023-04-19
requires: 165

*Edit: Removing full EIP to avoid duplicate updates. See PR for most recent changes.

## Replies

**axe** (2023-04-19):

I really like proposed simplified token standard, which aims to address some of the complexities found in the ERC-1155 standard.

> ERC6909Metadata

Do you see any utility of providing a standard way of changing metadata URI?

I think this can be a good solution: [Metadata Standards](https://docs.opensea.io/docs/metadata-standards#metadata-updates)

`event MetadataUpdate(uint256 _tokenId);`

---

**RenanSouza2** (2023-04-19):

1 - there is not a ‘getOperator’ function, what is the reason of it’s removal?

2 - Would you be willing to treat tokenId as bytes32 instead of uint256? this was always a pet peeve I had with ERC721 and ERC1155. The bad side would be less backwards compatibility.

ps: it is not good to copy the whole proposal here because it can get outdated compared to the one in github

---

**jtriley-eth** (2023-04-19):

1. This was an oversight, just added isOperator to the specification.
2. I would prefer uint256 for the sake of compatibility, are there specific advantages to bytes32 over uint256?
3. Updated, thank you!

---

**jtriley-eth** (2023-04-19):

It looks like OpenSea supports either the [EIP-4906](https://eips.ethereum.org/EIPS/eip-4906) `MetadataUpdate(uint256)` and `BatchMetadataUpdate(uint256,uint256)` events or the [EIP-1155](https://eips.ethereum.org/EIPS/eip-1155) `URI(uint256)` event.

The metadata extension currently doesn’t specify a URI update event, but I would favor `URI(uint256)` since the spec is close to EIP-1155 as-is.

---

**RenanSouza2** (2023-04-19):

Not many reasons to change from uint256 to bytes32 tbh, I just with the original protocols used bytes32 because it makes more sense as identifiers. Totally agree with you in keeping the compatibility.

Another thing that just came to my mint, Neither ERC20 nor ERC1155 required decimals to be implemented. Was this change intentional?

---

**jtriley-eth** (2023-04-19):

Just noticed ERC-20 requires it only in the metadata extension, but ERC-1155 only mentions it in the metadata spec.

I think it would make sense to require the decimals method in the metadata extension since it defaults to one (`10 ** 0`), so there’s no harm in implementing the method and not explicitly setting decimals for each token id.

Thoughts?

---

**RenanSouza2** (2023-04-19):

It is a great change, it makes decimals reliable enought defi protocols can use it and de default implementation is easy.

maybe talk about it in the rationale

---

**zachobront** (2023-04-20):

This is great, strong support for the idea of getting the bloat out of 1155.

I don’t love that decimals “SHOULD be ignored if not explicitly set to a non-zero value.” It’s not clear when decimals for each ID will be set, but seems likely to cause downstream problems that non-existent IDs will simply return 0, which could be used to creatively break share accounting.

I would recommend that either:

a) decimals is a consistent value across all ids on a given contract

b) the decimals mapping isn’t public, and instead uses a getter function that reverts if it’s set to zero

---

**RenanSouza2** (2023-04-20):

A contract can see the totalSupply for that tokenId and only care for the decimals if there is any token

the moment decimals is set is up to the implementation

setting a non zero decimal number would hurt the ability to represent fingible and non fungible tokens in the same contract

---

**jtriley-eth** (2023-04-20):

I like the idea of removing “SHOULD be ignored …” terminology, though I would argue against solution “a” since this may be used to wrap multiple assets of varying decimal amounts and  “b” because this would require contracts to use `try`/`catch` syntax for a view method on chain. The `tokenURI` being fallible is a product of ERC-721’s behavior, though decimals are more often queried on-chain than token uri’s.

Also, even if the decimals should never be ignored, querying decimals for an asset that have not been explicitly set will yield zero, which resolves to `n * 10 ** 0` or `n * 1`.

---

**RenanSouza2** (2023-04-20):

Hey,

the interfaceId needs to be updated to `0x3b97451a` if my calculation is correct

and what do you think about internal _mint and _burn in the Reference Implementation?

---

**jtriley-eth** (2023-04-24):

I computed a different interfaceId, `0xb2e69f8a`.

Also, I added the internal mint and burn logic to the reference!

---

**RenanSouza2** (2023-04-24):

I saw your commit and your value is correct, when I calculated again it matched with yours

---

**fubuloubu** (2023-05-04):

Really like this standard, and appreciate the usage of YAML definitions ![:sunglasses:](https://ethereum-magicians.org/images/emoji/twitter/sunglasses.png?v=12)

My one comment is that the token URI functionality should be a separate extension from the regular token metadata, for cases where it makes sense to define normal metadata (e.g. Give the the token a name, symbol and decimals) but not URI metadata (because the different IDs represent something semi-fungible such as tokens with different classes of rights or a progressive unlock)

---

**jtriley-eth** (2023-05-10):

Makes sense (re: URI breakout). What would this be called? ERC6909MetadataURI?

---

**RenanSouza2** (2023-05-17):

Hey, the next EIP Editing Office Hour Meeting is being discussed here: [EIP Editing Office Hour Meeting 18 · Issue #234 · ethereum-cat-herders/EIPIP · GitHub](https://github.com/ethereum-cat-herders/EIPIP/issues/234)

would you like to take your proposal there?

---

**jtriley-eth** (2023-05-18):

That would be great! What’s the best way to join the list?

---

**RenanSouza2** (2023-05-18):

it is very simple, just comment in the link above that you want to include your EIP for dicussion at the next meeting and say the EIP number and the PR number

---

**RenanSouza2** (2023-06-05):

I just found this new initiaitve and may be helpful to your project [[Current] Agenda for 3rd AllERCDevs (Asian / US Friendly) Tue, 2023-06-13 23:00 UTC · Issue #4 · ercref/AllERCDevs · GitHub](https://github.com/ercref/AllERCDevs/issues/4)

---

**calvbore** (2023-06-12):

One thing that I like about 1155 that isn’t here is the `bytes calldata _data` as additional arbitrary data in an unspecified format in the transfer functions. Personally, I would like to see them here as well, as they could be useful for extensions to the standard or for a specific token implementation.


*(59 more replies not shown)*
