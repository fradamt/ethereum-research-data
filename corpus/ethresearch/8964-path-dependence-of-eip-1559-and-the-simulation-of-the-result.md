---
source: ethresearch
topic_id: 8964
title: Path-dependence of EIP-1559 and the simulation of the resulting permanent loss
author: mtefagh
date: "2021-03-19"
category: Economics
tags: [fee-market, resource-pricing, eip-1559, gas-token]
url: https://ethresear.ch/t/path-dependence-of-eip-1559-and-the-simulation-of-the-resulting-permanent-loss/8964
views: 4114
likes: 4
posts_count: 11
---

# Path-dependence of EIP-1559 and the simulation of the resulting permanent loss

Continuing the discussion from [DRAFT: Position paper on resource pricing](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838/24):

There exists an unintentional and uncoordinated version of [this](https://ethresear.ch/t/draft-position-paper-on-resource-pricing/2838/24) attack which is inevitable due to its decentralized nature. Suppose that a small portion of users (e.g., 5%) are rational enough to pay less fee by waiting whenever their transactions are not an emergency. For instance, a wallet client has a built-in feature that asks how much the user is willing to wait if the base fee is currently declining. The simple strategy here is to wait as long as the mempool is considerably less than (e.g., half) the target size full. This gives a somewhat reliable prediction that the current block will not be full enough, and the base fee will decrease. Otherwise, the client will broadcast the transaction. This optimization is simple enough to be implemented and is very likely to be used by some people shortly after EIP-1559. However, this will result in the same result as mentioned [before](https://nbviewer.jupyter.org/github/mtefagh/fee/blob/master/fee.ipynb), which is the base fee will converge to zero over time. The intuition behind this is that even though users act uncoordinated, their incentives are well aligned to not broadcast transactions whenever blocks are less-than-target full. Therefore, their collective behavior mimics that of an attacker in the [previous](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/24) version. For a thorough simulation, see [here](https://mtefagh.github.io/fee/).

## Replies

**mtefagh** (2021-03-19):

![Noise](https://ethresear.ch/uploads/default/original/2X/a/a9a85e459222f1e52487771b049423c927f535f9.svg)

---

**mtefagh** (2021-03-28):

An alternative EIP designed to resolve these issues:


      [github.com](https://github.com/ethereum/EIPs/blob/85c5f80c10810f5c3016f0983ea0a5c79788af55/EIPS/eip-3416.md)




####

```md
---
eip: 3416
title: Median gas premium
author: HexZorro (@hexzorro), Mojtaba Tefagh (@mtefagh)
discussions-to: https://ethereum-magicians.org/t/eip-3416-median-gas-premium/5755
status: Draft
type: Standards Track
category: Core
created: 2021-03-18
---

## Simple Summary

A transaction pricing mechanism with a fixed-per-block network fee and a median inclusion fee.

## Abstract

There is a base fee per gas in protocol, which can move up or down by a maximum of 1/8 in each block. The base fee per gas is adjusted by the protocol to target an average gas usage per block instead of an absolute gas usage per block.  The base fee is increased when blocks are over the gas limit target and decreases when blocks are under the gas limit target. Transaction senders specify their fees by providing *only one value*:

* The fee cap which represents the maximum total (base fee + gas premium) that the transaction sender would be willing to pay to get their transaction included, resembles the current maximum gas price specified by senders but in this protocol change proposal the final gas price paid, most of the time, will be lower than the proposed by the transaction sender.
```

  This file has been truncated. [show original](https://github.com/ethereum/EIPs/blob/85c5f80c10810f5c3016f0983ea0a5c79788af55/EIPS/eip-3416.md)

---

**vbuterin** (2021-03-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/mtefagh/48/3417_2.png) mtefagh:

> which is the base fee will converge to zero over time

This does not follow. I agree that block size volatility will make the fee lower than it otherwise would have been, but decreasing the fee brings in increased demand, until the fee reaches an equilibrium where the greater demand compensates for the distortion. The fee should never just keep decreasing until zero (unless there really is no demand even at extremely low gasprices).

---

**mtefagh** (2021-03-28):

Let me rephrase my point more eloquently:

“Assume that the cumulative deviation of the sum of gas cost from the target gas cost times the number of blocks is bounded (has a finite upper bound which can be arbitrary large enough). Then, gas price converges to zero unless the gas used in each block converges to the constant function equal to the target gas (which will never happen in reality).”

In other words, your point is valid but shows that we should constantly and unboundedly overuse the blockchain more than the target gas to keep the gas price at around the same level. This violates the purpose and use of the word “target” in the first place!

---

**vbuterin** (2021-03-28):

Right, I agree that because of this issue it’s possible that long-run average usage will exceed the target by a couple percent. I’d support replacing the formula with an exponential curve (or at least a degree-2 Taylor approximation thereof) to cut that down to <0.1%, though that can be done in some future fork.

---

**mtefagh** (2021-03-28):

This suggestion has theoretical guarantees that this problem will never happen, and a simple trick provides a neat [equivalence](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/102?u=mtefagh) to an AMM model for gas pricing. If you are interested, I can elaborate more on the mathematical details of this alternate way of thinking about it as a dynamic pricing mechanism by constant product market makers.

---

**vbuterin** (2021-03-29):

> This suggestion has theoretical guarantees that this problem will never happen, and a simple trick provides a neat equivalence  to an AMM model for gas pricing.

That’s a nice result. Fascinating!

---

**mtefagh** (2021-03-29):

Consider a hypothetical automated market maker as a protocol-level price oracle for the trading pair GAS/ETH whose reserve of gas and ether after the n-th trade are g_n and f_n \times g_n, respectively. Moreover, let g_{n+1} = g_n + M/2 - w_n, that is, g += excess. It can be proved that the limit of f_n as the initial reserve g_0 goes to infinity is given by:

1. the Almgren-Chriss additive formula in the case of constant sum market maker,

![additive](https://latex.codecogs.com/svg.latex?%5Cmbox%7BGAS%20reserve%7D%20+%20%5Cgamma(%5Cmbox%7BETH%20reserve%7D)%20=%20g_%7Bn+1%7D%20+%20%5Cgamma(f_%7Bn+1%7D.g_%7Bn+1%7D)%20=%20g_n%20+%20%5Cgamma(f_n.g_n)%20%5C%5CLongrightarrow%20f_%7Bn+1%7D%20=%20f_n%20%5Cbig(%5Cfrac%7B%5Cgamma%20g_n%7D%7B%5Cgamma%20g_%7Bn+1%7D%7D%5Cbig)%20+%20%5Cfrac%7Bg_n%20-%20g_%7Bn+1%7D%7D%7B%5Cgamma%20g_%7Bn+1%7D%7D%20%5Cstackrel%7B*%7D%7B=%7D%20f_n%20%5Cbig(%5Cfrac%7B%5Calpha%7D%7B%5Calpha+%5Cgamma(M/2%20-%20w_n)%7D%5Cbig)%20+%20%5Cfrac%7Bw_n%20-%20M/2%7D%7B%5Calpha+%5Cgamma(M/2%20-%20w_n)%7D%20%5C%5CLongrightarrow%20%5Clim_%7B%5Cgamma%20%5Crightarrow%200%7D%20f_%7Bn+1%7D%20=%20f_n%20+%20%5Cfrac%7Bw_n%20-%20M/2%7D%7B%5Calpha%7D%20%5C(*)%20%5Cmbox%7B%20if%20%7D%20g_n%20=%20%5Cfrac%7B%5Calpha%7D%7B%5Cgamma%7D%20%5Cmbox%7B%20for%20some%20constant%20%7D%20%5Calpha)

1. and your proposed exponential formula in the case of constant product market maker.

![exponential](https://latex.codecogs.com/svg.latex?%5Cmbox%7BGAS%20reserve%7D%20%5Ctimes%20(%5Cmbox%7BETH%20reserve%7D)%5E%5Cgamma%20=%20g_%7Bn+1%7D(f_%7Bn+1%7D.g_%7Bn+1%7D)%5E%5Cgamma%20=%20g_n(f_n.g_n)%5E%5Cgamma%20%5C%5CLongrightarrow%20f_%7Bn+1%7D%20=%20f_n%20%5Cbig(%5Cfrac%7Bg_%7Bn+1%7D%7D%7Bg_n%7D%5Cbig)%5E%7B-1-%5Cfrac%7B1%7D%7B%5Cgamma%7D%7D%20=%20f_n%20%5Cbig(1+%5Cfrac%7BM/2-w_n%7D%7Bg_n%7D%5Cbig)%5E%7B-1-%5Cfrac%7B1%7D%7B%5Cgamma%7D%7D%20%5Cstackrel%7B*%7D%7B=%7D%20f_n%20%5Cbig(1+%5Cgamma(%5Cfrac%7BM/2-w_n%7D%7B%5Calpha%7D)%5Cbig)%5E%7B-1-%5Cfrac%7B1%7D%7B%5Cgamma%7D%7D%20%5C%5CLongrightarrow%20%5Clim_%7B%5Cgamma%20%5Crightarrow%200%7D%20f_%7Bn+1%7D%20=%20f_n%20.%20e%5E%7B%5Cfrac%7Bw_n-M/2%7D%7B%5Calpha%7D%7D%20%5C(*)%20%5Cmbox%7B%20if%20%7D%20g_n%20=%20%5Cfrac%7B%5Calpha%7D%7B%5Cgamma%7D%20%5Cmbox%7B%20for%20some%20constant%20%7D%20%5Calpha)

This observation immediately implies that both of these update rules (and any other one based on another constant function market maker) are path-independent. Ironically, this is exactly why we have arrived at these formulas in the first place when attempting to solve a simple instance of path dependence attacks.

---

**mtefagh** (2021-03-29):

For a cleaner LaTeX typesetting, see the following link:


      [fee](https://mtefagh.github.io/fee/#relation-to-constant-function-market-makers)




###

EIP-3416

---

**mtefagh** (2021-03-31):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That’s a nice result. Fascinating!

Apparently, they both have names in the economy. The version derived from the constant sum market makers is called the Almgren-Chriss model which I have [mentioned](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/26?u=mtefagh) two years ago. Also, your exponential formula has a name and is called the Bertsimas-Lo model, however, with a major difference explained and discussed in [here](https://ethereum-magicians.org/t/eip-1559-fee-market-change-for-eth-1-0-chain/2783/366?u=mtefagh).

