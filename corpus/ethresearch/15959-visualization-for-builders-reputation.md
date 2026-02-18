---
source: ethresearch
topic_id: 15959
title: Visualization for builders reputation
author: Keccak255
date: "2023-06-22"
category: Economics
tags: [mev]
url: https://ethresear.ch/t/visualization-for-builders-reputation/15959
views: 4417
likes: 14
posts_count: 13
---

# Visualization for builders reputation

*thanks to Thogard, Dougie DeLuca, ek, askyv, masato james, jun, yupi for discussion and feedback.*

## Abstracts

This article addresses the centralization of block builders, which may reduce the user experience and censorship resistance of Ethereum. I argue that an important solution from a future where the supply chain building blocks becomes centralized, dominant & predatory is to make the reputation of the builders visible.

## Background

- Factors for centralization

Block builders collect order flow to build high-value blocks. If the collection is only from open, permissionless access, then centralization will not occur. Currently, however, they can be collected from private spaces as well, and this is a factor in centralization.

- Order flow collection channels

Public Order Flow : Transactions that are publicly broadcast through mempool and are the easiest to study because anyone with the resources to run a few Ethereum nodes can have high visibility
- Searcher order Flow : Transactions where the searcher sends bundles to n builders, and needs to select builders who can build highly competitive blocks without stealing their own MEV. Or, in some cases, resourceful searchers who do not want their MEV stolen may build a full block themselves.
- Private Order Flow : This is the collection of order flow independently through RPC endpoints, and is basically a channel dedicated to a specific builder, so other competing builders do not have access to it.

Correlation between builder market share and searcher order flow

As the number of searchers increases, the number of bundle order combinations increases, potentially allowing builders to extract more value. According to data from [Frontier Research](https://frontier.tech/builder-dominance-and-searcher-dependence), the top four of the 38 active builders have a combined 87% market share with more searcher submissions than the other builders, with 88.5% of searchers submitting to four or more builders.

- Rational Searcher Selection

Since the combined market share of the top seven builders covers nearly 94% of the market, the most rational choice for searchers would be to submit to multiple builders.

However, increasing the number of submissions to too many builders makes it difficult to identify which builder has stolen the bundle and makes it easier for one builder to dismantle and sandwich the bundle. Also, if the share ratio is low just because they are trustworthy, they will not be able to build competitive blocks, which will negatively affect inclusion. So how does a searcher select the builders? It chooses a small number of trustworthy builders who can build highly competitive blocks. There is a trade-off between the cost of trusting these builders and inclusion.

Also note that searchers follow economic rationality, so it is likely that they will all make the same choice. For example, if builder A appears in the future with more than 50% market share, a rational choice would be to send to builder A and a few other builders.

Now, what if this is closer to 100%? The rational choice for most searchers would be to send only to the builder with a share rate close to 100%.

This rational choice of searchers and competitive environment of builders will cause centralization of block builders.

## What is the problem with centralization of block builders?

- Disincentives for new entrants and competition.

[![](https://ethresear.ch/uploads/default/optimized/2X/8/88c2c45bd3853bb39dc415fb584aad53e02df4e2_2_690x343.jpeg)1920×955 58.8 KB](https://ethresear.ch/uploads/default/88c2c45bd3853bb39dc415fb584aad53e02df4e2)

Source: [Builder Dominance and Searcher Dependence](https://frontier.tech/builder-dominance-and-searcher-dependence)

The figure of the percentage of blocks built by each builder normalized by searcher transmission rate shows that the differences in searcher transmission among builders are more pronounced. Searcher rationales and the competitive environment of the builder market tend to create further disparities even among the top builders, as certain block builders have the advantage of monopolizing the market, discouraging new entrants and competition.

- censorship-as-a-service

As newcomers and competitors are weeded out, a dominant `n = 1` builder may emerge and extract maximum value from users by exploitative means to maintain its dominance. One example of this is the formation of the [censorship-as-a-service market](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/4) to exclude users from trading from the block. The formation of an open market where users can bid to exclude transactions from the block. The user sends a bribe and a hash of someone else’s transaction that he does not want included in the block to the `n = 1` builder. The block builder is only considered if the bribe is more than the gas (and MEV) he would have received from the transaction, allowing him to make a profit by censoring traction. Similarly, an `n = 1` builder could also provide a protection service by sending a hash and a bribe to help users protect themselves from this censorship, which would only be considered if it is more than the highest censored bid for the transaction. With the formation of such a self-contained market, users would have to guess whether their own transactions could be censored, and would have to pay an additional fee to pay for censorship protection.

- The Downside of Block Generation

If a dominant block builder is created, all block creation may stop if for some reason the `n = 1` builder goes offline. It has been [argued](https://ethresear.ch/t/block-builder-centralization/12135/2) that it is not particularly important that there are many regular block builders, but that it is critically important that there are several people who regularly try to create blocks, even if some of them do not succeed.

## So what to do?

- Visualizing Block Builder Reputation

Visualizing the reputation of block builders will reduce the cost of credit for searchers and make it easier to send to multiple builders. This can put builders at risk for dishonest behavior.

For example, there are searchers who assign specific values such as calldata, priority fee, hash, etc. to each builder and AB test which builder also sandwiched it. Creating a receptacle to collect the results of such AB testing and visualize reputation would have the effect of helping searchers and POF decide which builders to send to.

There may also be a strong need to develop tools that can easily monitor and detect plagiarism, assuming searchers are unable to spot dishonest builders.

- Who will this lead to value for?

This [page](https://collective.flashbots.net/t/block-scoring-for-mev-boost-relays/202/8?u=revy) asks, “To whom does scoring a block lead to value?” It is argued that the scoring target will vary depending on the question "to whom does it lead to value?

1. is it value to the builder?
2. the value to the proposer?

For example, if one were to calculate 1, it would not be to the builder’s advantage to include in the calculation transactions that would increase the value of the block, as it would give the impression that the builder is lining their own pockets with a large portion of the MEV. 2. The value to the proposer must be taken into account in the calculation.

In this article, neither 1 nor 2, but the value to searchers and users, who are at a more upstream layer than builders, needs to be considered, and they are the focus of the calculation here, as risk management against dishonest behavior such as reverse engineering of bundles is important to them.

- Concerns

1. the account of the user or searcher doing the evaluation may be revealed. Since searchers, in particular, tend to avoid account identification, it is necessary to use a mechanism such as stealth addresses to ensure the privacy of the evaluator.
2. the system to measure evaluators and their credibility should also be taken into consideration. For example, in the popular Japanese service “Eat Log”, people who visit many restaurants and write many reviews have a large influence on the score, while those who write reviews for only a few restaurants have a small influence. How to calculate such indicators needs to be discussed.
3. it is possible that the effect of the reputation system works in the opposite direction, encouraging order flow to be attracted to the top few builders more. The problem, however, is that n = 1 dominant builders will arise, and the ease of sending to multiple builders due to reputation visualization could prevent the worst case. The issue of new builders not getting order flow will be explored in depth in another article.

## Conclusion

The right of builders to build competitive blocks needs to be decentralized, and this requires searchers to keep sending bundles to multiple builders. To do this, we will lower the cost of credit for searchers and make it easier for them to send bundles to multiple builders by providing builders with appropriate monitoring and reputation systems.

This is similar in many ways to the behavior we have seen when booking a meal or hotel in a new location, where we search for high ratings on Google and other search engines to reduce the likelihood of encountering low-quality service.

Nevertheless, there is much room for discussion about formulas, implementation, new options and trade-offs, and we would like to hear other ideas and opinions from the community. The purpose of this article is to advocate the concept, facilitate discussion, and hopefully talk about ways to solve the centralization of block builders.

## List of Notes, Citations, and References

- Block scoring for mev-boost relays - Relays - The Flashbots Collective
- Block builder centralization
- MEV-Boost: Merge ready Flashbots Architecture
- Two-slot proposer/builder separation - #5 by pmcgoohan
- Builder Dominance and Searcher Dependence
- The Year Ahead for Infrastructure - Delphi Digital

## Replies

**gutterberg** (2023-06-26):

This analysis concludes that a searcher sends the same bundle to multiple builders. Could it instead be that a searcher is sending different bundles to different builders (i.e., a diversification mechanism) and therefore appears in the blocks of many builders?

Additionally, if a searcher sends the same bundle to multiple builders, do all builders receive the same bid or do larger builders have leverage to request a bigger cut?

---

**winnster** (2023-07-10):

Currently, most understanding of a builder’s credibility comes from reading between the lines of discord channels. Some kind of public platform that provides more systematic and accessible insights on builder’s behaviours can be very helpful in mitigating harmful builder centralisation. My main concerns with such a platform that you suggested are:

1. Will this platform accelerate builder centralisation? Larger builders will gain even more credibility and smaller builders will gain little. However, this platform may still provide positive benefits to smaller builders since now their credibility went from 0 to 0.1. This concern may also be mitigated if the platform only gave visibility to smaller builders (i.e. those with market share <10%) and not even showing the top ones.
2. Since this will be a permissionless and anonymous platform, how will it prevent or mitigate DoS’ing? A malicious builder can write up lots of reviews for themselves.

Overall, I think this platform is much needed! Likely, most searchers have their own internal builder credibility dashboard. By way of such a platform, we can contribute to equalising the playing field of searchers and builders alike.

---

**DonMartin3z** (2023-07-11):

Amazing. i would love to connect whis work as an solution to integrate our project. We are trying to create strong iniciatives for the blockbuilders become educational institutions and sustainable communities.

---

**maniou-T** (2023-07-11):

great, this article sheds light on an important issue in Ethereum and invites the community to engage in dialogue and propose solutions to ensure a decentralized and robust ecosystem.

---

**Keccak255** (2023-07-12):

Thanks for the feedback!

1. That is a possibility. If searchers defaulted to sending bundles only to the top builder with the highest rating score, this would increase centralization.
To counteract this, we need to consider counteracting this by putting this score on a discrete scale rather than a continuous one, or, as you say, not showing the top builders.
2. I had not yet thought of specific ways to prevent DoS, but I think there is a great deal to learn from the examples that already exist. If you have any good ideas, please let me know.

I too think we need this platform. I would actually like to discuss and develop the implementation aspects and get a grant to test it

---

**Keccak255** (2023-07-12):

Yes.

Also, I think the bid amount is not constant and can be adjusted for each block builder.

---

**Keccak255** (2023-07-12):

The person who provided feedback was omitted and could not be corrected, so I am adding it here.

thanks to Thogard, Dougie DeLuca, Michael, ek, askyv, masato james, jun, yupi for discussion and feedback.

---

**Keccak255** (2023-07-12):

Thank you, let’s come up with a good synergy for both of us.

---

**winnster** (2023-07-12):

A more pressing concern that I have is whether the premise of this dashboard can align with economically rational searchers. Searchers have incentives to withhold information about builder credibility to prevent competition for the same block space.

A builder that gets more searchers means more bundles are competing for the same amount of block space. Searchers will now have to pay more to get into the block. More critically, having more bundles also increases the likelihood that a searcher’s bundle will conflict with another searcher’s. Overall, divulging information about builder credibility leads to higher cost of doing business for a searcher.

This comes down to the fact that searching is, more often than not, a zero-sum game. Searchers benefit from information asymmetry and the economically rational ones will not contribute to transparency.

One way that economically rational searchers can be incentivised to contribute is by motivating them to think about the bigger pie here. A monopolistic builder can seek rent from searchers by asking to them to pay more from their profits in order to get included. Since there is no other way to get on the blockchain besides submitting to the dominant builder, searchers have to succumb to that kind of extractive behaviour. In the long-run, searchers benefit from a competitive and decentralised block building market.

In the short-run, however, searchers will withhold information because searchers that contribute always end up at a worse spot. This kind of reverse prisoners dilemma situation punishes those who contribute and the rational behaviour is stay silent.

---

**Keccak255** (2023-07-13):

Great analysis. I completely agree with your thoughts.

I think there is value in considering an incentive design to help searchers properly value builders as a solution to a short term problem.

In fact, I have in mind this dashboard and the above proposal (incentive design for not hiding information) and a hybrid solution combining the two should make the searcher’s behavior of not hiding information an economically rational behavior.

I intend to propose it soon, but it is not yet perfect and has many shortcomings, so I would appreciate feedback when the time is right.

---

**askyv** (2023-07-15):

I really like this idea.

As you know, the hardest part of this idea is how to get the builder’s reputation. It seems to me two types of directions.

One is aggregating the searcher’s subjection. Previous research about [SchellingCoin](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed) will help in thinking about how to make evaluators act with integrity.

Another is collecting objective evidence. There are some outputs that show builders behave evilly, e.g., the block, which includes a  bundle rewritten by the builder. If the searcher can prove that they have created the bundle and sent it to the builder, it will be evidence of the builder’s dishonesty.

---

**nonechuckX** (2023-08-04):

Thanks for the great article! Just to confirm-

mev-boost has two main claims-

1. that they eliminate mev opportunities like front-running etc. by giving node operators (proposer of a particular slot) a full block instead of them having to go through issues of MEV attacks when building blocks locally.
2. they offer rewards to the tune of 2x-5x more per block than vanilla block building

This claim has gotten mev-boost adoption to a point that 96% blocks today are being built using this. And now therefore searchers can’t attack mempools directly by sending txs from their nodes, and have to collaborate with block builders and relays. So block builders use the MEV insights submitted by searchers to propose blocks which will cause profitability, and disburse rewards to the searcher, proposer and keep the rest for themselves (split between them is unclear)

So the thing to clarify- instead of becoming MEV-free, the routes of MEV being actualized has changed  with a positive sounding narrative to it. Does this sound correct?

