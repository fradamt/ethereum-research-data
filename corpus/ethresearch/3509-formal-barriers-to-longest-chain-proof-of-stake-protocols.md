---
source: ethresearch
topic_id: 3509
title: Formal Barriers to Longest-Chain Proof-of-Stake Protocols
author: RhysLindmark
date: "2018-09-23"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/formal-barriers-to-longest-chain-proof-of-stake-protocols/3509
views: 3589
likes: 5
posts_count: 5
---

# Formal Barriers to Longest-Chain Proof-of-Stake Protocols

New paper [Formal Barriers to Longest-Chain Proof-of-Stake Protocols](https://arxiv.org/pdf/1809.06528.pdf) from [Arvind Narayanan](https://twitter.com/random_walker) of Princeton.

Not sure if these papers should be posted to this forum (my instinct is that they should!), but trying it as an experiment (instead of just discussing on Twitter).

[Key idea](https://twitter.com/random_walker/status/1043552710086340609):

*At a conceptual level, the barriers stem from the following: all cryptocurrencies require some source of (pseudo)randomness. In Proof-of-Work, this pseudorandomness is in some sense external to the cryptocurrency: the first miner to successfully find a good nonce produces the next block, and this miner is selected completely independently of the current state of the cryptocurrency. In Proof-of-Stake, it is highly desirable that the pseudorandomness comes from within the cryptocurrency itself, versus an external source (due to network security concerns discussed in Section 2). One might initially suspect that with sufficiently many hashes or digital signatures of past blocks, this can indeed serve as a good source of pseudorandomness for future blocks. However, we formalize surprising barriers showing a fundamental difference between external pseudorandomness and pseudorandomness coming from the cryptocurrency itself.*

## Replies

**vbuterin** (2018-09-24):

Copying my reply to Arvind:

---

Thanks for writing the paper, it definitely captures a lot of issues with many kinds of PoS algorithms that I think are very important! Some comments:

> (Globally-Predictable Selfish Mining)

One issue with this section is that there are ways to make selfish mining unprofitable from an incentive point of view. Particularly, if a block is created that is not part of the main chain, we can penalize *both* that block and the block with the same height on the main chain by 1 coin, so a successful selfish mining attack even if successful would cost the attacker.

The more general principle behind this is that when developing incentives for a consensus algorithm, as a general rule, if you can tell that either A or B were faulty, but you can’t tell which one, then it’s best to penalize *both* A and B at least by some amount (a version of this insight could also be used to bring PoW’s selfish mining resistance arbitrarily close to 50%; a version that looks only at first-order “sister” blocks brings it to ~39% as I recall).

Another issue that I think you missed that is even more interesting is that the randomness itself can be strategically manipulated. See [RANDAO beacon exploitability analysis, round 2](https://ethresear.ch/t/randao-beacon-exploitability-analysis-round-2/1980) for my analysis on our earlier RANDAO proposal. The summary is that in RANDAO each block producer contributes to randomness used to select the immediately next block using data that they precommitted to, and so any block proposer can manipulate the randomness by not showing up, at the expense of sacrificing their ability to make that block. This seems expensive, but actually an attacker can simulate the paths where manipulating randomness lets them get *more* than 1 block of advantage, and altogether an attacker with infinite computing power can do chain reversion attacks with ~36% of total stake. I have a mathematical argument and a link to a simulation in that post that backs up the numbers; it’s surprisingly cool, showing a relationship between the probability a path favoring the attacker exists and limit ratios of diagonals of Pascal’s triangle.

Finally, here [Beacon chain Casper mini-spec](https://ethresear.ch/t/beacon-chain-casper-ffg-rpj-mini-spec/2760) is our latest proposal. We aim to prove the security property that the algorithm’s security is essentially independent of randomness, because there are many validators participating simultaneously in each round and so it would be near-impossible for the attacker to “corrupt” even one round; a GHOST variant (not the naive one!) is used as the fork choice rule.

I think the thing to keep in mind re GHOST is that PoS is fundamentally different from PoW, in that in PoW making two blocks is twice as hard as making one block, but in PoS this is not the case; hence, it’s philosophically wrong to have a fork choice rule that “adds up” two different messages from the same validator that are in support of a message. Additionally, validators need to be selected well in advance so there are no exponential forking issues.

---

**kladkogex** (2018-09-25):

I think it is a great paper which shows that PoS protocols with single proposers have lots of problems.  It is bad when a block is proposed by a single guy, since he can manipulate and control the randomness.

In asynchronous masterless protocols such as HoneyBadger and Redbelly, as well as the protocol we use at Skale, there is no problems with randomness since everyone participates in the proposal phase and a common coin is used (based on BLS).  Once the proposal is made by a committee and not by a single miner, the problems with randomness dissapear as long as the size of the committee is large.

So for Casper beacon chain, an alternative is to have a block proposal committee running an asynchronous masterless protocol with a common coin.  Honeybadger as an example ) And then include the BLS-based common coin derived by the committee in the block.

---

**vbuterin** (2018-09-25):

> I think it is a great paper which shows that PoS protocols with single proposers have lots of problems. It is bad when a block is proposed by a single guy, since he can manipulate and control the randomness.

Not strictly true. What you actually want is lots of *attesters* per round. if that means no single proposer, great, but having one proposer immediately followed by lots of attesters that must agree on their block is also sufficient.

---

**cat721** (2019-11-21):

I think this is also an interesting [consensus protocol](https://www.fractalblock.com/assets/iching_consensus_protocol.pdf) that mimics Nakamoto’s design but via proof-of-stake. It is a hybrid longest chain PoS. And I think it doesn’t meet the barriers.

