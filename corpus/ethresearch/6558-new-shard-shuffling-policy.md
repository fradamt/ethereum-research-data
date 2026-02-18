---
source: ethresearch
topic_id: 6558
title: New shard shuffling policy
author: ethorld
date: "2019-12-02"
category: Sharding
tags: []
url: https://ethresear.ch/t/new-shard-shuffling-policy/6558
views: 954
likes: 0
posts_count: 1
---

# New shard shuffling policy

Hello. I have a question in my think about shuffling policy. I would appreciate it if you tell me about any contradictions (can’t be justified) or supplement.

Suffling shard is high cost in node because node need to download every time when it’s shard id is changed. So I think about **new shuffling policy for maximizing social welfare**, even at the increased risk of forming cartel between nodes.

First, **protocol issues a credibility score every specific time period (e.g. 30 epoch) and each nodes can buy it using own deposit.** Score’s price is formed by auction. (Exchange rate between score and ETH will be described later).  **Nodes with higher scores get less probability to shuffle in next shuffle time.** (The actual probability calculation through the score is not sure. Please advice) Maybe this idea should be assumed that validator can deposit more than 32 ETH in one seat to buy more score. **There is no interest on deposits used to buy credibility score.**

I guess some side effect can be occured. For example, this makes probability richer to form cartel to get more 1/3 deposit within shard more higher. And If the validator has just joined the network or there is not enough ETH, the score is very low. Also, The interest on depositing the ETH used to buy the score may be greater than the gain from less shuffling.

To overcome this, when protocol detect someone misbehavior, give penalty him in proportion to the score to minimize probability to be formed cartel. The penelty means that malicious validator lose all of his score and ETH that is used to buy score (so, except for deposits that is not used to buy score). Penalty can be reward to reporter or burned.

Second, To bridge the gap of score between new and existing validators, and avoid having a high score that is dangerous to protocol stability, the maximum amount of scores validator can buy is limited in proportion to it’s total deposit (e.g. 50%). And last, to adjust the gain that results from less shuffling and the interest when depositing without using to buy score, the exchange rate between score and ETH can be changed at every auction).

I wonder if the above ideas are reasonable and do not ruin the economic system. Please advise.
