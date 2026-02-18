---
source: magicians
topic_id: 22718
title: "New ERC: Wallet Signing API"
author: lsr
date: "2025-01-29"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-wallet-signing-api/22718
views: 82
likes: 1
posts_count: 1
---

# New ERC: Wallet Signing API

## Abstract

Defines a new JSON-RPC method which enables apps to ask a wallet to sign EIP-191 messages.

Applications can use this JSON-RPC method to request a signature over any version of `signed_data` as defined by EIP-191. The new JSON-RPC method allows for support of future EIP-191 `signed_data` versions.

The new JSON-RPC method also supports EIP-5792-style `capabilities`, and support for signing capabilities can be discovered using `wallet_getCapabilities` as defined in EIP-5792.

## Motivation

Wallets and developer tools currently support multiple JSON-RPC methods for handling offchain signature requests. This proposal simplifies wallet & tooling implementations by consolidating these requests under a single `wallet_sign` JSON-RPC method. This also leaves room for new EIP-191 `signed_data` versions without needing to introduce a new corresponding JSON-RPC method.

Furthermore, this new `wallet_sign` method introduces new functionalities via EIP-5792-style `capabilities`.
