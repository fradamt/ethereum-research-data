---
source: magicians
topic_id: 4830
title: "EIP-3046: Add basefee to eth getUncleByBlockNumberAndIndex"
author: abdelhamidbakhta
date: "2020-10-14"
category: EIPs
tags: [json-rpc, eip-1559]
url: https://ethereum-magicians.org/t/eip-3046-add-basefee-to-eth-getunclebyblocknumberandindex/4830
views: 2260
likes: 0
posts_count: 1
---

# EIP-3046: Add basefee to eth getUncleByBlockNumberAndIndex

https://github.com/ethereum/EIPs/pull/3046

EIP-1559 introduces a base fee per gas in protocol.

This value is maintained under consensus as a new field in the block header structure.

This change should be reflected in RPC methods that return block header information.
