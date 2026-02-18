---
source: ethresearch
topic_id: 8300
title: First block proposer slashing on ETH2
author: kladkogex
date: "2020-12-02"
category: Proof-of-Stake > Block proposer
tags: []
url: https://ethresear.ch/t/first-block-proposer-slashing-on-eth2/8300
views: 1317
likes: 0
posts_count: 1
---

# First block proposer slashing on ETH2

Looks like the first block proposer has been slashed on ETH2 for double-proposing.

**https://beaconscan.com/slots-slashed**

Theoretically, there could be several reasons:

- a client crashed and lost state, then proposed the same block
- two copies of the same client have been executed (buggy devops script?)
- client software bug
- a malicious client

Opinions ?)
