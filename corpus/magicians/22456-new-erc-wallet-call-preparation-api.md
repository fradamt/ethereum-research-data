---
source: magicians
topic_id: 22456
title: "New ERC: Wallet Call Preparation API"
author: lsr
date: "2025-01-08"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/new-erc-wallet-call-preparation-api/22456
views: 100
likes: 0
posts_count: 2
---

# New ERC: Wallet Call Preparation API

## Abstract

This proposal defines complementary JSON-RPC methods to EIP-5792’s `wallet_sendCalls`. While `wallet_sendCalls` is used for an app to submit `calls` to be signed and submitted in a wallet’s interface, the methods in this proposal are for an application to request prepared calls (where “prepared” depends on the wallet implementation) to be signed and submitted by the application itself.

## Motivation

With more recent developments in account abstraction and session keys, there is an increasing need for applications to be able to sign and submit operations without switching to a wallet interface (e.g. browser extension). This can be tricky because different account implementations might have different call data encoding, signature formats, etc. To remedy this, we need a way for apps to know how to submit an operation for any account implementation.

See more: https://github.com/ethereum/ERCs/pull/758

## Replies

**SamWilsn** (2025-01-29):

I’m not familiar enough with user ops, but I just wanted to ask if these endpoints encourage blind signing? Can the wallet server display useful information, or does it just get the hash?

