---
source: ethresearch
topic_id: 253
title: "Perceived Risk/Reward Ratio: Improving the Sharpe Ratio"
author: jonchoi
date: "2017-11-26"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/perceived-risk-reward-ratio-improving-the-sharpe-ratio/253
views: 2517
likes: 4
posts_count: 5
---

# Perceived Risk/Reward Ratio: Improving the Sharpe Ratio

This came out of session with [@vladzamfir](/u/vladzamfir) earlier this week.

In financial theory, we can roughly approximate how compelling an investment is by comparing the returns (excess of risk-free rate) to a proxy of risk (commonly the standard deviation of the returns i.e. Sharpe ratio).

Therefore, comparing returns / risk is a common way to compare various assets in portfolio theory. However, that approach is often limited to one perspective of what risk is. Therefore, when discussing a heterogenous validator set, Sharpe ratio is far too simplistic to model a validator’s risk assessment. While we will continue to improve this definition, here is a proposed working model of a validator’s perception of risk:

 \delta_i = \frac{\sigma_{perfect} + \sigma_{error}}{1-p_{byzantine}} * (1+b_i)

*Perceived risk proxy with respect to (1) risk of the perfect game, (2) unknown risk, (3) perception of byzantine peers, and (4) portfolio concentration risk*

where:

- \delta_i  is a behavioral model of a validator’s own view of the perceived risk of participation at any given point.

While a validator’s perspective may change at any point, it can act only decide to participate, stay or exit. There will be another section that handles withdrawal delay and related costs to staying & exiting (and consequently participating)

 \sigma_{perfect}  is the theoretical standard deviation of being a validator (i.e. perfect execution).

- Should be same a priori and a posteriori.
- Just using this would result in a Sharpe ratio.

 \sigma_{error}  is the additional risk due to perceived errors outside of the game (i.e. client bugs, new systems).

- Highest a priori and should asymptotically approach zero a posteriori (validator bugs or commonplace aversion to new processes).

  p_{byzantine}  is the validator’s perceived proportion of byzantine validators in the validator set.

- It is a proxy for the common prior assumption in Bayesian games (with incomplete information).
- This will diverge to either a honest supermajority or a byzantine quorum over an iterated game, but the perception of this state on any given round will affect the marginal validator’s perceived risk.
- \frac{1}{1 - p_{byzantine}} can range from 1 when there is full belief that they are honest to larger multiples of risk when people believe there are significant byzantine proportion of actors).
- This magnifies the overall risk. We can tune the relationship with a constant k_0 as well.
- Also, we can replace  1 - p_{byzantine}  with  k_{byz} - p_{byzantine}  where k_{byz} is the byzantine quorum threshold of \frac{1}{3}.

 b_i  is a proxy for portfolio concentration and need for diversification & liquidity. We can begin this by approximating `amount validated / total investment budget` for a given validator (without having optimized, let’s start the framework at [up to double the risk for going “all-in”]).

- This will model how an investment with the same Sharpe ratio equivalent will make the investment far more risky for someone with a lower total investment budget and therefore makes a given absolute amount investment more risky as a percentage of their portfolio.
- For example, the same $25k angel investment in a startup is exceedingly more risky for someone with $100k vs $100m in wealth. So for a given sharpe ratio, validators will need to be more risk-taking to invest in an asset with a higher % of its own investment budget. This proxy reflects that.
- This proxy will come in handy when we discuss heterogenous wealth/income distribution of validators.

While WIP, we can imagine replacing the Sharpe Ratio with this proxy ratio (*name tbd*, `PRR` ratio below; for “Perceived Risk/Reward” ratio) that captures various factors that model validator perceived risk.

PRR = \frac{r_v - r_f}{\delta_i}

where high V values represent a more compelling mechanism for validators. (where r_v is risk of validation and \delta_i is defined above. r_f is mentioned for completeness)

## Replies

**djrtwo** (2017-11-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonchoi/48/165_2.png) jonchoi:

> where high V values represent a more compelling mechanism for validators

What is “V” defined as?

also,

Where is the volatility of the underlying asset (ether) taken into account? Validators are making two levels of risk assessment. First, “do I think ether will appreciate during the length of time I will be a validator (or at least remain stable)” and then “is the return of validating worth the associated risks”.

Or do we just encapsulate this extra level of risk in r_v and/or \sigma_{perfect}?

---

**djrtwo** (2017-11-29):

Another quick question…

This ratio allows us to compare different settings and states of the network against each other, but it does not allow a validator to compare the investment of being a validator with other traditional investments, correct?

I suppose it is generic enough to allow a validator to compare against staking in various protocols. “I’m interested in staking in X-coin, Y-coin, and Z-coin… let me use the Choi ratio to decide which protocol to stake in”

---

**jonchoi** (2017-12-08):

Thanks for the thoughtful questions [@djrtwo](/u/djrtwo)! Sorry for the delay.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> What is “V” defined as?

Think it must have been a typo. Just “high values”

Regarding the two questions below, you’re spot on that **this framework in its current form is only intended for comparing various optimizations of the same mechanism (e.g. Casper)**.

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> This ratio allows us to compare different settings and states of the network against each other, but it does not allow a validator to compare the investment of being a validator with other traditional investments, correct?
>
>
> I suppose it is generic enough to allow a validator to compare against staking in various protocols. “I’m interested in staking in X-coin, Y-coin, and Z-coin… let me use the Choi ratio to decide which protocol to stake in”

Yes, byzantine behavior doesn’t apply to equities or bonds for example. However it could theoretically be replaced with equivalent game theoretic risk (risk of investment outside of the observed standard deviation of the returns). Risk of an investment in Uber with respect to Lyft’s strategy etc or the risk of Travis Kalanik’s actions. Doesn’t translate 100% but you get the idea.

However, the portfolio concentration still applies to various asset classes. This affects how various socioeconomic classes have access to and participate in various asset classes (i.e. accredited investors have separate access to higher risk/reward asset classes and can get richer quicker in success cases).

![](https://ethresear.ch/user_avatar/ethresear.ch/djrtwo/48/12_2.png) djrtwo:

> Where is the volatility of the underlying asset (ether) taken into account? Validators are making two levels of risk assessment. First, “do I think ether will appreciate during the length of time I will be a validator (or at least remain stable)” and then “is the return of validating worth the associated risks”.
> Or do we just encapsulate this extra level of risk in r_v and/or \sigma_{perfect}?

Yep, this should be included if trying to compare staking in different networks.

---

**nisdas** (2017-12-18):

Hey is it needed to actually use b_i when trying to ascertain the validator’s perception of risk when staking their ether ?

Adding the concentration of their portfolio to this seems out of place as we are trying to find a risk-adjusted return specifically for this ‘operation’ and not including any other assets that the validator might have in their portfolio. I feel that  if a validator is looking at their total risk profile of their portfolio it will look some thing like this :

 \delta_v = w_1\delta_1 + w_2\delta_2 + w_3\delta_3  ..... w_i\delta_i  where w is the weight of the asset in the portfolio and \delta is the associated risk with that asset.

I feel that if we are looking at diversification and liquidity of the whole portfolio , we would have to look at the risk profile of all the various assets in the validator’s portfolio. Then the associated risk that would come about from staking ether specifically would end up becoming:

\delta_i = \frac{\sigma_{perfect} + \sigma_{error}}{1-p_{byzantine}}

Then using this for the `PRR` ratio would seem more rational as you are looking at the risk adjusted return for specifically this ‘investment’ and not including other assets that the validator might have in his\her portfolio

