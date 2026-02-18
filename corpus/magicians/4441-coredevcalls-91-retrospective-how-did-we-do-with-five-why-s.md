---
source: magicians
topic_id: 4441
title: "CoreDevCalls 91 Retrospective: How did we do with \"Five Why\"s?"
author: AlexeyAkhunov
date: "2020-07-22"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/coredevcalls-91-retrospective-how-did-we-do-with-five-why-s/4441
views: 1350
likes: 4
posts_count: 3
---

# CoreDevCalls 91 Retrospective: How did we do with "Five Why"s?

Here are the notes: [pm/Meeting 91.md at cd5e46d86909e034568ef01b0022def006248e0a · ethereum/pm · GitHub](https://github.com/ethereum/pm/blob/cd5e46d86909e034568ef01b0022def006248e0a/All%20Core%20Devs%20Meetings/Meeting%2091.md)

Ahead of the meeting, [@pipermerriam](/u/pipermerriam) suggested "Five Why"s methodology to drive further discussion and exploration of the problem we are facing and possible causes, because it was observed that at the Meeting 90 we perhaps jumped too quickly to the solutions. So how did we do with "Five Why"s?

First of all, what was the problem? Apparently, it was the fact that most critical installations are running on one implementation of Ethereum, which is go-ethereum, making the stability and performance of the go-ethereum code too important, so that the development team rightly feels too much under pressure. Already after the call, I realised that “most critical installations are running on go-ethereum” is a conjecture, which feels about right, but do not actually have a good data to back it up. Metrics from crawlers, counting number of nodes of certain type found in the network, are not really useful, because they do not tell us what the impact of a code defect in go-ethereum would be. More useful metrics would count the nodes that actually create an impact, i.e. mining pools, exchanges, wallet backends, dapp backends, infra providers, etc.

Assuming that we get data and confirm the problem, the first why would be “Why do most critical installations run on go-ethereum?”. Here is my summary of answers (please let me know if you think there are more):

**1.** go-ethereum is the oldest and most trusted implementation. It is backed by Ethereum Foundation, so unlikely to run out of money.

**2.** No other implementation offers the same functionality and any significant difference in performance or operator’s experience.

**3.** Due to lack of standards in external interfaces (JSON RPC), it is not so easy just to switch the backend.

**4.** Running multiple implementations (to mitigate a risk of code defect in go-ethereum) is extra cost, and not justified from business point of view. This may be because:

**a)** The risk is viewed as systemic, so it would affect everyone, so “why do we need to bother”

**b)** The risk is hard to estimate because there is not reliable data on what is the actual share of each implementation in critical installations.

I do not think we spent any time discussing answer (**1**), because it can only be fixed with time, and with commitment from EF to fund alternatives, which already exists in some form.

During the meeting 91, we mostly talked about answer (**2**), and if we ask “Why?” again, the main answer I read/heard, was:

**2.1** It is just too difficult to write a fully functional performant Ethereum implementation

I think we tried to ask “Why?” again, and this is where we started to disagree on what the main answer is. Here are answers (and they might be contradicting at this point):

**2.1.1.** Ethereum protocol is constructed in such a way - there is something inherent in the design of Ethereum that makes the implementations hard at this point.

**2.1.2.** Volumes of data transfer and computation we are dealing with, requires constant optimisations. And these optimisations inevitably cut across component boundaries and gradually ruin modularity.

**2.1.3.** There is lack of proper analysis of the implementation’s architecture, even though Ethereum is live for 5 years. Lack of “reference architecture” makes it hard to push back against the cross-cutting optimisations and prevents getting specialists to optimise individual components instead.

**2.1.4** The prevailing architecture is wrong, and needs to change to allow cleaner optimisations. It has been noted that the shift to the “flat storage” architecture is gaining pace with go-ethereum introducing snapshots, and turbo-geth getting closer to the first usable version.

I personally agree with (**2.1.3**) and (**2.1.4**) and skeptical about (**2.1.1**) and (**2.1.2**), seeing them more as excuses for why things were not done in a better way, rather than real reasons.

I do not think we went any deeper than that with “Why?”, so we were 3 levels deep ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) Comments welcome!

## Replies

**rai** (2020-07-23):

I’m most interested in your assertion on the call that the correct modularization will actually increase performance. I remember that even after you said it, someone made an argument assuming that it couldn’t be the case. This shows that it’s still counter-intuitive to most. I think one thing that might have been contributing to the increasing monolithicness of clients is the untested assumption that cross-cutting optimizations need to be implemented for performance reasons.

It’s understandable since “modularity causes overhead” is more quickly and frequently encountered by engineers over the observation you made that “modularity causes simplicity causes performance optimizations”.

This is especially true when you compare the turbo-geth mandate to those of most other clients. We walk around in local minima by improving existing structures. Your team has traversed the landscape with (what I assume) was an experimental client that couldn’t have been depended on in the process.

All this to say that now that we know there might be a deeper valley somewhere, that’s awesome! It could be hard to get pack up and move there while delivering other things however.

I support the idea of architecture development and guidance but wanted to offer this observation of how we might have gotten here.

---

**jpitts** (2020-07-24):

Here is the discussion of this topic from today’s ACD meeting:

Discussion at CoreDevCalls #92



Also, general info on the Five Whys Methodology:



      [en.wikipedia.org](https://en.wikipedia.org/wiki/Five_whys)





###

Five whys (or 5 whys) is an iterative interrogative technique used to explore the cause-and-effect relationships underlying a particular problem. The primary goal of the technique is to determine the root cause of a defect or problem by repeating the question "why?" five times, each time directing the current "why" to the answer of the previous "why". The method asserts that the answer to the fifth "why" asked in this manner should reveal the root cause of the problem.
 The technique was describe...

