---
source: magicians
topic_id: 2554
title: The roadmap and dev-led vs. research-led projects
author: lrettig
date: "2019-01-31"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/the-roadmap-and-dev-led-vs-research-led-projects/2554
views: 1364
likes: 11
posts_count: 5
---

# The roadmap and dev-led vs. research-led projects

Attempting to move another interesting Twitter thread over here:

https://twitter.com/lrettig/status/1090720088125292559?s=20

In brief, I feel that a project led by developers would be one in which the roadmap were concrete, with incremental, regular, realistically achievable milestones. Research would be asked to help fill in the gaps, or to improve upon “brute force” stopgap designs put in place by the dev team.

In contrast, a project that’s research led would be more likely to become “detached from reality,” aiming for a conceptually perfect design that is unlikely to translate into a realistic, concrete, deliverable roadmap. In short, devs are more likely to ship.

Clearly this tension exists for a reason and clearly there is great value in both research and development. I can’t help but wonder whether Ethereum has moved a bit too far in the “research-led” direction and whether we wouldn’t be better served by a more dev-led process.

Another way of looking at it is that the research team is doing precisely what they should be doing, but that we should much more aggressively be pursuing Eth1x-style network upgrades and that, in fact, Eth1x should be considered the canonical roadmap until Eth2 has proven viable.

While research is moving well, the dev roadmap seems a bit stuck. I can think of two reasons. 1. Lack of clear leadership/vision/roadmap and 2. Dev teams are overwhelmed & have limited resources

What do others think?

CC [@vbuterin](/u/vbuterin) [@djrtwo](/u/djrtwo)

## Replies

**boris** (2019-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/lrettig/48/14_2.png) lrettig:

> Another way of looking at it is that the research team is doing precisely what they should be doing, but that we should much more aggressively be pursuing Eth1x-style network upgrades and that, in fact, Eth1x should be considered the canonical roadmap until Eth2 has proven viable.

I think this is exactly what a number of us have been feeling. Especially when there isn’t clarity around the transition from one to the other. But, at the same time, we DO want to move towards PoS and other aspects of ETH2 – but can’t wait to improve ETH1x today.

---

**gcolvin** (2019-02-02):

In my experience, big companies and small, the same team (or even person) did research, design, development and maintenance, in overlapping iterations, for the lifetime of the product or system.  And especially in startups a constraint on the design was that it had to be implementable within your remaining runway, which was best assured by implementing designs as you researched them, in a production language, so you could ship a working design as soon as you had one.  Completely separate research departments were rare.

---

**gcolvin** (2019-02-02):

[Software Engineering at Google](https://arxiv.org/pdf/1702.01715.pdf)

**Research Scientist**

The hiring criteria for this role are very strict, and the bar is extremely high, requiring demonstrated exceptional research ability evidenced by a great publication record *and* ability to write code. Many very talented people in academia who would be able to qualify for a Software Engineer role would not qualify for a Research Scientist role at Google; most of the people with PhDs at Google are Software Engineers rather than Research Scientists. Research scientists are evaluated on their research contributions, including their publications, but apart from that and the different title, there is not really that much difference between the Software Engineer and Research Scientist role at Google. Both can do original research and publish papers, both can develop new product ideas and new technologies, and both can and do write code and develop products. Research Scientists at Google usually work alongside Software Engineers, in the same teams and working on the same products or the same research. This practice of embedding research within engineering contributes greatly to the ease with which new research can be incorporated into shipping products

---

**gcolvin** (2019-02-09):

[@lrettig](/u/lrettig) [@boris](/u/boris) [@djrtwo](/u/djrtwo)  [@vbuterin](/u/vbuterin)

Been thinking on the lessons of my two posts here for a while. These are very much personal observations, some of them under-informed in such a large community.

From what I hear of the current Ethereum its birth was like my experience in small startups: all phases of development ran concurrently and iteratively, with little by way of a roadmap, but solid science, maximum vision and motivation, and hard deadlines.

Then we had to slow down, but we still have to maintain both a steady pace of innovation and assurance of stability for our users.  This takes successful R&D.  I picked Google as just one well-publicized example of a common approach to success.

The way the client teams are working with Research looks good that way, and with increasingly effective and open communications and organization.  Research is in effect the Eth 2.0 development team.  What seems to be missing is a steady pace of delivery and solid commitment to backwards compatibility.  This is of course difficult when designing a completely new system.

For 1.0 development the client teams and the community remain a source of new ideas which are being incrementally added to the current system.  There I see researchers and developers being mostly the same people.  We are getting our communications and organization together, with the Magicians and 1.x efforts, and are moving quickly in the face of a looming scalability crisis.  We face the limitations of working with an existing design, and strong requirements for backwards compatibility.

The 1.0 development doesn’t seem to have strong connections with the Research group, except where the same people participate in both groups.  We even face some lack of buy-in due to the false belief in much of the community that Eth 1.0 will be completely replaced by Eth 2.0 in just two or three years.  This also reduces the motivation to build new applications on the 1.0 platform, for fear that they will be made obsolete by the success of 2.0, or will fail along with the rest of Ethereum if 2.0 is not delivered.

A problem for most all Layer 1 development is that it did not get what a for-profit company gets out of initial success–capital and profits to fund further development.  The client teams seem to operate on a shoestring, making plans based on their lack of resources rather their abundant or at least adequate resources.

