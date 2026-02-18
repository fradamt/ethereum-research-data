---
source: magicians
topic_id: 19921
title: Block.header elements should be well known and easy to access
author: alexbabits
date: "2024-05-07"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/block-header-elements-should-be-well-known-and-easy-to-access/19921
views: 526
likes: 1
posts_count: 4
---

# Block.header elements should be well known and easy to access

Every major update that effects the block headers should broadcast more clearly the exact current elements of the block header, so block hash verification is always straightforward.

What are the current block header elements post merge and today in 2024? I’ve searched a lot and tried a lot of things but have come up short, also see this post below:



      [ethereum.stackexchange.com](https://ethereum.stackexchange.com/questions/163229/how-to-verify-block-hash-post-merge-block-15-5m)



      [![Babs](https://ethereum-magicians.org/uploads/default/original/2X/e/e230e878deb1cd3dfe06a42c2f67add3a153c465.png)](https://ethereum.stackexchange.com/users/133839/babs)

####

  **rlp, blockhash**

  asked by

  [Babs](https://ethereum.stackexchange.com/users/133839/babs)
  on [04:29AM - 07 May 24 UTC](https://ethereum.stackexchange.com/questions/163229/how-to-verify-block-hash-post-merge-block-15-5m)

## Replies

**alexbabits** (2024-05-07):

This post shows how to recreate the block hash for all 5 “eras” of different block headers: [rlp - How to verify block.hash post-merge (block > 15.5M)? - Ethereum Stack Exchange](https://ethereum.stackexchange.com/questions/163229/how-to-verify-block-hash-post-merge-block-15-5m)

This should be easily accessible public knowledge, not esoteric and difficult to find.

---

**xrchz** (2025-05-06):

I agree - is there still not some canonical place to find the specification for RLP encoding of blocks as used in the current fork?

---

**bbjubjub** (2025-05-06):

There are the [execution layer specs](https://github.com/ethereum/execution-specs) which have a Block dataclass for each fork.

