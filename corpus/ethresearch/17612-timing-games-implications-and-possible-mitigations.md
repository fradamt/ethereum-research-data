---
source: ethresearch
topic_id: 17612
title: "Timing Games: Implications and Possible Mitigations"
author: casparschwa
date: "2023-12-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612
views: 10102
likes: 75
posts_count: 20
---

# Timing Games: Implications and Possible Mitigations

## Timing Games: Implications and Possible Mitigations

by [caspar](https://twitter.com/casparschwa) and [mike](https://twitter.com/mikeneuder) – based on extensive discussions and reviews from [barnabé](https://twitter.com/barnabemonnot) and [francesco](https://twitter.com/fradamt).

**Acknowledgements**

*Additional thanks to [Thomas](https://twitter.com/soispoke), [stokes](https://twitter.com/ralexstokes), [Toni](https://twitter.com/nero_eth), [Julian](https://twitter.com/_julianma), & [Anders](https://twitter.com/weboftrees) for discussions and comments!*

**Framing**

*This post aims to provide context about timing games, highlight their implications, and outline different paths forward. The goal is to initiate a constructive discussion, contributing to an informed decision by the community.*

---

## Context

### Intro

Relying on honest instead of rational behavior in incentivized systems such as blockchain protocols is not sustainable. However, we are in a situation where timing games are individually rational to play and cause negative externalities for the network as a whole.

**The equilibrium where everyone maximally plays timing games is not more favorable to any one validator than if everyone follows the protocol specifications honestly.** However, there is money to be made on the path to the equilibrium by block proposers playing timing games more aggressively than others; thus the honest strategy is not an equilibrium. While more research on sustainable and incentive-compatible mitigation schemes is conducted, it might be helpful to explore temporary, but less sustainable approaches to coordinate honest protocol participation.

In this post, we try to lay out the consequences of timing games and the options both in the short and long term. Ideally, this serves as a starting point for a genuine discussion regarding timing games within the broader community.

### Time in Ethereum

In Ethereum, time is measured in 12-second slots. During each slot, one validator is selected as the block proposer. According to the [honest validator specifications](https://github.com/ethereum/consensus-specs/blob/b2f2102dad0cd8b28a657244e645e0df1c0d246a/specs/phase0/validator.md#phase-0----honest-validator), the rules for protocol participation, a [block should be released at the beginning of the slot (0 seconds into the slot, t=0)](https://github.com/ethereum/consensus-specs/blob/b2f2102dad0cd8b28a657244e645e0df1c0d246a/specs/phase0/validator.md#block-proposal). Furthermore, the protocol selects a committee of attesters from the validator set to vote on the canonical block in their local view. The [specification dictates](https://github.com/ethereum/consensus-specs/blob/b2f2102dad0cd8b28a657244e645e0df1c0d246a/specs/phase0/validator.md#attesting) that the attestation is made as soon as they hear a valid block for their assigned slot, or 4 seconds into the slot (`t=4`), whichever comes first. We refer to `t=4` as the attestation deadline.

More on this [here](https://www.paradigm.xyz/2023/04/mev-boost-ethereum-consensus) and [here](https://www.youtube.com/watch?v=gsFU-inKRQ8).

### What are timing games?

Timing games are a strategy where block proposers intentionally delay the publication of their block for as long as possible to maximize MEV capture. Given the attestation deadline at `t=4`, a rational proposer needs to ensure a sufficient share of the attesting committee, [40%](https://github.com/ethereum/consensus-specs/pull/2895), votes for their block to avoid [being reorged by the subsequent block proposer](https://github.com/ethereum/consensus-specs/pull/3034).

A validator who *intentionally* delays their block proposal to capture more MEV is playing timing games. We define honest behavior as:

- Using mev-boost: Requesting a block header at t=0.
- Not using mev-boost: Requesting a block from the execution engine at t=0.

Deliberate deviation from either strategy by modifying the client software is considered playing timing games under our definition. This is in contrast to “organic” latency in which a block proposal is later (e.g., from low-resource home staking).

Timing games are deeply rooted in how time in (partially) synchronous Proof-of-Stake protocols works. It’s not clear whether there exists an alternative design that prevents them entirely. Still, the status quo can be improved through short-term mitigations, as well as longer-term resolutions including protocol changes aimed at directly improving incentive compatibility. We explore both below.

More on this [here](https://arxiv.org/abs/2305.09032), [here](https://x.com/casparschwa/status/1660931488110583811?s=20), [here](https://www.youtube.com/watch?v=sJBZGqAT7gE), and [here](https://www.youtube.com/watch?v=jTZq58SB1l8&t=48s).

## Impact of timing games

### Zero-sum nature

By playing timing games, the proposer at `slot N` reduces the duration of the `slot N+1` auction. Any additional MEV earned by the `slot N` proposer is, by definition, being taken away from the following validator. There is no free lunch; no new MEV is being created.

### Consensus degradation

Delayed block proposals may lead to more missed slots, reorgs, and incorrect attestations. The protocol is designed around the network latency of propagating blocks between peers, thus any change in the timing of the initial release of the block has downstream effects on the attesting committee and subsequent proposer. Note that the degradation of the network is only rational insofar as proposers continue to benefit from playing more aggressive timing games. Any missed slots have a large negative impact on the yield of the pool, so optimizing for the inclusion rate should help with the consensus stability.

### Attester timing games

In response to late proposals, rational attesters may delay their attestation deadline to vote accurately. This in turn allows block proposers to further delay their blocks. At the limit, a rational proposer knows their block needs to receive only 40% of the committee’s attestation votes ([proposer boost](https://github.com/ethereum/consensus-specs/pull/2895)). If they maximally delay their proposal they could target a split in the committee such that 40% of the committee hears the block before the attestation deadline (and vote for it), and 60% do not hear the block before the attestation deadline (and vote for the parent). An attester wants to get their head vote correct and so wants to make sure to be part of the accurate 40%. They can achieve this by delaying their attestation slightly (while making sure they propagate it in time for aggregation - a second round of sub-slot timing games). Attestation committees are large enough that targeting splits is feasible. Arguably the timing game would still be contained within the slot boundaries because otherwise, the subsequent block proposer could reorg the very late block.

This risks degrading into a consensus protocol that is hard for validators to reason about both theoretically and practically, potentially greatly undermining the stability and reliability of the Ethereum network overall.

### Impact on blob inclusion (h/t Dankrad for mentioning this)

Blobs offered by EIP-4844 increase the size of the blocks and thus slow down their propagation to the rest of the network. If the attesting committee does not hear about a block and the accompanying blobs in time, there is a risk for the block to be reorged. Let t_1 denote the latest release time for a blobby block to reach sufficient attesters; let t_2 represent the same time but for a non-blobby block. Then t_1 < t_2 because of the increased block size of the blobby block. If the expected revenue of a block without blobs (but more MEV) released at t_2 is greater than that of a block with blobs at t_1, a rational proposer will not include blobs. Blob creators may be required to pay higher blob priority fees to compensate for the opportunity cost faced by the rational block proposer.

The extra-protocol PBS market established by `mev-boost` changes the game dynamics. Proposers do not know whether they can capture more MEV by including blobs and releasing the block earlier or excluding blobs. The underlying incentives exist for builders and proposers to overcome this information asymmetry. The most straightforward way is for them to enter a trusted relationship in the form of builder-relays (such as Flashbots, bloXroute, Eden, & Manifold). At the very least a builder-relay can delay their response to the `getHeader` request up until the 950ms timeout.

Some more on this [here](https://efdn.notion.site/Blob-concerns-4168d74619554ac1b7ee50c3b9e5d637?pvs=4).

## Genuine latency or timing games?

It is not obvious if a validator is intentionally playing timing games or unintentionally proposing a block late.

### mev-boost detour

Note that this subsection is directly taken from “[Time is Money: Strategic Timing Games in PoS Protocols](https://arxiv.org/pdf/2305.09032.pdf)”.

Searchers look for MEV opportunities (e.g., arbitrages), and submit bundles of transactions alongside bids to express their order preference to block builders. Block builders, in turn, specialize in packing maximally profitable blocks using searcher bundles, internally generated bundles, and other available user transactions before submitting their blocks with bids to relays. Relays act as trusted auctioneers between block proposers and block builders, validating blocks received by block builders and forwarding only valid headers to validators. This ensures validators cannot steal the content of a block builder’s block, but can still commit to proposing this block by signing the respective block header.

[![](https://ethresear.ch/uploads/default/optimized/2X/4/47b1fb321cf475cbf77eee57e859476aa78c7e65_2_690x411.png)1712×1022 81.9 KB](https://ethresear.ch/uploads/default/47b1fb321cf475cbf77eee57e859476aa78c7e65)

When the proposer chooses to propose a block, the proposer requests `getHeader` to receive the highest bidding, eligible block header from the relay. Upon receiving the header associated with the winning bid, the proposer signs it and thereby commits to proposing this block built by the respective builder in slot n. The signed block header is sent to the relay, along with a request to get the full block content from the relay (`getPayload`). Finally, the relay receives the signed block header (`signedAt`) and publishes the full block contents to the peer-to-peer network and proposer. As soon as peers see the new block, validators assigned to the slot can attest to it. This cycle completes one round of consensus repeating every slot.

### Role of latency in mev-boost

Honest validator clients request a block from `mev-boost` at `t=0`. `mev-boost` then pings all relays that it is connected to for their maximum bid and waits up to 950ms for the response. As a consequence, a block header might only be returned to the validator client 950ms after it was requested (note that this is not the norm). Stakers that behave honestly become indistinguishable from someone playing timing games and intentionally delaying their block.

Consider three hypothetical proposers, Alice, Bob, and Charlie. They each use `mev-boost` to outsource their block production, but have slightly different setups. As a result, their p2p footprint is significantly different:

**Alice:** As a solo staker in the eastern US, Alice sends her request to a US-based relay right at the beginning of her slot. With a short latency of 20ms and a quick signing on her local machine, the block is published at 60ms into the slot (three round trips are necessary). Because she made her request at `t=0`, she unintentionally captured an extra 20ms worth of MEV that was generated in that interval.

**Bob:** As a solo staker in Australia, Bob sends his request to the same US-based relay at the start of his slot. He has a worse internet connection and thus has a latency of 200ms to the relay. His block is published at 600ms into the slot, despite his request also being sent at `t=0`. Bob benefits from being further from the relay because the 200ms it takes for his request to land on the relay are additional milliseconds of MEV captured by the winning bid.

**Charlie:** Charlie is part of a staking pool also running out of the US. He intentionally waits 500ms into his slot before making the call to the relay. From his perspective, he can still get his block published well before the `t=1`, so why not collect a little extra MEV for his trouble?

**Tldr; honest protocol participation can be indistinguishable from rational validators playing timing games.** It requires active monitoring to understand if delays are due to bad latency or timing games and intentions are not necessarily distinguishable (bid time stamps provided by relays are fully trusted).

## The path forward: To play or not to play timing games?

### Time is money

The simplest path forward is to let things play out naturally and accept the reality of the protocol incentives as it is designed currently. It could be that timing games just shift the block release times back a bit and after a while, everyone adjusts to the new equilibrium, which is almost identical in payoffs compared to everyone following the (not rational) honest protocol specifications. We would likely observe more missed slots than before, but for the expected value of timing games to be positive, validators cannot be too aggressive with their block release strategy because they run the risk of their blocks being orphaned. In such a setting, one needs to consider accelerating timing games to allow stakers who cannot or do not want to actively engage in tuning latency parameters to partake in the arena of timing games. One way to enable this easily is the idea of “timing games as a service”, see further below.

The flip side to this is that this is uncharted territory with potential failure modes that are not well understood. Most importantly, why should only proposers play timing games, when it is rational to delay attestations in such an environment? It is unclear how this would play out and if the chain would be able to reliably produce blocks. Given this, such an accelerationist position toward timing games is potentially a higher risk.

### Time is money but only temporarily

The honest protocol specification is not incentive-compatible because playing timing games is a more profitable strategy if a validator plays it more successfully than others. The equilibrium of timing games is identical in payoffs to everyone playing honestly (assuming relay enforcement via option 2, see below, or a relatively simple change to `mev-boost` that is already [discussed](https://ethresear.ch/t/bid-cancellations-considered-harmful/15500#future-directions-12)). Ultimately, all validators face a deadline, be it `t=0` or `t=4`. Facing either deadline leaves validators with equal payoffs relative to other validators. Playing honestly is merely not an equilibrium because there is money to be made on the path to the equilibrium, which is everyone playing timing games maximally. In this equilibrium, an optimized staking operator can gain a competitive advantage over another staker equivalent to the reduction in one-way latency between the validator and the relay. But this same competitive advantage already exists if everyone plays honestly.

Given the negative externalities of timing games and the short-lived room for increased profits, it’s worth exploring whether it’s possible to keep the honest strategy a Schelling point (in the colloquial meaning).

## Possible short-term mitigations

### Timeliness enforced by relays

Timing games present a typical prisoner’s dilemma where each validator has the option to defect by engaging in these games. This situation is inherently unstable, as any single validator’s decision to defect can disrupt the stability of everyone playing honestly. **Relays can help to coordinate around not playing timing games** by enforcing some timeliness on validators, thereby reducing the scale of the coordination challenge to the more manageable count of relays.

Relays may reject builder bids that arrive after `t=0`, or reject `getHeader` or `getPayload` requests after `t=0`. In the status quo, this removes the ability for proposers to take advantage of timing games.

#### Assumptions

- No relay defects from enforcing these rules. Relays are already trusted entities so extending that trust further is not ideal, but not unrealistic.
- Validators do not enter trusted relationships with builders directly, circumventing the necessity for relays (e.g., builder-relays). Validators need a reputation to be trusted by builders, as they could steal the MEV. Hence, it is largely about trusting that large staking pools and whales do not defect from using relays.

#### Benefits

The coordination problem is reduced by orders of magnitude. It is still a prisoner’s dilemma, but socially it is much easier to coordinate and sustain.

- Defection is more easily detectable, see the section on monitoring. Importantly, only a handful of relays need to be monitored to not release blocks late (further assuming no trusted validator-builder relationships).
- Relays are already trusted not to steal MEV, so adding a new trust assumption is more feasible than trusting the validators themselves.
- Relays already have some cutoff times implemented, which could easily be changed.

#### Drawbacks

- It is still rational for validators to defect if they find a way to do it.
- It only takes a single relay to “defect alongside” with a validator for defection to be possible.
- A validator and builder entering a trusted relationship can defect together. In other words, it incentivizes vertical integration.
- Social coordination is unsustainable and messy.

#### Monitoring

- Block release times. If consistently late, likely due to timing games.
- Cross-referencing bids on different relays to check when they were received. This can help give an idea of the winning bid likely arrived after the start of the slot.
- Transactions included in blocks that were not in mempool before t=0 indicate timing games are being played. There is still the possibility that the prior point is due to private orderflow, rather than the inclusion of late transactions. But together with late block releasing, this becomes a strong indicator for timing games.
- Correlating prices of on-chain trading venues with off-chain prices (potentially super noisy).

Overall, relay enforcement is a tool to make social coordination on following the honest protocol specifications easier. While it is not sustainable, it could help in the short term. The figure below shows the three calls that define the block production flow in `mev-boost`. Each dotted line represents a point at which a relay enforcement could take place. Options 1-3 are discussed in detail below.

[![photo_2023-12-05 15.00.55](https://ethresear.ch/uploads/default/optimized/2X/a/ae9f63a3af0c8394fabf71a04d390e91228e6116_2_690x373.jpeg)photo_2023-12-05 15.00.551139×616 50.3 KB](https://ethresear.ch/uploads/default/ae9f63a3af0c8394fabf71a04d390e91228e6116)

#### mev-boost calls

The [mev-boost](https://github.com/flashbots/mev-boost/#api) flow contains three critical events, each of which could be enforced at the slot boundary of `t=0`: (i) `submit bid`, (ii) `getHeader`, (iii) `getPayload`. Right now, there are already [two timestamps](https://github.com/flashbots/mev-boost-relay/blob/98576112e245454a225e9a668cacfa498eea00b4/services/api/service.go#L83) enforced by the relay:

```auto
getHeaderRequestCutoffMs = cli.GetEnvInt("GETHEADER_REQUEST_CUTOFF_MS", 3000)
getPayloadRequestCutoffMs = cli.GetEnvInt("GETPAYLOAD_REQUEST_CUTOFF_MS", 4000)
```

In other words, `getHeader` must be called by `t=3`, and `getPayload` must be called by `t=4`. The following options explore changing these bounds to be more strict.

#### Option 1: Relay rejecting new bids after t=0

Description: The relay can reject any bids submitted by builders once the slot has begun (at `t=0`). This removes any incentive for the proposer to delay their call to `getHeader` because the value of the bid will no longer increase.

#### Option 2: Relay rejecting getHeader requests after t=0

Description: Alternatively, a relay could reject `getHeader` requests once the slot has begun (at `t=0`). This has the effect of ending the auction since no new bids are served to the proposer and also enforces that the proposer at least receives their bid by the beginning of the slot.

#### Option 3: Relay rejecting returning getPayload requests after t=0

Description: A relay could reject any calls to `getPayload` after the slot has begun (at `t=0`). This is an even stronger requirement because it enforces that the proposer completes the signing process by the beginning of their slot.

### Timing Games as a Service by relays (h/t Justin)

Description: Another idea is for relays to offer “Timing Games as a Service” (TGaaS). This approach aims to democratize access to timing game rewards rather than eliminate them – the same design principle that inspired `mev-boost` in the first place. TGaaS builds on the following facts:

- relays are well-peered in the p2p layer, and
- relays know the ping latency to the proposer.

With this, the relay can take on an additional role of advising the proposer on when they should sign a builder’s bid. This is easiest understood with a toy example; assume the relay has calculated that

1. the ping latency of the slot N proposer is 100ms,
2. the proposer expects to take 100ms to sign a header (this could be a new field in the validator registration),
3. the block takes 400ms to propagate given the relay peering.

Then the relay can push a header to the proposer at `t=3.3`, expecting the proposer to receive it at `t=3.4`, complete the signing at `t=3.5`, return the signed header to the relay at `t=3.6`, leaving 400ms for the relay to circulate the block to the attesters. In reality, it would be up to the relay to tune these parameters to minimize the number of missed slots they cause. Most likely, a few hundred additional milliseconds would be added as a safety buffer to account for the tail latencies of networking.

In theory, a proposer could tune the `getHeader` request time such that they receive the block header by the relay at the same time as the relay offering TGaaS would push the header to the proposer. Practically however, it is likely that outsourcing this complexity allows e.g. home stakers to play timing games more aggressively.

However, it is unclear how to not introduce complexity for a proposer if they sign up for multiple TGaaS relays. Say there are two relays A and B, with A fast, and at the “final time” for B (the time at which the proposer has to either sign B’s header or give up on B) the bid from B is higher. Now the proposer has to determine whether the extra time bought by A’s latency advantage is worth gambling on.

**Pros:**

- It democratizes access to timing games, reducing the benefit of sophistication.
- Relays would have extensive access to data and could tune their parameters to minimize the liveness impact of TGaaS.

**Cons:**

- It increases the probability of attester timing games being played.
- It is unclear how a proposer avoids complex latency parameter tuning without relying on a single point of failure.
- Proposers lose agency over block release time to relays.
- Relays might not maximize over the same objective function. The opportunity cost of a relay missing a slot is significantly less, e.g. they do not stand to lose CL rewards.
- This proposal furthers the dependency on relays and their performance directly corresponds to the Ethereum network health. Relays absorb more responsibility and risk, while presently they serve more as a simple pipe connecting proposers to builders.

## Possible long-term mitigations

This section highlights some of the design space (by no means complete) that exists to alter incentives to improve protocol resilience to timing games. Each idea will only be briefly discussed as the details are beyond the scope of this post.

### Retroactive proposer rewards

The goal here is to explicitly incentivize timeliness. The trouble is to find a good on-chain heuristic for what “timely” means. One heuristic could be to use the share of “same-slot attestations” that are included in the subsequent block. The intuition is that, if almost all attesters (from the same slot) saw the block in time to vote for it, then the block must have been somewhat timely.

**Pros:**

- Explicitly incentivizes timeliness.
- Arguably rewards intended validator behavior regardless of timing games.

**Cons:**

- MEV rewards can dominate timeliness rewards.
- Hard to discriminate between different degrees of timeliness, as within a few milliseconds the share with which the block is seen by most of the attesting committee jumps from a very low to high value.

[Here](https://notes.ethereum.org/@css/H162Hky85) is an old high-level write-up of this idea.

### Missed slot penalties

Currently, there is no penalty for a proposer missing a block. The “only” cost is the opportunity cost of not receiving any consensus and execution-related rewards. Introducing a penalty for missing a slot would decrease the expected value of playing timing games because the increased probability of a missed slot (by playing timing games) now carries negative weight.

**Pros:**

- Simple to implement and reason about.
- Reduces the expected value of playing timing games.

**Cons:**

- Penalizes honest proposers who happen to organically miss a slot (solo stakers likely miss more slots relative to professional staking operators).
- Big node operators can better manage associated penalty risks for they propose many blocks a day.
- Requires selection of a “magic number” for how large the penalty is (all consensus rewards are already arbitrary, but due to the high variance of MEV, pricing penalties in that domain is particularly tricky).

### Earlier attestation deadline with some backoff scheme

The attestation deadline being at `t=4` makes the timing games highly profitable. If instead, the deadline was earlier, there would be less value to capture relative to everyone participating honestly. In other words, it reduces the difference in the value of playing honestly and playing timing games. This comes at the cost of worse liveness properties of the protocol because of the higher probability of organically missed slots due to network latency. Thus a backoff mechanism that dynamically adjusts the attestation deadline based on chain performance is necessary.

**Pros:**

- Reduces the absolute value capturable by timing games: lower opportunitiy cost to honest protocol participation.
- A backoff scheme is also a prerequisite for (block, slot)-voting, which in turn is useful for several things: a cleaner implementation of honest reorgs of late blocks and a prerequisite for ePBS designs.

**Cons:**

- Increases protocol complexity.
- Unlikely that the attestation deadline would be shifted significantly. Blobs will naturally shorten the possible timing game window. Even rebalancing the attestation deadline to something later is discussed.
- Only effective in reducing the opportunity cost to honest protocol participation.
- It does not perevent attester timing games, but could accelerate them.

### Probabilistic sub-slot proposing (h/t Francesco & Vitalik)

Say a slot is 10s long and split up further into 100ms sub-slots. Each sub-slot has a 1% probability of having a proposer such that in expectation you have one proposer every 10s.

Then a proposer is only guaranteed their monopoly for the duration of their sub-slot. It might be that a proposer is elected for the subsequent sub-slot already. As a result, timing games are practically only possible in expectation.

**Pros:**

- Fundamentally changes the game dynamics and challenges timing games at its ‘core’: Delaying block proposals immediately risks being reorged.
- Prevents attester timing games.

**Cons:**

- Timing games are playable in expectation, but importantly it avoids attester games.
- Deep protocol change.
- PoW-style block times as opposed to a block proposer every 12s.

This is an exciting direction to explore further as it tackles the problem closer to the root. But it is also an involved protocol update with lots of elements yet to be understood. Currently, this is only a promising idea.

## Conclusion

In the end, the path to choose largely depends on how dangerous attester games are considered to be. This post aims to provide context about timing games, highlight their implications, and outline different paths forward. The authors do not favor any mitigation specifically. Instead, the goal is to initiate a constructive discussion, contributing to an informed decision by the community.

## Replies

**tripoli** (2023-12-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> The equilibrium where everyone maximally plays timing games is not more favorable to any one validator than if everyone follows the protocol specifications honestly

This is only true for small perturbations where timing games don’t cause degradation in consensus. If proposers maximize their expected value and are willing to miss the occasional slot then the game ceases to be zero-sum and morphs into a new game. In this new game the valuable attributes are low latency and low variance–this is where professional staking services excel and is what parts of the community have been warning about.

When people say that decentralized sets of validators (ie: solo validators or Rocket Pool) are matching the performance of more centralized sets, it’s because those professional/centralized sets haven’t leveraged their advantages at all.

---

I think it’s important to determine whether proposers other than p2p are actively playing timing games. The tone of your post implies that they’re not that common, but if we look at the bid timing data from relays and strip out all but the very first relay to receive the winning block hash there’s a very clear spike between 2000 and 2500 ms. I’ve observed similar data in the flashbots mempool dumpster dataset, and as much as it could be from latency, the consistency around where other research has identified as the peak value time is far too striking for me to call a coincidence.

[![slot-time-distribution-all 2](https://ethresear.ch/uploads/default/optimized/2X/1/10f8ec3683c0a891b39a831c62d79546c76614fe_2_690x345.png)slot-time-distribution-all 22600×1300 101 KB](https://ethresear.ch/uploads/default/10f8ec3683c0a891b39a831c62d79546c76614fe)

> Data via: GitHub - dataalways/mevboost-data: Public domain Ethereum MEV-Boost winning bid data

---

**mkoeppelmann** (2023-12-06):

**The equilibrium where everyone maximally plays timing games is not more favorable to any one validator than if everyone follows the protocol specifications honestly.**

In my view we need to think about how this equilibrium looks like. If e.g. the equilibrium looks like - everyone would propose at t+3 than this would be an acceptable outcome - or, it would likely mean that we should do attestations at t+1 instead of t+4.

However - this will NOT be an equilibrium as if everyone would push back proposal it would also be rational to delay attestations. You mention that this game has and end when approaching the next slot time - but even that is not clear - if all attestations come in only in the last second of the previous block certainly it will be better to wait a bit as a proposer for the next block.

My strong hunch is (and there is strong theoretical research that show that most complex games have only nash equilibria that involve “mixed strategies”  (player randomly deciding to act in the same situation different))

A few theoretical thoughts of how such a desirable equilibria looks like:

a) proposer payoff is highest a t+0

As we know that MEV will increase at least linear (actually MEV increases more than linear with more transaction/time) delaying the submission needs to increase orphaned risk/ orphaned patently at least in such a way to not lead to a greater payoff than at t+0

IMO this can be best achieved by attesters playing a mixed strategy about when to submit their attestation. There needs to be at least some chance they they decide to attest already after the minimum time it would take to see the block if the proposer attests at t-0.

For a mixed strategy to be an equilibrium every possible decision needs to have the same expected payout - so the expected payout for the attester needs to be the same, regardless wether they (randomly) decide to attest at t+1 or at t+7.

b) attester payoff needs to be equal over a range of time, starting at t+(minimal propagation)

---

**Nero_eth** (2023-12-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> For a mixed strategy to be an equilibrium every possible decision needs to have the same expected payout - so the expected payout for the attester needs to be the same, regardless wether they (randomly) decide to attest at t+1 or at t+7.

This would just postpone the event and in t+7 we’re still not sure what the head of the chain is because all attesters would play rational by waiting until t+6 - t+7 until they attest for block t+1 to make sure that they attest on the right fork.

I think it could be more interesting to think about something like “attestation boost”, meaning a mechanism that punishes late p2p gossiped attestation, maybe letting the aggregaters categorize attestations into early and late attestations that come with different payouts.

Just to create an incentive to determine the head of the chain as quickly as possible.

Then, the actual inclusion doesn’t matter if those rewards are higher than the inclusion, but not sure what a healthy balance could look like. Just some random thoughts.

---

**terence** (2023-12-06):

Some notes from client implementation’s angle:

> The specification dictates that the attestation is made as soon as they hear a valid block for their assigned slot, or 4 seconds into the slot (t=4), whichever comes first. We refer to t=4 as the attestation deadline.

Note that Prysm and some other client implementations(?) always wait until 4s to submit attestation. But this has no relevance to this post.

> ## Impact of timing games

I’d also add user experience degradation into the mix. The impact on blob inclusion is a big one, IMO. Say Including blob txs delays your block proposal by `x`, while blob txs profit you by `y`. Calling `getHeader` late by `x` and allocating time to build the block can profit you by `z`. Assuming `z` is greater than `y`, profit-maximizing validators will prefer using `x` for building blocks instead of including blob transactions and propagating them through the network.

> #### Option 2: Relay rejecting getHeader requests after t=0

Validator client will do specific accounting tasks like update head before `getHeader` in addition to network latency so realistically, this can never be `0`. It’s also hard to set a time bound here because client implementation and network latency varies.

Option 1, that relayer rejecting new bids after t=0, seems like the cleanest short-term solution.

> ### Missed slot penalties

A cute idea here is something provable by consensus that a slot is “skipped” or “orphaned”; given such proof, it can be penalized accordingly.

In conclusion, it’s important to determine if there is a measurable impact on validator profitability from these time-sensitive games. Specifically, what is the increase in rewards for bids posted after time t=0? It seems feasible to gather this data from the relayer. If the profits are significant, I am concerned about the potential for vertical integration among validators, relayers, and builders, possibly through co-location or other means. Such integration could harm decentralization and various aspects of chain neutrality. A short-term solution might be for relayers to agree not to accept bids after t=0 collectively

---

**casparschwa** (2023-12-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> This is only true for small perturbations where timing games don’t cause degradation in consensus. If proposers maximize their expected value and are willing to miss the occasional slot then the game ceases to be zero-sum and morphs into a new game. In this new game the valuable attributes are low latency and low variance–this is where professional staking services excel and is what parts of the community have been warning about.

I don’t think I follow what precisely you’re getting at, but maybe this clarifies something: The point we’re making in the post is that all validator are indifferent between everyone playing honestly and everyone maximally playing timing games. The intuition for this is that latency advantages exist in either scenario, as in both a low-latency proposer can sign later block headers.  A qualifier for the above argument is this statement from the post:

> (assuming relay enforcement via option 2, see below, or a relatively simple change to mev-boost that is already discussed).

---

![](https://ethresear.ch/user_avatar/ethresear.ch/tripoli/48/22199_2.png) tripoli:

> I think it’s important to determine whether proposers other than p2p are actively playing timing games. The tone of your post implies that they’re not that common

In this post we do not empirically analyze who is playing timing games at all. So we do not suggest anything about anyone specifically. Some early data analysis I have seen does suggest that some staking operators are very slow to sign blocks (and so do not extract more MEV despite the network seeing blocks late), but some operator(s) play timing games (low latency + late blocks). A good starting point for understanding whether timing games are intentionally played or whether someone has bad latency is to look at the difference between winning bid timestamps and when a block is first seen on the p2p layer.

---

**austonst** (2023-12-06):

A little bit from the relay operator perspective (Aestus here). It seems very likely to me that proposer latency games are inevitable and will always push any deadlines enforced by relays or the protocol to their limits. I’m surprised it’s taken this long, but with the topic more public now, I suspect remaining social consensus around honest behavior will quickly fall apart.

The primary concern for me is the difference in block value between sophisticated and unsophisticated proposers. In the extreme, we could see home stakers proposing honestly at `t < 1s` while sophisticated staking-as-a-service providers propose at `t >= 3s`. This 2s+ difference (as p2p has argued) makes a sizeable difference in block value, and threatens the level playing field that MEV-Boost had created for proposers.

### TGaaS

For short-term mitigations, I lean towards some version of timing games as a service. If timing games are truly an inevitability, the best thing we can do is democratize access to it. Relays are well-suited to helping proposers play timing games safely, and can do their best to mitigate the risks to network health while providing an open interface to timing game functionality that is equally accessible to all proposers.

In the minimally simple example I’ve been imagining (functionally similar to the toy example in the IP), the proposer’s getHeader call could contain an additional parameter, e.g. `?returnMsIntoSlot=` (with an appropriate timeout). The relay estimates the proposer’s latency and times their header delivery such that the proposer will have their header downloaded by their requested time. Otherwise relay behavior is unchanged.

Very simple changes to MEV-Boost client and relay, and closes the vast majority of the sophistication gap. Proposers have one parameter to tune, which sophisticated proposers can heavily optimize but hopefully home stakers could be recommended reasonably-safe defaults and offered tools to help monitor and further optimize. Websockets or SSE would be useful, but that’s implementation details.

### MEV-Boost Deadlines

My first concern here is incentive compatibility for relays. If relays begin to [compete more heavily](https://youtu.be/kumD7njaCcU?si=UcXPc8_L_0-6DZ-S&t=750) with one another or we see relay-builders grow in dominance, there is a significant incentive for any of these imposed deadlines to be relaxed. The current 3s deadline for getHeader is our one real data point so far, which as far I know has remained uncontested, but in the current environment we 1) have relays that tend to cooperate on these topics and aren’t yet competing heavily on block value, and 2) are not yet feeling pressure from staking pools to loosen constraints. There is a good chance these will change.

My second concern (for options 2 and 3) is that the long length of the current deadlines (3s getHeader, 4s getPayload) are in some ways a good thing. I have helped a fair number of home stakers debug slots that were either missed or reverted to local block production. It’s often the case that under suboptimal network or hardware conditions, the block production pipeline starts late and progresses slowly. Tightening the bounds on access to MEV-Boost blocks means restricting unsophisticated actors moreso than the sophisticated ones.

---

**casparschwa** (2023-12-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> IMO this can be best achieved by attesters playing a mixed strategy about when to submit their attestation.

It’s an intuitive idea to ask validators to randomize their attestation deadline. However, there are problems with this:

- A validator is incentivized to vote correctly, not at some random point in time. In other words, it is not in their interest to (randomly) vote early, if they have not seen a valid block. They want to ensure to vote for the canonical block. But a block might show up after a random, early attestation deadline of a given validator and still become canonical. In such a scenario voting early would imply voting incorrectly.
- Even if all attesters randomized their attestation deadline, a proposer would be able to play timing games and even target to split the committee into different views. Committees are large enough to get a sufficiently well-behaved distribution of random attestation deadline times so that a proposer can reproducibly broadcast their block so that it splits the committee into different views, such that 40% hear it before their random attestation deadline (and so vote for the block) and 60% after their random attestation deadline (and so vote for the parent block).

So unfortunately I do not think that the idea of random attestation deadlines helps here.

---

**tripoli** (2023-12-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> (assuming relay enforcement via option 2, see below, or a relatively simple change to mev-boost that is already discussed).

Ah, okay this is fair, but then it puts more onus on unfunded relays and we already see bloXroute pretty [strongly opposed](https://twitter.com/uriklarman/status/1729529034218832012) to more duties. And then it opens the door for minority relays to quickly gain market share by not adhering to the socially enforced deadline etc.

---

**mkoeppelmann** (2023-12-07):

I suggest to you guys to model the game in a simplyfied way:

4 players

player 1 proses in the first round, then player 2, 3, 4, 1, 2,…

The proposer can propose either at:

t+0, t+4 or t+8

If they successfully propose the get a reward of FIX + MEV - the MEV part gets bigger if they choose t+4 or t+8 but it also depends on what the previous proposer had choosen. If the previous proposer missed it gets biggest.

Now attester can also choose between 3 strategies:

waiting till t+2, t+6, t+10

---

Their payouts depend on what the proposer picks and what other attester pick. We can modle the game here in such a way that there are 2 outcomes. Either at least 2/3 attester pick a time before the proposer - in this case the proposer gets the reward and the attester also get a small reward - the reward can be slightly higher for t+6 and t+10 to model that by playing t+2 you might still miss a somehow delayed t+0 submission (latency). However - if 2 or more attester pick a time before the proposer, the proposer will get nothing (orphaned block).

In this game the safest play as a proposer is to play t+0 and the safest play as an attester is to play t+10. However - this is not a stable equilibrium as, if all attester play t+10 it is best to play t+8 as a proposer. However, against a proposer player that always plays t+8 the attesters can simply all play t+2. Note that this move will benefit player n+1 (as she will get extra MEV from the orphaned block) but it takes at least another player to perform the “punishment” of player n (the proposer). In theory we could model something where n+1 pays (bribes) the other player with part of the extra rewards she gets to encourage the other players to help her - though likely this is not necessary. She can “reward” player n+2 by simply playing t+0 and not “stealing” from n+2 by choosing t+4 or t+8. This is similar as the [tit for tat](https://en.wikipedia.org/wiki/Tit_for_tat) strategy in a 2 player repeated prisoner dilemma.

---

In this game it should be clear that attester HAVE TO PLAY A MIXED strategy. An attester that always “chooses to fight” by playing t+2 will be beaten by any attester that also plays t+4 or t+10 once in a while. On the other hand an attest that “never fights back” and always play t+10 will get exploited by an proposer that will play t+8 before it is high turn and other attester will not help him defend if he never defends. They on the other hand can make it costly to “attack them” by defending with playing at least sometimes t+2 and t+4.

---

So I stick to my claim:

“A equilibrium will require mixed (timing) strategies of attesters”

(P.S: If someone finds time, tools like https://www.gambit-project.org/ allow to model those games and calculate equilibrium strategies)

---

**pavelya** (2023-12-07):

> A validator who intentionally delays their block proposal to capture more MEV is playing timing games. We define honest behavior as:

- Using mev-boost: Requesting a block header at t=0.
- Not using mev-boost: Requesting a block from the execution engine at t=0.

> Deliberate deviation from either strategy by modifying the client software is considered playing timing games under our definition. This is in contrast to “organic” latency in which a block proposal is later (e.g., from low-resource home staking).

That’s a tricky one. It looks like “honest” & “fast” < “honest” & “slow”; a protocol is not rewarding a professional honest validators, as additional latency generates more rewards. What if a node operator keeps requesting a block header at t=0, but instead locates nodes as far away as they can/using specific infrastructure setup, therefore intentionally delaying request, but on geo/infra level? That would be also a case of timing games, which is seems to be even worse in terms of stability of the network. To catch up with them, “fast” validators have to introduce software latencies, and by doing these they become “dishonest”. So what’s is honesty then? And what’s the line when a validator should step away from the competition?

As soon as:

> It is not obvious if a validator is intentionally playing timing games or unintentionally proposing a block late.

a validator that want to keep up with the rest cannot distinguish “dirty games” from “honest low-resource home staking”. Should a node operator give up the idea to introduce request delay and lose clients that will go to another operator with a weaker setup? The outcome for network health is not good either.

In general, removing a power from a validator to finish bid auctions could be a solution, in particular, setting a t=0 threshold on relays, but it’s hard to accomplish in short term, probably impossible in not-ePBS space. Therefore, I lean towards “missed slot penalties”, as a form of a damage control.

Also, it would be nice to make a more precise evaluation of the “zero-sum game” statement, it’s not straightforward (at least for me). To compare case of known auction time threshold (theoretical endgame when all are maxing out delays/some protocol cut-off) versus more realistic, when the auction end is stochastic, just like now. Some ideas/directions from the top of my head (would be awesome if some block builder could comment on that):

1. The growing value in bids can contain convergence to the true valuation of the block inclusion, meaning that more profits are going away to validators. Yes, it’s enough to add epsilon to the best bid value to win, however it might be feasible to add higher values given expectations of auction duration and constraints on bidding frequency (relays have limits), up to the values that result in 0 profits or negative profits (subsidized blocks). MEV rewards increase then attributed to profit redistribution.
2. Blockbuilder-searchers heterogeneity in order flow / information set / strategies / capacity, etc.

---

**quintuskilbourn** (2023-12-07):

Nice post.

Two related points:

1. Geographic centralisation forces: Incentives to be on time where “on-time” is defined relative to the speed of other nodes are incentives for geographic centralisation. E.g. if an attester gets rewarded for timely attestations and proposers are incentivised to submit blocks late so that the slowest x% of attesters are too slow to attest, attesters are incentivised to move to more central locations.
2. Current fee markets don’t adequately capture the cost of additional bandwidth usage. For example, in time of high volatility, it might make sense for builders to ignore some low-value transactions to reduce latency. We may not be there yet, but if latency competition continues then we eventually get to a point in which these optimisations matter.

---

**vladismint** (2023-12-08):

I think there’s no real point in discussing whether it’s possible to maintain a Focal point within the bounds of a validator’s described honest behavior. [We’re already past that point](https://twitter.com/nero_eth/status/1733016369715675358).

> Given the negative externalities of timing games and the short-lived room for increased profits, it’s worth exploring whether it’s possible to keep the honest strategy a Schelling point (in the colloquial meaning).

Thus, in assessing the situation and deciding on the strategy, the validator sees that the majority of operators are delaying GetHeader. However, as [@PavelYa](/u/pavelya) noted, the validator can’t discern whether other validators are doing this intentionally or not.

> a validator who wants to keep up with the rest cannot distinguish between “dirty games” and “honest low-resource home staking”. Should a node operator give up the idea of introducing request delays and lose clients who will go to another operator with a weaker setup? The outcome for network health is not good either.

In assessing the risks of decision-making, validators choose between losing clients now and a rather hypothetical issue of negative externalities. Given this, I think operators are not faced with the choice of whether to introduce delay or not, but which strategy to choose - profit maximisation / risk-averse strategy, or something in between.

I feel that the crypto community is quite small, and reputation is very important. Therefore, a strategy of profit maximization will be marginal. Due to this, I think we still have the opportunity to establish a Focal point within the limits of an acceptable healthy delay for the network.

Thinking about this from a validator’s perspective, we have shaped the vision of a good validator based on following rules:

1/ We should allow our users to choose whether they want to use the GetHeader delay or not. This way, we won’t lose users, but we will significantly reduce the use of delays since many users are very risk averse and will not engage in timing games.

2/ We must monitor missed blocks. If misses increase, the delay is reduced /turned off.

3/ We should be transparent about whether we are playing timing games or not. This will allow the community to control points one and two.

---

**barnabe** (2023-12-08):

Hey Martin!

![](https://ethresear.ch/user_avatar/ethresear.ch/mkoeppelmann/48/417_2.png) mkoeppelmann:

> However, against a proposer player that always plays t+8 the attesters can simply all play t+2.

This is true but then (Proposer plays t+8, Attesters play t+10) is still a Nash equilibrium, if *all* attesters punish by deviating to t+2 sure, the best response of the Proposer is to play t+0, but the Nash equilibrium condition is about unilateral deviations, not coordinated. It’s possible to organise coordinated deviations with a mediator or a smart contract, but as described, the outcome (P+8, A+10) remains a Nash equilibrium. In our situation unilateral deviations make more sense to me given that players cannot commit to actions, even if they organised with smart contracts an outside party could not ascertain that an attester is playing an action over another, including mixed strategies (off-chain monitoring is maybe possible, [though the randomness complicates it](https://twitter.com/barnabemonnot/status/1728821054989353035)).

---

Some more thoughts on the game: Let’s look at the profile (P+0, {1/3 A+2, 1/3 A+6, 1/3 A+10}), where all attesters randomise perfectly between the three release times. The proposer needs only to receive 40% of attestations on their block, so they can safely play P+4 and get 2/3 of the attesting weight voting for their block with high probability when the number of attesters is large. The main issue is that an attester playing a randomised strategy can always get the same payoff or better by giving more weight to later release times. So for instance, attesters could shift in an uncoordinated fashion to the strategy {1/2 A+6, 1/2 A+10}, in this case the proposer’s best response remains P+4, but given P+4 attesters would now be indifferent between playing {1/2 A+6, 1/2 A+10} or A+10. Of course once enough attesting weight has shifted to later release times the proposer’s best response becomes P+8, and we arrive at the (P+8, A+10) equilibrium.

I don’t think this issue is due to the discretised model you suggested, if the proposer could choose any release time in the interval [0,12], and so could attesters, a mixed attester strategy choosing uniformly between 0 and 12 means the proposer can target the 60-th quantile as their release time, to obtain more than 40% of attestations on their block. Attesters would want to best respond to this by abandoning the uniform strategy and shift to later release times.

Back to the discretised model, even in a (no-latency) world where for some reason we need the proposer to gather 100% of the votes, (P+0, {1/3 A+2, 1/3 A+6, 1/3 A+10}) is an equilibrium (no one has a deviation that gives them *strictly* better payoffs), but so is (P+0, A+2), as well as (P+4, A+6) or (P+8, A+10). Many profiles in between are equilibria too, such as (P+0, 1/2 {A+2} + 1/2 {A+6}), where half of the attesters play A+2 as a pure strategy and half play A+6. In this case, attesters are indifferent between releasing early or later, so it is a not a strictly profitable deviation to move from A+2 to A+6, but it’s the same payoff. This holds true until the last attester moves from A+2 to A+6: given P+0, this does not change the attester’s payoff, but the new profile, (P+0, A+6) is no longer an equilibrium, proposer now wants to play P+4 and arrive at the (P+4, A+6) equilibrium.

---

Overall it seems to me that the conditions you want for the mixed strategy to hold as an equilibrium are too strong, given that many individual deviations exist for attesters which may not improve their payoffs but gives them a bit more room to breathe, especially if they are made to be “suckers” by the proposer targeting a 40% vote. If they give themselves a bit more slack, the proposer can use that slack to their advantage, and without coordinating with each other again, attesters cannot unilaterally bring the proposer’s release time back to 0 to begin with.

---

**vshvsh** (2023-12-11):

My two cents here is if short-term solution is made in a way that mimics the most likely ePBS design, with a shortcut being that it needs some trust to function, it can be a good proving ground for ePBS designs. Pretty much like mev-boost is a proving ground for ePBS based on builder auctions. It’s good if we can do a stopgag that can be with time and effort replicated into cold hard consensus code.

---

**Julian** (2023-12-12):

Enforcing timeliness of proposers using relays seems like a very crude solution that can have some irreversible effects.

As mentioned in the post, using relays to enforce timeliness is not incentive-compatible and relies on social consensus. Although it will decrease the amount of timing games played in the short run, it will lead to vertical integration in the medium to long run.

To me, the consequences of vertical integration between proposers and builders seem irreversible. Operating both of these entities will always be more profitable than operating both separately. The current PBS ecosystem aims to decrease the difference between these two alternatives such that the investment of vertical integration is very small.

If we enforce timeliness with relays, the incentive to invest in vertical integration increases and we actually expect this to happen. When this happens, there is no incentive to ever revert this vertical integration.

Is it worth it to have permanent vertical integration to prevent timing games in the short run, while putting pressure on social consensus?

---

**tripoli** (2023-12-12):

Even if we don’t see vertical integration of proposers and builders, using relays to enforce timing would also encourage colocation of proposer sets with relays. Unless the geographic distribution of relays improves this would add meaningful regulatory tail risk.

---

**sachayves** (2023-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/casparschwa/48/3001_2.png) casparschwa:

> #### Option 1: Relay rejecting new bids after t=0
>
>
>
> Description: The relay can reject any bids submitted by builders once the slot has begun (at t=0). This removes any incentive for the proposer to delay their call to getHeader because the value of the bid will no longer increase.

[@tripoli](/u/tripoli) not necessarily. e.g. schelling point could be for relays to reject new bids

---

**sachayves** (2023-12-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/julian/48/10541_2.png) Julian:

> Is it worth it to have permanent vertical integration to prevent timing games in the short run, while putting pressure on social consensus?

if the endgame is attester-proposer separation, does this change your point of view in any way?

---

**Julian** (2023-12-14):

If we were to have attester-proposer separation in the way just now proposed by Justin Drake at CCE, I think we don’t need to worry as much about proposer timing games. We still want a credibly neutral validator set so we don’t want vertical integration for e.g. geographical decentralization. I don’t think APS changes a lot about my point of view.

