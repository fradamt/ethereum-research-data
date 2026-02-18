---
source: magicians
topic_id: 14070
title: "EIP-6960: - Dual Layer Token"
author: Aboudjem
date: "2023-04-30"
category: EIPs
tags: [nft, token, rwa, real-world-asset]
url: https://ethereum-magicians.org/t/eip-6960-dual-layer-token/14070
views: 2644
likes: 4
posts_count: 1
---

# EIP-6960: - Dual Layer Token

Hey Ethereum Magicians! ![:waving_hand:](https://ethereum-magicians.org/images/emoji/twitter/waving_hand.png?v=15)

Introducing [EIP-6960](https://github.com/ethereum/EIPs/pull/6960), the Dual Layer Token Standard designed to improve token classification and management on Ethereum. Let’s dive into the key points:

- Addresses limitations of ERC-1155 in managing tokens with multiple classifications
- Specially designed for Real World Assets (RWAs) and fractionalization of assets
- Two-level classification system for enhanced organization and management

Explore the details:

## Introduction

Tokenization is the core of a token-based economy, it transfers the value of real-world assets (RWAs) to the digital world hence improving their tradability and unlocking new markets for otherwise illiquid assets. In such an economy, it is important to facilitate different investment structures to allow a far broader and diverse investor base to participate.

Fractional ownership is a common investment approach that gives individuals the opportunity to own a portion or share of a high-value asset that they typically wouldn’t be able to afford as a whole. It has many advantages including lower costs, portfolio diversification, and distributing the responsibility of maintaining the asset among multiple owners.

## Problem statement

The existing token standards lack the ability to support fractional ownership of both fungible and non-fungible tokens. While ERC-6150 is an extension of ERC-721 that standardizes an interface for the hierarchical representation of NFTs in a tree-like structure, its implementation is limited to NFTs only. This highlights the need for a more comprehensive standard that provides the same features as ERC-1155 but with added flexibility and support for hierarchical representation and fractional ownership.

## Purpose

This EIP proposes a token standard that supports the hierarchical representation of both fungible and non-fungible tokens through a dual-layer classification where one main asset (layer 1) can be further sub-divided into several sub-assets (layer 2) and the total supply on each layer is being stored.

[![Dual-Layer-Token-for-RWA-1](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9ebeaab6b43140586e95090b9bf40f2721030e21_2_690x263.png)Dual-Layer-Token-for-RWA-11022×390 29.2 KB](https://ethereum-magicians.org/uploads/default/9ebeaab6b43140586e95090b9bf40f2721030e21)

If we take an invoice as an example, in a token-based economy, it can be tokenized and fractionalized for investors to own. By implementing the dual-layer token standard, a `mint` function assigns an owner to a fraction worth a certain amount by taking the following values:

- wallet address of buyer or investor
- main Id of invoice
- sub Id of the invoice fraction
- amount of the invoice fraction

The standard can be implemented in many more cases and on many different kinds of real-world assets which reflects its flexibility and robust design.

## Methodology

To create a multi-token standard interface based on a dual-layer classification, we couldn’t simply extend the ERC1155 interface as it would require significant modifications to do so. Hence, a standalone interface would be a more suitable approach that draws its design inspiration from the ERC1155 standard.

Each token is assigned with a mainId if it represents a main asset and its sub-assets are assigned with subIds that might have their own metadata, supply, and other attributes. The relationship between a mainId and its subIds is one-to-many but can be extended to support other types of relationships. Furthermore, sub-assets are nested into a main asset and are identified by passing their parent token id (mainId) and their respective subId to each method.

The classification layer is limited to two-levels, this means that a sub-asset can’t have children of their own. Otherwise, it would be necessary to introduce additional methods to track each sub-asset and its derivatives, which is impractical and increases the complexity of the contract.

`DLT` is the core interface that is required for a `DLT` compliant contract whereas `DLTReceiver` interface handles the safeTransfer of dual-layer token types. The standard is designed to be unopiniated allowing developers to access the internal functions in `DLT` and expose them as external functions in the way they prefer. Additionally, we offer a `DLTEnumerable` extension defined in the EIP 6960 that adds enumerability of all the main ids and subIds in the contract as well as total supply by each mainIds and subIds.

Join the discussion, share your thoughts, and help us refine this exciting new token standard!
