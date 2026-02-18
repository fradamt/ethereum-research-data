---
source: ethresearch
topic_id: 6833
title: Definition of a rollup
author: kladkogex
date: "2020-01-24"
category: Layer 2
tags: [zk-roll-up]
url: https://ethresear.ch/t/definition-of-a-rollup/6833
views: 3867
likes: 10
posts_count: 5
---

# Definition of a rollup

Some one asked me about to provide a definition of a rollup - here is what I came up with

rollups can be loosely defined as solutions where transactions are put on chain but other things like transaction processing and state storage may be offchain

Good or bad ?

## Replies

**pinkiebell** (2020-01-24):

Sounds good, one could also say that data-availability is on-chain and everything else is not defined by a `rollup`.

---

**vbuterin** (2020-01-26):

The core essence of a rollup is data on-chain, computation off-chain. Particularly, a user is guaranteed to have the ability to personally reconstruct the full state of the system by scanning the chain history, and use that to deposit, withdraw or potentially enter as a sequencer.

---

**kladkogex** (2020-01-26):

Great!! Looks like everyone agrees!

---

**sachayves** (2020-01-29):

I think [Ed Felton’s](https://medium.com/offchainlabs/whats-up-with-rollup-db8cd93b314e) definition complements [@vbuterin](/u/vbuterin)’s (useful as an introduction):

> Rollup is a general approach to scaling open contracts, that is, contracts that everyone can see and interact with. In rollup, calls to the contract and their arguments are written on-chain as calldata, but the actual computation and storage of the contract are done off-chain. Somebody posts an on-chain assertion about what the contract will do. You can think of the assertion as “rolling up” all of the calls and their results into a single on-chain transaction. Where rollup systems differ is in how they ensure that the assertions are correct.

