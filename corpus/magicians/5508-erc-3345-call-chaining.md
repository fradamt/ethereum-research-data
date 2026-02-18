---
source: magicians
topic_id: 5508
title: "ERC-3345: Call chaining"
author: albertocuestacanada
date: "2021-03-08"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/erc-3345-call-chaining/5508
views: 583
likes: 0
posts_count: 1
---

# ERC-3345: Call chaining

I’ve drafted a new standard to replace ERC667 and ERC1363, as well as an alternative to ERC777. It goes a bit further even in that it is not limited to token transfers, but can be applied to any smart contract:

https://github.com/ethereum/EIPs/pull/3345

It is inspired on the ENS multicall pattern, but adding a user-provided abi-encoded function call from the smart contract that the user interfaces to, to an user-specified receiver.

There are some safety and implementation challenges to this standard, but I think they can be overcome. I think that the gas savings and UX improvements are worth it.
