---
source: ethresearch
topic_id: 15064
title: Solution to scalability trilemma using a hierarchy of *independent* chains of different speeds
author: sim31
date: "2023-03-15"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/solution-to-scalability-trilemma-using-a-hierarchy-of-independent-chains-of-different-speeds/15064
views: 785
likes: 0
posts_count: 1
---

# Solution to scalability trilemma using a hierarchy of *independent* chains of different speeds

So there’s an idea that I’ve been developing that is relevant for DAOs, naming systems, soulbound tokens and overall security of blockchain applications. Proof of concept also relies heavily on EVM, and I’m interested to hear what Ethereum research community thinks of this.

I will just paste an intro here, link to the rest of the post comes after the intro.

## Intro

Scalability trilemma is a well-known problem in the blockchain space. It states that there’s always a trade-off between blockchain security, decentralization, and scalability. Specifically, it claims that you can choose only two of those but never all three. Or rather any improvement in any of the three will require a trade-off in one of the other two.

The point of this post is to try to convince you that we do not need one blockchain that achieves all of these properties together. What we need is:

1. Slow chain: blockchain that is maximally secure and decentralized;
2. Fast chain: separate blockchain that is fast and scalable;
3. Fast chain to be a fully validating client of the slow chain;

Now, you’re probably thinking that the 3rd one is impossible. That seems to be what the whole blockchain space thinks. But, in reality, if the 3rd is impossible it just means that the slow chain component is not slow (secure) enough. Yes, I really mean it when I call it the *slow chain*. I mean *weekly* blocks of size up to 1 MB. You read that right - blockchain where you would have 1 week of time in between blocks.

Why would we need such a slow blockchain? Let me explain.

…

Read the rest here: [Fractal Blockchains | PeakD](https://peakd.com/fractally/@sim31/fractal-blockchains)

---

I’m already implementing this as a solidity smart contract which represents a validator of these kinds of “slow chains”, and could be run in a browser as well as EVM-enabled blockchains: [GitHub - sim31/firmcontracts](https://github.com/sim31/firmcontracts)

What do you think?
