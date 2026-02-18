---
source: ethresearch
topic_id: 6855
title: Negative votes in quadratic funding
author: vbuterin
date: "2020-01-30"
category: Economics
tags: [quadratic-funding]
url: https://ethresear.ch/t/negative-votes-in-quadratic-funding/6855
views: 4169
likes: 8
posts_count: 6
---

# Negative votes in quadratic funding

After my [review of Gitcoin Grants round 4](https://vitalik.ca/general/2020/01/28/round4.html) yesterday, there have been many questions asking what exactly it would mean to add negative contributions to quadratic funding, and how this would work. The purpose of this post is to provide a mathematically principled explanation of why negative contributions are a natural extension to quadratic funding, and in what way.

### Quadratic voting

First, let us start with the granddaddy of quadratic decision protocols, quadratic voting. Quadratic voting is a voting mechanism where you can make n votes for or against a candidate at a cost n^2; the cost could be in dollars or in specially designated “voting tokens” that each person is assigned the same amount of (see [here](https://vitalik.ca/general/2019/12/07/quadratic.html) and [here](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2003531) for background on why this is a good idea).

Consider a quadratic vote in a case where there are more than two candidates, let’s say for example five; we’ll call them A B C D E. Suppose that you want to express the opinion “I think candidate A deserves one less vote”. There are actually two ways to do it:

1. Vote (-1, 0, 0, 0, 0)
2. Vote ( 0, 1, 1, 1, 1)

Notice how (1) and (2) have the exact same effect; they both push A one unit behind the other four candidates. However, in terms of voting tokens cost, (1) is much more economical than (2): (1) costs you 1 token, whereas (2) costs you 1^2 + 1^2 + 1^2 + 1^2 = 4 tokens. Hence, any negative vote can be simulated by positive votes, but doing so is much more costly. And if the voter wanted to spend a *fixed* budget (say, four tokens) on opposing A, then by doing (2) they would push A one unit back, but by doing a scaled-up version of (1) that costs four tokens, that is `(-2, 0, 0, 0, 0)` they could push A *two* units back.

Technically, the optimum is `(-0.8, 0.2, 0.2, 0.2, 0.2)` which costs (-0.8)^2 + 0.2^2 + 0.2^2 + 0.2^2 + 0.2^2 = 0.8 tokens to push A one unit back, or we can do `(-1.788, 0.447, 0.447, 0.447, 0.447)` which pushes A \sqrt{5} \approx 2.236 units back at a cost of four tokens. But it’s clear that if you had to make the binary choice between opposing-by-opposing and opposing-by-supporting-everyone-else, the former is vastly more efficient, and so a quadratic *voting* system that only allowed opposing-by-supporting-everyone-else would not give fair representation to negative signals.

### Quadratic funding

As I described in [my article on QV/QF](https://vitalik.ca/general/2019/12/07/quadratic.html), quadratic funding can be viewed as a form of quadratic voting. When you donate $x to a project, you are actually making \sqrt{x} votes in favor of a resolution that moves money from a central pool to that project. How much money? An amount of money equal to the amount that the central pool would have to spend to individually counteract everyone’s vote for the resolution with a single vote against. If two people donate $x and $y, then their combined votes are \sqrt{x} + \sqrt{y}, and the total donation would be (\sqrt{x} + \sqrt{y})^2 - exactly the cost of making \sqrt{x} + \sqrt{y} countervailing votes against.

So now it becomes natural to ask: why not allow people to make votes against? Much like in regular QV, where you can spend x to make \sqrt{x} votes in favor of a motion or to make \sqrt{x} votes against a motion, here too we could allow anyone who contributes x the choice to determine whether this should be treated as a positive signal or a negative signal. For example, if three people contribute $x, $y and $z, but the third participant is making a vote against, the total amount received by the project would be (\sqrt{x} + \sqrt{y} - \sqrt{z})^2. Every voter chooses whether their square root carries a plus sign or a minus sign. If the total sum is negative, then the grant fails outright and the amount received by the project is zero.

Note that the argument for allowing explicit downvoting, and not just downvoting-by-supporting-everyone-else, is the same as before. Spreading your vote among N projects would decrease the strength of each vote by a factor of \approx\sqrt{N} for the same reasons as before, and it certainly adds an imbalance to penalize negative opinions to such a large extent.

### Pairwise-bounded quadratic funding

In the case of *[pairwise-bounded QF](https://ethresear.ch/t/pairwise-coordination-subsidies-a-new-quadratic-funding-design/5553)*, we unpack the square-of-sum-of-square-roots into a matrix and look at each pair of contributors separately:

[![](https://ethresear.ch/uploads/default/original/2X/f/f4c8832d958643c849de60b387634a2584db8b70.png)651×471 7.65 KB](https://ethresear.ch/uploads/default/f4c8832d958643c849de60b387634a2584db8b70)

In the case of negative contributions, we can look at this as follows (showing only a single positive contributor and a single negative contributor for simplicity):

[![Untitled Diagram](https://ethresear.ch/uploads/default/original/2X/e/e2e060783c85d4c5dc6594a673d0e0ed5da08cde.png)Untitled Diagram336×381 2.17 KB](https://ethresear.ch/uploads/default/e2e060783c85d4c5dc6594a673d0e0ed5da08cde)

However, there is a problem. In pairwise-bounded QF, every pair has a separate matching coefficient. It’s conceivably possible that there is a set S_1 of contributors who all vote for a project, a set S_2 who all vote against a project, where the matching coefficients *between* members of S_1 and members of S_2 are all low (because eg. there are N other projects where each project received a large donation from a member of S_1 and from a member of S_2), but matching coefficient between members *within* S_2 are high. Then, the *positive* matches M_{i,j} =  (-\sqrt{c_i}) * (-\sqrt{c_j}) (where i,j \in S_2) would exceed the negative matches M_{i,k} = (-\sqrt{c_i}) * (+\sqrt{c_k}) where k \in S_1, and so a set of negative matches could *increase* the total!

I see two solutions to this:

1. Force the product of two negative numbers to zero (note that this includes the squares on the diagonal)
2. Separately compute the total subsidy considering only positive contributions (call this s_+) and the total subsidy considering only negative contributions as though they were positive contributions (call this s_-). The final subsidy would be (\sqrt{s_+} - \sqrt{s_-})^2

I prefer the second; particularly, note that in the case where all correlation coefficients are identical it returns the result that you get from the basic quadratic matching formula.

When a negative contribution reduces the total match from a project, where do the funds go? Simple: they get proportionately redistributed to other projects.

### Other concerns

There are other reasons to potentially avoid allowing negative votes; that it “creates bad vibes” is the most common criticism. It’s certainly possible that on net this makes allowing negative votes a bad idea. At the very least, it seems reasonable to work harder to make negative votes anonymous. This is all out of scope for this post, which focuses on the math.

## Replies

**jpitts** (2020-01-30):

Why would negative contributions be treated as a sort of opposing force to positive contributions per project? A better approach may be to start with what the incorporation of negative feedback is attempting to accomplish, and then construct a viable “social design” for incorporating this into CLR from principles.

The Round 4 [CLR](https://medium.com/gitcoin/experiments-with-liberal-radicalism-ad68e02efd4) system enabled quadratic funding w/ matching for a set of projects, but did not facilitate community feedback to specify preferences such as “against”. In traditional political systems and user interfaces, preferences against an option often use a very different approach than preferences for. For example, in courts the opposing attorney can interrupt proceedings with an objection based on certain criteria.



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Objection_(United_States_law)#List_of_objections)





###

Proper reasons for objecting to a question asked to a witness include:
 1.Ambiguous, confusing, misleading, vague, unintelligible: the question is not clear and precise enough for the witness to properly answer. |
 2.Arguing the law: counsel is instructing the jury on the law. |
 3.Argumentative: the question makes an argument rather than asking a question. |
 4.Asked and answered: when the same attorney continues to ask the same question and they have already received an answer. Usually seen aft...










In this case of CLR, perhaps the other feedback that is incorporated (negative or otherwise) can take on the form of a QV at certain time windows, the results triggering certain properties affecting the outcomes. Properties might include bonuses, penalties, even disqualification.

This creates a control system around the CLR, bringing ideas from control theory to liberal radicalism.



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Control_system)





###

 A control system manages, commands, directs, or regulates the behavior of other devices or systems using control loops. It can range from a single home heating controller using a thermostat controlling a domestic boiler to large industrial control systems which are used for controlling processes or machines. The control systems are designed via control engineering process.
 For continuously modulated control, a feedback controller is used to automatically control a process or operation.   The c...

---

**vbuterin** (2020-01-30):

> In traditional political systems and user interfaces, preferences against an option often use a very different approach than preferences for.

I wonder why this is the case. At first glance there is certainly no *mathematical* reason to do such a thing, and it seems very plausible that the idea that zero is some kind of special pivot point is just a psychological bias. And in market-like systems, a less prominent zero pivot (eg. ease of shorting) is typically considered a sign of *more efficiency*.

Perhaps we’ll learn from doing a round of the experiment.

---

**jpitts** (2020-01-31):

Seeing CLR as a series of experiments is exactly the right approach, and will lead to a much better design in the long run!

One reason for the asymmetry may be “negativity bias” in users. This is the idea from psychology research and behavorial finance that events or notions that are perceived as negative have greater salience in the mind (among other interesting properties).

One really funny property is that the negative thing has more complexity in the mind than the positive thing. Another is that the negative thing increases more in its perceived negativity as the outcome approaches, vs. the positive thing.

*I don’t know how researchers measure these properties, and of course take it with a grain of salt.*

The abstract from the classic paper “Negativity Bias, Negativity Dominance, and Contagion” on this effect is here:

https://journals.sagepub.com/doi/abs/10.1207/S15327957PSPR0504_2?journalCode=psra

Negativity bias effects show up all over the place: elections (e.g. disapproval voting), social media phenomena (sharing rate of negative stories is higher), and in service design (e.g. how people report problems to authorities).

---

**vbuterin** (2020-02-01):

There’s also anti-negativity biases, eg. average ratings typically quickly climb to near-100%. Definitely a valuable point that this is something that may need to be designed around!

---

**jpitts** (2020-02-01):

Yes, this one you’re referring to is probably “social influence bias”, in which initial positive inputs like ratings / stars / upvotes lead to subsequent positive inputs, and reinforcement. Initial negative ratings do not have the same kind of amplification. Restaurants suddenly become 5-star places with lines, meanwhile the same kind of place across the street can’t get a break.



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Social_influence_bias)





###

 The social influence bias is an asymmetric herding effect on online social media platforms which makes users overcompensate for negative ratings but amplify positive ones. Driven by the desire to be accepted within a specific group, it surrounds the idea that people alter certain behaviors to be like those of the people within a group. Therefore, it is a subgroup term for various types of cognitive biases. Some social influence bias types include the bandwagon effect, authority bias, groupthin










I wonder how this effect relates to witch-hunting / scapegoating / moral panics, which involve a negative value but seem to take on a similar amplification of value assignment.

There is the potential for witch-hunting effects to impact negative votes. Similar to the case you brought up in your CLR Round 4 retrospective, the nature of a particular project can be seen as a violation of the moral/ethical status quo or expectation, leading to a sudden buildup of negative votes submitted.

The information needs to be incorporated, but extreme effects stemming from biases “designed around”.

