---
source: magicians
topic_id: 4829
title: "EIP-3045: Add basefee to eth getUncleByBlockHashAndIndex"
author: abdelhamidbakhta
date: "2020-10-14"
category: EIPs
tags: [json-rpc, eip-1559]
url: https://ethereum-magicians.org/t/eip-3045-add-basefee-to-eth-getunclebyblockhashandindex/4829
views: 2278
likes: 0
posts_count: 1
---

# EIP-3045: Add basefee to eth getUncleByBlockHashAndIndex

https://github.com/ethereum/EIPs/pull/3045

EIP-1559 introduces a base fee per gas in protocol.

This value is maintained under consensus as a new field in the block header structure.

This change should be reflected in RPC methods that return block header information.
