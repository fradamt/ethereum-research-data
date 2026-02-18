---
source: ethresearch
topic_id: 2886
title: Parallel chain evolution
author: DB
date: "2018-08-11"
category: Sharding
tags: []
url: https://ethresear.ch/t/parallel-chain-evolution/2886
views: 1065
likes: 0
posts_count: 1
---

# Parallel chain evolution

tl;dr: new network configurations can arise as independent networks with a bridge, allowing users to migrate at their own time.

The Ethereum protocol development so far has been research<->development<->test-net->main-net HF (sometimes assisted by a difficulty time-bomb). This worked well so far, but maybe is not the optimal way forward. Now that the main-net is stable and useful for some applications, there is less justification to force the switch to something more advanced, but also inherently more risky. On the other hand, some applications will benefit from quicker access to advance features (like lower cost and more TPS) even at the risk of using a beta product.

One solution to this (and forgive me if this was discussed and I missed it) is to release the new network in parallel to the existing Ethereum. This will also enable developers to fork faster and keep a temporary “back door” to revert any changes from bugs/theft. Moving ETH/tokens (bidirectionally) between the networks can be done by a smart contract on both sides. Users can move at their own rate, after seeing to their personal satisfaction the new network is safe.

With time, the old network may become compromised. Before this happens, a date can be set, when the old state/balance is mirrored in the new network and the bridge is burned.
