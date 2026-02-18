---
source: magicians
topic_id: 25260
title: "EIP-8011: Multidimensional Gas Metering"
author: misilva73
date: "2025-08-27"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-8011-multidimensional-gas-metering/25260
views: 105
likes: 4
posts_count: 2
---

# EIP-8011: Multidimensional Gas Metering

Discussion topic for [EIP-8011](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-8011.md); [Web](https://eips.ethereum.org/EIPS/eip-8011)

#### Abstract

This proposal introduces multidimensional gas metering, changing the way we account for gas used at the block level. This enables Ethereum to increase throughput and better control excessive resource usage, with minimal changes to the protocol and the UX. During transaction execution, gas is metered for each resource dimension, such as compute and state. At the transaction level, everything remains unchanged. A transaction still pays fees according to the sum of gas used across all resources and still has a single gas limit imposed on this same sum. However, at the block level, only the gas used in the bottleneck resource is considered when checking if the block is full and when updating the base fee for the next block.

#### Update Log

- 2025-08-22: initial draft, PR

#### Relevant resources

- 2025-06-17: “Going multidimensional - an empirical analysis on gas metering in the EVM”, by Maria Silva,  post
- 2025-06-25: “A practical proposal for Multidimensional Gas Metering”, by Maria Silva and Davide Crapis,  post

## Replies

**wjmelements** (2025-09-24):

I have reviewed the opcode category lists. Looks correct to me.

