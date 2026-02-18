---
source: ethresearch
topic_id: 5647
title: State Providers, Relayers - Bring Back the Mempool
author: villanuevawill
date: "2019-06-24"
category: Sharded Execution
tags: [fee-market]
url: https://ethresear.ch/t/state-providers-relayers-bring-back-the-mempool/5647
views: 6503
likes: 7
posts_count: 11
---

# State Providers, Relayers - Bring Back the Mempool

# Prior Discussions

[@matt](/u/matt) : [An Optimistic Generic Gas Market Executor for Phase 2](https://ethresear.ch/t/an-optimistic-generic-gas-market-executor-for-phase-2/5429/2)

[@vbuterin](/u/vbuterin): [Phase 2 Proposal 2](https://notes.ethereum.org/s/Bkoaj4xpN)

[@vbuterin](/u/vbuterin): [One fee market EE to rule them all](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608)

# Background

To give credence to this discussion, we need a good, consolidated summary on the background of the fee market discussion for eth 2.

## First Proposal

The first iteration looked similar to the following:

[![Relayer%20Diagram](https://ethresear.ch/uploads/default/optimized/2X/b/bd7e8f34af53ca1bdf0fbfa8a45d1b228377c58a_2_690x220.png)Relayer%20Diagram1652×528 17.9 KB](https://ethresear.ch/uploads/default/bd7e8f34af53ca1bdf0fbfa8a45d1b228377c58a)

A user would submit a transaction to a `relayer`. A `relayer` would be responsible for adding witness data in a stateless system and collect a proposed block of transactions. In this system, transaction fees would be paid directly to the `relayer`. The `relayer` would then offer a flat fee, `F` to the block producer to publish its block.

This system introduced a number of issues. To summarize:

- A JMRS scheme would need to be introduced - Optimised proposal commitment scheme.

This adds significant implementation complexity and introduces other incentive questions.
- This scheme assumes only one relayer is awarded per execution environment which essentially strengthens the relay market as a centralization risk.

A number of asymmetries introduced. I summarize below, but please read the post by [@benjaminion](/u/benjaminion) here for a detailed analysis: [Exploring the proposer/collator split](https://ethresear.ch/t/exploring-the-proposer-collator-split/1632).

- Depending on the market around the flat fee offered from relayers, a block producer may be incentivized to be its own relayer and pick transactions randomly without maintaining full state.
- Malicious relayers can attack an entire block by offering a high fee.

Elegant POS is throttled by the relay market’s cheapest computation, cheapest hardware approach.

- Relayers with low cost hardware and computation will have an advantage on the lowest fee. This could lead to a cartel of relayers that own the relay market and can censor transactions at will.

The original rationale behind the relay market was to manage witness/state data in a stateless system and provide incentives for maintaining state. However, it introduced a number of issues and similar incentives can be introduced in other ways (read further).

## Second Proposal

After time, [@vbuterin](/u/vbuterin) introduced a new proposal: [One fee market EE to rule them all](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608). It was a significant improvement and removed many concerns listed above.

The proposal introduced a universal fee market or execution environment. In this fee market, all the execution environments could own a balance. Transaction fees would pay into the balance of the execution environment. At the end of a set of transactions, a `receipt` would be generated. This `receipt` could be used by the block producer to claim funds from the fee market EE and withdraw the funds to their validator account on the beacon chain or to another EE (depending on what the block producer wanted to do ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14) ).

Some major improvements in this proposal:

- Fees are paid to the EE and then to the block producer. There is no longer a relay market with a potential cartel which may act as a throttling function. Relayers exist in a new capacity. Lets call them state providers for now.
- Because it is in the interest of all validators to receive the highest fee transactions, the mempool would be introduced again, encouraging a more  distributed system.

This process and proposal requires additional steps of complexity and introduces a few questions:

- Complexity in the multi-step process of moving funds from one EE to another through the beacon chain.
- Who has the incentive to maintain state and provide witness or state data?

# More Light Client Servers - State Providers

As a result, this proposal introduced even more demand for the class of actors, `light client servers`. These `light client servers` or `state providers` would be incentivized to maintain state. [@vbuterin](/u/vbuterin)  describes further here: [One fee market EE to rule them all - #5 by vbuterin](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608/5). He also suggests an elegant system where transaction senders can maintain a state channel with the `state provider` and pay to add state/witness data to their transaction. Assuming tooling around a light client server is simple and easily runnable as a daemon, there should be a fairly distributed network of `state providers`.

The writeup also suggests `state providers` would package transactions together before sending them to the block proposers. The basis for this approach was to have a package that generates one payment receipt that can be claimed later, see  [One fee market EE to rule them all](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608/1). It also still refers to this actor as a `relayer`.

In reality, there no longer needs to be a concept of a `relayer` as it was originally. They would just broadcast the tx to a mempool now and add the necessary witness data. Additionally, the `state providers` do not need to create transaction packages. They already received their payment through a state channel. From there, they can submit each transaction to a network of `mempool`s and be done. In turn, the block producer can create transaction packages as 1:1 to the number of EEs the set of transactions represent. 3 EEs would result in 3 transaction packages and 3 receipts to claim.

# Iterating Further - Sync Calls Between EEs

We can continue to simplify the proposal if we support synchronous calls between EEs within the same shard. In this case, we no longer need receipts to be claimed through this multi-step process. The entry point to a set of transactions would be directly through the fee market EE. This fee market EE could iterate through each of the transactions and delegate its call through the proper EE each transaction is associated with. Through each call, the funds can be transferred directly to the block producer.

Additionally, state channel payments to the `state providers` are no longer needed. The user may sign their transaction with a `state provider` id and therefore payment can be transferred synchronously.

In order to determine if synchronous calls between EEs within the same shard are possible, benchmarking within [scout](https://ethresear.ch/t/phase-2-execution-prototyping-engine-ewasm-scout/5509) is needed.

# Another Step Forward - Generic Asset EE

We can simplify our system as a whole even further assuming we have sync calls between EEs. We may have one EE dedicated to the balances of accounts across all EEs. It is one shared EE to rule the token (ERC20) and beacon eth balance of every EE and every account within the EEs. [@matt](/u/matt)  shared a quick concept: [One fee market EE to rule them all - #11 by matt](https://ethresear.ch/t/one-fee-market-ee-to-rule-them-all/5608/11).

Additionally, this approach may support gas payments in tokens other than pegged beacon eth.

# Summary and Conclusion

In closing, the main points are as follows:

- We no longer need relayers in the same capacity. Lets call them state providers as part of a light client server for now.
- Transaction packages (if needed in a non-sync inter-ee system) can be 1:1 between the number of EEs represented in a block. They would be packaged by the block proposer.
- Mempools should be introduced again.
- Synchronous calls between EEs make everything simpler (but we need to benchmark if it can work).

**Questions**

- How do we ensure the network of state providers is distributed and open vs a centralization risk?
- Since opening a state channel requires a tx and a fee, will this system encourage users to rely on only a small set of infrastructure providers to add state?
- What type of additional layers of frontrunning does this system introduce?
- Is the mempool a part of the phase 1 or phase 2 specification?

## Replies

**terence** (2019-06-24):

> block producer can create transaction packages as 1:1 to the number of EEs the set of transactions represent.

Wouldn’t a block proposer to choose to limit the number as transaction packages to include? to avoid less receipts to be claimed later. Any concerns for that?

---

**vbuterin** (2019-06-25):

> Wouldn’t a block proposer to choose to limit the number as transaction packages to include? to avoid less receipts to be claimed later. Any concerns for that?

That’s definitely an incentive toward encouraging many transactions to be merged into a single package, and that’s an intended and good thing! We actually don’t want every transaction to be isolated, because if transactions are combined into a package then they can get savings from sharing witness data etc etc.

So these state providers would definitely have an aggregation role, and not just add witnesses to individual transactions and pass them along.

---

**villanuevawill** (2019-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So these state providers would definitely have an aggregation role, and not just add witnesses to individual transactions and pass them along.

I’m actually proposing that the state providers no longer need to make transaction packages. This whole setup complements a mempool quite well and transactions can be based individually again. Having a mempool encourages sharing of these transactions across all validators and removes questions/issues around a state provider giving easier incentive for a block producer to just take packages that fill their entire block (ignoring smaller packages). In this case, the block producer can pull transactions from the mempool and wrap them by EE into their own packages - still achieving the goal of packages as an aggregate and one receipt. Why even require the state providers to aggregate?

---

**vbuterin** (2019-06-25):

> In this case, the block producer can pull transactions from the mempool and wrap them by EE into their own packages - still achieving the goal of packages as an aggregate and one receipt. Why even require the state providers to aggregate?

Because the block producer does not necessarily have any idea what kind of witness construction is being used by the EE, and so doesn’t know how to efficiently aggregate multiple witnesses in a way that preserves the validity of the transactions. Hence we need state providers to do that functionality.

---

**villanuevawill** (2019-06-25):

Interesting… The mempool’s refresh algorithm would have to be aware of the different constructions, which is the general argument against managing them individually again vs. in packages?

So in this scenario of packages, we would need to have fresh broadcasts every slot. Any thoughts on how this may again create the scenario where just a few package providers maintain power? If I’m an individual user and want to package my own transaction outside the popular state provider network/nodes, there may not be incentive for the block producer to accept my transaction? How do intersecting transactions get managed (two packages with the same transaction)? How efficient/dos protected is a broadcast mechanism for all transactions every slot to the block producer?

Also, broadcasting my transaction to as many state providers as possible will now be discouraged since it requires a state channel in this construction. Although maybe there can be work around building a network of the state providers within a channel network that can route you… hmmm

Thoughts in general on some of these points above?

---

**vbuterin** (2019-06-25):

> Interesting… The mempool’s refresh algorithm would have to be aware of the different constructions, which is the general argument against managing them individually again vs. in packages?

Basically yes.

> Any thoughts on how this may again create the scenario where just a few package providers maintain power?

It may be the case that optimal state provision markets are pretty centralized and that’s fine! As long as at least one honest competitor exists, if the leading provider starts censoring then the competitor should be able to start outbidding them. It’s not like there’s a 51% attack risk among state providers.

> If I’m an individual user and want to package my own transaction outside the popular state provider network/nodes, there may not be incentive for the block producer to accept my transaction?

Not unless you pay a high fee. But why would you want to self-package? You could just broadcast on the network and then any state provider can just pick up your transaction and include it.

> How do intersecting transactions get managed (two packages with the same transaction)?

The second will likely fail. In general, I’m hoping for an equilibrium where we see one package per EE per slot per shard.

> How efficient/dos protected is a broadcast mechanism for all transactions every slot to the block producer?

This needs to be modeled / thought about more!

---

**villanuevawill** (2019-06-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The second will likely fail. In general, I’m hoping for an equilibrium where we see one package per EE per slot per shard.

I am very cautious about this approach. Simply put, it seems to reduce the permissionless nature of the system as a whole. The mechanics of an honest competitor replacement seems fairly tricky/abstract (with fair delays) and should be studied more thoroughly.  Additionally, it could present an entirely new dimension to selective front-running and adds significant friction to players who want to be sure they will not be censored or conveniently delayed (arbitrage, etc.). I tend to like the idea of having an incentive system on refreshing witness data in the network, as an alternative, with a mempool sharing all transactions. If I am dealing with sensitive transactions under certain circumstances where I should not be paying additional premiums to prevent intentional delays from centralized aggregators, being able to run my own nodes and just broadcast to a mempool seems much more preferable.

---

**vbuterin** (2019-06-25):

I see where your caution comes from!

There’s a lot of crazy properties and moving parts we are trying to combine here, particularly for example if we want to use [Near-instant transaction confirmation via staggered shard block production](https://ethresear.ch/t/near-instant-transaction-confirmation-via-staggered-shard-block-production/5643) to achieve sub-1-second app-level confirmation times then you want users to send transactions either directly to block producers or to aggregator nodes that then forward the data along to block producers immediately, without leaving room for weird multi-network-round games.

So the things that we want to have at the same time, as far as I can tell, are:

- Efficiency-saving batching (eg. merging Merkle branches) should happen somehow in the normal case (eg. if efficiency-saving batching temporarily stops happening when attempted censorship is taking place that’s ok)
- Block producers should not have to run custom per-EE code
- Avoid centralization or at least facilitate easy circumvention of centralized-actors-turned-harmful in relayer networks
- Maximize simplicity of the whole construction

Anything else I am missing?

---

**vbuterin** (2019-06-25):

Note that the scheme has to be abstract because we already know of a pretty diverse set of possible EEs that people will want to use, namely (i) the basic Merkle-tree-account-based one, (ii) ZKRollup, (iii) OVM, ie. Plasma with data published on chain (CC [@karl](/u/karl)). All three of these have very different notions of what “state” is, eg. Plasma doesn’t really have state, it has challenge games between receipts.

So far, it does seem like having state providers act as relayers but preserving the ability to self-package a transaction is a decent approach. The one challenge there is that if you self-package a transaction with one witness, and someone else relays another and the other gets in first, then your witness will be wrong. The best way to fix this that I see is some kind of “buffer state” for each execution environment that could be used to store recent witness data, eg. even 32 KB would do a lot (so don’t change the construction at all, but it possible for EEs to pay more for larger state size, so that going up to 32 KB is feasible; the only hard cap is that this state should be small enough to fully fit into a beacon block in a fraud proof). This would also mitigate [@JustinDrake](/u/justindrake)’s concerns about L2 witnesses not allowing the efficiency gains of batching being between larger sets of transactions than just one slot.

---

**Mikerah** (2019-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> It may be the case that optimal state provision markets are pretty centralized and that’s fine! As long as at least one honest competitor exists, if the leading provider starts censoring then the competitor should be able to start outbidding them. It’s not like there’s a 51% attack risk among state providers.

This tends towards a monopoly/being monopolistic instead of being permissionless. In practice, it is not straightforward to determine the difference between an honest competitor and a rational competitor. Often times, they may be the same and at other times, different due to market conditions!

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> Additionally, it could present an entirely new dimension to selective front-running and adds significant friction to players who want to be sure they will not be censored or conveniently delayed (arbitrage, etc.)

This could potentially be remedied by implementing something like Submarine Sends ([To Sink Frontrunners, Send in the Submarines](http://hackingdistributed.com/2017/08/28/submarine-sends/)) at the consensus/L1. It allows for temporarily hiding transactions in order to prevent front-running.

Another concern I have for this proposed scheme is that is seems to have eliminated the gas/transaction fee abstraction that previous proposals brought. These abstractions make it easier, from the get-go to pay these fees in a potential, separate “sub-currency” e.g. ERC20s and allowed for others to pay for other people’s gas/transaction fees. The latter fact could potentially enable various forms of privacy-preserving payment systems in ETH2.0. Am I wrong here?

