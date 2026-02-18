---
source: ethresearch
topic_id: 1050
title: Cryptoeconomic oracles
author: whgeorge
date: "2018-02-11"
category: Proof-of-Stake > Economics
tags: []
url: https://ethresear.ch/t/cryptoeconomic-oracles/1050
views: 3016
likes: 5
posts_count: 8
---

# Cryptoeconomic oracles

I recently wrote a [blog post](https://medium.com/kleros/kleros-and-augur-keeping-people-honest-on-ethereum-through-game-theory-56210457649c) talking about some of the cryptoeconomic issues in encouraging honest oracles for smart contracts, specifically comparing some of the choices of Kleros (which I work on) and Augur.

As this crowd is interested in cryptoeconomic issues, I would be interested in hearing people’s thoughts (here or on the kleros slack at [slack.kleros.io](http://slack.kleros.io)).

## Replies

**vbuterin** (2018-02-12):

> Ultimate appeal
> [Augur] Fork into multiple chains, one for each outcome to disputed case
> [Kleros] Kleros general court

Why not have Kleros use the same mechanism of allowing dissenters of general court decisions to split off and make their own fork? It *is* a good way of dealing with global 51% attacks, as it ensures that if a successful 51% attack leads to the wrong answer then that particular system can get easily outcompeted by a clone that has more honest stakeholders.

---

**vbuterin** (2018-02-12):

Also, there is a third kind of proposal that I think someone should try at some point (this is not my original idea, though this specific formulation is): basically, use forking into multiple chains to solve *every* problem. The idea is that if there are N decisions that have been made, then you have 3^N token types, where each token type is a length-N ternary string (eg. 012010221). When the system starts, everyone has only tokens of type 000000… Anyone has the ability to split tokens of type x0y, where x and y are arbitrary strings, into 1 token of type x1y and 1 token of type x2y (eg. 012010221 can split into 012110221 + 012210221), and you can also recombine.

Anyone has the ability to burn 1 coin of any type to ask a question; question IDs are sequentially assigned globally. At that point, anyone who has coins of that type or a subtype (eg. if the type is 012010221, then with the new assigned question ID it becomes 0120102210, and 1120102210 is a subtype) is expected to convert them into *1 + *2 pairs (eg. someone with 1120102210 would convert to 1120102211 + 1120102212), and sell the coin that they think corresponds to the incorrect answer and buy the coin that they think corresponds to the correct answer (this could be done on a DEX, or the 1 coin could be used to subsidize an on-chain market maker).

The goal here is that coin types that correspond to correct answers are the coin types that people would want to burn in order to ask the holders of those coins questions, as people feel those holders are more likely to give more correct answers, and so coin types that correspond to correct answers will be more valuable, and most other coin types will fall to such a low value that most of the time people will not even bother to send a single transaction of them (this is why this scheme won’t actually have exponential overhead in practice even if it seems like it might in theory).

You could also organize the scheme as a tree, where you can burn 1 coin of some type and at that point generate two child types that everyone must choose between, but the 3^N hypercube solution (yay, hypercubes!) is nice because it potentially allows decisions to be made in parallel, and it allows users to just not participate in votes that they are not sure about.

---

**whgeorge** (2018-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Why not have Kleros use the same mechanism of allowing dissenters of general court decisions to split off and make their own fork? It is a good way of dealing with global 51% attacks, as it ensures that if a successful 51% attack leads to the wrong answer then that particular system can get easily outcompeted by a clone that has more honest stakeholders.

We imagine that there might be extreme cases where community would want to fork the Kleros token, particularly after a sucessful 51% attack. The difference between that and what Augur does is that  in Augur’s scheme the ETH in the prediction markets goes with the fork that has the most REP committed to it (via users choosing that side of the dispute) within a certain period. At first glance, this might seem better, but if an attacker could mount a 51% attack to win a malicious case in the Kleros general court, then they would also have enough tokens to make sure that their branch of a fork “wins” the dispute under an Augur-like mechanism and gets all the ETH in the current contracts (even if the token itself on attacker’s branch winds up being worthless). So whether you build in an automatic forking mechanism from the beginning or whether the community does it ad hoc after an attack, an attacker capable of doing a 51% attack will wind up with all of the ETH in the current contracts on their side of the fork either way.

So really the advantage of the Augur forking proposal is that an attacker risks rendering her tokens worthless by committing them to a malicious branch of a fork, inflicting on herself a potentially greater cost for performing the attack. The downside of their proposal is that users who are unsure of the correct response to a question will be risk averse/not willing to commit their entire holdings and will not commit their tokens to either side of the fork, ie not vote. Then it can actually become easier for an attacker to steal the ETH in the current contracts with less than 51% of the tokens. For Augur, people are voting on the result of a prediction market - namely they are voting whether some real event has already happened, so it is rare that there isn’t some clear, correct answer. For Kleros, there will often be cases where reasonable, non-malicious jurors will disagree increasing the risk of situations where unsure token holders would avoid committing themselves either way in the event of a fork.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, there is a third kind of proposal that I think someone should try at some point

Interesting idea. I’ll think about this.

---

**rkapurbh** (2018-02-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> sell the coin that they think corresponds to the incorrect answer and buy the coin that they think corresponds to the correct answer

Can such a model be applied to questions with more than 2 potential answers?

---

**vbuterin** (2018-02-13):

Yes, you just binary-encode the question into log(N) questions.

---

**clesaege** (2018-02-18):

Let’s recap the difference between forcing fork via contract rules(Augur) or only having fork by social consensus(Kleros).

Pros of contract rules over social consensus:

-Fork by contract rules forces people to make a decision. Without it people may not bother or not even be aware of the fork (even if clients dev should warn during forks).

-Fork by contract rules may force communities to split on some issues which are not necessarily an attack but a different interpretation of rules. This is more likely for general dispute resolution mechanism than prediction market oracle.

-Fork by contract rules will likely result in more forks. This will lead to higher competition between forks but also a more fractioned ecosystem with lower individual marketcaps and therefore less resistance against 51% attacks.

---

**clesaege** (2018-02-18):

Some idea of the truthcoin whitepaper was to allow miners to have the final say. It was in a different context, as truthcoin had planed to make their own blockchain.

But even in Ethereum we could let miners or stakers have the final say. We can count miners/stakers voices by requiring them to send tx to a contract which verifies that msg.sender==block.coinbase. We would then just need a counter and if a majority of them vote in direction, the oracle/dispute resolution system would follow it. It would not lower security as miners/stakers can softfork to censor tx of voter of one side anyways. But just formalises it such that it is not considered an attack.

Actually it could even be included in a lot of smart contracts having other purpose and would solve some disputes about stakers/miners forking to solve bugs. In this cases they could only do it in contracts which would follow this “validator as saviour” pattern and it would not break the principle of Ethereum as those contracts would still execute as planed (they would have planed to follow orders of validators).

So people in favor validator saving bugged contracts would allow it and orhers would not without fighting about the issue (as we’ve seen with the DAO hack and the recovery fund proposal).

