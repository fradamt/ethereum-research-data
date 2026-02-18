---
source: ethresearch
topic_id: 12450
title: Causal Relationships Between Blockchain Consensus Mechanisms and Decentralization
author: krabbypatty
date: "2022-04-19"
category: Economics
tags: []
url: https://ethresear.ch/t/causal-relationships-between-blockchain-consensus-mechanisms-and-decentralization/12450
views: 1478
likes: 0
posts_count: 2
---

# Causal Relationships Between Blockchain Consensus Mechanisms and Decentralization

Topic: Causal relationships between blockchain consensus mechanisms and network decentralization (OLS regression).

I am an undergraduate student in the research stage of my thesis defense on the topic above. I was hoping to get some clarification on whether my understanding and proposed modeling of my topic is correct. I am trying to figure out what consensus mechanisms have the biggest effect on decentralization, and what consensus protocols have achieved the greatest level of decentralization.

From what I understand the consensus protocol is more or less the parameters for how and who can participate in updating the blockchain. Although there are many different mechanisms, they can generally be broken down into 4 categories.

1. Block time
2. Block size
3. Block submission (Criteria for signing privilege eg: PoW, PoS, PoB)
4. Consensus algorithms (How blocks are verified/propagated throughout the network)

My first question is whether slasher/dagger/tendermint/snowball (avalanche) all fall within the consensus algorithm category. From what I understand this is the voting process to see whether a new block is accepted into the blockchain. Generally the algorithms can be classified as all-to-all or probabilistic and is how a proposed block is distributed across the network to all the nodes.

If all of the above is correct I was hoping for feedback on my OLS model.

yi = Beta0 + Beta1Block_time + Beta2Block_size + Beta3Block_submission + Beta4Consensus_algo + Beta5Blockchain_lifespan

block_submission and consensus_algo would be dummy variables, and blockchain_lifespan would be how long the blockchain has existed. I was also thinking of doing a time series regression to see which mechanisms achieve decentralization the fastest but the variables would more or less be the same.

My biggest problem is what I should use for my dependent variable. Although architectural decentralization is a) how many individuals are updating the global state and b) how equitable their participation is, I am not sure how to best combine these two criteria. I was thinking of what percentage of voting power the the top 10 validators have but this feels like a very bad solution. If anyone could offer any thoughts for this it would be extremely helpful.

I am looking for general feedback about what misunderstandings I have of consensus protocols, and whether my proposed model is acceptable. Additionally any resources that would help me gather information about the number of full nodes in major blockchains and their voting power/submission rate would be greatly appreciated!

## Replies

**gavinyue** (2022-04-20):

A survey paper for blockchain consensus: [[2001.07091] Blockchain Consensus Algorithms: A Survey](https://arxiv.org/abs/2001.07091), but I do not guarantee it is good ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=10)

For the decentralization, first, you could read [@vbuterin](/u/vbuterin) [blog](https://medium.com/@VitalikButerin/the-meaning-of-decentralization-a0c92b76a274)

Then, go back to the first principle to find answers to

1. why decentralization?
2. what kind of benefits we can get from it?
3. could these benefits be measurable?
4. If yes, how to build the metrics?

