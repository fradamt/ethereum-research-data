---
source: ethresearch
topic_id: 22590
title: "Rapidblocks: minimizing \"merge conflicts\" in the block building pipeline"
author: cskiraly
date: "2025-06-12"
category: Sharding
tags: [scaling]
url: https://ethresear.ch/t/rapidblocks-minimizing-merge-conflicts-in-the-block-building-pipeline/22590
views: 188
likes: 0
posts_count: 2
---

# Rapidblocks: minimizing "merge conflicts" in the block building pipeline

The main idea behind rapidblocks is that if we could somehow **build blocks without inter-block dependencies**, we could potentially **speed up slot times**, **reduce transaction inclusion times**, and **scale block production** substantially.

This is mainly because:

- we could make “reorgs” cheaper: we could simply skip some of the rapidblocks without a need for an expensive reorg. (Whether it is really much cheaper, or just a bit cheaper, is still to be understood.)
- we could allow to build such independent blocks almost in parallel. Almost, because we do need to order the builders and have a small amount of information flow.

Of course, there is a cost to this, since blocks do actually need to depend on each other somehow. We will get to this towards the end.

*Please consider this post more as a brain dump and discussion starter than a finalized design. The description is high level, neglecting many details, which might make the whole idea infeasible in practice.*

*Besics of the idea first appeared [in a reposonse to the BAL post](https://ethresear.ch/t/block-level-access-lists-bals/22331/2).*

## How to build “independent” blocks

### Modified state

Assume the builder of block i+1 knows all the addresses (or <address,storagekey> pairs) where the state was modified by block i.

Now it can build a block that is only based on the part of the state that was not modified by block i. In other words, it can build it on top of the “old” post-state of block i-1, which also means:

- the block i could be “skipped” from the chain without dropping block i+1
- the builder of block i+1 does not need to execute block i before build
- it does not even need to know the state changes of block i

### Accessed state

Now assume the builder of block i+1 knows all the addresses (or <addresses,storagekey> pairs) that were accessed (read or write) by block i. With this information, it can build an even stronger block which is logically parallelizable with block i.

- block i+1 does not depend on block i
- block i does not depend on block i+1

This enables us to cheaply reorganize the “chain” even further, since execution order does not matter.

Of course, the reader noticed that both assumption 1 and 2 already hold today. Our block builder knows all these addresses. So what are we speaking about?

There are two important points to note here:

- a, while the next block builder has this knowledge, we don’t deliver it efficiently, leading to longer slot times
- b, while the next block builder has this knowledge, we are not enforcing block independence, which would lead to more frequent and more expensive reorgs if we would reduce the slot time.

But this is insane, blocks do depend (now) on the previous block, right?

Right, but only a small part of them. Interestingly, over 90% of the transactions in a typical block seems to contains transactions that are not dependent on the previous block. For more details on the current state of inter-block dependencies, see [this post on warming](https://ethresear.ch/t/block-level-warming/21452).

With this premise, let’s see what are the potential tools that we could use to make repidblocks happen.

## The tools

### BAI and BMI

The main inspiration for these ideas is the exploration of various forms of block level state changes and access lists, also called [BAL, in an excellent work from Toni](https://ethresear.ch/t/block-level-access-lists-bals/22331).

It is easy to see that our condition 1 is the address list part of the post-block state change of the BAL. Let’s call this the BMI, the block level state modification index.

Our condition two instead maps the the BAL without pre or post state info. Lets call this the BAI, the Block-level Access Index.

*Note: maybe we should call these storage locations / write locations, but the L of Locataion was already taken for the L in Lists*

Thus, if we could fast-forward one of these to the next builder, and we would take advantage of the cheaper reorgs allowed by block independence, we could reduce slot times. In Ethereum we cannot just fast-forward this to the next builder, we need to send it to the whole network. Even if we know the next validator, we don’t know where it is in the network and we have no routing based on validator ID, for obvious reasons.

Still, we could think of prioritizing the BAI (larger) or the BMI (smaller) on the network, reducing slot time.

### BAF and BMF

It would be even better if we could somehow compress the BAI or BMI, say, into a single IP packet, and fast-forward that in the network. This would potentially allow us to diffuse the information in the whole network in as low as 300ms. One way we could try to achieve this is with Bloom filters. See [my BAF post](https://ethresear.ch/t/bafs-scaling-ethereum-l1-with-block-level-access-filters/22585) for more details.

### The rapidblock “chain” structure

Our final tool is the new “chain” structure. Actually, the underlying structure is not a chain but a restricted DAG, but we can easily “linearize” it into a chain view if someone really needs that. (And I think this is an important part for compatibility and an eventual evolutionary introduction of the ideas here).

Of course block should have dependencies. But they do not have to depend on the previously built one. If we can reduce the slot time, enforcing independence from the previous one and allowing it from the one before, could actually have the same result.

What we have created above is a block production pipeline that can build

- blocks that are mutually independent

any of these can be independently removed from the “chain”, without a influencing the validity of the other block.

blocks that are strictly ordered, but not state dependent

- if a block b was based on the BAF or BMF of block a still any of these can be cheaply removed from the chain, but they can’t be executed in a reverse order, or in parallel, since a might access state that was modified by b

Clearly, consensus becomes more complex, at least seemingly. Attestation is not just magically becoming faster just because we build blocks more frequently. But reorgs are much cheaper, and blocks can be built with a higher frequency. To be clear, I don’t yet have a clear view of how this should work, but I think we can create a consensus mechanism that is pipelined and can selectively “merge” independent sub-chains into a virtual **safe chain horizon**.

## What we gain

### Speeding up slot times

We can speed up slot times with this design for two reasons.

The main reason is the cheap reorg. Since blocks can be selectively skipped from the canonical chain, we effectively have very cheap reorgs, which means we can be more permissive on building blocks that will not make it for one or another reason.

The second reason is that we need less information to build a block, and we can distribute that small amount of information much faster in the network.

### Reduced transaction inclusion time

With shorter slot times, comes smaller transaction inclusion times. While this is not important for all, this is clearly part of the user experience.

### Scaling block production

Since we only need a very small filter to reach the next builder, we can also think of parallelizing block building. A kind of dynamic sharding without a pre-imposed state-space division. Again, the design is not yet clear here, but I think we can go in a direction where distributed block building is parallelized and pipelined based on the fast diffusion of BAFs or BMFs.

## Relation to other ideas

One can also see this idea as looking at BALs and warming from a new perspective. Instead of trying to send a large state change fast, we could try to ensure we don’t have a large change.

There are also ideas going in the direction of allowing transaction level “skip” in case of conflicts. I think there is space to try to combine such ideas, minimizing, but not necessarily eliminating inter-block dependencies. We could even try to devise a “fast path” for independent changes, and a “slow path” (but not slower than today) for dependent changes, leading to a design where overall chain capacity can increase without being limited by specific “worst case” transactions.

## Replies

**terence** (2025-06-12):

Interestingly, this is kind of what the inclusion list proposer in FOCIL is doing. The IL proposer for parent block `n` doesn’t need to see the block itself to release the inclusion list, it could build on grant parents, because the IL inclusion rules allow it

