---
source: ethresearch
topic_id: 2053
title: Network latency based clocks and their limits
author: vbuterin
date: "2018-05-22"
category: Sharding
tags: []
url: https://ethresear.ch/t/network-latency-based-clocks-and-their-limits/2053
views: 3408
likes: 1
posts_count: 10
---

# Network latency based clocks and their limits

One consistently thorny topic in blockchain design is timing. All blockchains so far rely on timestamps provided by nodes in blocks in order to calibrate their blockchain’s block time, whether directly (eg. as in PoS schemes that explicitly say “a block at slot 1045 can be created at time 1457284250…1457284259”), or indirectly (eg. like in PoW difficulty adjustment). One possible scheme for going without timestamps is a clock that depends directly on network latency. The blockchain would not even care about timestamps; instead, the clock would be a logical clock whose height keeps incrementing, and every time the height enters a new range (eg. 3570…3579), nodes in the PoS chain would be allowed to create a new block.

However, there is an obvious limit to the possibility of such a clock: if the clock can survive with only portion \alpha of the network online, then an attacker with an \alpha share of consensus power can cheat the clock by running the algorithm locally between its own nodes. The good news: it’s not that hard to make a near-optimal clock for any \alpha. Here’s the algorithm:

- The genesis 0x000000 is a “signed message”, with sequence number 0 (this is an inductive base case)
- Anyone can create an “unsigned message”, which points to a (signed message) parent; its sequence number is the parent’s sequence number plus 1
- The hash of that unsigned message identifies a random sample of M validators (the closer M is to infinity, the better, but the more overhead)
- A signed message can be created by combining an unsigned message with signatures from \alpha * M of those M validators

The current clock value is simply the highest seen sequence number. Note that we do not care about the specific chain, only the height, so reversions and “51% attacks” are not an issue.

For efficiency, each random sample signature could include a list of all unsigned messages that it has seen, and inefficiency could be further capped by specifically specifying a smaller sample of validators which are the only ones allowed to make unsigned messages on top of a given parent. This could potentially be made even more efficient and leaderless through some kind of fancy DAG algorithm, though it may not be worth the added complexity.

## Replies

**jamesray1** (2018-05-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The hash of that unsigned message identifies a random sample of M validators (the closer M is to infinity, the better, but the more overhead)

How would that work, exactly? I think you mean that the hash is used as a source of randomness to identify a random sample of M validators.

---

**lithp** (2018-05-23):

This is a cool idea. You can only increase the depth by sending the message to at least  \alpha * M  nodes, so a signed message at some depth  d  is proof that time has passed since the signed message at depth  d - 1  was created.

**It sounds like you’re making some kind of “law of large numbers” assumption?**

You’re assuming that if a bunch of nodes are all gossiping to each other, the amount of time it takes a message to reach \alpha*M of them is roughly constant as time passes? I’m not sure that’s true! And I’m not sure how a system which eschewed timestamps could keep accurate time without that assumption.

It’s especially not true in an adversarial environment: An attacker controlling less than \alpha could still introduce jitter by sometimes running its validators locally to speed that round up and sometimes not running at all, to slow the round down.

**I think you need to use something like BLS threshold signatures to prevent attacks**

BLS threshold signatures have the nice property that no matter which subset of M signs the message you’ll always get the same signature. Let me be careful with my symbols: say \alpha *M is the threshold, I’ll call \beta the proportion of the network which the attacker controls. I think that even when \alpha < \beta you’re still safe. The attacker might sometimes get lucky and have rounds where she can run everything locally but the outcome of those rounds is predetermined, she’ll be forced to give up control.

(you still have to be careful, if \beta > M the attacker will sometimes get lucky and have the option of halting the clock by not signing)

Schemes which result in each message having a different signature depending on which subset of nodes signs them are dangerous because they might allow an attacker with a large number of nodes to grind through candidate messages and only release ones which allow her to sign the next message; by doing so she can run the scheme locally and quickly increase the depth.

**This part makes me afraid that I’m entirely misunderstanding you:**

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> For efficiency, each random sample signature could include a list of all unsigned messages that it has seen

How does that make this more efficient?

---

**vbuterin** (2018-05-23):

> You’re assuming that if a bunch of nodes are all gossiping to each other, the amount of time it takes a message to reach \alpha * M of them is roughly constant as time passes? I’m not sure that’s true! And I’m not sure how a system which eschewed timestamps could keep accurate time without that assumption.

The point is not to keep accurate time. The point is to create a fake “clock” that tells the network when it’s ok to create new blocks, or how to adjust difficulty. It could be used with a PoW or PoS chain. And it’s actually a good thing that it adjusts to changes in network latency.

> BLS threshold signatures the nice property that no matter which subset of M signs the message you’ll always get the same signature.

I agree that threshold sigs do make it harder to cheat by attempting to make many different subsets and pick a favorable one; that said, it’s only a marginal improvement, even without BLS sigs you can compensate by just increasing M somewhat.

> How does that make this more efficient?

What if there is a really large number of children after some parent (because anyone can make a child)? Then you’ll have everyone trying to sign everything, clogging up the network. The efficiency improvements I suggested both serve to mitigate this by reducing the number of things that need to be signed.

---

**MicahZoltu** (2018-05-23):

I think calling it a metronome instead of a clock would more simply get your point across.  I also couldn’t figure out how this resulted in a clock.

---

**vbuterin** (2018-05-23):

I was thinking of: https://en.wikipedia.org/wiki/Logical_clock

---

**MicahZoltu** (2018-05-23):

I *think* Logical clocks are only for ordering, not for pacing.  If I understand you correctly, you want a solution to pacing, as ordering can be solved if you can first solve for pacing (and some other primatives).

---

**kladkogex** (2018-05-23):

Believe it or not this is Hashgraph ![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)![:joy:](https://ethresear.ch/images/emoji/facebook_messenger/joy.png?v=12)

> The hash of that unsigned message identifies a random sample of
> M validators (the closer M is to infinity, the better, but the more overhead)

What does prevent one from trying a message candidate many times until a favorable set of validators is derived (all bad guys) ?)))

---

**ghasshee** (2018-05-24):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png)

      [Network latency based clocks and their limits](https://ethresear.ch/t/network-latency-based-clocks-and-their-limits/2053/8) [Sharding](/c/sharding/6)




> Believe it or not this is Hashgraph
>
> The hash of that unsigned message identifies a random sample of
> M validators (the closer M is to infinity, the better, but the more overhead)
>
> What does prevent one from trying a message candidate many times until a favorable set of validators is derived (all bad guys) ?)))

How did you calculate the price of the incentive with which the bad validators cheat?

If validators cheated, validators would be punished.

With finalization is it possible ??

---

**lithp** (2018-05-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The point is not to keep accurate time. The point is to create a fake “clock” that tells the network when it’s ok to create new blocks, or how to adjust difficulty. It could be used with a PoW or PoS chain. And it’s actually a good thing that it adjusts to changes in network latency.

ooo, I understand now, this is cool. If you want to set a high block rate but don’t know much about the network before it launches you have to pick conservatively or else you’ll have a ton of orphans. **With this clock you can say: “whatever the block propagation time is, you’re only allowed to make a new block every three of those”** and then start building blocks as fast as the network will support it.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The efficiency improvements I suggested both serve to mitigate this by reducing the number of things that need to be signed.

I understood as much from “inefficiency could be further capped by specifically specifying a smaller sample of validators which are the only ones allowed to make unsigned messages on top of a given parent”, but I’m still unsure what “each random sample signature could include a list of all unsigned messages that it has seen” does for you.

Maybe you mean that the one signature actually signs many messages at once?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This could potentially be made even more efficient and leaderless through some kind of fancy DAG algorithm, though it may not be worth the added complexity.

I think you don’t need any of this complexity if you use BLS sigs ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Each node can look at the last signed message and know whether it’s allowed to sign the next one. You’ll have up to M signature shares which are gossiped. Any node with  \alpha*M  of them can build the next signed message and start working with it.

I am assuming that the messages are deterministic. Something like: `[depth hash-of-last-signed-message]`

