---
source: magicians
topic_id: 21447
title: "EIP-7797: Double speed for hash_tree_root"
author: etan-status
date: "2024-10-23"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7797-double-speed-for-hash-tree-root/21447
views: 99
likes: 4
posts_count: 2
---

# EIP-7797: Double speed for hash_tree_root

Discussion topic for EIP-7797 [EIP-7797: Double speed for hash_tree_root](https://eips.ethereum.org/EIPS/eip-7797)

#### Update Log

- 2024-10-23: initial draft https://github.com/ethereum/EIPs/pull/8995/files

#### External Reviews

None as of 2024-10-23.

#### Outstanding Issues

- 2024-10-23: Security analysis
- 2024-10-23: Determine all locations where historical hashes are needed
- 2024-10-31: Reference test vectors to measure timings across impls

## Replies

**etan-status** (2025-03-31):

EIP-7797 Compress function instead of SHA256 could btw be integrated by re-interpreting the existing SSZ binary tree as a 4-way tree that supplies the current children as elements 0+1 and then supplies second round SHA constant as elements 2+3. That way, historical trees could be transformed without changing the hashes, and newer SSZ types (StableContainer / ProgressiveList) could *actually* be hashed by combining 4 elements at a time instead of 2 elements. Advantage being that no new proof format is required. One could supply the SHA-256 2nd round constant as additional branches as if it was actually part of the tree, then verify using the compress function.

