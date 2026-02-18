---
source: magicians
topic_id: 19537
title: "EIP-7676: EOF - Prepare for Address Space Extension"
author: shemnon
date: "2024-04-04"
category: EIPs
tags: [eof]
url: https://ethereum-magicians.org/t/eip-7676-eof-prepare-for-address-space-extension/19537
views: 938
likes: 0
posts_count: 1
---

# EIP-7676: EOF - Prepare for Address Space Extension

A very small change to EOF to allow future extension of the address space.

https://github.com/ethereum/EIPs/pull/8385

TL;DR all operations that use an address will not trim the high 12 bytes / 96 bits, and (for now) exceptionally halt if they are not zero.  Only `BALANCE` is not otherwise spoken for within EOF. Future uses of these high bits would necessarily change this behavior. but they are not defined in this EIP.
