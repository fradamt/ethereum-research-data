---
source: ethresearch
topic_id: 16781
title: "Recovering from smart contract hacks: Forkable, Reversible Roll-Ups"
author: josojo
date: "2023-09-28"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/recovering-from-smart-contract-hacks-forkable-reversible-roll-ups/16781
views: 1333
likes: 1
posts_count: 5
---

# Recovering from smart contract hacks: Forkable, Reversible Roll-Ups

**Tldr:**

We are proposing a new kind of roll-ups that can reverse and recover from serious failures, such as bugs in smart contracts, all without relying on multi-signatures.

# Motivation:

Cryptocurrency technology embodies the principle that “code is law,” establishing a transparent and open system for financial transactions. However, this “code” is not infallible, and sometimes unforeseen bugs and challenges emerge, potentially resulting in substantial financial losses.

To operate under normal conditions with the crypto ethos, but still address this weakness, we propose the development of forkable, reversible roll-ups that allow for the reversal of problematic transactions without depending on central trusted entities. These roll-ups enable creating a system that can essentially “undo” errors and thereby protect users and their assets.

# Design:

## Design Idea:

Every user holding an RWA trusts the RWA issuer. This roll-up construction facilitates this existing trust to enable state reversals for hacked contracts.

## Forkable Roll-up:

In simple terms, a forkable roll-up is a roll-up with the ability to fork itself: it can create a copy of itself to isolate and address issues without affecting the original chain. To do so, the original chain splits into two paths, each operating independently with their own unique identifiers (chain IDs) and continuing to record their own transactions. One fork will have a modified state - with a deployed fix for a bug - while the other fork will be the normal chain. Users can choose freely which fork to adopt: Either the one with a state update or without.

The value of each fork can then be assessed based on trading activities in the primary layer (L1), helping users to identify the more valuable option between the two.

## Forkable Roll-up bridges:

There are two kinds of bridges for forkable roll-ups:

1. #### Majority Chain Bridge:

This bridge works like a normal L2 bridge and can hold any assets. After a fork, it automatically sends assets to the new fork’s bridge of the chain with the highest value.

1. #### Real World Asset bridge:

RWA will be bridged into a forkable roll-up by a bridge from L1 with an owner - ideally the RWA issuer. After a fork, the bridge will send the funds to the new child bridge of the fork that is chosen by the owner of the bridge. It is expected that the owner will send the funds to the chain with the higher marketcap, unless an attack is started against the open interest of the chain. If the owner is the RWA issuer, there is no additional trust assumption for a user.

With these definitions, we can define a reversible forkable roll-up:

## Reversible forkable roll-ups:

Reversible forkable roll-ups are roll-ups that are able to recover from severe smart contract issues. They will fork each time a hack has repercussions beyond a certain threshold measured in dollars.

Then they go through two phases:

Phase 1: Containment fork:

Bots are proposing a fork that contains the hack: E.g. they set the state of the chain to the state right before the hack and freeze the vulnerable contracts - maybe by setting the bytecode of the affected contracts to zero. This will prevent the hack + restore all funds that are not yet bridged away from the chain - which can be prevented by having a delayed bridge. These forks can be triggered by bots automatically and hence are initiated quickly (only some blocks after the attack). Users can then choose the most promising containment fork and use it for their business needs.

Phase 2: Resolution fork:

These forks will unfreeze the vulnerable contract and replace it with a fix. This for sure is much harder to organize than a containment fork and will take more time and coordination. However, it should eventually happen for each containment fork. Again users will have the choice of which fork they actually follow and RWAs issuers will likely follow the chain with the highest market value.

# Analysis:

The presented roll-up builds a framework that allows to change the state in a trustless - non-multisig - manner with the following assumptions:

- Assumptions for assets in the Real World Asset bridge: Assuming the users are trusting their RWA issuer - this trust is required for any RWA - and this issuer controls the bridge, then the only additional trust in this construction taken by each user is that the RWA issuer is technically and legally able to choose the right fork for representing their RWA after a fork. In most cases this act of choosing a fork should be trivial: The market will likely decide which chain should be picked by forking and trading the forked native tokens on L1. The issuer only needs to read the onchain price and pick the fork with the higher valuation. Only in unexpected situations the market could fail and RWA issues would have to investigate the situation more deeply. But even a “wrong choice” by the issuer is not in all cases fatal as users in most situations withdraw the RWA assets to L1 from any fork.
- Assumptions for assets in the Majority Chain Bridge: For anyone holding non-forkable L1 native assets in the forkable chain that are deposited via majority-chain-bridge, there are also economic incentives securing their assets as long as the value of all the deposited L1 native tokens is less than the market cap of the native token in L2. If the L1 native assets are less valuable than the L2 native token, then the cost of manipulating the value of the L2 forks is - in a market with perfect information - higher than any potential gains from stealing L1 tokens and thereby not worth any profit-oriented attacker.

## Replies

**MicahZoltu** (2023-09-29):

This introduces a very hard dependency on the rollup having a native asset that is valued higher than the total value of all other assets on the chain.  Current rollup design doesn’t require *any* L2 native asset (though many rollups tend to add one for various reasons) but there is nothing that ensures the L2 native asset is worth more than the sum of the bridged assets.

---

**josojo** (2023-09-29):

No. I disagree. I think the majority of assets on such an appchain would be RWA secured via the described RWA’s bridges.

If the value of RWA’s is much higher than value of the native token, someone could try to manipulate the value of the forks - by manipulating the value of the native token -, but RWA issuers would observe it and prevent any obvious attack by using their power in the bridges.

This does not extend any trust assumption as the trust in RWA issuers is needed in the first place for anyone owning RWAs.

Note that attacks on the system will be very obvious as an attacker needs to deploy a smart contract fix for a contract that has no vulnerability. IMO this is easy to find out for RWA issuers and prevent the fix

---

**MicahZoltu** (2023-09-29):

Even if we ignore all RWAs and fully accept your argument for them resolving as you have described, the dependency I described still holds true.  Any L1 assets bridged to the L2 can be stolen (in their entirety) by someone who is able to upgrade the contracts.  Whether this “upgrade” happens through some forking mechanism, or through a multisig, or a DAO vote doesn’t change the fact that an actor with the ability to change the L1 contracts has the ability to drain all of the bridged assets.

If you want economic security (meaning no profit motive to execute an upgrade/forking attack) and the L1 contracts follow the L2 branch with the highest market cap of the L2 native token, then you need the L2 native token to have **at least** 2x the value of the sum of the assets at risk.  In this case, the assets at risk are all of the assets sitting in the bridge contract on L1 (not including RWA assets, if we accept that some centralized actor can independently route them).

---

**josojo** (2023-09-29):

yes, what you are saying is right: L1 assets bridge via the Majority Chain Bridge are only save as long as the assumption on market caps holds (as I wrote in the original post in the analysis section).

But the point of this whole construction is that we can have a forkable, reversible appchain where users can hold all kinds of RWAs (tokenized t-bills, bonds, stocks etc.) and they can even be secured from hacks leveraging the trust that exists already in holding these assets.

I am very sorry, if the text did not make that clear…

Yes, the chain is not ideal for L1 native tokens: it has only small capacity for native blockchain assets like ether, but given that the amount of RWAs are soon much bigger than the crypto native assets, I find this construction quite valuable and interesting.

