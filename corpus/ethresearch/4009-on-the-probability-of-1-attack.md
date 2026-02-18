---
source: ethresearch
topic_id: 4009
title: On the probability of 1% attack
author: daniel-tung
date: "2018-10-30"
category: Sharding
tags: [proposal-commitment]
url: https://ethresear.ch/t/on-the-probability-of-1-attack/4009
views: 4154
likes: 6
posts_count: 13
---

# On the probability of 1% attack

Has anyone calculated this:

Assuming that 10000 nodes randomly divided into 100 shards. What is the number of malicious nodes, such that the situation where at least one shard having 51% or more malicious nodes occurs with probability p?

For example, it would be important to know the number of malicious nodes such that there is a 50% chance of launching a 1% attack.

In analogy to the birthday problem, the number should be significantly less than 5000.

## Replies

**MihailoBjelic** (2018-10-30):

Of course, it was one of the critical things to calculate/evaluate at the beginning of the sharding research. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Roughly speaking, if we assume: 1) a large validator pool with no more than 1/3 of malicious validators and 2) a secure RNG (this is extremely important), than a committee of a few hundred validators (e.g. 350) has an extremely small probability (probably around 2^-40) of having a malicious majority.

For more details, you can check [this answer](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-is-the-randomness-for-random-sampling-generated) in Sharding FAQs.

---

**daniel-tung** (2018-11-01):

I think the reply and the link given are pertain to a different problem.

The answer given is on the probability of randomly choosing more than half (> N/2) malicious nodes, given p% of chance to be chosen.

The problem posted above is related to finding the probability of *at least one shard* having more than half malicious nodes.

To illustrate this, let’s adapt the birthday problem to this situation:

Say there are 1095 nodes in total, being divided into 365 shards, 3 nodes in each shard. Then if the malicious node only controls 23 of the nodes (merely 2.1% of the nodes), there is already a 50% chance of at least one shard having 2 malicious nodes. This means in every two rounds of random sampling, there is, on average, one round where the malicious player controls one shard.

The probability is therefore much higher than what the link is given.

---

**MihailoBjelic** (2018-11-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> The problem posted above is related to finding the probability of at least one shard having more than half malicious nodes.

That’s exactly what my reply pertains to.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> birthday problem

I fail to understand how the birthday problem is relevant for analyzing this issue. We are discussing probabilities, and we already have a number of proven formulas/methods to calculate them (the most appropriate one in this case would be Binomial distribution).

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> Say there are 1095 nodes in total, being divided into 365 shards, 3 nodes in each shard.

This example is not appropriate because the validator set in Ethreum will be much larger. Simply put, that’s exactly why the probability of a malicios majority on a single shard is negligible.

---

**drcode1** (2018-11-01):

Ah, now I understand why such great emphasis has been placed recently into keeping staking requirements low.

---

**MihailoBjelic** (2018-11-01):

Yep, and that (negligible probability for electing a malicious committee) is only one of the benefits of this model. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) The others are:

1. Low barriers to entry (we don’t want this to be rich people’s game; now even a small group of enthusiasts in a developing country can join forces and run a validator node)
2. Extremely high censorship resistance (instead of big pools and farms that adversaries such as governments can easily locate, attack, confiscate etc. you have thousands of anonymous nodes all around the world, each  running nothing but a single machine)
3. Rich are not getting richer (unlike conventional PoS models, if you want to scale your stake in order to increase your earnings/rewards, you also need to linearly scale a number of machines you’re running; this maxes substantial stake concentration almost impossible).

IMHO, this (by “this” I mean low-barrier, highly decentralized, equally staked validator set model) is the single most brilliant design choice in Ethereum 2.0. ![:ok_hand:](https://ethresear.ch/images/emoji/facebook_messenger/ok_hand.png?v=9)![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=9)

---

**daniel-tung** (2018-11-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> That’s exactly what my reply pertains to.

One-shard takeover is about controlling any one shard (i.e. at least one shard).

Your link gives the probabilities of *one given shard* being controlled.

The chance of at least one shard being controlled could be much larger than this, depending on the value of N.

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> This example is not appropriate because the validator set in Ethreum will be much larger. Simply put, that’s exactly why the probability of a malicios majority on a single shard is negligible.

How big is the validator set? If N is too large then it beats the purpose of sharding.

Also, the more reshuffling going on to avoid collusion, the higher expected number of times of one shard having majority of malicious nodes.

---

**MihailoBjelic** (2018-11-02):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> One-shard takeover is about controlling any one shard (i.e. at least one shard).
> Your link gives the probabilities of one given shard being controlled.
> The chance of at least one shard being controlled could be much larger than this, depending on the value of N

“The chance of at least one shard being controlled” has nothing to do with N in this case, it’s simply “the probability of a single shard takeover” * 1000 (number of shards), i.e. roughly 2^-40 * 1000 (this is the worst case, it might be much lower than that).

I can see you’re really interested in this issue, so let me put it into perspective for you. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) If we assume:

1. constant presence of 1/3 malicious validators (basically a permanent attack)
2. 2^-40 * 1000 probability
3. reshuffling every hour (this is not final yet)

then we can realistically expect that “at least one shard” will be taken over every 125,515 years. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) And I repeat, the system needs to be under permanent attack for all this time. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> How big is the validator set? If N is too large then it beats the purpose of sharding.

AFAIK, the long-term target is 10M ETH staked, i.e. 312,500 validators. Would you mind explaining why do you believe this defeats the purpose of sharding?

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/d/67e7ee/48.png) daniel-tung:

> Also, the more reshuffling going on to avoid collusion, the higher expected number of times of one shard having majority of malicious nodes.

Of course, I took this into consideration in the calculation above.

---

**Enigmatic** (2018-11-04):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> Rich are not getting richer (unlike conventional PoS models, if you want to scale your stake in order to increase your earnings/rewards, you also need to linearly scale a number of machines you’re running; this maxes substantial stake concentration almost impossible).

Hi Mihailo - Please don’t mind me catching up with the implementation details with regard to the staking amount. Is the restriction on stake scaling per validating node enforced as “a maximum stake of 32ETH” or “the higher the amount stake the lower the return”, or etc?

Thanks in advance.

---

**MihailoBjelic** (2018-11-04):

Sure, no problem. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

It’s the former, a single validator has a fixed stake of 32ETH. So, if you want to stake e.g. 100*32ETH, you need to run 100 machines/validators, which makes stake concentration in the validator pool extremely unlikely.

---

**daniel-tung** (2018-11-13):

![](https://ethresear.ch/user_avatar/ethresear.ch/mihailobjelic/48/20459_2.png) MihailoBjelic:

> AFAIK, the long-term target is 10M ETH staked, i.e. 312,500 validators. Would you mind explaining why do you believe this defeats the purpose of sharding?

312,500 is total number of validators right? how many validators in one shard?

---

**MihailoBjelic** (2018-11-13):

I’m sorry, I don’t see this discussion being productive in any way. Have a nice day. ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=9)

---

**master-davidlee** (2022-08-11):

It looks like you are saying that the reason for mandating 32 ETH per verifier is to have more verifier nodes/machines, which is for the purpose of preventing equity concentration. But I have two questions, 1 an attacker with a lot of money can control a higher percentage of verifier nodes, which factor has a greater impact on security, the increase in the number of nodes or the increase in the percentage of malicious nodes 2 one article states that malicious nodes can take over a shard with a higher probability by creating multiple qualified sybil nodes “A tractable probabilistic approach to analyze sybil attacks in sharding-based blockchain protocols” Do you think this article is right

