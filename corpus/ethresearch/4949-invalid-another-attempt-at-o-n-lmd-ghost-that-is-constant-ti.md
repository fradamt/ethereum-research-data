---
source: ethresearch
topic_id: 4949
title: "[Invalid] Another attempt at O(n) LMD GHOST that is constant time on the number of blocks since genesis"
author: KentShikama
date: "2019-02-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/invalid-another-attempt-at-o-n-lmd-ghost-that-is-constant-time-on-the-number-of-blocks-since-genesis/4949
views: 1356
likes: 0
posts_count: 1
---

# [Invalid] Another attempt at O(n) LMD GHOST that is constant time on the number of blocks since genesis

Edit: You end up needing to record too much with the updated algorithm.

For background on CBC Casper, see: https://vitalik.ca/general/2018/12/05/cbc_casper.html

Here is an idea for a O(n) time estimator where n is the number of validators that is constant time in the number of blocks since genesis. In short, we are pushing all the information needed to execute the LMD GHOST fork choice rule into each block. In the map of bonded validators, in addition to their stakes, record a list of sequence numbers of all the blocks the validator has proposed in the current chain. Based on your view, do a pairwise comparison across the bonded validator (w/ sequence number of latest) map of the latest messages (blocks). When comparing two maps, compare across each validator and drop the validator with the lower max sequence number (if they are equal, keep both) unless one sequence number list is a subset of the other. The score for each latest message is the sum of the weights of the remaining validators in the map. The estimator should return the latest message (block) with the highest score. Note that this estimator returns the same result as the original LMD GHOST fork choice rule.

Note: A sequence number is basically a per validator block height. Assuming you had a long chain with no orphaned of blocks, the sum of the last sequence number of all the validators would be equal to the height of the the chain.

Note 2: I say pairwise comparison for ease of explanation but this step can be done in one pass (in O(n) time) by continuously recording the maximum sequence number per validator.
