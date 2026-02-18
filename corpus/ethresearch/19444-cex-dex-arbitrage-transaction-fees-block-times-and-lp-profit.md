---
source: ethresearch
topic_id: 19444
title: CEX/DEX arbitrage, transaction fees, block times, and LP profits
author: atiselsts
date: "2024-05-02"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/cex-dex-arbitrage-transaction-fees-block-times-and-lp-profits/19444
views: 6508
likes: 16
posts_count: 13
---

# CEX/DEX arbitrage, transaction fees, block times, and LP profits

It’s widely recognized that CEX/DEX arbitrage trades create a large part of DEX volume, perhaps even the majority of that volume. The [Loss Versus Rebalancing](https://a16zcrypto.com/posts/article/lvr-quantifying-the-cost-of-providing-liquidity-to-automated-market-makers/) (LVR) model stands out as a key tool for quantifying and modeling this arbitrage volume from a theoretical perspective. However, the research focusing on LVR  so far has mostly ignored transaction cost as a parameter in CEX/DEX arbitrage.

This post aims to extend the LVR model to blockchains such as Ethereum’s mainnet, where CEX/DEX arbitrage transactions are expected to have a significant fixed cost term. It conceptualizes LVR as a quantity that is distributed between three primary actors: (1) the LPs of the AMM, (2) the searcher-builder-proposer (SBP) as an aggregate entity, and (3) ETH holders, due to the block basefee that is burned by each transaction. Some implications are:

- As the block time is decreased, an increased share of the nominal LVR is spent on transaction fees.
- Liquidity provider (LP) losses from arbitrage trades do not have the same magnitude as the profits of the arbitrager (searcher-builder-proposer), and as such, are not accurately predicted by a model that approximates them with the square root of the block time.
- Changes in Ethereum’s block time (either increase or decrease) are expected to affect the profitability of AMM LPs, but in many situations, other factors are more important, including the transaction fees.

*A more explanatory and less formal version of this post is available on [Medium](https://atise.medium.com/anatomy-of-cex-dex-arbitrage-481936c83831).*

# Background

According to ([Millionis 2022](https://arxiv.org/abs/2208.06046), [Millionis 2023](https://arxiv.org/abs/2305.14604)) the expected instantaneous LVR is :

\overline{\mathrm{LVR}} \triangleq \lim _{T \rightarrow 0} \frac{\mathrm{E}\left[\mathrm{LVR}_T\right]}{T}=\frac{\sigma^2 P}{2} \times y^{* \prime}(P)  .

This quantity depends only on the volatility, price, and marginal liquidity of the pool. By integrating the expected instantaneous LVR over time, we can obtain the expected LVR for a time period t. Once again, it is not dependent on external factors such as swap fees, block times, transaction costs, etc., and can serve as a nominal baseline metric for any further investigations in this area.

In (Millionis 2023) the authors push their LVR model further, and consider a situation when the AMM has a trading fee γ ≥ 0, and that arbitrageurs arrive to trade on the AMM at discrete times according to the arrivals of a Poisson process with rate λ > 0. They extend the asymptotic analysis of arbitrage profit in a fast block regime (\lambda \rightarrow \infty). They establish a key result that \overline{ARB} = Θ( \sqrt{λ^{-1}} ), where \overline{ARB} is the expected arbitrage profits over time. The authors do not explicitly discuss the case when block times are not Poisson distributed, however, intuitively, one can expect the approximation to remain reasonably accurate when the blocks are uniformly distributed. To formalize this idea: \overline{ARB} = Θ( \sqrt{BT} ), where BT is the average block time.

One key question is whether we see this formula play out in real-world data? A group of research papers generally confirm the \sqrt{BT} model:

- (McMenamin 2023) draws an analogy between the model and the time value of options, which “typically grows proportionally to the square root of time to expiration.”
- (Adams 2024) describe shorter block times as a reason for  increased fee returns for liquidity providers, stressing the difference between Optimism and Arbitrum, in favor of later due to shorter blocks.
- (Fritsch 2024) empirically study the arbitrage profits predicted by the LVR model, and conclude that “our empirical findings come close to [the \sqrt{BT} model] for most pairs and block times larger than 1s”, and attempt to explain any deviations as a result of: (1) uniform block times (i.e. not Poisson-distributed), and (2) price action that does not match the Geometric Brownian motion (GBM) model. Their work is a step towards verifying the \sqrt{BT} model – however, it must be stressed that they measure arbitrage profits, not the LP losses.

In contrast:

- (Dahi 2023) investigate AMM on the XRP ledger and find only a tiny impact on the LPs: 0.35% in relative terms, if block time in simulations is reduced from 12 seconds to 4 seconds. This is much smaller than predicted by the \sqrt{BT} model.
- The Uniswap Foundation’s LP strategies series include simulation results that show a limited dependence on the block time, overshadowed by other factors.

How do we reconcile these differing results and bridge the gap between theory and practice?

The LVR model treats the arbitrage problem as a two-player, zero-sum game, where \overline{ARB} = - \overline{LP}  (where the latter term refers to the expected LP profits). However, this assumption is not valid in the post EIP-1559 world, where transactions cannot be free. Each arbitrage trade not only divides profits among the searcher, builder, and proposer (“SBP” further in this article) but also burns some ETH, contingent on the blockspace demand at the time of the arbitrage. To borrow a term from physics, the basefee introduces a friction in the process. This friction eliminates a significant portion of potential trades, and reduces LP income.

# Analyzing the single-trade LVR

Let’s look at the details of how LVR arises in real-world arbitrage trades. The difference between the DEX and CEX quoted prices (P_{DEX} and P_{CEX}) triggers the arbitrage trade. However, the trade is not going to happen if:

- The CEX price is in the non-arbitrage region created by AMM’s swap fees.
- The CEX price is in the friction region, created by the chain’s basefees and other factors (CEX fees, other  operational costs for arbitrager, risk aversion, etc.).

[![No-trade and friction regions](https://ethresear.ch/uploads/default/original/3X/6/7/672739182dd8b8981b4f531f74a221f1d289dd42.png)No-trade and friction regions665×261 40.3 KB](https://ethresear.ch/uploads/default/672739182dd8b8981b4f531f74a221f1d289dd42)

***Figure 1:** Non-arbitrage and friction regions of an AMM pool with 0.05% swap fee.*

Moreover, the nominal single-trade LVR is “distributed” between three entities:

- Liquidity providers.
- The searcher, block builder, and block proposer (SBP) as a collective entity.
- Holders of ETH, due to the ETH burned in the transaction.

[![image](https://ethresear.ch/uploads/default/optimized/3X/9/5/953c0c9cfa203ff4a017fba5b4f37c5d4c17b2e3_2_345x86.png)image720×181 43.7 KB](https://ethresear.ch/uploads/default/953c0c9cfa203ff4a017fba5b4f37c5d4c17b2e3)

***Figure 2:** The nominal LVR is distributed between three entities: ETH holders (due to the burned basefees), LPs, and the searcher/builder/proposer as a collective entity.*

**LPs** receive the swap fee, while the **SBP** collects the arbitrage profits, which are subsequently divided among these three actors. It’s no surprise that integrated searchers-builders dominate the arbitrage market ([Heimbach 2024](https://arxiv.org/abs/2401.01622)), as for them it is simpler to divide up the profits. **ETH** **holders** do not directly receive compensation, but burning the basefee creates a deflationary pressure on ETH as an asset.

By comparing the nominal single-trade LVR with the LP fees from that trade, we can assess the fairness of the trade to the LP. In a scenario where price evolution is smooth without any jumps, the LP fee nearly recoups the LVR, and the LP loss is minimal. However, if the DEX-to-CEX price difference fluctuates due to block time granularity or actual price discontinuities on the CEX, the LP fee becomes smaller than the LVR, resulting in some loss for the LP against the theoretical rebalancing strategy. One example is shown in the figure below:

[![image](https://ethresear.ch/uploads/default/optimized/3X/2/7/27985324648027915d4f1d0cbb40dcb010494d61_2_690x240.png)image720×251 27.7 KB](https://ethresear.ch/uploads/default/27985324648027915d4f1d0cbb40dcb010494d61)

***Figure 3:** Distribution of the LVR between the three actors. Relative scale. The LVR created by 0.1 % price changes has a much more equitable distribution than the LVR created by 1.0% price change at once.*

# Computing the nominal LVR

Let’s assume that we are a given sequence of CEX prices at BT intervals and a constant product AMM (i.e. AMM that follows the equation xy=k). In order to compute the empirical approximation of the nominal LVR defined as above, we can use the following algorithm:

[![image](https://ethresear.ch/uploads/default/optimized/3X/a/7/a7817e6afc2ee78f955045da5d6d1e370b8bc64e_2_552x500.png)image1434×1298 60.3 KB](https://ethresear.ch/uploads/default/a7817e6afc2ee78f955045da5d6d1e370b8bc64e)

The results of the algorithm have been verified to match both the nominal LVR and the arbitrage trade probability as defined in (Millionis 2023) – see [“Replicating the theoretical results”](https://atise.medium.com/anatomy-of-cex-dex-arbitrage-481936c83831) section in the Medium post.

# Simulation studies

Let’s model the in-range liquidity of the [Uniswap v3 ETH/USDC 0.05% pool](https://app.uniswap.org/explore/pools/ethereum/0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640). As of April 2024, it has approximately $1 billion worth of virtual assets, corresponding to approximately $150 millions of real assets. As a result, the liquidity concentration factor is between 6 and 7. It’s essential to have deep liquidity if we want arbitrage swaps to happen even on relatively small price changes.

The graphs below show the DEX performance metrics using random GBM simulations. The simulations assume 50% yearly volatility, which corresponds to approximately 2.6% daily volatility and 0.03% per-block volatility for 12-second blocks. This is the approximate volatility of ETH in the recent years.

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/2/52ed204954c80c12fe60d115b8530dc19e33c5d9_2_517x369.png)image720×515 88.4 KB](https://ethresear.ch/uploads/default/52ed204954c80c12fe60d115b8530dc19e33c5d9)

***Figure 4:** Simulated DEX metrics with zero basefee.*

Due to a coincidence, the LVR turns out to be approximately $1 per second or $3600 per hour. The LP losses in turn are in the range from $350 to $900 per hour ($3 to $8 million per year). To be clear, this theoretical model does not include any LP fees coming from noise / uninformed traders, which are expected to produce zero LVR, and consequently compensate for the LP losses from the arbitrage trades.

The results show that when the basefee is zero, the LP losses indeed can be more-or-less accurately modeled by the function \sqrt{BT}. However, after introducing EIP-1559 basefees to the model, this isn’t true anymore.

The subsequent two graphs show what happens with when each transaction is assumed to cost a fixed amount of $. A simple Uniswap v3 swap might consume around 150’000 gas, which corresponds to $10 cost per swap in USD terms – assuming the reasonable 22 gwei basefee cost and $3000 ETH/USDC price. In times of high usage or high volatility, the cost of a transaction can easily increase several times.

[![image](https://ethresear.ch/uploads/default/optimized/3X/5/a/5afc2619927bd3babb3015f3cb3ed9e9b00cd2b8_2_517x369.jpeg)image720×515 59.3 KB](https://ethresear.ch/uploads/default/5afc2619927bd3babb3015f3cb3ed9e9b00cd2b8)

***Figure 5:** Simulated DEX metrics with $10 per swap spent on the basefee.*

[![image](https://ethresear.ch/uploads/default/optimized/3X/4/2/42c2d88113ebb2d718f19a54de820c151ca37b90_2_517x369.jpeg)image720×515 61.4 KB](https://ethresear.ch/uploads/default/42c2d88113ebb2d718f19a54de820c151ca37b90)

***Figure 6:** Simulated DEX metrics with $30 per swap spent on the basefee.*

For a summary of the LP losses, see the figure below. Even adding a constant offset from the *x* axis to the \sqrt{BT}. model does not lead to a good fit (the brown line). More frequent transactions also burn more ETH, thus canceling out most of the positive impact on the LP fees.

[![image](https://ethresear.ch/uploads/default/optimized/3X/b/5/b53b8658e7ad04dc746ae61a681bd639a0c3d72e_2_517x370.jpeg)image720×516 70.7 KB](https://ethresear.ch/uploads/default/b53b8658e7ad04dc746ae61a681bd639a0c3d72e)

***Figure 7:** The \sqrt{BT} model shows a good-but-not-perfect fit if the basefee is zero, but much worse otherwise.*

### Simulations with longer block times

Following Table 1 in (Millionis 2023), I also include results with 120 second and 600 second blocktimes.

Uniformly distributed blocks, $10 swap basefees:

```auto
swap fee:                          1bp   5bp  10bp  30bp 100bp
block time   600 sec, arb prob %: 92.7  85.2  76.4  50.5  21.7
block time   120 sec, arb prob %: 83.7  68.4  53.5  27.4   9.9
block time    12 sec, arb prob %: 53.1  29.9  19.1   7.7   2.0
block time     2 sec, arb prob %: 20.8   9.4   5.5   1.8   0.1
swap fee:                          1bp   5bp  10bp  30bp 100bp
block time   600 sec, LP loss  %: 96.3  83.5  71.3  44.8  19.6
block time   120 sec, LP loss  %: 92.1  69.1  52.5  26.9  10.0
block time    12 sec, LP loss  %: 80.0  44.2  28.3  11.6   3.8
block time     2 sec, LP loss  %: 69.6  31.3  18.6   7.1   2.2
```

Uniformly distributed blocks, $30 swap basefees:

```auto
swap fee:                          1bp   5bp  10bp  30bp 100bp
block time   600 sec, arb prob %: 88.8  81.5  72.8  48.1  20.8
block time   120 sec, arb prob %: 75.4  61.0  47.8  24.5   8.8
block time    12 sec, arb prob %: 36.2  21.3  14.0   5.8   1.5
block time     2 sec, arb prob %: 10.7   5.5   3.3   1.1   0.1
swap fee:                          1bp   5bp  10bp  30bp 100bp
block time   600 sec, LP loss  %: 96.3  83.6  71.4  45.0  19.8
block time   120 sec, LP loss  %: 92.3  69.8  53.3  27.6  10.3
block time    12 sec, LP loss  %: 82.5  48.5  32.0  13.5   4.5
block time     2 sec, LP loss  %: 76.5  39.5  24.6   9.8   3.2
```

The results show that:

- The approximation from (Millionis 2023) that arbitrage probability is approximately equal to LP loss does not hold, in general.
- In most cases, the swap fee is a more dominant factor for the LPs than either the block time or basefee.
- Increasing the block time does increase LP losses, but by a much smaller factor than predicted by the \sqrt{BT} model, especially in pools with low swap fees (1 bps to 10 bps).

# Discussion

### Generalizing the results

1. Generalizing to other pools. The simulation results above are specific to the USDC/ETH 0.05% pool, which is typically the most liquid volatile pool on Uniswap v3. (There are stable pools with deeper liquidity). For pools with lower liquidity, the importance of the friction created by the basefee would be increased. For instance, let’s say that the ETH/USDT 0.05% pool has 1/3 of the liquidity. Then the results from $10 basefee on that pool would match those of the USDC/ETH pools with $30 basefee. For pools with higher liquidity (such as USDC/USDT) the friction would be decreased, proportional to the rise in liquidity.
2. Generalizing to other chains. The model assumes that shorter blocks simply divide the available blockspace differently, rather than add more blockspace. The simulation results would not generalize if the block time decrease was accompanied with a proportional decrease in basefees.

### Implications for blockchain design

The results clearly show that LP losses are not accurately predicted by the \sqrt{BT} model, unless the basefee is close to zero. While it’s true that shorter blocks benefit LPs, the effect is limited and frequently less significant than other factors (basefee, liquidity depth, swap fee %, and potentially others). More compelling arguments for fast block times may come from other perspectives, like the perspective of traders, or that of block builders, but these are out of the scope for this article.

Potentially, we can view the optimal block time choice problem from two viewpoints:

- From L1 perspective, reducing the basefee could provide a quicker win, compared with changing the block time. However, keeping the design decentralized and credibly-neutral is arguably a higher priority.
- From L2 / appchain perspective, especially for chains that focus on DeFi or on trading in particular, it makes sense to excessively optimize for LP profits, including block time and basefee reduction.
- The \sqrt{BT} model implies that decreasing block times is especially important if the block time is already close to zero, since the \sqrt{~} function rapidly grows in the near-zero region.

- L2 fees may already be low enough to minimize the friction caused by the basefee to negligible levels. If this isn’t the case, then paradoxically, exempting CEX/DEX arbitrage swaps from the EIP-1559 basefee would benefit DEX users (both LPs and retail traders).

### Shorter blocks = less MEV?

To be clear, this article makes no claims about MEV in general, just about CEX/DEX arbitrage in particular. Regarding the latter, clearly, there’s a connection between CEX/DEX arbitrage, transaction fees, and block times. However, it is perhaps confusing because this connection goes **both ways**:

- Shorter blocks increase the number of arbitrage transactions and the proportion of gas that they consume.
- On the other hand, shorter blocks decrease the expected value of LP losses.

The same conflicting results apply to changes in basefees. As a result, there’s potential for a confusion, because MEV is increased in one sense, and decreased in another sense.

# Conclusion

This work extends the existing LVR and LVR-with-fees models by adding another component: transaction cost. To summarize the main results:

- CEX/DEX arbitrage transactions are not frictionless due to the EIP-1559 basefee and other factors.
- As a result, the nominal LVR in real-world AMMs is divided among three entities: LPs, ETH stakers, and the SBP as a collective entity.
- More gradual price changes result in more equitable LVR distribution among these three entities.
- On chains with significant transaction costs, LP losses under the LVR assumptions are not accurately predicted by the \sqrt{BT} model.
- The LP losses are determined by several factors, including basefees, swap fees, and block times, the relative importance of which varies.

*Source code of the simulations [is available here](https://github.com/atiselsts/cex-dex-arbitrage-anatomy)*.

## Replies

**Pfed-prog** (2024-05-08):

Thank you so much for such a well research post, but I am pretty sure that the point of the research was Uniswap, not Ethereum.

I am very curios if there is much difference between V2 and V3, if this is true. Otherwise, what about other functions and models for LPs.

---

**atiselsts** (2024-05-09):

Thanks for the comments.

![](https://ethresear.ch/user_avatar/ethresear.ch/pfed-prog/48/14689_2.png) Pfed-prog:

> the point of the research was Uniswap, not Ethereum

I realize I may have made a mistake in not being clear enough about motivation behind this research. Kind of a professional habit - in academia you’re always expected pitch a new piece as something that fills a gap in the existing literature.

In all honesty, that was not the main reason why I wrote up these results. The point is, I have seen many Ethereum’s researchers and users debating about increasing or decreasing the block times, increasing the block’s gas limit, getting rid of events etc. There are all core protocol design choices, and I hope this research and the simulation code that I shared will make these debates more informed. There’s also research on how L2s are better for AMMs, but hopefully my article will make it more clear where these improvements are coming from, and how to push further.

![](https://ethresear.ch/user_avatar/ethresear.ch/pfed-prog/48/14689_2.png) Pfed-prog:

> I am very curios if there is much difference between V2 and V3, if this is true. Otherwise, what about other functions and models for LPs.

The model used in simulations is basically V2, but without fee compounding. It’s a high level simulation and doesn’t take into account non-uniform liquidity distribution, ticks, and other V3 factors. I don’t expect them to make a big difference.

There’s however a big difference in the orderflow that hits V2 and V3 in the real life. USDC/ETH on V2 is much less arbitrage-driven, and better for the LPs - see this [article](https://atise.medium.com/uniswap-v2-still-a-good-deal-for-liquidity-providers-a-retrospective-of-2023-11475e9d8610).

---

**Pfed-prog** (2024-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/atiselsts/48/11051_2.png) atiselsts:

> In all honesty, that was not the main reason why I wrote up these results. The point is, I have seen many Ethereum’s researchers and users debating about increasing or decreasing the block times, increasing the block’s gas limit, getting rid of events etc. There are all core protocol design choices, and I hope this research and the simulation code that I shared will make these debates more informed. There’s also research on how L2s are better for AMMs, but hopefully my article will make it more clear where these improvements are coming from, and how to push further.

Absolutely, I am very excited about your research but I always thought that mev bots would be the primary subjects to be affected by the block time changes.

---

**kosunghun317** (2024-09-19):

Maybe instead of  \sqrt{BT} + C  we should use  \sqrt{BT + C}  where C is determined by size of liquidity pool, base fee, volatility and swap fee rate.

There is no theoretical background or intuition for this guess, just came after seeing graphs in figure 7… those look like sqrt function to be shifted to left.

Any thoughts on this idea?

---

**gutterberg** (2024-09-23):

Very nice article. I have a couple of questions (apologies if they are nonsensical!):

Why is the black LVR line the same in all graphs? Wouldn’t it be impacted by a higher base fee that prevents some arbitrage trades?

Also, what is the intuition for a higher base fee increasing the loss of LPs? Does a higher fee lead to less frequent but larger arbitrage trades, and thus less frequent but larger losses for the LP?

---

**atiselsts** (2024-09-25):

The point is that the block time alone is not sufficient to model the LP losses even if we add arbitrary constants. Adding the constant before taking the square root rather than after taking the square root is almost certainly still not the right thing to do, even though it might give a better fit in the example

It’s better to model the LP loss to arbitrage as:

 L_{LP} = \sqrt{BT} + f(BT, \dots) + r

where f(BT, \dots) is the losses due to base fees (increasing with shorter block time) and r is some remainder due to other factors.

---

**atiselsts** (2024-09-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/gutterberg/48/12265_2.png) gutterberg:

> Why is the black LVR line the same in all graphs? Wouldn’t it be impacted by a higher base fee that prevents some arbitrage trades?

It’s in my opinion a very counterintuitive result, but the fact is, the simulation results excellently match the theoretical LVR (as defined in the original paper by Millionis and others). This “classical” LVR is not affected by the block times, LP fees etc (they don’t model any of that in the paper!). In practice, it’s an upper bound of what the arbitragers can extract from the LPs.

The simulation code was carefully checked for mistakes, since this particular result is so counterintuitive. The source code is linked in the post (and I think it’s very readable!), so anyone is welcome to check that the simulations that produce the black line are correct.

![](https://ethresear.ch/user_avatar/ethresear.ch/gutterberg/48/12265_2.png) gutterberg:

> Also, what is the intuition for a higher base fee increasing the loss of LPs? Does a higher fee lead to less frequent but larger arbitrage trades, and thus less frequent but larger losses for the LP?

Yes, either like that (the LVR of a single trade are proportional to the square of the price move), or because the price reverts back towards the starting price, and the LP ends up with a similar position composition but with fewer fees.

---

**atiselsts** (2024-10-07):

There is now a proposal to reduce [ETH block times to 8 seconds](https://github.com/ethereum/EIPs/pull/8931) (EIP-7781).

Let’s run some simulations fine-tuned to match the highest volume pool on Uniswap v3, ETH/USDC 0.05%:

- swap fee: 5 bps
- pair volatility: 0.6072 (yearly)
- virtual liquidity depth: $909 million
- swap transaction fees: $2 (bearish demand), $4 (baseline), $10 (bullish), and $0 (as a reference)

An EF researcher claims that it will “make DEXes like Uniswap v3 roughly sqrt(12/8) ≈ 1.22x more efficient”. The simulation results shows that this is not accurate, even if we assume that the “efficiency” of a DEX is exactly equal to the non-atomic arbitrage costs it’s exposed to.

As expected, the LP losses increase as the swap transaction fee goes up:

[![eip7781_cex_dex_arbitrage_lp_losses_basefee](https://ethresear.ch/uploads/default/optimized/3X/1/7/174d8530976252a078683352af225edad2104c12_2_690x493.png)eip7781_cex_dex_arbitrage_lp_losses_basefee969×693 46.2 KB](https://ethresear.ch/uploads/default/174d8530976252a078683352af225edad2104c12)

Here are the numerical results quantifying the reduction in LP losses after reducing the block time from 12 to 8 seconds:

```auto
basefee=$0 improvement=15.8%
basefee=$2 improvement=12.4%
basefee=$4 improvement=10.4%
basefee=$10 improvement=7.3%
```

Even for zero basefee, the improvement is less than 22%, because the \sqrt{BT} formula is an approximation, not fully acccurate at low swap fee levels.

For the baseline $4 transaction cost, the improvement is around 10%. It’s still something significant, of course. However, in practice it may even be smaller than than, as the arbitragers will need to increase their profit margins due to an increased likelihood of reorgs at 8 second blocks, so they may decide to skip some of the barely profitable transactions.

**Repeatability:** The updated code is available [here](https://github.com/atiselsts/cex-dex-arbitrage-anatomy/tree/experiment/8-second-block-times). The file `eip7781_get_parameters.py` prints up-to-date parameters for the simulations, and `simulation_examples_eip7781.py` runs the new simulations.

---

**umbnat92** (2024-10-21):

Hey [@atiselsts](/u/atiselsts) thanks for your research.

I have few questions tho.

1. It seems you are using Eqs for LVR in a Constant Product Market Maker (i.e. Uniswap v2). However, you often refer to Uniswap v3. Can you explain better this point?
2. LVR is a really interesting concept, but it seems only few have looked into how this apply to Concentrated Liquidity. Indeed, LVR is mostly an issue for CPMM because liquidity is not optimally allocated. Despite here we have a theoretical formulation, it is known it is derived on several assumptions may not hold true.

If one takes empirical data on v3, it seems PNL for LP positions is positive, indicating that the impact of LVR is negligible due to a better use of liquidity (we discussed it [here](https://chorus.one/articles/hedging-lp-positions-by-staking) - extensively [here](https://chorusone.notion.site/Hedging-LP-position-by-staking-651f4e543f2448a58d99b788d35d941b)). We also made a dashboard to track LPs’ PNL [here](https://dune.com/umbnat92/uniswap-v3-lps-pnl?Start+Day_d47e5e=2024-09-01+00%3A00%3A00), where you can see that by introducing the revenues from fees LPing is overall in profit - attached a screenshot from the dashboard.

[![Dune Dashboard on LPs PNL (Uniswap v3)](https://ethresear.ch/uploads/default/optimized/3X/e/3/e3b14365ad55fd6e2e64d0b14596c64413d21613_2_690x298.png)Dune Dashboard on LPs PNL (Uniswap v3)1884×814 83.6 KB](https://ethresear.ch/uploads/default/e3b14365ad55fd6e2e64d0b14596c64413d21613)

---

**atiselsts** (2024-10-21):

Hello, thanks for engaging, good questions.

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> It seems you are using Eqs for LVR in a Constant Product Market Maker (i.e. Uniswap v2). However, you often refer to Uniswap v3. Can you explain better this point?

Inside a tick range v3 pool is governed by the same formulas as a v2 pool. The 0.05% pool uses 10 tick range, corresponding to approximately 0.1% price change. Almost all swaps in the pool are small enough to not cross a tick range boundary. Moreover, even when the swaps do cross a boundary, in almost all situations the liquidity in the neighboring tick ranges is similarly deep. ([This paper](https://www.sciencedirect.com/science/article/pii/S1544612323010899) shows that in most situations assuming flat / v2-like liquidity distribution is accurate enough; my experience confirms that.)

To be clear, in my post I talk about virtual liquidity (in USD) terms of $1 billion. This is still fairly accurate as of now. (You can check the virtual depth using the script `eip7781_get_parameters.py` from the latest git branch `experiment/8-second-block-times`, reference in my last comment.) The real liquidity depth (in USD) of the v3 pool right now is $148.5 million. That’s a liquidity concentration factor of around seven.

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> LVR is a really interesting concept, but it seems only few have looked into how this apply to Concentrated Liquidity. Indeed, LVR is mostly an issue for CPMM because liquidity is not optimally allocated. Despite here we have a theoretical formulation, it is known it is derived on several assumptions may not hold true.

From a theoretical point of view, LVR for CL is a simple generalization of LVR for CPMM. The original LVR paper already includes the formula for Uniswap v3.

The LVR is basically the same except that it’s scaled by the concentration factor.

For instance, if ETH volatility is 0.5 per year then:

- for v2 LPs, acceptable fee APR is 0.5**2 / 8 = 3.125%
- for v3 LPs in the ETH/USDC pool with concentration factor 7, acceptable fee APR is 7 * 0.5**2 / 8 = 21.9% (that’s for the whole pool, individual LPs obviously may have different concentration factors)

In short, the v3 pool must earn 7 times as much from unit of liquidity to offset the cost of LVR.

Empirically, there are many other differences between v2 and v3 that make a fair comparison hard. I agree that not that much work has been published on this, and not that many dashboards either.

Comparing PnL vs hold is also hard to do in a methodical way, because it’s such a noisy metric that depends on the asset’s price path. Looking at the markouts or hedged PnL gives a much less noisy outcome.

On your last point. Proving which assumptions are or aren’t true in the real life (and when LVR is an inaccurate metric) would be really important, especially as many alleged solutions for LVR are being published and implemented, some of them making questionable compromises to that end.

---

**umbnat92** (2024-10-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/atiselsts/48/11051_2.png) atiselsts:

> The LVR is basically the same except that it’s scaled by the concentration factor.

It should not be a concentration factor, but rather a dependency on the tick price range (so it’s dependent on the position of the LP). This is what is puzzling me the most!

![](https://ethresear.ch/user_avatar/ethresear.ch/atiselsts/48/11051_2.png) atiselsts:

> Moreover, even when the swaps do cross a boundary, in almost all situations the liquidity in the neighboring tick ranges is similarly deep.

It doesn’t seem to be true tho. However, this below is a screenshot, you can show the impact in a quantitative way, probably that would add value to the analysis.

[![Liquidity on WETH/USDC (Uni v3)](https://ethresear.ch/uploads/default/original/3X/7/d/7d1ceb34f1b8eb22d9230972a2c202ade453ef52.png)Liquidity on WETH/USDC (Uni v3)771×527 19.6 KB](https://ethresear.ch/uploads/default/7d1ceb34f1b8eb22d9230972a2c202ade453ef52)

![](https://ethresear.ch/user_avatar/ethresear.ch/atiselsts/48/11051_2.png) atiselsts:

> Looking at the markouts or hedged PnL gives a much less noisy outcome.

But that is a usually biased metric since it doesn’t account for liquidity on both sides (at least all estimators based on markouts I’ve seen so far). This is why I’ve built the dashboard above, where I account for the Pool Value, so the PnL is referred to the Pool, not the user, and this removes the bias.

![](https://ethresear.ch/user_avatar/ethresear.ch/atiselsts/48/11051_2.png) atiselsts:

> On your last point. Proving which assumptions are or aren’t true in the real life (and when LVR is an inaccurate metric) would be really important, especially as many alleged solutions for LVR are being published and implemented, some of them making questionable compromises to that end.

Yeah, that’s true.

---

**atiselsts** (2024-10-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> It should not be a concentration factor, but rather a dependency on the tick price range (so it’s dependent on the position of the LP). This is what is puzzling me the most!

I don’t see a problem, if you look at an individual LP then it’s more convenient to use the tick range, if the whole pool, with many positions, then it’s the concentration factor.

![](https://ethresear.ch/user_avatar/ethresear.ch/umbnat92/48/9019_2.png) umbnat92:

> It doesn’t seem to be true tho. However, this below is a screenshot, you can show the impact in a quantitative way, probably that would add value to the analysis.

1. Sorry I missed a link to a paper in my post, I meant this one about using V2 methods to analyze V3.
2. I have a script that compares V3 quoter contract output with a simple approximation shown below:

```python
def v2_approximate(zero_for_one, amount_in, reserve0_x96, reserve1_x96, pool_fee):
    reserve_in, reserve_out = (reserve0_x96, reserve1_x96) if zero_for_one else (reserve1_x96, reserve0_x96)
    amount_in_with_fee = amount_in * (1_000_000 - pool_fee)
    numerator = amount_in_with_fee * reserve_out
    denominator = reserve_in * 1_000_000 + amount_in_with_fee * Q96
    amount_out = numerator // denominator # this rounds down
    return amount_out
```

For the major pools the error is usually negligible, not even a bps for swaps below $1M. For instance for the pool in the screenshot, at block 21000000:

```plaintext
fair price=379316774.9966937 (2636.3189447888685)
swap qoute -> base (USDC -> WETH)
1000 -> 0.379126
  1000 -> 0.379126
  error=-2.220446049250313e-14 %
10000 -> 3.791200
  10000 -> 3.791200
  error=0.0 %
100000 -> 37.905617
  100000 -> 37.905617
  error=-2.220446049250313e-14 %
1000000 -> 378.401901
  1000000 -> 378.418854
  error=-0.004480043787635779 %

swap base -> quote (WETH -> USDC)
0.37931677499669364 -> 999.498129
  0.37931677499669364 -> 999.498129
  error=0.0 %
3.7931677499669365 -> 9994.812933
  3.7931677499669365 -> 9994.812933
  error=0.0 %
37.93167749966936 -> 99931.322296
  37.93167749966936 -> 99931.296492
  error=2.5821733773412348e-05 %
379.31677499669365 -> 997639.522619
  379.31677499669365 -> 997632.793882
  error=0.0006744657611745808 %
```

