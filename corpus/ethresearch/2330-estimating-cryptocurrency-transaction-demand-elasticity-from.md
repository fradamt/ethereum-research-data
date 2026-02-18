---
source: ethresearch
topic_id: 2330
title: Estimating cryptocurrency transaction demand elasticity from natural experiments
author: vbuterin
date: "2018-06-23"
category: Economics
tags: [transaction-demand-elasticity]
url: https://ethresear.ch/t/estimating-cryptocurrency-transaction-demand-elasticity-from-natural-experiments/2330
views: 8323
likes: 6
posts_count: 4
---

# Estimating cryptocurrency transaction demand elasticity from natural experiments

One variable of interest in cryptocurrency is the demand curve in the transaction fee market; that is, for any value X, what is the fee level that the highest-fee-paying set of users whose usage makes up X (gas | weight units | bytes) is willing to pay? This has relevance in block size policy design; to take an extreme example, if the elasticity is very low (eg. 0.1), then setting inflexible block size caps is a very bad idea, because setting a cap that is even 10% below the optimum would more than double the fees that users would have to pay, and an influx of 10% more users could have the same effect.

However, it is difficult to estimate demand directly. We can try to look at the levels of transaction fees that users are sending, but this data is highly imperfect because the fee levels do not actually reflect users’ [reserve prices](https://en.wikipedia.org/wiki/Reservation_price); rather, they are a strategic choice, taking into account both the user’s demand and market conditions (see [First-price sealed-bid auction - Wikipedia](https://en.wikipedia.org/wiki/First-price_sealed-bid_auction#Strategic_analysis)). So what can we do instead? This post attempts a novel strategy, looking at “natural experiments” where the supply (ie. block size limit) changes for exogenous reasons that have nothing to do with cryptocurrency price or underlying adoption, and see how the equilibrium price adjusts. We will examine five situations:

- The Bitcoin block rate crunch of 2017 Aug 22-26 (a result of BTC/BCH difficulty adjustment interplay)
- The Bitcoin block rate crunch of 2017 Nov 11-12
- The Ethereum gas limit increase from 4.7m to 6.7m on 2017 Jun 29
- The Ethereum block time decrease on 2017 Oct 16 (a result of Byzantium cancelling the ice age)

We will ignore previous situations like the Ethereum DoS attacks and the Bitcoin block reward halvings because they occurred at a time of naturally non-full blocks, and in the former case involved a single exceptional actor greatly contributing to transaction demand. Note that these experiments give fairly short-run demand curves, looking at situations that last over the course of one week; long-run demand curves may be different.

### Data from Bitcoin

In the Bitcoin case, we can look at https://www.smartbit.com.au/charts/blocks for block rate data; from a natural rate of 150/day, the block rate decreased on Aug 22-26 to ~100/day, and on Nov 11-12 to ~80/day:

[![Screenshot_2018-06-23_19-29-58](https://ethresear.ch/uploads/default/original/2X/6/6681b01e770af76efaa38347d70af8f6480fd968.png)Screenshot_2018-06-23_19-29-58549×350 29.5 KB](https://ethresear.ch/uploads/default/6681b01e770af76efaa38347d70af8f6480fd968)

Transaction fees paid spiked during those same two intervals:

[![Screenshot_2018-06-23_19-30-56](https://ethresear.ch/uploads/default/original/2X/8/82c60bc571b6bbab92e92cd1a2cec99f45456e7e.png)Screenshot_2018-06-23_19-30-56549×273 22.9 KB](https://ethresear.ch/uploads/default/82c60bc571b6bbab92e92cd1a2cec99f45456e7e)

The last “fully normal” day before the August drop was Aug 19 (151 blocks) and the first “fully normal” day after is Aug 27 (155 blocks); the fees on those days are 209 and 378 BTC. During the peak, Aug 22 (89 blocks), fees rose to 542 BTC, and on the remaining days (~100 blocks) fees were at an average of ~400 BTC. Looking at the left side, this gives an elasticity of log(\frac{151}{89}) \div log(\frac{542}{209}) \approx 0.55. At the right side, transaction fees took longer to subside; they returned to ~280 at the beginning of September, when the block rate reached 175/day; this gives an elasticity of log(\frac{175}{100}) \div log(\frac{400}{280}) \approx 1.57.

In November, block rate went from 153 on Nov 9 to 80 on Nov 11-12 to 140 on Nov 13 and “returned to normal” to 152 on Nov 15. Transaction fees went from 320 BTC on Nov 9 to 783 BTC on Nov 12, eventually subsiding back at the 290 level on Nov 17. This gives an elasticity of log(\frac{153}{80}) \div log(\frac{783}{320}) \approx 0.72 on the left side and log(\frac{152}{80}) \div log(\frac{783}{290}) \approx 0.64 on the right side.

However, average fees may be misleading’ they reflect the average transaction, and not the marginal transaction (ie. the cheapest transaction that got included). We can also look at [Jochen Hoenicke’s mempool data](https://jochen-hoenicke.de/queue/#1,1y); we will use as our index the transaction fee level, in satoshis per byte, at which 2000 transactions are in the mempool (the rationale being that 2000 is the average number of transactions in a block, and so reflects the marginal (ie. cheapest) transactions that would make it into the next block). We will simply provide these levels for some key dates:

- Aug 19 (151 blocks): 20
- Aug 22 (89 blocks): 400
- Sep 1 (174 blocks): 200
- Nov 9 (153 blocks): 170
- Nov 13 (80 blocks): 500
- Nov 17 (167 blocks): 20

This gives possible elasticities of:

- log(\frac{151}{89}) \div log(\frac{400}{20}) \approx 0.18
- log(\frac{174}{89}) \div log(\frac{400}{200}) \approx 0.97
- log(\frac{153}{80}) \div log(\frac{500}{170}) \approx 0.60
- log(\frac{167}{80}) \div log(\frac{500}{20}) \approx 0.22

To summarize, we get (0.18, 0.22, 0.60, 0.97) using mempool (marginal) data, and (0.55, 0.64, 0.72, 1.57) using average fee data. The mode is 0.41 using marginal data and 0.68 using average data.

### Data from Ethereum

Here is the Ethereum [gas limit](https://etherscan.io/chart/gaslimit) over time:

[![Screenshot_2018-06-23_20-04-44](https://ethresear.ch/uploads/default/original/2X/0/0f6580733efa70b9f105f5414600eddae730e2f3.png)Screenshot_2018-06-23_20-04-44359×363 4.46 KB](https://ethresear.ch/uploads/default/0f6580733efa70b9f105f5414600eddae730e2f3)

And the Ethereum block time during the ice age:

[![Screenshot_2018-06-23_20-05-29](https://ethresear.ch/uploads/default/original/2X/e/e342a345fe1143d775f2465f76f9b742dc4afd1d.png)Screenshot_2018-06-23_20-05-29357×385 7.27 KB](https://ethresear.ch/uploads/default/e342a345fe1143d775f2465f76f9b742dc4afd1d)

Here are average fees during the same time period:

[![Screenshot_2018-06-23_20-09-26](https://ethresear.ch/uploads/default/original/2X/a/a5ae1a835051c1679f9fa698d2ad62769ed987a9.png)Screenshot_2018-06-23_20-09-26550×196 14.9 KB](https://ethresear.ch/uploads/default/a5ae1a835051c1679f9fa698d2ad62769ed987a9)

We will give average gasprices (in gwei) for some key dates:

- June 27-28: 31.5 and 43.4 (average 37.5)
- June 30-July 1: 27.2 and 26.6 (average 26.9)
- Oct 14: 24.2
- Oct 17: 14.2

Between June 28 and June 30, the gas limit increased from 4.7m to 6.7m (1.42x increase). Between Oct 14 and Oct 17, the block rate increased from 2900 to 6200 (2.13x increase). Between Dec 7 and Dec 11, the gas limit increased from 6.7m to 8m (1.19x increase). This gives possible elasticities of:

- log(\frac{6.7*10^6}{4.7*10^6}) \div log(\frac{37.5}{26.9}) \approx 1.05
- log(\frac{6200}{2900}) \div log(\frac{24.2}{14.2}) \approx 1.41

Of course, we can similarly look at marginal data. Here, we will scan through Ethereum blocks directly, and take the average of the 90th-percentile fees (ie. the Nth lowest fee in a block with 10N transactions) of the 5000 blocks starting from the start of a given day. Here are the values for key dates:

- June 27-28: 24.7 and 26.9 (average 25.8)
- June 30-July 1: 22.7 and 23.4 (average 23.0)
- Oct 14: 16.0
- Oct 17: 7.8

This gives possible elasticities of:

- log(\frac{6.7*10^6}{4.7*10^6}) \div log(\frac{25.8}{23.0}) \approx 3.09
- log(\frac{6200}{2900}) \div log(\frac{16.0}{7.8}) \approx 1.06

The first value is likely an outlier; the likely cause is wallet software that specified 20 gwei as a static gas price. In the second two cases, the wallet software was modified to have more dynamic gasprice setting, allowing gasprices to rise and fall more flexibly.

To summarize, the median elasticity is 1.23 looking at average data, and 2.07 looking at median data.

### Conclusions

In sum, Bitcoin’s demand elasticity appears to be around 0.4-0.7, and Ethereum’s around 1-2. Other, cruder, ways of estimating demand elasticity seem to confirm this on the Bitcoin side. Here is a chart of bitcoin’s block usage versus transaction fees:

[![Screenshot_2018-06-23_20-58-07](https://ethresear.ch/uploads/default/original/2X/c/c031994a2a4a72cfca9bb9db1030e481e04e1218.png)Screenshot_2018-06-23_20-58-07550×310 153 KB](https://ethresear.ch/uploads/default/c031994a2a4a72cfca9bb9db1030e481e04e1218)

Block usage increased by ~3x between 2015 May and 2016 Apr, and when blocks became full the growth in demand switched to fees, growing ~11x in 11 months. Taking the extremely crude assumption that the rate in growth of demand was constant, this suggests a demand elasticity of log(3) \div log(11) \approx 0.46.

Ethereum’s demand is more elastic likely because there is a wider array of applications that can be developed on Ethereum, with different costs per unit gas. For example, it is known that when gasprices went to an all-time high of ~70 gwei in early January, transaction counts hit an all-time high (despite no growth in *gas usage*), which showed that demand from more complex smart contract use cases was being substituted by demand for simpler transactions such as ETH and ERC20 token transfers.

In the case of Bitcoin, it is also known that many Bitcoin “tumblers” used to anonymize transactions [shut down](https://cointelegraph.com/news/worlds-largest-bitcoin-tumbling-service-announces-sudden-shutdown) between 2014-2017, raising the possibility that tumblers made up a large part of the low-cost-per-transaction demand and they were pushed out by higher-fee-paying “regular” transactions, though increasing law enforcement risk may have also been a factor.

It would be an interesting area of further study to evaluate this hypothesis, and also to try to more generally evaluate the composition of the Bitcoin and Ethereum blockchains at different fee levels, and try to understand the levels of willingness to pay transaction fees across different use cases, and particularly what use cases are most able to temporarily shut down “at a moment’s notice” in the event of sudden transaction fee spikes. Another possible challenge is evaluating the role of cryptocurrency competition in increasing any single cryptocurrency’s transaction demand elasticity.

### Sources

- http://etherscan.io
- Blockchain.com | Blockchain Charts
- https://www.smartbit.com.au/charts/blocks
- Johoe's Bitcoin Mempool Size Statistics

Here is the script used to calculate the 90th-percentile fees. Timestamps are the UTC time of the start of each day.

```auto
from web3.auto import w3

def binsearch(ts):
    value = 0
    skip = 2**22
    while skip:
        if value + skip <= w3.eth.blockNumber and w3.eth.getBlock(value + skip)['timestamp'] < ts:
            value += skip
        skip //= 2
    print('Binary search resolved:', ts, value)
    return value

def analyze(block):
    tot = 0
    for i in range(block, block + 5000):
        gps = sorted([w3.eth.getTransaction(tx)['gasPrice'] for tx in w3.eth.getBlock(i)['transactions']])
        tot += gps[len(gps)//10] if len(gps) else 0
        print(i, tot / (i+1-block))
    return tot / 5000
```

### Addendum (2020.09.02)

Here’s a quick “eyeball analysis” of the most recent rise from 10m to 12m.

The gaslimit went up from 10m to 12m from June 18-20:

[![Screenshot from 2020-09-02 14-45-21](https://ethresear.ch/uploads/default/original/2X/e/e83bee72aa67a8c65ae17609184cc0a72e2e539d.png)Screenshot from 2020-09-02 14-45-21425×312 10.5 KB](https://ethresear.ch/uploads/default/e83bee72aa67a8c65ae17609184cc0a72e2e539d)

The average transaction fee went down from 38.4 gwei to 29.5 gwei over the same time period:

[![Screenshot from 2020-09-02 14-46-38](https://ethresear.ch/uploads/default/original/2X/3/3bc12838e932ae59c545278fa95c50431bf9a47e.png)Screenshot from 2020-09-02 14-46-38420×231 10.6 KB](https://ethresear.ch/uploads/default/3bc12838e932ae59c545278fa95c50431bf9a47e)

This implies an elasticity of log(1.2) \div log(\frac{38.4}{29.5}) = 0.69. Clearly, this is a rough estimate from noisy data (eg. on Jun 22 the gasprice went back up, and before June 15 the gasprice was lower for clearly unrelated reasons) but it does roughly align with the other measurements that we saw above.

## Replies

**BenMahalaD** (2018-06-28):

Fantastic analysis. I’ve been thinking about block size fee economics a lot recently, so it’s nice to see hard data on this. Pricing the cost of a limited block space in terms of fees seem hard to do in a stable manner. A few comments:

When blocks are full, the real fee that the user pays is larger then the nominal fee because of uncertainty in transaction confirmation. In other words, if a user pays fee X in a hope to get confirmed in Y blocks, there is a chance that others will outbid them and they might not get in for Z >> Y blocks. This is effectively a queue cost, having to waste time in a queue until you are allowed to complete your transaction. This is especially bad in cases where you can’t cancel your transaction or increase your fee, because you might have paid much less then X for confirmation in Z blocks, but you end up charged for the full amount even though, if you had known you had to wait that long, you would not have made a transaction at all. This is probably what increases average fees so much over marginal fees, as people pay more then the marginal cost of the transaction in order to avoid the queue.

I’m been thinking about systems with softer block size limits that could expand when demand is high and contract when demand is low in order to prevent the chaotic fee increases that can happen in periods of high demand. I might make a stand alone post about this, but do you know if anyone else has thought about this before?

---

**vbuterin** (2018-06-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/benmahalad/48/76_2.png) BenMahalaD:

> I’m been thinking about systems with softer block size limits that could expand when demand is high and contract when demand is low in order to prevent the chaotic fee increases that can happen in periods of high demand. I might make a stand alone post about this, but do you know if anyone else has thought about this before?

I have. I’m actually writing a longer-form paper about this; one of the conclusions is that some flexibility is a good idea, and could be implemented via a block size limit structure where the miner can pay a fee `F(new_gas_limit)` (that gets burned) to expand the gas limit to some new value, where F is superlinear and hits some asymptote at a higher “real” gas limit. That said, the optimal policy likely reflects more flexibility on gas usage that reflects longer-term social costs (eg. history and state storage) and less flexibility on gas usage like computation and bandwidth.

---

**BenMahalaD** (2018-07-01):

Interesting. I was thinking of having it done on the user level then the miner level.

Define the market clearing fee as the equilibrium fee for which blocks are full, but there is no transaction backlog at the current price. In other words, all of the people who want to pay the current price for block space (or gas) can do so with no waiting, but there is no one who would be willing to pay the current price but cannot because blocks are full. (There may be a backlog of people who would do transactions at a lower price, but not at the current price).

A problem blockchains run into is that the network fee is generally far (x10 at least) below the market clearing fee. This means that people get comfortable paying 10 cents for a transaction; but, as people learn about the system and see the fee is low, more and more people use it. This causes a ‘full block sticker shock’ when blocks fill up and the system must now forcibly lower demand to meet supply. People feel cheated, even though the system could not remain decentralized and supply those prices. Effectively, early adopters are free riding off the unpaid cost of decentralization and it’s not until blocks fill up that the system notices and people have to pay.

Miners/validators have to receive a fee to cover the higher orphan rate for bigger blocks, but otherwise I think there must be some mechanism that can create a network fee that is closer to the market clearing fee that doesn’t go to them directly, to prevent side channels for lower fees.

I’ve been thinking of a system of ‘overflow’ areas in blocks, where, to be considered for one of these areas, you have to burn some minimum overflow fee (it can’t go to the miner/validator, since this means miners could fill these areas themselves for free). Their could be a series of these overflow areas with exponentially increasing minimum fees.

Then, you could have the network fee raise when the overflow areas were being filled. It would have to raise relatively slowly an attacker can’t just fill a few blocks to raise the network fee a lot, but over a few weeks or months the network fee would rise for everyone. This would mean that everyone who used the network would be bearing part of the cost of decentralization, even if blocks aren’t currently full. It could reduce the sticker shock of having fees go 10x when blocks fill up.

You could also have refunds for people who set the network fee to an overflow area, but were able to get into the regular block space instead. (Although this might require a consensus rule for how you fill blocks into transactions, to prevent griefing). Someone wanting to make sure they got a time-sensitive reaction though could set the fee to be high, and then get a refund if they miscalculated. This would let people set their fees to the price they were willing to pay instead of the price they think they can get away with.

The gains from this might mostly be mental. Paying a high fee and seeing it was unnecessary feels bad, as does paying a low fee then having to pay attention to make sure it goes though and having to bump it later

