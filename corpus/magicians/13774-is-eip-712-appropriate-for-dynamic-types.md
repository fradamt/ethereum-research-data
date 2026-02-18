---
source: magicians
topic_id: 13774
title: Is EIP-712 appropriate for dynamic types?
author: That3Percent
date: "2023-04-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/is-eip-712-appropriate-for-dynamic-types/13774
views: 550
likes: 1
posts_count: 2
---

# Is EIP-712 appropriate for dynamic types?

We are considering using EIP-712 signing for structs which can have implementation-defined additional members (“dynamic types”), or nullable values.

It seems to me that the spec does not account for this as a possibility. For example,

> Note: The typeHash is a constant for a given struct type and does not need to be runtime computed.

But, from my reading of the spec it doesn’t appear that dynamic types would lead to any possibility for collisions or other problems.

Our motivation for adopting EIP-712 would be to get nice tooling “for free”, like displaying friendly structs in Metamask.

Is using EIP-712 in this way problematic or would the possibility of non-const typeHash be ok and a valid interpretation of the spec?

## Replies

**h4l** (2023-04-12):

You can do this. Take a look at the Uniswap Permit2 contracts for an example — they allow additional user (developer)-specified typed data to be included in their own typed data. They refer to the additional data as a witness in their docs & code.

- This page describes the API which allows their base signed data to include additional arbitrary typed data: SignatureTransfer | Uniswap
- This is where the additional data gets handled in their implementation:
permit2/PermitHash.sol at main · Uniswap/permit2 · GitHub

