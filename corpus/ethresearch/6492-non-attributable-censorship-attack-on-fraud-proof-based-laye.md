---
source: ethresearch
topic_id: 6492
title: Non-attributable censorship attack on fraud-proof-based Layer2 protocols
author: nrryuya
date: "2019-11-24"
category: Layer 2
tags: []
url: https://ethresear.ch/t/non-attributable-censorship-attack-on-fraud-proof-based-layer2-protocols/6492
views: 5142
likes: 10
posts_count: 9
---

# Non-attributable censorship attack on fraud-proof-based Layer2 protocols

## TL;DR

We propose an attacking strategy to censor specific transactions (e.g., fraud proofs in Layer2 protocols), in which it is difficult to identify the attacker.

Even if users can recover from this attack by a socially coordinated soft/hard fork, we cannot penalize the attacker without penalizing honest validators.

## Background

The safety of fraud-proof-based Layer2 protocols (e.g., Plasma, Optimistic Rollup, state channels) depends on the assumption that if operators/players claim invalid off-chain state, a fraud proof can be submitted to and gets included in the chain within a pre-defined period (Footnote 1). Recently, [@gluk64](/u/gluk64) brought up the security of these protocols for discussion on [Twitter](https://twitter.com/gluk64/status/1184399877146587136) and [ethresear.ch](https://ethresear.ch/t/nearly-zero-cost-attack-scenario-on-optimistic-rollup/6336). Roughly speaking, an attacker can make a profit by cheating in such Layer2 constructions by 51% attack to censor fraud proofs, making the whole system (including Layer1) not incentive compatible, especially because the in-protocol reward compensates for the attacker’s cost to run validators (Footnote 2).

The major countermeasures are:

- We can increase the cost of such censorship attacks by the “counter DoS attack.” (cf. @adlerjohn’s comment)

TL;DR: In Ethereum’s smart contract model, you don’t know which contracts are called in executing a transaction without actually executing it, so DoS attack against the censorship is possible by sending a bunch of transactions to the attacker

We can recover from the attack via soft fork and also “wipes out” the attacker’s stake in PoS. (cf. [@vbuterin](/u/vbuterin)’s [comment](https://twitter.com/VitalikButerin/status/1184485221871210496))

In this post, we describe a strategy of censorship attack for which these mechanism does not apply. This strategy works for any transactions other than fraud proofs in Layer2 protocols.

## Description of the attack

We assume a PoS system like the eth2 beacon chain (Footnote 3), where a block proposer creates a block, a committee of validators vote for a block every slot (e.g., 6 seconds), and those votes are also interpreted as Casper FFG votes to finalize blocks. We expect similar strategies work for other consensus protocols or PoW systems.

#### Attacker’s capability

In this post, we assume an attacker who controls more than the majority of stakes with a margin (e.g., 55% stakes). Because such an attacker controls more than 1/3 of the votes, blocks which is not favored by the attacker cannot be finalized by Casper FFG.

#### Attacker’s strategy

1. If the main chain does not include a fraud proof, the attacker vote for the main chain.
2. If the main chain includes a fraud proof, the attacker creates and vote for a conflicting chain to fork off the fraud proof.
2.1 However, a small number of attacker’s validators vote for the chain which includes the fraud proof.

These are “alibi votes” to make the attacker’s validators behave similarly to honest validators
3. The number of alibi votes must be sufficiently small (e.g., 5% of the votes of the slot) so that the block cannot win in the fork-choice.

[![image](https://ethresear.ch/uploads/default/original/2X/5/50ec11834eaa3268ccfe6c68a94272cb0d76967c.png)image690×494 16 KB](https://ethresear.ch/uploads/default/50ec11834eaa3268ccfe6c68a94272cb0d76967c)

The attacker chooses either one of the below with a certain probability when creating a block.

1. Create a block without a fraud proof, filled with self-made transactions (e.g., A transaction that transfers tokens between accounts which the attacker controls) (Footnote 4).
2. Create a block which contains a fraud proof, along with self-made transactions.
4.1 The attacker publishes this block slightly after the next block is published so that most honest validators do not vote for the block
4.2 The attacker publishes alibi votes for this block (e.g., with 40% of the votes of the slot)

Also, the attacker has a strategy to encourage honest validators to create blocks without fraud proofs.

1. The attacker frequently broadcasts self-made transactions with high fees

## “Security arguments” for attackers

#### Resistance to the “counter DoS attack”

When the attacker creates a block, he does not include any transactions created by other people. Therefore, the attacker verifies only the transactions included in honest validators’ blocks, which is already required to be a full node, so the attacker does not suffer from the above DoS attack.

#### Difficulty of detecting the attacker

In the above strategy, the attacker does not make equivocations or invalid messages. The differences between attackers and honest validators are only about how they create, publish, and vote for blocks that contain fraud proofs. To decrease the difference in the ratio of creating blocks with fraud proofs, the attacker increases the use of strategies 3 and 5 more. To decrease the difference of the ratio of voting for blocks with fraud proofs, the attacker increase alibi votes (strategies 2.1 and 4.2) and decrease honest validators’ votes for fraud proofs made by attackers (strategy 4.1).

Other than these, the strategies 2 and 4.1 leverages the nature of distributed systems that liveness faults cannot fundamentally be distinguished from a network failure. Further, there would be various [network-level attacks](https://eprint.iacr.org/2015/263.pdf) by which the attacker can delay honest validators’ blocks and votes to make the honest validators look similar to the attacker.

Therefore, although we must refine the strategies (e.g., by parameterizing the attacker’s stake, the network conditions) to make these arguments more formal, we conjecture that it can become difficult to identify the attacker’s validators without making a false accusation.

## Punishing the attacker by a soft/hard fork

If users coordinate a soft fork to recover from a censorship attack, the attacker can join the new chain soon to avoid being detected and any punishment on liveness failure (e.g., [inactivity leak](https://notes.ethereum.org/9l707paQQEeI-GPzVK02lA#Inactivity-leak)). Because it is difficult to identify who is the attacker, what we can do to slash the attacker’s stake is to punish all the suspicious validators with the risk of punishing honest validators, with a philosophy similar to the “penalizing both sides.”

#### Collateralization

One approach to make sure that only the attacker’s side gets penalized is to force anyone to deposit to be an operator of Plasma/Optimistic Rollup or participate in channels and slash the collateral by a fraud proof. If we assume socially coordinated soft fork is likely to succeed and the collateral is sufficiently high, such Layer2 protocols can potentially achieve incentive compatibility, with a trade-off of higher barriers to entry. If we want to avoid punishing too much on frauds due to [honest mistakes](https://twitter.com/zmanian/status/1145074988459814912), where it is expected that the fraud proofs smoothly submitted without being censored, we can limit the default amount of punishment, and punish a lot by a hard fork (irregular state change) in the case of censorship attack.

---

#### Footnotes

1. OTOH, fraud proofs of invalid state roots in sharding invalidate the chain without being included on-chain. This post proposes a clever technique about this.
2. Note that the attacker can benefit not only from a single Layer2 construction but also from multiple Layer2 constructions at the same time. This is why to cap the value of the off-chain asset does not solve the problem.
3. In eth2, Layer2 systems will be deployed on shard chains, not beacon chain, so the optimal attacking strategy might become different. We leave this for future discussion.
4. The fees of such self-made transactions go back to the attacker’s hand.

## Replies

**adlerjohn** (2019-11-24):

First, the cost of this attack is non-zero.

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> The attacker frequently broadcasts self-made transactions with high fees

Let’s assume a reasonable bond of 1 ETH to commit to an ORU block, a burn ratio of 1/2, a finalization delay of 2 weeks, a conservative 10 tps, and an attacker’s block producing power of ~55\%. Therefore we get an in-protocol cost of attack of approximately 3 million ETH, or 450 million USD at the time of writing.

Second (and more importantly) your voting strategy is incorrect:

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> If the main chain includes a fraud proof, the attacker creates and vote for a conflicting block to fork off the fraud proof.

Creating blocks is not part of a voting strategy, it’s part of a block creation strategy. The leader at each slot (the block proposer) is known, at least in the Eth 2.0 version of Casper, which is the consensus protocol used in your post. It’s impossible for a slot to have more than one block proposer, so the attacker’s block would be trivially discarded.

---

**nrryuya** (2019-11-25):

> First, the cost of this attack is non-zero.

Yep, the attacker’s cost includes the transaction fee for strategy 5 and this cost increases by a longer challenge period. However, I think the economics around fraud proofs is not trivial, e.g., rational operators/users start to submit fraud proofs with small fees and gradually increase fees?

> Second (and more importantly) your voting strategy is incorrect:

I mean, the attacker creates a conflicting block in the next slot and continue to extend that until it becomes the main chain. (Modified the wording in the post slightly.) In eth2, the attacker cannot make use of the votes of the slot in which the block with a fraud proof gets created, so it will take a few slots or more to fork off the fraud proof if honest validators succeed to agree on the head. This is one of the “bonuses” of chain-based consensus with the committee voting, with a trade-off of potential network-level attacks (e.g., [splitting votes](https://t.me/c/1223138737/790)) which helps the above strategy and is not well studied IMO. This is more challenging than Nakamoto consensus because everyone votes at the same time without seeing each other.

---

**gluk64** (2019-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> Therefore we get an in-protocol cost of attack of approximately 33 million ETH, or 450450 million USD at the time of writing.

Yes, this strategy will probably not work because the fraud proof gas price can be set incredibly high. However, the attack will work without subsidizing fraud proof blocks, and this is what matters. All attacker needs is alibi.

Ability to have an alibi is really the most important result of this research.

The miners are selfish and proactive. Once they realize that blocks with fraud proofs are always rejected, many might naturally introduce censorship policy to avoid losses. Especially if this behavior is a) undetectable (with an alibi) and b) incentivized through bribing with swag futures.

---

**vbuterin** (2019-11-25):

I know [@vladzamfir](/u/vladzamfir) was working on a “subjective CBC censorship detection” system that, assuming a synchrony assumption (all censorship detection must obviously depend on synchrony because censorship is indistinguishable from sufficiently high latency), allows validators to detect who is censoring and form clusters where if a majority is censoring the minority can find each other and build on each other’s blocks. I wonder if it ended up being similar to https://vitalik.ca/general/2018/08/07/99_fault_tolerant.html ; it’s possible a technique similar to Lamport’s synchronous 99% fault tolerant consensus may end up being mandatory in a “truly clean” solution to automated rejection of censoring chains.

---

**nrryuya** (2019-11-25):

Let me define a simplified utility of the attacker (1 - p)R - pD + r - c, where

R: Reward from successful cheating in (potentially multiple) Layer2 systems

D: Punishment in the recovery of soft/hard fork

p: Probability of successful soft/hard fork

r: In-protocol reward of block production and voting

c: Cost of the attack

Higher *p* and *c* disincentivizes this attack, and setting the challenge period longer will help this, with a trade-off of making the time to withdraw longer.

About D, as in Vitalik’s comment, there would be various heuristics to detect the attacking validators. This is fundamentally the [failure detection problem](https://en.wikipedia.org/wiki/Failure_detector), which is much harder than catching equivocations. Identifying a few slots of timing failure likely makes false accusations by accident or trap, especially in the network environment of public chains.

---

**adlerjohn** (2019-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> However, the attack will work without subsidizing fraud proof blocks, and this is what matters.

I think you’re correct about this, which is unfortunate for you as well. If the attack costs nothing, then new blocks in zk-rollups can be stalled indefinitely for free. Sure the attacker can’t profit by stealing user funds directly, but the attack is free so why not? This can also be used to coerce users of a zk-rollup chain to divert a portion of their funds to the attacker on the rollup chain (can be done using transactions that are indistinguishable to normal transfers, to any number of different addresses).

Note: for better or for worse, this attack is not an issue for PoW. Since miners in PoW are anonymous anyways, our only option to a majority-hashrate censorship attack is to scorched-earth brick all mining equipment with a new PoW algo (all the more reason to have ASICs on the network).

![](https://ethresear.ch/user_avatar/ethresear.ch/gluk64/48/11557_2.png) gluk64:

> Once they realize that blocks with fraud proofs are always rejected, many might naturally introduce censorship policy to avoid losses.

[This can be done with minority Sybil resistance as well](https://bitcointalk.org/index.php?topic=312668.0), so that incentive is orthogonal to the core of the attack.

---

**adlerjohn** (2019-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> Cost of the attack

So we have two potential results here:

1. This attack is free to pull off, as spamming transactions isn’t actually needed. Conclusion: a majority of stake can censor any transaction (not just a fraud proof transaction) for free without attribution. The version of PoS chosen for Eth 2 is fundamentally broken and we can pack up our bags and go home, the whole thing is a failure.
2. The attack isn’t free to pull off, spamming transactions is needed. Conclusion: users can coordinate a soft fork to force inclusion of the fraud proof. They don’t need to identify the attacker because the attacker identified themselves and penalized themselves through the absurd amount of transaction fees already paid.

Case 1 is an interesting result, as it would require drastic changes to Eth 2’s consensus protocol. Case 2 is a non-result.

---

**gluk64** (2019-11-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/adlerjohn/48/2924_2.png) adlerjohn:

> This attack is free to pull off, as spamming transactions isn’t actually needed. Conclusion

This is definitely the case with 51% in PoW. Intuitively, this should also apply to PoS.

Now, the conclusion is not valid. With normal accounts (or ZK Rollup, for that matter) there is no direct way to benefit from permanent censorship over long period of time other than extortion. The best strategy for the affected users is then not to give in. This makes the probability of the success of the attack low, which, in turn, renders the attack futures very cheap. The attacker cannot fund ongoing bribery of miners/validators from the attack futures pool.

With fraud proof L2 solutions on the other hand, the chances to sustain the attack for ~1 week are not so bad. There will likely be enough people willing to risk a little money with the potential 1:10 or 1:100 upside. This drives the drives on the attack futures up and makes it possible for the black hats to trustlessly coordinate the attack.

Moreover, a permanent censorship of ETH accounts is much more likely to be considered a deliberate attack on the entire network than short-term “unfortunate situation” with a single time-locked smart contract. The former will have big consequences for the validators stake. The latter can lead to short-term ETH price decline, offset for the miners by the attack’s gains, and then everybody will quickly forget – just like it happened with the DAO.

