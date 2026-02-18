---
source: ethresearch
topic_id: 6593
title: "PoLW: proof of less work to reduce energy consumption"
author: ChengWang
date: "2019-12-06"
category: Mining
tags: []
url: https://ethresear.ch/t/polw-proof-of-less-work-to-reduce-energy-consumption/6593
views: 3529
likes: 0
posts_count: 6
---

# PoLW: proof of less work to reduce energy consumption

Hello Everyone,

I propose an improved mining algorithm called PoLW to reduce the energy consumption of Nakamoto mining. One of the PoLW algorithms in the paper could reduce energy consumption by an arbitrary factor in equilibrium. (It’s inspired by the recent and great work from Itay, Alexander, and Ittay [https://arxiv.org/abs/1911.04124] and one of my previous work.)

The key idea is to shift part of the external costs of mining to internal costs inside the network. In PoLW, the miners are able to give up part of the coin rewards so as to get weight (> 1) for the mining work they have done. Let’s give more details below. For better description and analysis, please check out my little paper here [https://github.com/alephium/research/raw/master/polw.pdf].

Let’s say in a PoW system, the normal block reward is 1 coin and the work required is W. In Nakamoto mining, the miners mine a block with work > W and take the block reward. In PoLW, a miner could choose to get less reward, let’s say \alpha (0 < \alpha <= 1). By giving up a portion of the reward, the miner gets a weight 1+ f(1 - \alpha). If the work of a new block the miner generates is W’, then the weighted work of the block is (1 + f(1 - \alpha))W’. If this weighted block reaches the block mining target, the miner could claim \alpha coin as reward.

In my paper, I discussed two PoLW algorithms: linear PoLW with f(1- \alpha) = (1 - \alpha)/\gamma; and exponential PoLW with f(1 - \alpha) = e^{\gamma(1 - \alpha)} - 1. In equilibrium of linear PoLW, miners would choose \alpha as (1 + \alpha) / 2 to maximize the return, so the energy consumption could be reduced by a factor close to 1/2. While in equilibrium of exponential PoLW, miners would choose \alpha as 1/\gamma to maximize the return, so in theory the energy consumption could be reduced by a factor close to 0.

In practice, it takes a very long time to reach the equilibrium state and hash rate is dynamic always. The system could, however, update the system parameters (e.g. \gamma) according to the actual mining work done by the miners.

Note: the conclusion is not that we could reduce the energy cost of Bitcoin/Ethereum to zero. That’s gonna make the system attackable with existing mining powers level. The algorithms are gonna help the existing/new system based on PoW to reduce energy consumption gradually, especially for the future.

Looking forward to feedback and discussions.

## Replies

**spengrah** (2019-12-06):

How would the weight be applied? In nakamoto consensus the POW, block creation, and reward are all tied up together; the miner that gets to produce the block and thus gets the reward is the one that solves the POW task. I don’t see where you could add a weight to the W done to change how likely a given miner is to win the reward.

Maybe you could dynamically change the difficulty depending on the miner declared reward? I.e. a block is considered valid if (in addition to transaction validity, etc.) some function of difficulty *and* coinbase amount returns true.

---

**ChengWang** (2019-12-06):

Yes, you are right, the declared reward will be used for calculating \alpha, then \alpha will be used for the weight calculation.

The difficulty adjustment will be based on weighted hash work. The validation would based on weighted hash work to.

The actual difficulty as Nakamoto PoW is still useful too. We could use it to adjust other system parameters for example \gamma, so that the network is bounded in a good area of mixed external costs and internal costs.

---

**poemm** (2019-12-06):

Interesting. Nice work. Two concerns.

(1) Low \alpha may still require lots of work. This is because block time must be long enough, say at least 5 seconds on average, to allow miners to download and process each block, otherwise there can be DoS attacks.

(2) Low \alpha rewards may still need to be significant. This is because a miner has incentive to get any reward, even if it is small. And if small \alpha rewards are not significant, then there is less incentive for miners to protect the network.

So in practice, this may reduce to the current system. With bonuses if you get lucky and mine smaller hashes.

Maybe I am wrong. It is difficult to discuss crypto-economic systems without hand-waving.

---

**ChengWang** (2019-12-06):

You concerns are about how we tune parameters in real system. We could find proper rules to keep \alpha in proper range, definitely not letting miner try random value between [0, 1].

One approach is that we could infer a proper lower bound for \alpha based on current actual mining work (hashrate) done by miners. In this way, we set a lower bound for the external mining costs, so that the block time could not be too short.

I would expect \alpha to become lower very slowly. When the actual hashrate is low, \alpha will still be high. Only when the actual hashrate is high and energy waste is a concern, the weights will become a thing. Just for example, the \alpha and the weight could be related to the log of hashrate.

Very good points! Happy to discuss always ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**ChengWang** (2019-12-06):

The actual external costs (hash rate) would still grow, but not catch up the growth of rewards value any more. Just for example, if we shift 0.25 or half of the external costs to internal costs, it’s already something useful, the hashrate will only decrease by 0.25 or half accordingly.

Projects could very aggressive or moderate on how much shift they would like to see in long term and set the rules for \alpha properly.

