---
source: magicians
topic_id: 25945
title: "EIP-8059: Gas Rebase for High-precision Gas Metering"
author: misilva73
date: "2025-10-24"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8059-gas-rebase-for-high-precision-gas-metering/25945
views: 53
likes: 1
posts_count: 1
---

# EIP-8059: Gas Rebase for High-precision Gas Metering

Discussion topic for EIP-8059; [PR](https://github.com/ethereum/EIPs/pull/10583)

#### Abstract

This proposal rebases Ethereum’s gas unit by a factor of 1,000 to enable high-precision metering without introducing fractional gas. All gas-related parameters and variables are increased by a factor of 1,000. This reduces rounding errors that arise when repricing EVM operations and future-proofs gas costs as hardware improves and state access remains costly, while avoiding major changes in the internal logic of the EVM.
