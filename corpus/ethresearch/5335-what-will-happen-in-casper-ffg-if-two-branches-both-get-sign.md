---
source: ethresearch
topic_id: 5335
title: What will happen in Casper FFG if two branches both get significant amount of votes?
author: ChengWang
date: "2019-04-20"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/what-will-happen-in-casper-ffg-if-two-branches-both-get-significant-amount-of-votes/5335
views: 2057
likes: 4
posts_count: 10
---

# What will happen in Casper FFG if two branches both get significant amount of votes?

In Casper FFG, to finalize a checkpoint, it needs to get >2/3 votes.

What will happen if two checkpoints (of the same height) each get voted by >1/3 of the validators (by deposit)? In this case, no checkpoint would get >2/3 votes.

## Replies

**dlubarov** (2019-04-22):

Neither checkpoint would be finalized, as you say, but one of their descendants could be finalized later on.

As an example, given this checkpoint structure

```nohighlight
  b – d
 /
a
 \
  c – e
```

Say `a` is finalized. If the votes are split 50/50 between `a → c` and `a → c`, then neither will be finalized. But later on, there could be a supermajority vote for `a → d`, finalizing `d`. Then `b` would be “effectively final”, since any branch conflicting with `b` would also conflict with `d`.

---

**ChengWang** (2019-04-22):

In order to get supermajority vote for `a → d`, some of the voters for `a → c` would have to switch to vote for `a → d`; these voters would lose their staking rewards in the branch `a → c`.

Either voters for `a → b` switch or voters for `a → c` switch, but both are not incentivized to do so.

---

**adlerjohn** (2019-04-22):

Interesting question, especially given the design goal of Casper to the WW3-proof.

---

**dankrad** (2019-04-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/chengwang/48/2628_2.png) ChengWang:

> In order to get supermajority vote for a → d , some of the voters for a → c would have to switch to vote for a → d ; these voters would lose their staking rewards in the branch a → c .

Actually, validators voting for `a → d` after `a → c` will not get slashed, so it is ok. (You only get slashed for conflicting votes at the same height or skipping over your previous votes, both of which would not be happening here)

---

**kladkogex** (2019-04-22):

Thats one of the weaknesses … Theoretically this could go on forever unless someone runs a binary consensus protocol to select one of the two trees …

---

**dlubarov** (2019-04-22):

I agree with Dankrad – switching branches isn’t necessarily slashable. In this case it’s not since the source of each vote is the same (`a`).

[@kladkogex](/u/kladkogex) technically most consensus protocols could go on forever, right? (Excluding protocols which assume full synchrony or tolerate zero faults.) Although granted, Casper could be particularly slow in practice since it essentially runs one step of a consensus algorithm at each checkpoint.

---

**ChengWang** (2019-04-22):

[@dankrad](/u/dankrad) [@dlubarov](/u/dlubarov) It’s not about slashing. It’s about losing potential staking rewards.

---

**dlubarov** (2019-04-22):

Ah I see. Well the spec says that validators should use LMD GHOST as their fork choice rule. Validators could ignore that and follow the branch that they had accumulated more rewards on, but wouldn’t that be a suboptimal strategy since nobody would receive rewards if consensus gets stuck? Whereas if a validator switches branches, at least their second vote would be rewarded.

From a game theoretic perspective, it seems like the strategy of not switching branches after a 50/50 split would be a Nash equilibrium, since no single player could change the outcome; consensus would get stuck regardless. But that equilibrium would have a payoff of zero, so the equilibrium where everyone follows LMD GHOST would be payoff dominant.

---

**kladkogex** (2019-04-23):

Yes,  the worst case can go forever, but the average time is bounded.

Here the average time can be unbounded . If the attacker has full info about the network, the attacker can make the thing stuck forever.

