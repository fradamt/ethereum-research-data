---
source: ethresearch
topic_id: 8713
title: How high can the gas limit be increased?
author: clesaege
date: "2021-02-20"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/how-high-can-the-gas-limit-be-increased/8713
views: 5426
likes: 19
posts_count: 15
---

# How high can the gas limit be increased?

Currently the network congestion has made ETH1 L1 pretty much unusable outside of financial applications (manipulating large amount of money).

L2 and ETH2 are good answers to that, but in the meantime the risk is to kill the Ethereum ecosystem of non financial applications and see projects moving to other chains trading decentralization for higher throughput.

From my understanding the main bottleneck around increasing gas limit is storage capacity (state rent could change that but it’s another topic).

The cost for SSD (I’m not looking at HDD as they are impractical anyways) has significantly been reduced since Ethereum launch: [900$ per tera in 2015-08](https://blocksandfiles.com/2020/05/15/enterprise-ssds-are-ten-x-cost-of-nearline-disk-drives/)  to [117$ today](https://www.amazon.com/Hikvision-E100N-Internal-Interface-Protocol/dp/B086F679KD/ref=sr_1_2_sspa?dchild=1&keywords=1TB+Internal+SSD&qid=1613777593&sr=8-2-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzRklTUlNRSUdWQzMzJmVuY3J5cHRlZElkPUEwNTU2NDU1MUZFSjJWR0IzSzFQRCZlbmNyeXB0ZWRBZElkPUEwODE5NzQ5MVlETEcyNVFNR1ZaSyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=).

However, the gas limit has only increased from 3M in 2015-08 to 12M today.

A 4X increase of gas limit while we had a 8X decrease in SDD cost.

Gas limit has increased, but only at a rate of half the SDD progress.

Now even if increasing the gas limit would result in a requirement of higher-end hardware, I would expect those inconvenience be pretty low compared to the issue of gas cost. A 117$ SSD can store more than 2 times the current weight of an [Open Ethereum full node](https://etherscan.io/chartsync/chaindefault) while a complex TX now costs far more than that.

And not every user needs a full-node, but at current gas price almost all users wanting to continue using Ethereum would need to pay far more in gas.

So the questions are:

- Would doubling the gas limit right now lead to any serious issues?
- Would doubling the gas limit lead to serious issues which would not have happened if the gas limit and SSD capacity would not have changed since 2015-08?
- Would those issues be worth the benefit of extra gas (I suggest reading this article on resource pricing)?

(Note that this post may appear one-sided and asking rhetorical questions. Those are not and there may be adverse consequences I am not aware off.)

## Replies

**sourav1547** (2021-02-20):

I worked on a paper sometime back that tries to address this problem.


      ![image](https://static.arxiv.org/static/browse/0.3.2.6/images/icons/favicon.ico)
      [arXiv.org](https://arxiv.org/abs/2005.11791)


    ![image]()

###

Proof-of-Work~(PoW) based blockchains typically allocate only a tiny fraction
(e.g., less than 1% for Ethereum) of the average interarrival
time~($\mathbb{I}$) between blocks for validating transactions. A trivial
increase in validation time~($τ$)...

---

**clesaege** (2021-02-21):

This article is about protocol change, I don’t think investigating complex protocol changes answer the immediate issue of increasing gas costs. And Ethereum moving to PoS, it’s unlikely that significant PoW changes would be implemented in the meantime.

---

**vbuterin** (2021-02-21):

> [2005.11791] Better Late than Never; Scaling Computation in Blockchains by Delaying Execution

So I actually don’t think this would help much. The reason is that right now the primary constraint on block size is NOT the uncle rate. Rather, it’s:

1. Risk of DoS attacks (a worst-case block could take up to 20-80 seconds to process)
2. State size growth

Delayed processing would solve neither of those issues.

EIP 2929 is going in Berlin (scheduled for mainnet activation on April 14), and that will solve (1) by reducing worst-case block processing time to 7-27 seconds, and client optimizations (turbogeth?) could go further. We can accept faster state size growth if we have a solid roadmap toward fixing (2); either state expiry or weak statelessness or eventually both.

---

**Mister-Meeseeks** (2021-02-22):

Binance BSC is running a straight clone of Geth. The only difference is that PoW miners are replaced with centralized validators. But from the perspective of a full node, the workload is exactly the same. BSC runs with 30 million Gwei block sizes, and 3 second block times. From a workload standpoint, that’s the equivalent of 120 million Gwei block sizes at Ethereum’s 12 second block times. Nobody seems to have any trouble running a full node on BSC.

That would suggest that Ethereum can increase its block sizes by at least an order of magnitude. Maybe the PoS/PoW distinction makes a difference but I doubt it. Certainly miners should not be starved of compute/storage/bandwidth compared to the average full node.

Another datapoint. I’ve forked Geth to run pre-mine commits with 50+ million block sizes. On a large AWS instance, it’s no problem at all. Considering that the sizable majority of full nodes run in the cloud, the P2P network should easily handle an increase in requirements. The era of the home hobbyist running a full node is already well behind us.

---

**TheCookieLab** (2021-02-22):

> The era of the home hobbyist running a full node is already well behind us.

Is it though? [Network Types - ethernodes.org - The Ethereum Network & Node Explorer](https://www.ethernodes.org/network-types) shows ~41% of mainnet nodes are from residential connections.

Perhaps more importantly, is such an outcome desirable? I was under the impression that a healthy population of Joe and Jane Savvys running (non-mining) nodes in their basement was a positive (necessity?) for decentralization. As the saying goes, miners can create any kind of block they want but it’s the (Joe Savvy) nodes that decide whether or not to accept it. If I’m not mistaken this was Bitcoin Core’s (public) argument against bigger blocks way back when, as it can lead to miner-run blockchains.

As Ethereum transitions to ETH2, I would think having a sizable population of independent hobbyist-run nodes is even more important as this also applies for validators who are directly involved in the consensus process.

---

**clesaege** (2021-02-23):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/da6949/48.png) TheCookieLab:

> If I’m not mistaken this was Bitcoin Core’s (public) argument against bigger blocks way back when, as it can lead to miner-run blockchains.

When moving to PoS, blocksize would not have the same impact as it can have on Bitcoin as the quantity of validators and their distribution will be way more decentralized than what can be achieved through PoW (i.e. having only miners run nodes is worse than having only stakers run nodes). And the hardware cost is negligible compared to ETH capital requirement. A 117$ SDD is negligible when you need 41 000$ worth of capital to be a validator, and even if we were to multiply it by 10x hardware costs would still be low compared to capital costs (~3%).

About the hobbyists, current gas prices makes it hard to be a hobbyist. Sure you can theoretically run a node without doing any TX, but in practice hobbyists are Ethereum users and if they are priced out of the fee market they are unlikely to continue or start running nodes.

I still don’t think at this point (while still on PoW) we should have crazy increase like BSC (3X gas limit and 5X block speed for X15 more gas available) which could prevent hobbyist nodes.

But (unless someone found another issue) just increasing the gas limit 2X (just keeping up with hardware progress), even if conservative, could significantly help with the gas price.

---

**MicahZoltu** (2021-02-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/mister-meeseeks/48/5638_2.png) Mister-Meeseeks:

> BSC runs with 30 million Gwei block sizes, and 3 second block times. From a workload standpoint, that’s the equivalent of 120 million Gwei block sizes at Ethereum’s 12 second block times. Nobody seems to have any trouble running a full node on BSC.

Binance chain doesn’t have a 6 years of history being dragged along with it.

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> But (unless someone found another issue) just increasing the gas limit 2X (just keeping up with hardware progress), even if conservative, could significantly help with the gas price.

Block size impacts the *rate* of growth, not the current state size.  Hard drive costs have been coming down since 2014, while state size has been increasing since 2014.  If the current *rate of state growth* equals the current *rate of SSD cost decrease* then we are in equilibrium and no change is needed.  Here you are comparing rate of state growth (block size) against current cost of SSDs, which isn’t an appropriate comparison (apples to oranges).

---

**Mister-Meeseeks** (2021-02-23):

@MicahZolutu

You’re making an invisible assumption that larger block sizes necessarily mean faster state growth. That seems intuitive, but based on current usage patterns I’m not sure if that’s true to any significant degree. Most of the marginal transactions are interacting with the same narrow set of Defi contracts.

If a single Uniswap pair gets traded 100 times instead of 10, that doesn’t increase state growth rate. The same storage just gets written updated a lot more, instead of new storage being created. Another example are bots that use the contract self-destruct refund trick to save gas in priority auctions. Large block sizes would probably mean they bank a lot more dummy contracts. But 100% of those contracts get self-destructed in a day or two, so there’s no long-term impact on growth.

I won’t deny that larger block sizes would lead to some increase in stage growth. But I’m virtually certain that the relationship is significantly *sub-linear*. At the very least, the EVM fee schedule certainly doesn’t optimize for this dynamic.

---

**MicahZoltu** (2021-02-24):

Block bodies take up quite a bit of space, and receipts as well (though you don’t strictly need to retain those for a healthy blockchain).  These sort of growths *are* linear.

You are correct that blocksize isn’t 1:1 with state growth specifically, but I do think that there is a strong correlation and it is *probably* close to linear.  If we increase the block size by 2x I suspect we will get a *very* substantial increase in state growth (something close to 2x).

In fact, I believe this is true if we assume that the average behavior on-chain remains constant.  So if right now 10% of the block is new storage writes, then I suspect 10% of a 2x sized block will also be new storage writes unless users change behavior when gas prices decrease.  Given that gas high gas costs drive people away from writing to storage and toward doing things that are storage minimized (like optimistic rollups), we may even see a supralinear growth of state with a a decrease in gas prices!

---

**clesaege** (2021-02-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/mister-meeseeks/48/5638_2.png) Mister-Meeseeks:

> I won’t deny that larger block sizes would lead to some increase in stage growth. But I’m virtually certain that the relationship is significantly sub-linear . At the very least, the EVM fee schedule certainly doesn’t optimize for this dynamic.

Yeah, repeated activity may not result in higher storage usage in a classic setting, but for a system to be secure, we should generally look at the worse case assumptions (here that any increase of gas limit would induce a proportional increase in state growth) and assume an adversarial setting (i.e. that some actors would actively try to attack the chain, which has already happened with the Shanghai attacks).

A more efficient pricing system could put some individual limits on computation and storage but that would be quite complicated to switch to it.

---

**kladkogex** (2021-02-25):

There are many ways to solve the problem, one of them is to use rectangular blocks instead of linear ones.

EVM is single threaded. Rectangular blocks essentially provide synchronized shards.

---

**clesaege** (2021-02-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Block size impacts the rate of growth, not the current state size. Hard drive costs have been coming down since 2014, while state size has been increasing since 2014. If the current rate of state growth equals the current rate of SSD cost decrease then we are in equilibrium and no change is needed. Here you are comparing rate of state growth (block size) against current cost of SSDs, which isn’t an appropriate comparison (apples to oranges).

My assumption was that the initial gas limit was made to be able to sustain a linear growth for a decent amount of time without accounting for SSD progress (but I don’t know how this was set up and it would be interesting if someone who participated in deciding the initial limits could enlighten us).

Having

*Current rate of state growth* = *Current SSD size*

may not be conservative enough but is a interesting approximation.

Since SSD size increases exponentially while the state size increases linearly (in respect of the gas limit), the state size due to old TXs becomes negligible compared to the state size due to new ones.

*Current rate of state growth* = *Current rate of SSD cost decrease*

would be a lower bound on how fast the state growth but may be too conservative.

Because initially the state was empty so this equation would not have been practical.

*Current rate of state growth* >> *Current rate of SSD cost decrease* in the initial condition.

Another issue is that is we set up *Current rate of state growth* = *Current rate of SSD cost decrease* if we have the gas limit at a value lower than what we could technically, the state will would have grown at a slower rate, thus the state would be smaller, thus the *current **rate** of state growth* would be higher (as you divide by *state size* to compute the **rate**).

Maybe to determine acceptable gas limits, we need not to focus into past rates like I did in my initial post but to look at current state, SSD costs, their rates of increase and balance that with transaction fees (the idea being that there is no point of restricting the gas limit such that a 100$ machine can run it if it also costs 100$ to make an average complexity TX).

---

**MicahZoltu** (2021-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> My assumption was that the initial gas limit was made to be able to sustain a linear growth for a decent amount of time without accounting for SSD progress (but I don’t know how this was set up and it would be interesting if someone who participated in deciding the initial limits could enlighten us).

I *believe* the state growth rate was setup under the assumption of hard drive cost decreasing with time.  I wasn’t around for the initial decision, but back when I started getting involved it was something people were talking about as an assumption.

---

**MicahZoltu** (2021-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/clesaege/48/533_2.png) clesaege:

> Maybe to determine acceptable gas limits, we need not to focus into past rates like I did in my initial post but to look at current state, SSD costs, their rates of increase and balance that with transaction fees (the idea being that there is no point of restricting the gas limit such that a 100$ machine can run it if it also costs 100$ to make an average complexity TX).

I’m not a fan of this calculation because it assumes that everyone is transacting on layer 1.  A layer 2 BLS rollup transaction can be incredibly low gas per transaction but the user still would ideally have a synced Ethereum node of their own rather than relying on centralized service providers.  Also, once we do have sharding (and thus more space), we don’t want the ETH1 shard to have already blown up to the point where only servers can run it.

To put it another way, I would rather focus on the problems of tomorrow than the problems of today, and I especially am hesitant to make choices today that will cause us problems tomorrow… even if they fix problems today.

