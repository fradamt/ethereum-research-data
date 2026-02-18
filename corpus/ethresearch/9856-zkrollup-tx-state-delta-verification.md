---
source: ethresearch
topic_id: 9856
title: Zkrollup tx state delta verification
author: ethgcm
date: "2021-06-16"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/zkrollup-tx-state-delta-verification/9856
views: 1075
likes: 0
posts_count: 1
---

# Zkrollup tx state delta verification

In ZKRollup operation; when tx state delta is published as part of the proof on chain, I havent found any information that indicates this tx data is validated.

Is it assumed that the zksnark circuit includes a hash(txs) as part of the constraints and later the on chain verifier will hash the transactions and include them as public inputs?
