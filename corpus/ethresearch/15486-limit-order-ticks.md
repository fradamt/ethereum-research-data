---
source: ethresearch
topic_id: 15486
title: Limit Order Ticks
author: 0xrahul
date: "2023-05-04"
category: Decentralized exchanges
tags: []
url: https://ethresear.ch/t/limit-order-ticks/15486
views: 989
likes: 0
posts_count: 1
---

# Limit Order Ticks

**Introduction**

The concept of limit order ticks involves inserting new ticks on an AMM curve to allow for highly concentrated liquidity at a single price point. This feature improves price precision and enables users to place limit orders at a specific price, similar to order book exchanges.

**Implementation**

The liquidity on the AMM curve is concentrated on a single tick, which represents a significant improvement over legacy tick logic where liquidity was distributed between ticks in a range. Additionally, the limit order ticks are embedded in the concentrated AMM curve, and all the limit order ticks together represent an on-chain order book.

**Liquidity types**

- Concentrated Liquidity Concentrated liquidity is a liquidity model that is bi-directional in nature. It refers to liquidity that is used for a swap in a certain direction and can be utilized again if the trend reverses to the opposite direction. This allows it to convert back to the previous token.
- Limit Order Liquidity Limit order liquidity is a uni-directional liquidity concept. It refers to liquidity that is used for a swap in a certain direction and is not utilized if the trend reverses to the opposite direction. Hence, it does not convert back to the previous token.

**Conclusion**

Limit order ticks can allow users to create truly on-chain limit orders and create a limit order-book for decentralized exchanges.
