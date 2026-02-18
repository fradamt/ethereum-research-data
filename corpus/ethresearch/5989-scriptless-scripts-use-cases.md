---
source: ethresearch
topic_id: 5989
title: Scriptless Scripts Use Cases
author: guyz
date: "2019-08-17"
category: Applications
tags: []
url: https://ethresear.ch/t/scriptless-scripts-use-cases/5989
views: 1296
likes: 1
posts_count: 3
---

# Scriptless Scripts Use Cases

Has anyone put thought into the use cases of scriptless scripts in Ethereum? I can understand the excitement around them in Bitcoin/MW, but wondering if anyone has given any thought to the topic on Ethereum. I only found this - [Scriptless Scripts with BLS signatures in ETH2.0?](https://ethresear.ch/t/scriptless-scripts-with-bls-signatures-in-eth2-0/5446), but I’m more interested in use-cases rather than the implementation details.

## Replies

**Mikerah** (2019-08-17):

A potential use case for scriptless scripts in Ethereum would be atomic swaps between BTC and ETH. Although the expressivity of Ethereum makes this redundant, you can use the 2-party ECDSA protocol as described by Lindell and the ECDSA scriptless script protocol by Moreno-Sanchez and Kate. The main advantage of doing an atomic swap this way instead of the usual way would be privacy and efficiency. If you did it the usual way, everything is easily seen on chain whereas if you used scriptless scripts, everything looks like a digital signture and no one would no that an atomic swap took place. Also, dealing with signatures directly is cheaper than having to store the information needed in an atomic swap on-chain.

---

**guyz** (2019-08-20):

Thanks [@Mikerah](/u/mikerah)! I agree more efficient Atomic Swaps is an interesting proposition, and it seems to be the main motivation for thinking about these in Bitcoin, but I was hoping there are more creative ideas for Ethereum that would justify it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14).

