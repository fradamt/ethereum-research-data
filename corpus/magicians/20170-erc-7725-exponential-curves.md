---
source: magicians
topic_id: 20170
title: "ERC-7725: Exponential Curves"
author: ownerlessinc
date: "2024-05-30"
category: ERCs
tags: [erc]
url: https://ethereum-magicians.org/t/erc-7725-exponential-curves/20170
views: 788
likes: 1
posts_count: 1
---

# ERC-7725: Exponential Curves

Hello ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=15)

I’ve been looking into on-chain exponential curves for a while to assist in a reputation project that aims to decrease the soul-bounded governance power as time passes. Similar projects such as ENS have [implemented this](https://github.com/ensdomains/ens-contracts/blob/c15e4afd5f1e886094459e5e74d21dd080704443/contracts/ethregistrar/ExponentialPremiumPriceOracle.sol#L6) to decay the premium on expired names.

[ERC-7725](https://github.com/ethereum/ERCs/pull/498)

But every single project that strives to use exponential curves ends up using different formulas. Thus I’ve found myself developing a standard that everyone can use to easily manage exponential curves on-chain.

[EXPCurves](https://github.com/0xneves/EXPCurves) on GitHub

This smart contract implements an advanced exponential curve formula designed to handle various time-based events such as token vesting, game mechanics, unlock schedules, and other timestamp-dependent actions. The core functionality is driven by an exponential curve formula that allows for smooth, nonlinear transitions over time, providing a more sophisticated and flexible approach compared to linear models.

```solidity
function expcurve(
    uint32 currentTimeframe,
    uint32 initialTimeframe,
    uint32 finalTimeframe,
    int16 curvature,
    bool ascending
  ) public pure virtual returns (int256);
```

The smart contract provides a function called `expcurve` that calculates the curve’s decay value at a given timestamp based on the initial timestamp, final timestamp, curvature, and curve direction (ascending or descending). The function returns the curve value as a percentage (0-100) in the form of a fixed-point number with 18 decimal places.

We can create up to 4 types of curves or even keep a straight line. You can play around with the curvature (k) to determine the steepness of the curve.

You can also fork this [spreadsheet](https://docs.google.com/spreadsheets/d/1E4cLaAw3_9PI2IjZINoQz9u353N1NMxVicfYhctU_MM/edit?usp=sharing) and play with the formula and the resulting charts.

I’m currently writing the EIP but I would like to know if this contribution was previously developed to avoid duplicated work, otherwise, let me hear what you think and what I should’ve done differently!

[![ascending_with_positive_curvature](https://ethereum-magicians.org/uploads/default/original/2X/a/aa0e379655c5b4438f717b19f117b2631975c0b6.png)ascending_with_positive_curvature600×371 11.1 KB](https://ethereum-magicians.org/uploads/default/aa0e379655c5b4438f717b19f117b2631975c0b6)

[![descending_with_negative_curvature](https://ethereum-magicians.org/uploads/default/original/2X/2/220433927912537f24aa36fca262a3ce9fdf80af.png)descending_with_negative_curvature600×371 11 KB](https://ethereum-magicians.org/uploads/default/220433927912537f24aa36fca262a3ce9fdf80af)
