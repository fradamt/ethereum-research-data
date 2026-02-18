---
source: ethresearch
topic_id: 13247
title: "\"Hiding\" the P + epsilon attack with staking delegation"
author: llllvvuu
date: "2022-08-05"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/hiding-the-p-epsilon-attack-with-staking-delegation/13247
views: 1612
likes: 0
posts_count: 1
---

# "Hiding" the P + epsilon attack with staking delegation

> Note: There is plenty of discussion around liquid staking derivatives (LSD), so I apologize if this repeats some ideas.

**Abstract:** Much of the worry around staking delegation pertains to monopoly and centralization. We argue that the opposite (perfect price competition) is also a risk, mirroring the [P + epsilon attack](https://blog.ethereum.org/2015/01/28/p-epsilon-attack/). We also characterize incentives for a delegate to misbehave (principal-agent problem) as well as the delegators’ share of burden of the agency cost.

## Delegation today

In Ethereum, a majority of stake is delegated to a single DAO, perhaps with the help of liquidity mining (LM). In Cosmos, delegators seem to prioritize “spreading out” stake to some degree; it is also possible to sort by commission, but this does not seem to be the #1 motivating factor. In both Cosmos and Ethereum, the largest validators are typically doxxed.

## Agency theory

In undelegated staking, we face the following incentives/disincentives to double-spend:

- the exit liquidity available on counterparties (CEXes, bridges, etc) during the undetected period of the attack
- social fork and slashing
- a collapse of the ecosystem, including a collapse of the token price to 0

We make the optimistic assumption that the last point always happens, such that a double-spend is necessarily an exit-scam, thus facing the harshest cost/benefit tradeoff.

Delegation splits these incentives/disincentives among *principals* (delegators) and *agents* (delegates). The agents have the following incentives/disincentives:

- the exit liquidity available on counterparties (CEXes, bridges, etc) during the undetected period of the attack
- loss of future commissions
- any costs associated with being doxxed

whereas the principals are weighing yield vs risk of a total loss of capital.

## What happens in perfect fee competition?

We consider two models: one where users sort by yield (unlike the monopoly model, there are no network effects), and one where users factor in both yield and *agency costs* (note that there are high search costs for searching this way, which is one plausible explanation for network effects).

Suppose users naively sort by yield. Then there is an exposure to *adverse selection* (unscrupulous delegates would offer low-commissions and LM rewards) and *moral hazard* (scrupulous delegates could become unscrupulous upon commissions declining). This is analogous, but not equal (as we’ll discuss later), to the [P + epsilon attack](https://blog.ethereum.org/2015/01/28/p-epsilon-attack/), in which a marginal increase in yield attracts users.

The solution to P + epsilon is [subjectivity](https://blog.ethereum.org/2015/02/14/subjectivity-exploitability-tradeoff/), which imposes an *agency cost* on unscrupulous delegates even when they have a supermajority. However, our setting has a few differences:

- Users are guaranteed to receive epsilon regardless of whether there is an attack or not.
- There is not guaranteed to be an attack.

As such, the agency cost for selecting a cheap / high-yield delegate is not 100% (or whatever the success rate of the subjectivity mechanism is). Instead, the agency cost is related to how much the marginal delegation adds to the chance of attack; one may model it as a game of chicken, where there is no marginal cost to being the first delegator but there is a large cost to being the delegator which crosses the threshold for an attack. This threshold could be obscured via Sybils and/or collusion (Sybils can be quite convincing; [see this recent example](https://www.coindesk.com/layer2/2022/08/04/master-of-anons-how-a-crypto-developer-faked-a-defi-ecosystem/)). More research is wanted to understand what exactly the agency costs are in this scenario. If 10% APY is enough to take the gamble, one could imagine an attacker of a smaller chain keeping the rewards on for a month - whether it is worth it would be borderline. If zero-commission is enough, then an attacker could sustain the fundraise forever. This would be a bit more concerning, given the crypto community’s love and trust of anons, yield, and especially yield products built by anons.

We also note again that there does not need to be an attacker fundraising at low-to-negative commissions. Marginal price competition among scrupulous delegates could push commissions to zero without being held back by marginal agency costs (due to the game of chicken) and potentially corrupt said delegates.

## Conclusion

Different delegate markets have different search costs and lead to different choices. Norms also lead to selfless behavior. Further research is wanted in order to understand the delegate selection process and have stronger guarantees that people will not gravitate towards unscrupulous delegates.
