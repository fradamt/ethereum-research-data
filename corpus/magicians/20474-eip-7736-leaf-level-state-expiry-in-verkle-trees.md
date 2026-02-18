---
source: magicians
topic_id: 20474
title: "EIP-7736: Leaf-level state expiry in verkle trees"
author: gballet
date: "2024-07-05"
category: EIPs
tags: [stateless, state-expiry]
url: https://ethereum-magicians.org/t/eip-7736-leaf-level-state-expiry-in-verkle-trees/20474
views: 660
likes: 3
posts_count: 2
---

# EIP-7736: Leaf-level state expiry in verkle trees

This proposal relies on the structure of verkle trees to implement state expiry. A counter is maintained at the extension node level, and only extention-and-suffix nodes (colloquially referred to as “leaves”) are deleted.

Proposal at: [Add EIP: Leaf-level state expiry in verkle trees by gballet · Pull Request #8724 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8724)

## Replies

**norswap** (2024-07-13):

One comment is that it seems very disruptive to expire state that is read often but not written to.

Updating the counter on the first read of each epoch does not seem like an awful thing to do — I suppose it could a DoS vector if someone purposefully tried to read a bunch of value at the start of an epoch given that read is priced too low (2k for a cold read vs 20k for a write).

We could change the price of reads to be 20k for the initial epoch read.

In any case, and not covered here or in a mentionned related EIP, would need a RPC call for archive nodes that gives the list of values that need to be resurrected.

But in theory (to be safe) you would need to call this every time, incurring latency and cost. To avoid this, we would need to modify `eth_sendRawTransaction` to clearly indicate when it fails because of an expired value. Then the frontend could resurrect the previous value (using the archive RPC call).

Since this whole flow would be required anyway, maybe not updating the counter on reads is not such a big problem as I thought though…

