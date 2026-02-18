---
source: magicians
topic_id: 23183
title: EIP-7910 - Eth_config JSON-RPC Method
author: shemnon
date: "2025-03-18"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7910-eth-config-json-rpc-method/23183
views: 122
likes: 1
posts_count: 3
---

# EIP-7910 - Eth_config JSON-RPC Method

Discussion topic for [EIP-7910](http://eips.ethereum.org/EIPS/eip-7910)

#### Update Log

- 2025-03-18: initial draft PR#9493

#### External Reviews

- twitter post Besu intends to adopt.

#### Outstanding Issues

None as of 2025-03-18

## Replies

**lu-pinto** (2025-03-27):

This could be useful for checking configs at runtime in clients remotely. Can optional fields be included or is it strict to the fields stated in the EIP?

---

**shemnon** (2025-03-27):

I could see user provided extensions by adding flags to the rpc call, but there needs to be an EIP and only EIP fields response to the no-args call.

