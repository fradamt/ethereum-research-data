---
source: ethresearch
topic_id: 19753
title: Is it worth using MEV-Boost?
author: Nero_eth
date: "2024-06-06"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/is-it-worth-using-mev-boost/19753
views: 6777
likes: 36
posts_count: 10
---

# Is it worth using MEV-Boost?

# Is it worth using MEV-Boost?

To answer that question from an economic perspective, we will look into the APYs.

> *For simplicity, we assume a total of 1 million active validators and ignore sync-committee rewards.*

> *The underlying data ranges from November 2023 - 6 June 2024 and includes all slots.*

First, let’s check the **difference between local block building and using MEV-Boost**.

We can see that the block reward is higher for MEV-Boost users:

[![reward_comparison (3)](https://ethresear.ch/uploads/default/optimized/3X/e/9/e91a721ea6757f818e7a0fd840534c63a581145e_2_690x316.png)reward_comparison (3)1200×550 22.3 KB](https://ethresear.ch/uploads/default/e91a721ea6757f818e7a0fd840534c63a581145e)

**The median block reward increases from 0.0076 to 0.0380 ETH (400% more).**

## What does that mean on an annual basis?

The statistical 2.6 blocks a validator gets to propose per year yield a total of **0.0199 ETH in block rewards**.

For MEV-Boost blocks, the 2.6 blocks yield a total of **0.0998 ETH per year**.

When shown in a pie chart, we can see that the share of the block reward (green) grows from 2.96% to 13.4%, compared to the total expected rewards per year.

[![rewards_comp_pie](https://ethresear.ch/uploads/default/optimized/3X/c/4/c452b447c422ed7be7095bd313ef4f9081bcf9c4_2_690x316.png)rewards_comp_pie1200×550 37.1 KB](https://ethresear.ch/uploads/default/c452b447c422ed7be7095bd313ef4f9081bcf9c4)

### What does that mean for the APY?

For validators **not using MEV-Boost**, the expected annual revenue is **0.929 ETH.**

For validators **using MEV-Boost**, the expected annual revenue is **1.009 ETH.**

**These are additional ~8.6% of revenue.**

**Using MEV-Boost increases the APR from 2.93% to 3.24%.**

For the **APY** (compounding every epoch):

\text{APY}_{local\ builder} = \left(1 + \frac{\text{APR}}{n} \right)^n - 1  = \left(1 + \frac{\text{0.0297}}{365 \times 225} \right)^{365 \times 225} - 1 = 2.97\%

\text{APY}_{mevboost} = \left(1 + \frac{\text{APR}}{n} \right)^n - 1  = \left(1 + \frac{\text{0.0324}}{365 \times 225} \right)^{365 \times 225} - 1 = 3.29\%

**Finally, using MEV-Boost increases the APY from 2.97% to 3.29%.**

---

Find the code used for this analysis [here](https://github.com/nerolation/is-mevboost-worth-it).

## Replies

**BrunoMazorra** (2024-06-06):

It’s probably true that MEV-Boost has increased the profits of validators (to some extend). But I want to add some points. First, we haven’t observed the counterfactual scenario. If no validators use MEV-Boost, searchers would optimize their strategies through priority gas auctions potentially increasing the competition on blocks being build without using MEV-Boost and so increasing the revenue. Second, probably users would not have private communication with validators (potentially leading to more MEV due to sandwich attacks!). Therefore, I doubt we would see a 2.97% APR in the counterfactual scenario. In other words, you are not taking into account the Lucas critique.

Doing that I could also make the following troll take:

I could say that MEV-Boost reduced the MEV since if users send their private orderflow through the meempool searcher could sandwich them, increasing the  Validators’ revenue!

Also, we should also consider the costs associated with running the MEV-relays when evaluating the net benefits.

---

**sui414** (2024-06-06):

I think the 2 sides of opinions comes from the different scope when u read the data:

- if you compare it with consensus layer rewards, MEV is not that big (i.e. when comparing the % increase on top of staking APY it’s only a +0.32%, which is ~10% lift)
- but if you compare within execution layer it is big (it increased validator’s revenue by 4x)

---

**Evan-Kim2028** (2024-06-06):

Could you use KDE (kernel density estimation) or something else to calculate the expected return? The mev-boost distribution is clearly not normal and much more skewed than the local-building distribution.

---

**tripoli** (2024-06-06):

It looks to me like you are calculating the returns using the medians? Because the skew makes the difference even bigger. For MEV-Boost the average is > 2x the median, whereas for local building the average is ~ 1.5x median.

Your medians also seem a little low to me, are you factoring in missed slots? Ignoring missed slots, [this is what I get](https://dune.com/queries/3805389).

| Block Type | Median [eth] | Average [eth] |
| --- | --- | --- |
| MEV-Boost | 0.049999 | 0.11214 |
| Local | 0.011345 | 0.01634 |

---

**Nero_eth** (2024-06-06):

Yeah, using the medians and skipped the section on variance to make the piece shorter.

I agree that some important information gets lost - this is the same that [@Evan-Kim2028](/u/evan-kim2028) indicates too.

Regarding the numbers, I’ve filtered mssed slots too. Also, it’s txfee - basefee for local builders.

I got the following:

| Block Type | Average [eth] | Median [eth] |
| --- | --- | --- |
| MEV-Boost | 0.072330 | 0.041258 |
| Local | 0.016221 | 0.011005 |

Using data as of Nov 2023.

---

**Nero_eth** (2024-06-06):

However, I believe that transitioning from a potentially more centralized environment dominated by large stakers using MEV-Geth to one where MEV is accessible to proposers was the right decision. To strengthen the argument for MEV-Boost, it’s worth noting that MEV-Boost would have inevitably been developed eventually. By opening it up and making it accessible to everyone, a significant first step in the PBS roadmap was taken.

Challenges such as censorship and node operator centralization are not new to PBS. It should be evident that priority fee auctions are far less efficient than the current external block market.

MEV inherently has centralizing forces, as do economies of scale. PBS is simply the fairer evolution of MEV-Geth.

---

**antonydenyer** (2024-06-07):

It’s also worth noting that the other side of the supply chain was opened up. Previously, only larger, more sophisticated entities had the know-how and contacts to send private transactions.

Furthermore, transaction simulation was costly and, again, only available to large entities. Flashbots offers `eth_callBundle` for free and is accessible to anyone. All block builders offer revert protection, which has negated the need for simulations in many scenarios.

---

**hasu.research** (2024-06-10):

In my eyes, mev-boost has achieved both of the outcomes you describe

- minimize MEV from users by giving them access to fast private mempools, which would be impossible in a no-PBS world
- maximize MEV for validators under the constraints imposed by those users, in particular said use of private mempools, but also other techniques like intents etc.

There is no doubt in my mind that w/o mev-boost, MEV on Ethereum would be *a lot* higher than it is today. At the same time, users would use Ethereum less, since transacting would be more expensive.

This is why the most recent criticism of PBS is so braindead; it simultaneously argues that (1) mev-boost doesn’t do anything for users, and (2) it doesn’t add much revenue for validators. As we see, they cannot both be true at the same time.

---

**BrunoMazorra** (2024-06-10):

Just to clarify, my point is not against the claims themselves, but rather against the methodology used to achieve those claims. After all, we are in EthResearch, not MEV-BoostShill. That being said, I generally agree that the criticisms of PBS are not very well-structured; they haven’t been able to answer whether there are incentive-compatible mechanisms that offer better guarantees to users.

I do not disagree with your take, except for the statement about “impossibility.” Saying something is impossible in the early years of MEV-tech development seems like too bold a statement. Time will tell whether it is truly impossible, or if we simply haven’t had the right tools to understand or develop other mechanisms.

What is true is:

1. Cool products were enabled by MEV-Boost, such as MEV-Share, MEVBlocker, and Flashbots Protect. Thus, users can operate in a more user-friendly manner without needing to be more sophisticated.
2. We currently face a builder oligopoly, and who knows if some of them would prefer a monopoly.
3. The relay runs at a deficit; MEV-Boost is not individually rational for all participants.

That being said, I have always thought that minimizing or maximizing MEV is not the right mental model. We need to maximize overall welfare with the constraint of having incentive-compatible mechanisms. If that approach maximizes or minimizes Miner Extractable Value (MEV), then so be it. MEV is an externality of having rational auctioneers.

