---
source: ethresearch
topic_id: 17450
title: What communication protocols do the eth clients/nodes use for communicating with other eth clients?
author: EggsyOnCode
date: "2023-11-17"
category: Networking
tags: []
url: https://ethresear.ch/t/what-communication-protocols-do-the-eth-clients-nodes-use-for-communicating-with-other-eth-clients/17450
views: 1093
likes: 0
posts_count: 3
---

# What communication protocols do the eth clients/nodes use for communicating with other eth clients?

Like normally we have HTTP or SSH or other networking protocols dictating how machines communicate via the OSI model; in a similar vein i was wondering how do eth nodes communicate with each other and sync the latest EVM state with the local EVM state stored on their SSDs.

Any links to official documentation or other helping material would be appreciated!

## Replies

**thogard785** (2023-11-19):

[github.com](https://github.com/ethereum/devp2p)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/5/e/5e5119e8f3b9f42127c9e31ce384cdef720fe0eb_2_690x344.png)



###



Ethereum peer-to-peer networking specifications










I believe the current protocol is ETH68 but I could be out of date.

---

**mratsim** (2023-11-22):

- Networking layer | ethereum.org
- libp2p & Ethereum (the Merge) | libp2p Blog & News

