---
source: ethresearch
topic_id: 10004
title: High-frequency trading and the MEV auction debate
author: kelvin
date: "2021-07-06"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/high-frequency-trading-and-the-mev-auction-debate/10004
views: 5028
likes: 12
posts_count: 3
---

# High-frequency trading and the MEV auction debate

I’ve worked for four years developing market making and arbitrage bots at the brazilian futures exchange, so I wanted to share some insights here that may be useful for the MEV auction debate.

Probably the most profitable HFT strategy is a relatively simple one that I call the ‘unidirectional arbitrage’. The way it works is that you see some large trade moving the price of some very liquid market, and then you copy that price movement in all other markets that are equivalent or highly correlated with it.

For example, if you see one big trade moving up the mini-S&P futures you can do all of the following:

- Buy micro-S&P futures
- Buy all stocks that are highly-correlated with the S&P (at NYSE and NASDAQ)
- Buy ETFs that follow similar indexes
- Buy call options for the S&P and for stocks
- Sell put options for the S&P and for stocks

Of course, none of this is guaranteed a profit, as the prices may fall before you close your position, but given that you will be doing thousands of trades per day, you really just need to win on average, which you definitely will if you can manage to do your trades before everyone else can.

There are basically three ways of having your trades execute first.

1. If the exchange you are trading at has a “fair” or a “first-in-first-out” ordering policy, then you need to be really fast. If you are trading in two markets in the same exchange then you may need FPGAs, overclocked CPUs, special code optimization, expensive network interfaces, and so on. For different exchanges you will need straight-line submarine cables, microwave towers, or maybe these new hollow-core fibers. There may also be some tricks to get the information first, such as placing small orders in the market to let you know about big trades before everyone else.
2. If ordering has some random element, then you need to send tens or hundreds of orders and hope that one of them will execute. This may happen accidentaly, for instance, if the exchange has several gateways with multiple processes running. The more orders you send, the higher the chances that you’ll get lucky with the process scheduling.
3. If instead you have to pay to get a better order endpoint or to get the trade information faster, then you have to pay it. While in principle some exchange could auction the fastest connection for a single highest bidder, I’ve never seen an exchange to that, so in general, you still need techniques from (1) and (2) to win.

Of course, in practice there is often a mix of the three ordering strategies (you can pay for colocation, lower latency is usually first, but there is some random component). Sometimes there are also some other tricks that only insiders know and that work only in some exchanges.

While this is my experience with traditional finance, HFT in crypto probably works exactly the same in the centralized exchanges. In DeFi of course it is totally different because the orders are all in the mempool to be seen and can be frontrunned, sandwitched, and you can even place and remove huge amounts of liquidity from the pools to extract all the trading fees.

These transaction reordering exploits are so hurtful right now that many are arguing that latency arbitrage is not a problem by itself, because of some positive consequences of arbitraging such as allowing fast liquidations and propagating price information.

As an insider that made quite some money by “propagating information” a few microsseconds earlier than the others, I disagree. All revenue made by arbitrators has to come out of somewhere, and where it usually comes from is from the liquidity providers.

In centralized exchanges, the money comes out of the market makers who respond with higher spreads. The exchanges don’t like the way the orderbook looks with these high spreads, so they create subsidies with negative fees (maker rebates). Of course, they have to charge the high “taker fees” to pay for it.

In decentralized exchanges, the arbitrage revenue come out disguised as very high *impermanent loss*, which people seemed to have regarded as a normal fact of life than can only be compensated by high trading fees or liquidity mining, which by the way is nothing but another type of subsidy.

Yes, traders do need to be rewarded for incorporating information into the markets, and statistical arbitrage needs to be rewarded, but only inasmuch as it is the information incorporated is really unique. One shouldn’t be paid to ‘incorporate’ obvious information a few microsseconds before someone else would. A good description of the problem is given by [Budish et al](https://academic.oup.com/qje/article/130/4/1547/1916146?login=true).

The proposed solutions for transaction ordering in DeFi mirrors the three ordering components  mentioned above:

1. You can propose some type of first-in-first-out mechanism in which transactions sent first arrive first.

Not only this is a very hard task in decentralized setting, the goal may even be undefined! This may be a bit theoretical, but at least according to general relativity you can’t even talk meaningfully about ordering events that happen at different positions in space. If one could agree on what exactly is the goal here, this might help alleviate frontrunning, but would probably add a lot of complexity to the consensus layer and would still result in negative-sum latency arbitrage wars as in traditional HFT.

1. You can propose some sort of random ordering of transactions as @pmcgoohan appears to have done here and as others have tried to propose before.

As hard as it may be to get random ordering in a ‘fair’ way in which the seed cannot be manipulated by the miners/validations and so on, it doesn’t change the fact this will encourage traders to sometimes send as many orders as they can to execute first.

One may think that, because each order always has a 50% chance of being placed after any other, there is no money to be made with frontrunning or sandwitching attacks, but that is totally false. There are many clever ways to send many transactions and have the wrong ones fail. One can even deploy a smart contract that inspects a given user’s balance and the uniswap price to decide whether any order relayed though it is to proceed or not! So I don’t think random ordering should be involved in any proposed solution.

1. You can have MEV auctions as proposed by @vbuterin here

This approach has a very significant disadvantage in that, by allowing MEV to be extracted more efficiently, it will make the frontrunning costs paid by regular users of uniswap-like exchanges even worse than they already are.

Even so, *I’m strongly in favor of that proposal*. First because it changes consensus rules at lot less, second because at least resources are sent to validators instead of being destroyed as with transaction bloating or useless underground cables, and third but not less importantly, because the **frontrunning costs are temporary and can be solved completely in the application layer**

How is this so? The key is that, while blockchains are great for decentralized smart settlement, they are not necessarily good for time-critical trading. On-chain order matching is *not necessary* for decentralized custody and settlement, which is what makes DeFi great. *Disclaimer: I’m currently building a hybrid exchange with off-chain batch-auction order matching.*

I will not go into details of how this can be done now, but one can create a TradingBalance contract that is similar to a payment channel, but in which users can not only sign messages authorizing payments, but also messages authorizing specific swaps (e.g. I authorize you to exchange up to 1000 DAI into WETH at a maximum price of 3000$ as long as you settle this trade on-chain before block X). Smart contracts could do a similar authorization by a function call.

If the exchange is malicious, it can of course frontrun the order itself, but here the exchange has a reputation to keep. The exchange could give a reply back in milisseconds confirming the trade with a signed message. Again, the exchange would have the power to revert the trade until it is settled, but its reputation is on the line, and because it can extract trading fees from users who trust it, this reputation will be worth much more than the profits that reverting a few trades might bring.

So I think this explains how I believe application layer solutons can be designed to remove frontrunning costs while settling them on-chain later.

What I have not explained yet is how an exchange can prevent latency arbitrage from happening. I’ve actually been working for the last three years in a solution to this problem. I developed a design for a new matching mechanism based on batch auctions, but this is one *without uniform pricing*. We instead design it so it can have a truthful property for the liquidity takers (they don’t need to worry about their own price impact). We use a cyclical mechanism in which each step is inspired by [Ausubel (2004)](https://www.econ.umd.edu/sites/www.econ.umd.edu/files/pubs/efficient-ascending-auction-aer.pdf).

We have a demo working [here](https://tickspread.com), and we are testing it in a centralized exchange setting. It will look just like a regular orderbook (that is the idea), but one can place an order on the book and the order might be executed with price improvement later. For example, suppose there is an order selling for $100 initially at our exchange, the price rises in some other exchange and three bots send buy orders at $108, $109, $110 respecively at roughly the same time. Then the last bot will get to buy it and will pay $109 (like a second-price auction), and the selling order will get price improvement. Early documentation is [here](https://tickspread.com/auction.pdf).

Gnosis team [@mkoeppelmann](/u/mkoeppelmann), [@fleupold](/u/fleupold) and others, I know you are working on a different batch auction mechanism with CowSwap. I really think we could work together on a solution for this. Please let me know if you are willing to schedule a call. Others interested in potentially contributing to this project please contact me.

## Replies

**pmcgoohan** (2021-07-06):

What a truly fantastic and informative post. On a par with the work of [@Mister-Meeseeks](/u/mister-meeseeks).

It’s so full of ideas. I will take a few of the points in turn, most notably the ones I don’t entirely agree with, so please don’t think I disagree with the post in general which is very sound.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> These transaction reordering exploits are so hurtful right now that many are arguing that latency arbitrage is not a problem by itself…I disagree

Yes so do I, perhaps for slightly different reasons although yours are valid too. For me, latency arbitrage is not even possible in Ethereum because time order is perfectly corrupted by miner control. Miners never order by time, always by self interest.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> according to general relativity you can’t even talk meaningfully about ordering events that happen at different positions in space

I actually investigated this as part of my looking into send time ordering as an ideal.

You would have to travel on an airplane for over 260,000 years to get enough gravitational time dilation to drop one video frame’s worth of time compared to people on the ground. I’m pretty sure that even the Apollo moon landings used Newtonian physics not General Relativity in their calculations, so I think we can safely discount this as a problem!

As an aside, you can test a network for fair send time ordering by sending txs with different MEV values and checking their divergence from the known send time.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> this will encourage traders to sometimes send as many orders as they can to execute first.

Yes this is well known to me now and I have shelved the Random Alex protocol for the time being as a result.

Counter intuitively, if Uniswap (for eg) got rid of the slippage parameter, it would actually combat stat arb attacks in random ordering because failure would be too expensive for the attacker.

My documentation is lagging my ideas, please [see this talk](https://www.youtube.com/watch?v=zf2l3veT9EI&t=655s) for a description of my plain, encrypted and fair ordered versions of Alex.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> Even so, I’m strongly in favor of that proposal. First because it changes consensus rules at lot less

You had me until here! In actual fact, it’s not quite true to say I am against MEVA. I think collusion like MEVA is inevitable given the existing L1 protocol design, whether Flashbots or anyone else does it or not.

And this is why I disagree with your second statement. It is not an advantage not to have changed consensus rules, we must change them, specifically to bring block content into the consensus mechanism rather than allowing it to sit entirely within centralized miner control.

![](https://ethresear.ch/user_avatar/ethresear.ch/kelvin/48/6173_2.png) kelvin:

> So I think this explains how I believe application layer solutons can be designed to remove frontrunning costs while settling them on-chain later.

I can’t say I fully understand your proposal, but if it uses the existing consensus/SC mechanisms, it does not fix MEV because the MEV auction winner can censor transactions from ever entering the chain.

If you do this for one block, and enter your tx instead, you have frontrun them.

Censorship, while little discussed, is actually the killer MEV attack type. I cannot think of a single use case for Ethereum that it does not threaten.

Don’t get me wrong, I’m a fan of MEV fixes at all levels very likely including app level fixes like yours, but it also must include the base layer IMO.

---

**kelvin** (2021-07-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> You would have to travel on an airplane for over 260,000 years to get enough gravitational time dilation to drop one video frame’s worth of time compared to people on the ground. I’m pretty sure that even the Apollo moon landings used Newtonian physics not General Relativity in their calculations, so I think we can safely discount this as a problem!
>
>
> As an aside, you can test a network for fair send time ordering by sending txs with different MEV values and checking their divergence from the known send time.

I think you are right about general relativity, it really doesn’t matter. However, it is still not clear to me how could we possibly sort correctly (or even approximately) by sending time in a distributed application. If I send a transaction from Brazil and another person sends a transaction from Japan roughly at the same time, what process could be used to decide which transaction is to be included first? People in South America will see my transaction arrive first, while people in Asia will see the exact opposite. Who is to decide?

The best I can think of is having several trusted timestamping servers located all over the world, each of them running an atomic clock, and then have the blocks respect such timestamps, but I don’t see how we could have a decentralized way to assess the accuracy of these clocks.

What I think is the most important disagreement that we have, however, is on the nature of data corruption. You claim that transaction reordering is data corruption, but I think that depends on what the protocol is. If your application is receiving TCP packets out of order, that *is* data corruption. If, however, your UDP datagrams arrive out of order, this is *not* corruption, because UDP does not give you ordering guarantees. I think a blockchain like Ethereum does not and probably cannot give you any reliable ordering guarantees, and therefore that applications building on Ethereum *should not rely on transaction ordering at all*.

Of course, applications *are* relying on that right now, particularly DEXes, and that is what in my opinion is causing this much frustration. We see an alternative in which trades do not *happen* on chain, but rather are only *settled* on it. In this model, waiting even a few extra blocks for the settlement to happen matters very little, because the participants already received an off-chain trade confirmation, meaning that as they wait for settlement the participants *already know* both the trade amount and trade price. Moreover, it is possible to make sure that other transactions being included first will not cause the settlement transaction to fail. This way, if someone censors their transaction for a few blocks or reorders the block in which they are included, the trade price and amount *do not* change, and so there is little incentive for doing so.

I understand there might be some resistance to the idea of having to trust a counterparty between trade execution and settlement, but I think that is the natural order of things. When Hanyecz bought the bitcoin pizza, the trade was *executed* as soon as both agreed to it. The transaction being included on the block (as well as the pizza arriving at his home) was only the settlement part. Until both parts of the settlement were made, they had to trust each other.

One nice thing of smart contracts is that we can enforce settlement rules, so that if one is buying GNO with ETH, we can settle both the GNO and ETH transfers atomically, greatly reducing how much trust is needed. Maybe in the future we can use advanced techniques such as time-lock encryption (that can simultaneously be verified quickly) to allow fully trustless transactions with no frontrunning, but I don’t think we are quite there yet.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Counter intuitively, if Uniswap (for eg) got rid of the slippage parameter, it would actually combat stat arb attacks in random ordering because failure would be too expensive for the attacker.

That is not true at all. The slippage parameter is just the Uniswap contract enforcing a condition in a simple way for users, but you could create your own smart contract to enforce this condition for you if you wanted. The uniswap pool price and liquidity variables are public, so another contract can just inspect them, calculate what the average price for the desired trade would be, and then decide to call Uniswap or not depending on that. Because regular users would most likely not deploy such contracts for them, they would get screwed with infinite slippage instead.

Even if Uniswap tried to prevent that by making these variables private this would also not work because the smart contract would still be able to make very small trades and look at the execution prices to reverse engineer the variables based on that.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> I can’t say I fully understand your proposal, but if it uses the existing consensus/SC mechanisms, it does not fix MEV because the MEV auction winner can censor transactions from ever entering the chain.
>
>
> If you do this for one block, and enter your tx instead, you have frontrun them.
>
>
> Censorship, while little discussed, is actually the killer MEV attack type. I cannot think of a single use case for Ethereum that it does not threaten.

Censorship resistance *is* an important property of Ethereum, but I think we need to interpret that narrowly. It does not mean that you should expect your transaction to always be included in the next block if you pay a significant tip. Rather, what it means is that, if you pay a reasonable fee, you should expect your transaction to be included eventually, maybe within 10 or 20 blocks. Most often you will indeed get it in the next block, just as UDP packets often arrive with the right order, but you shouldn’t rely on that.

I think I have not managed to explain our proposal correctly. We’ll be executing trades off-chain and then settling the trades on-chain later. Several minutes later may be totally fine, so that is dozens of blocks. A settlement transaction being censored for a few blocks won’t make much difference for us.

An user willing to trade at us will have to deposit his assets at a channel-like contract first. The transaction settling the trade will be using the assets that are ‘frozen’ in this contract. This way we don’t have to worry about the user withdrawing his assets and causing the settlement transaction to fail. Of course he’ll be able to withdraw his assets unilaterally, but that will take some time (like in a channel) to give us opportunity to settle all pending trades first.

So please let me know whether my explanation makes more sense now!

