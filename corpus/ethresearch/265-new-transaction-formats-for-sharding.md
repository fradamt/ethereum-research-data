---
source: ethresearch
topic_id: 265
title: New transaction formats for sharding
author: vbuterin
date: "2017-11-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/new-transaction-formats-for-sharding/265
views: 2962
likes: 1
posts_count: 1
---

# New transaction formats for sharding

Here is a proposed new transaction format.

```
[
    version_num,  # Transaction format version, 0 for now
    chain_id,     # 1 for ETH, 3 for ropsten...
    shard_id,     # The ID of the shard the tx goes on
    acct,         # The account the tx enters through
    gas,          # Total gas supply
    data          # Tx data
]
```

Depending on what is done in [Tradeoffs in Account Abstraction Proposals](https://ethresear.ch/t/tradeoffs-in-account-abstraction-proposals/263), fields can simply be added on to the end of this as needed.
