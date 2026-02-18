---
source: magicians
topic_id: 20092
title: "EIP-7713: Box type for EIP-712 messages"
author: frangio
date: "2024-05-23"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7713-box-type-for-eip-712-messages/20092
views: 788
likes: 2
posts_count: 1
---

# EIP-7713: Box type for EIP-712 messages

This EIP defines a new type `box` for use in EIP-712 messages. A `box` value is a value of an arbitrary struct type whose underlying type is encapsulated and hidden from the outer struct but transparent and type-checkable by the wallet, and thus able to be fully inspected by the user prior to signing. A verifying contract can be made agnostic to the underlying type of a `box` value, but this type is not erased and can be verified on-chain if necessary.

[See full text](https://github.com/frangio/EIPs/blob/eip-box-712/EIPS/eip-7713.md)

https://github.com/ethereum/EIPs/pull/8594
