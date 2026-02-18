---
source: ethresearch
topic_id: 1105
title: Allowing validators instant logout is a bad idea
author: vbuterin
date: "2018-02-17"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/allowing-validators-instant-logout-is-a-bad-idea/1105
views: 1949
likes: 0
posts_count: 7
---

# Allowing validators instant logout is a bad idea

Suppose that validators are infinite-term, so no logout or withdrawal is possible. Suppose that a (51%+) attack begins, which degrades performance and causes even honest validators to start losing small amounts of money from inactivity penalties. Honest validators have one of three choices:

- Keep attempting to validate on the main chain
- Coordinate on a minority fork
- Do nothing (ie. shut down)

The first strategy might give them a payoff of -1 on the main chain and -10 on the minority fork (because that’s what minority forks do; they heavily penalize any validator that is not participating in the fork). The second strategy would give them a payoff of -5 on the main chain and 0 on the minority fork. The third would give them a payoff of -5 on the main chain and -10 on the minority fork. Hence, honest validators have to make a judgement: could they successfully coordinate a minority fork? If probably yes, they go for strategy 2, if probably no, they go for strategy 1.

However, suppose that we add “log out” into the decision set. Log out gives a payoff of 0 on the main chain and 0 on the minority fork; hence, it strictly dominates all other strategies. However, validators logging out is quite a pathological outcome, because it only further cements the attacker’s stranglehold on the blockchain.

Hence, it seems that allowing logging out during any situation that might look like an attack is a bad idea. However, we also want to prevent or at least discourage griefing attacks that make it impossible for validators to ever leave.

I see two approaches:

1. Allow validators to log off with 1 month’s notice (replacing 1 month with the length of time needed to perform a minority fork under near-worst-case conditions)
2. Remove the concept of logging off entirely, in favor of fixed-term deposits (say, 4 month term). Allow validators that are in “term ended, waiting for withdrawal” mode to extend their terms for another term length, potentially indefinitely.

(2) can serve the secondary function of enforcing fairness if conditions for depositing change. For example, if the minimum deposit size increases between the start of one term and the start of the next term, then term extension can only be allowed if the deposit satisfies the same conditions that a newly logging in validator would.

## Replies

**vindberg** (2018-03-09):

Fixed-term deposits sounds like a valid solution. If implemented, how would a validator increase its deposit during that period? Should we spin up another validator node if we wanted to stake more eth?

In the current simple_casper contract it not possible to increase the stake without doing a logout but I guess that would change then.

We are planning to serve wallet providers by enabling staking for their users, creating a validation pool so this discussion is very interesting for us.

B,

Vindberg

---

**kladkogex** (2018-03-09):

What is your definition of perversiv[quote=“vbuterin, post:1, topic:1105”]

Because that’s what minority forks do; they heavily penalize any validator that is not participating in the fork) [/quote]

Is it possible to describe the “minority fork” mechanism in more detail - I do not think it is described in the Casper paper. How does a smartcontract determine

it is a minority fork?  What is the definition of “non participating in the fork”?

---

**drstone** (2018-03-09):

My intuition is that there is some function “fork” on the PoS smart contract and once forked, creates a copy of the previous main consensus contract. Thus it mirrors the same validator set and so it knows if validators are not participating in it and begins punishment immediately of those validators. Though, this may be incorrectly formulated.

[@vbuterin](/u/vbuterin) You mention that logging out is a strictly dominant strategy but that isn’t the case according to your payoffs; please correct me if I’m missing something. But with strategy 2 vs. logging out, it is (-5,0), (0,0) so log out only weakly dominates strategy 2 if it exists.

I had mentioned this to [@nate](/u/nate) as a high-level topic and since I am not sure where all these constants in the protocol come from (4 month fixed-term length, etc.). In this framework, we only analyze the utilities of the validators. We also have some target/optimal behavior that we want validators to follow. This behavior creates an optimal setting for finality to occur and so defines the utility of the PoS mechanism.

If we (can) define the utility of mechanism designer/blockchain mechanism, then we would want to maximize the social welfare + designer welfare. Then using polynomial weights over various parameters in a multi-armed bandit setting, we can arrive at optimal fixed-term lengths or other constants over time in a traditional no-regret fashion, ensuring that we maximize the function we want. This could be the frequency of finality occurring, etc.

---

**djrtwo** (2018-03-15):

Coordinating a fork happens out-of-band. There is no in-protocol mechanism to conduct a fork.

To conduct a fork in this instance, the minority validator pool would stop building on and finalizing the attacker’s blocks. They would only be concerned honest validator’s blocks and messages, thus forking from the attacker chain. Their fork would not be able to finalize until the attacker bled due to inactivity and they became the 2/3 majority.

---

**jacob-eliosoff** (2018-04-05):

Anyone have a link to a description of how a 51% attacker would cause honest validators to suffer inactivity penalties?  (I presume you don’t just mean a DOS attack.  For Casper, would the “51%” actually need to be 67%?)

As a high-level note, while I’m all for protecting against these attacks, given how debilitating 51% control already can be under PoW, I think it should be a much higher priority right now to ensure Casper behaves well when it’s *not* under 51% attack than when it is.

---

**BenMahalaD** (2018-05-15):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Remove the concept of logging off entirely, in favor of fixed-term deposits (say, 4 month term). Allow validators that are in “term ended, waiting for withdrawal” mode to extend their terms for another term length, potentially indefinitely.

How does this work with respect to withdrawals, what’s stopping someone from attacking at the very end of their term and then leaving?

I wonder if this could be solved by having the ability to automatically and programmatically force-logoff people who are provably not voting. Say if it has been N epochs since the last checkpoint, then a validator who has not voted since the last checkpoint gets automatically logged out.

Now you could have an attacker try and censor votes from other validators by orphaning any blocks with votes in them so the longest chain has zero votes in it, but you could solve this by having clients not just hold the longest chain since the last checkpoint, but also all minority chains as well.

In this situation, there would obviously be two chains, an attacker chain with only their votes (or no votes in it) and a smaller honest chain without the attacker. After N epochs, the attacker would be logged out of the honest chain, and finality would be reached.

