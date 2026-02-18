---
source: ethresearch
topic_id: 5074
title: How much should we care about Decentralization?
author: Dapploper
date: "2019-03-01"
category: Miscellaneous
tags: []
url: https://ethresear.ch/t/how-much-should-we-care-about-decentralization/5074
views: 1752
likes: 9
posts_count: 3
---

# How much should we care about Decentralization?

As you all know, there are lots of blockchains emerged with emphasis on scailability(e.g. high TPS) sacrificing decentralization at the same time. I think EOS is a representative example of this.

By the way, I heard from someone that as there are many different kinds of philosophy in open source software(OSS), there will be many kinds of blockchains in the future.

He said, “Ethereum is very radical like GPL license in OSS, and EOS is more like neutral OSS license” “I’ve seen so many software to become just a toy of developers at last as it obsessed over radical idea” And he said that we should consider blockchain in terms of pragmatism so that we can at least serve any meaningful service to ordinary people.

After his saying, I had many fundamental questions in my mind about the decentralization, what we are building now, and what we are trying to achieve. I think these questions are worth to think for what we are doing now, and it would be great to share various ideas each other about these questions.

1. Can decentralization be viewed from the perspective of the range, or can only be one(decentralized) or zero(not decentralized)? Is it meaningful to measure degree of decentralization in blockchain?
2. If the answer of 1. is ‘yes’, then how can we measure the degree of decentralization?
3. What is more important thing in blockchain, the scailability or the decentralization? If we should give up one thing, which thing should we do? And why?

## Replies

**cleanapp** (2019-03-02):

Great questions.

What follows is one unorthodox way to think about decentralization (of many many more), but it checks out:

*as a more-or-less objective measure of success/failure, Ethereum’s legal personality (or lack thereof) is one of the best tests of the extent of Ethereum’s actual level of decentralization* .

Here’s the broader context/argument:

https://medium.com/cryptolawreview/legal-frameworks-for-pow-pos-79d57c8fbca9

---

**nullchinchilla** (2019-03-04):

I think that generally when people talk about decentralization something along the lines of “more entities involved in the consensus process = more decentralization” is meant. So people say EOS isn’t decentralized because only 21 supernodes are involved in the consensus.

Then the EOS people come along and say that those 21 supernodes are theoeretically elected from all the users, so everybody has a delegated voice in the consensus, so EOS is actually the most decentralized cryptocurrency out there!

I think decentralization, in both of these senses, really isn’t very important for blockchains. The key property we want from a blockchain is that it operates autonomously according to its specification without depending on the goodwill of anybody. It’s essentially supposed to be an infinitely trustworthy, completely objective record that’s always a third-party in transactions, disinterested in what the participants are doing.

Centralization, say in a government-regulated banking system, is bad not because the number of participants is small, but because the system is capable of having intent and interests and is definitely not even close to a permanently neutral and incorruptible third-party.

I believe a point has to be made that **blockchain consensus is not analogous to political governance**. In governance, you want to make sure that decisions reflecting some measure of political desirability (popularity, feudal traditions, or whatnot) are efficiently and reliably made. For example, shareholders elect corporate boards of directors so that corporate decisions benefit shareholders’ interests. In blockchain consensus, **you do not want any collective decisions to be made**. Bitcoin miners getting together and legislating the optimal blockchain history in the interests of the general public of Bitcoin users is absolutely not what you want. Instead, you design a cryptoeconomic mechanism so that participants are incentivized to dumbly follow a protocol and not try to pursue any interests other than collecting protocol rewards.

Thus, intuitions about (de)centralization from politics are likely to be highly misleading when designing blockchains. Compare the following two hypothetical blockchains:

1. A blockchain that elects 1000 validators out of all blockchain users, with some magic device to ensure one user gets one vote. The validators then run a BFT consensus to decide blocks.
2. A proof-of-stake blockchain entirely controlled by at most the top 20 richest people, by using an absurdly high minimum stake requirement, with Casper like slashing, rewards, etc.

In political terms, the first one sounds much more “democratic” and “decentralized”, while the second one sounds like the worst kind of plutocratic oligarchy. For blockchains, though, the second one is almost certainly going to be more secure and robust — 20 is a large enough number to mostly offset irrational crazies or compromised nodes from destroying the network, and protocol incentives will keep most of the validators “honest”. The first one is going to be subject to the same sort of game-theoretical pressures that give us party politics, wasteful election campaigning, public-choice economics, etc. We’ll probably end up with some sort of “ruling coalition” of validators controlling over half of the consensus set, routinely making policy decisions like censorship and payment reversions, occasionally getting elected out to be replaced by another coalition with different policies. Wait, that’s starting to sound like EOS…

Thus, I think that the most important thing is **cryptoeconomics**, combined with just enough decentralization to prevent idiosyncratic “crazy monarch” interests from overpowering protocol incentives. Past a certain point, decentralization in the sense of increasing consensus participation adds nothing but an impediment to scalability. And “decentralization” on the model of political democracies is a terrible idea through and through.

