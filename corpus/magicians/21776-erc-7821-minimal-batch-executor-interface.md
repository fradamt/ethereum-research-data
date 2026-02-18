---
source: magicians
topic_id: 21776
title: "ERC-7821: Minimal Batch Executor Interface"
author: Vectorized
date: "2024-11-21"
category: ERCs
tags: [erc, wallet]
url: https://ethereum-magicians.org/t/erc-7821-minimal-batch-executor-interface/21776
views: 490
likes: 4
posts_count: 5
---

# ERC-7821: Minimal Batch Executor Interface

## Motivation

With the advent of EIP-7702, it is possible for Externally Owned Account (EOA) to perform atomic batched executions.

We anticipate that there will be multiple EIP-7702 delegation accounts from multiple vendors. To enable frontends to be able to detect and prepare a batched transaction that works across multiple vendors, we will need a standardized interface for batched executions.

In the absence of such a standard, the vendors may choose to create their own proprietary implementations, causing ecosystem fragmentation.

This standard propose a minimal batch execution interface that is easily implementable, extensible, and performant. It also includes a signalling function for tell frontends that the account supports the standard.

## Reference Implementation

A optimized implementation is available in Solady.

The ERC proposal has a more readable implementation.

## Replies

**wjmelements** (2024-11-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vectorized/48/7129_2.png) Vectorized:

> This standard propose a minimal batch execution interface that is easily implementable, extensible, and performant.

Actually, concatenation is the most extensible and performant batch ABI.

---

**ernestognw** (2024-12-29):

Hi [@Vectorized](/u/vectorized),

I like the minimal approach of the ERC, and I believe it can be a default minimal batch execution interface not only for EOAs via ERC-7702 but also for other ERC-4337 accounts.

For example, a simple ERC-4337 account may implement ERC-7821 instead of the `IAccountExecute` interface. I see it was recently changed to allow `msg.sender` to be the entrypoint, which is great.

Some concrete feedback

- ERC-7579 dropped the requirement for ERC-165 so I don’t think ERC-7821 needs to be explicit about it
- The standard is not clear whether replacing address(0) with address(this) is mandatory. I would say it’s a “MAY” but feel free to correct me.

Opening [a PR](https://github.com/ethereum/ERCs/pull/816) with this feedback if you think makes sense

---

**chaitanyapotti** (2025-01-06):

Created a small PR #829 to fix reference implementation

---

**mcoso** (2025-02-03):

added a PR to match the Call struct to the ERC-7579 Execution struct [PR](https://github.com/ethereum/ERCs/pull/883)

