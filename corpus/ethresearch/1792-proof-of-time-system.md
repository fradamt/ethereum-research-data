---
source: ethresearch
topic_id: 1792
title: Proof of Time System
author: ArrowThunder
date: "2018-04-21"
category: Consensus
tags: []
url: https://ethresear.ch/t/proof-of-time-system/1792
views: 2524
likes: 0
posts_count: 1
---

# Proof of Time System

# Introduction

An attempt is made to define a strategy that will produce non-fungible

time consensus.

## The Problem

The problem being solved is taken from the problems section of the wiki

on Etherium’s github repository.

> 2. Timestamping
>
>
> An important property that Bitcoin needs to keep is that there should
> be roughly one block generated every ten minutes; if a block is
> generated every day, the payment system becomes too slow, and if a
> block is generated every second there are serious centralization and
> network efficiency concerns that would make the consensus system
> essentially nonviable even assuming the absence of any attackers. To
> ensure this, the Bitcoin network adjusts difficulty so that if blocks
> are produced too quickly it becomes harder to mine a new block, and if
> blocks are produced too slowly it becomes easier.
>
>
> However, this solution requires an important ingredient: the
> blockchain must be aware of time. In order to solve this problem,
> Bitcoin requires miners to submit a timestamp in each block, and nodes
> reject a block if the block’s timestamp is either (i) behind the
> median timestamp of the previous eleven blocks, or (ii) more than 2
> hours into the future, from the point of view of the node’s own
> internal clock. This algorithm is good enough for Bitcoin, because
> time serves only the very limited function of regulating the block
> creation rate over the long term, but there are potential
> vulnerabilities in this approach, issues which may compound in
> blockchains where time plays a more important role.
>
>
> Problem: create a distributed incentive-compatible
> system, whether it is an overlay on top of a blockchain or its own
> blockchain, which maintains the current time to high accuracy.
>
>
> Additional Assumptions and Requirements
>
>
>
>
> All legitimate users have clocks in a normal distribution around
> some “real” time with standard deviation 20 seconds.
>
>
>
>
> No two nodes are more than 20 seconds apart in terms of the amount
> of time it takes for a message originating from one node to reach
> any other node.
>
>
>
>
> The solution is allowed to rely on an existing concept of “N
> nodes"; this would in practice be enforced with proof-of-stake or
> non-sybil tokens (see #9).
>
>
>
>
> The system should continuously provide a time which is within 120s
> (or less if possible) of the internal clock of >99% of honestly
> participating nodes. Note that this also implies that the system
> should be self-consistent to within about 190s.
>
>
>
>
> The system should exist without relying on any kind of
> proof-of-work.
>
>
>
>
> External systems may end up relying on this system; hence, it
> should remain secure against attackers controlling  regardless of incentives.

While the problem being solved was thusly defined, the actual solution

has some substantially different parameters, much of which have been

generalized.

## Premise and Assumptions

The problem assumes that there is network composed of N nodes, which can

communicate with each other reliably. The solution relies on several

assumptions, many of them stemming from the initial problem. They are:

- The network size N is sufficiently large (roughly >2000 active
nodes, more on that later)
- Messages broadcast from any node will be reliably heard no more than
some period of time \Delta {\operatorname{net}} after
they were initially transmitted.
- This network performance does not decrease, even if every node in
the network were to each broadcast a message simultaneously. Yeah,
this is a fun one.
- The actual delay for a given message between two nodes is random and
follows a known distribution whose shape, formula, relevant moments
etc. are known.[1]
- Each node has a clock which measures the cumulative passage of time
at the same rate as that of every other node.
- The population of honest clocks reporting
\Delta {\operatorname{net}} = 0 are normally distributed with a known standard deviation of \sigma.
- At any given block in the chain, no more than k reputable nodes
are malevolent or inactive, where 2 k + 1 = N.[2]
- Nodes never timestamp their own messages. Self-timestamping
invalidates a message and is an offense punished by the network.
- All meaningful messages are broadcast to all nodes in the network.
That is not to say that less distributive transmissions cause
failure, but rather that they risk being functionally disregarded by
the network.
- All meaningful messages are signed by their sendors. Unsigned or
malsigned messages are to be disregarded.
- At least one node in the network is altruistic. Objectively
speaking, if 2000 nodes can’t meet this requirement, the blockchain
probably deserves to fail.

Some futher defintions are provided below:

// TODO (active nodes, reputable nodes, nonreputable nodes, honest

nodes)

# The Strategy

The strategy is composed of 5 key elements. They are:

1. Modeling Algorithm, used to interpret a sample of timestamps.
2. 3-Stage Voting, used to achieve consensus.
3. Keystone Genesis, used to bootstrap consensus of the genesis block
timestamp, providing a fixed reference point.
4. Recursive Improvement, using the existence of even low-accuracy
concurring timestamps to improve the performance of the system,
allowing for the creation of more accurate and secure timestamps.
5. Reputation System, used to incentivize and minimize the impact of
common attack strategies.

## Modeling Algorithm

Diving right in:

Contaminated Sample: A statistical sample of which an unknown subset has

been falsified by intelligent attackers in a way that leaves no

distinguishing characteristics between the subset and the set except for

the data itself. All elements of that subset are ’contaminated values’.

Sifting Model: A statistical model attempting to obtain information from

only the non-contaminated elements of a contaminated sample.

Intelligent Attacker: An actor with complete knowledge of the sifting

model that will be applied to the data, who acts with the intent to

alter the infromation obtained from the sifting model in some way,

shape, or form. All intelligent attackers are potentially conspiratory

and cooperative with each other.

It is impossible for a sifting model to obtain uncompromised information

from a contaminated sample whose contaminated values make up more than

half of the sample.

Theorem 4 is a natural extension of May’s Theorem (which essentially

states that majority rule is the only “fair” binary decision rule),

applied to contaminated samples.

If there is nothing known about the population distribution of the

uncontaminated elements of a contaminated sample, no effective siftng

model can be created.

An effective sifting model’s maximum tolerance of a sample’s deviation

from its population distribution and the model’s maximum error from

contamination are inversely proportional.

An effective sifting model’s maximum contamination error is directly

proportional to the variability of the uncontaminated population

distribution being modeled.

Corollary 7 is key, because it makes it imperative that the variability

of the clocks in the network be reduced as much as possible. This will

be done in subsection 5.

### The Basic Sifting Model

Despite the subsubsection title, creating even the most basic model took

several weeks of contemplation, testing, and math. Omitting the somewhat

circular journey and cutting to the chase, there are exactly five

general steps the basic model that was implemented in R. Other practical

sifting models will likely need to follow these same steps, even if they

are taken in different ways.

1. Generate a weighted and unweighted kernel density function of the
sample with a fixed bandwidth. The weights are derived from the
reputation of the node providing the data.[3]
2. Approximate the kernel density function with a smoothed spline f_s
  (x) generated from a series of coordinates on the kernel density
function that include the range of the sample data. This is done
because actually calculating the kernel density function every time
you need it in the next few steps would be a terrible nightmare.
Generate another, f_{s_w} (x) for the weighted kernel density
function.
3. If the population has a propability distribution
D \left( \mathtt{}
  x, \mu \right), let the modeling function be defined as
f_m (x, \bar{x},
  k) = kD (x, \bar{x}).
4. Maximize \int^{\infty}_{- \infty} F (x, \bar{x}, k)
  dx with respect to both \bar{x} and k, where
F (x, \bar{x}, k) = \left\{ \begin{array}{ll}
       f_m (x, \bar{x}, k) {,}& f_s (x) \leqslant f_m (x, \bar{x}, k)\\
       I (f_m), & f_s (x) > f_m (x, \bar{x}, k)
     \end{array} \right\} where I is a function, typically
less than 0, that varies depending on the exact implementation. Note
that 0.5  that is based on a non-normal distribution
shouldn’t be too difficult and is left as an exercise for the
reader.
2. That said, I think the system would sleep a lot better at night if
the attacking population was < 33%. As you get past that, it just
gets too easy to significantly influence the outcome of the model.
Of course, this is a subjective cutoff on a smooth continuum, but
3. While the weighted version & information derived from it technically
are outside the definition of a sifting model, it seems unlikely
that any realistic implementation would avoid their usage.
