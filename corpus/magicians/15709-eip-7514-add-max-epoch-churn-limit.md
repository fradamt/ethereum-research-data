---
source: magicians
topic_id: 15709
title: "EIP-7514: Add max epoch churn limit"
author: dapplion
date: "2023-09-07"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7514-add-max-epoch-churn-limit/15709
views: 3015
likes: 4
posts_count: 5
---

# EIP-7514: Add max epoch churn limit

Discussion thread for EIP-7514



      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7514)





###



Modify the churn limit function to upper bound it to a max value

## Replies

**adietrichs** (2023-09-13):

I personally think this is a very important proposal. For one, it gives CL clients more time to prepare for the increase in load from a larger validator set (and/or for us to ship some upgrade that helps with that, like MaxEB).

More importantly though (at least to me), it also gives us more time to formulate a concrete plan for where we want long term staking dynamics to go (~100% staked? <50% staked? how to deal with LSTs? etc). Potentially required changes to the staking model are much easier to make while we are not yet in a different equilibrium (say, close to 100% staked).

While this EIP doesn’t address any of the underlying issues, it does give us more breathing room. For that reason, I would personally strongly be in favor of inclusion into Dencun (and a Dencun rollout asap, ideally by the end of the year), with an aggressive value for `MAX_PER_EPOCH_CHURN_LIMIT` of 8 or lower.

---

**_pm** (2023-09-14):

The issue is not amount of validators, it’s terrible validator creation UX. If you want to reduce strain in beacon chain, just implement the max effective stake increase from 32 eth to 4096 eth. Min stake could be kept at 32. This was described in [FAQ on EIP-7251; Increasing the MAX_EFFECTIVE_BALANCE - HackMD](https://notes.ethereum.org/@mikeneuder/eip-7251-faq)

That improvement alone would reduce validator count ten-fold, probably more. We’ll get from 800k to 80k validators easily, if proper incentives are implemented.

EIP7514 risks have been described by Vitalik in [Paths toward single-slot finality - HackMD](https://notes.ethereum.org/@vbuterin/single_slot_finality#Idea-2-validator-set-size-capping)

---

**NatPDeveloper** (2023-10-03):

I am curious if technical specifics have, or can be, provided about the increase in gossip traffic due to an increase in validators.

If traffic is limited to propagation of transactions, blocks, attestations, etc, in my mind this is already limited. In addition to this, the p2p list can be set per validator so they are not receiving the same information from multiple sources.

Thank you.

---

**poojaranjan** (2023-11-09):

A conversation with [@dapplion](/u/dapplion) on [EIP-7514: Add Max Epoch Churn Limit](https://youtu.be/URQZVqgKZI4)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/4/497f4eb6cdaf9d1d3171b9524ad939e456f2c7d9.jpeg)](https://www.youtube.com/watch?v=URQZVqgKZI4)

