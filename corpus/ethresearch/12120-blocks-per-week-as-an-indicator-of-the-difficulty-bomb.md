---
source: ethresearch
topic_id: 12120
title: Blocks per week as an indicator of the difficulty bomb
author: quickBlocks
date: "2022-02-26"
category: Data Science
tags: []
url: https://ethresear.ch/t/blocks-per-week-as-an-indicator-of-the-difficulty-bomb/12120
views: 23144
likes: 46
posts_count: 31
---

# Blocks per week as an indicator of the difficulty bomb

**Go to the bottom for the latest chart.**

This chart (blocks produced per week) may be of interest to the core devs as they plan the timing of the hard fork for the Merge.

Blocks produced per week stands in for the number of seconds it takes on average to produce a block, which stands in for the effect of the difficulty bomb.

Here’s the repo for the ‘R’ code that creates the chart: [tokenomics/explorations/difficulty at main · TrueBlocks/tokenomics · GitHub](https://github.com/TrueBlocks/tokenomics/tree/main/explorations/difficulty). The data was created using this code: [trueblocks-core/src/other/difficulty/difficulty.cpp at fc4edc17c75739393e93add4ef805c137b747b03 · TrueBlocks/trueblocks-core · GitHub](https://github.com/TrueBlocks/trueblocks-core/blob/fc4edc17c75739393e93add4ef805c137b747b03/src/other/difficulty/difficulty.cpp).

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/cbb9ba1b8cb52ce56819fe2fb16af1fa899e5460_2_690x401.png)image2702×1574 339 KB](https://ethresear.ch/uploads/default/cbb9ba1b8cb52ce56819fe2fb16af1fa899e5460)

The vertical dashed grey lines are the hard forks.

The pink vertical line is June 15th

The horizontal grey dashed lines are how many blocks would be produced in a week if the per-block production were 14 seconds, 16 seconds, 18 seconds, etc.

I think it will be pretty easy to see where the bomb is in its ‘explosion.’ You can see that it stays pretty flat until it goes off, but once it goes off, it really does explode.

I’ll try to produce this once a week (on Friday’s), but if I forget and you’all find it useful, please poke me.

This data was produced with [TrueBlocks](https://trueblocks.io), which all you’all should check out. It’s really good for data science with on-chain data.

Thanks to OmniAnalytics and Tim Beiko for helping me get this done. Hope it helps.

Cheers.

## Replies

**quickBlocks** (2022-03-04):

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d5a0355a04ddf38d2875f7b2be14d8021c445430_2_690x427.png)image2534×1570 316 KB](https://ethresear.ch/uploads/default/d5a0355a04ddf38d2875f7b2be14d8021c445430)

---

**yulesa** (2022-03-07):

It can be automatized using Dune.

https://dune.xyz/yulesa/Blocks-per-Week

---

**quickBlocks** (2022-03-11):

Oh. This is great. So I don’t have to update it. Cheers.

---

**yulesa** (2022-03-11):

The graph is a little clunky, though. From my perspective the bomb is starting to be visible.

---

**quickBlocks** (2022-03-11):

It doesn’t update already?

As far as the bomb, I don’t think it’s started to go off yet.

That’s why I had the horizontal lines across at each ‘second’. So the top-most one is how many blocks there would be in a week *if* each block was 14 seconds. If each was 16 seconds, it would be down at the next horizontal line. This is the latest chart – you can see it hasn’t really started to decend.

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e2540bcde2716fcb23a2e97a3f318257eccc6a10_2_690x426.png)image2548×1576 296 KB](https://ethresear.ch/uploads/default/e2540bcde2716fcb23a2e97a3f318257eccc6a10)

---

**quickBlocks** (2022-03-17):

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/6bd1bf554a171db529e3f699643d46bef6a7d721_2_690x389.png)image2980×1684 461 KB](https://ethresear.ch/uploads/default/6bd1bf554a171db529e3f699643d46bef6a7d721)

It would be great to get someone to double-check this work? Repo link above. The solid red line is June 15. The dashed red lines are each time the bomb’s period was at period 31 for comparison. (Period 31 is where it was reset in December.)

---

**quickBlocks** (2022-03-25):

Latest installment. I guess we’re starting to see a very slight effect. Notice from previous bombs how quickly it comes once it starts to come. Red vertical line is June 15.

Stay tuned…

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/706b101983f9b03b9ef46330918fd22aa4c18c94_2_690x461.jpeg)image2642×1766 325 KB](https://ethresear.ch/uploads/default/706b101983f9b03b9ef46330918fd22aa4c18c94)

---

**quickBlocks** (2022-04-01):

Latest installment. I see a slight dip. I expect we will start seeing an effect in the coming weeks. A higher hash rate delays the first ‘appearance’ of the bomb, but there’s a concern that once the bomb appears it will be more virulently.

The horizontal grey lines are the number of seconds between blocks given the number of blocks produced in a week on the y-axis.

I’m going to post another chart shortly to show another view.

[![image](https://ethresear.ch/uploads/default/optimized/2X/4/43cad4ac294e3f90446f2a9a6431ee04d1d151de_2_667x500.png)image2396×1796 371 KB](https://ethresear.ch/uploads/default/43cad4ac294e3f90446f2a9a6431ee04d1d151de)

---

**quickBlocks** (2022-04-01):

This chart shows the real block number (in red), the fake block number (in green), and the bomb’s period (the staggered blue line which changes discontinuously every 100,000 blocks).

The dashed grey horizontal line is what I call the “We should start paying attention” line. If you look closely at previous bombs, you can see the slight diminishment in the block number over time. We’re not seeing that yet, but stay tuned.

[![image](https://ethresear.ch/uploads/default/optimized/2X/e/e28ef3966f222a8ed3a10e8e59238342dcdad02b_2_690x428.png)image2542×1578 386 KB](https://ethresear.ch/uploads/default/e28ef3966f222a8ed3a10e8e59238342dcdad02b)

---

**nollied** (2022-04-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> The dashed grey horizontal line is what I call the “We should start paying attention” line. If you look closely at previous bombs, you can see the slight diminishment in the block number over time. We’re not seeing that yet, but stay tune

is a “bomb” a stark decrease in the block-production rate over a certain period of time? what is it about the time preceding hard-forks that cause such down-spikes? is it because node-runners deactivate their nodes to update the software?

what does this mean for the transaction rate for ethereum? does it remain at a stable rate? do these bombs have measure-able impact on gas prices?

---

**quickBlocks** (2022-04-02):

I’ve written about a lot of this here: [Adventures in Difficulty Bombing. An exercise in predicting the future… | by Thomas Jay Rush | Coinmonks | Medium](https://medium.com/coinmonks/adventures-in-difficulty-bombing-837890476630). That link also has links to a bunch of other articles as well.

About the impact on gas price, I’m not sure. It has had, mistakenly I think, a serious effect (at least on the arguments surrounding) the block reward, but I don’t know about gas prices.

---

**quickBlocks** (2022-04-11):

It’s coming…

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f89c60dafd9fec18c6312c510750e750e03ab116_2_690x429.png)image2538×1580 371 KB](https://ethresear.ch/uploads/default/f89c60dafd9fec18c6312c510750e750e03ab116)

---

**quickBlocks** (2022-04-19):

At block 14,600,000, which happened this week, we entered into period 39, which based on previous bombs is when we usually start seeing a diminishment in block times. I’m not seeing that yet. This is not yet concerning, but is becoming “interesting.” (See below).

Here is an estimate, assuming no growth in block times, of when the next three doublings in difficulty will happen. (A doubling happens when the period changes – period = fakeBlockNum/100000 – fakeBlockNum = realBlockNum-10,700,000 – the additional difficulty at each block is 2^period).

```auto
blockNumber	timestamp	date	name
14000000	1642114795	2022-01-13 22:59:55 UTC
14100000	1643450273	2022-01-29 09:57:53 UTC
14200000	1644784417	2022-02-13 20:33:37 UTC
14300000	1646123109	2022-03-01 08:25:09 UTC
14400000	1647466065	2022-03-16 21:27:45 UTC
14500000	1648811420	2022-04-01 11:10:20 UTC
14600000	1650160464	2022-04-17 01:54:24 UTC
14700000	1651492241	2022-05-02 11:50:41 UTC	 (est flat)
14800000	1652822241	2022-05-17 21:17:21 UTC	 (est flat)
14900000	1654152241	2022-06-02 06:44:01 UTC	 (est flat)
```

In this estimate, which extends to period 42 (the same period just prior to the Byzantium fork–see above charts), I add NO additional seconds to each block. This may seem conservative, but it tries to take into account the possibility that the much higher hash rate we’re seeing now (compared to the past) may be masking the increasing difficulty of each change of period (bomblet).

This next group of data is a slightly less conservative estimate showing a one-second slowing down of blocks with each doubling. If this happened, we may be at 16-second blocks by the end of June):

```auto
blockNumber	timestamp	date	name
14000000	1642114795	2022-01-13 22:59:55 UTC
14100000	1643450273	2022-01-29 09:57:53 UTC
14200000	1644784417	2022-02-13 20:33:37 UTC
14300000	1646123109	2022-03-01 08:25:09 UTC
14400000	1647466065	2022-03-16 21:27:45 UTC
14500000	1648811420	2022-04-01 11:10:20 UTC
14600000	1650160464	2022-04-17 01:54:24 UTC
14700000	1651837086	2022-05-06 11:38:06 UTC	 (est onesec)
14800000	1653730218	2022-05-28 09:30:18 UTC	 (est onesec)
14900000	1655823350	2022-06-21 14:55:50 UTC	 (est onesec)
```

My growing concern is that due to a much higher hash rate, unlike previous bombs, this bomb’s effect may not appear at all until it appears massively. (In other words, this bomb may truly explode!)

The higher hash rate may be hiding the initial, smaller shocks to the system (the bomblets) which are being recovered from more quickly, so much so that they don’t reveal themselves in the weekly production. (I looked at a daily chart that also does not show much of a slow-down.)

The concern is that once the system loses its ability to recover from the shock of a doubling, it will lose that ability in a serious way.

I’ll keep watching it.

We should start seeing a recognizable diminishment in block times soon. If not, we’ll need to dig deeper.

---

**watersky** (2022-04-25):

You can also track this on Coin Metrics [here](https://charts.coinmetrics.io/network-data/#3712)

[![ETH_Mean_Block_Time_and_Daily_Block_Count](https://ethresear.ch/uploads/default/optimized/2X/0/0b08d7d06b7fe5113e68a7499ccaa33a429d6cb8_2_690x407.png)ETH_Mean_Block_Time_and_Daily_Block_Count1200×709 80.2 KB](https://ethresear.ch/uploads/default/0b08d7d06b7fe5113e68a7499ccaa33a429d6cb8)

---

**quickBlocks** (2022-04-29):

Latest chart fresh off the presses…

[![image](https://ethresear.ch/uploads/default/optimized/2X/f/f784a28794a8a5a252039255b7bf5f8e7794f58d_2_690x435.png)image2828×1784 467 KB](https://ethresear.ch/uploads/default/f784a28794a8a5a252039255b7bf5f8e7794f58d)

---

**quickBlocks** (2022-05-05):

Chart as of today. The bomb is clearly starting to show. It’s reasonable to estimate its future progress based on previous bombs.

[![image](https://ethresear.ch/uploads/default/optimized/2X/6/69dbfa4fe48c6385d673ede62c51ec572a882413_2_690x489.jpeg)image1920×1363 199 KB](https://ethresear.ch/uploads/default/69dbfa4fe48c6385d673ede62c51ec572a882413)

---

**CryptoWhite** (2022-05-07):

I guess a new hardfork for delaying the difficulty bomb is around the corner

---

**jgm** (2022-05-11):

On the basis of daily block time we’re already at the point where Arrow Glacier kicked in.

[![blocktime-recent](https://ethresear.ch/uploads/default/optimized/2X/9/9530a21caf9cca95415a8500a8d8bf1d5d04adf1_2_690x342.png)blocktime-recent1785×885 23.7 KB](https://ethresear.ch/uploads/default/9530a21caf9cca95415a8500a8d8bf1d5d04adf1)

---

**quickBlocks** (2022-05-12):

Some new charts. Back in December, I was asked to predict 15-second blocks by mid-June. Impossible to be certain, but I wouldn’t be surprised if this were the case.

The red line is June 15.

The dashed red lines are the last time we were at the same period in each of the previous forks. Much higher hash rates now has tamped down the effect, but that won’t last forever.

The blue dashed vertical lines are the previous forks.

The table tries to compare past forks with the current one and predicts the next bomblet to be around May 18.

[![Screen Shot 2022-05-12 at 6.48.38 PM](https://ethresear.ch/uploads/default/optimized/2X/c/cb2776cd40f3f2af51b6429eac8897606aa9a5a5_2_690x416.jpeg)Screen Shot 2022-05-12 at 6.48.38 PM1920×1158 93.3 KB](https://ethresear.ch/uploads/default/cb2776cd40f3f2af51b6429eac8897606aa9a5a5)

[![Screen Shot 2022-05-12 at 6.22.36 PM](https://ethresear.ch/uploads/default/optimized/2X/b/bd91229424f2306ea02d6f33fc86f550b3af015b_2_690x310.jpeg)Screen Shot 2022-05-12 at 6.22.36 PM1920×864 298 KB](https://ethresear.ch/uploads/default/bd91229424f2306ea02d6f33fc86f550b3af015b)

---

**quickBlocks** (2022-05-24):

Latest chart as of last night…I’m quite confident that the is the correct data, but I would be happy to have others produce similar results independently if possible.

It looks to me like it’s getting close the time to make a decision. I think we can expect a fairly quick decline from here (based on previous bombs).

[![image](https://ethresear.ch/uploads/default/optimized/2X/5/580bb07af5b190bcfa69a2b778a8bf204faeddb3_2_690x385.jpeg)image1920×1072 90.3 KB](https://ethresear.ch/uploads/default/580bb07af5b190bcfa69a2b778a8bf204faeddb3)


*(10 more replies not shown)*
