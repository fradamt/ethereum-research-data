---
source: ethresearch
topic_id: 6487
title: ETh2, authenticated data structures, and gas costs
author: secparam
date: "2019-11-22"
category: Data Structure
tags: []
url: https://ethresear.ch/t/eth2-authenticated-data-structures-and-gas-costs/6487
views: 2474
likes: 1
posts_count: 7
---

# ETh2, authenticated data structures, and gas costs

Hi, I’m Ian, applied cryptography researcher and soon to be professor at the University of Maryland. I’ve been working on applied cryptography and cryptocurrency for a while (Zcash was my Ph.D. thesis), but am rather new to Ethereum and its low level details.

Ethereum writes data for one contract instance to many random locations in the Merkle Patricia Trie. By my understanding, this was intended to limit the damage an attacker can do by reducing everything to the average case. However as result, any update to the contract’s data 1) causes many random writes to disk and far worse 2) forces a number of different hash chains to be recomputed for the Trie. The second one of these is a major cost. Optimistic and zk-roll up work around this by, in CS terms, batching writes to one location and letting people dispute it.

In general, when designing high performance systems, one of the major things is to limit random IO operations as this causes performance issues. This is common research problem in systems. Here of course there is also a security dimension in terms of resource exhaustion. The fact that, in blockchains, this is done in authenticated data structures makes the issue far worse as it costs computational resources to recompute the authentication (regardless of the on disk/in memory representation).

What are the plans to address this in Eth2? Is the plan to still write data to random locations even within one contract? It seems there are a number of ways to limit the damage an attacker can do that do not come with the IO and hash computation costs of doing random writes.

## Replies

**adlerjohn** (2019-11-22):

Eth 2 is planning to using a modular “execution environment” (EE) framework. See link below for an overview. Each EE is basically the specification of a VM, written in WASM. As such, each EE defines its own accumulator—and thus data—format. Your concerns are valid, but should be addressed to EE designers rather than Eth 2 designers.

https://medium.com/@william.j.villanueva/a-journey-through-phase-2-of-ethereum-2-0-c7a2397a36cb

Moreover, execution in Eth 2 is stateless by design, as being stateful would result in no scalability gains. This externalizes the costs of doing these database accesses to state providers on the relay network.

https://medium.com/@adlerjohn/relay-networks-and-fee-markets-in-eth-2-0-878e576f980b

---

**secparam** (2019-12-04):

So those are both good, in that they appear to shift the cost off of the main chain and avoid forcing a particular choice of solution. This is great, in that it gives everyone the freedom to do it right. But doesn’t seem to provide an answer to the locality problem itself.  Someone is still going to have to deal with it. Whats the current thinking on solutions to the issue?

[@phil](/u/phil)  mentioned a move towards a simple binary Merkle tree. This lowers the cost of poor locality,  but doesn’t address root issue.  Are there other approaches being considered?

---

**musalbas** (2019-12-04):

Unless there has been any new developments, my understanding is that in general Eth 2.0 will prefer [Sparse Merkle trees](https://ethresear.ch/t/data-availability-proof-friendly-state-tree-transitions/1453/6) instead of Patricia tries, for state commitments. Sparse Merkle trees nodes have a constant height.

Keys are hashed to determine where their values in the tree should be, so this still seems to require random IO.

See also [spec](https://github.com/ethereum/eth2.0-specs/issues/1472) discussion.

---

**secparam** (2019-12-04):

Thanks.  Is the plan still to write to random locations in the tree even within a contract or to have locality and all data effectively in one location?

---

**musalbas** (2019-12-04):

I’m not aware of any discussions to achieve contract-level locality, but I suppose you can achieve that by storing the value for a variable x for contract ID y at H(y)||H(x), but you’d have to increase the size of the nodes in your tree as you need two collision-resistant hashes per node instead of one.

Isn’t there a way to prevent random IO without modifying the underlying tree design? You could implement your state storage system so that values for a particular contract are stored together, despite them having randomised key identifiers.

---

**secparam** (2019-12-05):

One way to do it is make all contract data some form of structured blob living under its ID.  I assume that’s a non starter,  but not knowing ETHs design goals, I’d be curious why.

Otherwise, I don’t entirely see how you get locality if your identifiers are randomized. If they aren’t randomized, then this seems easy.

But there appears to be some attack surface on the sparse tree if your identifies aren’t randomized. Given some data for a contract at location X,  it’s possible to write data to near by parts of the tree and make it, locally, less sparse around X. This messes with compression and I’m betting  this then increases the time it takes to compute an update.

So, unless I’m missing something, there’s still a locality vs adversarial attack problem that needs some thought.

