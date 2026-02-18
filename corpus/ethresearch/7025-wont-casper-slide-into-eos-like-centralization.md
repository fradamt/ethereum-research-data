---
source: ethresearch
topic_id: 7025
title: Won't Casper slide into Eos-like centralization?
author: timid
date: "2020-02-25"
category: Economics
tags: []
url: https://ethresear.ch/t/wont-casper-slide-into-eos-like-centralization/7025
views: 1956
likes: 4
posts_count: 7
---

# Won't Casper slide into Eos-like centralization?

We saw that what happened to Eos’s dPoS is exactly what was predicted:

- Level 1 bribery: block producers pay back part of the block rewards to voters. A market forms among block producers, approaching a point where ~100% of the rewards are distributed back to holders.
- Level 2 bribery: lazy holders give coins to a custodian, custodian handles voting instead of holders. Block producer pays part of the block reward back to the custodian, custodian takes a cut, passes on the rest to holders. Another market forms, now among custodian-voters, with a similar outcome as above.
- Level 3 bribery: custodian-voters are also block producers. They form cartels with other custodian-voter-block producers and agree to vote on each other for various percentages of the block reward they reap.

On each level, validation ends up in the hands of a few large entities.

Casper PoS moves beyond the problems on Level 1 and Level 3 by not relying on the model of N block producers and voting. But I suspect something similar to Level 2 can happen in Casper PoS:

Lazy holders give coins to a custodian (Coinbase, Binance, [Bitcoin Suisse](https://www.bitcoinsuisse.com/staking/ethereum-2), etc), custodian handles validation instead of holders. Lazy holders get the validator rewards, custodian takes a cut. A market forms among custodian-validators, approaching a point where ~100% of the rewards are distributed back to holders. For efficiency and reputational reasons, the number of the successful custodian-validators will be quite low.

Casper-FFG tries to counter this centralization incentive with a sliding penalty scale (the more stake you control, the greater your effective penalty will be when your setup fails, because penalties grow with malfunctioning total stake). However, with experienced industry participants such as mentioned above, we can assume they will build a resilient and fairly decentralized staking grid – they’ll need to protect their reputation and their customer’s funds. But coins, validator choices, and what software they run (!) will still be under their control. I acknowledge this penalty mechanic will reduce centralization to some degree, but I assume it will be a partial deterrent at best.

(Or worse, in an extreme case, a custodian-validator (or a cartel of these) can gain control of <1/3 of the stake and issue credible threats of thwarting the chain. I haven’t explored this scenario more deeply, but may be worthy to keep in mind.)

So, in Casper, what will prevent validation from ending up in the hands of a few large entities?

## Replies

**alonmuroch** (2020-03-16):

Custodians that manage stakers is an issue… also considering that eth is non transferable will make this worse.

I suspect exchanges will offer some kind of a way to liquidate your staking positions (say exchange with someone wanting to get in?) so people might value liquidity over decentralisation …

---

**timid** (2020-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/timid/48/4604_2.png) timid:

> Or worse, in an extreme case, a custodian-validator (or a cartel of these) can gain control of >1/3 of the stake

Almost the same thing happened to the Steem blockchain a week after my OP:

[Tron Executes Hostile Takeover of Steem, Exchanges Collude](https://cryptobriefing.com/tron-executes-hostile-takeover-steem-exchanges-collude/)

Can we please have this conversation before launching phase 0? Cc’ing [@vbuterin](/u/vbuterin) and [@djrtwo](/u/djrtwo).

---

**vbuterin** (2020-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/timid/48/4604_2.png) timid:

> agree to vote on each other for various percentages of the block reward they reap.

What “voting” mechanic are you thinking about here? In Casper FFG, there isn’t really a choice of who to vote for (under normal circumstances); everyone just attests to the (normally single) block that is the tip of the strongest chain.

---

**timid** (2020-04-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What “voting” mechanic are you thinking about here?

That’s from the “Level 3” bribery description of dPoS systems. My concerns about Gasper PoS (stake centralization due to the “Level 2” effect) are described below the bullet points:

![](https://ethresear.ch/user_avatar/ethresear.ch/timid/48/4604_2.png) timid:

> But I suspect something similar to Level 2 can happen in Casper PoS:

---

**sachayves** (2020-04-15):

Perhaps the best defence against this is to make validating as frictionless as possible (a few clicks to get up and running, and a dead-simple interface from which to manage) – i know this is something [@CarlBeek](/u/carlbeek) has been thinking hard about.

In parallel, i think we need to do a much better job at communicating the philosophical reasons behind why running your own validator is so important.

It’s not as obvious as we think to people outside the community. We need to communicate it in a way that makes them dream.

---

**sherif** (2020-04-16):

Using round robin in selecting block producer guarantees that no malicious nodes can produce a block. In other hand delegating and (why you do it yourself while you can delegate it) shows a venerability as shown above, but correct me if I’m wrung it didn’t tamper with the data and dpos still tamper proof dispute what happened with Steem by Justin.

