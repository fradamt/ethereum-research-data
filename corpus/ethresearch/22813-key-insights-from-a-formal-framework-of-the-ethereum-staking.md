---
source: ethresearch
topic_id: 22813
title: Key Insights from a Formal Framework of the Ethereum Staking Market
author: no-swisseconomics
date: "2025-07-25"
category: Economics
tags: []
url: https://ethresear.ch/t/key-insights-from-a-formal-framework-of-the-ethereum-staking-market/22813
views: 486
likes: 3
posts_count: 1
---

# Key Insights from a Formal Framework of the Ethereum Staking Market

> This post summarizes research by the Center for Cryptoeconomics. See the full report here. This research was funded by cyber.Fund. The opinions expressed in this post are solely those of the authors Juan Beccuti, Thunj Chantramonklasri, Matthias Hafner, and Nicolas Oderbolz. We thank @artofkot, @kkulk , @PaulYa5hin and @thelazyliz for their invaluable support, comments and reviews.

# TL;DR

With the goal of contributing to the study of how changes in Ethereum’s issuance curve affect the staking decisions of different categories of stakers and, consequently, the degree of decentralization in the staking market, we develop a game-theoretic model of the Ethereum staking market and use it to conduct a comparative analysis of different issuance schedules. We discuss the results of this analysis in the context of the available empiricial literature, as well as our own preliminary estimates of staking supply elasticities. In addition to contributing to the debate on reducing protocol issuance, we expect that the model can serve as a basis for further extensions, providing a flexible framework for analyzing staking dynamics under different protocol changes.

Existing empirical research, as well as our own estimates using an Instrumental Variable (IV) approach, tends to suggests that solo stakers may be more sensitive to changes in staking yields than other staking categories.

The game-theoretic model presented below shows that a staker’s equilibrium staking supply is determined by their staking costs and revenues, as well as the strategic behavior of other market participants. Our results suggest that later competitive market forces may be important in explaining why solo stakers are more sensitive to changes in staking yields. Other staking categories benefit from additional revenue streams, such as superior MEV access and DeFi yields, which makes them less responsive to changes in consensus rewards. Given Ethereum’s downward-sloping issuance schedule, strategic solo stakers internalize these competitive pressures, rendering them more sensitive to changes in consensus yields.

By comparing the equilibria of our model under the current issuance schedule with those of a proposed alternative, we find that reducing issuance could exacerbate this effect. While a change in the issuance schedule in our model is associated with a reduction in the supply of staked ETH across all staking categories, it is also associated with a reduction in the market share of solo stakers and an increase in the market share of centralized staking solutions.

Additionally, our model predicts that solo staking becomes less profitable than other staking methods. While outside of the scope of our model, this could undermine the long-term viability of solo staking  and accelerate the exit of solo stakers from the market in favor of alternative solutions, such as decentralized staking service providers and liquid staking.

# Motivation

As the volume of ETH staked within Ethereum’s Proof-of-Stake (PoS) protocol has grown significantly over the past few years, discussions around the long-term sustainability of the current issuance schedule have become prominent. Central to this debate is the trade-off between the efficient use of validator infrastructure, issuance-driven inflation, and economic security.

A reduction in the consensus issuance schedule has been argued to be important in avoiding an end-game scenario in which most of the circulating supply of ETH is staked (see for example [Elowsson (2024)](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448) and [Schwarz-Schilling (2024)](https://ethresear.ch/t/endgame-staking-economics-a-case-for-targeting/18751)). Such an outcome would mean that the supply of staked ETH far exceeds the necessary threshold for economic security, resulting in unnecessary inflationary pressure and inefficient allocation of validator resources. In addition, there are concerns about the potential systemic risks posed by the proliferation of liquid staking tokens and their potential to replace ETH as the de facto currency in the ecosystem. These considerations suggest that it may be prudent to revise the issuance schedule to effectively reduce the incentives for staking.

Conversely, a reduction in staking rewards may disproportionately affect the profitability of relatively expensive decentralized staking solutions compared to centralized solutions, and thus may result in less decentralization. In particular, solo stakers, who already represent a small segment of the total validator population, may be disproportionately driven out of the market.

In what follows, we aim to test the validity of this argument by examining how different staking methods, and in particular solo stakers, may be affected differently by changes to Ethereum’s consensus issuance policy. Specifically, we focus on answering two key research questions:

- How do different types of stakers respond to shifts in the issuance schedule?
- How might these changes impact the decentralization of the Ethereum staking ecosystem?

# Methodological Approach

To address these research questions, we employ the following methodological approaches, the results of which we highlight in this post:

- Empirical Estimation: We use an Instrumental Variable approach to estimate how changes in staking rewards affect the supply of staked ETH across these different staking categories.
- Game Theoretic Model: Guided by the empirical results, we develop a game-theoretic model of the Ethereum staking market in which staking agents of different types determine their staking supply based on the revenue streams and cost structures associated with different staking methods. The goal is to construct a modeling framework that links individual staking decisions to the aggregate staking supply in the Ethereum staking market.
- Simulation and Comparative Analysis: By simulating this game-theoretic model under various parameter configurations, we seek to understand how individual cost structures and revenue streams influence equilibrium outcomes in the aggregate staking market. In addition, we calibrate the model to specific parameter settings and evaluate how changes in Ethereum’s issuance schedule could affect staking market outcomes, in particular the market shares of different staking categories.

# Estimation of Staking Supply Elasticity

## Methodology

We estimate the sensitivity of staking supply to changes in staking rewards across different staker types. To address endogeneity concerns, we employ an Instrumental Variable (IV) approach. Endogeneity is an issue in this context, since any combination of staking yields and staking supply observed at a given point in time is in theory a result of a market equilibrium, where the supply and demand for staking meet. Changes in this market equilibrium can arise from both shifts in the supply curve and shifts in the demand curve, creating endogeneity in any simple estimate of the correlation between staking yields and staking supply. The purpose of this estimation approach is thus to identify instruments that shift the demand curve for staked ETH without simultaneously affecting the factors determining the supply curve. Using such instruments allows us to isolate the shape of the supply curve, at least at a local equilibrium point.

For the estimation of the yield elasticities of supply for different staking categories, we propose the use of gas fees as a robust instrument. Gas fees may represent a valid instrument in this context, because they directly influence staking rewards but remain exogenous to the determinants of staking supply, as they are driven by external factors such as network activity, DeFi transactions, and NFT trading. Leveraging the natural fluctuations and publicly available gas fee data, we conduct a two-stage least squares (2SLS) analysis using daily-level data, with rewards and amount staked denominated in USD. A detailed description of the estimation approach and the corresponding results is provided [here](https://arxiv.org/abs/2503.14385).

## Results

Importantly, the approach yields estimations of the yield elasticities of supply that suggest that the staking supply of solo stakers is more sensitive to changes in staking yields compared to the staking supply of the overall population of stakers. The elasticity of staking supply to staking rewards is estimated at 1.184 for solo stakers and 1.078 for all stakers. Both estimates are statistically significant at the 1% level. These results are generally consistent with the findings of [Eloranta and Helminen (2025)](https://ethresear.ch/t/impact-of-consensus-issuance-yield-curve-changes-on-competitive-dynamics-in-the-ethereum-validator-ecosystem/21617), whose estimations similarly suggest that solo stakers are more sensitive to changes in the staking yield than the overall population of stakers.

**Table 1: 2SLS estimates with gas fees used as an instrument for staking rewards**

|  | Solo Staking | All Staking Types |  | (1)  Log Amount  Staked (USD) | (2)  Log Amount  Staked (USD) | (3)  Log Amount  Staked (USD) | (4)  Log Amount  Staked (USD) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Log Rewards (USD)t | 1.184***(0.073) |  | 1.078***(0.035) |  |  |  |  |
| Log Rewards (USD)t−1 |  | 1.176***(0.074) |  | 1.075***(0.036) |  |  |  |
| Constant | 6.774**(0.877) | 6.868***(0.888) | 7.739***(0.543) | 7.786***(0.556) |  |  |  |
| Observations | 622 | 621 | 622 | 621 |  |  |  |
| R-squared | 0.128 | 0.101 | 0.858 | 0.851 |  |  |  |



# Game-theoretic Model

To further understand what drives staking supply elasticities, we develop a game-theoretic framework that allows us to model the strategic staking decisions of different staking market participants as a function of the Ethereum issuance schedule, other external revenue sources, and the cost of staking.

## Agent Types

We propose a game-theoretic model of a segmented staking market, where ETH holders are differentiated based on their preferences and/or level of technical sophistication, which in turn determines how they will stake. Specifically, three distinct types of ETH holders are considered:

\theta \in \{\text{Retailer, Techie, Expert}\}

Each category comprises a fixed number of stakers, denoted as N_r, N_t, and N_{ss} for *Retailers*, *Techies*, and *Experts* (or Solo Stakers), respectively. To ensure tractability, within-group homogeneity is assumed.

## Segmented Staking Market

In addition, the model incorporates several staking methods that differ in both the costs they impose on the ETH holder and the revenue streams they provide. These methods include solo staking, staking through a centralized service provider (cSSP), such as a centralized exchange or a professional direct staking delegation company like Kiln, and staking through a decentralized service provider (dSSP) that provides additional DeFi yields through an LST, such as Lido. We do not model restaking explicitly.

Each type of ETH holder has different staking options based on their level of expertise. In principle, Retailers stake exclusively through a centralized staking service provider (cSSP); Techies choose between a cSSP and a decentralized provider (dSSP); and Experts can access the full range of options, including solo staking.

However, we model revenues, cost and preferences that results in a segmented staking market. That is, each ETH holder selects a single staking method or stays out, and does not diversify across options. Specifically:

- Retailers either stake with a cSSP or abstain, reflecting a preference for ease of use and limited technical capacity.
- Techies prefer dSSPs over cSSPs because they receive higher returns from LSTs. That is, we model revenue and cost functions such that Techies’ profits are larger than Retailers’s ones.
- Experts are assumed to exclusively choose to solo stake—despite potentially lower profits—due to an intrinsic (but unmodeled) utility derived from contributing to decentralization. As a consequence, Experts solo stake or leave the staking market.

Note that segmented staking markets are also considered in other studies, such as [Kotelskiy et al. (2024)](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992). Also note that we do not model the staking decision as a portfolio allocation problem. Instead, each ETH holder allocates their entire stake to the option that yields the highest utility for their type. This framework emphasizes clear segmentation rather than hybrid strategies. An alternative approach could involve portfolio management. In that case, the model presented below would require modifications to avoid corner solutions—for example, by explicitly incorporating Experts’ intrinsic preferences for decentralization.

## Staking Revenues

Depending on the staking option they choose, ETH holders may receive revenues from three different sources: 1) consensus layer revenue, 2) MEV revenue, and 3) additional DeFi yield.

The first is **consensus layer revenue**, determined by the protocol’s issuance schedule. The annual consensus yield provided to an ETH holder i when staking is denoted as y_i(D). Under the current issuance schedule, the annual consensus yield is given by

y_i(D) = \frac{cF}{\sqrt{D}} = \frac{2.6 \cdot 64}{\sqrt{D}},

where D represents the total amount of ETH staked in the protocol. In later sections, we will compare model outcomes under the current issuance schedule y_i(D) to those under an alternative specification y_i'(D).

The second revenue source is **MEV revenue**. Validators selected as proposers in block production can extract additional revenue from structuring transactions, referred to in the following as MEV revenue. Letting N = D/32 denote the total number of validators, the probability that an ETH holder controlling d_i/32 validators is chosen as a proposer is d_i/D. Conversely, if a staker joins a staking pool (i.e. stakes with an intermediary), proposers may share MEV revenues with others in the pool. The probability that any validator in the pool is selected as a proposer is d_{pool}/D, and a validator with stake d_i receives a share of d_i/d_{pool}. Thus, the expected MEV revenue for a staker in a pool remains the same as for a solo staker. In both cases the expected annual MEV revenue y_v for an ETH holder is theoretically given by

y_v \cdot \frac{d_i}{D}.

The third source of revenue is additional **DeFi yield**. ETH holders utilizing a dSSP may earn additional yields by reinvesting the LST they receive. The annual yield from this source of revenue is simply defined as y_d.

## Staking Costs

From the perspective of the ETH holder, staking is associated with different costs. In the present model, the cost function faced by an ETH holder is allowed to differ for each staking solution. We define a cost function that include fixed costs and non-linear variable costs

C(d) = C+c\,d^{\alpha}.

Later, we calibrate the model looking for the set of parameters that gives a similar distribution of staking supply than the one observed in the market at the moment of this study. We also assume that the costs functions are such that there are interior solutions. This assumption is standard in models where agents face no binding constraints on their choices, such as budget constraints.

Furthermore, ETH holders staking through an intermediary incur **fees**, which are modeled as a tax on revenues and as such treated separately from the cost functions. The cSSP fee rate is denoted as f_c, and the dSSP fee rate as f_d, both of which are assumed to be exogenous in the baseline model. As such, fees are simply assumed to be fixed and not determined by the strategic behavior of the staking service providers in the market. Subsequent extensions will relax this assumption and to some extent allow fees to be determined as a function of the profit maximization problem of the staking service providers in the model.

## Staking Decisions

Under the assumption of a constant ETH price, thus isolating staking decisions from price volatility and inflation effects, each staker maximizes expected annual profit.

Given the deposits of other stakers \{d_{ss},d_r,d_t\}, a representative **Expert** chooses a deposit \hat{d}_{ss}\geq 0 to maximize

\max_{\hat{d}_{ss}}\, \Big\{ y_i(D)\,\hat{d}_{ss} + y_v\, P_{ss}(D) - \Big(C_{ss}+c_{ss}\,\hat{d}_{e}^{\alpha_{ss}}\Big) \Big\},

with

P_{ss}(D)=\frac{\hat{d}_{ss}}{\hat{d}_{ss}+(N_{ss}-1)d_{ss}+N_r d_r+N_t d_t},

and such that their profits are not negative (negative profits implies no staking).

Let P_{ss}(D) denote the probability that a staker with deposit \hat{d}_{ss} becomes a proposer. We model this probability as the ratio of the staker’s deposits to the total deposits, as indicated in the denominator. However, a more accurate representation would model this as the ratio of the number of validators controlled by the staker to the total number of validators. This would require a step function that increments with every 32 ETH, corresponding to the validator activation threshold. For tractability, we instead model P_{ss} as a continuous function of \hat{d}_{ss}, which simplifies the analysis.

\hat{d}_{ss}^* denotes the optimal choice of the maximization problem. Due to homogeneity within each staker type category, all Experts must choose the same deposit level in equilibrium. That is, in equilibrium, the individual optimal choice \hat{d}_{ss}^* satisfies \hat{d}_{ss}^* = d_{ss}.

Similarly, each **Techie** chooses a deposit \hat{d}_{t}\geq 0 to maximize

\max_{\hat{d}_{t}}\, \Big\{ (1-f_d)\Big[y_i(D)\,\hat{d}_t + y_v\, P_t(D)\Big] + y_d\, \hat{d}_t - \Big(C_{t}+c_{t}\,\hat{d}_t^{\alpha_{t}}\Big) \Big\},

with

P_t(D)=\frac{\hat{d}_{t}}{N_{ss}\,d_{ss}+\hat{d}_t+(N_t-1)d_t+N_r d_r}.

Homogeneity again implies \hat{d}_t^*=d_t. Notice that this type of staker pays a fee f_d and enjoys of DeFi yields y_d.

**Retailers** choose a deposit \hat{d}_{r}\geq 0 to maximize

\max_{\hat{d}_{r}}\, \Big\{ (1-f_c)\Big[y_i(D)\,\hat{d}_r + y_v\, P_r(D)\Big] - \Big(C_{r}+c_{r}\,\hat{d}_r^{\alpha_{r}}\Big) \Big\},

with

P_r(D)=\frac{\hat{d}_{r}}{N_{ss}\,d_{ss}+N_t\,d_t+\hat{d}_r+(N_r-1)d_r}.

Again, homogeneity implies \hat{d}_r^*=d_r.

Depending on their type, these ETH holders make strategic decisions about how much ETH to stake. In effect, they choose their profit-maximizing supply of staked ETH taking into account their costs and fees to pay, and their expected revenues while anticipating the staking behavior of the other agents. The [full paper](https://arxiv.org/abs/2503.14385) provides a detailed description of the model and the derivation of the resulting Nash equilibrium.

These above staking decisions define the strategic behavior of different agent types in the baseline model. However, real-world staking is subject to additional complexities, which we now introduce as model extensions.

## Model Extensions

We extend the baseline model in several key ways, adding important details to the characteristics of staking agents as well as the intermediary market (please refer to the [full report](https://arxiv.org/abs/2503.14385) for a formal description of these extensions):

- Variability in MEV rewards for solo stakers: We assume that the staking type Expert is risk-averse and experiences a disutility from the variance in MEV revenues. The profit maximization problem for the other staker types remains unchanged. This formulation accounts for the fact that solo stakers may require several years to propose a block with high MEV, unlike other stakers in a pool who can benefit from smoothing MEV revenues over time.
- Non-strategic staker type: We divide the Retailer category into two subgroups: (1) institutions and (2) inattentive retail investors. The latter group is assumed to be unresponsive to changes in the issuance yield, meaning they do not behave strategically. This behavior could stem from their inelasticity, but a more realistic interpretation is that they are inattentive agents or that their profit-maximizing decisions result in a corner solution (staking either all or none). The primary purpose of incorporating this type of agent into the model is to assess how their presence influences the staking behavior of other types, particularly solo stakers.
- Intermediary SSPs with market power: Finally, we add complexity to the intermediary market for staking providers by incorporating intermediary dSSPs with market power. In the baseline model, it is assumed that staking fees are fixed and as such that dSSPs operate under perfect competition and that they themselves provide the staking service. A more realistic approach would model dSSPs as intermediaries or middleware between stakers and centralized staking service providers (cSSPs). For example, when an ETH holder decides to stake with Lido, the stake is managed through a cSSP. Lido itself does not directly provide the staking service; instead, it facilitates the connection between the ETH holder and the cSSP. In this arrangement, the ETH holder benefits from Lido by receiving a derivative representing their stake. The following figure illustrates this setup in a simplified form.

 **Figure 1: Market structure with dSSPs as middleware**

[![Figure 1: Intermediary Market Structure](https://ethresear.ch/uploads/default/optimized/3X/c/8/c86f8ba52c6c03923be97810674980b634b710bf_2_690x270.jpeg)Figure 1: Intermediary Market Structure1280×501 28 KB](https://ethresear.ch/uploads/default/c86f8ba52c6c03923be97810674980b634b710bf)

## Results

To assess how different issuance schedules impact equilibrium staking decisions, we compare staking outcomes under two alternative issuance rules. The first issuance schedule corresponds to the one currently implemented by the Ethereum protocol:

y_i(D) = \frac{2.6 \cdot 64}{\sqrt{D}},

where D represents the staking deposit level. The second issuance schedule follows one of the alternative proposals presented by [Elowsson (2024)](https://ethresear.ch/t/reward-curve-with-tempered-issuance-eip-research-post/19171):

y'_i(D) = \frac{2.6\cdot 64}{\sqrt{D} \cdot (1+k\cdot D)},

where k=2^{-25} and D again represents the total amount of ETH staked.

These schedules might influence staking incentives differently. Before comparing the equilibrium staking decisions, we first conduct numerical simulations to better understand the forces behind the impact of transitioning from y_i(D) to y'_i(D).

### Numerical Simulations

We run extensive simulations of the baseline model, randomly varying all parameters across 10 million runs. These simulations provide insight into how different parameters influence equilibrium adjustments when moving from y_i(D) to y'_i(D).

Our key findings are as follows:

- Observation 1: Higher marginal costs lead to smaller adjustments in the equilibrium staking supply when transitioning from y_i(D) to y'_i(D). This effect is illustrated in Figures 2a - 2c, using solo staking as an example.
- Observation 2: The presence of additional MEV revenues or DeFi yields dampens stakers’ responses to changes in the issuance schedule.  Figures 2d and 2e illustrate this effect using staking via dSSP as an example.
- Observation 3: The sensitivity of different agent types to changes in the issuance schedule is interdependent.  For instance, when Techies become less sensitive to issuance schedule changes—such as when additional DeFi yields are high—the sensitivity of Experts to a change in the issuance schedule increases. Figures 2f illustrates this effect.

 **Figure 2: Relationship between cost parameters and change in equilibrium staking decision**

[![Figure 2](https://ethresear.ch/uploads/default/optimized/3X/7/c/7c714fefae76dea58f2599bb1b88055347b198e6_2_690x468.png)Figure 21545×1050 134 KB](https://ethresear.ch/uploads/default/7c714fefae76dea58f2599bb1b88055347b198e6)

*Note: The plots display the binned average percentage change in the total staking supply of different staking methods when transitioning from y_i(D) to y'_i(D), categorized by different levels of model parameters. The number of bins is set to 20.*

The simulations provide preliminary insights, but a structured comparison of equilibrium outcomes under the different issuance schedules is necessary. We now move to a comparative analysis that incorporates additional model refinements.

### Model Calibration

We calibrate the model with specific parameters and compare Nash equilibria under two issuance schedules. Given the number of parameters to be calibrated, we find that estimating model parameters based on a method of simulated moments, i.e., algorithmically setting parameters to minimize the distance between simulated and observed market shares, does not provide a stable best fit. In other words, we find that a variety of possible parameter combinations can yield simulated market shares that are consistent with the observed data (see [full report](https://arxiv.org/abs/2503.14385) for more details).

As a second best approach, we propose parameter settings which are consistent with our qualitative understanding of the Ethereum staking market and that in the baseline model achieve a close fit to the observed market shares of the different staking types reported in Table 2. To shape our qualitative understanding, we conducted a [survey](https://www.reddit.com/r/ethstaker/comments/1dneiy3/solo_stakers_questionnaire/) for solo stakers on the Reddit forum *r/ethstaker*.

 **Table 2: Reference staking distribution used in parameter calibration**

| Staking Method | M ETH | % |
| --- | --- | --- |
| dSSP | 18 | 54.1% |
| cSSP | 14.4 | 44.6% |
| Solo Staking | 0.9 | 2.7% |
| TOTAL | 34.2 |  |

*Note: The estimated number of validators is based on a simplification of the categorization reported by [Kotelskiy et al. (2024)](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992) and is calculated as the amount of staked ETH divided by 32. We categorize DSMs, LRTs, Whales, and Unidentified as dSSPs. Meanwhile, cSSPs consist of CSPs and CeXs.*

Importantly, we assume solo staking incurs fixed costs, while staking via a dSSP or cSSP does not:

C_{ss} = 0.4,\quad C_{t} = 0,\quad C_{r} = 0.

Contrary to staking through an intermediary, solo staking requires an individual to set up an Ethereum node with a running consensus and execution client. To do this, solo stakers can purchase dedicated hardware, subscribe to a cloud computing service, or use existing hardware. The costs associated with each of these options vary substantially. To further complicate matters, a range of hardware specifications can be used to run a node, each with varying costs. To date, the literature has made highly simplifying assumptions about the hardware costs of solo validators. In particular, both [pa7x1 (2024)](https://ethresear.ch/t/the-shape-of-issuance-curves-to-come/20405) and  [Kotelskiy et al. (2024)](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992) assume that a solo staker factors in 1000 USD to initially purchase the necessary hardware, which they amortize over a period of 5 years. The anecdotal evidence collected from the survey on *r/ethstaker* generally supports this assumption but also reveals substantial variation owing to the fact that some stakers use existing hardware and do not purchase dedicated hardware for staking.

Similar to hardware costs, we assume costs for energy and internet to be fixed, since they are a fundamental requirement to running an Ethereum node but do not scale when adding additional validators to a node. Again, [pa7x1 (2024)](https://ethresear.ch/t/the-shape-of-issuance-curves-to-come/20405) and  [Kotelskiy et al. (2024)](https://ethresear.ch/t/maximum-viable-security-a-new-framing-for-ethereum-issuance/19992) assume around 1.4 to 2 USD in energy costs per week and around 0 to 12 USD per week for internet costs. These assumptions are generally supported by the anecdotal evidence from the *r/ethstaker* survey. However, there is likely substantial variation, since it is difficult to assume that hobbyist solo stakers would explicitly monitor and base their staking decisions on the internet and energy consumption of their solo staking setup.

Taken together, we assume fixed costs of \approx 1'000 \$/year. This includes hardware which is usually assumed to be amortized in 5 years (200-400 \$/year), high-speed and stable internet connection (50 \$/month), and additional electricity expenditures (100 \$/year). Denoting this cost in terms of ETH, at a price of ETH in USD of 2’400 USD, we obtain a parameter setting of C_{ss} = 0.4. Again, we assume that staking through an intermediary does not create any fixed costs from the perspective of the ETH holder. Thus, we set C_{r} = 0 and C_{r} = 0.

We further assume

c_{ss} < c_{t} < c_{r} \quad \text{and} \quad \alpha_{ss} > \alpha_{t},\ \alpha_{ss} > \alpha_{r},\ \alpha_{t} = \alpha_{r}.

The literature is much sparser on the variable costs of the various staking methods. As a result, we rely primarily on anecdotal evidence and simplifying assumptions. We argue that imposing the above conditions may be reasonable when considering maintenance costs of solo staking. As the number of validators increases, complexity and operational overhead may increase non-linearly. For example, more validators require better network management. Managing and updating multiple nodes, as well as handling security patches and upgrades, requires more effort as the infrastructure scales. Based on the results of the *r/ethstaker* survey, it is also plausible to assume that, at least at lower levels of staking, stakers are hobbyists and do not price in maintenance and upkeep costs. As staking operations increase in size, we expect that individual stakers begin to price in maintenance and upkeep costs when choosing their optimal.

Moreover, we assume that the variable costs for staking via a cSSP exceed those for staking via a dSSP. This assumption is based on the observation that, in addition to the inherent risks of staking (e.g., slashing risks), centralized exchanges introduce additional custodial risks—risks that are absent in decentralized staking service providers such as Lido, which do not take custody of users’ assets. In addition, institutional stakers staking via a centralized solution may accrue additional legal costs. Finally, we assume that \alpha_{j} > 1 for all staking methods j. This allows for concave profit functions such that there are interior solutions. This assumption is standard in models where agents face no binding constraints on their choices, such as budget constraints.

Overall, due to the argumentative nature of our calibration approach, we argue that the results presented below should not be interpreted as predictive point estimates. Rather, the focus should be on the relative changes and dynamics observed between the Nash equilibria under the two issuance schedules being considered.

The table below summarizes the parameter settings chosen for the subsequent comparative analysis.

**Table 3: Summary of parameter settings**

| Parameter | Description | Parameter Value |
| --- | --- | --- |
| N_{ss} | Number of agents of type Expert | N_{ss} = 25'000 |
| N_t | Number of agents of type Techie | N_t = 200'000 |
| N_r | Number of agents of type Retailer | N_r = 925'000 |
| y_{v} | Annual MEV revenue | y_{v} = 300'000 |
| y_{d} | Annual DeFi yield | y_{d} = 0.02 |
| f_d | Fee dSSP | f_d = 0.1 |
| f_c | Fee cSSP | f_c = 0.25 |
| C_{ss} | Fixed cost parameter solo staking | C_{ss} = 0.4 |
| c_{ss} | Variable cost parameter solo staking | c_{ss} = 0.00053 |
| \alpha_{ss} | Exponent cost function solo staking | \alpha_{ss} = 2 |
| C_{t} | Fixed cost parameter for Techie staking via dSSP | C_{t} = 0 |
| c_{t} | Variable cost parameter for Techie staking via dSSP | c_{t} = 0.0038 |
| \alpha_{t} | Exponent cost function for Techie staking via dSSP | \alpha_{t} = 1.5 |
| C_{r} | Fixed cost parameter for Retailer staking via cSSP | C_{r} = 0 |
| c_{r} | Variable cost parameter for Retailer staking via cSSP | c_{r} = 0.0048 |
| \alpha_{r} | Exponent cost function for Retailer staking via cSSP | \alpha_{r} = 1.5 |

### Staking Outcomes

With this calibration, we examine Nash equilibrium staking behavior under each issuance schedule. We highlight the key findings when we consider the model including solo stakers’ exposure to a higher MEV variability and the presence of inattentive retail stakers. Results of the baseline model and/or the model without inattentive retailers can be found in the [full report](https://arxiv.org/abs/2503.14385).

The results are presented in the table below:

**Table 4: Comparison of Nash equilibria of extended model across different issuance schedules**

| Types | Num | yi(D) | y'i(D) | Δ | Deps | Ratio | Profita | Deps | Ratio | Profita | Deps | Profit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ss | 25K | 0.8M | 2.4% | 0.6% | 0.57M | 2.2% | 0.0% | -26.9% | -100% |  |  |  |
| t | 200K | 18.1M | 54.7% | 1.8% | 13.7M | 53.3% | 1.6% | -24.3% | -11.1% |  |  |  |
| i | 300K | 7.7M | 23.3% | 1.0% | 4.9M | 19.1% | 0.8% | -36.4% | -20.0% |  |  |  |
| r | N/A | 6.5M | 19.6% | N/A | 6.5M | 25.3% | N/A | 0.0% | N/A |  |  |  |
| Total |  | 33.1M |  |  | 25.7M |  |  | -22.4% |  |  |  |  |

The following observations can be made:

- Observation 4: The overall staking supply falls by 22.4%, which is less than in the baseline model where all ETH holders act strategically (see full report). This can be explained by the fact that we are assuming that a fraction of stakers do not respond to changes in the issuance curve.
- Observation 5: ETH Holder types who do adjust their supply lose market share under the new schedule.  When one ETH holder type does not modify its staking supply in response to an issuance reduction, i.e. is particularly inelastic, the adjustments made by the other more elastic types tend to become more pronounced. Notably, Experts (solo stakers) see a larger reduction than Techies, who benefit from external DeFi yields, resulting in even lower staking profits per ETH for Experts. In addition, the relative decrease in deposits for techies (-24.3%) is greater than the relative decrease for retailers and institutions (-19\%= 2.8/(6.5+7.7)). On this basis, it can be argued that the level of decentralization in the network could suffer as a result of a change in the issuance schedule in that the market share for decentralized staking solutions declines to a greater extent than the market share for centralized solutions, such as those offered by centralized exchanges.
- Observation 6: Even under the current issuance schedule, solo stakers have lower profits per ETH staked than Techies or Retailers. While outside of the scope of the model, solo stakers therefore have economic incentives to switch to being Techies or Retailers, with the incentives being stronger for joining the Techie group. If solo stakers choose not to switch, this may be due to preferences for decentralization or altruism (which in this case is captured by the assumed market segmentation).
- Observation 7: Despite reduced staking supply, all ETH holder types face lower profits per ETH under the adjusted issuance schedule. Solo stakers are the most affected by this decline, primarily due to the cost function assumed for them, which includes fixed costs and higher average costs. If fixed costs were excluded, the decrease in solo stakers’ profits would be less severe.
- Observation 8: The reduction in the issuance yield brings solo stakers from a positive expected profit situation to one with negative profits. This could imply a migration from solo staking to other staking alternatives, which would further reduce decentralization, especially if some solo stakers become Retailers. Again, this is outside the scope of the model and by assuming a segregated market, we essentially assume a strong preference for decentralization among solo stakers which entirely limits this migration.

### Intermediary dSSPs with Market Power

We examine how an intermediary dSSP with market power might influence staking behavior, focusing not on solving for its optimal fee but on the direction in which its fee should adjust after a change in the issuance schedule.  That is, we first calculate dSSP’s profits under the current issuance schedule and the fee assumed in the baseline model. Then, under the updated issuance yield curve, we simply identify the new fee as the fee that would yield a similar profit, and then use that fee to derive the new staking equilibrium. We leave the incorporation of the dSSP’s strategic decision-making into the model for future research.

The table below reports the results of the comparative analysis:

**Table 5: Nash equilibria of extended model with intermediary dSSP**

| Types | Num | yi(D); fd = 10% | y′i(D); fd = 13% | Δ | Deps | Ratio | Deps | Ratio | Deps |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ss | 25K | 0.9M | 2.4% | 0.6M | 2.2% | -26.9% |  |  |  |
| t | 200K | 18.0M | 54.5% | 13.4M | 52.5% | -25.5% |  |  |  |
| i | 300K | 7.7M | 23.3% | 5.0M | 19.6% | -35% |  |  |  |
| r | NA | 6.5M | 19.7% | 6.5M | 25.5% | 0.0% |  |  |  |
| Total |  | 33.1M |  | 25.5M |  | -22.7% |  |  |  |

Again, several observations can be highlighted:

- Observation 9: The dSSP (Lido) responds with an increment of 30\% in f_d after the reduction in the issuance yield.
- Observation 10: The staking distribution becomes more concentrated. The increase in f_d primarily impacts stakes from Techies, reducing their participation (see comparison with the previous table). Institutions, in turn, benefit from this reduced Techie participation, increasing their staking level by compared to the equilibrium with fixed fees—approximately equivalent to the decrease in Techie participation. Since cSSPs are the providers for Institutional stakes, this shift leads to greater concentration within the staking market.

# Discussion

In general, the analysis presented above may be best suited for capturing short-run dynamics and it may not fully reflect long-term market shifts. By construction, the empirical estimation of yield elasticities of staking supply capture short-term changes in staking supply driven by short-term fluctuations in staking rewards. In addition, the game-theoretic model is based on a fixed market segmentation of ETH holder types and does not allow switching between staking methods. Still, our analysis may be able to capture important short-term effects of a change in the issuance schedule on the dynamics in the Ethereum staking market.

Both the empirical evidence and the comparative analysis of the theoretical model suggest that solo stakers respond more strongly to yield changes than ETH holders who stake via centralized providers or liquid staking providers. Therefore, under a reduced issuance schedule, the market share of solo staking is expected to decline while that of centralized exchanges is expected to rise. This would have important effects on the degree of decentralization of the Ethereum validator set.

In addition, the game-theoretic model helps clarify why solo stakers could be more sensitive to changes in consensus yields. Other staking methods have a competitive advantage in the market through better MEV access and DeFi yields, making them less elastic and indirectly leading to an increased sensitivity of solo stakers and a crowding-out effect when issuance adjusts. This underscores the need to consider measures like MEV burn alongside issuance changes, as they could play an important role in mitigating the competitive disadvantages of solo stakers and as a result the negative effects of an issuance reduction on solo stakers.

Finally, the reduced issuance schedule  lowers the profitability of solo staking compared to other staking categories. While long-run effects are outside the scope of our model, this could lead to exits or shifts to alternative staking solutions (e.g., dSSPs offering additional DeFi yields) in the long-run.

We expect this model to serve as a foundation for future research and extensions. For instance, a future iteration could provide a more detailed characterization of the strategic behavior of intermediaries and different types of staking service providers. As shown above, these entities play a crucial role in shaping how the aggregate staking market responds to changes in issuance, making their inclusion essential for a more comprehensive analysis.

# References

- Properties of issuance level: Consensus incentives and variability across potential reward curves
- Endgame Staking Economics: A Case for Targeting
- Impact of consensus issuance yield curve changes on competitive dynamics in the ethereum validator ecosystem
- Reward curve with tempered issuance
- Maximum viable security: A new framing for ethereum issuance
- The shape of issuance curves to come
