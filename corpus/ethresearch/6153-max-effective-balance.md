---
source: ethresearch
topic_id: 6153
title: Max_effective_balance
author: jgm
date: "2019-09-17"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/max-effective-balance/6153
views: 1312
likes: 1
posts_count: 1
---

# Max_effective_balance

Is there a particular reason that `MAX_EFFECTIVE_BALANCE` is set to 32 ETH?  This appears to punish well-behaved and long-running validators whose accounts gain funds but are capped at using 32 ETH as their base for further rewards.

I can understand the idea that we don’t want a single validator with lots of ETH in it, but in that case wouldn’t it be fairer to set `MAX_EFFECTIVE_BALANCE` to 64 ETH rather than 32, as it then tops out at the point that another validator could be created?

(Although at current `MAX_EFFECTIVE_BALANCE` is somewhat overloaded in that it is also used to ascertain when validators can be activated and how much can be transferred out of an active validator so if this change were implemented there would need to be two parameters rather than the current one).
