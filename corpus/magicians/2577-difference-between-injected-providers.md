---
source: magicians
topic_id: 2577
title: Difference between injected providers
author: filips123
date: "2019-02-03"
category: Working Groups > Provider Ring
tags: []
url: https://ethereum-magicians.org/t/difference-between-injected-providers/2577
views: 1272
likes: 1
posts_count: 2
---

# Difference between injected providers

There are many ways to detect injected provider (MetaMask, Mist, …). Some of them are `Web3.givenProvider`, `web3.currentProvider` and `window.ethereum`.

What is the difference between them? I know that `window.ethereum` uses EIP-1102, but what is the difference between the other two? Which one should I use?

I first asked this [on Web3’s GitHub](https://github.com/ethereum/web3.js/issues/2298), but @nivida suggested to ask this here.

## Replies

**danfinlay** (2019-02-04):

The original provider is `window.web3.currentProvider`, but this came with the baggage of the `web3.js` framework. To reduce the amount of code injected in every page, every provider that is 1102 compatible should inject the same provider at `window.ethereum`.

You can fall back to the `web3` one if you need to.

Sample code is available on [the metamask docs site](https://metamask.github.io/metamask-docs/API_Reference/Ethereum_Provider).

