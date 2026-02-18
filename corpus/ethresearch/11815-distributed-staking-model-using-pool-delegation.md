---
source: ethresearch
topic_id: 11815
title: Distributed staking model using pool delegation
author: basememara
date: "2022-01-19"
category: Economics
tags: []
url: https://ethresear.ch/t/distributed-staking-model-using-pool-delegation/11815
views: 1630
likes: 0
posts_count: 4
---

# Distributed staking model using pool delegation

The [staking delegation model Cardano](https://cardano.org/stake-pool-delegation/) uses is quite brilliant and wondering if we could do something here with the merge.

The idea is I stake everything in my wallet by delegating it to a pool provider and I still get to use all the funds in my wallet freely. The rewards are from the funds I’m not using in my wallet and collect staking rewards on it, like a savings account. It’s a native feature and safe in that pool provider can’t withdraw funds, they just use what’s available for staking purposes of their node.

The beauty of this is it makes the whole network more decentralized, with further guards in place like if pool providers get too big, the rewards diminish for delegators so they’ll find a less saturated pool for higher earnings. And just to add, this will take the power away from large financial institutions and put it back into the hands of the people, being facilitated natively by the protocol; Ethereum will effectively be a distributed bank.

I’m not shilling but honestly admiring and researching the tech out there and seems like it would be great for an Ethereum2 world. Does anyone know of any discussions or proposals along these lines? Any thoughts or feedback would be greatly appreciated!

## Replies

**MicahZoltu** (2022-01-23):

Staking in Ethereum specifically requires locking up your assets for an extended period of time so that you can be punished after-the-fact for bad behavior.  There are some types of behavior that are not decidably bad until sometime in the future, and in some cases they can only be identified extra-protocol.  For this reason, it is critical that assets that are staked are not “usable” while they are staked.  They **MUST** be locked up.

---

**basememara** (2022-01-24):

That makes more sense that funds would be locked up. Other chains like Cosmos has a 21-day locking period for example which seems fair but runs on an entirely different security model.

Currently, the closest thing to distributed staking to secure the network is RocketPool, which has done amazing work. This was something that was greatly needed to spread staking participation.  It seems for this to be natively included in the protocol would require a specification to be created for Ethereum wallets to connect to delegated validators and create a contract between them.

---

**MicahZoltu** (2022-01-25):

The problem with distributed staking is that ultimately *someone* needs to be in charge of decision making, and ideally we want that person on the hook for all of the losses for making bad decisions.  If you have 9 ETH worth of people delegating decision making to a one ETH worth person, then that decision maker has 10x leverage, which means if they do a bad thing they lose 1 ETH but they get to do 10 ETH worth of bad.

There are some situations like a group of real life friends or family that can make this work, because the connection costs are far higher than the assets being pooled.  However, for an pseudo-anonymous/decentralized staking pool system you have no such off-chain connections with pool participants, so it just gives leverage to would-be attackers.

