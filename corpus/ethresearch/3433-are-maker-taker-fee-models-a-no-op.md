---
source: ethresearch
topic_id: 3433
title: Are maker-taker fee models a no-op?
author: vbuterin
date: "2018-09-19"
category: Economics
tags: [market-microstructure]
url: https://ethresear.ch/t/are-maker-taker-fee-models-a-no-op/3433
views: 4416
likes: 2
posts_count: 27
---

# Are maker-taker fee models a no-op?

The default fee model for exchanges to use is one where some fee, eg. 0.30%, is charged to both the buyer and the seller of an order. However, some exchanges use a newer model called “maker-taker fees”, where the party that posted the order earlier (the “maker”) pays a lower (or even zero or negative) fee, and the party that posted the order that claimed the other order and caused the exchange to take place (the “taker”) pays a higher fee.

I can argue that such a model is actually economically equivalent to a model where fees are even. Suppose that, in universe A, there is an exchange with a 0.30% fee to both sides, where the buyers and sellers are willing to bid $1000 and ask $1010. If someone wants to come in and sell, then they would get $997 and the buyer would pay $1003, and if someone wants to come in and buy, they would pay $1013 and the seller would get $1007.

Now, consider universe B, where there is a 0.60% taker fee and a zero maker fee. Rational market participants do not care about numbers displayed on a screen; they care about how much money they ultimately pay or get. The sellers that bid $1000 in universe A were clearly willing to buy *under the terms that they pay $1003*. Hence, in universe B, they have the same preferences, and so they would be willing to bid $1003, as there are no fees for makers. Similarly, the buyers were willing to *sell under the terms that they get $1007*. Hence, they would be willing to ask $1007. Now, the spread is nominally smaller ($1003-1007 instead of $1000-1010), but in reality, someone coming in to sell would get $1003 - 0.60% = $997, and someone coming in to buy would get $1007 + 0.60% = $1013. So the de facto situation is unchanged.

So this leads be to believe that any differences between maker-taker fees and standard fees are entirely behavioral and cosmetic in nature, and not economic; from a pure economic point of view, both costs and benefits of switching from one model to the other are zero to all parties.

I read the [SEC memo on maker-taker fees](https://www.sec.gov/spotlight/emsac/memo-maker-taker-fees-on-equities-exchanges.pdf) and as far as I can tell it does not address this.

Is my logic correct? Are there any flaws in my reasoning?

---

Edit: here’s another way of seeing this. Imagine in universe C there was an exchange with 0.30% fees, but where the *interface* was modified so that creating a bid order at x actually created an order at x + 0.3%, and creating an ask order actually created an order at x - 0.3%. Hence, when someone *claims* an order, they would pay a 0.6% “fee” relative to the amount inserted into the textbox by the order creator, and the order creator would pay a 0.3% fee based on a rate 0.3% more favorable than what they inserted into the textbox, so their “perceived fee” would be zero. Hence, a maker-taker fee model is isomorphic to a distortion in the user interface, and it’s clear to see that if traders were faced with a distortion in the user interface as described above, they would simply mentally compensate for it, typing in $1000 when they mean to make a bid order at $1003, etc, and so this should happen with a maker-taker fee model as well.

## Replies

**gloine** (2018-09-19):

I think the whole point of maker-taker fee is to steal liquidity from other exchanges. If all the exchanges adopt maker-taker fees, there should be no difference as per your argument above. However, if two exchanges with different fee models coexist, market makers would do arbitrage trading by:

1. placing orders on the maker-taker fee exchange
2. waiting for the orders to be executed
3. immediately executing a market order on the standard fee exchange (or placing an aggressive limit order).

The total fee cost would be 0.30%, which is half of the case there are two standard fee exchanges, or two maker-taker fee exchanges. If they do this in the opposite direction, the fee cost would be 0.90%. Thus, one way liquidity stealing takes place.

---

**MicahZoltu** (2018-09-19):

The argument for maker-taker fee models that I have seen is entirely around behavioral psychology.  I think everyone agrees that given a single exchange, who pays the fee doesn’t matter, the cost of the fee will be born by those most willing to pay it.

The behavioral argument is that makers need to be incentivized because they are adding liquidity while takers are removing liquidity.  The maker-taker fee model makes people *feel* like they get a better deal when they are the maker instead of the taker, thus converting some people who would otherwise be on the fence from takers to makers.  Following this logic, you want to set the difference in fees such that you optimize for having an equal number of makers and takers (by volume).

---

**Lars** (2018-09-19):

If I had a lot I want to sell, I probably would select an exchange with low maker fees.

If I want to buy a lot, I probably select an exchange with low taker fees.

This should lead to an unbalanced demand/supply situation. The first type of exchange would have a lower ratio of demand/supply than the other one, resulting in lower prices.

On the other hand, maybe most volumes come from traders. They tend to sell and buy approximately the same volume. For a trader, I think it the various fee systems can be seen as equivalent, regardless of the distribution of fees.

---

**paborre** (2018-09-19):

Consider that there exists a mandated minimum tick size.  So in your example, assume a minimum tick size of $10.  Orders for $1000 and $1010 are valid, but orders for $1003 and $1007 will be rejected.  Now universe B can no longer realize an equivalence.

---

**vbuterin** (2018-09-20):

> If I had a lot I want to sell, I probably would select an exchange with low maker fees. If I want to buy a lot, I probably select an exchange with low taker fees. This should lead to an unbalanced demand/supply situation. The first type of exchange would have a lower ratio of demand/supply than the other one, resulting in lower prices.

Sure, but then what that would mean is that if you want to buy a lot, you would then be more inclined to buy on the first exchange, because its prices are lower. In equilibrium, the buy and sell prices inclusive of fees should be equal on both exchanges.

> Consider that there exists a mandated minimum tick size. So in your example, assume a minimum tick size of $10. Orders for $1000 and $1010 are valid, but orders for $1003 and $1007 will be rejected. Now universe B can no longer realize an equivalence.

Sure, but what kind of exchange has a minimum tick size equal to 1% of the purchase price? Or is this argument actually relevant in traditional stock exchanges but not in crypto exchanges because in traditional stock exchanges trade commissions are much lower and minimum tick sizes are higher?

---

**paborre** (2018-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Or is this argument actually relevant in traditional stock exchanges but not in crypto exchanges

Yeah, sorry, I was thinking of US stock markets where the tick size is $0.01 and taker fees are typically $0.003 (not a %) per share.  Maker-taker is pervasive there because of regulatory constraints like the penny rule and also because of a best price (not best all-in cost) priority rule. In the absence of those constraints, as with crypto, it’s harder to explain.  I suppose it is still true that an asymmetric fee should make a trader marginally more likely to post a resting limit order rather than just take the best available price.  The difference is immediacy and probability of trade.  In theory, the trader has some private value for those properties and may be willing to sacrifice them for lower or no fees.  The exchange thus has marginally more orders resting on its book and may be a more attractive venue relative to other exchanges with symmetric fees.

---

**denett** (2018-09-20):

There is a real change in market behavior when the maker fee is below the taker fee. This is because markets usually have a constraint, that in the order-book, the bids should be below the asks. So at some point a maker can not increase its buy-price or lower its sell-price.

This will result in a slightly less efficient market, because some transactions are not possible even when there is a maker and a taker available who are both willing to do the trade.

I think this lower efficiency works in favor of the makers, because the takers are usually more time constrained and are more willing to take a less favorable price.

---

**denett** (2018-09-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/lars/48/14_2.png) Lars:

> If I had a lot I want to sell, I probably would select an exchange with low maker fees.
> If I want to buy a lot, I probably select an exchange with low taker fees.

Why does it matter if you are buying or selling? Buying ether with dollars is the same as selling dollars for ether.

---

**Lars** (2018-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> Why does it matter if you are buying or selling?

You are right, I didn’t think about it that way. You can of course sell ether without being a market maker. I was thinking about the case where you put up a big sum of ether on the supply side. Of course, it may be better to use OTC services if that is the case.

---

**jtran** (2018-09-21):

As a whole, users are incentivized to engage in mechanisms that benefit either the exchange or siding to either becoming a maker, taker.

Reduce one area, we see a shift towards the other. However, entirely there is a set of people who find minimal maker, taker percentages less meaningful to their overall state.

---

**MaverickChow** (2018-09-22):

The main reason why (as I personally understand it) exchanges arrange different maker-taker fees is purely to bring in different market participants to provide (or take, dependent on specific need) liquidity / activity to that particular exchange. Say if I maintain an exchange and I desperately want to have participants to provide the necessary liquidity, I will arrange to have 0% maker fee so that participants are more incentivized to post limit orders that will help to make my order book thick, and that will further attract more participants to trade at my exchange. Participants that are desperate enough for liquidity that they will trade at market order will care less about the 0.6% I would impose on them being takers because if they were to trade elsewhere that have much less liquidity, they would incur far higher costs like wider spread and slippage.

Not behavioral. Not cosmetic. Purely economic dependent on the need of the exchange.

For further study, please refer to topics on **market microstructure**.

---

**vbuterin** (2018-09-22):

My argument in the initial post showed that from a purely economic standpoint, you can prove that going from (0.3%, 0.3%) to (0%, 0.6%) should in equilibrium cause the *nominal* spread to shrink by 0.3%, so the *real* spread (ie. amount you can buy for including fees minus amount you can sell for including fees) is unchanged.

You can’t say that “participants are desperate for liquidity and so they are price insensitive”, because if that was true, the exchange would have already increased the fee from, say, (0.3%, 0.3%) to (0.3%, 0.6%) or even (0.6%, 0.6%).

---

**MaverickChow** (2018-09-22):

I believe there is always inefficiencies that will remain persistent for a long time. And that includes the spread regardless of whether it will shrink by 0.3% or remain wide. At most, what an efficient participant can do is to exploit the inefficiencies but still that does not guarantee the inefficiencies will certainly fade away. In a market where everyone has equal footing, aggregate inefficiencies make it more efficient as a whole, but not perfectly so. In a market whereby we see 100% perfect efficiency always have participants that have unfair privileges. Because maintaining perfect efficiency incur costs that only a participant with unfair privileges can afford to maintain. The world of HFT (high-frequency trading) is a good example.

A desperate participant will certainly be price insensitive, no matter what logic says. This is because all trading is forward-looking, i.e. I expect the price will appreciate by 5%, everyone expects the same, the current price is at 1% premium, if I do not buy now but instead wait for it to fall by 1% before I do so, then I will forgo 4% return potential to other more aggressive participants that do not care to buy at premium. And thus, I will take the action to buy at 1% premium even though logic says it is inefficient as of now.

Indeed, if all participants are very desperate for liquidity and the exchange is the one and only dominant player around, then yes, it is very likely fee may be increased to (0.6%, 0.6%) or even (1.2%, 1.2%). But as there is stiff competition around, then such fee may not increase despite desperate participants. If human decision-making can be as efficient as computer logic, then the world may probably have no need for economics as nobody can be gamed.

If the maker-taker fee is purely cosmetic and not economic, then what do you think a newly-opened exchange should do to attract participants? How should the fee be set to attract both market makers and liquidity takers? The industry is so competitive that some exchanges are even offering rebates to market makers. Ultimately, the point of having differing fee structure is to attract participants to generate liquidity and activity to the exchange. How the fee is being structured, or sliced and diced between the different participants depends on the need of the exchange. I cannot think of any cosmetic reason other than economic ones.

---

**vbuterin** (2018-09-22):

> How should the fee be set to attract both market makers and liquidity takers?

Honestly, if everyone else is doing maker-taker fees and that’s what attracts people for behavioral reasons, then go ahead and do that; it’s not like there’s any economic harm in doing it one way over another. But in general, I don’t think there’s anything you can do to incentivize a lower net spread into existence unless you are willing to pay for it, whether in lost revenues from lower total fees or from explicit subsidies.

---

**MaverickChow** (2018-09-22):

That is why some exchanges are offering rebates, as you correctly pointed out by saying “unless you are willing to pay for it, whether in lost revenues from lower total fees or from explicit subsidies.” Exchanges that do not play the game in a fair manner try to minimize such cost of running the business by engaging in all sorts of nefarious activities, including front-running the participants and trading between their own accounts to give the illusion of liquidity. The behavioral reason is purely an economic one. Ultimately, it is all about making a profit.

I would submit a limit order of $1000 even when I mean to buy at $1003 **if and only if** I expect the market to go sideway within the duration of my order while it lasts. As the market is forward-looking and if I anticipate it will move up, I would not submit limit order of $1000. Probably I would do so at $1005 if market activity is very high. At the same time, I would also expect the limit sell order to be much higher than 0.3% spread as participants engage in FOMO, thus the “inefficiency.”

Yes, in a market whereby every participant has fixed supply of stuff to buy and sell that they cannot inflate or deflate at will, both costs and benefits of switching from one model to the other will be zero to all parties. Here, we are talking about taking the average. In reality, some will make lots of money while many others will lose lots of money.

An exchange does not have any interest in determining which participant will make lots of money and which other will lose lots of money. It cares only to structure the right maker-taker fees in accordance to its needs in order to attract all sorts of participants, winners and losers alike, to join the exchange and provide liquidity and activity so that it will earn fees from everyone. If it cannot do so at first through honest means, it will do so through nefarious means, including front-running, internalizing orders, sub-pennying, etc.

---

**MaverickChow** (2018-09-22):

After going through the SEC memo on maker-taker fees very briefly, assuming I understand it correctly, the SEC is trying to review the current maker-taker fee structure for a possible revamp in order to create a fairer market for all participants and increase the liquidity.

If so, then I believe the increasing illiquidity has nothing to do with any form of maker-taker fee. Rather, it has to do with rampant HFT, sub-pennying, decimalization of share prices, etc that while it caused the spread to artificially narrow, it also took the market-making potential away from traditional market-makers and relentlessly exploit market participants through front-running. As a result of trying to make the market more efficient, exchanges engaged in unfair means that end up making it far more inefficient than ever. As result, liquidity declined over the years substantially.

You can find various books on HFT on how it gamed the market and sucks liquidity out of it. Revamping the maker-taker fee structure will not restore liquidity if all the market manipulations such as front-running and sub-pennying are not resolved. If I know I would lose in a highly manipulated market whereby the structure is generally fake, I would not trade in such market even if there is 0% fee.

For exchanges to fantasize it can get all the real liquidity it desires while allowing rampant manipulations to persist is foolish. No restructuring of the maker-taker fee will solve the problem.

Exchanges can restore liquidity by getting rid of HFT front-running, getting rid of sub-pennying, and centralizing the order books (instead of having lots of exchanges that end up fragmentalizing the liquidity) and let real liquidity to grow organically. Whatever the maker-taker fee structure can stay the same.

---

**gloine** (2018-09-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/gloine/48/1830_2.png) gloine:

> The total fee cost would be 0.30%, which is half of the case there are two standard fee exchanges, or two maker-taker fee exchanges. If they do this in the opposite direction, the fee cost would be 0.90%. Thus, one way liquidity stealing takes place.

I realized that this does not steal any more liquidity after two exchanges reach an equilibrium, thus it should be entirely behavioral if it affected liquidity in real world exchanges - let me think twice before wasting valuable time of others…next time.

I have some more thoughts though - if we pay a rebate to market makers by taking it from takers (e.g. -0.3% maker fee and 0.9% taker fee), and the rebate happens to be greater than the average spread (i.e. the average spread < 0.6%), two exchanges never reach an equilibrium, right? Makers should be supplying liquidity on the ‘rebate’ exchange as long as takers consume the orders. This can be argued as behavioral but it reduces uncertainty on the maker’s side - they can confirm that desperate takers (willing to lose some additional 0~0.3%) exist on that exchange (which remains relatively stable over time), and serve them by sucking liquidity from other exchanges. It can enter a positive feedback loop - more immediate liquidity attracts more desperate takers (or I would say normal users), and more market makers enter this business for profit, moving liquidity in one direction. Does this make sense?

---

**0xpeter** (2018-09-28):

The question is about whether a per unit tax or subsidy to one side of a market is fully offset by a change in the price charged to the other side.

Under complete ‘pass through,’ subsidies are fully offset by price reductions and thus subsidies become completely inconsequential. Complete pass through could easily arise in a model, but is much less likely in real life.

Under incomplete ‘pass through,’ the side receiving the subsidy captures some value. The subsidy then encourages entry into the subsidized activity.

You will fail to get complete pass through if any of the following conditions hold:

1. There are ‘transaction costs’ that impede adjustment of prices.
2. Participants on at least one side of the market pay a fixed cost as well as a cost per unit.
3. The side receiving a subsidy is not perfectly competitive.

I would say that (1), (2), and (3) are all important reasons for incomplete pass through on exchanges.

For example:

(1) Many exchanges have minimum tick sizes. This limits makers ability to undercut one another. Once you have a minimum tick size, transaction costs make complete pass through impossible.

(2) Some orders originate from brokers. There is fixed fee component to retail brokerage fees.

(3) The business of market making is highly competitive as a whole. However, market making in at a specific asset/time/place can be much less so. For example, you would likely see greater pass through for highly liquid tokens where many market makers are active simultaneously. For a highly illiquid token, however, there may be only one or two market makers active at a time. In this case, more of the subsidy would be retained by the market makers, the narrowing of the bid ask spread via passthrough is smaller, the increase in the depth of liquidity available as a result of the subsidy is larger.

(Note: (3) implies that the subsidy primarily encourages entry into illiquid trading pairs. Interestingly, after entry, the incumbent market maker will capture less of the subsidy and there will be more pass through. Their is potentially a phenomenon where subsidies work to bootstrap new markets, but you move towards full pass through as the market matures. This is a nice feature because you usually want to selectively subsidize entrepreneurial activity. You do not want the subsidy to be captured by a market that could function effectively without it.)

The concluding section of the following paper has a really awesome and math free discussion of pass through:


      [rchss.sinica.edu.tw](https://www.rchss.sinica.edu.tw/cibs/pdf/RochetTirole3.pdf)


    https://www.rchss.sinica.edu.tw/cibs/pdf/RochetTirole3.pdf

###

311.18 KB

---

**_charlienoyes** (2018-09-28):

This is directly observable in the behavior of exchanges with reasonably sophisticated market participant access and high relative taker costs. For example on GDAX:

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/3b8edf024fa081d6e56ddd4e70a4b17ddf601fb0_2_690x159.png)image1600×370 97.9 KB](https://ethresear.ch/uploads/default/3b8edf024fa081d6e56ddd4e70a4b17ddf601fb0)

Note that the spread is a single cent ($0.01), the minimum tick size. This is a relative bid-ask spread of 0.00013% or .013 BPS at that price level. Credit Suisse publishes yearly data on US equities relative spread trends:

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/73fa1fba8edb4dde27b121c2ee8668149bddd3e2_2_625x500.png)image1260×1008 59 KB](https://ethresear.ch/uploads/default/73fa1fba8edb4dde27b121c2ee8668149bddd3e2)

Implies about a 200x multiple on average relative spread US equities vs GDAX. Considering that Bitcoin is a far more volatile asset than the average US equity (and the spread makers are willing to offer should be directly related to volatility) one could reasonably conclude that the phenomenon is the result of sophisticated actors, who would otherwise be takers, meeting at a 1c spread, waiting for either (1) an unsophisticated retail trader to naively take the order, or (2) a more informed sophisticated actor to take it once their predicted change is > the cost of taking it (in this case, the cost being 0.1%-0.3% of notional trade value that GDAX charges).

Interestingly, traditional equities and commodities markets charge flat fees (e.g. 0.25c/share) instead of “% of notional trade value” fees that are common in crypto. It basically means that actor (2) in the above must always be able to reliably predict change in BTC value >= 0.1-0.3% in order to make any liquidity taking order worth it. As the cost of a taker order goes to zero the amount of time expected for that much volatility also goes to zero so you would see less time spent sitting at a 1c spread.

You can check the spread yourself, right now and every other time I’ve looked it’s at or quickly approaching 1c (screenshot above isn’t cherrypicked). I suspect that if the tick size were to be arbitrarily more granular it wouldn’t matter and the spread would continue to approach it (e.g. we’d still be sitting at a $1e-5 spread if that level of tick resolution was offered).

---

**vbuterin** (2018-09-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/0xpeter/48/2321_2.png) 0xpeter:

> Participants on at least one side of the market pay a fixed cost as well as a cost per unit.
> The side receiving a subsidy is not perfectly competitive.

I think this line of reasoning fails to take into account the other argument that I added to the end of my post: that a maker/taker fee model is isomorphic to a change in the user interface. I agree that fixed tick sizes are a good reason why maker/taker models would not be no-ops, but (2) and (3) do not change the basic reality of my argument, which does not make any assumptions about cost structure or competitiveness.


*(6 more replies not shown)*
