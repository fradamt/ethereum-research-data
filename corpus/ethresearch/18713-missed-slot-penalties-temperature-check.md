---
source: ethresearch
topic_id: 18713
title: Missed Slot Penalties [Temperature Check]
author: MaxResnick
date: "2024-02-18"
category: Consensus
tags: [mev]
url: https://ethresear.ch/t/missed-slot-penalties-temperature-check/18713
views: 2267
likes: 27
posts_count: 13
---

# Missed Slot Penalties [Temperature Check]

Recently, we saw 9 missed slots caused by an optimistic relay bug. Missed slots aren’t the end of the world but they do result in economic loss for the network. Due to the burn implemented in 1559 the economic penalty that the proposer incurs for missing a slot is about an order of magnitude lower than it would be without the burn because transaction fees are dramatically reduced. I think we should implement a missed slot penalty of 15m * base fee so that we can realign the economic incentives for the proposer with the overall social welfare of the network.

This change would be a relatively simple change to the slashing conditions that would both decrease the effect of timing games and increase penalties for builders and optimistic relays that cause missed slots.

I think we should aim to include this change in Electra.

Wanted to see if there are any objections to this other than the obvious solo staker argument. My response to the solo staker argument is that solo staker or not it still makes sense to align public and private incentives. If the transaction fee mechanism we were using didn’t have the burn and incentives were properly aligned, I don’t think anyone would argue that we need to lower the economic penalty for missing a slot to preserve the long tail of solo stakers.

## Replies

**potuz** (2024-02-18):

I support a penalty for missed slots, just two comments:

- “slashing conditions” have nothing to do with this and shouldn’t be involved
- “15m * base_fee”: I assume you are referring to base fee per gas to penalize for the average burn. This penalty would be applied in the CL that does not have access to this, it should be measured in terms of the base_reward instead to make it in line with other penalties/rewards in the CL. Although these don’t change with gas price

---

**tripoli** (2024-02-18):

Missed slot penalties going to be needed eventually and I think sooner is better because they’ll kneecap timing games. I would personally like to see someone take an empirical look at the data and see if there are any causes of missed blocks that would help to inform the magnitude of the penalty.

![](https://ethresear.ch/user_avatar/ethresear.ch/maxresnick/48/13097_2.png) MaxResnick:

> a missed slot penalty of 15m * base fee

Presumably this would be tied to 1/2 × gas_limit. I don’t think it would be a meaningful factor, but maybe it’s worth discussing whether it makes proposers less likely to raise the gas limit. Increasing their bandwidth, state growth, missed slots, and the penalty for those missed slots all for maybe a small bump in MEV doesn’t seem easy to sell.

---

**MaxResnick** (2024-02-18):

Hmm good point that the CL doesn’t have access to the base fee. It would be ideal not to enshrine a penalty for missing a slot that is too high or too low in the long run (i.e. doesn’t depend on gas price). Perhaps this is an acceptable tradeoff tho.

---

**MicahZoltu** (2024-02-19):

I like this proposal with the originally proposed penalty.  I dislike it if we try to apply some other arbitrary penalty instead.

`gas_target * base_fee_per_gas` of the missed block is the “appropriate” penalty to apply.  It is a reasonably good proxy for the economic activity that would have happened but didn’t because the proposer missed, and thus it should do a reasonably good job of aligning incentives.  Essentially, it is the approximate cost they would have had to pay to buy out all of the block space in the block they missed.

While the CL doesn’t have direct access to this information, can’t they get it from the EL over the execution API pretty easily?  The EL definitely knows the `gas_target` and `base_fee` of the block immediately prior to the missed block, so it feels like this is just a matter of getting the information from the attached EL (similarly to how I believe we get `block_hash` from the EL).

---

**potuz** (2024-02-19):

Since the penalization is on the CL and this is a consensus issue, it cannot be simply obtained from the engine API by a call to the EL, both machines do not share a common state. The easiest way of implementing this would be to either obtain it from the EL as above with an API call and then put it in the CL state, or by interpreting the corresponding field in the `ExecutionPayload` and register it in the CL state. Both of these things are bad precedent in that it crosses a boundary that we want to keep lean.

While I sympathize with the idea that the gas burn would be a more accurate penalty. I think that simply penalizing the full reward that the block would have obtained from the CL network (we can compute this to be a full block filled with right attestations) should be enough.

Regardless of what penalty is imposed, this number will only factor in the statistics of timing games, if one meassures milliseconds in terms of money, whatever penalty you impose, it will be converted in number of milliseconds earlier that you need to submit your block.

---

**MicahZoltu** (2024-02-20):

Normally I agree that increasing complexity should be avoided at nearly all costs.  However, one of the few thing that trumps that for me with Ethereum is sound mechanism design/incentives, and right now the design is not sound and using some arbitrary penalty is also not a sound solution.

As an example, I think the CL block reward right now is something like 0.01 ETH, but the burned fees are ~0.5 ETH.  If we just did negative block reward, this would not be the right order of magnitude of punishment to appropriately align incentives.  The burn rate can be as low as 0.000000000105 ETH, and we have seen prices that would put the burn rate as high as 3 ETH, with no hard upper limit aside from demand.  Anything that is just a fixed value will not accurately represent the cost to the network that is incurred by missing blocks.

The reason we should make this accurate and not smoothed over time or a fixed penalty is because we want to encourage people to “try harder” during times of high economic activity and “slack off” during times of low economic activity.  Normally this doesn’t matter, but people will do maintenance on their nodes and we want to encourage them to do so during “off-peak” hours rather than during peak hours, which means we should penalize based on the real cost to the network so they are encouraged to do maintenance when demand is low.

---

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> Since the penalization is on the CL and this is a consensus issue, it cannot be simply obtained from the engine API by a call to the EL, both machines do not share a common state. The easiest way of implementing this would be to either obtain it from the EL as above with an API call and then put it in the CL state, or by interpreting the corresponding field in the ExecutionPayload and register it in the CL state. Both of these things are bad precedent in that it crosses a boundary that we want to keep lean.

Why does this need to be in CL state?  IIUC, the CL currently comes to consensus on state *derived* from the EL, such as the blockhash, so why couldn’t the CL similarly come to consensus on state *derived* from block header values for `gas_target` and `base_fee_per_gas`?  In this case, the thing the CL would come to consensus on (and presumably store somewhere) would be `missed_block_penalty`.

![](https://ethresear.ch/user_avatar/ethresear.ch/potuz/48/11413_2.png) potuz:

> Regardless of what penalty is imposed, this number will only factor in the statistics of timing games, if one meassures milliseconds in terms of money, whatever penalty you impose, it will be converted in number of milliseconds earlier that you need to submit your block.

While true if you look at things from a very zoomed in perspective, this alignment ensures that the people incurring the cost on the network (proposers missing blocks) are penalized in accordance with the cost they imposed, which varies over time.  They will still play their games, but their games will accurately account for the cost they are imposing rather than being able to ignore it as an externality.

Essentially, we should strive to internalize all externalities we can, and this is one we definitely can internalize.

---

**potuz** (2024-02-20):

> Why does this need to be in CL state? IIUC, the CL currently comes to consensus on state derived from the EL, such as the blockhash, so why couldn’t the CL similarly come to consensus on state derived from block header values for gas_target and base_fee_per_gas? In this case, the thing the CL would come to consensus on (and presumably store somewhere) would be missed_block_penalty.

We technically can break the invariant that the payload is a set of raw bytes that we don’t read and take the base fee from there. But that boundary of keeping the EL and the CL interdependence to a minimum is there for a reason. Regardless, any such change breaks the way we currently sync blocks. The CL does not store the EL payload to avoid duplication on disk. When you start a node that has an existing DB it will perform some state transitions out of blocks that were already on db. Such a change would require to request the full payload from the EL to be able to validate the state transition.

There’s a substantial difference from going to simply an `assert payload.is_valid` in state transition, to actually performing a computation based on the payload.

Any reasonable implementation of this will move the base fee to the CL state I believe.

---

**fradamt** (2024-02-20):

I don’t think it’s feasible to do an uncapped `15m * basefee_per_gas` penalty, given the current state of staking. Stakers right now assume that being inactive for small periods of time cannot result in heavy losses, and that even long periods of inactivity are normally almost harmless, unless the network is failing to finalize and is undergoing an inactivity leak. On the other hand, the average burn since the merge has been about ~0.5 ETH, with peaks of 16 ETH, and over 200 ETH if we go back to the 1559 fork. Even just in the last 30 days, there have been blocks with over 10 ETH burnt.

I disagree with the argument that it’s equivalent to if we didn’t have the burn, because this would just be the opportunity cost of missing a slot. Missing a slot once in a while might make you less profitable but it wouldn’t threaten to erase your stake.

Assuming I am correct that this is not something we can plausibly implement right now, and that we would instead need to cap the penalty, e.g. to 0.1 ETH or something, I think it would make more sense to completely ignore `basefee_per_gas` and make the penalty fixed.

---

**MicahZoltu** (2024-02-20):

If we aren’t going to try to align incentives on this, then why bother doing anything on this front?  As [@potuz](/u/potuz) said, just adding flat penalties for things will adjust the timing game calculus slightly, but it won’t align incentives between stakers and the externalities of their decisions.  It will just make people add a handful of milliseconds to how long they wait.

With a flat fee, we should expect people to *increase* their delay in times of high demand because priority fees would be high and thus the profitability of building a bigger block increases.  This is the exact opposite of the effect we want, which is that during times of high demand we want them to become *more* aggressive at getting blocks out to the network ASAP.

If we were to make a change like this we should give a huge amount of warning to stakers and do everything in our power to alert them of the change.  However, I am very much in favor of aligning incentives even if it drives some people away from staking (in fact, that is part of why I favor it).  Staking on Ethereum isn’t a money printer, it is a job that requires you put in effort.  If we lose too many stakers because doing their job is hard and risky, we can increase the per-staker ROI curve to attract more.  My guess is that on net it will cost the network less money to have incentives properly aligned, even if we have to pay 25% APR to stakers for them to be willing to take on the risk, because we’ll have less stakers and the stakers we do have will be more robust and reliable.

---

**fradamt** (2024-02-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If we aren’t going to try to align incentives on this, then why bother doing anything on this front? As @potuz said, just adding flat penalties for things will adjust the timing game calculus slightly, but it won’t align incentives between stakers and the externalities of their decisions. It will just make people add a handful of milliseconds to how long they wait.

At current levels of MEV (which have been stable for quite a while) timing game incentives are quite weak, it wouldn’t take much to make a meaningful difference. Another solution in this direction are [retroactive proposer rewards](https://ethresear.ch/t/timing-games-implications-and-possible-mitigations/17612#retroactive-proposer-rewards-29).

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> With a flat fee, we should expect people to increase their delay in times of high demand because priority fees would be high and thus the profitability of building a bigger block increases. This is the exact opposite of the effect we want, which is that during times of high demand we want them to become more aggressive at getting blocks out to the network ASAP.

On the other hand, the opportunity cost of losing the block becomes higher when priority fees are high.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If we were to make a change like this we should give a huge amount of warning to stakers and do everything in our power to alert them of the change. However, I am very much in favor of aligning incentives even if it drives some people away from staking (in fact, that is part of why I favor it). Staking on Ethereum isn’t a money printer, it is a job that requires you put in effort. If we lose too many stakers because doing their job is hard and risky, we can increase the per-staker ROI curve to attract more. My guess is that on net it will cost the network less money to have incentives properly aligned, even if we have to pay 25% APR to stakers for them to be willing to take on the risk, because we’ll have less stakers and the stakers we do have will be more robust and reliable.

The issue isn’t losing too many stakers (we likely wouldn’t, because for a pool this wouldn’t change things too much), it’s that we would primarily lose solo stakers. How many I don’t know, but it’s a pretty dramatic change in the potential downside of staking and I don’t think we can just hand-wave the issue of solo stakers away.

If the execution rights were to be auctioned off instead of being given to stakers (through some form of slot auctions, e.g. execution tickets), I think this proposal would likely be perfectly ok as is.

---

**MaxResnick** (2024-02-21):

Thanks for all the feedback, everyone. I agree with [@MicahZoltu](/u/micahzoltu) that getting the ‘right’ economic penalty is critical here even if it means blurring the lines between consensus and execution client a little bit.

I will note that even if the penalty is wrong, it would (in theory) reduce the number of missed slots induced by timing games. the few ms improvements that [@potuz](/u/potuz) alluded to would lead to a smaller tail of the block arrival distribution arriving after the deadline.

---

**Pintail** (2024-03-06):

Rather than a missed slot penalty, I would advocate for a proposer fee which always applies and effectively neutralises the CL reward for proposers (assuming they successfully propose a block containing all attestations). My reasoning is that this would significantly reduce the variability in reward which comes from the Poisson randomness of block proposals (which affects small stakers much more than large ones). But a proposer fee would also have the side effect of applying a modest penalty in the case of missed proposals.

Tying the penalty to missed slots only using the basefee doesn’t make sense to me. The idea that an unlucky proposer suffering network latency at a time of high basefee could be massively penalised doesn’t seem right. If missed slots are serious problem then we should instead be moving to a system of multiple proposers to ensure no single point of failure.

