---
source: ethresearch
topic_id: 15547
title: Removing Unnecessary Stress from Ethereum's P2P Network
author: adiasg
date: "2023-05-10"
category: Networking
tags: []
url: https://ethresear.ch/t/removing-unnecessary-stress-from-ethereums-p2p-network/15547
views: 3942
likes: 19
posts_count: 5
---

# Removing Unnecessary Stress from Ethereum's P2P Network

# Removing Unnecessary Stress from Ethereum’s P2P Network

Ethereum is currently processing 2x the number of messages than are required. The root cause of this unnecessary stress on the network is the mismatch between the number of validators and the number of distinct participants (i.e., staking entities) in the protocol. The network is working overtime to aggregate messages from multiple validators of the same staking entity!

We should remove this unnecessary stress from Ethereum’s p2p network by allowing large staking entities to consolidate their stake into fewer validators.

**Author’s Note:** There are other reasons to desire a reduction in the validator set size, such as [single-slot finality](https://notes.ethereum.org/@vbuterin/single_slot_finality#What-are-the-issues-with-validator-economics). I write this post with a singular objective - to reduce unnecessary p2p messages - because it’s an important maintenance fix irrespective of other future protocol upgrades such as single-slot finality.

---

**tl;dr** – steps to reduce unnecessary stress from Ethereum’s network:

- Investigate the risks of having large variance in validator weights
- consensus-specs changes:

Increase MAX_EFFECTIVE_BALANCE
- Provide one-step method for stake consolidation (i.e., validator exit & balance transfer into another validator)
- Update the withdrawal mechanism to support partial withdrawals when balance is below MAX_EFFECTIVE_BALANCE

Build [DVT](https://github.com/ethereum/distributed-validator-specs) to provide resilient staking infrastructure

---

## Problem

Let’s better understand the problem with an example:

[![image](https://ethresear.ch/uploads/default/optimized/2X/c/cbd3ad04bff02b4c40169724aef85508f962f0af_2_215x249.png)image858×995 63.7 KB](https://ethresear.ch/uploads/default/cbd3ad04bff02b4c40169724aef85508f962f0af)

Each validator in the above figure is controlled by a distinct staker. The validators send their individual attestations into the Ethereum network for aggregation. Overall, the network processes 5 messages to account for the participation of 5 stakers in the protocol.

The problem appears when a large staker controls multiple validators:

[![image](https://ethresear.ch/uploads/default/optimized/2X/d/d8465ea65ff6562766b9d2b77c1908aa9efdb611_2_224x250.png)image882×983 57.9 KB](https://ethresear.ch/uploads/default/d8465ea65ff6562766b9d2b77c1908aa9efdb611)

The network is now processing 3 messages on behalf of the large staker. As compared to a staker with a single validator, the network bears a 3x cost to account for the large staker’s participation in the protocol.

Now, let’s look at the situation on mainnet Ethereum:

[![image](https://ethresear.ch/uploads/default/optimized/2X/7/7fd26820f2573b8a770d52f905bd2dcc9e02ea86_2_289x250.png)image713×615 68.8 KB](https://ethresear.ch/uploads/default/7fd26820f2573b8a770d52f905bd2dcc9e02ea86)

About 50% of the current 560,000 validators are controlled by 10 entities **[source: [beaconcha.in](https://beaconcha.in/charts/pools_distribution)]**. Half of all messages in the network are produced by just a few entities - meaning that we are processing 2x the number of messages than are required!

Another perspective on the unnecessary cost the network is bearing: the network spends half of its aggregation efforts towards attestations produced by just a few participants. If you run an Ethereum validator, half your bandwidth is consumed in aggregating the attestations produced by just a few participants.

The obvious next questions – ***Why do large stakers need to operate so many validators? Why can’t they make do with fewer validators?***

### MAXIMUM_EFFECTIVE_BALANCE

The [effective balance](https://github.com/ethereum/consensus-specs/blob/01b53691dcc36d37a5ad8994b3a32d8de69fb1aa/specs/phase0/beacon-chain.md#validator) of a validator is the amount of stake that counts towards the validator’s weight in the PoS protocol.

[MAXIMUM_EFFECTIVE_BALANCE](https://github.com/ethereum/consensus-specs/blob/01b53691dcc36d37a5ad8994b3a32d8de69fb1aa/specs/phase0/beacon-chain.md#gwei-values) is the maximum effective balance that a validator can have. This parameter is currently set at `32 ETH`. If a validator has a balance of more than `MAXIMUM_EFFECTIVE_BALANCE`, the excess is not considered towards the validator’s weight in the PoS protocol.

PoS protocol rewards are proportional to the validator’s weight, which is cappped at the `MAXIMUM_EFFECTIVE_BALANCE`, so a staker with more than 32 ETH is forced to create multiple validators to gain the maximum possible rewards.

***This [protocol design decision](https://notes.ethereum.org/@vbuterin/serenitydesignrationale#Why-32-ETH-validator-sizes) was made in preparation for shard committees (a feature that is now obsolete) and assuming that we have an entire epoch for the hearing from the entire validator set. Since then, Ethereum has adopted a rollup-centric roadmap, which [does not require](https://notes.ethereum.org/@vbuterin/singleslotfinality#What-are-the-issues-with-validator-economics) this constraint!***

## Solution: Increase MAXIMUM_EFFECTIVE_BALANCE

[![image](https://ethresear.ch/uploads/default/optimized/2X/3/3da85b880ae0f37f7f17e937de51b2bb498d47c1_2_202x250.png)image785×969 53.1 KB](https://ethresear.ch/uploads/default/3da85b880ae0f37f7f17e937de51b2bb498d47c1)

Increasing `MAX_EFFECTIVE_BALANCE` would allow these stakers to consolidate their capital into far fewer validators, thus reducing the validator set size & number of messages. Today, this would amount to a 50% reduction in the number of validators & messages!

### Sampling Proposers & Committees

The beacon chain picks [proposers](https://github.com/ethereum/consensus-specs/blob/01b53691dcc36d37a5ad8994b3a32d8de69fb1aa/specs/phase0/beacon-chain.md#compute_proposer_index) & [committees](https://github.com/ethereum/consensus-specs/blob/01b53691dcc36d37a5ad8994b3a32d8de69fb1aa/specs/phase0/beacon-chain.md#compute_committee) by random sampling of the validator set.

The sampling for proposers is weighted by the effective balance, so no change is required in this process.

However, the sampling for committees is not weighted by the effective balance. Increasing `MAXIMUM_EFFECTIVE_BALANCE` would allow for large differences between the total weight of committees. An open research question is whether this presents any security risks, such as an increased possiblity of reorgs. If so, we would need to change to a committee sampling mechanism that ensures roughly the same weight for each committee.

### Validator Exit & Transfer of Stake

Currently, the only way to consolidate stake from multiple validators into a single one is to withdraw the stake to the Execution Layer (EL) & then top-up the balance of the single validator.

To streamline this process, it is useful to add a Consensus Layer (CL) feature for exiting a validator & transferring the entire stake to another validator. This would prevent the overhead of a CL-to-EL withdrawal and make it easier to convince large stakers to consolidate their stake in fewer validators.

### Partial Withdrawal Mechanism

The current [partial withdrawal mechanism](https://github.com/ethereum/consensus-specs/blob/01b53691dcc36d37a5ad8994b3a32d8de69fb1aa/specs/capella/beacon-chain.md#is_partially_withdrawable_validator) allows validators to withdraw a part of their balance without exiting their validator. However, only the balance in excess of the `MAX_EFFECTIVE_BALANCE` is available for partial withdrawal.

If the `MAX_EFFECTIVE_BALANCE` is increased significantly, we need to support the use case of partial withdrawal when the validator’s balance is lower than the `MAX_EFFECTIVE_BALANCE`.

### Resilience in Staking Infrastructure

A natural concern when suggesting that a large staker operate just a single validator is the reduction in the resilience of their staking setup. Currently, large stakers have their stake split into multiple validators running on independent machines (I hope!). By consolidating their stake into a single validator running on one machine, they would introduce a single point of failure in their staking infrastructure. An awesome solution to this problem is [Distributed Validator Technology (DVT)](https://github.com/ethereum/distributed-validator-specs), which introduces resilience by allowing a single validator to be run from a cluster of machines.

## Replies

**flubdubster** (2023-05-11):

There is an additional, imho extremely important, argument to increase MAXIMUM_EFFECTIVE_BALANCE: The current max. favors stake-pools over home-stakers as with withdrawals activated, Pools can easily withdraw all stake >32ETH and spin up additional validators. Even taking into account Pool-Fees, a large number of Home-Staker currently make **less** APY compared to staking their ETH with a pool. By increasing the MAXIMUM_EFFECTIVE_BALANCE, home-stakers with only 1 or 2 validators would get access to re-compounding of stake as well.

As compounding would affect the staking rewards economics an extensive analysis on the economics should get done.

---

**spacetractor** (2023-05-11):

There needs to be an analysis on the effects on the churn rate and how deposits/exits are constructed/limited. The churn limit has to be mechanically revamped to handle a change like this proposal. Can’t allow 20% of the stake to leave the network instantaneously.

Some arguments why large validators wouldn’t want to consolidate even if they have the option:

Slashing risk: It’s easier to mitigate large slashing events, i.e. script that shuts down all validators if one get slashed.

Funding for LSTs: Easier to pull out a couple of smaller eth validators to meet exit funding, than to exit full stake and then have to restake with 80-90% of the collateral again

Would love to see more counter arguments, these are just a few on top of my head.

---

**pepesza** (2023-05-11):

> Would love to see more counter arguments

- This increases effectiveness (defined as bandwidth per ETH staked) for large players - an additional minor centralization vector.
- This introduces additional complexity.
- Available bandwidth is likely to be a resource that will grow in future (“Nielsen’s Law of Internet Bandwidth”).

---

**JosepBove** (2023-09-21):

![](https://ethresear.ch/user_avatar/ethresear.ch/pepesza/48/628_2.png) pepesza:

> lable bandwidth is likely to be a resource that will grow in future

I completely agree with you hare, however internet might be one of the key differences between world regions. Most of them can have a good internet connection but some areas that are far from very big cities can maybe have bandwidth problems. I really think that the proposal does not harm, however we need to do more research on the risks that this could add to the ethereum protocol.

Is there any update on this front? [@adiasg](/u/adiasg)

