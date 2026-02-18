---
source: ethresearch
topic_id: 20262
title: DoS on block proposers in PoS and block builders in PBS
author: ivan-homoliak
date: "2024-08-13"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/dos-on-block-proposers-in-pos-and-block-builders-in-pbs/20262
views: 154
likes: 0
posts_count: 1
---

# DoS on block proposers in PoS and block builders in PBS

1. In Ethereum 2.0 PoS, the block proposer of the next block is known a certain time (~12s) before she creates the block. It might create an opportunity for attackers to DoS the next proposer who will therefore not create the new block and lose the reward. This might be systematically repeated again. We know that something similar was of concern for Algorand PoS and its VRF-based leader election that avoided this kind of attack.
2. In PBS, the builder reveals the sealed block bid (commitment), and then later reveals the block contents. If the contents are not revealed, the builder will be penalized. So, the attacker already knowing the network address of victim can DoS her and cause severe penalties for not revealing the block on time. This might be systematically repeated again.

My question or point to discuss is how Ethereum protects against this kind of attack?
