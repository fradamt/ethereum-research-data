---
source: ethresearch
topic_id: 4325
title: Are "Elon Musk VDFs" feasible?
author: kladkogex
date: "2018-11-21"
category: Security
tags: []
url: https://ethresear.ch/t/are-elon-musk-vdfs-feasible/4325
views: 2360
likes: 4
posts_count: 5
---

# Are "Elon Musk VDFs" feasible?

It was announced during the DevCon4 that ETH foundation together with Filecoin is going to spend $20M on hardware based verifiable delay functions.

Arguably the speed of light provides one of the best VDFS, because it is impossible to go faster than the speed of light.  The question is then, is it feasible to create a VDF by placing satellites on orbit?

In particular, if there are multiple satellites forming a mesh network,  one can form a verifiable delay function based on message hopping from one satellite to another and getting signed every time.

Since the costs of sending a mini satellite is as [as low as $25,000](https://www.fool.com/investing/general/2016/05/22/got-25000-then-you-can-build-a-satellite-and-a-spa.aspx), it may be well possible that such a network of say 100 satellites could be launched for < $20M (?).

Each satellite would have an opensource specification and a zero gravity detector.  Once the zero gravity detector would detect absence of gravity for an extended period of time, it would generate the private key inside a smartcard chip. The key would be used to sign all messages passing through the satellite.

## Replies

**vbuterin** (2018-11-21):

I think that would require trust assumptions involving where the satellites are, and that the satellites will stay operational and follow the protocol.

---

**PaulRBerg** (2018-11-21):

It’s definitely more than $20M, given the overhead costs in [long-term maintenance](https://space.stackexchange.com/questions/2869/how-much-does-it-cost-to-operate-a-satellite-in-orbit) and hiring the right people, from technical expertise to legal matters.

Relying on unmanned objects some hundred kilometres above the surface of the Earth doesn’t sound “WW3 bulletproof”.

---

**kladkogex** (2018-11-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I think that would require trust assumptions involving where the satellites are

I think the model could to have satellites independently owned by stakers, so that would be decentralized network of satellites.

One would need to create some kind of a trusted launch procedure ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kladkogex** (2018-11-23):

Turns out something like that already is being built

http://www.southgatearc.org/news/2018/november/spacechain-foundation-advances-blockchain-based-satellite-network.htm#.W_fwNd9fhhE

One can live-track their first node


      ![image](https://spacechain.com/wp-content/uploads/2018/07/cropped-favicospc-32x32.png)
      [SpaceChain](https://spacechain.com/space-node/)


    ![image](https://forms.aweber.com/form/displays.htm?id=jMyMjExsrCzsDA==)

###

SpaceChain is building the world’s first open-source satellite network to enable a next-generation infrastructure for blockchain industry.

