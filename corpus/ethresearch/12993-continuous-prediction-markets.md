---
source: ethresearch
topic_id: 12993
title: Continuous Prediction Markets
author: xhipster
date: "2022-07-05"
category: Economics
tags: []
url: https://ethresear.ch/t/continuous-prediction-markets/12993
views: 3628
likes: 3
posts_count: 9
---

# Continuous Prediction Markets

Current prediction market thinking is focused solely on discrete mechanism. That is, there is a moment in time when prediction market must be settled. Still this approach failed to gain traction. So it is probably a good idea to ask why?

My assumption is that reality is changeable in nature, and the truth deviate in time. So even [seemingly improbable events such as death](https://en.wikipedia.org/wiki/Paschal_greeting) could be reversed in a mind of the crowd.

I failed find any insights on this topic. So let us start discussion on continuous prediction market idea in which trading could last indefinitely expressing current estimation of the probability in such a way that participants could profit based on existing beliefs and not only on future beliefs.

The design came to my mind is shockingly simple and is a mix between 2 brilliant mechanisms: [conviction voting](https://medium.com/giveth/conviction-voting-a-novel-continuous-decision-making-alternative-to-governance-aa746cfb9475) and bonding curve:

- Let us assume that we have some fact. Let say 2*2=4
- Participant could vote for true and false by buying tokens in quadratic bonding curves
- Estimator is proportion between true reserve pool and false reserve pool
- Periodically loosing reserve pay some payoff percent to the winning reserve

The question I ask is how `payoff percent` could be defined? I like the idea of [adaption quorum biasing](https://polkassembly.medium.com/adaptive-quorum-biasing-9b7e6d2a2261). This concept could be applied to our case: the more contradictory is opinion the more time it needs to converge.

[Original](https://cyb.ai/ipfs/QmUpkMhB8PYte39iLQAdByEtpSWKqvjN5dV7ZFsCfoWTuM)

## Replies

**bowaggoner** (2022-07-10):

1. For your question, you might want something based on proper scoring rules, like Hanson’s original prediction market, so that the incentives are for the price to converge to the truth.
2. Do you have a particular motivating application in mind? There are a lot of advantages to resolving and closing a prediction market at a specific time. I feel like an application would be where you expect a lot of ambiguity or disagreement about the outcome; or you’re not sure when it will resolve.
3. It’s difficult and expensive to implement good decentralized oracles. This unknown-end-time setting makes oracles much harder. So I think implementing oracles is the trickiest part. A tempting idea in prediction markets that never close is to have periodic payoffs where e.g. we pay people based on their predictions one month ago using today’s market as the oracle. This might be similar to what you’re proposing? It’s pretty analogous to a stock market. It might work but is vulnerable to a well-funded attack that always, say, bets against the event and then drives the price to zero to make it look like the event didn’t happen.

---

**themandalore** (2022-07-21):

You could say perp contracts are continuous prediction markets.  I think it just depends on what you’re trying to bet on.  Futures/options style perpetuals have gotten some traction, but even discrete prediction markets have failed to take off in the space for a lot of good reasons that I doubt just making it continuous would address

---

**claytonroche** (2022-07-30):

> It’s difficult and expensive to implement good decentralized oracles. This unknown-end-time setting makes oracles much harder. So I think implementing oracles is the trickiest part.

UMA has in development an “optimistic rewarder” that would work for this. UMA’s oracle [already handles prediction market data requests](https://medium.com/uma-project/polymarket-integrates-umas-optimistic-oracle-7fa89cae493e) and has demonstrated that it can [handle ambiguity](https://twitter.com/UMAprotocol/status/1541870773207306240).

The optimistic rewarder is a design whereby an account can accrue an owed balance based on a payout function (with the prediction market datapoint being one of the variables in that function.)

---

**NunoSempere** (2022-08-04):

Here are some related ideas that might be of interest, in addition to the conviction voting/bonding curve ideas you propose:

- Resolving traditional prediction markets as something other than $0 or $1. So for example, you could have a prediction market on [(what probability I will assign to China invading Taiwan by 2030) at the end of the year?], and if my probability assignment is 30%, prediction markets are resolved to 30cts per share.
- Having prediction markets about “what will the price of Tesla shares be”. You can have a prediction market where share price is mapped to a 0 to 1 range, and shares in that prediction market likewise resolve to fractions of a dollar. Polymarket has done some of this.
- Extending prediction market setups to allow for distributional inputs. Manifold Markets does this a bit, but I don’t think that they’ve really figured out the math, and doing so could be a nice research project.

---

**bowaggoner** (2022-08-05):

HI NunoSempere, can you explain what you mean by bullet 3, “distributional inputs”?

Bullet (1) we can do, but requires a lot of trust in the oracle (person who is being predicted). Bullet (2) we can do, we can define prediction markets on any range of real numbers, e.g. simply make a security that will pay out exactly equal to the price of Tesla on a given date.

---

**NunoSempere** (2022-08-09):

[@bowaggoner](/u/bowaggoner), suppose that you want to know how many monkeypox cases there will be in the next year in the US. Then you repurpose prediction market infra, and create a market that pays out to the number of confirmed mokeypox cases,  normalized by 1M, if you think that 1M cases is quite unlikely. So the market pays 0 per share if there are 0 cases, $1 if there are 1M cases or more, and somewhere in between if the number is in between.

The problem with that is: suppose you see a price of 50cts. Then you don’t know if that number assigns high certainty to there being 0.5M cases, or 50% to there being very few cases and 50% to there being 1M+. But both things imply different policies, e.g., about the number of hospital beds to prepare.

The alternative would be having distributional inputs, e.g., allowing users to input something like normal(500k, 200k), or a lognormal from 100k to 10M. Eliciting that distribution is a can of worms, but I think it could be solved by something like [Squiggle](https://www.squiggle-language.com/playground#code=eNqrVirOyC8PLs3NTSyqVLJKS8wpTtUBi7mmZJbkFylZlRSVAkUy8zJLMhNzggtLM9PTc1KDS4oy89KVrJQMDQyyFUryFQwNfJVqAVeAGyA%3D), which I’ve been working on.

But suppose now you have a few distributions, from a few users and they would like to bet against each other. How do they do this at all? How do you ensure that the users are incentivized by the market mechanism to input their “true” distribution? How do they do this in a capital efficient way? How do you allow users to disagree with only part of the market distribution?

These questions don’t seem unsolvable, but someone would have to sit down and figure them out.

---

**bowaggoner** (2022-08-10):

Hi [@NunoSempere](/u/nunosempere), could be fun to connect to talk more. Coming from theory of prediction markets, I’d love to understand how theory applies or fails. Squiggle looks like a great interface.

- By classic theory, we can definitely elicit distributions with proper scoring rules, and we can use them to design scoring-rule based markets using Hanson’s original idea that incentivize participants to input their true distributions. And, we can use cost-function based interfaces (i.e. ones that sell shares for prices) that are equivalent – main reference Abernethy, Chen, Wortman-Vaughan 2013.
- So the main problem, I think, is practicality of the interface, since specifying a full distribution is complicated. Also, on a budget, you don’t want to specify your true distribution, because it involves taking on a lot of risk (it’s equivalent to buying many, many shares), so you just want to modify the market consensus toward your beliefs a little – we need good interfaces for that. It sounds like that’s where you’re going with Squiggle, which looks awesome!
- One thing we proposed (Waggoner, Frongillo, Abernethy 2015) is based on kernels from machine learning. A nice example is: The market maker offers to sell “shares” in any given point on the real line. The payoff of a share drops off with distance between its center point and the actual outcome, in the shape of a Gaussian. E.g. if you bought a share of 500k, and the outcome is 300k, your share pays out something like e^{-(500k - 300k)^2 / 2sigma^2} where sigma is a constant chosen ahead of time.
- In the above market, the implied market prediction (a probability distribution) is shaped by the shares everyone purchases, but indirectly. You could imagine letting people directly modify a shared consensus prediction by adding Gaussian bumps to the probability distribution at places they think it’s too low and rewarding them with a proper scoring rule. That should work in theory, but it’s actually not what’s happening in our proposal. Instead people just buyi shares at points they think are likely, and the consensus distribution is computed via convex duality from the total purchases of everyone. I’ve never implemented it so I’m not sure how this really plays out, but we thought this interface can be more intuitive for people, i.e. it’s easier for people to decide what trades make sense to them than trying to write down their actual distributional belief.

---

**NunoSempere** (2022-08-30):

> One thing we proposed (Waggoner, Frongillo, Abernethy 2015) is based on kernels from machine learning. A nice example is: The market maker offers to sell “shares” in any given point on the real line. The payoff of a share drops off with distance between its center point and the actual outcome, in the shape of a Gaussian. E.g. if you bought a share of 500k, and the outcome is 300k, your share pays out something like e^{-(500k - 300k)^2 / 2sigma^2} where sigma is a constant chosen ahead of time.

This looks very ingenious, cheers

