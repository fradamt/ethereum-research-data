---
source: ethresearch
topic_id: 8280
title: Prediction market design for betting on many highly improbable events
author: vbuterin
date: "2020-11-29"
category: Economics
tags: []
url: https://ethresear.ch/t/prediction-market-design-for-betting-on-many-highly-improbable-events/8280
views: 8339
likes: 37
posts_count: 21
---

# Prediction market design for betting on many highly improbable events

One of the challenges with prediction markets on events where the probabilities are very lopsided (ie. either very close to 0 or very close to 1) is that betting on the more likely outcome is very capital inefficient. If the probability of some event is 90%, someone wishing to bet for that event must put up $0.9 of capital per $1 of position, whereas someone betting against the event need only put up $0.1 of capital. This potentially (and arguably already in practice) is leading to prediction markets on such events systematically providing probabilities that are “too far away” from the extremes of 0 and 1.

Arguably, it is very socially valuable to be able to get accurate readings of probabilities for highly improbable events (if an event is highly probable, we’ll think about that event *not* happening as the improbable event): bad estimates of such events are a very important source of public irrationality. The position “don’t get too worried/excited, things will continue as normal” is often frequently undervalued in real life, and unfortunately because of capital efficiency issues prediction markets make it hard to express this position.

This post introduces a proposal for how to remedy this. Specifically, it is a prediction market design optimized for the specific case where there are N highly improbable events, and we want to make it easy to bet that none of them will happen. The design allows taking a $1 position against each of the N improbable events at a total capital lockup of $1. The design compromises by making the market have somewhat unusual behavior in the case where *multiple improbable events happen at the same time*; particularly, if one improbable event happens, everyone who bet on that event gets negative exposure to every *other* event, and so there is no way to *win* $N on all N events happening at the same time.

## The two-event case

We start with a description of the case of two improbable events, a and b. We abuse notation somewhat and use 1-a to refer to the event of a *not* happening, and similarly 1-b refers to b not happening. Note that you can mentally think of a and b as the *probability* of each event happening. We consider the “outcome space”, split into four quadrants: ab, a(1-b), (1-a)b and (1-a)(1-b). These quadrants add up to 1:

[![Untitled Diagram](https://ethresear.ch/uploads/default/original/2X/3/3e1bccc9965f1c2f621884c73319084b85cc110e.png)Untitled Diagram321×321 4.79 KB](https://ethresear.ch/uploads/default/3e1bccc9965f1c2f621884c73319084b85cc110e)

Now, we will split this outcome space into three tokens: (i) the “yes A” token, (ii) the “yes B” token and (iii) the “no to both” token. The split is as follows:

[![UD1](https://ethresear.ch/uploads/default/original/2X/2/238c4f67653c7fbe987146a9ba7c636b1f208356.png)UD1365×355 5.75 KB](https://ethresear.ch/uploads/default/238c4f67653c7fbe987146a9ba7c636b1f208356)

The “no to both” token pays $1 only if neither event happens. If only A happens, the YES A token pays. If only B happens, the YES B token pays. If both events happen, the payment is split 50/50 between the YES A and YES B sides.

Another way to think about it is, assuming the probabilities of the events are a and b:

- The price of the NO TO BOTH token should be (1-a)(1-b)
- The price of the YES A token should be a(1-\frac{b}{2})
- The price of the YES B token should be b(1-\frac{a}{2})

If you expand these expressions, you’ll find that they do in fact sum up to 1 as expected. The goal of the design is that if the probabilities a and b are low, and the events are reasonably close to independent, then it should be okay to mentally just think of the YES A token as representing a (as the \frac{ab}{2} term is very small), and then YES B token as representing b.

### Expanding to more than two assets

There is a geometrically and algebraically natural way to expand the design to more than two assets. Algebraically, consider the expression (1-x_1)(1-x_2) ... (1-x_n), claimed by the NO TO ALL token. The YES tokens claim their share of the *complement* of that expression: 1 - (1-x_1)(1-x_2) ... (1-x_n). This is a sum of 2^n - 1 monomials: x_1 + ... + x_n -  x_1x_2 - ... - x_{n-1}x_n + x_1x_2x_3 - ...

Each YES x_i token would simply claim its fair share of all monomials containing x_i: the full share of x_i, half of every x_i x_j, a third of x_i x_j x_k, etc. That is, if only one event x_i happens, the holder of the YES x_i token gets a full $1, but if m events x_i, x_j … x_z all happen, then the holder of each corresponding YES token gets paid \$\frac{1}{m}.

Geometrically, we can see this by extending the outcome space to a hypercube, giving the largest (1-x_1)(1-x_2) ... (1-x_n) sub-hypercube to the “NO TO ALL” token, and then assigning the rest by giving the portion closest to the x_i “face” to x_i. In either interpretation, it’s easy to see how:

1. The different shares actually do sum up to $1 (so money does not get leaked in or out of the mechanism)
2. The events are treated fairly (no x_i is treated better than some other x_j)
3. The mechanism does a good job of giving each YES x_i holder as much exposure to x_i as possible and as little exposure to other events as possible given the constraints.

### Extensions

#### Events with N>2 possibilities (eg. Augur’s “INVALID”)

If there are more than two possibilities for some event, then the easiest extension is to simply treat all possibilities except the dominant as simply being separate events. Particularly, note that if we use the above technique on different improbable outcomes of *one* event, then it reduces exactly to a simple market that simply has different shares for each possible outcome.

#### Emergently discovering which side of an event is improbable

Another useful way to extend this mechanism would be to include some way to naturally discover which side of a given event is improbable, so that this information does not need to be provided at market creation time. This is left as future work.

## Replies

**ryanberckmans** (2020-11-30):

Here, we may have a sort of “law of leaky abstraction,” where capital efficiencies gained from this proposed market design might be weighed against trader UX and wholistic transaction costs.

Prediction markets’ predictive power increases with volume, especially ongoing volume as traders reassess their positions. At current levels of maturity, PMs are an entertainment product. What we’ve seen is that, all other things equal, simpler markets drive volume. The entertainment-minded trader wants to understand the market herself. There’s a reflexive common knowledge aspect in that she wants to believe that her fellow traders will trade the market so that her purchase of shares has a social utility component. She is likelier to believe that the market will be widely traded if she believes her fellow traders understand the market.

Under this proposal, there may be a few tricky UX issues that have a chilling effect on volume:

- explaining to traders why these events are bundled, and the choice of the bundle
- explaining to traders why the “yes” side of long odds must split the pot if rare events co-occur
- managing around the fact that trader has a price mapping problem in that she may care only about event A and not B, thinks YES A will occur with probability a, yet to buy YES A she must handle the fact that the price of YES A is a(1-b/2)
- to a lesser degree, explaining why the “no” side loses if any rare event occurs

Potential open questions / next steps for this proposal from the perspective of [catnip.exchange](https://catnip.exchange):

- can this market design be built on Augur v2, or does it require protocol changes?
- what might be guidelines for identifying rare events to bundle into one of these markets? Starter: two events A and B that are expected to be rare (to Vitalik’s point, this may be hard to tell up front), maximally independent, and settle on the same date
- proposals for UI mechanisms + messaging to address the UX issues above

---

**vbuterin** (2020-12-01):

I agree that the assets other than NO TO ALL are tricky to explain; hence I think this kind of market would work best when the probabilities of the events truly are quite low and there’s only a ~10-20% or less chance that *any* event would be triggered. And I agree that the choice of bundle is somewhat arbitrary.

> can this market design be built on Augur v2, or does it require protocol changes?

I think it can be built on top of augur v2, except that the events would need to be defined differently. They would all need to be range events (ie. like prices), which are defined as “this market should resolve to 1 if event A and no other event in the bundle {A, B … Z} happens, 1/k if k events in the bundle {A, B … Z}, including A, happen, and otherwise 0”.

I think there are natural categories to experiment with; “will weird third party political candidates do well” (aggregating across multiple electoral races and maybe even countries) is one. That said, for early-stage experiments, I think just centrally picking a bundle of eg. unlikely political events and a bundle of unlikely economic events, would work fine.

> proposals for UI mechanisms + messaging to address the UX issues above

I’m somehow less worried about this! “NO TO ALL” is quite self-explanatory, and the others can be described as “A [reduced payout if multiple events from this bundle happen]”. I predict some unavoidable level of confusion when something like this is rolled out initially, but then the community would quickly understand what’s going on after even a single round finishes.

---

**samueldashadrach** (2020-12-04):

This design transfers the complexity of the model to YES betters. Practically speaking however, YES betters are more likely to be common folk, either seeking insurance or gambling, whereas NO betters are larger funds who provide insurance for lower returns.

I would prefer a model that transfers the complexity to the NO betters instead.

Transferring complexity to a third party is also possible, in fact it’s the kind of model that TradFi may be most comfortable with. Allow NO betters to use their NO tokens as collateral to buy NO tokens on more markets, as they please. This choice is important because not everyone wants to provide insurance on every market. Have liquidators as a third party that bear the losses if two NO markets simultaneously swing at the same time, which leads to collateral not being liquidated in time.

Liquidators will profit from people using NO collateral, either via a margin of capital left for liquidation, or an interest rate.

---

**vbuterin** (2020-12-05):

So that design would *still* require $N collateral to bet against N events, at least if we want to preserve simplicity for YES voters by giving them an unconditional guarantee of $1 upon victory. It just creates two classes of NO voters, one of them called “liquidators” that absorbs the complexity.

Unfortunately, I do think that the asymmetry of the situation inherently doesn’t leave good choices other than increasing complexity on the YES side…

---

**samueldashadrach** (2020-12-05):

You’re right, I just tried to take advantage of the fact that bet resolutions (and antecedent price movements) are likely to happen sequentially not simultaneously. In the worst case, this still requires liquidators to have a lot of capital ready to absorb losses.

Is there a better way to take advantage of this (sequential resolution)?

Also my kind of a model creates three tranches with different risk-reward tradeoffs. Some more analysis of how many actors are willing to take on how much risk may be prudent, since the lack of low risk - low reward actors is what causes prediction markets to skew towards YES betters in the first place as you note. Tranching is common in TradFi since it allows actors with various risk-reward profiles to enter the market in some way or the other.

---

**vbuterin** (2020-12-05):

Agree that tranching is valuable and can create efficiencies! We could for example adjust the design by adding a tranche for “<= 1 event will happen”, so that there’s two winners in any result and event bettors will be fully compensated if the case of anywhere up to (and including) two events taking place.

If the events resolve sequentially, one approach would be to structure the assets as follows:

- YES TO 1
- NO TO 1 BUT YES TO 2
- NO TO {1, 2} BUT YES TO 3
- …
- NO TO {1, 2...n-1} BUT YES TO n
- NO TO ALL

This way you can get the odds for each event by taking the ratio of the price of its associated asset to the sum of the prices of all assets later than it in the list (assuming the event is independent of sequentially earlier events, of course). This market structure would also be really interesting and worth trying out.

---

**samueldashadrach** (2020-12-05):

This looks interesting. Sorry if I’m slow but … how does someone bet on an event in this sequential model? If someone wants to bet YES on event 3 and have no exposure to other events, does he have to wait for events 1 and 2 to settle before buying event 3?

---

**vbuterin** (2020-12-05):

Unfortunately yes… Or they could balance their exposure somewhat by buying a little bit of the first two assets alongside the third.

---

**samueldashadrach** (2020-12-05):

If we assume all tokens are fairly priced, then that’s doable actually. Using that ratio they can calculate the implied probability of each of the events and figure out how much to hedge. Ofcourse a buyer would prefer not to assume a market is fairly priced when he can’t analyse it himself.

I do still kinda feel like we’re optimising for the wrong thing, I’ll writeup when I have something concrete. Definitely an interesting topic.

---

**hoytech** (2021-02-17):

The common name for a bet of this type is a [parlay](https://en.wikipedia.org/wiki/Parlay_(gambling)), and it’s one of the most common types of sport bets. To initiate an in-depth discussion on this topic, go to literally any bar on a Sunday night (or to any horse track) and ask your neighbours what’s on their tickets.

Usually parlays are bad bets since the sportsbook marks them up a lot. There are some exceptions though:

> the events are reasonably close to independent

This is much easier said than done. A common strategy is to find bets that are more correlated than the sportsbook understands, for example when a low-scoring game favours team A more than team B.

Another smart reason to use parlays is to place bets that are larger than the betting limits offered by the sportsbook. If the first 2 legs on a 3-leg parlay win, then the remaining leg can have a much higher amount bet on it than the sportsbook would have allowed if you had singly bet that last leg (do this at 2^2 books for full coverage).

---

**sheegaon** (2021-06-13):

I agree with [@samueldashadrach](/u/samueldashadrach) that the complexity of the bet should be shifted as much as possible to the “NO” side. Of course, as [@vbuterin](/u/vbuterin) says, a design that has absolutely no complexity on the “YES” side would require full collateralization by the “NO” side. The trick to solving this is likely to be a design which shifts enough complexity to the “NO” side so that the corresponding “YES” bet can be seen as practically equivalent to the simple “YES” bet, but still allowing << $N collateral from “NO” bettors.

The situation we’re talking about is a classic insurance problem. “YES” bettors are akin to insurance policy holders, while “NO” bettors are the issuers, or insurance companies. Insurance companies hold far less collateral than would be necessary to make payments on all their claims. Nevertheless they are trusted by most common people to have enough money to make good on their claims very close to 100% of the time.

The right prediction market design for highly improbably events is functionally equivalent to a market design for blockchain-based insurance. A few models for such insurance already exist, but there is no clear winner as of yet. I believe the right market design for what you discuss has not yet been invented. I have some ideas on how to improve on these models, which I’m still fleshing out before posting publicly. I believe borrowing the core idea of tranching risk from TradFi, with multiple interlinked collateral pools, is the right one. I don’t know if what I have in mind is similar to what [@samueldashadrach](/u/samueldashadrach) is referencing. I’d welcome further discussion offline.

---

**chaseth** (2023-09-23):

It’s been 2 years since anyone has posted… Are there any experiments ran, or running, that showcase any of these theories? Where are we now…?

---

**bowaggoner** (2025-03-12):

Should we compare this approach to using e.g. LMSR or another AMM with the following specific betting language?

- We have securities x_1,\dots,x_n,y,z where: x_i represents “event i and only event i occurs”, y represents “none of these events occur”, and z represents “more than one occur”.
- Now we run LMSR or another AMM design on these n+2 mutually exclusive and exhaustive securities. It will maintain a probability distribution on these n+2 events, i.e. only one dollar is required to bet against n events, by purchasing y.

The original post allowed the slightly more natural interface of betting on “i happens” rather than “i and only i happens” (although in the motivating scenario, these have almost the same probability). But, a bettor who just wants to express that x_i is quite likely can always buy both x_i and z (the interface could even suggest a bundle containing some amount of z by default, according to current prices).

I think one can always in theory solve this general problem with LMSR, but doing so in a computationally efficient way is often the issue. (One can always run LMSR on all 2^n outcomes and achieve the goal of only needed to stake $1 to bet against multiple events, but efficiency is the problem, even if a limited UX is presented.)

---

**bowaggoner** (2025-03-17):

Another feature you would want to have with this proposal is ability to partially resolve the market as the events occur. (If we bundle together a number of unrelated improbable events, it will be hard to find many that all resolve at the same time.) LMSR will make this easy: when x_1 resolves, if it’s true, then we can immediately resolve y to “no”. Then, we can take x_2,\dots,x_n and z, and we can split the z token into y',z' where y' represents “none of x_2,\dots,x_n” and z' represents two or more. If x_1 resolves to false, then we don’t need to do anything and the market continues. I think the original proposal could probably be made to work as well.

---

**clesaege** (2025-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> Should we compare this approach to using e.g. LMSR or another AMM with the following specific betting language?
>
>
> We have securities x_1,\dots,x_n,y,z where: x_i represents “event i and only event i occurs”, y represents “none of these events occur”, and z represents “more than one occur”.
> Now we run LMSR or another AMM design on these n+2 mutually exclusive and exhaustive securities. It will maintain a probability distribution on these n+2 events, i.e. only one dollar is required to bet against n events, by purchasing y.

This is interesting and may look simpler for traders. If we assume events to be independent, we can get probabilities by rescaling:

P(i)=\frac{x_i (z+\sum^{n}_{j=1}x_j)}{\sum^{n}_{j=1}x_j}

However I think the capital efficiency gains would be smaller than the initial proposal as if z price is high, most of the cost of predicting i would be spent buying the z token which doesn’t provide much info on i.

So this settings seems attractive when the likelihood of multiple events happening is low (while the original proposal works even in cases where the likelihood of each individual event is low, but the likelihood of multiple event happening is high). So in the initial proposal we can group more events within the same market.

---

**clesaege** (2025-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/chaseth/48/13258_2.png) chaseth:

> It’s been 2 years since anyone has posted… Are there any experiments ran, or running, that showcase any of these theories? Where are we now…?

So at Seer, we did end up more or less inadvertently implementing this proposal. The initial idea was to be able to predict the number of seats a party would get in an election, so we ended up implementing multiscalar markets (tokens of each party redeems for the proportion of the seat the party got). It then looked obvious that we could use the same logic for events leading to multicategorical markets (split the underlying between the tokens of all events which happened, [example for the Romanian election](https://app.seer.pm/markets/100/who-will-win-or-advance-to-the-next-round-in-the-re-run-of-round-1-of-the-2024-romanian-presidential-election?outcome=A+candidate+or+candidates+not+listed)).

It’s only after the beta release that we got the idea to use those types of markets to predict many improbable events and this thread has been quite helpful figure out the details.

The idea is to evaluating the risk of:

- Rollups suffering from a major hack.
- Staking operators being slashed.
- Assets of lending markets crashing faster than the ability of a lending market to liquidate related positions.

We’re currently looking for an entity who’d be interest in consuming those kind of information and we’ll launch an experiment.

---

**bowaggoner** (2025-03-20):

That’s very cool, and I like the idea of using this for tail risks!

Your point is very interesting about the regime where Pr[i happens] is low for all i, but Pr[some i happens] is high. In that case, I’m not sure if the original proposal is doing much different from having n independent markets, so if we knew in advance that we’re in this case, we might just do independent markets? But it’s nice that the design more cleanly handles that case if it does happen, compared to my LMSR version.

It might be possible computationally to implement a version of LMSR that only allows bets of the form “Yes i”, “No i”, “No To All”, “Yes To At Least One”. Underneath the hood, it would implicitly maintain a probability distribution over all 2^n outcomes, by only tracking weights for the things that have been bet. Even if it’s doable in polynomial time, it’s probably too expensive on a blockchain, though. An interesting generalization would be allowing bets on exactly how many of the events will happen.

---

**clesaege** (2025-03-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> Your point is very interesting about the regime where Pr[i happens] is low for all i, but Pr[some i happens] is high. In that case, I’m not sure if the original proposal is doing much different from having n independent markets, so if we knew in advance that we’re in this case, we might just do independent markets?

The initial proposal would be quite different compared to having independent markets. Concrete example: [L2BEAT](https://l2beat.com/scaling/summary?) is listing 153 platforms. The yearly likelihood of each platform suffering from a major hack is probably something of the order of 1-5% (let’s pick a 3% average). So we’d have on average approximately 5 major hacks per year and a z of almost 1.

If we wanted to have 153 markets with a potential gain / collateral of 20k$ in case of a hack, it would require 3M$ of capital.

But with the proposal we could have a unique market with 100k$ of collateral which would pay on average 100/5=20k$ for tokens of projects getting hacked.

I think the key of making this work is to allow users to abstract this kind of complexity through a good UI. Users would just enter the risk estimates for platforms they have knowledge of, and the the UI should automatically convert this into optimal trades.

---

**bowaggoner** (2025-03-21):

That’s really interesting. I see how it’s nice in terms of collateral by the market maker. I’m wondering how informative the prices would end up being in that environment? If I’m thinking of buying “Yes i will get hacked”, then if the hack happens, I’ll get a payout of maybe 1/3, maybe 1/4, 1/5, 1/6 depending on how many others get hacked. So my fair price is in a pretty big range depending on what I think about the total number of likely hacks. On the other hand, we could imagine making a separate market for that number, which could help people calibrate.

> I think the key of making this work is to allow users to abstract this kind of complexity through a good UI. Users would just enter the risk estimates for platforms they have knowledge of, and the the UI should automatically convert this into optimal trades.

Strong agree!

---

**clesaege** (2025-03-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/bowaggoner/48/7119_2.png) bowaggoner:

> If I’m thinking of buying “Yes i will get hacked”, then if the hack happens, I’ll get a payout of maybe 1/3, maybe 1/4, 1/5, 1/6 depending on how many others get hacked.

This is true, but with a good frontend users don’t even need to think about this. Because with the current price of the tokens, we can infer the probability of all events if we assume them to be independent.

I’ll show the case where n=3, with probabilities of events A, B, C being respectively a, b and c. We’ll call t the number of events ending up happening.

- The price of Y (“No to all”): y=(1-a)(1-b)(1-c)
- Price of A YES: x_A=a(1 - \frac{1}{2}p(t=2|A) -\frac{2}{3}p(t=3|A)) = a (1-\frac{b}{2}-\frac{c}{2}+\frac{b c}{2})
- Price of B YES: x_B= b (1-\frac{a}{2}-\frac{c}{2}+\frac{a c}{2})
- Price of C YES: x_C= c (1-\frac{b}{2}-\frac{a}{2}+\frac{b a}{2})

So we have a system of 4 equations with 3 unknowns. I don’t think that there is a closed form equation for it, but a solver should be able to handle it.

I tried on Wolfram alpha with y=0.1,x_A=0.2,x_B=0.4,x_C=0.3 and got the result.

[![image](https://ethresear.ch/uploads/default/original/3X/a/4/a48c9f2774f77b87b642a5c6391dba19cab1275a.png)image424×439 15.4 KB](https://ethresear.ch/uploads/default/a48c9f2774f77b87b642a5c6391dba19cab1275a)

Now, the frontend to make those kind of predictions would work the following way:

- Compute the current event probabilities and display those to users.
- User picks an event he wants to predict on.
- User specifies his predicted probability of the event.
- Compute the price of the related token, but this time replacing the probability of the event in question by the user input.
- Place an order to buy/sell the related token depending of the computed price.

Continuing with the current example, the front would display:

a: 0.382

b: 0.654

c: 0.531

y: 0.100

The user wants to predict that a is 0.5, we express it by a'=0.5.

So we compute x_A'= a' (1-\frac{b}{2}-\frac{c}{2}+\frac{b c}{2}) = 0.262.

So the frontend proposes to buy tokens of the event A up to a maximum price of 0.262.

The drawback is that there would be some randomness in the user payout (I mean from their perspective, as they’d get an exposure to events they are not knowledgeable about). But if the market is pretty big, the relative variance in term of the number of events happening would be lowered (so the market would actually be less random the larger it is).

I wonder if we could have a prediction market based on this principle. I would see this a bit like the “GMX of prediction markets”.

