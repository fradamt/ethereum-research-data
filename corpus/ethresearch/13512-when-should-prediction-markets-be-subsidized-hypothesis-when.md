---
source: ethresearch
topic_id: 13512
title: "When should prediction markets be subsidized? Hypothesis: when there is harmful information asymmetry"
author: llllvvuu
date: "2022-08-27"
category: Economics
tags: [public-good, futarchy]
url: https://ethresear.ch/t/when-should-prediction-markets-be-subsidized-hypothesis-when-there-is-harmful-information-asymmetry/13512
views: 2201
likes: 8
posts_count: 5
---

# When should prediction markets be subsidized? Hypothesis: when there is harmful information asymmetry

**Abstract:** Market making involves two things: paying for information, and providing liquidity to uninformed traders. Uninformed traders are comprised of routine flow (when the asset has utility) and gamblers. Neither of these are apply to “serious” prediction markets, e.g. for policy. Hence, it is unlikely that prediction market makers will have their information generation significantly subsidized by trading noise. However, many kinds of information are public goods, so there is a case for subsidizing the market with public and/or philanthropic funds. When is this *counterfactually efficient*? We attempt to answer this question in terms of *counterfactual revelation*.

## Example Settings

We consider the following settings.

1. A sports game or an election proceeds. At several points in time, the public simultaneously receives information. Eventually, the market pays out.
2. The effects of a policy are betted on, the market opens well after the public has had the chance to discuss & grok the effects, and closes well before any data is actually available.
3. Someone has private information about a group/organization, and a market is formed to encourage the leaking of this information (this could be societally beneficial or harmful).

## The cost/benefit of a bid/offer

WLOG we can analyze the market maker as placing a single bid and offer. Suppose we quote .40/.60 with $100 units on either side. Then we are offering a bounty of up to $40 for an opinion. The opinion is not fully informative, nor is the $40 loss guaranteed. However, we should assume the worst case, i.e. we pay the maximum loss to learn the minimum information.

As noted in [Othman et al (2013)](https://www.cs.cmu.edu/~sandholm/liquidity-sensitive%20automated%20market%20maker.teac.pdf), if both orders get filled, we’ve now made money and both:

- have a larger budget to pay for information
- have more dissent and hence perhaps a higher want for information
- have more likelihood of future dissent which compensates us financially

thus we should put out two larger orders; and as a corollory, if we get filled on e.g. the bid, then we should put out another offer (a bounty for taking the other side - e.g. correcting misinformation).

Is $40 the right price? If the choice were between publishing the information now, and never publishing the information, then this would be an easy decision. However, the choice may often be between publishing the information now versus publishing it a day or even a second later.

## The opportunity cost of a bid/offer

The problem is overpaying for information when we could pay less. An intuitive solution would be to conduct “price discovery” via e.g. a reverse Dutch auction (per price band, e.g. one at 0.60, one at 0.70, etc) on the number of units offered to the market, with a reserve price indicating the societal value of the information.

As a toy model (i.e. all of the following is pseudomath only), we assume each counterparty i is endowed with b_i bits of information, has a cost of information production c_i(t, b) to produce b bits of information at time t, and a disincentive p_i(b) to release b bits of information. We should not expect a fill if we are offering less than p_i(b) + c_i(t, b - b_i) for all i. This quantity may sharply decline over time (i.e. liquidity becomes stale) - in these cases, a reverse Dutch auction will still overpay. The quantity will also be cheap when b_i is high for some i, and in general there is most “bang for buck” when variance in b_i, c_i are high (information asymmetry).

## Conclusion

Most of the prediction markets live today are probably unproductive. Many proposed use-cases (futarchy, whistleblowing) may be viable but will require the subsidization to be efficient. Public goods funds may use Dutch auctions to sink an optimal amount of money into protocol-owned liquidity (POL), but should take care not to have the market open during times of free/cheap information diffusion.

### Questions

What should the liquidity be at time t if we have a “reserve price” of P? Should we roll Othman et al (2013) and just increase the liquidity parameter b over time? Should we instead choose a different shape for the liquidity curve? Can we gather evidence for the ideal shape from the size traders are trading? Should the shape itself evolve over time? Should the liquidity parameter (partially) reset upon a trade?

## Replies

**NunoSempere** (2022-08-30):

Agree that prediction markets subsidized by those who want to provide a public good might be a better model.

Not sure of what you mean here:

> . Suppose we quote .40/.60 with $100 units on either side. Then we are offering a bounty of up to $40 for an opinion.

Do you mean that the .40/.60 quote with $100 units on each side is equivalent to a $40 bounty, or do you mean that in that scenario you would additionally offer someone a $40 bounty to bet on the market? Not sure I agree/understand either way.

Incidentally, I think that thinking about this in terms of an AMM whose liquidity is subsidized is a better model than thinking about limit orders.

---

**llllvvuu** (2022-08-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/nunosempere/48/9801_2.png) NunoSempere:

> Agree that prediction markets subsidized by those who want to provide a public good might be a better model.

Yup, and it is [closer to Robin Hanson’s original intention as well](https://mason.gmu.edu/~rhanson/infoprize.html). I guess my “contribution” here is finding the minimum viable bounty/subsidy based on a Dutch auction or some similar price discovery mechanism. And more broadly, thinking about subsidy wastage in subsidizing “high-frequency trading”.

![](https://ethresear.ch/user_avatar/ethresear.ch/nunosempere/48/9801_2.png) NunoSempere:

> Do you mean that the .40/.60 quote with $100 units on each side is equivalent to a $40 bounty, or do you mean that in that scenario you would additionally offer someone a $40 bounty to bet on the market? Not sure I agree/understand either way.

$100 here is referring to the payout amount, e.g. if a counterparty has full information (e.g. is an insider), they can win $100 off the market with a payment of $60, so net profit of $40. Of course, if the information is incomplete (e.g. EV of $75 or something) then the profit is lower (hence “up to $40”), so this is a heavily simplified analogy.

![](https://ethresear.ch/user_avatar/ethresear.ch/nunosempere/48/9801_2.png) NunoSempere:

> Incidentally, I think that thinking about this in terms of an AMM whose liquidity is subsidized is a better model than thinking about limit orders.

I do think that in practice, it will be an AMM. Limit order is a useful toy model since an AMM is an average/integral of limit orders, so reasoning about limit orders will be informative about AMMs (although maybe LMSR wouldn’t have been *that* much harder to reason about - IIRC, you can win \$b off of an LMSR or something).

---

**KimKaiv** (2022-09-05):

llllvvuu — we touch upon these issues in the *Nature Climate Change* article, " Prediction-market innovations can improve climate-risk forecasts". Read-only full-text is available [here](https://rdcu.be/cUMH6).

In the pay-to-play Prediction Markets for e.g. sports or political outcomes, there is on average a transfer of resource from less-well-informed ‘punters’ to more informed and more disciplined PM participants.

If one is relying on uninformed participants to fund the informed participants in this way, the viability of the market is determined by the viability of attracting sufficient uninformed participants.

So far, political and sports-based markets have succeeded in attracting uninformed participants. Even still liquidity concerns persist.

Prefunded prediction markets are useful especially where the questions being asked are not likely to generate sufficient interest from among uninformed punters.

There are other benefits too. When uninformed participants trade in a correlated manner, then they can distort the market prices. In behavioral finance this is known as ‘noise trader risk’. Prefunded markets avoid this potential problem.

---

**bowaggoner** (2022-09-12):

The reverse Dutch idea sounds really cool! I need to think about it more. I also strongly agree with the idea of AMMs as procuring public goods and receiving a public subsidy to do so. Some other responses:

- Your idea sounds a bit like a model where the market essentially pays people to go out and gather information from the world. This is a really interesting problem to formalize, I think there is only one recent paper: Schoenebeck, Yu, Yu 2021: [2011.03645] Timely Information from Prediction Markets
- We could also ask about the single-shot version. E.g. we have a proper scoring rule, and we’re going to take “bids” for people to get to be the one to predict. There are some related papers but I don’t think anyone’s addressed this. It also sounds a bit like nikete’s “advice auction”: http://nikete.com/advice_auctions.pdf
- One motivation of uninformed participants in a prediction market is to hedge against outside risk (e.g. I own a ski resort, so I bet on global warming to accelerate). This might or might not be unbiased on average (Kim’s “noise trader risk”), but I don’t think it goes away with a prefunded market.
- A general AMM approach following up on the Othman et al. ideas was Abernethy, Frongillo, Li, Wortman Vaughan, A General Volume-Parameterized Market Making Framework, EC 2014. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/vpm.pdf
- In theory, it’s possible to run into a “complements” situation. You and I each have inside information. Whoever trades today will make a bit of money and reveal their information. But whoever waits will get to see the other’s info, combine it with their own, and make a LOT of money tomorrow. So we are in a standoff with neither wanting to trade.
- The general problem of how to automatically adjust liquidity over time has gotten lots of thought from smart people such as Othman et al. and I don’t think we know much beyond what you wrote in the top post. My favorite take is relating it to thinness and thickness of the market - if we have lots of people willing to trade at the same time, we probably should not be taking on a lot of risk as the market maker —  nor should we need to, since there is a lot of demand. (One of Hanson’s main points of AMMs was to facilitate trade in illiquid markets.)

