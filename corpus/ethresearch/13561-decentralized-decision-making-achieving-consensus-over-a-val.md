---
source: ethresearch
topic_id: 13561
title: "Decentralized decision making: achieving consensus over a value"
author: kakia89
date: "2022-09-02"
category: Applications
tags: []
url: https://ethresear.ch/t/decentralized-decision-making-achieving-consensus-over-a-value/13561
views: 2339
likes: 2
posts_count: 13
---

# Decentralized decision making: achieving consensus over a value

Suppose we want to find a true state/value over a normalized interval [0,1]. A few examples are disputing parties trying to share a fixed amount, single parameter of a system: emergency, security, efficiency, etc.

One way to find this value is to delegate to a committee of jurors/experts who try to acquire information about the true state and report it. The question is how to derive the final outcome. Note that choosing the average of reported values is not a good idea, as it suffers from two issues, as the average directly depends on all reported values. First, if the jurors have preferences, they may shift their report to improve the outcome. Second, if some of the jurors are corrupted, they may increase/decrease their report in favor of the corrupter.

A more robust function of reports is the median. If the jurors have (single peaked) preferences, then reporting true valuation is optimal no matter what others do. Also, corrupting a few jurors won’t affect the outcome.

Now suppose that jurors do not have any preferences and all they care about is rewards. My proposal is to choose the median as a final outcome and reward the jurors depending on the distance between their reported value and the median. The reward is decreasing in the distance and in total, they make a fixed amount --budget for the procedure. Assuming the jurors can not talk to each other and collude, the idea of why such a procedure should work is the following. The only thing jurors can do is find out more about the true state of the world, to be closer to other jurors who do the same. Therefore, even if acquiring information about the true state of the world is costly, the jurors will do so because of rewards. The optimal size of the committee and exact reward function depends on these costs and is left for research. Are there any pitfalls or obvious attacks to this approach?

## Replies

**alexnezlobin** (2022-09-05):

This sounds very much like a Keynesian Beauty Contest.

---

**kakia89** (2022-09-05):

Thank you for the comment. It indeed sounds like a Keynesian Beauty Contest (KBC). One difference I am thinking of is in the assumption of the existence of the ground truth, while the way I remember KBC assumes there is no such truth (or it is irrelevant) and the value/winner is determined solely by beliefs about others. My assumption makes sure that acquiring information is the only way of getting close to what others think the truth is. I would be very interested to see if there are any working incentive mechanisms around KBC. I am only aware of project Kleros, where the jurors vote for one of the alternatives (similar to KBC in that it has a finite number – mostly 2 – of alternatives) but haven’t seen anything that chooses the outcome on a continuum interval.

---

**domothy** (2022-09-05):

It seems you are describing the concept behind SchellingCoin:


      ![](https://ethresear.ch/uploads/default/optimized/2X/1/134c969f80984ce094b03aa89723aa5c98c7bcf1_2_500x500.png)

      [Ethereum Foundation Blog](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed)



    ![](https://ethresear.ch/uploads/default/optimized/2X/2/29e9efc91b5b9eb80f7b906e630b72a72947f845_2_690x295.jpeg)

###

---

**MicahZoltu** (2022-09-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/kakia89/48/5646_2.png) kakia89:

> while the way I remember KBC assumes there is no such truth (or it is irrelevant) and the value/winner is determined solely by beliefs about others

Even if there is a clear schelling point, you can still have a KBC.  A KBC is essentially just a “voting” system where the winning vote is defined (after the fact) as the truth, and it doesn’t actually have any constraints that require it to align with reality.

While a KBC where collusion is impossible is expected to resolve to the most obvious schelling point (e.g., truth), if collusion is possible then this property may not hold.  If trustless collusion is possible, or a single voter can decide the vote on their own, then the schelling point may actually be *less likely* than the truth if you can make money off of causing the oracle to fail.

---

**kakia89** (2022-09-05):

Thank you. It is certainly related. However, I would not focus on jurors’ beliefs about what others think in the analysis of the equilibrium point, but rather on costly information acquisition and then aggregation, because I see it as the only way to coordinate. That is, instead of jurors starting to form beliefs about others’ beliefs, they start to read the issue at hand and try to find the right value, hoping that others also do so, i.e., they invest in finding the truth.

---

**llllvvuu** (2022-09-06):

This is all very reminiscent of old Vitalik posts on [Schelling coin](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed), [P + epsilon attack](https://blog.ethereum.org/2015/01/28/p-epsilon-attack), and [subjectivity/forking](https://blog.ethereum.org/2015/02/14/subjectivity-exploitability-tradeoff). When the colluding party selects the wrong value, people burn tokens on this fork to create a new fork where they take the colluding parties’ tokens.

I believe Augur rolled with this model. UMA went with something more lightweight IIRC?

---

**kakia89** (2022-09-16):

Original proposal is certainly related to Shelling points, Keynesian Beauty Contest, and suggested projects that implement price oracles. However, I have a simpler setting in mind. In this setting, there are no multiple sources of information, unlike in case of price oracles where there are many of them and price is obtained by aggregation through these sources. In a simple setting with single source of information, the truth is obtained by spending efforts to acquire more information. That is, if the jurors can not collude, the only way to be close to median is to acquire costly information. Rewards need to compensate for this efforts, so that in the equilibrium state, the median itself is sufficiently close to the truth. Regarding more than one source of information: as long as majority of jurors acquire information from the same source, the median will be close enough to the truth. This adds to the robustness of the median.

---

**MicahZoltu** (2022-09-17):

![](https://ethresear.ch/user_avatar/ethresear.ch/kakia89/48/5646_2.png) kakia89:

> if the jurors can not collude

How do you intend to prevent collusion?

More characters to meet Discourse minimum character requirement.

---

**kakia89** (2022-09-17):

One way of avoiding collusion is to have a large pool of jurors and choose a subset at random. The chosen ones should not be able to prove that they are members. There are similar protocols to this, e.g., random sample voting, where all voters look alike but a majority of them are decoys.

---

**MicahZoltu** (2022-09-17):

How would you make it so a voter can know that they are part of the set but not be able to prove they are part of the set?  Also, this doesn’t actually prevent collusion, it just makes it trusted (which is good, but not necessarily sufficient).  If a single actor is 50% of the voting set then the “voters” here would implicitly trust each other (since they are all the same actor) and could then resolve the market however they like and profit off of it (even if it resolves incorrectly).

---

**kakia89** (2022-09-17):

Let’s say anyone can request a decoy vote, which is indistinguishable from the real vote (e.g., some password that works in the system, but the report through this password is ignored). In this case, anyone can claim they have a vote and there is no way to prove that one didn’t ask for a decoy vote. The real voters know that they were chosen because they did not ask for the vote, they just received it, but they can’t prove it to others. There might be more efficient ways to mitigate collusion and vote buying, this is just one of them.

---

**MicahZoltu** (2022-09-18):

Generally speaking, with ZK proofs you can prove just about anything, including that you voted a certain way.  There are techniques to raise the complexity of generating such a proof (like you have described) but ultimately there will be ways around it.

This doesn’t address the fundamental issue though, which is that a single actor could just control 50% of votes and can resolve the system any way they want.

