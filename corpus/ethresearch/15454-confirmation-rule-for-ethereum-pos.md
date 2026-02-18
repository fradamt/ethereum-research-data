---
source: ethresearch
topic_id: 15454
title: Confirmation Rule for Ethereum PoS
author: adiasg
date: "2023-04-28"
category: Consensus
tags: []
url: https://ethresear.ch/t/confirmation-rule-for-ethereum-pos/15454
views: 6036
likes: 10
posts_count: 10
---

# Confirmation Rule for Ethereum PoS

This post is opened for discussion re. the following fast confirmation rule for Ethereum proof-of-stake:

- Draft paper: confirmation-rule-draft.pdf (396.2 KB)
- Explainer blog post

This work was conducted together with Francesco D’Amato [@fradamt](/u/fradamt), Roberto Saltini [@saltiniroberto](/u/saltiniroberto), Luca Zanolini [@luca_zanolini](/u/luca_zanolini), & Chenyi Zhang.

## Confirmation Rule

**Assumptions:**

- From the current slot onwards, the votes cast by honest validators in a slot are received by all validators by the end of that slot, i.e., the network is synchronous with latency

**Notation:**

- n is the current slot, and e is the current epoch.
- b is a block from the current epoch e.
- There are S FFG votes from epoch e in support of c.
- W_f is the weight of validators yet to vote in epoch e, and W_t is the total weight of all validators.
- The adversary controls \beta  \frac{1}{2(1-\beta)} for all b' in the chain of b.
- \textrm{isConfirmed}(b,n) if:

the latest justified checkpoint in the post-state of b is from epoch e-1, and
- \textrm{isLMDConfirmed}(b,n), and
- [S - \textrm{min}(S, \alpha W_t, \beta (W_t - W_f))] + (1-\beta)W_f \ge \frac{2}{3}W_t.

If \textrm{isConfirmed}(b,n), then b is said to be ***confirmed*** and will remain in the canonical chain.

Since p_b^n cannot be observed, we define a practical *safety indicator* q_b^n to determine if p_b^n is in the appropriate range:

- q_{b}^n = \frac{\textrm{support for block } b}{\textrm{total weight}} from committees in slot b\textrm{.parent.slot} + 1 till slot n
- q_{b'}^n > \frac{1}{2} \left(1+\frac{\textrm{proposer boost weight}}{\textrm{total honest weight}}\right) + \beta for all b' in the chain of b implies \textrm{isLMDConfirmed}(b, n)

## Performance

In ideal conditions, the rule would confirm a block immediately after the end of its slot.

Under typical mainnet conditions, we expect the rule to confirm most blocks within 3-4 slots (under 1 minute).

We observe the following values for q (plot generated using [this prototype](https://gist.github.com/adiasg/4150de36181fd0f4b2351bef7b138893)):

[![q_plot](https://ethresear.ch/uploads/default/original/2X/1/133809368928eac36a12b930c866542202d23fc7.png)q_plot846×571 38.5 KB](https://ethresear.ch/uploads/default/133809368928eac36a12b930c866542202d23fc7)

The current slot is `6337565`, and the latest confirmed block is at slot `6337564`.

## Previous Work

- Safe head with LMD – this post is an extension of the linked work.
- Safe block confirmation rule
- High confidence single block confirmations in Casper FFG

## Replies

**czhang-fm** (2023-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/adiasg/48/1635_2.png) adiasg:

> in the last equation of q_{b’}^n > … total honest weight … isLMDConfirmed(b, n)

Please change to “total weight from slot(b’.parent)+1 to n”

---

**mart1i1n** (2023-12-21):

I have found a very easy way to delay the confirmation time forever.

First, I describe the way to delay the confirmation time from one slot to one epoch.

In the function `isLMDconfirmed` specified in [spec](https://github.com/saltiniroberto/eth2.0-specs/blob/21b9d2e29b057027fe08d96a34a4283a17d2b5e6/fork_choice/confirmation-rule.md#is_lmd_confirmed), confirming a block requires that its last 32 ancestors are also LMD confirmed.

However, the adversary can delay the release of a block to prevent its confirmation. In particularly, if a block is released at the 2/3 of the slot, almost no attestations support it. This leads the block can not be confirmed. Therefore, the next 32 blocks with the delayed block as the ancestor cannot be confirmed.

As a result, the strategy to delay the comfirmation time forever is delay a block during every epoch.

---

**barnabe** (2023-12-22):

If almost no attestations support the block, can the block not be trivially re-orged by the next proposer using the [late block re-org](https://github.com/ethereum/consensus-specs/pull/3034) feature?

---

**mart1i1n** (2023-12-22):

The answer is yes, I think. However, the block proposer can release the block between 4s to 4.5s after the slot starts, to make it not be re-org and also not be confirmed.

---

**Nero_eth** (2023-12-22):

If you release a block at second 4s to 4.5s the likelihood of this block getting reorged is very very high. Without doing any analysis on it, I’d say about as high as the market share of prysm and lighthouse as both support honest reorgs.

---

**mart1i1n** (2023-12-23):

I think the release time is not an vital issue.

I believe that if the block proposer releases its block just before validators release their attestations (e.g., at 3.9 seconds), there is a likelihood of a condition where at least 20% and at most 50% of validators receive the block before attesting. I believe this release time can be measured.

Even the precise determination of the release time may be challenging, an adversary holding a 20% stake could attest to its delayed block to prevent it from being reorganized by honest validators.

Therefore, I find it highly probable that such a scenario may occur.

---

**fradamt** (2023-12-23):

This is only causes a minor slow down of the confirmation rule. If the block stays in the canonical chain, it will keep accruing weight and eventually be confirmed, regardless of what the weight it accrued in its own slot is: as more slots and more votes accumulate, that original weight becomes less and less important. If instead it doesn’t stay in the canonical chain (i.e. it is reorged), then it becomes irrelevant to the confirmation rule.

---

**saltiniroberto** (2024-05-03):

We have just released [here](https://arxiv.org/abs/2405.00549) a paper presenting an updated version of the confirmation rule algorithm described in this post.

---

**thegaram33** (2025-08-05):

Do any consensus clients support this confirmation rule already? (I see Prysm has an [open PR](https://github.com/OffchainLabs/prysm/pull/15164)).

In Berlin, [@dankrad](/u/dankrad) mentioned this work to me and was surprised to learn that rollups generally don’t use it, e.g. for confirming deposits. The reason might be is that this spec is not implemented yet.

