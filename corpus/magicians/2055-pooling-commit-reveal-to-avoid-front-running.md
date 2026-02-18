---
source: magicians
topic_id: 2055
title: Pooling commit/reveal to avoid front running
author: bbin
date: "2018-11-28"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/pooling-commit-reveal-to-avoid-front-running/2055
views: 610
likes: 0
posts_count: 1
---

# Pooling commit/reveal to avoid front running

Hello!

So, many kinds of contracts need fraud/fault-proofs with economic incentives. Unfortunately miners can steal the reward without doing any, or just a bit of, validation which breaks the incentive structure. A way to mitigate this is to commit a hash of a message containing the *intention* to send a fraud proof. The reward then would go to the first person who committed an intention, not the first person to submit a fraud proof (or begin some kind of fraud proof game, truebit-style).

A problem with this is that if the system is small enough, just the fact that someone commits an intention to prove fraud could be enough for a miner(/validator) to do some checking and find the fraud in question.

Could this be mitigated further by creating a standardized commit/reveal contract that could be utilized by *all* systems of this kind? Would it be worthwile? The miner would then know only that someone is committing a secret for some kind of commit/reveal-based system, increasing the likelihood of the honest fraud prover getting the reward.

Thoughts?
