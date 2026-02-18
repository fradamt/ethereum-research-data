---
source: magicians
topic_id: 4162
title: Merkle Tree Generalized Index
author: axe
date: "2020-03-25"
category: EIPs
tags: [eth1x]
url: https://ethereum-magicians.org/t/merkle-tree-generalized-index/4162
views: 930
likes: 0
posts_count: 2
---

# Merkle Tree Generalized Index

Hi to all, I’m collecting feedback on Merkle Tree Multi Proofs.

**Based on your feedback**, this can became a EIP and deployed in all networks of Ethereum.

**Objective**

Deploy on chain a tool that helps smart contract developers to incorporate a merkle tree functionality with the possibility of selecting a subset of proofs in opposition of giving all the proofs.

The library calculates the root of the tree based on the information given. That information is split in two arrays that we will define below.

The general idea is to have a Merkle Tree capable of generating the correct root given a subset of leafs and all the necessary intermediary nodes values.

The user should review there’s proof requirements before using this tool.

The ideal case is when we have 2^n leaves. If there is less of that number, the user can fill the leafs with dumb data, and make the appropriated changes.

![:eyes:](https://ethereum-magicians.org/images/emoji/twitter/eyes.png?v=9) See more : [naxe / MerkleTreeMultiProofs · GitLab](https://gitlab.com/ngmachado/MerkleTreeMultiProofs)

Cheers

## Replies

**axe** (2020-03-27):

## Context

Merkle tree is a data structure that calculates each node value by hashing the values of two subnodes. If you don’t know much about Merkle Tree please refer to : [article](https://medium.com/hackernoon/merkle-trees-181cb4bc30b4) and [wikipidia](https://en.wikipedia.org/wiki/Merkle_tree) to get an basic idea.

The main point of using a Merkle Tree is data integrity checks. You can recalculate the tree from the leaves (most bottom nodes) until the root (most upper node) and check if the data was temper in the same way.

We have the same libraries in solidity that implement this basic use case, but they have a problem of scale. The biggest problem is that to validate a tree root you have to submit all the leaves.

If you have to submit all the leaves to calculate the root, you are bound to that limit. If you have a tree with 32 leaves, than you have to commit all the 32 leaves.

By using a coordenation system as the Generalized Index, we can selective choose each leaf to be part of the computation. This is the natural usage of a Merkle Tree.

By having this capacity of selection we can construct one tree that can represent many proof system.

Merkle Tree by itself is a multi part proof system, here you can select some leafs to “prove” and give the intermediate node values as needed. We will see with more detail below that this means.

This library aims to implement that functionality in a way that is useful to a large use case and at the same time don’t be very opinionated about the proof that you are trying to make.

