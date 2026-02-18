---
source: ethresearch
topic_id: 3079
title: Higher voting threshold for checkpoint committees
author: MihailoBjelic
date: "2018-08-24"
category: Sharding
tags: []
url: https://ethresear.ch/t/higher-voting-threshold-for-checkpoint-committees/3079
views: 1448
likes: 9
posts_count: 9
---

# Higher voting threshold for checkpoint committees

We currently target 2/3 threshold when voting on FFG checkpoints and/or crosslinks. Could we instead require a higher majority (e.g. 99%), and reduce the sample size?

If I’m not mistaken, this is a common practice for validating computation in grid/volunteer computing platforms like BOINC. Validation of blockchain state transitions is essentially the same thing.

The main point here is that we will need much smaller samples to achieve the same statistical security (I didn’t do exact calculations, but this is very obvious if you know how binomial probability is calculated). BOINC computations gets re-computed/validated 3-20x on average, while in Eth 2.0 we need hundreds of validators.

So, while retaining the same level of security, we can achieve:

1. Lower fees/inflation (less validators are performing the same work)
2. Higher availability of validators (less validators are busy validating a single shard → more are available to accept new tasks).

Did we simply inherit 2/3 from BFT research, and now we unnecessarily stick to it? Can we change our thinking paradigm to something similar to TrueBit’s computational courts - if we have e.g. 100 validators sample and 99% threshold, we need ONLY TWO honest validators NOT TO SIGN and we know something is wrong?

Thanks.

P.S. Clearly, we would use cryptoeconomics to incentivize honest and disincentivize bad actors (this is an obvious improvement over BOINC-like models).

## Replies

**eolszewski** (2018-08-24):

If we had 100 nodes in the system that required less than 34 to be byzantine to proceed, we have a much more robust protocol to byzantine actors and issues with liveness than if we were to require that less than 2 be byzantine. I assume this is the driving reason.

---

**MihailoBjelic** (2018-08-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/eolszewski/48/1902_2.png) eolszewski:

> If we had 100 nodes in the system that required less than 34 to be byzantine to proceed, we have a much more robust protocol to byzantine actors and issues with liveness than if we were to require that less than 2 be byzantine. I assume this is the driving reason.

Thanks for the answer. That logic is right for such extreme cases, of course, but my thinking is more like “can we have a sample of a size 100 instead of 300, and statistically prove that the security of the system is the same or higher”.

---

**eolszewski** (2018-08-24):

I don’t understand what you’re advocating - you’re asking why we can’t have a more strict majority  2/3 => 99% and using fewer validators. Validators are appointed to committees in rounds, there are active validators and those which are in a general pool - are you advocating that we have fewer active validators? If so, I don’t believe this is a detail which has been worked out yet.

---

**MihailoBjelic** (2018-08-24):

I’m sorry if it’s hard to understand. I’ve updated the post, maybe it can help you understand my reasoning better.

We have one large validator pool and we randomly sample it to form committees. General opinion at the moment is that those samples should have 200-300 validators, and 2/3 threshold. I’m only wondering if we can achieve the same level of security with smaller committees and higher threshold. This will have few benefits, I wrote about that in the post.

---

**ldct** (2018-08-24):

> the same level of security with smaller committees and higher threshold

you can, but you still lose a lot of liveness (an attacker with a small amount of stake can make it very unlikely that the small sampled committee will meet the high threshold)

---

**MihailoBjelic** (2018-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> but you still lose a lot of liveness (an attacker with a small amount of stake can make it very unlikely that the small sampled committee will meet the high threshold)

I’m trying to understand how would that attack look like if we leverage cryptoeconomics?

Let me try to sketch the model.

Standard (fast) mode:

1. Block proposer proposes a block
2. We sample a 50 validators committee
3. Validators vote on the block
4. We reach our strict threshold and block gets finalized

Attack (slow) mode:

1-3. The same as above

4. We don’t reach the threshold

5a. We sample a larger committee (e.g. 400 validators) with a lower threshold (2/3) and they vote on the same block, or

5b. We start an interactive game to prove if block computations/transitions are valid

6. If 5a/5b shows that the block is valid, we slash the validators from the small sample who didn’t vote, otherwise we slash those who voted.

Of course, 99.9% of the time we will be in standard (fast) mode.

Does this make sense? What’s the motivation/benefit for the attacker?

---

**vbuterin** (2018-08-25):

I have thought about similar ideas; in one of my earlier scalability proposals I had the idea that a block could be approved by either a committee of 42 of 50, or 90 of 135; assuming the attacker has 1/3 stake the two are equally unlikely for the attacker to reach. I believe Justin suggested extending it to be even more “fluid”, basically allowing any M of N where the probability of rolling a three-sided die N times and getting a 1 >= M times is less than, say, 2-40.

I personally think the idea is fundamentally reasonable, though it would complicate the protocol for not much value to include it at this point, as we’re *already* dual-purposing the FFG signatures as crosslink votes, and so the full 135 votes (or however many) would have to be included anyway.

---

**MihailoBjelic** (2018-08-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I have thought about similar ideas; in one of my earlier scalability proposals I had the idea that a block could be approved by either a committee of 42 of 50, or 90 of 135; assuming the attacker has 1/3 stake the two are equally unlikely for the attacker to reach. I believe Justin suggested extending it to be even more “fluid”, basically allowing any M of N where the probability of rolling a three-sided die N times and getting a 1 >= M times is less than, say, 2-40.

This sounds really cool to me, glad to see there are similar ideas.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> it would complicate the protocol for not much value to include it at this point

Yes, I was thinking the exact same thing. It’s definitely better to remove as much complexity as possible in the beginning, but it might be worth considering for future iterations.

