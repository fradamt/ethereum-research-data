---
source: ethresearch
topic_id: 5355
title: Question - alternative accumulators for history
author: liamzebedee
date: "2019-04-23"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/question-alternative-accumulators-for-history/5355
views: 1332
likes: 0
posts_count: 1
---

# Question - alternative accumulators for history

I’m wondering if my line of thinking is correct. Construct an accumulator, which resembles a Merkle tree, but non-leaf nodes are XOR’ed, rather than hashed. Publish the root, and proofs of items are worst-case O(log N) long.

This is not an original idea, it’s been specifically [brought up here](https://github.com/zcash/zcash/issues/2258#issuecomment-342143841) in the zcash repo and also referred to in general about [alternatives to Merkle accumulators](https://github.com/zcash/zcash/issues/2134).
