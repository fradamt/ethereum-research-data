---
source: magicians
topic_id: 6760
title: DAI-like stable asset pegged to BASEFEE (post EIP-1559)
author: shadycoderjeff
date: "2021-08-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/dai-like-stable-asset-pegged-to-basefee-post-eip-1559/6760
views: 525
likes: 0
posts_count: 1
---

# DAI-like stable asset pegged to BASEFEE (post EIP-1559)

Hi Friends,

I wanted to seek feedback on designing a token, say $FEE, which is pegged to BASEFEE.

Motivation:

1. Hedge against varying BASEFEE with the expected demise of CHI/GasTokens (post EIP-3529)
2. Meta transactions are better price din BASEFEE
3. Growing demand for a stable coin which is not pegged to currencies of nation states (inspired by RAI and also several tweets by prominent thinkers)

Why is BASEFEE a good unit of account for motivation #3? Because BASEFEE always buys you a certain quantity of compute resource (can be considered a proxy to a certain kind of basket of goods).

Proposed design:

1. Users lock X ETH in a contract and mint Y BaseFeeTokens where X / Y >= C * BASEFEE, C is the collateralization ratio
2. Liquidation, redemption etc like Maker
3. BASEFEE can double/halve in 6 blocks, C needs to be large enough to cover liquidation window of N blocks

A big benefit of pegging to BASEFEE: No oracles needed anywhere, BASEFEE is available in the EVM directly.

Would be happy to hear thoughts of like-minded people around refining the design.
