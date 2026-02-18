---
source: ethresearch
topic_id: 5019
title: Evictable Account Nonce
author: Zergity
date: "2019-02-19"
category: Meta-innovation
tags: [stateless, cross-shard, storage-fee-rent]
url: https://ethresear.ch/t/evictable-account-nonce/5019
views: 1506
likes: 3
posts_count: 1
---

# Evictable Account Nonce

My proposal for Evictable Account Nonce is up for discussion. Please share your thoughts.

Current properties of Nonce to preserve

- Replay attack proof (a.k.a. can be used only once)
- Chainable transactions (a.k.a. send many transactions without waiting for the previous ones to be confirmed)

New properties can be achieved

- Re-creation of evicted accounts.
- Cross-chain and cross-shard replay attack proof without additional ChainID or ShardID fields.

Apply to

- Both contract and non-contract accounts.
- New chain, hard-forkable and soft-forkable.
- Any state machine blockchain.

[github.com/Zergity/research/wiki/Stateless-Account-Nonce](https://github.com/Zergity/research/wiki/Stateless-Account-Nonce)
