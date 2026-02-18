---
source: ethresearch
topic_id: 10400
title: Exit/entry queue clogging after withdrawals are enabled
author: vshvsh
date: "2021-08-23"
category: The Merge
tags: []
url: https://ethresear.ch/t/exit-entry-queue-clogging-after-withdrawals-are-enabled/10400
views: 7042
likes: 46
posts_count: 17
---

# Exit/entry queue clogging after withdrawals are enabled

After the beacon chain will enable withdrawals, both exit and entry queues will clog for multiple months, maybe forever. The reasons for that, besides the genuine desire to stake/unstake:

1. stake compounding
2. key rotation

Both of these don’t have to involve changing the validator set, and shouldn’t clog the queue. The clog can be greatly reduced by adopting additional features to allow key rotation and skimming off the rewards.

## Compounding stake in the beacon chain

To make the most out of your stake, you must run  `(your total amount of ETH)/32` validators. If you deposit 32 validators at 32 ETH each and after half a year each of them earns 1 ETH of rewards, to get the most out of your stake you need to get the 32 ETH of rewards off them and start a new validator.

By current spec, the only way to do it is to unstake all of your validators and redeposit 33 of them (that’s disregarding fees).

When withdrawals are enabled, there will be hundreds of thousands of validators (conservatively - 300000 of them) with a good number of rewards that would want to compound their stake.

With current settings, that would clog the exit/entry queue for 10 months, and in that time the rest of the validators, including freshly deposited, will get more stake on them, driving the next wave of compounding and so on. Most likely the eventual equilibrium here is a permanent clog of a few weeks on both queues.

Note that these withdrawals/deposits are not “real” in the sense that people doing them do not wish to change the validator set - they just want to skim and restake the rewards.

That can be amended with an EIP to “skim” the rewards - partial withdrawal of validator’s balance over 32 ETH. That way compounding is still possible but there’s no need to exit/reenter for a validator, and there’s no stress on queues.

## Key rotation

Beacon chain had been launched with key handling infra that is much less mature than today. Some people would want to rotate both their withdrawal credentials and validation keys to a different setup. That will be especially important when the time of secret-shared validators established via distributed key generation will come.

By current spec, the only way to rotate any of them is through withdrawal and restaking. It’s impossible to give an informed estimation of how many validators that is, but I know it’s at least 18000 of Lido’s validators.

That too can be rectified with an EIP.

## What do

I think the best way forward would be:

1. Extend 0x3 withdrawal credentials with a generalized message relay that would allow building a number of features for beacon chain by using existing execution layer fees mechanisms for spam protection. Fees can be amplified on the execution layer with custom smart contract logic. Alternatively, rate limits can be imposed.
2. Make a “skim rewards” message using this mechanism that would make a withdrawal of rewards over 32 ETH from the validator to the withdrawal credentials. If execution environment tx fees seem inadequate for spam prevention, additional application-level fees or rate limits can be imposed.
3. Adopt a withdrawal credential rotation solution, e.g. [1], [2], or [3].

Validator key rotation is also often desired by node operators, but it is a much more nuanced topic. It can represent actual validator churn, not a routine security operation, and some uses of it should be subject to exit/entry queues, so this operation should be handled with care. There’s a proposal to implement it via adding a new kind of message in consensus layer and a new kind of credentials [[4](https://ethresear.ch/t/adding-pos-validator-key-changes/9264)].

Based on feedback, I’ll try to get the ball rolling in that direction. I believe that clogging the queues for months is undesirable (though not critical), and should be avoided if possible.

## Replies

**vbuterin** (2021-08-23):

I also have my own key rotation suggestion:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Adding PoS validator key changes](https://ethresear.ch/t/adding-pos-validator-key-changes/9264) [Proof-of-Stake](/c/proof-of-stake/5)



> One feature that would be nice to add to eth2 would be the ability for a validator to switch their staking key. This is nice because it would allow a form of de-facto “delegation” where validators give their staking keys to a pool, and if the pool misbehaves or starts to have a high risk of misbehaving they can quickly switch the key to a different pool or to a self-hosted key, without any downtime. Currently, switching keys requires one withdraw → re-deposit cycle, incurring a minimum of 27 hou…

Skimming (I think we’ve called it “partial withdrawals” before or something like that) does make sense and seems very useful.

---

**vshvsh** (2021-08-23):

I think [@djrtwo](/u/djrtwo) proposed it before but couldn’t find the exact place.

---

**darcys22** (2021-08-23):

Is there any particular reason why a validator would need greater than 32 eth? Could the skimming be an automatic transaction

---

**XofEE** (2021-08-23):

Yes I think valiators who want to withdraw their ETH to stake it again will clog the queue constantly.

I had thought about a system (maybe too complex) to put some validator to sleep. This solved the complexity of having too many validators. In this case, only sleeping validators can perform operations such as partial withdrawal.

**[Active Validator Cap to improve Downtime Management](https://ethresear.ch/t/active-validator-cap-to-improve-downtime-management/9422)**

---

**vshvsh** (2021-08-23):

It’s a good idea IMO. The only reason to have >32eth balance is to be sure you stay live for longer if you go offline but it’s not a very realistic desire.

A way to make this automatic *and* not particularly hard load for a chain is when you make a block and have a balance over 32.5 eth skimming happens automatically.

---

**TobesVibration** (2021-08-23):

Hi, I am a node validator and would be grateful to add an opinion to this subject.

Is there a way we can validate our identities to our nodes in case our keys have been breached, similar to the warning that was just voiced by Cyber Polygon conference 2021, what I am talking about is adding a protocol that stops a bad actor from using a breached withdrawal key. I have a couple of ideas but have been a bit worried about public discussion boards in case the info becomes valuable to the bad actors.

I have two ideas, I have discussed one of those with [@timbeiko](/u/timbeiko) and the other is in my head, I have tagged Tim in case he would prefer I keep that discussion private. I only have two nodes but I am concerned not just for breached keys but also if the intent of the bad actor is not to steal the ETH but to harm the Ethereum Foundation. Tobes

---

**alonmuroch** (2021-08-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> It’s a good idea IMO. The only reason to have >32eth balance is to be sure you stay live for longer if you go offline but it’s not a very realistic desire.
>
>
> A way to make this automatic and not particularly hard load for a chain is when you make a block and have a balance over 32.5 eth skimming happens automatically.

Effective balances goes down in steps so it shouldn’t be an issue to stay at 32.



      [github.com](https://github.com/ethereum/consensus-specs/blob/15a6c48a469fd12107cfe74d8cce70df2049e57a/specs/phase0/beacon-chain.md#effective-balances-updates)





####



```md
# Phase 0 -- The Beacon Chain

## Table of contents

- [Introduction](#introduction)
- [Notation](#notation)
- [Custom types](#custom-types)
- [Constants](#constants)
  - [Misc](#misc)
  - [Withdrawal prefixes](#withdrawal-prefixes)
  - [Domain types](#domain-types)
- [Preset](#preset)
  - [Misc](#misc-1)
  - [Gwei values](#gwei-values)
  - [Time parameters](#time-parameters)
  - [State list lengths](#state-list-lengths)
  - [Rewards and penalties](#rewards-and-penalties)
```

  This file has been truncated. [show original](https://github.com/ethereum/consensus-specs/blob/15a6c48a469fd12107cfe74d8cce70df2049e57a/specs/phase0/beacon-chain.md#effective-balances-updates)

---

**alonmuroch** (2021-08-23):

I like the approach of using generalized message relay that costs gas on the execution layer to trigger things on the consensus layer.

Skimming IMO is very important and useful, both for the network(more ETH @ stake)  and the individual user.

Key rotation is a bit trickier. With the eth address withdrawal credentials we’ve enabled ownership of the assets to be dynamic but the validating “service” (if you will) to remain static. That is you can chose where your sake will go to but not who operates your validator.

Key rotation is for the validation key which then brings the question of what types of use cases will need such a thing?

Use case 1) Most stake is in pools, in which case you can’t rotate the validation keys as nothing guarantees the staker has 32 ETH validators (can have more or less). De facto there is a separation between the validator key ownership and the method by which ETH ownership is managed.

You could think of a settlement protocol between staking services in which if 32X tokenized stake ETH was moved from service A to service B then A also rotates X validation keys to service B.

Use case 2) There are staking services which allow only 32ETH batches in which case rotation might be useful if a user wants to completely leave the service but still continue staking.

Use case 3) An SSV type setup where the validation key is offline but shares of it exist at different operators, key rotation in this case makes it much easier to switch operators whenever the user wants to.

---

**vshvsh** (2021-08-24):

One possible use for validator key rotation is switching to DKG SSV without going through restaking ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**lsankar4033** (2021-08-25):

specific features aside, spec-ing out a generalized message relay (i.e. contract methods/events/how they’d be interpreted in clients) seems valuable sooner rather than later

---

**vshvsh** (2021-08-26):

Hopefully can get out the draft next week.

---

**alonmuroch** (2021-09-02):

I very much agree with this approach!

---

**samueldashadrach** (2021-09-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vshvsh/48/5489_2.png) vshvsh:

> that would clog the exit/entry queue for 10 months

I don’t have a stance on the proposal itself but this feels incorrect. I can’t imagine why someone would want to lose 10 months of rewards to get rewards from a new validator. If 20 validators need to exit and re-enter (cycle) to get 1 new validator, then 1 month of wasted time in the entry queue for those 20 validators means the new validator needs to be staking for 20 months to recoup this loss (assuming constant yield). Even doubling the queue length to 2 months means the new validator needs to run for 40 months to recoup the lost rewards from cycling.

So even if this proposal is not implemented, entry queue length shouldn’t exceed 1-2 months atleast due to such cycling reasons.

---

**vshvsh** (2021-09-29):

My wording was unclear: I expect the queues to be (back of a napkin calc) more than a month-long, and that state of queues to continue for 10 months due to just rewards cycling reasons.

---

**vshvsh** (2021-09-29):

Also, heads up: draft of a proposal for generic message queue from execution layer to consensus layer: [Generalized message bus for exection layer to consensus layer communication - HackMD](https://hackmd.io/@lido/BkiOdwcmK)

---

**ehariton** (2021-11-12):

Thanks for bringing this issue up. I’ve been worried about it for some time ever since I saw several web-based compounding staking calculators and I couldn’t understand how ETH could be compounded without entering/exiting. Clogging entry/exit queue for 10 months would be horrible, and by the time that clog was over, you’d have a new wave of people that had earned enough ETH in rewards during that 10 months to clog again.

I’d like to see a system where staking rewards could be allocated to a designated address so they could either be spent (aka live off the interest) or staked once you’ve accumulated enough.

