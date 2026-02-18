---
source: ethresearch
topic_id: 1640
title: Incentivizing full state nodes
author: MicahZoltu
date: "2018-04-07"
category: Economics
tags: []
url: https://ethresear.ch/t/incentivizing-full-state-nodes/1640
views: 5862
likes: 6
posts_count: 5
---

# Incentivizing full state nodes

Note: Very similar to the topic being discussed at [Incentives for running full Ethereum nodes](https://ethresear.ch/t/incentives-for-running-full-ethereum-nodes/1239), but I wanted to have a focused discussion on this particular mechanic.

## Problem

As running a full node becomes more and more expensive due to the cost of storing and maintaining full state, we need a way to incentivize multiple parties to *actually* store the full state.

## Solution

- Periodically, the system asks everyone to commit (encrypted) what is at a particular address in state.
- Anyone can commit that they know what is at that address along with staking some amount of coins.
- Some time later (short duration) everyone reveals what they believe is at that address.
- Anyone who is right, gets a share of minted coins proportionate to their stake.
- Anyone who is wrong or doesn’t reveal loses their stake.

## Implementation Detail Problems

- How to choose what data to ask for?  Want random selection, but also want the answer to not be 0 99% of the time.

## Issues

- The target data becomes unavailable between the start of the round and the reveal phase as a selfish miner does not want to share the data during this time.  IMO, this is acceptable but it does pressure the rounds to be short (maybe just a few blocks).
- An attacker can subvert the system by running a full node and sharing data during the rounds.  This attack would be to make it so the system doesn’t realize that full nodes are disappearing because they are not being rewarded.  It is an odd attack, but I don’t have a great solution for it.
- Proof pools.  Someone can run a full node and then sell answers to the question to users in exchange for a small fee.  Due to merkle tree magic, it is possible for this information sharing to be trustless, and with ZK proofs you can even (in theory) prove that you have the information prior to sharing it.  This could result in a single actor running a full node and selling the information to others during the round.  The saving grace here is that anyone can “break” this system by buying the data from the pool (at as low cost as possible) and then making it public for free.  This devolves into something similar to the attack mentioned above.

Given the above issues, it feels like the worst case scenario is “no worse off than now” with no incentive to run a full node and some minted coins (inflation) being distributed to anyone who participates in the degenerate system and the best case scenario (no attackers) we are rewarding people who run full state nodes via some minted coins.

I’m curious if people have any other thoughts on what is wrong with such a system or ideas on how to resolve any of the above problems?

## Replies

**jamesray1** (2018-04-08):

> IMO, this is acceptable but it does pressure the rounds to be short (maybe just a few blocks).

There is a related scheme in sharding which has been recently proposed: [A general framework of overhead and finality time in sharding, and a proposal - #3 by jamesray1](https://ethresear.ch/t/a-general-framework-of-overhead-and-finality-time-in-sharding-and-a-proposal/1638/3). It should be inspiration for your proposed scheme.

---

**ldct** (2018-04-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Someone can run a full node and then sell answers to the question to users in exchange for a small fee.

Seems like you want full nodes to provide non-outsourceable proofs of custody (of blockchain state). The file-storage coins (Filecoin, Storj etc) have the same problem but for user data. I also remember Sergio Lerner had a devcon 3 talk about this idea of paying full nodes to store blockchain state.

As for specific protocols, Justin’s one at [Enforcing windback (validity and availability), and a proof of custody](https://ethresear.ch/t/enforcing-windback-validity-and-availability-and-a-proof-of-custody/949) is the only one I’ve read in detail and I think it technically works for this use-case. In fact since ethereum blocks commit to the state root and Justin’s proof of custody is constant in the size of data stored (I think) you can just pay full nodes for storing the whole state. However the overhead introduced by snarks is probably too high.

You can probably find more protocols by googling for proof of {custody, retrievalibity, storage}.

---

**SylTi** (2018-04-10):

I love the idea, but without even talking about proof pool, what is stopping someone from participating while not running a node at all and getting is answers from infura?

---

**ldct** (2018-04-10):

That would be an example of “outsourcing a proof of custody” - e.g. if you try to do this in Justin’s scheme, infura would be able to steal all your eth

