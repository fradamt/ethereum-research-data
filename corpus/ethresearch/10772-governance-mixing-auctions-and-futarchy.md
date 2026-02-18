---
source: ethresearch
topic_id: 10772
title: Governance mixing auctions and futarchy
author: bowaggoner
date: "2021-09-17"
category: Economics
tags: [governance]
url: https://ethresear.ch/t/governance-mixing-auctions-and-futarchy/10772
views: 3019
likes: 7
posts_count: 6
---

# Governance mixing auctions and futarchy

## Abstract

I’ll recall the strengths and weaknesses of 3 different group decisionmaking protocols: voting, auctions, and futarchy. I’ll describe a hybrid auction-prediction mechanism and call for more ideas!

## Background

Governance decisions require aggregating two kinds of objects:

- preferences
- information

These are orthogonal. I might personally prefer that my town builds a library instead of a park. But I might predict better outcomes for my town as a whole in the case of the park.

Traditional voting schemes are designed to aggregate preferences, not information. (I’d presumably vote for the library). But even for pure preference aggregation, auctions can sometimes be better than voting. Voting is not incentive compatible, can be manipulated, doesn’t reflect strength of preference, etc.

Instead, we could for instance auction off lottery tickets for the right to decide between a library and a park. People can express the strength of their preference by buying more tickets. (The revenue can be redistributed equally.)

But neither auctions nor voting take into account information aggregation.

Futarchy attempts to remedy this via “vote values, bet beliefs”:

1. Vote on which metrics are important to society.
2. Use prediction markets to determine which decision optimizes those metrics, and take it.

## Some drawbacks of futarchy

From what I’ve seen on ethresearch, proposals for DAO futarchy often skip the “vote values” stage entirely and assume the metric is the price of the DAO’s token. But as I understand it, this severely limits the kinds of decisions that futarchy can make. For example, it seems hard for the DAO to decide via futarchy to allocate resources toward charity or something non-profitable.

To make other kinds of decisions, we need to include the “vote values” stage of futarchy. This likely inherits the drawbacks of standard voting schemes. And it relies on existence of some objective metrics for us to choose from. Something like “total welfare of members of the DAO” is very hard to measure objectively. So using futarchy to optimize it seems futile.

## Proposal: mechanisms mixing auctions and prediction

On the other hand, auctions can be good for optimizing things like total welfare of a group. (And one can redistribute the revenue, etc.) So how about governance mechanisms that combine auctions and prediction?

I have one. It’s based on Vickrey-Clarke-Groves (VCG) and inherits its drawbacks. It also uses proper scoring rules. We published it in a paper in 2013 for a very different context, but I also have a blog post about it.[1]

I’ll explain by example. Each participant submits 3 numbers:

- v_a =  their value for “accept the proposal”
- y_a =  their forecast for the value of the token if we accept
- y_d =  their forecast for the value of the token if we deny

Interpret v_a as the amount they’d be willing to pay to switch the decision from deny to accept. v_a could be negative.

**Decision rule.** Now let V be the average of everyone’s v_a submissions. Let Y_a be the average of everyone’s y_a submissions and similarly for Y_d.

- If V + Y_a^2 > Y_b^2, we accept the proposal.
- Otherwise, we deny the proposal.

Notice this objective is a compromise between futarchy (accept iff Y_A > Y_b) and auctions (accept iff V > 0).

**Payment rule.** Now we have to decide how much everyone pays. It’s a bit complicated, but the idea is that we can use proper scoring rules and the VCG mechanism so that people are incentivized to report all three numbers truthfully. I’ll leave the details to the blog post / paper. But the idea of VCG is that if your bid “flipped” the outcome, then you pay an amount equal to the externality you impose (i.e. how much worse off everyone else is thanks to your bid flipping the outcome). And the idea of the scoring rule is that if we accept the proposal, you’ll pay based on (y_a - Y^*)^2, where Y^* is the actual price of the DAO token at a given future point in time, like a week after the vote. I.e. the squared loss of your prediction. If we reject then you’ll pay based on (y_d - Y^*)^2.

**Extensions.** We can replace Y^2 with any other convex function. We can also multiply it by a constant, which changes the relative importance of preferences vs predictions. The only issue with scaling up the prediction importance is that every participant is potentially on the hook to pay a lot of money if their predictions are wrong.

## Questions

The really cool aspect is that the above proposal is in theory incentive-compatible, which neither voting nor futarchy is. The idea is if you want one outcome a lot more than the other, then your best way to achieve it is simply to bid your true value v_a. Manipulating your predictions on top of that only hurts you.

But a big drawback of this particular scheme is that the aggregation of information is pretty weak. We just average everybody’s forecasts. One would expect a prediction market to do a much better job.

**Is there a simpler or better way to make governance decisions based on auctions and individual predictions?**

**Can we do governance combining auctions with prediction *markets*? Auctions with futarchy?**

**Do auctions have a legitimate role in governance decisions?**

The argument I know for the last one is this: either (a) you think everyone has enough money relative to the importance of these decisions (i.e. you believe economists’ quasilinear assumption), in which case clearly auctions are the best since they maximize welfare. Or (b) you don’t. In that case you probably agree that people with more money and power are able to use it to influence governance decisions, via direct or indirect manipulation. So why not just let rich people directly pay for the governance decisions they want (since they do that anyway indirectly), and redistribute that money to everyone else, in hopes of at least working toward a more egalitarian future? Okay, tongue mostly in cheek.

[1] [The Tiger's Stripes](https://bowaggoner.com/blog/2018/06-23-hybrid-auction-prediction-mechanisms/index.html)

## Replies

**kelvin** (2021-09-17):

Your 2013 paper is very interesting! I’m going to study it in more detail over the next days, thanks for sharing it here.

I have a few questions. Can you give more details on the payment rule? In the paper, the “outcome” being predicted (in the paper’s simpler model), called the *quality* of the proposal, is bounded in [0, 1], where here the price is not. Is the mechanism still individually-rational?

If I understood correctly, people pay (y_d - Y^*)^2 when their proposal is rejected. This is in contrast to the paper, in which losing bids don’t pay anything. How is the mechanism incentive-compatible? What is the incentive for me to submit a proposal that has only a small probability of being accepted?

Regarding the drawbacks of futarchy, I’m totally for experimentation of different “values” of “vote values” ideas for DAOs, as they’ll make them more general and useful. [This proposal](https://ethresear.ch/t/practical-futarchy-setup/10339) is really only intended for DAOs competing with or intended to replace profit motive companies. Such DAOs will be unable to donate to charity or really do anything other than maximizing profits to tokenholders.

The default argument against such concerns is that tokenholders should use some of the profits due to them to promove the charities that they themselves like. I don’t like this argument as this may be inefficient: there may be some low-cost, high-impact opportunity for public good that are uniquely available to the DAOs.

One solution is for charities or other philantropic entities to “bribe” the DAO into acting for the public good. I admit this does not generate the best optics, but at least it prevents economic inefficiencies.

---

**Shymaa-Arafat** (2021-09-18):

I haven’t read the paper yet, but I think all can be achieved by optimizing a weighted function & some problem dependant constraints.

For example in the library Vs park one could suggest building a library above a park, requiring a min no of parks & libraries in the city,…etc.

I believe whatever specific to the problem in ur mind can be formulated into weights & constraints.

I had a chance to see the impact of this in a completely different context; that’s game thoeritic model for any conflict ( in my case the Ethiopian Nile Dam conflict) u see different papers with different models& Equilibrium depending on how they adjusted the function & the parameters

---

**bowaggoner** (2021-09-20):

kelvin, re: differences between the paper and this post: thanks a lot for taking this in-depth look! I apologize because there is a pretty big gap between the paper’s focus and the applications here, and I didn’t clarify the gap well.  Quick points:

- the paper starts with a single-item auction model, then gives a general model.
- for governance, I’m thinking not of the first single-item auction model, but of a different special case of the second general model. I think this clarification will address some of your questions!
- will it always be individually rational: not “ex post”, no. If I make a bad prediction, I might have to pay a lot and end up with negative utility after the fact.

Here is a rewording of the mechanism that I hope is clearer!

1. There is some decision to be made, e.g. a proposal we must accept or reject. I didn’t think yet about where proposals come from or who proposes them. I just assume there is one proposal in front of us to decide on, accept/reject. For example, the proposal is to increase our member dividend.
2. Everybody submits those three numbers v_a, y_a, y_d: value for accepting, prediction if we accept, prediction if we reject. Since there’s only one proposal, everybody is submitting their value and predictions for that same one proposal. Letting Y_a be the average of everyone’s y_a, we can view Y_a as the group’s aggregate average prediction for the value of the token if we do increase the dividend. And Y_d is the average prediction if we reject.
3. We can think of this mechanism as two-in-one: we require everyone to bid v_a as though they’re in a sort of auction, and we require everyone to make predictions as though they’re participating in a futarchy prediction market for this dividend-increase proposal.
4. We accept iff V + Y_a^2 > Y_d^2.
5. We wait a week (or whatever) and then everybody makes a payment based on how accurate their prediction was, as well as how much they bid. If we accept the proposal, then your payment will have a component involving (y_a - Y^*)^2. If we reject the proposal, your payment will have a component involving (y_d - Y^*)^2. So it’s like you participated in a futarchy market and are now getting your net payoff.

## More about that paper vs this discussion

Okay, so, in the general model of the paper, there is a set O of possible outcomes. We will pick exactly one outcome. So we could have O = {library, park} if those are the two options. Or we could have O = {accept proposal, reject proposal}. But here I didn’t think about where proposals come from or the incentives of creating proposals. I just assumed there is some decision to be made.

Whereas – the simple model of the paper is a single-item auction and here the “decision” we have to make as a group is who should get the item. So if there are ten participants then O = {person 1, …, person 10}. And in the simple model, we assume people’s preferences are of the form: person i gets value v_i from winning the item, and value 0 otherwise. But this is not how the “accept/deny” preferences work. **So this single-item auction model doesn’t seem to work for most governance decisions.**

**About VCG for public projects.** To understand the payment rule, let’s forget about the predictions/futarchy part and just consider: what if we tried to run a city-wide auction using the classic VCG mechanism to decide between library/park? Everyone submits a “bid” v_i representing how much they’re willing to pay to switch the decision from park to library. v_i could be negative if they’d need to be paid because they prefer the park. Let V be the sum of all bids. Then we build the library if V > 0, otherwise the park. Now the payment rule looks like this: If we build the library, but V - v_i < 0, then person i has to pay v_i - V. That’s because person i was “critical” and caused the decision to flip. Similarly every “critical” person has to pay basically the amount needed from them to flip the decision. The same idea goes if we build the park. More at e.g. [Section 3.4 of these pdf notes](https://chekuri.cs.illinois.edu/teaching/spring2008/Lectures/scribed/Notes12.pdf).

There are strange implications from this. You can easily get a situation where e.g. 70% of people prefer a proposal, so nobody is “critical” and it passes without anyone having to pay anything. In fact someone could costlessly manipulate the mechanism by creating a million fake accounts and having them all bid a small amount. I would love to improve on this problem.

Anyway, the idea of the 2013 paper is to change the “social welfare” from: V if we accept, zero if we don’t; to: V + Y_a^2 if we accept, Y_d^2 if we don’t. If we did this, then VCG would suggest a payment rule that looks like the expected payments below. But we have to modify it to use squared error.

## Payment rule details

In short, the payment rule is weird partly because the VCG mechanism (above) is weird. Also, I have added an extension here that isn’t in the paper, similar to what kelvin mentioned: In the general model of the paper, people’s predictions are a probability distribution over something (e.g. a distribution over the value of the coin). We use a ‘proper scoring rule’ to determine the payment. However, it also works if we just ask people to predict y_a as their expected value and we use squared loss, rather than asking people to give a full probability distribution. However, their potential loss is technically unbounded, a detail that would have to be fixed.

Anyway, here’s the exact payment rule. Let V, Y_a, and Y_d be the averages of the submissions. Suppose participant i submitted v_a^i, y_a^i, y_d^i. Remember n is the number of participants and Y is the observed value of the DAO’s token one week after the vote.

**If we accept the proposal, i pays**

(v_a^i - nV) + \frac{1}{n}(y_a^i - Y^*)^2 - C_a(Y^*) ,

where C_a(Y) = \frac{1}{n} \left(Y^* + \sum_{j \neq i} y_a^{j}\right)^2.

Here the first terms is the sum of everyone else’s value. The second term is the squared error of i's prediction. And finally, C_a(Y^*) is a bonus that only depends on everyone else’s predictions, not her own.

The point of this payment rule is that, if my calculations are right, then when i's prediction y_a is truthful, her expected payment in this case is

(v_a^i - nV) - n Y_a^2.

Meanwihle, **if we reject the proposal, i pays**

\frac{1}{n} (y_d^i - Y^*)^2 - C_d(Y^*).

Here C_d(Y^*) is the analogous bonus depending on others’ predictions. I similarly claim that if i's prediction y_d is truthful, her expected payment is

- n Y_d^2.

Now we can see that if i's predictions are truthful, she prefers the proposal to be accepted iff nV + n Y_a^2 > nY_d^2. (This is true because her utility if it’s accepted is v_a^i minus her payment; and her utility if rejected is just negative payment.) Since this is the choice rule the mechanism actually uses, she should just be truthful about her value and the mechanism will choose in her favor. Also, above I wrote “if she’s truthful about her predictions”, but we can see that she should be, because if not, her expected squared loss will be worse and her expected payment will be higher.

(I simplified something: i's payment in either case would also include a term W_{-i} which depends on everyone else’s reports, but not i's. This is added to i's total payment either way.)

---

**bowaggoner** (2021-09-20):

By the way, a concrete open problem is to propose a much simpler and more direct mechanism for decisionmaking that has both an auction and a prediction component. I think the above is a starting point because it “works” in theory, but I know it’s opaque.

Here’s an example of a simple one, though it’s probably bad:

- We open a futarchy-style pair of prediction markets for the DAO’s token value in the future. One market each for accept and reject. Call the market prices \pi_a and \pi_d.
- Once the market closes we hold a sale for votes. You can purchase as many as you want. The price of an accept vote is 1/\pi_a. The price of a reject vote is 1/\pi_d.
- The winning option is the one with the most purchased votes.

Actually I would modify this to be a bit random. If there are A and D total votes respectively, accept with probability e^{A}/(e^A + e^D).

---

**adamstallard** (2021-11-24):

I read this yesterday and it inspired me to add a section to “[rules markets](https://docs.google.com/document/d/1TKA-K8YadRdgz-Qek01TUcCkRaI9CKCXGtJ31AbVWIU/edit#heading=h.ejtvi2tfe6ad)” to hypothesize how they might be used to discover the metrics and actions (markets) for a futarchy. I apologize for the crudeness of the document; I’m still collecting feedback on how to improve it, and would love yours.

