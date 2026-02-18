---
source: magicians
topic_id: 2962
title: "Ideation session: Reasonably fair algorithm to measure current contribution"
author: jpitts
date: "2019-03-21"
category: Magicians > Primordial Soup
tags: [contributing, ideation]
url: https://ethereum-magicians.org/t/ideation-session-reasonably-fair-algorithm-to-measure-current-contribution/2962
views: 1043
likes: 12
posts_count: 8
---

# Ideation session: Reasonably fair algorithm to measure current contribution

Post ideas about a reasonably fair algorithm to identify contributors and measure current contribution to Ethereum-related work of all kinds.

This algorithm could be run in an oracle and used to allocate community contribution rewards. It would be able to access data from the web or Ethereum mainnet, and track contributors and types of work.

***Please don’t argue about which is good or bad, just reply with ideas.*** I will collect related ideas together for focused evaluation.

## Replies

**lrettig** (2019-03-21):

Spitballing/brainstorming:

- GitHub comments/reviews/merges/commits/etc.
- “Likes” on this forum, ethresear.ch, etc.
- Physical attendance at events
- “Reputation” score of some kind, but this is very hard to measure

---

**alberreman** (2019-03-21):

I mean, I just posted on the ol’ Twitter machine, but I’ll post here too, 'cos why not?

For reputation you could do some kind of Colony-like peer-assigned and review task-based system. The benefit would be accounting of non code-related tasks. It isnt sybil resistant, but you could potentially mitigate attacks/noise if there were recognized stakeholder groups that managed and reported contributions within their groups, and were then probably audited by other peer stakeholder groups. ex: magicians, cat herders, EF, Parity, Geth, maybe a union of open source contributors, etc.

---

**alberreman** (2019-03-21):

maybe a way of coming to this would be to start with an open doc that allowed people to list all of the ways in which a person can “contribute to Ethereum.” And then set out prioritizing that list somehow. fuck it, make it a TCR. Why not? and then come up with ways to measure contribution around all of the significant identified contribution types. but the point would be to start with what we consider valuable contribution. I think we too often just measure the things that seem most easy to measure, regardless of the comparative value we place on those contributions, or the relevance of those contributions to a person’s ability to make certain decisions (assuming that youre looking for contribution measurement approaches to identify decision-makers).

Edited to include my brainstormed list of contribution types:

base level protocol coding

dapp development

ethereum research

cat herders

event organizers

magicians

lobbying groups

dapp users

conference attendees

conference speakers

people who write articles explaining things

working for an ethereum company

buying ether

auditing code

contributing to twitter/reddit/other forums

educating people

---

**jpitts** (2019-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alberreman/48/984_2.png) alberreman:

> I think we too often just measure the things that seem most easy to measure, regardless of the comparative value we place on those contributions, or the relevance of those contributions to a person’s ability to make certain decisions (assuming that youre looking for contribution measurement approaches to identify decision-makers).

We should definitely not be afraid to try our best to measure all the types of contributions that are relevant.

Perhaps those in each field of Ethereum could maintain their own measuring systems, updating their part of the algo, much in the way that Google is constantly updating PageRank.

---

**alberreman** (2019-03-21):

sure - then you would all have to have some way to universalize metrics across and within groups, or it’d get difficult to measure contributing groups against each other. maybe you could identify some meta-level Ethereum purpose/outcomes and prioritize them in some way (TCR or EIP-like process, like Aragon’s AGP process) so that they could be assigned value, and then each contributor group could self organize around how they can contribute to reaching those outcomes. Then individuals within that group would make a claim about their contribution totals which could be audited by the rest of the groups in some way.

---

**jpitts** (2019-03-21):

Inputs, things to measure, things to track over time:

- community priorities, addressed by the work
- the work, quality of the work
- adoption of / use of / dependency on work
- peer review, qualitative and quantitative recognition

Things to counteract:

- distortions caused by social media popularity
- distortions caused by personal choices, e.g. privacy orientation
- stakeholder groups gaming the algo construction process
- gaming of the algo

---

**kronosapiens** (2019-03-25):

If we’re allowed to use an oracle, then I would be quite interested in incorporating a PageRank-style reputation system in which community members can “endorse” other community members and these endorsements are used to generate contribution scores – an endorsement from someone who is also endorsed is worth a lot, while an endorsement from someone who is unendorsed is worth little. The subjectivity gets around the Goodhart-related problems which we get into when we use objective metrics.

It can also be made somewhat sybil-resistant by limiting who gets a contribution score “to start” (i.e. we use objective github data to determine the “starting contribution distribution” and then use the subjective endorsements to distribute the contribution scores beyond what the data themselves can capture). If someone creates a fake account, their endorsements have zero weight until someone endorses them. So not sybil-resistant per-se, but not trivially sybillable either.

I like this idea because it is grounded in something objective (i.e. github contributions) but incorporates subjective information (endorsements) beyond what the objective can provide. It also means that we don’t have to worry about capturing every objective signal as the subjective assessments will “smooth out” the gaps in what the metrics show.

