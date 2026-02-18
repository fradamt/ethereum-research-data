---
source: ethresearch
topic_id: 22239
title: Incentives of builder multiplexing in PBS
author: awmacp
date: "2025-04-30"
category: Economics
tags: [mev, proposer-builder-separation]
url: https://ethresear.ch/t/incentives-of-builder-multiplexing-in-pbs/22239
views: 223
likes: 0
posts_count: 1
---

# Incentives of builder multiplexing in PBS

# Incentives of builder multiplexing in PBS

*Andrew W. Macpherson, [Shtuka Research](https://shtuka.io).*

*Supported by PBS Foundation through Research Grant R9.*

This post is an abridged version of an extended report of roughly the same title. The full report, which contains the details of our model and scenario analysis, is published [here](https://github.com/shtukaresearch/pbs-research/releases/tag/builder-muxing-v1). The author is grateful to the PBS Foundation for supporting this work.

## Background

Concentration and exclusive “backroom deals” in Ethereum’s PBS builder markets has long been a concern of the Ethereum blockspace community (Gupta, 2023). Concentration is regarded as an unwanted pathway to monopoly, centralisation, and all of the inefficiencies that entails. Unfortunately, it appears to be an inevitable consequence of the present structure of the blockspace supply chain that builders can only achieve edge by privately negotiated exclusive arrangements. Worse than being simply opaque, exclusive arrangements are extremely hard to come by for new entrants and hence present an apparently insurmountable barrier to entry, severely limiting the competitiveness of builder markets (Yang, 2024). Moreover, the exclusivity of these links fragments the market, reducing reliability.

In this work, we attempt to illuminate these issues by introducing an incentive model of builders and what we call *multiplexers* or *muxers*, that is, entities who forward transaction items to one or more builders together with a request for partial rebate. The incentive model quantifies the tradeoff between the reliability of multiplexing to many builders and the possibility of obtaining a larger rebate from the edge that a single builder gains through an exclusive arrangement. This builds on a body of previous empirical work (Öz, 2024) by quantifying at the model level:

- why order flow sources (OFS) might enter into risky exclusive arrangements, and
- the conditions that make an OFS “pivotal” to a builder in the sense that its presence or absence decides the outcome of the PBS auction.

Finally, we wish to emphasise that our model assumes complete trust in the execution of the PBS auction. The frictions we identify would therefore persist even if the well-known issue of trust in the relay were resolved.

### Key findings

Our model predicts that PBS markets are dominated by builders with persistent edge, regardless of auction structure, and that the key sources of edge are OFS with high-value bundles and relatively high risk tolerance who may choose an exclusive forwarding strategy for its higher expected returns. We find conditions under which exclusive flow can materialise “permissionlessly,” that is, even in the absence of a formal partnership between OFS and builder.

Significantly, the model shows that this state of affairs — already well known to be the case in the PBS market today — is not due to the idiosyncracies of the present incumbents, the PBS auction rules, or the method by which trust in the execution of those rules is achieved. Rather, it is an inevitable consequence of the single item auction structure of PBS and the existence of major OFS with certain risk preferences.

In more detail:

1. We describe the source of contention between transaction items as a set of “safety rules” governing block construction. As well as consensus rules, safety rules can be inherited from commitments further up the OF supply chain such as execution guarantees and bundle compatibility.
By definition, contentious transactions are those for which inclusion into the optimal block depends on the other transactions in a builder’s mempool. It is therefore difficult to get strong upstream assurances about whether such items will be included without knowledge of future states of this mempool.
2. Builder-side muxing with nonzero rebate is a way for a builder to maintain edge at the same time as derisking tx landing rate by sharing flow.  Based on the market layout today, it appears that this edge is currently much smaller than those associated to exclusive flow.
3. Market dominance in the current structure requires only consistent edge. The size of the edge doesn’t affect the amount of dominance. To allow builders with weaker edge to acquire non-trivial market share, a new market structure — probably one with multiple sellers and multiple items — is necessary. Simply changing the auction format, as suggested by (Öz, 2024), isn’t good enough.
4. We identify two major theoretical sources of edge: originating contentious items (searcher-builder), and a preferential relationship on pivotal flows. In the pivotal flows case, an exclusive forwarding strategy sometimes dominates even without a formal partnership or contention. Even under conditions of complete trust in the PBS relay, these sources of edge are only available to builders with specific structural advantages or under specific builder market conditions.
5. Once a builder has achieved market dominance, he can substantially increase his profit margins by making decisions on additional contentious items, including those where the contention is idiosyncratic to that builder (for example because of jurisdictional issues). This single point of control over allocation is an efficiency and censorship threat.

### Recommendations for future research

We call on the Ethereum research and business communities to intensify research into the following areas:

1. Quantitative analysis of sources of builder edge. If the largest sources of edge were smaller, minor sources of edge like priority sharing could become viable routes to entry, improving market access. To understand how these sources can be broken up and shared, we need a deeper, quantitative understanding of why exclusive arrangements of the two types identified are attractive for the OF sources. This objective could be pursued with more detailed scenario analysis, gathering case studies, and statistical analysis of labelled data to fit the model parameters.
2. Costs and returns of reliability guarantees. As far as we know there are currently no muxer services that offer a concrete guarantee on transaction landing rate (though Flashbots Protect does at least report theirs). For classes of items where contention is limited, more effort should be made into modelling landing rate with a goal of underwriting such a guarantee. Part of the work involved would be to explicitly identify the relevant low-contention classes. Statistical research into the demand for improved reliability would illuminate the value of such constructions to the Ethereum business community.
3. Novel market structures for full blocks. The single change that we think would have the widest impact on the current bottlenecks of the PBS market would be to move from a single seller to multiple seller market for blocks, breaking the proposer monopoly on the single slot timescale. Some movement in this direction is already under way, with partial block construction being factored out to other markets (via preconf protocols) or in-protocol committees (via FOCIL).
Making this change for the full block, particularly the part of the block containing the highest value contentious items, would need either widespread community support for a consensus upgrade or a large fraction of validators signing up for an external commitment market. We therefore expect this line of research to play out over a longer time scale than the previous two directions.

## Model description and discussion

For details, see the [full report](https://github.com/shtukaresearch/pbs-research/releases/tag/builder-muxing-v1).

## Selected references

- Gupta, T., Pai, M. M., & Resnick, M. (2023). The Centralizing Effects of Private Order Flow on Proposer-Builder Separation. In J. Bonneau & S. M. Weinberg (Eds.), 5th Conference on Advances in Financial Technologies (AFT 2023) (Vol. 282, p. 20:1-20:15). Schloss Dagstuhl – Leibniz-Zentrum für Informatik. The Centralizing Effects of Private Order Flow on Proposer-Builder Separation
- Öz, B., Sui, D., Thiery, T., & Matthes, F. (2024). Who Wins Ethereum Block Building Auctions and Why? In R. Böhme & L. Kiffer (Eds.), 6th Conference on Advances in Financial Technologies (AFT 2024) (Vol. 316, p. 22:1-22:25). Schloss Dagstuhl – Leibniz-Zentrum für Informatik. https://doi.org/10.4230/LIPIcs.AFT.2024.22
- Titan. (2023, June 13). Builder Dominance and Searcher Dependence. Builder Dominance and Searcher Dependence. Builder Dominance and Searcher Dependence
- Yang, S., Nayak, K., & Zhang, F. (2024). Decentralization of Ethereum’s Builder Market (No. arXiv:2405.01329). arXiv. [2405.01329] Decentralization of Ethereum's Builder Market
