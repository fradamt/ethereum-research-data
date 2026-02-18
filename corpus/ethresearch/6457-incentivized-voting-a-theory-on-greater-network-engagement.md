---
source: ethresearch
topic_id: 6457
title: Incentivized Voting - A theory on greater network engagement
author: bgits
date: "2019-11-15"
category: Economics
tags: []
url: https://ethresear.ch/t/incentivized-voting-a-theory-on-greater-network-engagement/6457
views: 1356
likes: 1
posts_count: 1
---

# Incentivized Voting - A theory on greater network engagement

Implementing incentivized voting with voter credits may provide positive utility value to the network stakeholder which should result in more engagement and create a feedback loop that drives more network adoption.

Stakeholder apathy is an issue that has emerged even in networks with votes that have fairly large on-chain consequences.

Part of the reason seems to be that frequent and proper (research and ballot casting/proposals) voting itself is work. At some point people assume (perhaps correctly) that if they don’t vote, the people who have done the work will make the correct decision or that the effort invested by them is not worth the impact on the outcome.

The modern rational voter theory developed by Downs (1957), Tullock (1967), and Riker and Ordeshook (1968) is a framework for analyzing why people vote.

It can be expressed as:

**U = qB − C + T**

Where

**q = the probability voter is pivotal**

**B = Benefits if ballot wins**

**C = cost of voting**

**T = extra benefit of voting**

Through this lens we can see that if B is 0, then no matter how high the probability of a pivotal vote the benefits are still zero and what remains is the cost, making the utility of the vote negative and therefore the voter will simply not vote.

While quadratic voting impacts (q), the way it is implemented today does not as there is no practical way to enforce identity in a vote of an open community.

A possible way to implement some of quadratic voting is to focus on voting credits - being able to defer voting for future benefits. Impacts (q)

Incentivization increases T, by making U positive it should lead to greater participation. In order to prevent possible bad decision making, the default should be **DEFER_VOTES** so as not to force a decision from voters, they will only choose another option when it increases the utility of their vote. The act of participation itself should increase stakeholder awareness and incentivize self education.

Tracking the **DEFER_VOTES** overtime will enable seeing if incentivization is a strategy that increases voter awareness and provides insight in to the quality of the polls.

Incentivization also serves the purpose of boosting polls. If no money has been put into backing a poll this conveys little confidence in the importance of the poll. Although in another designs the same amount maybe put into each poll if the funds are from allocating network fees in which case some other process needs to exist to boost proposed polls and make them eligible for a vote.

**Engagement Theory**

The [Hooked model](https://www.amazon.com/dp/B00LMGLXTS/ref=cm_sw_r_tw_dp_U_x_GIXZDb7RKD261) helps build habit-forming products, that prompt users to return and use those products over and over again, without depending on costly advertising or aggressive messaging.

Instead of using the model to form bad habits (ie: casino gambling and endless social media scrolling) we can use it to help form good habits (participation in the governance of a public good)

**[![](https://ethresear.ch/uploads/default/optimized/2X/8/8c2c1cc30f7f18dcf4075c97f70850614034187d_2_519x356.jpeg)1600×1100 224 KB](https://ethresear.ch/uploads/default/8c2c1cc30f7f18dcf4075c97f70850614034187d)**

In this model the external triggers are: **notifications of polling open and polling closed.**

The action is: **checking the polls**

Variable rewards: **Monetary rewards from incentive funding and winning ballots.**

*These fit variable rewards because the user can not know in advance the exact amount of reward or if they will win the ballot.*

Investment: **Claiming rewards, Accumulating vote credits, Voting**

Claiming rewards increases the user’s stake in the network(when it is token based voting and the reward is the same token) giving them potentially larger claims and voting power in the next vote and compounding out to future votes.

Accumulating votes is an investment that the user can then use giving them more reason to check up on future votes.

If they voted they will want to see the outcome of the vote to claim their rewards and even more so when the vote outcome has a benefit to them.

**Example**

***Funding a pool for each vote and allowing each voter to claim a proportional amount of the funds in the pool***

Each voter would be able to receive a payout according to:

**POOL_SIZE X AMOUNT_VOTED / TOTAL_AMOUNT_VOTED**

There are 10 polls with 1 million ballots being cast in each vote. Alice is a voter with 100,000 Tokens. 5 of the polls benefit alice if they win and 5 she is indifferent to. For simplicity we will use binary values as precisely estimating these variables requires further investigation.

**CONSTANTS**

**B** = 5 ( 5 benefits + 5 no benefits)

**C** = 10 (voting in each poll has a cost)

**Scenario 1 - No Incentivization, no voting credits:**

q = 1/10 (100,000 / 1mm tokens)

**U** = **-9.5** (1/10*5 - 10)

**Scenario 2 - Incentivization, no voting credits:**

q = 1/10 (100,000 / 1mm tokens)

T = 10

**U = 0.5** (1/10*5 - 10 + 10)

**Scenario 3 - Incentivization and voting credits:**

q = 2/10 (200,000 / 1mm tokens)

T = 10

**U = 1** (2/10*5 - 10 + 10)

**Scenario 4 - No incentivization and voting credits:**

q = 2/10 (200,000 / 1mm tokens)

**U = -9** (2/10*5 - 10)

Of the scenarios presented above only no incentive votes have negative utility for the voter while combining incentive funding with voter credits has the highest.
