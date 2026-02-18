---
source: ethresearch
topic_id: 22585
title: "BAFs: Scaling Ethereum L1 with Block-Level Access Filters"
author: cskiraly
date: "2025-06-11"
category: Execution Layer Research
tags: [scaling]
url: https://ethresear.ch/t/bafs-scaling-ethereum-l1-with-block-level-access-filters/22585
views: 155
likes: 1
posts_count: 1
---

# BAFs: Scaling Ethereum L1 with Block-Level Access Filters

*The idea of BAFs was inspired by the excellent research on BALs from [@Nero_eth](/u/nero_eth) , in fact I’ve first posted it [in a response to his post](https://ethresear.ch/t/block-level-access-lists-bals/22331/2). Below I try to explain the idea better.*

*Please consider this post more as a braindump than a finalized design.*

Slot time is clearly limited by the time it takes to diffuse state change in the network, since information about the change is required by the next block builder. Whether in the form of a block (list of transactions to be executed), or in form of a BAL (set of state changes), this means sending quite some data around the world.

This dependency is often elegantly modeled by a hypothetical \Delta upper bound on network latency. In reality, however, network latency depends on the size of the information to be diffused.

What if we could **expedite** a **small amount** of information, enough to **start the preparation of the next block** well before the actual block arrives?

BAFs are aiming to do exactly this. A BAF is small Bloom filter that identifies the part S’ of the state S that was not accessed by a block i. Any operation on S’ is thus safe to do in block i+1, even without knowing block i.

### But Bloom filters are “loose”, how could this work?

We take the BAL (more details on which BAL type we use will follow) and compress it using a Bloom filter to get the BAF. Then, we use this filter to check whether a part `e` of the state was “untouched” (not accessed) by block i.

We can see a bloom filter as a lossy compression. It has a fixed small size, and it:

- has False Positives (FP): we think some e was accessed, while it was not
- does not have False Negatives (FN): we think some state e was not accessed but it was.

So while a bloom filter is not precise, this is not a problem for us when we use it in a negated way. We might be excluding too many elements (because of the FPs), but we never include something that was modified by block i (because that would be an FN).

### Can this filter be small?

Currently the average uncompressed BAL size is 55 KB with [each entry being 32 + 20 = 52 bytes long](https://github.com/dajuguan/lab/blob/c0ed0175b9919805fbc815a67b2c65ff4cd92464/eth/go/access_list_count.go#L321). That’s approx 1000 entries.

Say we use a 1KB bloom filter, which easily fits in an UDP packet. That’s 8196 bits, quite some space for a bloom filter. A bloom filter is defined by k hash functions, each mapping an element to a single position out of the 8196. When adding an element to a bloom filter each of these bits are turned on (if it wasn’t already). When checking an element, we can be sure it was not added if at least one of these bits are 0.

The ideal number of hash functions is defined by

k = 1000/8192 * ln(2)≈5.678

Our FP probability can then be estimated as:

p = \left(1 - e^{-\frac{5.678 \times 1000}{8192}}\right)^{5.678} \approx 0.0195 \ \text{(1.95%)}

Someone using this BAF can then check whether a given transaction could potentially interfere with another block, even without having the block or the BAL, and tell, with certainty, if it cannot interfere.

### What should be the content and granularity of the BAF?

There are various design options here:

- account level granularity vs. slot level granularity
- state access vs. state modification

#### Account vs. slot granularity

For state access, both account and slot level granularity might make sense. Account level means an emptier filter but more structural exclusion; slot level means less exclusion but a more saturated filter, which means a higher FP rate. The above 2% estimate was with this latter.

An account level exclusion would also be needed for the transaction sender to avoid nonce conflicts.

Interestingly, if needed, we can easily combine two different granularities in the same filter by using binary OR, adding both account level transaction senders and slot level state access information in the same bitmap.

#### State access vs. state modification

Note that a state access level BAF is by definition more saturated (have more 1s) than a state modification level filter (which from now we call the BMF).

#### BMF

We could use a BMF to help builders start preparing their blocks. Assuming the BMF can reach the next block builder in a small fraction of the slot time (say 300ms), it could be used to start preparing a part of block that does not depend on the previous one.

A BMF could be useful for speeding up slot times, making sure the sequence of blocks is conflict free. By knowing the BMF of block i, the builder of block i+1 can start building on state that is immutable between block i-1 and block i. This, in fact, allow it to decide at the last moment whether to base its block on block i or block i-1.

#### BAF

A BAF could instead eventually be useful for parallel block building. If a builder is respecting the BAF of another block, then the two blocks become mutually independent and thus parallelizable. In other words, these blocks are order independent, when finally sequenced into a chain.

## Securing the BAF (or BMF)

Signinig: The BAF can be signed by block producer and enforced

Strict: if signed and enforced, we can make it a requirement that the BAF is exact, not a more than what filter is generated during a re-execution

### Pricing the BAF

There are transactions that are simply accessing lots of state, resulting in a large BAL and a saturated BAF. These clearly reduce possibilities for BMF based pre-build and BAF based parallelization.

Would it make sense to make it expensive to have a full BAF? I’m not sure this is a right idea, but it can be part of the design space.

### Unlucky combos

Being a probabilistic filter, it might happen that some combinations create saturated BAFs even if the accessed (or modified) state is not that large. This is an unlucky combination of the hash functions forming the bits of the bloom filter.

We can mitigate such effect by using a “rotating” bloom filter construct, by making the hash functions depend on the slot number (or chain height). We can even make this change gradual, shifting in/out hash functions one-by-one as the slot number grows.
