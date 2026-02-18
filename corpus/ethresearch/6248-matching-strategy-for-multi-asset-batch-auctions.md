---
source: ethresearch
topic_id: 6248
title: Matching strategy for multi-asset batch auctions
author: mkoeppelmann
date: "2019-10-04"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/matching-strategy-for-multi-asset-batch-auctions/6248
views: 4580
likes: 7
posts_count: 7
---

# Matching strategy for multi-asset batch auctions

In our view batch auctions are in interesting direction for DEX research. In contrast to “normal” orderbook (continues double auction) dexs where trades are executed continuously, batch auctions collect orders into a batch (discrete time) and then calculate a “single clearing price” and which all orders are executed.

If you do not want to rely on a “operator”/“trade coordinator” or any other central entity that creates an order of transactions/orders the smalest unit of time is “one block”. This is - you can say this transaction came first if it is part of an earlier block, but if 2 transactions are part of the same block there is no way to say which came first.

Exchanges like OasisDEX or Uniswap however nevertheless treat orders in the same block differently depending on the order in which the miner includes them into a block. Ultimately this is completely arbitrary and can be exploited by miners and adds to what [@phil](/u/phil) calls “miner extractable

value” (MEV)— [here](https://arxiv.org/pdf/1904.05234.pdf).

Our simple claim is:

***The same 2 orders in the same block should get the same price.***

In a batch auction a batch could be potentially as small as a block. This would reduce the MEV but miners would still have significant influence by potentially censoring specific orders. Thus it might make sense to have a batch running over multiple blocks. In any case - we need to define a strategy of how to “clear a batch” == “find the single clearing price and settle the orders accordingly”.

[A paper](https://faculty.chicagobooth.edu/eric.budish/research/HFT-FrequentBatchAuctions-ImplementationDetails.pdf) that argues for batch auctions for different reasons describes a clearing strategy as follows:

[![06](https://ethresear.ch/uploads/default/original/2X/c/c9105b66cd9e77a83d66729044f22e5c6c059340.png)06278×222 8.88 KB](https://ethresear.ch/uploads/default/c9105b66cd9e77a83d66729044f22e5c6c059340)

Simplified speaking - either there is no overlap in the order book - than no matches, or if there is overlap, than where supply and demand cross.

More exact version here:

*Case 2: Supply and demand cross. Typically, if supply and demand cross they do so horizontally. Let p*

denote the unique price and let q denote the maximum quantity. In this case, all orders to buy with a price greater than p* and all orders to sell with a price less than p* transact their full quantity at p. For orders with a price of exactly p* it will be possible to fill one side of the market in full whereas the other side will have to be rationed. We suggest the following rationing rule: pro-rata with time priority across batch intervals but not within batch intervals. That is, orders from earlier batch intervals are filled first, and in the single batch interval in which it is necessary to ration, this rationing is pro-rata treating all orders submitted within that interval equally. This policy encourages the provision of long-standing limit orders, as in the CLOB, but without inducing a race to be first within a batch interval. There is also a knife-edge case in which supply and demand intersect vertically instead of horizontally. In this case, quantity is uniquely pinned down, and the price is set to the midpoint of the interval. There is no need for rationing in this case.*

Now this assumes a case of a single trading pair. There are plenty of reasons to allow many assets/tokens be traded all in one system. A primary reason is that you can allow so called “ring trades”. If trader 1 wants to trade A->B, 2 B-C and 3 C-A those 3 trades could match together.

To illustrate this: those are the trading pairs on Kraken and since many tokens are traded in several currencies/tokens there is plenty of opportunity for “ring trades”.

[![08](https://ethresear.ch/uploads/default/optimized/2X/f/ff50c937f6718c3f643755c3bf902029356b27c9_2_560x500.jpeg)081148×1024 258 KB](https://ethresear.ch/uploads/default/ff50c937f6718c3f643755c3bf902029356b27c9)

However - in this multi asset world the question how to settle the trades becomes much less obvious.

Since we want an arbitrage free result prices of A<->B and B<->C should also define the prices of A<->C.

A very simple implementation to ensure this is to store just one price number for very token and the prices of every pair are calculated by the ratio of the price number of 2 tokens. Obviously that means that if you optimizing for the A<->B pair and you are changing the price of A you are influencing all trading pairs that contain A.

A valid solution in addition to the price consistency need to also full-fill “value preservation” - that is, for each token the total number sold and bought need to equal out.

Here is a visualization of optimizing prices for 3 tokens.

[![25](https://ethresear.ch/uploads/default/optimized/2X/4/459aecc4b2df7b6dad75b99e5604ac961f01afed_2_690x313.png)251102×501 122 KB](https://ethresear.ch/uploads/default/459aecc4b2df7b6dad75b99e5604ac961f01afed)

When it comes to this optimization problem we currently have the assumption that this is a NP-hard problem and thus the optimal solution can not practically be calculated deterministically (and certainly not on the EVM). We want to deal with this by creating a open competition. After a batch closes anyone can submit a solution within a fix time period and the best on is executed. In this case the 2 operations that need to be done on-chain are simply: **make sure the solution is valid; check the value of the objective function.**

The problem now is: what is a good objective function.

1. Overall trading volume (all trades would need to be converted based on current prices to a reference token)
2. Overall trader utility (simply speaking - (how much of an asset did a trader get - how much did they wanted to get at least)

We can shorty summarize the constraints of a solution:

1. Pick a price for each token
2. Orders that are on or below the clearing price CAN be executed
3. Define a volume (from 0-100%) for each order that CAN be excuted
4. Make sure that for each token “total amount sold == total amount bought”

Let’s create a simple example and see how those two objective functions perform.

***“Volume creates unnecessary long ring trades”***

**Example volume optimization**:

Consider we have 3 stable coins that should all be worth $1. (S1, S2, S3) We have 3 market makers that each have 1000 of one of the stable coins and they are willing to trade them for every other stable coin if they make a spread of at least 1% on the trade. If those 9 trades where the only open orders in the system no trade would be possible.

Now a user comes that simply wants to convert 10 S1 to S2. They post a trade of e.g. 10 S1 for at least 9.98 S2.

A system that will optimize for volume will now set prices of S1 to 1.00 of S2 to 0.98 and of S3 to 0.99. Now it can execute a full ring. The user Trades S1 to S2, market maker 2 trades S2 to S3 and MM3 trades 3 to 1. Bother market makers make 1% on the trade and the user “pays 2 %”. The overall trading volume is roughly $30.

For further discussion, please note that MM2 is trade S2 for S3 (at there limit price) but the order S2 for S1 which would create more utility for MM2 remains full unfilled although the limit price is strictly below the clearing price.

So the intuitive solution to simply settle the trade of the user with the market maker that is willing to do the opposite trade does NOT maximize volume. If the user would pick a lower limit price and the number of tokens would be increase (possibility for bigger rings) the problem would get worse. Basically the user is exploited to the max to allow more trades.

**Example utility optimization**:

The described problem can be fixed if we optimized for “overall trader utility” instead. Utility in the example above would be 0 since all trades are exactly executed at the limit price == you could argue the price at which the person is indifferent between trading and not trading. However - any solution that lets MM2 trade directly against the user will create utility for MM2 if executed at a price of 0.998 for the user if executed at 0.99 and for both if executed anywhere in between. If writing and optimizer it turns out that the optimal solution will split the utility 50% 50% between the two trades. This might lead to an “acceptable price” in this example of ~0.9985 but it gets worse if the user would submit a “market order” == “an order with a very low limit price”.

We would argue if the market provides plenty of liquidity at $0.99 then the user should get that price. Of course the system does not differentiate between market maker and user, so simply the fact that more liquidity is available at a price makes this price the market maker price.

Those prices can be enforced if we tighten the rules for a valid solutions:

1. Pick a price for each token
2. ..
a) Orders that are below the clearing price HAVE TO BE FULLY executed
b) Orders that are on the clearing price CAN be executed
3. Define a volume (from 0-100%) for each order that CAN be executed
4. Make sure that for each token “total amount sold == total amount bought”

Now we still could not come up with a proof (nor a counter proof) that a valid solution under those rules is always possible. But we are pretty certain that there is no way that a valid solution can be practically found in a given time period.

For this reason we tried a 3rd optimization criteria that does not fully forbid unfilled orders below the “clearing price” but it penalized them. We called it “disregarded utility”. Basically for each order it calculates the utility as before but IN ADDITION it subtracts the amount that was “disregarded”. “Disregarded utility” is defined here as the utility that would have been generated if the order was executed fully - how much utility was actually generated. If the clearing price is == the limit price of an order the utility is always 0 no matter how much was executed. However - if the limit price of an order is below the clearing price it will generate disregarded utility UNLESS it is executed fully.

So far this optimization metric has generated results that are in line with what we intuitively would have expected the system to do.

**Solution verification on-chain**

The only big downside of this metric over utility and volume is that the solution verification/ specifically the measurement of the objective function are now in terms of gas costs depended on the total number of open orders instead of only those orders that are executed in the batch.

This is a reason why we are looking for other objective functions where ideally only the touched orders play a role in the objective function.

**Additional resources:**

https://github.com/gnosis/dex-contracts

Smart contract that allows so far submissions optimized for volume

[Paper](https://link.springer.com/chapter/10.1007/978-3-030-18500-8_29) on how to convert the optimization problem for volume into a mix integer optimization problem.

[batchauctions_or2018.pdf](/uploads/short-url/fwDWwQibfMw1xGyXkMo7O3qKRII.pdf) (187.9 KB)

## Replies

**vbuterin** (2019-10-04):

Here’s a hopefully helpful tool for looking at it geometrically. Define a price A : B : C between three assets (this generalized to n > 3 but the n=3 case is clearer visually), as a point (x, y), where x = log(A:B), y = log(B : C), and so naturally x+y = log(A : C).

[![Prices](https://ethresear.ch/uploads/default/original/2X/7/77480c327855cbee0b27ed13b1d509dd2617f048.png)Prices369×360 3.21 KB](https://ethresear.ch/uploads/default/77480c327855cbee0b27ed13b1d509dd2617f048)

Any unclaimed order blacks out half the area according to the following rules:

- An order buying B for A blacks out everything to the right of a vertical line
- An order buying A for B blacks out everything to the left of a vertical line
- An order buying C for B blacks out everything above a horizontal line
- An order buying B for C blacks out everything below a vertical line
- An order buying C for A blacks out everything to the NE of a NWSE diagonal line
- An order buying A for C blacks out everything to the SW of a NWSE diagonal line

[![Prices(1)](https://ethresear.ch/uploads/default/original/2X/d/d5c8df416a1f8eb487edb5faafc6381fde6335a7.png)Prices(1)469×360 12.2 KB](https://ethresear.ch/uploads/default/d5c8df416a1f8eb487edb5faafc6381fde6335a7)

The task is to figure out which orders to remove (and removing orders must happen in sets that share an incompatible region or at least line/point) to make the white triangle (or sometimes polygon) nonzero.

> Now we still could not come up with a proof (nor a counter proof) that a valid solution under those rules is always possible

I think in this model proving this is easy. Start removing incompatible orders in sets; eventually this process will lead to the white polygon being nonzero, because if it is zero then there’s still more touching/intersecting sets that can be removed.

---

**technocrypto** (2019-10-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> Pick a price for each token
> …
> a) Orders that are below the clearing price HAVE TO BE FULLY executed
> b) Orders that are on the clearing price CAN be executed
> Define a volume (from 0-100%) for each order that CAN be executed
> Make sure that for each token “total amount sold == total amount bought”

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think in this model proving this is easy. Start removing incompatible orders in sets; eventually this process will lead to the white polygon being nonzero, because if it is zero then there’s still more touching/intersecting sets that can be removed.

Martin was filling me in on this one a little bit this evening.  I don’t think you can remove incompatible orders while still satisfying the rules, if they exhibit incoherent preferences.  That’s basically the Condorcet paradox (or at least the Condorcet paradox is an example of a net incoherent preference).  With net cyclic preference it is impossible to satisfy the rule of orders below clearing prices having to be fully executed.  I came up with a specific example that I claim exhibits this and Martin is going to look over it and see if he agrees that it has no solution while abiding by the stricter ruleset. Do you claim that a valid solution is possible even if net market preferences are cyclic?

---

**vbuterin** (2019-10-10):

I think the 2D plane representation inherently blocks out incoherent/cyclic preferences. But would love to hear the argument if that’s somehow not true.

---

**mkoeppelmann** (2019-10-11):

Trying to summarize latest discussion:

[@technocrypto](/u/technocrypto) assumption was that there might be set of cyclical preferences where no single price clearing with the strict clearing criteria (Orders with a limit price strictly below the clearing price MUST FULLY be executed)

Roughly the idea was that trades prefer A > B; B > C but also C over A. We do on each pair 2 orders - and if those orders would be cleared against each other we would result in the cyclical preference.

However - it is also possible to first clear a ring A-B-C which removes at least one order from that ring. Now we can find price points for the other 2 trading pairs so that they even out.

You can find the exact example as a JSON here:



      [pastebin.com](https://pastebin.com/BNvTkEyc)





####

```auto

```










The solution looks like this:

> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyAforB_ : sell    88.200000 / buy    84.000000 / executable 1 / utility   0.000000
> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyAforC_ : sell     0.000000 / buy     0.000000 / executable 0 / utility   0.000000
> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyBforA_ : sell    80.000000 / buy    84.000000 / executable 1 / utility   4.200000
> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyBforC_ : sell    10.000000 / buy     9.523810 / executable 1 / utility   0.000000
> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyCforA_ : sell     4.000000 / buy     4.410000 / executable 1 / utility   0.410000
> [INFO : OptModelNLP.py:427 | getOrderExecution()]                       buyCforB_ : sell     5.323810 / buy     5.590000 / executable 1 / utility   0.132381
> [INFO : main.py:341 | solve()]  Computed prices:
> [INFO : main.py:344 | solve()]      A :     1.1025
> [INFO : main.py:344 | solve()]      B :     1.0500
> [INFO : main.py:344 | solve()]      C :     1.0000

Full solution data here:



      [pastebin.com](https://pastebin.com/GZqu24NR)





####

```auto

```










log 2D representation after [@vbuterin](/u/vbuterin) here:

[![IMG_8408](https://ethresear.ch/uploads/default/optimized/2X/e/e70ed6559b3c31696c874039bfbd81db7f48e8b0_2_375x500.jpeg)IMG_84083024×4032 2.03 MB](https://ethresear.ch/uploads/default/e70ed6559b3c31696c874039bfbd81db7f48e8b0)

While the graphical representation helps it is not yet clear if it results in a path to an algorithm that always finds a solution. The issue is that e.g. in this instance the first set of orders that needs to be “removed” is the ring (and not a pair on one trading pair). It is not clear if that is a general strategy. Another issue is that wether or not orders are removed DEPENDS ON THE EXACT PRICE POINT. So if after removing orders you end up with a triangle space - then moving within this space might make the orders no longer fully removed.

In summary, the open questions are:

a) Does always a solution exist under the strict criteria?

b) Does a algorithm exist to find it in polynomial time?

In reality more restrictions do exist - since in a blockchain system we will only be able to execute a limited number of orders per batch. For that reason it is clear that we can not in every case clear all orders according to the rule. Therefore we will likely in any case not fully require the strict criteria but penalize solutions that violate the strict criteria (substract disregarded utility)

---

**fleupold** (2019-10-13):

I believe what we are trying to find here is a Walrasian Equilibrium in a pure exchange economy (sometimes also referred to as General Equilibrium). The following definition is taken from [this paper](https://web.stanford.edu/~jdlevin/Econ%20202/General%20Equilibrium.pdf).

[![15](https://ethresear.ch/uploads/default/optimized/2X/7/7abb1c311daa162a2e46a3c3fd88065c2bb90d3f_2_690x116.png)15707×119 35.3 KB](https://ethresear.ch/uploads/default/7abb1c311daa162a2e46a3c3fd88065c2bb90d3f)

[![21](https://ethresear.ch/uploads/default/optimized/2X/b/b90a647209bea95f285eb398ae1c328219f6b1ee_2_690x130.png)21712×135 17.8 KB](https://ethresear.ch/uploads/default/b90a647209bea95f285eb398ae1c328219f6b1ee)

(Where p is a non-negative price vector of the L goods).

[![58](https://ethresear.ch/uploads/default/optimized/2X/5/5be1496c633d24808f31428b3aa43c5e8bb64d61_2_690x436.png)58743×470 71.2 KB](https://ethresear.ch/uploads/default/5be1496c633d24808f31428b3aa43c5e8bb64d61)

Definition 1.1. implies that

> 2.a) Orders that are below the clearing price HAVE TO BE FULLY executed

Otherwise there would exist an agent i who could increase their utility by selling their remaining non-executed sell volume.

> 2.b) Orders that are on the clearing price CAN be executed

Traders whose limit prices are equal to the clearing price are indifferent, therefore partial execution does not affect their utility.

> Make sure that for each token “total amount sold == total amount bought”

Equivalent to definition 1.2.

**Now the question is does such an equilibrium always exist?**

I haven’t really found an answer to this problem. [This paper](http://www.ebour.com.ar/pdfs/Faruk%20Gul,%20Walrasoan%20Equilibrium.pdf) seems to show that such an equilibrium can only exist if the valuation functions are *gross substitute*:

[![56](https://ethresear.ch/uploads/default/optimized/2X/8/876f5862424ef8b18b1eaf1af1e5d655f5074f12_2_690x93.png)561432×194 38.6 KB](https://ethresear.ch/uploads/default/876f5862424ef8b18b1eaf1af1e5d655f5074f12)

(where the strict inequality `x_l(p') > x_l(p)` can be relaxed to a weak inequality)

This is not the case in our application since we use one good to pay for another, thus an increase in the price of the good to be sold, might lower our demand for the good to be bought (at p(A)=0.9 you might be willing to buy 100B, but at p(A) = 1.1 your demand for B could be 0).

[Another Paper](https://arxiv.org/pdf/1511.04032.pdf) claims that the above mentioned result only applies to *“the class of valuation functions that are closed under summing an additive functions”* and that there are non gross-substitutes valuations (e.g. a single buyer) in which we can still guarantee such an equilibrium. I’m not sure if our valuation profile (expressed by a finite set of limit sell orders) satisfies that criteria.

---

**mkoeppelmann** (2020-01-28):

The question around the best matching strategy is still an ongoing research topic.

However - we went ahead and published the first version of contracts facilitating batch auctions.

Current parameters are:

- 5 minutes batch times
- all orders submitted on-chain
- (almost) unlimited number of tokens and orders
- a solver can submit solutions always 4 minutes after the batch closes
- solutions will be immediately executed - the previous submitted solution will be rolled back if the current one is better
- a solution is only allowed to touch 30 trades (otherwise you can get too close to the block gas limit and miners would get an unfair advantage including those large transactions)

Contract live [here](https://etherscan.io/address/0x6F400810b62df8E13fded51bE75fF5393eaa841F#code). Public [bug bounty](https://blog.gnosis.pm/2020-dex-bug-bounty-210f2b67a764) started today.

