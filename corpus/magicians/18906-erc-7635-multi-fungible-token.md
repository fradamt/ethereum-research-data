---
source: magicians
topic_id: 18906
title: "ERC-7635: Multi-Fungible Token"
author: memeking
date: "2024-02-23"
category: ERCs
tags: [erc, nft, erc-721]
url: https://ethereum-magicians.org/t/erc-7635-multi-fungible-token/18906
views: 1297
likes: 1
posts_count: 5
---

# ERC-7635: Multi-Fungible Token

We propose a Multi-Fungible Token (MFT) as a standard for defining and implementing various composite assets, such as financial assets and game assets.

This standard describes a new token paradigm with properties including TOKEN ID, SLOT, and SLOT BALANCE. The TOKEN ID functionality is similar to ERC-721, while the SLOT allows for customizable storage of multiple assets, including ERC-721, ERC-20, and other custom assets.

Each SLOT can be individually authorized or transferred, and the entire MFT can also be authorized or transferred. If a SLOT stores an NFT or FT asset, it can be transferred to another MFT or an address.

Under this token standard, it is possible to simulate various composite assets such as bank accounts, game accounts, financial products, and decentralized identifiers (DID). For example, an account can simultaneously hold savings accounts, investment accounts, credit accounts, and other assets. The account itself becomes a token that holds various other assets, which can be transferred together or individually.

Similarly, for game accounts with multiple characters, equipment, and game assets, this token standard offers significant convenience in managing and transferring such assets.

This is a discussion thread, and the latest proposals can be found in the following repository: [GitHub - memelabs-dev/ERC-7635](https://github.com/memelabs-dev/ERC-7635)

## Replies

**Swader** (2024-03-02):

This already exists in various comprehensive forms. See [evm.rmrk.app](https://evm.rmrk.app) for final ERCs regarding these use cases and more.

---

**memeking** (2024-03-08):

Thank you very much for pointing out the information and for being able to discuss ERC-7635 with you.

We have studied the multi-asset management protocols of RMRK and ERC-7635 in detail:

1. Similarities:

a. Flexibility:

Both protocols allow for flexible configuration of sub-asset types and attributes.

b. Centralization:

The parent NFT has the ability to manage the sub-assets, and the sub-assets can be transferred along with the parent NFT.

c. Diversification:

Both protocols support management of multiple tokens, types, and nested assets.

1. Differences:

a. Quantity Set and Pricing:

ERC-7635 follows a standardized sub-asset slot management approach, where each slot in an MFT contract has the same definition and can contain a quantity set of assets. These assets can be flexibly transferred, and their pricing is clear.

RMRK’s multi-asset protocol takes an independent approach to sub-asset management. Each NFT can hold different types of assets, and each sub-asset is treated independently, without the concept of a quantity set.

b. Token Types:

ERC-7635 supports ERC20 and ERC721 tokens in slots, as well as custom assets such as points or equities. The number of slots is unlimited.

RMRK’s multi-asset protocol supports ERC721 and ERC7401 tokens but does not support the management of ERC20 tokens.

c. Permission Allocation:

ERC-7635 allows for the allocation of managers and authorization quantities for each slot asset.

RMRK’s multi-asset protocol does not support separate authorization for sub-assets.

d. Trading Behavior:

ERC-7635 follows a slot-based standardization, where slot token assets can be flexibly combined to form liquidity pools and engage in market activities.

RMRK’s multi-asset protocol treats each sub-asset independently, allowing for individual trading of each sub-token asset.

In practical application scenarios, RMRK and ERC-7635 also have completely different use cases, which are based on different understandings of assets.

---

**pyrobit** (2024-03-11):

This is ‘idea stage’?

---

**memeking** (2024-03-11):

The draft has been submitted and now is the discussion period.

