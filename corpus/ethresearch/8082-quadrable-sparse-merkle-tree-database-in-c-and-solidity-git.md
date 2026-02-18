---
source: ethresearch
topic_id: 8082
title: "Quadrable: Sparse merkle tree database in C++ and Solidity, git-like command-line tool"
author: hoytech
date: "2020-10-07"
category: Data Structure
tags: [sparse-merkle-tree]
url: https://ethresear.ch/t/quadrable-sparse-merkle-tree-database-in-c-and-solidity-git-like-command-line-tool/8082
views: 2602
likes: 2
posts_count: 3
---

# Quadrable: Sparse merkle tree database in C++ and Solidity, git-like command-line tool

Hi! I’ve been working on a project called [Quadrable](https://github.com/hoytech/quadrable) that I think might be of some interest to this group.

It’s a sparse, binary merkle tree database. The primary implementation is a header-only C++17 library, and most of the functionality is exposed by a git-esque command-line tool (`quadb`). I also have an implementation of the core operations in Solidity. One of the main applications I have in mind is an optimistic roll-up system.

Features:

- Persistent database: Tightly integrated with the LMDB embedded database, instead of as a stand-alone tree data-structure library. No limits on key or value size. ACID transactions. Instant crash recovery (no write-ahead logs).
- Multi-version: Many trees can exist in the DB simultaneously, and all structure is shared where possible. Making snapshots or checkpoints is cheap, as is switching between them. Orphaned nodes can be garbage collected.
- Combined proofs: When making proofs for multiple elements, redundant and computable nodes are omitted (I think this is sometimes also called a multi-proof). Quadrable’s approach is a bit more complicated than the usual octopus algorithm since our leaves can be at different heights in the tree. Instead, there is a mini “proof command-language” to hash and merge strands together to re-build the tree. A separation between proofs and the various possible proof encodings is maintained.
- Partial trees: While verifying a proof, a “partial tree” is constructed (in fact, this is the only way to verify a proof). A partial-tree can be queried in the same way as if you had the full tree locally, although it will throw errors if you try to access non-authenticated values. You can also make modifications on a partial-tree: the new root of the partial-tree will be the same as the root would be if you made the same modifications to the full tree. Once a partial tree has been created, additional proofs that were exported from the same tree can be merged in, expanding the partial-tree over time as new proofs are received. New proofs can also be generated from a partial-tree, as long as the values to prove are present (or were proved to not be present).
- Appendable logs: In addition to the sparse map interface, where insertion order doesn’t affect the resulting root, there is also support for appendable (aka pushable) logs. These are built on top of the sparse merkle tree, but proofs for consecutive elements in the log are smaller because of the combined proof optimisations. Pushable proofs let you append unlimited number of elements onto partial trees (a pushable proof is essentially just a non-inclusion for the next free index).

Interfaces:

- C++: Batchable operations. Multiple modifications or retrievals can be made in one traversal of the tree. All get operations are zero-copy: values are returned to your application as pointers into the memory map.
- Solidity: Supports importing proofs and the core get/put/push operations on the resulting partial trees. All pure functions. Recursion-free. ~700 lines of code.
- quadb command-line app: 20+ sub-commands. Snapshot checkouts/forking. Batch imports/exports. Tree diff/patch. Debugging and dumping.

Other:

- I’m told the documentation is pretty good. There are some colourful pictures.
- Nearly 100% test coverage. Address sanitiser support. AFL fuzzing of proof decoder started.
- Everything is BSD licensed

## Replies

**tawarien** (2020-10-07):

This is very interesting. I read the documentation and was wondering if you ever considered bubbling non-empty subtrees in addition to non-empty leaves as well?

It would compact the tree even more and may enable the Integer Key case out of the box without any special treatment.

You find a discussion of this in: [Compact Sparse Merkle Trees](https://ethresear.ch/t/compact-sparse-merkle-trees/3741) on this Forum. In the same discussion later down I presented an alternative to the initial suggestion ([Compact Sparse Merkle Trees](https://ethresear.ch/t/compact-sparse-merkle-trees/3741/12))

---

**hoytech** (2020-10-07):

Thank you! Yes, bubbling non-empty sub-trees is a very good idea. I guess it would make the tree like a radix tree or trie. I did consider doing this at the design stage but it seemed too complicated for me at the time and since keys are usually hashes I didn’t anticipate a very large benefit. However, as you point out it would simplify the integer key case and further compact the tree in other situations as well. I will read your forum post you linked and think more about this – thanks!

In fact, I recently became aware of another implementation that does this and in some other ways is similar to Quadrable: https://news.ycombinator.com/item?id=24593570

