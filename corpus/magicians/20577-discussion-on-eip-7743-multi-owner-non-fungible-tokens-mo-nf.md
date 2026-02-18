---
source: magicians
topic_id: 20577
title: "Discussion on EIP-7743: Multi-Owner Non-Fungible Tokens (MO-NFT)"
author: jamesavechives
date: "2024-07-17"
category: ERCs
tags: [nft]
url: https://ethereum-magicians.org/t/discussion-on-eip-7743-multi-owner-non-fungible-tokens-mo-nft/20577
views: 387
likes: 0
posts_count: 3
---

# Discussion on EIP-7743: Multi-Owner Non-Fungible Tokens (MO-NFT)

Hi everyone,

I’d like to start a discussion on my new EIP-7743: Multi-Owner Non-Fungible Tokens (MO-NFT).

**Abstract**:

This EIP proposes a new standard for non-fungible tokens (NFTs) that supports multiple owners. The MO-NFT standard allows a single NFT to have multiple owners, reflecting the shared and distributable nature of digital assets. This model also incorporates a mechanism for value depreciation as the number of owners increases, maintaining the principle that less ownership translates to more value.

**Motivation**:

Traditional NFTs enforce a single-ownership model, which does not align with the inherent duplicability of digital assets. MO-NFTs allow for shared ownership, promoting wider distribution and collaboration while maintaining secure access control. This model supports the principle that some valued information is more valuable if fewer people know it, hence less ownership means higher value.

You can view the full proposal and PR [here](https://github.com/ethereum/ERCs/pull/539).

I welcome any feedback, suggestions, or discussions on this proposal.

Thank you!

## Replies

**SamWilsn** (2025-02-04):

This standard seems similar to [Update ERC-7628: Move to Last Call by chenly · Pull Request #868 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/868). Perhaps a potential to collaborate?

---

**jamesavechives** (2025-02-09):

**Thank you for bringing up ERC-7628!** While both proposals aim to extend the non-fungible token paradigm, each addresses different design goals:

- ERC-7743 (MO-NFT)

Additive Ownership: Multiple owners can co-exist for a single token; each transfer adds a new owner without removing existing owners.
- Provider-Driven Model: Introduces fees paid to a provider for each transfer, supporting use cases like digital file assets and service-based royalties.
- Minimal ERC-721 Logic: The contract does not rely on the standard single-owner transfer or ownerOf mechanics; instead, it redefines these in terms of multi-owner sets. Some ERC-721 functions (like approve) are intentionally disabled to reflect shared ownership.

**ERC-7628**

- Fractional Ownership: A single ERC-721 token can represent multiple shares of ownership, each transferrable or partially controlled.
- Allows Share Transfers: Shares can be approved, transferred to another token, or even minted to a new address, making partial ownership easy to subdivide.
- Focuses on Profit-Sharing and Fine-Grained Fractional Rights: Perfect for scenarios that require precise distribution of revenue or partial investment in a single unique token.

**Collaboration Potential**

If there’s a project that needs both multi-owner sets **and** fine-grained fractional shares, merging the concepts of ERC-7743 and ERC-7628 could be valuable. One might implement a multi-owner structure from 7743 and layer fractional shares on top, as in 7628, so each “owner” has a fractional stake within a broader set of owners.

**Why They Differ**

- ERC-7743 essentially replaces standard ERC-721 single-owner logic with a multi-owner paradigm, disabling or overriding traditional functions like approve and the typical single ownerOf.
- ERC-7628 retains core ERC-721 mechanics—maintaining a single owner for each token—but adds the concept of fractional shares inside that single ownership token, allowing partial transfer of ownership rights.

In short, **ERC-7743** and **ERC-7628** have different design philosophies. **ERC-7743** best suits collaborative digital assets requiring multiple concurrent owners, while **ERC-7628** suits fractional share distribution under a single token. They could synergize if a use case demands both multi-owner sets *and* fractional shares.

