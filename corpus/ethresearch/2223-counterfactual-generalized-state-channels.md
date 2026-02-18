---
source: ethresearch
topic_id: 2223
title: "Counterfactual: Generalized State Channels"
author: ldct
date: "2018-06-12"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/counterfactual-generalized-state-channels/2223
views: 4202
likes: 12
posts_count: 10
---

# Counterfactual: Generalized State Channels

Hello everyone,

I’d like to introduce the generalized state channels framework that L4 has been working on for the past couple of months. We released an introductory blog post at https://medium.com/statechannels/counterfactual-generalized-state-channels-on-ethereum-d38a36d25fc6 geared towards a more non-technical audience, as well as a technical paper at https://counterfactual.com/statechannels.

For existing readers of ethresear.ch, I think the best place to start would be to jump right in and read the paper ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

In the rest of this post I’ll highlight what we think are the important innovations we’ve introduced, especially with respect to the existing discussion on channels we’ve seen on this forum. I hope this list provides a good comparison to existing research and will provide a good jumping-off point for discussions.

# Latency

While many people discuss channels as a way to increase transaction throughput, we additionally highlight the latency-reduction benefits. Once a channel is set up, interacting within it only requires off-chain message exchange, hence the interaction finalizes instantly and we provide web-like response times. This is in contrast to non-channelized interactions (e.g., directly on ethereum, or on Plasma) where one normally has to wait for “confirmations” (or for some other finality metric, e.g., a finalized block in Casper). Channels are the only technology that provide this instant finality guarantee.

# Application-specific channels, generalized state channels, counterfactual instantiation, and multisigs

We introduce the concept of “generalized” state channels. In our terminology, an application-specific state channel runs a specific application (e.g., payments or chess), and requires an on-chain transaction to deploy before the specific application can be used. In contrast, a generalized state channel is one where new applications and functionality can be installed into an existing channel without any on-chain transactions. In particular, a user installing a new application into an existing channel experiences instant finality for installing the application.

In a generalized state channel, parties are able to enter into a contract (i.e. be bound by the terms of the contract) just by exchanging messages. We call the process of being bound by the contract, “counterfactually instantiating” the contract.

See sections 4.1.3 and 5.3 for more details.

# Multisigs

In our constructions, the only on-chain component of any individual state channel is a multisig wallet. This is possible due to counterfactual instantiation. This has privacy and upgradability benefits.

See section 5.4 for more details

# Counterfactual terminology

Counterfactual terminology is not a new feature we provide, but a useful way of thinking about state channels and many other L2 techniques. For any on-chain operation X, we say that “counterfactual X” holds when

1. X could happen on-chain, but doesn’t
2. The enforcement mechanism allows any participant to unilaterally make X hap- pen
3. Participants can act as though X has happened

This terminology is already useful when talking about existing payment channels. In that case, X could be “4 ether is transferred from the payment channel smart contract to Alice’s account, and 6 ether from the smart contract to Bob’s account”, and counterfactual X would be the state of affairs if both parties have the latest signed copy, which records Alice’s balance as 4 and Bob’s as 6.

We use this terminology to talk about counterfactual instantiation, counterfactual state, counterfactual state transitions, and counterfactual objects. This definition can also be adapted to talk about Plasma.

# Object-Oriented Approach

A generalized state channel can have many applications or instances of the same application going on at the same time. We organize this in an “object-oriented approach” that combines state and functionality, much like how ethereum contracts combine state and functionality.

See sections 5.5 and 5.7 for more details.

# Miscellaneous Features

One reason we think the way we think about state channels is fruitful is that it allows us to naturally support many features without any special effort:

- n-party channels for n > 2
- Instant closeout of a channel (i.e., releasing the funds to the owning parties without waiting for the dispute period; only possible if all parties agree)
- Partial withdrawal, where some amount of funds is taken out of a channel and moved elsewhere on-chain, without the channel being closed
- Top-ups, where some amount of funds is moved on-chain into the channel (e.g., in a payment channel, if your balance is running low, you can do a top-up into the channel to replenish your balance)
- Contracts that have some notion of time
- Contracts that depend on non-channelized on-chain state (e.g., betting with your friend within a channel on the outcome of some Augur market)

# State Channel Networks and Metachannels

In a payment channel network, two people who do not have a payment channel with each other but who have channels with some path of intermediaries to each other can still do a channelized payment to each other. State channel networks are the analogous constructions for state channels. Some existing work on state channel networks include:

- Perun’s “virtual channels”, at Perun: virtual payment and state channel networks
- Celar Network’s mediated conditional payments
- For payment channel networks: Lightning, Sprites

These different constructions present different usage models to the end-user. For example, with lightning or sprites style payment channel networks, the intermediaries have to cooperate for every payment, even if the same route is reused, whereas virtual channels don’t have this problem. The flip side is that per-payment routing might tie up capital for lesser amounts of time.

Our “metachannels” construction is an object-oriented approach to constructing state channel networks. In terms of usage model, is most similar to Perun’s virtual channels, but with some differences. Note that since generalized state channels support counterfactual instantiation, you can also do HTL-style payments within a network of generalized state channels, if desired.

See section 5.9 and 4.3.9 for constructions and discussions.

# Griefing

Analyses of griefing in state channels is under-explored in the existing literature. We explain different types of griefing possible, how it affects the threat model of channel users, and some mitigations in section 3, as well as mention some third-party services that can help in section 7.2.

# Definition and Limitations of Channels

The definition of “state channels” is not entirely consistent among researchers, and has recently provoked a friendly twitter war ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) For our definitions, interactions within a channel must proceed only by unanimous consent, and these interactions must have instant finality (except in special cases like partial withdrawal).

In section 7.1, we give a representative example of something that cannot be channelized (a public bounty).

## Replies

**tomclose** (2018-06-12):

Really excited to see this paper released! ![:tada:](https://ethresear.ch/images/emoji/facebook_messenger/tada.png?v=9)

Quick question on counterfactual terminology: when you say “X could happen on-chain, but doesn’t” should that be interpreted as “X could happen on-chain, but hasn’t yet”? Related to this: if the operation X does happen to be later enforced on-chain, does it transition from “counterfactual X” to “actual/factual(?!) X”?

---

**ldct** (2018-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/tomclose/48/3252_2.png) tomclose:

> should that be interpreted as “X could happen on-chain, but hasn’t yet”?

I don’t think there is a requirement that X eventually happens on-chain; eg in the payment channel example, if counterfactual X holds at some point in time, after the balance is updated, it no longer holds, and X never happens on-chain

> does it transition from “counterfactual X” to “actual/factual(?!) X”?

I think so, but the language we have around this is certainly not the best ![:stuck_out_tongue:](https://ethresear.ch/images/emoji/facebook_messenger/stuck_out_tongue.png?v=12)

---

**tomclose** (2018-06-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> I don’t think there is a requirement that X eventually happens on-chain

I wasn’t trying to suggest that it should be a requirement that it eventually happens on chain - rather that it should be clear that there isn’t a requirement that it *never* happens on chain. The wording “but doesn’t” seems like it could potentially be interpreted that way (e.g. “the sun doesn’t rise in the west” v.s. “the sun hasn’t yet risen in the west” ).

---

**ug93tad** (2018-06-26):

Let’s say Alice and Bob instantiated a new counterfactual object O (for chess, for example). They played until move N, then Alice wants to raise a dispute. What would she need to submit on-chain? Are they:

1. The signatures on the instantiation -> O will then be deploy
2. The signatures on move N-1 of the game -> the deployed contract for O will execute state (N-1)

Appreciate the clarification.

---

**ldct** (2018-06-26):

yeap, that’s the idea

---

**nrryuya** (2018-07-21):

Thank you for the great paper.

From my understanding, even after Alice raises dispute and the challenge period have finished, she can change the contract’s state with the functions other than update(). (e.g. Alice continues to play chess calling the function to change the chess board)

If so, how the contract authenticate the caller?

For example, the participants’ address are set in constructor and it is checked whether msg.sender is participant when the function is called.

---

**ldct** (2018-07-21):

> For example, the participants’ address are set in constructor and it is checked whether msg.sender is participant when the function is called.

Yes, this should be the way the contract authenticates that it is Alice

---

**nrryuya** (2018-07-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> Yes, this should be the way the contract authenticates that it is Alice

Thanks!

Does the isFinalized function of counterfactual object sometimes include not only nonce dependencies but also app-specific one? (e.g. in chess game whether the king has been dead or not)

Channels like payment channel might not need app-specific isFinalized condition, though.

---

**liam** (2018-07-21):

We only really describe in the paper the generic idea of conditional finalization but in practice there are several nuances. The main categories of situations when you want to use conditional finalization are:

1. Has a nonce been finalized at value n? (in some other approaches people use HLC too)
2. Has a state channel application’s state been finalized? (e.g., is the payment channel “done”?)
3. Has a state channel application’s state arrived at a conclusive state? (e.g., is the chess game “won”?)

For (3) you can of course have any generic function call, but in practice it’s much nicer to model your game as a state machine and have a notion of “terminal states” that can be queried. For example, in Tic Tac Toe you might have X_TURN, O_TURN, X_WON, O_WON, DRAW where of course X_WON, O_WON, DRAW are terminal states and X_TURN and O_TURN are “in play” states.

