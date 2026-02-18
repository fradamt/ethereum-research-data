---
source: ethresearch
topic_id: 3047
title: Event-driven smart contract development
author: sinamahmoodi
date: "2018-08-22"
category: Applications
tags: []
url: https://ethresear.ch/t/event-driven-smart-contract-development/3047
views: 5064
likes: 10
posts_count: 10
---

# Event-driven smart contract development

**TL;DR:** The goal of this project is to allow smart contracts to subscribe to events emitted from other contracts, on-chain and in a verifiable manner.

### Introduction

Event logs produced within the context of a transaction are only accessible off-chain and by querying clients. Enabling smart contracts to take action based on these events, could potentially introduce interesting use cases.

### Related Work

The architecture resembles two others, namely, oracles and subscription-based payment models.

It can be seen as an oracle, the query response of which is Ethereum transaction data. Current oracles usually have a pull-model, where the contract requests their required data from an off-chain source. The proposed approach however, employs a push-model, where any normal event emitted by any contract could potentially trigger the invocation of some subscribers. This means, contracts could subscribe to events from already deployed contracts. The downside being that, they have less control over how often their callbacks are invoked.

Moreover, the mechanism could allow conditional delayed execution, meaning, the end user would not need to start a transaction manually, and actions could be taken conditional on the occurrence of an event elsewhere in the network. It can be seen as a generalization of the current subscription-based payment models. The difference being that it’s not only for payments, and the actions need not take place at regular intervals. However, regular events can be achieved for example with the help of a cron contract that incentivizes users to emit events at regular intervals. This generalization however comes at a cost.

### Method

A `Registry` contract would store subscription information, and additionally deposits from subscribers and the price they’re willing to pay per invocation. Upon emission of an event, if there are any subscribers with an `offer >= gasEstimation`, miners would submit the event log data, along with a proof that the log exists within a particular block, to the registry, earning ether, and causing the invocation of the subscriber’s callback. Because it’s the miners who pay the gas fee, it might be possible to improve UX by making some of the transactions async, and having other means of funding them.

Ideally, the verification could be done via a merkle proof that shows log `l` is in receipts trie of the block `b` with block hash `h` (`b` should be among the most recent blocks, as contracts only have access to most recent block hashes, and older events are probably not useful anyway), or if such a proof is infeasible or inefficient, via zero knowledge proof systems. In the worst case, it would be necessary to revert to stakes and challenge games, which would introduce some delay from the emission of an event, and its corresponding callback being invoked, and additionally would have weaker guaranties.

### Implementation

You can find a very primitive example of a `Registry` (along with a subscriber and an emitter) [here](https://github.com/planet-ethereum/call-me). The incentive and proof parts are still being worked on.

### Final Remarks

Thanks for reading the proposal. I apologize in advance if there are glaring mistakes in the proposal, we’re less experienced than many here, and as such we’d love to hear your feedback on whether you think this is a direction worth pursuing, and if so, how it can be improved, the possible attack vectors, the verification, etc.

## Replies

**sg** (2018-08-22):

(Implementation link is broken)

---

**sinamahmoodi** (2018-08-22):

My bad, sorry, fixed.

---

**sdtsui** (2018-08-28):

Is the idea here that miners would have an incentive to read from chain and emit log data?  I’m not quite following why we would want miners to pay the gas fee.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/s/f04885/48.png) sinamahmoodi:

> Upon emission of an event, if there are any subscribers with an offer >= gasEstimation , miners would submit the event log data, along with a proof that the log exists within a particular block, to the registry, earning ether, and causing the invocation of the subscriber’s callback.

---

**sinamahmoodi** (2018-08-28):

Thanks for your comment.

First I have to clarify that the term miner here doesn’t necessarily refer to Ethereum miners. it refers to someone who:

1. watches events from chain
2. checks if anyone is subscribing to this event via the registry
3. If so, calls the subscriber’s callback function

And it is in the 3. step that the miner has to pay gas for calling the callback. Now, in order to compensate for the gas fee, and additionally, to incentivize the miner to do this, the subscriber offers to pay a certain amount.

As to why we’d want this: we don’t *want* this per se, and it is an inevitable consequence of the current proposal, that the miners have to pay the gas fee. However, in some cases, it could improve the UX by not requiring the user to send a transaction manually, and paying gas on it, e.g. a user would receive the reward of a bet they participated in automatically, without them needing to claim it.

---

**lsaether** (2018-08-28):

We’ve been working on a similar concept in our work on conditional execution. The idea is that a user can schedule a transaction which will be executed only under certain conditions which will be reflected in the state of smart contracts.

For example, a user can create a stop-loss contract for their Melon Fund in which an asset is sold off “automatically” when it reaches a price threshold, granted that there exists an on-chain oracle which provides this data.

This is accomplished through a layer 2 execution market (what you’re calling miners). These executioners get passed signed messages of users who wish to schedule transactions. They parse the signed message to determine which contracts to watch and for which states of the contracts need to be triggered. When the states of the contracts fulfill the specific conditions, the executions submit the transaction on chain. Using yet another smart contract, we can ensure that the transaction is submitted exactly as it was specified by the signing user. In this case, the signing user doesn’t ever need to pay gas as it’s handled by the executioner. But we expect some kind of incentive being necessary for the executioner to continue to run.

---

**hemulin** (2018-08-28):

An initial flow of communication is proposed [HERE](https://github.com/planet-ethereum/call-me/wiki/Workflow).

Perhaps you’ll find it contributing to the discussion or making the idea clearer.

*Copy Paste from the above link:*

## Suggested workflow overview

- A registry contract is being deployed, its address is being published in a publicly accessible location.
- A miner declares that he is supporting events communication over that registry.

#### The registry holds two main structs:

1. Mapping (emittingEventContractAddress, eventType) => (subscriberEventContractAddress, functionToBeInvoked, invokationBounty)
2. Mapping eventSubscriberContract => balanceOfSubscriberContract

#### The registry contains (at least) the following functions:

1. addEntry - Adding an entry to mapping (1)
2. getBalanceOf - Retrieving the current balance of subscriber from mapping (2)
3. addToBalanceOf - Adding value to the balance of a subscriber
4. invokeEvent - Recieving the event that was mined and a proof (TBD) for that event.
5. rewardMiner - Transfer bounties from subscirbers to an event miner
6. removeEntry - Removes an entry from mapping (1) and return remaining funds in mapping (2)

Now to the flow:

1. Devloper which requires event handling logic, estimates the gas required for executing his callback function.
Then calls the addEntry and lists:

which event he is interested in
2. which callback function should be invoked upon recieving that event.
3. Funds as he see fit to invoke the callback function.

Those should include (the invokation gas + a bounty to incentivize miners to publish events mined) * initial number of times he wishes that eventHandling to take place.
4. Event of type E is being emitted from a contract.
5. Miner M (the publisher) is mining that event and calls the invokeEvent.
6. The registry varifies E using the proof provided with it.
7. Upon successful varification, the registery invokes the callback function of all the subscribers that are listed for E, using capital from their registry balances (mapping (2)).
8. Regisgtry invokes rewardMiner transferring all the bounties from the above subscribers to M.

***Note, it is up for the subscriber contract to validate its funds at the registry and update them accordingly to meet its needs.***

---

**HarryR** (2018-08-28):

I’ve been working on a similar system recently, it’s event driven although it isn’t a subscription model where smart contracts subscribe to events - the user must push through proof that an event occurred to trigger the next state in a smart contract.

See: https://github.com/HarryR/panautomata

The first example which demonstrates the event driven nature is https://github.com/HarryR/panautomata/blob/master/solidity/contracts/example/ExamplePingPong.sol

This creates a ‘Ping Pong’ session between two contracts, it’s started on contract A by calling `Start`, then proof of that `Start` transaction is provided to contract B via `ReceiveStart`. If contract B accepts the transaction it emits a `Ping` event, proof of the event is provided to contract `A` via `ReceivePing` which in turn emits a `Pong` event which is provided to `ReceivePong` on contract `B` which then emits a `Ping` event - and the two contracts loop forever. A sequence/nonce and a session ID are used to ensure correct ordering etc.

The mechanism I’m using for on-chain proofs of transactions and events are short merkle tree proofs, e.g. there is a daemon which must be trusted to periodically and honestly compact all of the events and transactions which occur in each block and publish the root hash in-sequence to an on-chain contract ([LithiumProver.sol](https://github.com/HarryR/panautomata/blob/master/solidity/contracts/LithiumProver.sol)).

The interesting thing about this is that any event or transaction from any block-chain can be proven on any other block-chain as long as there is a trusted and regularly updated sequence of merkle roots accessible to that contract.

I’ve provided another example, [ExampleCrossToken.sol](https://github.com/HarryR/panautomata/blob/master/solidity/contracts/example/ExampleCrossToken.sol), which allows you to lock tokens on chain A then redeem them on chain B, you can then burn the tokens (or an arbitrary number of them) to redeem the equivalent value on chain A again - this ensures the tokens will only be in one place at any point in time.

However, this doesn’t work with Ethereum block headers so you can’t verify authenticity of transactions or events from the same chain within the last ~256 blocks. But, there is a project which uses proofs of events and transactions against block headers @ https://github.com/clearmatics/ion - when proving against the same chain within the last ~256 blocks it wouldn’t be necessary to have an external trusted daemon to upload the block headers, but the proofs of events and transactions become quite large (e.g. to prove an event you must provide it with the full transaction receipt - see [EventVerifier.sol](https://github.com/clearmatics/ion/blob/ion-stage-2/contracts/EventVerifier.sol). If used correctly that would provide a trustless mechanism for verifying recent events from the same chain.

From @lsaethers example, if there where an event emitted by the fund whenever the price changes, miners could provide proof of it automatically and trustlessly to your contract in return for a reward.

It should be relatively straightforward to adopt the LGPL-3+ code from Ion to do the same-chain event proofs. Or use https://github.com/lorenzb/proveth

---

**tucker-chambers** (2018-09-30):

Could part of the protocol feature an automatic gas refund function, which is funded by a part of subscribers’ fees? Maybe it could even be managed by the protocol you are proposing – if a miner (your definition) calls a subscriber’s callback function, that is recognized as an event, the consequence of which is the triggered refund of the gas amount. Hope that makes sense.

---

**sinamahmoodi** (2018-09-30):

Thanks a lot [@HarryR](/u/harryr) for the really helpful resources and explanations, and [@lsaether](/u/lsaether) for the interesting conversation here and at ETHBerlin which helped me see some of the challenges ahead.

Borrowing code and ideas from ion, panautomata, proveth, etc., the [ethbase](https://github.com/planet-ethereum/ethbase/blob/master/contracts/Verifier.sol) PoC now verifies the inclusion of a log in one of the most recent 256 blocks via MPT proofs sent from [relayers](https://github.com/planet-ethereum/relay-network/blob/master/ethbase/proof.go).

The next focuses are the [collision issue](https://github.com/Meta-tx/Harbour-MVP/issues/3), and [preventing](https://github.com/planet-ethereum/ethbase/issues/6) “double spends” (submitting the same event twice). Another direction being considered, is to integrate this with identity proxies (smart contract wallets), and enabling users to schedule actions being taken on emission of events.

![](https://ethresear.ch/user_avatar/ethresear.ch/tucker-chambers/48/2360_2.png) tucker-chambers:

> Could part of the protocol feature an automatic gas refund function, which is funded by a part of subscribers’ fees?

Hey [@tucker-chambers](/u/tucker-chambers), thanks for the suggestion. Although the incentive layer is not yet concrete, it would most likely encompass what you mentioned in some form. The relayers (new preferred term for miners), would be compensated for the gas cost of submitting events, which comes from the subscription fees. However, it might turn out not to be a direct deal between subscribers and relayers, as batching events and submitting them as “blocks” is also being considered. In that case, a relayer would be submitting multiple events, each of which, might be of interest to multiple subscribers, which entails multiple subscribers chipping in to pay for each event they care for.

