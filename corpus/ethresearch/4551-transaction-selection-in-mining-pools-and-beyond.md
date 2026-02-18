---
source: ethresearch
topic_id: 4551
title: Transaction selection in mining pools and beyond
author: drstone
date: "2018-12-11"
category: Mining
tags: []
url: https://ethresear.ch/t/transaction-selection-in-mining-pools-and-beyond/4551
views: 1562
likes: 0
posts_count: 1
---

# Transaction selection in mining pools and beyond

I’ve been working on understanding the effects of congestion/validation externalities imposed on miners and validators in the Ethereum network. I was exploring the efficacy of dynamic pricing of opcodes to optimize a social welfare metric with respect to these externalities but have been stumped by the following question.

1. What strategies do miners choose when selecting transactions? They don’t seem to simply take the highest fee transactions (is this even the default?).
2. Does anyone know if miners factor in the cost of validation of certain transactions?
3. Are there complex models being deployed in pools for this matter, to decide how much a block should be filled before sending out work to pool miners?

In looking at etherscan, there is weird behavior exhibited by miners that I am not understanding. Why is the variance in Gwei pricing so high and why are blocks left unfilled when profit should not be left on the table. Is this a reaction to fear that one’s block will not be broadcast in time throughout the network or are there side payments or private transactions involved that only miners have within their mempool/cache.

I’m looking to also talk to miners and people with more insight into these ideas, purely for research purposes to understand behavioral strategies of large miners and pool operators.
