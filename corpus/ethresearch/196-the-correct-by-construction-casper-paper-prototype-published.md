---
source: ethresearch
topic_id: 196
title: The "correct by construction" Casper paper + prototype published at DEVCON. Tear it apart
author: virgil
date: "2017-11-05"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/the-correct-by-construction-casper-paper-prototype-published-at-devcon-tear-it-apart/196
views: 4276
likes: 15
posts_count: 21
---

# The "correct by construction" Casper paper + prototype published at DEVCON. Tear it apart

Paper: https://github.com/ethereum/research/blob/master/papers/CasperTFG/CasperTFG.pdf

Prototype: https://github.com/ethereum/cbc-casper

## Replies

**djrtwo** (2017-11-05):

Tear it apart! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

Just wanted to let the forum know that we’ll be enhancing the codebase and getting some closer to real-world experimental results soon. We will also be cleaning up the paper a decent amount over the next couple of weeks.

I’ll drop a line here when we bump the version on either the code or paper.

As for the code, if you are interested in getting involved, check out/comment on our current [issues](https://github.com/ethereum/cbc-casper/issues) and feel free to reach out to me to discuss where might be a good place to start.

Thanks in advanced for all of the feedback and questions we expect to get here.

---

**jamesray1** (2017-11-10):

Unfortunately the link for the PDF doesn’t work for me.

---

**djrtwo** (2017-11-10):

Weird. Here’s the raw https://github.com/ethereum/research/raw/master/papers/CasperTFG/CasperTFG.pdf try that. And here’s the folder it is in https://github.com/ethereum/research/tree/master/papers/CasperTFG.

Let me know if those work.

---

**jamesray1** (2017-11-11):

Both of those links work! Thanks.

---

**jamesray1** (2017-11-13):

I have opened [>25 PRs](https://github.com/ethereum/research/pulls) as well as 4 issues on Github.

Last sentence before section 2: “Thus, two nodes who decide on safe estimates have consensus safety if there is less than t Byzantine faults, and all this required saying almost nothing about the estimator! :)” While I appreciate the emoji ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9) , this is a formal academic paper, and my understanding is that it is not conventional to use such emojis, so it may be best to omit it. But I guess it’s not a big deal if it’s included and maybe a few people don’t like it.

Haha, an e-clique sounds like it will be meme-worthy.

---

**kladkogex** (2017-11-16):

Here is my recap (correct it if I am wrong)

1. Validators issue bets on the corrrect block, specifying how sure they are in a bet
2. initially validators are not sure in their bets, but as time progresses and nodes get info about bets from other nodes
a node can do a new bet. Ultimately bets become stronger and stronger and reach a safety threshold.

What I do not understand from the paper is

1. What algorithm does a node use when making a new bet based on the current info (graph of bets from other nodes)?
Is this function fixed? You could imagine a network, where nodes would use machine learning to issue bets based
on the previous history.
2. What bounties do validators get for issuing early correct bets? One would imagine a network where validators would
be strongly “bountied” for issuing early correct and sure bets, so there would be a competition essentially in
machine learning algorithms.
3. What is Weight? How is it related to deposit?
4. What is safety and what algorithm is used to decide that a block is safe? Is it a simple weighted sum of most recent bet estimates, if yes, how is the threshold determined?  One could imagine a network where the threshold sum would be determined by machine learning essentially as a  regression algorithm.

---

**jamesray1** (2017-11-17):

[@kladkogex](/u/kladkogex), your understanding seems correct to me.

While your queries may not be addressed in the paper, they may be in the code at [GitHub - ethereum/cbc-casper](https://github.com/ethereum/cbc-casper).  I haven’t had a look there yet, but I plan to. If they’re not addressed then they would be topics for research!

---

As far as I know, specific reward amounts haven’t been determined yet, but I haven’t read much yet so I may be wrong. I remember reading in a [blog post by Vitalik](https://blog.ethereum.org/2016/03/05/serenity-poc2/) that there is a high reward for betting early and with high surety, while he also mentioned there was a penalty for betting incorrectly with maximum surety.

> More precise numbers on interest rates and scoring rule parameters – the scoring rule (ie. the mechanism that determines how much validators get paid based on how they bet) is now a linear combination of a logarithmic scoring rule and a quadratic scoring rule, and the parameters are such that: (i) betting absolutely correctly immediately and with maximal “bravery” (willingness to converge to 100% quickly) on both blocks and stateroots will get you an expected reward of ~97.28 parts per billion per block, or 50.58% base annual return, (ii) there is a penalty of 74 parts per billion per block, or ~36.98% annual, that everyone pays, hence the expected net return from betting perfectly is ~22 parts per billion per block, or ~10% annual. Betting absolutely incorrectly (ie. betting with maximum certainty and being wrong) on any single block or state root will destroy >90% of your deposit, and betting somewhat incorrectly will cause a much less extreme but still negative return. These parameters will continue to be adjusted so as to make sure that realistic validators will be able to be reasonably profitable.

> More precise validator induction rules – maximum 250 validators, minimum ether amount starts off at 1250 ETH and goes up hyperbolically with the formula min = 1250 * 250 / (250 - v) where v is the current active number of validators (ie. if there are 125 validators active, the minimum becomes 2500 ETH, if there are 225 validators active it becomes 12500 ETH, if there are 248 validators active it becomes 156250 ETH). When you are inducted, you can make bets and earn profits for up to 30 million seconds (~1 year), and after that point a special penalty of 100 parts per billion per block starts getting tacked on, making further validation unprofitable; this forces validator churn.

---

The set of weights are outlined on p. 5 after definition 2.3 as a map from the set of validators to the set of positive real numbers. But yes, I also thought the paper was a bit vague on weights. IIRC the finality gadget paper gives more info on weights. A validator’s weight (or a set of validators) is the ratio of their deposit size to the total deposits of all validators. I’ll make a PR to clarify that (if my understanding is incorrect then I’ll be corrected).

Definition 4.2 and algorithm 2 on pp. 9–10 may address your question about safety, although as you can see it has left out detailed proofs.

---

**vbuterin** (2017-11-17):

Casper FFG and CBC have nothing to do with the scoring rule paradigm that we expressed back then. They are completely different protocols.

---

**jamesray1** (2017-11-17):

OK. Even still, what was expressed in that blog post gives you an idea of a possible implementation, even if such an implementation is rejected.

---

**djrtwo** (2017-11-17):

Thanks [@jamesray1](/u/jamesray1)! I’ve been out this week but will be reviewing all your PRs Monday.

---

**jamesray1** (2017-11-18):

No worries [@djrtwo](/u/djrtwo)! Vlad is already onto it!

---

**nate** (2017-11-18):

If CBC Casper validators are building a blockchain, then the bets they are making *are blocks themselves*. This is a fundamental difference between CBC Casper and most other existing consensus protocols.

Also, when validators make blocks, they don’t specify how sure they are about this block (or any other block, for that matter) being in the chain. In fact, when they make a block, they have absolutely no safety guarantees on that block, as no one has built on top of it yet!

> What algorithm does a node use when making a new bet based on the current info (graph of bets from other nodes)?

The algorithm that determines where to build a new block (which, remember, are the bets), is called the forkchoice. You can read a python implementation [here](https://github.com/ethereum/cbc-casper/blob/master/casper/blockchain/forkchoice.py), and read about the inspiration [GHOST](https://eprint.iacr.org/2013/881.pdf). Essentially:

1. Set current_block to the last block that is “final” in a view.
2. Look through current_block’s children and find the one with the heaviest weight. Select that child as the new current_block.
3. Repeat step 2 until the current_block  has no children.

When the *current_block*  has no children, you have reached a tip of the blockchain. If you want to make a new block, use this block as the block to point to with your previous block pointer. This is your new bet/block!

> What is Weight? How is it related to deposit?

In the case of PoS, weight == deposit. But as CBC Casper is specified a general purpose consensus protocol, there is no need to say it will always be a deposit. You can imagine giving all the validators the same weight, and just having a “regular” consensus protocol where the participating nodes are known and all equal.

> What is safety and what algorithm is used to decide that a block is safe? Is it a simple weighted sum of most recent bet estimates, if yes, how is the threshold determined? One could imagine a network where the threshold sum would be determined by machine learning essentially as a regression algorithm.

There are a couple different safety oracles that can be used to determine if a block is safe. You can see implementations of them [here](https://github.com/ethereum/cbc-casper/tree/master/casper/safety_oracles). Most of them come from the “ideal adversary” line of thinking. The idea here is essentially: if the entire world was trying to convince me that this block will not end up in the main blockchain, and they can’t do it, then this block is absolutely going to be in the main chain. The ideal adversary essentially simulates the entire world conspiring to remove the block from the chain - and if it can’t do it, then no one can.

---

**kladkogex** (2017-11-21):

Nate - OK - lets consider a simple example, where two competing blocks are mined in different segments of the p2p network APPROXIMATELY AT THE SAME TIME so that there are essentially two competing trees built

If validators get reward by identiying the correct tree, then it makes sense for a validator to wait until other validators decide.  Whats the economic incentive to vote early if voting later is less risky.

It does not actually matter what the specifc algorithm is. What matters is that a validator needs decide as early as possible which of the trees is the correct one, and the problem is a prediction problem,  the earlier you try to predict the more higher is the chance that you wlll mispredict, so by default there is an incentive to predict as late as possible after others predicted.

I read through the paper on casper economics, and it seems to include penalties for validators not voting in a particular epoch. If this is going to be implemented, then validators will rush to vote at the very end of the epoch, which may create a DoS attack.

---

**vlad** (2017-12-02):

This paper is not about economics It gives an asynchronously safe blockchain consensus protocol. And it doesn’t prove liveness.

So, as far as the work presented here is concerned, it may be that you never end up with a new safe block; one that you know will always be in your fork choice rule. But there are cases where you can determine that the protocol is “stuck” and there’s no way (regardless of timing conditions) that a block won’t be in your fork choice rule in the future (assuming that there’s less than some number of Byzantine faults).

---

**yhirai** (2017-12-04):

With the current definition, the intersection of M and L(v, M) is always empty.

---

**yhirai** (2017-12-04):

There is a paper http://ilyasergey.net/papers/toychain-accepted.pdf that does something in the same direction in Coq (accepted to CPP 2018).  The assumptions and the conclusion are both much weaker there.

---

**kladkogex** (2017-12-07):

Vlad - I think what I and many other people are missing is a 100-word simple explanation of how this works.

I have re-read the whitepaper multiple times, but I can not grasp  general mathematical feeling behind the security of it.

For any algorithm to be secure it has to be understood by people,  and the more people can understand it, the more people can improve it.  How would you explain it to your grandma in 100 words?

---

**yhirai** (2017-12-08):

Each party calculates all possible future scenarios where less than `t` validators (measured using the size of deposits) go Byzantine (= don’t equivocate, and emit estimates based on the justifications), and if an estimate is the same in all those futures, the estimate is `t`-safe.  This calculation can be done locally with signed messages from validators.  After any other messages, if the estimate is overturned, there must be `t` protocol violations.  In that case, you can blame `t` validators.

No incentive mechanisms are specified there, and the validators can do whatever, and with enough noise, everybody sees `t` equivocations, and the notion of `t`-safe doesn’t make sense anymore.  That’s a problem to be solved later.

---

**kladkogex** (2017-12-08):

Yoichi - let me describe a particular algorithm that I think corresponds (somewhat) to the description you are giving.

This algorithm makes an assumption there are ONLY TWO competing checkpoints. So it is a BINARY agreement.

I am going to describe it from the point of view of a particular validator V.  Lets assume we are trying to agree on a new checkpoint. Lets also take an example where not more than t of deposits are corrupt.

1. Initially validator V does not have any message from any other validator. So the validator sends a stage-0 guesstimate based only on its own local info, say on what the validator perceives as the heaviest subtree.
2. Then the validator waits for stage-0 messages from other validators, which represent at least N-t of deposits (including its own deposit).  It is clear that bad guys can withold sending anything, so
waiting for more than N-t messages could cause the algorithm to block.
3. The validator will then select the stage-1 estimate as the deposit-weighted majority of the estimates it received during Stage 0, including its own estimate. It will then send out its stage-1 estimate, and wait for stage-1 estimates from other validators, so we are essentially looping back to 2.

The 2.-3. loop can continue, hopefully as the loop progresses, the validators will start converging with each stage n.

In the example above, it is a binary consensus, and at some point there has to be a condition for the validator to stop the 2.-3. loop and commit.

The first question is then, whether the loop will converge.  In particular, lets assume that the node receives deposit-weighted X estimates at stage n equal to its own estimate.  The question is, whether the function X(n) will grow as n grows, so that the nodes will form a consensus as n grows.

The second question, is what is the commitment criterion, something that the paper calls a “safe condition”? At which point can a node feel safe and commit to an estimate? In other words what is the function S(X,n) such that a node can commit if S(X,n) > 1

The example above is for binary consensus. the real situation seems to be much more complex since there will be potentially multiple competing checkpoints, so we are talking about a multi-valued consensus, which is much harder for BFT algorithms.

And then an assumption that was made above is that each node follows the same strategy by selecting on each stage a deposit-weighted majority of the previous stage. But as you said “the validators can do whatever”, a validator may for instance try using machine learning (reinforcement learning) … This complicates things even further …

---

**yhirai** (2017-12-08):

The network is asynchronous, so the messages from stage 0 might not in time for stage 1 (or validators might not send messages and that’s considered fine).

So, the loop might not converge.

An example commitment criterion is implemented in the prototype.

The validators might do whatever, including machine learning, but when they send a message containing an estimate not backed by the justifications, they are considered Byzantine.

