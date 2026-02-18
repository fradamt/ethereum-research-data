---
source: magicians
topic_id: 7916
title: "Idea : Adding block in two way order of genesis block"
author: saurabhburade
date: "2022-01-06"
category: EIPs
tags: [evm, gas, core-eips, ethereum-roadmap, feedback-wanted]
url: https://ethereum-magicians.org/t/idea-adding-block-in-two-way-order-of-genesis-block/7916
views: 806
likes: 3
posts_count: 1
---

# Idea : Adding block in two way order of genesis block

### Focused Problem

- The current implementation for ANY sort of blockchain is considered to add blocks afterward of the genesis block.

### Solution Proposed [In Idea State]

- Allow the blockchain to add blocks on both sides of the blockchain (Left & Right) genesis block.
- Every block to contains the flag to represent the side on which it will get added.
- One of the calculation mechanisms will calculate the time to add block and transfer it to the most preferable side.

### Concept [In Idea State]

#### Basic overview

[![alt text](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9b7b76d4344c1e89f7a87b26888b92b401d09d2a_2_690x106.png)alt text1230×190 8.97 KB](https://ethereum-magicians.org/uploads/default/9b7b76d4344c1e89f7a87b26888b92b401d09d2a)

#### Mechanism

[![alt text](https://ethereum-magicians.org/uploads/default/optimized/2X/c/c4d2e1d2ab73d9e63d765a4ac9029cb6e469b7ff_2_690x256.png)alt text1159×431 26.3 KB](https://ethereum-magicians.org/uploads/default/c4d2e1d2ab73d9e63d765a4ac9029cb6e469b7ff)
