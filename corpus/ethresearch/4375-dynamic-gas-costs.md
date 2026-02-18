---
source: ethresearch
topic_id: 4375
title: Dynamic gas costs?
author: nullchinchilla
date: "2018-11-25"
category: Economics
tags: []
url: https://ethresear.ch/t/dynamic-gas-costs/4375
views: 2453
likes: 0
posts_count: 4
---

# Dynamic gas costs?

Is it possible to have a system where the gas costs of different EVM instructions is determined by some on-chain voting mechanism similar to the mechanism used to decide the block gas limit? Basically, for each block, the miner can adjust the cost of each instruction up or down by at most 1%.

It seems like such an approach will be able to avoid DoS vectors due to mispriced instructions, as well as accomodate future advancements in hardware that might make the relative costs of instructions drastically different (say, if elliptic-curve instructions in CPUs become commonplace, the elliptic curve instructions’ gas cost could be downvoted).

Furthermore, it seems like such a mechanism can also be extended to contracts, or at least pure-function contracts that use a fixed amount of gas. Every time a miner runs such a contract, it could up/downvote a “discount factor” tied to the contract in the state tree that discounts the gas price of calling that contract from another contract. This would allow contracts whose real cost to the miner is less than the sum of its instructions (say, due to interpreter optimizations) to have a lower gas cost. It might also allow the elimination of precompiled contracts; we can instead implement then in EVM on-chain, but hard-code an optimized implementation and a discount factor in clients.

Is there something wrong with such a system? Would bad actors be able to manipulate the costs in a cryptoeconomically problematic way? I vaguely recall [@vbuterin](/u/vbuterin) mentioning that he once considered dynamic contract costs but rejected it since it’s not incentive-compatible, but I don’t see any obvious reason dynamically pricing instructions and contracts can lead to abuse that doesn’t also apply to dynamically adjusting the block gas limit.

## Replies

**drstone** (2018-11-25):

Awesome to see more discussion on this. I’ve been researching very similar ideas, working off of the resource pricing paper and common ideas around mechanism design and learning with limited feedback.

Distributed, adaptive pricing of opcodes is another consensus problem. Whether or not you inherit the security of the underlying consensus protocol is a starting assumption, but from there if you can design a scheme that identifies honest participation (i.e. a fork choice rule but for non-malicious price updates/votes) you should be able to price goods with respect to a sensible objective function.

Consider a traditional BFT based blockchain with known validators. I’ve been interested in embedding a bandit learning algorithm in the client’s software to vote to explore or exploit a la traditional decision making under uncertainty. All participants submit their vote for a new set of opcode prices, potentially within some bounded range such as 1% from the previous.

Say that n=3f+1 where f denotes the amount of faulty nodes we would like to tolerate. We assume that all honest nodes run said protocol out of the box and thus need only devise a modified multi-armed bandit algorithm that reaches consensus on something like the median proposed price for each opcode (each arm is a menu of prices). Median mechanisms are less prone to being swayed with non-truthful responses as averaging mechanisms. Furthermore, we actually aggregate the submissions once 2f+1 updates are proposed where the aggregation function is a median, average, or arbitrary mechanism and submit the aggregated result as the posted prices of opcodes.

Alternatively, one can search for subsets of proposed updates from the f+1 pricing updates that minimize some geometric property such as is done in some byzantine gradient descent research. Plainly put, if you can identify the submissions of honest nodes, the network should allow some global objective function to converge to a maxima; that is, a set of prices that attempts to optimize against the current but unknown distribution of users and miners. Miners are included because there is some negative externality forced onto online miners even when they are not block proposers (as they have to validate transactions at changing gas prices). This should protect you from so-called bad actors if you assume the bad actors f fraction of the system’s power.

A really interesting part of implementing this correctly is in constructing a relatively correct objective function that can serve as the global network’s utility. Contrary to what you wrote, if elliptic-curve instructions because extremely commonplace then maybe people are willing to pay more for them? Looking at it purely from a pollution standpoint, lowering the prices could lead to large increases in usage to the point where it imposes large negative externalities on smaller miners and quantities of hardware, and thus lowering the decentralization. Miners running a protocol like this can be not only faulty but rational, seeking profit maximization over social welfare.

In any case, it seems like a really interesting entry point for learning based methods in economically-driven consensus protocols.

---

**nullchinchilla** (2018-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/drstone/48/946_2.png) drstone:

> Looking at it purely from a pollution standpoint, lowering the prices could lead to large increases in usage to the point where it imposes large negative externalities on smaller miners and quantities of hardware, and thus lowering the decentralization. Miners running a protocol like this can be not only faulty but rational, seeking profit maximization over social welfare.

This would only happen if most miners have a relative cost for elliptic-curve operations drastically different from that of most users, which means miners have very different hardware, which is going to lead to centralization no matter how you dice or slice it. So I don’t think price-voting by itself causes more centralization pressure.

Another thing to mention is that if votes can only be for “increase price by 1%” “decrease price by 1%” “don’t change price”, then we don’t actually need to use medians or an explicit voting system to prevent faulty miners from corrupting the consensus. If faulty nodes get to be block proposers less than half of the time, then they simply cannot affect the price.

Consider the case where the true cost of an opcode is 100 gas, but faulty nodes want to downvote it to 0. Every time a faulty proposer downvotes the cost to 99 gas, the next proposer is going to upvote it to 100. Essentially whenever the price is less than 100 it undergoes a random walk where going up is more likely than going down at every step. The result is that unless the faulty nodes have a majority, the price is going to bounce up and down very slightly below 100. In fact the price is going to be stable when exactly the same amount of people want a lower and higher price — i.e. the median!

So I don’t think miners that aren’t block proposers need voting rights at all.

---

**drstone** (2018-11-26):

Right, but under this construction you progress very slowly and naively in reconstructing the demand distribution. You protect against adversaries who want to harm prices but not adversaries that will prevent progress, i.e. consensus on optimal values w.r.t the chosen objective function.

I don’t necessarily agree that we know the true cost of an opcode too, but the goal of using a learning protocol with limited feedback would be to approximate the true cost with respect to the current distribution of users/buyers.

