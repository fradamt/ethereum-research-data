---
source: ethresearch
topic_id: 16027
title: Preventing restaking centralization risks
author: Idan-Levin
date: "2023-07-03"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/preventing-restaking-centralization-risks/16027
views: 3440
likes: 8
posts_count: 5
---

# Preventing restaking centralization risks

In the latest Bankless episode about restaking, Justin Drake highlighted a key risk that restaking protocols pose to Ethereum’s decentralization.

I want to explain this risk and offer an economic solution that I believe can solve it, and by this to prevent centralization risks from restaking protocols in the future.

Let’s start by explaining the risk itself first - stake centralization due to the existence of restaking services.

We need to go back to Proposer-Builder-Separation (PBS) to understand this better:

One of the great successes of PBS was that it leveled the playing field for validators. With PBS, every validator that tapped into the PBS relay got to enjoy the same yield for staking (and offer it to its delegating stakers).

The idea here is that there isn’t any economic advantage for any validator from building more profitable blocks than others. Hence users are indifferent in delegating their stake between the different validators because all the returns are the same.

Post PBS, there isn’t a return-to-scale advantage to any validator. Return to scale for some validators enables them to have better returns, and consequentially to become very dominant by attracting more stake than other validators (=centralization risk).

So the key principle to eliminating centralization risks is not allowing any validator to have an economic advantage over other validators (especially advantages that compounds with size).

Now let’s move to restaking, and why it changes this dynamic:

EigenLayer and similar restaking services allow an infinite number of new permissionless services to be built on top of Ethereum, using the same stake. This creates an infinite space for inventing new permissionless services built on top of Ethereum.

But this also creates a new type of centralization risk that PBS was aimed at solving -

Restaking protocols will allow validators to tap into new staking services in addition to just validating Ethereum consensus.

Eventually, these validators can offer better returns to their delegators by not just offering plain Ethereum staking yields. Now we can get some additional yield on top of Ethereum staking yield! yay!

After restaking, validators that tap into restaking services can offer higher APY to their delegators! How much higher? Well, it depends on how many staking services they eventually tap into (you can theoretically tap into how many you would like).

How will validators determine which restaking services they should tap into and offer to their stake delegators? analyzing a specific service built on restaking might not be such an easy job as one might think. Understanding the risks from new consensus protocols, oracles, or other permissionless services built using restaking protocols, is not an easy job!

As a validator, you need to have a very deep understanding of the service you tap into and offer to your stake delegators, in order to truly understand the risks and potential rewards.

Stake delegators, and subsequently capital inflows, will likely avoid validators who mindlessly tap into restaking services without fully understanding the associated risks. They will most likely prefer to delegate their stake to sophisticated validators with reputations that can underwrite restaking services successfully.

This presents a significant challenge - sophisticated validators with more resources and deeper pockets can better understand the risks and rewards of specific restaking services.

Over time, this advantage can accumulate and result in a better reputation for the validator that has more resources.

This returns us to the starting point - some validators will have a return to scale, which will allow them to attract more capital. This leads to centralization risks, the very issue PBS was designed to solve!

The end game here is that a few validators that can underwrite restaking services better (and communicate it outwards) will gain most of the stake and reputation.

Can we get out of this centralization pithole in an elegant way and still enjoy restaking innovation?

Yes!

The solution, in short, is standardizing a restaking aggregation service that all validators can tap into, a ‘one size fits all’ approach. This is akin to an Exchange-Traded Fund (ETF) in traditional finance.

Before we get into the solution, there are some simple assumptions we need to make first -

1. there will be many restaking services, probably hundreds of them eventually
2. They will have a different risk-reward ratio
3. Pareto rule will apply to their success, meaning few services (could be tens) will probably become very dominant, so if you will rank services by their dominance you will get a pareto distribution.

Now let’s introduce a classical finance theory called ‘portfolio theory’, coined by Harry Markowitz (who won the Nobel prize for this).

Portfolio theory explains how to allocate an investment portfolio in an optimal way. We can think of each restaking service as a specific asset and the combination of different restaking services as a portfolio.

What if we could select an optimal mix of restaking services?

That will be great because instead of having lots of discretion for each validator in picking the different services to tap into and offer to restakers, they can just pick the optimal portfolio. And then it doesn’t matter which validator you delegate your stake to because they offer the same optimal portfolio.

The optimal portfolio is great and advances decentralization, because there is no discretion in picking staking services!

Now every validator that wants to offer restaking, can offer the vanilla product (which is the optimal portfolio of restaking services), and assuming this will be the market-preferable option, we are again, evening the playing field for validators!

This also solves the problem of individual restakers that hold LSTs and want to restake by themselves. In their case the issue is that stake will accumulate to specific services, which might get too much of Ethereum stake used by them.

Instead of having to underwrite a specific service, the restaker can just choose the optimal portfolio and enjoy diversification of restaking. This will ensure that the stake flowing to some services will not make them ‘too big to fail’ (because they accumulated too much stake).

You may ask, why should this work? Why would restakers prefer an ‘optimal portfolio’?

We have a lot of evidence from traditional markets that ETFs are a great efficient solution for long-term investment (a big portion of public funds are held in these portfolios). There are some good reasons for that:

1. Optimal portfolios are diversified, and diversification, when done in a good way, eliminates risk
2. Users don’t have the capacity to actually choose across tens/hundreds of different restaking services
3. Buy-and-hold (restake-and-hold in our case) is a great strategy for passive investors

We can safely assume that having a market-agreed-upon efficient portfolio of restaking services can become very popular by restakers.

There are obviously some open questions:

- How do we agree on such an optimal portfolio and what are the criteria for getting in as a restaking service?
- Will this standard create overdominance of a specific set of services?
- Can we get a market consensus on this?
- Should we create multiple optimal portfolios catering to different risk levels (high risk, medium risk, or low risk)?

Summary:

1. Create an optimal portfolio of restaking services
2. If the market accepts this as a standard, most users participating in restaking will likely choose the vanilla product used by others
3. Most validators offering the optimal portfolio alongside regular staking will ensure no single entity has an economic advantage
4. Multiple optimal portfolios can be created to suit different risk profiles

Would love to hear your thoughts.

[![20230703_192840](https://ethresear.ch/uploads/default/optimized/2X/f/f98f4e2eb334bd6784e9e073448b24f3b01043b9_2_690x368.jpeg)20230703_1928401050×561 76.3 KB](https://ethresear.ch/uploads/default/f98f4e2eb334bd6784e9e073448b24f3b01043b9)

## Replies

**tripoli** (2023-07-03):

Good post! I agree with most of it, and do think that restaking plays an important role in the decentralization of the ecosystem, but I don’t think this completely captures the economic concerns that (I believe) Justin was alluding to.

Staking is a trade-off where real yield can be paid to validators because it comes with a cost (the illiquidity of your tokens). What liquid staking, restaking, and worst of all the two leveraged together, do is reduce the cost of staking. This has positive first-order effects, but the second-order effects could become problematic.

Now that the cost of staking is much lower (through LSTs), the risk-adjusted real yield of LSTs will drop to zero, which in turn will push the risk-adjusted real yield of running a validator negative; i.e., when the staking ecosystem has matured and is closer to its equilibrium, solo validation won’t be able to economically compete with LSTs and/or restaking. The way that Ethereum’s staking reward structure was designed doesn’t account for external forces that push APY away from its natural equilibrium.

The question that I would start asking is how important are solo validators, and how can we incentivize them to continue operating?

The other really important nuance that I think needs discussion is minimum viable issuance. One of the big ideas historically has been to lower staking APY to disincentivize staking, but this has only been modelled in a vacuum. Dropping base yield has a more severe effect on solo validators than it does liquid staked or restaked validators because base yield is a greater share of their income. If we drop APY close to zero because LSTs and restaking are enough to incentivize validators, it means that we’ve taken away the only reason to be a solo validator.

---

The other question that just popped up in my head about the optimal restaked portfolio is about management. I wouldn’t want to constantly be managing my own restaked ether, so what are the chances that the market just consolidates into a few active management vehicles. If I’m Blackrock and coming into this market then I’ll want to basically create an iShares restaking vehicle which could introduce centralization risks. Has anyone discussed this possibility?

---

**krane** (2023-07-03):

This post makes a ton of sense and I think services that offer some risk-adjusted mix of AVSs will exist (dm me on Twitter to chat more: https://twitter.com/0xkrane because I think what I’m working on is not a million miles off) but it does to some extent ignore the fact that different validators come with different professionalism and different quality of service. So there will also need to be a way for users to be able to decipher which validators are actually good if you are delegating. This was one problem that ETH PoS had, and Lido solved (users didn’t need to pick validators) allowing Lido to get dominating market share amongst LSTs.

Also, the post does allude to validators offering higher yield to users by opting them into AVSs but how Eigenlayer works today is that stakers opt-in to different AVS to earn additional yield and validators can’t opt users into new AVSs without their consent (this is important because if the validators could opt-in stakers to other AVSs they could 51% attack several smaller AVS by colluding).

---

**Idan-Levin** (2023-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> The other question that just popped up in my head about the optimal restaked portfolio is about management. I wouldn’t want to constantly be managing my own restaked ether, so what are the chances that the market just consolidates into a few active management vehicles. If I’m Blackrock and coming into this market then I’ll want to basically create an iShares restaking vehicle which could introduce centralization risks. Has anyone discussed this possibility?

I think that if you can agree on a methodology for optimal portfolios, you can have a competitive market for these products. There are some centralization risks here as well, but this is second-order effect I guess.

---

**0xNimrod** (2024-04-24):

Nice analysis!

I do want to add one thing - from the POV of an AVS, they have to realize the risks that restaked capital carries and incentivize it accordingly. This consideration should, in the long term, reach some kind of equilibrium where it’s not profitable for operators to opt into more AVSs.

In general, I feel like Eigen ecosystem’s analysis must separate between long and short term - a good thumb rule for Nobel Prize nomination ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

