---
source: ethresearch
topic_id: 1728
title: Safe notary pool size
author: JustinDrake
date: "2018-04-14"
category: Sharding
tags: []
url: https://ethresear.ch/t/safe-notary-pool-size/1728
views: 2385
likes: 1
posts_count: 3
---

# Safe notary pool size

**TLDR**: We suggest a way to enforce a safe minimum notary pool size.

**Background**

Two bad things can happen with a notary pool that is too small:

- Overwork: The amount of work per notary (largely bandwidth) is inversely proportional to the notary pool size. To preserve notary decentralisation, bandwidth requirements for individual notary identities should be manageable by a mainstream internet connection. A given notarisation scheme (parametrised by committee size, collation size, period length, number of shards, minimum deposit, etc.) will have a corresponding safe (minimum) notary pool size relative to a maximum acceptable internet connection speed.
- Takeover: The amount of capital an attacker has to deploy to take over notorisation (which may include fully notarising withheld or equivocated collations, delaying or stalling notorisation, breaking the RNG, etc.) is proportional to the notary pool size. A given notarisation scheme (parametrised by implicit or explicit voting thresholds) will have a corresponding safe (minimum) notary pool size relative to a minimum acceptable capital threshold for takeover.

Below we suggest infrastructure to enforce a minimum notary pool and mitigate notary overwork and takeover risks.

**Construction**

When the sharding scheme is first deployed, and more generally whenever the safe notary pool size is increased (e.g. because more shards are instantiated), the SMC managing deposits undergoes a bootstrap phase. Similar to a KickStarter project there are deposit thresholds for system activation. Activation can be all-or-nothing with a single threshold, or be gradual e.g. with shards activated with individual granularity.

After activation the system maintains the safe pool size with a priority queue. Deregistration requests by individual notaries are processed immediately if the pool size stays above the minimum. Otherwise deregistration requests are queued until new notaries add to the deposit pool. At that point deregistration priority is given to the notary with the oldest deposit.

**Discussion**

The main risk for notaries is “deregistration tail risk”—everyone cannot de-register immediately. In exceptional circumstances the queuing mechanism would be a backstop that provides the sharding infrastructure with a “guaranteed steady state”, buying time for a solution to kick in. Such a solution may be an external intervention by the community (e.g. a hard-fork) or a protocol-level response (e.g. an automatic increase in collation subsidies).

## Replies

**rauljordan** (2018-04-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> shards activated with individual granularity

Can you elaborate more on this, Justin? Do you mean that some shards could be inaccessible until the notary pool reaches a safe size?

---

**JustinDrake** (2018-04-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/rauljordan/48/740_2.png) rauljordan:

> Do you mean that some shards could be inaccessible until the notary pool reaches a safe size?

That’s right.

Here’s a concrete example. Let’s say that we have 256kB collations every 5 seconds per shard, that collations are notarised by committees of size 423, that each notary can only spare 0.5 Mbit/s of bandwidth to download collations, and that the notary deposit is 32 ETH. Then to activate a single shard we’d need at least 32 ETH * 423 * 256kB / 5s / (0.5 Mbit/s) = 11,089 ETH of deposits, or about 1.1M ETH for 100 shards.

