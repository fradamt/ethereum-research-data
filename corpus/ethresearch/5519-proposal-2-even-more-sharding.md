---
source: ethresearch
topic_id: 5519
title: "Proposal 2: even more sharding"
author: ryanreich
date: "2019-05-28"
category: Sharding
tags: [data-availability]
url: https://ethresear.ch/t/proposal-2-even-more-sharding/5519
views: 3684
likes: 1
posts_count: 4
---

# Proposal 2: even more sharding

[@vbuterin](/u/vbuterin)’s recent [Phase 2 Proposal 2](https://notes.ethereum.org/w1Pn2iMmSTqCmVUTGV4T5A?view) document presents an “execution environment” concept: contracts on the beacon chain that hold independent per-shard states.  Shards run their various blocks in these environments, updating their personal state, which is eventually committed to the beacon chain, presumably when the block is attested or via a crosslink (I can’t find a definite statement on this, but I think the details don’t matter in this post, so long as the states eventually reach the beacon chain).

My point in this post, in brief, is that this introduces a new perspective on the nature of shards, and that this perspective admits an expansion to a more nuanced shard structure capable of cross-shard communication.  This expansion is compatible with everything that has already been done for sharding, but also adds a huge capability to shard-level metaprogramming.

---

Right now (as of Proposal 2), the beacon state tracks a list of execution environments, each of which has some code and also tracks a list of shard states corresponding to calls made to that environment in each shard.  I like to “commute” this description: as a pure function, an EE is essentially an export from some notional “library”, which may be instantiated into an actual smart contract by giving it a mutable state object; therefore, the EE list is more conceptually understood as being a data store of contracts, each of which is called by exactly one shard at various times (a single shard may call multiple contracts in its lifetime).

This creates a picture of the beacon chain as a set of noninteracting streams of contract calls, and each stream is part of a shard.  Though this resembles a set of separate, parallel execution threads (i.e. many independent Ethereum-1.0s), by existing together in one central beacon chain what we actually have is a single smart contract universe in which only transactions may make calls, but not contracts themselves.  The activity of sharding is then to parcel out maintenance of the contracts to separate consensus environments.

In this model, cross-shard communication would simply be the ability of one transaction to call multiple contracts.  This means that transactions would not easily be divided among separate shards, but for execution purposes, it doesn’t matter: clients can still have a set of EEs (contracts) they want to watch, and choose to process only the transactions that call them.  This is the same kind of behavior that clients of the current sharding model would exhibit.

This gives a kind of static interaction among contracts (“shards”): transaction messages would be able to write programs that call contracts, call pure functions on the results, and call other contracts with *those* results, so long as no jumps are allowed, so that we can still identify which contracts are affected.  A form of conditional logic could even be included if the return values are augmented with a `Nothing` or other exceptional value that would propagate through subsequent contract calls on that value. This is more than sufficient for many useful purposes, the most common of which would surely be to pay contract A with money from contract B.  This logic, programmatic though it is, would not even require gas, since the length of the program and the duration of its execution are essentially the same.

What about consensus?  Part of the point of sharding as it stands is to distribute the actual activity of running a blockchain, regardless of what it carries.  I think this could still be done.  Two observations:

1. The existence of validators who run transactions is necessary in order for consensus to include an affirmation of state updates.
2. Absent concerns about state transition, there is no reason that all transactions couldn’t just be lumped into a single blockchain without validation (i.e. “data availability”).

So let’s take a two-stage approach to sharded consensus.

- Stage 1: Blocks are created indiscriminately from transactions.  There is still a potential for incentives here, because the beacon chain itself tracks ether, and transaction senders can offer a payment directly from their accounts as they stand before the block is created; we can assume by induction that those balances are validated.  These blocks are subject to a round of consensus and formed into a chain.
- Stage 2: Now that the transaction order is established, validators can go to work.  Each one is responsible for following some contracts, and so is capable of validating transactions up to the point that one of them includes a call to a contract they don’t follow and whose pre-state hasn’t yet been validated.  They release affirmations into the network for everything they can validate, and these get formed into a block, subjected to consensus, and committed to a second chain.
 The second chain will necessarily lag behind the first one: there will be multiple Stage 2 blocks for each Stage 1 block until all validators can complete their work on the latter’s transactions.  But progress, however incremental, will always be made.
 The best case is the existing transaction structure: noninteracting calls to separate contracts.  Then this sharding will look just like it does now, all validators will be able to do their entire portion of the block at once, and the Stage 1 – Stage 2 correspondence is one-to-one.
 The worst case is total interconnectivity, in which case the Stage 2 blocks have to be very short as validators coordinate their incremental efforts via the Stage 2 consensus process.  This seems like an obvious and necessary limitation of scaling: if every transaction has global consequences, then either everyone executes everything, or everyone is waiting for everyone else to do their part.  It’s a basic concurrency tradeoff.

This execution structure would also create an opportunity to create smaller shards, simply by writing much more limited execution environments for special purposes, which may even *end* and not require further following, or fragment into several successor environments (i.e. create new contracts and then self-destruct), each of which could then go to different validators.  The validator pool could be much more flexible and, at least ideally, would not necessarily suffer from “horizontal” bloat of individual execution environments as they become too popular.

This post, once again, is very long and does not contain the kind of formal definitions that I see in Vitalik’s work.  I don’t want to introduce ambiguity but I thought I could explain it better in a verbal narrative than through code.  Hopefully anyone reading this will find that despite that, it’s not entirely hand-waving.

## Replies

**villanuevawill** (2019-05-28):

Thanks [@ryanreich](/u/ryanreich) - I’m going to comment on a few things and ask for further clarification to have some understanding on what you are proposing.

In general, this appears to be a form of a delayed execution model which is generally discussed here [Delayed state execution, finality and cross-chain operations](https://ethresear.ch/t/delayed-state-execution-finality-and-cross-chain-operations/987) and most recently [Phase One and Done: eth2 as a data availability engine](https://ethresear.ch/t/phase-one-and-done-eth2-as-a-data-availability-engine/5269).

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> This is the same kind of behavior that clients of the current sharding model would exhibit.

Is this? In general, there can be a separate EE dedicated to block payments in which the block proposer could be fairly agnostic on what EEs it runs as long as it brings in sufficient funds.

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> A form of conditional logic could even be included if the return values are augmented with a Nothing or other exceptional value that would propagate through subsequent contract calls on that value.

Confused by this statement - can you provide a more concrete explanation here?

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> They release affirmations into the network for everything they can validate, and these get formed into a block, subjected to consensus, and committed to a second chain.

In general, this is a layer 2 market to confirm what the state transitions would be? What incentives do you see on being a stage 2 validator?

![](https://ethresear.ch/user_avatar/ethresear.ch/ryanreich/48/3479_2.png) ryanreich:

> The worst case is total interconnectivity, in which case the Stage 2 blocks have to be very short as validators coordinate their incremental efforts via the Stage 2 consensus process.

I understand the idea here, however, wouldn’t you actually argue that the majority of cross-contract calls be a part of the same EE or contract/transaction framework? Therefore, incremental efforts wouldn’t need to be as short if you assume this? (Some of the explanations seem to blur the line between EEs and contracts that exist within an EE).

Just trying to understand the general thought process and these are my quick observations/responses.

---

**ryanreich** (2019-05-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> In general, this appears to be a form of a delayed execution model which is generally discussed here Delayed state execution, finality and cross-chain operations  and most recently Phase One and Done: eth2 as a data availability engine.

That sounds right.  I was explicitly implicitly alluding to the latter; I should have remembered the former, as I did read it once.  Either way, thank you for the links I should have provided.  It seems like Vitalik, in particular, expressed the consensus process for delayed execution in more detail than I have here.  Since my suggestion was so similar, I think the smart-contract part of my argument stands as another argument in favor of the idea.

I think what I’m saying is actually significantly different from what Casey was: for one, contracts aren’t stateless here.  And I’m actually proposing a kind of hybrid setup with two different kinds of execution: one for coordinating shards, and one for their execution environments themselves.  Also, this proposal lives more on top of Phase 0 than Phase 1: it’s like an alternate Phase 1 that facilitates the evolution of Phase 2.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> This is the same kind of behavior that clients of the current sharding model would exhibit.

Is this? In general, there can be a separate EE dedicated to block payments in which the block proposer could be fairly agnostic on what EEs it runs as long as it brings in sufficient funds.

How does that work, in the current sharding model?  If I have a transaction T, and I also want to pay the block creator by passing money through another transaction T’ in the special EE, there is no trustworthy relationship between the two.  The block creator could just take T’ and forget T.

In my proposal, it would work, because you could put both contract calls in the same transaction.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> A form of conditional logic could even be included if the return values are augmented with a Nothing or other exceptional value that would propagate through subsequent contract calls on that value.

Confused by this statement - can you provide a more concrete explanation here?

I just mean that if you call some contract and get a result `x`, which you want to feed to another contract call, it’s okay if the execution model allows `x` to be an exception that causes the latter call to also return an exception.  This allows *forward* jumps, but not backward ones, effectively: *if* this call succeeds, then do the latter call; otherwise just proceed from after both of them.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> They release affirmations into the network for everything they can validate, and these get formed into a block, subjected to consensus, and committed to a second chain.

In general, this is a layer 2 market to confirm what the state transitions would be? What incentives do you see on being a stage 2 validator?

It’s more like Layer 1.5: still subject to trustless consensus, but also post-blockchain formation.  Say that I’m a light client user who wants to receive some money in a transaction that contains a service to the buyer in return.  I require the buyer to put in a proof of correct payment (most directly, this could just be the literal byte string representing the value offered in payment, that *would* be returned from the contract if it were actually executed), and I include a block payment to the Stage 2 validator.  Now the transaction is only valid if the proof is correct, and that is certified by the trustless process that chooses the block; the validator gets paid for including my transaction, I get paid for getting it into a block, and the buyer gets their service.  If they lie, of course, they get nothing, unless they can suborn the validator, which is your 51% attack scenario.

![](https://ethresear.ch/user_avatar/ethresear.ch/villanuevawill/48/16625_2.png) villanuevawill:

> The worst case is total interconnectivity, in which case the Stage 2 blocks have to be very short as validators coordinate their incremental efforts via the Stage 2 consensus process.

I understand the idea here, however, wouldn’t you actually argue that the majority of cross-contract calls be a part of the same EE or contract/transaction framework? Therefore, incremental efforts wouldn’t need to be as short if you assume this? (Some of the explanations seem to blur the line between EEs and contracts that exist within an EE).

I think it’s kind of an open question (in the sense of having many answers, not of having an unknown definite answer) whether the EE-internal operations would outweigh the inter-EE coordination logic.  It depends on how large a “universe” the execution environments in question represent.  If they are limited-scope markets, then you’d expect more interconnectivity, which has kind of a parabolic curve of returns: up to a point, this increases parallelizability of shards, but with too much interconnectivity, it’s like there’s no sharding at all.  Certainly, Ethereum-like EE’s will not have the latter problem as much.

---

**vbuterin** (2019-05-30):

> Stage 2: Now that the transaction order is established, validators can go to work. Each one is responsible for following some contracts, and so is capable of validating transactions up to the point that one of them includes a call to a contract they don’t follow and whose pre-state hasn’t yet been validated. They release affirmations into the network for everything they can validate, and these get formed into a block, subjected to consensus, and committed to a second chain.

This seems fundamentally similar to the approach I described for synchronous cross-shard comms here [Simple synchronous cross-shard transaction protocol](https://ethresear.ch/t/simple-synchronous-cross-shard-transaction-protocol/3097). Basically, an individual validator aware of the state of some shard A up to slot N and the state root of every other shard up to slot N can incrementally compete the state of shard A up to slot N+1, and then wait for light client confirmations of the state roots of all other shards up to slot N+1.

I think the main reason I haven’t been thinking about this approach at layer 1 is just that the logic would be too complicated (part of the reason I insist on writing these proposals in python is precisely so that we can upper-bound the consensus complexity of actually doing them ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12)), and it also introduces a high layer of base-level fragility: if any of those light client confirmations for any shard turn out to be wrong, then the computation for every shard from that slot on must be thrown out and redone.

Though I feel like it should be possible to code this up as an EE…

