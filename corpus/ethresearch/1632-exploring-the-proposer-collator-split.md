---
source: ethresearch
topic_id: 1632
title: Exploring the proposer/collator split
author: benjaminion
date: "2018-04-06"
category: Sharding
tags: []
url: https://ethresear.ch/t/exploring-the-proposer-collator-split/1632
views: 11290
likes: 21
posts_count: 24
---

# Exploring the proposer/collator split

## Tl;dr

We argue that the dominant strategy encouraged by the proposer/collator distinction will simply be collators making self-proposals. Given the substantial additional protocol, engineering and security complexity introduced by the proposer/collator split, it would be expedient to abandon this distinction (for now, at least) and revise the proposed sharding roadmap accordingly.

## Background

For definitions of the roles of proposer and collator, and also the roadmap outlining the phases mentioned below, see [Sharding Phase 1 spec](https://ethresear.ch/t/sharding-phase-1-spec/1407).

A [key motivation](https://ethresear.ch/t/separating-proposing-and-confirmation-of-collations/1000) for dividing the roles of proposer and collator is that,

> the nodes participating in the transaction ordering process still need to have access to the state, and still need to perform state executions, because they need to know whether or not the transactions they accept will pay for gas.

The idea is that collators will not invest in maintaining state since they will be shuffled rapidly between shards. Instead, each shard will have proposers who maintain the state and use that information to construct collation proposals in which they “know whether or not the transactions they accept will pay for gas.”

## Economic model

Based on the quality of their proposals (i.e. the transaction fee revenue for the collation), and possibly other factors, proposers will offer their collations to the collator along with a bid amount. A [four step](https://ethresear.ch/t/alternative-fix-for-proposer-withholding-attack/1268/3) “proposer–collator” game follows, both to protect the proposers from the theft of their proposals, and to protect the collator against data withholding by proposers. The likelihood is that the collator will accept the proposal that offers the highest bid, although it is not bound to do so, and may even choose to use its own proposal (a self-proposal).

From each proposer, n, we have the equality,

B_n = T_n - c_n - ε_n

where

- B_n is the bid amount for this proposal,
- T_n is the anticipated transaction fee revenue to the proposer,
- c_n is the cost to the proposer of maintaining state, finding the optimal transaction ordering, participating in the bidding process, etc. including the proportional costs of unsuccessful bids, and
- ε_n is the proposer’s profit.

The collator is likely to select the proposal from n with the greatest B_n.

On the face of it, this looks good: use of collation space is optimised by ensuring that it is filled with high value, non-invalid transactions (maximise T_n); inefficient proposers are discouraged (minimise c_n); and, assuming the market is competitive, proposers’ profits are held in check (minimise ε_n).

One potential issue is that, since ε_n may be negative (a proposer may subsidise a proposal), it is possible for a proposer to censor transactions on a shard for arbitrary lengths of time. Eventually, the sender of a censored transaction may be able to increase the transaction fee so that a different, non-censoring proposer can win, but this is undesirable.

## Asymmetries

A collator making self-proposals has two significant advantages over the  proposers.

1. A proposer needs to bid an amount B to the collator. To minimise the risk of losing funds it needs to ensure that (on average) B
Elimination of the opportunity for proposers to censor or hide transactions.
Elimination of the wasteful use of resources by proposers all independently creating proposals of which only one is selected.
Reduction the number of actors who need to have their private keys available (and therefore vulnerable) to sign proposals and collations.

It is our hypothesis that the network will degenerate to this proposer-less situation in any case.

---

Ben Edgington, Nicolas Liochon - ConsenSys/PegaSys

## Replies

**jamesray1** (2018-04-06):

I think we need to ensure that we maintain or improve decentralization as we make changes to Ethereum. So while your critique is concerning, I am wary about removing proposers (although with your model they will degenerate out anyway) while doing nothing else to reduce centralization risk and increase the probability of decentralization. Additionally it’s not fully clear whether joint collator-proposers can not maintain the state.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> The collator does not need to maintain state for this, it can consult executors to check past outcomes on a particular shard.

Yes but then it has also been suggested by [@hwwhww](/u/hwwhww) that collators are likely to be executors. They collate the transactions so can execute them at the same time (and have the extra incentive to do so). So combined, you have collator-proposer-executors, which is even more of a centralization risk/tendency.

AIUI in phase 3 we aren’t going to have complete statelessness, rather there will be state minimization.

At any rate, I may halt development and engage in further research to address these issues and we find a convincing way to scale Ethereum while maintaining or improving decentralization.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> inefficient collators are discouraged

I think you mean proposers (which includes collators also acting as proposers).

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> Is it possible for a proposer to to make

to make

---

**vbuterin** (2018-04-06):

It’s worth noting that some of our latest thinking (not yet written up but will be soon) involves merging proposers and executors and having them be randomly sampled per shard; collators are replaced by “notaries” which are globally sampled, which simply express approval or disapproval of collations without containing collation data themselves. So this whole problem could simply end up not mattering.

---

**jamesray1** (2018-04-06):

Well I would certainly like to see more detail on that, and if the role of collators are going to change and that changes the phase 1 spec, so we will need to rewrite the implementations that we have been developing. Then again, maybe the phase 1 spec would not change much as it is now with the role you outlined.

---

**benjaminion** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> I am wary about removing proposers

Our expectation is that they will remove themselves since collators will basically ignore them. If we really think the proposer–collator model is valuable, then it needs to be incentivised somehow (e.g. by punishing the inclusion of spam/invalid transactions, for example, if we can even define what invalid means in the new regime).

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> So combined, you have collator-proposer-executors

Which is no worse than the situation we are in on Mainnet today.

Thanks for the typos. Will correct!

---

**jamesray1** (2018-04-06):

I realize that proposers would degenerate anyway under your assumptions which seem reasonable, although it’s hard to assess how they would hold in practice, and edited my comment to make a note of that. But having collator-proposer-executors in a sharding context is not the same as the current situation, since we are trying to remove the need for a node to have to process every transaction. What’s the point of sharding if we don’t remove the need to do that?

---

**prestonvanloon** (2018-04-06):

Wouldn’t it be too risky for a self-selecting collator to *not* verify transactions prior to including them in a collator? It would be trivial for an attack to flood this collator with junk transactions reducing T_n to zero.

It would also be too expensive for a self-selecting collator to maintain state on all shards for the infrequent chance that they are a selected as a collator for any shard. The self-selecting collator would have 101x c_n of a single proposer.

---

**benjaminion** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/prestonvanloon/48/232_2.png) prestonvanloon:

> Wouldn’t it be too risky for a self-selecting collator to not verify transactions prior to including them in a collator?

Yes, as per the “High-spam regime” section, this may be the best argument for having the proposer/collator split. Though, note that the risk to the collator is only opportunity cost. It does not lose funds (under the current sharding proposals), and also gets the collation reward.  If the collator has either (a) relatively lightweight heuristics for identifying spam Txs without knowledge of state (think email spam filters), or (b) access to a stateless client, then it can still likely do better than relying on proposers’s bids.

---

**hwwhww** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Yes but then it has also been suggested by @hwwang that collators are likely to be executors.

I think what I said is that the *proposers* are likely to be executors.

---

**jamesray1** (2018-04-06):

Ah OK, sorry for misquoting you. That makes sense, since they would execute the transactions anyway to verify that they are valid.

---

**prestonvanloon** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> If the collator has either (a) relatively lightweight heuristics for identifying spam Txs without knowledge of state (think email spam filters),

Email spam filters have large datasets with labelled data. How will this be provided without knowing state data?

How would the collator have any sense of precision or accuracy in spam filtering?

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> or (b) access to a stateless client, then it can still likely do better than relying on proposers’s bids.

How so?

---

**MaxC** (2018-04-06):

Hi Ben,

What do you think of Vitalik’s post? It seems one could keep the validator’s fee fixed, and get rid of the bidding process altogether by just rotating proposers. That seems to align incentives (as on average proposers will not fill the state with junk transactions), and obviates the need for a validator to keep any global state.

I wonder if you could even generate schemes that decommission proposers who turn up with low value transactions compared to the average proposal value.

---

**MaxC** (2018-04-06):

I think a good long term justification for the split between collators and proposers is that if you had really large GB sized blocks, just about the only thing a collator could do with such a huge block in such a short period of time is check for availability. Even access list checking would take too long.

---

**benjaminion** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/prestonvanloon/48/232_2.png) prestonvanloon:

> How would the collator have any sense of precision or accuracy in spam filtering?

Yes, admittedly, this is hand-wavy. The main point is that this regime is currently planned to be temporary (where the proposer has access to full state, and the collator doesn’t, so they are on an unequal footing).  When stateless clients appear, they move to a more equal footing, hence…

![](https://ethresear.ch/user_avatar/ethresear.ch/prestonvanloon/48/232_2.png) prestonvanloon:

> or (b) access to a stateless client, then it can still likely do better than relying on proposers’s bids.
>
>
> How so?

This is covered in the “High-spam regimes and stateless clients” section in the article.

---

**benjaminion** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> What do you think of Vitalik’s post?

The one in this thread?  I’d like to see more detail, especially around how data availability is guaranteed if there is only one proposer per period. But sounds interesting.

---

**ChosunOne** (2018-04-06):

I second this suggestion.  There seems to be little reason to have a separate proposer section when all it is really doing is just collecting blobs into collations.  It makes sense to separate the tasks *logically*, but if collators don’t need to store the entire state of each shard then I don’t really see the need to encourage the tasks to be distributed *physically*.  In my opinion a Proposer-Collator-Executor is not really so bad given that the performance requirements of such nodes are generally accessible to most laptops (running Casper).

Is the concern that running a proposer and collator simultaneously would be too difficult to achieve a large number of nodes?

---

**terence** (2018-04-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> Is the concern that running a proposer and collator simultaneously would be too difficult to achieve a large number of nodes?

I would certainly think so. As a single self-electing collector will need to cover 101x proposer’s performance requirement right?

---

**ChosunOne** (2018-04-06):

> I would certainly think so. As a single self-electing collector will need to cover 101x proposer’s performance requirement right?

I don’t see why that would be the case.  At any given period a collator is only concerned with one shard, and only has to deal with proposers of that shard.  It doesn’t make sense to collect proposals from other shards than the one you are assigned to.  Since you have the lookahead period, you can get ready for that shard ahead of time.  Yes there are some storage requirements (such as the state of the assigned shard), but nothing I think would be drastic in changing the number of participating nodes.

Could you elaborate on that figure of 101x?

---

**prestonvanloon** (2018-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/chosunone/48/732_2.png) ChosunOne:

> Could you elaborate on that figure of 101x?

This assumes the proposer has to maintain the state for a given shard. A collator has no idea which shard it will be selected to commit a collation so it must maintain the state for all 100 shards. A collator must do this to ensure that the transactions would execute properly before including them in the collation body or they risk including a junk transaction and forfeit some of T_n. We also must assume that it would not be possible to download the entire state of a shard within a lookahead period (how long does it take to sync today? 8 hours?) so the collator must maintain state for each shard all the time.

However, Ben claims that the proposer/collator can determine whether a given transaction will execute properly without maintaining state by way of a stateless client. If this is a reliable method then the self-proposing collator’s cost would be a low constant given that the stateless client paradigm can be trusted enough to validate transactions.

![](https://ethresear.ch/user_avatar/ethresear.ch/benjaminion/48/612_2.png) benjaminion:

> If the collator has either (a) relatively lightweight heuristics for identifying spam Txs without knowledge of state (think email spam filters), or (b) access to a stateless client, then it can still likely do better than relying on proposers’s bids.

So either the self-proposing collator’s cost will be either 101 times that of a proposer or a negligible low fixed cost by using a stateless client.

---

**vbuterin** (2018-04-07):

Link to newer thoughts: [A general framework of overhead and finality time in sharding, and a proposal](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638)

---

**vbuterin** (2018-04-07):

> One potential issue is that, since ε_n may be negative (a proposer may subsidise a proposal), it is possible for a proposer to censor transactions on a shard for arbitrary lengths of time.

I am not convinced that this is an issue. Consider that in the current system, it is possible to simply send 8 million gas transactions with a high gasprice, which seems like it would have a similar effect.

> The non-full shard

Agree that in these cases state is not required for self-proposals.

> for example, using the order in which transactions appeared in the shard’s transaction pool.

This is actually an interesting hidden insight: you can use nodes in the network to filter out non-fee-paying transactions for you for free, and use this as a source of transaction data. Though this technique is likely to be quite imperfect.

> In Phase 1 sharding, there is no concept of a “spam” or invalid transaction

To clarify, there is never a concept of an invalid transaction at the collation finalization layer.

> This model degenerates either to there being only one super-efficient (or malicious) proposer per shard

Not necessarily. I would argue that if there is only one proposer, then that proposer gets the incentive to start rent-seeking (increasing \epsilon), and that by itself creates the incentive for more proposers to undercut. It seems like the Nash equilibrium is that there is always some nonzero probability for the dominant proposer to lose any particular bidding round, which means multiple proposers. Also, there is the possibility of proposers that represent specific applications, as well as the possibility of proposers that acquire specialized domain knowledge about fee payment in specific applications (eg. accepting fees in E-DOGE).

It’s additionally worth pointing out that if the dominant proposer tries censoring, then that by itself confers an economic advantage to all of the other proposers.

I would be interested to hear what you think about the proposal/notarization separation model that I outline in the newer post I linked ([A general framework of overhead and finality time in sharding, and a proposal](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638)).


*(3 more replies not shown)*
