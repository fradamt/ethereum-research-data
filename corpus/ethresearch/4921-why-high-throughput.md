---
source: ethresearch
topic_id: 4921
title: Why high throughput?
author: bedeho
date: "2019-01-31"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/why-high-throughput/4921
views: 2413
likes: 3
posts_count: 9
---

# Why high throughput?

Lots of PoS based BFT algorithms are claiming to have very high rates of throughput*, combined with low latency. Much more so than what one finds in deployed Nakamoto consensus chains.

**What critical tradeoff or assumption is made in these algorithms which unlocks this capacity improvement?**

*I mean high rates on the base layer, not about enabling sharding or any L2 solution.

## Replies

**sir_assistant** (2019-02-01):

Correct me if i’m wrong:

With POW, when a block is mined (miners)

Compute the new block ASAP => hash the hell out of it => Be the first to propagate it

With POS, when a block is mined

Proposers compute the new block => Validators validate and vote it => it gets part of the canonical chain

With POW, you are incentiviced to make that time to hash the block as long as possible to have a chance to find the solution to the puzzle. So you need the computation of the new block to be as fast as possible.

With POS you can take all that time to compute transactions, since it doesn’t matter how much time you spend as long as you vote in time and your vote gets propagated.

---

**djrtwo** (2019-02-03):

If they are not sharding or partitioning the protocol in any way, these chains are likely making sacrifices in decentralization (requiring network participants to have larger than O© resources where C is the resources of a consumer laptop) and not making in protocol guarantees about data availability.

There are some gains to be had wrt more strict timing of events (not relying upon the random distribution of blocks via pow) but these are generally minor.

---

**bedeho** (2019-02-04):

Hi, thanks for the reply.

I am afraid I really don’t understand what you are saying, even though your descriptive premise of POS/POW seems about right, in particular what does this mean?

> you are incentiviced to make that time to hash the block as long as possible to have a chance to find the solution to the puzzle

---

**bedeho** (2019-02-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> There are some gains to be had wrt more strict timing of events (not relying upon the random distribution of blocks via pow) but these are generally minor.

Could you possibly elaborate on what these are?

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> If they are not sharding or partitioning the protocol in any way, these chains are likely making sacrifices in decentralization (requiring network participants to have larger than O© resources where C is the resources of a consumer laptop) and not making in protocol guarantees about data availability.

This was my intuition also, however, I am seeing claims about 100s of validators, across multiple continents, sub 10s finality and 100s of transactions per second. This just does not seem to be something I would expect normal Nakamoto type chains to be able to handle, but perhaps I am wrong.

---

**nourharidy** (2019-03-03):

PoW chains can theoretically be configured to target any arbitrary block time but the block time is inversely proportional to the orphan rate (rate of unincluded valid blocks due to network latency). The higher the orphan rate, the lower the economic incentives to mine because more work is left unrewarded, the lower the network hashrate, and therefore the lower the security of PoW.

Ethereum *solved* this problem via the introduction of “uncle blocks”, basically issuing an extra reward to orphaned blocks in addition to included blocks. This is how Ethereum can reach a target block time of 15 seconds instead of Bitcoin’s 10 minutes. This does however force the community of ETH tokenholders to subsidize the cost of security through extra inflation. If we decrease the block time even further, sub-10s as you proposed, we would have to issue rewards for more orphaned blocks and subsidize the security of the network via more inflation, driving ETH value down over time.

To answer your original question about high throughput BFT consensus algorithms (e.g. Tendermint), byzantine fault-tolerant finality is based on the assumption that at least 2/3+1 of preset **validator nodes** will remain online and honest at all times. Because the number of validator nodes is preset, finality is achieved once a required quorum of validator signatures is present. There is no need for further block confirmations because of the 2/3+1 assumption.

Additionally, since we’re already making the 2/3+1 assumption, non-validator nodes generally do not have to run full nodes or download full blocks to verify the validity of the chain because they rely can query information about the blockchain from the validators based on the assumption that 2/3+1 of them are honest.

---

**MihailoBjelic** (2019-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/nourharidy/48/2143_2.png) nourharidy:

> at least 1/3 of preset validator nodes will remain online and honest at all times

It’s actually 2/3+1 validator.

---

**kladkogex** (2019-03-28):

Believe it or not, PoW algorithms can also be fast.   The reason why PoW is slow is network and not PoW itself.

At Skale we know how to do a PoW which will have 1000 tps or more.

What is hard to do with PoW is fast finalization, because you need to wait for a larger number of blocks to be secure.   High throughput PoW is totally possible,  fast finalizing PoW - not really, because it is forkful

---

**nourharidy** (2019-03-30):

You’re right. My bad. Edited.

