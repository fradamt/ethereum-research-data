---
source: magicians
topic_id: 21872
title: "EIP-7814: Introspection precompiles"
author: Brechtpd
date: "2024-11-28"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7814-introspection-precompiles/21872
views: 98
likes: 0
posts_count: 1
---

# EIP-7814: Introspection precompiles

Discussion topic for [EIP-7814](https://github.com/ethereum/EIPs/pull/9028)

# Abstract

This EIP proposes to add two precompiles that enable introspection of the chain state at arbitrary points within a block in the EVM. Currently, the EVM only has access to the state of previous blocks. No block data is currently exposed to the EVM for the block it’s executing in.

# Motiviation

The new precompiles aim to enhance introspection capabilities within the EVM, enabling the calculation of the latest chain state offchain at any point in an Ethereum block. This is important to allow general and efficient synchronous composability with L1. Otherwise, to ensure having the latest L1 state, the state would have to be read on L1 and passed in as a separate input. This is expensive and there may be limitations on who can read the state without something like [EIP-2330](https://eips.ethereum.org/EIPS/eip-2330).
