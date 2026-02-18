---
source: ethresearch
topic_id: 5999
title: How necessary are State Fees?
author: admazzola
date: "2019-08-19"
category: Economics
tags: []
url: https://ethresear.ch/t/how-necessary-are-state-fees/5999
views: 1044
likes: 3
posts_count: 2
---

# How necessary are State Fees?

So at this moment, full Ethereum node state is 140GB and growing linearly .

Proof: https://etherscan.io/chart2/chaindatasizefast

That is absolutely the entire state of the network.  All you need.  To me, 140GB isn’t that much.  2TB solid state drives are the norm now and can be purchased at little monetary cost.  In the next decade, we will see 4TB and 16TB drives become cheap and by that time, the total eth node state will be roughly twice or 4x what it is now at current pace of growth.

So why exactly are state fees necessary? And if so, WHEN are they necessary?  Next year? Next decade? Next century?

## Replies

**jgm** (2019-08-20):

(The chart you link to is the pruned state, not the entire state, but most people do only care about the pruned state).

Personally I think that state fees in Ethereum 1 would be a mis-step; contracts and storage have not been designed to take this idea in to account and would lead to a lot of confusion, unhappiness and distrust.  In short: the downsides of bringing state fees to Ethereum 1 outweigh the benefits when Ethereum 2 is on the horizon (at which point many projects will migrate to and most new projects would start on Ethereum 2).

Ethereum 2 is basically a new start so having state fees built in to the design means that execution environments can build their own mechanisms for users.  To take a simple example: if state rent was introduced to Ethereum 1 and I have a token balance on a given contract “someone” has to pay for the entirety of the contract’s storage to stick around or I lose my tokens.  In Ethereum 2 each account’s balance would be held in an “owned state” that is controlled by the token contract but paid for separately from the rest of the state, so I would only have to pay for my piece of the storage (note this isn’t, as far as I know, how things will work it’s just an example of how they might).

