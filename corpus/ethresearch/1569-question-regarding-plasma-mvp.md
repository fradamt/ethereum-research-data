---
source: ethresearch
topic_id: 1569
title: Question regarding Plasma MVP
author: loiluu
date: "2018-03-30"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/question-regarding-plasma-mvp/1569
views: 1234
likes: 0
posts_count: 3
---

# Question regarding Plasma MVP

I haven’t followed Plasma development for awhile and just recently saw Karl’s [video](https://www.youtube.com/watch?v=jTc_2tyT_lY) regarding Plasma MVP. Very interesting and useful presentation. I have a bunch of questions after watching the video though, hence would be great if people can discuss them here. Pinged Karl a couple of days ago but looks like is not active on Skype.

1. It seems that the plasma chain will have to spend a lot of gas/ resources to commit their block headers to the contract on ETH mainchain. This is gonna be expensive imo, not sure if the team has got any measure/ experiment yet?
2. Does plasma assume that everyone has to be online to watch out for scammers and exit if the operator is bad? This is not gonna work in practice as people often go offline.
3. Since the protocol processes the exit requests based on the “age” of the transactions related to accounts/addresses. I dont understand how its gonna scale if Plasma chain will have millions of users and billions of transactions in the future?
4. Further, looks like the arbitration process is currently linear in the number of plasma blocks, which won’t scale as well.

## Replies

**danrobinson** (2018-03-30):

Have you seen the design for [Plasma Cash](https://karl.tech/plasma-cash-simple-spec/)? It should address some of your concerns.

![](https://ethresear.ch/user_avatar/ethresear.ch/loiluu/48/1080_2.png) loiluu:

> Does plasma assume that everyone has to be online to watch out for scammers and exit if the operator is bad? This is not gonna work in practice as people often go offline.

True (as in Lightning), but this can be outsourced to redundant and incentivized third parties. And in Plasma Cash, you only need to monitor the *parent chain* (not the Plasma chain).

![](https://ethresear.ch/user_avatar/ethresear.ch/loiluu/48/1080_2.png) loiluu:

> Since the protocol processes the exit requests based on the “age” of the transactions related to accounts/addresses. I dont understand how its gonna scale if Plasma chain will have millions of users and billions of transactions in the future?
>
>
> Further, looks like the arbitration process is currently linear in the number of plasma blocks, which won’t scale as well.

I don’t think these were true in Plasma MVP anyway, but it’s definitely not true in Plasma Cash; determining which of two transactions is older (i.e. was included in an earlier Plasma block) is very simple and not dependent on the total number of transactions, and I think challenges can always be resolved in a constant number of steps.

---

**loiluu** (2018-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/danrobinson/48/755_2.png) danrobinson:

> I don’t think these were true in Plasma MVP anyway

From the [video](https://youtu.be/jTc_2tyT_lY?t=741).

Anyway, PlasmaCash is a different design of Plasma and I also have a few concerns as well, but lets not discuss them here. I also don’t see how PlasmaCash can solve the first concern that I have.

