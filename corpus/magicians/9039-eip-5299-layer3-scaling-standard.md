---
source: magicians
topic_id: 9039
title: EIP 5299 - Layer3 scaling standard
author: v9hstk
date: "2022-04-25"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-5299-layer3-scaling-standard/9039
views: 1829
likes: 3
posts_count: 2
---

# EIP 5299 - Layer3 scaling standard

Ethereum Improvement Proposals

**EIP 5299 - Layer3 scaling standard**

https://github.com/ethereum/EIPs/pull/5299

A primitive standard facilitating eternal upgradeability of smart contracts, by making storage slots dynamic; mitigating the need for redeployment of the proxy in case the storage structure changes.

## Replies

**mudgen** (2022-05-19):

From what I see here, it seems to me that this standard or pattern is the idea to combine the old Eternal Storage pattern with EIP-2535 Diamonds.

While the Eternal Storage pattern only works with Solidity data types,  diamond storage works with structs.  So instead of only dealing with `setInt`, `setString`,  `getInt`, `getString` type functions EIP9000 can deal in custom structs,  so `setSomeDataInStructA`, `setSomeDataInStructB`,  `getSomeDataFromStructA`,  `getSomeDataFromStructB` etc.   Dealing with structs can add a layer of data organization.   Also,  new functions and state variables and structs can be added to an EIP9000 diamond.

It would be great to see a useful application of this standard.

