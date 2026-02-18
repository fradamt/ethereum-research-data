---
source: magicians
topic_id: 1810
title: Data standardization with a rough consensus
author: vlad-kahoun
date: "2018-11-05"
category: Working Groups > Data Ring
tags: []
url: https://ethereum-magicians.org/t/data-standardization-with-a-rough-consensus/1810
views: 839
likes: 1
posts_count: 2
---

# Data standardization with a rough consensus

I suppose we agree that dApps and platforms need to cooperate with each other. It’s not possible now, because they use different formats of messages. I think that we need an abstraction layer – middleware - that can translate various data/message standards between each other. As a result everyone’s idea can become a standard, protocol or feature understandable to other parts of the system.

I’m working on that kind of middleware (please see my introduction: https://ethereum-magicians.org/t/the-big-introduce-yourself-thread/75/66?u=vlad-kahoun) and I’m happy to create a working group to discuss and cooperate with others interested in the topic and various ways to solve standardization. Please let me know here in discussion or message me if you’re interested to discuss further, so we can set up our communication.

**There are at least 3 ways to establish standards**

1. Directive – when a strong organization introduces and pushes a new standard.
2. Consensual – when a diverse group of people/organizations agree on the best standard for a particular purpose (e.g. the standard for bounties).
3. The 3th way is based on a rough consensus. It means that the best standard is not decided in advance. Instead, anyone can introduce his own standard and the successful ones are the standards used by the most clients and platforms.

I propose the 3th way as a solution for standardization because it enables anyone to create better standard/language while being still understood by all other parts of the system. This approach will be possible once we have the abstraction middleware that can translate one standard to another, even in a multi-hop manner.

The translation middleware is useful mainly for off-chain data, meta-data in transactions and all messages exchanged between various clients and platforms.

There is a description of an example client backed by the middleware: https://github.com/unfwk/jekyll

## Replies

**jpitts** (2019-03-02):

[@vlad-kahoun](/u/vlad-kahoun) my apologies for not replying earlier. We definitely do believe in “rough consensus and running code”, and hope that all Rings use it. More so, that Rings find rough consensus in person with a final decision only happening here on the Forum, so that all can participate.

Principles of the Fellowship: https://github.com/ethereum-magicians/scrolls/wiki/Principles-of-the-Fellowship

