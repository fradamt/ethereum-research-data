---
source: magicians
topic_id: 16520
title: Are block.timestamp and block.number still problematic under Proof of Stake?
author: Yleisnero1
date: "2023-11-08"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/are-block-timestamp-and-block-number-still-problematic-under-proof-of-stake/16520
views: 690
likes: 0
posts_count: 2
---

# Are block.timestamp and block.number still problematic under Proof of Stake?

As stated in the SWC116 ([SWC-116 - Smart Contract Weakness Classification (SWC)](https://swcregistry.io/docs/SWC-116/)) using `block.timestamp` and `block.number` in Smart Contracts under Proof of Work was problematic.

1. Block.timestamp could be influenced by the miners up to 15s
2. Using block.number as proxy for time is inaccurate since the time between block depended on the difficulty i.e. was not fixed.

Do those two issues still exists under Proof of Stake? If not, are there any other/new concerns about using block values as a proxy for time?

## Replies

**sullof** (2023-11-10):

The issue is still there, and as long as Miner Extractable Value (MEV) attacks are possible, will continue to be an issue. Just don’t use block.timestamp for anything critical.

