---
source: ethresearch
topic_id: 1819
title: Another way of understanding what cryptoeconomic aggregated signatures do
author: vbuterin
date: "2018-04-24"
category: Cryptography
tags: [signature-aggregation]
url: https://ethresear.ch/t/another-way-of-understanding-what-cryptoeconomic-aggregated-signatures-do/1819
views: 2581
likes: 1
posts_count: 2
---

# Another way of understanding what cryptoeconomic aggregated signatures do

Background: [Cryptoeconomic signature aggregation](https://ethresear.ch/t/cryptoeconomic-signature-aggregation/1659)

A cryptoeconomic aggregate signature (CAS) allows a node to make a claim of the form “either this sample of validators all signed off on what I am building, or I am burning my deposit”. This could be used as an ingredient to make forking in chains (scalable or otherwise) less likely and more expensive.

Here is how this would work. Suppose that you have a chain-based protocol, but creating a block requires adding a CAS from a sample of 200 validators, which sign off on their belief that the block is building on top of the current head at the time. If a CAS is later found to be fraudulent, then the block is still valid, but the creator gets penalized. If we trust that the majority of validators will refuse to sign blocks that do not build on what they think is the current head, then building a chain that reverts the current main chain would not be impossible, but it *would* cost the validators an entire deposit for each block that they attempt to revert.

The scheme can also be extended as follows:

- Validators can be constrained with Casper FFG-style slashing conditions (NO_DOUBLE_VOTE and NO_SURROUND) preventing them from contradicting their previous votes.
- If signatures are included in a CAS in block N, then randomness revealed in block N+1 could select a few signatures from block N for which the proposer of block N+1 could reveal the Merkle paths, rewarding the signers.

If we can incentivize signers to publish their signatures most of the time, then we could have a notion of client-side finality, where clients could passively watch for signatures (which would also be required to be votes in a global Casper FFG cycle) and accept some block as justified if 2/3 of a global validator set votes for it (and finalized if it and its direct child are justified), though the chain would not have consensus on whether or not finality happened at any specific point in time.

## Replies

**marckr** (2019-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If we trust that the majority of validators will refuse to sign blocks that do not build on what they think is the current head, then building a chain that reverts the current main chain would not be impossible, but it  would cost the validators an entire deposit for each block that they attempt to revert.

This is key, and the core problem as I see it with PoW, regardless of economic externalities.

This seems a UX problem, in the incentives for the signers. I recently came across Swarm and the several working groups thereof and I really have to say, I hold in high esteem what Ethereum is working on yet again.

Signatures however, aggregated in this manner, is a light treatment of any cryptoeconomic incentive. I read the Casper FFG paper practically when it came out, and the finality is absolutely vital, however the incentives are unclear when seen through anything but cryptography, that is it may presuppose quite a bit. It will take some effort to create validator sets that actively sign blocks as a part of their independent operation. As the state propagates forward, the fidelity of NO_DOUBLE_VOTE is paramount to ensure proper and faithful execution of the underlying consensus. There cannot be double dealing, but it relates vitally then to the staked tokens and the conditions thereof. I would like to think the cryptographic layer is one step closer to the metal as far as the human decisions that might be made above.

I believe there are mechanisms that could allow for incentivizing desirable actions such as the Bayesian Truth Serum, reversing the situation as it were. Was interested in IOTA initially for this reason in fact. I have to dig through all these print outs, and well my incentive to communicate and edit is rather low.

These are core challenges however. What is the constraint on not publishing a signature? Are you viewing this as predominantly an incentive problem with respect to client-side finality?

How is the validator set determined? Simply through money staked, is that intended to be endogenous from the system or from outside financial interest? I recently saw some of the mathematics for the ETH 2.0 economics in this [js](http://hackingresear.ch/libs/economics-eth2.js) file. It might not be a financial problem as far as the yield. It is most importantly a matter of incentivizing at the cryptographic layer proper action, otherwise we just have a whole mess.

