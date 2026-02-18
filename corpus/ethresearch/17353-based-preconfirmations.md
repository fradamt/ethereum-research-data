---
source: ethresearch
topic_id: 17353
title: Based preconfirmations
author: JustinDrake
date: "2023-11-08"
category: Layer 2
tags: [preconfirmations, based-sequencing, sequencing]
url: https://ethresear.ch/t/based-preconfirmations/17353
views: 23213
likes: 85
posts_count: 32
---

# Based preconfirmations

*Special thanks to Dan Robinson, Mike Neuder, Brecht Devos for detailed design discussions.*

**TLDR**: We show how [based rollups](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016) (and based validiums) can offer users preconfirmations (“preconfs” for short) on transaction execution. Based preconfs offer a competitive user experience for based sequencing, with latencies on the order of 100ms.

**construction**

Based preconfs require two pieces of onchain infrastructure:

- proposer slashing: A proposer must have the ability to opt in to additional slashing conditions. This write-up assumes slashing is achieved with EigenLayer-style restaking.
- proposer forced inclusions: A proposer must have the ability to forcefully include transactions onchain, even with PBS when self-building is non-economical. This write-up assumes forced inclusions are achieved with inclusion lists.

A L1 proposer may become a **preconfer** by opting in to two preconf slashing conditions described below. Preconfers issue signed **preconf promises** to users and get paid **preconf tips** by users for honouring promises.

Preconfers are given precedence over other preconfers based on their slot position in the proposer lookahead—higher precedence for smaller slot numbers.

A transaction with a preconf promise from the next preconfer can be immediately included and executed onchain by any proposer ahead of that preconfer. The preconfer is then expected to honour any remaining promises on their slot using the inclusion list.

There are two types of promise faults, both slashable:

- liveness faults: A promise liveness fault occurs when the preconfer’s slot was missed and the preconfed transaction was not previously included onchain.
- safety faults: A promise safety fault occurs when the preconfer’s slot was not missed and the promise is inconsistent with preconfed transactions included onchain.

Safety faults are fully slashable since honest preconfers should never trigger safety faults. The preconf liveness slashing amount, mutually agreed by the user and preconfer, can be priced based on the risk of an accidental liveness fault as well as the preconf tip amount.

Non-preconfed transactions included onchain by non-preconfers will not execute immediately. Instead, to give execution precedence to preconfed transactions over non-preconfed transactions, an execution queue for non-preconfed transactions is introduced. Non-preconfed transactions included onchain are queued until the first preconfer slot is not missed. At that point all transactions execute, with preconfed transactions executed prior to queued non-preconfed transactions.

**promise acquisition**

A user that wants their transaction preconfed should aim to acquire a promise from, at minimum, the next preconfer in the proposer lookahead. This process starts with the user sending a promise request to the next preconfer.

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9667dc80c8d911fa3cd86108c3375d0de06e4252_2_690x387.png)2110×1184 141 KB](https://ethresear.ch/uploads/default/9667dc80c8d911fa3cd86108c3375d0de06e4252)

The offchain mechanisms by which users acquire promises are not dictated by the onchain preconf infrastructure. There is an open design space with several considerations relevant to any preconf infrastructure, not just based preconfs.

- endpoints: Preconfers can publicly advertise point-to-point API endpoints to receive promise requests and return promises. At the cost of latency, p2p gossip channels can be used instead of point-to-point endpoints.
- latency: When a point-to-point connection is used between a user and preconfer, preconf latencies can happen on the order of 100ms.
- bootstrapping: Sufficient L1 validators must be preconfers to have at least one preconfer in the lookahead with high probability. The beacon chain has at least 32 proposers in the lookahead so if 20% of validators are preconfers there will be a preconfer with probability at least 1 - (1 - 20%)32 ≈ 99.92%.
- liveness fallback: To achieve resilience against promise liveness faults a user can acquire promises in parallel from more than one of the next preconfers. If the first preconfer triggers a liveness fault a user can fallback to a promise from the second preconfer.
- parallelisation: Different types of promises can have different preconf conditions. The strictest type of promise commits to the post-execution state root of the L2 chain, creating a sequential bottleneck for promise issuance. A weaker form of promise only commits to the execution state diff, unlocking parallel promise issuance across users. Even weaker intent-based promises (e.g. “this swap should receive at least X tokens”) are possible. The weakest form of promise, which only commits to transaction inclusion by a preconfer slot, may be relevant for some simple transfers.
- replay protection: To avoid replay attacks by preconfers such as sandwiching via transaction reordering, transaction validity is recommended to be tied to the preconf condition. This can be achieved with a new L2 transaction type, either with account abstraction or a native transaction type.
- SSLE: Preconfer discovery in the lookahead remains possible with Single Secret Leader Election (SSLE). Indeed, preconfers can advertise (offchain and onchain) zero-knowledge proofs they are preconfers at their respective slots without revealing further information about their validator pubkey. Preconf relays intermediating users and preconfers can shield IP addresses on either side.
- delegated preconf: If the bandwidth or computational overhead of issuing promises is too high for a L1 proposer (e.g. a home operator), preconf duties can be delegated (fully or partially) to a separate preconfer. The preconfer can trustlessly front collateral for promise safety faults. Liveness faults are the dual responsibility of the L1 proposer and the preconfer, and can be arbitrated by a preconf relay.
- fair exchange: There is a fair exchange problem with promise requests and promises. Given a promise request, a preconfer may collect the preconf tip without sharing the promise to the user. A simple mitigation is for users to enforce that promises be made public (e.g. streamed in real time) before making new promise requests. This mitigation solves the fair exchange problem for all but the latest preconf promises. A relay mutually trusted by the user and the proposer can also solve the fair exchange problem. Finally, a purely cryptographic tit-for-tat signature fair exchange protocol can be used.
- tip pricing: We expect that for many transactions a fixed preconf gas price can be mutually agreed. Some transactions may have to pay a correspondingly larger tip to compensate for any reduction to the expected MEV the proposer could otherwise extract. For example, a DEX transaction preconfed several seconds before the preconfer’s slot may reduce the expected arbitrage opportunity for the preconfer. Mutually trusted relays may help users and preconfers negotiate appropriate preconfirmation tips.
- negative tips: Negative tips may be accepted by preconfers, e.g. for DEX transactions that move the onchain price away from the offchain price, thereby increasing the expected arbitrage opportunity for the preconfer.

## Replies

**ben-a-fisch** (2023-11-09):

Nice idea! This seems to offer a different (weaker) type of “preconfirmation” guarantee than *finality,* which is what a consensus protocol like Espresso’s Hotshot protocol provides. What happens to these preconfs when there is a reorg on Ethereum’s LMD Ghost protocol? Also, how much stake would be slashed for invalid preconfirmations in this proposal versus a protocol like the Espresso Sequencer (e.g., assuming the same amount of L1 validator stake is participating in each via Eigenlayer)? For the Espresso Sequencer the amount slashed would be 1/3 of the entire stake. Am I also understanding correctly that, unless every single L1 validator is also participating as a preconfer, a user can’t get any promise on precisely where in the order its tx will be included until the next preconfer’s turn? E.g., if 20% of L1 validators participate as preconfers this would be every minute? Lastly, this construction seems to be orthogonal/complementary because the Espresso proposers (leaders) can also offer this weaker flavor of preconf with the same claimed 100ms latency etc. In fact, with Hotshot or any protocol that has single-slot finality, the proposer/preconfer has arguably lower risk when providing a user with a preconf of this form than with LMD Ghost as there isn’t the same risk of reorg (only the risk of missing/failing to complete the slot). With Espresso there would also be no delay that depends on the fraction of L1 validators participating.

---

**The-CTra1n** (2023-11-09):

I think this discussion highlights the blurred lines that define what it means to be based. From Justin’s [og post on based rollups](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016), the “sequencing is driven by the base L1”. Both proposals discussed by Justin and Ben aren’t technically being driven by the base L1 anymore, but rather by some form of off-chain consensus, albeit with the L2 proposers explicitly now some subset of the L1 proposers in Justin’s proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Non-preconfed transactions included onchain by non-preconfers will not execute immediately. Instead, to give execution precedence to preconfed transactions over non-preconfed transactions, an execution queue for non-preconfed transactions is introduced. Non-preconfed transactions included onchain are queued until the first preconfer slot is not missed. At that point all transactions execute, with preconfed transactions executed prior to queued non-preconfed transactions.

This sounds like removing the basedness of the rollup. Based sequencing using the standard non-preconf entry point becomes an elaborate forced inclusion list, which will have no guarantee of execution as preconfs can always front-run the non-preconfs. Sequencing is effectively moved off-chain using both this protocol and the Espresso suggestion, which is a contradiction to based sequencing imo.

Maybe it’s not? Interested to hear your thoughts.

---

**gets** (2023-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> replay protection: To avoid replay attacks by preconfers such as sandwiching via transaction reordering, transaction validity is recommended to be tied to the preconf condition. This can be achieved with a new L2 transaction type, either with account abstraction or a native transaction type.

Why does transaction validity prevent sandwiching?

---

**bruno_f** (2023-11-16):

Why couldn’t I just do the same without restaking? I can create a rollup with a token, have people stake my token on some L1 contract and then have this kind of round-robin consensus that is being used here. Except that now my rollup has more sovereignty (doesn’t rely in EigenLayer) and more importantly can capture more value (especially MEV). Outsourcing the consensus to EigenLayer isn’t any better than having my own consensus. At least the original based rollup was truly codeless.

Any L2 sequencing that outsources its validator selection to a L1 contract, already inherits the liveness and decentralization of Ethereum. The main differentiators of based rollups still seem to be only two: that it doesn’t require any code and that MEV flows to L1.

MEV flowing to L1 is not desirable for a rollup. If I’m a rollup and I capture more value than my competitors then my token is worth more and I have more resources to hire developers, do marketing, provide ecosystem grants, etc.

It’s also not desirable for Ethereum to capture that much value. If all that value goes to L1, then there won’t be any companies willing to spend billions on rollup projects. Then it would have to be the EF to do all of the work on developing those rollups. An Ethereum where the EF does all the R&D for the ecosystem is not decentralized or neutral.

---

**kartik1507** (2023-11-16):

Interesting idea. But I have a question about the design. Typically, builders need to know the system’s state to build the next set of blocks, e.g., to determine whether a set of transactions is valid. This also plays into figuring out how much MEV they get and what they bid.

Now imagine a situation where one entity X is a validator, builder, and client simultaneously. Let’s assume that this validator is the earliest preconfer, and its slot is 5 blocks away. It creates a preconfed transaction that is not publicly known until it is X’s turn to be the proposer at which point it includes the transaction. All preconf conditions are satisfied, so there are no issues there. But for the last 5 blocks, builders other than X do not have the latest state of the system, making them unable to guarantee that the transactions they include will be executed. This gives X an unfair advantage since it is the only one to know the state of the system. Can this result in builder centralization?

In fact, one can do this attack adaptively. Wait until it is X’s turn to be a preconfer. Observe the last 5 blocks and create and preconf transactions such that it imparts maximum harm to other builders (and consequently clients). This would also provide an easy means to frontrunning after multiple blocks have been proposed, correct?

---

**The-CTra1n** (2023-11-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> Based sequencing using the standard non-preconf entry point becomes an elaborate forced inclusion list, which will have no guarantee of execution as preconfs can always front-run the non-preconfs.

I made the same point here. Feels like the proposed design can’t get around this issue.

---

**JustinDrake** (2023-11-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/ben-a-fisch/48/11572_2.png) ben-a-fisch:

> This seems to offer a different (weaker) type of “preconfirmation” guarantee than finality, which is what a consensus protocol like Espresso’s Hotshot protocol provides. What happens to these preconfs when there is a reorg on Ethereum’s LMD Ghost protocol?

Agreed!

![](https://ethresear.ch/user_avatar/ethresear.ch/ben-a-fisch/48/11572_2.png) ben-a-fisch:

> how much stake would be slashed for invalid preconfirmations in this proposal

The amount slashed for safety faults is fully programmable and not limited to 32 ETH. For example, one could delegate preconfs to a dedicated preconfer (e.g. a relay) which can pledge an arbitrarily-large amount of collateral, including non-ETH collateral. Another strategy to boost collateral may be for  an operator to combine the stake from k validators to get k * 32 ETH of collateral.

![](https://ethresear.ch/user_avatar/ethresear.ch/ben-a-fisch/48/11572_2.png) ben-a-fisch:

> Am I also understanding correctly that, unless every single L1 validator is also participating as a preconfer, a user can’t get any promise on precisely where in the order its tx will be included until the next preconfer’s turn?

Nope, that’s a misunderstanding ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) A user can get a promise (within ~100ms, by communicating with the next preconfer) on the execution of their transaction (down to the post-state root, if desired—see the section titled “parallelisation”).

![](https://ethresear.ch/user_avatar/ethresear.ch/ben-a-fisch/48/11572_2.png) ben-a-fisch:

> this construction seems to be orthogonal/complementary because the Espresso proposers (leaders) can also offer this weaker flavour of preconf with the same claimed 100ms latency

Agreed—I removed the sentence “This is roughly an order of magnitude faster than running an external consensus, e.g. as done by [Espresso](https://www.espressosys.com/).”

---

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> This sounds like removing the basedness of the rollup.

Based sequencing with preconfirmations remains a tokenless, hatch-free, credibly neutral, decentralised, shared sequencer which reuses L1 sequencing and inherits its censorship resistance.

I think the point you are making is that when preconfirmers don’t preconfirm (e.g. are offline) transactions execution is delayed. If X% of proposers are preconfirmers then transaction execution can be delayed by 1/X% on average. The good news (as discussed on our call, as well as in the response to [@kartik1507](/u/kartik1507)  is that rational proposers are incentivised to become preconfirmers so I expect X% to be relatively close to 100%. There may also be an opportunity to somehow enshrine preconfirmations and mandate that every proposer be a preconfirmer.

![](https://ethresear.ch/user_avatar/ethresear.ch/the-ctra1n/48/9792_2.png) The-CTra1n:

> preconfs can always front-run the non-preconfs

I expect the vast majority of transactions will be preconfed and that non-preconfed user transactions will be a thing of the past. There’s no execution latency overhead to preconfirmation (preconfed transactions can be immediately executed onchain by any proposer ahead of the next preconfer) and the section titled “replay protection” explains how to protect preconfed transactions from frontrunning.

Now let’s assume that for some reason a significant portion of transactions are not preconfirmed. Then any transaction that is frontrunnable (e.g. a swap) can be protected by encryption similarly to encrypted mempools. That is, frontrunnable transactions would go onchain encrypted and would only decrypt and execute after the preconfirmed transactions. Again, such protection is unnecessary if preconfirmations are used in the first place.

![](https://ethresear.ch/user_avatar/ethresear.ch/kartik1507/48/12966_2.png) kartik1507:

> for the last 5 blocks, builders other than X do not have the latest state of the system, making them unable to guarantee that the transactions they include will be executed. This gives X an unfair advantage since it is the only one to know the state of the system. Can this result in builder centralization?

In your scenario the preconfirmer has monopoly power to execute transactions (and extract certain types of MEV like CEX-DEX arbitrage) for 5 slots. It’s as if their slot duration was a whole 1 minute instead of the usual 12 seconds. Longer effective slot durations definitely favour preconfirmers but are largely orthogonal to builder centralisation. (As a side note, building is already extremely centralised.)

This monopoly power to execute transactions is an incentive for proposers to opt in to becoming preconfers. You can think of it as a bootstrapping mechanism which temporarily rewards early preconfirmers and incentivises most proposers to become preconfers.

![](https://ethresear.ch/user_avatar/ethresear.ch/gets/48/11577_2.png) gets:

> Why does transaction validity prevent sandwiching?

If the transaction is only valid if executed as preconfirmed, and the preconfirmed execution does not sandwich, then the transaction cannot be replayed to sandwich the user.

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> Why couldn’t I just do the same without restaking?

You can!

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> I can create a rollup with a token

One of the value propositions of based sequencing is neutrality and tokenlessness. The based sequencer is a credibly neutral sequencer for L2s and their competitors to enjoy the network effects of shared sequencing. Moreover, using a non-ETH token will almost certainly reduce economic security. (Today Ethereum has $60B of economic security).

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> more sovereignty (doesn’t rely in EigenLayer)

EigenLayer is not required—any restaking infrastructure (e.g. home-grown, or an EigenLayer fork with governance removed) could work.

---

**ed** (2023-12-24):

Thank you [@JustinDrake](/u/justindrake) for this post!  A few of us at Espresso have written a detailed follow-up discussion [here](https://ethresear.ch/t/analyzing-bft-proposer-promised-preconfirmations/17963).

---

**Perseverance** (2024-01-13):

For the past couple of weeks, I and a couple of my team members have been diving into all things required to build a POC of based preconfirmations (EigenLayer, PBS, Based rollups & more). I guess it is obvious from this thread that based preconfirmations are a complex matter. We’d like to share our thoughts and further research avenues we ended up with.

## Obstacle 1: How do you even talk with preconfirmers

Preconfirmations require the users to be able to discover upcoming preconfirmers and ask them to commit to a preconfirmation. As preconfirmers are validators: “You dont talk to them. They talk to you.”. Think of mev-boost and relays. Builders dont talk directly to validators, they tell their blocks to relayers and the relayers get asked by the validators for blocks. This adds security & privacy properties to the validator that [I guess] they would not want to lose.

So if users are to talk with validators for preconfirmations, a pull mechanism needs to be designed (similar to relays) for validators to pull preconfirmation requests and possibly honour them.

## Obstacle 2: Who do you even talk to

Lets ignore the previous obstacle for a while. While the general thought process is one where the user connects to **a** preconfirmer - which preconfirmer exactly? One idea would be to talk with the next pre-confirmer available, but you are at the mercy of their response. What if this preconfirmer censors you or it is down? You can wait for a certain timeout and try the next one. And the next one. You get the idea. With every subsequent timeout you are getting worse UX.

Another approach would be to talk to the next X (lets say 16) preconfirmers in parallel and wait for the first commitment. This approach however is wasteful as all but one of these commitments will be used - and waste drives prices up.

## Obstacle 3: Preconfirmations validity rules

Spoiler - we looked at [PEPC](https://efdn.notion.site/PEPC-FAQ-0787ba2f77e14efba771ff2d903d67e4#1087a2bc8b664113b6682d201788bfe0) for some inspiration and ideas for solutions. Preconfirmations look like a really good fit for the “generalized mev-boost” - PEPC. However, PEPC doc briefly mention something called *payload template*. While payload template likely makes sense in many use cases its details are going to be crucial for preconfirmations.

While many generalised use cases might require for a certain types of transactions to be a part of the transactions list, with based preconfirmation it is quite trickier. You need to enforce/validate that an L2 transaction is included in the sequencing transaction. This means a subsection of the calldata of a single transaction contains the pre-confirmed transaction.

Add to this:

- Data compression - so the payload is even harder to enforce
- Danksharding - what data… its not even here
- Unknown permissionless sequencer - “I dont even know who to expect the sequence transaction from”
- Complex sequencing pipeline through multiple contracts - “I need to look into the trace”
- More than one preconfirmation per sequence - order matters

In PBS world where the preconfirmers are separate from the block builders, the proposers would need a mechanism to pass very complex templates for builders to honour.

# Some of our thoughts

These are just some of the nasty edge cases of the current state of preconfirmation and the hardship of their implementation in the current state of Ethereum.

Obstacle #1 lead us to think of an architecture looking like a generalized mev-boost. Fortunately EF researchers are some months (years? ![:smiley:](https://ethresear.ch/images/emoji/facebook_messenger/smiley.png?v=12)) ahead and PEPC is a generalized ePBS architecture. With PEPC architecture one can have a communication channel and validity rules in the protocol itself. Without PEPC numerous trust assumptions need to be introduced even if you are building a simple PoC.

Obstacle #2 leads us to think about the efficiency of talking to preconfirmers. Is it even viable to have preconfirmers? Various practical issues can lead to a worse UX for the user.

Obstacle #3 lead us to think about the complexity of enforcing sub-section of a transaction. A responsibility that will likely be passed to builders.

# Research avenues

We believe that the following are research avenues that need to be further looked at to explore possible preconfirmations solutions.

1. Intersection of pre-PEPC state of PBS (optimistic relay) and preconfirmations. Is optimistic preconfirmations-enabled relay feasible? Intersaction of pre-PEPC state of PBS with EigenLayer
2. Current state of research for Inclusion lists and its ability to enforce transactions based on complex template - required for forcing inclusion of sequence transaction including one or multiple preconfirmations.
3. How can a complex template be designed and implemented
4. Based on the previous findings - how does one design based-preconfirmations

---

**CalabashSquash** (2024-01-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> parallelisation: Different types of promises can have different preconf conditions. The strictest type of promise commits to the post-execution state root of the L2 chain, creating a sequential bottleneck for promise issuance. A weaker form of promise only commits to the execution state diff, unlocking parallel promise issuance across users. Even weaker intent-based promises (e.g. “this swap should receive at least X tokens”) are possible. The weakest form of promise, which only commits to transaction inclusion by a preconfer slot, may be relevant for some simple transfers.

This makes it seem like we are expecting pre-confirmations would be requested by some sort of aggregator, who requests pre-confirmations for entire state changes. I would have thought “The weakest form of promise” of only pre-confirming one transaction would be the most common use case.

> transaction validity is recommended to be tied to the preconf condition

What does this mean?

---

**bruno_f** (2024-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> One of the value propositions of based sequencing is neutrality and tokenlessness. The based sequencer is a credibly neutral sequencer for L2s and their competitors to enjoy the network effects of shared sequencing. Moreover, using a non-ETH token will almost certainly reduce economic security. (Today Ethereum has $60B of economic security).

Tokenlessness is not a feature, is a bug. To quote from [this post](https://medium.com/@nfett/eigenlayer-crypto-rehypothecation-and-the-infinite-trust-machine-4e8164845b59) on restaking (it’s worth a read):

> One of the main selling points of tokens is to bootstrap something which doesn’t have network effects or a business model yet. By stripping away your token and using base ETH instead, you get rid of the bootstrapping effect because you remove the ability of the protocol to print inflationary rewards in exchange for security / activity.

Besides this, creating a token is the only way many blockchain startups have of raising capital. Which you need in order to actually build a product.

On the point about economic security, as was said by other posters, the security of my preconf is secured only by the stake of the preconfirmer. It’s irrelevant if that preconfirmer is staking ETH or something else.

---

**JustinDrake** (2024-02-07):

> On the point about economic security, as was said by other posters, the security of my preconf is secured only by the stake of the preconfirmer. It’s irrelevant if that preconfirmer is staking ETH or something else.

The point about economic security is related to censorship resistance of sequencing, not security of preconfirmations. Using a non-ETH token for sequencing will dramatically lower real-time censorship resistance.

---

**bruno_f** (2024-02-08):

Apologies if it’s obvious, but I don’t see as using ETH for sequencing will improve censorship resistance. Could you explain in more detail?

---

**JustinDrake** (2024-02-10):

> I don’t see as using ETH for sequencing will improve censorship resistance. Could you explain in more detail?

The L1 serves as a inclusion list for rollups, to provide censorship resistance. Without based sequencing the best you can have is delayed forced transactions (aka an “escape hatch”). For example, on Arbitrum there’s a 24h delay between when a transaction is included on L1 (bypassing the Arbitrum sequencer) and when that transaction is forcefully executed on the Arbitrum execution environment.

With based sequencing there’s no need for a delay: if a transaction goes on L1 it’s safe to compel the next sequencer to execute the transaction by their slot, without delay. I explain in the original based rollup post (see [here](https://ethresear.ch/t/based-rollups-superpowers-from-l1-sequencing/15016)) why escape hatches are bad design:

[![Screenshot 2024-02-10 at 10.42.20](https://ethresear.ch/uploads/default/original/2X/a/a221f81c396537e4a99cea755c7f3372050829db.png)Screenshot 2024-02-10 at 10.42.201354×470 60.3 KB](https://ethresear.ch/uploads/default/a221f81c396537e4a99cea755c7f3372050829db)

---

**donnoh** (2024-02-10):

> Without based sequencing the best you can have is delayed forced transactions (aka an “escape hatch”).

That’s not always true: OP stack chains include forced txs via L1 immediately in the next L2 block in the order they appear on L1 (in particular, in the first portion of the first L2 block, right before L2 sequenced txs).

You could say that Bedrock already uses based sequencing but just for forced transactions.

---

**bruno_f** (2024-02-10):

I agree with [@donnoh](/u/donnoh) here. There’s no reason for an escape hatch to have a long timeout, that timeout can be arbitrarily small. The disadvantages that you mention are true of older escape hatch designs, but they have evolved quite a bit meanwhile (and it is a big design space, there’s more room for improvement).

---

**JustinDrake** (2024-02-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/donnoh/48/12917_2.png) donnoh:

> OP stack chains include forced txs via L1 immediately

![](https://ethresear.ch/user_avatar/ethresear.ch/bruno_f/48/8809_2.png) bruno_f:

> that timeout can be arbitrarily small

I don’t see how this can be compatible with unconditional preconfirmations on state. Let’s assume that a transaction `T` was force-included at L1 at slot `n` and the OP sequencer starts giving out unconditional transaction preconfirmations (on post-execution state, not just inclusion) which assume the execution of `T` at slot `n`. Now if slot `n` is reorged (e.g. via a depth 1 reorg) the execution of `T` may change, itself potentially invalidating the unconditional transaction preconfirmations.

[@donnoh](/u/donnoh): Do you have a link to how OP does immediate forced inclusions, and how they make them compatible with preconfirmations?

---

**donnoh** (2024-02-10):

I guess OP preconfirmations are weaker than Arbitrum’s. The spec of the transactions list derivation can be found [here](https://github.com/ethereum-optimism/specs/blob/b1c9b7985b65bd2d065a414f5ad0552f36e48540/specs/protocol/derivation.md#deriving-the-transaction-list).

---

**JustinDrake** (2024-02-13):

[@bruno_f](/u/bruno_f): I think I concede your point—it’s possible for non-based rollups to enjoy the full censorship resistance benefits of Ethereum L1, all while enjoying preconfirmations ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Thank you for bringing this up—a significant update to my mental model! If liveness is not one of the fundamental advantages of based sequencing then I guess the two big remaining advantages are a) credible neutrality, which is critical for a shared sequencer and b) L1 compatibility, necessary to have synchronous composability with L1 contracts and $0.5T of assets.

I think my favourite preconfirmation design so far is preconfirmations that are conditional on the L1 state. That is, if the L1 reorgs then the corresponding preconfirmations no longer apply. I believe these L1-conditional preconfs work fine because a preconfirmer at slot n can offer two types of preconfirmations in parallel: preconfirmations assuming the block at slot n-1 doesn’t get reorged, and preconfirmations assuming the block at slot n-1 does get reorged (e.g. falling back to the block at slot n-2 being the parent block). There can also be an insurance market to hedge users against reorgs (which should be rare, especially with single slot finality).

---

**JustinDrake** (2024-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> it’s possible for non-based rollups to enjoy the full censorship resistance benefits of Ethereum L1

Actually I take that back ![:see_no_evil:](https://ethresear.ch/images/emoji/facebook_messenger/see_no_evil.png?v=12) If an L2 transaction is force-included at L1 and the L2 sequencer has been compromised (e.g. so that the sequencer is no longer settling anything) then that L2 transaction can’t execute until after some timeout. This timeout can’t be made arbitrarily small because otherwise that would completely break preconfirmations. To summarise, based sequencing gives the same settlement guarantees as the L1 (no need for a timeout to force settle).


*(11 more replies not shown)*
