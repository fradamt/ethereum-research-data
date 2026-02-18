---
source: ethresearch
topic_id: 22706
title: Were MPTs ever the best choice?
author: "71104"
date: "2025-07-06"
category: Cryptography
tags: []
url: https://ethresear.ch/t/were-mpts-ever-the-best-choice/22706
views: 264
likes: 1
posts_count: 7
---

# Were MPTs ever the best choice?

Now I’m well aware that Ethereum is migrating to Verkle trees which are a completely different beast, but while working on my own blockchain project I evaluated Merkle-Patricia trees (or tries) versus various types of self-balancing trees and I suspect I have a result that makes **3-ary B-trees** significantly better than MPTs.

Let’s consider a highly simplistic scenario where we only need to index account balances, so no smartcontract storage or anything else. We need to construct a Merkle-proven associative data structure whose keys are account addresses and whose values are their respective ETH balances in wei.

I understand that Ethereum uses nibbles as the “trie alphabet” (is that correct?), meaning each node of the trie can have at most 16 children, all keys are 40 characters long, and so is the maximum height of the trie.

If we assume a more or less uniform distribution of the addresses we’re going to have:

- 16 sub-trees in the root node, each with the ~same size;
- 16 sub-trees in each second-level node, each with the ~same size;

and so on. **Basically a complete 16-ary tree**. Note that past a certain prefix each address stops having characters in common with other addresses, so the remaining suffix is a long list of characters that are unique to that address. So this tree is complete from the root down to a certain point, after which it’s just long individual branches (… a “willow tree”?). From now on I’ll ignore these long suffixes and only focus on the tree of prefixes, which is the most critical part because it’s relatively easy to optimize the suffixes (if the MPT is a [compressed trie](https://en.wikipedia.org/wiki/Radix_tree) then each suffix contributes with a single hash).

If we assume 1 billion known accounts, that makes for a height of:

log_{16}(1e9) = 9 \cdot log_{16}(10) = 9 \cdot \frac{ln(10)}{ln(16)} \approx 7.47

Since this is a Merkle tree, **the metric we need to optimize for is the number of hashes in each proof**, which equals the length of a root-to-leaf path multiplied by the arity of the tree (at each step the Merkle proof requires all sister hashes). Let’s call this metric M, and let N be the number of known accounts:

M = 16 \cdot log_{16}(N)

With N = 1e9 we have:

M = 16 \cdot log_{16}(1e9) \approx 16 \cdot 7.47 \approx 119.59

About 120 hashes in each proof.

Now let’s compare that with self-balancing trees, assuming our trees are perfectly balanced for simplicity.

AVL trees are binary, so those would result in:

M = 2 \cdot log_2(1e9) \approx 59.79

hashes in each proof. It looks like **AVL trees would pretty much half the size of all proofs**, but it’s actually even better than that! Search trees are slightly different from tries: in tries you need to walk all the way down to a leaf to find a value, while in search trees *all* nodes are values, not just the leaves! That means the length of a proof from an AVL tree isn’t necessarily log_2(N), it could be anything between 1 and log_2(N). Roughly half of the nodes are internal and half are leaves, so the average case is still O(log_2(N)) but in the best case (i.e. when we query the node that happens to be the root) the corresponding proof has only one hash.

And it gets even better with B-trees. [B-trees](https://en.wikipedia.org/wiki/B-tree) are self-balancing trees with arbitrary order. With 3-ary trees we have:

M = 3 \cdot log_3(1e9) = 27 \cdot log_3(10) \approx 56.59

Can it get even better? Let’s analyze the function of the worst-case number of hashes, k \cdot log_k(N). We’re generally interested in k \geq 2 and we can assume N \gg 1. Let’s convert it to a real-variable function and search its minimum:

\frac{d}{dx} x \cdot log_x(N) = \\
= \frac{d}{dx} x \cdot \frac{ln(N)}{ln(x)} = \\
= ln(N) \cdot \frac{d}{dx} \cdot \frac{x}{ln(x)} = \\
= ln(N) \cdot \frac{1}{ln^2(x)} \cdot \left( ln(x) - \frac{x}{x} \right) = \\
= \frac{ln(N) \cdot (ln(x) - 1)}{ln^2(x)}

Since N \gg 1, the only root is x = e:

\frac{ln(N) \cdot (ln(x) - 1)}{ln^2(x)} = 0 \\
ln(x) - 1 = 0 \\
ln(x) = 1 \\
x = e

When x \to +\infty our function diverges positively:

\lim_{x \to +\infty} \frac{x}{ln(x)} = +\infty

When x \to 1^+ it also diverges positively:

\lim_{x \to 1^+} \frac{x}{ln(x)} = \frac{1^+}{0^+} = +\infty

So x = e must be a minimum, not a maximum.

e is around 2.7, so the self-balancing trees that best minimize M must be either binary trees or 3-ary trees, and we’ve already shown that 3-ary trees are slightly better than binary trees.

## Conclusions

Purely in terms of size of the Merkle proofs, I don’t think Merkle-Patricia Tries were the best choice for managing Ethereum’s storage. I think 3-ary B-trees were.

It’s possible that MPT were still preferred because they are deterministic, whereas self-balancing trees are not. But how relevant is that? Blockchain state is immutable, once a block is built you don’t need to re-index all data into another tree, risking to produce a different but equivalent tree. Am I missing anything?

## Replies

**qizhou** (2025-07-12):

I am not sure the proof size is the solo optimization goal, but I guess another primary optimization goal is the access latency of different trees (i.e., number of intermediate nodes to traversed from root to leaf), given a typical 4K IO size of a SSD, 4K / 32 = 128 is the optimal one at the price of a larger proof size.  16 seems to be a good trade-off between proof size and access latency.

---

**71104** (2025-07-12):

If we’re dealing with microscopic times then you should also factor in the time to re-calculate all the hashes to verify the proof. The larger the order of the tree, the longer the array to digest in each hash (sister hashes don’t need to be re-calculated but they contribute to the calculation of the parent hash).

OTOH if you’re talking about optimizing the bandwidth-delay product I’d note that a good implementation probably wouldn’t need to do a disk seek upon querying the storage because it would use memory-mapped files, so we could reasonably assume that all data is there from previous accesses.

---

**qizhou** (2025-07-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/71104/48/20098_2.png) 71104:

> OTOH if you’re talking about optimizing the bandwidth-delay product I’d note that a good implementation probably wouldn’t need to do a disk seek upon querying the storage because it would use memory-mapped files, so we could reasonably assume that all data is there from previous accesses.

We cannot cache all of the nodes of the trees if the memory size is limited.  E.g., the MPT of the latest state is about ~200GB.  Tons of optimizations have been done recently by Ethereum clients such as Geth/Nethermined, including path-based scheme, which improves the EVM processing power from ~100M gas/sec to ~300-500 M gas/sec.

I would be curious how the MPT design may impact the performance given that the Ethereum roadmap is pivoted to scaling L1 first.

---

**71104** (2025-07-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> E.g., the MPT of the latest state is about ~200GB

… most of which is never queried because it belongs to past blocks, so the OS can safely swap it out.

---

**qizhou** (2025-07-12):

This is a single state size, not including historical states in past blocks.

---

**71104** (2025-07-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/qizhou/48/1953_2.png) qizhou:

> This is a single state size, not including historical states in past blocks.

Okay, that’s surprising, but on the other hand I’m struggling to understand the rationale for replicating the whole storage of the entire blockchain at every block. It looks to me like that would be massively inefficient. In my opinion, a good alternative is to engineer each node of the tree to store a B-tree map (with sparse keys!) from block numbers to values for that node. That way you can update the same tree incrementally rather than copying it at every block.

