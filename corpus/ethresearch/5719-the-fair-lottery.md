---
source: ethresearch
topic_id: 5719
title: The Fair Lottery
author: Joseph
date: "2019-07-08"
category: Consensus
tags: []
url: https://ethresear.ch/t/the-fair-lottery/5719
views: 5501
likes: 6
posts_count: 13
---

# The Fair Lottery

# The Fair Lottery

### Summary

The fair lottery is a thought experiment of a fictitious lottery. Each participant in the lottery is indistinguishable from any other entrant into the lottery. The probability of each entrant winning is uniformly distributed, regardless of the amount of tickets purchased.

### Rules of the Fair Lottery

1. All participants are indistinguishable
2. The number of participants is unknown
3. All participants must obtain at least one ticket
4. Each participant has equal chance of winning the lottery regardless of the tickets they hold
5. Winners of the lottery must be greater than 1 and less than the number of tickets sold

### Notes

I. Tickets can be free or sold

II. Lottery drawing can rely on provided entropy but is not required

III. *A participant is not discrete and can collude or collaborate with n other participants. A participant is abstract and represents a unified holder of tickets in the lottery.*

### Appendix



      [mathoverflow.net](https://mathoverflow.net/questions/155385/is-a-fair-lottery-possible)



      [![Maestro](https://ethresear.ch/uploads/default/original/3X/a/1/a1b0e91c9313e5d4297e41b292e4ab1cc128f4c2.png)](https://mathoverflow.net/users/45864/maestro)

####

  **pr.probability, st.statistics, game-theory**

  asked by

  [Maestro](https://mathoverflow.net/users/45864/maestro)
  on [12:59PM - 22 Jan 14 UTC](https://mathoverflow.net/questions/155385/is-a-fair-lottery-possible)

## Replies

**Joseph** (2019-07-08):

I would be interested in hearing people’s solutions. Feel free to comment in the thread for clarification.

---

**wanghs09** (2019-07-09):

A simple solution would be : use the random number from random beacon to get the winner.

You cannot get some solution more scalable and secure.

---

**Joseph** (2019-07-09):

The proposition isn’t about randomness, randomness can be provided externally. The question is regarding uniform distribution of odds of winning. A solution has implications for Sybil attacks.

---

**vbuterin** (2019-07-09):

This seems impossible unless you have a unique-identity solution; otherwise any participant can obtain multiple tickets and thus pretend to be two or more participants.

---

**Joseph** (2019-07-09):

That’s what makes it a fun problem

---

**sina** (2019-07-09):

The kernel of the problem statement seems to be “sybil resistance”. Since there’s no way to make proxy voting expensive or enforce identities, it seems impossible.

I believe the problem may be framed as “who gets chosen to create the next block” (ie. that’s the “lottery”). So from that framing, our current best-effort solutions in this space of PoW, PoS, and the like come to mind. But the result for these solutions isn’t that every participant gets equal chance of winning, since the identity mechanism can favor certain people (ie. someone with more hash power, or with more stake).

---

**vardthomas** (2019-07-10):

This is a problem that’s fun to think about. In terms of coming up with a “hard” solution, it seems impossible due to the fact that anyone can enter the lottery multiple times as long as they can obtain more than one unique ticket. It seems we would need to turn to game theory. You would need some kind of mechanic that either forces or encourages participants who hold more than one ticket to reveal themselves since this is the only  way to calculate their odds of winning.

---

**Joseph** (2019-07-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vardthomas/48/3487_2.png) vardthomas:

> It seems we would need to turn to game theory. You would need some kind of mechanic that either forces or encourages participants who hold more than one ticket to reveal themselves since this is the only way to calculate their odds of winning.

Exactly where my head is at right now

---

**ChosunOne** (2019-07-10):

I think it is fairly simple to prove the impossibility of such a system.  Here’s a sketch of a proof:

1. Assume you have a perfect lottery system, that satisfies all the properties stated in the problem.
2. Conduct the fair lottery and select a winner.

At this point, it is entirely possible for the winner to be a member of a completely out of band coalition of lottery ticket participants who have been forced or tricked into giving up their winnings should they be selected.

1. The organizer of this coalition collects the winnings, with probability proportional to the size of his coalition.

Thus unless you can enforce the constraints down to the basest level of physics you cannot have a provably fair lottery.  In fact, the stated constraints of the lottery creates incentives to attack other legitimate honest players, which is probably not what you want.

---

**Kaykutee** (2019-09-01):

***Joseph ", REALLY…now, let’s become great friends and share secret’s***

I want to know it all! I always knew I was going to achieve great things, Gods Plan.

I am wondering how Ethereum knew? Obviously, tracking my man hours of Labor on the Internet.I am so blessed, and grateful.

Thank You,

Ethereum

---

**plotozhu** (2019-12-11):

[![image](https://ethresear.ch/uploads/default/original/2X/5/5c8e0d20491e136cecb7f5819ac85494baccdfe2.png)image415×222 17.2 KB](https://ethresear.ch/uploads/default/5c8e0d20491e136cecb7f5819ac85494baccdfe2)

We have presented a new scheme called DDPFT—Dynamic Delegated Power Fault Tolerance, which should resolve this. It can be divided into three phases:

- Committee election:
 for every epoch, select a large scale of committee(about 1024 nodes). This can be done according to RANDAO algorithm.
- Block proposal :

For round n+1, on block of n’s  arrival, Get new VRF result: R_{n+1}={\rm signautre}c(R_n), where c is the codebase of block n, the new R{n+1} is published on block body.
- each node calculates its opportunity:   and  , where HMR is Hash of node M in round R, Opm is the opportunity for node M
- Fixed number, such as 99 or 149, of delegates for new round is calculated out accord to R, the can be those whose addresses are shortest distance to Rn+1
- Node delays for a while according to Opm and sends vote requests to those delegated after timeout if needed. Nodes who had sent vote request is called as candidates.
- Delegates should wait for a specified time to collect vote request as much as possible. After timeout, sort vote requests by Opm, and then create votes. Different votes have different priority, which is the order of sorted requests.
- Delegates send votes to each candidate.
- A candidate collects votes and calculates its weight, weight of node m is Wm.
- Node delays for a while according to Wm, then create and broadcast new block if no block with higher weight arrives.
- Time Delayed Broadcast:
On new block’s arrival, each node should delay and wait for a while on the block’s weight.

## Benefits:

1. Opm is according to node’s power, inspired by Filecoin, this power can be any measurable capacity of node, such as storage or just stake.
2. Block codebase gains most reward and delegates gets least, reducing incentive of delegates for signing in different fork.
3. Signing in different votes with same priority is easy to find and will be punished.
4. Delegates who abide specified time will have the most possibility to be rewarded, which will guarantee block generation time.
5. Block with more weight will be propagated faster and larger scale
6. Liveness assurance: If block with more weight failed, the least one will  propagated instead.
7. Fast finalization: Blocks with more that 50% of 1st priority are finalized.

The consensus is designed for multi-layer sharding system, any challenge and discuss will be very appreciated. This is the first time to post on ethresear.ch, should i create a new thread to discuss this?

---

**plotozhu** (2019-12-11):

Inspired by Filecoin’s EC,  measurable power may be used to against  Sybil attack.

