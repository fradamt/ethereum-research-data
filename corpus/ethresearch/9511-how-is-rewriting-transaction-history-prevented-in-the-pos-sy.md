---
source: ethresearch
topic_id: 9511
title: How is rewriting transaction history prevented in the POS system?
author: zes
date: "2021-05-15"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/how-is-rewriting-transaction-history-prevented-in-the-pos-system/9511
views: 1342
likes: 1
posts_count: 1
---

# How is rewriting transaction history prevented in the POS system?

Not sure how similar this is to the ETH implementation, but for example,

The #100 RANDAO + VDF round generates a random number that selects validator X1, X2 etc to make block #1234, #1235 etc, X1 signs the #1234 block including transactions A, B, and C.

However, during the #100 RANDAO + VDF round, one of the people contributing to the randomness pretends to be offline during the round but make up a number after learning the others’ VDF results to make a fake round pointing to his/her addresses to make #1234, #1235 etc blocks. He/she makes the blocks but only includes transactions D, E and F in it without transactions A, B and C and then continues to build on and send out this chain and the fake RANDAO + VDF data.
