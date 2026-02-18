---
source: magicians
topic_id: 1273
title: Informal Meetup of Ethereum Architects in Berlin 10.09.2018 15:00 in ! America Memorial Library
author: Ethernian
date: "2018-09-08"
category: Working Groups > Ethereum Architects
tags: []
url: https://ethereum-magicians.org/t/informal-meetup-of-ethereum-architects-in-berlin-10-09-2018-15-00-in-america-memorial-library/1273
views: 1185
likes: 4
posts_count: 12
---

# Informal Meetup of Ethereum Architects in Berlin 10.09.2018 15:00 in ! America Memorial Library

As already mentioned, there are two topics I would start with in Ring of EAs:

1. Categorize (tagging) EIPs
2. Create a list of Ethereum Projects useful as a good examples for Ethereum Architecture.

I think both of tasks can be organized and incentivised as TCR or similar and see it a funny exersize in tokenomics.

I am in Berlin until at least 10.09.2018 (most probably more).

Is somebody is interested to meet in person and brainstorm in details how to do it?

Any other ideas are welcome as well.

## Replies

**aogunwole** (2018-09-08):

I’m up for #1. I think it’s super important to start helping people find and follow EIPs.

I’m based in Berlin but pretty busy with ETH Berlin. Are you free at all the day of the 10th to meet?

---

**Ethernian** (2018-09-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/aogunwole/48/429_2.png) aogunwole:

> Are you free at all the day of the 10th to meet?

on 10th afternoon should be OK.

Anyone else would like to meet?

---

**aogunwole** (2018-09-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> on 10th afternoon should be OK.

Cool. Let me know what time? I’m heading to a token engineering workshop after 5pm.

---

**Ethernian** (2018-09-09):

> I’m heading to a token engineering workshop after 5pm.

then let’s do it  before the workshop. at 3-5pm. Where?

---

**aogunwole** (2018-09-09):

How about Full Node at 3pm then?

---

**Ethernian** (2018-09-09):

ok. agree.

=== 20 chars nonce ===

---

**aogunwole** (2018-09-11):

Here are my notes from our first meetup yesterday on tagging/taxonomy for EIPs. Feel free to add to this or change if I misinterpreted anything from the discussion. Hopefully with our next discussion, we can get closer to having an MVP for the taxonomy

EIPs Taxonomy Discussion

4 types of tagging/taxonomy categories for each EIP:

1. Status: At what stage of review or implementation is this EIP?  Examples - submitted, read, finalized, rejected, etc.This category already exists in the EIP repository.
2. Context - What is the subject matter of this EIP/what aspect of the technology is this EIP addressing? Examples - Wallet, Security, Token, UI, etc.  We could subsequently create a link to the community(ies) that are most impacted by this EIP (FEM Wallet Ring, Gitter Communities, etc.)
3. Impact : At what technical criticality will this EIP require if implemented? Examples - Hard Fork, Asthetic Design Only, etc.
4. Notification Level: For the stakeholders affected, what type of notification should they receive? Example: Notification to update code base, awareness notification only, etc. Note - we would need to include a list of which stakeholders are impacted.

3 Groups As Targets for Understanding this taxanomy for EIPs:

1. Author
2. Editors from Core Devs
3. Supporting Groups

*Note - most of the taxanomy, specifically for the Context category, can be derived from supporting communities to then notify the communities involved on if they are impacted, However, the tags themselves should be stored centrally on the EIPs Github.*

Editors should decide and add high level tags, interested supporting groups/communities can add further granular tags for their interest.

Example: EIP editor adds a tag “Security” to an EIP, an FEM Security Ring member adds a tag for “User Facing” to that EIP.

Oustanding Questions:

- How do the analyze which tags are most used so that they get mass adoption? Do they need to be promoted i.e a system of “liking” a tag? Or will the natural order progress them already?
- Who will have access to create tags? The entire community? Just Editors?

---

**Ethernian** (2018-09-12):

//Work in Progress

Thank you, [@aogunwole](/u/aogunwole) for your help and your feedback!

Here are more notes from my side from the brainstorming:

**Why do we need better EIP tagging:**

1. There are too much EIPs.
Some of them MUST be reviewed by whole community because of their global impact, but many of them - do not. This mix causes a huge overhead making community member read every EIPs.
An Moderator could place tags on EIP, signalling to other community members what they should read and what not. It will save time and efforts in whole community.
2. In order to detect duplicates, an Moderator must know all EIPs, which is quite a lot. Every new Moderator must currently read and understand all existing EIPs to detect duplicates, which is a lot too.
Tagging could help an Moderator to find related EIPs quickly.

**Delegated Tagging**

It is wrong to expect from the someone to understand all tags in all knowledge areas. The tagging works well only inside the community undestanding the tagging scheme.

Therefore it is the task for Moderators in the specific community to read all related EIPs and set community specific tags.

Moderators from other communities should only know top-level tags from each other in order to mark EIPs as related to responsible community.

If some community has no suitable tag to watch on, it creates a new one and promotes it globally among all other Moderators and asks them to tag EIPs accordingly, creating a signal for this community.

A small fee can be paid from community to external Moderator for this pre-selection, because it safes time and efforts of community members.

---

**aogunwole** (2018-09-21):

Thinking about this again [@Ethernian](/u/ethernian), I wonder if we should create an EIP actually to address this? Based on our notes there are two main issues that need to be addressed:

1. Too many EIPs with varying significance on the community.
2. Too hard to quickly understand the relevance of each EIP as it pertains to those in the community who may be interested in that EIP’s progress.

I just started reviewing all of the current EIPs in the entire repository and it really is a mixed bag. Even from a basic sorting stand point (which EIPs are completed are mixed in with which EIPs are in progress in one large list) it’s hard to digest what has been submitted, what was rejected, what is in on the roadmap. It would be a significant undertaking to not only tag each EIP for context and stage, but also understand the impact of each EIP. I think it would good to raise this concern directly with the core devs group so that we can partner together on how to address this systemically, openly, and with a lot of participation.

What do you think?

---

**Ethernian** (2018-09-22):

Ha!

There is a funny self-recursive problem there!

I think, such EIP will not be accepted because even it targets a real problem, there is no formal proposal how to solve it. This is exactly what I am working on currently: specification of decentralized tagging process.

As a one of the goals I aim is to make it easier to create some preliminary EIPs drafts (and not be spammed by them).

The EIP you propose is currently in very beginning of its implementation but the problem is already clear. It may be not ready for publication in terms of EIP-1. Nevertheless it should allow to publish such kind of preliminary EIPs, so it could be one of this kind.

good point, let us do it.

I would suggest, let us create a new PM thread for us two, where we put two our visions into one combined text and then publish a new separate topic for further discussion.

---

**aogunwole** (2018-09-24):

Sounds good! Once you create the thread I’ll add on

