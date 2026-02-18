---
source: magicians
topic_id: 25796
title: Win-win-win solution for state bloat
author: LeonardDarvin
date: "2025-10-14"
category: EIPs
tags: [storage, refund, storage-cleanup]
url: https://ethereum-magicians.org/t/win-win-win-solution-for-state-bloat/25796
views: 35
likes: 0
posts_count: 1
---

# Win-win-win solution for state bloat

**Why I offer this**: I just wanna earn some money developing contracts which doesn’t hurt the network.

**What’s the win-win-win**

- Miner’s win - less of active state to handle(economy)
- Contract developer’s win - earn extra money writing cleanup logic
- Contract users - better network condition hence faster and cheaper transactions

**Short solution description**: storage cleanup cost should rely on another gas price opposite to the main price. So that the cheaper normal gas the more expensive gas of storage cleanup refund

**Few details**:

- nodes negotiate cleanup gas price ceiling dependently on how state bloat is bad now
- cleanup gas price is getting calculated as ceilingCleanupGasPrice - normalGasPrice
- amount of gas per state deletion should become substantial
- contract developers know what data could be removed securely for contract’s primary function. They run cleanup when network load is the lowest to maximize profit
As a result storage reduces and network load balances

**What could go wrong**

- storage growth could not be the biggest problem of node keepers
- technical complexities of EVM update
