---
source: ethresearch
topic_id: 22225
title: "Fair fees: A dynamic formula for balancing dapp value creation/capture"
author: owocki
date: "2025-04-27"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/fair-fees-a-dynamic-formula-for-balancing-dapp-value-creation-capture/22225
views: 515
likes: 3
posts_count: 1
---

# Fair fees: A dynamic formula for balancing dapp value creation/capture

Authors: Kevin Owocki, Devansh Mehta (@thedevanshmehta), inspiration from Vitalik Buterin

# Scope

IMPORTANT: THIS IS A PROPOSAL ONLY FOR INDIVIDUAL APPS TO THINK ABOUT MONETIZING THEIR APP.  IT IS *NOT* A PROPOSAL TO CHANGE ANY ECONOMICS AT PROTOCOL LAYER!

## TLDR

We propose a sustainable fee structure for individual apps to bake into their economic model  that addresses a fundamental tension:

1. builders need financial incentives to create and maintain these systems,
2. but excessive fees undermine their effectiveness.

Our approach provides higher proportional returns for smaller funding flows while gradually decreasing to a minimal percentage for larger ones, ensuring both sustainability and fairness across the entire ecosystem of public and private goods funding.

## Executive Summary

Builders of dapps face a fundamental tension: they need viable revenue to develop and maintain these systems, but excessive fees can undermine their purpose and effectiveness.

This post outlines our proposed solution - a dynamic fee structure that works across the spectrum of dapps, whether they’re dapps for funding public goods, private ventures, or anything in between.

Our approach aims to strike the right balance between rewarding the crucial work of mechanism builders while ensuring the majority of funds reach their intended destinations. By implementing a formula-based approach, we create appropriate incentives at various funding scales without excessive rent extraction.

## Problem Statement

Dapps- which include crowdfunding platforms, public goods funding, private investment vehicles, grants programs, and many hybrid models - face a critical challenge that threatens their long-term sustainability:

1. Need for Financial Return: Building and maintaining dapps requires significant investment of time, expertise, and resources. Without adequate financial returns, talented builders are less likely to dedicate themselves to creating and improving these crucial systems.
2. Risk of Excessive Extraction: Conversely, if the financial incentives are too high (or become too high over time), the system risks being perceived as extractive. This can undermine trust in the mechanism and reduce its effectiveness in directing capital to its intended purpose, whether that’s public goods, private investments, or something in between.

This creates a fundamental tension in designing dapps across the entire spectrum from purely public to purely private goods. Too little financial incentive and the ecosystem struggles to attract talented builders who can build such mechanisms; too much and the systems risk extracting excessive value from the very projects they aim to support and reduce enthusiasm from customers to even use the mechanism

## Solution: A Dynamic Fee Structure

We propose a simple formula to balance the value created by new dapps with the value captured by those who built it:

if projects get $N, builders get $max(sqrt(1000 * N), N * 0.01)

In plain English:

- For smaller funding amounts, the fee follows a square root function (sqrt(1000 * N)), providing proportionally higher returns to make building mechanisms for smaller pools worthwhile. For example, if the funding pool is $170,000, then root of 1000 * 170,000 = $13,038.4 or 7% is taken as overhead.
- Once funding exceeds $10 million, the fee transitions to a flat 1% rate (N * 0.01)
- This creates a smooth curve that decreases proportionally as the funding amount increases

Visualizing this fee structure: (TVF = total value flowed)

[![AD_4nXeeGDBZfR29aE8mu9A-vSzM7IiPNoETwvISnuwdRyf6ansL7U_sWUp-QqLl-EwXfM8uFsh3m4f_QRqK-lwxwKt1byonyaMLuHDbTtFSJ5t-L-hL_2EpiuSPXER8qpMVocNu9Ijbkw-1](https://ethresear.ch/uploads/default/original/3X/c/a/cadfc1175445feb6b463ce4ce5a4971781a54448.png)AD_4nXeeGDBZfR29aE8mu9A-vSzM7IiPNoETwvISnuwdRyf6ansL7U_sWUp-QqLl-EwXfM8uFsh3m4f_QRqK-lwxwKt1byonyaMLuHDbTtFSJ5t-L-hL_2EpiuSPXER8qpMVocNu9Ijbkw-1592×736 14.2 KB](https://ethresear.ch/uploads/default/cadfc1175445feb6b463ce4ce5a4971781a54448)

This approach ensures that:

1. Small-scale dapps remain financially viable to build and maintain, boosting experimentation in the space
2. As dapps grow larger, the proportion directed to fees decreases
3. There’s a predictable, transparent mechanism for all participants to rely upon.

You can experiment with different funding amounts using[this spreadsheet](https://docs.google.com/spreadsheets/d/189KZ2zpFyf18XOV9jWL7mgDiLy9aylS_vVzvCFK_Rlc/edit?gid=699870709#gid=699870709) to see how the formula works across various scales.

## Outstanding Questions

While we believe this formula represents a promising approach, several questions remain open for community discussion:

1. Formula Decay Speed: Is the current rate at which the proportional fee decreases appropriate? Should it decrease more rapidly or slowly?
2. Minimum Threshold: Is 1% the right minimum rate, and is $10 million the appropriate threshold at which to reach this minimum?
3. Fee Distribution: Should this fee be directed entirely to dapp builders, or should some portion flow to dependencies of the project itself? Should the formula be applied fractally down the dependency stack?

## Next Steps

To move from theory to practice, we propose the following next steps:

1. Begin experimenting with these fee mechanisms in smaller test rounds across different types of capital allocation dapps (public goods funding, private investment pools, other models)
2. Possible specific pilots

Implement this as a fee mechanism for community round organizers in the upcoming Gitcoin Grants round (GG24)
3. Implement this as a fee mechanism for novel capital allocation experiments, like Deep Funding.

Consider directing 10-25% of the overhead charged with the formula to funding dependencies of the mechanism itself (such as underlying smart contracts and open source repos that it uses) to transform what might feel like an extractive fee into a constructive experiment to fund the mechanisms own dependencies

## Conclusion

dApps - whether funding crowdfundign platforms, public goods funding, private ventures, or anything in between - require sustainable incentives to thrive. The formula we’ve proposed aims to create appropriate rewards for builders while ensuring the vast majority of funds reach their intended destinations.

By implementing a dynamic fee structure that scales with funding amounts, we can create a balanced system that works effectively across different funding scales and use cases. This approach avoids the extremes of insufficient incentives or excessive extraction, creating a more sustainable ecosystem for experimentation with dapps.

We invite the community to experiment with this approach, provide feedback, and help refine these mechanisms. Together, we can build funding systems that effectively direct capital throughout the ecosystem while fairly compensating those who build and maintain these crucial allocation mechanisms.

## Appendix - Accrued Fees in a CrowdFunded World

In a more emergent, crowdfunded world, then this mechanism would allocate fees differently than in a world where one big pool is set out.

Here’s an example:

1. Say, a pool of $10k is set aside, and the fee recipient is sent only the fee once, at 32%.  .
2. Say, a more emergent pool of $10k is put together by two seperate donations sent at t1 and t2.  First a pool of of $5k is set aside with a 45% fee (which is then sent to the fee recipient). Then another $5k is added to the pool, reducing the fee to 32% (which is then sent to the fee recipient at newer, lower rate).  Because the fee was accrued over time, the fee recipieint receives more money.

In this example, the fee is calculated differently if its distributed in an accrued methodology vs a basic methodology. Here is how the fee works in both scenarios.

| Basic Methodology | $10k * 32% = $3.2k |
| --- | --- |
| Accrued Methodology | $5k * 45% + $5k * 32% = $3850 |

In prettymuch any scenario, the accrued methodology is more generous to the fee collector than the basic methodology. Here’s the difference between the two.

[![3f6675eabdd21a17d9d93c842bf5d4c11df65461_2_1248x766](https://ethresear.ch/uploads/default/optimized/3X/9/d/9d6107cb1a827329aef3dd8e9ef5a3af9e3205a1_2_690x423.png)3f6675eabdd21a17d9d93c842bf5d4c11df65461_2_1248x7661248×766 52.1 KB](https://ethresear.ch/uploads/default/9d6107cb1a827329aef3dd8e9ef5a3af9e3205a1)

We suggest using basic methodology for basic funding pools, and the accrued fee for more crowdfunded pools; though how exactly to implement the formula is up to the implementor. We’ve put an[‘accrued fees’ tab in the worksheet](https://docs.google.com/spreadsheets/d/189KZ2zpFyf18XOV9jWL7mgDiLy9aylS_vVzvCFK_Rlc/edit?gid=1466396196#gid=1466396196)to help you work with this methodology.

---

x-post: [Fair fees: A dynamic formula for balancing value creation and value capture - Research & Strategic Intelligence - ⛲️ Allo.Capital](https://research.allo.capital/t/fair-fees-a-dynamic-formula-for-balancing-value-creation-and-value-capture/322)
