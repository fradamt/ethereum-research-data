---
source: ethresearch
topic_id: 1346
title: Gastoken.io showed a flaw in gas design (refund function). Refund should be function of the time spent in the storage
author: dhadrien
date: "2018-03-09"
category: Economics
tags: []
url: https://ethresear.ch/t/gastoken-io-showed-a-flaw-in-gas-design-refund-function-refund-should-be-function-of-the-time-spent-in-the-storage/1346
views: 1588
likes: 2
posts_count: 5
---

# Gastoken.io showed a flaw in gas design (refund function). Refund should be function of the time spent in the storage

Gas is supposed to be linked to cost of computation + storage.

But computation is a one time energy cost whereas storage is a cost per unit of time.

Without a gas refund function, it can work well since you can say that Gas = Computation power + Cost of storage for lifetime.

But if you introduce refund and you break the ‘lifetime’, you need to make sure that amount of gas refunded is a function of (Time of refund - Time of initial storage) otherwise the consistence of gas is broken. (You’re mixing apples and carrots)

## Replies

**yhirai** (2018-03-12):

Is there a no-risk arbitrage?

---

**3esmit** (2018-03-12):

You also clean the storage for lifetime… Gas refunds actually only reduce the total amount you need to pay, you not going to get ether back from an execution.

---

**dhadrien** (2018-03-12):

So my reasoning is that:

If you store data for 1 year ( costs X Gas) and then refund it via the storage refund function (Y gas)

or

If you do the exact same tx (costs X Gas) and then 1 month later refund it via the storage refund function, (Y’ Gas)

Currently Y = Y’

Which means that in some use cases ([gatstoken.io](http://gatstoken.io) for instance) you have the incentive to store as much data as early as you can, since part of the gas you spent to store data is partly refundable and this potential gas refund is constant overtime (its value it terms of refundable gas does not decrease).

1. Storing data onchain is like charging a battery, storing a potential energy, the tx has a one-time non recoverable cost (C+: the computational part of the gas spent that will never be recovered).
2. Using the refund storage function is like using this battery, spending the potential energy, it has also a one-time cost (C-: the gas spent on unlocking this data)
3. Between 1 and 2, it is free from a User perspective, whether 1 week or 2 years happen between the first two steps, the ethereum user has access to the same amount of gas refunded. (The battery is perfectly storing its potential energy for no cost)

BUT, for miners, the cost of maintaining this battery (i.e having a large storage EVM) is not free. Maintaining this storage 2 years or 1 month is different cost.

So from a miner perspective:

my revenue is :

C+ (gas received from computing the first step) + C- (gas received from computing the second step) + X (gas received to store the initial data) - Y (gas refunded to delete the data) = constant

my costs are:

- Computation costs of (C+ and C-), constant
- Maintaining the storage which increases over time.

Imho, it would make much more sense to have a system such as:

A block, b=b0, to store data A for life (let’s say life == 30m blocks), it costs X Gas.

A block b=b1, If you delete this data, you are refunded  (X*(1-(b1-b0)/(30*10e^6)) (doubt the linear function is the most optimal, but you see the idea)

OR: just remove the refund of gas for storage deletion

Otherwise, the gas concept is kinda broken and as a miner, I would not mine storage refunding transactions since it incentives people to play against me by storing in advance a lot of useless storage on which I’ll have to accept refunds.

---

**nootropicat** (2018-03-13):

> the gas concept is kinda broken and as a miner

Agree with that, not with the proposed solution. The problem is that gas price depends on available capacity at one moment, so it can only price the gas cost impact of accessing storage, not storing it.

For this reason there’s no solution other than adding a completely separate storage fee system, ie. locking ether in some amount. It would implicitly form a time-based payment due to lost interest from staking.

> I would not mine storage refunding transactions since it incentives people to play against me by storing in advance a lot of useless storage on which I’ll have to accept refunds.

Free storage can be emulated by using nonces of empty accounts. This is also a fundamental problem with the nonce solution but it’s unclear if any better alternative exists.

