---
source: magicians
topic_id: 20094
title: "RIP-7712: Multi-dimensional 256-bit nonce for RIP-7560 Account Abstraction transactions"
author: alex-forshtat-tbk
date: "2024-05-23"
category: RIPs
tags: [account-abstraction, rip]
url: https://ethereum-magicians.org/t/rip-7712-multi-dimensional-256-bit-nonce-for-rip-7560-account-abstraction-transactions/20094
views: 526
likes: 1
posts_count: 1
---

# RIP-7712: Multi-dimensional 256-bit nonce for RIP-7560 Account Abstraction transactions

The original RIP-7560 previously required a creation of a `NonceManager` contract and an introduction of a 256-bit wide two-dimensional nonce parameter. This closely reflects the implementation of “nonce” replay protection in ERC-4337.

However, this requirement seemed to complicate an already complex design while not being strictly necessary to achieve most of the goals set forward by RIP-7560, so this feature has been extracted into a separate document here:

https://github.com/ethereum/RIPs/pull/23
