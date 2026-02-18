---
source: ethresearch
topic_id: 7628
title: Applying the "Five Why's" to the Client Diversity Problem
author: pipermerriam
date: "2020-07-02"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/applying-the-five-whys-to-the-client-diversity-problem/7628
views: 2194
likes: 14
posts_count: 6
---

# Applying the "Five Why's" to the Client Diversity Problem

The majority of last week’s All Core Devs call was spent discussing a topic that has been near and dear to my heard for years.  I’d like to attack this by applying [The Five Whys](https://en.wikipedia.org/wiki/Five_whys) so that we can understand the root cause, and hopefully avoid wasting effort focusing on the wrong problems.

We’ll start with the following problem statement

## Problem Statement #1

> Geth represents a super-majority of the Ethereum mainnet and is maintained by a very dedicated, but small team. The current conditions under which the client is developed are not sustainable and lead to client burn out.

Alright, so there’s the first try at capturing the problem.  We’ve got at least two things going on here.  The *correctness* requirements for the project are extreme, since the health of the network rests effectively entirely on their shoulders, resulting in the job being stressful.  The small team makes this a lottery/bus problem since one or two of the devs burning out and moving onto something else would likely significantly impact the velocity of development on the project that might take years to recover from.

So we can *maybe* agree on part of the problem here.  Having a single client that represents a super majority of the network results in a situation where **if** the client has a consensus bug which would cause a fork, the entire network will follow the *wrong* fork since the majority of the nodes on the network will have the bug.  Said differently, the minority clients on the network play near zero role in choosing the *correct* fork, since they will always be out-voted by the client holding the super majority.  We’ll refer to this going forward as *“client diversity”*.

The other facet of this problem, the team itself being small and subject to burnout, is a real problem, but I’m going to set it aside for now.  We can’t fix the problems associated with poor client diversity by focusing on the go-ethereum project alone.  Maybe we could reduce the stress on the team, and build out a larger team to get to a safer place, but we can’t address the rest of the problem via focusing on a single client.

With this established, we can now take another stab at the problem statement.

## Problem Statement #2

> The Ethereum mainnet does not have adequate client diversity.  Because of this, a critical consensus bug, or other denial of service attack effecting the Geth client could severly impact the smooth operation of the network.

With this new problem statement we get closer to the real problem. What happens when the Geth client breaks.  Software is notoriously difficult to get right, and even were we to try and apply the most stringent practices to focus on achieving correctness in the Geth client, it’s still likely that something would eventually go wrong.

Having established that this problem can’t be solved by focusing on the Geth client itself, we expand our focus to the minority clients.  Here is what the network looks like today according to Etherscan data

- Geth: 75%
- Parity: 15%
- OpenEthereum: 5%
- Nethermind: 1%

None of the other clients on the network have a meaningful market share.

To the best of my current knowledge, there are four minority clients actively working towards being viable mainnet clients for production use.

- Nethermind
- Besu
- Turbo Geth
- Trinity

I won’t go into specifics about any of these. Instead, I want to look at the broader trend.  With the exception of maybe Nethermind and Besu very recently, there has not been a new client introduced to the network which could sync and operate reliably since Parity joined the party years ago.  Why haven’t we seen more clients join the network? Why aren’t the current minority clients progessing faster and being used more broadly?

I have spent almost three years working on the Trinity Ethereum client.  I’m going to gloss over the details, but my conclusion after working for a long time to try and introduce a new client to the network is that it is prohibitively difficult.

## Problem Statement #3

> Creating an Ethereum client is too difficult.  This has lead to poor client diversity, which leaves the network in a vulnerable position.

Now we’re getting somewhere. A naive approach to our current client diversity problem would be to try and provide better support for minority clients. One problem with this approach is that Geth has years of head start.  We cannot [reasonably](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) expect new clients to catch up anytime soon.

So, if we cannot create new clients quickly due to the underlying difficulty in doing so, can we attack the problem from a different direction and make it easier to create clients?

## Problem Statement #4

> The current structure of the Ethereum network results in it being prohibitively difficult to create a client for the network.  This results in the network having very few clients, and thus, poor client diversity.

Here we re-focus the problem from the clients, back to the protocol.  Here are some things that are difficult in the current protocol.

1. The Ethereum “state” is very large
2. Managing the local “state” requires high end hardware and complex software
3. Syncing the state in a reasonable amount of time is complex
2. The network stack is a “monolith”.  Being part of the DevP2P ETH network requires you to support:

On demand access to any part of the Ethereum state and state trie
3. On demand access to the full chain history

This results in a high barrier to entry for new clients since accomplishing these things, amoung the many other things an Ethereum client must do is a complex engineering task.

## Problem Statement #5

I don’t think there is necessarily a 5th layer to this, but the [Five Whys](https://en.wikipedia.org/wiki/The_Mythical_Man-Month) inspiration for this post requires me to have five things.

## Conclusion

If we accept that there is a problem with client diversity, then I believe there is a strong case to be made that we can fix the problem by focusing on the network and protocols themselves.  Specifically, we need to make it easier for clients to manage and sync the state, and we need to loosen the requirements placed on clients to join the DevP2P network.

I’ve intentionally stayed away from the “solution” space but I believe that the current “Stateless Ethereum” roadmap aims to address a part of this problem.  Alexey’s “three networks” model likely solves the “monolith” issue.  The [re-genesis](https://ethresear.ch/t/regenesis-resetting-ethereum-to-reduce-the-burden-of-large-blockchain-and-state/7582/1) suggestion by Alexey would also temporarily address some of the problems as well.

## Replies

**AlexeyAkhunov** (2020-07-02):

Thank you for writing this down (or up), it is definitely helpful to think deeper about this. I have my own opinions on the difficulty of writing Ethereum implementations, need a bit more time to formulate those

---

**vbuterin** (2020-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> Parity: 15%
> OpenEthereum: 5%

IMO this is revealing. It shows that lots of people are unwilling to change to a different client out of pure inertia. Not sure how solvable that is; even if it is not, it might be both good and bad news, as it shows that while a single-client equilibrium is sticky, a multi-client equilibrium may be sticky too.

---

**dankrad** (2020-07-02):

I generally agree with the reasoning, and I think it is clearly better in terms of decentralization to have more client diversity. However, this seems a strange statement to me:

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> We’ve got at least two things going on here. The correctness requirements for the project are extreme, since the health of the network rests effectively entirely on their shoulders, resulting in the job being stressful.

Let’s say we have three clients with each 1/3 of the share of the network. I would claim that the total effort of maintaining these clients with a quality standard is definitely more than one client, even at the extra quality that is demanded by it being the single client.

Now you may argue that it can be distributed across more shoulders, but I don’t see why that can’t be the case for a single client? In other words, if you can get enough devs to develop 3 clients, you could also just develop one client and assign 2 further teams to do QA and write lots of tests, and I actually expect better results from this approach overall. Having 3 different teams working on this independently also prevents the management problems from having to manage one large team working on one client (which I actually think doesn’t work that well).

As I said, I do support client diversity, but it seems very surprising to me that this would be a solution to significantly relieve the Geth teams workload.

To rephrase it into a concrete proposal, can we hire a team that just does QA on Geth and thus relieves the pressure on the core team to get everything right?

---

**AlexeyAkhunov** (2020-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> if you can get enough devs to develop 3 clients, you could also just develop one client and assign 2 further teams to do QA and write lots of tests, and I actually expect better results from this approach overall.

The benefits of a dedicated QA team are questionable. I worked in couple of places where QA team was very strong, and they worked very hard, but we could not make releases more than once in 6 or 12 months. And the whole thing was quite stressful, partly because a lot of energy was spent in managing the communication between dev and QA team and make sure they are really helping each other and not working against one another. In the end what really helped the quality of code is letting developers really work on improving code architecture, removal lots of technical debt, etc. That required temporarily cutting back on the new features and putting more devs on code improvement. That has massively paid off later, when the product went from 1 outage per week to 2 outages per year.

I also worked in places with QA team that was subsequently made redundant (not because they did not work well, but because there was a rule to get rid of 10% of people every year and then perhaps hire new ones - good rule actually). Initially, everyone thought it would be a disaster, but very quickly devs just started to write tests themselves (and there were of much better quality) and we forgot why we ever needed a QA. Our secret then was the ability making releases quickly and ability to roll them back even quicker - something that, of course, might not really apply to Ethereum implementation.

In the third place, there was never a QA, but the lead developer was too strict on accepting changes and quite paranoid, so we spend most of our time waiting for the pull requests to be approved - quite boring and not very rewarding. I never stayed around to see what happened next, bugs were rare, but changes were happening at a glacial pace.

Based on that experience, I am not sure that “QA department” will help a lot. You’ve got to be more creative generally and find solution that suits team and the product.

There is an extra benefit in having multiple teams. They can have different visions and different levels of conservatism, and come up with some radical ideas that look terrible but then turn out to be great. I have some experience with that too ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) Different team leaders have different qualities and attract different kinds of people. I think that is also crucial.

I believe that experimentation with architecture can help a lot. Even though from what [@pipermerriam](/u/pipermerriam) wrote it seems that Ethereum make modular implementation hard, it all depends on finding good abstractions and places to split up the code. I suspect that Geth team has not really been given enough time to do these kind of things and therefore make their code more modular and easier to maintain.

---

**pipermerriam** (2020-07-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/dankrad/48/3288_2.png) dankrad:

> Now you may argue that it can be distributed across more shoulders, but I don’t see why that can’t be the case for a single client?

I believe there is a simple way to refute this approach.  I’m going to make up some numbers here.  The specific numbers aren’t exactly meant to be important, just the way they interact.

Suppose we demand a 99% guarantee of correctness (I know, that reality would have more 9’s but it shouldn’t be important for this exercise).

In the single client world, we have to create one client that achieves the correctness goal.

Now, in a network with three clients, each with equal share of the network, we only fail if two or more clients fail at the same time.  After an embarrassing amount of futzing with the statistics, we achieve the same overall 99% guarantee as long as each of the three clients is at least 94% correct.

The difficulty of improving the correctness is non-linear, meaning as you increase correctness, so does the difficulty of increasing it any further.  By spreading the responsibility out across multiple clients, they each can be less correct and it is my assertion that the overall difficulty is on par or lower to have three clients each with a lower correctness guarantee than to have a single client with an extremely high correctness guarantee.

