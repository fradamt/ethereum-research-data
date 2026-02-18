---
source: ethresearch
topic_id: 10323
title: Will PoS result in the geographic clustering of validators?
author: Mister-Meeseeks
date: "2021-08-13"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/will-pos-result-in-the-geographic-clustering-of-validators/10323
views: 1749
likes: 3
posts_count: 2
---

# Will PoS result in the geographic clustering of validators?

One under-appreciated aspect of the PoS transition is that it’s a lot easier to relocate a validator node than a mining operation. Thus we’d expect block validators to be much more geographically mobile than the current block miners. Which means, if there’s even a small advantage to a certain geolocation we’d expect a disproportionate number of validators to cluster there. That’s obviously bad for the resiliency, security and decentralization of the network.

In particular my tangible concern is related to MEV arbitrage. The bulk of centralized exchange price discovery occurs in Tokyo. The FTX, Binance and Huobi matching engines all run in a single datacenter.

Being co-located to these exchanges is a major advantage to a validator engaged in MEV. Having a low latency data feed to order book activity means the ability to arbitrage against the decentralized exchanges. In contrast running a validator outside Japan adds hundreds of milliseconds of latency. With 12 second block times, putting your validator in Tokyo is worth tens of million a year to a $1 billion CeX/DeX arbitrage strategy.

In particular, Tokyo is an especially high-risk as a geolocation for network clustering. It’s at high risk for earthquakes and tsunamis. What happens to the network if 90%+ of the validators go offline at the same time? To fix this problem, I think the protocol has to either 1) completely eliminate validator’s ability to extract MEV. Or 2) explicitly incentivize geographic diversity through some rewards scheme that outweighs MEV extraction.

## Replies

**kelvin** (2021-08-13):

That is a very insightful observation. Validators (or block-builders in a sequencer auction mechanism) will likely try to get as much market-data from the CEXes as possible to decide how to extract MEV in a block. Even if we have sequencer auctions, validators in Japan may end up receiving blocks that pay slightly more fees on average.

I think that If we could have a way to have only the block-builders be concentrated in Japan, with the validators being free to run anywhere, that would be good enough, but I can’t figure out how to do it.

I like your idea of incentivizing geographic diversity. Maybe that can happen naturally if there is some small advantage to be had by getting to see some mempool transactions faster than other validators do.

