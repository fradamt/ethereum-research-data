---
source: magicians
topic_id: 1860
title: Separating EIPs and ERCs
author: ligi
date: "2018-11-09"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/separating-eips-and-ercs/1860
views: 652
likes: 5
posts_count: 5
---

# Separating EIPs and ERCs

As this was just briefly topic at the end of the AllCoreDevs meeting just now (and the idea there was also to bring it up here) - I am opening this discussion with this post. I am still a very big fan of this idea. Started an initiative for this a while ago:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/896)












####



        opened 12:00AM - 22 Feb 18 UTC



          closed 11:11PM - 01 Jan 22 UTC



        [![](https://avatars.githubusercontent.com/u/111600?v=4)
          ligi](https://github.com/ligi)





          stale







This is a proposal to split the EIP process in **E**thereum **P**roposals for **[…]()I**nterfaces of **C**ontracts that only specify contract interfaces (think ERC #20,ERC #721,ERC #801,..) and other EIPs (no change here).
This will have the following advantages:
 1. easier to find and get an overview of all contract interfaces (my current pain point)
 2. can be less opinionated than changes that might fork hard -> less governance pain
 3. less noise when you want to keep up to date if you are just interested in contract interfaces (could improve interoperability between projects/contracts - not all contract devs can read all EIPs)
 4. maybe less potential legal problems (but IANAL!) could also help getting very talented editors back on board that just have problems with certain kind of proposals (cc @pirapira)
 5. less work for editors involved in this process
 6. more decentralized in a sense
 7. smaller numbers - easier to remember interface numbers - when being embedded in EIP process we get into 4 digits soon
 8. easier to require formal defaults like methods and events

To decease mental workload requirements for the transition we could use the old numbers - but fill the gaps (see point 7)

ERC-20 -> EPIC-20
ERC-721 -> EPIC-721
ERC-801 -> EPIC-801

Opinions and links to EIPs that could become EPIC very welcome! Was on the search for EIPs that define contract interfaces and this is possible but painful manual work - one reason for this very proposal.












People liked it (just some bike-shedding around the naming) - but I am not sure about how to roll this change out - this was also the reason I did not proceed with it. If anyone has an idea how to actually roll this out: please shoot!

## Replies

**boris** (2018-11-09):

Run both in the EIPs repo. But have more clearly defined separate tracks. Have ERC editors separate from EIP editors (although both have power to help each other out with the basics).

I have an edit in progress to track and bring in more specifications — JSON-RPC, devp2p, whisper. So that everything to build a compliant and compatible Ethereum client is in one place.


      [github.com](https://github.com/spadebuilders/EIPs/blob/specs-and-standards/README.md)




####

```md
# EIPs [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ethereum/EIPs?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
Ethereum Improvement Proposals (EIPs) describe standards for the Ethereum platform, including core protocol specifications, client APIs, and contract standards.

A browsable version of all current and draft EIPs can be found on [the official EIP site](http://eips.ethereum.org/).

# Standards and Specifications

Aside from improving and upgrading the Ethereum platform, the goal of the EIP process is to document the standards and specifications that define it. Following these specifications, an implementation team should be able to build interoperable components that connect to the Ethereum main net, various test nets, and other layers of the Ethereum network.

The list of Ethereum components is as follows. Each component may have a different process for maintenance and updates, but will create or update EIPs to reflect changes.

* formal specification https://github.com/ethereum/yellowpaper
* devp2p https://github.com/ethereum/wiki/wiki/%C3%90%CE%9EVp2p-Wire-Protocol
* Light Ethereum Subprotocol https://github.com/ethereum/wiki/wiki/Light-client-protocol
* whisper https://github.com/ethereum/go-ethereum/wiki/Whisper-Overview
* swarm https://github.com/ethereum/go-ethereum/pull/2959
* API/RPC https://github.com/ethereum/wiki/wiki/JSON-RPC
* contract ABIs https://github.com/ethereum/wiki/wiki/Ethereum-Contract-ABI
```

  This file has been truncated. [show original](https://github.com/spadebuilders/EIPs/blob/specs-and-standards/README.md)








I’m up for discussing and helping with this.

---

**ligi** (2018-11-10):

I think they should not reside in the same space. Really separating them has some advantages - e.g. something trivial like smaller numbers that are easier to remember ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)  - also I think it makes the process more agile as one group can move/change processes without influencing the other one.

---

**boris** (2018-11-11):

So, separate repos for each type of specs? I’m not super tied to one approach or the other, but i believe that there aren’t enough people involved in the process today, and splitting it means there will be even less.

And that coordinating in general will be harder.

Do you have some specific thoughts of how this would work? How do we brainstorm approaches?

More broadly — who cares enough to help?

---

**ligi** (2018-11-11):

Ya - splitting it in very fine granularity would not be good. I would just split in 2 parts (for now) - EIPs and contract interfaces. In the EIPs we could still go track route you suggested. But I think contract interfaces should be really split out already.

