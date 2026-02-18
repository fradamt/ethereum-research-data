---
source: ethresearch
topic_id: 1738
title: Rsmt2d - Go implementation of two dimensional Reed-Solomon merkle tree data availability scheme
author: musalbas
date: "2018-04-15"
category: Sharding
tags: []
url: https://ethresear.ch/t/rsmt2d-go-implementation-of-two-dimensional-reed-solomon-merkle-tree-data-availability-scheme/1738
views: 2083
likes: 2
posts_count: 5
---

# Rsmt2d - Go implementation of two dimensional Reed-Solomon merkle tree data availability scheme

I’ve written an experimental Go library, [rsmt2d](https://github.com/musalbas/rsmt2d), that implements a two dimensional Reed-Solomon merkle tree data availability scheme. It has a [reparation algorithm](https://github.com/musalbas/rsmt2d/blob/master/extendeddatacrossword.go#L94) with the ability to repair squares in a byzantine setting, detecting byzantine rows and columns and inconsistencies between rows and columns, and allows for the generation of fraud proofs.

Feel free to use for experimentation or pick it apart. I plan to experiment with this as a data availability proof layer for fraud proof-supporting blockchain data structures.

I did discover some intricacies around designing a square repair algorithm: for example, it is important to verify that the original data of each row/column matches the extended data, even if the whole row/column is available, because otherwise other clients might reject the block if they receive different pieces of a row/column than you, causing a fork.



      [github.com](https://github.com/celestiaorg/rsmt2d)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/9/8/984da124b50ad8a44d41861845ea41052f1697e3_2_690x344.png)



###



Go implementation of two dimensional Reed-Solomon merkle tree data availability scheme.

## Replies

**josephjohnston** (2018-04-15):

[@musalbas](/u/musalbas)  Can you explain more what this is, or point to some resources for me? What’s a Reed-Solomon merkle tree, just a merkle tree encoding a Reed-Solomon codeword? How does that make an availability scheme?

---

**musalbas** (2018-04-15):

[@josephjohnston](/u/josephjohnston) Check out https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding. Sorry, should’ve probably linked to that in the original post.

---

**jamesray1** (2018-04-18):

Talk to Geth-sharding. Pinging [@rauljordan](/u/rauljordan) and [@prestonvanloon](/u/prestonvanloon).

Rust can be used with Go and other programming languages and vice versa.


      ![](https://ethresear.ch/uploads/default/original/3X/f/5/f5cd65cd6f9b4e886225927de7fef87ca18d40aa.svg)

      [doc.rust-lang.org](https://doc.rust-lang.org/book/second-edition/ch19-01-unsafe-rust.html#using-extern-functions-to-call-external-code)





###












      [github.com](https://github.com/mediremi/rust-plus-golang)




  ![image](https://ethresear.ch/uploads/default/optimized/3X/8/5/85bb3b9b10a3ae76e5cd0643f50d7e16abf40724_2_690x344.png)



###



Rust + Go — Call Rust code from Go using FFI










I will consider this for [Diamond Drops](https://github.com/Drops-of-Diamond/diamond_drops) when we get up to data availability proofs.

---

**prestonvanloon** (2018-04-18):

Definitely interested in this. Thanks!

