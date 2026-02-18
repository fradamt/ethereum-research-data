---
source: ethresearch
topic_id: 4070
title: Strategies for Plasma Clients
author: kfichter
date: "2018-11-02"
category: Layer 2 > Plasma
tags: []
url: https://ethresear.ch/t/strategies-for-plasma-clients/4070
views: 1962
likes: 4
posts_count: 9
---

# Strategies for Plasma Clients

I think there’s an interesting discussion to be had about the various strategies that plasma chain clients should take when dealing with things like challenges or exits. I haven’t seen a *ton* of discussion about this yet - a great thread was started [here](https://ethresear.ch/t/rabbit-or-child-dilemma-in-plasma-implementations/3583) in the context of withdrawals, but I’m very curious to see how client developers are already handling this.

## Motivation

To first motivate why you should care about this topic, let’s look at a naive plasma implementation. A client developer might choose to have a piece of software that always watches the plasma/root chains and automatically challenges if something goes wrong. This sounds pretty good - as soon as someone tries to start an invalid exit, someone will respond with a challenge.

Unfortunately, this strategy of immediately challenging becomes problematic when more than a few clients are actively watching/challenging. Only one person can actually win the challenge, but all of the clients are submitting challenges at the same time! One of these challenges will go through, the rest will throw and burn a bunch of gas.

There’s also similar discussion necessary about exactly how long to wait before bailing on a plasma chain that isn’t publishing the contents of a block. It’s not unlikely that a plasma chain operator will eventually submit a block and then somehow crash/go offline unexpectedly, even for a few hours. What strategy should clients use to decide when to exit? It seems like there’s inherently a social component here too - if a trustworthy operator publicly claims the downtime is accidental, I might be inclined to believe it. [@MihailoBjelic](/u/mihailobjelic) started a thread about this in a [post here](https://ethresear.ch/t/rabbit-or-child-dilemma-in-plasma-implementations/3583).

## Coming up with strategies

We obviously need a better strategy for this - it generally seems like interesting design space. In theory we could allow clients to select their own strategy, but unfortunately my guess is that most clients will [simply follow the default strategy](https://pagefair.com/blog/2015/the-tyranny-of-the-default/) (also it’s a UX nightmare). So we’ll probably have to come up with a solid strategy to ship along with clients.

I’ll note here that this might be a totally solved problem, ideally there’s some provably optimal strategy that statistically burns the least gas possible. I’m sure we could do some simulations to get initial results. I’ve heard suggestions that this could be similar to traffic control problems, which already have some [game-theoretic thinking](https://ieeexplore.ieee.org/document/4739461) [behind them](https://www.sciencedirect.com/science/article/pii/S1474667016400960). This seems like a pretty simple game and I’d be surprised if someone hasn’t explored it in a different context.

One simple strategy might be to have clients wait a random amount of time before challenging, based on their best estimate to the number of challenging clients in the network. This probably works pretty effectively at first, but gets worse and worse as the number of clients increases. It’s also worth noting that not all clients are required to challenge, so the total number of clients may not be an accurate indicator. I’m also guessing that we should weight the % chance that a client challenges at any point in time more heavily as the number of invalid exits increases and as an invalid exit gets closer and closer to finalizing.

All of this is purely conjecture and I haven’t spent nearly enough time thinking about it in front of a whiteboard, but it seems important that client developers be aware of this problem!

## Some questions

1. How are clients currently handling this?
2. Has anyone explored different strategies already?

## Useful things to do

1. A simulation of various strategies for clients who want to exit from a plasma chain.
2. A simulation of various strategies for clients who want to challenge an invalid exit.
3. Seeing if there’s more game theoretic research out there that could help us.

I’m going to spend some time working on (2) here and try to optimize on total gas wasted. Help/suggestions would be much appreciated!

## Replies

**MihailoBjelic** (2018-11-02):

[@kfichter](/u/kfichter) thanks for expanding on my thoughts. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I agree that this is an interesting and underdiscussed topic.

![](https://ethresear.ch/user_avatar/ethresear.ch/kfichter/48/951_2.png) kfichter:

> I’ve heard suggestions that this could be similar to traffic control problems

This might be true, but only in terms of avoiding main chain congestion, right? It cannot help with the dilemma I described?

I still think some sort of scoring mechanism could be useful here. You track a few critical parameters (number of exits per unit of time, your balance on the chain etc) and normalize and aggregate them into an “exit coefficient” q (0 < q < 1). Then all that is left is to decide on some standard waiting time t (relatively long, probably in hours or even days in some implementations), and in every particular case client “knows” that it should wait q * t.

---

**bharathrao** (2018-11-03):

The papers you have referenced discuss flow of entities moving in opposing directions through a choke point, while exit challenges are one way (utxos exiting chain).  Orderly exit of a building on fire is a more accurate model than traffic control.

In general, most plasmas have the following issues:

- Too many people in the burning building(Too many UTXOs)
- Everyone wants to run when there is a fire! (When anyone observes a jump in challenges, its obvious that its all crashing down)
- No fire drills resulting in a stampede (everyone exits their utxo)

Little’s law from Queueing theory L = \lambda W, is probably the simplest way to model this situation. The plasma contract can process W exits per block and the number of requests arrive at the rate of \lambda per block. The primary implication of Little’s law is that if \lambda or W becomes uncontrolled, the system will be overwhelmed.

In practice, as \lambda increases, the congestion quickly becomes unbearable. We see this routinely in all queueing situations from lines at DMV to webapp requests. Controlling \lambda is the simplest way to ensure smooth flow of the system. Highways have metered on-ramps for this reason and we can observe that a congested highway suddenly smooths after passing an exit, even though very few cars seem to be exiting.

The naive exit strategy is for everyone to *get out now!* causes \lambda to spike very high and makes any form of exiting impractical. The real issues with plasmas (that we have attempted to fix in Gluon Plasma) are the following:

- There is no control on ingress into plasma. Anyone can create millions of dust utxos. This is equivalent to not having a “Maximum persons allowed” into a building. Every UTXO including every intermediate UTXO potentially needs to be challenged. Each of the millions of dust utxos can have a million transfer history. This is essentially an unbounded \lambda for exit queue.
- When there is a sudden spike in challenges, its obvious that the operator is compromised. There is a good chance the operator will try to exit an earlier version of an UTXO that the user owns. He would need to either exit (depending on priority property of chain) or be ready to challenge. The point here is that the sudden urgency to act for everyone may render the scheme impractical.
- There need to be a few fire drills that simulate an orderly exit to ensure that any of these schemes even work. The original plasma paper had the concept of a mass exit that is submitted as one request. Without an equivalent to this, if everyone is acting on their own, I don’t see any pragmatic sketch of how to dealing with a compromised operator situation will ever work.

Our attempts to fix the above issues in Gluon:

- Operator has the choice to admit deposits. Dust deposits can be ignored and on ramp can be metered. There are no intermediate or multiple utxos to exit. In general the number of deposits and withdrawals are tightly controlled (Tight control on number of people in the building)
- Halting the chain via a vote is the equivalent of a single mass exit which relieves the urgency to act now or be doomed.
- Halting games held regularly on testnet. Fire-drills condition the mind to act rationally even in a panic situation.

---

**sdtsui** (2018-11-04):

What if there was a way for the eventual winner to commit to distributing her reward to other successful challengers, within a threshold time?

---

**MihailoBjelic** (2018-11-04):

Makes sense to me.

I guess the winner could be awarded a portion of the original reward, e.g. 40% and the Plasma contract could distribute the remaining 70%… If there was few other challengers (or none), the winner could keep the bigger share of the reward (or the whole of it).

---

**derekchiang** (2018-11-05):

I’m glad this is finally being discussed!  It’s actually a common problem in any challenge-based system such as Truebit and Tenfold (a system I’m working on).

In general, there are two ways to solve this problem (and the solutions are largely orthogonal):

1. Splitting the reward between multiple challengers.
2. Restricting who gets to challenge.

[@sdtsui](/u/sdtsui) and [@MihailoBjelic](/u/mihailobjelic) were suggesting #1, but it’s actually a bit tricky to get right.  Specifically, the splitting function needs to be sybil-resistant.  Consider the trivial splitting function where each challenger gets `1/N` of the reward.  An attacker can then simply gain the lion share of the reward by challenging from multiple addresses at once.

Truebit correctly observed that the function family `f(m)= c * 2^(-m)`, where `m` is the number of challengers, is sybil-resistant.  For instance, consider if `c=1` so we have `f(m)=2^(-m)`.   Now if we have 1 challenger, the reward is `1/2`.  If we have 2 challengers, the reward for each is 1/4 and the total reward is 1/2.  If we have 3 challengers, the reward for each is 1/8 and the total reward is 3/8.  Therefore, the total reward actually decreases as the number of challengers increase, which is why it’s sybil-resistant.

However, I think this solution is not sufficient in itself for a system like Plasma (and Tenfold), because the clients are largely uncoordinated.  That is, they don’t really know whether 1) they should challenge because no one else would, or 2) they shouldn’t challenge because there are already other challengers.

So, this leads us to solution #2, namely restricting who gets to challenge.  Here I describe the scheme we use in Tenfold:

For each challenge, we compute the “barrier” as follows:

`B = F(E, A) mod W`, where:

- E is the hash of the exit.
- A is the address of the challenger.
- W is the length of the challenge window.  The length can be measured in time (e.g. seconds) or blocks.

The barrier is essentially the amount of time that one has to wait before it can challenge an exit.  Barriers are enforced by the smart contract that handles exits and challenges.

So for instance, let’s say the challenge window is 300 seconds.  When a client sees an invalid exit, it computes `B` locally.  Let’s say `B` works out to be 127 seconds.  Then the client knows that the smart contract is not going to accept its challenge until at least 127 seconds has passed.  So it waits 127 seconds, and submits a challenge if no one has already done so.

The idea is basically to spread out the clients within the challenge window in a deterministic and fair way, so that they challenge one by one as opposed to all at once.

This scheme is not perfect, however.  Here are a couple issues and how we plan to address them:

- It’s not sybil-resistant.  Since F takes the address of the challenger into account, a client who’s determined to get the opportunity to challenge can simply spawn a large number of addresses and use the one that yields the lowest barrier.

There are multiple ways to make F sybil-resistance.  One way is to require clients to register themselves on-chain upfront.  In a PoS system like Tenfold, F can in fact be a weighted random shuffle function where the clients are weighted by their stake; that is, the more stake you own, the more likely that you are placed towards the start of the challenge window.

There are still no guarantee that there won’t be multiple challenges, since it’s entirely possible that multiple clients wound up with barriers that are close to each other, and they all submitted their challenges before any of the challenges is included into a block.

- This basically leads us back to the reward splitting problem earlier.  However, since we can be fairly certain that the number of concurrent challenges will be small, we can use a non-punishing splitting scheme such as 1/N or an algorithm similar to what Ethereum uses for uncle blocks, where the first challenger gets the lion share and subsequent challengers get smaller shares.

---

**bharathrao** (2018-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/derekchiang/48/1342_2.png) derekchiang:

> There are still no guarantee that there won’t be multiple challenges

Why not allow only the first challenger? There is a risk that in a multi-step game, the first challenger runs out of gas or abandons the challenge (in collusion with the bad actor), so *anyone else* should be able to pick up the challenge according to the same barrier formula. This ensures that one and only one challenger can take part in the challenge at any step.

---

**MihailoBjelic** (2018-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/derekchiang/48/1342_2.png) derekchiang:

> @sdtsui and @MihailoBjelic were suggesting #1, but it’s actually a bit tricky to get right. Specifically, the splitting function needs to be sybil-resistant. Consider the trivial splitting function where each challenger gets 1/N of the reward. An attacker can then simply gain the lion share of the reward by challenging from multiple addresses at once.

This is totally true. A lot of chains (i.e. dApps that run on them) will have some sort of user accounts/IDs, so they can solve this issue more or less trivially. I don’t have an idea what could the chains without accounts do about it, though.

Your analysis of solution #2 is very good, I have nothing to add.

---

**derekchiang** (2018-11-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/bharathrao/48/1141_2.png) bharathrao:

> Why not allow only the first challenger?

Sure, allowing only the first challenger is a valid strategy as well, assuming that the barrier mechanism does a good job of spreading out clients so that it’s unlikely that more than a couple clients challenge at once.  I was merely proposing the splitting schemes in case it’s important that honest clients don’t waste gas.

