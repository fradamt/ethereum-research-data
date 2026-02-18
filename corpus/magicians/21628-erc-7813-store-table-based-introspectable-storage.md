---
source: magicians
topic_id: 21628
title: "ERC-7813: Store, Table-Based Introspectable Storage"
author: alvarius
date: "2024-11-08"
category: ERCs
tags: [erc, storage, indexing]
url: https://ethereum-magicians.org/t/erc-7813-store-table-based-introspectable-storage/21628
views: 160
likes: 4
posts_count: 1
---

# ERC-7813: Store, Table-Based Introspectable Storage

This standard introduces a flexible on-chain storage pattern that organizes data into structured tables with schemas, similar to a traditional database. This approach allows new tables to be added at runtime without impacting existing contracts, thereby simplifying upgrades and extensions. By providing a unified interface for data access, the standard enables any contract or off-chain service to read stored data without the need for custom getter functions. Additionally, by standardizing event emissions for state changes it enables automatic, schema-aware indexing.

PR:

https://github.com/ethereum/ERCs/pull/711
