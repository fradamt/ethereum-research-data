---
source: magicians
topic_id: 18991
title: "EIP-7639: Cease serving history before PoS"
author: matt
date: "2024-02-28"
category: EIPs > EIPs networking
tags: []
url: https://ethereum-magicians.org/t/eip-7639-cease-serving-history-before-pos/18991
views: 1190
likes: 2
posts_count: 1
---

# EIP-7639: Cease serving history before PoS

This EIP proposes that execution layer clients stop server historical data from before the merge over p2p.

It also officially commits to Ethereum chain before the merge via the root of the header accumulator: `0xe6ebe562c89bc8ecb94dc9b2889a27a816ec05d3d6bd1625acad72227071e721`

https://github.com/ethereum/EIPs/pull/8266
