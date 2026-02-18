---
source: magicians
topic_id: 4567
title: "EIP-1559Q: Quadratic burn of gas fees as fees increase"
author: cotrader
date: "2020-09-03"
category: EIPs
tags: [eip-1559]
url: https://ethereum-magicians.org/t/eip-1559q-quadratic-burn-of-gas-fees-as-fees-increase/4567
views: 1319
likes: 2
posts_count: 8
---

# EIP-1559Q: Quadratic burn of gas fees as fees increase

I propose higher (e.g. quadratic or logarithmic) gas burns with higher gas prices. The benefits include:

1. Increasing the benefits of EIP 1559 as gas prices increase

A) Miners aren’t over paid to secure the network

B) High has fees goes to ETH holders and generally benefits the Ethereum community and makes economic abstraction far less relevant

C) Misuse and miner collusion becomes quadratically more costly and unlikely

D) Miners should always earn more for higher gas prices but decreasingly so. Ie the function slope is always positive but flattens over time.

The exact function can perhaps be adjusted by vote within some parameters.

Twitter discussion for it might continue here:

https://twitter.com/Gary_Bernstein/status/1301615988819935232?s=20

## Replies

**MicahZoltu** (2020-09-04):

Can you define the specific mechanism you are imagining here?  Are you imagining that the amount of gas used is multiplied by some function of gas price, where the higher the gas price the higher the multiplier?  If so, how would that result in any different behavior from users?  Wouldn’t it also result in blocks being underfilled?

---

**cotrader** (2020-09-04):

The miners should always earn more for higher prices but decreasingly so. So yes, the function for miner revenue r would take the gas price p and have a positive slope as p increases.

---

**lmaonade80** (2020-09-24):

This might be interesting if it could be flushed out a little further

---

**CryptoBlockchainTech** (2020-09-25):

All this will do is put Defi on Steriods as the more yields that are farmed, the more Ethereum goes to coin creators. It purposely takes the cost of insane yield farming and gives it back to them. If you want to destroy Ethereum, this will do it single handedly. It will simply grind to a hault as fees go so high that only yield farmers with their rebate will be able to use it.

Why is this so urgent? Why not be patient for phase 1.5 and sharding before you send thousands of high cost transactions across the network? I will tell you why, because you are greedy and are only here to line your pockets of poor souls thinking they can make money buying fake yield coins.  You could care less about Ethereum, only that it provides you a vehicle to exploit others.

Take a page out of the GPU miners book that have been patiently waiting for almost three years now for the devs to live up to what is in the Ethereum founding yellow paper and remove ASICs from the network. “ASICs are a plague”

Get in line, learn to be patient. Greatness takes time.

---

**cotrader** (2020-10-03):

What? How would more Ethereum go to coin creators? 1559 burns gas, it doesn’t create ETH. 1559 rather reduces miner collusion incentive to drive up gas costs. Wealthy eth users may spend very high gas still, but the burn will benefit the entire eth community & holders. I never launched any farmable tokens (yet), but regardless, dapp token makers provide value that users want, or there’d be no sales. Miners aren’t contributing anything by earning from gas beyond the network’s security requirement. Miner may earn just as much if not more, also, with 1559Q, since eth price rises from burns.

---

**cotrader** (2020-10-03):

An example simple harmonic function of the % miners would earn (y-axis) vs the gas price (x-axis), may be proportional to 1/(x+1)

100 * (1/(x+100)/100)

When gas price is at

1 gwei, miners get nearly 100%

100 gwei, 50%

200 gwei, 33%

300 gwei, 25%

400 gwei, 20%

Here’s an image of that function:

https://imgur.com/gallery/eaeCz3H

---

**CryptoBlockchainTech** (2020-10-04):

So I assume this will apply to POS also? Seems like the POS guys will be hugely impacted and this could cause a major reversal in long term investments in POS!

I know as a GPU miner I will be turning off the lights very soon if this is implemented. I am not the only one, we won’t stick it out next time through a two year bear market only to be reduced in earnings once we make it out and greedy Defi comes along out of nowhere expecting us to take another hit. Again remove ASICs and we will have a different perspective.

