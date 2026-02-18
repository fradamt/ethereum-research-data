---
source: ethresearch
topic_id: 10012
title: Crypto Native CPI Using Only Onchain Signals/Prices for Energy/Food/Housing Possible?
author: EazyC
date: "2021-07-06"
category: Economics
tags: []
url: https://ethresear.ch/t/crypto-native-cpi-using-only-onchain-signals-prices-for-energy-food-housing-possible/10012
views: 1665
likes: 3
posts_count: 10
---

# Crypto Native CPI Using Only Onchain Signals/Prices for Energy/Food/Housing Possible?

We are building a crypto native CPI called the FPI at our project so that the new generation of algostables like RAI, OHM, FLOAT, FRAX can peg to a floating standard of living index that is purely governed, updated, and published onchain.

We’re doing research if we can use something like BTC’s PoW difficulty as a gauge for global energy price averages standardized against BTC’s mcap. But the main issue is that ASIC efficiency is difficult to bring onchain without trusting an oracle whereas difficulty can be easily brought trustlessly through a BTC SPV smart contract. We could create some kind of Moore’s Law input where the expectation is doubling ASIC efficiency every 2 years and normalize against that+BTC mcap, but there must be better ways, no?

My main question here is: even if we figure out how to bring a trustless ASIC measurement, is there any research done on onchain, endogenous proxies for food/consumables and housing/rent? Assume we want global average and don’t care about particular regions for simplicity at first. That seems very difficult to measure without an oracle setup but worth asking here. Ideally it wouldn’t be just tracking the TWAP price of some custodial quasi-security token on AMMs since that’s not very novel. What interesting areas are there to explore in this crypto native CPI protocol that can be oracle-minimized/no-oracle?

## Replies

**MicahZoltu** (2021-07-07):

If your goal is to create a stable coin, rather than a pegged coin, then you can trust that the rate of improvement in ASIC efficiency is low enough that it can be ignored.  With a stable coin, the goal is to create an asset that is stable against some metric (cost of energy in this case) over time but this doesn’t mean it has to maintain a perfect 1 to 1 peg.  It just means that you can buy about the same amount of good X today as you will be able to buy tomorrow.

I’m a big fan and have blogged (I think) in the past about using PoW as a way to get the approximate cost of energy on-chain in a totally trustless way (no oracles needed).

For the other things you mentioned, you can’t do trustless.

---

**EazyC** (2021-07-07):

Thanks for your reply Micah. If you have a link to your blog posts would love to read them. We are doing extensive research in this area of crypto native CPI (we call it the FPI) so the energy component is very relevant.

I understand the stablecoin isn’t going to be tightly pegged to the price index and it can “float” to loosely track the FPI. But the price index also can’t be completely inaccurate for extended periods of time

As for ASIC efficiency, I don’t think we can discount it? Because it is an independent variable no? For simplicity sake, let’s say a new ASIC came out that was 100x more efficient than anything before. And for simplicity sake let’s also assume that BTC market cap and global energy prices stayed flat (no change). Wouldn’t the difficulty go higher up to 100x if the new ASIC permeated every BTC mining operation? Or at least it would 20x+ the difficulty. The point is, it would be a statistically significant change to hashing difficulty. If hashing efficiency per kW is not normalized how would our FPI not become very inaccurate since it is blind to hardware efficiency gains. There’s 3 variables here: BTC mcap, PoW hashing difficulty, efficiency per kW/h.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> For the other things you mentioned, you can’t do trustless.

Yes it does appear that there’s no current way to find a tight proxy for food/consumables and real estate but I don’t want to give up just yet. I think there could be very clever designs. There’s also some really smart people in this very forum that might have good theories. Maybe other prominent ETH Foundation researchers like Vitalik and others have some ideas in this field.

---

**MicahZoltu** (2021-07-08):

I did some digging and can’t find anything I wrote on the subject.  It may have been in a transient communication channel like Twitter or Discord or something.  ![:cry:](https://ethresear.ch/images/emoji/facebook_messenger/cry.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> For simplicity sake, let’s say a new ASIC came out that was 100x more efficient than anything before.

This is definitely a theoretical problem, but I am not convinced it is one that we need to worry about.  What are the odds that some new SHA256 ASIC breakthrough happens that results in a 100x increase in hashes per watt, and this happens on a short time frame?

As long as the hashes per watt remains relatively stable over time with only small increases in efficiency over time, then your stablecoin will simply decrease in value (relative to the cost of energy) slowly over time, much like how *many* modern currencies do.

If you are trying to create a token that is stable against the cost of energy *long term* then things become *much* more complicated.  I personally don’t recommend chasing that goal, as I think you’ll find that just targeting short-term stability against energy mostly solves the desired problems.

---

**EazyC** (2021-07-09):

I agree it’s a theoretical problem but it can also be empirically tested right? Historical hashrate from [blockchain.com](http://blockchain.com). If this was normalized by BTC mcap, would it actually yield any kind of reliable energy price average (globally or otherwise. Just any kind of reliable measure)? My intuition, without doing any math, says no since there was zero trend in hashrate decrease during the 17-18 bear market as BTC shed 80% of its mcap in 12 months and hashrate trend still continued to climb? So either energy must have gotten significantly cheaper (I don’t think so?) or ASIC efficiency also increased a lot.

[![Screen Shot 2021-07-09 at 11.44.28 AM](https://ethresear.ch/uploads/default/optimized/2X/4/4321dc85f93a38329f6ce6099e64e45e0f21cf3e_2_533x500.png)Screen Shot 2021-07-09 at 11.44.28 AM919×862 30.3 KB](https://ethresear.ch/uploads/default/4321dc85f93a38329f6ce6099e64e45e0f21cf3e)

---

**EazyC** (2021-07-09):

Also, this might sound even more farfetched, but if digital land (Decentraland and other metaverse games) end up exhibiting any kind of network effect similar to real land prices, perhaps we can use the oldest digital land plots and their rising (or dropping) prices as the real estate component? Or that might be too devoid from reality at that point and taking “crypto native” CPI too far to be practical. Just trying to think about how to sidestep the “oracle problem” entirely so that the price index we are building does not even have to answer the age old oracle question and remains entirely anchored to onchain assets while providing the same (ideally better) utility of the CPI for soft pegging an algostable.

---

**MicahZoltu** (2021-07-09):

Hashrate is a very lagging indicator, and while you would want to factor that in, it is something that is acceptable for a long term stable coin.  When price of the other asset (BTC in this case) changes rapidly, hashrate won’t change to match right away.  If the price then falls afterward, the hash rate may still be behind.

---

**EazyC** (2021-07-12):

That makes sense. But then how would a stablecoin protocol “soft pegged” to this price index enact monetary policy? Holding BTC in the treasury to partially back the stablecoin could do it but as you’re saying, BTC price could be changing very rapidly than the lagging hashrate indicator so it seems somewhat decoupled? Or would holding BTC proportional to the energy index weight be sufficient for that component of the price index?

---

**MicahZoltu** (2021-07-12):

I personally am a fan of fully collateralized systems like Maker.  You would use the hashrate as the price targeting mechanism, but you would develop a separate mechanism for having the price actually hit the target.

---

**EazyC** (2021-07-13):

I’m a fan of that system too, but I personally also think that a protocol controlled value system where the protocol’s own balance sheet expands like Olympus DAO is a good idea as well. Perhaps a hybrid approach of these two systems is a good idea.

