---
source: magicians
topic_id: 11757
title: "EIP-1898: Add `blockHash` option to JSON-RPC methods that currently support defaultBlock parameter"
author: macfarla
date: "2022-11-16"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1898-add-blockhash-option-to-json-rpc-methods-that-currently-support-defaultblock-parameter/11757
views: 1979
likes: 0
posts_count: 1
---

# EIP-1898: Add `blockHash` option to JSON-RPC methods that currently support defaultBlock parameter

Raising EIP-1898 - basically adding the option to query by blockHash in JSON-RPC methods that currently support defaultBlock parameter - so you can specify block number, tag, or blockHash. This enables querying irrespective of the canonical chain.

This EIP has fallen into stagnant status but it is already supported by at least Geth and Besu:

- Geth 1.9.6 (PR 19491)
- Besu 20.10.4 (PR 1784)

PR changing status from stagnant to draft [EIP-1898 - change back to draft by macfarla · Pull Request #5980 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/5980)

and adding relevant parts to the execution-apis spec [add option for blockHash per EIP-1898 by macfarla · Pull Request #326 · ethereum/execution-apis · GitHub](https://github.com/ethereum/execution-apis/pull/326)

Feedback welcome!
