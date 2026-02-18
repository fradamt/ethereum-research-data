---
source: ethresearch
topic_id: 12307
title: Np-completeness of a strong form of scalability
author: jonreiter
date: "2022-04-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/np-completeness-of-a-strong-form-of-scalability/12307
views: 3850
likes: 4
posts_count: 7
---

# Np-completeness of a strong form of scalability

Curious thoughts on:

https://datafinnovation.medium.com/the-consequences-of-scalable-blockchains-8c4d23c6af4d

effective sharding is also np-complete in this framework (forthcoming result, but really an exercise for the reader)

This is a strong set of definitions and intended as a rigorous starting point nothing more.

## Replies

**experience** (2022-04-02):

Very interesting approach. The infamous scalability trilemma has been cited a lot the past few years and I’ve always wondered whether the general idea could be formalized as an impossibility result or if it was just a heuristic. This looks like a first step in this direction. Although not an impossibility result per se, if this work is correct, it would have strong implications because saying “we have a scalable blockchain”  would translate to “we solved the P vs NP conjecture” which would force us to take it with a kilogram of salt rather than just a grain.

As with all impossibility theorems, definitions are probably what’s most important here. I don’t have the skills to discuss the proof so I will focus on this. In particular here the term scalability is taken to mean *“can process more transactions per unit time than a single node on the network”*.

A question that immediately comes to mind is how this definition fits into the context of decoupling execution and verification layers, in particular with zk / validity  rollups wherein a single node “processes” transactions, but the validity of *batches* of transactions is guaranteed by nodes in the distributed ledger validators processing only the mathematical proof of validity, such that the end results seems to be a blockchain that can *effectively* process more transactions than a single node.

What is your view on this? Do you think this framework applies to such systems, and if yes what is the compromise or economic vulnerability?

---

**jonreiter** (2022-04-02):

we need to distinguish between average- and worst-case here.  the result concerns worst-case.  all that other stuff may well work great for the average (on average!).  the extension to sharding formalizes the worst-case problem.

so long as a worst case exists the system needs to be hardened for it.  fee spikes/liveness issues/etc are then inevitable sometimes. hardening requires accepting you have a problem (its the first of the 12, and last of the 5, steps!).

the case of public blockchains is particularly difficult as arbitrary smart contract code converts this design limit into exploits.  you can view that as putting the hard problem on the users – this has implications for perceived reliability/complexity of the system and ux in general.

---

**MicahZoltu** (2022-04-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonreiter/48/8910_2.png) jonreiter:

> we need to distinguish between average- and worst-case here. the result concerns worst-case. all that other stuff may well work great for the average (on average!). the extension to sharding formalizes the worst-case problem.

One of the goals (for me at least) for Ethereum is that fully trustless clients can be run on as simple/small of hardware as possible.  One can imagine a blockchain that “scales” by making it so almost all nodes in the system can run on low end hardware while you need a very small number (as low as one) who run on massive hardware.  In this case, by using zkProofs whatnot one can imagine the “worst case scenario” mattering only for the heavy node types in the system (that actually do full execution).  In this case, the system is still limited by how fast one node can process things, but we can accept that one node being incredibly powerful.

---

**jonreiter** (2022-04-06):

ok - different meanings of scaling i guess.  i think you are concerned that even v light clients can validate the network, or maybe push individual transactions and ensure they were handled properly. sure.

my concern is how to control future fees.  if you are limited to a single (albeit v fast) node’s throughput then it feels like it’ll be difficult to do that.  it’s not like the semiconductor industry isn’t already trying to build the fastest things it can – if you’re capped at a node, you’re capped at xyz manufacturer’s best.

will try to more carefully distinguish between “scalability of participation” and “scalability of transaction throughput” … the whole idea a network admits (requires?) a wide range of capabilities/scales for different sorts of functionality is interesting.  certainly more general than “assume all nodes are the same.”

---

**MicahZoltu** (2022-04-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonreiter/48/8910_2.png) jonreiter:

> if you are limited to a single (albeit v fast) node’s throughput then it feels like it’ll be difficult to do that. it’s not like the semiconductor industry isn’t already trying to build the fastest things it can – if you’re capped at a node, you’re capped at xyz manufacturer’s best.

Yes, this is true, but if one crazy fast piece of hardware is enough then that is fine.  With rollups, you can also scale horizontally to some extent, while also vertically scaling the roll-up settlement layer.

What about techniques where you can run two transactions in parallel when they don’t touch any shared state (this order doesn’t actually matter)?  One can imagine a design where that is the case and it could run faster than a single piece of hardware (this is functionally what rollups do, shard state access).

---

**jonreiter** (2022-04-14):

so the problem i’m thinking about is the tension among:

1 - those things (roll-ups, not sharing state) don’t always work, and reshuffling the network when needed is also a hard problem (its pretty much precisely set or vertex covering).

2 - if the network is somehow magically partitioned properly, yeah its fine. but how?

3 - without scaling scaling you’re stuck with whatever balance exists between demand and “intel/amd/nvidia’s best” at each point in time. when the fastest-available-now computer is no longer enough what can you do?

1 means fees can spike. and because it’s a smart contract platform you can cause the problem as an attack to raise fees etc. this is an unavoidable problem if its permissionless.  it’ll also happen randomly sometimes (because its possible). you can defend against the intentional version – but the “occasional” issue is surely unavoidable.

2 might be possible under some economic incentive / equilibrium condition.  but it feels like that would simply be a different form of fee spikes (i.e. get off this shard, fees are lower somewhere else). is that solvable? i don’t know.

