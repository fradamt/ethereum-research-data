---
source: magicians
topic_id: 25832
title: "ERC-8050: Compressed RPC Link Format with Method-Specific Shortcuts"
author: brunobar79
date: "2025-10-16"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-8050-compressed-rpc-link-format-with-method-specific-shortcuts/25832
views: 112
likes: 0
posts_count: 2
---

# ERC-8050: Compressed RPC Link Format with Method-Specific Shortcuts

## Abstract

This ERC defines a compact, URL-safe payload format for JSON-RPC requests targeting wallet interactions. It uses Protocol Buffers for binary serialization, an optional Brotli compression layer, and Base64url encoding for transport. The format supports **shortcuts**: method-specific encodings that optimize size and structure for particular RPC methods. This ERC standardizes three shortcuts:

- Shortcut 0: Generic JSON-RPC (universal fallback for any method)
- Shortcut 1: wallet_sendCalls (EIP-5792) with optimized encodings for ERC20 transfers, native transfers, and generic calls
- Shortcut 2: wallet_sign (EIP-7871) with optimized encodings for spend permissions and receive-with-authorization signatures

## Motivation

Applications often need to pass wallet RPC requests through QR codes, NFC tags, or deep links. JSON is verbose and not URL-friendly at small sizes. This standard provides:

- Universal compatibility: Any JSON-RPC request can be encoded via the generic shortcut
- Optimization: Common transaction patterns achieve 60-80% size reduction via specialized shortcuts
- Interoperability: A single format works across apps, wallets, and programming languages
- Extensibility: New shortcuts can be added without changing the core format

This enables one-step, connection-agnostic flows for payments, signatures, and other wallet interactions.

## Replies

**brunobar79** (2025-10-16):

Draft here: [Add ERC: Compressed RPC Link Format with Method-Specific Shortcuts by brunobar79 · Pull Request #1261 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1261)

