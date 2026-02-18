---
source: magicians
topic_id: 15818
title: EIP-7519 - Atomic Storage Operations - SCREDIT and SDEBIT
author: shemnon
date: "2023-09-18"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7519-atomic-storage-operations-scredit-and-sdebit/15818
views: 1425
likes: 1
posts_count: 1
---

# EIP-7519 - Atomic Storage Operations - SCREDIT and SDEBIT

Discussion of SCREDIT and SDEBIT operations.  And possibly concurrent friendly operations in general.

> EIP-7519 Abstract
>
>
> Two new opcodes that atomically mutate smart contract storage are proposed:
> SCREDIT, which increments a storage slot by a specified value, and SDEBIT, which
> decrements a storage slot by a specified value. Overflow and underflow errors
> are enforced, reverting when an unsigned 256-bit integer would overflow or
> underflow.
