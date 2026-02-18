---
source: ethresearch
topic_id: 4942
title: Rate-limiting entry/exits, not withdrawals
author: vbuterin
date: "2019-02-04"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/rate-limiting-entry-exits-not-withdrawals/4942
views: 8111
likes: 11
posts_count: 22
---

# Rate-limiting entry/exits, not withdrawals

Currently, validators are able to enter and leave the validator set relatively quickly: each time a validator set transition happens, 1/64 of the validator set can switch in or out, and so in the normal case, every validator can switch out within a day. There is a much slower queue for *withdrawing*, to prevent validators from all withdrawing as soon as they perform a large-scale attack before they can be penalized. I argue that this current status quo is suboptimal, and we should set the withdrawal delay to a minimal constant (eg. 1 day) and instead use a much more conservative bound on entry/exit rate to serve the same function.

I claim this is a good idea for a few reasons:

- CBC Casper compatibility: part of CBC philosophy is that the chain does not need to converge on one specific mechanism to determine canonical “finality”; applications can choose what thresholds they use. The current validator set change mechanism (1/64 every time the chain finalizes) requires the chain to have a canonical finality oracle.
- Light client friendliness: having a much slower bound on validator set change makes it easier for light clients to skip ahead a relatively long distance at a time.
- Ability to resume finalization via a surge of friendly deposits: if there are not enough validators that are online, a fixed rate limit on entry/exit, that does not require the chain to finalize to proceed, would allow altruistic ETH holders to swoop in and join the validator set to cause it to resume finalization.
- Resistance to discouragement attacks: a discouragement attack (link to mini-paper here) involves an attacker (with >=33% stake) causing a medium amount of disruption to consensus, with the purpose of making it unprofitable for others to validate. This drives others to leave, making further attacks cheaper and more profitable. Making it simply not possible for validators to leave quickly (intuition: you joined the army, the fort is under attack, you have to stay around to defend it, being on-call for that sort of thing is the job description!) is the best known strategy to increase the cost of discouragement attacks.

The alternative is simple to implement:

- Reduce the maximum number of validators that can enter or exit from 1/64 of the total to a much lower fraction, or even a square root or a constant (think: 1-3 months to rotate the entire validator set)
- Repurpose the withdrawal queue into a entry/exit queue. Repurpose exit_slot as the slot when either (i) a deposit was processed or (ii) an exit was triggered. Post-exit withdrawal is now a fixed length of time (possibly extendable with proofs of custody)

## Replies

**naterush** (2019-02-05):

Very cool. The main tradeoff that jumps out here is the increased cost validators bear in the case they want to stop validating - and it’s not even increased capital lockup costs, but rather the fact that they have to stay online and keep generating messages.

Are there any other disadvantages this scheme has over the previous one that I’m missing?

> Ability to resume finalization via a surge of friendly deposits :

It seems like the answer is obviously no, but is there any case where “lots of deposits can enter without finality” actually makes things worse? I’m wondering if it might make some weird discouragement attack more powerful (or something), as this change expands the attackers set of strategies when finality is not being reached…

---

**vbuterin** (2019-02-05):

> Very cool. The main tradeoff that jumps out here is the increased cost validators bear in the case they want to stop validating - and it’s not even increased capital lockup costs, but rather the fact that they have to stay online and keep generating messages.

Capital lockup costs are unchanged; it’s the stay-online requirement that’s stronger. Though it’s worth keeping in mind that the current system also has a stay-online requirement, as you need to respond to proof of custody challenges.

---

**naterush** (2019-02-05):

Sure. This strengthens the stay-online requirement though, as validators must be online per-epoch as compared to per-response-deadline.

---

**vbuterin** (2019-02-05):

Agree! Though OTOOH validators can earn revenue throughout this extra time period, whereas in the current design they’re just sitting in limbo.

---

**econoar** (2019-02-07):

I think this is interesting and it would seem to me that the pros outweigh the cons.

On the economics side, we’d essentially be taking staking from a money market type product to a smaller term product. Although, it sounds like in your proposal that’d be only a month or so? I’d say from a validator standpoint and attractiveness of investment, they’d only demand slightly more interest. The one caveat is that since the staking rate is floating, a validator technically does not know what his interest rate will be over period of lockup. Probably a smaller concern but one I’d say is worth considering.

What we’re seeing in open finance so far is that instant lending is not offering a very big return, because the borrower set is much smaller than the lending set. I see some fixed term products coming online that are hoping to increase that rate but I’d expect almost all validators to think of staking as a longer term investment anyways. As long as this is known up front I don’t really see much concern.

---

**ryanseanadams** (2019-02-07):

I think the staking community would tolerate a reasonable delay in withdrawal time. Choosing to stake is not like having funds in a savings or checking account, it’s closer to a deposit into CDs & T-Bills. It’s understandable that a withdrawal would not be instant.

Off the cuff, a 1 to 2 day withdrawal period seems fine. 3-4 days, starts to feel like hardship. 5 days or longer would be quite the ask. Depending on the length, you might expect staking pool services to crop up that provide immediate withdrawal liquidity to customers as a service or for a fee (an unintended centralization vector perhaps? You could imagine stakers moving to a Coinbase or RocketPool for their “instant withdrawal times”).

Of course, all of these dynamics (reward rate, slashing risk, withdrawal time) will play into the decision to stake & weighed against alternative uses of the capital, or more specifically alternative uses of the Eth in the open finance world.

---

**vbuterin** (2019-02-08):

What would happen here is that 1 day would be the “happy case” withdrawal time, and something like 3-6 months would be the “worst case” withdrawal time if everyone is trying to withdraw at the same time. I’m expecting the happy case to be the normal case, but still trying to come up with better ways to reason through that.

---

**sassal** (2019-02-08):

1 day withdrawal time is completely fine, imo. The 3-6 months is a very long time if we look at it from a market perspective for obvious reasons. Though, I can’t imagine many scenarios (besides actual attacks) where everyone would be trying to withdraw at once.

In saying this, I speculate that a lot of the people who will be staking are those that are currently just holding their ETH in cold storage so this long withdrawal period may not be an issue for them.

I also imagine that there will be some sort of derivative product that tracks the underlying ‘withdraw in progress’ ETH so that people could ‘offload’ their stake before the withdrawal is finalized.

Also, do validators have to wait until the withdraw is finalized before they can re-stake their ETH?

---

**vbuterin** (2019-02-08):

I did a simulation of actual withdrawal times assuming two simplifications: (i) a Zipf’s law (ie. power law with power=1) distribution of validator deposit sizes, (ii) each validator has a 1/D chance of deciding to start exiting any given day.

Here’s the code: https://github.com/ethereum/research/blob/2d3ed6e42087d5b14cdf107c897e8d3e5db3ee7a/exit_queue_tests/exit_queue_tester.py

The results were fairly bimodal: if you set a rule that the entire validator set can withdraw after N days (ie. 1/N of the set per day), and D > N, then we get validators being able to withdraw almost instantly. Here’s N = 180 and D = 360:

```auto
Total delays in days
21759:  11.318 (min 12.534)
10879:  6.528 (min 6.267)
5439:  3.643 (min 3.133)
2719:  1.995 (min 1.566)
1359:  1.088 (min 0.783)
679:  1.010 (min 0.391)
339:  0.989 (min 0.195)
169:  0.836 (min 0.097)
84:  0.942 (min 0.048)
42:  0.866 (min 0.024)
21:  0.925 (min 0.012)
10:  0.928 (min 0.006)
5:  0.933 (min 0.003)
2:  0.943 (min 0.001)
1:  0.952 (min 0.001)
```

(delays are sometimes lower than the minimum because the minimum is calculated based on the target total deposit size which doesn’t perfectly match the actual one)

Now here’s D = 180, N = 240 (only the top 5 rows for compactness):

```auto
21759:  12.667 (min 12.534)
10879:  8.149 (min 6.267)
5439:  5.059 (min 3.133)
2719:  3.866 (min 1.566)
1359:  3.003 (min 0.783)
```

Now D = 180, N = 180:

```auto
21759:  26.618 (min 12.534)
10879:  25.083 (min 6.267)
5439:  23.793 (min 3.133)
2719:  22.048 (min 1.566)
1359:  22.355 (min 0.783)
```

And D = 180, N = 120:

```auto
21759:  76.153 (min 12.534)
10879:  73.770 (min 6.267)
5439:  74.317 (min 3.133)
2719:  74.556 (min 1.566)
1359:  74.288 (min 0.783)
```

This makes me think that things will be fine but we would benefit from some explicit policy to discourage validators from exiting too quickly. Perhaps have the exit queue favor “older” validators in some way.

---

**CRN** (2019-03-15):

Took a while to collect my thoughts. Here’s my take on this proposal.

I think 1/N of the set per day, with a 2-3 day min delay is good. But, I think there’s a case to increase the min delay to 3-5 days. I would argue that a longer minimum delay constant (e.g. 3 days) actually helps self-select validators that are aligned with the “defend the fort” intuition, and thus are more prone to be agreeable to the 1/N limit.

Here’s how I would construct the argument:

- Using a lower min constant (e.g. 1 day) sets up an anchoring bias that will lead people to underestimate how much of a commitment validating can be. This may cause some validators to regret their decision, which can result in poor retention.
- For example, econoar, ryanseanadams and sassal have commented to the effect that 1 day is painless, this despite the delaying effects of the 1/N limit (i.e. everyone thinks they’ll manage to be the first out). So, I argue that if the min constant has no bite, it won’t be taken into consideration when deciding to stake or not, and thus might recruit less responsible validators (e.g. screw the fort, I’m just passing through, SO LET ME OUTTA HERE!).
- If we want to balance the instantaneous security of more validators with the extended-time security of more fort-defenders, then I suggest we choose a goldilocks value for the min constant. This feels to me like 2 days minimum, but my preference would be for 3-5.
- ADDENDUM: I feel that the choice of N is less sensitive as it will likely be discounted by most non-robotic validators. The anchoring effect of the min constant seems to be more important, at least while validators are mostly human.

---

**vbuterin** (2019-03-16):

> I think 1/N of the set per day, with a 2-3 day min delay is good

Sorry, by delay here do you mean exit delay or withdrawal delay? Note that the proof of custody game already forces a 2 day min delay after you’ve exited.

> ADDENDUM: I feel that the choice of N is less sensitive as it will likely be discounted by most non-robotic validators. The anchoring effect of the min constant seems to be more important, at least while validators are mostly human.

I don’t think it’s quite so simple. Humans are affected not just by numbers, but also by scare stories. And hearing someone say on reddit “OMG my exit took 49 days!!!1!” vs “OMG my exit took 176 days!!!1!” do have significantly different effects.

---

**CRN** (2019-03-16):

I assumed a variable exit delay and a fixed withdrawal delay. I wasn’t aware that the custody game added 2 days delay as well. Hsiao-Wei Wang’s recent slides make it appear as if this only for Phase1. Either way, my concern was only with the possibility of 1 day of total delays, from voluntary exit to withdraw-able state. That seems to not be the case. If it totals to a *minimum* of 2-5 days, I think that’s great.

re: long exit delays, if I’m interpreting your code (above) correctly, it looks like month long delays will be exceedingly rare. To test this, I extended your python code to run a monte carlo simulation and count the number of n-day delays that occur on the network. Looks like on average, only one staker every 2 years should experience more than a 30 day delay in the absence of a black swan (based on your starting assumptions).

Here’s the extended code:



      [gist.github.com](https://gist.github.com/crn-maximizer/a4558014eb38036f6339e808579fda72)





####










And the results (key is the # of days delayed, value is the mean over 1000 trials):

[![image](https://ethresear.ch/uploads/default/optimized/2X/4/491a7ea153d53ec333ae3438e10a3e1e92f519d8_2_690x133.png)image1560×302 34.8 KB](https://ethresear.ch/uploads/default/491a7ea153d53ec333ae3438e10a3e1e92f519d8)

So, if you add to these averages a total of 2-3 days to account for the custody game and minimal withdrawal delay, then I think this is looking good (at least w/ these assumptions). ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=14)

---

**CRN** (2019-03-16):

More thoughts…

An interesting reason to support rate-limiting exits rather than withdraws is that it boosts incentives for validating nodes to be physically decentralized as a way of avoiding slashing.

Here’s a non-exhaustive list of scenarios that promote decentralization of nodes under a rate-limited exit scheme by making validators avoid being effected by the same environmental factors of other validators:

1. Power grid issues (e.g. rolling blackouts or national power outage).
2. Connectivity issues (e.g. the internet gets shutdown in country X).
3. Oppressive regulation (e.g. Crypto is made illegal in country X).
4. Geo-political strife in region X produces one of the above.
5. A natural disaster and/or global warming produces one of the above.

*Counter-argument:* Validators shouldn’t be penalized for environmental factors outside their control.

*Counter-counter argument:* The priority of the network should be to keep nodes up. Better to have fewer nodes in unstable regions and more nodes in stable ones. Validators in these regions can also move their operations elsewhere if disaster strikes.

*Counter^3 argument:* Not all people in these regions will have the freedom of mobility to physically relocate their operation.

*Counter^4 argument:* Hopefully there will be easy to use migration tools for validators to move their operation into the cloud ahead of some pending environmental danger.

---

**lightuponlight** (2019-03-17):

My problem with this is that people may become aware that they will be unable to validate because of a hardware / network outage, etc.

In that case, they would be penalized for not being online / validating, which may be of no fault of their own.

Because of this, my preference would be that someone can stop validating quickly but withdrawals are rate limited.

---

**vbuterin** (2019-03-18):

The counter-argument to that would be that *in the normal case*, where the outage only hits you and a few other validators, you still will be able to exit quickly; the only case where you can’t is if the outage hits everyone at once. But if the outage hits everyone at once, it’s your duty to try really hard to get your node back online; that’s what you signed up for by being a validator.

---

**vbuterin** (2019-03-22):

Another interesting alternative is a queue where the rate of processing depends on the existing queue length. This seems like it reduces volatility of exit times.

Here are results from simulating a queue that always allows a maximum of 1% per day of exits, assuming the average validator sticks around for `k` days, so think of `1/k` as the rate of churn (if k < 100, then the queue is filling faster than it is clearing, though there is a natural upper bound as in the limit *all* ETH is stuck in the queue):

| k | Avg delay |
| --- | --- |
| 200 | 0.5 |
| 150 | 1.4 |
| 120 | 3.7 |
| 110 | 5.6 |
| 100 | 13.6 |
| 90 | 21.4 |

Now, let’s make the withdrawal rate proportional to `log(len(exit_queue))`, with parameters targeted to keep the average withdrawal delay at k=120 unchanged.

| k | Avg delay |
| --- | --- |
| 200 | 0.8 |
| 150 | 1.7 |
| 120 | 3.7 |
| 110 | 5.0 |
| 100 | 8.4 |
| 90 | 11.7 |

We could go further, and use `sqrt(validator_count * len(exit_queue))`. Then we get:

| k | Avg delay |
| --- | --- |
| 200 | 2.0 |
| 150 | 2.9 |
| 120 | 3.7 |
| 110 | 4.1 |
| 100 | 4.5 |
| 90 | 5.0 |

*Now* we can see some stability. We can clearly tune the tradeoff in whatever way we like.

---

**mohamedhayibor** (2020-05-11):

I think 99% of times, we’ll be in a “happy” case. The “mayhem” case is when a disaster (or massive FUD, black swan event) happens and almost every validator wants out immediately. For example somebody yells FIRE in a crowded theater with only one exit. The only model I can think of is everyone squeezed up at the door trying to get out.

I think there gotta be incentives for people who stick it out when the network really needs it. Some rewards which could even incentivize brand new validators to rush in to help (and stay online).

Btw is this representative of the validators entry and exit steps?

[![Entry-Exit-POS](https://ethresear.ch/uploads/default/optimized/2X/f/f8a4fb5672bba2e7059484630fb0bafe5cb7131e_2_266x500.jpeg)Entry-Exit-POS934×1754 176 KB](https://ethresear.ch/uploads/default/f8a4fb5672bba2e7059484630fb0bafe5cb7131e)

---

**JustinDrake** (2020-05-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/mohamedhayibor/48/4824_2.png) mohamedhayibor:

> is this representative of the validators entry and exit steps?

One small detail. The “can’t get penalized” can go up one level next to “receives back the stake”. A withdrawable validator [is not slashable](https://github.com/ethereum/eth2.0-specs/blob/5b2a08b717c68557e4f4f7667952060cb9407037/specs/phase0/beacon-chain.md#is_slashable_validator).

---

**mohamedhayibor** (2020-05-13):

Updated

[![Entry-Exit-updated](https://ethresear.ch/uploads/default/optimized/2X/0/0b979c81e2fa35a04514fcb5ed098d8215311113_2_266x500.jpeg)Entry-Exit-updated934×1754 170 KB](https://ethresear.ch/uploads/default/0b979c81e2fa35a04514fcb5ed098d8215311113)

---

**tutacrypto** (2022-07-07):

Hello,

I was looking to find the rate limit in the exit queue for ETH2 validators, and how this relates to withdrawals. I couldn’t find any clear answer about what has been implemented as limit exit rate and ended up here.

Do you know where I could find the details of 1) the maximum rate of validators exit, and 2) if funds can be withdrawn 1 day after a successful exit, as explained [here](https://www.attestant.io/posts/understanding-the-validator-lifecycle/) ?

Thanks


*(1 more replies not shown)*
