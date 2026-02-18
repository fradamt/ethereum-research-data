---
source: ethresearch
topic_id: 5071
title: Nitro Protocol - generalized, n-party state channel networks
author: tomclose
date: "2019-02-27"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/nitro-protocol-generalized-n-party-state-channel-networks/5071
views: 2356
likes: 6
posts_count: 3
---

# Nitro Protocol - generalized, n-party state channel networks

[Nitro protocol](https://eprint.iacr.org/2019/219.pdf) is completely specified protocol for building generalized, n-party state channel networks.

The high-level overview of the approach is as follows:

1. We set up an on-chain system of balances. Balances can correspond to both participants and channels.
2. We view a state channel as a device that allows a fixed set of participants to reach an outcome by executing a multi-party application.
3. The outcome can be used to update the balances on-chain, including allowing one channel to pay out to another.

The strength comes from the fact that, armed with the knowledge that the outcome *could* update the balances on-chain if required, it becomes possible for the parties to do the majority of the rebalancing off-chain.

This approach decouples the operation of the state channels from the network that they are part of, allowing the state channels to update independently and making it easier to reason about their behavior. We don’t require atomic updates across multiple channels (e.g. the Counterfactual root nonce) nor do channels acquire additional constraints from being part of at the network (e.g. the validity time limit seen in the Perun approach).

In the paper we present two protocols:

- Turbo Protocol: enables ledger channels, allowing multiple channels between the same set of participants to be supported by a single on-chain deposit.
- Nitro Protocol: enables virtual channels, allowing a set of participants who share on-chain deposits with a common intermediary to open a channel without a shared on-chain deposit of their own.

The bulk of the paper is spend presenting constructions/procedures in these two protocols, including partial withdrawals and top-ups for ledger channels and an example of a 3-party virtual channel. We also provide algorithms for calculating the value attributable to each channel/participant in the network and develop the theory for reasoning about the correctness of the protocol.

We have a [v1 implementation](https://github.com/magmo/force-move-games/blob/1db5aef84f83e64d0635c2d6b657e6afc5251543/packages/fmg-nitro-adjudicator/contracts/NitroAdjudicator.sol) of the protocol in solidity and are currently working on client/server code to allow us to run a state channel application on top of it.

## Replies

**jfdelgad** (2019-04-06):

Had gone through the paper, this is really interesting. I have a question.

In Turbo, when participants A and B that have a ledger channel L create a sub-channel L', how the system controls for instance, A not collaborating on closing the sub-channel?, can B submit the outcome of L' to the adjudicator directly for resolution?, is this implemented already?, the procedure in this case is application dependent or does Turbo have a general procedure to deal with this cases?

---

**tomclose** (2019-04-06):

Ledger channels are just regular state channels that happen to be used for the purpose of funding other channels. If A stops signing updates, B can launch a challenge (i.e. a “force-move”) on chain, just as they would in a regular channel. B can’t force A into making the update but they can claim the current outcome.

To see how this works in practice, it’s probably worth looking at exactly how ledger channels function. Ledger channels run the consensus game. In the two player case, the consensus game has two types of state, with the following transitions (here \omega_1 and \omega_2 are *outcomes*):

Finalizable(\omega_1) \rightarrow Propose(\omega_1, \omega_2)        *[propose a new outcome]*

Propose(\omega_1, \omega_2) \rightarrow  Finalizable(\omega_1)       *[reject proposal]*

Propose(\omega_1, \omega_2) \rightarrow Finalizable(\omega_2) *[accept proposal]*

Finalizable(\omega_1) \rightarrow Finalizable(\omega_1) *[pass (optional)]*

The other important fact here is the default outcome for both Finalizable(\omega_1) and Propose(\omega_1, \omega_2) is \omega_1. This means that if a challenge is launched in either one of those states and there is no response before the timeout, then the outcome \omega_1 will be finalized in the adjudicator.

So, what does it mean for A to not collaborate on closing the sub-channel? It means that B has moved to some state Propose(\omega_1, \omega_2) in channel L and A is refusing to move to Finalizable(\omega_2).

The first (and most likely) option here is that A is just not moving at all. In this case, B would launch a challenge on the state Propose(\omega_1, \omega_2). One of three things then happens:

1. The challenge expires and \omega_1 is finalized on-chain. In this case the sub-channel can’t be closed off-chain. Instead B needs to transfer funds out of L to L' on-chain, separately finalize the outcome of L' on-chain and then use this outcome to transfer and withdraw their share of L'. This is a hassle, but B does have a path to claiming the funds they are owed.
2. A responds to the challenge with an acceptance, providing the state Finalizable(\omega_2). In this case, we are done: the channel closing can now be continued off-chain.
3. A responds to the challenge with a rejection, providing the state Finalizable(\omega_1).  In this case, B can then challenge on the Finalizable(\omega_1) state. As this is A's state, only B can respond, so they have the power to let the challenge timeout. The outcome \omega_1 is then finalized on-chain and they can proceed as in step 1. (An alternative to challenging on their opponents state is to make a transition to a conclude state, which leaves open the option of skipping the timeout if A decides to cooperate.)

The other option here is that A does respond off-chain but with a rejection. This case then plays out in the same way as option 3 above, where A responded with a rejection on-chain.

All of this is already implemented with the [basic implementation of the protocol](https://github.com/magmo/force-move-games/blob/bbd57b06a6a469ec9ec45e707e7d719029237145/packages/fmg-nitro-adjudicator/contracts/NitroAdjudicator.sol), as you don’t need anything more than the standard channel challenge mechanisms and the rules of the [consensus game](https://github.com/magmo/force-move-games/blob/bbd57b06a6a469ec9ec45e707e7d719029237145/packages/fmg-nitro-adjudicator/contracts/ConsensusApp.sol).

