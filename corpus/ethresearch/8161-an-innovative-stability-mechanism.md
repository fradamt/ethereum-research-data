---
source: ethresearch
topic_id: 8161
title: An innovative stability mechanism
author: cangurel90
date: "2020-10-25"
category: Economics
tags: [stateless]
url: https://ethresear.ch/t/an-innovative-stability-mechanism/8161
views: 2910
likes: 3
posts_count: 8
---

# An innovative stability mechanism

Almost all algorithmic stablecoins are good in mitigating periods of high demand but fail to offer sustainable stability mechanism during periods of low demand

**The core idea is to shift the demand in time in order to achieve a low volatile crypto native unit of account**. That is; temporarly disable selling if price is low and temporarly disable buying if price is high.

Example Implementation:

Say PP coin (aka purchasing power coin) targets 1 DAI as a price target

Say PP is mainly bought from or sold to PP-DAI pool (highest liquidity market)

We define the 2 types of txns to contract

Buy txn = Send DAI to pool Recieve PP

Sell txn = Send PP to pool Recieve DAI

Target Realized Cap (TRC) =  Σ [Target price of PP in units of DAI (= 1) x PP amount in realized buy/sell txn over z blocks ]

Actual Realized Cap (ARC) = Σ [Actual price of PP in units of DAI at the time of txn x PP amount in realized buy/sell txn over z blocks  ]

if

TRC > ARC

then

//Slow down sell txns

Disable sell txns up to certain block height (determined by the difference between TRC and ARC. If ARC = TRC/10 then sell txns become temporarily disabled for 10*y blocks where y is coefficient of slowdown )

else if

TRC < ARC

//Slow down buy txns

Disable sell txns up to certain block height

Obviously this is a very simplistic high level view. What are your thoughts? How can it be improved…

## Replies

**vbuterin** (2020-10-27):

What do you mean by “disabling sell txs”? There’s an unlimited number of ways to sell a token; you can sell it on uniswap, or on loopring, or on some centralized exchange… it’s impossible to prevent all of them.

And also there’s the philosophical question: if a token that you have becomes unsellable, doesn’t that *really* mean that its value has dropped to zero, thereby violating the definition of a stablecoin?

---

**MaverickChow** (2020-10-28):

Personally, I believe the main reason why no third-party stablecoin can ever maintain stability indefinitely, regardless of market demand or how anyone try to stabilize it technically / algorithmically, is due to **counterparty risk**. Technical operation is not the heart of the problem. If one has thought out something that is wrong, and then try to make up for it with technically competent solution, hoping to right what is fundamentally wrong and make sure everything will be fine once and for all, one can only expect disappointment in the end.

Current range of stablecoins aren’t really technically stablecoins. They are stablecoins by merit of hype and misinformation. Such coins behave far more like lending / loan coin than stablecoin, and I wonder why almost nobody ever notice this still.

What is stablecoin? It is a coin that maintain fiat value at par regardless of price volatility of the cryptocurrencies pegged to it. If so, then this means at market top, stablecoin providers will be the bag holder of cryptocurrencies, while at market bottom they will be the bag holder of stablecoins. Given enough time and volatility, all the stablecoin providers will go broke trying to maintain the value. And this is why the stablecoins that we have today are not really stablecoins. Rather, they are lending / loan coins, i.e. if you want to hold them you need to pay interest. Do you need to pay interest for holding USD or your local government currency in your wallet or bank account (not talking about NIRP)? So why is it not the same with stablecoins?

So here are my points:

1. If stablecoins behave exactly like stablecoins, then the entity that provides price stability is continuously taking counterparty risk that will eventually go bust given enough time and volatility. Such stablecoin is not sustainable.
2. If stablecoins behave like lending / loan coins whereby the holders need to pay interest for holding them, then you can never be able to maintain stability indefinitely with algorithm alone, at least not gracefully. Such stablecoin is not really a stablecoin. And to talk about technical solution for it is nothing but a waste of time. If there is no free lunch to stablecoin buyers / holders, then there is no free lunch to stablecoin providers just the same, except in a manipulated condition.

I think stablecoins are best provided and maintained by central banks because they are in the best position to absorb counterparty risk as they can print / manipulate money indefinitely and without limit. Thus, I believe CBDC is a very good starting point leading to a proper form of stablecoin in the future. I don’t think current range of third-party stablecoins, aka lending / loan coins, will survive in the long term with cryptocurrency adoption reaching maturity.

---

**EazyC** (2020-10-28):

I’m not sure if I understand you correctly since it seems like even Vitalik is asking for some clarification, but if by “disable sell tx’s” you actually mean stopping people from transferring the ERC20 through the token’s smart contract, that doesn’t make any sense. You can’t just stop market forces by turning off certain coding functions. If the stablecoin is sufficiently desirable and large, there would be many ways to wrap it out of the original contract to new ones that allow free transfers of the coin. There is no way to stop any kind of tx of a coin through code. It would just get wrapped if there is sufficient demand to buy or sell it somehow.

That’s like when governments try to price fix their currencies by making it illegal to sell it at any price below the government mandated price. It just finds black market avenues and the free market information leaks out.

I apologize if this isn’t what you meant by “disabling/slowing down” transactions. That’s just what it sounded like to me.

If you are interested in stablecoins though, I’m personally working on one that is a hybrid algorithmic stablecoin that you might like. It’s the first stablecoin where part of the supply is algorithmic and part of it is collateralized and the ratio between collateralized and algorithmic is constantly being adjusted to keep the price of the coin stable at $1.

---

**EazyC** (2020-10-28):

As Vitalik says, there’s 2 ways to look at this:

1.) If you literally cannot sell something, then by definition it is not worth $1.

2.) What I was saying in my post below is that if something is actually valuable, like a stablecoin, then you prevent its selling/transfer, it can trivially be wrapped in contracts you can’t control/have no ability to stop. There is no such thing as an ability to stop selling by code/law if the demand to interact with the value is actually there. You’re better off designing proper game theory than trying to ban selling/controlling movement.

---

**cangurel90** (2020-10-28):

1st point -> You are right…  My thought process was built on most liquid market having the most influence on price. But i guess when you control the flow in that market, alternative markets will quickly emerge with their own set of rules. Making it impossible to ensure flexible control of flow.

2n point -> in a system where all txns are temporarily disabled based on price, temporary can become infinity, dropping price to zero. No different than increasing txn fees to discourage velocity. The catch here was separation of buy and sell txns and putting restriction to one or the other. So that when u can’t sell the coin, u would still be able buy up more to eventually create a window to fully cash out.

Background of my thought process depends on impossible trinity theory of international finance according to which any currency issuer can control 2 out of these 3;

1.exchange rate

2.supply

3.flow of capital

The idea is to control 1 and 3 and let market decide the supply.

In theory, this can solve “the what’s in it for me?” problem that any single coin stablecoin design face. It allows an incentive mechanism to be created where early adopters can increase their purchasing power through supply inflation

Thanks to everyone who shared their comments. They are all valuable and unfortunately i’m convinced that this mechanism won’t work

I think a decentralized = oraceless, non collateralized, crypto native stablecoin ( “cryptocurrency with mechanisms to mitigate fluctuations in its purchasing power.” ) is whats needed the most for next revolution. We just have to try better.

[@EazyC](/u/eazyc) I believe we chatted before about Frax (and Meter) on telegram. Good luck on your project

---

**cangurel90** (2021-01-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/eazyc/48/5266_2.png) EazyC:

> What I was saying in my post below is that if something is actually valuable, like a stablecoin, then you prevent its selling/transfer, it can trivially be wrapped in contracts you can’t control/have no ability to stop. There is no such thing as an ability to stop selling by code/law if the demand to interact with the value is actually there. You’re better off designing proper game theory than trying to ban selling/controlling movement.

Would you say the same thing for FEI protocol whose whitepaper just got published



      [fei.money](https://fei.money/static/media/whitepaper.7d5e2986.pdf)



    https://fei.money/static/media/whitepaper.7d5e2986.pdf

###

---

**cangurel90** (2021-04-07):

yup you were so right [@EazyC](/u/eazyc)

restriction on free flow of capital did not work

