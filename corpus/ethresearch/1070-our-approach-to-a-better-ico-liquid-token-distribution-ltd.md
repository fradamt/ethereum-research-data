---
source: ethresearch
topic_id: 1070
title: Our approach to a better ICO - Liquid Token Distribution (LTD)
author: AnthonyAkentiev
date: "2018-02-13"
category: Better ICOs
tags: []
url: https://ethresear.ch/t/our-approach-to-a-better-ico-liquid-token-distribution-ltd/1070
views: 3077
likes: 6
posts_count: 8
---

# Our approach to a better ICO - Liquid Token Distribution (LTD)

Hi guys! We would like to get more feedback about our “No-ICO” approach described here in details:

[Thetta’s Liquid Token Distribution (LTD) approach](https://medium.com/thetta/thettas-liquid-token-generation-event-ltge-988e29425d34)

In short:

1. We don’t do any ICO
2. We emit tokens starting from day one of the official launch
3. All payments/bonuses will be done in tokens only!
4. We won’t need ETH or BTC to fund the development
5. Token buyers or team members can sell tokens starting from the day one.

How we do that?

1. We have the first smart contract (SC1) that emits tokens in small chunks with milestones and voting. All team tokens are vested. This helps to avoid large sums of tokens being emitted for team members/buyers. Only a small number of tokens are emitted. Token are emitted continuously. All rules are in the smart contracts.
2. Second smart contract (SC2) is a Bancor Smart Token (market maker) contract. We put X ETHs there and N tokens. There is initial price generated automatically by the Smart Token.
3. If developers or token holders need ETH — they can go to SC2 and sell their tokens at the current price effectively lowering the price of Thetta tokens.
4. If people want to buy some Thetta tokens — they can go to SC2 and buy some tokens at the current price effectively increasing the price of Thetta tokens.

We are going to use this approach in our project and to test its Pros/Cons.

Questions:

1. What do you think about the “liquidity” in this approach? if we don’t put enough ETH funds into the Bancor smart tokens -> price may become very volatile.
2. What do you think about the continuous token emission? Ethereum has the same approach as ETHs are generated with each block.
3. Do you think this approach can provide a better “token buyer” security?

Thx!

## Replies

**vbuterin** (2018-02-13):

As I mentioned in another post, this is exactly the model that MakerDAO used, and I strongly support it.

---

**AnthonyAkentiev** (2018-02-13):

Thx for quick answer.

Yes, Maker is very similar, i agree.

But the difference between [Thetta.io](https://web.thetta.io) and MakerDAO is:

1. We are going to use Bancor as a market-maker.
2. MakerDAO uses MKR/DAI token pair and the token mechanics and economy are very different. Our approach is more about “almost any crypto project can use instead of ICO”, while the Maker’s is not so generic and more highly-specialised.
3. Our approach can be described in 5 sentences, so it is very easy to understand. I wish more projects took this approach.

What we described in the blog post is only a single side of the equation.

The other side is how the tokens are emitted. If we emit billions of tokens and then will be able to “sell” that to market maker -> token price will eventually become ~0.

So in [Thetta.io](https://web.thetta.io) tokens will be emitted continuously only in a small chunks to the team members, for doing tasks/bounties. This side of the equation (say, DAO) is more interesting i think.

But still, Maker took a different approach:

“You could not find any ICO information because there has never been one. MKR has been slowly moved on to the market first through private sales, then bitshares markets before mkr.market opened up. We really need people to read the whitepaper and understand Maker, not just buy some coins. So there is plenty of scope to join as we still do daily sales.”

“There wasn’t an ICO for MKR, it was sold off over time at a steady pace, initially through our forum and in private deals, and later through sell orders on openledger and now maker market.

Polychain was able to get a good price because they bring some extremely important resources to the table, such as financial industry contacts and marketing and business development resources. The difference in the price they got and the market price represents the additional tangible value they will give us.”

Still, my intent is not to claim “i got a patent to this approach”))

I wish more crypto project move to what we call “Liquid Token Generation Event (LTGE)” maybe with some changes and additions. You can rename it anyway you like. So we are going to test this approach. Maybe it will evolve into something else, we’ll see. As you can see, we are about the Research then “get lambos and stop development”.

Thank you very much.

---

**vbuterin** (2018-02-13):

Though perhaps you don’t want to subsidize liquidity in the early stages. If the token is illiquid, then people who are paid in the token will be more likely to hodl it, increasing incentive alignment.

---

**AnthonyAkentiev** (2018-02-13):

Thx!

Also we are thinking about 3-6-12 month vesting schedules for team/community members.

p.s. Is there any possibility to get some funding from the Ethereum Foundation for research?

I don’t think we need more than 100 ETHs for the first 6 month of development and to put into into the market maker to provide initial ETH supply. We can issue 12-18 month vested tokens to the Ethereum Foundation in return.

---

**kladkogex** (2018-02-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/anthonyakentiev/48/362_2.png) AnthonyAkentiev:

> We are going to use Bancor as a market-maker.

Bancor is really a suboptimal way to do a market maker for reasons [explained here](http://hackingdistributed.com/2017/06/19/bancor-is-flawed/)

We are opensourcing a market maker which is infinitely better than Bancor, it does not bleed money like Bancor  and will save you lots of ETH. And it is completely free !!

The market maker has been created by one of our super smart student interns in Ukraine, here is  documentation (in Russian at the moment, we are working on English version))

[GexBot_documentation.pdf](https://ethresear.ch/uploads/default/original/1X/33b8981e5925793c5fdd04c3adce903c8d52c821.pdf) (124.1 KB)

Here is an English description:

The main purpose of GEXBot is to achieve liquidity of GEX vs. ETH.

Typically, when an asset is traded on an asset exchange, buyers post bids

(buy requests) and sellers post asks (sell offers).

If the asset is thinly traded, bids and asks become scarce, orders take long

time to complete and the price fluctuates strongly. Intuitively it is explained

by visualizing a picture, where buyers and sellers come to the market place

infrequently. When a seller comes to the marketplace there is no buyer, and

when the buyer comes to the marketplace, there is no seller.

To increase liquidity, we introduce GEXBot, an automated market  maker that

is always available for transactions.

Let us first describe a very simple algorithm, where GEX sellers and ETH

sellers place their orders with GEXBot.

In particular,

(1) Intra-day, GEX sellers communicate orders to GEXBot, depositing

GEX coins to sell with GEXBot

(2) Intray-day, ETH sellers communicate orders to GEXBot, depositing

ETH coins to sell with GEXBot

(3) All order amounts are public

(4) At the end of the day, at time 0:00, GEXBot calculates GEX vs ETH

exchange rate by dividing the total GEX deposits by the total ETH

deposits

(5) GEXBot then distributes deposits according to the exchange rate,

transferring GEX to ETH sellers and ETH to GEX sellers

The algorithm described above can actually work quite well. The exchange

rate may fluctuate a bit against the exchange rate at external asset exchanges,

but since the order book is public, as time 0:00 approaches, arbitrage traders

will seek profit by issuing pairs of orders against GEXBot and against the

external exchange. As a result of this profit-seeking, the rate at the close time

0:00 will be reasonably in sync with external exchanges.

The main problem with the algorithm described above is that the participants have to wait until 0:00 to get the assets they want. Someone who needs

GEX services and has ETH in her waller will need to wait hours to get GEX.

This is clearly not tolerable.

The idea is to augment the algorithm above, so when the seller places an

order with GEXBot, GEXBot temporarily lends to the seller the asset that

the seller needs, assuming that the loan is repaid at the close time 0:00.

The question is then, how much can GEXBot lend to the seller without

assuming too much risk.

Let us consider an example, where the seller needs to sell 100 ETH for

GEX, and the exchange rate at the previous day close time is 2ET H = 1GEX

(1) The seller deposits 100 ETH with GEXBot.

(2) GEXBot immediately lends to the seller 50 GEX, hoping that the ex-

change rate at close will be the same, as it was yesterday at 0:00.

(3) Imagine the exchange rate drops, so at 0:00, 100 ETH = 47 GEX.

GEXBot will then realise a loss of 3 GEX, that will have to come out

of its GEX reserve.

As we see in the example above, if GEXBot lends to the seller at the

exchange rate of the previous day, GEXBot can incur a loss if the rate drops.

To compensate for these losses, let us require the seller to deposit a 20%

safety margin, since we know that most day-to-day price fluctuations are less

than 20%.

Then the modified algorithm works as follows:

(1) The seller deposits 120 ETH with GEXBot. Out of this, 100 GEX is

the principle, and 20 GEX is the safety margin

(2) GEXBot immediately lends to the seller 50 GEX, applying the previous

day’s exchange rate to the principle

(3) imagine, the rate drops, so at 0:00 one has, 100 ETH = 47 GEX

(4) GEXBot sells ETH for GEX. For 120 ETH it gets 56 ETH

(5) GEXBot then uses 50 GEX to cover the loan. The remaining 6 GEX

is transferred to the seller

As we see from the example above, the seller deposited 120 ETH, got 50

GEX immediately, and then 6 GEX as an adjustment at time 0:00.

The algorithm above is good for the seller, since the seller gets most of

GEX immediately, and ultimately gets the fair value in GEX.

GEXBot can incur a loss in the infrequent case where the rate drops more

than 20% day to day.

Lets consider an example the where the rate drops so much that,

GEXBot only gets 49 GEX at time 0:00. It is not enough to cover the previous

loan of 50 GEX, so the seller owes to GEXBot 1 GEX.

GEXBot will note this 1 GEX as an outstanding loan, and charge this 1

GEX from the seller the next time the seller comes to GEXBot to exchange

assets.

The seller may decide to never come back to GEXBot. In this case,

GEXBot loses 1 GEX, and the seller loses its reputation in the network and

its ability to easily exchange GEX for ETH.

Since the purpose of GEXBot is to provide GEX liquidity to users and

providers for service payments and not for market speculation, GEXBot will

impose exchange limits, that will depend on the reputation of the seller, as

well as on the amount of the service provided or used by the seller in the past.

The exchange limits will limit the losses that GEXBot can incur.

Yet, there will be cases where sellers will never come back and GEXBot will lose

reserves. To compensate for this average loss, GEXBot will charge transaction

fees on each transaction. The fees will be proportional of to the size of the

order multiplied by the fee rate. The fee rate starts with zero and goes up as

GEXBot starts depleting its reserves.

---

**rumkin** (2018-02-13):

This is pretty good idea. I’ve thinking about freelance for tokens. But how to manage milestones from the contract. Who and how will accept tasks? Is this tokens holder or independent witness?

---

**AnthonyAkentiev** (2018-02-13):

Thx! We will post info about the process soon.

Please subscribe to our Slack.

