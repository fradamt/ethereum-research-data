---
source: magicians
topic_id: 25912
title: "EIP-8057: Block Temporal Locality Gas Discounts"
author: benaadams
date: "2025-10-21"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8057-block-temporal-locality-gas-discounts/25912
views: 55
likes: 0
posts_count: 1
---

# EIP-8057: Block Temporal Locality Gas Discounts

Discussion topic for EIP-8057: Block Temporal Locality Gas Discounts

> This proposal introduces a deterministic, multi-block discount for the first
> access to accounts and storage keys in a transaction. The discount depends on
> the number of blocks since that item was last accessed and decays smoothly to
> zero over a fixed window of recent blocks. Intra-block warming semantics remain
> unchanged (no block-level warming).
>
>
> The mechanism relies on block-level access lists (EIP-7928) committed in headers so that a newly synced node can price the first block it validates without executing historical blocks.
