---
source: ethresearch
topic_id: 4934
title: "[Invalid] O(n) LMD GHOST that is constant time on the number of blocks since genesis"
author: KentShikama
date: "2019-02-02"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/invalid-o-n-lmd-ghost-that-is-constant-time-on-the-number-of-blocks-since-genesis/4934
views: 1795
likes: 0
posts_count: 9
---

# [Invalid] O(n) LMD GHOST that is constant time on the number of blocks since genesis

Please see [[Invalid] Another attempt at O(n) LMD GHOST that is constant time on the number of blocks since genesis](https://ethresear.ch/t/another-attempt-at-o-n-lmd-ghost-that-is-constant-time-on-the-number-of-blocks-since-genesis/4949) for an updated version.

For background on CBC Casper, see: https://vitalik.ca/general/2018/12/05/cbc_casper.html

Here is an idea for a O(n) time estimator where n is the number of validators for the blockchain. In short, we are pushing all the information needed to execute the LMD GHOST fork choice rule into each block. In the map of bonded validators, in addition to their stakes, keep a counter that represents the depth of the last block the validator has proposed in the current chain. When proposing a new block, add 1 to the previous value of the counter for every other validator but yourself and set your counter to 0. Score the latest messages (blocks) based on the following formula:

1. Subtract the maximum counter value from all counters. Call this negative (or zero) value the normalized counter.
2. Build an list of tuples as follows. Drop the validator corresponding to the maximum value counter (which will be zero) and take the negated sum of all the remaining validator’s stakes. The first element will be a tuple of that sum followed by the largest normalized counter value remaining. Drop the validator corresponding to the second largest normalized counter and take the negated sum of all the remaining validator’s stakes. The second element will be a tuple of that sum followed by the value of the largest normalized counter value remaining. And so on. For tied normalized counter values, drop the validator with the higher stake. For example, if you have a map from validator stakes to normalized counters that look like {10:-4, 10:-5, 11:0, 10:0} this will become [(-30,0), (-20,-4), (-10,-5)].
3. The resulting array is the score. To compare scores, compare across the first element of each tuple down the array. Tiebreak using the second element of each tuple. For example, [(-31,0), (-21,-3), (-10,-5)] is smaller than [(-31,0), (-20,-4), (-10,-5)].

The estimator should return the latest message (block) with the LOWEST score. Note that this estimator returns the same result as the original LMD GHOST fork choice rule.

Edit: I change the algorithm to drop the validator with the higher stake for tied normalized counter values.

## Replies

**vbuterin** (2019-02-03):

Let’s say you have a structure as follows:

```auto
    _,----[A1]-----[A2]
[G]:_
     `----[B1]-----[B2]
```

And suppose that there are 10 votes for A2, 50 votes for B1, and zero votes for A1 and B2. Following the GHOST rule, B2 should be the head. However, it seems like  according to this rule, A2 would dominate, as it has a (x, 0) component in its score, while the B chain does not.

Another challenge: what if two different blocks contain different information, and according to each of the two blocks that block is the head?

---

**KentShikama** (2019-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Let’s say you have a structure as follows:
>
>
>
> ```auto
>     _,----[A1]-----[A2]
> [G]:_
>      `----[B1]-----[B2]
> ```
>
>
>
> And suppose that there are 10 votes for A2, 50 votes for B1, and zero votes for A1 and B2. Following the GHOST rule, B2 should be the head. However, it seems like according to this rule, A2 would dominate, as it has a (x, 0) component in its score, while the B chain does not.

Edit: I’ve modified the algorithm to drop the highest weighted validator on ties on the normalized counter value.

Let me expand on your example. Let’s say there is 3 validators in your example: A, B, and C. Validator A has proposed A1 and A2. Validator B has proposed B1. Validator C has proposed B2. A, B, and C have weights of 10, 50, and 0.01, respectively. I say 0.01 because a validator cannot have a weight of 0 (at least in my head). Thus as you’ve mentioned following the GHOST rule, B2 is the head because it has a score of 50.01 while A2 only has a score of 10.

Now lets score each block according to this new algorithm.

Score for A1

Note we don’t have to score for A1 as it is not the latest message (block) of any validator

Score for A2

Validator to counter map {10:0, 50:2, 0.01:2} =>

Validator to normalized counter map {10:-2, 50:0, 0.01:0} =>

Score array [(-10.01,0),(-10,-2)]

Score for B1

Validator to counter map {10:1, 50:0, 0.01:1} =>

Validator to normalized counter map {10:0, 50:-1, 0.01:0} =>

Score array [(-50.01,0),(-50,-1)]

Score for B2

Validator to counter map {10:2, 50:1, 0.01:0} =>

Validator to normalized counter map {10:0, 50:-1, 0.01:-2} =>

Score array [(-50.01,-1),(-0.01,-2)]

B2 has the lowest score followed by B1 and then A2. Hence, we would pick B2 as the head as desired.

> what if two different blocks contain different information, and according to each of the two blocks that block is the head?

Would you be willing to expand on this? Scoring happens according to one view, so either one score is higher or the scores are equal - the latter is impossible unless they are the same block.

---

**KentShikama** (2019-02-03):

[@vbuterin](/u/vbuterin) Apologies for the many edits on my post. Thanks for pointing out the issue - I’ve edited my original post with the fix.

---

**vbuterin** (2019-02-04):

> B2 has the lowest score followed by B1 and then A2. Hence, we would pick B2 as the head as desired.

Ah, so you’re comparing based on which block has the fewest validator voting at the most recent slot, I see. Then let’s do the following example:

```auto
    _,----[A1]-----[A2]
[G]:_
     `----[B1]-----[B2]
```

A1 has 50 votes, A2 has 10 votes. B1 has 30 votes, B2 has 1 vote.

B2 would have a score array [(-1, 0), (-30, 1)], A2 has [(-10, 0), (-50, 1)]. Hence, B2 would dominate. However, under LMD GHOST, A2 should dominate.

---

**KentShikama** (2019-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Then let’s do the following example:
>
>
>
> ```auto
>     _,----[A1]-----[A2]
> [G]:_
>      `----[B1]-----[B2]
> ```
>
>
>
> A1 has 50 votes, A2 has 10 votes. B1 has 30 votes, B2 has 1 vote.
>
>
> B2 would have a score array [(-1, 0), (-30, 1)], A2 has [(-10, 0), (-50, 1)]. Hence, B2 would dominate. However, under LMD GHOST, A2 should dominate.

Let there be 4 validators in your example: A, B, C, and D. Validator A has proposed A1. Validator B has proposed A2. Validator C has proposed B1. Validator D has proposed B2. A, B, C, and D have weights of 50, 10, 30, and 1, respectively.

Score A2

Validator to counter map {50:1, 10:0, 30:2, 1:2} =>

Validator to normalized counter map {50:-1, 10:-2, 30:0, 1:0} =>

Score array [(-61,0),(-60,-1),(-10,-2)]

Score B2

Validator to counter map {50:2, 10:2, 30:1, 1:0} =>

Validator to normalized counter map {50:0, 10:0, 30:-1, 1:-2} =>

Score array [(-41,0),(-31,-1),(-1,-2)]

A2 has a lower score array than B2, and thus A2 is picked as the head as desired.

---

**KentShikama** (2019-02-04):

I found a counter-example with the infinitely switching fork-choice example.

---

**KentShikama** (2019-02-05):

I’m thinking that if we also record a sequence number alongside the counter, we could resolve the issue. I’ll have to think a bit more.

---

**KentShikama** (2019-02-05):

Please see [[Invalid] Another attempt at O(n) LMD GHOST that is constant time on the number of blocks since genesis](https://ethresear.ch/t/another-attempt-at-o-n-lmd-ghost-that-is-constant-time-on-the-number-of-blocks-since-genesis/4949) for the fix. I didn’t want to pollute this thread since the examples in this discussion no longer apply and the new algorithm is considerably simpler.

