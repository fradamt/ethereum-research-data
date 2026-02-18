---
source: ethresearch
topic_id: 17888
title: Empirical analysis of the impact of block delays on the consensus layer
author: aimxhaisse
date: "2023-12-18"
category: Consensus
tags: [mev]
url: https://ethresear.ch/t/empirical-analysis-of-the-impact-of-block-delays-on-the-consensus-layer/17888
views: 1895
likes: 12
posts_count: 1
---

# Empirical analysis of the impact of block delays on the consensus layer

author: *[mxs@kiln.fi](mailto:mxs@kiln.fi)*

> Vladimir: That passed the time.
> Estragon: It would have passed in any case.
> Vladimir: Yes, but not so rapidly.
>
>
> — Waiting for Godot

# Overview

Timing games were described in the [Time is Money](https://arxiv.org/pdf/2305.09032.pdf) and [Time to Bribe](https://arxiv.org/pdf/2305.16468.pdf) papers. They both explore the behavior of honest-but-rational validators which can intentionally delay block proposal to increase their MEV rewards, noting that there is an expected impact on the network health.

**In this post we measure the impact of intentional delays vs non-intentional delays on the mainnet network.**

Two approaches are taken to gauge the timing of blocks:

1. at a validator level by intentionally delaying blocks with different timing values during periods of 8 hours (intentional delays),
2. at a network level by looking at the bid timestamp from relays of the proposed block (which we call here non-intentional delays). This is done with the assumption that the number of participants engaged in timing games is small at the time of the analysis.

To gauge the impact on the network, **we look at the consensus rewards from attestations generated on the next slot**: a late block has less chance of being correctly attested in time by participants voting on the following slot, resulting in less rewards. We compare the values of delayed blocks against the average of the network at the time during the 8 hours period.

# Impact of intentionally delayed blocks

In this section, we intentionally delay `getHeader` calls with different delay times ranging from 1500ms to 2100ms during periods of 8 hours on selected validators (which correspond to about ~80 block proposals for each delay time), picking the best bid seen each time. We then observe the sum of all attestation rewards generated on the next slot, and compare it with the network average of attestation rewards per block during the corresponding 8 hours period. These experiments were performed early December 2023 on mainnet.

## Delays as seen by the network versus configured delay

[![operator_bid_time_distribution](https://ethresear.ch/uploads/default/optimized/2X/9/9a0b810d59b3f2b4f6f2d0f2cb0bc5d1ac9e5b03_2_690x345.png)operator_bid_time_distribution2000×1000 30.1 KB](https://ethresear.ch/uploads/default/9a0b810d59b3f2b4f6f2d0f2cb0bc5d1ac9e5b03)

**Fig 1**: *distribution of bid time of selected blocks using intentionally delayed proposals.*

[![operator_delay_time_distribution](https://ethresear.ch/uploads/default/optimized/2X/e/e0b35bdfb998785c19844b18370fad50f76c38b3_2_690x345.png)operator_delay_time_distribution2000×1000 29.3 KB](https://ethresear.ch/uploads/default/e0b35bdfb998785c19844b18370fad50f76c38b3)

**Fig 2**: *distribution of delay time of selected blocks using intentionally delayed proposals.*

Even though we see a correlation between the two observations, there is no perfect match as there is no guarantee that waiting more will result in a better bid.

## Impact on the consensus rewards of the next slot

[![operator_impact_consensus_rewards_bid](https://ethresear.ch/uploads/default/optimized/2X/c/ca9528aee7121de09fdea0fe247c1f6e89223af2_2_690x345.png)operator_impact_consensus_rewards_bid2000×1000 54.3 KB](https://ethresear.ch/uploads/default/ca9528aee7121de09fdea0fe247c1f6e89223af2)

**Fig 3**: *impact on the next slot relative to the network average using the winning bid time*

There is higher variance in this graph outside the `{1500,2000}` ms range due to the small number of proposed blocks matching those effective bid times. Since we have the view from the validator’s perspective, we can use the same approach with the actual delay time to get a more accurate picture.

[![operator_impact_consensus_rewards_delay](https://ethresear.ch/uploads/default/optimized/2X/b/b3daeae9f71d50b73954332c4438f771ab434c76_2_690x345.png)operator_impact_consensus_rewards_delay2000×1000 41.9 KB](https://ethresear.ch/uploads/default/b3daeae9f71d50b73954332c4438f771ab434c76)

**Fig 4**: *impact on the next slot relative to the network average using the actual delay*

Here the variance is smaller, we see there is a small impact caused by intentionally delayed blocks which tends to increase as the delay increases, it is however close to the average of the network at the levels we measured.

# Impact of non-intentionally delayed blocks

In this section, we perform the same analysis using the winning bid time on the entire network, during the exact same period as the previous experiment, excluding blocks intentionally delayed by the experiment.

## Delays as seen by the network using bid times

[![network_dist_bid_time](https://ethresear.ch/uploads/default/optimized/2X/0/0b6770445e0e4f2fb6650a06d086cf8a9ebf150d_2_690x345.png)network_dist_bid_time2000×1000 30 KB](https://ethresear.ch/uploads/default/0b6770445e0e4f2fb6650a06d086cf8a9ebf150d)

**Fig 5**: *distribution of bid time of proposed blocks at a network level excluding the intentionally delayed blocks from the previous section.*

As seen before, this distribution is to be taken with a grain of salt. The bid time in practice may not correspond to the actual delay used by the validator: one could for instance try to hide its timing game by favoring early bids if the bid obtained after delays is not profitable enough. Using other approaches to measure the delay, such as the block arrival time seen on beacons on the network would uncover this. We assume there is no advanced participant at the network level tricking bid times at the time of the experiment.

[![network_next_impact_consensus_rewards](https://ethresear.ch/uploads/default/optimized/2X/4/44f20a8db963285f0a3feb04cb95a53d75dec115_2_690x345.png)network_next_impact_consensus_rewards2000×1000 68.7 KB](https://ethresear.ch/uploads/default/44f20a8db963285f0a3feb04cb95a53d75dec115)

**Fig 6**: *impact on the next slot relative to the network average using the winning bid time*

# Intentional versus non-intentional delays

[![comparison_next_impact_consensus_rewards](https://ethresear.ch/uploads/default/optimized/2X/e/ee8c681b597d66a76421bbd71909f4ce65e6ab60_2_690x345.png)comparison_next_impact_consensus_rewards2000×1000 80 KB](https://ethresear.ch/uploads/default/ee8c681b597d66a76421bbd71909f4ce65e6ab60)

**Fig 7**: *impact on the network between intentional/non-intentional delays*

One thing to note here is that the moment the network participants (non-intentionally delayed blocks) deviate too much from the median time in slot, we start observing a bigger impact on the next slot than with intentional delays. This is expected as non-intentional delays are usually the result of network hiccups, issues encountered by participants, which can impact other parts of the block proposal process such as propagation time. It is thus important to delay under performant conditions.

This means using the bid time/block arrival time and corresponding impact on the network can be a criteria to differentiate “honest” from “honest but rational” validators. An “honest but rational” validator is unlikely to take the risk of propagating badly late blocks, as it could lead to missing the block proposal.

# Conclusions

We observe little impact on the next block attestation rewards following even large intentional intentional delays compared to non-intentional ones (Fig 7): the time in the slot at which a validator picks a block is one part of many factors that contribute to network instability. When other factors are controlled such as propagation time it can be done with little impact on the consensus layer stability.

Mitigation involving `getHeader` or `getPayload` time constraints (options 2 & 3 from [Timing Games: Implications and Possible Mitigations](https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612)) will hurt some honest validators as seen above: they do delay blocks unintentionally and will miss block proposals if enforced. We can gauge how many participants would be hurt by looking at the distribution from Fig 5. From this perspective it is likely a better option to time restrict the bid arrivals at the relay level to T=0 to keep the system fair for everyone (option 1).

In the long run, delaying blocks is not something all participants will be able to do in the same way: there is an advantage for performant setups who can push to higher delays with little impact and risk to miss blocks. Taking this line of reasoning further, actors who need longer signature times (DVT for example) won’t be able to play timing games as efficiently as performant direct staking operators.
