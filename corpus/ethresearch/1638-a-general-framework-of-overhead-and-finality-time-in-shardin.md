---
source: ethresearch
topic_id: 1638
title: A general framework of overhead and finality time in sharding, and a proposal
author: vbuterin
date: "2018-04-07"
category: Sharding
tags: []
url: https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638
views: 7428
likes: 15
posts_count: 17
---

# A general framework of overhead and finality time in sharding, and a proposal

In general, a “phase 4” tightly coupled sharding chain works in the following way:

1. Collations get produced (via some mechanism)
2. Some set (“committee”) of M randomly sampled notaries verifies the data availability of the collations, and somehow votes that the collations are available.
3. The collation header plus committee votes backing it up get included in the main chain (the main chain validator verifies the votes, and may also verify a data availability proof of the collation itself), at which point the main chain and that collation are “tightly coupled”: if, for some reason, the collation is unavailable despite the votes being there, then that entire main chain block must be rejected by clients.

So the pipeline is:

![image](https://ethresear.ch/uploads/default/original/3X/8/3/83856925bba10a4be4b62a2d0b49a49b739be611.svg)

In phases 1-3, we lack tight coupling, but instead we can replace this with any kind of in-protocol mechanism where a majority of validators can roll back a chain that contains a block that they deem to be unavailable.

Consider in the abstract the following variables:

- N: the number of shards
- M: the size of a random sample
- T: time between collations on each shard (ie. block time in the shards)
- C: the size of a collation
- R: the number of distinct collations that a notary message votes for
- F: time to internal finality (ie. tight coupling)

In the sharding 1.1 spec, these variables are as follows:

- N: 100
- M: ~25
- T: 70 seconds
- C: 1 MB
- R: ~25
- F: 70 seconds * ~25 ~= 30 minutes

Note that the sharding 1.1 spec does not have an explicit “committee size”, but it is there implicitly, as it’s expected that when a collator gets assigned to a shard, they only check the last M collations in the chain, with an attempt to cryptoeconomically enforce a hard minimum of 25. Hence, if a collation gets 25 confirmations, it does not really get checked anymore, so M = 25. R = 25 because [forking is voting](https://ethresear.ch/t/in-favor-of-forkfulness/1225); the act of making a collation on top of a head signifies approval of the head and its 25 most recent ancestors. Finality is subjective, but since there is no further verification after 25 collations, saying that it comes after 25 periods is as reasonable as anything else.

But there are forms of voting other than forking; for example, collations could all be independent of each other, except that each collation could contain a bit field expressing which of the 25 most recent collations that collator thinks are available. We could have a scheme where there is no forking of any kind; for a collation to even go into the main chain, it must already come with 25 votes supporting it, and at that point it’s finalized. One goal of this post will be to try to analyze all schemes of this kind.

We can calculate the main chain overhead as:

\frac{N * M}{T * R}

This is justified as follows:

- N is the number of shards, and M is the committee size per shard. For every collation header there would thus be M signatures, so with N collation headers that’s N * M on-chain overhead.
- The above happens once every T seconds.
- The above can be cut down if one signature represents multiple things, hence we can add R into the denominator.

Another important kind of overhead is *notary burst overhead*: when a notary gets called to vote on one or more collations, they have some deadline within which they have to submit a signature, and they need to download all the data to check availability within that time. We can calculate notary burst overhead as:

\frac{C * R}{F}

This can be justified as follows:

- C is the size of each collation. R is the number of collations they have to check.
- Internal finality (ie. tight coupling) requires seeing the notary signatures, so whatever the length of time notaries are given to download the data, internal finality requires waiting for at least that.

Within this framework, we can calculate the efficiency of a few schemes:

- The 1.1 forkful model: main chain overhead = \frac{100 * 25}{70 * 25} \approx 1.41, collator burst overhead = \frac{10^6 * 25}{1750} \approx 14286 bytes per second. Notice that in reality, the forkful model is actually much less efficient than this ideal because the lookahead is only 3 periods and not 25, so collator burst overhead is \frac{10^6 * 25}{210} \approx 119047 bytes per second.
- Increase collation block time to 1750 seconds, collation size to 25 MB, require collations to be ratified by committee or else rejected immediately. Main chain overhead = \frac{100 * 25}{1750} \approx 1.41, collator burst overhead = \frac{25 * 10^6}{1750} \approx 14286 bytes per second.

Notice that the two models seem to give exactly the same costs, and exactly the same finality time (1750 seconds), and the second is much simpler. So why even consider the first? The answer is: a model based on smaller collation sizes gives faster indication of partial confirmation. 25 confirmations is as final as it gets, but even 3 confirmations usually gives a lot of confidence that a transaction will be included for good.

If we look at the equations for calculating overhead, we see a few clear tradeoffs:

- The 1:1 tradeoff for main chain overhead versus notary overhead. You can halve main chain overhead at the cost of doubling notary overhead by doubling R.
- The 1:1 tradeoff between notary burst overhead and finality time. You can halve notary burst overhead by doubling finality time (or alternatively, you can shift the savings to main chain overhead by also doubling R).
- You can always reduce both C and T by an equal proportion, and cancel out the impact on the main chain and notary burst overhead by increasing R by the same proportion.

This more generally shows that we can use techniques to make one signature mean multiple things to reduce T, and try to provide faster partial information. But are there techniques other than forking to do it, and are they better?

First of all, let us switch from forking to a model where collation proposal and notarization are separate functions; that is, every period, a collation header gets proposed, but then a separate set of notaries engages in voting to finalize them. Collation proposers could, for instance, be randomly sampled from a set that exists within a particular shard, thereby allowing them to hold the state of that shard, and removing the need for [collator-proposer games](https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000). Let us also switch from a forking-as-voting model to an explicit model: every period, k notaries are selected per shard, and these notaries must attempt to download the last \frac{M}{k} collations and deliver a verdict on the availability of each through a bitfield (ie. a string like 11110111001111111011101). After a collation is created, after p periods, there would be p * k votes on the collation, delivering evidence of partial confirmation. This allows us to move away from *one* unit of voting per period per shard, and instead opens up the full parameter space between k = 1 (similar to the 1.1 forkful model) and k = M (a collation gets ratified within one round, and ratification is done before the next collation is created).

Notarizations can be cryptoeconomic: you get more rewards by voting 1 on more collations that ultimately get accepted, but if you vote for a collation you are responsible for providing any specific chunk of the collation body is challenged, and if you can’t do that you lose your deposit.

To achieve optimally low notary burst overhead, the lookahead needs to be equal to \frac{M}{k}, so notaries can start downloading and checking collations as they come. However, there is a clever way to improve security of this scheme against semi-adaptive adversaries: instead of checking availability *vertically* across a range of period numbers on one shard, notaries check *diagonally*, checking a collation from a different shard in each period. The randomness that determines which shard a notary checks during each period can be delayed until that period, achieving zero lookahead transparency, making the scheme secure under honest majority except for all but the most adaptive adversaries who can launch attacks on specific nodes within a single period.

To summarize, in this kind of diagonal scheme, a notary would be called upon during period p, and required to verify a collation from some shard during every period from p to p+\frac{M}{k}. During the last period, the notary would submit a signature that contains that notary’s opinion on every collation within that range as a bitfield. This allows us to:

- Remove proposer/collator separation, as its function is now replaced by proposer/notary separation/
- Achieve even higher notary burst overhead efficiency (or alternatively, shift some of the gains into increasing M from 25 to a safer 100-200)
- Make it known which notaries are active in general \frac{M}{k} shards in advance, but not make it known which shard a given notary will be notarizing in some period until that period begins.
- Avoid all concerns about using transaction fees or bids to bribe collators to make collations off the main chain, as the voting function is done by notaries
- Remove the complexity of having a “forking chain inside a forking chain”
- Still have basically the same main chain overhead as before
- Still have the same level of information about partial confirmations as before

## Replies

**jamesray1** (2018-04-07):

In the draft [Sharding phase 1 spec (RETIRED)](https://ethresear.ch/t/sharding-phase-1-spec/1407) tight coupling isn’t until phase 5.

---

**jamesray1** (2018-04-07):

Don’t read this comment! I need to read some of the linked to posts, recursively if need be. I’m mostly just summarizing/rehashing what you said for understanding.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Collations get produced (via some mechanism)
> Some set (“committee”) of MM randomly sampled notaries verifies the data availability of the collations, and somehow votes that the collations are available.

So without collators, having notaries and proposers instead, one way for these two to work in more detail is:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> First of all, let us switch from forking to a model where collation proposal and notarization are separate functions; that is, every period, a collation header gets proposed, but then a separate set of notaries engages in voting to finalize them. Collation proposers could, for instance, be randomly sampled from a set that exists within a particular shard, thereby allowing them to hold the state of that shard, and removing the need for collator-proposer games. Let us also switch from a forking-as-voting model to an explicit model: every period, kk notaries are selected per shard, and these notaries must attempt to download the last  \frac{M}{k} collations and deliver a verdict on the availability of each through a bitfield (ie. a string like 11110111001111111011101). After a collation is created, after p periods, there would be p∗k votes on the collation, delivering evidence of partial confirmation. This allows us to move away from one unit of voting per period per shard, and instead opens up the full parameter space between k=1 (similar to the 1.1 forkful model) and k=M (a collation gets ratified within one round, and ratification is done before the next collation is created).
>
>
> Notarizations can be cryptoeconomic: you get more rewards by voting 1 on more collations that ultimately get accepted, but if you vote for a collation you are responsible for providing any specific chunk of the collation body is challenged, and if you can’t do that you lose your deposit.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Collation proposers could, for instance, be randomly sampled from a set that exists within a particular shard, thereby allowing them to hold the state of that shard, and removing the need for collator-proposer games.

Yes, this is something that occurred to me, I think I touched on it in the P1SS spec comments. it would be good to reduce complexity.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> deliver a verdict on the availability of each through a bitfield (ie. a string like 11110111001111111011101)

Then later you have:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> During the last period, the notary would submit a signature that contains that notary’s opinion on every collation within that range as a bitfield.

So it sounds like each bit in the bitfield represents a collation. It would be interesting to develop that, but it seems not too hard to implement.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> However, there is a clever way to improve security of this scheme against semi-adaptive adversaries: instead of checking availability vertically across a range of period numbers on one shard, notaries check diagonally, checking a collation from a different shard in each period. The randomness that determines which shard a notary checks during each period can be delayed until that period, achieving zero lookahead transparency, making the scheme secure under honest majority except for all but the most adaptive adversaries who can launch attacks on specific nodes within a single period.
>
>
> To summarize, in this kind of diagonal scheme, a notary would be called upon during period p, and required to verify a collation from some shard during every period from p to p+\frac{M}{k}. During the last period, the notary would submit a signature that contains that notary’s opinion on every collation within that range as a bitfield.

Sounds good. It would add more complexity to implementation, e.g. the source of the randomness, notaries being registered in each shard, listening to the SMC during every period to see what shard they’re assigned to, downloading the collation for that period, somehow verifies the data availability e.g. with Reid Solomon codes, ‘submits a signature on the collation at the end of the lookahead periods that contains that notary’s opinion on every collation within that range as a bitfield’ (presumably this opinion could be a boolean where true = valid and available and false is otherwise).

Presumably multiple notaries are assigned to every shard in every period, so that there are multiple confirmations, where they then would randomly shuffle between all shards, and don’t need to store the state of any shard. They don’t need to store the state so you would not need to have a separate registry of notaries for each shard, but would still have that scheme for proposers, where proposers can store the state of the ones they’re registered in. Or perhaps you don’t need to have multiple notaries for each shard for each period, but you would increase the time to internal finality for votes to accumulate over a longer period before “the main chain validator verifies the votes, and may also verify a data availability proof”.

In the mean time with phase 1, it seems that we still need to have a collator-proposer game, or a viable model. (There’s a reasonable critique of the collator-proposer game here: [Exploring the proposer/collator split - #21 by vbuterin](http://ethresear.ch/t/exploring-the-proposer-collator-split/1632/21)) This model seemingly won’t work with phase 1 since we have no execution, so we can’t couple with the main chain, which does have execution; and more importantly because proposers need to know whether transactions are valid by executing them.

---

**jamesray1** (2018-04-07):

I think I need to re-evaluate or halt development until we have a clearer understanding of viability for an initial implementation in phase 1. In phase 1 proposers may degenerate out of the system with collators as self-proposers. It seems like we may waste a lot of time if we implement phase 1 and have to re-write a lot of it. This proposal doesn’t seem to address how to do that.

Unless we can figure out a viable model without execution, perhaps we should work on developing one with execution. I will consider implementation without execution a topic of ongoing research until I am convinced that one is viable.

---

**MaxC** (2018-04-07):

Nice, I had also been thinking that adopting a fork-free model with notaries would be the way to go for sharding, and have been writing up my proposals. The reason that dfinity, Zilliqa et al can achieve finality so quickly is that they are using randomly sampled committees to vote on and notarise/finalise blocks.

In Zilliqa,  for instance, they show that with a committee of size 400, if fewer than 25% of nodes are bad, they almost certainly ensure an honest majority of 2/3 within the committee, which means blocks are very likely to be valid and almost no forking should occur.

---

**jamesray1** (2018-04-07):

And this is with execution, right? In phase 1 sharding we have no execution, I am yet to see a viable model for that. I do think that abstraction of execution is useful, but it seems that more research is needed.

---

**MaxC** (2018-04-07):

In Zilliqa nodes vote on execution, but that is a flaw as voting nodes spend too long in each shard (is it a week?), and would be for Ethereum under a similar scheme since it would be costly for the collators/validators to acquire new state.

This is also a problem for dfinity but in a different way. Notaries are only attesting to data availability in dfinity, so they are quick. However dfinity’s problem is that the random beacon groups that generate the randomness aren’t shuffled quickly enough.

I think the question on whether collators could be really just be validators executing state is a nuanced one.

(1)If block sizes are relatively small, and we are in the stateless client model, then yes it could be done.

(2) long term if you want humungous blocks per shard, then they can’t do any form of execution.

So long term, I kinda agree with execution abstraction, but a lot more research needs to be done and there may be ways to improve/ modify trubit. I am working on one idea currently.

---

**MaxC** (2018-04-07):

^^ Please see above. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**jamesray1** (2018-04-07):

What area are you working on? ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**MaxC** (2018-04-07):

Trying to reduce the number of rounds of interactive verification. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**vbuterin** (2018-04-07):

> Unless we can figure out a viable model without execution, perhaps we should work on developing one with execution. I will consider implementation without execution a topic of ongoing research until I am convinced that one is viable.

Not sure I understand this. A model without execution is strictly easier than a model with execution.

I would recommend at this point continuing to build at least:

- The capability of having 100 separate shard p2p networks, and building and sending collations across those networks
- The ability to read logs emitted by an SMC
- The ability to send transactions that call an addHeader function of the SMC
- The ability for a client to maintain a database of which collation roots it has downloaded the full body for
- The ability of a validator to (i) log in, (ii) detect that it has been randomly sampled, switch to the right p2p network, and start doing stuff, (iii) log out

These things are mostly not affected by protocol changes.

---

**jamesray1** (2018-04-08):

I have a few concerns with two directions that could be taken without execution. Actors that only participate as proposers would seemingly degenerate, leaving only collator-proposers. Collator-proposers seemingly have a centralization risk. There may be asymmetries between a supercomputer that stores all the state of all shards and acts as a proposer on all shards, and is pseudorandomly shuffled as a collator between shards; vs a collator-proposer that acts as a proposer on one or a subset of shards. This proposed model in phase 5 with tightly coupled sharding where there are no collators, only notaries and proposers, would require re-work between 1 and 5. However having notaries and proposers in phase 1 seems infeasible without execution.

But thanks for the recommendations, that gives us something useful to work with less concern that we are expending time on something that will have to be substantially rewritten.

At any rate, AIUI we can only link to the main net when we get to phase 3. So limitations with phase 1 are then less concerning if it’s only a testnet.

---

**vbuterin** (2018-04-08):

> Actors that only participate as proposers would seemingly degenerate, leaving only collator-proposers.

Why?

---

**jannikluhn** (2018-04-08):

First of all, I like this approach of describing the protocol as general as possible and then just choosing an optimal parametrization. Reminds me very distantly of the Casper CBC paper ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

Two questions:

> the main chain validator verifies the votes, and may also verify a data availability proof of the collation itself

What’s the point of having both notary votes and availability proofs? Just for early partial confirmation?

And what happens if proof and votes disagree?

> every period, k notaries are selected per shard, and these notaries must attempt to download the last Mk collations and deliver a verdict on the availability of each through a bitfield (ie. a string like 11110111001111111011101).

Does that mean that a collation can be included in the chain, but at the same time be considered unavailable? Sounds a bit funny, although I can’t see a problem with it so far.

---

**jamesray1** (2018-04-08):

As per [Exploring the proposer/collator split](https://ethresear.ch/t/exploring-the-proposer-collator-split/1632/22). OK so maybe per your arguments there the centralization risk is low. But it seems like proposer-only agents would degenerate as there are asymmetries between collator-proposers and only-proposers.

---

**vbuterin** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> What’s the point of having both notary votes and availability proofs? Just for early partial confirmation?

As a double-check. With both checks, the system is secure if either (i) the honest majority model holds, or (ii) the availability proof mechanism works.

> And what happens if proof and votes disagree?

Post-tight-coupling, a node would reject any main chain blocks that have internally finalized collations that that node sees as unavailable.

> Does that mean that a collation can be included in the chain, but at the same time be considered unavailable?

A collation header can get included in the chain, but the collation header is not considered “internally finalized in the chain” (think: “accepted in the chain”; perhaps that’s better terminology) until the full notarization happens. The intention is that if the honest majority model holds, then unavailable collations would (basically) never pass notarization.

---

**jamesray1** (2018-04-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> A collation header can get included in the chain, but the collation header is not considered “internally finalized in the chain” (think: “accepted in the chain”; perhaps that’s better terminology) until the full notarization happens.

Not being accepted in the chain may imply that it is not included in the chain, so included but not internally finalized sounds more accurate.

