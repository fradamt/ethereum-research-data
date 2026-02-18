---
source: ethresearch
topic_id: 5214
title: Forking in effort-intensive Schelling game systems
author: whwgeorge
date: "2019-03-26"
category: Economics
tags: [schelling-game]
url: https://ethresear.ch/t/forking-in-effort-intensive-schelling-game-systems/5214
views: 2308
likes: 1
posts_count: 8
---

# Forking in effort-intensive Schelling game systems

Goal:

This post is an idea for how to handle forking in Schelling point based systems. One should compare it to the forking system of Augur (see Section 9 of their whitepaper); however, this proposal will be adapted to a generality/context that is not present in Augur.

Specifically, we still have the general Schelling game framework where one is rewarded for voting coherently with the majority and penalized for voting incoherently, with the idea that if we ask questions about the real world, the “truth” will often be a Schelling point. However, we attempt to adapt to the situation when the questions we ask might be hard. Namely, we expect 1) reviewing a given case to take a non-trivial amount of effort, and 2) honest parties will arrive at the “wrong answer” - i.e. an answer other than that which would ultimately selected by an honest majority - some non-trivial percentage of the time. (This idea was conceived for use in Kleros, which attempts to be a fairly general dispute resolution platform. In real world disputes there will be situations where honest people will disagree sometimes. Compared to a Schelling point based oracle that is used to handle more objective questions, honest participants in a Kleros-type system are likely to have more variability in their returns, but that should be okay as long this averages over the long term. As it can take a lot of effort to review a case, we have a generally small, discrete number of token holders who are drawn to vote on each case, with the possibility of appeals, to minimize duplication of effort.) Recall that block producing can be [thought of as a sort of Schelling game](https://blog.ethereum.org/2014/03/28/schellingcoin-a-minimal-trust-universal-data-feed/) where people are voting on rival blocks/the order of transactions, so there may conceivably be some applicability of these ideas to forking in consensus algorithms, but I haven’t thought much about that angle.

tl;dr:

When considering which fork they would want to wind up on, token holders may consider both the outcomes of the case associated with the two sides of the fork but also the percentage of the community that goes with each fork. To find the largest fork that is compatible with users’ cutoffs for not being willing to “go it alone”, one can use a sort of auction system.

Context:

The fact that cases can require a significant amount of effort to evaluate probably implies that a system such as the one Vitalik discusses [here](https://ethresear.ch/t/cryptoeconomic-oracles/1050/2) is not viable in our setting. The idea is that every decision results in a fork and a DEX could be used to determine which fork has the highest market value, taking that as the “true value” for the purposes of a smart contract using the result. While such a system shouldn’t require participants to reevaluate *every* case because usually only one outcome of any given case will give forks that have non-negligible value after a certain time, this system would probably nevertheless require all active market participants to evaluate most of the *recent* cases, which will likely already be a significant duplication of effort.

We want a forking mechanism that both:

1. facilitates an honest minority forking out an attacker’s holdings in situations where there is a 51% attack (or indeed one might also want a fork in case of some kind of ideological split such as the literalist/spirit of the rules kind of split that one might have seen with the Augur “who will control the US house after the midterms”; market if it had gone on long enough to force a fork).
2. while still allowing for the possibility of cases where, potentially after a long process of appeals, there is not a consensus among honest parties on which side should win. Then, a ruling should be made one way or the other, but if token holders recognize that there is not a need to split the community over this case, then such a split shouldn’t occur involuntarily. (An important note here is that we image that, absent eventual forks, only a percentage of a given voter’s tokens would generally be staked on the outcome of any given case. So, if there is no fork, a voter that is incoherent with a given case would still typically have tokens/be “part of the community”.)

We imagine that a given token holder’s utility for a given case with a potential fork as a function: utility=fct(case outcome, percentage of tokens that are on the same fork as me after the case).

This allows for a possible trade-off between how egregiously incorrect/unacceptable the winning answer is and the breakdown of how the community splits. We can imagine cases where someone would think that outcome A is pretty injust, and it would be worth forking to a universe where outcome B won, but only if a large percentage of the community forked with her. Otherwise, if only some marginal amount of the community would have been willing to fork over this case, she prefers tolerating outcome A and remaining in the main branch.

(This possibly abstracts both the price they might expect the tokens to get on markets going forward after the case as well as their morality/altruism and willingness to participate in a system that they view as just or injust.)

We expect that the utility function should be monotonic in the percentage of tokens going to the same fork as you. I.e. all else being equal, we assume that participants would not prefer that the fork they are going to be smaller, as this would be a sign that it would be less likely to catch on. These dynamics are reminiscent of the “battle of the sexes” coordination problem in game theory, where two parties try to coordinate on two possible outcomes, and while they have different preferred outcomes, their preference for landing on the same outcome as the other party is stronger than their preference for their better outcome.

Proposal:

User USR_i submits (vote_i, r_i)\in\left\{0,1\right\}\times [0,50]. The user’s choice of r_i will essentially allow them to specify a minimum threshold for community support for a fork at which USR_i would want to join the fork.

The “main fork”; is the one where the outcome_{main} corresponds to the choice receiving the most token-weighted votes. The main fork is the fork that is used to settle any payments of ETH in existing contracts. For the moment, we only consider cases with binary outcomes. Then the “alternative fork” is one where the other outcome is adopted.

We want to organize voters, weighted by tokens, into the two forks such that

1. USR_i remains on the main fork if vote_i = outcome_{main}
2. USR_i remains on the main fork if vote_i \neq outcome_{main}, but the total percentage of tokens that go to the alternative fork is less than r_i
3. USR_i goes to the alternative fork if vote_i \neq outcome_{main}, and the total percentage of tokens that go to the alternative fork is greater than r_i

In Kleros, the users who would normally cast a vote are limited to those who were drawn to consider the case, which initially isn’t very many people but grows with appeals. We could have a special forking vote as some sort of ultimate round like Augur does if a case gets appealed enough times. Alternatively, one could always give users the ability to submit a preference including an r_i like this (even if they aren’t drawn and their vote doesn’t contribute to the outcome of the case in that appeal round), with the expectation that in early appeal rounds, the total percentage of tokens willing to fork will be small because only users who were drawn to vote will be likely to be paying attention to this case.

Note that which fork a voter is included on influences the percentage of tokens on each fork and hence the constraints on r_i for the other voters. Hence, there are potentially multiple possible consistent assignments of the voters to the two forks. Indeed, assuming r_i>0 for all USR_i, then the choice of putting everyone on the main fork satisfies these conditions. We would like to choose the assignment of voters that maximizes the percentage of tokens on the alternate fork.

The process of finding the maximum percentage of tokens that go to the alternative fork can be done efficiently.

Specifically,

1. Take the list L of voters who voted for an vote_i \neq outcome_{main}.
2. Sort L by the user’s r_i.
3. Take the sum of the number of tokens over all voters on L. Denote this by r.
4. Take the user USR_i with the largest r_i. Compare r_i to r. If r_i<r, remove USR_i from L.

Repeat steps 3)-4) until L stabilizes.

Then, the token holders remaining on L go the alternative fork. A simple inductive argument shows that none of the voters removed in step 4) could have gone to the alternative fork under any subdivision. On the other hand, all voters that remain on L after this process have r_i\leq r; hence if they all go to the alternative fork together this is compatible with their choices.

Sorting L takes O(NlogN) time, where N is the number of voters who vote for vote_i \neq outcome_{main}. The repeated process of 3)-4) takes O(N) time, so the entire process takes O(NlogN) time.

Conclusion:

One wants to give maximum freedom to participants to fork as last defense against attacks and then facilitate the organization of the resulting groups. This idea attempts to balance that against not causing the community to split when splitting isn’t really the will of the community.

## Replies

**MicahZoltu** (2019-03-27):

Am I blindly or do you use r_i without ever defining it?

---

**MicahZoltu** (2019-03-27):

It is definitely possible I’m misunderstanding something, but it sounds like this is formalizing a Keynesian Beauty Contest.  It feels like the dominant strategy would be to vote: TRUE, but I’ll vote for LIE if >50% of people vote LIE.  Basically, always follow the majority, whether you agree with it or not.

---

**clesaege** (2019-03-27):

r_i is “The minimum percentage of the tokens migrating to the new fork such that USR_i wants to migrate to the new fork”.

So if I want to fork but only if the fork comprises at least 10% of the network I’ll set r_i = 10\%

---

**whwgeorge** (2019-03-27):

Right. As clesaege points out, the idea is that r_i is a threshold that the user submits for the percentage of tokens that go to the new fork for them to also want to be part of that fork. I’ll update the original post for clarity.

It is true that Schelling game systems in general have aspects of a Keynesian Beauty Contest. You are incentivized to vote for what you think others will vote for regardless of your own belief. However, it is worth pointing out that Keynes introduced Keynesian Beauty Contests as a [metaphor for pricing in equity markets](https://en.wikipedia.org/wiki/Keynesian_beauty_contest). As problematic as financial markets can be, it isn’t for nothing that that structure is still widely used. The value of the stock of a company may not perfectly reflect how one would evaluate the “true value” of that company, but it is still a decent proxy most of the time. So such a system can still give an acceptable signal to noise ratio, particularly in the absence of good (decentralized) alternatives.

Indeed, in terms of this forking proposal, one might want to fork because a successful attack has produced a “clearly wrong” outcome that discredits the main branch and negatively affects the price of the token that it uses. Then by forking you can move your tokens to a parallel version of the system where that outcome was reversed, so the corresponding token may take on a higher value than the main branch’s token. By being able to submit a threshold r_i, users can make their decision of whether they want to fork or not conditional on having a sufficient amount of community support for the fork, which one might expect to have a connection to the market values of the resulting forks. So, ultimately, everything boils down to financial markets.

---

**MicahZoltu** (2019-03-27):

Equity markets are not a Keynesian Beauty Contest because there exists a mechanism for valuing an equity that can be achieved regardless of what everyone else thinks the value is, and if you know that valuation and price towards it, you will win in the long run regardless of how everyone else prices the equity.  This assertion is much stronger for when the market price for the equity is *below* that valuation, though it still can be argued when the market price for that equity is *above* that valuation.

The problem is that without this fundamentals-based valuation, Keynesian Beauty Contests can become *really* pathological, especially if you have a dominant actor or collusion between large participants.

If you still use something like Augur’s mechanism for REP valuation (reporting fees and fee pressure relative to open interest) then I think you would retain the fundamental valuation, and that could prevent this system from turning into a Keynesian Beauty Contest.

---

**whwgeorge** (2019-03-27):

On the comment that equity markets aren’t a Keynesian Beauty Contest because you can make long term gains based on a true evaluation of value, I just have to point out the Keynes addresses that argument [literally in next the paragraph after he introduced the concept of a Keynesian Beauty Contest](http://cas2.umkc.edu/economics/people/facultypages/kregel/courses/econ645/winter2011/generaltheory.pdf) (it is in Chapter 12, page 100).

> If the reader interjects that there must surely be large profits to be gained from the other players in the long run by a skilled individual who, unperturbed by the prevailing pastime, continues to purchase investments on the best genuine long-term expectations he can frame, he must be answered, first of all, that there are, indeed, such serious-minded individuals and that it makes a vast difference to an investment market whether or not they predominate in their influence over the game-players. But we must also add that there are several factors which jeopardise the predominance of such individuals in modern investment markets. Investment based on genuine long-term expectation is so difficult to-day as to be scarcely practicable. He who attempts it must surely lead much more laborious days and run greater risks than he who tries to guess better than the crowd how the crowd will behave; and, given equal intelligence, he may make more disastrous mistakes … Furthermore, an investor who proposes to ignore near-term market fluctuations needs greater resources for safety and must not operate on so large a scale, if at all, with borrowed money—a further reason for the higher return from the pastime to a given stock of intelligence and resources.

That said, I agree with the general point that the more incentivized a fundamentals based approach is, the further you get from a “pure” Keynesian Beauty Contest and the less likely you are to have pathological effects. Ultimately in Kleros, the connection to fundamentals comes from the fact that people will want to have a version of the token that is being used by people that want their disputes arbitrated, otherwise the token holders won’t have the opportunity to earn arbitration fees. Specifically, if the token forks, you want to be on the side that people will want to use to get their disputes arbitrated. Those users will be unlikely to use a system that is producing miscarriages of justice, but they may also be unlikely to use a very marginal fork that only got a few percent of the community. On a general dispute resolution platform like Kleros, if the side that you don’t agree with wins a dispute, that outcome could be anything from “a miscarriage of justice” to “something on which reasonable people could disagree.” (This is a possible contrast with Augur where results are typically more clear cut.) Then, with this forking proposal, individual token holders can weight how blatantly wrong they think an outcome is versus how signficant the resulting fork would be.

---

**MicahZoltu** (2019-03-27):

I have never actually read the original by Keynes, it is interesting to see the source of the term Keynesian Beauty Contest.  I don’t want to get too off topic here, but suffice it to say that I disagree with most of what they say in that excerpt.

![](https://ethresear.ch/user_avatar/ethresear.ch/whwgeorge/48/4271_2.png) whwgeorge:

> Specifically, if the token forks, you want to be on the side that people will want to use to get their disputes arbitrated.

As long as you have this, I think you don’t have a KBC.

I am not convinced that the proposed “vote A unless B reaches x%” solves the problem you want it to solve though.  Ultimately, you want your tokens in the universe that future participants use, and following other reporters doesn’t increase your chances of that happening *unless* traders are following reporters.  If traders are following reporters, then I argue that there is a bigger incentives problem because reporters should be trying to guess where traders are going to go and then going there first.

