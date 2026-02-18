---
source: ethresearch
topic_id: 15801
title: Increase the MAX_EFFECTIVE_BALANCE – a modest proposal
author: mikeneuder
date: "2023-06-06"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/increase-the-max-effective-balance-a-modest-proposal/15801
views: 24041
likes: 86
posts_count: 61
---

# Increase the MAX_EFFECTIVE_BALANCE – a modest proposal

# Increase the MAX_EFFECTIVE_BALANCE – a modest proposal

> NOTE: This proposal **does not** increase the minimum of 32 ETH to become a validator.

*by [mike neuder](https://twitter.com/mikeneuder), [francesco d’amato](https://twitter.com/fradamt), [aditya asgaonkar](https://twitter.com/adiasg), and [justin drake](https://twitter.com/drakefjustin) – june 6, 2023*

*~ accompanying artifacts ~*

*[a] the diff view of a minimal consensus spec [pull request](https://github.com/michaelneuder/consensus-specs/pull/3/files)*

*[b] security considerations + annotated spec [doc](https://notes.ethereum.org/@fradamt/meb-increase-security)*

*[c] the full consensus pyspec/spec tests [pull request](https://github.com/michaelneuder/consensus-specs/pull/4/files#diff-4acdddb708abdca02e1e5354345448359a631a949b28dbba14e52b47d8034d77)*

---

**Proposal** – *Increase the `MAX_EFFECTIVE_BALANCE` to encourage validator set contraction, which*

1. unblocks single-slot finality and enshrined PBS, and
2. reduces unnecessary strain on the p2p layer.

*Critically, we do not propose*

1. increasing the 32 ETH minimum required to become a validator, or
2. requiring any sort of validator consolidation (this process would be purely opt-in).

---

*tl;dr; [MAX_EFFECTIVE_BALANCE](https://github.com/ethereum/consensus-specs/blob/9c35b7384e78da643f51f9936c578da7d04db698/specs/phase0/beacon-chain.md#gwei-values) (abbr. `MaxEB`) caps the effective balance of Ethereum validators at 32 `ETH`. This cap results in a very large validator set; as of June 6, 2023, there are over [600,000 active validators](https://beaconcha.in/) with an additional 90,000 in the activation queue. While having many validators signals decentralization, the `MaxEB` artificially inflates the validator set size by forcing large staking operations to run thousands of validators. We argue that increasing the `MaxEB` (i) unblocks future consensus layer upgrades on the [roadmap](https://storage.googleapis.com/ethereum-hackmd/upload_1a45d0f8e3eff90c4832d9cb2700a441.jpg), (ii) improves the performance of the current consensus mechanism and p2p layer, and (iii) enhances operational efficiency for both small and large-scale validators.*

*Many thanks to [Caspar](https://twitter.com/casparschwa), [Chris](https://twitter.com/metachris), [Terence](https://twitter.com/terencechain), [Dan Marzec](https://twitter.com/_danielmarzec), [Anders](https://twitter.com/weboftrees), [Tim](https://twitter.com/timbeiko), [Danny](https://twitter.com/dannyryan), [Jim](https://twitter.com/jgm), and [Rajiv](https://twitter.com/rajivpoc) for comments on draft versions of this document.*

---

## Effective balances and MAX_EFFECTIVE_BALANCE

*Effective balance* is a field in the [validator struct](https://github.com/ethereum/consensus-specs/blob/9c35b7384e78da643f51f9936c578da7d04db698/specs/phase0/beacon-chain.md#validator) calculated using the amount of `ETH` staked by each validator. This value is used for a number of consensus layer operations, including

1. checking if a validator is eligible for the activation queue,
2. calculating the slashing penalties and whistleblower rewards,
3. evaluating the attestation weight used for the fork-choice rule and the justification & finalization of epochs,
4. determining if a validator is selected as a proposer,
5. deciding if a validator is part of the next sync committee, etc…

Effective balance is calculated in increments of 10^9 `gwei` (1 `ETH` – the [EFFECTIVE_BALANCE_INCREMENT](https://github.com/ethereum/consensus-specs/blob/9c35b7384e78da643f51f9936c578da7d04db698/specs/phase0/beacon-chain.md#gwei-values)) and is updated in [process_effective_balance_updates](https://www.attestant.io/posts/understanding-validator-effective-balance/). The update rule behaves like a modified floor function with hysteresis zones determining when a balance changes. See [“Understanding validator effective balance”](https://www.attestant.io/posts/understanding-validator-effective-balance/) for more details.

The `MAX_EFFECTIVE_BALANCE` is a [spec-defined](https://github.com/ethereum/consensus-specs/blob/9c35b7384e78da643f51f9936c578da7d04db698/specs/phase0/beacon-chain.md#gwei-values) constant of 32 \times 10^9 `gwei` (32 `ETH`), which sets a hard cap on the effective balance of any individual validator. Post-capella, validator balances are automatically withdrawn. As defined in the [spec](https://github.com/ethereum/consensus-specs/blob/9c35b7384e78da643f51f9936c578da7d04db698/specs/capella/validator.md#enabling-validator-withdrawals), exited validators have their full balance withdrawn and  active validators with a balance exceeding the `MaxEB` are partially withdrawn.

## Why we should increase it

There are many inefficiencies resulting from the `MaxEB` being low. We analyze the benefits of increasing it from the perspective of (i) future [roadmap](https://storage.googleapis.com/ethereum-hackmd/upload_1a45d0f8e3eff90c4832d9cb2700a441.jpg) upgrades, (ii) the current consensus and p2p layers, and (iii) the validators.

*Without a validator set contraction, single-slot finality is not feasible using the [current](https://ethresear.ch/t/a-simple-single-slot-finality-protocol/14920) [designs](https://ethresear.ch/t/horn-collecting-signatures-for-faster-finality/14219). Without single-slot finality, we believe that enshrined PBS is also not viable. Additionally, the current p2p layer is [heavily burdened](https://ethresear.ch/t/removing-unnecessary-stress-from-ethereums-p2p-network/15547) by the artificially large and rapidly growing validator set (see [this thread](https://twitter.com/potuz1/status/1657031082749861891) from Potuz outlining what happened during the May 12 non-finality event).  ~~ We see a validator set contraction as a must-have for a sustainable and upgradable Ethereum consensus layer. ~~*

### The roadmap perspective

As outlined in Vitalik’s [roadmap](https://twitter.com/VitalikButerin/status/1588669782471368704), there are still ambitious goals around improving the consensus layer. We present two upgrades that are infeasible given the size of the validator set, but are unblocked by increasing the `MaxEB`.

1. single-slot finality – SSF has long been researched and is a critical component of the end-game vision for Ethereum Proof-of-Stake. Horn is the state-of-the-art BLS signature aggregation proposal. From the post, a validator set with 1 million participants results in the worst-case signature aggregation taking 2.8s on a top-tier 2021 CPU and 6.1s on an older machine. While there may be more improvements in the aggregation scheme and the hardware, this performance is prohibitively slow in the near-term given a validator set of this size. By compressing the validator set, we can begin working towards single-slot finality immediately.
2. ePBS – Enshrined Proposer-Builder Separation has also been discussed for multiple years. Due to security concerns around ex-ante/ex-post reorgs and balancing attacks, proposer boost was implemented as a stop-gap measure to protect HLMD-GHOST (Hybrid Latest Message Driven-GHOST). If we were to implement ePBS today, the security benefits from proposer boost (or even the superior view-merge) are reduced. The high-level reasoning here is that the security properties of HLMD-GHOST rely heavily on honest proposers. With every other block being a “builder block”, the action space of a malicious proposer increases significantly (e.g., they may execute length-2k ex-post reorgs with the probability equal to the length-k ex-post reorgs under today’s mechanism). We plan on writing further on this topic in the coming weeks. With a smaller validator set, we can implement new mechanisms like SSF, which have stronger security properties. With a stronger consensus layer we can proceed to the implementation of ePBS (and even mev-burn) with much improved confidence around the security of the overall protocol.

### The current consensus layer perspective

The consensus nodes are under a large load to handle the scale of the current validator set. On May 11th & 12th, 2023, the beacon chain experienced two multi-epoch delays in finalization. Part of the suspected root cause is [high-resource utilization](https://twitter.com/potuz1/status/1657031082749861891) on the beacon nodes caused by the increase in the validator set and significant deposit inflows during each epcoh. We present two areas of today’s protocol that benefit from increasing the `MaxEB`.

1. p2p layer – To support Gasper, the full validator set is partitioned into 32 attesting committees (each attesting committee is split into 64 sub-committees used for attestation aggregation, but these sub-committees do not need to be majority honest for the security of the protocol and are mostly a historical artifact of the original sharding design which has been abandoned); each committee attests during one of the slots in an epoch. Each attestation requires a signature verification and must be aggregated. Many of these checks are redundant as they come from different validators running on the same machine and controlled by the same node operator. Any reduction of the validator set directly reduces the computational cost of processing the attestations over the duration of an epoch. See Aditya’s “Removing unnecessary stress from Ethereum’s P2P layer” for more context.
2. processing of auto-withdrawals – Since withdrawals of all balances over the MaxEB are done automatically, there is a large withdrawal load incurred every epoch. By increasing the MaxEB, validators can choose to leave their stake in the protocol to earn compounding rewards. Based on data from rated.network the average withdrawal queue length is about 6 days (this may quickly increase to ~10 days as more withdrawal credentials are updated and the validator set continues to grow). The vast majority of this queue is partial withdrawals from the active validator sweep (see get_expected_withdrawals).  A validator set contraction would directly reduce the withdrawal queue length.

### The validator perspective

We focus on two pros of increasing the `MaxEB`:

1. Democratization of compounding stake (benefits solo-stakers) – Currently, any stake above the MaxEB is not earning staking rewards. Staking pools can use withdrawals to compound their staking balance very quickly because they coalesce their rewards over many validators to create  32 ETH chunks needed to instantiate a new validator. With the current APR of ~6%, a single validator will earn roughly 0.016\% daily. At this rate, it will take a solo-staker over 11 years to earn a full 32 ETH for a fresh validator. Coinbase on the other hand, will earn 32 \cdot 0.00016 \cdot 60000 \approx 307 new ETH every day, which is enough to spin up 9 additional validators. By increasing the MaxEB, validator’s of any size can opt-in to compounding rewards.
2. Reducing the operational overhead of managing many validators (benefits large-scale stakers) – With the MaxEB being so low, staking pools are required to manage thousands of validators. From mevboost.pics, the top 3 validators by block-share are responsible for over 225,000 validators (though Lido is a conglomerate of 29 operators, each still represents a significant portion of the validator set).

```auto
1. Lido	       161,989 (28.46%)
2. Coinbase	   59,246 (10.41%)
3. Kraken  	   27,229 (4.78%)
```

- This means 225,000 unique key-pairs, managing the signatures for each validator’s attestations and proposals, and running multiple beacon nodes each with many validators. While we can assume large pools would still distribute their stake over many validators for redundancy and safety, increasing the MaxEB would allow them the flexibility consolidate their balances rather than being arbitrarily capped at 32 ETH.

*Note: Reducing staking pool operational overhead could also be seen as a negative externality of this proposal. However, we believe that the protocol and solo-staker improvements are more significant than the benefits to the large staking pools.*

## Why we shouldn’t increase it

While we think the benefits of increasing the `MaxEB` far outweigh the costs, we present two counter-arguments.

1. simplicity of the current implementation – By ensuring the effective validator balances are constrained to the range [16,32] ETH (16 ETH is the ejection balance; effective balance could drop slightly below 16 ETH because of the exit queue duration, but 16 ETH is the approximate lower bound), it is easy to reason about attestation weights, sync committee selection, and the random assignment of proposers. The protocol is already implemented, so the R&D costs incurred by changing the mechanism take away focus from other protocol efforts.

Response – The spec change we are proposing is quite minimal. We analyze these changes in “Security Considerations and Spec Changes for a MAX_EFFECTIVE_BALANCE Increase”. We believe that the current size and growth of the validator set are unsustainable, justifying this change.
2. considerations around committees – Preliminary note: In SSF, committees are no longer part of the fork-choice rule, and thus these concerns will be irrelevant. Given validators have differing stake, partitioning them into committees may result in some validators having much larger impact over the committee than others. Additionally, by reducing the validator set size, we decrease the safety margin of random sampling. For sync committees, this is not an issue because sampling the participants is done with replacement and proportional to effective balance. Once a sync committee is selected each validator receives one vote. For attesting committees, some validators will have much more voting power by having a larger effective balance. Additionally, with less validators, there is a higher probability that an attacker could own the majority of the weight of an attesting committee. However, with a sufficiently large sample, we argue that the safety margins are not being reduced enough to warrent concern. For example, if the validator set is reduced by 4x, we need 55% honest validators to acheive safety (honest majority) of a single slot with probability 1-10^{11}. With today’s validator set size, we need 53% honest validators to achieve the same safety margin; a 4x reduction in the validator set size only increases honest validator threshold by 2%.

Response – See committee analysis in “Security of Committees”. We believe this change adequetely addresses concerns around committees, and that even a validator set contraction is a safe and necessary step.

## Mechanisms already in place

Attesting validator weight, proposer selection probability, and weight-based sampling with replacement for sync committees are already proportional to the effective balance of a validator. These three key components work without modification with a higher `MaxEB`.

1. attesting validator weight – validators with higher effective balances are already weighted higher in the fork-choice rule. See get_attesting_balance. This will accurately weight higher-stake validators as having more influence over the canonical chain (as desired). We provide an analysis of the probability of a maliciously controlled attesting committee in “Security of Committees”.
2. proposer selection probability – We already weight the probability of becoming a proposer by the effective balance of that validator. See compute_proposer_index. Currently, if a validator’s effective balance (EB) is below the MaxEB, they are selected as the proposer given their validator index was randomly chosen only if,

EB  \cdot 255 \geq MaxEB \cdot r, \; \text{where} \; r \sim U(0, 255).

Thus if `EB = MaxEB`, given the validator index was selected, the validator becomes the proposer with probability 1. Otherwise the probability is

Pr(proposer | selected) = Pr\left(r \leq \frac{255 \cdot EB}{MaxEB}\right)

This works as intended even with a higher `MaxEB`, though it will slightly increase the time it takes to calculate the next proposer index (lower values of `EB` will result in lower probability of selection, thus more iterations of the loop).

1. sync committee selection – Sampling the validators to select the sync committee is already done with replacement (see get_next_sync_committee_indices). Additionally, each validator selected for the committee has a single vote. This logic works as intended even with a large increase to the MaxEB.

## Replies

**TheCookieLab** (2023-06-06):

This would significantly decrease “real” decentralization by effectively raising the 32 ETH solo staking floor to whatever the new EB value would be. Sure while one can still spin up a validator with 32 ETH, its influence would be one of a second-class citizen when compared to one with “maxed out” EB.

A few other observations:

1. The SSF numbers you provided as rationale are straw-man numbers (quite literally - the linked Horn proposal calls them “A Strawman Proposal” and notes significant improvements are possible with multi-threaded implementation).
2. You refer to the current 600K validator set as “artificially high” but the Ethereum upgrade road-map extensively uses 1-million validators as a scaling target. How can we currently be at “artificially high” levels despite being well under the original scaling + decentralization target?
3. You point to the May 11th & 12th, 2023 non-finalization as evidence of undue stress on the P2P layer however the root cause of said event was due to unnecessary re-processing of stale data. The fact that there were clients that were unaffected (namely Lighthouse) shows that the problem was an implementation bug rather than being protocol level.
4. The two pros listed under “validator perspective” are questionable. Sure, solo-stakers can now compound additional rewards, but at the trade-off of (potentially drastic) lower odds of proposals, sync committee selections, etc. This would be a huge net loss for the marginal 32 ETH solo staker. As for large-scale stakers, there is already tooling to manage hundreds/thousands of validators so any gain would be a difference in degree rather than kind, and even the degree diminishes by the day as tooling matures.

---

**DrewF** (2023-06-06):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/t/da6949/48.png) TheCookieLab:

> Sure, solo-stakers can now compound additional rewards, but at the trade-off of (potentially drastic) lower odds of proposals, sync committee selections, etc. This would be a huge net loss for the marginal 32 ETH solo staker.

Each unit ETH in the effective balance has the same likelihood of proposing and the same attestation weight as before.

Imagine a network with 2 real entities, one with 32 ETH and 1 validator, and another with 128 ETH in 4 validators. The entity with 32 ETH has 20% chance of selection, and 100% chance of proposing if selected, while the other entity has 80 and 100% chance for the same.

If the max EB was raised to 256 ETH, and the large entity consolidated its stake, the 32 ETH entity would have a 50% chance of selection, but only a 12.5% chance of proposing once selected, while the larger entity has 50% chance of selection, and 50% chance of proposing if selected.

Multiplying these out gives you 6.25% chance for the small entity and 25% chance for the large one. Since these don’t add up to 100% you have the “increased loop iterations” where you ping-pong between them more to decide who proposes, but with their odds of proposing normalized, the 32 ETH entity proposes 20% of the time, while the 128 ETH entity proposes 80% of the time.

The benefit of compounding rewards for solo stakers is pretty large, and their chance of proposing doesn’t fall due to a change in Max EB, only an increase of ETH being staked by others.

---

**yorickdowne** (2023-06-06):

> Reducing the operational overhead of managing many validators (benefits large-scale stakers)

Not entirely clear/convinced.

From the perspective of a firm that handles at-scale stake:

- We keep each “environment” to 1,000 keys, 32,000 ETH, for blast radius reasons. How many validator keys that is does not impact the operational overhead even a little bit. I am happy to unpack that further if warranted, if there are questions as to the exact nature of operational overhead.
- If I have validators with 2,048 ETH, how does that impact the slashing penalty in case of a massive f-up? I am asking - is there a disincentive for large stakers to consolidate stake into fewer validators?
- If I have validators with 2,048 ETH, does this reduce the flexibility of LST protocols to assign stake? For example, “the large LST” currently is tooled to create exit requests 32 ETH at a time, taking from older stake and NOs with more stake first. 2,048 ETH makes it harder for them to be granular - but at the same time so far there have been 0 such requests generated, so maybe 2,048 is perfectly fine because it wouldn’t be a nickel-and-dime situation anyway. Maybe someone at that LST can chime in.

Followup thought: Maybe the incentive for large-scale staking outfits is a voluntary “we pledge to run very large validators (VLVs) so you don’t do a rotating validator set”

---

**austonst** (2023-06-06):

Definitely see the advantages of this. Would this also reduce bandwidth requirements for some nodes, as currently running more validators means [subscribing to more attestation gossip topics](https://www.symphonious.net/2022/04/06/exploring-eth2-cost-of-adding-validators/)? Bandwidth is already a limiting factor for many solo/home stakers and could be stressed further by EIP-4844, seems any reductions there would be helpful.

But I’m also looking to understand the downsides. Presumably when the beacon chain was being developed, the idea of supporting variable-sized validators must have been discussed at some point, and a flat 32 ETH was decided to be preferable. Why was that, and why wasn’t this design (with all its benefits) adopted in the first place? If there were technical or security concerns at the time, what were they, and what has changed (in this proposal or elsewhere in the protocol) to alleviate them?

Are there any places in the protocol where equal-sized validators are used as a simplifying mathematical assumption, and would have to be changed to balance-weighted?

Thanks for putting this together!

---

**KuDeTa** (2023-06-08):

Generally strongly in favour of this proposal. Has any thought been given to how this might impact products and services related to the staking community? Restaking services like EigenLayer may be particularly interested in analysing the consequences.

---

**Wander** (2023-06-09):

Very interesting proposal. From the perspective of the core protocol’s efficiency, I do see the benefits, but I can’t support it in its current form due to the problems it presents for UX.

As presented, this proposal forces compounding upon all stakers. It’s not opt-in, so skimming is no longer reliable income for stakers. I appreciate the simplicity of this change, but it clearly sacrifices one UX for another.

To make this a true upgrade for all users, partial withdrawals would need to be implemented as well. Of course, this presents the same CL spam issue that partial voluntary exits have always had.

To solve this, I suggest we change the order of operations here. First, let’s discuss and finalize EL-initiated exits for both full exits and arbitrary partial amounts. The gas cost would be an effective anti-spam filter for partial withdrawals, and then we can introduce this change without affecting users as much. It does means the current UX of free skimming at a (relatively) low validator balance would now incur a small gas cost, but I think that’s a much more reasonable trade-off to gain the advantages of this proposal. And to some extent, the CL skimming computation is incorrectly priced today anyway.

---

**mikeneuder** (2023-06-14):

hi TheCookieLab! thanks for your response ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> This would significantly decrease “real” decentralization by effectively raising the 32 ETH solo staking floor to whatever the new EB value would be. Sure while one can still spin up a validator with 32 ETH, its influence would be one of a second-class citizen when compared to one with “maxed out” EB.

i don’t understand this point. how does it become a “second-class citizen”? a 32 ETH validator still earns rewards proportional the size of the validator. the 32 ETH validator is still selected just as often for proposing duty.

> The SSF numbers you provided as rationale are straw-man numbers (quite literally - the linked Horn proposal calls them “A Strawman Proposal” and notes significant improvements are possible with multi-threaded implementation).

agree! there can be improvements, but regardless, i think the consensus is that doing SSF with a validator set of approx. 1 million participants is not possible with current aggregation schemes. especially if we want solo-stakers to meaningfully participate in the network.

> You refer to the current 600K validator set as “artificially high” but the Ethereum upgrade road-map extensively uses 1-million validators as a scaling target. How can we currently be at “artificially high” levels despite being well under the original scaling + decentralization target?

it’s artificially high because many of those 600k validators are “redundant”. they are running on the same beacon node and controlled by the same operator; the 60k coinbase validators are logically just one actor in the PoS mechanism. the only difference is they have unique key-pairs. [Solo stakers: The backbone of Ethereum — Rated blog](https://blog.rated.network/blog/solo-stakers) is a great blog from the rated.network folks showing the actual amount of solo-stakers is a pretty small fraction of that 600k.

> You point to the May 11th & 12th, 2023 non-finalization as evidence of undue stress on the P2P layer however the root cause of said event was due to unnecessary re-processing of stale data. The fact that there were clients that were unaffected (namely Lighthouse) shows that the problem was an implementation bug rather than being protocol level.

it was certainly an implementation bug, but that doesn’t mean that there isn’t unnecessary strain on the p2p layer! i linked [Removing Unnecessary Stress from Ethereum's P2P Network](https://ethresear.ch/t/removing-unnecessary-stress-from-ethereums-p2p-network/15547) a few times, but it makes the case for the p2p impact.

> The two pros listed under “validator perspective” are questionable. Sure, solo-stakers can now compound additional rewards, but at the trade-off of (potentially drastic) lower odds of proposals, sync committee selections, etc. This would be a huge net loss for the marginal 32 ETH solo staker. As for large-scale stakers, there is already tooling to manage hundreds/thousands of validators so any gain would be a difference in degree rather than kind, and even the degree diminishes by the day as tooling matures.

this is the part that there must be confusion on! the validators have the same probability of being selected as proposer and sync committee members. the total amount of stake in the system is not changing and the validators are still selected with a probability proportional to their fraction of the total stake. as far as the large validators go, we have talked to many that would like to reduce their operational overhead, and they see this as useful proposal! additionally, it is opt-in so if the big stakers don’t want to make a change, then they can continue as they are without any issues.

---

**mikeneuder** (2023-06-14):

thanks, Drew! this is a great example ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) i mentioned the same think in my response to TheCookieLab too

---

**mikeneuder** (2023-06-14):

thanks, Yorick! this is really helpful context

> We keep each “environment” to 1,000 keys, 32,000 ETH, for blast radius reasons. How many validator keys that is does not impact the operational overhead even a little bit. I am happy to unpack that further if warranted, if there are questions as to the exact nature of operational overhead.

this makes a lot of sense. i think some staking operators would like to reduce the key-pair management, but maybe it isn’t a huge benefit. (if the benefits for big stakers aren’t that high, then that is ok IMO. we care most about improving the health of the protocol and helping small stakers compete.)

> If I have validators with 2,048 ETH, how does that impact the slashing penalty in case of a massive f-up? I am asking - is there a disincentive for large stakers to consolidate stake into fewer validators?

right, slashing penalties still are proportional to the weight of the validator. this is required because consider the case where a 2048 ETH validator double attests. that amount of stake on two competing forks needs to be slashable in order to have the same finality guarantees of today. we see the slashing risk as something validators will need to make a personal decision about.

> If I have validators with 2,048 ETH, does this reduce the flexibility of LST protocols to assign stake? For example, “the large LST” currently is tooled to create exit requests 32 ETH at a time, taking from older stake and NOs with more stake first. 2,048 ETH makes it harder for them to be granular - but at the same time so far there have been 0 such requests generated, so maybe 2,048 is perfectly fine because it wouldn’t be a nickel-and-dime situation anyway. Maybe someone at that LST can chime in.

i am not as familiar with the LST implications you mention here!

> Followup thought: Maybe the incentive for large-scale staking outfits is a voluntary “we pledge to run very large validators (VLVs) so you don’t do a rotating validator set”

absolutely! again, we are proposing something that is purely opt-in. but encouraging it from a roadmap alignment and network health perspective is useful because any stakers that do consolidate are helping and should be recognized for helping.

---

**mikeneuder** (2023-06-14):

Hey Auston ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) thanks for your reply.

> Definitely see the advantages of this. Would this also reduce bandwidth requirements for some nodes, as currently running more validators means subscribing to more attestation gossip topics? Bandwidth is already a limiting factor for many solo/home stakers and could be stressed further by EIP-4844, seems any reductions there would be helpful.

yes! less validators directly implies less attestations so a reduction in bandwidth requirements.

> Why was that, and why wasn’t this design (with all its benefits) adopted in the first place? If there were technical or security concerns at the time, what were they, and what has changed (in this proposal or elsewhere in the protocol) to alleviate them?

the historical context is around the security of the subcommittees. in the original sharding design, the subcommittees needed to be majority honest. this is not the case for 4844 or danksharding, so now the subcommittees are just used to aggregate attestations (1 of N honesty assumption). we talk a bit more about this in this section of the security doc: [Security Considerations and Spec Changes for a MAX_EFFECTIVE_BALANCE Increase - HackMD](https://notes.ethereum.org/@fradamt/meb-increase-security#Subcommittees)

> Are there any places in the protocol where equal-sized validators are used as a simplifying mathematical assumption, and would have to be changed to balance-weighted?

only a few! check out the spec pr if you are curious: [[DRAFT] Increase `MAX_EFFECTIVE_BALANCE` minimal spec change by michaelneuder · Pull Request #3 · michaelneuder/consensus-specs · GitHub](https://github.com/michaelneuder/consensus-specs/pull/3/files). the main changes are around the activation and exit queues, which were previously rate limited by number of validators, and now are rate limited by amount of ETH entering or exiting!

---

**mikeneuder** (2023-06-14):

hi KuDeTa!

> Generally strongly in favour of this proposal. Has any thought been given to how this might impact products and services related to the staking community? Restaking services like EigenLayer may be particularly interested in analysing the consequences.

staking services providers have seen this and we hope to continue discussing the UX implications for them! i am not sure if any restaking services people have considered it specifically! i will think more about this too ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**mikeneuder** (2023-06-14):

hi Wander! thanks for your reply ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

> As presented, this proposal forces compounding upon all stakers. It’s not opt-in, so skimming is no longer reliable income for stakers. I appreciate the simplicity of this change, but it clearly sacrifices one UX for another.

sorry if this wasn’t clear, but the proposal ~is~ opt-in. that was a big design goal of the spec change. if the validator doesn’t change to the `0x02` withdrawal credential, then the 32 ETH skim is still the default behavior, exactly as it works today.

> To solve this, I suggest we change the order of operations here. First, let’s discuss and finalize EL-initiated exits for both full exits and arbitrary partial amounts. The gas cost would be an effective anti-spam filter for partial withdrawals, and then we can introduce this change without affecting users as much. It does means the current UX of free skimming at a (relatively) low validator balance would now incur a small gas cost, but I think that’s a much more reasonable trade-off to gain the advantages of this proposal. And to some extent, the CL skimming computation is incorrectly priced today anyway.

i do love thinking about how we could combine the EL and CL rewards, but this paragraph seems predicated on the 32 ETH skimming not being present. i agree that in general, the tradeoff to consider is how much spec change we are OK with vs how the UX actually shakes out. i think this will be the main design decision if we move forward to the EIP stage with this proposal.

---

**ethDreamer** (2023-06-14):

I like this idea ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

My main concern with the proposal as currently written is that it seems to degrade the UX for home stakers. Based on my reading of [the code in your current proposal](https://github.com/michaelneuder/consensus-specs/blob/dd3911d7fc2bc86e983efe917743daa872dacab4/specs/_features/maxeb/beacon-chain.md#new-get_validator_excess_balance), if you’re a home staker with a single validator and you opt into being a compounding validator, you won’t experience a withdrawal until you’ve generated `MAX_EFFECTIVE_BALANCE_MAXEB` - `MIN_ACTIVATION_BALANCE` ETH, which (based on your 11 year calculation) would take ~66 years.

Speaking for myself, I don’t think I’d want to opt into this without *some* way to trigger a partial withdrawal before reaching that point. You have to pay taxes on your staking income after all ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12)

Off the top of my head, I can think of 2 ways to mitigate this:

1. Enable MAX_EFFECTIVE_BALANCE_MAXEB to be a configurable multiple of 32 up to 2048 by either adding a byte to every validator record or utilizing the WITHDRAWAL_PREFIX and reserving bytes 0x01…0x40 to indicate the multiple of 32.
2. Enable execution-layer initiated partial withdrawals

Note that 1 is a bit of a hack. I’ve heard 2 discussed before and (after reading some comments) it looks like [@wander](/u/wander) already mentioned this

---

**Wander** (2023-06-14):

Hey [@mikeneuder](/u/mikeneuder) thanks for the clarification! I have to admit that I only read your post, I didn’t click through to the spec change PR. The 0x02 credential is the first thing to pop up there ![:laughing:](https://ethresear.ch/images/emoji/facebook_messenger/laughing.png?v=12)

At first glance, a withdrawal credential change sounds like a great way to make this proposal opt-in while leaving the original functionality unchanged, but there are hidden costs.

Although this isn’t an objection, it’s worth noting that suggestions to add *optional* credential schemes are a philosophical departure from 0x01, which was *necessary*. While the conception of 0x00 makes sense historically, today it makes little sense to create 0x00 validators. Put another way, if Ethereum had been given to us by advanced aliens, we’d only have the 0x01 behavior. At least the Ethereum community, unlike Linux, has a view into the entire user space, so maybe one day 0x00 usage will disappear and can be removed safely. Until then, though, we’re stuck with it. Do we really want to further segment CL logic and incur that tech debt for an optional feature? Again, not an objection per se, but something to consider.

Regardless, I suspect that achieving this via EL-initiated partial withdrawals is better because users will want compounded returns anyway, even with occasional partial withdrawals.

Optimal workflow if `MAX_EFFECTIVE_BALANCE` is increased for all users after EL-initiated partial withdrawals are available:

1. combine separate validators (one-time process)
2. partially withdraw when bills are due
3. repeat step 2 as needed, compound otherwise

Optimal workflow if `MAX_EFFECTIVE_BALANCE` is increased for an optional 0x02 credential:

1. combine separate validators (one-time process)
2. exit entirely when bills are due
3. create an entirely new validator
4. go back to step 2 and 3 as needed, compound otherwise

Even if the user and CL costs end up similar under both scenarios, the first UX seems better for users and the network. The 0x02 path may only be worthwhile if validator set contraction is truly necessary in the short term. Otherwise, we have a better design on the horizon.

---

**mikeneuder** (2023-06-15):

thanks for the comment ethDreamer!

Absolutely the UX is a critical component here. The initial spec proposal was intentionally tiny to show how simple the diff could be, but it is probably worth having a little more substance there to make the UX better. We initially wrote it so that any power of 2 could be set as the *ceiling* for a validator, so you could choose 128 to be where the sweep kicks in. This type of question I hope we can hash out after a bit more back and forth with solo stakers and pools for what they would make use of if we implement it ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**mikeneuder** (2023-06-15):

thanks for the thorough response [@Wander](/u/wander) ! I agree that the first workflow sounds way better! Again we mainly made the initial proposal with the 0x02 credential to make the default behavior unchanged, but if we can get a rough consensus with everyone that we can just turn on compounding across the board with EL initiated partial withdrawals, then maybe that is the way to go! (it has the nice benefit of immediately making the withdrawal queue empty because now withdrawals have to be initiated and there is no more sweep until people hit 2048 ETH).

---

**dapplion** (2023-06-15):

Noting that reducing state size also facilitates (or unlocks depending who you ask) another item from the roadmap. Single Secret Leader Election, with any possible construction would require a significant increase in state size (current Whisk proposal requires a ~2x increase)

---

**TheCookieLab** (2023-06-17):

[@DrewF](/u/drewf) thanks for the info.

[@mikeneuder](/u/mikeneuder) my mistake, I was under the impression that raising the effective balance would alter the real-world reward dynamics but in light of DrewF’s explanation I stand corrected. What - if any - impact on RANDAO bias-ability? Is the current system implicitly assuming that each randao_reveal is equally likely, and if so how would the higher “gravity” of large effective balances play out?

---

**0xTodd** (2023-06-19):

Excellent proposal, especially raising the node cap to 2048 (or even 3200, seems entirely reasonable to me). Currently on the Beacon Chain, the addition of new nodes requires an excessively long wait time. For instance, on June 18th, there were over 90,000 nodes in queue, and they needed to wait for 40-50 days, which is extremely disheartening for those new to joining ETH consensus.

In fact, from my personal interactions, I’ve come across many users who hold a significant amount of ETH. Considering the daily limit on nodes the consensus layer can accommodate, if one individual holds 2000 ETH, under this new proposal, they would only occupy 1 node instead of 62-63 nodes. This could potentially increase the efficiency of joining the node queue by 10x or even 20x, enabling more people to join staking at a faster rate. This also reduces people’s reliance on centralized exchanges for staking (simply bcuz there is no waiting time in cexs), which would make ETH network more robust.

I sincerely hope this proposal gets approved.

---

**djrtwo** (2023-06-19):

[@0xTodd](/u/0xtodd) The amount of *eth* is rate limited into and out of the active validator set for security reasons (security margin epoch-over-epoch degrades as eth enters/leaves). **Not** the number of validators.

In the event such a proposal goes into effect, the amount of ETH that can enter and leave per unit time would generally remain unchanged (unless the security margin was decided to be changed).


*(40 more replies not shown)*
