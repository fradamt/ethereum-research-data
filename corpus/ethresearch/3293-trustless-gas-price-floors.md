---
source: ethresearch
topic_id: 3293
title: Trustless Gas Price Floors
author: kfichter
date: "2018-09-10"
category: Economics
tags: []
url: https://ethresear.ch/t/trustless-gas-price-floors/3293
views: 1789
likes: 10
posts_count: 15
---

# Trustless Gas Price Floors

Figured I’d write something up about this for fun. Sorry if people have written about this before!

While working on some Plasma stuff I started thinking about efficient ways to place floors on gas prices. If you don’t have any legal means to set a price floor, you can just [offer to buy everything](https://en.wikipedia.org/wiki/Government_cheese) at the floor price. If other people are willing to pay even more than your floor price, then you don’t actually need to buy everything.

I wrote up a small [a smart contract](https://ethfiddle.com/CkcYJuarzy) that basically offers to fill the remainder of a block at a specified gas price. As long as the contract has enough funds, miners are guaranteed that floor price.

The cost to sustain a floor price maxes out at the cost to fill every block at that gas price (which makes sense). Currently that’s about $1m to push gas prices up to 100 gwei for a day. You’d probably end up paying less in practice because people will still want to use Ethereum.

All of this generally depends on the economics around mining (rationality, cost of mining software, decrease in block production rate for extra cycles spent on this logic). Feedback/improvements welcome.

## Replies

**PhABC** (2018-09-10):

What’s the main use case you have for this?

---

**MicahZoltu** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Currently that’s about $100k to push gas prices up to 100 gwei for a day

I believe you are off by a factor of 10.

```auto
24 hours/day * 60 minutes/hour * 4 blocks/minute = 5760 blocks/day
5760 blocks/day * 8000000 gas/block * 100 nanoeth/gas * 10^-9 nanoeth/eth = 4608 eth/day
4608 eth/day * 200 usd/eth = 921,600 usd/day
```

---

**kfichter** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/micahzoltu/48/18591_2.png) MicahZoltu:

> I believe you are off by a factor of 10.

Whoops you’re right. I dropped a 0.

---

**kfichter** (2018-09-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/phabc/48/35_2.png) PhABC:

> What’s the main use case you have for this?

So the backstory here is that I’m analyzing some Plasma attacks that involve spamming the network for an extended period of time.

When users want to withdraw funds from a Plasma contract they need to wait out a “challenge period.” If the withdrawal is invalid for some reason (user already spent the funds), then it can be challenged during that period.

Currently, a successful challenger receives a fixed reward that’s meant to cover the gas cost of challenging. If gas prices rise sufficiently for the entire duration of the challenge period, then the reward could actually be less than the cost to challenge. No one would challenge unless they have a direct incentive to do so, and users can suddenly be heavily griefed.

So I wanted to figure out the cost to raise gas prices to some arbitrary level. I also wanted to see if there was a way to do this without any interaction by the “attacker” to further reduce overhead costs. This is what I ended up with.

---

**Danny** (2018-09-11):

You mean that we could set a price floor, in which any tx sender doesn’t have to pay more than the floor price?

If I got your opinion right, regarding the relation of miners and tx senders, it is quite similar to general marketplace described in micro-economics. So the price floor has a problem of **excessive demand.** (In this market, the demand curve is driven by the tx senders)

This may cause a chaos on the network due to the mass txs or furthermore black market which trades the higher price than the even equilibrium. If there is any error, please give me a hard feedback ! ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**adamskrodzki** (2018-09-11):

This value is significantly less as You need to bare only marginal costs.

In times of it’s greatness CryptoKietties where responsible together for like 20% of gas use. Still they forced everyone to pay 70-100 Gwei at that time.

This goes even lower if You are a miner. If by filling 20% of block You can force another 80% to pay higher fees. Then with 25% of hashing power You can do that for free, forever.

---

**Danny** (2018-09-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/adamskrodzki/48/1910_2.png) adamskrodzki:

> Still they forced everyone to pay 70-100 Gwei at that time.

Why do you think they force users to pay those high fees sometimes ? Is it just a guidance for their users how to get their TXs to be contained in a limited block size ?

---

**adamskrodzki** (2018-09-14):

Maybe i misused word forced i will rephrase then

In times of it’s greatness CryptoKietties where responsible together for like 20% of gas use. This 20 % was enough to cause everyone (also not using CryptoKietties) to choose among two possibilities

1. paying 70-100 GWEI
2. waiting literally days for transfer

Point of the post was to point out that in order to cause Ethereum gas price to rise to level X You do not need pay X for all gas in every block. Paying for 20% of a gas in a block will be probably enough.

If You are a miner then interesting effects kicks in making this levels even lower.

---

**kfichter** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/danny/48/2151_2.png) Danny:

> You mean that we could set a price floor, in which any tx sender doesn’t have to pay than the floor price?

What you’re referencing would be a price ceiling, this post is referencing a [price floor](https://en.wikipedia.org/wiki/Price_floor). This post isn’t suggesting that we implement a price ceiling in practice, more just a costly (but trustless) way to enforce a price floor. In practice, price floors shut other users out of the market or force them to pay more since supply is generally inelastic when it comes to Ethereum block space.

---

**Danny** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> This post isn’t suggesting that we implement a price ceiling in practice, more just a costly (but trustless) way to enforce a price floor.

okay I got you. There was an misunderstood of the word itself sorry ![:sweat_smile:](https://ethresear.ch/images/emoji/facebook_messenger/sweat_smile.png?v=12) I was thinking a mitigation of higher gas price is the main purpose.

Then, you mean that you’re going to make a certain level of gas price which is more upper than the status quo, right?

i) What’s the purpose of this?

ii) How we could say the miner supply is enelastic? I guess it’ll be more elastic than the each tx sender, who is the general peer on Ethereum blockchain network. In contrast, the miner is close to a monopoly producer. The number of miner is absolutely less than the senders. (Supposing in a single block space)

---

**phil** (2018-09-15):

Instead of doing something useless like an empty while loop, mine https://gastoken.io/.  Literally what it’s for.

Miners should already be incentivized to do this.  It’s not a lack of existing mechanism issue, it’s a lack of sophistication one.

---

**kfichter** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/phil/48/18_2.png) phil:

> Instead of doing something useless like an empty while loop, mine https://gastoken.io/.

Good point.

![](https://ethresear.ch/user_avatar/ethresear.ch/phil/48/18_2.png) phil:

> Miners should already be incentivized to do this.

Incentivized to do what exactly?

---

**phil** (2018-09-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> Incentivized to do what exactly?

Fill all excess block space they aren’t mining with transactions that mine GasToken for free (since they’re paying themselves fees), essentially establishing a floor at the cheapest transaction to not do this.

---

**Danny** (2018-10-21):

Is this Gas Price Floor mechanism is for the guarantee of tx fee revenue per block space for miners at least?

IMHO, the problem in Ethereum network is the higher price so I could not understand why the miner is going to be more beneficiary. Price floor is only effective when the floor price is set upper than the equilibrium level of certain price of commodity. If the purpose of the mechanism is to give more revenue and utility to suppliers(miners), maybe the gas price doesn’t fit with that. So, I mean, what is the main use case and specific purpose of this ?

Would be glad to have feedback on this ! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

