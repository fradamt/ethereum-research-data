---
source: magicians
topic_id: 4610
title: "EIP-2976: eth/##: Typed Transactions over Gossip"
author: MicahZoltu
date: "2020-09-13"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-2976-eth-typed-transactions-over-gossip/4610
views: 2419
likes: 0
posts_count: 1
---

# EIP-2976: eth/##: Typed Transactions over Gossip

**Simple Summary**

Adds support for transmission of typed transactions over devp2p.

**Abstract**

Typed Transactions can be sent over devp2p as `TransactionType || TransactionPayload`.

The exact contents of the `TransactionPayload` are defined by the `TransactionType` in future EIPs, and clients may start supporting their gossip without incrementing the devp2p version.
