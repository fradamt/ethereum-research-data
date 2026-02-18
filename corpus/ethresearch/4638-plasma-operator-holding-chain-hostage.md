---
source: ethresearch
topic_id: 4638
title: Plasma operator holding chain hostage
author: fahree
date: "2018-12-20"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-operator-holding-chain-hostage/4638
views: 2211
likes: 7
posts_count: 10
---

# Plasma operator holding chain hostage

One issue with any reliance on exit games as a response to block withholding is that since there is no authority on whether a block was withheld or not, there HAS to be a mechanism of priority to exist from earlier blocks. This leads to an attack of preloading a chain with lots of tiny accounts that will get priority over everyone else, and hold everyone’s money hostage indefinitely.

The only solution I see to such an attack is that users should refuse to put money on a chain that was loaded, and exit immediately if it was.

There is of course a race condition in deposits: the operator can go rogue just after a series of huge deposits, and before acknowledging them on his chain, so you’re never sure you’re safe when you deposit. To address this race, deposits must require a two-phase commit of some sort between the two chains.

As to when a chain is considered “loaded”, it should depend on the answer to the question: “how long are you willing to wait for an exit?” — consider how many accounts already exist on the blockchain, and how long it will take at the longest for them to all exit in the worst case, because that’s how long it will probably take.

In the end, that means that a Plasma chain probably cannot scale in terms of number of simultaneous users, and might even need a way for the operator to reject users and/or expel them from his chain, so as to make space for active users (alternatively, he could perhaps atomically move chunks of active users to a new chain).

## Replies

**fahree** (2018-12-20):

If publishing the trace of valid transactions can increase the priority of a claim, then you don’t have to wait for all the preloaded accounts to exit anymore… but instead you have to publish all the preloaded transactions, which can also be massively inflated by the operator. For efficiency, this publication should be shared between outputs that have a shared history, or else the exit games may have even more of a scaling issue.

In any case, every plasma chain must make it easy to compute the expected and/or maximum time and money required for a user to exit should he do or accept a transaction, and the user must have limits on what he’ll accept. In the end, these limits must remain within how much the main chain can scale, or bad operators can grief users with withholding attacks.

---

**gakonst** (2018-12-21):

This is true for MVP-like designs which require exit priorities.

Both attacks you describe here and in [Chunked Plasma Exit Games with Expensive Griefing](https://ethresear.ch/t/chunked-plasma-exit-games-with-expensive-griefing/4636) do not apply for Plasma Cash-like constructions with rootchain enforced non-fungibility.

In these constructions you are never forced to exit a coin because the cheating party (operator) is required to add a separate security bond for each exit of a coin (or slice). Each exit is separate from others and has its own dispute period. Assuming liveness for challenges and that the exit-game is incentive compatible, we can expect that the operator will not try to attack if they are to lose money.

(You can additionally burn part of the challenge bond, if you consider that the operator is also front-running challenges - context: [Plasma Front Running problem](https://ethresear.ch/t/plasma-front-running-problem/4542/))

As a result, each exit is individually challengeable which means it suffices to challenge exits involving coins that you own to maintain safety.

This also applies to Cashflow/Prime designs, given that if an operator attempts to exit a large slice of coins, a challenge involving any coin inside this slice is sufficient to cancel the exit.

---

**fahree** (2018-12-28):

Thanks for your comments.

The problem then is the non-fungibility, which makes it impossible for users to pay the operator small fees, and then how will the chain be sustained? Also a non-fungible chain cannot scale, since there can only be as many independent assets as there are deposit transactions. And if you’re ready to accept lack of scalability, then you could implement a *much* simpler limit on scalability (e.g. transaction count) and get fungibility for free.

Scalability is an essential part of what makes Plasma interesting. Without it, it might be much simpler (and probably safer) to just use an ERC20.

---

**nginnever** (2018-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> Also a non-fungible chain cannot scale, since there can only be as many independent assets as there are deposit transactions

One deposit can issue many cash ids of a *lowest* denomination.

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> The problem then is the non-fungibility, which makes it impossible for users to pay the operator small fees, and then how will the chain be sustained?

Micropayments don’t work for any layer 2 system (including lightning network) if you consider the case of just one transaction. In such a case, the value of the deposit must be larger than the cost of exiting the layer 2 or security is broken. Therefore you need some system of repeated transactions to make any layer 2 system worth while. In this spirit, an operator could maybe keep tabs on how many times a user transacts (perhaps by some sequence of account). When a certain threshold of transactions accumulates per user the operator could require the next transaction come with a send of the plasma cash chain’s smallest denomination to the operator.

---

**fahree** (2018-12-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> One deposit can issue many cash ids of a lowest denomination.

If you mean that a deposit can issue a range of tokens from 1 to N, then we’re back to fungible assets through ranges of pennies. But while the deposits scale trivially, the withdrawals still don’t. You’ll have to have one exit per penny and/or an attacker can cause such division into tiny range that no one can afford to exit.

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> Therefore you need some system of repeated transactions to make any layer 2 system worth while.

Of course. But if exits can’t scale, then it has to involve a relatively small number of participants, if not of transactions. Exit games can scale better than simple state channels, but not quite as well as side-chains with a trusted validation network.

![](https://ethresear.ch/user_avatar/ethresear.ch/nginnever/48/1936_2.png) nginnever:

> When a certain threshold of transactions accumulates per user the operator could require the next transaction come with a send of the plasma cash chain’s smallest denomination to the operator.

This requires fungibility, which so far as I understand, requires some amount of scaling.

---

**kfichter** (2019-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> This leads to an attack of preloading a chain with lots of tiny accounts that will get priority over everyone else, and hold everyone’s money hostage indefinitely.

I believe this is actually untrue in Plasma MVP. From the original spec:

> However, if when calling exit, the block that the UTXO was created in is more than 7 days old, then the blknum of the oldest Plasma block that is less than 7 days old is used instead.

This mechanism effectively creates a “max priority” of 7 days. Anything older than 7 days is assigned a priority of “7 days old” (in practice, substitute 7 days for whatever you want). Therefore exits of old UTXOs can only delay new exits by a maximum of 7 days, not indefinitely as stated in your post.

To better illustrate what this means, let’s say you created an output a long time ago. I create an output at (time t+0) and start a withdrawal of my output before t+7 days. Since my output was created less than 7 days ago, the priority of my output is determined by the exact time at which I created my output, t+0.

At time t+8 days, you submit a withdrawal of your output. Your output is older than 7 days, so your output is given an effective priority of (now - 7 days), (t+8-7 = t+1). My output (created *after* yours) will be processed first because of this “max priority” mechanism.

---

**fahree** (2019-02-25):

OK, that means everyone should exit immediately and exits can neither scale nor be delayed. This also creates an intense pressure upward for gas prices as the demand explodes.

---

**kfichter** (2019-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> that means everyone should exit immediately

Exit immediately in what circumstance?

![](https://ethresear.ch/user_avatar/ethresear.ch/fahree/48/1380_2.png) fahree:

> exits can neither scale

MVP exits can scale linearly (mass exit protocols) but I agree that it’s not enough.

---

**fahree** (2019-02-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Exit immediately in what circumstance?

Indeed, that’s another weak point for the old MVP: you need to audit the side-chain (which defeats some of the scaling purpose if lots of users need to process lots of data) or have someone you trust audit it, or you won’t know for sure when to exit or not exit.

The new Plasma with a mapping from asset to owner is much nicer: you only have to watch the main chain for an exit, and only for those assets you own. *THAT* works.

