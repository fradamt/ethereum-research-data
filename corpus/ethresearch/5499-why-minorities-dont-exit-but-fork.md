---
source: ethresearch
topic_id: 5499
title: Why minorities don't exit but fork?
author: jsrimr
date: "2019-05-23"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/why-minorities-dont-exit-but-fork/5499
views: 1128
likes: 0
posts_count: 2
---

# Why minorities don't exit but fork?

hello, i have a question about

why minority incentive mechanism assumes censored minorities would vote on minor chain rather than withdraw their money?

Is the request of withdrawl would be censored too? I thought request of withdrawl was out of voting, but maybe withdrawl request is just one of a transaction which can be censored too… I’m confused.

## Replies

**vbuterin** (2019-05-26):

A withdrawal requires the chain to finalize to take effect, so if <2/3 are on each chain the withdrawals can’t happen. And even if there is a supermajority on the main chain, (i) they could censor withdrawals and (ii) even if they don’t there’s a rate limit to how fast withdrawals can happen.

