---
source: ethresearch
topic_id: 1003
title: How alive is Casper Liveliness Algorithm?
author: kladkogex
date: "2018-02-05"
category: Proof-of-Stake > Casper Basics
tags: []
url: https://ethresear.ch/t/how-alive-is-casper-liveliness-algorithm/1003
views: 2325
likes: 3
posts_count: 8
---

# How alive is Casper Liveliness Algorithm?

[Casper paper](https://github.com/ethereum/research/blob/master/papers/casper-basics/casper_basics.pdf) proves plausible liveliness, in a sense that it is always mathematically possible for validators to create supermajority links to produce new finalized checkpoints.  In other words, the system never deadlocks or stalls.

1. Would it be correct to day though that mathematically possible liveliness and real life liveliness seem are  two different things ?  In other words, a “dumb” set of validators may be not smart enough to produce the right supermajority link to get out of a deadlock.
2. Would it be correct also to say, that “dumb” validators could DoS things in a sense that they would create too many unnecessary supermajority links?
3. Since it looks like Casper is progressing to the release, would it be fair to start discussing the actual algorithm implemented in the source code ?
I was trying to find it starting from the source code of the docker container in the test net, but was not able to get to the actual algorithm that produces supermajority links …

## Replies

**vbuterin** (2018-02-05):

> Would it be correct to day though that mathematically possible liveliness and real life liveliness seem are two different things ? In other words, a “dumb” set of validators may be not smart enough to produce the right supermajority link to get out of a deadlock.

Correct. However, there is also a separate proof that using the Casper FFG fork choice rule (prefer highest justified epoch) is a sufficient strategy to achieve real liveness, at least if latency is sufficiently low that everyone receives everyone else’s messages in time.

> Would it be correct also to say, that “dumb” validators could DoS things in a sense that they would create too many unnecessary supermajority links?

No. A supermajority link requires votes from 2/3 of the validators, so such a scenario would require a large portion of validators to be seriously screwed up in some way.

> Since it looks like Casper is progressing to the release, would it be fair to start discussing the actual algorithm implemented in the source code ?

I’d personally prefer to keep code discussion out of scope at least here so that this can stay as a pure theory forum; maybe make github issues on the repo?

---

**kladkogex** (2018-02-05):

I read the paper multiple times, and I think I now understand everything up to Section 2.2.

What still confuses me is a logical gap from section 2.1 to 2.2. Section 2.1  discusses rules that validators must obey, and proves that,  if the validators obey these rules, there is always a way for a validator to add a supermajority link to create new justified checkpoints.

Therefore, section 2.1 does not seem to prescribe any strategy for the validator on how to actually to create these links that lead to justified checkpoints.

Section 2.2 discusses the fork choice rule under assumption of existence of the longest justified checkpoint.

What seems to be missing is a description of a simple reasonable strategy that a validator should take.

It may be that a strategy as simple as “steps back in time” will work - namely that if a validator thinks that a particular checkpoint should be justified, it should first try to justify it using the shortest possible smartmajority link, and then if the attempt deadlocks due to a split vote,   make other attempts for the same checkpoint moving the origin of the supermajority link back in history.  I think there was a discussion that in case of a network split  the situation can be remedied moving the origin of the supermajority link back in time to a point before the split.

I have a feeling that things will work well,  and simple reasonable “keep trying” strategies can work in this case.  What  would be nice though is to fill what seems to be a gap in the paper by providing at least a brief discussion of these strategies.

---

**vbuterin** (2018-02-06):

Agree that could be written better.

The correct strategy follows from the fork choice rule: always try to vote with the target checkpoint being the checkpoint the highest PoW checkpoint on top of the longest justified checkpoint, and the source checkpoint should be *what that chain thinks* is the most recent source checkpoint.

Alternatively, the source checkpoint could just *be* the longest justified checkpoint, but this is messier for a couple of reasons; namely:

(i) it means validators stop voting for T as their target as soon as T becomes justified

(ii) it’s more likely to not come to consensus in the case where there are 2/3 votes for some link but they fail to make it into the dominant chain for some reason, whereas looking at what the dominant chain says ensures that if nodes agree on what target to use they agree on what source to use.

---

**kladkogex** (2018-02-07):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The correct strategy follows from the fork choice rule: always try to vote with the target checkpoint being the checkpoint the highest PoW checkpoint on top of the longest justified checkpoint, and the source checkpoint should be what that chain thinks is the most recent source checkpoint.

I thought that this would need to be an additional sentence (do not claim to be a super expert on this though):

The correct strategy follows from the fork choice rule: always try to vote with the target checkpoint being the checkpoint the highest PoW checkpoint on top of the longest justified checkpoint, and the source checkpoint should be what that chain thinks is the most recent source checkpoint. *If after a timeout T you see, that the link you voted for did not turn into a supermajority link, then keep the source checkpoint, increment the target checkpoint by one checkpoint up, and then vote again.*

What I thought (correct me if I am wrong …) was that due to network delays, you could get to a fork point where there would be two strong links originating from a single origin checkpoint, going to two different target checkpoints on different branches of the fork,  and getting near 50\% each. In this case you would be deadlocked, and the way to resolve the deadlock would be to move one checkpoint up for the target and start voting again from a clean slate … Since the “clean slate” vote would happen later in time, by that time the network delays effects would subside, and the validators would be able to agree on a supermajority link

In other words, I thought that “local deadlocks” could happen for a particular pair of source/destination heights h1, h2.  Would you agree with that statement?  In other words you get two competing links that split votes and there is no way to reach supermajority on each of them, so the way to avoid a deadlock is to start from a clean slate in some sense?  I thought, that in real life the algorithm would need to use some kind of “keep trying” philosophy to get out of these “local deadlocks”

---

**vbuterin** (2018-02-07):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> If after a timeout T you see, that the link you voted for did not turn into a supermajority link, then keep the source checkpoint, increment the target checkpoint by one checkpoint up, and then vote again.

Nope! The current implementation does not do that. What it actually does is, as soon as its current head block is part of the next epoch (in the normal case, this just means that 50 blocks have been mined), it applies the algorithm again, voting in the new epoch.

> In other words you get two competing links that split votes and there is no way to reach supermajority on each of them, so the way to avoid a deadlock is to start from a clean slate in some sense?

The way you start from a sort of clean slate is precisely by waiting for a checkpoint of the next epoch to appear. Remember that Casper FFG is chain-based, so a proposal for epoch N implicitly contains a proposal for all epochs k < N; PBFT’s concept of sequence numbers and view numbers is effectively merged, and the role of both is taken up by epochs.

---

**kladkogex** (2018-02-07):

Ok ) Now I understand it, they will just keep voting for the fresher checkpoints until a supermajority link is created.  This should definitely work in a more or less low latency network where forks get settled down after a while.

Unless there is a major network problem that causes kind of a fractal set of forks to develop on top of the latest justified checkpoint, but this would be a temporary glitch which would get resolved after a while …

---

**vbuterin** (2018-02-07):

The Casper FFG testnet has had multi-hour latency between nodes because of networking issues, so there have been forks, but the chain is doing a great job of maintaining consistency and even liveness on finalized checkpoints: http://34.203.42.208:3000/

