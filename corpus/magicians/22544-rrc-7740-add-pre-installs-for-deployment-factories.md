---
source: magicians
topic_id: 22544
title: "RRC-7740: Add pre-installs for deployment factories"
author: rmeissner
date: "2025-01-15"
category: RIPs
tags: [rrc]
url: https://ethereum-magicians.org/t/rrc-7740-add-pre-installs-for-deployment-factories/22544
views: 132
likes: 7
posts_count: 4
---

# RRC-7740: Add pre-installs for deployment factories

Discussion thread for [RRC-7740](https://github.com/ethereum/RIPs/pull/30/files)

Open questions:

- Should other non-factory contracts be added too (i.e. multicall3, ERC-1820 registry)?
- What other factories should be added (i.e. ERC-2740)

## Replies

**rmeissner** (2025-01-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/rmeissner/48/643_2.png) rmeissner:

> Should other non-factory contracts be added too

I would only support this for existing contracts that are well established (as the ones referenced). As new contract should utilize one of the singleton factories to deploy instances that are consistent across networks.

---

**wminshew** (2025-01-15):

`multicall3` would be a great addition imo

---

**Arvolear** (2025-01-22):

Can we think of some deterministic singleton WETH contract that may be preinstalled as well?

