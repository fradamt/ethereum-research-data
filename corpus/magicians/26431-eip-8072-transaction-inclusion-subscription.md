---
source: magicians
topic_id: 26431
title: "EIP-8072: Transaction Inclusion Subscription"
author: LukaszRozmej
date: "2025-11-05"
category: EIPs > EIPs interfaces
tags: []
url: https://ethereum-magicians.org/t/eip-8072-transaction-inclusion-subscription/26431
views: 32
likes: 0
posts_count: 1
---

# EIP-8072: Transaction Inclusion Subscription

Discussion topic for [EIP-8072](https://github.com/ethereum/EIPs/pull/10666);

Abstract

This EIP extends the existing `eth_subscribe` JSON-RPC method with a new subscription type `transactionInclusion` that enables clients to receive real-time notifications when transactions are included in blocks. This subscription-based approach provides efficient transaction confirmation monitoring without blocking connections, supporting both combined transaction submission and monitoring in a single call, as well as monitoring of already-submitted transactions.
