---
source: ethresearch
topic_id: 3134
title: ELI5 Plasma vs Polkadot
author: schone
date: "2018-08-29"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/eli5-plasma-vs-polkadot/3134
views: 2648
likes: 6
posts_count: 10
---

# ELI5 Plasma vs Polkadot

As much as I try to read about the two, I don’t understand how they’re different from one another.  Aren’t they both protocols for creating subchains or para-chains which are secured by an oversight chain?

How do the two differ and what does each offer?

## Replies

**fubuloubu** (2018-08-29):

Not sure if the protocol for Polkadot changed since I saw a presentation on it last year, but the main difference would be that in Polkadot it would be the “master” chain, and in Plasma Ethereum is typically the master or root chain.

Plasma also has the exit procedures which gives it different trust properties than Polkadot, which leverages the validators on each chain it connects to validate.

Things have probably changed though, I know that they have the “Parity Bridge” in the architecture now.

---

**MihailoBjelic** (2018-08-29):

Similarities:

1. One root chain (Ethereum mainnet in Plasma, Relay chain in Polkadot)
2. Many child chains (Plasma chains in Plasma, Parachains in Polkadot)
3. Mostly centralized child chain block proposers (Plasma operators in Plasma, Collators in Polkadot)

Differences:

1. Polkadot has platform-wide, shared security (big pool of validators that get randomly sampled to validate child chain blocks and “checkpoint” them to the Relay chain), while Plasma doesn’t (Plasma operators validate and checkpoint blocks themselves, and users have to constantly monitor their behavior).
2. Polkadot plans to support smart contracts and other advanced stuff (synchronous inter-chain communication/contract calls/transactions…) from the beginning, while Plasma plans to deal with those complexities in latter iterations.
3. Plasma has “exits” i.e. an option to move funds to the root chain by submiting a transaction to it directly (no Plasma operator action is required), while Polkadot doesn’t.
4. Plasma is not a single project, but more of a design philosophy/set of guidelines, and Polkadot is a single, specific project.

Hope this helped. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**schone** (2018-08-29):

Correct me where I’m wrong here.  Do they both provide more or less the same end product? Albeit a tad differently in the details of implementation

If they’re not the same, how would the end products differ.  What would be the use case for having them both, an implementation of Plasma protocol and an implementation of Polkadot?

[@MihailoBjelic](/u/mihailobjelic) is Plasma a protocol specification while Polkadot a proposed concrete implementation of a slightly different idea for relatively the same end product?

---

**MihailoBjelic** (2018-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/schone/48/4894_2.png) schone:

> Do they both provide more or less the same end product?

Plasma has no “end product”, or it will have a number of them, depending on how you want to look at it.

![](https://ethresear.ch/user_avatar/ethresear.ch/schone/48/4894_2.png) schone:

> What would be the use case for having them both, an implementation of Plasma protocol and an implementation of Polkadot?

There are so many use cases for both. Different businesses/organizations have different needs, so I truly believe Plasma and Polkadot can and will co-exist. Think of Linux and Windows.

![](https://ethresear.ch/user_avatar/ethresear.ch/schone/48/4894_2.png) schone:

> @MihailoBjelic is Plasma a protocol specification while Polkadot a proposed concrete implementation of a slightly different idea for relatively the same end product?

Again, Plasma is a design philosophy, a high-level specification for building layer 2 blockchains secured by the Ethereum blockchain, and a number of specific implementations will be derived from it (we already have Plasma MVP and Plasma Cash, and there will be more of them). And I wouldn’t say Plasma and Polkadot slightly differ, there are important differences in the aspects of technology, flexibility, community support, root chain security, timelines etc.

---

**kladkogex** (2018-08-30):

For Plasma a Plasma operator is centralized, it is just a guy, not a set of guys.

Polkadot is a chain of nodes, so it is still decentralized. This is my humble understanding of Polkadot.

---

**kfichter** (2018-09-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> For Plasma a Plasma operator is centralized, it is just a guy, not a set of guys.

Plasma chains can be secured by a PoS mechanism instead of a single operator, if desired.

---

**kladkogex** (2018-09-03):

Does this need to be a fork-less PoS ? I do not think Plasma considers forks or re-orgs in the Plasma chain.

---

**kfichter** (2018-09-03):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Does this need to be a fork-less PoS ?

Not necessarily, especially if you allow a Plasma block time < ETH block time. But typically the root chain contract won’t allow forks anyway.

---

**0zAND1z** (2018-09-25):

Thanks to all participating in providing clarity.

However, this doesn’t seem like research material.

Closing the topic for now.

