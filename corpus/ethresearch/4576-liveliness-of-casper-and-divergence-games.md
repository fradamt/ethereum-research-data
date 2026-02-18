---
source: ethresearch
topic_id: 4576
title: Liveliness of Casper and Divergence Games
author: kladkogex
date: "2018-12-13"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/liveliness-of-casper-and-divergence-games/4576
views: 3001
likes: 2
posts_count: 7
---

# Liveliness of Casper and Divergence Games

There is a liveliness question of Casper CBC (a similar problem may exist in Casper FFG)

from [@vbuterin](/u/vbuterin)   https://vitalik.ca/general/2018/12/05/cbc_casper.html

“I think it should be possible to write up an academic proof for consensus under synchrony for a class of problems I call “divergence games”. Suppose you have a game where validators publish messages, and each message is either +1 or -1. If the total sum of valid messages a validator saw is positive, validators will try to publish +1, if it’s negative, validators will try to publish -1, and if it’s 0 validators will do either. If the average time between new valid messages is greatly above network latency, then I would claim that you can guarantee it will converge to + or - infinity assuming honest majority.”

Consider a case where there are initially 51% of good validators voting for 1 (“majority vote”) and 49% of good guys vote for 0 (minority). Then the bad guys can send 0 votes to the “minority vote” good guys, and withhold the vote from the “majority vote” guys to keep the problem from being resolved deciding.   Note  that witholding a vote is not a slashable offense.

Note that the same problem may exist in Casper FFG.  If there are two approximately identical subtrees trees, validators may get stuck (50/50) resolving them, and then move to create a deeper link.   The bad guys though may again withold the vote from some nodes. and having a smart algorithm (say machine learning) may prevent finalization forever,  provided that the good guys are dumb enough … It may be a hard things to do but seems possible.  The next step is to do simulations to prove or disprove this.

## Replies

**vbuterin** (2018-12-13):

> Consider a case where there are initially 51% of good validators voting for 1 (“majority vote”) and 49% of good guys vote for 0 (minority). Then the bad guys can send 0 votes to the “minority vote” good guys, and withhold the vote from the “majority vote” guys to keep the problem from being resolved deciding. Note that witholding a vote is not a slashable offense.

Note that the good guys can and will change their vote to align with what they see as the majority. So if there exists a span of time where no one submits new messages long enough for everyone to see what was already submitted, then all of the validators will see the same value, and it will start diverging in one direction from there. So maintaining an attack that prevents the game from diverging is a very unstable and delicate matter.

---

**kladkogex** (2018-12-14):

Vitalik - agree ,  it is not a very realistic attack, having that the bad guys have to keep on doing it forever and be lucky to keep the unstable equilibrium …

---

**PhABC** (2018-12-15):

As Vitalik suggested, I believe simulations and analytical linearization of such a model would indicated that the 50% mark is a fixed *unstable* point, where small perturbation would push the system on one side or the other with increasing velocity.

---

**Alistair** (2018-12-17):

Under the assumption that “the average time between new valid messages is greatly above network latency”, the analysis of this is very similar to that that shows  the longest chain rule will reach eventual consensus on which of two blocks is in the chain, which has been analysed many times with the result that 50+epsilon% honest is enough if the network latency is small enough compared to epsilon. The balance attack has also been analysed a bit for proof of work:https://arxiv.org/abs/1612.09426 . Iddo Bentov’s latest PoW scheme, which I saw him talk about at Buidl, actually includes a common coin specifically to defeat this kind of attack.

A protocol like epochless Casper FFG, where many validators vote at the same time, is a bit more vulnerable to this. If the voters voting at one block height vote closly enough together that they do not take each other’s vote into account, then there is some time that bad guys witholding deciding votes can vote to split the voters and keep the divide going. I’d doubt that the network is predictable enough to keep this going for long, but it’s annoying in theory.

---

**dlubarov** (2019-04-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> So if there exists a span of time where no one submits new messages long enough for everyone to see what was already submitted, then all of the validators will see the same value

It seems like an attacker could stall consensus by broadcasting contrarian votes at the last second though, so that only a portion of the network will observe them in time.

Say we’re running Casper FFG with 100 nodes, with 67 being honest, and 33 controlled by an adversary. Say we have this checkpoint structure:

```plaintext
1   2   3   4   5
―――――――――――――――――
    b ― d ― f ― h
  /
a
  \
    c ― e ― g ― i
```

Say `a` is justified, and nothing is justified in epoch 2. In epoch 3, 40 honest nodes vote `a → d`, while 27 vote `a → e`. Suppose miners build off of `e`, so the fork choice rule favors that branch.

In epoch 4, the adversary broadcasts 33 votes for `a → d` at the last second. 27 honest nodes observe the votes in time, see that `d` is justified, and vote `d → f`. 40 don’t observe them in time, and vote `a → g`.

Similarly, in epoch 5, the adversary broadcasts 33 votes for `a → g` at the last second. A minority of honest nodes observe that `g` is justified in time and vote `g → i`; a majority don’t and vote `d → h`. And so on…

Credit to [@AlexAtNear](/u/alexatnear) who raised very similar concerns in the context of other algorithms.

---

**nrryuya** (2019-07-24):

I think the divergence game cannot be easily applied for LMD GHOST since it only considers the latest message of each validator.

For LMD GHOST, the initial state of the game matters.

(Note that divergence games in a blockchain do not start with 0 vs 0 or even tie because of small forks by an adversary or temporal network failure.)

Specifically, we must consider these things:

1. A vote does not increase a score of the target block if the voter has already voted for that block: in non-LMD voting rules, if the protocol converges to one block and honest validators keep voting for it, its score will monotonically grow. However, in LMD voting rules, the score grows only if the previous latest vote of the voter is not for that block.
2. If a validator votes for a block different from the block which the validator previously voted for, the score of the previous option decreases.

