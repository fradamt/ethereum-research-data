---
source: ethresearch
topic_id: 13485
title: "Model: Pool Centralization From MEV"
author: pmcgoohan
date: "2022-08-23"
category: Economics
tags: [proposer-builder-separation]
url: https://ethresear.ch/t/model-pool-centralization-from-mev/13485
views: 4466
likes: 9
posts_count: 20
---

# Model: Pool Centralization From MEV

# Model: Pool Centralization From MEV

## Summary

One of the main justifications given by [@vbuterin](/u/vbuterin) and others for in-protocol PBS is [this](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs):

> “A pool that is 10x bigger will have 10x more opportunities to extract MEV but it will also be able to spend much more effort on making proprietary optimizations to extract more out of each opportunity”.

This is an early version of a model to find out how much of a problem this kind of validator centralization is, and to find out whether MEV auctions are an effective solution.

It’s a work in progress and a call for peer review, not a final publication. I’m looking for input on any problems with my logic, model, assumptions, parameters etc. Thanks all!

## Model

Run/edit the model code in your browser: [Ethereum Validator Centralization Model | C# Online Compiler | .NET Fiddle](https://dotnetfiddle.net/DRPUAd)

Here are my results: [ValidatorCentralizationResults - Google Sheets](https://docs.google.com/spreadsheets/d/1vQ8dsBoyj8TD5fGR7wd3Is_JJ7aDzktKJcQY7x7JSaE/edit?usp=sharing)

First Thoughts:

1. Validator centralization from MEV is low in all cases, even over 50 years
2. MEV auctions (eg: MEV-Boost/PBS) make it worse
3. Toxic MEV mitigation makes it better
4. Builder/Order flow centralization (which is incentivized by MEV auctions without toxic MEV mitigation) makes things much worse

[![Validator Centralization Model Results](https://ethresear.ch/uploads/default/optimized/2X/a/aa2cdc02f0c88d1925d1cd0f0c4dc657b4ee2c0b_2_690x421.png)Validator Centralization Model Results880×538 25.2 KB](https://ethresear.ch/uploads/default/aa2cdc02f0c88d1925d1cd0f0c4dc657b4ee2c0b)

- If a pool is significantly better at extracting than anyone else, they will earn relatively more to reinvest in staking when using mev auctions than without, which worsens validator centralization
- Builder centralization is incentivized by mev auctions, especially private order flow from users trying to avoid toxic mev, which worsens centralization further (ie: builder centralization causes validator centralization).
- I’m aware that the builder centralization modeling is inadequate, I just added it as a fixed amount of mev for now- actually there will be a feedback effect.

## Description

- Initial pool sizes are taken from current figures (see poolStartingAllocations  0.3, 0.15, 0.14, 0.09, 0.06, 0.03, 0.23)
- The mev extraction efficiency for each pool is estimated based on pool size (1, 0.9, 0.85, 0.8, 0.75, 0.75, 0.7), and doesn’t drop below 70% due to MEV extraction still being possible via GPA even on gas price only validators (poolMevEfficiency, 1 = all possible mev extracted, 0 = no mev extracted)
- Select preset tests to run (test = 0,1,...)
- Estimated mev per block is taken from MEV in Eth2 by Alex Obadia
- Staking rewards per block are estimated from Beacon Chain Validator Rewards by pintail
- Define whether you want to use mev auctions or not (useMevAuctions)
- Define how much mev has been mitigated as a percentage (mevMitigated, 1 = no mev mitigated, 0.5 = half mev mitigated). It is set to 40% in the mitigation sim to represent preventing sandwich attacks via threshold encryption of the mempool
- Iterates blocks over a 50 year period choosing block producers proportional to their stake
- Adds staking rewards and mev per block:

No mev auctions: the producer extracts mev at their own level of efficiency
- With mev auctions: the producer gets the winning bid, the extractor wins the difference between the mev they can extract and the nearest competitor bid

Assumes all rewards and mev are reinvested into staking

## Replies

**pmcgoohan** (2022-08-23):

UPDATE:

Here’s what I think has been missed by the PBS designers…

PBS does what it claims if the dominant builder is not a pool, but it fails catastrophically if it is (ie: does the opposite and worsens centralization).

Trouble is, pools want to be the dominant builder because it increases their market share over competing pools- and they have the resources to do so and latency advantages to help them.

You can’t deny this is their aim, because it is this that PBS was [designed to address](https://ethresear.ch/t/proposer-block-builder-separation-friendly-fee-market-designs).

So it is far from clear that PBS will have a positive impact on validator decentralization.

*(To model the scenario where MEV is not extracted by the pools, which is what Flashbots hope will happen, you can use these parameters to add a dominant mev extractor that is not a pool.*

`poolStartingAllocations = new double[] { 0.3, 0.15, 0.14, 0.09, 0.06, 0.03, 0.23, 0.0001 }; `

`poolMevEfficiency = new double[] { 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 1 };`*)*

---

**MicahZoltu** (2022-08-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Here’s what I think has been missed by the PBS designers…
>
>
> PBS does what it claims if the dominant builder is not a pool, but it fails catastrophically if it is (ie: does the opposite and worsens centralization).

I don’t think I have heard anyone make the claim that builders would decentralize with PBS.  Everyone I have spoken with acknowledges that builder centralization is incredibly likely/probable and the point of PBS is to make it so that isn’t particularly problematic.

---

**pmcgoohan** (2022-08-24):

The problem comes when a pool is also the dominant builder. In this scenario PBS worsens validator centralization.

Consider this:

1 - A big pool extracting MEV grows faster than the others

2 - So we give them PBS and hope they won’t extract MEV themselves

3 - Instead, the big pool uses PBS to extract and grows faster than it would have done in (1)

How is this an unlikely scenario given that the very thing we are trying to mitigate is pools aiming to expand, and that a pool can use PBS to do this faster?

---

**MicahZoltu** (2022-08-24):

Is there a market advantage that a pool has over a non-pool builder?

---

**pmcgoohan** (2022-08-24):

Yes, pools have these advantages:

- all block producers have a network latency advantage over other builders, and pools are the biggest block producers
- pools have big economies of scale when paying for hardware and low latency feeds to other layers/chains/CEXs (same as HFT hedgies)
- pools have the funds for research and development

Most MEV will be cross layer/chains/CEXs where latency makes a big difference.

---

**MicahZoltu** (2022-08-24):

The first one is interesting, but the other two I feel like isn’t an advantage that is exclusive to validator pools.  Bloxroute, for example, I think has better connectivity to the network right now than most mining pools (at least, that is what they advertise to the mining pools they sell to) and I see no reason why this would be different under PoS.  Also, there are searchers out there who may actually make more than mining pools in terms of revenue (hard to say since no one is public about such things).

---

**pmcgoohan** (2022-08-24):

Before I go on, the overarching point here is that **PBS does not improve validator decentralization in all cases**. I’ve not seen this admitted anywhere.

You’re right that the network latency advantage is the only one exclusive to pools, and it is significant (the other two are also available to a handful of well resourced hedge fund style extractors).

A pool doesn’t actually need any special advantages to also be the dominant builder, they have the motive and the resources anyway. But given that they do have a latency advantage, I see two main scenarios:

1. a handful of dominant builders pay for low latency feeds from nodes/chains/layers/CEXs (read advantage) and integrate equally with all pools (write advantage), in which case validator centralization is mitigated anyway and PBS is just in their way

or

1. a pool becomes the dominant builder and centralizes the network around them

Either way, how does PBS help?

In (1) if some pools do the ‘right’ thing and refuse to integrate with dominant builders, they fall behind, also creating validator centralization.

In (2) PBS just makes it easier for the pool to dominate.

---

**BrunoMazorra** (2022-08-24):

Maybe there is something that I’m misunderstanding.

Yes, big pools would grow faster, but relative to smaller pools, they won’t.

That is, with PBS, if initial proportional stakes of small pool and big pool are s0 and s1. Then, in expectancy, the proportional stakes will be s0 and s1 at any time. On the other hand, without PBS, big pools will increase slower (in absolute terms) but faster in relative terms.

---

**pmcgoohan** (2022-08-24):

That was the assumption, but the model shows that if a pool is also the best at mev (and/or private order flow) then they outpace other pools at a faster rate with PBS than without (see the blue vs orange plots in the chart above).

---

**MicahZoltu** (2022-08-25):

Novel MEV may not be first discovered by a big pool.  While they do have resources to sink into searching for novel MEV sources, often times novel MEV is discovered by just looking in the rights place at the right time.  This means that there will always be a little room at least for competitors as long as those competitors can continue to participate (meaning, new entrants can’t be excluded).

---

I feel like you are arguing against a straw man.  If you have some specific claim you are arguing against then it would be best to reference it.  While lots of uninformed people say lots of things on Twitter, I haven’t seen any actual proposals/discussions that where the conclusion is that “PBS will decentralized block production”.

---

PBS, IMO, is useful compared to current relayer based system in that it doesn’t require trust in a privileged entity.  The goal of PBS isn’t to solve all of the problems, it is to make the system better than it currently is.

---

**pmcgoohan** (2022-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I feel like you are arguing against a straw man. If you have some specific claim you are arguing against then it would be best to reference it.

The opening line of this thread…

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> One of the main justifications given by @vbuterin and others for in-protocol PBS is this:
>
>
>
> “A pool that is 10x bigger will have 10x more opportunities to extract MEV but it will also be able to spend much more effort on making proprietary optimizations to extract more out of each opportunity”.

My model suggests that **PBS can just as easily worsen centralization** in exactly this case.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Novel MEV may not be first discovered by a big pool.

If maximizing MEV doesn’t help validator decentralization (or anything else), we don’t want to encourage it as most of it harms users and is inflammatory to regulators.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> PBS, IMO, is useful compared to current relayer based system in that it doesn’t require trust in a privileged entity. The goal of PBS isn’t to solve all of the problems, it is to make the system better than it currently is.

My criticisms apply equally to MEV-Boost, but at least that isn’t such a drag on the devs/EF and the complexity of L1 consensus. What problems is PBS actually solving? The justifications keep changing and none of them hold up.

The central irrationality of in-protocol PBS is that it is a complex, distributed system designed to centralize block building. Why bother building decentralized technology to promote centralization?

Compare this to TE on L1 which reduces validator centralization in all cases, improves censorship resistance, lessens the power of centralized builders over users and the network, solves the majority of toxic MEV and gives basis to the legal argument that validators are no longer intermediaries.

---

**MicahZoltu** (2022-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> MicahZoltu:
>
>
> I feel like you are arguing against a straw man. If you have some specific claim you are arguing against then it would be best to reference it.

The opening line of this thread…

I just glanced over the linked post and I didn’t see anything that indicated that the purpose of PBS was to decentralize block building.  The quote you mentioned is just the author *acknowledging* that MEV searching is a centralizing force.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> If maximizing MEV doesn’t help validator decentralization (or anything else), we don’t want to encourage it as most of it harms users and is inflammatory to regulators.

MEV is very unlikely to go away.  All we can do is try to control where it happens (in the light or in the dark) and who can participate in it (permissioned vs permissionless).  PBS can achieve one or both of these goals without changing the centralization of searching/building.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> What problems is PBS actually solving?

It increases the probability that MEV searching will have a low barrier to entry, be permissionless, and occur in the light rather than the dark.  It doesn’t stop some amount of private/secret/permissioned/connected MEV extraction, but it decreases the likelihood of that occurring and decreases the likelihood of that dominating the space.

---

**pmcgoohan** (2022-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I just glanced over the linked post and I didn’t see anything that indicated that the purpose of PBS was to decentralize block building

Block *building* has been known to be centralized by PBS since I raised it in this [series of posts](https://ethresear.ch/t/two-slot-proposer-builder-separation/10980/5).

I think you mean block *production*. As the linked document makes clear, and as Flashbots and others have continually maintained, PBS is meant to protect validator decentralization.

But as I’m now showing PBS also worsens this in some very probable cases.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> MEV is very unlikely to go away. All we can do is try to control where it happens

Ah but that’s just it. There *is* something we can do. Instead of maximizing MEV we can minimize it with base layer TE (or similar). Where MEV was an oversight before, with PBS it is now a choice.

We will need to justify to the users that are suffering frontrunning attacks and the regulators and law makers authoring legislation why we have *chosen* to maximize MEV when we could be minimizing it.

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> be permissionless, and occur in the light rather than the dark

Who cares whether frontrunning is permissionless or not. It’s frontrunning! Shouldn’t be happening at all.

Look at [zeromev.org](http://zeromev.org) before Flashbots in Feb 2011 and you’ll see we’re just as capable of auditing MEV before mev-geth as after.

In fact, PBS reduces auditability because it forces users to go direct to builders and bypass the decentralized mempool (which has not been protected by encryption).

---

**MicahZoltu** (2022-08-26):

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> Ah but that’s just it. There is something we can do. Instead of maximizing MEV we can minimize it with base layer TE (or similar).

If you want to lobby for transaction encryption then I encourage doing that directly.  Transaction encryption is very much not an obvious win because it has some very significant UX side effects, complexity costs, or technology requirements.  That discussion is out of scope here though.

![](https://ethresear.ch/user_avatar/ethresear.ch/pmcgoohan/48/8540_2.png) pmcgoohan:

> as Flashbots and others have continually maintained, PBS is meant to protect validator decentralization.

The situation people are comparing PBS to isn’t to a hypothetical transaction encryption solution, but rather to the current state of affairs or in some cases the expected state of affairs should nothing be done.  Under the current (live on mainnet) system, solo miners do not have access to MEV because the miner must be trusted (have a reputation worth losing).  Under MEV-Boost, the relay must be trusted (and we have evidence that we cannot/should not trust them already as they are known to censor).

PBS is strictly better than either of those situations in that it removes the trust requirement from the relay and the proposer.  It doesn’t solve other problems really besides the trust/permission issue, but this is significant because it allows solo validators unprivileged access to builders thus removing an incentive for them to join a well connected pool.

---

It is also worth noting that transaction encryption won’t solve all MEV, it will at best address front running issues but you can still end up with back running MEV and speculative MEV (which has potential to be a net negative impact compared to status quo).  Again though, debating the merits of transaction encryption is out of scope for this thread IMO.

---

**pmcgoohan** (2022-09-01):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> If you want to lobby for transaction encryption then I encourage doing that directly… That discussion is out of scope here though.

It is not (or should not be) out of scope because mitigation is a valid alternative response to the MEV vulnerability.

We have a big problem and limited resources. There is a fork in the road, we can either choose maximization or mitigation (or both at once). Simply comparing one version of MEV maximization to another, as you have done, is ignoring this choice.

And I’m really not sure why you would. The same issue that exposes users to toxic MEV also makes the network vulnerable to censorship (ie: transaction content being visible to a centralized builder). It was following the MEV maximizers that got Ethereum to this point.

Seperately, it’s important to note that if the validator centralization argument doesn’t hold water, then Flashbots should not be enouraging searchers to “extract extract extract”.

That’s a big deal given they that they hold conferences promoting extraction (known to include [frontrunning](https://info.zeromev.org/terms.html#frontrunning) and [censorship](https://info.zeromev.org/terms#censorship)) at the moment, even talking about it in [spiritual terms](https://www.youtube.com/watch?v=9iHlyaRsgYI). The excuse has always been that this harm is neccessary to protect consensus (when they even acknowledge user harms).

It was always a poor trade-off anyway, because users are non-consensual. If they don’t have even this fig-leaf of a reason, they just need to stop.

---

**0xShitTrader** (2022-09-01):

Toxic, user-tx-generated frontrun/backrun MEV can be mitigated by auctions upstream of the block builder layer, where searchers perform the same behavior they do today but the auction proceeds get routed back to the user rather than to the consensus layer.

This requires order flow auctions, which can probably be made public via partial transaction shielding. Such a system likely still requires trust in a central, aligned intermediary to run these auctions, like how Flashbots Auction requires that Flashbots’ mev-relay has good behavior.

---

**pmcgoohan** (2022-09-01):

As with all services based around builders, this scheme is trusted and centralized (as you admit).

PBS as it stands provides trustless, consensus based guarantees that protect the ordering interests of builders and validators alone.

Meanwhile, users are left with centralized, reputational systems for protection, which builders are ultimately incentivized to [make fail](https://twitter.com/pmcgoohanCrypto/status/1516410063665127425?s=20&t=bJMY1-Ehpqmzabz_QEZoRw).

Ethereum surely exists to serve its users, not its builders.

So how have we ended up lumbering users with reputational systems, while validators and builders are protected by the full weight of consensus?

---

**Mister-Meeseeks** (2022-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> Is there a market advantage that a pool has over a non-pool builder?

A pool builder has guaranteed control over the next block, whereas a non-pool builder will only win the block from the validator to the extent he bids more than all other non-pool builders.

When there is no uncertainty about the value of the MEV in the block, these two conditions are economically equivalent. But when individual traders have partially overlapping private information, the non-pool builder is at a disadvantage. This is because winning the public auction for the block involves an *adverse selection cost*.

For example if you are watching real-time prices at FTX and I am watching real-time prices at ByBit, we have correlated but not equivalent information. Even though the trades you submit are independent of the ByBit specific price discovery, the blocks you end up winning are skewed in the wrong direction against ByBit. For this reason every bid you make must reflect the adverse selection cost of the mutually exclusive private information the other competitors in the auction make, and therefore you always bid less than your internal prediction of the block’s value.

Or in other words the validator who outsources block building does not get paid as much as the validator that builds the full infrastructure internally. And therefore validators with internal block building capabilities can extract larger economic returns than the sum of validators and block builders operating at arms length distance.

---

**pmcgoohan** (2022-09-05):

Thanks for the input [@Mister-Meeseeks](/u/mister-meeseeks). I’m trying to work out if your adverse selection cost is palpably different from the [network latency cost](https://ethresear.ch/t/model-pool-centralization-from-mev/13485/6) I identified above.

It seems they might be equivalent (ie: the proposer is best positioned to get the latest information possible from both FTX and ByBit) or have I misunderstood?

