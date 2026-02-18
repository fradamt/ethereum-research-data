---
source: magicians
topic_id: 4165
title: Ethereum state trie format change using an overlay
author: jpitts
date: "2020-03-26"
category: Magicians > Primordial Soup
tags: [eth1x, merkle-patricia-trie]
url: https://ethereum-magicians.org/t/ethereum-state-trie-format-change-using-an-overlay/4165
views: 1268
likes: 1
posts_count: 1
---

# Ethereum state trie format change using an overlay

This is a proposal by [@gballet](/u/gballet), articles and resources collected here for convenience.

“During the 1.x workshop in Paris last weekend, a couple ideas have been discussed for the transition from hexary tries to binary tries. It has been agreed that each proposal should be published on ethresearch for comparison and further discussion.”

**Overview article**

“The proposed process introduces a transition period during which two trees are maintained. This has the advantage that the main chain can keep operating while the tree is being converted, and it also ensures that all accounts will be translated to a binary format.”

https://medium.com/@gballet/ethereum-state-tree-format-change-using-an-overlay-e0862d1bf201

**The main discussion for [@gballet](/u/gballet)’s proposed is on ethresear.ch**

“A hexary to binary conversion method in which new values are stored directly in a binary tree sitting ‘on top’ of the hexary, while the ‘historical’ hexary tree is converted in the background. When the process is finished, both layers are merged.”


      ![](https://ethresear.ch/uploads/default/optimized/1X/_129430568242d1b7f853bb13ebea28b3f6af4e7_2_32x32.png)

      [Ethereum Research – 12 Mar 20](https://ethresear.ch/t/overlay-method-for-hex-bin-tree-conversion/7104)



    ![image](https://ethresear.ch/uploads/default/original/2X/a/a6752fc77965717e886135acc0c8d6288a1247e1.png)



###





          Execution Layer Research






During the 1.x workshop in Paris last weekend, a couple ideas have been discussed for the transition from hexary tries to binary tries. It has been agreed that each proposal should be published on ethresearch for comparison and further discussion....



    Reading time: 5 mins 🕑
      Likes: 13 ❤











**“Quick and Dirty” prototype implementation in geth (a pull request)**



      [github.com/holiman/go-ethereum](https://github.com/holiman/go-ethereum/pull/12)














####


      `trie_gen` ← `gballet:snapshot-to-bintrie`




          opened 03:20PM - 23 Mar 20 UTC



          [![](https://avatars.githubusercontent.com/u/3272758?v=4)
            gballet](https://github.com/gballet)



          [+1010
            -1](https://github.com/holiman/go-ethereum/pull/12/files)







Quick and Dirty prototype to build a binary trie from the snapshot, aimed at pro[…](https://github.com/holiman/go-ethereum/pull/12)ducing initial data for [1]. It doesn't do any caching, it doesn't do any parallelism, doesn't try to save memory and it stores branches very inefficiently.

@holiman it's also based on a pre-rebase version of `trie_gen`, I'll rebase if it helps/makes sense.

### Refs
 1. https://ethresear.ch/t/overlay-method-for-hex-bin-tree-conversion/7104/3

### TODO

 - [x] rebase
 - [x] pruning
 - [x] extensions
 - [x] parallelize generation and db writes
 - [x] rework storage format
 - [x] benchmark tests

### Running

This adds a `bintrie` subcommand to `geth` that takes the current snapshot and performs the conversion based on that, so conversion can be started with:

```
geth --snapshot bintrie
```












---

**Background**

Understanding Trie Databases in Ethereum

https://medium.com/shyft-network-media/understanding-trie-databases-in-ethereum-9f03d2c3325d

Modified Merkle Patricia Trie Specification

https://github.com/ethereum/wiki/wiki/Patricia-Tree
