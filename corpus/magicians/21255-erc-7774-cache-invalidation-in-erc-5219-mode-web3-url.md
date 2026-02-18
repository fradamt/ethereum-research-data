---
source: magicians
topic_id: 21255
title: "ERC-7774: Cache invalidation in ERC-5219 mode Web3 URL"
author: nand
date: "2024-10-03"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7774-cache-invalidation-in-erc-5219-mode-web3-url/21255
views: 47
likes: 0
posts_count: 1
---

# ERC-7774: Cache invalidation in ERC-5219 mode Web3 URL

## Abstract

In the context of the ERC-6860 `web3://` standard, this ERC extends the ERC-6944 resolve mode: This standard add mechanisms to alleviate limitations to the use of standard [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) HTTP caching.

## Motivation

Calls to an Ethereum RPC provider are costly: CPU-wise for local nodes, and money-wise for paid external RPC providers. Additionally, external RPC providers are rate-limited, and can quickly lead to the breaking of the loading of `web3://` URLs.

Thus, it makes sense to use a caching mechanism to limit RPC calls when possible.

In the ERC-6944 resolve mode, smart contracts can already reply with standard [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) HTTP caching headers, such as `Cache-Control`, `ETag`.

Unfortunately, due to the impossibility of reading request HTTP headers, they cannot act on the `If-None-Match` and `If-Modified-Since` cache validation headers. Thus they are limited to the `Cache-control: max-age=XX` mechanism, and each cache validation request ends up with RPC calls regenerating the whole response.

This ERC defines a mechanism to bypass this limitation by having websites broadcast cache invalidations with smart contract events.

Besides, even if the smart contract could read request HTTP headers, using smart contract events is more efficient as it will eliminate a significant proportion of RPC calls.

## ERC pull request

https://github.com/ethereum/ERCs/pull/652

I’m still refining a bit, and I’m open to suggestions / ideas ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

Thanks!
