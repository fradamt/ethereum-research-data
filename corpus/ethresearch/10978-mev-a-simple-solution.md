---
source: ethresearch
topic_id: 10978
title: MEV a simple Solution
author: LightForTheForest
date: "2021-10-10"
category: Economics
tags: []
url: https://ethresear.ch/t/mev-a-simple-solution/10978
views: 5082
likes: 1
posts_count: 13
---

# MEV a simple Solution

Hello guys,

I’m new here but a veteran on the trading side and maybe can give some insights from a personal trading perspective. And maybe a simple solution idea to MEV. Hope it is the right place for the post. TLDR: The current situation sucks and is getting worse with systems like flashbots.

What I think hurts most:

Transactions with lower (gas + tip ) are placed in a better position in the block. I often experience something like this: Very high priced transaction fails against some “dark” transaction with lower gas price at the end of the block. This is simply not right.

A proposed solution should include in my perspective just two points:

1. Blocks must be ordered by (gas + tip).
2. It should be possible to backrun a transaction. So sending something like this [my_tx_1, tx, my_tx_2] and paying for it some extra fee.

Implementation:

1. Is simple and clear
2. Maybe:

GasPrice of the bundle in the block [my_tx_1, tx, my_tx_2]  should be (gas + tip) of tx
3. my_tx_1/2 gasPrice should be higher than tx gasPrice. You just pay for being around the backrun tx.
4. for failure you would pay my_tx_1/2 gasPrice * minGasConstant. (Failure means that tx is already executed)

What do you think guys? Don’t let Ethereum become a dark place!

PS Here is a short explanation for 2 (you can skip this):

Before flashbots come in we had a situation that sucked but was kind of clear how it works.

Most of the time it was something like this: Someone send’s a bad transaction. You could calculate the price impact and arbitrage it. Everyone was trying to catch and spam the block since it was in random order. Later the eth community introduced timestamps. Now it was a latency game. I tried to play it as well. But it was clear: First come first serve although the miners started to manipulate the blocks. That sucked as well. Here already big players with good infrastructure and connections to miners had the edge. I think sandwich-like attacks are ok, in the sense that a solution can be implemented on the application layer. You already have often some protection by specifying max slippage.

Now flashbots came and introduced bundles. This really rigged the game. YES, Flashbot’s solved (2) but introduced a huge unfairness to the game. We just need a solution where you can simply backrun or let’s say react to transactions. That would solve all the spamming and prevent unfair transactions at the end of the block. Miners would get basically the same or even more since flashbot’s biding is hidden and you could compete for the execution in an open biding which already happens for normal transactions and works pretty well in my opinion. 99% of all real MEV are of the form (2). The rest could be handled in the classical biding mechanism, like in the old days (which still works but sometimes gets rigged by flashbot like transactions). You could basically adjust the replacement percentage if the load on the system becomes too high.

## Replies

**LightForTheForest** (2022-01-23):

Hello again,

sorry for pushing this thread, but would really love to know, what you think about forcing block order by (gas + tip)?

For example *Alice* know’s that buying item Y might be difficult on the blockchain. She pays a very high gasPrice to get it executed first. *Chuck* has good friends at a third party (company/miner/flashbots), submits the same order with a 10x lower gasPrice, and his transaction gets executed first. Of course *Alice* transaction fails and she has to pay high fees for nothing. That sounds not reasonable. Would the block be sorted by (gas + tip) then *Chuck* transaction would probably not be included and *Alice* would be protected from an ***unfair*** transaction order.

---

**MicahZoltu** (2022-01-25):

A front runner can just pay a slightly higher gas price than the target transaction to get in front, and slightly lower to get behind.

---

**LightForTheForest** (2022-01-25):

> A front runner can just pay a slightly higher gas price than the target transaction to get in front, and slightly lower to get behind.

For a very high gasPrice a lot of sandwich attacks would disappear since the attacker would have to make two transactions and pay approximately 2x the fees.

Sure, you don’t prevent sandwich attacks with it, but you would at least guarantee a **fair** transaction order according to the paid fees (gas + tip).

---

**MicahZoltu** (2022-01-25):

Sandwichers and frontrunners already pay above market rate for their bundles, it just is paid directly to the miner rather than through the gas pricing fields of a transaction.  This requirement would just add a tiny bit of extra complexity to bot authors, but not enough to slow them down or stop them in any way.  At best you would have a couple of bots with newly introduced bugs which would be rapidly fixed.

---

**LightForTheForest** (2022-01-25):

Here is an example:

0x59fa131b4cb2a0fe1a850be353128cfea023e60396dfe13b8c8a73f83f88199d

Sandwitch Revenue (without fees) 1.589  - 1.557 = .032

Fees: 0.02 (gasPrice = 267) and 0.011 ( gasPrice =134)

Profit: 0.001

In this case, the *victim* could pay a slightly higher gasPrice and the attack would not work for an ordered block. I think there are a significant number of such cases.

---

**wjmelements** (2022-04-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/lightfortheforest/48/7606_2.png) LightForTheForest:

> Blocks must be ordered by (gas + tip).

This is how miners ordered blocks before they knew about MEV, and MEV was much easier in that era.

---

**jonreiter** (2022-04-17):

been pondering things adjacent to this.  for a permissionless system it feels like you cannot avoid this problem unless the entire fork-resolution process is internal to the protocol and there is no social consensus backstop.

if transfers occur in the way you describe – which they do – there is no reason to believe the out-of-band resolution process is pristine either. such mev action may be unavoidable in the limit for permissionless systems.

---

**gavinyue** (2022-04-20):

![](https://ethresear.ch/user_avatar/ethresear.ch/lightfortheforest/48/7606_2.png) LightForTheForest:

> Very high priced transaction fails against some “dark” transaction with lower gas price at the end of the block. This is simply not right.

Why is it not right?  Miner/validators can choose to do some pro-bono work, even if they will be paid in other forms.

---

**MicahZoltu** (2022-04-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonreiter/48/8910_2.png) jonreiter:

> if transfers occur in the way you describe – which they do – there is no reason to believe the out-of-band resolution process is pristine either. such mev action may be unavoidable in the limit for permissionless systems.

This is the current prevailing belief.  Either you have a permissioned system and you explicitly *trust* the permissioned actors to behave a certain way (e.g., strict ordering by local receipt time), or you have a permissionless system and you accept that transaction ordering can and will be manipulated by some participants in the system for profit and you design your applications around that.

---

**jonreiter** (2022-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> This is the current prevailing belief. Either you have a permissioned system and you explicitly trust the permissioned actors to behave a certain way (e.g., strict ordering by local receipt time), or you have a permissionless system and you accept that transaction ordering can and will be manipulated by some participants in the system for profit and you design your applications around that.

ok i’m now convinced this belief is true.  it mirrors a proof (older) that a social consensus backstop is unavoidable for trustless proof-of stake systems.

not sure how to design around inevitable off-chain coordination and mev.  curious what people think about this. that’s painful to a degree i did not expect to find.

---

**MicahZoltu** (2022-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/jonreiter/48/8910_2.png) jonreiter:

> how to design around inevitable off-chain coordination and mev

Often little things can help, like just letting the user know they are placing a fill-or-kill limit order and not a market order.  You can also do more advanced things like automatically calculating slippage based on market conditions rather than just using fixed values.  I think Uniswap does some of this now, so the automatically calculated slippage for USDC is going to be incredibly tight compared to the automatically calculated slippage for something like UST.

---

**jonreiter** (2022-05-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> using

Lets put user education aside (I think losses are the best error messages personally)

For formulaic trading (amm, whatever) you can compute slippage but that does not mitigate reordering problems.

For non-formulaic you have to execute to find the slippage.  Mev opportunities here abound.

I’m not even sure fok limit orders help.  They are still short options for the duration of the block creation and the mev is the value of those options.

Market makers love working “all or nothing” limit orders because there is mev all over the place. This applies equally to traditional markets.

