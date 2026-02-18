---
source: ethresearch
topic_id: 2636
title: PoS fork choice rule desiderata
author: vbuterin
date: "2018-07-21"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/pos-fork-choice-rule-desiderata/2636
views: 3835
likes: 2
posts_count: 1
---

# PoS fork choice rule desiderata

Here are some properties of PoS fork choice rules that are desirable:

- Majority honest progress: if >=50% of nodes build blocks by following the fork choice rule, the chain progresses and is (exponentially) unlikely to revert older blocks
- Manipulation resistance: even if an attacker captures a temporary supermajority of some small set (eg. =1/3 of nodes violating a slashing condition

---

Let’s analyze some known PoS fork choice rules:

- Longest chain: yes majority honest progress (many proofs of this), no manipulation resistance (if you capture a majority of a string of 100 validators, you can revert up to 100 blocks), yes stability, no finality bearing
- Latest message driven GHOST (as in Casper CBC): yes majority driven progress, yes manipulation resistance if many voters per block, yes stability, finality bearing possible but complicated to implement in practice
- Casper FFG plus longest chain: adds finality bearing, but may compromise stability (eg. there are 66 votes for some checkpoint that’s not part of the head, then suddenly a 67th shows up and it becomes justified)

We can try to improve the standing of Casper FFG with respect to manipulation resistance and stability by adding a version of GHOST that we call **recursive proximity to justification** (RPJ): [Immediate message-driven GHOST as FFG fork choice rule](https://ethresear.ch/t/recursive-proximity-to-justification-as-ffg-fork-choice-rule/2561)

However, RPJ has the issue that it still requires a fork choice rule to choose at the *intra-epoch layer*. In general, “stitching together” two distinct fork choice rules is a bad idea for stability, because there will inevitably be cases where one is not a good prediction of the other. For example, a winning checkpoint could have children A and B, where A is winning under the original fork choice rule, but then the first validator in the next epoch votes for B, and now RPJ says to choose B.

We can solve this by allowing justification to happen not just at checkpoints, but at *any height*. We also do not reshuffle validators at all except at dynasty boundaries (though we can reshuffle the selection of *proposers*). After this, we can just use RPJ as the sole fork choice rule. This leaves the only “stability” hole being the weakness described at the end of [Immediate message-driven GHOST as FFG fork choice rule](https://ethresear.ch/t/recursive-proximity-to-justification-as-ffg-fork-choice-rule/2561) , which is arguably an exceptional case. It gives us majority honest progress, manipulation resistance and finality, and stability in all “normal” cases.
