---
source: ethresearch
topic_id: 1687
title: Adversarial Shortsell Probability = Sum(dapps price) / Sum(ETH price)
author: sg
date: "2018-04-10"
category: Economics
tags: []
url: https://ethresear.ch/t/adversarial-shortsell-probability-sum-dapps-price-sum-eth-price/1687
views: 4164
likes: 4
posts_count: 6
---

# Adversarial Shortsell Probability = Sum(dapps price) / Sum(ETH price)

I saw a discussion on Japanese twitter world.

And here is no such discussion so far (as far as I’ve seen) hence I post this summary of that discussion.

## Problem and attack procedure

1. When “the sum of dapps price is far bigger than the sum of Ethereum price” scenario
2. Short-selling on dapps on DEX
3. Do the 51% attack on Casper PoS Ethereum, then make network paralyze
4. Make money

## Solution

- Mitigation for excessive “mother-children ratio”(=ETH-dapps ratio)
- Discouragement of adversarial short-sell

## Ambiguity, excuse, and help wanted

- How the community’s thought?
- What is the current “mother-children ratio”?
- Indeed a PoW-based smart contract chain is weaker because mining machine cannot be a collateral, and reusable. (If that is ASIC poisoned chain, it can work as collateral fortunately ツ )
- The mitigation for this issue is Casper PoS, because when the 51% attack happens, that 51% amount of collateral gonna be lost its value
- No simulation for short-sell profitability and 51% attack’s cost, need feedback

## Replies

**vbuterin** (2018-04-10):

I think I see. The argument is that even though attacking ethereum to short-sell ETH may not work (as a successful 51% attack would also burn >1-5m ETH, so it may well on net make the price go up (!!)), but it could easily interfere in any dapps on top of ethereum in the meantime with no compensation. This is certainly an issue. Mitigations I can think of are:

1. Designing dapps so that they maximally “fail safe”; try to avoid assuming liveness on scales of less than a few weeks as a security assumption.
2. Plasma and state channels - even if the underlying blockchain fails, most layer-2 constructions lead to zero loss of service if you temporarily introduce the additional assumption that the counterparty/operator is honest. That is, for plasma or channel constructions to break, both the main chain and the counterparty/operator must be trying to attack you.
3. Protocol changes such as rent and fee reclaiming which burn a portion of txfees; this ensures that the value of ETH goes up under conditions of high demand for dapp usage, making it less likely that dapps will have a high value without ETH having a high value.

---

**ldct** (2018-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> That is, for plasma or channel constructions to break, both the main chain and the counterparty/operator must be trying to attack you.

I guess we should distinguish between “break” in the sense of “irregular state transition / money is stolen” and “cannot provide the service to the user”, since even if a plasma operator is honest users might not be willing to continue making state transitions on the plasma chain, leading to a drop in the price of some app token.

---

**vbuterin** (2018-04-10):

Agree; I was talking about safety failures. If we’re talking about liveness failures, then the operator/counterparty attacks that can break liveness, but the main chain breaking cannot even break liveness, at least with state channels; with plasma you would have to rely on cryptoeconomic commitments to include things in some order.

---

**sg** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> successful 51% attack would also burn >1-5m ETH

Let me elaborate. I assume this burning would be caused by community initiated hardfork, is this correct?

I couldn’t understand “how” burning comes with this scenario.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> maximally “fail safe”

True. Some earlier implemented sidechain might not have this parental fail-safe though, matured sidechain must have it by default. All earlier implemented sidechain must upgrade themselves as new security insight comes up. This is little bit hard part to me as Plasma lover.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> assumption that the counterparty/operator is honest.

In the “malicious party trying to attack the Rootchain” scenario, Casper PoS internally-applied nth-layer chains are also can be target of “collateral share overwhelming”. And it’s easier because nth-chains are rely on the Rootchain security. Hence I doubt “zero loss” is over expressive, yet still I can agree what you intended to say.

BTW, I got an insight that under this nth-chain also overwhelmed scenario, only the targeted “CDS or DEX used short-sell executor chain” might be kept alive for enabling attack.

postscript)

- If I could understand “burning” rationale, almost all doubt will be not a big deal.

---

**vbuterin** (2018-04-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/sg/48/14420_2.png) sg:

> If I could understand “burning” rationale, almost all doubt will be not a big deal.

The idea is that if ETH gets partially burned if paid for transaction fees, there’s a direct connection between expected future transaction fees and the value of ETH, so if there’s (expected to be) a very high level of base-chain activity, the value of ETH will incorporate that prediction, so there’s a natural upper bound to the ratio between expectations of future activity (and therefore value) of on-chain dapps and the value of the total amount of ETH.

