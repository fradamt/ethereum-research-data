---
source: magicians
topic_id: 1008
title: "Forming a Ring: State Channels"
author: eolszewski
date: "2018-08-10"
category: Working Groups
tags: [state-channels-ring]
url: https://ethereum-magicians.org/t/forming-a-ring-state-channels/1008
views: 755
likes: 7
posts_count: 6
---

# Forming a Ring: State Channels

There are a number of companies working on Payment and State Channels right now and I wish to assemble a ring to promote open standards for state management, griefing, channel integration, etc… through clear code examples and documentation. Who’s in?

Follow on:

The biggest hurdle I see (at present) is the fact that a lot of these projects are running into sadness with griefing whereby they need to deploy contracts for an adjudication process. I think we can mitigate these deployments through raising the cost of griefing through an additional bond in each channel - the implementation details of this being left up to the implementer.

## Replies

**ameensol** (2018-08-11):

With all due respect, this isn’t even close to the most important priority for anyone doing real work on channels right now. We don’t need “open standards” that aren’t informed by real world usage, because then we’re just speculating about the real world usage. The risk that we’ll have to change something is high, and the cost of collaboration along the way is also high, meaning prioritizing forming a ring around this would actually only serve to slow everyone down for no reason.

Much more immediately important is putting channels in front of real users and seeing what sticks. If you *actually* care about pushing this forward, work full-time alongside Connext, Kyokan, and SpankChain as we upgrade our production payment channel hubs, or with one of the other teams close to shipping a production channel implementation.

It’s not as sexy as “bringing everyone together”, but making progress isn’t always sexy.

[Edit] Actually in this *specific* case, making progress on SpankChain’s tech might actually be sexier ![:sunglasses:](https://ethereum-magicians.org/images/emoji/twitter/sunglasses.png?v=9)

---

**eolszewski** (2018-08-11):

There are a number of things that are coming out of the work that is being done throughout these collaborations that will undoubtedly be important for developers and companies to incorporate into their individual architectures. I’m advocating that companies provide good documentation and code samples as they build out their individual implementations in a http://learnchannels.org/ - like fashion.

I agree about getting things done, and we can get things done while not going down a path where we get to a ‘best viewed in Internet explorer’ world. In terms of working alongside companies, I agree, and will help y’all with tests and formalization of some of your code **when you push it** ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9)

---

**jpitts** (2018-08-12):

When users have to manage a multitude of complex things of a category, it is crucial that there is some coordination amongst the developers. Do you know of cases in which the state channel devs are coordinating? Is there any work done or thoughts written about what the user experience will be like?

In this case, the builders of the desktop and mobile dapp browsers (and other user-centered gateways) can be approached for this ring.

---

**compscidr** (2018-08-17):

Definitely interested in this topic - if you’re in Prague around DevCon, let’s connect.

---

**eolszewski** (2018-08-19):

There are some efforts around cooperation, but mostly, no. I’m trying to put out content on medium and twitter discussing some of the work in the space and syndicate teams’ work between each other. I think I may be getting some grant to do this a bit more formally, which would be chill and add some legitimacy to the cause ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=9)

The user experience should be as though they are using a normal application without having to eat the cost and latency of the blockchain.

