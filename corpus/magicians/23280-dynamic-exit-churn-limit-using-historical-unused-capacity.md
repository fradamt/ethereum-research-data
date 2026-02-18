---
source: magicians
topic_id: 23280
title: Dynamic Exit Churn Limit Using Historical Unused Capacity
author: mikeneuder
date: "2025-03-27"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/dynamic-exit-churn-limit-using-historical-unused-capacity/23280
views: 93
likes: 0
posts_count: 1
---

# Dynamic Exit Churn Limit Using Historical Unused Capacity

Discussion topic for [EIP-XXXX](https://github.com/ethereum/EIPs/pull/9552): “Dynamic Exit Churn Limit Using Historical Unused Capacity”

## Abstract

This EIP proposes updating Ethereum’s validator exit churn calculation by dynamically adjusting the churn limit at the start of each 256-epoch period (“generation”) based on historical validator exits. Specifically, the maximum churn allowed in each generation will adjust according to the unused churn from the past 16 generations. This approach reduces validator wait times during periods of high exit demand *without sacrificing network safety*.

## Motivation

Ethereum currently implements a fixed, rate-limited queue for validator exits to ensure the security and stability of the network. The exit queue ensures the economic security of transactions finalized by the validator set. Suppose a malicious validator could immediately exit the set without any delay. In that case, they may attempt to execute a double spend attack by publishing a block while withholding a conflicting block, which they release after their stake has exited the protocol. The slashing mechanism can no longer hold the malicious validator accountable, and two conflicting finalized transactions may exist (if the attacker has 1/3 of the total stake and successfully splits the 2/3 honest majority in half).

The `CHURN_LIMIT_QUOTIENT=2^16` was selected according to the rough heuristic that it should take approximately one month for 10% of the stake to exit. With 1,053,742 validators, we have a churn limit of 16 exits per epoch. 225 epochs per day $\implies$ 3600 exits per day $\implies$ 108,000 exits per 30 days. Then 108,000/1,053,742 $\approx$ 0.10. We can interpret this as “*the economic security of a finalized transaction decreases by no more than 10% within one month*.”

Another way of understanding the 16 exits per epoch security model is that it encodes the following constraints around validator exits:

1. at most 16 validators exit in the next one epoch, and
2. at most 32 validators exit in the next two epochs, and
3. at most 48 validators exit in the next three epochs, and
…
4. at most 16 $\cdot$ n validators exit in the next n epochs.

While these constraints are simple to understand, the fixed per-epoch churn limit can result in unnecessarily long validator withdrawal delays during periods of higher-than-average exit demand, such as during institutional liquidations or market events. We argue that we should choose a *single* constraint from the above set and implement that flexibly.

We illustrate this with an example. With one million validators, the current protocol specifies that 16 validators may exit per epoch. Over two weeks, this corresponds to 50,400 exits. This translates directly to “no more than 5.04% of the validators (equiv. stake) can exit within two weeks.” Now imagine that in the past 13 days, no validators have exited the protocol, and thus, none of the two-week churn limit has been used. If a large staking operator with 3% of the validator set (30,000 validators) seeks to withdraw immediately, they should be able to – this doesn’t violate the two-week limit of 5.04%. However, since only 16 exits can be processed per epoch moving forward, they are forced to wait 1875 epochs (equiv. 8.33 days).

> Key observation: If we enable the protocol to look backward at the exit history, we no longer need the per-epoch limit looking forward.

For example, say we chose the following constraint explicitly:

> Proposed weak subjectivity constraint: No more than 50,400 exits in two weeks.

Then, we only need to ensure that the constraint is honored over every rolling two-week period without setting a hard cap on exits during every epoch. A dynamically adjusted churn limit based on historical validator exit data allows Ethereum to flexibly accommodate spikes in exit demand while *preserving the same security over every two-week period*. By calculating the unused churn capacity of recent generations, we can safely increase the churn limit when the network consistently operates below capacity, significantly improving the validator exit experience.

#### Update Log

> 2025-03-25: PR Opened
>
>
> Fill in the log for the EIP’s initial draft below:

- yyyy-mm-dd: initial draft

#### External Reviews

None as of 2025-03-26.

#### Outstanding Issues

None as of 2025-03-26.
