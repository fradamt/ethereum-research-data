---
source: ethresearch
topic_id: 6586
title: Discussing the various adaption of game theory
author: ethorld
date: "2019-12-05"
category: Economics
tags: []
url: https://ethresear.ch/t/discussing-the-various-adaption-of-game-theory/6586
views: 1528
likes: 0
posts_count: 1
---

# Discussing the various adaption of game theory

Almost problems of incentivation in Ethereum are based on economics, especially game theory. So I would like to discuss ways to apply game theory deeper to the Ethereum economic system. Game theory can be used for various reward and punishment policy design, mechanism design, and detail economic parameter determination.

To suggest an example topic, in Eth 1, transaction fee is first-price auction. As mentioned in [this document](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838), a second price auction may be alternative that allows for a simple, optimal, buyer side truthfull strategy. But due to the exclusively properties of auction, it is not incentive compativility on the proposer’s side due to the Civil Attack. This is possible because the cost of creating a dummy transaction for fee manipulation is small. However, if the bidder is the one with the minimum deposit, such as the verifier (in eth2), then the above-mentioned attack would be much more expensive and difficult to carry out. So are there situations where auctions can be used for verifier’s true strategy, not for transaction fee issues? If there is no civil attack, we can think a situation where protocol can apply a solution that has proven to be an Incentive Compatible, such as the VCG mechanism, between verifiers and protocol

Another example is a cooperative game. Cooperative games are a matter of the allocation of benefits/costs in the context of cooperation (e.g. Family of shapley value, such as an approximation of Shapley Value without computational complexity). The nodes of the blockchain are all individual, and because of collusion problems, it is assumed that cooperation has a negative effect on the protocol. (so non-cooperative game). In practice, however, there are factors that can lead to cooperation, such as pool and collusion and they are inevitable, harmful to protocol. So, on the contrary, are there situations where cooperation can directly or indirectly benefit the protocol? If the protocol can detect the degree of cooperation and control it, will it be able to intentionally insentive more node involvement and at the same time prevent the cartel from growing too large ?

More specific situation is not enough, but I would also like to discuss an approach to find a problems that can be solved through proven solutions.
