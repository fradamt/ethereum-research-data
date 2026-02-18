---
source: ethresearch
topic_id: 219
title: "Casper: CAPM & Validation Yield"
author: jonchoi
date: "2017-11-17"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/casper-capm-validation-yield/219
views: 3165
likes: 1
posts_count: 5
---

# Casper: CAPM & Validation Yield

### Casper FFG:  & Validation Yield

[Link to working doc](https://paper.dropbox.com/doc/Casper-FFG-CAPM-Validation-Yield-axlhF83BrULU5d38fJCds)

**tl;dr** While the CAPM model and Sharpe ratio have major limitations, there are concrete takeaways for designing Casper incentivization. Primarily, **the more we can limit the standard deviation of validation yield, the lower the required returns of the validators**. That allows for either lower issuance/dilution—or for any given level of issuance, a higher risk-adjusted return—which will make participation in the network more compelling for the same level of issuance.

#### Introduction to CAPM

E(R_i) = R_f + \beta_i (R_m - R_f)

E(R_i) - R_f = \beta_i (R_m - R_f)

In other words, the risk premium of a given asset (such as ETH validation stake) should be the (a) relative volatility of the asset vs the market times (b) the market premium of the asset.

- The risk premium (E(R_i) - R_f) is defined as the expected return of the asset in excess of the risk-free rate (e.g. 3 month US Treasury bill)
- The beta of the asset (B_i) is the standard deviation of the asset returns divided by the standard deviation of market returns (\sigma_i/\sigma_m). This measures the relative volatility of the asset returns to the market.
- The excess market returns R_m - R_f is the returns of a given “market” in excess of the risk-free return.

The two large factors for this analysis is:

1. What is the correct & reasonable selection of the relevant “market returns” that this asset class is under?
2. How the reward/penalty parameters will affect \sigma_i and therefore the \beta_i of the asset.
3. The more we can limit the standard deviation of the asset returns (make it more predictable, the less we have to reward the validators. i.e. less issuance / dilution of ether value. or higher excess return for same level of issuance).

To take it one step further: there are three real drivers of the assets required returns E(R_i). The required returns of the asset will be greater when:

1. The market returns are higher.
2. The standard deviation of the asset returns are higher.
3. The standard deviation of the market returns are lower.

#### Conclusion

The main takeaway here is that, **there is a direct cost to ETH holders for having high standard deviation validator returns**. So for a given level of “economic security,” we should strive to minimize the standard deviation of validator returns. That will allow for (1) additional “resources” to increase penalties / cost of attack by increasing TD, (2) decreasing issuance and enhancing value of ETH, or (3) provide additional excess risk-adjusted returns to validators (attracting a broad set of validators).

*Also related: [Sharpe ratio](https://www.investopedia.com/terms/s/sharperatio.asp) and its cousin [Sortino ratio](https://www.investopedia.com/terms/s/sortinoratio.asp)*

## Replies

**vbuterin** (2017-11-17):

This looks like it might be an argument for lower p values as I describe here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Casper: The Fixed Income Approach](https://ethresear.ch/t/casper-the-fixed-income-approach/218/2) [Economics](/c/proof-of-stake/caspers-economic-incentive-structures/11)



> OK, so this is what I in my previous paper call the p=1 approach. The formula was
> interest_rate = k / total_deposits^p
>
> With p=1, that becomes a simple
> interest_rate = k / total_deposits
>
> The other main alternatives are p=0 (fixed interest rate), p=0.5 (what we’re currently doing) and p=infinity (consider this as the limit of k and p going to infinity at the same time; basically, this is a policy that targets some specific total deposit size, and if the actual deposit size is different then it…

---

**nate** (2017-11-20):

> The required returns of the asset will be greater when:
> …
> 2.The standard deviation of the asset returns are higher.

I’m a total econ nube (so let me know if I’m totally off-base here ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) ), but it seems like the standard deviation on the returns should not include the returns of validators who were slashed for *purposeful* malicious behavior. E.g. the returns of some validators who got caught (and slashed!) for a purposeful finality reversion attack shouldn’t be considered in this calculation.

The reasoning is that, if you are an honest node, there isn’t more risk to validation because some evil validators decide to get themselves slashed (though this behavior might change your rewards in some way as well). This makes sense, as we wouldn’t want to minimize the difference between the good validator and evil validator returns anyways.

---

**jonchoi** (2017-11-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This looks like it might be an argument for lower p values as I describe here

Yes, lower than `p=1` would add a “defensive” feature to validator returns per your point.

Although, if we believe that higher `p`-values are more prescriptive of issuance level in relation to TD, that would be an argument towards higher `p`-values lowering the std deviation of returns by providing more predictable relationships between the variables mentioned.

This is a subtle tradeoff across multiple variables that all affect perceived risk/reward of participation.



    ![](https://ethresear.ch/user_avatar/ethresear.ch/jonchoi/48/165_2.png)

      [Casper: The Fixed Income Approach](https://ethresear.ch/t/casper-the-fixed-income-approach/218/3) [Economics](/c/proof-of-stake/caspers-economic-incentive-structures/11)




> Thanks for the thoughtful response. Enjoyed pondering the tradeoff exploration with respect to p.
> Context
> For reference, found the approach you’re referring to in the previous paper. You are right that it is a specific instance of: BP(TD, e - e_{LF}) = \frac{k_1}{TD^p} + k_2 * [log_2(e - e_{LF})] (Didn’t realize we had set on 1/2 for p)
> As we discuss, here are the plots for reference for various p values and constant k:
>  [image]
> (blue is p = 1, green is p = 3/4, orange is p = 1/2)
> Additiona…

---

**jonchoi** (2017-11-21):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/n/e95f7d/48.png) nate:

> it seems like the standard deviation on the returns should not include the returns of validators who were slashed for purposeful malicious behavior.

Good insight, but the inference is actually flipped.

What you mentioned is not an affordance / free assumption, but a result we’d like to drive by having clear mechanism/incentives that have deterministic guarantees on reward and penalty protection based on a validator’s actions (i.e. online validators shouldn’t lose money, voting should always be more lucrative than not voting, etc).

We want to create a mechanism with incentives such that the validators themselves can assume what you just said about not including the chances of being slashed.

One of the reasons why we can’t just take that as a given is that, there’s no guarantee that validator’s are 100% immune from slashing based on bugs or other observed Byzantine behavior that don’t stem from malicious intent. Validators need to have a guarantee of no slashing, if not, they will necessarily incorporate that into their risk assessment and therefore required return.

Taking a step back, I think the mechanism design in general can assume and design the “ideal execution,” but implementation and incentivization should assume maximal entropy and push the equilibrium towards the “ideal execution” as imagined.

Let me know if that makes sense.

