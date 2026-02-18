---
source: magicians
topic_id: 24616
title: "EIP-7782: The case for 2x shorter slot times in Glamsterdam"
author: barnabe
date: "2025-06-20"
category: EIPs
tags: [glamsterdam]
url: https://ethereum-magicians.org/t/eip-7782-the-case-for-2x-shorter-slot-times-in-glamsterdam/24616
views: 1697
likes: 17
posts_count: 5
---

# EIP-7782: The case for 2x shorter slot times in Glamsterdam

*Authors:* [@benaadams](/u/benaadams), [@dankrad](/u/dankrad), Julian Ma and [@barnabe](/u/barnabe)

---

## Summary (ELI5)

Shorter slot times make Ethereum a better confirmation engine, which is arguably one of its main value propositions for apps and rollups settling on Ethereum L1. Everyone benefits directly:

- Users on L1 have reduced transaction inclusion latency and better UX, with improved censorship-resistance from having more proposers per second,
- Apps enjoy more frequent triggers, leading to reduced staleness of onchain data, and relatively less value leaking away from users, i.e., lower fees, as a result,
- Block construction markets (builders, and in the future provers) offer more frequent opportunities to compete for smaller chunks of work, leading to healthier markets,
- Interoperability protocols receive L1 finality quicker, as well as quicker confirmations,
- Stakers have lower reward variability, reducing incentives to pool for the purpose of reducing risk,
- Node operators receive improved load management, in particular bandwidth, as smaller blocks are disseminated more frequently, lowering resource peaks.

We propose targeting **6-second slot times** in Glamsterdam, as originally proposed in [EIP-7782](https://eips.ethereum.org/EIPS/eip-7782).

## Detailed Justification

We detail each of the points above in this section.

### Faster inclusion latency and censorship-resistance

Halving the slot time leads to faster inclusion for users, improving the UX with a more responsive chain. This means wallets can display fresher data following transaction inclusion and update of the chain head.

In particular, censored transactions also receive shorter time-to-inclusion, as twice as many proposers are sampled per unit of time. Note that while this effect is linear (2x halving of slot time also halves by 2x time-to-inclusion, all else equal), this effect remains small relative to FOCIL with 16 includers, which would then decrease time-to-inclusion 16x.

### Better On-chain Exchanges

Exchanges on Ethereum are suboptimal because prices only update every slot, today 12 seconds. Shorter slots lead to more efficient exchanges as prices can be updated more frequently. Users therefore enjoy lower trading fees and Ethereum mainnet will attract deeper liquidity and more users, which has many positive side effects.

Arbitrage on Ethereum decentralized exchanges is risk-free profits extracted from the system by buying low on a decentralized exchange and selling high on a centralized exchange, or vice versa. [Milionis, Moallemi and Roughgarden (2023)](https://moallemi.com/ciamac/papers/lvr-fee-model-2023.pdf) find that arbitrage profits increase with block times, keeping the amount of liquidity constant. The first effect of faster slots will be that existing liquidity providers lose less value to arbitrageurs.

The second effect will be that more liquidity is deposited into automated market makers (AMMs), since arbitrage costs will decrease and trading fee revenue stays the same. This added liquidity attracts more traders which in turn again attracts more liquidity, indicating a flywheel effect [(Ma and Crapis, 2024)](https://arxiv.org/abs/2402.18256). The improved user experience of faster slots also attracts more traders, leading to more liquidity as well. Faster slots leads to more liquidity, which means lower trading fees for users and increased network effects for Ethereum.

Some new AMM designs, like [CoW Swap’s design](https://cow.fi/cow-amm), based on [Canidio and Fritsch (2025](https://arxiv.org/abs/2307.02074)), reduce arbitrage losses regardless of the slot time. Still, faster slots may lead to more efficient exchanges since arbitrageurs can settle their positions faster, meaning arbitrageurs take less [risk on the tokens they hold](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1411943). So even for future AMMs, faster slots lead to better on-chain exchanges.

### Healthier block construction markets

This point may be more theoretical than relevant in practice. However, one could argue that competition is favored in settings where bidders have more opportunities to participate in auctions where the value of the item is lower. In particular, less capital may be required to participate in some of the PBS block auctions, all else being equal.

For proof markets, the work can be heavily parallelised, so a single logical prover could be obtaining subproofs from many other provers. Still, reducing the slot time means offering more opportunities per unit of time to compete for the right to provide the proof of a block.

### Improved interoperability

Rollup settlement on Ethereum happens when the canonical bridge contract on L1 is convinced that the state provided to it by the rollup results from the valid transition of transactions contained in a posted batch of data. For optimistic rollups, this happens after the usual 7-day window, during which time the posted state can be challenged. For pessimistic rollups, this happens after the validity proof is posted, usually along with the batch of data itself.

However, to external parties, the rollup state may be derived by oneself whenever the batch of data is *finalized* on mainnet. Past this point, there is the strongest guarantee that the ordering derived from the data contained in Ethereum L1 blocks will not be reverted. While this is the strongest form of confirmation, there is a weaker form, so-called “[safe confirmation](https://arxiv.org/abs/2405.00549)”, that also provides fairly high guarantees, once the block containing rollup data is posted and voted on by sufficiently many attesters. For even more sophisticated participants, it may even be enough to see the rollup data included in a block which is itself just included as proposal to continue the chain. Finally, for based rollups which reorg with the L1, 6-second slots means their own clock moves twice as fast.

All three forms of confirmation—L1 finality, safe confirmation and block inclusion—are improved with shorter slot times, as they are provided faster and are thus more immediately actionable by protocols using this signal to trigger actions on domains other than the L1. This holds in particular for interoperability protocols, bridging in and out of L1, using e.g., intents. See [this clip](https://www.youtube.com/live/m5HFO4DYckQ?si=OpzXxtpfcbWS1zqO&t=3000) by Matt Rice from Across in the Protocol Research Call #1 for more background, and a comparison of various proposals (faster finality, shorter slots, and shorter rollup withdrawal windows).

### Lower staking reward variability

The change to shorter slot times should not change the aggregate issuance paid out to stakers over the course of their operations. However, stakers would receive smaller rewards more frequently, including block rewards, which lowers the variability of the rewards overall. Lower variance removes some incentive to pool funds, a better setup for solo stakers and home operators.

### Better resource utilization

With more frequent, smaller messages, peak demands on resources (e.g., bandwidth) are reduced, spreading the load over time. Maintaining existing p2p network maximum smooths bandwidth usage over time, avoiding peak-load spikes and preserving accessibility for nodes with diverse bandwidth capacities.

While peaks are lowered, there is some bandwidth increase from the more frequent voting rounds. These messages (roughly the size of the beacon block, minus the execution payload) [tend to be small](https://ethresear.ch/t/big-blocks-blobs-and-reorgs/19674) compared to the execution payload itself, especially including blobs.

### Comparison with other solutions

Obtaining shorter slot times is often weighed against scaling the L1. With shorter slots, the gas throughput would remain the same, all else being equal. However, there is some evidence that the effects of scaling may be less than linear, see e.g., [MEV and the limits of scaling](https://writings.flashbots.net/mev-and-the-limits-of-scaling). Note that this effect is likely much less pronounced on mainnet, where the MEV markets are mature and onchain searching is limited. We also have [incidental evidence](https://x.com/mteamisloading/status/1925921633497182352) that shorter slots may be more in demand than scaling the L1 by 3x.

Out-of-protocol preconfirmations may also be an alternative to shorter slots/faster finality. There too, [incidental evidence](https://x.com/dankrad/status/1911406384932937910) shows a preference for in-protocol improvements to the confirmation engine, rather than out-of-protocol. Preconfirmations would provide UX benefits to users, but may not directly offer many of the benefits spelled out above.

## Technical Readiness

We follow the proposal of EIP-7782 for the slot duration:

- Change block proposal subslot from 4 seconds to 3 seconds.
- Change attestation proposal subslot duration from 4 seconds to 1.5 seconds.
- Change aggregation proposal subslot duration from 4 seconds to 1.5 seconds.

Shorterning the subslots means there is less time to perform each duty. With a constant throughput, we should expect blocks to be half the size (in gas), but there is possibly fixed overheads at the start of the slot that require attention. In particular, some clients start building at 0 seconds into the slot, rather than sending the block at 0 seconds, and so this building time may consume some of the 3-second budget. Note however that with constant throughput, there is an actually greater relative share of time for block production and propagation (3 seconds out of a 6-second slot time, instead of 4 seconds out of a 12-second slot time).

According to CL core developers (see [Eth R&D thread](https://discord.com/channels/595666850260713488/1382065239360802826)), the main technical hurdle consists in implementing conditional logic for slot times in existing clients and infrastructure (e.g., explorers). The chain has run with 12-second slot times until now, and it would need to keep this constant when replaying blocks before the transition to 6-second slot times. Further scoping is required to understand the magnitude of the changes to client code, and are not fully available at the time of publication of this proposal; we hope to motivate further exploration given the value of this proposal, and encourage core developers to reach out following its publication.

While this is not an apples-to-apples comparison given the validator set size differences, we observe that [Gnosis chain](https://gnosis.blockscout.com/) runs today at slot times of 5 seconds, and Nethermind [Perfnets](https://teragas.wtf/) run at slot times of 4 seconds, with an otherwise equal architecture to Ethereum mainnet. We note that in the case of Gnosis chain, [supported clients](https://docs.gnosischain.com/node/architecture) (a subset of the available clients for Ethereum mainnet) were required to move to accounting for time in milliseconds rather than seconds, to support divisibility.

## Security & Open Questions

The main risk of shorter slot times consists in raising the bar for effective participation in the validator set. Slower, less well-connected validators could find their performance affected. However, we estimate that restructuring the slot time judiciously would not damage participation, as long as gas and blob throughputs are maintained to their current values. We intend to study further the possible prevalence of one-block reorgs from late blocks under a shorter slot regime, as well as the propagation of attestations and aggregates.

If gas and blob throughputs were to be increased, research and engineering would need to be performed, independently of the slot time value. It would be worth thinking holistically about the slot in the context of proposals such as [delayed execution](https://ethereum-magicians.org/t/eip-7886-delayed-execution-the-case-for-glamsterdam/24500) (EIP-7886) or [ePBS](https://ethereum-magicians.org/t/eip-7732-the-case-for-inclusion-in-glamsterdam/24306) (EIP-7732), but we stress that shortening slot times has independent benefits and may be realized independently.

A study ought to be performed to understand whether any contracts rely on the fixed assumption of 12-second slot times, rather than a variable assumption. Variable assumptions were prevalent under Proof-of-Work, as the slot time was variable, so it is possible that the fixed assumption pattern is not very widespread. To future-proof further slot time reductions, it should be investigated whether to deploy a current slot precompile in the same hard fork.

To go further than the proposed 6-second slot time target, we would likely need to fundamentally change the consensus mechanism. [3-slot-finality](https://arxiv.org/abs/2411.00558) is a current contender for such a mechanism, but it needs to be decided whether to cap the validator set or opt for a rotation mechanism in order to achieve smaller active validator set sizes.

## Replies

**Giulio2002** (2025-06-20):

I do not think we can do ePBS/DE + 6s slots in the same hardfork.

maybe we can just do a simple slot restructuring and decrease slot time to 6s?

also out of curiosity: do we have data on how much you can restructure the slot? I think it would be nice if we could have a 4s/1s/1s split to keep the time required to build the block the same.

---

**catwith1hat** (2025-06-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/barnabe/48/15482_2.png) barnabe:

> Change attestation proposal subslot duration from 4 seconds to 1.5 seconds.

Do you have any metrics to demonstrate that this is a safe change and doesn’t hurt the participation of not so well connected home stakers?

---

**msoos** (2025-06-25):

Injecting some physics into this discussion: a cable half-way around the globe has a minimum latency of 100 ms, 200 ms round-trip (20,000 km distance / 200,000 km/s signal speed [1]) - that’s the physical, lower limit. 6 seconds affords us <30 such round-trips, as there are routers on the way, and one needs to also process the packets and respond accordingly.

[1] Yes, it’s not ~3x10^8 m/s but ~2x10^8 m/s in glass, see: [Speed of light - Wikipedia](https://en.wikipedia.org/wiki/Speed_of_light)

---

**rolfyone** (2025-06-27):

For me there’s a clearer path to success for shorter slot times once we fully understand it.

We need to look at the flow on effects, and move to define all of the second order changes (eg. issuance curve / gas potential changes).

We also need to define in the first instance what the change is (eg. consensus-spec has no PR yet), it’s wide reaching at the spec level including fork choice.

A spec change would allow more implementation teams to get an appreciation for their precise changes, and start finding their tech-debt that they’ve accrued since pre-phase0 due to this previously being a ‘constant’.

I am 100% on board with changing this as soon as it’s ready to be changed, but i think that slot restructuring gives us more space to consider this change and maybe choose a different actual new slot time.

Re. shipping this AND something like ePBS in the same timeframe, I’d prefer to not have that many testing things in flight. I do think it’d cause significant delivery delays and ultimately probably mean delivering ePBS (or restructuring, but my pref is likely ePBS at this point) AND shorter slot times in a similar end point. Concretely, i think if it was 2 forks separate, or 1 fork combined, the end date would be similar to get to a world where we had both shorter slot times AND restructuring.

tl/dr; i can’t see this being actually ‘ready’ to implement in a Glamsterdam timeframe unless Glamsterdam is variable time.

