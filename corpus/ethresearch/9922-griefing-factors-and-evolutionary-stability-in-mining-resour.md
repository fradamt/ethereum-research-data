---
source: ethresearch
topic_id: 9922
title: Griefing factors and evolutionary stability in mining resource allocations
author: sleonardos
date: "2021-06-24"
category: Economics
tags: []
url: https://ethresear.ch/t/griefing-factors-and-evolutionary-stability-in-mining-resource-allocations/9922
views: 959
likes: 1
posts_count: 1
---

# Griefing factors and evolutionary stability in mining resource allocations

In our recent paper “*From Griefing to Stability in Blockchain Mining Economies*” [[arxiv link](https://arxiv.org/abs/2106.12332)] with [@georgios](/u/georgios), [@SHSR2001](/u/shsr2001) and Marco, we study the incentives of miners to allocate their (mining) resources in an ecosystem of multiple blockchains.

The main technical idea of the paper is largerly motivated/inspired by this post on [griefing factors](https://ethresear.ch/t/a-griefing-factor-analysis-model/2338), and, as a special thanks, we thought to share its main findings/insights here. Any feedback would be greatly appreciated! Thank you!

Our key findings are the following:

- The main technical contribution is that griefing is closely related to the game-theoretic notion of evolutionary stability. Specifically, we show that an allocation (of mining resources) in a single (minable) blockchain is evolutionary stable if and only if all its individual griefing factors are less than 1 (non-griefable allocation).
- This (surprising) equivalence (non-griefable = evolutionary stable) holds for homogeneous populations of miners (equal costs) for which evolutionary stability is defined. Thus, griefing factors (which are defined also for non-homogeneous populations) can be used to generalize the notion of evolutionary stability to arbitrary populations and may thus, constitute a tool of independent interest in game theory.
- We show that the unique Nash equilibrium is griefable, in the sense that miners have incentives to allocate more resources than predicted by the Nash equilibrium. In the unique evolutionary stable (non-griefable) equilibrium allocation, miners dissipate excess resources (over-mining) which provides a theoretical explanation for the increasing energy waste (in PoW blockchains), the consolidation of mining power in few entities and the high entry barriers that are currently observed in practice.
- The previous (negative) result hinges on the assumption that each miner can influence aggregate market outcomes. If each miners’ capacity is negligible in comparison to the total network resources (as originally envisioned), then griefing is no more a concern.
- In this case, we calculate the market equilibria (which are approximate Nash equilibria) and find evidence that the proportional profitability ratio is the main metric that drives miners decisions on how to distribute their resources among different blockchains.
- Our empirical results suggest that risk diversification, restricted mobility of resources between different networks (as enforced by the use of incompatible mining technologies) and growth of the miners’ network are all factors that contribute to the stability of the mining allocations in the long-run.

---

You can e-mail questions/comments to: [sleonardos@outlook.de](mailto:sleonardos@outlook.de).

---

**Reference:** Yun Kuen (Marco) Cheung, Stefanos Leonardos [@sleonardos](/u/sleonardos), Georgios Piliouras [@georgios](/u/georgios) and Shyam Sridhar [@SHSR2001](/u/shsr2001), *From Griefing to Stability in Blockchain Mining Economies*, arxiv-eprint:2106.12332, 2021.
