---
source: magicians
topic_id: 6336
title: Addressing common criticisms about Ethereum
author: kladkogex
date: "2021-05-26"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/addressing-common-criticisms-about-ethereum/6336
views: 955
likes: 3
posts_count: 1
---

# Addressing common criticisms about Ethereum

A notable article was posted on Reddit, addressing “rollup-centric” view of ETH2.

https://www.reddit.com/r/ethereum/comments/najp2c/addressing_common_criticisms_about_ethereum/

Here are some alternative thoughts on the subject:

*“What’s missing are generalized programmable rollups.”*

There are several points that prevent the adoption of rollups as a generic solution.

- Rollups are inferior to PoS blockchains in terms of centralization, MEV extraction, censorship, government-action resistance
- In PoS you at have rotating block proposers that do not know in advance if they are going to propose. In addition, threshold encryption completely solves MEV for fixed size chains.
- For rollups, the rollup operator is an uber-MEV extractor with unlimited capabilities.
- Government can simply shut down rollups by a single action since all rollups that run today are executed literary by a single party on a single computer (take Loopring  or Optimism as an example).
- Due to centralized nature rollups will probably need to satisfy KYC/AML rules
- no economic model has been developed for rollup operator fees. Clearly, the rollup operator is an uber-monopolist that can dictate fees
- economic evolution naturally leads to all rollups except one dying and the remaining one becoming an Uber-rollup, differing very little from centralized exchanges.
- as other people here have noted, no economic model has ever been developed for rollup verifiers. They have no profitable way to exist
- no satisfactory economic model has ever been developed for dynamically selecting a rollup operator among many candidates. If the model is simply stake based, it will naturally lead to one operator growing and others dying, until most of the stake is controlled by the Uber-operator

*“The first upgrade, beacon chain, went live in Dec 2020, The Merge is actively being developed (the second devnet is going live today) and scheduled to release by late 2021.”*

There are several points that have not been demonstrated

- ETH2 running stably with large blocks.  The current ETH2 net essentially produces empty blocks.
- ETH2 + ETH1 merge being able to run as fast as ETH1 (at least 15M gas blocks and 15 sec block times).  For me personally, it is a question mark, because clearly many ETH2 proposers may have slow network connections as compared to ETH1 mining pools.

" Fortunately, Ethereum is moving to proof-of-stake within the next 9 months, which will cut Ethereum’s energy consumption by 99+%."

Since ETH2 and rollups are more vulnerable to MEV extraction then PoW,  as DeFi grows in complexity, it becomes inevitable for huge neural network farms will appear to win the MEV extraction war. Therefore,  MEV on ETH2 and rollups may end up using more energy than PoW.
