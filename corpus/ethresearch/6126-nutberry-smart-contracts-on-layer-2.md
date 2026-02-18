---
source: ethresearch
topic_id: 6126
title: NutBerry - smart contracts on Layer 2
author: pinkiebell
date: "2019-09-10"
category: Layer 2
tags: []
url: https://ethresear.ch/t/nutberry-smart-contracts-on-layer-2/6126
views: 2704
likes: 6
posts_count: 4
---

# NutBerry - smart contracts on Layer 2

# NutBerry(Jelly) - Offroading Ethereum Transactions

I’m thrilled to announce the upcoming release of a permissionless layer 2 solution

with support for smart contracts, aka the NutBerry Project.

The design is similiar to what we generally call `rollups` but it intentionally has the same transaction encoding

and signing scheme as Ethereum transactions to be one-to-one compatible with the existing ecosystem.

The most anticipated feature is the possibility for on-chain EVM verification, that makes it possible to

run smart contracts on a permissionless / trustless layer 2 solution.

Though, the runtime has some restrictions like not be able to call other contracts.

I call that a `state-minimized EVM` or `LEVM` - Lean Ethereum Virtual Machine.

So, unlike PoA, PoS or other forms of `custodial` { child, side }-chains, the NutBerry `offroading engine` as I call it

is not another blockchain. Data availibilty is fully archieved on the root-chain and the contract is able verify and replay

all transactions either through directly finalising a blob of transactions on-chain (if you are in a hurry)

or via an interactive computation verification game to offload the computation but

enforce correctness on-chain for a given transaction blob.

# Roadmap

- 1st Milestone
Supports only the ERC20 token standard.
(Already does that via a fixed smart contract)
- 2nd Milestone
Going to support the ERC721 standard.
- 3rd Milestone
Support stateless smart contracts.
- 4th Milestone
Stateful smart contracts, aka smart contracts with support for storage.

All resources will be published on [NutBerry · GitHub](https://github.com/NutBerry)

once the first milestone is complete.

Ask me anything ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

## Replies

**pinkiebell** (2019-11-01):

![:flexed_biceps:](https://ethresear.ch/images/emoji/facebook_messenger/flexed_biceps.png?v=14)Released ![:ship:](https://ethresear.ch/images/emoji/facebook_messenger/ship.png?v=14)

https://github.com/NutBerry/stack

---

**johba** (2019-11-01):

> LEVM - Lean Ethereum Virtual Machine

sounds cool ![:partying_face:](https://ethresear.ch/images/emoji/facebook_messenger/partying_face.png?v=12)

---

**pinkiebell** (2019-11-02):

[@johba](/u/johba) Thanks for asking ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I’m cross-posting the question here for everyone else:

> is nutberry using optimistic rollups?

> At the moment I would call NutBerry a half-optimistic rollup
> The reason is that it can verify a block by replaying on the root-chain but NutBerry doesn’t use state-roots or intermediate state roots yet.
> And if the block is too big to be replayed on the root-chain, NutBerry relies on the verification game alone to resolve the outcome.
> (Btw, using the verification game is default modus operandi)
> But after implementing a gated  computing model I can basically remove the negative aspects of the dispute game,
> together with state-roots NutBerry will actually  become a optimistic rollup system

