---
source: ethresearch
topic_id: 20272
title: On Attestations, Block Propagation, and Timing Games
author: Nero_eth
date: "2024-08-14"
category: Proof-of-Stake
tags: [mev]
url: https://ethresear.ch/t/on-attestations-block-propagation-and-timing-games/20272
views: 2209
likes: 22
posts_count: 6
---

# On Attestations, Block Propagation, and Timing Games

# On Attestations, Block Propagation, and Timing Games

By now, [proposer timing games](https://timing.pics/) are no longer a new phenomenon and have been analyzed, [here](https://eprint.iacr.org/2023/760), [here](https://arxiv.org/abs/2305.09032) and [here](https://ethresear.ch/t/deep-diving-attestations-a-quantitative-analysis/20020).

In the following research piece, I want to show the **evolution of [proposer timing games](https://timing.pics/)** and analyze their impact on attesters. Through a case study of the node operators of Lido, Coinbase, and Kiln, we dive deep into block proposal timing and its impact on Ethereum’s consensus.

[![kilnmeme](https://ethresear.ch/uploads/default/original/3X/1/5/152baa9c8da23d4524a4e75101c4a1c0967ebf83.png)kilnmeme456×413 198 KB](https://ethresear.ch/uploads/default/152baa9c8da23d4524a4e75101c4a1c0967ebf83)

As of August 2024, the **block building market is largely outsourced**, with [~90%](https://mevboost.pics/) handled by [mevboost](https://github.com/flashbots/mev-boost) block builders. In practice, two builders, [Titan Builder](https://www.titanbuilder.xyz/) and [Beaverbuild](https://beaverbuild.org/), produce approximately [80%](https://mevboost.pics/) of all blocks that make it on-chain.

**Kiln is among the entities pushing timing games the furthest**, delaying block proposals to the **3-3.5 second** mark within the slot.

> In today’s environment with mevboost, block propagation is primarily handled by relays. Although proposers still propagate the block after receiving it from the relay, relays typically have better network connectivity and can therefore do it faster. However, the timing remains under the control of proposers, who can delay their getHeader calls to engage in timing games.

This chart shows the **evolution of timing games**. We can see that blocks from Kiln validators appear later and later over time.

![proposer_timing_games](https://ethresear.ch/uploads/default/original/3X/8/2/82cad8533f90505055f8eced73ae89d774a96111.gif)

**This comes with an impact on the network: for blocks proposed by Kiln proposers, the missed/wrong head vote rate is significantly higher:**

[![missed_head_votes_over_proposers](https://ethresear.ch/uploads/default/optimized/3X/8/d/8d3a31d4dd9d8856d2baaf1b7ad1528312b72923_2_690x316.png)missed_head_votes_over_proposers1200×550 26.1 KB](https://ethresear.ch/uploads/default/8d3a31d4dd9d8856d2baaf1b7ad1528312b72923)

[Previous analysis](https://ethresear.ch/t/deep-diving-attestations-a-quantitative-analysis/20020) showed that **the longer one waits, the higher the expected number of missed head votes** (*“80% of attestations seen by the second 5 in the slot”*). Kiln proposes blocks very late, causing some attesters to miss them and instead vote for the parent block. **Given that there are approximately 32,000 validators assigned to each slot, this results in about 10% of them voting for the wrong block.**

Let’s examine the attesting behavior of three large node operators and compare how they respond to **blocks proposed at different times within a slot.** The chart below illustrates the distribution of correct and timely head votes across the seconds within a slot.

![attestations_seen_late](https://ethresear.ch/uploads/default/original/3X/5/e/5eb241fefdf5cecb08a41d95fbf6d0263dbb573d.gif)

For early blocks, we observe that both **Lido and Coinbase display a characteristic “U”-shape** in their voting patterns that might be caused by different geo locations or client software. In contrast, **Kiln shows a single prominent peak** that slightly lags behind the first peaks of Coinbase and Lido. **However, for late blocks, Kiln attesters also show the “U”-shape pattern.**

**When blocks are first seen at the 4-second mark in the p2p network during a slot, most Lido attesters attest up to 2 seconds earlier than most of the Kiln or Coinbase attesters.** This pattern doesn’t necessarily suggest that Kiln is executing “individual strategies.” Instead, it could be attributed to running different clients or using different geographical locations.

### But who affects whom?

In the following chart, we compare a node operator’s performance over different proposers. A bar above y=1, for example, the green bar at Lido, indicates that Lido attesters miss more head votes for blocks from Kiln proposers. At the same time, Lido attesters do better for Lido blocks. The dashed line at 1 indicates the average share in missed head votes over all entities as proposers. A bar below 1 means the specific entity misses fewer head votes in conjunction with the respective proposer compared to the average.

[![missed_head_votes_over_proposers_percentage](https://ethresear.ch/uploads/default/optimized/3X/7/8/786e634d534692c6bcef1859d4baf99b6490a363_2_690x316.png)missed_head_votes_over_proposers_percentage1200×550 28.1 KB](https://ethresear.ch/uploads/default/786e634d534692c6bcef1859d4baf99b6490a363)

> Importantly, it is expected that each node operator does best with its local blocks. This is expected even without a coordination oracle, simply by co-locating nodes.

To quickly summarize what we see:

- Most node operators are rather stable across different proposers.
- Figment performs significantly worse for Kiln proposers. The same applies to Lido, Kraken, and EtherFi attesters.
- Kiln and Binance are the only entities performing better for Kiln blocks (which are, as a reminder, very late).

**Kiln attesters generally do well.** [Earlier analysis](https://ethresear.ch/t/deep-diving-attestations-a-quantitative-analysis/20020) showes that Kiln does a more than good job when it comes to running high-performing validators. Refer to [this analysis](https://ethresear.ch/t/deep-diving-attestations-a-quantitative-analysis/20020) for further details of Kiln’s attestation performance.

**Kiln causes stress.** Now, we know that Kiln blocks cause stress to other attesters but not necessarily to Kiln’s attesters.

**Explaining how.** The “*how*?” is difficult to respond to at this point. A possible explanation might be that Kiln’s validators are heavily co-located, with many validators running on the same machine, or have very dense peering. Another reason might be coordinated behavior across multiple nodes, either through custom peering/private mesh networks or through another additional communication layer connecting their validators. The latter is regarded as more centralizing as it leverages economies of scale even more.

A similar pattern can be observed when examining the (correct & timely) attestation timing of Lido and Coinbase for the blocks proposed by each respective entity (26.07.2024-03.08.2024).

![attestations_seen_late_by_proposer_misses](https://ethresear.ch/uploads/default/original/3X/5/a/5acb3eda53b7f342972637ae3d881d9e7cb44983.gif)

Interestingly, Kiln develops a “U”-shape distribution ranging from 3.8 \Rightarrow
 6.1 for their own late blocks, Lido a peak at 4.2s, and Coinbase a plateau starting at second 4 with a small peak at second 6 in the slot.

## “Prevent reorgs of my own proposed blocks”

Let’s shift our focus to reorged blocks. One strategy from the perspective of a node operator might be to **never** vote for reorging out one’s own block. Simply speaking, “*never vote for the parent block as the head if the proposer is me*”.

Instead of calling it *an entity’s own block*, I will use *local block* in the following.

The following chart shows the percentage of attesters voting for the reorged block vs voting for the parent block. The red part displays the % of all attesters from that entity that voted for a reorged block built by that entity.

[![votes_for_local_reorged_block](https://ethresear.ch/uploads/default/optimized/3X/f/5/f580dddb61ad6a3e4f577516f312475182d980d7_2_690x316.png)votes_for_local_reorged_block1200×550 31.2 KB](https://ethresear.ch/uploads/default/f580dddb61ad6a3e4f577516f312475182d980d7)

Kiln shows outlier behavior. While most node operators’ attesters correctly vote for the parent block rather than the local block, Kiln’s attesters appear to disregard this norm. **Over 10% of Kiln attesters attempt to keep the local block on-chain by voting for it.** If such strategies are adopted, they might justify the losses from incorrect head votes if they prevent the local block from being reorged. However, these tactics are generally frowned upon within the Ethereum community: “*don’t play with consensus*”.

> The chart uses 365 days of data. Thus, if some sophisticated strategy was implemented during the last year, the red portion would be proportionately smaller.

## But how do we feel about any additional level of coordination?

Regarding coordinated attesting, we, as community, seem to accept that validators run on the same node vote for the same checkpoints.

We probably don’t want any additional efforts that cross the boundaries of physical machines to improve coordination across validators. It’s something that everyone can build that goes beyond [what the specs describe](https://github.com/ethereum/consensus-specs/blob/b2f2102dad0cd8b28a657244e645e0df1c0d246a/specs/phase0/validator.md#attesting). Such coordination could have different forms:

- Level 1 - Fall-backs & Static Peering: Have a central fall-back/back-up node for multiple physical machines. This can also be a circuit breaker, some particularly fault-tolerant machine acting as a private relayer for information. Setups with improved peering, private mesh networks, or similar might also fall into this category.
- Level 2 - If-else rules: Have hard-coded rules waiting longer in certain slots. Those would be installed on multiple physical machines, allowing them to “coordinate” based on predefined rules.
- Level 3 - Botnet: Have a centralized oracle that communicates with all validators and delivers the checkpoints to vote for and the timestamp when they should be published.

In my opinion, crossing the line into the latter form of coordination (*level 2 and 3*) is problematic, and node operators should be held accountable. Finally, there may be a **gray area** for strategies involving **static peering** and **private mesh networks**.

**Such setups could be used to run (malicious) strategies such as:**

- ensuring to never vote for different checkpoints across multiple physical machines.
- ensuring to never vote for reorging out a block from one’s own proposer.
- coordinating based on the consecutive proposer (honest reorg client (y/n)).
- censoring attestations of a certain party.
- not voting for the blocks of a certain party.
- etc.

**When discussing *coordination*, it’s important to distinguish between two types:**

1. Coordinated behavior that occurs when validators are run from the same physical machine.
2. Coordinated behavior that arises from running the same modified client software or relying on the same centralized oracle.

A potential solution to counter sophisticated coordinated validator behavior is [EIP-7716: Anti-Correlation Penalties"](https://ethereum-magicians.org/t/eip-7716-anti-correlation-attestation-penalties/20137), which proposes to scale penalties with the correlation among validators.

***Find the code for this analysis [here](https://github.com/nerolation/timing-games-and-economies-of-scale).***

# More on that topics

| Title | Author |
| --- | --- |
| Timing.pics | DotPics Website |
| Timing Games: Implications and Possible Mitigations | Caspar & Mike |
| Deep Diving Attestations - A quantitative analysis | Toni |
| Time, slots, and the ordering of events in Ethereum Proof-of-Stake | Georgios & Mike |
| Time is Money: Strategic Timing Games in Proof-of-Stake Protocols | Caspar et al. |
| Time to Bribe: Measuring Block Construction Market | Toni et al. |
| The cost of artificial latency in the PBS context | Chorus One |
| Empirical analysis of the impact of block delays on the consensus layer | Kiln |
| P2P Presentation on Timing Games (Youtube) | P2P_org |
| Time is Money (Youtube) | Caspar |

## Replies

**tripoli** (2024-08-14):

vcool post. tyty.

Have you modelled how strong the effect of the wrong head votes would be if we implemented correlation penalties, i.e., might there be a world in which these correlation penalties backfire due to timing games and proposer-proposer colocation becomes encouraged instead of discouraged? Especially considering the relative frequencies of intentionally delayed blocks vs. the events that EIP-7716 targets.

And might it make sense to modify EIP-7716 to also punish the block proposer to stamp out aggressive timing games that affect consensus?

---

**Nero_eth** (2024-08-14):

I haven’t analyzed the impact of correlation penalties this time, but previous analyses indicate that solo stakers wouldn’t be affected, whereas large operators would be. I don’t expect this to change significantly.

Since most blocks are broadcasted by MEV-boost relays, this would likely lead to a situation where proposers and relays co-locate. This is already economically rational today.

A good question you raised is whether this co-location could negatively impact the goals of EIP-7716. Initially, I’d say it might. However, it would also mean that co-located operators are potentially distant from solo stakers and could face correlation penalties if they fail to attest to a solo staker’s block that doesn’t get reorged. Thus, it’d be better to also be exposed to locations a little more far away from the big relays to not vote for the parent too early and frontrun the block of the current slot with your attestation.

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> And might it make sense to modify EIP-7716 to also punish the block proposer to stamp out aggressive timing games that affect consensus?

This is an interesting thought and I’ve heard about ideas how this can be achieved. However, so far I’m not fully convinced what the best way to achieve that could be. I’ve been playing with the thought of making proposer boost decrease with the time in slot, just to make timing games even more risky.

---

**tripoli** (2024-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> previous analyses indicate that solo stakers wouldn’t be affected, whereas large operators would be. I don’t expect this to change significantly.

Right, but this was backwards looking analysis that doesn’t account for how proposers might change their behavior to try to game the system. The change will almost definitely be a boon to solo stakers, but I’m curious as to the impact on mid-sized proposer clusters and understanding the impacts from different sources of correlation penalties would be helpful to steelman the proposal.

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> Since most blocks are broadcasted by MEV-boost relays, this would likely lead to a situation where proposers and relays co-locate. This is already economically rational today.

Right, but there is still variance from relay to relay. Today it doesn’t matter which relay a proposer chooses to colocate with, but in the limit where correlation penalties are very strong might this encourage sophisticated proposer sets to all colocate at the same relay?

![](https://ethresear.ch/user_avatar/ethresear.ch/nero_eth/48/18443_2.png) Nero_eth:

> co-located operators are potentially distant from solo stakers and could face correlation penalties if they fail to attest to a solo staker’s block that doesn’t get reorged.

In theory blocks proposed by solo stakers should have more time to gather the attestations though. There’s probably an EV calculation that flips at some ratio of solo stakers vs. colocated proposers who play timing games.

---

**potuz** (2024-08-14):

Two things to get out of this:

- (block, slot) voting is good, even if not for the original reasons.
- We need to shorten the aggregation time.

I’m conceding on this point to [@arnetheduck](/u/arnetheduck), while I still think that it’s a burden on small nodes, I think these games are even worse.

---

**Nero_eth** (2024-08-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Right, but this was backwards looking analysis that doesn’t account for how proposers might change their behavior to try to game the system.

How do you think sophisticated node operators could gaim the system?

The only thing I can think about is “tricking” the system by not investing in anti-correlation but in fault-tolerance. This argument doesn’t really count as no existing fault tolerance will be able to reduce the missed attestation rate to zero, thus the small occurencies hurt even more.

The other outcome is investing in anti-correlation, thus, do exactly what the EIP suggests.

No matter what a big node operator does, it costs money, shrinks the APY and eventually benefits small parties.

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> Right, but there is still variance from relay to relay. Today it doesn’t matter which relay a proposer chooses to colocate with, but in the limit where correlation penalties are very strong might this encourage sophisticated proposer sets to all colocate at the same relay?

Good point. I’m not sure about this, though. The major relays today are already using the same network channels to propagate blocks as fast as possible.

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> In theory blocks proposed by solo stakers should have more time to gather the attestations though.

If we assume solo stakers are slower then their blocks should arrive later, thus not in time for more attesters than compared to a fast proposer. If solo stakers use mevboost without playing timing games, then they’ll be (more) competitive. If we assume the blocks of solo stakers to arrive earlier (because no latency+timing games), then you’re right and solo stakers do better.

