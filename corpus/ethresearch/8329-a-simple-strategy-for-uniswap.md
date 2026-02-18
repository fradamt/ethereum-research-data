---
source: ethresearch
topic_id: 8329
title: A simple strategy for Uniswap?
author: kladkogex
date: "2020-12-07"
category: Economics
tags: []
url: https://ethresear.ch/t/a-simple-strategy-for-uniswap/8329
views: 6182
likes: 3
posts_count: 11
---

# A simple strategy for Uniswap?

Front-runners take lots of money on Uniswap. The question is if there is a simple-but-better strategy to pay less money to front runners.

One strategy I came up with is to write a script that observes Uniswap pending transactions and issues matching ones.

As an example, if I want to buy, say, 10 tokens  of X,  the script will wait until it sees someone in the pending queue selling, say, 6 tokens, and then immediately issue a high gas price transaction to buy 6 tokens.

The question is whether the strategy above is better than simply buying on Uniswap immediately.

## Replies

**MaverickChow** (2020-12-18):

I don’t know of cheaper way to suffer as a result of getting front-run. But I think I have a way to counteract the front-runners. Front-runners behave like HFTs in the traditional markets whereby HFTs have early access to all incoming orders to front-run before anyone else can see such orders, but the only difference is crypto front-runners refer to the blockchain pending transactions to front-run large orders.

So one possible way (example) to counteract this parasitic and unproductive behavior is to send huge fake sell transaction order (if you want to buy) at very low gas (to ensure it will take a long time for confirmation) while you also queue with a genuine buy order at the same time, so that front-runners will front-run your huge fake sell order by selling at slightly lower price to your genuine buy order. Once your genuine buy order gets filled, you can quickly cancel out your huge fake sell order by sending a new transaction to yourself (same nonce as that huge fake sell order) at much higher gas for faster confirmation to override that previously huge fake order. Vice versa if you want to genuinely sell.

---

**kladkogex** (2020-12-18):

Interesting :))

I  will try ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**lightcycle** (2021-02-17):

The frontrunners I see on-chain use contracts that revert.  It’s ironic in a sense that they build in the anti-frontrunning features while frontrunning other contracts.

I’ve decompiled a few contracts and see that they usually stick to around a 3% slippage

---

**pmcgoohan** (2021-03-07):

It’s a great idea- called ‘spoofing’ in the traditional markets, and illegal there (although it happens all the time).

But you’ll get wiped out if you’re up against a miner. They’ll include your big transaction however low the gas fee just so they can front run it, and then front run your small transaction too. Eeek

---

**mar2424** (2021-03-08):

We have to look at memepool, where miners can reorder transactions and also maybe neglect some transactions by purpose. a small tool to scrutinize memepool will be more helpful. someone has benn working on it but still needs further polish.

---

**Mister-Meeseeks** (2021-03-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/maverickchow/48/2858_2.png) MaverickChow:

> So one possible way (example) to counteract this parasitic and unproductive behavior is to send huge fake sell transaction order (if you want to buy) at very low gas

This strategy won’t work. As a frontrunner, typically what you do is reconstruct the pending block form the mempool. Or maybe an expanded pending block, with higher block size. But the idea is that you have a pretty good idea what’s likely to get mined in the next few blocks.

You’re not going to target a transaction until it’s about to be mined. A transaction with low gas won’t get frontrun until if/when it’s at the top of the mempool gas queue.

---

**0xkangaroo** (2021-03-11):

This is a very fascinating problem. It sounds like you’re trying to frontrun the frontrunners with very high gas transactions. Won’t this further exacerbate the problem of high gas prices though? It sounds like a method to make L1 even more unusable.

---

**Mister-Meeseeks** (2021-03-15):

To a first order approximation, I’d say bidding wars don’t change the block inclusion fee to any significant degree. Whether a bot bids 20,000 Gwei instead of 100 Gwei, it still consumes the same amount of block space.

It’d be pretty rare for more than two bidding wars in a single block. (The major exception is when the price of ETH/USD swings exposing many separate Defi arbitrages at once.) A Uniswap trade with a gas refund uses about 60,000 gas out of the 12.5 million block limit. So “ordinary” transactions almost never have to worry about competing with the gas bid at the top 1% of the block.

The block inclusion, or even median fee is not meaningfully affected. In the same way that billionaires competing to buy beachfront property in Oahu doesn’t meaningfully increase the price of housing in Peoria.

Bidding wars may potentially decrease the gas impact of front running. If auctions never get too expensive than many marginal front runners would be tempted to make an attempt. The lower the gas fee the more a free option it is. (Even if you lose the bidding war a failed Uniswap trade costs about 26,000 gas.) Fierce bidding wars probably drive marginal players out, which frees up block space, lowering prices at the bottom of the block, despite increasing prices at the very top.

That being said, bidding wars may have an indirect impact through gas oracles. Hopefully gas oracles use non-parametric statistics, like median. But imagine a gas oracle that uses arithmetic mean. It sees 100 transactions at 100 Gwei and one at 20,000 Gwei. Then it tells its users to bid 300 Gwei to get mined. If enough ordinary users were using that gas oracle, then even a small right tail of super-high gas trades could indirectly raise everyone’s costs.

---

**0xkangaroo** (2021-03-15):

I agree with everything you’ve said above the following quote:

![](https://ethresear.ch/user_avatar/ethresear.ch/mister-meeseeks/48/5638_2.png) Mister-Meeseeks:

> That being said, bidding wars may have an indirect impact through gas oracles. Hopefully gas oracles use non-parametric statistics, like median. But imagine a gas oracle that uses arithmetic mean.

But this is the main concern that I have, and I do not think these secondary effects are insignificant.

First of all, I don’t think gas oracles do this as they are not incentivized to provide the “best” price for regular individuals. They are only incentivized enough to show a “real-enough” price that people have *some* visibility as to the relative fluctuations of the system.

And more importantly, the gas strategies used by many (not all) bots may also not be this sophisticated either. And this activity does percolate down to affect people executing “regular” transactions. Keep in mind that bots do not need to be *maximally* profitable all the time, just profitable enough that they can operate autonomously in a relatively small and inefficient market.

Since we are discussing implementations where we are not privy to, there can be no real resolution in our difference of opinion. But it does seem that we do agree on the existence of secondary effects, but maybe we differ on the degree. Thank you for the push back in refining my stance.

---

**kladkogex** (2021-04-02):

My recent experience with Uniswap is that you can set almost zero gas price, and miners will accept the transaction, if the value is significantly high

