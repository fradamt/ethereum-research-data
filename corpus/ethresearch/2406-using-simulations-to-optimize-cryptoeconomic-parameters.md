---
source: ethresearch
topic_id: 2406
title: Using Simulations To Optimize Cryptoeconomic Parameters
author: timbeiko
date: "2018-07-02"
category: Economics
tags: []
url: https://ethresear.ch/t/using-simulations-to-optimize-cryptoeconomic-parameters/2406
views: 3710
likes: 25
posts_count: 13
---

# Using Simulations To Optimize Cryptoeconomic Parameters

## TL;DR

I believe you could use simulations, possibly with reinforcement learning, to determine what cryptoeconomic parameters to use in new token projects, or in changes to existing networks. I am wondering whether others have thought about this, and looking to start a discussion around better methodology to determine cryptoeconomic parameters for blockchain projects.

# Background

Cryptoeconomic parameters, a.k.a. hyperparameters (in the AI world), are important for blockchain projects because they have a significant impact on the future distribution of tokens. Yet, today most projects seem to choose these arbitrarily. For example, an ICOing project may decide to keep 10, 20, 50, or even 90% of its tokens, contribute some of the rest to a “development fund”, have a founders’ reward of X%, etc. Similarly, Ethereum is currently considering reducing the block reward from 3ETH to 0.8ETH when Casper FFG goes live. In most projects, there is likely an “ideal” long-term distribution of tokens that the founding team or community would want to optimize for (ex: most tokens in the hands of users/devs vs. speculators or miners), but few projects seems to have made rigorous attempts at quantifying this, as well as the impact of potential changes on this distribution.

This post describes a high-level idea for how this could be done using reinforcement learning, and is meant to initiate a discussion around developing better methodology for hyperparameter optimization in cryptoasset & blockchain projects.

# Cryptoeconomics as a RL Problem

Reinforcement learning (RL) is a sub-field of artificial intelligence, where instead of using training and testing data to teach and evaluate the model, we define agents, which can take a variety of actions over time in a specified environment. Each action produces a reward (or penalty), specific to the agent, which is quantified using a reward function. The agents must optimize their reward function over time, and will thus learn the “best” actions to take to maximise its long term reward in the environment.

This framework seems relevant to several cryptoasset and blockchain projects, as many of them have a finite set of agents (ex: users, developers, miners, speculators, hackers, etc.), which can take a finite set of actions when interacting with the project, and receive a reward (in the form of tokens or value from the project) for their actions.

## Why RL?

What I believe makes cryptoassets particularily well-suited to reinforcement learning is that building a model of the environment may be simpler than in several other reinforcement learning use cases. All interactions with a blockchain happen online, and while some offline actions may be incorporated into models (ex: collusion amongst validators in a dPOS system),  these seem to be the exeception and not the rule.

Also, reinforcement learning has proven very successful in finding bugs in its operating environments ([[1]](https://arxiv.org/pdf/1803.03453v1.pdf)). Most blockchain designs are fairly simple, at least compared to other types of environments such as video games or “the real world”. This suggests that RL would likely be effective at finding issues with blockchain system designs.

Lastly, one of the challenges of reinforcement learning is defining clear reward functions. Fortunately, most blockchain projects have a token associated with them, which carries some value. Therefore, for several agents, the reward function could be based on accumulating tokens, with some caveats.

**EDIT:** [@cpfiffer](/u/cpfiffer) pointed out in the comments that:

> Another point towards RL is that we care about the equilibrium of the state (at time T) as much as we do about all the intervening steps (times t0, t1, … T) You can make a pretty strong argument that the intervening steps may describe the evolution of the system.

## How

The specifics of the implementation are beyond the scope of this post, but at a high level, we can imagine building RL simulations using the following workflow:

1. Define the set of hyperparameters to optimize, the agents involved in the network, and the potential actions of each agent in the network;
2. Define reward functions for each agents taking into account all their potential interactions with the network;
3. Define an operating environment for agents that models the network;
4. Add agents to an instance of the environment with specific hyperparameters (ex: number of tokens, txn cost, mining reward, etc), have them maximise their reward function over a period of N units of time, and output the final state of the network, i.e. how many tokens does each agent have, and perhaps the amount of value they’ve contributed or received from the network;
5. Re-run (4) with a different set of hyperparameters for however many values of hyperparameters should be tested;
6. Perform an analysis on the results and select hyperparameters that lead to “best” final state of the network.

## Issues & Caveats

Although RL could be a promising approach to determining the best hyperparameters for a network, it is far from perfect. Here are some issues associated with this approach:

1. High computational cost of simulations
2. High “barrier to entry” to build models (in other words, you need to grok both RL/AI and “the blockchain”)
3. Challenges around defining environments and reward functions that mimic real-life behaviour
4. RL is non-deterministic, so two runs of the same simulation may produce different results.

For a sobering read on the current state of RL, see [Deep Reinforcement Learning Doesn't Work Yet](https://www.alexirpan.com/2018/02/14/rl-hard.html)

# Conclusion

Reinforcement learning could potentially be used to better determine hyperparameters for blockchain networks. I have outlined a high-level approach around how this could be done, as well as some of its potential pitfalls. It is important to state that reinforcement learning is simply a tool to help us acheive the goal of having optimal hyperparameters for these projects. Other approaches may be more promising, and the result of RL models should be treated as one of many inputs into the decision of which hyperparameters to use.

## Replies

**cpfiffer** (2018-07-03):

Sounds interesting! I do have some refining questions and comments that might be useful going forward.

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> Reinforcement learning (RL) is a sub-field of artificial intelligence, where instead of training a model with labelled data and then testing its capacities on unseen data, we define agents, which can take a variety of actions in a specified environment.

This description of RL is not entirely accurate – we don’t typically have labelled data. It’s not even clear in this case what labelled data would be. That’s the domain of supervised learning. Not terribly important, but it’s a useful distinction to make.

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> This framework seems relevant to several cryptoasset and blockchain projects, as many of them have a finite set of agents (ex: users, developers, miners, speculators, hackers, etc.), which can take a finite set of actions when interacting with the project, and receive a reward (in the form of tokens or value from the project) for their actions.

This is certainly true. However, the better question here is whether or not RL (or any other ML/AI tool) is the right tool for the job. These kinds of models that you are pointing to here have a pretty strong tradition in economics and finance, and they tend towards treating them as pure optimization problems rather than a dynamic agent-type model, which is what I would stick this RL method under.

As you highlighted, this type of computation is *enormously* costly, even under the classical optimization approach. Is this an on-chain thing? A toolkit for people doing ICOs? A research paper? Who is using this and where?

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> Lastly, one of the challenges of reinforcement learning is defining clear reward functions.

When I saw the post title this was my immediate first thought. A couple things on this.

1. I would be a little skeptical of a model that used token accumulation as a reward function. Ultimately, what do you want to see as a result of this hyperparameter tuning? It’s still a bit unclear. Do you want to maximize wealth distribution? Efficient functioning? Chances are good that you don’t want to see how best to accumulate tokens – that has little to do with ICO parameters.
2. Agents can also take actions. What might be the scope of the actions an agent can take? Can they only transact? Who can they transact with outside the network, if so? Can they execute contracts? This opens up a whole nightmare of complexity.

I personally like the idea, but I tend to like ML tools a lot and I sometimes need a reality check as to whether it’s useful or realistic to use them. I’m still a little unlear on the *why* of the whole thing. Could you elaborate a bit more on the end product? How does doing this help people?

---

**timbeiko** (2018-07-03):

Thanks for the reply, [@cpfiffer](/u/cpfiffer)!

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> This description of RL is not entirely accurate – we don’t typically have labelled data. It’s not even clear in this case what labelled data would be. That’s the domain of supervised learning. Not terribly important, but it’s a useful distinction to make.
>
>
>  timbeiko:

Fair point. Will edit to simply specify training and testing data.

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> This is certainly true. However, the better question here is whether or not RL (or any other ML/AI tool) is the right tool for the job. These kinds of models that you are pointing to here have a pretty strong tradition in economics and finance, and they tend towards treating them as pure optimization problems rather than a dynamic agent-type model, which is what I would stick this RL method under.

Great point! I’m not particularly attached to RL. Are there any specific models you think would be better suited? The reasons why I though RL made sense were that (1) the environment could be modelled fairly early, (2) reward functions may not be *that* hard to define, and (3) it would potentially expose bugs in either a network’s structure or our simulation environment.

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> As you highlighted, this type of computation is enormously costly, even under the classical optimization approach. Is this an on-chain thing? A toolkit for people doing ICOs? A research paper? Who is using this and where?

This would not be on-chain, no.

The goal would be for people to use this before proposing changes to a network (or launching a new one) as an analysis tool that could highlight potential issues. For example,: What is the difference between having 0% vs 2% vs 10% token inflation each year? What is the difference between giving miners/validators a block reward of X vs Y? Will users end up holding tokens if they receive more/less value from the network than the price appreciation/depreciation of the token?

Before we get there, there would probably have to be a fair amount of upfront research around  determining what parts of these systems are best suited to model, and what promising architectures may look like.

There may also be “unknowns unknowns” uncovered by using “selfish” RL agents to maximise their interests in a decentralized network.

Perhaps a good analogy is something like [TensorFlow Playground](http://playground.tensorflow.org/#activation=tanh&batchSize=10&dataset=circle&regDataset=reg-plane&learningRate=0.03&regularizationRate=0&noise=0&networkShape=4,2&seed=0.14576&showTestData=false&discretize=false&percTrainData=50&x=true&y=true&xTimesY=false&xSquared=false&ySquared=false&cosX=false&sinX=false&cosY=false&sinY=false&collectStats=false&problem=classification&initZero=false&hideText=false) for certain cryptoeconomic parameters.

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> Ultimately, what do you want to see as a result of this hyperparameter tuning? It’s still a bit unclear. Do you want to maximize wealth distribution? Efficient functioning?

I think this would vary between projects and use cases. In the pre-ICO stage, you’d potentially want to optimize for a set of different constraints (ex: wealth distribution, speculative vs. consumptive use case, miner concentration, etc.). For live networks, you can imagine building a simulation testing various changes to a specific parameter (which you’d likely introduce in a fork) to get a feel for what different values result in. These could be block reward, block size, block time, etc.

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> Agents can also take actions . What might be the scope of the actions an agent can take? Can they only transact? Who can they transact with outside the network, if so? Can they execute contracts? This opens up a whole nightmare of complexity.

They certainly can! I think the actions would vary by agent type. For example, a user of the network may have the actions `use`, `buy token`, `sell token`, etc. while a miner may have `mine`, and `sell token`. There clearly is a tradeoff between how much you want to limit the actions of the agents (and have a simpler model) vs. building a model that truly represents the “real world”.

![](https://ethresear.ch/user_avatar/ethresear.ch/cpfiffer/48/1504_2.png) cpfiffer:

> I’m still a little unlear on the why of the whole thing. Could you elaborate a bit more on the end product? How does doing this help people?

I think the “why” is to develop better methodologies around setting these parameters in network, because their impact is large and that today a lot of it is done quite arbitrarily. ML/RL may not be the best tool for this, but in general having models that can give us a feeling for which settings may be better than others seems valuable.

Re: “the product”, I think at first there would need to be a lot of upfront research to build reliable models, but that once you have them, it may be possible to open them to the community so that more people can try things with these models.

Hopefully this clears a few things up! Again, thank you for the response.

---

**cpfiffer** (2018-07-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/timbeiko/48/1585_2.png) timbeiko:

> I’m not particularly attached to RL. Are there any specific models you think would be better suited? The reasons why I though RL made sense were that (1) the environment could be modelled fairly early, (2) reward functions may not be that hard to define, and (3) it would potentially expose bugs in either a network’s structure or our simulation environment.

Another option I would see as a contender in this space is a strictly deterministic system, where you have some agent who falls into one or more agent categories (miner, user, etc. as you mentioned). Each category provides some form of decision threshold for certain actions; the miner would decide to mine when some utility function of the expected value of mining was positive. This could have a stochastic aspect where different miners have different ways of valuing expected returns, which allows some miners to be more conservative and others more enthusiastic.

The issue with this is it requires the definition of all those decision thresholds. The allure of using RL in this case is that we just define an action space and some penalty/reward function and they figure all that stuff on their own.

Another point towards RL is that we care about the equilibrium of the state (at time T) as much as we do about all the intervening steps (times t_0,t_1...T). You can make a pretty strong argument that the intervening steps may describe the evolution of the system.

So I suppose that my answer is no, I think RL may be a good way to model this system, if not a fun way to do so.

---

**timbeiko** (2018-07-04):

Good point! I included it in the original post.

---

**piotrgrudzien** (2018-08-01):

I just saw this post and that’s what [Incentivai](http://incentivai.co/) are working on. Some case studies have been published already (example: [Bonding curve simulation](https://medium.com/incentivai/bonding-curve-simulation-using-incentivai-2b2bfe0c6400)). Curious to hear your thoughts!

---

**cpfiffer** (2018-08-01):

In the [bonding curve simulation](https://medium.com/incentivai/bonding-curve-simulation-using-incentivai-2b2bfe0c6400), I noticed that most of the key findings are regarding price. I wonder if perhaps it’s wise to simply not consider price except as a mechanism by which tokens are exchanged. Price is a byproduct of a system and not a variable input.

If I’m setting up my token, I am really more concerned with how robust the system is at any and all price levels. I want to know which things I can change to make the system better.

To be fair, there’s [another case study](https://medium.com/incentivai/incentivai-analysis-of-the-nexus-mutual-smart-contract-system-a9f8a1ac7c47) that is concerned a lot more with the stuff brought up in this thread – this is more the type of thing I’d like to see.

---

**PhABC** (2018-08-01):

I think here the most difficult part is to have meaningful models reflecting reality, which is in general much more difficult than optimizing a model to minimize a given objective function.

Games are great for RL because you can perfectly simulate the rules and laws governing the game, so the AI can find the right model, but this is not true at all for real world scenarios.

So my intuition is that before even using RL, you need to have a good simulation, otherwise RL will not give you the right stuff. Not saying this is worst than the current standard in choosing your project’s hyper parameters, but it’s definitely hard.

Would be happy to follow your work if you try some stuff out!

---

**piotrgrudzien** (2018-08-01):

Absolutely, models reflecting reality is a crucial aspect. Another key insight is that, well, machine learning (or RL in particular) is not yet a one-size-fits-all problem solver but rather a suite of techniques that are better at some tasks than other.

The way I like to think about it is that there will often be a trade-off between closely modelling the reality and making the problem approachable for ML algorithms. That’s one of the big learnings from my work on the subject so far.

Please feel free to [follow](https://twitter.com/incentivai) Incentivai and have a look at the [blog](https://medium.com/incentivai) where various case studies have already been published and more is to come. Thanks!

---

**beneficial02** (2018-08-02):

Though it is not using RL, check my [partial slashing simulation](https://github.com/beneficial02/partial_slashing_simulation) using agent-based modeling methodology if you are interested. My very first idea was simulating the security model of PoS with ABM+RL, but I gave up building the environment and I decided to simulate a much simpler problem so that’s what I did.

I think [this paper from DeepMind](https://arxiv.org/abs/1707.06600) gives some hints for using RL in cryptoeconomics.

---

**mratsim** (2018-08-02):

I think we can frame the state of a crypto as a [Multi-Armed Bandit](https://en.wikipedia.org/wiki/Multi-armed_bandit) problem with almost perfect information and multiple players/agents. I say almost perfect because the hashing power of miners is not known. Also I’m not sure we can say it’s zero-sum though.

The most famous multi-armed bandit problem that was “solved” by RL being the game of go with application on Google datacenters energy consumption (saving hundreds of millions per year).

The first things I would try would be:

- Monte-Carlo Tree Search ==> randomly try hyperparameters, choose if we want to continue to explore this value of hyperparameter otherwise try another one, then simulate up to an end state and score it. Benefits: since the past 10 years, robots/agents competitions have in a large majority been won by Monte Carlo Tree Search. It can also be applied to cooperative problems to simulate collusion.
- Genetic algorithms:

Generation 1, completely random hyperparameters. Those not adapted “die”. You crossoverthe others to pass main characteristics, add some mutations (might be beneficial or harmful).
- Generation 2, more natural selection and crossover and mutations.
- repeat ad infinitum
- check the end state and the surviving characteristics.

For those interested, the second edition of the best introductory Reinforcement Learning book is being written since a year ago in an open way. You can [download the current version here.](http://incompleteideas.net/book/the-book-2nd.html)

You might particularly interested in [adversarial bandit](https://en.wikipedia.org/wiki/Multi-armed_bandit#Adversarial_bandit) and the [iterated prisoner dilemma.](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma#The_iterated_prisoner's_dilemma) as Monte Carlo Tree Search can be used there to simulate collusion vs adversarial response.

---

**DennisPeterson** (2018-08-02):

A technique being used to solve some game theory problems is counterfactual regret minimization. Basically, after each action and its outcome, see how much better you would have done with other possible actions. This is your regret for not taking that action. Each action accumulates regret over time, and you choose actions in proportion to their accumulated regrets.

In a two-player zero-sum game, the overall average strategy converges on a Nash equilibrium. The University of Alberta has used this to build champion-level poker players. (I don’t know whether it can be used for multiplayer games.)

Here’s a longer description and introductory paper:

https://www.quora.com/What-is-an-intuitive-explanation-of-counterfactual-regret-minimization

http://modelai.gettysburg.edu/2013/cfr/cfr.pdf

There are more papers on CFR in the UofA poker group publications list, along with some other papers that look like they might be useful:

http://poker.cs.ualberta.ca/publications.html

---

**timbeiko** (2018-08-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/piotrgrudzien/48/1860_2.png) piotrgrudzien:

> I just saw this post and that’s what Incentivai  are working on. Some case studies have been published already (example: Bonding curve simulation ). Curious to hear your thoughts!

This is exactly what I had in mind! Will definitely be following your progress.

