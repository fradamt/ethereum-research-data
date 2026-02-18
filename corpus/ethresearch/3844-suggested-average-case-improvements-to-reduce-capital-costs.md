---
source: ethresearch
topic_id: 3844
title: Suggested average-case improvements to reduce capital costs of being a Casper validator
author: vbuterin
date: "2018-10-18"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/suggested-average-case-improvements-to-reduce-capital-costs-of-being-a-casper-validator/3844
views: 3876
likes: 4
posts_count: 13
---

# Suggested average-case improvements to reduce capital costs of being a Casper validator

1. Add a rule that the withdrawal delay is not a fixed number of seconds or slots; instead, it is linearly proportional to the number of ETH that was in the active validator set at the time that you join (eg. 3 months if it’s 10 million, 9 months if it’s 30 million, but only ~3 weeks if it’s 2.5 million). Alternatively, we can add a cap at eg. ~3 months.
2. Instead of having a hard ~3 month withdrawal time, when a validator withdraws put them at the end of a withdrawal queue, and if one period has length equal to 3 months * k (eg. k = 0.001), each period process a maximum k * active_validator_set_size validators from the front of the queue.

(1) ensures that under conditions of lower security demand, the total validator count does not decrease as much since more validators would be willing to participate with a lower withdrawal time, thereby spreading out the security loss evenly between reducing the cost of a 51% attack and reducing the maximum safe offline period. (2) ensures that validators can withdraw very quickly in “the normal case” but not during attacks. (1) and (2) can be combined by making the number of withdrawals processed per period be a fixed number.

## Replies

**drcode1** (2018-10-18):

This sounds like a great idea and like something obvious to do in hindsight.

*One possible modification:* Might it not be simpler to just have validators choose at the time of joining what “withdrawal time” they prefer (within limits) and then have a reward multiplier X that asymptotically approaches 1 if they choose a longer withdrawal time? That way, you only need to adjust rewards (not withdrawal time) when total validator count changes, and if rewards are high (because validator counts are low) people will naturally choose shorter withdrawal times based on their own initiative.

Giving people some flexibility over withdrawal times could be another incentive to spur on more validator participation- I mean, if you’re already taking on the extra pain (with regard to security/correctness proofs) of having dynamic withdrawal times, wouldn’t it then also make sense to just put this new power right into the hands of users?

---

**atlanticcrypto** (2018-10-18):

Wouldn’t fixed time validator lockups be easier both in implementation and ability to financially model?

You then stop looking like a financial instrument with some undefined duration, and can instead offer 1m, 6m, 12m, 24m validator lockups with market set rates for each timeframe. You could then have two ‘states’ for a validator, active and withdrawing, where 50% (or some ratio) of the time is spent in each - but it is pre-determined.

This would allow a number of things - the market could set rates based upon lockup length - the validator willing to lockup their ETH for 2 years SHOULD be paid more than someone willing to lock it up for 3 months.

This is only different, in theory, from [@drcode1](/u/drcode1)’s suggestion in that it isn’t a pre-defined reward structure based upon time. It becomes more dynamic - the market may perceive a 2 year lockup to have considerably more risk than a 3m lockup.

You could then even have a set reward bucket for each maturity type - and have an excellent understanding of your issuance profile over X timeframe. It could even allow for a more robust monetary policy framework.

---

**vbuterin** (2018-10-19):

You definitely could offer different buckets and offer more returns for the larger buckets, though that’s not especially useful because the security of the system depends on the withdrawal time of the *lowest* 1/3 of the validators, so a few validators having longer lockups than everyone else won’t actually help too much.

The objective of my proposal (2) is to try to target having maximally low withdrawal time *except when it seems like there might be an attack*.

---

**atlanticcrypto** (2018-10-19):

I assume a

100pct long duration validator deposit balance is most secure? Just want to make sure I am not wrong in that.

Couldn’t you just weight the reward for 2y duration higher than for 1m duration? If you have duration buckets like that you might even be able to use participation to identify potential attacks…

Need to think some more on it…

---

**vbuterin** (2018-10-19):

> Couldn’t you just weight the reward for 2y duration higher than for 1m duration? If you have duration buckets like that you might even be able to use participation to identify potential attacks…

You could, but the point is that the *possibility* of 1/3 of validators participating with 1m duration means that the algorithm has no economic security regardless of how long the deposit period of the other 2/3 is.

---

**denett** (2018-10-19):

(2) seems like a good strategy to throttle the outflow at times everybody wants to leave.

I doubt (1) is very effective in managing the size of the deposit pool. Having a unnecessary  large waiting period is basically a unnecessary cost for the depositor. Adjusting the validator rewards seems like a better tool for managing the total deposit pool. If you want to attract more deposits increase the reward, if you have enough deposits, lower the reward.

---

**vbuterin** (2018-10-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/denett/48/2237_2.png) denett:

> Having a unnecessary large waiting period is basically a unnecessary cost for the depositor.

Sure, but it’s a benefit for the protocol and its users, who get to enjoy a longer weak subjectivity period. If you think the benefit is not worth the cost at the 3 month level, then the fix is to lower the weak subjectivity period in an absolute sense (eg. to 3 weeks if we’re keeping a constant period, or reduce the number of withdrawals processed per period from `x` to `x/2` if we’re using that solution).

---

**atlanticcrypto** (2018-10-22):

If validator lockup duration is known (whether through defined duration deposits or some other method), then the network could have a duration seeking function to optimize for some optimal weak subjectivity period (almost like the current PoW difficulty function targeting block time).

For instance, it can always solve for > 67% of deposits to have a duration > 3 months.

It will allow for the market to set rates by duration bucket, guided by an equilibrium seeking function. If there are multiple defined lockup contracts, I believe a market mechanism will do a better job of rewarding duration risk than any arbitrary set of rules. This also solves the question of “What should PoS deposits be paid?” - this rate will change based upon any number of market dynamics, including underlying market sentiment, risk free alternatives, regulatory and technology risks, etc.

The market based mechanism paired with the duration seeking function, I believe, should (over time) minimize the cost per ETH of validator deposits.

Providing a defined duration component should allow for a much more efficient staking system - allowing potential stakers a much cleaner ability to model the economic consequences of choosing to stake versus allocating resources elsewhere (especially in the early stages where there is not a robust lending market).

This is a significantly more complex mechanism, but it may be required to ensure participation is sufficient?

---

**denett** (2018-10-23):

I think the throttle (2) is the best way to control the subjectivity period. But it is difficult to get right, because it is hard to predict the waiting queue length. The queue length depends on the average validator turnover which we don’t know in advance and might change over time. If we set the throttle too tight we get long unpredictable queues. If we set the throttle too loose, there will be no queue, but we miss out on a longer subjectivity period.

So maybe we can adjust the throttle to target a fixed average waiting time of say 1 week. If during the last month the average waiting time was below 1 week, we tighten the throttle. If the waiting time was longer, we loosen the throttle. We can set a lower bound of say 3 month for 33% of the deposit pool, so we have a guaranteed minimal subjectivity period.

I assume the validators are able to vote and earn rewards while in the queue, so the cost of being in the queue is relatively low.

---

**atlanticcrypto** (2018-10-23):

![:point_up:](https://ethresear.ch/images/emoji/facebook_messenger/point_up.png?v=9)![:point_up:](https://ethresear.ch/images/emoji/facebook_messenger/point_up.png?v=9)![:point_up:](https://ethresear.ch/images/emoji/facebook_messenger/point_up.png?v=9)

Agree.

---

**denett** (2018-10-24):

As an alternative to the queue it is possible to auction off the exits. So every period the X validators with the highest bids can withdraw. We can adjust X in a similar manner as proposed above to target an average auction price that could be equal to for example one week of validator rewards. The auction receipts should be burned.

---

**atlanticcrypto** (2018-10-24):

I think it’s cleaner just to have defined duration windows, as you and I both described - with an equilibrium seeking function targeting a 67% deposit duration of X time.

Auctioning off exits is extraneous as soon as there is a robust lending market - then the lending rate should be directly tied to the staking rate.

