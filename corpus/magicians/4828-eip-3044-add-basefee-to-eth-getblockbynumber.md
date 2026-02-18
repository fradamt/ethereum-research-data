---
source: magicians
topic_id: 4828
title: "EIP-3044: Add basefee to eth_getBlockByNumber"
author: abdelhamidbakhta
date: "2020-10-14"
category: EIPs
tags: [json-rpc, eip-1559]
url: https://ethereum-magicians.org/t/eip-3044-add-basefee-to-eth-getblockbynumber/4828
views: 2292
likes: 0
posts_count: 1
---

# EIP-3044: Add basefee to eth_getBlockByNumber

https://github.com/ethereum/EIPs/pull/3044

[EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) introduces a base fee per gas in protocol.

This value is maintained under consensus as a new field in the block header structure.

This change should be reflected in RPC methods that return block header information.
