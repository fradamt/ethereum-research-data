---
source: ethresearch
topic_id: 4883
title: Alternative proposal to solve the storage problem
author: kladkogex
date: "2019-01-24"
category: EVM
tags: []
url: https://ethresear.ch/t/alternative-proposal-to-solve-the-storage-problem/4883
views: 1663
likes: 1
posts_count: 4
---

# Alternative proposal to solve the storage problem

Here is an alternative proposal to the storage problem in lieu of storage rent:

1. EVM storage instructions are umodified as they are now.
2. Each full node accepting read requests registers its IP endpoint and deposits a standard stake.
3. Clients pay probabilistic payments for each full node read request.
4. Each read request has to be load balanced so that each registered node gets the same traffic.  The load balancing is done as follows:

a) for each request, three nodes are pseudo-randomly selected based on the hash of read request

b) the client decides to which of three nodes to make the probabilistic payment  based on which node replied first.

Thats it.  Each node get the same share of load balanced requests and becomes interested in upgrading its hardware and storage.  So we end up with 100 times more powerful nodes that can store 100 times more data.

## Replies

**sorawit** (2019-01-24):

Can people just query their local node to avoid paying fee? If they do that, other nodes would still need to maintain the data for processing further transactions forever, but they won’t get any fee for storing such data in state storage.

---

**kladkogex** (2019-01-25):

Most users I guess do not run their nodes, they trust to services like Infura.

If you run your local node, you will still need to pay to initially  download the state from other nodes.

---

**dlubarov** (2019-01-25):

How would you stop clients from using the service without paying? Unless it was reputation-based, it seems like clients would need to make deposits as well. If so, it might be worth considering LN-style payment channels as an alternative to probabilistic payments.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> b) the client decides to which of three nodes to make the probabilistic payment based on which node replied first.

This doesn’t seem enforceable though; theoretically nodes might offer out-of-band rebates and clients might select nodes with the highest rebate. In particular, an operator wealthy enough to make `n` deposits could have `n` node identities backed by the same storage, so they would be `n` times more efficient than operators with a single identity, and might offer those savings as rebates.

Another concern is that, unless replication proofs were required, some nodes might use an LRU cache rather than storing all data. Depending on the cache size, nodes could potentially still answer most requests while saving on storage costs. That could be an issue for clients who needed to access old, stale data; they might find that none of the three nodes assigned to their request have it.

There are some projects using similar ideas like https://pokt.network/ ([@o_rourke](/u/o_rourke)), although I can’t recall how incentives work in their design.

