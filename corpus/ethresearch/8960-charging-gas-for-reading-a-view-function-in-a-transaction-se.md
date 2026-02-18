---
source: ethresearch
topic_id: 8960
title: Charging Gas for reading a view function in a transaction seems odd
author: aak-dev
date: "2021-03-19"
category: Architecture
tags: []
url: https://ethresear.ch/t/charging-gas-for-reading-a-view-function-in-a-transaction-seems-odd/8960
views: 1068
likes: 0
posts_count: 1
---

# Charging Gas for reading a view function in a transaction seems odd

I just cant get my head around why view functions which are gas free suddenly cost 5k gwei when sandwiched between a state transitioning function which just uses the view function like a web3 call.
