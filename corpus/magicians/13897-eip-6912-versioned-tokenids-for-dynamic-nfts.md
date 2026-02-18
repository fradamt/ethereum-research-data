---
source: magicians
topic_id: 13897
title: "EIP-6912: Versioned TokenIds for Dynamic NFTs"
author: emo
date: "2023-04-19"
category: EIPs
tags: [nft, erc-721]
url: https://ethereum-magicians.org/t/eip-6912-versioned-tokenids-for-dynamic-nfts/13897
views: 629
likes: 0
posts_count: 3
---

# EIP-6912: Versioned TokenIds for Dynamic NFTs

eip: 6912

title: Versioned TokenId Standard for Dynamic NFTs

author: James Wenzel (emo.eth, @emo_eth)

discussions-to: https://github.com/ethereum/EIPs/pull/6912

status: Draft

type: Standards Track

category: ERC

created: 2023-04-19

requires: 721

This EIP proposes an extension to the EIP-721 non-fungible token standard by introducing a Versioned TokenId standard for “dynamic” NFTs with on or offchain properties that may change over time. The new `versionedTokenId` is meant to track both the “identifier” of a token as well as its current “version” so that old outstanding orders and approvals for updated tokens are automatically invalidated.

See linked PR for latest details.

## Replies

**ashhanai** (2023-04-27):

Hey [@emo](/u/emo). Interesting EIP draft.

The described approach will probably work for marketplaces but fail for any protocol that uses escrow, like lending & renting with collateral. Those protocols assume that the `tokenId` will be immutable during the time locked in the protocol. By allowing `tokenId` updates (e.g., expired condition based on `block.timestamp`), those protocols cannot transfer the locked collateral back to the borrower or let the lender claim it, as they will not have the correct `tokenId`. The backward compatibility fails here.

I see another issue with deterministic `tokenId`s. If somebody updates the token to a new state and back, all existing bids will be invalidated.

Why not use [EIP-5646](https://eips.ethereum.org/EIPS/eip-5646)?

---

**SamWilsn** (2023-09-18):

Some non-editorial related comments:

Would you consider a function naming scheme closer to ERC-721? Something like `currentVersionedTokenIdOf(...)` and `encodedTokenIdentifierOf(...)`.

---

I find your function names *very* confusing. I might recommend removing the separate concepts of “token id”, “versioned token id”, and “identifier”, and just using “token id” on its own?

That would mean you’d only need a single function: `latestIdOf(uint256 tokenId)`.

---

You should mention in your Security Considerations something to the effect of:

> If a token is locked in a contract (eg. as collateral for a loan), and the metadata changes causing a version bump, the token may be lost forever.

---

You don’t mention what happens to ERC-721-style approvals when a version number bumps in the Specification section. Do they get ported to the new token, or lost, or is it implementation defined?

