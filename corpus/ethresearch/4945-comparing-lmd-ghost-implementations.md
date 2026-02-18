---
source: ethresearch
topic_id: 4945
title: Comparing LMD GHOST implementations
author: protolambda
date: "2019-02-04"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/comparing-lmd-ghost-implementations/4945
views: 2408
likes: 3
posts_count: 2
---

# Comparing LMD GHOST implementations

Since the last Eth 2.0 implementers call (nr 11), I started work on a comparison of the different LMD-GHOST implementations.

The discussion is split up in two:

1. Work out simulation parameters to compare implementations with, here: https://github.com/ethereum/eth2.0-specs/issues/570
2. Collect all LMD-GHOST implementations + explanations. I created a github repo here: https://github.com/protolambda/lmd-ghost

So far I have 5 different implementations, some with very different trade-offs. The Readme contains a write-up for each of them.

With this post here I hope to get more people involved, outside of the sharding gitter. Feedback and new implementations are welcome.

## Replies

**vbuterin** (2019-02-04):

Great work! I really love the stateful sum vote DAG and the optimization there of only needing to update going back to the intersection between the old vote and the new vote.

Made some comments already in the sharding gitter. Copying some important ones:

- There’s an important optimization usable for all of these implementations, that if some set of validators are (attesting to | newly attesting to | no longer attesting to) the same block, those effects can be aggregated together and processed as one. So in the maximally happy case, where all validators participate every epoch so their new latest messages are in the current epoch and their previous ones are in the previous epoch, the fork choice rule can be computed/evaluated in O(128 * log(t)) time, with the exception of the preprocessing step, but that’s relatively trivial as it’s just up to 4 million arithmetic and equality checking operations.
- Need to take into account validator balance changes (see https://github.com/ethereum/eth2.0-specs/pull/571); but if we use int(balance) instead of balance as in the PR then these changes should be infrequent.
- In the longer term, changes like Rate-limiting entry/exits, not withdrawals might make it so that instead of using one validator set, there would be different validator sets active at different contexts. For example, if a block R has children A and B, and A has children A1 and A2, and B has children B1 and B2, the validator sets used to decide A vs B, A1 vs A2, and B1 vs B2 would all be different.

