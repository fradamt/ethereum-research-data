---
source: ethresearch
topic_id: 220
title: "Casper: Shape of Reward/Penalty PoC1"
author: jonchoi
date: "2017-11-17"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/casper-shape-of-reward-penalty-poc1/220
views: 2255
likes: 1
posts_count: 3
---

# Casper: Shape of Reward/Penalty PoC1

Recommended: [Link to working doc with images](https://paper.dropbox.com/doc/Casper-FFG-Reward-and-Penalty-Shapes-joTPPLGyNn4UJ9gr1ZXCq)

#### Asymmetric Risk/Reward for Good vs Bad Actors

The key to an ideal implementation will be a successful asymmetrically prominent reward for good actors and asymmetrically prominent penalty for bad actors. Taking arbitrary numbers for example, a mechanism that rewards good actors by up to 40% with maximum downside of 10-20% and penalizes bad actors by up to 75-100% with the same reward profile would be a successful asymmetric risk/reward design for good vs bad actors.

#### Reward/Penalty

1. Vote! Voting should always be better off than not voting.
2. Cooperate! The group should be rewarded for cooperating (finalizing with 100% p_v is a less fragile equilibrium than finalizing with 67% p_v, so they should be rewarded as such), and vice versa.
3. Finalize! There’s a discontinuous jump in rewards and penalties if the proportion of the validator set p_v voting on the correct checkpoint is lower than the supermajority.

#### Shapes of Y & N with respect to each p_v, ESF, TD

[![PoC1](https://ethresear.ch/uploads/default/optimized/1X/1828051c2c6dd5112b6345aba2bbc1141d0dc057_2_375x500.jpeg)PoC11620×2160 2.34 MB](https://ethresear.ch/uploads/default/1828051c2c6dd5112b6345aba2bbc1141d0dc057)

Here’s a proof of concept shapes of Y & N with respect to proportion of validators who voted, time since finality and total deposits. I’m sure a lot of this will change as we iterate, but here’s a first cut.

1. If you vote, you’re always better off than not voting.
2. If you vote, there’s no penalty other than the slashing conditions.
3. The more time passes since finality, the more your rewards deteriorate (until it’s 0) and the more the penalties become draconian.
4. There’s a fixed constant penalty (or removal of rewards) if p_v is below supermajority.
5. Reward rate increases if a higher proportion of the validators vote (or reward rate is decreased if a lower proportion of the validators vote. Same effect with non-voting.
6. Yield with respect to total deposits reflect fixed income assets (i.e. asymptotically approach market required returns as determined by validator set, more in +Casper FFG: Returns, Deposits & Market Cap). There’s some reasonable min TD to prevent excessively high yield.

#### Bootstrapping vs Mature Networks

The sections above suggested shapes of the rewards/penalties with respect to relevant variables. Let’s add another variable and another layer of complexity: maturity of the network (the validator set).

If the ultimate goal for total deposits is a $1B and the network is currently at $10M in deposits, we have to adjust the magnitude of the changes (i.e. slope, coefficients).

For example, the observed rewards level maybe trend down as the network becomes more stable and the required returns trend down. The observed penalties may also come down as security increases with higher TD as % of MCap.

*Need more eyes on this please, feedback welcome!* ![:unicorn:](https://ethresear.ch/images/emoji/facebook_messenger/unicorn.png?v=14)

## Replies

**kladkogex** (2017-11-21):

Jon - one  interesting question is how PoW mining will interact with Casper.

If I am a PoW pool,  I have an incentive to become a Casper validator and vote for my own mined blocks as early as possible.  As a result,  we may end up having a significant portion of Casper validators owned by competing PoW pools. In this case, each pool will always vote as early as a possible for the blocks mined by this pool.

---

**skithuno** (2017-12-27):

> If the ultimate goal for total deposits is a $1B and the network is currently at $10M in deposits, we have to adjust the magnitude of the changes (i.e. slope, coefficients).

Shouldn’t we just refer to a total deposit goal as a %MB as opposed to a $ value? MB seems to be the right abbreviation for all non-fractional reserve money ([wikipedia](https://en.wikipedia.org/wiki/Money_supply))

