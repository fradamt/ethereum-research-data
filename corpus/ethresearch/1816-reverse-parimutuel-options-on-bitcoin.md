---
source: ethresearch
topic_id: 1816
title: Reverse Parimutuel Options on Bitcoin
author: fima
date: "2018-04-24"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/reverse-parimutuel-options-on-bitcoin/1816
views: 1704
likes: 0
posts_count: 1
---

# Reverse Parimutuel Options on Bitcoin

In the previous article, we considered problems faced by centralized exchanges when creating a derivatives market for cryptocurrencies. We also proposed a solution that we developed, which we called reverse parimutuel options. Now let’s look at the practical side of trading reverse patimutuel options on Bitcoin.

The ability to make money on fluctuations in the price of an asset is one of the inalienable components of a financial market. It can done in several ways, such as buying the asset itself, buying the asset using leverage, buying futures or options. We will consider a case of using reverse parimutuel options on Bitcoin and compare them with buying and owning actual Bitcoin.

Assuming the reader is familiar with standard option calls and puts and read the previous article about reverse parimutuel. At the time of this writing, Bitcoin (BTC) was worth about $8,700. All calculations will be made based on this value.

**Scenario 1: Rising Market**

So, in order to purchase one BTC, we will need $8,700. If the value grows by $3,000, we will earn $3,000, if it falls by the same amount, then we will lose $3,000. What advantage does reverse parimutuel give us in this scenario?

First, let’s calculate the value of a reverse parimutuel call with a strike price of $8,500 and an upper limit for the option at $11,500 and 3 months to expiration. The premium will consist of the total cost of all base states (ranges) from 8,500 to 11,500 inclusive.

[![1*LHz2ib05Nxp3iKVaDpqNgA](https://ethresear.ch/uploads/default/optimized/2X/0/064db549f4cfc5cb9303e19c02fb5ebdfae53457_2_690x299.png)1*LHz2ib05Nxp3iKVaDpqNgA937×407 56.3 KB](https://ethresear.ch/uploads/default/064db549f4cfc5cb9303e19c02fb5ebdfae53457)

*Reverse Parimutuel Call 8500 vs BTC*

The total cost would be $315 or 3.7% of the price of BTC. In other words, in order to earn on the growth of Bitcoin, we would only need to pay $315 and if Bitcoin grows by $3,000, we will earn $2,685 ($3,000 — $315 is the profit minus the premium paid earlier). However, in the event of a drop in price of Bitcoin, the situation becomes much more profitable when compared to simply buying Bitcoin outright. If the value drops by $3,000, we would only lose $315, which is the original cost of options (called “predetermined risk”). The second-most important advantage of using options is for the leverage effect. In order to earn on the rising price we only need to invest $315 instead of $8,500, in other words for $8,500 we can buy 26 options and earn 26 times more than buying 1 Bitcoin.

**Scenario 2: Falling Market**

As we outlined in the previous article, it is extremely difficult to create short sale on the crypto-currency market, and all attempts to implement it were taking a step back, back to the centralized exchanges. Standard options for cryptocurrencies, due to their unique qualities, carry huge premiums even though the buyer has no guarantee that the seller will pay. Therefore, in the event of a fall in the market, if you have a cryptocurrency in your portfolio, you have nothing left to do but to wait it out or sell everything at the market. Who knows when a bear market will end and the growth will begin again?

Let’s consider a reverse parimutuel put with a strike price of $9,000, a lower limit of $6,000, expiring in 3 months and calculate its premium.

[![1*YlamV0BW9XJIvmfKv1SQMQ](https://ethresear.ch/uploads/default/optimized/2X/a/a254043f1d5b812bdd306ab033fbeff395251126_2_690x303.png)1*YlamV0BW9XJIvmfKv1SQMQ800×352 86.1 KB](https://ethresear.ch/uploads/default/a254043f1d5b812bdd306ab033fbeff395251126)

*Reverse Parimutuel Put 9000 vs BTC*

The total cost of the option premium will be $315 or 3.7% of the BTC price (exactly the same as for the call. This is because we are using the price of Bitcoin at 8,700 and the premiums for call and put options should be the same in order to exclude the possibility of arbitrage). So, if we own Bitcoin and the market falls, our portfolio will lose proportionally to the market. But, if we buy a put option for $315 and the market drops by $3,000, then we will profit by the fall of $2,685 ($3,000 — $315 or profit minus the premium paid earlier). What that means is that derivatives can function in the crypto-currency market, and this is an excellent tool for it whether trading long or short. If you add the effect of leverage, then in a falling market you can earn multiple times more than selling Bitcoin futures (due to the huge collateral now required by exchanges).

**Scenario 3: Hedging Risk for Miners and ICO**

This scenario is more suitable for companies or private investors who are engaged in crypto-currency mining, as well as for companies that conduct ICOs.

For mining, a fall in the exchange rate directly affects profitability, and for companies conducting an ICO, the exchange rate affects financial planning.

In both cases, buying a put option is ideal. To insure their portfolios, miners will need to buy as many put options as they plan to produce in 3 month period. As a result, this insurance will cost them 3.7%. So, if at the expiration date the exchange rate is lower, the company can compensate for the loss with the profit from the exercise of the put options (minus the premium paid). Companies conducting ICOs can choose options with a shorter term, and lock in the rate for the date the ICO begins.

**Conclusion**

Options are universal financial instruments that can be used in many scenarios and have numerous advantages, such as:

1. Provide leverage, in our example 26 to 1
2. Limit risk in the event of a market movement in the opposite direction
3. Allow an investor to profit in a falling market
4. Provide the ability to insure a portfolio against depreciation

[We want to invite you to participate](https://apofinance.io) in the creation of a new market based on cryptocurrency derivatives. This is another step towards changing the global financial system.
