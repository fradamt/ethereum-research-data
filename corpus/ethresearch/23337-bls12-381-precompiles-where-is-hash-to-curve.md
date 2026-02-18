---
source: ethresearch
topic_id: 23337
title: Bls12-381 precompiles, where is hash_to_curve
author: vans163
date: "2025-10-23"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/bls12-381-precompiles-where-is-hash-to-curve/23337
views: 132
likes: 1
posts_count: 2
---

# Bls12-381 precompiles, where is hash_to_curve

Using the new precompiles for bls12-381 one thing missing is when a DST is used following the eth2 specced hash_to_curve function.  Is anyone aware of a solidity implementation of this or how to go about verifying a signature produced?

## Replies

**0xSooki** (2025-10-30):

You can use the [solady](https://github.com/Vectorized/solady/blob/73f13dd1483707ef6b4d16cb0543570b7e1715a8/src/utils/ext/ithaca/BLS.sol) library’s BLS module. For a working example, you can check out this [repo](https://github.com/0xSooki/bribery-zoo), especially the tests. The convert.py file can be used to convert a signature into its upper and lower limbs that can be used directly in Solidity.

