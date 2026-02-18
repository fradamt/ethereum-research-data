---
source: ethresearch
topic_id: 7613
title: Better Curation via Inversely Coupled Bonding Surfaces
author: enjeyw
date: "2020-06-30"
category: Economics
tags: [bonding-curves]
url: https://ethresear.ch/t/better-curation-via-inversely-coupled-bonding-surfaces/7613
views: 1805
likes: 2
posts_count: 7
---

# Better Curation via Inversely Coupled Bonding Surfaces

I’ve been mulling this for a while, but was prompted to write-up by [@vbuterin](/u/vbuterin)’s tweet on [gauging support for protocol changes](https://twitter.com/VitalikButerin/status/1276630083898355718).

## Background

Crowdsourced methods such as “Likes” on Twitter and ‘Upvotes’ on Reddit have become a fundamental tool for curating content and by extension, ideas. Crowdsourced curation is superior to relying on a handful of specified curators in that it:

- smooths out individual biases
- is able to curate a higher volume of content, because content consumers are also able to provide curatorial input

However, existing methods do not reward consumer-curators for their efforts, and so there is little incentive to search through generally lower-quality uncurated content, to find as-of-yet unidentified high quality content. As a consequence, the overwhelming majority of people take a path of least resistance, and consume-curate content that has already been curated to some extent by others, for example by following already-popular Twitter handles. This leads to a reversion back to curation being dictated by a handful of individuals, and as a consequence a lot of high quality content remains undiscovered.

More fundamentally, it results in feedback loops wherein populist or inflammatory content is amplified, and more controversial or balanced content is suppressed. This increases groupthink and makes online information aggregation tools less effective for reasoned discourses and comparison of alternative ideas.

A solution may be to leverage the Efficient Market Hypothesis for content curation, wherein curators are incentivised to identify undervalued content. In such a market-based mechanism, instead of simply ‘Liking’ content, curators purchase tokens that signify support of that content. These tokens are issued at an algorithmically determined price using a bonding curve model; the more tokens in circulation, the higher their purchase price is.

This means curators who are able to identify good quality content early are able to purchase tokens at a lower price. Such curators are then able to subsequently sell their tokens at the current market price, thereby making a profit from their insight, and equally driving the price back down. As such, the price of the ‘support’ token, fluctuating according to demand, becomes a measure of how popular a piece of content is. Critically, there is no concrete payout for holding a support token - all potential profit is in speculation around a Schelling Point.

## Inversely Coupled Bonding Surfaces to prevent Price Manipulation

On its own, the price of a support token can be manipulated by a content creator to artificially make their content appear more popular than it is. By purchasing a large number of tokens as soon as a market is created, a creator can increase the token price from P_0 to P_1. As the creator was the first participant in the market, the token price can not drop below P_1 without the creator selling their tokens. This means the creator, having artificially inflated the price for a desired period, can sell their tokens at any point and recoup all of their initial investment.

In order to prevent this phenomenon, a secondary token that signifies opposition to the content is also available to purchase. The price of the support and opposition tokens are algorithmically linked, such that purchasing opposition tokens drives the price of support tokens down and vice-versa.

This means that the initial listing price of the ‘support’ token is no longer its lowest possible price, making it impossible to inflate its price without any risk. The secondary token has the advantage of allowing a direct comparison of the support versus opposition to a particular idea or policy.

## Bonding Surface Construction

Together the two tokens form a bonding surface, which is used to define their price behaviour. To construct this Bonding Surface, we will use a Cost Function  C(s_1,s_2) , which states that the total amount of funds paid to the contract in exchange for tokens T_1 and T_2 is a function of only their current supplies s_1 and s_2.Thus the cost to purchase \Delta s_1 of T_1 and \Delta s_2 of T_2 is

\Delta C = C(s_1 + \Delta s_1, s_2 + \Delta s_2) - C(s_1,s_2)

The Cost Function that defines our inversely couple bonding surface is then given by:

 C(s_1,s_2)=( {s_1^{ \frac{F_1}{ \beta}}} + {s_2^{ \frac{F_2}{ \beta }}})^{\beta}

Here F_i is analogous to the Reserve Ratio for each token, and determines the rate at which token price grows with respect to supply, and \beta is the coupling coefficient between the two tokens. Token prices are negatively correlated when 0<\beta<1, independent when \beta=1, and positively correlated when \beta>1.

To further understand the behaviour of the Cost Function, let us choose sensible parameter values, such as \beta=\frac{1}{2} and F_1=F_2=3. Then:

C(s_1,s_2)=(s_1^{6}+s_2^{6})^{\frac{1}{2}}

The price of a token is given by the partial derivative of its supply with respect to C, so for T_1:

p_1= \frac{\partial C}{\partial s_1} = 3 \frac{s_1^5}{(s_1^{6}+s_2^{6})^{\frac{1}{2}}}

We can now see that p_1 monotonically increases with respect to s_1, approaching p_1=3s_1^2 for s_1>>s_2. More critically, we can see that p_1 monotonically decreases with respect to s_2. Given the Cost Function is symmetric, the same logic applies to p_1.

*That is, as more of T_1 is issued, its price increases, and the price of T_2 decreases.*

Here’s a plot of p_1 for visualisation purposes. I’ve inserted a plane at s_1=0.2 to make it easier to see the price drop with respect to p_2.

[![Price Function](https://ethresear.ch/uploads/default/optimized/2X/9/9a0a1124e9e9c45b704752cfb12fd322c673b159_2_444x375.png)Price Function1518×1278 109 KB](https://ethresear.ch/uploads/default/9a0a1124e9e9c45b704752cfb12fd322c673b159)

While we are most interested in Coupled Bonding Curves with Two assets, the concept generalises to any number of assets (here we’ve included an extra weighting term):

C(s_1,…,s_n)=\left(\sum_{i=1}^{n} (\frac{s_i}{W_i})^{\frac{F_i}{\beta}}\right)^{\beta}

[Here’s a link to a google sheet if you’re interested in playing around with some numbers](https://docs.google.com/spreadsheets/d/1fxN6OfB1kjDg0d7t0hJGQSqQFAEPjEkaX9BM2B8IHfg/edit#gid=425166516)

## Possible Issues

**Plutocracy**

Like all curation methods that involve commitment of funds, those with more capital available have some capacity to exert more influence. I believe the market-mechanism addresses this to some extent, as depositing a large amount of funds to move a token to a vastly different price risks having another set of traders come in and move the price back, at your expense; the Efficient Market Hypothesis in action. However, this resilience is predicated on the market having sufficient depth and diversity of traders.

**Schelling Point Corruption**

For the curation process to be effective, the Market needs to have a strong Schelling Point tying token prices to the perceived quality of the associated quality.

it’s very common for Schelling Points to end up effectively measuring hype around an idea rather than the idea’s actual quality (see most of the ICO market). However I’m uncertain of the extent to which a Schelling Point that reflects hype rather than quality per-se would actually be problematic, as I suspect there’s a strong correlation between hype and quality in many cases, especially when the market is natively short-able. Of course, Schelling Points can shift entirely to market-endogenous speculation, as seen with Hertz’s recent stock price, though the Hertz case appears to have been caused by dark-pool trading and a lack of primary market liquidity, which is not a concern with a bonding curve.

## Possible applications

I think there are two immediately obvious applications for such a curatorial mechanism:

1. An alternative to Reddit/Twitter where users are incentivised to identify compelling content from normally overlooked sources.
2. A simple Dapp where people can register their support or opposition to various EIPs. I think this one could be particularly interesting as it wouldn’t be very difficult to build a prototype. I put together a small mockup to get an idea of what it could look like:

[![EIP Curator](https://ethresear.ch/uploads/default/optimized/2X/a/a9b6cb15daa0a42dad7832109f6852d6e8b1fa96_2_281x499.png)EIP Curator750×1334 61.8 KB](https://ethresear.ch/uploads/default/a9b6cb15daa0a42dad7832109f6852d6e8b1fa96)

That’s all for now. Keen to hear your thoughts.

## Replies

**vbuterin** (2020-06-30):

> \Delta C=C(Δs_1,Δs_2)−C(s_1,s_2)

Did you mean = (s_1 + Δs_1,s_2 + Δs_2)−C(s_1,s_2)?

> To further understand the behaviour of the Cost Function, let us choose sensible parameter values, such as β=1/2 and F1=F2=3 . Then:

I guess an even simpler example would have F_1 = F_2 = 1, in which case the cost C(s_1, s_2) would be the distance of the point (s_1, s_2) from the origin (ie. you could freely move without paying additional costs by going along a circle)?

The nice thing about the circle analogy is that you can use geometrical intuitions to see what the equilibrium is like: clearly, if you start off on the right, the circle starts off going up and tilting very very slightly leftward, so you can buy a lot of opposition tokens at a small cost of support tokens, but then the opposition tokens start getting more expensive, at which point there’s an equilibrium at some ratio. Alternatively, if you *already* have some support tokens, your revenues from selling are (roughly) defined by the portion of the vector (from the current position to the current position minus your token supply) that’s perpendicular to the circle, so if someone else buys many opposition tokens, that vector becomes more and more parallel to the circle, reducing your revenues.

The main challenge in these approaches is indeed the self-referential nature and the possibility of attacking it, especially through really powerful actors making credible commitments. Though I do see how the two-token model alleviates the issue somewhat. It may be necessary to anchor the system in a “ground truth” of some kind to have good incentives…

I look forward to more experiments ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**Levalicious** (2020-06-30):

Could this be used in some format for a non-decentralized social network? Hide this functionality from the actual user and then have some sort of simple ‘trading bot’ that chooses when to sell out on content to get the most ‘likes’ for the future? I think it’s a very interesting idea!

---

**enjeyw** (2020-06-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Did you mean = (s_1 + Δs_1,s_2 + Δs_2)−C(s_1,s_2) ?

Oh yes, good catch. I originally had the new state as s_i'… got lazy when swapping notation! Will fix.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I guess an even simpler example would have F_1=F_2=1

This is true and I like your point about the geometrical intuitions. In that sense it’s really nice to think of the cost function as a metric. However, F_1=F_2=3 has some nice convexity properties that I didn’t go into.

If you set F_1=F_2=1, then you have C=(s_1^2+s_2^2)^{1/2}, and p_1=\frac{s_1}{(s_1^2+s_2^2)^\frac{1}{2}}, in which case token prices are bounded above. This is very similar to the LMSR used in prediction markets C=b*ln(e^{s_1/b} + e^{s_2/b}).

The challenge with this is that it fundamentally changes the risk model for traders, as any return has an upper limit, but it’s still possible to loose all of your investment.

This is fine when you’re talking about probabilities as with the standard LMSR implementation, but there’s not a lot of reason to invest in a pure Schelling Market at p_1=0.95 if you know the price is bound by eg 0<p_1<1. By extension, there’s then less reason to invest at p_1=0.90 because you don’t believe the price can go above  p_1=0.95. Repeat *ad infinitum* and you’ve basically got a no-trade-theorem.

In constrast, F_1=F_2=3 is postive convex, and behaves quite differently from the LMSR in that prices are not bounded above.

---

**enjeyw** (2020-07-01):

Was that supposed to be non-*centralized* lol?

But yes, this is something I think has huge potential!

I’d love to see something where content isn’t necessarily hosted on the platform as per Twitter\Medium\Substack. Rather the only role of the network is to link to and aggregate content in a minimally-opinionated way - basically re-building the web-rings of old, but with a mechanism that encourages curation.

---

**Levalicious** (2020-07-01):

No, I specifically meant ‘classical’ non-decentralized social networks. Basically, I’m also interested if this framework can be reworked to ‘fix’ networks like twitter/whatever.

---

**enjeyw** (2020-07-01):

Oh sorry, my mistake! Hmmmmm interesting question in that case. My gut is that if it’s not something that the end user is aware of in some form, then it probably doesn’t result in the desired behaviour change, but I’m not certain.

