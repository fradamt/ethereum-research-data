---
source: magicians
topic_id: 1780
title: "Request For Comments: Transparent Contract Standard"
author: mudgen
date: "2018-11-02"
category: EIPs
tags: [erc1538]
url: https://ethereum-magicians.org/t/request-for-comments-transparent-contract-standard/1780
views: 505
likes: 0
posts_count: 1
---

# Request For Comments: Transparent Contract Standard

I recently published a new proposed standard that makes upgradeable contracts more flexible, unlimited in size and more transparent.

It is ERC1538: Transparent Contract Standard: https://github.com/ethereum/EIPs/issues/1538

I am looking for feedback.

Here is a list of benefits from the standard:

1. The ability to add, replace or remove any function.
2. Each time a function is added, replaced or removed, it is documented with events.
3. Build trust over time by showing all changes made to a contract.
4. Unlimited contract size.
5. The ability to query information about functions currently supported by the contract.
6. One contract address that provides all needed functionality and never needs to be replaced by another contract address.
