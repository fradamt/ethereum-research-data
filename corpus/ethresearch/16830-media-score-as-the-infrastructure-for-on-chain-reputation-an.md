---
source: ethresearch
topic_id: 16830
title: MEDIA SCORE as the Infrastructure for On-chain Reputation And User Value Assessment
author: 0xpeet
date: "2023-10-04"
category: Data Science
tags: []
url: https://ethresear.ch/t/media-score-as-the-infrastructure-for-on-chain-reputation-and-user-value-assessment/16830
views: 1472
likes: 4
posts_count: 2
---

# MEDIA SCORE as the Infrastructure for On-chain Reputation And User Value Assessment

# Why Does Web3 Need MEDIA Score?

In order to accurately assess users’ contributions to on-chain ecosystems, Trusta Labs has built MEDIA Score based purely on on-chain behaviors. The core goal of this system is to provide an objective, fair and quantifiable metric to comprehensively evaluate accounts’ on-chain engagement and value. MEDIA Score allows users to better know their own accounts, assess potential opportunities to earn ecosystem rewards, and interact with ecosystem projects more efficiently and reasonably. Meanwhile, MEDIA Score enables projects to accurately target users who have truly contributed to the project, and ensures resources and incentives are fairly distributed to these users.

# What is MEDIA Score?

MEDIA Score is an on-chain user value measurement within a range of 0–100 points. It aggregates a user’s on-chain behavior across five dimensions where M.E.D.I.A. stands for **M**onetary, **E**ngagement, **D**iversity, **I**dentity, and **A**ge respectively.

MEDIA Score designs in-depth indicators for each dimension that provide deep insights into on-chain activity, allowing users to better know their own accounts. MEDIA Score’s evaluation system covers not just simple statistics like amounts and numbers of a user’s interactions with smart contracts, protocols and dApps, but more importantly focuses on the breadth, depth and quality of a user’s interaction in on-chain activities.

Trusta Labs positions MEDIA Score as the infrastructure for on-chain user value assessment. In the KYA (Know Your Account) product called TrustGo from Trusta Labs, every user can look up their own unique MEDIA Score.

# MEDIA Indicator System

From a project’s perspective, the amount, depth, and breadth of a user’s interactions with the protocol are very important factors. At the same time, the user’s identity and credentials should also be considered in assessing them. Early adopters who accompanied the project’s growth reflect an even greater loyalty to the project. Based on this understanding, the MEDIA score designed the five dimensions of M.E.D.I.A.

## Monetary (25 points)

Interpretation: The monetary dimension assesses the financial value associated with an account. This indicator converts all tokens owned and traded by the account into USDT and shows the USD amount. In this dimension, a user can receive a maximum of 25 points.

Indicators:

- Balance: Check the account balance
- Total Interaction Amount: Total amount of interactions
- Official Bridge Amount: Total cross-chain amount on official bridges

## Engagement (30 points)

Interpretation: Assess whether the account is deeply engaged in on-chain ecosystem projects. A user with deep engagement not only has a large number of interactions, but their interactions are also unlikely to be concentrated in a single time period. In this dimension, a user can receive a maximum of 30 points.

Indicators:

- Active Days: Number of active days. Having at least 1 active interaction within a calendar day counts as 1 active day.
- Active Weeks: Number of active weeks. Having at least 1 active interaction within a calendar week counts as 1 active week.
- Active Months: Number of active months. Having at least 1 active interaction within a calendar month counts as 1 active month.
- Total Interactions: Total number of active interactions.
- Time Span Of Interaction: Time span from the first interaction to the most recent interaction.

## Diversity(15 points)

Interpretation: This dimension assesses the breadth (diversity) of contracts/protocols/categories interacted by the account. An on-chain user who is interested in projects across DeFi, NFT, Web3Game, and Infra categories is rare and valuable. Based on this thinking, We decrease the weight of this dimension and assign a maximum score of 15 points to this dimension.

Indicators:

- Unique Contracts Interacted: Number of unique contracts interacted with
- Unique Protocols Interacted: Number of unique protocols interacted with
- Unique Protocol Categories Interacted: Number of unique protocol categories interacted with

## Identity (10 points)

Interpretation: This dimension focuses on the specific identity roles and credentials of the account within the L1/L2 ecosystem. In this dimension, a user can receive a maximum of 10 points.

Indicators:

- Being a multisig signer, a DAO member, or holding a specific NFT, such as a zkSync Officially issued NFT
- Arbitrum airdrop users, Optimism airdrop users
- ENS holders

## Age (20 points)

Interpretation: A project’s early users are very valuable during the cold start phase. These users grow with the project, demonstrating a higher degree of loyalty. In this dimension, a user can receive a maximum of 20 points.

Indicators:

- Days Since First Bridge: Number of calendar days since the address first bridged token in.
- Days Since First Interaction: Number of calendar days since the address first actively interacted.

# MEDIA Scoring Methodology

## Computational Logic

[![](https://ethresear.ch/uploads/default/optimized/2X/9/9674782c9cd170658b34cf4e2341fbedede6bb64_2_690x287.png)1123×468 74.2 KB](https://ethresear.ch/uploads/default/9674782c9cd170658b34cf4e2341fbedede6bb64)

The Diagram is an illustration of the bottom-up computational logic of the MEDIA score:

1. The first step is to transform and normalize the variables using a normalized tunable sigmoid function. This function ensures that the values of the variables are mapped to a standardized range, allowing for consistent comparison and analysis.
2. For each of the five dimensions (Monetary, Engagement, Diversity, Identity, and Age), a subscore is computed. This is achieved by taking a weighted sum of all the variables within that dimension. Each variable is assigned a weight that reflects its relative importance in determining the overall score for that dimension.
3. After calculating the sub-scores for each dimension, they are scaled to a range of 0 to 100. This scaling process standardizes the sub-scores, making them easier to interpret and compare across different dimensions.
4. Finally, the MEDIA score is calculated by taking a weighted sum of all the sub-scores. Each sub-score is multiplied by its respective weight, reflecting its significance in contributing to the overall value assessment.

## Sigmoid Transformation

The Sigmoid function， represented by the equation,

is a non-linear S-shaped transformation function. As the input values x increase, the output y gradually transitions from 0 to 1. This gradual transition allows the sigmoid function to capture non-linear relationships. In the normalized tunable sigmoid function used in the MEDIA scoring system, there is a parameter that controls the pace or speed at which y transitions from 0 to 1 as x increases. This parameter allows for fine-tuning the behavior of the sigmoid function to match the desired range and sensitivity of the scoring system.

# An Example of MEDIA Score

Shown in the Figure is our MEDIA Score snapshot in TrustGo product. As of Aug 8, 2003, the queried account 0x0C…65BE had a MEDIA score of 64, ranking in the top 26% among all zkSync Era accounts.

This address scored 93 for interaction diversity, interacting with a relatively high variety of contracts and protocols. However, this address lags on interaction amount, currently scoring only 41. To effectively improve the MEDIA score, this user could focus on increasing the interaction amount. The 20 points this account obtained in the Identity dimension mainly come from proof of claiming and holding zkSync’s official NFT. Although this account did not receive previous airdrops for $ARB and $OP, it could improve its Identity dimension score by registering an ENS domain. In the future, we will enrich the Identity dimension by adding more credentials that represent on-chain reputation, achievements, and contributions.

# Summary

MEDIA Score is an objective, fair and quantifiable metric to comprehensively evaluate accounts’ on-chain engagement and value. By performing in-depth quantification and measurement of user behaviors within the blockchain ecosystem, MEDIA Score assigns a score from 0–100. MEDIA Score’s evaluation system covers not just simple statistics of interaction amounts and values with smart contracts, protocols, and dApps, but more importantly focuses on the breadth and depth of a user’s participation in on-chain activities, their loyalty, and any special identity roles and credentials held by the user.

Trusta Labs aims to continuously develop MEDIA Score as the infrastructure for on-chain user value assessment. In the KYA (Know Your Account) product called TrustGo (https://trustgo.trustalabs.ai/search) from Trusta Labs, every user can look up their own unique MEDIA Score. It helps to fairly identify accounts that contribute to the ecosystem. Through MEDIA Score, users can gain a deeper understanding of their on-chain activities and value, while project teams can accurately allocate resources and incentives to users who truly contribute.

Twitter: @trustalabs

Medium: https://medium.com/@trustalabs.ai

## Replies

**simbro** (2023-11-24):

It’s great to see more plurality and optionality for computing reputation scores in web3, especially with such a comprehensive methodology as this.   Do you think there is a way to do any analysis on how the MEDIA score compares to other scores such as GitCoin Passport, or some of the several other emergent reputation scores that user’s can use?  Is too early to start thinking about a comparison framework that would help users and dapps that consume such scores to understand the similarities and differences?

