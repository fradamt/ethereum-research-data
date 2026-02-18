---
source: ethresearch
topic_id: 4493
title: A Stochastic Model for Proof of Work Block Production
author: ChosunOne
date: "2018-12-06"
category: Mining
tags: []
url: https://ethresear.ch/t/a-stochastic-model-for-proof-of-work-block-production/4493
views: 1284
likes: 2
posts_count: 1
---

# A Stochastic Model for Proof of Work Block Production

Hello Ethresearch community!  I’ve worked on this paper to describe how to control the distribution of block times from PoW blockchain systems.  While I’m aware that this study is not necessarily applicable to Serenity, I do believe that it introduces an approach to thinking about PoW in a way that has been rarely discussed.  This paper is the first of three dealing with other topics, and we felt the need to create this paper as it is the paper we wish we could have cited but could not find.

Here is the abstract from the paper:

> In Proof of Work blockchain systems, block production time can be
> modeled as an exponential distribution, which provides a natural method
> for adjusting to changes in network hash power via a cumulative distribu-
> tion function. The cumulative distribution function can be adjusted by
> modeling network hash power via two exponential moving averages, one
> for block production time and the other for block work, and by choos-
> ing a desired quantile for a target time to produce a block. The bias in
> the exponential moving averages toward present information can be tuned
> such that the variance in the moving averages is tolerable. Improvements
> to the model include accounting for latency in effective hash power and
> block propagation.

You can view the rest of the paper on [GitHub](https://github.com/Team-Hycon/research/blob/f4cb4c3d3750d1c519cf571be5720590446f320b/A%20Stochastic%20Model%20for%20Proof%20of%20Work%20Block%20Production/stochastic_model.pdf)

I would greatly appreciate any feedback on the topics in the paper, including any ambiguities, disagreements, or improvements.  If you like the ideas presented and can publish to [arxiv.org](http://arxiv.org), then I would greatly appreciate it if you were willing to endorse us so that it may be published on arXiv.  If so, please message me directly and I will supply an endorsement link.
