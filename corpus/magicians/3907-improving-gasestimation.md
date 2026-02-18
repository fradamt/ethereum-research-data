---
source: magicians
topic_id: 3907
title: Improving GasEstimation
author: ligi
date: "2020-01-08"
category: Web > Wallets
tags: [wallet, gas]
url: https://ethereum-magicians.org/t/improving-gasestimation/3907
views: 1231
likes: 5
posts_count: 2
---

# Improving GasEstimation

Currently estimateGas has a practical problem. It can happen that you estimate gas for a transaction and then sign a transaction with this limit and this transaction fails with out of gas. E.g. caused by other transactions to the same contract in the meantime.

MetaMask mitigates this by multiplying 1.5 to the estimated gas (and limiting to 0.9xBlockGas limit)

These are kind of ugly magic constants and the system does not feel nice.

This thread is to collect ideas on how to improve on the situation. One idea could be that this multiplier can be influenced with NatSpec (cc [@chriseth](/u/chriseth)) as the author of the smart-contract function might have a better magic number than 1.5. Ideally we get away from magic numbers after all - but I am currently having no good idea on how to do so.

Would also be happy about the experiences/magic numbers of other wallets here.

## Replies

**mcdee** (2020-01-08):

If you’re after a “safe high” gas limit then perhaps having a different call that carried out accounting a little differently would be interesting.  Charging 20K for each SSTORE rather than the sometimes-5K-sometimes-20K would be an obvious tweak.

This wouldn’t catch everything, of course, but could help with one situation where gas estimation fails.

