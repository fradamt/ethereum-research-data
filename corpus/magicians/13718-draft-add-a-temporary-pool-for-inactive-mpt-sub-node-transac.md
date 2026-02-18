---
source: magicians
topic_id: 13718
title: "[Draft] Add a temporary pool for inactive MPT sub-node transactions"
author: joohhnnn
date: "2023-04-07"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/draft-add-a-temporary-pool-for-inactive-mpt-sub-node-transactions/13718
views: 307
likes: 0
posts_count: 1
---

# [Draft] Add a temporary pool for inactive MPT sub-node transactions

Summary:

Add a temporary pool for inactive MPT sub-node transactions as a way to indirectly increase TPS and block size.

Motivation:

Most transactions are independent (there are no secondary modifications to the same MPT node in a short period of time), and immediately synchronizing these data to the MPT is wasteful in terms of performance. By adding a separate transaction pool similar to a memory pool, we can temporarily store these transactions (note that the transactions in the separate transaction pool have already been completed, but have not yet been synchronized to the MPT tree). But how can we ensure that these transactions are recognized by the blockchain? We can add a “separate transaction pool Bloom filter” and “hashes of all transactions in the pool (sorted in a certain order)” to the block header. For example, before reading or writing an MPT node, we can check the “separate transaction pool Bloom filter”. If a transaction is not in the pool, we can perform the data read/write directly. If a transaction is in the pool, we can read it from the pool. If it is a write operation, we can add the corresponding operation in the pool to the MPT tree changes.

Unconfirmed ideas:

How many transactions can the “separate transaction pool” hold at maximum? Will this have an impact on performance?

Benefits:

By simply adding a Bloom filter and hashes to the block header, we can greatly increase the number of transactions that can be accommodated and increase TPS.
