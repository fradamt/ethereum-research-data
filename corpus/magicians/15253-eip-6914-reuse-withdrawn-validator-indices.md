---
source: magicians
topic_id: 15253
title: "EIP-6914: Reuse Withdrawn Validator Indices"
author: dapplion
date: "2023-07-27"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-6914-reuse-withdrawn-validator-indices/15253
views: 1927
likes: 1
posts_count: 5
---

# EIP-6914: Reuse Withdrawn Validator Indices

Discussion thread for EIP-6914

https://github.com/ethereum/EIPs/pull/6914

## Replies

**dapplion** (2023-07-27):

I would like to dispute the concern over data complexity to handle AttesterSlashings with pubkeys.

The maximum data increase in blocks due AttesterSlashing using pubkeys instead of indexes (for networks with more than 262144 validators, with 2 AttesterSlashing per block, 2 IndexedAttestations per AttesterSlashing)

```auto
(48 - 8) * (validator_count / 32 / 64) * 2 * 2
```

| validator_count | block size increase |
| --- | --- |
| 500,000 | 39kB |
| 1,000,000 | 78kB |
| 1,500,000 | 117kB |
| 2,000,000 | 156kB |

Considering that the network only has to handle this data load for sustained periods of time, in exceptional circumstances it does not sound unreasonable. Experiments motivated for eip4844 have shown that the network is perfectly capable of handling this data load.

---

**dapplion** (2023-11-23):

Wrote some thoughts on the question to adopt the EIP or just use an engineering approach.

TLDR

- Is unbounded beacon state growth actually a problem? Long term yes
- Can it be solved with engineering solutions (no EIP)? Not entirely
- Should we adopt EIP-6914? Maybe, in several years


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/@dapplion/eip6914)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Beacon chain today experiences unbounded growth. There is no mechanism to prune validators in any circumstance, and new deposits can append validator records in perpetuity. Note that the maximum possible number of active validators is bounded by the...

---

**xrchz** (2024-04-06):

I recognise that you note the ecosystem consideration of breaking the ability to identify validators by index. I just want to add an additional bid for not breaking this, or at least taking the cost into account. Applications relying on one-index-one-validator will, if this EIP is adopted, need to run a migration of their state. This may be costly and error prone especially if they are based on historical/archive data. (This is in addition to the ongoing relative space cost of using pubkeys instead afterwards.)

---

**grogo** (2025-04-23):

[@dapplion](/u/dapplion)

Is this EIP still considered? I saw it got marked as stagnant by a bot.

We are now doing some decisions in SSV protocol and we were wondering if you may later break us.

