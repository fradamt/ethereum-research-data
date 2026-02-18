---
source: ethresearch
topic_id: 5570
title: Cooperative game theory and ID-based cryptography for proof-of-stake consensus
author: richmcateer
date: "2019-06-06"
category: Consensus
tags: [identity, sybil-attack]
url: https://ethresear.ch/t/cooperative-game-theory-and-id-based-cryptography-for-proof-of-stake-consensus/5570
views: 1765
likes: 1
posts_count: 4
---

# Cooperative game theory and ID-based cryptography for proof-of-stake consensus

We are currently running an experiment called HumanityDAO, which attempts to maintain a registry of unique humans without a central authority (https://www.humanitydao.org/).

The ID verification game is based on web of trust, in which new applicants must be connected to verified humans (on Twitter) to join the registry. New humans earn voting tokens, which can then be used to vote on new applicants.

Interestingly, the payoff matrix for validators looks similar to a prisoner’s dilemma game. If the validators cooperate (i.e. vote YES to real applicants and NO to Sybil or duplicate applicants), the registry of unique humans is accurate, which means it can be used in Sybil-resistant smart contract protocols and the token should therefore increase in value. Validators can defect by voting incorrectly either to let Sybils in or just to troll the system. A 1959 paper ([https://en.wikipedia.org/wiki/Prisoner’s_dilemma](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)) shows that rational players can sustain a cooperative outcome in an unknown-round game.

I am curious whether this system can be improved and generalized as a proof-of-stake consensus mechanism. Early results are promising, but the system has yet to be truly battle-tested. I also don’t know how it would hold up with the additional complexities of a distributed computing environment.

Apologies for trying to explain this on Twitter, I forgot this forum existed.

## Replies

**tawarien** (2019-06-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/richmcateer/48/3817_2.png) richmcateer:

> The ID verification game is based on web of trust, in which new applicants must be connected to verified humans (on Twitter) to join the registry. New humans earn voting tokens, which can then be used to vote on new applicants.

Why the dependency on a centralized service like Twitter? Wouldn’t it be enough to allow verified humans to simply claim that they know / are connected to a new  applicant without the need of a round trip over a centralized service?

---

**richmcateer** (2019-06-06):

Yes, the project will eventually support other verification methods (Github, Discord, in-person, etc.). We started with Twitter for simplicity and virality.

---

**Xrosp** (2019-06-06):

I like this idea but why not capture the attributes that allow the new applicants to share data through cookies. This would leverage virality and also allow for compounded interest from data acquisition being leveraged by the user.

Also consider that true game mechanics would allow any user to display a series of attributes that are already mapped to identify their preferences and habits.

The benefits are also increased because there is incentive to transform the humanityDAO to the millions of sites and companies that already capture data from users. It could facilitate a seamless integration, payoff for all entities, smart contract protocols validator with ease.

