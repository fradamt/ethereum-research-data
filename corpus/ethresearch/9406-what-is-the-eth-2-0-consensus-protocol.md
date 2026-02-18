---
source: ethresearch
topic_id: 9406
title: What is the eth 2.0 consensus protocol?
author: NateMarrocco1
date: "2021-05-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/what-is-the-eth-2-0-consensus-protocol/9406
views: 1768
likes: 2
posts_count: 2
---

# What is the eth 2.0 consensus protocol?

Can someone explain the intuition behind it? Does it use random sampling of validators or does it poll every validator?

## Replies

**kladkogex** (2021-05-07):

Well, if you want a rough explanation:

1. Proposers are randomly selected and assigned time slots.
2. Normally each proposer proposes and the chain is linear, but sometimes there are forks due to, say, network propagation times (Alice does not get a block from Bob before it proposes)
3. To resolve forks there is a fork selection algorithm, which selects the chain with the most attestations (random committee of validators can send attestations for the chain they like)
4. There is a separate finalization mechanism, that requires 2/3 of votes to finalize.  If a particular vote is deadlocked, a new one can start by choosing an older start point. This guarantees liveliness.

