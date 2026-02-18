---
source: magicians
topic_id: 12826
title: Categorizing DeFi lending protocols by software risk
author: dcota
date: "2023-02-03"
category: Magicians > Primordial Soup
tags: [security, defi, risk]
url: https://ethereum-magicians.org/t/categorizing-defi-lending-protocols-by-software-risk/12826
views: 770
likes: 0
posts_count: 1
---

# Categorizing DeFi lending protocols by software risk

Hi Ethereum Community,

I’d like to start by introducing myself and the project I am working on, then move on to the topic of this discussion.

I am Daigaro and I am one of the co-founders of a project called [Fuji Finance](https://twitter.com/FujiFinance). At Fuji, we built the first borrowing money market aggregator and deployed it on Ethereum in May 2021. During our journey to find product-market-fit, we learned several lessons and now we are expanding the same concept but with money market aggregation across L2s/chains.

Aggregation of money markets consists of two general concepts:

1. Routing users to the lending market with the best interest rate, either the highest lending APY or the lowest APR for borrowers.
2. Rebalancing or refinancing the assets of pooled users from a current money market to one with better lending-borrowing interest rates, meaning moving the user/users’ positions or assets to another market when interest rates are better.

While these two concepts are a technical challenge on their own, we have addressed most of them. An interesting [Twitter conversation](https://twitter.com/hasufl/status/1612396212233142273) covered many of the other challenges of money market aggregation, with key players identifying challenges we have faced.

An important point to note is that money markets are not equal, meaning their risk levels are not the same. When aggregating a series of money markets, your risk exposure is that of the “weakest link” and users should be aware of this.

This problem led us to begin discussions with several groups on how this risk should be categorized. Being no experts in the matter, we bring the discussion here for the community and experts to discuss.

With the help of RiskDAO, we have synthesized the risk categories into three general fields, with ideas on how to measure them quantitatively or qualitatively:

1. Trust in the DAO/organization behind the money market:
1.a. Minimum economic power required to pass a vote and change the protocol parameters.
1.b. Number of entities required with enough economic power to pass a vote (looking into governance token distribution).
2. Trust in the code of the money market:
2.a. Amount of bug bounties relative to TVL.
2.b. Number of completed security audits.
2.c. Time elapsed since last version release.
3. Protocol economic risk exposure:
3.a. Exposure to volatile assets.
3.b. Exposure to low cap assets.
3.c. Exposure to “funny” stable coins and assets.
3.d. Type and reliability of price oracles used.

With that said, we open the discussion to find insights or, hopefully, reach consensus on what a proper risk rating system for money markets should be.
