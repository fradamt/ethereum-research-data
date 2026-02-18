---
source: ethresearch
topic_id: 20419
title: Pricing Ethereum Blocks with Vol Markets with Implications for Preconfirmations
author: lepsoe
date: "2024-09-12"
category: Economics
tags: []
url: https://ethresear.ch/t/pricing-ethereum-blocks-with-vol-markets-with-implications-for-preconfirmations/20419
views: 999
likes: 6
posts_count: 1
---

# Pricing Ethereum Blocks with Vol Markets with Implications for Preconfirmations

# Ethereum Block Pricing in the Context of Vol Markets

*by [Lepsoe](https://x.com/lepsoe) ([@ETHGas](https://www.ethgas.com/))*

*With thanks to the [Commit Boost](https://x.com/Commit_Boost), and [Titan](https://x.com/titanbuilderxyz) teams for making Preconfs a near-term open and scalable possibility, and [Drew](https://x.com/DrewVdW) for prompting the market sizing exploration*

## TL;DR

- With the forthcoming gas markets and the ability to buy Entire Blocks, we look at how to price these taking into account prevailing market Volatility, Token prices, Transaction Fees, and Liquidity
- Treating the Blockchain/Network as a financial instrument, Block purchases are effectively Options on this network. If one can buy 5 blocks of Ethereum (e.g. 1 minute), one can observe prices in CEXs over this time with an option to monetize the difference between CEX and DEX prices (e.g. latency arb trade)
- Buying a block is analogous to buying a Straddle on the Network, and all its DEXs. Taking into account transaction fees, liquidity and slippage, however, this is more analogous to a Strangle.
- We then employ an arbitrage trade that involves Shorting European Strangles in CEX (e.g. Deribit, Binance, OKX), and Buying Blocks or Preconfs of Ethereum. This implies a minimum or floor price for one or many consecutive blocks
- We can then draw a direct, real-time connection between the current implied Vol for ETH, BTC, SOL, etc… and Preconfs prices
- We conclude that if ETH Vol is 75%, and transaction fees are 0.10%, then buying 5 consecutive blocks of Ethereum should be no lower than 6.9 Gwei
- Historically, very short-end vol appears to rise dramatically higher than 75% with a Mean of 273%, although the median remains at 75% over the last 2 years
- With the current PBS flow and prior to blockspace commitment contracts, this strategy is possible but limited to only the current/next block. With the ability to buy two or more blocks, it becomes easier to execute on and thus price Preconfs with confidence
- Connecting the two markets, Vol and Macro traders may therefore trade the Preconf markets, in some cases, with little care as to how these instruments are used or valued with respect to the underlying physical gas markets themselves (e.g. typical orderflow, MEV)
- The terms Preconfs and Blocks are used interchangeable for readability

## Background

How much are Ethereum’s blocks worth?

Arbitrage, often referred to as ‘arb’ trading, typically involves quantitative strategies that exploit pricing discrepancies or minor imbalances between closely related financial instruments. These instruments may be similar in nature or expected to exhibit similar behaviors over time - they can be priced with models or priced using dynamic replication (such as options replicated through dynamic hedging).

One such arb is statistical arbitrage (‘stat arb’) that frequently employs mean reversion models to capitalize on short-term pricing inefficiencies. Another one is latency arbitrage that takes advantage of minute price variations across different trading venues. In the cryptocurrency, a common form of arbitrage is known as CEX/DEX arb, a type of latency arbitrage where decentralized exchanges (DEXs) respond more slowly to market changes than centralized exchanges (CEXs), largely due to differing block or settlement times. In such scenarios, traders engage in relative-value or pairs trading between centralized exchanges (such as Binance and OKX) and decentralized exchanges (such as Uniswap and Curve).

### The Network As a Financial Instrument

In this article, we look to delineate, and quantify such an arbitrage trade between two seemingly different instruments: the Vol markets on CEX vs the Ethereum Blockchain itself (i.e. the Network, not DEXs).

The purpose of this article is to introduce a closed-form solution to price a floor price for Ethereum Blocks drawing a direct relationship between Vol markets and the minimum price one should pay for Ethereum Blocks. More specifically, we will look at the effect of selling Strangles on ETH (and other tokens) in CEX, while buying Blockspace Commitments (or Preconfirmations) on Ethereum.

While this type of relationship may exist with limited effect today for 12 seconds, the burgeoning space of preconfirmations and validator commitments will enable this to exist for much longer periods turning what may be a theoretical exercise today into a practical exercise tomorrow.

Through this exercise, we position the Blockchain or Network itself as a financial instrument that can be used for macro hedging or relative value trading purposes.

### What is a Strangle?

The building blocks of options markets or ‘Vol’ markets are ‘vanilla’ options known as calls and puts. Combining such vanilla options together at the same strike produces a ‘V-shaped’ payoff known as a ‘Straddle’. A Straddle will always have a positive intrinsic value or payoff enabling the buyer to monetize any movement of the underlying instrument.

[![image](https://ethresear.ch/uploads/default/optimized/3X/7/1/71515733c74792ef64bb5afa1456f44c8a078678_2_690x399.png)image1234×714 59.7 KB](https://ethresear.ch/uploads/default/71515733c74792ef64bb5afa1456f44c8a078678)

*Figure 1: Straddles vs Strangles*

When the strikes are apart from one another, in the above example by a distance of ‘z’, they are called a ‘Strangle’. For example:

- A Put and Call both with strikes of 100 (i.e. X) would collectively be called a Straddle
- A Put and Call with strikes of 90 (i.e. X - z) and 110 (i.e. X + z) respectively, would collectively be a Strangle

Strangles payoff or have an intrinsic value only when the underlying spot price has moved by a sufficient distance, in this case ‘z’.

### What Are Preconfirmations?

Preconfirmations and Blockspace Commitments are part of a new field of Ethereum Research and Development focused on giving Validators (called Proposers, i.e. those that Propose the next epoch of blocks) expanded abilities to sell blockspace in a way that gives them more flexibility than they are currently afforded within the current PBS (Proposer-Builder- Separation) flow.

Such an initiative is intended broadly to bring more control in-protocol (as opposed to externally with Block Builders), and streamline scaling technology for the new field of Based Rollups.

While there are different forms of Blockspace Commitments, the general form has Proposers providing commitments to buyers - typically Searchers, Market Makers, Block Builders, and others looking to use the blockspace for transactions, among other purposes. For example, there are:

- Inclusion Preconfirmations: Where Proposers issue guarantees to include transactions within a specified block, anywhere in the block
- Execution Preconfirmations: Where Proposers issue guarantees to include transactions within a specific block, with a specific state or result
- Whole Block Sales which may be called Entire Blocks or Execution Tickets: Where Proposers sell their block en masse to an intermediary who then engages in some form of pseudo block building consisting perhaps of a mix of their own trades, Inclusion Preconfirmations, Execution Preconfirmations, private order flow, and public order flow.

For the purposes of this paper, we will be referring to Whole Block Sales by Proposers, but may refer to them generically as Preconfirmations or Preconfs for ease of reading and consistency with some current nomenclature.

### Current Preconf and Blockspace Pricing

The value of Ethereum blocks are often associated with the Maximum Extractable Value (MEV), that is, the largest amount of value that one could extract or monetize within a 12 second period. This may include a mix of the public’s willingness to pay for transactions (financial and non-financial), private order flow, as well as other MEV trades including sandwich attacks, atomic arbitrage, CEX/DEX arb, or other.

Extending into the Multi-block MEV (MMEV) or Consecutive Block valuation, MMEV valuation is often performed in the context of TWAP oracle manipulation attacks producing forced liquidations by price manipulation. While there is an intersection between longer-term CEX/DEX arb captured in single-block pricing discussions vs the relative value vol markets, we prefer the simplicity and forward-looking nature of the vol markets for the purpose of our pricing exercise.

Putting this together, there are multiple ways to value a single or multiple set of Ethereum blocks. From our analysis, we present a floor price for Ethereum blocks driven by non-arbitrage pricing and the Vol markets in CeFi. From this floor price one may additionally then consider encompassing other forms of value capture to arrive at a true mid-market price of an Ethereum Block.

## The Trade

### Historical Background

Buying a block, or multiple blocks of Ethereum enables one more control over order execution and states. Simply, if it were possible to buy 12.8 minutes of Ethereum (i.e. 64 blocks or two epoch) one could watch prices as they move in CEX during this time, and at any time during this 12 minute period, one could put on a relative value trade capturing the difference in prices between the CEXs and DEXs. If, for example, prices rose 5% in CEX during this time, one could sell assets in CEX, and buy those same assets in DEX (where the prices haven’t moved) earning 5% in the process. While this may not be currently feasible, it is the starting point for discussion.

Historically, we can look at these dynamics measuring the maximum price movements over 12 secs, 1 min, or more. We can then take into account the liquidity on DEXs and calculate a historical breakeven between the profitability of such transactions with the number of blocks for a given period. For more on this see this article: [| Greenfield](https://greenfield.xyz/2024/09/10/statistical-arbitrage-on-amms-and-block-building-on-ethereum-part-1/)

While possible to calculate, we’re more interested in looking forward, not backward. Enter the Vol markets.

### Vol Markets & Strangles

To execute the trade above, one must cross bid-offer, paying transaction fees on both the CEX and DEX side as well as ‘time’ the market accordingly to maximize the arbitrage. One furthermore has to factor in the liquidity or depth of the market. That is, for the strategy to pay off, prices need to move beyond a certain minimum threshold or in our case, a Strike price different from the current Spot price.

Let us assume that the “sum of transaction fees and slippage between CEX/DEX” - our ‘threshold’ or Strike is 0.10%. If we have the Vol of the asset, and a time horizon, we can now price this using Black-Scholes as a simple Strangle.

Assume the following:

- Trade Size: $10mm
- Token: ETH
- Spot Price: 100 || to keep things simple
- Interest Rates: 4.00%
- Dividend Yield: 0.00%
- Vol: 75%
- Expiry: 32 Blocks (12.8mins)
- Fees: 0.10 as accounted for in the following Strikes:

Strike 1: 100 + 0.10 = 100.10 - for the Call Option
- Strike 2: 100 - 0.10 = 99.90 - for the Put Option

Result:

- Call Price: 0.0620%
- Put Price: 0.0619%
- Strangle Price: 0.0620% + 0.0619% = 0.1239%
- Price in USD Terms: $12,388

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/a/ca508d8bddc9793de7b6326ed95552f760925a2e_2_690x376.jpeg)image1878×1024 64.8 KB](https://ethresear.ch/uploads/default/ca508d8bddc9793de7b6326ed95552f760925a2e)

*Figure 2: A Strangle on Ethereum and all its DEXs combined*

Per the diagram above, if one could trade this Strangle in CEX for $12,388 (see [spreadsheet](https://docs.google.com/spreadsheets/d/1wwhe-O8L0eG72Mb0PJGLhlDi1Fxe1E0CSzpX0sAaz2U/edit?usp=sharing) for calculations), one should equivalently be able to trade Preconfs on Ethereum for the same price. If the underlying spot market in CEX moves up or down more than 0.10, whilst DEX prices stay the same, then these options become in-the-money..

Putting CEX and DEX together below, one would sell the Strangle on ETH in CEX but buy Preconfs on Ethereum giving them an almost identical payoff where z represents both the expected transaction fees and the distance to the Strike price for pricing purposes:

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/b/9bf362500aa612b87a9254ea96544495005030a3_2_422x500.jpeg)image1784×2110 155 KB](https://ethresear.ch/uploads/default/9bf362500aa612b87a9254ea96544495005030a3)

*Figure 3: Short CEX Strangle + Long Ethereum Preconf*

If the Vol markets imply a price of $12,399 for 12.8mins (i.e. 32 blocks) then this is the amount (less one dollar) that one would be willing to pay to buy up 32 consecutive blocks (i.e. 12.8mins) of Ethereum. Given the assumptions above, the expected value is always positive and we thus have a closed-form solution to Floor pricing for Preconfs.

The arbitrage carries two scenarios:

- Prices are between 99.90 and 100.10: Both the Strangle and Preconf Expire ‘out-of-the-money’ without any cash settlement
- Prices are beyond 99.90 and 100.10 with options expiring ‘in-the-money’. The Trader incurs a loss on the CEX Strangle, but then monetizes the gain in DeFi by entering into an off-market spot trade (with respect to CEX) crystallizing the in-the-money value of the option

Vol Traders do this 1000s of times a day, with automated systems and razor-sharp precision. Trading Vol vs Preconfs opens up an entirely new relative-value asset class for them to potentially buy vol or gamma much more cheaply.

### Scenario Analyses and Sensitivities

Turning to Gas Market terminology, the price of $12,399 translates into a Gwei price of 165 Gwei ($12,399 / 2,500 * 1e9 / 30e6) assuming the ETH price is 2,500 in this example. Using the Strangle pricing method, we can then infer from the ETH Vol markets (75% vol in this case) the price of 1 block, all the way up to 32 consecutive blocks or slots as follows:

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/7/57defb97d1f6360692afa2c53920481469468872_2_690x285.png)image1832×758 73.5 KB](https://ethresear.ch/uploads/default/57defb97d1f6360692afa2c53920481469468872)

*Figure 4: Price for N-Consecutive Blocks of Ethereum*

Comparing the difference in Strangle prices between a period of N(0,1), to a Strangle with a period of length N(0,2), we can then price the Strangle for Slot 2 N(1,2), as follows for the entire curve. We can furthermore take the ‘average preconf price’ for N slots.

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/d/cd5b4a440fe65ad5649f789572044f132c3a152f_2_690x379.jpeg)image1860×1022 97.4 KB](https://ethresear.ch/uploads/default/cd5b4a440fe65ad5649f789572044f132c3a152f)

*Figure 5: Slot N Price vs Avg Price for N-Slots*

The following table highlights the fees in Gwei that validators would get paid for specific blocks/slots with 5.16 Gwei as the average. This may be compared, for example, to historical Priority Fees that one receives via MEV-Boost where 4.04 Gwei is the average:

[![image](https://ethresear.ch/uploads/default/optimized/3X/c/3/c3625c9aef9793341f69e2c496ba4151b8ba8a06_2_690x369.jpeg)image1912×1024 192 KB](https://ethresear.ch/uploads/default/c3625c9aef9793341f69e2c496ba4151b8ba8a06)

*Figure 6: Historical Priority Fees from MEV-Boost. Priority Fees from 24 Jan 2024 to 9 Sep 2024.*

#### Transaction Costs Impact on Pricing

The difference between the Strike Prices and Spot Price or transaction costs above are taken to be uniform at 0.10%. In practice however, transaction costs encompass i) actual transaction fees, and ii) liquidity/slippage in execution. Below, we see that Transaction Costs have a significant impact on Preconf pricing especially where there is a shorter time-to-maturity.

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/b/bb067308cb50d9cac678fffc4c4df056a7b697c3_2_690x395.jpeg)image1970×1130 146 KB](https://ethresear.ch/uploads/default/bb067308cb50d9cac678fffc4c4df056a7b697c3)

*Figure 7: Preconf Pricing for varying levels of Transaction Costs*

#### Volatility Impact on Pricing

Finally, as the CEX leg of the trade uses Volatility as the primary market input, we now consider the impact that volatility has on Preconf pricing with Vega close to 0.1 Gwei at the 4th slot, and ~0.06 Gwei at the 32nd slot. That is, **at Slot 4, a 10% change in Vol is impacts Block prices by 1 Gwei.**

[![image](https://ethresear.ch/uploads/default/optimized/3X/6/c/6c7b2d7c8762d69423e0fc605cd9d64cd9f85dbc_2_690x406.jpeg)image1764×1038 125 KB](https://ethresear.ch/uploads/default/6c7b2d7c8762d69423e0fc605cd9d64cd9f85dbc)

*Figure 8: Preconf Prices for Different levels of Volatility*

## Refinements & Market Sizing

For market sizing, we look exclusively at the CEX Strangle vs Preconf on Ethereum L1.

### Consecutive Blocks

The exercise considers buying multiple blocks, potentially up to 32 or 64 blocks depending on the lookahead window. In reality however, this is extremely difficult due to the diversity of Validators.

There is a subset of Validators that, for ideological reasons or other, do not adopt MEV-Boost, and would be unlikely to adopt a framework that captures more MEV. In economic terms, they are not rational. It could be that they do not ‘believe’ in MEV, or they simply could be an at-home staker that hasn’t upgraded to MEV-Boost. Either way, these Vanilla or self-built blocks account for slightly less than 10% (and decreasing) of blocks (see realtime with ETHGas’ [GasExplorer](http://www.ethgas.com), and research with [Blocknative](https://www.blocknative.com/blog/how-self-built-blocks-unintentionally-introduce-base-fee-volatility)).

Let’s assume the other 90% are rational (i.e. they are economically motivated) and that they are somehow able to coordinate among one another through some unifying medium for the sale of consecutive blocks. In this case, we can then model the frequency of single vs consecutive blocks where about half of the time there are less than 7 consecutive blocks, and the other half have somewhere between 8 and 32 consecutive blocks.

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/9/a96d126f31fbaa6afded0e3cdd01172eceba7b03_2_690x401.png)image1720×1000 82.9 KB](https://ethresear.ch/uploads/default/a96d126f31fbaa6afded0e3cdd01172eceba7b03)

*Figure 9: Frequency of Consecutive Blocks*

### Historical Volatility Analysis

Looking at almost 2 years of trades from 10 Sep 2022 to 10 Sep 2024 on Deribit, we uncover some fascinating dynamics for short-dated transactions.

#### 1 Hour to Expiry

For those transactions with less than 1 hour to expiry, we find approx 13,500 trades over this period, a mean Vol of 107.52%, a Median of 63%, and 75th Percentile as 102%. Note that Deribit’s Vols are capped at 999 suggesting that the mean may be higher than that which is indicated.

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/f/af0a574ea2876081224b6e7b6ecd012ff163221a_2_655x500.jpeg)image1654×1262 68.8 KB](https://ethresear.ch/uploads/default/af0a574ea2876081224b6e7b6ecd012ff163221a)

*Figure 10: Distribution of Implied Vol on ETH Options with less than 1 Hour to Expiry*

#### 12 Mins to Expiry

For transactions with less than 12 mins to expiry (or approx 64 blocks), we find almost 1,400 trades over this period with a mean of 273% Vol, median of 75% Vol, and 75th Percentile as 395% Vol.

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/e/deede16e86a88239a6ecc6e13c99cd93778fa614_2_662x500.jpeg)image1548×1168 60.9 KB](https://ethresear.ch/uploads/default/deede16e86a88239a6ecc6e13c99cd93778fa614)

*Figure: 11: Distribution of Implied Vol on ETH Options 12 Mins to Expiry*

#### <12 Minutes to Expiry

Across these 1,400 trades, we then split them into their 1-minute buckets to view distributions across times more closely associated with Preconf Block timeframes.

[![image](https://ethresear.ch/uploads/default/optimized/3X/1/4/14686bf48d5c989a80356631a03434fa70bca82f_2_690x493.jpeg)image1508×1078 90.6 KB](https://ethresear.ch/uploads/default/14686bf48d5c989a80356631a03434fa70bca82f)

*Figure 13: Distribution of ETH Implied Vol for the last 12 mins to Expiry*

The Vol numbers are far larger than we expected warranting further research into this area. While liquidity will need to be analyzed, we have provided some Preconf-implied Pricing given Vols of a much higher magnitude for convenience:

[![image](https://ethresear.ch/uploads/default/optimized/3X/d/f/df84a11dc4575ba83d2836af936004045965d8a4_2_690x411.jpeg)image1840×1098 162 KB](https://ethresear.ch/uploads/default/df84a11dc4575ba83d2836af936004045965d8a4)

*Figure 14: Preconf Implied Prices for very high levels of Volatility*

#### Vol Smile

As you may recall, we’re not looking for at-the-money Vol (used for a Straddle) but rather for Vol as it may relate to Strangles. The Vol for out-of-the-money options is almost always higher than at-the-money options. To this effect, we have provided a heat map below providing some color on the smile accordingly.

*Figure 15: Vol Smile for 0 to 12 minutes*

### Market Sizing

Bringing the above information together, we decide to take the combined Vol set and use that as a proxy for Strangle pricing. To account for illiquidity, we then provide different scenarios at lower volatilities assuming that as we sell more Strangles, the Vol would decrease accordingly.

We can now size the market considering:

- The historical mean Vol: 275%
- The frequency of Consecutive Blocks: Per the above
- The implied preconf Floor pricing as a function of Vol: Black-Scholes
- And, making some adjustment for Liquidity: Reducing Vol by up to 200%

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/7/b7472612ce4624f0df42973ca84c9800c70d6792_2_690x369.jpeg)image2004×1074 151 KB](https://ethresear.ch/uploads/default/b7472612ce4624f0df42973ca84c9800c70d6792)

*Figure 16: Preconf Pricing Based on Frequency of Consecutive Blocks, Historical Volatility and adjusted for Liquidity*

The annual market size for Blockspace could equal approximately 419,938 ETH per year historically (~$1bln equiv) and with approx 33 million Staked ETH, this amounts to 5.33 Gwei per block or an extra 1.25% in Validator Yields as a floor above Base Fees.

| Vol | 275% Vol | 225% Vol | 175% Vol | 125% Vol | 75% Vol |
| --- | --- | --- | --- | --- | --- |
| Gwei Total | 282,615 | 218,322 | 155,081 | 93,997 | 38,350 |
| Gwei per Block | 39.25 | 30.32 | 21.54 | 13.06 | 5.33 |
| ETH Total Fees | 3,094,638 | 2,390,631 | 1,698,137 | 1,029,270 | 419,938 |
| Increase to APYs | 9.10% | 7.03% | 4.99% | 3.03% | 1.24% |
| $ Total Fees | 7,736,594,273 | 5,976,577,160 | 4,245,342,208 | 2,573,176,209 | 1,049,844,310 |

## Other Considerations

### Liquidity

On the CEX side, we would like to assume there is infinite liquidity but this is not realistic. In the example immediately above, we bump the Vol downward to adjust for this but in reality, we would need more order book information. Looking forward, this market could also be illiquid because there was never another market to trade it against, e.g. Preconfs. We furthermore would need to run the analysis considering tokens other than ETH.

Everyday there is a 12-minute direct overlap where a set of option expiries for BTC, ETH, SOL, XRP on Deribit (and other exchanges) roughly match the time-frame for preconfs enabling one to recalibrate and reconcile any intraday Vol positions vs the actual Preconf markets with more accuracy. For the rest of the day, traders would need to run basis-risk between the Vol positions on their books, with their Preconf positions accordingly. As such, execution in the Vol markets and direct one-for-one pairs trading may be limited on a regular basis and only possible sporadically.

As an alternative to directly offsetting the Short Strangle positions with Long Preconfs, a trader may approach this on a portfolio basis and trade the greeks. In this instance, a preconf buyer may consider selling longer-dated, more liquid straddles, and buying them back up to 12 mins later or whenever the preconf is exercised. The gamma profile there is much less sharp meaning any moves in Spot will have a lesser impact on option price. There is additional Vol/Vega to consider (although less impactful for a short-dated option) and the time decay (which is in the arbitrageur’s favor here as they would be Short the options and theta decays faster closer to expiry). If one could seemingly buy Vol 5-10% cheaper via Preconfs over time, then this would indeed be attractive to options traders.

On the DEX side, liquidity across ETH, and other tokens is limited to about $4-5mm at the time of this article. Taking into account the total volume on major DEXs, we’d additionally expect about $200k of additional demand every block from general order flow. Although most of this typically may not be seen in the public mempool, over 32 blocks this would be $6.4mm which one could either use to estimate option expiration liquidity and/or capture via other conventional MEV approaches (i.e. front/back-runs).

More research on liquidity, and execution is warranted.

### Inventory

To execute trades on two different venues, traders will need to hold sufficient inventory on both locations. For this reason, an additional cost of capital is not considered in this exercise.

For example, if the Call part of the Strangle ends up in-the-money (ITM), when the Preconf is exercised, the user will:

- Buy, let’s say, ETH in the DEX and sell it in the CEX. That is, the user needs USDT/C inventory onchain, and ETH inventory in the CEX, to avoid any transfer lag.

Larger market makers should have sufficient liquidity on both sides making this lesser of an issue.

### European vs American Options

The CEX Strangle (i.e. where the Arbitrageur is ‘Short’) is a European Option unlike the Preconfirmation (i.e. where the Arbitrageur is ‘Long’) which is more an American Option. This gives the Arbitrageur positive basis such that the instrument they are ‘Long’ has more optionality or upside built into it. If the Preconf is early exercised, the trader receives the intrinsic value while the Strangle still has some time value (although minimal), therefore, the PNL is equal to the Net Premium minus the time value difference.

### What About Other MEV and MMEV?

While there is some intersection between conventional MEV and the Strangle strategy as highlighted above, there is still the value to the everyday deal-flow, alongside significant other forms of MEV that are not captured. Monetization of such flows would be separate to, and in addition to, that of the Floor price.

The Strangle exercise above suggests that some types of single-block MEV may currently be constrained by transaction costs which would indicate a non-linear MMEV for when multi-block purchases are possible (at least within the first few blocks).

## Conclusions

The purpose of this paper is to open up a discussion and illustrate a novel approach for the pricing of preconfs - one that importantly responds in real-time to prevailing market conditions. While the execution of such a strategy is difficult, it is not insurmountable for sophisticated players to automate.

Perhaps the most important consideration is that the Price of the Preconfs is a function of the Size of the Markets. If both the Options markets on Deribit and DEX liquidity are 10x larger than they are today, the Preconf Price Floors would be 10x those indicated above. Financial markets often look for inflection points where trades that were almost-possible suddenly become mainstream. With Gas Markets opening up, Macro traders now able to hedge Vol with Preconfs, Based Rollups increasing liquidity, and a trend towards lower transaction fees, this is indeed an interesting area of research.

We believe that highlighting a seemingly odd relationship between token Vol and the Ethereum Blockchain itself will help to further the study of risk-neutral block pricing and are excited to discuss and explore this, and other approaches, with any other parties who may be interested.

# References

[ 1 ] Pascal Stichler, [Does multi-block MEV exist? Analysis of 2 years of MEV Data](https://ethresear.ch/t/does-multi-block-mev-exist-analysis-of-2-years-of-mev-data/20345)

[ 2 ] Öz B, Sui D, Thiery T, Matthes F. Who Wins Ethereum Block Building Auctions and Why?. arXiv preprint arXiv:2407.13931. 2024 Jul 18.

[ 3 ] Jensen JR, von Wachter V, Ross O. Multi-block MEV. arXiv preprint arXiv:2303.04430. 2023 Mar 8.

[ 4 ] Christoph Rosenmayr, Mateusz Dominiak - Statistical Arbitrage on AMMs and Block Building On Ethereum - [Part 1](https://greenfield.xyz/2024/09/10/statistical-arbitrage-on-amms-and-block-building-on-ethereum-part-1/)
