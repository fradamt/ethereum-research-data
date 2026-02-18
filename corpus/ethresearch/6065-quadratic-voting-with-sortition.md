---
source: ethresearch
topic_id: 6065
title: Quadratic voting with sortition
author: vbuterin
date: "2019-08-31"
category: Economics
tags: []
url: https://ethresear.ch/t/quadratic-voting-with-sortition/6065
views: 14858
likes: 21
posts_count: 13
---

# Quadratic voting with sortition

One of the weaknesses of all voting, including quadratic voting, is that for any large-scale issue each individual’s ability to affect the result is so small, and so the incentive to deeply reflect and understand one’s genuine beliefs about an issue is tiny. For example, consider the US election. The probability that your vote will decide an outcome is currently [between 1 in 1 million and 1 in 30 billion](https://slate.com/news-and-politics/2016/11/here-are-the-chances-your-vote-matters.html), with an [average of 1 in 60 million](http://www.stat.columbia.edu/~gelman/research/published/probdecisive2.pdf). If to you the difference between the two parties for four years is worth $10,000, then your expected value from voting in the election is worth $0.00017. If quadratic voting was used to run the election, we are supposed to believe that people will be willing to spend roughly that amount on voting tokens, and people who care three times strongly really will spend $0.00051 instead, and that people are capable of making such fine-grained value judgements (hmm… is a lottery ticket chance of electing Andrew Yang worth 0.1 penny or 0.2 pennies?).

One possible remedy is [sortition](https://en.wikipedia.org/wiki/Sortition), a form of government where instead of polling everyone, you randomly select a smaller subset (“committee”) of participants. Each participant would then have a larger chance of influencing the result, and so would more easily be able to determine what the value is to them of some level of influence on the result, because the influence of each person in the committee would be large enough to notice and reason about on a human scale.

This writeup proposes a combination of sortition with quadratic voting, combining the benefits of quadratic voting and its ability to take into account the strength of preferences with the incentive-concentration benefits of sortition.

### Quick quadratic voting overview

In quadratic voting there is a set of participants p_1, \ldots, p_N where participant p_i can make a vote of weight w for a given option on any given issue by paying a cost C(w) = \frac{w^2}{2}. On any issue, the option with the most total *vote weight* wins.

[![QV1](https://ethresear.ch/uploads/default/original/2X/c/c79bccef59eada2294f75e4fad8cb3f5d81e76db.png)QV1541×331 11.4 KB](https://ethresear.ch/uploads/default/c79bccef59eada2294f75e4fad8cb3f5d81e76db)

Here is why quadratic voting is so cool. We can model voters as having a “strength of preference” x, which denotes the amount they are willing to pay for one unit of influence (ie. increasing the weight of their vote by one) on a given issue. A voter with strength of preference x will be willing to continue increasing their weight until the marginal cost of increasing the weight by one unit (ie. the derivative C'(w) = w) exceeds x. Hence, a voter with preference strength x will make a vote of weight x, and so by selecting the option with the highest total weight, the mechanism optimally selects the option with the highest combined strength of its supporters’ preferences. The key realization here is how the cost function C(w) = \frac{w^2}{2} and its derivative c(w) = w naturally incentive-align voters to make a vote whose weight is proportional to how strongly they feel about an issue.

This is better than standard voting, which does not take into account differing strengths of preferences, and is better than fixed-cost-per-vote vote buying, where voters with stronger preferences (or more money) too easily run roughshod over everyone else.

Now, we will try to make modifications of this to add an element of sortition.

### Strawman scheme 1

Randomly select portion p of the population. These selected voters have the right to participate in the quadratic vote, and make a vote of weight w with a marginal-cost function c(w) = \frac{w}{p} (remember lowercase c(w) is the *marginal cost*, the cost of increasing w by an additional unit; C(w) here would be \frac{w^2}{2p}). Everyone else cannot participate.

If you assume that the size of the voter pool is very large, then this modified mechanism will lead to the same result as standard QV: a particular voter with preference strength x will with probability p be able to vote and they will keep voting until c(w) = x, meaning they will make a vote of strength \frac{x}{p}, and with probability 1-p the voter will not be able to do anything. Hence the voter’s expected influence is p * \frac{x}{p} = x.

The main flaw of the scheme is that it does not distinguish between issues are large-scale enough to need sortition (applying sortition to small-scale issues risks adding too much random noise), and particularly it does not deal well with issues where some participants have a really strong position and other participants care little; in those cases, it either applies too much noise to the former, or does not provide sufficient concentration of incentive for the latter.

For a motivating example, consider cases like zoning, where there is typically a concentrated interest (someone looking to build a certain type of property) and an often countervailing diffuse interest (local residents who want to keep their neighborhood a certain way) and it’s not a-priori clear which side should win. We want to make sure the concentrated interest can always express itself but use sortition to amplify the clarity of the diffuse interest.

### Scheme 2

We create two voting opportunities. The first voting opportunity allows anyone to buy votes at marginal cost c(w) = M + w for some global constant M (so total cost C(w) = M * w + \frac{w^2}{2}). The second voting opportunity randomly selects portion p of the population, and allows only them to buy votes at cost c(w) = \frac{w}{p} up to a maximum weight of \frac{M}{p}. Note that a selected voter can participate in both voting opportunities.

[![QV2](https://ethresear.ch/uploads/default/original/2X/b/b74396a0e20cdf7dd8705743f6b16afd1062c252.png)QV2771×402 9.33 KB](https://ethresear.ch/uploads/default/b74396a0e20cdf7dd8705743f6b16afd1062c252)

Now, let’s analyze a voter’s expected influence. With probability p, a voter is “selected”, and in the second voting opportunity they will make a vote of weight \frac{\min(x, M)}{p}; if a voter is not selected they will not vote. In the first voting opportunity, everyone will make a vote of weight \max(x - M, 0). Now, we add these two in-expectation, and we get

p * \frac{\min(x, M)}{p} + \max(x - M, 0) = \min(x, M) + \max(x - M, 0) = x

So this mechanism still gives equivalent results to standard QV in-expectation, and it has the desired property of providing a consistent guarantee of input to strong-preference participants while using sortition to create a portion p of weak-preference participants that have their power amplified by a factor of \frac{1}{p}. But this scheme still feels hacky: you need to agree on both a threshold and a sortition factor for every issue, and it doesn’t seem able to adjust to different levels of preference strength on a finer scale.

### Scheme 3

What if instead, we create an infinite sum of schemes of the type presented before, with roughly the following property: above some threshold M, all participants’s votes are counted determinstically, but at level \frac{M}{2} we randomly select half the participants and double their power, at level \frac{M}{50} we select one-fiftieth of participants and 50-tuple their power, etc. This way, the set of participants at any level of preference strength (below the threshold M) that are able to vote have their power amplified to the same level, and so have the same level of incentive to consider the issue well.

Here is the scheme. For each participant, we assign them a uniformly-distributed random value q \in [0, 1]. We give them the ability to vote with a cost function C(w) = M^2 * q * e^{({\frac{w}{M}})} - M * q, so c(w) = M * q * e^{(\frac{w}{M})}. Voters are only able to increase their voting weight up to the point where c(w) = M and no further.

We then as in scheme 2 open a separate voting opportunity to let anyone buy votes at cost c(w) = M + w.

[![QV3(1)(1)](https://ethresear.ch/uploads/default/optimized/2X/7/7e9bc0723bf135adbd72e1dc79c8edaa159dcb28_2_690x314.png)QV3(1)(1)771×351 22.5 KB](https://ethresear.ch/uploads/default/7e9bc0723bf135adbd72e1dc79c8edaa159dcb28)

The curve e^{(\frac{w}{M})} has the nice property that scaling it vertically is the same thing as left-shifting it. Hence, instead of treating the multiplication by q as a multiplication, we’ll treat it as voters with lower q values being able to vote along the same c(w) = M * e^{(\frac{w}{M})} curve but *starting further left on the curve*, where their votes are cheaper and so their power is amplified. Specifically, a voter with preference strength x and value q will buy votes along the curve starting at ln(q) * M (where y = q * M) and ending at ln(\frac{x}{M}) * M (where y = x * M and y' = x).

We can compute the expected vote weight of a voter with preference strength x < M as an integral over q from 0 to \frac{x}{M} (because when q > \frac{x}{M} they won’t vote at all). We cover the M = 1 case first for simplicity of exposition:

\int_{q=0}^x [\ln(x) - \ln(q)] = x * \ln(x) - (x * \ln(x) - x) = x

And adding back M:

\int_{q=0}^\frac{x}{M} \left[M*\ln\left(\frac{x}{M}\right) - M*\ln(q)\right] = M * \frac{x}{M} * \ln\left(\frac{x}{M}\right) - M * \left(\frac{x}{M} * \ln\left(\frac{x}{M}\right) - \frac{x}{M}\right) = x

A voter with preference strength x > M will behave as a preference-strength M voter in the first vote, and will make a vote of weight x - M in the second vote as before. Hence, a voter with preference strength x will in-expectation make total votes of weight x.

Also, note that a voter with preference strength x < M, conditional on that voter making nonzero votes, will face q \in [0, \frac{x}{M}] with average q = \frac{x}{2M}, so their average voting weight will be \ln(\frac{x}{M}) * M  - \ln(\frac{x}{2M}) * M = \ln(2) * M, so we get the interesting property that any voter below the threshold, conditional on them being able to vote at all, will on average make votes with about the same level of impact.

### Further work

- Determine if other sortition functions make more sense
- Come up with principled ways of determining M
- Extend this scheme to quadratic funding (is it as simple as sending the project \sum_i w_i^2?)

For (1), note two ways of describing the problem:

- Give every voter a random uniform-distributed q \in [0,1], and define a set of  functions c_q(w) which has the property that \int_{q=0}^1 c^{-1}_q(y) = y where c^{-1}_q is the inverse function of c_q; this follows from the fact that c^{-1}_q(y) = w determines how the weight a voter would vote with if they had preference strength y and a random value q
- All voters can vote using a cost function C(w), but starting from different points (ie. so an individual’s cost function would be C(w) - C(w_i) for some w_i), with the property that if c(w_*) = p (always p \le 1) then the probability any given voter has w_i < w_* is equal to p. Consider different choices for C and how to calculate w_i from q \in [0,1] to be consistent with the criterion.

## Replies

**richardswitzer** (2019-09-02):

You could also employ quadratic voting to determine the sortition, as opposed to random selection. That provides some filtering that the participants of the sortition are people a population wants to speak for them, community leaders and ‘trusted’ citizens. I know this sounds like the electoral college, but the sortition would be unpaid, temporary and micro enough that it would be very difficult to use the position to your advantage. I suspect this would also produce a sortition that had a generally more informed opinion on the issues (how generally left or right shouldn’t change much, as sortitions would be hyperlocal), and might reduce the influence of voters whose worldview is determined by their Facebook feed.

---

**thibauld** (2019-09-02):

Interesting! I did not know the word “sortition” but it reminds me a little bit of what we did with [LaPrimaire.org](http://LaPrimaire.org). To make it short, LaPrimaire was an experiment aimed at organizing at 100% democratic and transparent primary to elect the most representative candidate for the french presidential election of 2017.

For context, the thesis behind LaPrimaire was the following:

- The main issue with elections is that citizens have no say in who gets to be a candidate. Candidates are either imposed by political parties or, when primaries are organized, everything is done to limit and exclude candidates (either through “internal rules”, or money or you-name-it…).
- What if we create an open, democratic (in the pure sense of the term, not in the “democratic vs republican” sense) and transparent primary to let citizens decide who should run and create a popular momentum around him or her (actually it was “her”!)?

The rules were simple:

- The election process is elaborated, frozen and publicly shared in advance for everyone to understand the rules that will apply to all.
- Anybody who can legally be elected can run.
- The organizers of LaPrimaire have (i) no influence power whatsoever over the process (ii) cannot be candidates and (iii) have a strong obligation of strict neutrality towards candidates.

To be able to run, you needed to first gather the support of 500 unique citizens (I won’t detail here how we did to prevent sybil attacks, it was definitely not perfect but it did work). There was no limit in the number of candidates allowed to run, which means we had no idea how many candidates would make it and we needed to plan the election accordingly.

My point is: your article overlaps in some ways with a problem we had to solve, which was: “*How to hold a democratic elections when candidates are too may?*” and I wanted to share that in the hope it might give you more cool ideas.

How we solved it:

Let’s say we had 100 candidates. You can’t expect all citizens to make vote for all 100 or make an informed decision to chose 1 among those 100 candidates. So what we did is we created random lots of 5 candidates and citizens had to vote (using [majority judgement](https://www.opendemocracy.net/en/what-does-brexit-mean-majority-judgment-can-solve-puzzle/) , meaning they **had to** evaluate each of the 5 candidates using one of the following mention: `[very good | good | fair | below average | bad]`) on their randomly allocated lot of 5 candidates, no more, no less.

The creation of the lots was not 100% random but was using a weighted random algorithm to give candidates the guarantee that they would be show to the same number of voters (minus a tiny delta).

This worked great ([results are here](https://articles.laprimaire.org/r%C3%A9sultats-du-1er-tour-de-laprimaire-org-c8fe612b64cb) for those interested)! First, it was making a candidate’s initial popularity much less useful as he could not just rally his supporters to go vote for him. Many voters really like the process and, obviously some hated it as well. Those who loved it liked the fact that it was “peaceful”: they had 5 candidates and could read about them (videos, interviews etc…) and give their honest opinion on the 5. Those who hated it said they were not able to evaluate their candidate of choice (fair point, but that’s by design).

But the main thing was, for citizens to trust us, we needed to prove that by doing like this, we would get results equivalent as if everyone had been able to vote for every candidate. And that what we did in [this (draft) paper](http://thibauld.com/paper.pdf). For a given number of candidates, we were able to calculate the required number of voters so that the results would be statistically acceptable.

The very simple algorithm used to create the random lots was definitely not the most efficient one (in the sense that it required a very high citizens/candidate ratio) but we thought that it would have been hard to convince citizens that an algorithm would have been better at choosing the most relevant candidates. So in the end, we decided that all candidates should get the same exposure even though, clearly, some candidates could have been quickly discarded had we use some type of A/B testing algorithm.

Just wanted to share this to (hopefully) positively contribute to the discussion.

---

**vbuterin** (2019-09-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/thibauld/48/2374_2.png) thibauld:

> How we solved it:
> Let’s say we had 100 candidates. You can’t expect all citizens to make vote for all 100 or make an informed decision to chose 1 among those 100 candidates. So what we did is we created random lots of 5 candidates and citizens had to vote (using majority judgement  , meaning they had to evaluate each of the 5 candidates using one of the following mention: [very good | good | fair | below average | bad] ) on their randomly allocated lot of 5 candidates, no more, no less.

Yep, this is a great use of sortition! Glad to hear it was already used and worked well in such a large-scale trial.

> The creation of the lots was not 100% random but was using a weighted random algorithm to give candidates the guarantee that they would be show to the same number of voters (minus a tiny delta).

You should use our [shuffling algorithm](https://notes.ethereum.org/@vbuterin/rkhCgQteN?type=view#Shuffling) ([spec](https://github.com/ethereum/eth2.0-specs/blob/5f1cdc4acca1bb3235efdc5b63dbf9c74c4c312e/specs/core/0_beacon-chain.md))! It’s a cryptographically fair permutation, so it can ensure that everyone on one side is matched to the same number of people on the other side.

---

**ghasshee** (2019-09-02):

It seems such an interesting research that there is the [Japanese Version](https://ghassheee.github.io/ethereum/2019-09-02-quadratic-vote.md/).

---

**tchitra** (2019-09-02):

Nice idea! Quick nit: For the marginal cost c(w) = w + M in scheme 2, C(w) = \int c(w) \mathrm{d}w = \frac{w^2}{2} + Mw as opposed to \frac{w(M+w)}{2} (as written above). You probably want c(w) = w + \frac{M}{2} to be consistent?

---

**vbuterin** (2019-09-02):

Yep you’re right! Fixed.

---

**mohsenghajar** (2019-09-05):

Sortition basically makes it function like a republic: instead of people voting for issues, they vote (truly randomly vs currently which is still random but with some non-uniform distribution) for people who are supposed to vote on issues.  Right?

---

**kladkogex** (2019-09-05):

Arguably Court Jury is the most widely used form of sortition which forces a small random group of people to analyze  issue for a  long time.

The best way to elect a president is probably randomly select 100 people and have them personally interact with the candidates.

---

**tasd** (2019-12-19):

Another way of dealing with the lack of incentive for voters to deeply study every issue is liquid democracy.  Do you see a way to combine that with QV?

A simplistic way might be to let voters quadratically assign their votes to different delegates for different topics – for example, I may assign 50% of my vote tokens to my delegate on tax policy, and 5% to my delegate on agricultural policy, which would be applied quadratically.  But this approach seems to have many flaws.

What do you see as the pros/cons of sortition vs liquid democracy with QV?

---

**Chxpz** (2020-01-09):

Brilliant! But why is that necessary to elect representatives, such as presidents or deputies? I mean, this idea of quadratic voting with sortition process might be a solution for a group of people to come up with a resolution for a issue that needed to be voted, however having the main focus for the development strictly on the election of representatives is waste of possibilities.

Optimization in election processes might relevant for developed countries, but it could not fit well for other developing countries (e.g. South America - Brazil, Argentina, etc), where we have historic problems related to governance and bribery schemes. Improve the way representatives are elected (although is excellent idea) is just like a crutch for issue,

The idea you propose here might be used for citizens (in case of political use) to decide about matters straight way without the participation of any unnecessary third party. It is not a matter of shut down the State or any proposal of revolution, it is just a way to correct severe problems in countries where law have not been enough to mitigate crimes related to bad administration, bribery and so on.

Please, consider this in the next developments stages.

---

**blainehansen** (2020-09-21):

A while ago I wrote up a little idea about making voting “persistent” instead of event-based, and it seems like it might address this problem as well? I don’t have a mathematical justification, but since preferences can be adjusted at any time, people would only tend to participate in decisions in which they had strong incentives/preferences. Since that idea could scale so nicely, it would allow many more much more granular decisions to be made democratically, creating a sort of “sortition by concern” where each issue/position had a relatively small number of people weighing on it.


      [blainehansen.me – 2 Mar 20](https://blainehansen.me/post/persistent-voting/)


    ![image]()

###

We all implicitly assume that elections are events that begin and end. What happens if we get rid of that assumption?

---

**theothersteven** (2022-04-28):

In scheme 1, shouldn’t the marginal cost function be `c(w) = pw` not `c(w)=w/p`?

That way when a voters preference is `x`, his voting power would be the `w` value that equates `c(w) = x`, which is `x/p`.

