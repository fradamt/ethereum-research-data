---
source: magicians
topic_id: 8699
title: "Eth JSON-RPC method for faster block updates: eth_getNextBlock"
author: danfinlay
date: "2022-03-23"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/eth-json-rpc-method-for-faster-block-updates-eth-getnextblock/8699
views: 850
likes: 3
posts_count: 2
---

# Eth JSON-RPC method for faster block updates: eth_getNextBlock

Today, the JSON-RPC API exposes a few different methods to get blocks:

- eth_getBlockByNumber
- eth_getBlockByHash

When using this API, the common way to get the latest block is to repeatedly poll for `getBlockByNumber` for the `current_block_number + 1`.

We could gain additional performance for JSON-RPC consumers by allowing them a way to get an immediate notification upon the next block, via [long polling](https://ably.com/topic/long-polling), ie the request would not resolve until the result was ready. Proposed name: `eth_getNextBlock`. Maybe it could take an argument for a known block, so the host could return a block that builds on it as soon as it’s available, allowing a graceful lazy walk up the block chain.

This doesn’t replace the utility of using Websocket based APIs, but can improve the performance for the JSON-RPC based interface.

Thoughts?

## Replies

**danfinlay** (2022-03-23):

On reorgs:

The method could take an optional parameter for the number of confirmations desired, servers could choose whether or not to implement that (to preserve open connection efficiency). Otherwise, this method would default to being understood as an optimistic (next known block) method, and consumers of it would need to handle the possibility of reorgs on their own.

