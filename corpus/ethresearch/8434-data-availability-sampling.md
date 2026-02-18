---
source: ethresearch
topic_id: 8434
title: Data Availability Sampling
author: kladkogex
date: "2020-12-29"
category: Sharding
tags: []
url: https://ethresear.ch/t/data-availability-sampling/8434
views: 1530
likes: 0
posts_count: 1
---

# Data Availability Sampling

https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/sharding_proposal

Interesting proposal.  By the way, the Honey Badger protocol uses erasure coding for block proposals.  We at SKALE also considered using erasure coding for block proposal, but decided it was a bit hard to debug.

A question about data availability - how is it defined in terms of time? If some piece of data is proven to be available now,  what prevents the attacker from making it unavailable later?

In other words, can one provide an exact definition of what data availability means for ETH2?
