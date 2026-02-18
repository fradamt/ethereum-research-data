---
source: magicians
topic_id: 17926
title: Targeting Optimal Staking Percentage and Minimizing Emission
author: DB_1
date: "2024-01-07"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/targeting-optimal-staking-percentage-and-minimizing-emission/17926
views: 537
likes: 0
posts_count: 1
---

# Targeting Optimal Staking Percentage and Minimizing Emission

Currently we may have too many validators, creating challenges in aggregating signatures and overpaying for security. This is in part due to the Ethereum emission schedule. The proposed change adjusts the total emissions of Ethereum (ETH) to peak at 33% of ETH staked, decrease linearly to zero at 66% of ETH staked, and remain at zero emissions for any staking level beyond 66% up to 100%.

**Motivation**

The current Ethereum emissions increase schedule dictates an increase when more validators are joining, even when too many validators are participating. This modification aims more tightly control the  incentivization for staking, reinforcing Ethereum’s economic security and sustainability.

**Specification**

- Emission Peak: Emissions go linearly from 0 to 33%, and peak when 33% of total ETH supply is staked. An APY of 10-20% at 10% staking and 3-4% at 33% staked can be targeted.
- Linear Decrease: Emissions decrease linearly from the peak at 33% staking to zero emissions at 66% staking.
- Zero Emissions Beyond 66%: Once 66% of ETH is staked, the emission rate stays flat at zero, regardless of additional staking up to 100%.

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/9/9a6401953a5ade1930447bb1fff459ddd8398636_2_690x406.png)image1521×895 130 KB](https://ethereum-magicians.org/uploads/default/9a6401953a5ade1930447bb1fff459ddd8398636)

**Rationale**

This emission schedule is designed to create a balance between incentivizing staking and controlling the inflation rate of ETH. By allowing the emissions APY to go to zero, we allow for better control over the number of validators. While the exact staking rate or APY, which also depended on unknown MEV rewards, cannot be predicted, this proposal guarantees both strong incentives for low double-digit staking percentage, and reduced cost to Ethereum when staking percentage becomes high. This can be further adjusted after restaking gains adoption, for peak emissions in the 10%-33% range.

By not going negative in any part of the curve, we ensure there is no incentive for vanilla (no MEV) stakers to leave.

**Security Implications**

This change is expected to enhance network stability by reducing the number of validators. It will reduce the economic guarantees of the network, however, these are arguably too high.  Additionally, the low/zero emission rate at higher staking levels reduces total ETH supply, contributing to economic stability.

**Backward Compatibility**

This change is backward compatible as it does not affect existing transactions or smart contracts. It only modifies the staking rewards calculation method and can be implemented with minimal disruption to the current Ethereum infrastructure.

**Conclusion**

The proposed modification to the Ethereum emission schedule aims to strike a balance between incentivizing staking, controlling inflation, and ensuring network security. This change is expected to have a positive impact on the Ethereum ecosystem’s long-term stability and sustainability.
