---
source: ethresearch
topic_id: 4636
title: Chunked Plasma Exit Games with Expensive Griefing
author: fahree
date: "2018-12-19"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/chunked-plasma-exit-games-with-expensive-griefing/4636
views: 1133
likes: 1
posts_count: 1
---

# Chunked Plasma Exit Games with Expensive Griefing

Individual exit games on Plasma don’t scale: you need at least two transactions per exiter. If there’s the child chain was higher-capacity than its parent chain (which is a large part of the point) then you just can’t do it within bounded time. And the bad guys can indefinitely hold everyone else’s exit hostage indefinitely and ransom them by having lots of tiny yet higher-priority claims.

The hope is for collective exit, where large chunks of the child chain could exit to a new side-chain in a couple of transactions. Problem: the bad guy could prevent the exit by peppering the child chain with tiny accounts or UTXOs everywhere in the chain, that he spends in the withheld block, so that any non-trivial chunk can be proven invalid, thus preventing any non-trivial collective exit, at which point we’re back in the previous case, that doesn’t scale.

Mitigation: keep the child chain sorted by total balance (whether accounts or UTXOs, with tie breaks by age). Now, to grieve the exit of a chunk of the chain of size N and total balance B requires the bad guy to have sunk in the side-chain a total amount ~B/N, making it an expensive proposition.

Remaining problem: life still sucks if you have a small account, or if you had a large account but made a transaction since. I have ideas in the latter case, but they are for another topic.
