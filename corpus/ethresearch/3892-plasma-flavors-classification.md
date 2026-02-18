---
source: ethresearch
topic_id: 3892
title: Plasma Flavors' Classification
author: sg
date: "2018-10-23"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/plasma-flavors-classification/3892
views: 2723
likes: 12
posts_count: 16
---

# Plasma Flavors' Classification

in order to dig the feasibility and advantage of Plasma generating framework (i.e. Plasma Generator), I roughly classified Plasma flavors. Feedback is much appreciated ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

[![49](https://ethresear.ch/uploads/default/optimized/2X/3/3a1be1007698a1d6ff31f5f477f77831cf749522_2_667x500.png)491022×765 92.1 KB](https://ethresear.ch/uploads/default/3a1be1007698a1d6ff31f5f477f77831cf749522)

## Replies

**bharathrao** (2018-10-31):

I think another interesting perspective is to have the three axes to be UX, scaling and security.

Or perhaps a [radar chart](https://en.wikipedia.org/wiki/Radar_chart).

---

**therne** (2018-11-01):

Why do you think that the security level of the verification game isn’t equal with Ethereum?

---

**MihailoBjelic** (2018-11-01):

Is “TinyRAM + Plasma Snapp” flavor discussed somewhere (never seen it being mentioned before)? Thanks! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**sg** (2018-11-02):

This is just my gut feeling though, the budget what I need for attack Leap is much cheaper than the attack budget for ETH. And the attack budget of Plasma Cash is the same as ETH.

---

**sg** (2018-11-02):

[@nrryuya](/u/nrryuya) gave me that motif. But no one digging for now AFAIK.

---

**bharathrao** (2018-11-02):

[![19%20PM](https://ethresear.ch/uploads/default/optimized/2X/7/77c845ad82b5b066d012a17419a62ee9b18837d7_2_690x250.png)19%20PM1620×588 75.6 KB](https://ethresear.ch/uploads/default/77c845ad82b5b066d012a17419a62ee9b18837d7)

Something like this

---

**sg** (2018-11-02):

The attributes and scores(especially Plasma Cash’s security guarantee is oddly undervalued lol) should be elaborated though, that visualization is quiet fair I think.

---

**bharathrao** (2018-11-02):

Red doesnt mean insecure, its just that it needs those pieces. Perhaps red/green is a bad color scheme

---

**sg** (2018-11-02):

Yeah color scheme is gonna be also one of elaboration ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Just for initiation, I made a issue to here

https://github.com/ethsociety/learn-plasma/issues/118

---

**nrryuya** (2018-11-05):

I think state transitions proved by SNARKs can include more than token transfers.

I found a issue made by [@barryWhiteHat](/u/barrywhitehat)  about general dapps in roll_up (https://github.com/barryWhiteHat/roll_up/issues/14) .

It’s said that a merkle tree which holds app specific data is added and only SNARKs can edit that.

TinyRAM wouldn’t comes in here.  Although with TinyRAM more complicated programs can be converted to circuits but they would be really expensive to prove.

---

**MihailoBjelic** (2018-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/nrryuya/48/1552_2.png) nrryuya:

> Although with TinyRAM more complicated programs can be converted to circuits but they would be really expensive to prove.

That was my understanding, too.

I think STARKs is definitely the way to go here. StarkWare is right now deciding what their MVP will be, contemplating between: a) shielded Ethereum transactions, b) grouped transactions (computations) on Ethereum and c) support for DEXs. It would be awesome if they decide to do b), they think they can release the MVP by the end of Q1 2019.

---

**bharathrao** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Something like this

[@johba](/u/johba) Can you please help fill in the matrix for Leap?

[@sg](/u/sg) Can you help fill in for Gen?

Anyone know if Plasma prime author is on this forum?

---

**johba** (2018-11-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Can you please help fill in the matrix for Leap?

Leap works under the same assumptions of the MoreVM exit game.

But i disagree with the green/red table above. It has criteria that are not inherent to the designs itself. Arguably most tweaks that have earned the Gluon column a green field could be applied to the MVP and Cash flavors as well. Especially trowing PoS at data-availability is like trying to create security by obscurity.

Let’s avoid glorified feature lists here and get back to research.

---

**sg** (2018-11-07):

I note still we need constructive approach given

1. Build fair attributes to make Plasma flavors easy to understand for beginners
2. Someone who is enough honest and sensible person fills these attribute as long as possible
3. Project owner of each flavor review that result

I’m sure we all wasting time to explain each flavors’ difference. I ask more help from community, or smarter alternative attitude for this mess.

---

**bharathrao** (2018-11-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> glorified feature lists

The plasma flavor comparison table is a use-case fit discussion so that adopters can make an informed decision about whats best for them.

The **UX aspect** dictates if the product can even be built using a particular flavor of plasma. For example, fast withdrawals is essential for arbitrage and any projects that depend on arbitrage would prefer supporting flavors. Instant finality is a requirement for hedging and HFTs.

**Scaling aspect** dictates deployment frameworks needed for the project. For example, Light nodes allow running on a desktop or browser vs others that require running in a data center.

**Security aspect** dictates the size of finances someone should be ok with risking on the network. A product like tipping or memo.cash, where many users have a small amount of coins may be quite OK with a watchtower model since everyone has the same usage pattern. However, any financial model where there are hubs that participate in most of the transactions may find it impractical to watch and challenge a huge number of transactions.

![](https://ethresear.ch/user_avatar/ethresear.ch/johba/48/20905_2.png) johba:

> It has criteria that are not inherent to the designs itself.

I happen to think *what you can do with it* is more important than *what it is built with*. Things are not better simply because something uses a Merkle tree vs snarks if the capabilities and user experience overall is the same.

