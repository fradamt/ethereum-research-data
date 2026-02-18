---
source: magicians
topic_id: 2924
title: "EIP-1844: ENS Interface Discovery"
author: Arachnid
date: "2019-03-15"
category: EIPs
tags: [ens]
url: https://ethereum-magicians.org/t/eip-1844-ens-interface-discovery/2924
views: 3171
likes: 0
posts_count: 2
---

# EIP-1844: ENS Interface Discovery

This thread is for discussion of [EIP 1844, ENS Interface Discovery](https://eips.ethereum.org/EIPS/eip-1844).

## Replies

**fulldecent** (2019-08-05):

This is a very useful standard. It could replace 165. Please add a note that a contract could designate itself as the implementer by returning its own address.

Backwards compatibility section could please be updated to add notes about 1820, specifically the cache. And about how this can replace 165.

Use case could be much more general if interface was changed from (bytes32 node, bytes4 interfaceID) into just a single bytes32 interfaceID. hash(bytes32 || bytes4) == bytes32. Now this is useful for much more than just ENS. A brief prescription could be given for how to convert ERC-165 style interfaces into the new 32byte interfaces (related to ERC-820).

Personally, I think this is immediately more useful than ERC-165 and solves most use cases of ERC-820 and ERC-1820.

