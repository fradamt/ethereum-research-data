---
source: ethresearch
topic_id: 8023
title: General purpose Oracle smart contract
author: Econymous
date: "2020-09-25"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/general-purpose-oracle-smart-contract/8023
views: 1077
likes: 0
posts_count: 1
---

# General purpose Oracle smart contract

I’ve tested and modified the code since I’ve done this video, but the idea is still the same.

Tokens are deposited into the contract, used to vote on oracle configurations (Fees, punishments and such) and also used to back different watchers (oracle verifiers)

1. A request ticket is filed (query string, data type,  “is it subjective?” boolean)
2. Watchers commit a secret vote
3. Watchers reveal their vote
4. If the request ticket is subjective, watchers go through a “attacking phase” for outliers
5. In finalize request ticket votes are counted up and rewards distributed.



      [pastebin.com](https://pastebin.com/UVwrJ6r6)





####

```auto

```
