---
source: ethresearch
topic_id: 3214
title: Benchmark frameworks for security assessment tools
author: JisuPark
date: "2018-09-04"
category: Security
tags: []
url: https://ethresear.ch/t/benchmark-frameworks-for-security-assessment-tools/3214
views: 1329
likes: 2
posts_count: 1
---

# Benchmark frameworks for security assessment tools

Recently, I’ve researched **white-box testing tools** for solidity contract.

IMO, most of the recent papers have threats to the validity of their test sets.

Usually, they collect all different verified contract from Etherscan.

And that’s all.

We’d better prepare the rigid standard for comparing and testing the accuracy of the verifiers.

I’ve kickstarted a project called [VeriSmartBench](https://github.com/soohoio/VeriSmartBench) similar to [BigCloneBench](https://github.com/clonebench/BigCloneBench) and [ethereum-analyzer-suites-runner](https://github.com/EthereumAnalysisBenchmarks/ethereum-analyzer-suites-runner) for research purpose.

Currently, the project only contains smart contracts worth to analyze selected by certain conditions: **“>= 30 TX history”, “>= 1ETH deposits”**.

But the goal of the project is

1. Integrate with popular white-box tools.
2. Support real-world vulnerable codes like Juliet Test Suite.
3. Describe details of the vulnerability.

Is it seems to be meaningful? If then, which work should be the first?
