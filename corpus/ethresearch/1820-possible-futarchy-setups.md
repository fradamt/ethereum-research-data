---
source: ethresearch
topic_id: 1820
title: Possible Futarchy Setups
author: chris.whinfrey
date: "2018-04-24"
category: Economics
tags: []
url: https://ethresear.ch/t/possible-futarchy-setups/1820
views: 3922
likes: 13
posts_count: 11
---

# Possible Futarchy Setups

I’d like to introduce two possible prediction market setups for implementing futarchy. First I will review 3 types of prediction markets. Then I will apply these to 2 different Futarchy models.

### Introduction to Prediction Market Setups

*If you already have a good understanding of categorical, scalar, and conditional prediction markets, feel free to skip this section.*

Each prediction market has a question, a collateral token, and at least two outcome tokens covering the possible outcomes of the question. At any point one collateral token can be locked up in exchange for one of each outcome token and likewise, a complete set of outcome tokens can be exchanged back for a collateral token.

1. Categorical markets - Categorical markets have a set of possible outcomes. When the market is resolved to one of those outcomes, that outcome token can be redeemed for a collateral token.
 Examples:

“Will the groundhog see his shadow?” Outcome tokens: YES, NO
2. “Who will win the election?” Outcome tokens: ALICE, BOB, CINDY
3. Scalar markets - Scalar markets predict what a particular value will be by a target date. This is a numerical value that lies within a specified range. A scalar market has exactly two outcome tokens. One for the upper bound of the range and one for the lower bound. The market is “resolved” when the target date is hit, and the outcome of the value is realized. When the market resolves, the upper bound outcome token can be exchanged for (RESOLVED_VALUE - LOWER_BOUND) / (UPPER_BOUND - LOWER_BOUND) collateral tokens. Likewise, the lower bound token can be exchanged for (UPPER_BOUND - RESOLVED_VALUE) / (UPPER_BOUND - LOWER_BOUND) collateral tokens. The upper bound and lower bound outcome tokens are also referred to as long and short tokens respectively.
 Example:

“What will the price of gold per oz be at the beginning of 2019?” Upper bound: $2,000, Lower bound: $0

If the market resolves to $1,000 per oz, long tokens will be worth 0.5 collateral tokens and short tokens will be worth 0.5 collateral tokens.
4. If the market resolves to $1,500 per oz, long tokens will be worth 0.75 collateral tokens and short tokens will be worth 0.25 collateral tokens.
5. Conditional Markets - Conditional markets consist of a base market, which is an existing categorical market. An example categorical market to use as a base market: “Will company A replace their CEO within the next six months?” Y/N. Conditional Markets use one of the outcome tokens from the base market as its collateral token (Y or N).  They are called conditional markets because they make a prediction based on the condition that the chosen outcome token represents the correct outcome of the base market. You might have a conditional market: "What will company A’s stock price be in six months?” which uses the NO token from the base market as it’s collateral token. This market can be thought of as predicting “What will company A’s stock price be in six months given the CEO is not replaced?” since the conditional market’s outcome tokens only have value if the CEO is not replaced. Conditional markets can be either categorical or scalar markets.
 Example:

The base market is “Will company A replace their CEO within the next six months?”. The conditional market is “What will company A’s stock price be in six months?” and uses the NO token from the base market as its collateral token. This market can be thought of as predicting “What will company A’s stock price be in six months given the CEO is not replaced?” because the conditional market’s outcome tokens only have value if the CEO is not replaced.

### Futarchy Market Setups

For both setups I’ll use an example DAO with a token called FTC. The decision being made is whether to accept or deny a proposal based on the predicted FTC price 6 months after the decision.

1. Create a categorical market for “Will the proposal be accepted or denied?” with two outcome tokens ACCEPTED and DENIED. Then create two conditional scalar markets with ACCEPTED and DENIED as collateral tokens predicting the token price 6 months after the decision is made. These markets produce four more outcome tokens LONG_ACCEPTED, SHORT_ACCEPTED, LONG_DENIED, and SHORT_DENIED. The decision is made based on the price of LONG_ACCEPTED vs. LONG_DENIED. An outcome with a higher LONG token value indcates a higher FTC value if that outcome is chosen.
 Advantages:

The value being maximized or minimized does not need to be tied to a token’s value (eg. voter satisfaction).
2. It’s hard to choose good upper and lower bounds.
3. If market resolves outside of the chosen range, no decision can be made.
4. Create two categorical markets for “Will the proposal be accepted or denied?” with ETH and FTC as the collateral tokens. These markets produce four outcome tokens ACCEPTED_ETH, DENIED_ETH, ACCEPTED_FTC, and DENIED_FTC. The decision is made based on ACCEPTED_FTC/ACCEPTED_ETH vs DENIED_FTC/DENIED_ETH. ACCEPTED_FTC/ACCEPTED_ETH represents the predicted price of FTC in ETH if the proposal is accepted. DENIED_FTC/DENIED_ETH represents the predicted price of FTC in ETH if the proposal is denied.
 Advantages:

Simpler to implement
5. There is no need to define bounds for token price.
6. A decision can always be made.
7. The value being maximized or minimized needs to be a token’s price.

I would like to open up a discussion on the advantages and disadvantages of each of the approaches and any possible alternatives.

## Replies

**MicahZoltu** (2018-04-24):

I considered not posting this comment because it doesn’t actually discuss the topic you want to discuss, however I think it is useful for someone to say it in case people aren’t already aware.

The primary problem with futarchy is defining metrics of success that are free from confounding variables.  The example you gave is only useful if there are *no* confounding variables that could cause FTC to rise in price 6 months from now.  Due to current crypto volatility and the fact that crypto trading appears to be entirely uncorrelated with value delivery, this is really just a futures market for FTC, unrelated to the thing you are trying to predict.

While I like the *idea* of futarchy, I have yet to see a solution to the “how do you isolate the thing you actually want to measure” problem.

---

**chris.whinfrey** (2018-04-24):

I think confounding variables are an issue if you are comparing the current token price to the predicted price of the token if a decision is made. However, if you are comparing two markets predicting 1. the token price if a decision is made and 2. the price if the decision is not made, I would think that any variables besides the decision itself would effect both markets equally thus isolating the decision. This is how both of the futarchy markets above are set up. Do think that is adequate to solve the isolation problem?

---

**MicahZoltu** (2018-04-24):

The problem is that we can only evaluate one of the conditions in reality, not both.  So while the market may ask people to predict “will the value go up if we choose A or we choose B”, but ultimately we can only test the hypothesis against either A or B.  Imagine the following scenario:

Users believe the value of asset will increase over the next 6 months. Someone proposes a choice between A and B and asks the market, will the value of the asset go up if we choose A or will it go up if we choose B?  Since users believe that the value will increase *regardless* of whether A or B is chosen, then they win either way.  However, presumably if A is chosen, then people holding B shares will no longer get exposure to the market.  This results in people trying to predict whether A or B will ultimately be chosen, because they want to hold shares in either one (since both are equally valuable).  This rapidly devolves into a Keynesian beauty contest since it is now a self-fulfilling market, where whichever gets more “votes” (A or B) wins, and anyone who voted for the winner wins, therefore people are merely voting for what everyone else is voting for, rather than voting for what they actually believe (which in this case is that it doesn’t matter).

---

**mkoeppelmann** (2018-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Since users believe that the value will increase regardless of whether A or B is chosen, then they win either way.  However, presumably if A is chosen, then people holding B shares will no longer get exposure to the market.  This results in people trying to predict whether A or B will ultimately be chosen, because they want to hold shares in either one (since both are equally valuable).

If a user thinks both conditional markets are underprices the user can of course go long on BOTH markets.

---

Back to the original question:

My comments would be:

a) this one can be seen as both advantage and disadvantage:

in model 1) EVERYONE (with money) can go short on a bad proposal - in model 2) you need to have the token to go short. However - if system like “decentralized token lending” this difference might get removed.

b) an advantage of proposal 2)

It can make it more intuitive how to act as a user/ token holder if a bad proposal is made: you just sell your tokens under the condition the proposal is accepted. This action will drive the price down and will make it more unlikely that this will be accepted. As you user you know that you can either “exit” at a decent price (it need to be higher than the non-acceptance price) or the proposal will be rejected.

c) a (big) problem of proposal 2)

If there are multiple suggestions in parallel tokens will get locked up in those decision markets. E.g. I want to sell all my tokens if proposal 1 is accepted - I would not have any tokens left to react on proposal 2. Long term this can be solved with multidimensional markets (2^n outcomes for n decisions) but short/mid term this will not be possible on Ethereum given the gas constraints.

So with this approach it might be necessary to decide on proposals sequentially.

d) capital costs of proposal 1)

While only “money”/ collateral token is used and not token those tokens are locked up in the market for 6(!) months.

---

**MicahZoltu** (2018-04-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> If a user thinks both conditional markets are underprices the user can of course go long on BOTH markets.

There is opportunity cost for choosing one over the other, so the user must allocate their finite capital towards the market that is most likely to win.  While they may hedge with the market they think will lose “just in case”, as the system sways toward one or the other people will allocate increasing amounts of capital toward that, re-enforcing the winner.

---

You can do “multi-dimensional” markets (Augur has something called this but it means something else) without gas problems by letting people use tokens for market A when buying shares in market B.  If all of the `n` open markets are sequential, then you can have each market denominated in the previous market’s tokens.

---

**emaG3m** (2018-04-30):

I think that there’s potential use-cases for futarchy, and also other use cases where futarchy would not be helpful. For instance, trying to predict the impact one decision will have on the price of ethereum would be extremely futile. However, in smaller ecosystems where the value of a token depends on a narrow range of factors, futarchy could be very effective. For instance, token curated registries —  where the token value depends on the quality of the list. With a manageable list size, deciding whether to accept or reject a new listing will most likely directly affect the value of the TCR token. As more patterns emerge in the way tokens and blockchains operate, we may discover a good niche for futarchy, and I think it’s worthwhile to explore different futarchy models.

So, for the purpose of something like a TCR, I think the second model suffices, because really, all we’re worrying about is the value of the TCR token. Plus, it’s a simpler, more digestible model for end-users. Obviously we want this technology to be accessible for anyone, not just mathematicians. So if token value is the priority, I’d say definitely resort to model #2. I think it only makes sense to venture out into the first, more complicated futarchy model when the second model is no longer sufficient. Where to draw that line exactly, I think is yet to be discovered.

---

**josojo** (2018-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/chris.whinfrey/48/10236_2.png) chris.whinfrey:

> Create two categorical markets for “Will the proposal be accepted or denied?” with ETH and FTC as the collateral tokens. These markets produce four outcome tokens ACCEPTED_ETH, DENIED_ETH, ACCEPTED_FTC, and DENIED_FTC. The decision is made based on ACCEPTED_FTC/ACCEPTED_ETH vs DENIED_FTC/DENIED_ETH. ACCEPTED_FTC/ACCEPTED_ETH represents the predicted price of FTC in ETH if the proposal is accepted. DENIED_FTC/DENIED_ETH represents the predicted price of FTC in ETH if the proposal is denied.

Could someone please explain this mechanism a little bit more in detail. I do not understand which forces push the prices smoothly into an equilibrium for the decision.

Maybe the following example illustrates my concern: Suppose 99% of participants are in favor of accepting a proposal. Then ACCEPTED_FTC and ACCEPTED_ETH are very valuable and DENIED_FTC and DENIED_ETH should be nearly worthless. Now, a manipulator could buy DENIED_FTC very cheaply. Then his denied decision would be in favor since DENIED_FTC/DENIED_ETH would shoot into the sky. Even if people will start buying DENIED_ETH at some point, the attacker might keep up a better ratio of DENIED_FTC/DENIED_ETH > ACCEPTED_FTC/ACCEPTED_ETH.

This way the attacker invested very cheaply in the Token FTC and made big-time profit since he bought nearly worthless tokens, but got good tokens, where only one decision - the futarchy decision - will suboptimal.

I think these kinds of attacks would not be possible in the other better-known futarchy setup.

---

**chris.whinfrey** (2018-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/josojo/48/10037_2.png) josojo:

> Could someone please explain this mechanism a little bit more in detail. I do not understand which forces push the prices smoothly into an equilibrium for the decision.
>
>
> Maybe the following example illustrates my concern: Suppose 99% of participants are in favor of accepting a proposal. Then ACCEPTED_FTC and ACCEPTED_ETH are very valuable and DENIED_FTC and DENIED_ETH should be nearly worthless. Now, a manipulator could buy DENIED_FTC very cheaply. Then his denied decision would be in favor since DENIED_FTC/DENIED_ETH would shoot into the sky. Even if people will start buying DENIED_ETH at some point, the attacker might keep up a better ratio of DENIED_FTC/DENIED_ETH > ACCEPTED_FTC/ACCEPTED_ETH.
>
>
> This way the attacker invested very cheaply in the Token FTC and made big-time profit since he bought nearly worthless tokens, but got good tokens, where only one decision - the futarchy decision - will suboptimal.

I think this attack would create an arbitrage opportunity that would prevent it from being successful. With this setup, one of decision markets (ACCEPTED_FTC/ACCEPTED_ETH or DENIED_FTC/DENIED_ETH) needs to be above the current FTC/ETH price and one below otherwise an arbitrage opportunity is presented.

Let’s say that these are the current market rates:

- ACCEPTED_FTC/ACCEPTED_ETH = 1.5
- DENIED_FTC/DENIED_ETH = 1.2
- FTC/ETH = 1.0

Someone could arbitrage these markets by buying 1 FTC with 1 ETH.

`1 ETH -> 1 FTC`

Then, buying both outcomes from the FTC collateralized market.

`1 FTC -> 1 ACCEPTED_FTC + 1 DENIED_FTC`

Sell both of those outcome tokens in the ACCEPTED_FTC/ACCEPTED_ETH and DENIED_FTC/DENIED_ETH markets.

`1 ACCEPTED_FTC + 1 DENIED_FTC -> 1.5 ACCEPTED_ETH + 1.2 DENIED_ETH`

And finally, sell 1.2 of both outcome tokens to the ETH collateralized market with 0.3 ACCEPTED_ETH remaining.

`1.5 ACCEPTED_ETH + 1.2 DENIED_ETH -> 1.2 ETH + 0.3 ACCEPTED_ETH`

Because of this type of arbitrage, an attacker trying to drive up the DENIED_FTC/DENIED_ETH price would also need to drive down the ACCEPTED_FTC/ACCEPTED_ETH price which would be much harder than manipulating a market with nearly worthless tokens alone.

---

**josojo** (2018-05-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/chris.whinfrey/48/10236_2.png) chris.whinfrey:

> I think this attack would create an arbitrage opportunity that would prevent it from being successful.

Yes, there will be a small arbitrage opportunity, but it might not prevent the attack. I like that you wrote it down with numbers, so let me do it as well.

Assume FTC has a marketcap of M and currently we have FTC/ETH = 1.0. If the proposal is accepted, then FTC would have a value of M * a and if it is declined, FTC would have a value of M * d, with d<1<a.

The problem I foresee is that rational players would sell the tokens of DENIED_FTC and DENIED_ETH

even for very low prices, as these tokens will probably be worthless anyway. Hence an attacker could probably buy over 50% of the DENIED_FTC for , let’s say, M*0.05. Now there is a huge incentive to buy up the rest of the  DENIED_FTC, since his gains would be: |d-0.05|*M/2.

The possible arbitrage costs of |1-d|M/2 might be much much smaller than the expected win |d-0.05|*M/2. Especially once people released that the attack will likely be successful, they will try to sell of  ACCEPTED_FTC and ACCEPTED_ETH very quickly so that the attackers do not even have an arbitrage cost.

I feel like this is not a good approach, since a small change in prices of ACCEPTED_FTC/ACCEPTED_ETH and DENIED_FTC/DENIED_ETH can induce huge price shifts in ACCEPTED_FTC/DENIED_FTC, which can be abused by malicious players.

---

**mkoeppelmann** (2018-06-12):

Here is a token flow graph for option 1) (scalar market maker markets)


      ![](https://ethresear.ch/uploads/default/original/3X/f/c/fc36827794b5b74689e06501b0e0bc2bf934eef3.png)

      [Google Docs](https://docs.google.com/drawings/d/1W-MoPY0wTA1U8Cdar1x-cgE8DJkNvF7S-W1vX8UgitM/edit)



    ![](https://ethresear.ch/uploads/default/optimized/3X/b/e/be72a0e792e2a89d22141e08b8b705f2c3ee5b64_2_690x362.png)

###



Registry Challenge FutarchyOracle CategoricalEvent “Will challenge be accepted?” ScalarEvent “What will price of FCR be if challenge is accepted” ScalarEvent “What will price of FCR be if challenge is denied” Challenger Applicant 10 FCR 10 FCR apply...










One think that can be optimized in this variant to be more capital/liquidity efficient would be to reuse a long/short position of already decided questions for future questions.

If a decision is made traders have a long or a short position with either “yes - decision accepted” or “no - not accepted” tokens as collateral tokens. Once that decision is made the collateral token can be redeemed for the collateral token of the “parent event”. A efficient implementation could recognise that the long/short event tokens are now collateralized by the token from the parent event.

If a new decision is upcoming (and the same oracle is used for the scalar markets) it should be in theory possible to convert your general long tokens long tokens of the the two conditional market (decision accepted yes/no)

