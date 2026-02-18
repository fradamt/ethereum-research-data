---
source: ethresearch
topic_id: 2561
title: Immediate message-driven GHOST as FFG fork choice rule
author: vbuterin
date: "2018-07-14"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/immediate-message-driven-ghost-as-ffg-fork-choice-rule/2561
views: 7519
likes: 0
posts_count: 9
---

# Immediate message-driven GHOST as FFG fork choice rule

*Edit 2018.08.16: I am from now on going to use “immediate message driven GHOST” to refer to what I previously referred to as “recursive proximity to justification” or “RPJ”.*

There are two desirable goals for fork choice rules that the current proposed fork choice rules [[1]](https://ethresear.ch/t/attestation-committee-based-full-pos-chains/2259) [[2]](https://ethresear.ch/t/attestation-committee-based-full-pos-chains-version-2/2427) fail to satisfy:

1. Bad proposer resistance: if there is a medium-length run of bad proposers (possible because of RNG manipulation), then this could lead to damaging the chain’s guarantees with relatively small coalitions (eg. censorship attacks with much less than 50% participating)
2. Stability: the fork choice should be a good prediction of the future fork choice

As an example of (1), consider the following case:

![image](https://ethresear.ch/uploads/default/original/3X/0/1/01449aa73b3561986da48433aa0cb06f0e564ab6.svg)

Suppose the red chain consists of only malicious proposers and attesters, and is published after the fact. In the grey “chain” (really not a chain at all), the proposers are malicious, but the attesters are honest. Suppose the fraction of malicious attesters is, say, 1/4. The attacker publishes A1, waits, and then after some time reveals the chain with B1…

In this model, the attacker’s chain clearly wins in the longest chain rule. The solution to these kinds of attacks is a GHOST scoring rule (see [[2]](https://ethresear.ch/t/attestation-committee-based-full-pos-chains-version-2/2427)), which would keep increasing the weight of A1 as more honest validators attest to it, ensuring that it continues to overtake the attacker’s chain.

However, GHOST has one weakness in the context of FFG, which is lack of stability. For example, consider this case, where each box represents a checkpoint and the number inside of it is the percentage of validators voting for that checkpoint.

![image](https://ethresear.ch/uploads/default/original/3X/6/b/6bda7e4df444ebc184a9360e32ee878b02d82d28.svg)

A GHOST implementation that tries to naively replicate GHOST in PoW would add up all votes in the subtree, and the green subtree would get 111 votes relative to 96 on the yellow subtree, so the green subtree would win, even though the yellow tree is clearly much closer to getting a justified checkpoint.

One could try to change this by instead only looking at most recent votes. But this would break in a different case:

![image](https://ethresear.ch/uploads/default/original/3X/8/0/8005f4455fda86ab6f7b66d90392a4f86dbd9c84.svg)

Here, yellow would win, even though the green subtree is clearly only 2% attestations away from being justified. This is dangerous because an attacker with 2% of stake could wait for such a scenario to arise (realistically, trigger it by forcing high network latency), then wait until the opportune moment to release their attestations, suddenly flipping over the chain.

Our fork choice rule will start from the first version of GHOST above, but make one modification: instead of *adding* the votes for the checkpoints in a subtree, we take the *maximum*. The philosophy here is that if a block is justified, that implicitly justifies its ancestors as well, so the distance of a block to being justified is really the minimum of the distances of any of its descendants, and so the *proximity* to being justified is the *maximum*.

Hence, in the first example, yellow is preferred over green because max(15, 16, 65) > max(55, 56), and in the second example, green is preferred over yellow because max(65, 20) > max(15, 51).

(As a historical note, I’ll add that this exact algorithm was considered for hybrid Casper FFG, but was ultimately rejected because there was no proof that some chain closer to justification had a longer PoW chain, and epoch numbers were tied to PoW lengths, but in the latest protocol epoch numbers are tied to slots, ie. timestamps, which resolves this issue).

Within an epoch, the GHOST rule can be used to find the preferred head to improve safety against bad proposers, though from the point of view of stability it does not theoretically matter as much which fork choice rule is used inside an epoch.

It is worth noting that there *is* one weakness of this fork choice rule:

![image](https://ethresear.ch/uploads/default/original/3X/5/8/58df7a95d44431a740a6544dcd398b8ee2eab69b.svg)

Here, even though the green chain is “closer” to justification according to the fork choice rule (60 > 51), it is “further away” in practice because getting it justified would require 7% equivocation, whereas the yellow chain could be justified with no equivocation. However, this kind of scenario could only arise in a fairly extreme circumstance with either a majority attacker or very high network latency.

## Replies

**djrtwo** (2018-07-16):

In response to the weakness described at the end of your post, we can make the fork choice rule resistant to this issue by removing checkpoint weights from the max calculation if it is seen to require equivocation to justify at that height. This reduces the fork choice to max of a subtree while only considering checkpoints that can be justified without equivocation.

Although this cleans up the described degenerate case, it dirties up the accounting on what was previously a very clean fork choice rule. It would be worth considering exactly in what scenarios this degenerate case might arise before modifying the fork choice to fight it

---

**vbuterin** (2018-07-16):

We can define a “path to finality” D(c) as a triple (U, C, F), where:

- U is the number of votes that are unseen in epoch(c) that appear as votes for c
- C is the number of validators that already voted for something conflicting with c in epoch(c) that also vote for c
- F is the number of future validators that vote for c (only possible for the latest epoch)

It seems like we can reasonably disagree on how “difficult” it is for a given number of class-U, class-C and class-F votes to appear, and so we can disagree which path to finality really is “shortest”. Surely c with \frac{2}{3} - \epsilon voting for it and \frac{1}{3} + \epsilon voting for something conflicting is closer than c' with 5\% voting for it so far. But then if we replace \epsilon with \frac{1}{6} that’s no longer true. But where’s the cutoff?

---

**djrtwo** (2018-07-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> disagree on how “difficult”

Ah, you mean here a probabilistic view as to what *could* be coming. Yes, I agree that gets messy quick providing a potentially different view of the head depending on personal probability calculations.

I was proposing a solution to the narrow case of there not being enough U in D(c) to provide a path without equivocation. In practice though, throwing out branches that would require equivocation for finalization could destabilize the fork choice rule in the case that an attacker equivocates the x\% required to finalize (at the approximate cost of 3*x\% loss).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> But where’s the cutoff?

Somewhere before 1/6 ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Here, yellow would win, even though the green subtree is clearly only 2% attestations away from being justified. This is dangerous because an attacker with 2% of stake could wait for such a scenario to arise (realistically, trigger it by forcing high network latency), then wait until the opportune moment to release their attestations, suddenly flipping over the chain.

In this scenario, why are we letting an attacker add in the 2\% attestations for a checkpoint that has already passed? Should we not require justification to have to occur during the course of the epoch in question? And can we not achieve this due to the strong sense of timing in the beacon chain?

---

**vbuterin** (2018-07-17):

> In this scenario, why are we letting an attacker add in the 2% attestations for a checkpoint that has already passed? Should we not require justification to have to occur during the course of the epoch in question? And can we not achieve this due to the strong sense of timing in the beacon chain?

Ah, but what if some proposer that was previously missing from that epoch makes a proposal that includes the attestations? Then, the fork choice rule would compel the checkpoint to be accepted and everyone more recent to build on top.

I don’t think it’s possible to have a stable fork choice rule that says “reject messages that appear too late”.

---

**vbuterin** (2018-07-17):

I suppose defining “proximity to justification” as something like “percentage of validators that did not yet vote in that epoch that would need to vote to justify it” and just ignoring the possibility of voluntary equivocation could work fine in practice though.

Another possible metric is “value at risk”: for that epoch to become justified, how much money would validators have to put at risk, including opportunity cost? For every validator in U, that’s just the reward they could have gotten in another chain, and for every validator in C that’s the penalty they would have to pay. This does seem like it at least has some more philosophical footing.

Though these are optimizaitons; naive recursive proximity to justification is good enough in all non-pathological cases.

---

**jamesray1** (2018-08-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it is “further away” in practice because getting it justified would require 7% equivocation

Where does 7% come from; you have 5% in the box. Sorry, can you clarify/explain or remind us what equivocation means in this context? I think you mean that in a fork choice rule, equivocation means picking one of the most recent blocks that doesn’t have a majority vote, nor a supermajority vote for justification.

---

**vbuterin** (2018-08-17):

The 7% comes from the fact that you need 67% to justify.

---

**jamesray1** (2018-08-17):

Right, gotcha. Although I still am not exactly sure what you mean by equivocation when you say that “the yellow chain could be justified with no equivocation”.

Edit: I think that equivocation in this context means that there are two competing chains, neither of which have been justified or finalized yet.

