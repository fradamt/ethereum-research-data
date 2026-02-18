---
source: ethresearch
topic_id: 2681
title: Merkle tree formation with odd number of leaves
author: noot
date: "2018-07-24"
category: Cryptography
tags: []
url: https://ethresear.ch/t/merkle-tree-formation-with-odd-number-of-leaves/2681
views: 6214
likes: 8
posts_count: 7
---

# Merkle tree formation with odd number of leaves

how is the merkle tree formed when the number of leaves isn’t log base 2?

for example, say you have 110 transactions in a block. the next power of 2 would be 128 - what is put in the last 18 leaves?

the two solutions I see would be having an unbalanced tree, where you hash pairs but don’t hash up the “extra” transactions until later up the tree.  branch lengths in this tree would be different. the other solution would be to duplicate the last transaction up until there are 2^n leaves, where n is the number of levels.

in the patricia tree [specs](https://github.com/ethereum/wiki/wiki/Patricia-Tree#transactions-trie), it states that a branch is a 17-item node, so this suggests that every branch has to be the same length, meaning we can’t have an unbalanced tree.

what is the solution ethereum takes? do we duplicate the last transaction, or do we create a tree as per [this answer](https://ethereum.stackexchange.com/a/29292) where we duplicate the last leaf to give it a sibling, hash those together, then duplicate the parent to give that a sibling, and so on.

## Replies

**vbuterin** (2018-07-24):

The other natural option is to fill all the remaining leaves with empty data.

You can absolutely do non-binary tree structures like Patricia trees, but IMO they’re uglier, and binary trees are simpler and more efficient.

---

**noot** (2018-07-24):

that makes sense, thanks for the reply. is this what the current implementation does?

---

**gakonst** (2018-07-25):

Our Sparse Merkle Tree implementation precomputes all leaves with default values:


      [github.com](https://github.com/loomnetwork/plasma-cash/blob/master/server/test/SparseMerkleTree.js)




####

```js
const utils = require('web3-utils');
const BN = require('bn.js');

module.exports = class SparseMerkleTree {
    constructor(depth, leaves) {
        this.depth = depth;
        // Initialize defaults
        this.defaultNodes = this.setdefaultNodes(depth);
        // Leaves must be a dictionary with key as the leaf's slot and value the leaf's hash
        this.leaves = leaves;

        if (leaves && Object.keys(leaves).length !== 0) {
            this.tree = this.createTree(this.leaves, this.depth, this.defaultNodes);
            this.root = this.tree[this.depth]['0'];
        } else {
            this.tree = [];
            this.root = this.defaultNodes[this.depth];
        }
    }

```

  This file has been truncated. [show original](https://github.com/loomnetwork/plasma-cash/blob/master/server/test/SparseMerkleTree.js)








https://github.com/loomnetwork/plasma-erc721/blob/master/plasma_cash/utils/merkle/sparse_merkle_tree.py


      [github.com](https://github.com/loomnetwork/plasma-cash/blob/master/server/contracts/Core/SparseMerkleTree.sol)




####

```sol
pragma solidity ^0.4.24;

// Based on https://rinkeby.etherscan.io/address/0x881544e0b2e02a79ad10b01eca51660889d5452b#code
// Original Code for the sparse merkle tree came from Wolkdb Plasma, this is now no longer compatible with that
// we have javascript and Golang implementations for reference of the new implementation.
contract SparseMerkleTree {

    uint8 constant DEPTH = 64;
    bytes32[DEPTH + 1] public defaultHashes;

    constructor() public {
        // defaultHash[0] is being set to keccak256(uint256(0));
        defaultHashes[0] = 0x290decd9548b62a8d60345a988386fc84ba6bc95484008f6362f93160ef3e563;
        setDefaultHashes(1, DEPTH);
    }

    function checkMembership(
        bytes32 leaf,
        bytes32 root,
```

  This file has been truncated. [show original](https://github.com/loomnetwork/plasma-cash/blob/master/server/contracts/Core/SparseMerkleTree.sol)

---

**noot** (2018-07-27):

Nice.

I was asking more specifically about the current implementation for forming merkle trees inside the EVM.

---

**ChainSafe** (2018-08-21):

How does ethereum specifically form merkle trees in the EVM?

---

**ZacMitton** (2019-03-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/noot/48/1811_2.png) noot:

> having an unbalanced tree, where you hash pairs but don’t hash up the “extra” transactions until later up the tree. branch lengths in this tree would be different.

This seems to be the more efficient solution. It seems easy enough to implement.

Unless someone can tell my why there is any meaningful benefit to repeating hashes and hashing them with themselves, I’m going to implement the [bagging the peaks](https://github.com/proofchains/python-proofmarshal/blob/efe9b58921b9a306f2b3552c30b84e1043ab866f/proofmarshal/mmr.py#L96) portion of the MMR structure from FlyClient as eluded by peter todd (in the efficient way shown in the link).

(To clarify, mmr is a more complex structure, but it is the 5 “peaks” that are getting put into a binary merkle tree)

