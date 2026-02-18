---
source: ethresearch
topic_id: 1188
title: Nested plasma chains (inception)
author: tim
date: "2018-02-21"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/nested-plasma-chains-inception/1188
views: 1432
likes: 2
posts_count: 3
---

# Nested plasma chains (inception)

[![image](https://ethresear.ch/uploads/default/optimized/1X/7f5bdd27a7d786c7ea8c36c618b81350d9c74d9f_2_281x499.png)image750×1334 92.3 KB](https://ethresear.ch/uploads/default/7f5bdd27a7d786c7ea8c36c618b81350d9c74d9f)

Is it possible to have nested plasma chains and what are the tradeoffs and factors to consider as you get deeper nesting?

i.e. main chain

|–> p1 → p2 → p3

Could you have diagonally nested chains like the following:

main chain

|–> p1 → p2 → p3

|                  |

|

|———-—>  \ —> p4

(Note to use my laptop going forward)

## Replies

**veqtor** (2018-02-21):

I think the point of plasma is that it is nested, so:

mainnet -> root-contract -> child 1-> children 1.1 & 1.2 - > children 1.1.1, 1.1.2 etc

The trick here I guess would be to find a dapp that has some natural partitioning scheme that doesn’t force accounts/datastructures to be locked on child-chains for operations to take place in parent chains.

Or you would have some kind of mask in parent-chain that locks certain adresses, so you then exit child-chain to perform cross-child-chain operations and then re-lock data in sub-chains

edit: as for diagonal operations, perhaps it can speed up some operations in that you could perform an operation on child A relative to state in child B without first going to parent AB

---

**ldct** (2018-02-21):

The plasma paper ([plasma.io](http://plasma.io)) talks about nesting plasma chains into a tree, and how withdrawals interact with the tree structure.

It is not clear to me what the diagonal chain means. Is there a plasma root contract running on both p1 and p3? Do headers in p4 get committed to p1 or p3 or both?

