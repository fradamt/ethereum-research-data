---
source: ethresearch
topic_id: 2129
title: Registrations, shard count and shuffling
author: JustinDrake
date: "2018-06-03"
category: Sharding
tags: []
url: https://ethresear.ch/t/registrations-shard-count-and-shuffling/2129
views: 5992
likes: 6
posts_count: 7
---

# Registrations, shard count and shuffling

**TLDR**: We detail a simple validator registration scheme with dynamic shard count, fixed-size committees and fluid shuffling. In the discussion we highlight key properties and justify some of the design decisions.

**Construction**

- Validators: The Ethereum 2.0 protocol layer has a single type of collateralised participant called validators simultaneously participating in proof-of-stake and sharding. Collateral is fixed-size (32 ETH) and done via a one-way burn contract on the legacy chain (the current Ethereum 1.0 chain).
- Registration states: Validators can be in one of three registration states: pending_registration, registered and pending_deregistration. A validator is said to be active is it either registered or pending_deregistration. Pending registrations and deregistrations are queued in a FIFO.
- Initialisation: At initialisation there are no validators and no shards. New validators enter the registration queue with state pending_registration.
- First shard: When num_pending_registration == 2^10 for the first time one shard is instantiated and those first 2^10 validators become registered.
- Deregistration: A registered validator can request deregistration which triggers a deregistration countdown of 2^21 periods (~4 months assuming 5-second periods). If num_pending_registration > 0 when the deregistration countdown ends, the validator is immediately deregistered and replaced by the top validator in the registration queue. Otherwise num_pending_registration == 0 and the validator enters the deregistration queue. Similarly, a non-empty deregistration queue gets immediately popped when a registration request is made.
- Shard doubling: Whenever num_pending_registration == num_registered the number of shards is doubled. For every new shard 2^10 pending_registration validators become registered. Notice the two invariants that shard count is a power of two, and that there are 2^10 active validators per shard. We limit the maximum number of shards to 2^9.
- Proposers and notaries: At every period each shard is assigned two sets of exactly 2^10 validators: a set of proposers and a committee of notaries.
- Shuffling: Proposers and notaries are shuffled (via pseudo-random permutations) across shards in a staggered fashion and at a constant rate. Proposers are assigned to shards for 2^19 periods (~30 days) and the oldest proposer from each shard are shuffled every 2^(19 - 10) periods. Notaries are assigned to a shard for 2^7 periods (~10 minutes) and the oldest 2^(10 - 7) notaries from each shard are shuffled every period.

**Discussion**

- Unity: Sharding and proof-of-stake validators are merged (credit to @vbuterin for pushing in this direction). See benefits here.
- Homogeneity: Every shard has the same number of active validators, i.e. the same number of proposers and notaries. The ratio of active validators to shards is a fixed power of two to simplify the design.
- Predictability and fairness: Every active validator is active on two shards (once as a proposer and once as a notary—possibly the same shard) with permutation-based shuffling (no Poisson distribution).
- Large committee: A large notary committee of size 2^10 allows for good safety and liveness. Targeting a 2^-40 probability of sampling a bad committee, 2^9-of-2^10 committees only require a 61% honesty assumption.
- Large set of proposers: Since proposers are infrequently shuffled (every ~30 days) a relatively large set of proposers increases resistance to adaptive attacks (e.g. bribing).
- Reasonable max stake: With 2^10 active validators per shard, the maximum of 2^9 shards corresponds to 2^24 ETH staked (~32 million ETH). With only 135 active validators per shard the maximum number of shards would balloon to 3,883 for the same amount of stake.
- Fluid shuffling: Shuffling is homogeneous and fluid. This avoids spikes in global resource usage (notably, bandwidth) to spread load over time. It is a more effective alternative to staggered periods.
- Upsize only: The shard count can only increase (at least until shard load balancing is implemented).
- Capital burn: While individual deposits are churned through with new validators joining, the global deposit pool can be considered permanently unavailable, i.e. burnt.
- Overwhelming upsize demand: We only increase the shard count if there is at least as much demand from new validators as there is existing supply. This allows for more churn liquidity for deregistrations.
- Infrequent upsizing: Shard doubling combined with the 2^9 maximum number of shards means that there can only ever be nine birthing events, limiting the total number of disruptions. The square-root shard count proposal (see here) achieves something similar in a less extreme way.
- Powers of two: Shard doubling makes the shard count a power of two which can help simplify crosslinks, and is consistent with the rest of the design.

## Replies

**vbuterin** (2018-06-03):

I feel like the main *substantial* difference between this proposal and [mine](https://ethresear.ch/t/a-proposal-for-structuring-committees-cross-links-etc/2118) is that your proposal has fluid shuffling (ie. one validator is reshuffled at a time) and mine reshuffles in discrete periods, so that’s the best thing to focus on.

First of all, reshuffling notaries fluidly makes it harder to cleanly implement my strategy for cross-link inclusion, which specifies that within each epoch (which is coincidentally a Casper FFG epoch) every validator can participate exactly once, and is assigned to exactly one shard during that epoch. With this approach, you could have weird situations where a cross-link for shard A is added at the start of an epoch, but then later on the cross-link for shard B cannot be added because the validators for shard A all went to shard B. A validator inducted near the end of an epoch would not be able to participate in a cross-link, because they would not have enough time to verify everything in that shard.

Second, the formulas for calculating shard assignment seem like they would be more complex. I suppose you could do it by storing the shard assignment in the state, permanently assigning each validator to a slice (0 <= k <= epoch\_length) and then storing a separate shuffle parameters for each slice and reshuffling slice k in every block k mod epoch\_length; that said, it’s still slightly more annoying.

I suppose one thing you *can* do to solve the first problem is to redesign the mechanism somewhat, for example so that in every epoch the system only accepts cross-link signatures made at a very specific height. But I’d need to think more about how to accomplish this.

Gradually reshuffling *proposers* is something I’m fully onboard with already.

---

**terence** (2018-06-03):

Great write up! Love the design of having two pending registrations and de-registrations queue, and proposers are infrequently shuffled so It makes them aware of the state, to make more reveune with tx fee, and easier syncing

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Proposers are assigned to shards for 2^19 periods (~30 days) and the oldest proposer from each shard are shuffled every 2^(19 - 10) periods. Notaries are assigned to a shard for 2^7 periods (~10 minutes) and the oldest 2^(10 - 7) notaries from each shard are shuffled every period.

Just curious, what’s the math behind 2^(19 - **10**) periods for oldest proposer and oldest 2^(**10** - 7) notaries from each shard are shuffled every period?

---

**jamesray1** (2018-06-04):

Hmmm, if we’re going to make the number of shards variable in the upwards direction, maybe we want to try and bring load balancing forward in the [roadmap](https://github.com/ethereum/wiki/wiki/Sharding-roadmap) to make the number of shards variable in the downwards direction. This could help to prevent validators deregistering and not enough new ones replacing them.

---

**JustinDrake** (2018-06-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Gradually reshuffling proposers is something I’m fully onboard with already.

Awesome; proposers are probably the most valuable target for gradual reshuffling.

If we have the slightly more complicated logic to calculate shard assignment for proposers we can reuse that same logic for notaries as well (quite probably without any extra storage, although now that the SMC will live on the beacon chain we don’t have to worry about the EVM and gas golfing).

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I suppose one thing you can do to solve the first problem is to redesign the mechanism somewhat, for example so that in every epoch the system only accepts cross-link signatures made at a very specific height.

That’s broadly the direction I’ve taken ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/aca169/48.png) terence:

> Just curious, what’s the math behind 2^(19 - 10 ) periods for oldest proposer and oldest 2^( 10 - 7) notaries from each shard are shuffled every period?

- Proposers: 1 proposer per 2^19/2^10 = 2^9 periods, i.e. 1 proposer per 2^9 periods
- Notaries: 1 notary per 2^7/2^10 = 2^-3 periods, i.e. 2^3 notaries per 1 period

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> if we’re going to make the number of shards variable in the upwards direction, maybe we want to try and bring load balancing forward in the roadmap 1 to make the number of shards variable in the downwards direction. This could help to prevent validators deregistering and not enough new ones replacing them.

Right! Note though that the insufficient validator problem exists even with a fixed number of shards. Vitalik and I are thinking about this right now.

The suggestion I made in the original post was “capital burn”, i.e. prevent deregistrations below a safe minimum. Since then we’ve looked at lowered security, shard pausing and shard slowdown. My gut feel is that load balancing is too hard to include in the initial phases of the roadmap.

---

**MPR** (2018-06-04):

The fact that there is no method to clear a large `pending_deregistration` list could pose a problem to potential stakers. The 4 month waiting period is already a powerful disincentive, adding an extra unknown waiting time into the mix would likely scare people off. If a potential staker was to see a large `pending_deregistration` pool for any reason they would be less likely to stake, under the assumption that it would be extremely hard to get their ETH out. This could lead to a vicious cycle where many people would like to deregister but few people would be willing to become a validator to take their place.

Instead of having a fixed number of validators per shard, how about a maximum number and a minimum number? Let’s say maximum number stays at 2^10 while the minimum becomes 2^9. While `num_pending_registration > 0` and the average validator number is less than 2^10 then the top candidate enters the validation pool. While `num_pending_deregistration > 0` and the average validator number is greater than 2^9 then the top candidate exits the validation pool. Otherwise, all other procedures stay the same

This should allow stakers to more easily enter and exit the validator pool, increasing willingness to participate and therefore reducing required issuance rates to validators.

---

**jamesray1** (2018-06-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Targeting a 2^-40 probability of sampling a bad committee, 2^9-of-2^10 committees only require a 61% honesty assumption.

Could you elaborate on this? Assuming the chosen period length of 5 s for the beacon chain, what average time to failure does that correspond to? How did you work out this assumption?

I think you mean by 2^9-of-2^10 committees that 2^9 out of 2^10 notaries per committee must sign off on a proposal for it to get through, not 2^9 referring to the number of shards. Source [here](https://gitter.im/ethereum/sharding?at=5af95f18bd10f34a68fe366c). AIUI, if we assumed a 50% honesty assumption, that would mean that if half of notaries went offline, all of the remaining half would have to sign off on a proposal to get through, which seems unlikely, so we either have to assume that this is unlikely to happen, or the proposal may be delayed until more honest validators come online (assuming that some of the remaining half are malicious).

