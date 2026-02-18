---
source: ethresearch
topic_id: 19971
title: Leaderless and Leader-Based Preconfirmations
author: chrmatt
date: "2024-07-04"
category: Economics
tags: [preconfirmations]
url: https://ethresear.ch/t/leaderless-and-leader-based-preconfirmations/19971
views: 3643
likes: 5
posts_count: 3
---

# Leaderless and Leader-Based Preconfirmations

*Joint work with [@murat](/u/murat). Thanks to [@The-CTra1n](/u/the-ctra1n) and [@bemagri](/u/bemagri) for reviewing and providing valuable feedback.*

# Introduction

A preconfirmation (preconf) for the context of this article refers to a promise about a given set of transactions relative to a future block, e.g., execution of a transaction in the next block or placing transactions at the top of the block. Entities who want to obtain a preconf can bid a certain amount indicating how much they are willing to pay for a preconf.

One dimension in which preconfs can be distinguished is whether there exists a unique preconf provider for every L1 block (a preconf leader), or whether there can be multiple competing preconf providers for every L1 block, without a leader. We here discuss the two approaches, their respective advantages and disadvantages, and how they can be combined. A particularly promising approach for combining the two concepts to obtain the best of both worlds appears to be using “sourcing leaders”, which are operating in a leaderless setting and collect preconfs from competing preconf providers.

# Overview and Definitions

## Leader-Based Preconfs

The simplest form of preconfs are ones issued by an appointed leader. This leader must have the authority to issue preconfs and have some means to enforce them. It is not necessary to have a single leader overall, as long as there is a unique, predetermined, and publicly known leader at each point in time. A straightforward way to choose leaders is using the current L1 proposer, as, e.g., in [commit-boost](https://github.com/Commit-Boost/commit-boost-client). More sophisticated leader-election methods are discussed below, and can be employed by [mev-commit](https://docs.primev.xyz/concepts/what-is-mev-commit).

## Leaderless Preconfs

An alternative to leader-based preconfs is to have multiple preconf providers simultaneously. The most natural instantiation of this is to have the block builders act as preconf providers, leveraging the strengths of the existing mev-boost landscape. This mechanism is [used by mev-commit](https://docs.primev.xyz/concepts/what-is-mev-commit). In this case, a single preconf provider cannot provide an authoritative preconf; in case the block builders are preconf providers, a single builder can only promise to honor the preconf for the blocks this block builder builds.

A preconf from a single block builder thus constitutes a probabilistic preconf in the sense that the preconf is conditioned on the issuing block builder winning the corresponding block. This can already be useful, e.g., for arbitrage searchers. A proper preconf with a 100% guarantee is obtained if all block builders preconfirm. A subtlety of this is that the set of all possible block builders must be known, which is not the case in a permissionless setting. This is solved by mev-commit by letting [block builders register](https://docs.primev.xyz/get-started/providers/registering-a-provider) as providers and [proposers and relays opt-in](https://docs.primev.xyz/get-started/validators) to only deliver blocks from registered block builders. Analyzing the game-theoretic interplay between bidders and multiple preconf providers is an interesting open problem.

# Comparison

Both approaches have their advantages and disadvantages, which we discuss below.

## Advantages of Leader-Based Preconfs

The most obvious advantage of leader-based preconfs is that a single preconf already constitutes almost a 100% guarantee (almost because the slot may be missed or the chain reorged). This simplifies the protocol interaction and also possibly provides faster feedback. Note that reorg risks are the same for all types of preconfs, so we do not discuss them further here.

## Advantages of Leaderless Preconfs

Having multiple simultaneous preconf providers creates a competitive environment, allowing for efficient preconf price discovery and thereby optimizing validator yield. A single provider having a preconf monopoly, on the other hand, can dictate the prices arbitrarily.

Further advantages come from letting the block builders be the preconf providers. First, block builders have sufficient sophistication to properly price preconfs. Secondly, builders are building the blocks and thus are the only entities that can issue preconfs without interfering with block production and adding latency: If another party issues a preconf, it must be communicated to the block builders such that they can build compatible blocks, and failure to receive the preconf in time leads to the block builder building a block violating the preconf. This also means that there is some delay between issuing the preconf and the builders learning about it in a leader based approach, which is particularly problematic towards the end of a slot, where builders may learn too late about the preconf. This also creates an advantage for block builders with fast connections to the preconf leaders, potentially leading to further centralization. Furthermore, receiving a preconf from a separate entity interferes with the block building strategy of the builders and thus can potentially lead to substantially less valuable blocks. Finally, leaderless preconfs can be integrated more easily into the existing mev-boost infrastructure.

# Leader Election

As mentioned above, the simplest way to elect a preconf leader is to choose the current L1 proposer. This, however, requires additional sophistication from the proposer and likely leads to economic inefficiencies. It is therefore likely that proposers want to outsource preconfs similarly to how proposers outsource block building in PBS, even though this might raise concerns such as increased complexity due to additional actors, and potentially more centralization. A crucial difference from PBS is that preconf leaders need to be chosen in advance, i.e., before preconf bids are available. Thus, when the right to become a preconf leader is auctioned off, the potential leaders need to place their bids in the leader election without knowing the value they can derive from becoming a leader. This means their bids can only be based on expected values rather than actual amounts as in PBS, similarly to [execution tickets](https://ethresear.ch/t/execution-tickets/17944). A notable exemption to this are scenarios in which preconfs are not time critical such as preconfs for blob inclusion bids. In this case, the auction can be run after all preconf bids have been issued and thus the auction can be based on the actual value instead of the expected one (cf. [Ethereum Research - Blob Preconfirmations with Inclusion Lists to Mitigate Blob Contention and Censorship](https://ethresear.ch/t/blob-preconfirmations-with-inclusion-lists-to-mitigate-blob-contention-and-censorship/19150)).

One concern with an expected-value-based auction is that this value likely remains relatively stable over time and thus a possible scenario is that a single entity that is very good at pricing wins an overwhelming fraction of the auctions, leading to centralization and a preconf monopoly (cf. [The Flashbots Collective - When To Sell Your Blocks](https://collective.flashbots.net/t/when-to-sell-your-blocks/2814/1)). A possible mitigation to this problem is to instead of running an auction, sell lottery tickets and choose the leader randomly as the holder of the winning ticket. This is akin to a similar mechanism recently proposed by [Espresso Systems in a related context](https://hackmd.io/@EspressoSystems/market-design). Further research is required to determine an optimal pricing structure for such lotteries.

# Combining Leaderless and Leader-Based Preconfs

To obtain the best of both worlds, one can combine a leaderless with a leader-based approach. We discuss some options how to achieve this below.

## Simultaneous Leaders and Leaderless Providers

One option to combine leaderless and leader-based preconfs is to have a dedicated preconf leader, but let this leader operate simultaneously with multiple non-leader preconf providers. We assume below that the non-leader providers are block builders. In such a scheme, both the leader and the builders can issue preconfs at any point in time. When the leader issues a preconf, it must be communicated to the block builders, who then need to honor them when building their blocks. At this point, block builders cannot commit to the already committed bid anymore (since such commitment would not add any value). On the other hand, if a builder issues a preconf first, the leader can still commit to the same bid, turning the preconf from the builder into a 100% guaranteed preconf.

While this approach might appear conceptually simple, it comes with several challenges. One issue is that it is probably very hard, if not impossible, for the leader to issue execution preconfs that are compatible with execution preconfs of the block builders. This approach might therefore be limited to inclusion preconfs. Another issue is the timing of preconfs: For the mechanism to work, a total order among preconfs needs to be established, since a builder should only be rewarded for a preconf on a bid that also been committed to by the leader if the builder committed first. This total order can be established by a dedicated side-chain, such as the mev-commit chain. Nevertheless, there is room for leaders to play games with the competing builders by delaying their preconfs or trying to frontrun the builders. Yet another difficulty of this approach are the more complex incentives. Who should be paid how much in case multiple preconfs are issued? Developing a fair mechanism that leads to good preconf prices requires further research.

## Sourcing Leaders

An alternative is to have leaders that themselves have no authority to enforce preconfs. Instead, the leaders receive bids from end users and subsequently try to obtain preconfs from the preconf providers. We call such leaders “sourcing leaders”. Once the sourcing leader has obtained preconfs from all providers, they issue a preconf to the end user. A sourcing leader is not strictly speaking a leader as defined above, but can provide the same advantage of a leader, namely issuing preconfs that themselves provide a 100% guarantee to the end user.

The role of a sourcing leader can be taken on by sophisticated actors such as solvers. A sourcing leader can in this case also offer preconfs before all providers have issued one and charge a premium to take on the risk that the preconf is violated. It is furthermore possible to have multiple competing sourcing leaders that offer preconfs with different prices at different speeds, where users can choose the best one for their purposes.

[![Sourcing Leader](https://ethresear.ch/uploads/default/optimized/3X/1/d/1df247e0731521b812fdecf14287017b6e1a772b_2_690x219.png)Sourcing Leader1232×392 56 KB](https://ethresear.ch/uploads/default/1df247e0731521b812fdecf14287017b6e1a772b)

**Figure 1:** Illustration of the interaction between an end user, a sourcing leader running a bidder node, and three preconf providers.

# Conclusion and Open Problems

Both leader-based and leaderless preconfs offer unique advantages and challenges. Leader-based preconfs offer a 100% guarantee (ignoring missed slots and reorgs) with a single preconfirmation, whereas leaderless ones create a competitive environment, enabling efficient price discovery, and potentially leading to more valuable blocks. Different methods for leader election also have their own trade-offs, with options ranging from auctions to lotteries.

Combining leaderless and leader-based preconfs can provide the benefits of both systems. One approach is to have a dedicated preconf leader operating alongside non-leader providers. Another approach is to use sourcing leaders who have no enforcement authority themselves, but attempt to obtain preconfs from providers. Both approaches allow for a high degree of competition, but also pose additional challenges.

There are still several unresolved research problems uncovered in this article. One of them is to analyze the game-theoretic interplay between bidders and multiple preconf providers in a leaderless preconf system. For a leader-based approach, relevant open problems are determining an optimal pricing structure for preconf leader lotteries to mitigate the risk of centralization and a preconf monopoly, and how to integrate with the existing mev-boost infrastructure. For combining leaderless and leader-based preconfs, designing fair mechanisms for the interaction between both types of preconf providers is left for future research. Finally, an important open question is how the approach with a sourcing leader compares to the others in terms of obtaining fair prices.

## Replies

**wooju** (2024-07-09):

I agree that a sourcing leader can provide a 100% guarantee to the end user as mentioned. However, I’m not entirely clear on how this differs from Leader-Based Preconfs. Specifically, setting up a sourcing leader seems to challenge the benefit of a competitive environment, which allows for efficient preconf price discovery and thereby optimizing validator yield. Also, if multiple competing sourcing leaders are established, it’s not clear how this method differs from a Leaderless system.

Therefore, I’m unsure if a sourcing leader truly represents a way to combine Leader-Based and Leaderless systems. Are there any advantages of having a sourcing leader that I might be missing?

---

**chrmatt** (2024-07-09):

A sourcing leader obtains preconfs from competing preconf providers, so the existence of a sourcing leader should not hinder price discover for the providers themselves. The sourcing leader himself could of course offer bad prices to the end user by pocketing a large margin. In that scenario, the end users who are consistently overpaying can switch to another sourcing leader. In that sense, sourcing leaders compete on a different level: They are chosen by a user for a given period of time, and during that time can thus provide (almost) 100% guarantees, but users can choose another sourcing leader later if they are unhappy with the outcomes.

