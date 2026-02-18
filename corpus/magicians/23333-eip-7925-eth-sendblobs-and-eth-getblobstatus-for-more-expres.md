---
source: magicians
topic_id: 23333
title: EIP-7925 eth_sendBlobs and eth_getBlobStatus for more expressive blob submission strats
author: sbacha
date: "2025-04-01"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7925-eth-sendblobs-and-eth-getblobstatus-for-more-expressive-blob-submission-strats/23333
views: 68
likes: 0
posts_count: 1
---

# EIP-7925 eth_sendBlobs and eth_getBlobStatus for more expressive blob submission strats

# EIP-7925: Optional RPC Methods eth_sendBlobs and eth_getBlobsStatus

- EIP-7925: Optional RPC Methods eth_sendBlobs and eth_getBlobsStatus
+ Purpose
+ Blobenheimer
+ Specification
- 1. eth_sendBlobs Method
- 2. eth_getBlobsStatus Method
+ TLDR:

> https://github.com/ethereum/EIPs/pull/9562

### Purpose

This Ethereum Improvement Proposal (EIP) introduces two new JSON-RPC methods:

1. eth_sendBlobs – Allows users to submit multiple EIP-4844 Type 3 transactions for the same sender and nonce, letting block-building infrastructure choose the most optimal one.
2. eth_getBlobsStatus – Enables querying the status of a previously submitted bundle of transactions.

It also introduces a partioned mempool called a sublet, a non-gopssiping pending pool for enabling users of the RPC method to submit multiple transactions of the same nonce. Each sublet represents its own building policy, in an effort to optimize blob inclusion. I am working on refining this part conceputally outside of this EIP, you can

> Read more here regarding ‘sublists’

### Blobenheimer

Blob transaction originators currently are limited in their ability to submit multiple transactions for varying blob transaction composition.

- Fixed Submission: Existing eth_sendRawTransaction forces a sender to commit to one transaction per nonce.
- Inefficiency: Transactions with more blobs may get excluded, even if a smaller variant could have been included.

`eth_sendBlobs` method enables senders to submit **multiple versions** of the same transaction (differing in blob count), and the most suitable one is selected based on network conditions. This prevents the sender from **guessing** the optimal number of blobs.  Each *subk

- The method returns a unique bundleId that represents the submitted transaction set.
- The eth_getBlobsStatus method provides visibility into whether the bundle was included in a block, is still pending, or expired.

> Question: Can a data structure be leveraged to communicate more information besides simply an opaque UUID?

### Specification

#### 1. eth_sendBlobs Method

- Input:

txs: Array of hex-encoded signed transactions, all from the same sender and nonce.
- maxBlockNumber: (Optional) Expiry block for the bundle.

**Output:**

- bundleId: Unique identifier for the submitted transaction set.
- error: If submission fails, an error code is returned.

#### 2. eth_getBlobsStatus Method

- Input:

bundleId: Identifier of the submitted bundle.

**Output:**

- Status of the bundle (pending, included, expired, etc.).

### TLDR:

- Optimized Inclusion: Avoids wasteful exclusions due to blob slot constraints.
- Improved Tracking: Provides a standard way to track blob transactions.
- Reduces Sender Complexity: No need to manually optimize transaction submissions.

> This method is based off of Titan Builders eth_sendBlobs method.
