---
source: ethresearch
topic_id: 2178
title: Minimal Progammable State Channels
author: tomclose
date: "2018-06-08"
category: Layer 2 > State channels
tags: []
url: https://ethresear.ch/t/minimal-progammable-state-channels/2178
views: 2237
likes: 7
posts_count: 3
---

# Minimal Progammable State Channels

We wanted to share the **force-move games** framework - a small, proof-of-concept state channel framework capable of running 3rd-party ‘applications’. We will be publishing a white paper containing a full description of the framework and its capabilities in the coming weeks but the code is already [available on github](https://github.com/magmo/force-move-games). Along with the framework, we provide the contracts and client-libraries for a few example applications that can be built on top of it (the game of [rock-paper-scissors](https://github.com/magmo/force-move-games/tree/master/packages/fmg-rock-paper-scissors) and a [payment-channel](https://github.com/magmo/force-move-games/tree/master/packages/fmg-payments)).

The framework takes a pragmatic approach, sacrificing generality of the supported applications, for simplicity in the on-chain and off-chain logic. In particular, the framework can’t (yet) support any applications that have state transitions whose validity depends on time, or other properties that are external to the channel’s state. For example, as it currently stands, you couldn’t build a state channel sports betting game, where bets have to be made by a deadline and the winner is determined through an oracle feed.

Writing an application to run on the framework involves creating a smart contract that defines a set of states and a `validTransition` function, which specifies the allowed transitions. The framework provides a `forceMove` action through which a player can challenge their opponent on-chain to take a move. If their opponent doesn’t respond within the timeout period, the game ends and the players receive a ‘fair’ settlement, which depends on the current state and is determined as part of the application design process.

The framework doesn’t currently support ledger channels or virtual channels, so at the moment an on-chain deposit is required for each game played. We’ve tried to decouple the funding of the channels from their behavior though, to allow us to add support for ledger and virtual channels at a later date. This also allows the channels to run in other state channel setups, such as that being created by L4.

We’d like to thank L4 for all of their support, collaboration, and helpful discussions throughout, and James Fickel for providing the funding for this work!

## Replies

**liam** (2018-06-08):

Thinking about this framework has been very interesting to us as we’ve worked through the pros / cons of on-chain vs off-chain logic when designing second layer blockchain applications.

I think fundamentally this is a great immediate-term solution to get the benefits of state channels for individual standalone applications that people are thinking of building these days (e.g., battleship, crypto kitties battling, tic tac toe, things like that).

Currently I’m interested in seeing an example that abstracts the `turnNum` to be decided by the application (to allow for types of games in which the number of players / turns taken is dynamic per round.

---

**tomclose** (2018-06-19):

We’ve now released [the paper](https://magmo.com/force-move-games.pdf) that describes the framework and the motivations behind it in more detail. Any feedback/questions/comments welcome!

