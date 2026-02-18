---
source: magicians
topic_id: 3605
title: Asking feedback - EIP 1973 - Scalable Rewards
author: lerajk
date: "2019-08-29"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/asking-feedback-eip-1973-scalable-rewards/3605
views: 613
likes: 0
posts_count: 1
---

# Asking feedback - EIP 1973 - Scalable Rewards

This is a layer-2 scalability solution to distribute token rewards to ten of thousands of participants in a completely decentralized manner without hitting the block gas limit.

However, I think this EIP can be made more general in order to facilitate adoption for DApps. Wanted to get feedback from the community on how to make it more general and what use cases could be interesting.


      [github.com](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1973.md)




####

```md
---
eip: 1973
title: Scalable Rewards
author: Lee Raj (@lerajk), Qin Jian (@qinjian)
type: Standards Track
category: ERC
status: Draft
created: 2019-04-01
---

## Simple Summary

 A mintable token rewards interface that mints 'n' tokens per block which are distributed equally among the 'm' participants in the DAPP's ecosystem.

## Abstract

 The mintable token rewards interface allows DApps to build a token economy where token rewards are distributed equally among the active participants. The tokens are minted based on per block basis that are configurable (E.g. 10.2356 tokens per block, 0.1 token per block, 1350 tokens per block) and the mint function can be initiated by any active participant. The token rewards distributed to each participant is dependent on the number of participants in the network. At the beginning, when the network has low volume, the tokens rewards per participant is high but as the network scales the token rewards decreases dynamically.


 ## Motivation
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1973.md)
