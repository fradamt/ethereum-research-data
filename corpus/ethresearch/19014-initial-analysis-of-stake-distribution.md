---
source: ethresearch
topic_id: 19014
title: Initial Analysis of Stake Distribution
author: Julian
date: "2024-03-15"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/initial-analysis-of-stake-distribution/19014
views: 3182
likes: 27
posts_count: 13
---

# Initial Analysis of Stake Distribution

Many thanks to [Caspar](https://twitter.com/casparschwa?s=21&t=YeRrbBitxQ2f6XFXk1HmMg), [Ansgar](https://twitter.com/adietrichs?s=21&t=YeRrbBitxQ2f6XFXk1HmMg), [Barnabé](https://twitter.com/barnabemonnot?s=21&t=YeRrbBitxQ2f6XFXk1HmMg), [Anders](https://twitter.com/weboftrees?lang=en) and [Thomas](https://twitter.com/soispoke?s=21&t=YeRrbBitxQ2f6XFXk1HmMg) for feedback and review. Review \neq endorsement.

## Introduction

Ethereum issues ETH to validators for performing their consensus duties. The amount of issuance depends on the amount of ETH staked. The current issuance curve may result in a very high long-term staking ratio. This post aims to analyze whether a change in the level of issuance, as [proposed to be implemented in the next Electra upgrade](https://ethereum-magicians.org/t/electra-issuance-curve-adjustment-proposal/18825), affects the distribution of staking mediums investors use. We differentiate between three mediums of staking: 1) investors may solo-stake, 2) investors may deposit their tokens with a decentralized staking service provider (SSP), or 3) investors may deposit their tokens with a centralized SSP. Subsequently, we define the cost structures of each staking medium. Finally, we model a linear programming problem in which an investor decides what fraction of their endowment to hold or stake via which medium based on the expected monetary return and an investor’s non-monetary preference, such as convenience, trust, and decentralization. Our main result is that the distribution of stake does not depend on the level of issuance. We show how the model can be used with two examples.

This post presents a minimum non-trivial model to analyze the distribution of stake with respect to the level of issuance. We refer the reader to this [post](https://ethresear.ch/t/properties-of-issuance-level-consensus-incentives-and-variability-across-potential-reward-curves/18448) for an explanation of why a change to the issuance curve may be useful. This post does not aim to discuss the motivation for an issuance reduction, nor does it aim to be maximally precise about the cost structures of different SSPs. What this post does aim to do is to ground the conversation around staking distributions in an addressable manner.

## Model

Consider an investor who receives a large endowment, E. It needs to decide how to invest this wealth. It can invest in a combination of the following products: solo-staking, “decentralized” SSP, “centralized” SSP, or simply holding the endowment.

We want to highlight the words decentralized and centralized because, in practice, the state of an SSP is not so binary. Decentralization is a spectrum, and an SSP may be more decentralized than other SSPs while still being more centralized than others. For simplicity, we assume an SSP is either decentralized or centralized.

Let y be the yield from issuance and MEV that each unit of stake accrues over some finite time interval.

## Cost Structure

Staking also incurs costs. The cost structure of the different staking mechanisms is given as

- Solo-Staking. Solo-stakers need to acquire hardware in order to function; we model this as a fixed cost solo-stakers incur, C^{Solo}_{F}. Furthermore, unlike SSPs, solo-stakers forgo the liquidity of their stake as they cannot issue liquid staking tokens (LSTs). We model this as a variable cost per unit of stake, C^{Solo}_{V}, that resembles the liquidity gap. The liquidity gap is the foregone returns that a solo-staker could have gotten if it were able to issue LSTs. Therefore, the cost function of a solo-staker is given by the following: S^{Solo} \geq 0 is the amount of solo-staked capital deposited by the investor.

C^{Solo} = C^{Solo}_{F} + C^{Solo}_{V} \cdot S^{Solo}

- Decentralized SSP. Decentralized SSPs must create nodes at different locations to remain decentralized. We assume that a decentralized SSP creates a new node for every K \cdot 32 ETH staked with the SSP. Furthermore, when staking with a decentralized SSP, the investor receives liquid staking tokens as a receipt for their provided capital, meaning that there is no - or little -  loss in the liquidity of capital. Therefore, we model the cost of a decentralized SSP as a step function that incurs a variable cost for every K \cdot 32 ETH staked with the decentralized SSP. X^{DSSP} > 0 is the amount of exogenous stake deposited with the decentralized SSP, and S^{DSSP} \geq 0  is the amount of stake deposited by the investor.

C^{DSSP} = C^{DSSP}_{V} \cdot \lfloor \frac{X^{DSSP} + S^{DSSP}}{32 \cdot K} \rfloor

- Centralized SSP. Centralized SSPs have negligible variable costs per unit of stake. However, they have large fixed costs, such as legal fees and infrastructure costs, that come with setting up a company to run a scalable staking operation. Moreover, stake deposited with a centralized SSP can also be exchanged for an LST. Thus, we model the costs of a centralized SSP as follows. In practice, we observe C^{CSSP}_{F} \gg C^{Solo}_{F}.

C^{CSSP} = C^{CSSP}_{F}

## Returns

The return on stake is given by the yield minus the costs. We assume SSPs *socialize* the costs and do not discriminate between stakers. Then, the yield on each unit of stake is defined as follows.

r^{i} = y - \frac{1}{X^{i} + S^{i}}C^{i}

where i = \{Solo, DSSP,CSSP \}. Furthermore, we define r^{Hold} = 0. Let r^{T} = \{r^{Solo},  r^{DSSP},  r^{CSSP}, r^{Hold}\} denote the vector of returns.

An investor measures its utility as follows

U = (r + \gamma)^{T} \cdot S

where S^{T} = \{S^{Solo}, S^{DSSP}, S^{CSSP}, S^{Hold}\} is the vector of stake and \gamma^{T} = \{ \gamma^{Solo}, \gamma^{DSSP}, \gamma^{CSSP}, \gamma^{Hold}\} is the preference vector of the investor. It represents factors that an investor cares about that are not expressed in yield, such as decentralization, trust, technical capabilities, and convenience. In this post, we assume that preferences are fixed and do not depend on other factors, such as other stakers or the level of issuance. In the discussion, we add more nuance to this assumption; therefore, we present it here as Hypothesis 1.

> Hypothesis 1. Investor’s preferences are independent of the level of yield.

## Main Results

The optimization problem of the investor is then given as

\max_{S} \quad (r + \gamma)^{T}S \\
\text{subject to} \quad S \in \mathbb{R}_{+}^{4} \\
\qquad 1^{T}S = E


This is a very simple linear programming problem. The Fundamental Theorem of Linear Programming states that if there is an optimal solution to a linear programming problem, and if the feasible region is non-empty and bounded, then there exists an optimal solution at one of the vertices of the feasible region. Therefore, solving the optimization problem is as simple as choosing the vertex that leads to the highest utility for the investor. This will lead to the investor depositing all assets in the maximum component of (r + \gamma). This leads us to our first result presented in Corollary 1.

> Corollary 1. If an investor decides to stake, it will stake its entire endowment via one medium.

We assume that an investor deposits their entire endowment with one staking medium in the event of multiple optimal solutions

The decision whether to stake or not depends on the level of issuance. If issuance is too low, an investor will opt to hold ETH instead of staking it. However, by using Hypothesis 1, it becomes clear that an investor’s choice of a staking medium does not depend on the level of issuance. Aggregating this across investors, we obtain our main result presented in Theorem 1.

> Theorem 1. The level of (issuance) yield does not affect the staking mediums used by individual stakers.

Informally, Theorem 1 supports the argument that competition between staking mediums is similar at every level of issuance. Therefore, a lower level of issuance, as proposed to be implemented in Electra, does not necessarily lead to a decrease in the number of solo stakers. Further research may expand this model into a game-theoretic model that includes frictions investors may see when (un)staking.

## Example

In this section, we consider two examples. The first example is of an investor who only cares about monetary gains and has no preferences for, e.g., decentralization or trust. It shows that this will lead to the investor depositing its assets with a centralized SSP (in the case of no rent extraction). The second example is of a solo staker. This example is constructed to show how the model allows putting a monetary amount on revealed preferences.

**Indifferent Investor**

Consider an investor who does not care about any non-monetary factors and solely wants to maximize returns. Let the preferences of this investor be given as \gamma = 0. We find then, by Lemma 1, that this investor deposits its entire endowment with the medium that gives the highest return. For this example, consider the price of 1 ETH to be 3000 USD and assume y = 4\% per year.

Solo-staking would cost the investor 1000 USD in fixed costs, depreciated over 10 years, so say 100 USD fixed per year. Furthermore, assuming the liquidity gap is 1\%, then the return for solo staking is roughly 2.9\% per year.

Suppose a decentralized SSP has variable costs of 3000 USD per node per year, and creates a new node for every 1,000,000 ETH deposited (K = 31,250). Assume there is 10 million ETH staked through this SSP. The reward for staking through the decentralized SSP is then around 3.7\%.

Finally, the centralized SSP has fixed costs of 10 million USD per year and it has 5 million ETH staked with it. The reward for staking with the centralized SSP is then around 3.9\%.

Therefore, the indifferent investor will choose to stake with the centralized SSP.

**Solo Staker**

Consider an investor who is a solo-staker. Furthermore, assume that r^{T} = \{r^{Solo}, r^{DSSP}, r^{CSSP}, r^{Hold}\} = \{2\%,  3\%,  4\%, 0\}, then we know that r^{Solo} +\gamma^{Solo} \geq r^{CSSP} + \gamma^{CSSP}  \implies \gamma^{Solo} \geq 2\%. Therefore, if this solo-staker has staked 32 ETH,  its preference for solo-staking is worth at least 0.64 ETH per year in monetary terms.

## Conclusion & Discussion

In conclusion, this model presents an investor’s optimization problem as a linear programming problem of the monetary and non-monetary returns that an investor will gain from depositing stake via a certain staking medium. Corollary 1 shows that an investor who stakes deposits their entire stake through one staking medium. Our main result is presented in Theorem 1. Since preferences do not depend on the level of yield, we find that the level of (issuance) yield does not affect the distribution of staking mediums used by investors. Although the model is very simple and does not consider frictions, this Theorem could be used to argue that a change in issuance, as proposed in Electra, will not change the distribution of staking mediums used.

The model presented in this post is meant as a minimum non-trivial model to analyze the distribution of stake with respect to the level of issuance. Clearly, this model is very simplified and makes idealized assumptions about the cost structure of different staking mediums. The intention is not to be maximally precise but to capture the core characteristics that differentiate staking types. This post aims to ground the conversation around staking distributions in an addressable manner. Further, this model’s assumptions can be adjusted accordingly, and the reader is invited to do so.

Finally, some other questions that might be considered are:

- How important are other investors’ investment decisions for an individual investor? For example, an investor’s preference for a staking medium may depend on the number of other investors who stake through it. Liquid staking tokens that are owned by more people could provide more use cases.
- As issuance reduces, which investors will unstake first? Potentially liquid stakers will unstake earlier as the SSP fees reduce future expected profits, whereas solo stakers’ costs can largely be considered sunk costs, thus not reducing future expected profits. In this podcast, Christine Kim and nixo.eth discuss that liquid staking protocols will likely see investors unstake their capital quickly as frictions are low. Solo stakers may not unstake as quickly as frictions are higher.
- Some of the investors’ preferences can potentially be endogenized into an extended model. How do preferences develop over time? Is there a potential survivorship bias in the preferences?

## Replies

**vshvsh** (2024-03-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> The decision whether to stake or not depends on the level of issuance. If issuance is too low, an investor will opt to hold ETH instead of staking it. However, by using Hypothesis 1, it becomes clear that an investor’s choice of a staking medium does not depend on the level of issuance. Aggregating this across investors, we obtain our main result presented in Theorem 1.
>
>
>
> Theorem 1. The level of (issuance) yield does not affect the distribution of staking mediums used by investors.

Aggregating that across multiple investors says that some of them will unstake earlier than others, changing the composition of the validator set.

Let’s adjust your example with two stakers, one indiffirent (no preference at all) and one with preference, with second one having \ \gamma^{Solo} = \gamma^{Hold} = 2\%. When y goes lower than 3.1\%, one of them will unstake and the other one won’t, changing the distribution of staking mediums used by investors.

I very much appreciate the direction though, I think we should do more models like this, and reality check them.

---

**pavelya** (2024-03-15):

Thanks for posting, cool to see research on the topic!

The assumption you make looks a little bit unrealistic to me, could you please explain your reasoning behind that in more detail?

> Investor’s preferences are independent of the level of yield.

My way of thinking:

Preferences (gamma) might depend on yield. Quality of staking services depend on the budget of SSP, which in its turn depends on the yield through fees (function of stake) that are charged & costs. Let’s say services introduce the same fixed cost for each operator. When the yield is high everyone can afford the same set of services and the competition is very narrow. Once we decrease the issuance, smaller operators one by one start losing the possibility to support initial set of services. Due to that gamma term starts skewing towards big SSPs. This is the thing that leads to further centralization.

I might be misunderstanding the model though, will appreciate your answer.

P.S. Likely I’m referring exclusively to issuance that is a part of the yield, what’s important to consider gamma’s dependence on (issuance yield, current stake)

---

**Julian** (2024-03-18):

Thanks for your reply. This is a valid point and the post is adjusted accordingly. The Theorem should state that the level of (issuance) yield does not affect the distribution of staking mediums chosen by stakers.

Then, the second point in the discussion proposes a method to study which investors are most likely to unstake first, effectively endogenizing certain preferences. Potentially this could be used for further study.

---

**Julian** (2024-03-18):

Thanks for your reply. This model is meant as an initial analysis and is simplified. Investors’ preferences may depend on yield. We see that the SSP market is already fairly centralized. An important consideration of an issuance reduction is ensuring that solo-stakers are not disproportionately affected.

This post assumes that staking mediums compete on returns and preferences are exogenous. Therefore, competition between staking providers is as intense with high issuance as with low issuance. So, it is unclear to me why competition would be narrow when yield is high, compared to when yield is low.

If certain SSPs go bankrupt, then it would be reasonable to say that preferences change. In this model, however, we assume three (types) of SSPs: decentralized, centralized, and solo-staking. Assuming that preferences are relatively stable over these types of SSPs, the results shouldn’t change much if you assume that one of the SSPs in a type goes bankrupt as long as there still are other SSPs of this type. Solo-stakers will not switch to SSPs.

It could be very interesting to see work that incorporates preferences that depend on issuance ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vshvsh** (2024-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Informally, Theorem 1 supports the argument that competition between staking mediums is similar at every level of issuance. Therefore, a lower level of issuance, as proposed to be implemented in Electra, does not necessarily lead to a decrease in the number of solo stakers. Further research may expand this model into a game-theoretic model that includes frictions investors may see when (un)staking.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Thanks for your reply. This is a valid point and the post is adjusted accordingly. The Theorem should state that the level of (issuance) yield does not affect the distribution of staking mediums chosen by stakers.

It does not prove that, or informally support that. On the contrary, in the very example you provide, if you assume non-negative preference vector, a “solo staker” will unstake before the “indifferent investor” as the issuance goes down, which means it does affect the distribution of staking mediums, and competition is not similar at different levels of issuance, even in this initial model.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Theorem 1. The level of (issuance) yield does not affect the staking mediums used by stakers.

If you consider holding as “staking medium”, this theorem is wrong. Otherwise, it’s probably better rephrased as

> Theorem 1. Each individual staker will either hold, or use the same staking medium regardless of yield.

Which is true in the model, but is a direct collorary from the definition of the actor and Hypothesis 1, and doesn’t tell much about the aggregate.

I think there’s a tad more interesting theorem to be had from that model, btw:

Let’s define  \gamma^{Hold}_{max}  to be the maximal preference for holding accross all stakers, and define  y_{max}  as such yield level so that returns for each staking medium are over  \gamma^{Hold}_{max} .

> Theorem 2. Increasing y over y_{max} will not change the distribuition of staking mediums.

Which reflects common sense of there being too much security budget - after some point increasing it further will not change the distribution of stakers at all.

NB I think the model must be more complex before it can be actually used to predict real market movements (e.g. explain why 25% fee on Coinbase is palatable to people but there’s a serious competition on fees between node operators), but that’s beyond the current point.

---

**NikNovo** (2024-03-19):

Great research! It’s great that this topic is getting attention. It effectively addresses the importance of significant changes directly related to the network’s decentralization from a generalized perspective.

Regarding the study, it’s a good first linear approx that can effectively address problematization tasks and vectors for further investigation.

As for the structure of staking itself, it’s much more complex, multi-layered, and quite nonlinear. Every entity in the system can be attributed to diff infrastructure, types of software, capital sources, management types, dependency on external factors, and many other metrics. This complexity is what makes the eth so fascinating. Imho it’s quite challenging to describe linearly.

However, this linear approach can also be improved, without delving into the structure itself, but through concepts.

1. In our view, it would be useful to replace the binary validator’s status with the “density” of “products,” and to update to “product inflow” and “product outflow.” This could partly smooth out behavioral effects (such as latency in losses, action delays, risk tolerance, etc.) and allow for the investigation of the impact of the system remaining in one state for an extended period. Simply put, the fact of halting new players’ entry means more than a total decrease in product population (where the effect has already gained momentum). It would also be interesting to look at the point where the direction changes, but the total outflow has not yet begun. Of course, such an approach can be considered in transferring the stake to a more efficient instrument (one man’s outflow another man’s inflow).
2. It appears that it would be interesting to calibrate the linear system at boundary conditions. This might introduce a behavioral factor into a sufficiently broad class and allow for basic clustering.

I hope you find this comment relevant.

---

**Julian** (2024-03-19):

With competition being similar at every level of issuance, I refer to the competition between staking mediums based on the yield level they can provide. This is similar at every level of issuance, and it is not the case that this competition is different for high levels of yield compared to low levels of yield. Assuming that the solo-staker you refer to has a positive preference for solo-staking, it will unstake later than an indifferent investor with 0 preferences. A lower level of issuance therefore does not lead to more solo stakers choosing another medium to stake.

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> If you consider holding as “staking medium”, this theorem is wrong. Otherwise, it’s probably better rephrased as

The adjusted version of Theorem 1 that you write is identical to the one written above, as the word “stakers” refers to people who stake, not investors who may hold ETH.

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> NB I think the model must be more complex before it can be actually used to predict real market movements (e.g. explain why 25% fee on Coinbase is palatable to people but there’s a serious competition on fees between node operators), but that’s beyond the current point.

I agree! Would be great to see more sophisticated models worked out.

---

**Julian** (2024-03-19):

Thanks for your reply!

I am not quite sure I understand what you mean by point 1. With the “binary validator’s status,” do you mean that the validator will choose one staking medium? How would you model product inflow and outflow?

It would be great to see more sophisticated models worked out ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vshvsh** (2024-03-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> With competition being similar at every level of issuance, I refer to the competition between staking mediums based on the yield level they can provide.

I don’t get what you mean her, can you explain? My understanding is in this model it is easy to show that, in general, different levels of base yield will result in different distribution of staking mediums. Which to me informally means that that competitive landscape changes and competition can be different in different level brackets of yield.

> Assuming that the solo-staker you refer to has a positive preference for solo-staking, it will unstake later than an indifferent investor with 0 preferences.

I crunched some numbers and it’s not true in general. Higher preference for holding can make them unstake earlier (in the example, they need it greater than 1.2% for to unstake before indifferent investor does). Consider this an example of “I love to run a node, but not into a loss” mindset.

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> The adjusted version of Theorem 1 that you write is identical to the one written above, as the word “stakers” refers to people who stake, not investors who may hold ETH.

It’s supposed to be identical in meaning, I just reformulated it. I think additional clarity is important to show it doesn’t actually state anything about the aggregate - just about an individual actor,

---

**NikNovo** (2024-03-20):

Thank you for your response!

In our view, it seems potentially interesting to specifically model the inflow into the "product "and the outflow from the “product”. To build separate models for each, whose superposition will provide the parameters present in the current model. And from these, construct the other aggregates.

*Broadly speaking,* the processes of changing profitability parameters have significantly different impacts on those entering and those inside (and can outflow/relocate). Changes first (should more) impact the incoming flow as more sensitive and only then does it compare it with the outflow cohort (where the outflow begins).

---

**Julian** (2024-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> I don’t get what you mean her, can you explain? My understanding is in this model it is easy to show that, in general, different levels of base yield will result in different distribution of staking mediums. Which to me informally means that that competitive landscape changes and competition can be different in different level brackets of yield.

I see what you say here but what I mean is that at any level of issuance, either an investor is willing to stake or it is not willing to stake. If the investor is willing to stake, it will choose the medium that gives it the highest utility. Therefore, these staking mediums compete on costs structures regardless of issuance level, even though some have larger shares of total staking ratio.

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> I crunched some numbers and it’s not true in general. Higher preference for holding can make them unstake earlier (in the example, they need it greater than 1.2% for to unstake before indifferent investor does). Consider this an example of “I love to run a node, but not into a loss” mindset.

Thanks for pointing this out. I was thinking about an investor with no preferences and an investor with a preference for solo-staking, keeping the other preferences equal.

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> It’s supposed to be identical in meaning, I just reformulated it. I think additional clarity is important to show it doesn’t actually state anything about the aggregate - just about an individual actor,

I adjusted the Theorem as well in case it wasn’t clear ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**vshvsh** (2024-03-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> I see what you say here but what I mean is that at any level of issuance, either an investor is willing to stake or it is not willing to stake. If the investor is willing to stake, it will choose the medium that gives it the highest utility. Therefore, these staking mediums compete on costs structures regardless of issuance level, even though some have larger shares of total staking ratio.

That’s true in the model but that’s basically your definition of staker. Before drawing real-world implications from this model I think it’s prudent to show that it actually fits what happens in reality, which I think it doesn’t.

