---
source: ethresearch
topic_id: 10442
title: Fixing gas prices and MEV
author: PatrickDehkordi
date: "2021-08-29"
category: Economics
tags: []
url: https://ethresear.ch/t/fixing-gas-prices-and-mev/10442
views: 2713
likes: 5
posts_count: 5
---

# Fixing gas prices and MEV

Can someone explain why fixing gas prices , and by that I mean somehow hard-coding a certain value or range to be accepted as valid, a bad idea? I see a chain called Avalanche does this. But I just get a sense that this solution causes more issues than it solves. If not why doesn’t ethereum do this?

## Replies

**MicahZoltu** (2021-08-29):

It * is unknown how much demand for blockspace there will be in the future.

- There is finite blockspace available.
- Someone has to decide which transactions get included, and which get excluded.
- If gas price (or equivalent) isn’t flexible, then someone will figure out how to pay for priority via some other less transparent and open means.
- If you have no mechanism for price priority at all (and prevent backchannel payments somehow), then you will just end up with an ever-growing backlog of transactions, effectively sacrificing all timliness.

---

**dild26** (2022-01-08):

Hi MicahZoltu,

Pl. explain why on Earth a simple Txn of  $1 costs 10x to 50x in ETH as GAS FEE !

ETH Core Technology is superior but Mathematic is Pathetic here…

Millions of users who start with ETH had to loose 99% of all their funds in the name in Gas fee as it is seen as cheating innocent newbies who never even imagined this.

It is as good as for a litre of gas you had to pay 1000s of $$$.

Still all Developers had to stick to DAPPs & other projects just to Recover their Lost funds to be recovered from new members who follow simply as Sheeps into ETH !

Thank You…

---

**wjmelements** (2022-04-15):

Markets solve the economic calculation (pricing & allocation) problem, which is one of the main reasons that attempts at socialism and communism have failed. When you fix the price, it will be either too high or too low. If it is too low, there will be a shortage of blockspace with no way to secure inclusion for the most-important transactions. If it is too high, the blocks will be wasted (surplus) because consumers are priced out of usage.

In the AVAX case, the price is (currently) too high, and the blocks are wasted. Some day it might be too low. Currently, if they did not institute their price floor their blockchain would be more spam-filled than it is. This is because they have artificially expanded their capacity far beyond their usage. The consequences of this are that it is prohibitively expensive to operate a node, and the costs will continue to grow over time.

See also:



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Economic_calculation_problem)





###

The economic calculation problem (ECP) is a criticism of using central economic planning (rather than market-based mechanisms) for the allocation of the factors of production. It was first proposed by Ludwig von Mises in his 1920 article "Economic Calculation in the Socialist Commonwealth" and later expanded upon by Friedrich Hayek.
 In his first article, Mises described the nature of the price system under capitalism and described how individual subjective values (while criticizing other theorie...












      [en.wikipedia.org](https://en.wikipedia.org/wiki/Price_floor#Effect_on_the_market)





###

A price floor set above the market equilibrium price has several side-effects. Consumers find they must now pay a higher price for the same product. As a result, they reduce their purchases, switch to substitutes (e.g., from butter to margarine) or drop out of the market entirely. Meanwhile, suppliers find they are guaranteed a new, higher price than they were charging before, but with fewer willing buyers.
 Taken together, these effects  mean there is now an excess supply (known as a "surplus") ...












      [en.wikipedia.org](https://en.wikipedia.org/wiki/Price_ceiling)





###

 A price ceiling is a government- or group-imposed price control, or limit, on how high a price is charged for a product, commodity, or service. Governments impose price ceilings to protect consumers from conditions that could make commodities prohibitively expensive. Economists generally agree that consumer price controls do not accomplish what they intend to in market economies, and many economists instead recommend such controls should be avoided.
 While price ceilings are often imposed by g...

---

**gavinyue** (2022-04-21):

I also think the free market is the best solution in long term. But we also learn a little bit socialism could stabilize the society, like our almost broken social security program.

So why not reserve a percentage of block space, like 5-15% to have zero or minimum gas fee?  I do not have a calculation here, but I feel it is worth trying.

