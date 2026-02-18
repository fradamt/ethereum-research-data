---
source: ethresearch
topic_id: 20409
title: Lookup argument and its tweaks
author: ETatuzova
date: "2024-09-11"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/lookup-argument-and-its-tweaks/20409
views: 357
likes: 10
posts_count: 3
---

# Lookup argument and its tweaks

In building the Placeholder proof system for =nil; Foundation, we use a lookup argument based on the [Plookup paper](https://eprint.iacr.org/2020/315.pdf) by Aztec researchers. We took Plookup technique as a starting point and then made some practical improvements for writing large PLONK circuits with a complex logic.

Lookup argument allows prover to prove that some table over prime field (hereafter assignment table) satisfies specific constraints: some cells computed from assignment table (lookup input) belong to list of values that is also computed from the assignment table (lookup table).

## Join-and-split algorithm

The core of Plookup techinque is a sorting algorithm. We call it **join-and-split** because it includes two steps:

- join — lookup table columns are joined together with input columns into single large vector using special reordering algorithm.
- split — constructed vector is split again into original size parts.

The case with the single lookup table and single input column is described in the Plookup paper in detail. But it wasn’t enough for our use-cases. We needed lots of efficiently packed lookup tables and lookup constraints applied to arbitrary rows and columns, and we didn’t want to repeat lookup argument for each `(input, table)` pair.

So, we modified join-and-split algorithm to be able to join more than two columns. It allows us to use multiple lookup constraints even if they are applied on same rows and use a large lookup table, even if its size is greater than the whole assignment table rows amount by appending columns to assignment table instead of rows. Balance between assignment table rows and columns amounts helps to find a perfect balance for the best prover performance and verification cost.

## Selector columns

Original article contains technique to lookup tuples of values that are placed in the same or neighboring rows. It constructs linear combinations of columns with a random factor. Combining this approach with polynomial expressions usage for lookup tables and input columns both we achieved selector columns full support. Circuit designer now can manage which rows exactly are constrained and what rows are reserved for lookup tables storing.

Plookup paper also describes technique for multiple lookup tables support. They propose to associate each lookup table with its unique identifier and fill tag column to mark what rows contains lookup tables with which identifier. Tag column for input helps to mark what constraints are applied to marked row. Tag columns should be a part of the random linear combination constructed for the lookup table and input columns respectively. This approach is obviously limited. Sum of lookup tables sizes should be less than the whole table rows amount.

We combined lookup table identifier usage with our selector columns construction and algorithms for large lookup tables. These modifications allow lookup tables to be stored and used without regard to lookup argument restrictions, but according to the best circuit design. It made our lookup argument into a universal and flexible tool.

Detailed description of our modifications can be found on our [HackMD](https://hackmd.io/@nil-research/rkjJFAtiC) page. Feel free to share your comments!

## Replies

**voronor** (2024-10-21):

How does the join-and-split algorithm modification for handling multiple lookup tables and columns improve the prover’s performance and verification cost in complex PLONK circuits?

---

**ETatuzova** (2024-10-24):

Here are some examples, where join-and-split works well.

**Prover performance**

Assume that we prove rather small computation that uses large lookup table.

If we don’t use join-and-split we have to resize whole assignment table to lookup table’s size.

Join-and split allows prover to work with smaller assignment table and pay for it by columns amout increasing. It leads to less memory consumption. Operations over assignment table columns also becomes cheaper.

[![Screenshot from 2024-10-24 13-02-31](https://ethresear.ch/uploads/default/original/3X/c/8/c85e749666baf136732ef620774fad70882916b6.png)Screenshot from 2024-10-24 13-02-31755×644 5.82 KB](https://ethresear.ch/uploads/default/c85e749666baf136732ef620774fad70882916b6)

**Verification cost**

Now suppose the scheme uses multiple lookup tables that are located to different columns and similar rows. The only way to implement this without join-and-split is to run the lookup argument twice, i.e., compute separate V polynomials for T1 and T2 lookup tables, generate separate packes of sorted columns. All V-s and sorted columns must be commited. The number of commited polynomials is smaller with join-and-split than without it. Commited polynomials amount directly affects on verification cost.

[![Screenshot from 2024-10-24 13-16-13](https://ethresear.ch/uploads/default/original/3X/7/a/7ae81fe53865ba218e3c118b121ae0cfa2627d2e.png)Screenshot from 2024-10-24 13-16-13432×337 2.09 KB](https://ethresear.ch/uploads/default/7ae81fe53865ba218e3c118b121ae0cfa2627d2e)

