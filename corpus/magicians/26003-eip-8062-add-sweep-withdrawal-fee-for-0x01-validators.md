---
source: magicians
topic_id: 26003
title: "EIP-8062: Add sweep withdrawal fee for 0x01 validators"
author: aelowsson
date: "2025-10-28"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8062-add-sweep-withdrawal-fee-for-0x01-validators/26003
views: 268
likes: 19
posts_count: 12
---

# EIP-8062: Add sweep withdrawal fee for 0x01 validators

Discussion topic for [EIP-8062](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8062.md); [PR](https://github.com/ethereum/EIPs/pull/10639); [Web](https://eips.ethereum.org/EIPS/eip-8062).

#### Description

Improve stake consolidation and fairness by imposing a “sweep” withdrawal fee for `0x01` validators set to 0.05% of the withdrawn amount.

### Abstract

A fee is proposed on the partial beacon chain “sweep” withdrawal of validators using `0x01` credentials to improve stake consolidation and fairness. Ethereum’s fast finality roadmap hinges on staking service providers migrating from `0x01` validators to `0x02` compounding validators. One roadblock is that `0x01` validators receive free-of-charge sweep withdrawals for balances exceeding 32 ETH, which consume protocol resources that are not accounted for. To address this, a 0.05% fee is imposed on the partial `0x01` sweep using a minimal modification to `process_withdrawals()`, applying the new constant `WITHDRAWAL_FEE_FRACTION = 2000`.

## Replies

**ChrisB** (2025-11-13):

I’d like to counter the proposal and spin the take around.

Instead of adding additional complexity for 2$/validator/year, why not actually remove complexity from the spec and archive the same goal. Get rid of the automatic withdrawals clock, onboard 0x01 to manual withdrawals like 0x02?

---

**aelowsson** (2025-11-14):

With withdrawals clock you are referring to the sweep? Removing the sweep would be a huge change and it is currently used also for exits. Also, it seems like it would degrade the UX. Furthermore it might not solve the underlying problem we are actually trying to solve, which is to provide the right incentives for stakers to consolidate stake in `0x02` validators. Finally note the alternative specification that outlines higher withdrawal fees and the rationale behind them.

---

**CelticWarrior** (2025-11-14):

EIP 8062 is deeply flawed in that it fails to address or even analyze the root cause of the lack-of-consolidations problem that is due to the flawed design of the 0x02 validator.

0x02 is flawed for two related reasons:

1. It fails to recognize that many validator operators (both pro and solo) need predictible income in order to pay taxes, business and living expenses, etc.  While 0x01 validators provide this with their automated sweep feature, 0x02’s need for an Ethereum transaction followed by a highly unpredictable time in a withdrawal queue (a horrible UX in itself) eliminates the predictible income nature of the 0x01 validator.
2. The 2048 ETH threshold for automated sweeping is way too high.  That level is so high that each validator key would now be worth ~$10 million and the validators so large that they should probably be called whale-idators.  If the 0x02 automated sweep level had been set to 320 (or maybe 512) ETH we would have seen a far greater level of consolidation.

Lastly, adding the fee that is proposed in 8062 merely penalizes the solo staker and those that need predictible cashflow.  Very few solos have enough ETH to consolidate to a whale-idator in order to benefit from the automated sweep.  And those that do consolidate are now trapped by the unpredictable timing of cashflow that 0x02 demands.

The best solution to encourage consolidations is not a flawed and reactionary EIP 8062.  It is a tweak to the 0x02 validator to either a) drop the sweep threshold to 320 ETH, or b) make the sweep threshold configurable via an onchain transaction.

Let’s fix 0x02 before meddling via 8062.  And maybe that is as simple as a copy/paste of 0x02 into 0x03 with a 320 ETH sweep threshold.

And why no mention of penalizing the 0x00 validators that have never migrated?

---

**ChrisB** (2025-11-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> Removing the sweep would be a huge change and it is currently used also for exits

I agree to some degree. It’s a process but it would be a step to deprecate the clock by removing the sweeps at least while keeping it for exits for now.

As for the UX, it would be the same as for 0x02. I feel like nobody asked to get a withdrawal sweep every 8 days, but we implemented it that way and now we punish people for getting these frequent automatic payouts, which they have no control over, by charging a fee.

While the UX for these automatic payouts is also super confusing and a separate tab on many block explorers, I’d argue that it’s actually better UX to have an explicit user action like in 0x02. It is fair to 0x02, reduces state bloat and is one step to reduce spec complexity.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> Furthermore it might not solve the underlying problem we are actually trying to solve, which is to provide the right incentives for stakers to consolidate stake in 0x02 validators

I feel like this EIP is not honest about its motivation then. It’s laid out as a fairness measure when the real intention is to force people to move to 0x02.

But I feel like this EIP does not a good job at that either. It only “forces” 0x01 to move but not 0x00? And 0x00, despite no withdrawals, still has a significant portion of share even after several years. People seem to have uses for this, and Ethereum takes pride in diversity but now we make an exception to that when it comes to credential type preferences?

There are valid reasons why one might not want to move to compounding, in some jurisdictions this has quite the tax implications. Not saying that we should cater to these external usecases but just to show that we might not understand the full picture why people still sit on their 0x00 and 0x01.

All while 0x00 proves that it will be impossible to sunset any withdrawal credential, so I feel like with this EIP we don’t really solve the root cause but rather fight the symptoms.

I do acknowledge though that 0x00 and 0x01 is more costly compared to 0x02 and it makes sense for wanting more people to move, but I respectfully dislike the approach of this EIP. Having said that, I do acknowledge the work you put into. You put in the effort to make this an EIP while I type up my thoughts on it on a phone. I’d just rather make 0x01 more unattractive in other ways like increasing the sweep interval or embrace the usecases of 0x01 and find a compromise between 0x02 and 0x01.

---

**aelowsson** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> EIP 8062 is deeply flawed in that it fails to address or even analyze the root cause of the lack-of-consolidations problem that is due to the flawed design of the 0x02 validator.
>
>
> 0x02 is flawed for two related reasons:
>
>
> It fails to recognize that many validator operators (both pro and solo) need predictible income in order to pay taxes, business and living expenses, etc. While 0x01 validators provide this with their automated sweep feature, 0x02’s need for an Ethereum transaction followed by a highly unpredictable time in a withdrawal queue (a horrible UX in itself) eliminates the predictible income nature of the 0x01 validator.

The current situation is not ideal. This is why we are increasing the churn limit on exits with EIP-8061 (or EIP-8080), which should significantly bring down the length of the queue. I also agree that lower sweep thresholds could be useful (more on this below).

An argument can at the same time be made that for the specific use cases mentioned, the unpredictability is rather manageable. The time in the withdrawal queue is predictable in the sense that you can always observe when a withdrawal will be processed simply from the current churn accounting for the queue. If you know beforehand when you need the money, you can make a withdrawal to achieve a desirable exit time. If you do not know beforehand, you can still watch the withdrawal queue and make partial withdrawals that produce a steady stream of income (setting aside the edge case if there is a sudden huge influx of exiting stake).

Naturally, it would however be ideal to reduce the delay between the withdrawal transaction and receiving the money, hence adjustments to the churn to bring down the queue. In practice, we could also remove the churn entirely for smaller partial withdrawals that do not alter the EB.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> The 2048 ETH threshold for automated sweeping is way too high. That level is so high that each validator key would now be worth ~$10 million and the validators so large that they should probably be called whale-idators. If the 0x02 automated sweep level had been set to 320 (or maybe 512) ETH we would have seen a far greater level of consolidation.

I agree that letting validators set their own sweep threshold could be beneficial, and this is something we should consider for the Heka hardfork. I have heard that developers did not see sufficient demand for this complexity when implementing the current design, but the situation may have changed.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> Lastly, adding the fee that is proposed in 8062 merely penalizes the solo staker and those that need predictible cashflow. Very few solos have enough ETH to consolidate to a whale-idator in order to benefit from the automated sweep. And those that do consolidate are now trapped by the unpredictable timing of cashflow that 0x02 demands.

Setting aside the potential merits of the sweep/partial withdrawal for a moment, it is actually easiest for solo stakers to switch to `0x02` and avoid the fee entirely, as they do not have the complex legal or smart contract constraints that staking pools do.

So this proposal is the more solo-staker-friendly way to incentivize consolidation. For fast finality, we need staking pools to consolidate stake in `0x02` validators, but at the same time want to avoid giving solo stakers a lower yield. This naturally leads to the idea of attaching a fee specifically to the `0x01` validators, and as it turns out, this can be done very simply by taking the fee out from the sweep.

It is very doubtful that we will be able to achieve desirable consolidation without incentives in place. The fast finality design is now already somewhat adapting to a landscape where we will not have a very good consolidation, at least initially. This can of course be wise anyway, since we do not want to make strong assumptions about consolidation level. But we are also restricting the design space.

Improved tooling is clearly also one component in the transition, which is pursued independently. Improvements to the `0x02` validator UX are also pursued. But these are likely to be insufficient on their own, particularly for transitioning staking pools that are locked in setups relying on `0x01` validators. A benefit of EIP-8062 here is that it signals clear intent: we will pursue consolidation, including with incentives when required, and staking pools should already today design with this in mind.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> The best solution to encourage consolidations is not a flawed and reactionary EIP 8062. It is a tweak to the 0x02 validator to either a) drop the sweep threshold to 320 ETH, or b) make the sweep threshold configurable via an onchain transaction.

For reasons outlined above, it is better to take a holistic approach and as quickly as possible pursue several paths for consolidation.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> Let’s fix 0x02 before meddling via 8062. And maybe that is as simple as a copy/paste of 0x02 into 0x03 with a 320 ETH sweep threshold.

The proposed copy/paste-strategy is unfortunately not a desirable option. It is better to allow stakers to set the sweep threshold themselves.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> And why no mention of penalizing the 0x00 validators that have never migrated?

These validators hold a very small proportion of the aggregate effective balance and they’re capital-inefficient already. There is no threat of staking pools opting for this solution (while staying competitive). We therefore do not need to focus on `0x00` validators at this moment.

---

**CelticWarrior** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aelowsson/48/14632_2.png) aelowsson:

> be made that for the specific use cases mentioned, the unpredictability is rather manageable. The time in the withdrawal queue is predictable in the sense that you can always observe when a withdrawal will be processed simply from the current churn accounting for the queue. If you know beforehand when you need the money, you can make a withdrawal to achieve a desirable exit time. If you do not know beforehand, you can still watch the withdrawal queue and make partial withdrawals that produce a steady stream of income (setting aside the edge case if there is a sud

So rather than implement another EIP that is just a band-aid and unnecessary additional complexity for the protocol, we should focus on implementing a fix to the 0x02 validator.

And at a minimum, sufficient time (i.e. at least a year) should be given for the required tooling (e.g. batching validator consolidations) to be developed for the large staking pools to begin to move to 0x02.

EIP-8062 is not needed now.

---

**aelowsson** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> So rather than implement another EIP that is just a band-aid and unnecessary additional complexity for the protocol, we should focus on implementing a fix to the 0x02 validator.
>
>
> And at a minimum, sufficient time (i.e. at least a year) should be given for the required tooling (e.g. batching validator consolidations) to be developed for the large staking pools to begin to move to 0x02.

The discussed adjustments to the `0x02` validator will be insufficient for achieving a desirable consolidation level. This EIP would go live over a year after the Electra hardfork, potentially quite a bit longer.

---

**CelticWarrior** (2025-11-24):

If the 0x02 validator had a configurable sweep threshold, it would be far more desirable to consolidate.  As currently designed with the 2048 ETH threshold, the cashflow characteristics of the 0x02 validator provide a negative incentive to consolidate.  And therein lies the problem.  Adding an uncesessary EIP to fix a problem at anything other than its root source seems to be misguided and adds unnecessary complexity to the protocol.

---

**aelowsson** (2025-11-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/celticwarrior/48/15145_2.png) CelticWarrior:

> If the 0x02 validator had a configurable sweep threshold, it would be far more desirable to consolidate. As currently designed with the 2048 ETH threshold, the cashflow characteristics of the 0x02 validator provide a negative incentive to consolidate. And therein lies the problem. Adding an uncesessary EIP to fix a problem at anything other than its root source seems to be misguided and adds unnecessary complexity to the protocol.

It seems we are in agreement on a variable sweep threshold for `0x02` validators potentially being useful to a subset of users. However, another component to consolidation is to provide incentives that make migration beneficial also for staking service providers (SSPs) that are currently locked (legal/smart contracts) in setups relying on `0x01` validators. Since we would prefer to not differentiate the yield between smaller and bigger validators at this point, we simply attach a fee to `0x01` validators, under the assumption that these SSPs will then opt to consolidate upon migration.

---

**yvesholenstein** (2025-11-25):

I would like to counter this proposal. Please be aware that ***custodial*** staking service providers like us (Bitcoin Suisse) are subject to many regulatory requirements for on-chain asset handling, as well as accounting and reporting.

Since Ethereum staking is fairly complex, it took us until now (November 2025) to build a “post-Pectra” staking product that is fully compliant and automated. However, we still have to develop the automation for migration of old validators to the post-Pectra product. This includes on-chain consolidation automation, but also (again) many rules regarding how we book all activities in the core-banking system and how we report all activities in client account statements and tax reports.

I often have the impression, that the burdens for us institutional players are unknown to Ethereum core developers. It is not that we do not “want” to migrate to post-Pectra, but we are slow “tankers”, not “speed boats”.

Please keep this in mind and do not suggest “penalizing” your users.

---

**aelowsson** (2025-11-26):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/y/e36b37/48.png) yvesholenstein:

> Please keep this in mind and do not suggest “penalizing” your users.

Let us try to establish common ground through a set of observations, and then consider timelines.

**Observation 1**: under current design constraints, Ethereum should adopt consolidation incentives in conjunction with fast finality. The goal is to ensure that finality is not delayed due to improper incentives. The main mechanism is a “consolidation force” that increases as the level of consolidation decreases, reducing the yield for smaller validators (and potentially collectively for all validators). Thus, when consolidation is acceptable, there may be no change in yield at all (relative to some baseline). On the other hand, if consolidation is so poor that fast finality degrades, the yield differential may be rather substantial. For reference, see the curves in Figures 1-3 [here](https://ethresear.ch/t/consolidation-incentives-in-orbit-vorbit-ssf/21593#p-52518-h-22-consolidation-force-shapes-6), although this is not the latest design.

**Observation 2**: it is preferable to not initially penalize small validators since these tend to be operated by solo stakers.

**Observation 3**: by making `0x01` validators relatively less profitable than `0x02` validators, consolidation can be promoted while the staking yield does not depend on validator size. The assumption is that SSPs will consolidate upon switching from `0x01` to `0x02`. The operational friction of switching for stakers that never intend to stake more than 32 ETH is then a trade-off that must be accepted. We can foresee a future where we want to put our focus on improving the `0x02` validator design, and switching might therefore be necessary down the line anyway.

**Observation 4**: as illustrated in EIP-8062 (Figure 1) and discussed in further detail in EIP-8068, `0x01` validators have better capital efficiency than `0x02` validators unless they hold a substantial amount of stake. This lends further credence to the idea of specifically reducing the yield for `0x01` validators. Otherwise, a staker deciding between running 4 `0x01` 32-ETH validators and 1 `0x02` 128-ETH validator has no incentive to switch. Preferences concerning sweep/partial withdrawals and the potential convenience of not having to re-allocate the skimmed ETH whenever it is not used for ongoing expenses may of course tip the scale in both directions.

**Observation 5**: Ethereum has never increased its issuance, and it is preferable to not break from this norm.

---

Hopefully we can agree on Observations 1-5. If so, having reached common ground, it largely becomes a matter of timelines—a question of *when* EIP-8062 should be adopted, not *if* it should be adopted.

Assume that the Glamsterdam hardfork takes place in September 2026: around 9-10 months from now, and a little less than 1.5 years after the Pectra hardfork that enabled consolidation. The question then is whether this is the right time to institute the first consolidation incentives. Is the subsequent hardfork—that may not happen until 2.5 years after Pectra—potentially too late? Or is that the right point?

Given the current consolidation progress, I believe that Glamsterdam is the preferred choice, but that the initial incentive can be kept relatively modest for this hardfork. Adopting EIP-8062 in Glamsterdam will then have a very moderate effect on the yield, but it will still put the spotlight on consolidation being important and something that is expected from stakers. It also prepares stakers and the protocol for a potential increase in the subsequent hardfork. Your input on Observations 1-5 and on timelines is of course welcome.

