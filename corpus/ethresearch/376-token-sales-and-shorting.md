---
source: ethresearch
topic_id: 376
title: Token sales and shorting
author: vbuterin
date: "2017-12-26"
category: Better ICOs
tags: [short-selling, efficient-market-hypothesis]
url: https://ethresear.ch/t/token-sales-and-shorting/376
views: 13557
likes: 21
posts_count: 28
---

# Token sales and shorting

I have started recently reading Eliezer Yudkowsky’s new book *[Inadequate Equilibria](https://equilibriabook.com/)*, and one of the topics brought up in the first chapter is the question of in what cases is the efficient market hypothesis less likely to hold well. One major answer that is brought up is: markets are much more inefficient if it is not feasible to short.

I quote:

> There was recently a startup called Color Labs, aka Color.com, whose putative purpose was to
> let people share photos with their friends and see other photos that had been taken nearby. They closed $41 million in funding, including $20 million from the prestigious Sequoia Capital. When the news of their funding broke, practically everyone on the online Hacker News forum was rolling their eyes and predicting failure. It seemed like a nitwit me-too idea to me too.
>
>
> And then, yes, Color Labs failed and the 20-person team sold themselves to Apple for $7 million and the venture capitalists didn’t make back their money. And yes, it sounds to me like the
> prestigious Sequoia Capital bought into the wrong startup. If that’s all true, it’s not a coincidence that neither I nor any of the other onlookers could make money on our advance prediction. The startup equity market was inefficient (a price underwent a predictable decline), but it wasn’t exploitable. There was no way to make a profit just by predicting that Sequoia had overpaid for the stock it bought.

Also:

> Though beware that even in a stock market, some stocks are harder to short than
> others—like stocks that have just IPOed. Drechsler and Drechsler found that creat-
> ing a broad market fund of only assets that are easy to short in recent years would have
> produced 5% higher returns (!) than index funds that don’t kick out hard-to-short as-
> sets (https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2387099). Unfortunately, I
> don’t know of any index fund that actually tracks this strategy, or it’s what I’d own as
> my main financial asset.

And regarding inefficiency of the housing market:

> Robert Shiller (https://www.nytimes.com/2015/07/26/upshot/the-housing-market-still-isnt-rational.html) cites Edward Miller (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.667.5934&rep=rep1&type=pdf) as having observed in 1977 that efficiency requires short sales, and either Shiller or Miller observes that houses can’t be shorted.

To those of us in the crypto space, this strikes close to home. We see coins whose market caps reach billions despite the professional crypto community pointing out scams, crazy technical schemes, insecure hash functions, underdeveloped projects, and more, and there really isn’t a good way to express these opinions in the market. Adding shorting markets is super-hard for a few reasons. First of all, most exchanges don’t support it, and even those that do often only support it for mainstream reputable cryptocurrencies. Second, cryptocurrency prices are absurdly volatile, so there’s a high risk anyone shorting will suffer a liquidation event.

So can we try to do better by adding good shorting mechanisms? One comment I can immediately make is that even if cryptos are super-volatile, they are less volatile against *each other* than they are against fiat, so markets that allow shorting [random possibly untrustworthy token] / [BTC or ETH] could work somewhat better. But high crypto-to-crypto volatility still remains.

There are three real solutions to the remaining hyper-volatility that I can see:

1. Require super-high capital inefficiency (eg. 30 ETH deposit for each 1 ETH that you short)
2. Support only partial shorting, where for example you lose 1 ETH every time the price of [random possibly untrustworthy token] rises 2x, but up to a maximum of 8x. People buying [random possibly untrustworthy token] could still want to buy the original if they’re hoping for gains above the 8x, but if they’re just hoping for a quick 2-3x gain then they’d get better luck betting in the shorting market, and shorters would be willing to pay some modest premium (ie. the average token they short would need to fall by at least, say, 1% per month for them to make a return).
3. Shared collateral. You would put down 80 ETH to be able to short 10 different tokens (ie. only 8x collateral requirements), and a liquidation event would only happen if the sum of all 10 returns reaches 80. This is the equivalent to the partial solution that the housing market already has, which is that you can short REIT shares.

Any other ideas that could help here?

## Replies

**kladkogex** (2017-12-26):

There is also a good book of George Soros called “Alchemy of Finance” , where he specifies his [reflexivity theory.](https://www.ft.com/content/0ca06172-bfe9-11de-aed2-00144feab49a)

> I can state the core idea in two relatively simple propositions. One is that in situations that have thinking participants, the participants’ view of the world is always partial and distorted. That is the principle of fallibility. The other is that these distorted views can influence the situation to which they relate because false views lead to inappropriate actions. That is the principle of reflexivity. For instance, treating drug addicts as criminals creates criminal behavior. It misconstrues the problem and interferes with the proper treatment of addicts. As another example, declaring that government is bad tends to make for bad government.
>
>
> Both fallibility and reflexivity are sheer common sense. So when my critics say that I am merely stating the obvious, they are right—but only up to a point. What makes my propositions interesting is that their significance has not been generally appreciated. The concept of reflexivity, in particular, has been studiously avoided and even denied by economic theory. So my conceptual framework deserves to be taken seriously—not because it constitutes a new discovery but because something as commonsensical as reflexivity has been so studiously ignored.
>
>
> Recognizing reflexivity has been sacrificed to the vain pursuit of certainty in human affairs, most notably in economics, and yet, uncertainty is the key feature of human affairs. Economic theory is built on the concept of equilibrium, and that concept is in direct contradiction with the concept of reflexivity. As I shall show in the next lecture, the two concepts yield two entirely different interpretations of financial markets.
>
>
> The concept of fallibility is far less controversial. It is generally recognized that the complexity of the world in which we live exceeds our capacity to comprehend it. I have no great new insights to offer. The main source of difficulties is that participants are part of the situation they have to deal with. Confronted by a reality of extreme complexity we are obliged to resort to various methods of simplification—generalizations, dichotomies, metaphors, decision-rules, moral precepts, to mention just a few. These mental constructs take on an existence of their own, further complicating the situation.
>
>
> The structure of the brain is another source of distortions. Recent advances in brain science have begun to provide some insight into how the brain functions, and they have substantiated Hume’s contention that reason is the slave of passion. The idea of a disembodied intellect or reason is a figment of our imagination.
>
>
> The brain is bombarded by millions of sensory impulses but consciousness can process only seven or eight subjects concurrently. The impulses need to be condensed, ordered and interpreted under immense time pressure, and mistakes and distortions can’t be avoided. Brain science adds many new details to my original contention that our understanding of the world in which we live is inherently imperfect.

---

**kladkogex** (2017-12-26):

One of the reasons why wall street does not fluctuate so much as crypto currencies is because on NASDAQ and NYSE have money makers so that you can always buy and sell from the money maker.

Here is a description of a money maker smart contract that we have been developing for our token tentatively named GEX. Essentially we want to provide for people to instantly buy our token on from a smart contract without them having to go to token exchanges.

The main idea is that the smart contract immediately lends you against its reserves, and then does the actual exchange at the end of the day (time 0:00)

> The main purpose of GEXBot is to achieve liquidity of GEX vs. ETH.
>
>
> Typically, when an asset is traded on an asset exchange, buyers post bids
> (buy requests) and sellers post asks (sell offers).
>
>
> If the asset is thinly traded, bids and asks become scarce, orders take long
> time to complete and the price fluctuates strongly. Intuitively it is explained
> by visualizing a picture, where buyers and sellers come to the market place
> infrequently. When a seller comes to the marketplace there is no buyer, and
> when the buyer comes to the marketplace, there is no seller.
>
>
> To increase liquidity, we introduce GEXBot, and automated money maker that
> is always available for transactions.
>
>
> Let us first describe a very simple algorithm, where GEX sellers and ETH
> sellers place their orders with GEXBot.
>
>
> In particular,
>
>
> (1) Intra-day, GEX sellers communicate orders to GEXBot, depositing
> GEX coins to sell with GEXBot
>
>
> (2) Intray-day, ETH sellers communicate orders to GEXBot, depositing
>
>
> ETH coins to sell with GEXBot
>
>
> (3) All order amounts are public
>
>
> (4) At the end of the day, at time 0:00, GEXBot calculates GEX vs ETH
> exchange rate by dividing the total GEX deposits by the total ETH
> deposits
>
>
> (5) GEXBot then distributes deposits according to the exchange rate,
> transferring GEX to ETH sellers and ETH to GEX sellers
>
>
> The algorithm described above can actually work quite well. The exchange
> rate may fluctuate a bit against the exchange rate at external asset exchanges,
> but since the order book is public, as time 0:00 approaches, arbitrage traders
> will seek profit by issuing pairs of orders against GEXBot and against the
> external exchange. As a result of this profit-seeking, the rate at the close time
> 0:00 will be reasonably in sync with external exchanges.
>
>
> The main problem with the algorithm described above is that the partic-
> ipants have to wait until 0:00 to get the assets they want. Someone who needs
> GEX services and has ETH in her waller will need to wait hours to get GEX.
> This is clearly not tolerable.
>
>
> The idea is to augment the algorithm above, so when the seller places an
> order with GEXBot, GEXBot temporarily  lends to the seller the asset that
> the seller needs, assuming that the loan is repaid at the close time 0:00.
> The question is then, how much can GEXBot lend to the seller without
> assuming too much risk.
> Let us consider an example, where the seller needs to sell 100 ETH for
> GEX, and the exchange rate at the previous day close time is 2ET H = 1GEX
>
>
> (1) The seller deposits 100 ETH with GEXBot.
>
>
> (2) GEXBot immediately lends to the seller 50 GEX, hoping that the ex-
> change rate at close will be the same, as it was yesterday at 0:00.
>
>
> (3) Imagine the exchange rate drops, so at 0:00, 100 ETH = 47 GEX.
> GEXBot will then realise a loss of 3 GEX, that will have to come out
> of its GEX reserve.
>
>
> As we see in the example above, if GEXBot lends to the seller at the
> exchange rate of the previous day, GEXBot can incur a loss if the rate drops.
> To compensate for these losses, let us require the seller to deposit a 20%
> safety margin, since we know that most day-to-day price fluctuations are less
> than 20%.
>
>
> Then the modified algorithm works as follows:
>
>
> (1) The seller deposits 120 ETH with GEXBot. Out of this, 100 GEX is
> the principle, and 20 GEX is the safety margin
> (2) GEXBot immediately lends to the seller 50 GEX, applying the previous
> day’s exchange rate to the principle
> (3) imagine, the rate drops, so at 0:00 one has, 100 ETH = 47 GEX
> (4) GEXBot sells ETH for GEX. For 120 ETH it gets 56 ETH
> (5) GEXBot then uses 50 GEX to cover the loan. The remaining 6 GEX
> is transferred to the seller
>
>
> As we see from the example above, the seller deposited 120 ETH, got 50
> GEX immediately, and then 6 GEX as an adjustment at time 0:00.
> The algorithm above is good for the seller, since the seller gets most of
> GEX immediately, and ultimately gets the fair value in GEX.
> GEXBot can incur a loss in the infrequent case where the rate drops more
> than 20% day to day.
>
>
> Lets consider an example the where the rate drops so much that,
> GEXBot only gets 49 GEX at time 0:00. It is not enough to cover the previous
> loan of 50 GEX, so the seller owes to GEXBot 1 GEX.
> GEXBot will note this 1 GEX as an outstanding loan, and charge this 1
> GEX from the seller the next time the seller comes to GEXBot to exchange
> assets.
>
>
> The seller may decide to never come back to GEXBot. In this case,
> GEXBot loses 1 GEX, and the seller loses its reputation in the network and
> its ability to easily exchange GEX for ETH.
> Since the purpose of GEXBot is to provide GEX liquidity to users and
> providers for service payments and not for market speculation, GEXBot will
> impose exchange limits, that will depend on the reputation of the seller, as
> well as on the amount of the service provided or used by the seller in the past.
> The exchange limits will limit the losses that GEXBot can incur.
>
>
> Yet, there will be cases where sellers will never come back and GEXBot will lose
> reserves. To compensate for this average loss, GEXBot will charge transaction
> fees on each transaction. The fees will be proportional of to the size of the
> order multiplied by the fee rate. The fee rate starts with zero and goes up as
> GEXBot starts depleting its reserves.

---

**nisdas** (2017-12-26):

All the solutions do require extremely high amount of capital in order to bring create a market where a token can be effectively shorted. If you are to create a more efficient market you could create a smart contract that would function as a crypto broker.

In the stock market, if you want to short the stock of any company , you usually borrow the stock from the broker for a fixed interest rate, sell it , then buy it back when you want to cover your short. With a smart contract, this could be achieved also. On one side you have dedicated parties holding long positions, their investment horizon is of more than 6 months , so they plan to hold the token long term rather than simply speculate on it. They could be incentivized to lend these tokens out to other parties to short at a certain interest rate.

The parties who want to short the token would have to deposit twice the total value of the tokens in ether plus the interest payable on borrowing those tokens to the smart contract. So the smart contract now is a repository for their ether. If the tokens go to zero, then the party cannot get their ether back.One way to get a constant stream of token prices would be whenever you call a function on that contract, the contract will get the token price through oracle and automatically adjust what the value of your position in ether.

x is the amount of ether deposited

0.5x is the initial value of the tokens in ether

y is the value of one token in ether

\delta is the interest payable on borrowing the tokens

The total number of tokens you short would be

z =\frac x{2y}

So right now the contract holds x ether and you have shorted z tokens.

What happens if the value of the token goes up ?

if the value of the token goes up by 50%, then right now you would have a loss of 0.25x +\delta. So at this point the shorting party has two choices either he/she can cover their short by buying back the tokens and then exchanging those tokens with the smart contract for around 0.25x - \delta(with the borrowing fee subtracted), or if they believe that the price appreciation is only temporary and it will go down in the future, they maintain their short position.

So if the price rises further , then there will come a point where the shorting party will be in the red for about 0.5x(this includes the borrwing fee). At this point the smart contract will have to close the position and would regard the shorting party as insolvent as the value of tokens has risen above their deposited margin. Now the smart contract would interact with another contract(etherdelta or something similar) and try to buy back those tokens. Before x ether could buy you 2z tokens now it will only get you z tokens.  Which is incidentally also the amount of tokens you initially lent out .

What happens if the price of the token goes down ?

If the price drops by about 50% , the shorting party has an unrealized gain of about 0.25x -\delta, if they decide to close their position and pocket the profit then they could return the z tokens to the smart contract and get back x-\delta eth. Their net profit would roughly be about 0.25x -\delta.

If they decide to hold their short position and the token loses all its value, then they could exchange z tokens with the smart contract and get back x-\delta eth. Their net profit would roughly be 0.5x - \delta

This mechanism is one way that I see as enabling parties to build up short positions in the market, which would allow for a much more efficient price discovery of the value of the tokens. The limitations of something like this would be that the contract would constantly be need to be fed the price of the tokens, so someone would have to be constantly calling functions on the contract so that the contract can constantly update short positions of all the parties using the contract. I imagine this would be very expensive due to the amount of gas required. Also this would be limited to only ERC-20 tokens

---

**kladkogex** (2017-12-26):

I think for shorting the easiest thing to do is to have market for covered call options. Some people would write call options and some people would buy call options.

To write a call option to buy 1 token XYZ at the price of 100 ETH, you would deposit 100 ETH into a smart contract, this would create an option token OPT that would be linked to this deposit.  If the option is callable for say 6 months, then anytime during these 6 months you could present the option token OPT and 1 XYZ to the contract and get 100 ETH back.

Options are easier to do than shorts, since shorts must include a mechanism for a forced cover, automatically executable if the price goes up very high (something that is called short squeeze)  - this essentially requires an external oracle. The forced cover mechanism is needed because shorts can potentially lead to unbounded losses… For options losses of each party are bounded.

---

**MicahZoltu** (2017-12-26):

Augur (and other prediction markets) markets are effectively bounded futures which means you can open a leveraged short or long position.  However, as futures they also have time expiry.

While I would love to be able to put my money where my mouth is for all of these terrible tokens/alt-coins, my predictions are all long term, not short term.  While I believe people will *eventually* realize that coin/token ABC is worthless, I also recognize that current crypto markets are completely irrational and even if I had the option to do so, I would not want to open a short position that could be called within a short period of time.

What I want is the ability to say, “In 5 years, this token is more likely to be 0 than it is to be double what it is today” or something similar.  If it goes above 2x between now and then, I don’t want my position to be closed on me (like with American options) and I don’t want to have to worry about unbounded losses to keep the position open.

One solution to this would be multi-year European style LEAP options.  However, what I would *really* like to see is some sort of inverse financial derivative where as the value of the asset approaches infinity, my losses for holding a short position approach 0 but never reach 0.  Meanwhile, as the asset approaches 0, my gains approach infinity (though I would be content with them approaching some large number).  I haven’t spent enough time thinking about how such an asset would work, but it *feels* like it should be possible to inverse.  With such an asset I can then hold it long-term, without a specific date in mind, merely knowing that it will eventually get wiped out.

---

**nisdas** (2017-12-27):

Yeah an issue with shorting would be the potential for unbounded losses and the smart contract requiring an external oracle.  An options smart contract might be better way to short a token.

I don’t think it’s possible for any financial derivative to offer extremely large returns when the underlying asset has a value approaching to zero without it being extremely levered. Having any derivative offering that sort of return would make it very volatile and prone to significant counterparty risk. Someone would have to eventually provide that extremely large payout, which wouldn’t make sense from their point of view, as their upside is limited while their potential downside is close to infinity.

---

**jacob-eliosoff** (2017-12-27):

I’ve argued before that crypto markets would be more efficient (and prices accurately lower) if there were shorting mechanisms with symmetric rather than asymmetric risks.  Specifically, I’m a fan of binary options.  See eg this [Twitter thread](https://twitter.com/JaEsf/status/935603595302535168): “I wish BTC had ‘over/under’ binary betting like this (cf US football).  I predict prices would be much lower, more stable - & more accurate.”

---

**superphil0** (2017-12-27):

I don’t understand a lot about this, but to me it seems very much that the single biggest reason why not much more shorting is available is simply because of liquidity.

Especially for shorting you need a reliable source of liquidity over a longer period of time.

The problem with all the tokens of ICOs is as you can see with most again: liquidity.

People tend to hold on to tokens for the lack of liquidity.

So if we agree that shorting requires more liquidity than normal trading, but many tokens are even too illiquid to trade, it is quite understandable why there is not shorting opportunities.

Think of Bitcoin’s liquidity, at a market cap of 200$ billion we got now roughly 10$ bil / day trading volume.

That is around 5%.

If we now take your example of [color.com](http://color.com)

if they managed to raise 41$ mil lets put there evaluation at 150$ mil

5% of that is 7.5 mil

So if we assumed their shares to be liquid (which were actually not) and the same ratio of market cap to volume who would take on shorts in such an assets? There is simply not enough money to be made for the intermediaries to put up such a shorting opportunity. I don’t know what the overhead cost for that might be, but I am sure it is considerable.

All in all decentralized system could lower the technical overhead costs by a factor of 10 or more, however the regulatory burden on such trades might still be too high

---

**jacob-eliosoff** (2017-12-27):

See also the follow-up thread at https://twitter.com/JaEsf/status/946114726026555393: “Another way to keep long & short risks symmetric is ‘log-space’ bets: bet $10 → make $10 when BTC doubles, lose $10 when it halves.”

---

**nootropicat** (2017-12-28):

It’s not going to work because market caps in crypto are universally fake.

If I own ~100% of a shit token the market price doesn’t really exist - market cap could be in the trillions, all it takes is some wash trading.

Some fool is likely to tag along and buy some for a ridiculous price.

If a token is lost it shouldn’t be counted in the market cap - yet it is. If you knew that only 1BTC is movable - all other coins provably lost - would you short BTC at $1 billion?

It’s even worse because the true supply is impossible to know and can only be estimated.

I would argue that shorting is not a cause but a result of liquidity - liquid markets make shorting possible which is why efficient markets are easier to short.

Shorting illiquid/manipulated tokens would only make price manipulation more profitable by forcing liquidations via a [short squezze](http://www.nytimes.com/2008/10/30/business/worldbusiness/30iht-norris31.1.17372644.html?pagewanted=all).

What could help in general is making markets more liquid, but that’s only possible to solve if illiquidity is caused by regulatory and technical barriers.

> as having observed in 1977 that efficiency requires short sales, and either Shiller or Miller observes that houses can’t be shorted.

That’s not true, a nonrecourse debt that uses house as collateral is a form of shorting.

---

**varna** (2017-12-28):

IMO availability of shorting will not reduce crypto price volatility towards fiat neither will cause better price discovery for hyped coins.

Seemingly smaller price volatility of major stocks compared to major cryptos is due more to regulatory “acceptable” price guidance or analysis, to stock exchanges price curbs, to company or interested parties buy/sell transactions, to the availability of funds - ETFs, pension, hedge, etc. Stock derivatives are somewhat neutral to the underlying stock price performance longer term.

I understand that there is an acute issue with many hyped up prices of dubious tokens (or even with some long established ones) that brand as cash, blockchain, crypto or similar - as their inevitable flop could cause alienation of investors to other credible projects. That is worrying on one side as fiat means exchange for digital tokens at exuberant price levels that reflect purely rosy expectations.

There are in my mind three solutions:

- leave current state of affairs as it is - so that many new projects are born and financed but leave enthusiasts get burned in dubious or ponzi tokens
- enhance price discovery and price drivers and enhance learning for the public
- invite regulation either self or governmental

Personally I do not think digital assets living on a decentralized and possibly secure and scalable platform should seek solutions or improvements looking back at examples of the existing financial or capital markets environment. So - regulations, options, shorting, futures, yields, IRRs, VARs, etc.  - are very important to understand but they should be irrelevant in the long term as long as cost effective salability of distributed digital assets (including digital means of exchange) can be achieved.

There is also a perception issue - some of my younger finance colleagues are saying “why are all media and people saying that bitcoin appreciates against USD - as in reality the USD decreased in value against one bitcoin?”

This caught me thinking - many people believe blockchain “currencies” or new tokens are somewhat predefined in number or purpose against an ever floating unknown number of fiat “legal” currencies …

I wonder if that marketed hard coded maximum number or algorithmic purpose of the crypto (which in reality is not a given eternal state) is not creating a wishful depreciation of the fiat given the existing lax money supply and zirp policy in fiat?

---

**yhirai** (2018-01-02):

Covered calls seem already implementable.  Do you want to draft an ERC or shall I?

---

**kladkogex** (2018-01-02):

Yoichi - thank you - I will be happy to draft an ERC.

---

**denett** (2018-01-03):

Writing covered calls still result in a positive delta, since you have to buy the token first and you only sell the upside.

I think a put option is also possible in a contract and that will result in a negative delta for the buyer.

The writer of a put option with strike price S, will lock S ether in the contract. The buyer has the right to swap the ether for a token. If the ether is not swapped at expiration, the writer can withdraw its ether.

This works great for betting on a price fall, since in that case the buyer can buy the coin cheap and sell it for the strike price of the option.

---

**h00701350103** (2018-01-07):

Yeah, prediction markets was my instant reaction upon reading the original post. With those you can not only bet on price at a given time (pegged against fiat, crypto, stablecoins, or % of market cap), but you can also bet on technicals (“network will process X transactions at time Y”, “token will have implemented feature X by time Y”, “core team will consist of X people at time Y” (all these will require detailed rundowns to specify what’s what ofc)).

It will be perfectly possible to open a market with “in 5 years, token will be closer to 0$ than to 2X$” and then you can buy shares in a high-percentage position." - and then you can settle your position before the time limit by selling your shares if you want to.

There’s still no direct way of shorting the real market price, so bad investors might simply ignore the prediction markets buy at irrational prices and there will be no way to arbitrage without other shorting tools (I think?), but this will give an on-chain price discovery tool that can be used for shorting, and if it becomes popular and notable it will very likely affect the market price.

for longer discussion, se e.g. https://medium.com/@death.taxes.crypto/prediction-markets-and-the-future-of-crypto-self-regulation-b320406e433a

---

**bpolania** (2018-01-24):

The fact that short selling makes markets more efficient is pretty well substantiated in academic literature, and there are many reasons:

- Short-selling activities are considerably informative about future stock returns when there is a higher likelihood of private information in stocks. Short-sellers also bring considerable additional information to the market, especially for smaller stocks, that is not fully captured by contemporaneous insider trading. Overall, it seems that on average short sellers bring informational efficiency to the market rather than destabilize them (Purnanandam and Seyhun).
- Then in a similar fashion, shorting demand is an important predictor of future stock returns especially in environments with less public information flow, this suggests that the shorting market is an important mechanism for private information revelation (Malloy, Diether and Cohen).
- Another study focusing on price efficiency shows that lending supply has a significant impact on efficiency: stocks with higher short-sale constraints, measured by low lending supply, have lower price efficiency, and   that relaxing short-sales constraints is not associated with an increase in either price instability or occurrence of extreme negative returns (Saffi and Sigurdsson).
- and finally a very interesting paper (Asquith, Pathak and Ritter) found that short-selling constrained stocks significantly underperformed during 1988-2002.

I think a possible semi-conservative approach is the creation of something similar to the 130/30 funds where the  130% (long) exposure is to ETH and and the 30% to short positions on any ETH based token, this will have access to big investors and then some of those funds can be “tokenized” similarly to ETFs, so those tokens will track the value of the 130/30 fund and will be tradeable in token exchanges where smaller investors can have access to them. The former (130/30 fund) can be a simple smart contract that will hold both ETH and other tokens, the latter could be a standard ERC20/ERC223 token.

I also recommend to read the 1977 paper by Edward M. Miller called *Risk, Uncertainty, and Divergence of Opinion* that I consider to be kind of seminal on this subject, exploring some of the implications of markets with restricted short-selling.

---

**themandalore** (2018-01-24):

Hey guys, I run the Decentralized Derivatives Association (DDA) but I’ll layout the current landscaped.  My company is seeking to do fully decentralized derivative contracts on Ethereum (https://github.com/DecentralizedDerivatives/DRCT_standard ), which to simplify, parties place money in a smart contract and then the contract pays out based on the change in an API that the contract references.  The next form you is the traditional exchange doing futures contracts.  And lastly is the protocol based shorting (like dydx) which allow for you to loan your token as a short.

Any of the above can work to keep prices in line, but to be honest I don’t think any will work.  Crypto as a whole has very little utility at the moment and the subjective/ speculative valuations of every coin (ETH included) are efficient given the current bull rush incoming investors.  It has nothing to do with efficiency of the market, but rather just irrational exuberance of the incoming crowds seeing riches in every sub-dollar token.  I think if we take anything from the economists it’s that the boom-bust cycle is necessary to shake out the losers and keep the good tokens honest.

---

**bpolania** (2018-01-30):

I wrote a short [article](https://medium.com/@Wholeonomics/cryptomarkets-maturity-and-price-volatility-12575125e919) on volatility and information flow through crypto-markets that you may find relevant on this point.

---

**rkapurbh** (2018-02-07):

Shorting constraints exist because in theory there is infinite downside and bounded upside. On top of general loss aversion, fewer people tend to express contrarian sentiments towards the market.

One way to normalize the notion of taking a contrarian position is to design “friendlier” instruments much like Inverse ETFs. For example, InverseETH - a Basecoin-style peg that follows the equal and opposite movements to ETH could largely simplify the experience of taking such a contrarian bet.

An inverse would (in theory) avoid the use of collateral and the potential indebtedness from shorting. Though, in practice, building such an Inverse Instrument using a Basecoin-like system  may require frequent rebalancing and/or lead to price mismatches due to the working of the Basecoin system itself. Any thoughts on how to build a simple Inverse ETH instrument?

---

**bpolania** (2018-02-08):

Inverse ETFs are usually constructed from other short-selling instruments, so the core issue would remain there: there are not enough short-selling mechanisms.

Regarding the avoidance of collateral, that’ll apply to the reverse fund buyers, but it will remain an issue for those instrument in the fund. In order to be able to bet on the losses of a crypto without using collateral you’d need to find a mechanism that doesn’t require lending/credit, and by definition short positions require borrowing.


*(7 more replies not shown)*
