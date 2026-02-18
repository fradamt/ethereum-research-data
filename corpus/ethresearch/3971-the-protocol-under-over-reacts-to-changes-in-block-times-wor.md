---
source: ethresearch
topic_id: 3971
title: The protocol under/over reacts to changes in block times. Worth Fixing?
author: MadeofTin
date: "2018-10-28"
category: Economics
tags: []
url: https://ethresear.ch/t/the-protocol-under-over-reacts-to-changes-in-block-times-worth-fixing/3971
views: 2516
likes: 3
posts_count: 9
---

# The protocol under/over reacts to changes in block times. Worth Fixing?

A few weeks ago I plotted Blocktimes overtime and noticed a pattern. The past few days I have been working on calculations around the difficulty bomb at the Status Hackathon. While working I observed a few more related pieces and after talking to a few people here, was recommended to post for additional feedback. I am not sure the significance of these findings from a Tokenomic incentives perspective, and would appreciate feedback and validation/invalidation of the underlying ideas.

**The probability distribution of block times is a [Log-Normal Distribution]**([Log-normal distribution - Wikipedia](https://en.wikipedia.org/wiki/Log-normal_distribution))

Most often when dealing with probabilities we see a Normal Distribution. At first thought it is easy to think that BlockTime fits into this as well, but it in fact does not. Logically, it can be seen because you are unable to have a Blocktime of less then zero on one end and on the other a blocktime can be of any length (all though very unlikely to be extremely long). You can also see this in the data. The chart below is distribution of blocktimes over 10,000 blocks starting on Sep-08-2018 12:53:38 PM +UTC

[![image](https://ethresear.ch/uploads/default/original/2X/1/1831c775310d7dd03b27c87c5a249c735a1a0003.png)image600×371 5.84 KB](https://ethresear.ch/uploads/default/1831c775310d7dd03b27c87c5a249c735a1a0003)

** The Difficulty Function Adapts Linearly **

The correction factor in the difficulty adapting equation responds linearly in respect to block time. Why may this be a problem?

** The probability that a blocktime occurs is an exponential function, but the function that responds to changes in blocktime reacts linearly **

If the claims are true the function adapting the difficulty target would under react or over react to changes in block time.

Some possible consequences:

- Oscillations in difficulty and blocktime. Eventually the linear function catches up and explains the stability of blocktimes over large enough periods of time.
- The existence of a “sweet spot” where there is an ideal acceleration or deceleration of Hashrate in order to maximize accumulation of coins over time.

My conclusion is that if we had a difficulty function that adapts to how statistically unlikely a block time is to occur that the blockchain would be more robust and stable against increases and decreases in Hashrate.

Feedback and correction is welcome and preferred. I am not a trained mathematician, just a musician that loves numbers and hopes any of these observations can help.

Cheers,

James

## Replies

**MadeofTin** (2018-10-28):

As a new user I was unable to add in a few other images I would have liked to include.

Here is one where you can see the relation between a log-normal and a normal distribution. It also shows the underlying exponential function.

[![image](https://ethresear.ch/uploads/default/original/2X/6/6b942a300e97e9d0108f3bc0d51a825785c4e21c.png)image629×465 42.9 KB](https://ethresear.ch/uploads/default/6b942a300e97e9d0108f3bc0d51a825785c4e21c)

---

**MadeofTin** (2018-10-28):

As well as equations for difficulty calculation from the yellow paper.

[![image](https://ethresear.ch/uploads/default/original/2X/3/3f72567f1976ca3baf80c2e57436124b2b9d0874.jpeg)image1026×577 70.7 KB](https://ethresear.ch/uploads/default/3f72567f1976ca3baf80c2e57436124b2b9d0874)

---

**MadeofTin** (2018-10-28):

[![image](https://ethresear.ch/uploads/default/original/2X/b/bd29745eeb4f7666cc05daea044cb9f3ab67ab47.jpeg)image675×577 54.9 KB](https://ethresear.ch/uploads/default/bd29745eeb4f7666cc05daea044cb9f3ab67ab47)

---

**vbuterin** (2018-10-28):

Technically, block times should be a Poisson distribution. The reason why they are not is network latency. Hence, instead what I think we’re seeing is the distribution of x+y, where x (latency) is a normal distribution and y (time to mine after seeing the parent block) is a Poisson distribution.

This seems to suggest network latency is somewhere around 3 seconds, which seems to confirm where the ~15-20% uncle rate is coming from.

---

**MadeofTin** (2018-10-28):

Oh, I hadn’t considered the latency of discovery affecting the distribution. This makes a lot more sense as it was difficult to fit it to one such model because it was the combination of two!

Has anyone deployed a local Ethereum instance and mined it with a fixed hash rate? I am curious what the function that models Ethereum’s blocks actually would be without the latency affecting it.

And a followup question, a  [Poisson Distribution](https://en.wikipedia.org/wiki/Poisson_distribution) is also not a linear function. So perhaps is still worth looking at the difficulty adjustment equations to match it more closely?

---

**vbuterin** (2018-10-28):

Ah sorry, I meant Poisson *process*, with an *exponential distribution*. This one: https://en.wikipedia.org/wiki/Exponential_distribution

---

**bharathrao** (2018-10-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Technically, block times should be a Poisson distribution.

This is only for POW, correct? This would change with POS?

---

**technocrypto** (2018-10-28):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> This is only for POW, correct? This would change with POS?

Yes.  Once block producers are known in advance block production is no longer random and will vary only by network latency.

