---
source: magicians
topic_id: 21507
title: "EIP 7801: eth/70 - Sharded Blocks Protocol"
author: Giulio2002
date: "2024-10-30"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7801-eth-70-sharded-blocks-protocol/21507
views: 217
likes: 0
posts_count: 1
---

# EIP 7801: eth/70 - Sharded Blocks Protocol

This EIP introduces a method enabling an Ethereum node to communicate its available block spans via a bitlist, where each bit represents a 1-million-block span. Nodes use this bitlist to signal which spans of historical data they store, enabling peers to make informed decisions about data availability when requesting blocks. This aims to improve network efficiency by providing a probabilistic snapshot of data locality across nodes.

The proposal extends the Ethereum wire protocol (`eth`) with version `eth/70`, introducing a `blockBitlist` field in the handshake. Nodes probabilistically retain certain block spans to support data locality across the network.
