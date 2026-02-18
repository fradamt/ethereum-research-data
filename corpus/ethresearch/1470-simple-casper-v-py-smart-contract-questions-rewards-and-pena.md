---
source: ethresearch
topic_id: 1470
title: Simple_casper.v.py Smart Contract Questions - Rewards and Penalties
author: terry.rossi
date: "2018-03-22"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/simple-casper-v-py-smart-contract-questions-rewards-and-penalties/1470
views: 1611
likes: 2
posts_count: 6
---

# Simple_casper.v.py Smart Contract Questions - Rewards and Penalties

Hello,

I am doing a research project focused on Casper FFG. Specifically, I’m trying to understand how validator rewards and penalties are implemented. Could someone help me answer the following questions:

1. It looks like deposit_scale_factor is directly proportional to the total deposit size. Why is this?
2. If deposit_scale_factor is always decreasing, what happens when it is less than 10^-10 (the smallest value supported by the viper decimal type)?
3. Is base_penalty_factor positive or negative, and why?
4. Can someone explain, mathematically, how it is that validators who vote while esf > 2 do not lose any money?
5. Where can we see the values passed initially passed into init()

## Replies

**vbuterin** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/terry.rossi/48/2483_2.png) terry.rossi:

> It looks like deposit_scale_factor is directly proportional to the total deposit size. Why is this?

`deposit_scale_factor` is a variable that is used as a “common factor” in deposits; that is, every validator’s “actual” deposit is `validators[i].deposit_size * deposit_scale_factor`. This is done so that all validators’ deposits can be scaled down by the same factor at the same time by simply updating a single variable.

> If deposit_scale_factor is always decreasing, what happens when it is less than 10^-10 (the smallest value supported by the viper decimal type)?

Casper will break. Think of this as a kind of built-in “ice age” mechanic that requires a hard fork to fix, though it will take thousands of years to actually reach that point.

> Can someone explain, mathematically, how it is that validators who vote while esf > 2 do not lose any money?

Every validator loses some percentage through the decrease to `deposit_scale_factor`, but then get the money back when they get rewarded during the `vote(...)` call.

---

**terry.rossi** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Every validator loses some percentage through the decrease to deposit_scale_factor, but then get the money back when they get rewarded during the vote(…) call.

We understand this at a high level, but are trying to work out the math based on the contract code.

Based on our understanding of the code (lines 273), we have the following relation. Note that we assume for all of this that esf > 2 and therefore there is no collective reward.

 DSF_{i+1}=DSF_{i}\ast(1-RF_{i})

We now want to show that the validator deposit + voting reward subject to  DSF_{i+1}  is equal to the initial validator deposit subject to  DSF_{i} :

 DSF_{i+1 }\ast D \ast (1+RF_{i}) = DSF_{i} \ast D

 DSF_{i+1}\ast(1+RF_{i}) = DSF_{i}

 DSF_{i}\ast(1-RF_{i})\ast(1+RF_{i}) = DSF_{i}

 (1-RF_{i})\ast(1+RF_{i}) = 1

 1-RF_{i}^{2}=1

This result doesn’t make sense, as RF cannot be equal to 0 (see the assert on line 280).

From a mathematical standpoint, how can we verify that every validator who votes when esf > 2 will always offset the deposit scale factor decrease with the voting reward?

---

**vbuterin** (2018-03-24):

That actually is going to be changed; specifically to: DSF_{i+1} = DSF_i * \frac{1 + CVR}{1 + RF_i}, where CVR is the “collective virtue reward” which pays everyone up to half of RF_i the more validators vote.

---

**terry.rossi** (2018-03-24):

This CVR term is the same as what is currently returned by `get_collective_reward()` in the current contract code, correct?

Also, will this CVR term be included in the DSF rescaling for any esf value? The current smart contract code looks to only include the collective reward in the DSF rescaling if esf <= 2 (otherwise the collective reward is 0).

In other words, will this CVR term be non-zero for any esf, or only for esf <= 2?

Further, it seems that the math doesn’t work out here either (assuming the case where esf > 2  (and as a result where CVR is 0):

 DSF_{i+1 }\ast D \ast (1+RF_{i}) = DSF_{i} \ast D

 DSF_{i+1}\ast(1+RF_{i}) = DSF_{i}

 DSF_{i}*\frac{1+RF_{i}}{1-RF_{i}} = DSF_{i}

 \frac{1+RF_{i}}{1-RF_{i}} = 1

Also, in general, what is the reasoning for including the reward factor in the calculation of the new deposit scale factor?

---

**vbuterin** (2018-03-25):

> The current smart contract code looks to only include the collective reward in the DSF rescaling if esf  Further, it seems that the math doesn’t work out here

Oops, you’re right! The denominator should be 1 + RF_i. Fixed.

