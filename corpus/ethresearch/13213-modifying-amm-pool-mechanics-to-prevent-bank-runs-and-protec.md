---
source: ethresearch
topic_id: 13213
title: Modifying AMM pool mechanics to prevent bank runs and protect LPs
author: kowalski
date: "2022-08-01"
category: Economics
tags: []
url: https://ethresear.ch/t/modifying-amm-pool-mechanics-to-prevent-bank-runs-and-protect-lps/13213
views: 1841
likes: 4
posts_count: 5
---

# Modifying AMM pool mechanics to prevent bank runs and protect LPs

Hi everyone,

Some time ago, we’ve all seen a series of stablecoin depegging fiascoes, most notably the UST one.

As a matter of fact I had some personal funds in [curve.fi](http://curve.fi) UST pool so I was observing very closely as the events unfold.

My main thought was, that once depegging begun it was enforced by a positive feedback loop, where  liquidity providers were closing their positions with the loss out of the fear of suffering an even greater loss if they waited for the peg to be restored. In some sense, I think the mechanism is somewhat similar to a bank run scenario, when even a rumor of a bank going under may actually cause it to go under as a result of sudden spike of withdrawal requests.

Standard, old-school finance had few hundred years to come up with the rules to minimize risks for investors. I think Defi community has a lot to catch up on. I was wondering if maybe this forum is a right place to have a discussion and maybe try to come up with some common set of rules, that would offer better investor protection without the need of calling to life an organization like SEC.

1. To prevent a bank run/everyone trying to withdraw at the same time, the pool should detect depegging event and halt trading that could push the price below the predefined price point. For example, if price of an asset that ought to be 1:1 falls down to 0.95, all LPs are offered a possibility to withdraw. However, they can only withdraw in proportions that the pool is currently at, so if the pool is at say 45/55 ratio, this is the ratio all LPs will receive.
2. Only trades in one direction would be blocked though, the move towards stabilizing the pool should not be discouraged.

This way, in UST scenario all LPs would suffer 55% loss, whilst in normal scenario if someone exited early enough, only lost 5% but investors who lagged behind lost up to 95% of their stake.

I think just this modification would at least remove the time-factor from reasoning of the investors. In the end everyone will get the same deal, regardless of the order in which they close their positions.

But of course there are downsides to this approach as well. Lets discuss those. What rules would you propose to protect market participant better? Or maybe you think AMM pools are good as they currently are?

## Replies

**MicahZoltu** (2022-08-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/kowalski/48/531_2.png) kowalski:

> I think Defi community has a lot to catch up on. I was wondering if maybe this forum is a right place to have a discussion and maybe try to come up with some common set of rules, that would offer better investor protection without the need of calling to life an organization like SEC.

We have been trying to provide this in the form of experts warning people not to buy-in to flawed economic schemes.  The problem is that no one actually listens to us.  ![:confounded:](https://ethresear.ch/images/emoji/facebook_messenger/confounded.png?v=12)  Just because something is desirable, doesn’t mean it is possible.  This includes things like anti-gravity, under-collateralized stable coins, and risk-free yield.  Everyone *wants* these things, and people go out and promise to deliver them, but that doesn’t mean they are actually possible.

When someone shows up claiming to have solved any of these problems, people should default to assuming it is a scam until there is sufficient proof that they have solved some fundamental very hard problem, and they should either research themselves or look to experts in the field to identify when those problems have *actually* been solved.

> What rules would you propose to protect market participant better? Or maybe you think AMM pools are good as they currently are?

The very simple rule of “don’t believe what people tell you on the internet” has protected me from 100% of the scams and poorly designed economic systems on Ethereum.  I recommend everyone follows this rule and we can be done with all of this and move on to building useful things.  ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=12)

---

**kowalski** (2022-08-05):

I think that two things you mentioned are equally possible:

- anti-gravity by the end of XXI century
- wide public listening to warning from experts

![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

We live in times when there is way too much opinions out there and it’s hard or impossible to gauge who are real authorities with your best interest at heart and follows his own agenda.

Still I think that mechanics of Defi protocols should be iterated upon to provide better investor protections and make it more like regulated markets and less like “dog eats dog” kind of situation.

If you think about it, a lot of services provided by the state regulation are the result of people reacting to stronger players taking advantage of the less capable. This is generally good for markets because it prevents crashes or at least make them milder. I don’t think that without offering better protections, at least for users who expect it, Defi could ever seriously make a dent in old-school financial systems.

Regulations are not bad by themselves. It’s only when you put in a center some organization led by people, the goals change from “protecting the weak” to “consolidate power”.

---

**MicahZoltu** (2022-08-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kowalski/48/531_2.png) kowalski:

> This is generally good for markets because it prevents crashes or at least make them milder.

Austrian economists generally believe the opposite, that regulatory interference with a free market results in more catastrophic failures.  At best, you can delay the failure but doing so just makes the failure more spectacular.  They believe this is generally *bad* for markets.

![](https://ethresear.ch/user_avatar/ethresear.ch/kowalski/48/531_2.png) kowalski:

> If you think about it, a lot of services provided by the state regulation are the result of people reacting to stronger players taking advantage of the less capable.

I also would argue that most regulations come out because of lobbying by some special interest group, which is *rarely* financially backed by “the little guy”.

I’m a fan of voluntary regulations.  For example, someone could offer a curated list of not-scams and well-designed-assets and then users could voluntarily subscribe to such a list and be protected from bad investments.  What I’m against is anything that *forces* people to follow such a list, e.g., baking it into the base layer or something.  Uniswap, for example, has token lists and users can choose which to use.

---

**bowaggoner** (2022-08-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kowalski/48/531_2.png) kowalski:

> if price of an asset that ought to be 1:1 falls down to 0.95,

This is close to the root of the issue. Who gets to decide “ought”?

It’s hard to argue that the price of an asset “ought” to be anything other than what people are willing to pay. And for every person you protect by intervening in the market, you may hurt someone else. You might hurt everybody if you make rules that prop up the price of scams and make them less profitable to bet against, making them seem more legitimate than they are.

I’d also say that the role of the market maker should probably be separated from the role of the token issuer or the bank. A market maker shouldn’t be colluding with the bank to protect it.

