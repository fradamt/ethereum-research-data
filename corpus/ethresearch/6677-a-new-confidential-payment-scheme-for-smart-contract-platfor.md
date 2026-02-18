---
source: ethresearch
topic_id: 6677
title: A new confidential payment scheme for smart contract platforms
author: trakl
date: "2019-12-25"
category: Privacy
tags: []
url: https://ethresear.ch/t/a-new-confidential-payment-scheme-for-smart-contract-platforms/6677
views: 2078
likes: 2
posts_count: 3
---

# A new confidential payment scheme for smart contract platforms

[![image](https://ethresear.ch/uploads/default/optimized/2X/8/8eb527d803bdec6af83537427022c17a608af692_2_386x500.png)image2000×2588 516 KB](https://ethresear.ch/uploads/default/8eb527d803bdec6af83537427022c17a608af692)

You can find the full version here: [https://github.com/suterusu-team/Suter_yellowpaper/blob/2b2eecf95dceffdf61298b79112979d86cc7360d/Suterusu%20yellowpaper%20V%200.1.pdf](https://github.com/suterusu-team/Suter_yellowpaper/blob/master/Suterusu%20yellowpaper%20V%200.1.pdf)

## Replies

**Mikerah** (2019-12-25):

This is really cool.

The main issue I see with this scheme if it were to be implemented on top of Ethereum is that class group operations might be quite expensive. Potentially as expensive as Zether currently is.

Are there any gas cost estimates that you can provide?

Anothet question I have is are you building a DSL to make it easier to write such privacy-preserving smart contracts or do you expect developers to write Rust?

---

**trakl** (2019-12-26):

Thanks for your comments. Here is my answer to your two questions:

1. As mentioned at the end of this yellowpaper, we are working on the simulation of the scheme and compare it with other similar schemes, and will choose the optimal scheme for our final implementation.
2. We focus on Rust at the moment.

