---
source: magicians
topic_id: 21580
title: "EIP-7807: SSZ execution blocks"
author: etan-status
date: "2024-11-04"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7807-ssz-execution-blocks/21580
views: 92
likes: 0
posts_count: 2
---

# EIP-7807: SSZ execution blocks

Discussion topic for EIP-7807 [EIP-7807: SSZ execution blocks](https://eips.ethereum.org/EIPS/eip-7807)

#### Update Log

*2024-11-04: initial draft https://github.com/ethereum/EIPs/pull/9017

#### External Reviews

None as of 2024-11-04.

#### Outstanding Issues

- 2024-11-04: Deposits / Withdrawals refactoring, https://github.com/ethereum/EIPs/pull/9017/files
- 2024-11-04: Engine API proposal, https://github.com/ethereum/EIPs/pull/9017/files
- 2024-11-04: Networking proposal, https://github.com/ethereum/EIPs/pull/9017/files

#### Update Log

- 2025-07-03: Adopt ProgressiveContainer

## Replies

**etan-status** (2025-07-03):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9976)














####


      `master` ← `etan-status:7807-progressive`




          opened 10:19AM - 03 Jul 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+57
            -44](https://github.com/ethereum/EIPs/pull/9976/files)







- Use EIP-7495 ProgressiveContainer for latest forward compatibility changes
- […](https://github.com/ethereum/EIPs/pull/9976)Replicate changes to ExecutionPayload / Header to avoid separate `block_hash` field / use hash_tree_root everywhere












- Use EIP-7495 ProgressiveContainer for latest forward compatibility changes
- Replicate changes to ExecutionPayload / Header to avoid separate block_hash field / use hash_tree_root everywhere

