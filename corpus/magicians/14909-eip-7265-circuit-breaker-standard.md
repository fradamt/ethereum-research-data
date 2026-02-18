---
source: magicians
topic_id: 14909
title: "EIP: 7265 - Circuit Breaker Standard"
author: diyahir
date: "2023-07-03"
category: EIPs
tags: [erc]
url: https://ethereum-magicians.org/t/eip-7265-circuit-breaker-standard/14909
views: 3291
likes: 4
posts_count: 5
---

# EIP: 7265 - Circuit Breaker Standard

This standard outlines a smart contract interface for a Circuit Breaker that triggers a temporary halt on protocol-wide token outflows when a threshold is exceeded for a predefined metric. This circuit breaker does not assume the structure of the underlying protocol, and mainly serves as a pass-through vehicle for token outflows. In order to maintain correct internal accounting for integrated protocols, and to provide maximum flexibility for developers, developers can specify if the circuit breaker contract should delay settlement and temporarily custody outflows during the cooldown period, or revert on attempted outflows.

https://github.com/ethereum/EIPs/pull/7265

Implementation/ testing:

https://github.com/DeFi-Circuit-Breaker/v1-core

We would love some feedback on this proposal!

## Replies

**frangio** (2023-07-06):

In `onTokenOutflow` it says:

> Before calling this method, the protected contract MUST transfer the EIP-20 tokens to the circuit breaker contract.

Have you considered instead having the protected contract approve the tokens and the circuit breaker  using `transferFrom`? This would be more efficient if there’s no rate limit because the circuit breaker can transfer directly from the protected contract to the recipient.

**Edit:** It turns out this doesn’t really improve net gas costs, and it relies on a larger refund which might be better to avoid, so I think two transfers is good.

---

**diyahir** (2023-07-10):

Thanks for validating this!

---

**Keinberger** (2023-09-10):

Excited to getting this PR merged. It will allow for increased modularization of the CircuitBreaker.

https://github.com/DeFi-Circuit-Breaker/EIPs/pull/3

---

**ernestognw** (2023-10-24):

Hey, I really like the EIP and the concept of limiters is very promising.

I got a question after taking a quick look. I noticed there’s an `AssetRegistered` event for the `registerAsset` function:

```auto
event AssetRegistered(address indexed asset, uint256 metricThreshold, uint256 minAmountToLimit);
```

However, there’s no counterparty for the `updateAssetParams`, which means that an indexer would be able to know the initial parameters of a registered asset but won’t be able to track further updates. Is this intentional or am I missing something?

