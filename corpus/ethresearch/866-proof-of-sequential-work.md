---
source: ethresearch
topic_id: 866
title: Proof of sequential work
author: JustinDrake
date: "2018-01-23"
category: Cryptography
tags: [proofs-of-sequential-work]
url: https://ethresear.ch/t/proof-of-sequential-work/866
views: 4176
likes: 2
posts_count: 14
---

# Proof of sequential work

Let `A` be a sequential work algorithm with constant size intermediary states and solution. (For example let `A` be the hashchain proof-of-work algorithm which starts with a seed `s` and sequentially computes hashes `SHA3^i(s)` for `i = 1, 2, ...`. A solution for `A` is an integer `i` such that `SHA3^i(s) < D` for some difficulty `D`.)

We propose solution proofs for the sequential work algorithm `A` which are constant size and take constant time to verify:

- Crypto-economic proof: Miners make TrueBit-style claims for solutions to A. The game validity is asserted and checked in constant space and time.
- Eventually-cryptographic proof: Miners post collateral promising to deliver, within a certain time period, a cryptographic proof (SNARK/STARK) that a claimed solution to A is valid. Both the initial crypto-economic game and the final cryptographic proof take constant space, and are checked in constant time. (Notice straight-up SNARKs/STARKs would not be satisfactory because the work to produce them is parallelisable and dominates A's run time.)

## Replies

**kladkogex** (2018-01-25):

A solution that I like works in the following way:

1. You have a peer-2-peer network of nodes, where less than, say, 1/4 of nodes are bad.
2. You then randomly pick say, 32 nodes out of the network.  The probability of having all of them bad is (1/4)^{32} which is of the order of 10^{-20}. So at least one of them will be good.
3. If all nodes report the same result, then you accept the result. This is the fast path.
4. If at least one node is bad,  you go through the slow path, where you run the same thing on 256 random nodes, and take the majority solution.   The probability that the majority of 256 randomly picked nodes is bad will be negligible.  Then you slash deposits of all minority nodes.
5. If one of the minority nodes disagrees, it can pay for running the problem on twice the number of nodes.  This doubling continues, until no one objects.

A problem I see with Truebit, is that it is impossible to mathematically estimate probability that only bad guys validate the solution, and good guys will miss it.  So actually there is no rigorous probabilistic model.

In the scheme proposed above,  one can clearly prove that probabilistically the correct solution will be used.

---

**truja** (2018-01-27):

If the majority determines distribution of rewards, then there exists some incentive to create Sybil identities.  Therefore the assumption that only 1/4 of nodes are bad may not be realistic.

---

**denett** (2018-01-27):

If you make the chance of being picked proportional to the amount deposited by the node, you can assume less than 1/4 of the deposited ether belongs to bad nodes. Now Sybil has to bring a lot of ether.

---

**truja** (2018-01-29):

I don’t think 1/4 is stable.  The attacker could use the task rewards to incentivize token holders to add deposits to his pool.  Existing lazy nodes, who want to receive rewards without exerting the effort of performing computations, might join as well.

---

**denett** (2018-01-29):

Lazy nodes will get kicked out. If a node is chosen and it does not produce a result , it will get kicked out of the pool. If it produces bad results it will get slashed.

You could design the system in such a way, that a lazy node cannot just copy the work of an other node. For example by first letting every node show SHA(node_public_key,SHA(job_id, result)). After all nodes have shown this hash, they then all show a hash of SHA(job_id, result).

If the nodes disagree on the result, you can ask other nodes to verify, without the result being public (using a different job_id off course).

---

**truja** (2018-01-29):

The attacking pool operator can broadcast “result” to its constituent nodes in order to avoid replication of work.

---

**denett** (2018-01-30):

I guess you are right, once you reach 1/4 of the node, you do not have to do any extra work, because you are already in 99% of all random groups of 16 nodes.  As a pool it is hard to do this work distributed and trust less, because then you have to solve the original problem. So best would be for the operator to set up the server park. Now the operator increases his stake as long as the reward is bigger than the interest rate.

So you likely will end up with a monopoly or an oligopoly.

I guess any proof of stake system has the same problem, once you are running a node, you do not have to do a lot extra validating work when you add more stake. Difference being that the entrance fee for running a Ethereum node is a laptop instead of a server park.

---

**denett** (2018-01-30):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> A problem I see with Truebit, is that it is impossible to mathematically estimate probability that only bad guys validate the solution, and good guys will miss it.  So actually there is no rigorous probabilistic model.

The number of challengers per forced error tell you something about the expected number of independent verifiers per job. Artificially increasing the number of challengers is costly, because it will lower the reward.

Maybe it is possible for the system throttle the number of concurrent jobs, if the number of challengers per forced error drop below a threshold.

---

**clesaege** (2018-02-01):

For a Trubit like scheme, you don’t need forced errors, you can allow multiple reporters putting a security deposit. If all reports are the same, consider the result valid, otherwise, use interactive verification.

You can model the % of cases where only bad guys would report in regard of the reward they can get by having a dishonest result accepted, the reward for honest submission and the size of the security deposit.

That would be some game where there is no pure Nash equilibria:

-If everyone does the computation and reports honestly, the reward which is necessarily limited, will not be enough to compensate the work to find the solution.

-if no one reports, you should have reported assuming the reward for one party reporting is higher than the computation costs.

-if only bad actors report and you did not, you should also have reported because you would have been able to win your interactive verification games against them.

This result that the Nash equilibrium is a misted one, An interesting research direction would be to know what should the deposits and reward function be to lower the probability that no one reports.

A challenge is to avoid reporters having incentive to make multiple reports in order to have a higher part of the reward. An interesting research direction is to divide by 2 the reward for each report such that you should always report only once. The non used reward can be put in a vault to subsidize further rewards.

The subsidy should be capped to avoid an attack similar to the jackpot ballooning attack(see appendix of Trubit WP) where the attackers report multiple time, even if that means less immediate reward, but more delayed reward to it an increase of the vault size leading to an increase in subsidies of further rewards.

I call this problem the “honest unity” problem and it has applications outside of computation (making an Oracle from a dispute resolution system where parties can answer question and use a dispute resolution system if the answers are conflicting and where we need at least one party giving an honest answer).

---

**kladkogex** (2018-02-03):

![](https://ethresear.ch/user_avatar/ethresear.ch/truja/48/640_2.png) truja:

> The attacking pool operator can broadcast “result” to its constituent nodes in order to avoid replication of work.

Since the nodes are randomly picked, in order to an attacker to form a pool like that, the number of nodes in the pool needs to be a significant portion of the total number of nodes, since nodes a picked randomly.

I do not think having nodes with arbitrary deposits is a good idea, one needs to have a standard deposit value for each node.

TrueBit has very much the same multiple identity problem  - the same node can be used with two identities both for computation and for verification.

In the scheme above, the multiple-identity problem can be solved easily by passing mutated code to the nodes from time to time and slashing deposits of nodes with multiple identities.  This completely addresses the “centralization” risk.

---

**denett** (2018-02-05):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> TrueBit has very much the same multiple identity problem  - the same node can be used with two identities both for computation and for verification.

Yes, but in TrueBit there is no gain in creating more identities. More identities mean that you are more often selected as a Solver, but you are allowed to verify all tasks. A solver and a verifier earn the same reward, so you need only one identity to earn the maximum reward.

As long as the reward is bigger than the calculation costs, new nodes have an incentive to participate.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> In the scheme above, the multiple-identity problem can be solved easily by passing mutated code to the nodes from time to time and slashing deposits of nodes with multiple identities.  This completely addresses the “centralization” risk.

How does this work? If you send mutated code to a node, they will notice the the task is different and will need to calculate the task. You can make them do useless work, but are not able to slash them.

---

**kladkogex** (2018-02-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> How does this work? If you send mutated code to a node, they will notice the the task is different and will need to calculate the task. You can make them do useless work, but are not able to slash them.

Good point :-))

Which makes me think that what needs to be done is to always mutate the code, but to have  two types of mutations:  trivial mutations that do not change the end results, and ones that that do - if calculations involve crypto this could be probably done in mathematically rigorous way - interesting subject

---

**denett** (2018-02-05):

I checked the TrueBit whitepaper and I see that the Solver is not automatically the first verifier, but receives only a fraction of the jackpot in case there is no verifier. So when the solver does not expect many verifiers, it might be profitable to also be a verifier.

I think it would be better for the solver not to have an incentive to have double identities and just give the solver the full jackpot.

