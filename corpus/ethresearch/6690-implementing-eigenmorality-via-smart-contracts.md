---
source: ethresearch
topic_id: 6690
title: Implementing Eigenmorality via Smart Contracts
author: fractastical
date: "2019-12-26"
category: Economics
tags: []
url: https://ethresear.ch/t/implementing-eigenmorality-via-smart-contracts/6690
views: 1145
likes: 0
posts_count: 2
---

# Implementing Eigenmorality via Smart Contracts

Enjoyed Vitalik’s update to Hard Problems and started thinking about reputational systems again, esp. a smart contract driven implementation of [Eigenmorality](http://www.scottaaronson.com/morality.pdf)

> The idea was to use the link structure of the web itself to rank which web pages were most important, and therefore which ones should be returned first in a search query.  Specifically, Kleinberg defined “hubs” as pages that linked to lots of “authorities,” and “authorities” as pages that were linked to by lots of “hubs.”  At first glance, this definition seems hopelessly circular, but Kleinberg observed that one can break the circularity by just treating the World Wide Web as a giant directed graph, and doing some linear algebra on its adjacency matrix.  Equivalently, you can imagine an iterative process where each web page starts out with the same hub/authority “starting credits,” but then in each round, the pages distribute their credits among their neighbors, so that the most popular pages get more credits, which they can then, in turn, distribute to their neighbors by linking to them.

I’m curious if anyone is familiar with this concept and thinks it could be implemented on an EVM blockchain. I assume it would need at least 10x the transaction throughput of even a PoS system but perhaps there is some way to mitigate this.

## Replies

**liamzebedee** (2019-12-27):

I previously had a go - implementing something like PageRank is possible on EVM, I wonder though how you can better distribute the cost so everyone can use the output? ie. map-reduce. An eigenvector reputation metric would be very useful, if not for the fact that matrix optimisation is  O(N^2) .

