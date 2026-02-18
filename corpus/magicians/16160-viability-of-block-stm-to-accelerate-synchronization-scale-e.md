---
source: magicians
topic_id: 16160
title: Viability of Block STM to accelerate synchronization & scale Ethereum?
author: u4ea
date: "2023-10-19"
category: Magicians > Primordial Soup
tags: [evm]
url: https://ethereum-magicians.org/t/viability-of-block-stm-to-accelerate-synchronization-scale-ethereum/16160
views: 508
likes: 0
posts_count: 1
---

# Viability of Block STM to accelerate synchronization & scale Ethereum?

Right now I believe all Ethereum clients execute transactions one-by-one (correct me if I’m wrong). The [Block STM](https://arxiv.org/abs/2203.06871) algorithm was invented and used by the Aptos team to execute over [160k](https://medium.com/aptoslabs/block-stm-how-we-execute-over-160k-transactions-per-second-on-the-aptos-blockchain-3b003657e4ba) transactions per second. I’ll explain here how it works briefly.

Transactions are executed all at once, and those with conflicting write/read sets (storage slots write to/read from) are re-run serially according to the order preset by the block. This optimistic algorithm allows for massively parallelized waiting for storage results while the CPU is saturated completely with useful work.

Since most transactions in a blockchain workload don’t conflict with each other, it’s possible to run them in parallel and detect concurrency conflicts instead of avoiding them in advance.

I’m wondering to what extent this has been investigated for Ethereum and if so what were the results? Is this a way to scale Ethereum as an L1?
