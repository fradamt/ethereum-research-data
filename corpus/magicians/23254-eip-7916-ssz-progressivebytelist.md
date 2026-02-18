---
source: magicians
topic_id: 23254
title: "EIP-7916: SSZ ProgressiveByteList"
author: zsfelfoldi
date: "2025-03-25"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7916-ssz-progressivebytelist/23254
views: 92
likes: 1
posts_count: 5
---

# EIP-7916: SSZ ProgressiveByteList

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9523)














####


      `ethereum:master` ← `etan-status:sz-progressivebytelist`




          opened 03:47PM - 24 Mar 25 UTC



          [![etan-status](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+72
            -32](https://github.com/ethereum/EIPs/pull/9523/files)







Move SSZ ProgressiveByteList to its own EIP so that it can be worked on independ[…](https://github.com/ethereum/EIPs/pull/9523)ently of the eth_getLogs filter usage.

Plans are to work with @wemeetagain to generalize it beyond byte lists, and to simplify the parameters with `CAPACITY = unbounded` as well as `COMMON_RATIO = 4`. That way, in EIPs such as EIP-6404 and EIP-6466 it is no longer necessary to define arbitrary bounds to byte lists, and in consensus we can use such an `UnboundedList[T]` construct to replace proposer / attester slashing lists (with a shared maximum allowed len), and could use it for attestations list that keeps changing across forks.

First step is to move this out to its own EIP with Zsolt as author, then do the followup work with me and @wemeetagain in separate PRs.












This EIP introduces a new [Simple Serialize (SSZ) type](https://github.com/ethereum/consensus-specs/blob/b3e83f6691c61e5b35136000146015653b22ed38/ssz/simple-serialize.md) to make `List[T, N]` with large capacities `N` more efficient in cases where the list is much shorter than the capacity.

## Replies

**etan-status** (2025-06-24):

[github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/pull/9931/files)














####


      `master` ← `etan-status:7916-treeleft`




          opened 12:26PM - 24 Jun 25 UTC



          [![](https://avatars.githubusercontent.com/u/89844309?v=4)
            etan-status](https://github.com/etan-status)



          [+94
            -108](https://github.com/ethereum/EIPs/pull/9931/files)







- Added `ProgressiveBitlist`
- Tree now grows to left instead of right
- Fixed[…](https://github.com/ethereum/EIPs/pull/9931) incorrect `Bitvector` notion in graphic: Unused chunks are padded with 0 chunks instead of default(T) chunks.
- Simplified Merkleization code












- Added ProgressiveBitlist
- Tree now grows to left instead of right
- Fixed incorrect Bitvector notion in graphic: Unused chunks are padded with 0 chunks instead of default(T) chunks.
- Simplified Merkleization code

---

**etan-status** (2025-07-31):

Started an implementation tracker: https://pureth.guide/implementations-ssz/

---

**etan-status** (2026-01-06):

[![image](https://ethereum-magicians.org/uploads/default/optimized/3X/a/4/a41f4d5bb0f67344ec8d78117e047f7122bc0360_2_690x327.jpeg)image1280×607 108 KB](https://ethereum-magicians.org/uploads/default/a41f4d5bb0f67344ec8d78117e047f7122bc0360)

Received EIP-7916 feedback where some people slightly prefer changing to the Merkle tree layout in the right picture (while others slightly prefer staying on the left).

Arguments for left:

- Easier implementation, as standard left-to-right DFS iteration visits deeper branches first. O(1) memory instead of O(log(N)), or simpler algo. Also easier formulas for handling gindices.

Arguments for right:

- Later list indices are assigned a gindex further right in the tree than earlier list indices. Maybe makes incremental building (e.g., deposit contract snapshot style) a bit easier.

Same for both:

- Hash count is the same. Proof size is the same.

Personally fine with either, but will lock it down by end of week so that implementation effort doesn’t get derailed.

---

**etan-status** (2026-01-06):

Draft for Merkleizing to right:

- Update EIP-7916: Merkleize to right by etan-status · Pull Request #11032 · ethereum/EIPs · GitHub
- Merkleize progressive shape to right by etan-status · Pull Request #16 · ethereum/remerkleable · GitHub
- Merkleize progressive SSZ shape to right by etan-status · Pull Request #4813 · ethereum/consensus-specs · GitHub

