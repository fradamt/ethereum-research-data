---
source: ethresearch
topic_id: 3185
title: Schelling Points, TCRs, and Commitment Strategies
author: Planck
date: "2018-09-02"
category: Economics
tags: [schelling-game]
url: https://ethresear.ch/t/schelling-points-tcrs-and-commitment-strategies/3185
views: 1986
likes: 7
posts_count: 4
---

# Schelling Points, TCRs, and Commitment Strategies

I’m finishing up an article on commitment strategies as solutions to coordination games and I’m curious if this is a well-known phenomenon around here. I’m assuming it is, but is there a name for this?

The argument is that for any on-chain Schelling Point, a suitably funded commitment strategy can always enforce a different equilibrium for rational agents. The commitment strategy can be just basically “I commit to losing additional amount x if I don’t get my way”, which commitment then means you know the person will try very, very hard to get their way. If x is sufficiently large, then it’s rational to let them get their way. And since it’s rational to do so, *this commitment was free*. That’s the really tricky part–effective commitment strategies can be “off-equilibrium” and so someone can enforce their preferred outcome at 0 cost, in theory.

I discussed this strategy last month in the context of Fomo-3D, and Tarrence Van As pointed me to a recent illustration of this in Adchain’s Token Curated Registry (a coordination game).  The founder of SpankChain appeared to use a commitment strategy to help his business get added to a TCR:

![image](https://ethresear.ch/uploads/default/optimized/2X/f/f08841f6e60a40c7c3cb4c7f713f89a4df037ccf_2_690x76.png)

As far as I can tell, this seems to be a general vulnerability of on-chain “Schelling Point” models–they can be solved with commitment strategies (or, more accurately, they aren’t Schelling Points at all.) Hopefully that point is clear enough. When someone institutes a effective commitment strategy then the Pareto solution is always going to be choosing their preferred equilibrium (because value is destroyed in other cases-- that’s what the commitment strategy does.) The resulting outcome might not always be free for the committer but it should always result in their preferred outcome, regardless of whether it’s the right one.

Comments appreciated.

## Replies

**MicahZoltu** (2018-09-02):

Naive schelling games turn into [Keynesian Beauty Contests](https://en.wikipedia.org/wiki/Keynesian_beauty_contest) when there are economic incentives at play, and those devolve into “guess how the biggest whale will move” games, which (assuming rational actors) reduces to “only the biggest whale even plays the game”.

---

**Planck** (2018-09-02):

Just to explain a little more specifically: in a coordination game, if player M effectively commits to strategy s_1 such that if they don’t follow it there is an irrevocable loss of value x, then only some player/group W who’d stand to gain an additional x from M choosing some s_{i \ne 1} would try to enforce a different equilibrium. (e.g. if W only gains y<x from their preferred then they could bargain with M for y and both are better off.) And yes, while a whale who could marshal 50\% + \epsilon of the voting currency could guarantee any outcome, they may not want/need to conditional on the commitment.

---

**vbuterin** (2018-09-03):

I agree with all of this. This is exactly why I do think that any Schelling game needs to have a “split and let the market decide” clause. If 51% vote incorrectly, then the remainder can fork the dapp into a new version where the losers are treated as actually being the winners, at which point there are two versions of the dapp, one where the incorrect voters have more tokens, and one where the correct voters have more tokens, and the market would naturally favor the correct one. The goal of the cryptoeconomics is to make it expensive to create a point of human decision, so as to reduce the number of such decisions that users need to think about.

