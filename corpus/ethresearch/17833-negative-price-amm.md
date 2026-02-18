---
source: ethresearch
topic_id: 17833
title: Negative Price AMM
author: v-for-vasya
date: "2023-12-15"
category: Decentralized exchanges
tags: [mev]
url: https://ethresear.ch/t/negative-price-amm/17833
views: 1735
likes: 3
posts_count: 3
---

# Negative Price AMM

**TL;DR:** We discover that negative liquidity is possible and construct an AMM to access the negative domain by allowing the price to go negative. The invariant for a negative price happens to be the formula for a circle and the liquidity distribution happens to have a power law tail. You can interact with and compare it to an RMM [here](https://www.desmos.com/calculator/hftsrbp1xj). *Most interesting points are outlined below with link to paper at the end.*

[![Screenshot 2023-12-14 at 2.05.07 AM](https://ethresear.ch/uploads/default/optimized/2X/2/2aa7f87f50d43b6ca8c3608ca6d021214a3693c2_2_661x500.jpeg)Screenshot 2023-12-14 at 2.05.07 AM2294×1734 172 KB](https://ethresear.ch/uploads/default/2aa7f87f50d43b6ca8c3608ca6d021214a3693c2)

**Figure 1**:*Two negatively priced assets can be exchanged between each other for a positive price. An impossible task in tradfi, requiring a fiat numeraire to act as an intermediary.*

---

**Summary:**

Swapping and liquidity provision transactions of a Concentrated Circular Market Maker (**CCMM**) are obfuscated using Fully Homomorphic Encryption ([FHE](https://github.com/zama-ai/fhevm/blob/17d43894e925db08bbf1f8b570903ead8445a993/fhevm-whitepaper.pdf)) to mitigate MEV in the public mempool by combining game theory with the Kelly criterion. Liquidity of the CCMM is adjusted using a scale parameter and can be modified with a hook in Uniswap v4. We show how it is possible to enter the negative liquidity domain with the CCMM.

---

## Negative Liquidity

If we look at a Constant Product Market Maker (CPMM) such as Uniswap, we can see that it happens to provide liquidity in the negative domain. Take the [Uniswap Invariant](https://www.paradigm.xyz/2021/06/uniswap-v3-the-universal-amm) with liquidity L

xy=L^2

introducing price p as p = y/x and y = px

xpx=L^2

solving for x

x=\sqrt{\frac{L^2}{p}}

note the appearance of a negative sign

x=±\frac{L}{\sqrt{p}}.

It’s just difficult to access this negative liquidity in Uniswap due to the invariant being a hyperbola. By pressing the invariant against the axes, concentrating liquidity, and folding it on itself we can travel to the  [negative domain](https://www.desmos.com/calculator/hftsrbp1xj). A liquidity provider may become a liquidity taker with the following invariant where z is a scale parameter

(x−z)^2 +(y−z)^2 =z^2.

We like to call it the DiracAMM (Paul Dirac discovered anti-matter with a similar trick by seeing that energy \sqrt{E^2} could have a negative value in the [energy-momentum relation](https://en.wikipedia.org/wiki/Energy%E2%80%93momentum_relation)). One can program the invariant to not provide liquidity after touching the axes though, in which case its liquidity distribution L happens to be the Student’s-t distribution with degree of freedom df=2, a special case of a power law tail where the law of large numbers has no predictive capacity on the [variance](https://en.wikipedia.org/wiki/Student%27s_t-distribution#Special_cases).

L_{Student-t}(x) = \frac{1}{(1+x^2)^\frac{2}{3}}

## LP Payoffs

If price, following a power law, is allowed to flow into the negative, as is empirically observed with [various](https://www.bloomberg.com/news/articles/2023-11-23/trader-error-causes-huge-plunge-in-finnish-power-prices) [assets](https://www.jstor.org/stable/2353198), then the LP payoff function happens to resemble a collection of non-linear payoffs.

[![f4](https://ethresear.ch/uploads/default/optimized/2X/2/26bcfee31f3367d0f7f7c86d0e2508a53489be9b_2_690x345.jpeg)f43072×1536 396 KB](https://ethresear.ch/uploads/default/26bcfee31f3367d0f7f7c86d0e2508a53489be9b)

But it’s not necessary though for the underlying price to be negative for this AMM to be useful. Rather, one suggestion is to use the price of $0 as an offset from the current underlying price of, let’s say $100 . A negative 1 price indicates a decline of the underlying from $100 to $99. If the CCMM has one asset that can not go negative, such as a stablecoin, then it can only have LP payoffs **2A2** and **2B2**, but by borrowing the LP position through a lending protocol one could mimic the payoffs of **2D2** and **2C2** respectively.

## MEV approach with Kelly Criterion and FHE

Since a gain and a loss can be defined as an offset with a CCMM, we can combine it with the game theory behind rational MEV decision makers who follow the Kelly criterion, a strategy that ensures long-term optimal geometric growth

f∗= p - \frac{1-p}{b}

where f∗ represents a MEV extractor’s portfolio allocation in a MEV attack with the probability of success p and betting odds b. By targeting **Kelly-neutrality** we set a MEV extractor’s Kelly betting amount f = 0 at an increased gas cost by rearranging for the following equality to hold

p=\frac{1-p}{b}.

We do so by introducing two encrypted boolean values ([ebool)](https://docs.zama.ai/fhevm/writing-contracts/types) for swapping B_{swap}=[0,1] and providing liquidity B_{LP}=[0,1] going into the mempool. Where the boolean value can mean 1 for swap x for y and 0 for swap y for x (or remove and re-add liquidity for B_{LP}). We can also encrypt the swap quantity dx (or dy) as [euints](https://docs.zama.ai/fhevm/writing-contracts/types), thereby making it unclear what the betting odds b (gain and loss relationship) are.

E⟨B_{swap/LP}⟩=\frac{1-E⟨B_{swap/LP}⟩}{\frac{E⟨Gain⟩}{E⟨Loss⟩}} = \frac{1-0.5}{\frac{x}{x}}=0.5

Setting the expected value of a MEV extractor’s Kelly bet E⟨f∗⟩ = 0. Targeting Kelly-neutrality could be a useful mechanism for MEV. We noticed that with FHE we can selectively target just the variables we want to obfuscate enough without having to encrypt everything and think that this approach could be useful to others looking into MEV.

## Further work

An approach to avoid negative prices for the underlying could be to construct a passive **wall of liquidity**, a liquidity fingerprint that asymmetrically increases non-linearly as price approaches zero, denting price impact. The super-heavy tailed distributions like the [Log-Cauchy distribution](https://en.wikipedia.org/wiki/Log-Cauchy_distribution) with concentration parameter c come to mind with liquidity fingerprint in price space being

L_{Log−Cauchy}(p) = \frac{1}{\pi p} \frac{c}{ln(p)^2+c^2}.

[![f44](https://ethresear.ch/uploads/default/optimized/2X/2/24b37c0e2b2d52fb38f2be8db48606f43be14827_2_500x500.jpeg)f441920×1920 236 KB](https://ethresear.ch/uploads/default/24b37c0e2b2d52fb38f2be8db48606f43be14827)

This is a very interesting liquidity fingerprint because it captures what we see in crypto where some tokens stay where they are, the majority approach the zero bound, and a select few fly towards the right tail. One of the mathematical challenges here being that liquidity spikes to infinity at 0 though.

> Our paper with more interesting details is on GitHub

## Replies

**Pfed-prog** (2024-01-07):

Here is an excerpt from the paper

[![image](https://ethresear.ch/uploads/default/optimized/2X/0/01a76c81561665b31a626f8f5c5fc29f59551524_2_690x200.png)image1068×310 70.2 KB](https://ethresear.ch/uploads/default/01a76c81561665b31a626f8f5c5fc29f59551524)

I am very curious how negative liquidity would affect the LPs pay outs in contrast to Uniswap V2 and V3.

---

**v-for-vasya** (2024-01-12):

Just added a desmos example [here](https://www.desmos.com/calculator/qkexksh7vf) that shows how a CPMM (uni v2), CLMM (uni v3), and CCMM would differ from each other. For the sake of simplicity, I used oil priced in dollars (which has gone [negative before](https://www.nytimes.com/2020/04/20/business/stock-market-live-trading-coronavirus.html)) and set the price to 1 and matched the amount of liquidity in each LP payoff for ease of comparison.

[![payoffs](https://ethresear.ch/uploads/default/optimized/2X/b/b8b5d58173e939e29309af0f8bae710cf6a2ea9f_2_657x500.jpeg)payoffs2142×1630 125 KB](https://ethresear.ch/uploads/default/b8b5d58173e939e29309af0f8bae710cf6a2ea9f)

In the case of an LP position consisting of both assets going negative (let’s say a token pair of oil/onions), the payoff would go to infinity on one end and emerge on another, creating an infinity loop:

[![payoff_inf](https://ethresear.ch/uploads/default/optimized/2X/b/b33a265a5815aa8b7a3b39d9666c9388c74408d9_2_661x500.jpeg)payoff_inf2158×1630 108 KB](https://ethresear.ch/uploads/default/b33a265a5815aa8b7a3b39d9666c9388c74408d9)

I used onions as an example because they also went negative before. In 1958 Congress had to pass the [Onion Futures Act](https://en.wikipedia.org/wiki/Onion_Futures_Act) banning the trading of onions as the price went negative at the CME. This applies only to the US, but DeFi is permissionless. The ability to trade two negatively priced assets appears to be a unique feature in DeFi that is just not possible in TradFi where one has to go through a numeraire such as the US Dollar to trade a negatively priced oil barrel for a negatively priced natural gas BTU instead of exchanging them directly through a token pair.

Additionally, a potential application of negative prices besides commodities that can go negative (oil [[1](https://www.nytimes.com/2020/04/20/business/stock-market-live-trading-coronavirus.html)], natural gas [[2](https://www.spglobal.com/commodityinsights/en/market-insights/latest-news/natural-gas/041023-negative-gas-prices-return-to-permian-basin-as-overlapping-maintenance-looms#:~:text=Negative%20gas%20prices%20return%20to%20Permian%20Basin%20as%20overlapping%20maintenance%20looms,-Author%20J%20Robinson&text=Spot%20natural%20gas%20prices%20in,two%20critical%20intrastate%20gas%20pipelines.)], onions [[3](https://en.wikipedia.org/wiki/Onion_Futures_Act)], electricity [[4](https://emp.lbl.gov/publications/plentiful-electricity-turns-wholesale#:~:text=Negative%20electricity%20prices%20result%20either,due%20to%20system%2Dwide%20oversupply.)]) could actually be some form of a reputation token.

For example, reputable individuals in an industry, or famous personalities, or reputable DAOs, or brands may issue a token that can be redeemed for time spent with such an entity or services rendered.

If a reputation token does go beyond the zero bound after a large sale, maybe an insider was simply interested in making a quick buck or a scammer was aiming to simply deceive uninformed people. By having a zero bound, the insider and scammer would be able to extract value due to information asymmetry versus the uninformed token purchasers since the price can only crash to zero.

If a reputation token LP pair creator does not allow for the entry into the negative domain, then it would look incredibly suspicious in a world where reputations can go negative!

This might help deal with a lot of the anonymous scams one sees in crypto where v2 LP pair names with a zero bound are created. If a company/person/token/DAO truly is legit, then one shouldn’t worry if one’s token price can go negative. A kind of skin in the game.

