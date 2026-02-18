---
source: magicians
topic_id: 2232
title: "Hypothetical: If ethereum core governance was a meritocracy, what would constitute merit / reputation?"
author: auryn
date: "2018-12-17"
category: Magicians > Primordial Soup
tags: [reputation-systems]
url: https://ethereum-magicians.org/t/hypothetical-if-ethereum-core-governance-was-a-meritocracy-what-would-constitute-merit-reputation/2232
views: 797
likes: 3
posts_count: 9
---

# Hypothetical: If ethereum core governance was a meritocracy, what would constitute merit / reputation?

Defining how one’s voice should be weighted seems like a necessary first step to implementing a governance solution that extends beyond the implicit governance of networks; people’s ability to vote with their feet / fork.

As a hypothetical scenario, let’s assume that Ethereum core governance should be meritocratic.

---

By what metric should we measure merit in order to award reputation / voting weight?

---

How should we account for contributions that occurred prior to the implementation of this meritocracy?

---

## Replies

**jpitts** (2018-12-17):

Are you describing an *on-chain* meritocratic governance solution?

A good place to start is to understand how decisions are made now, among people. Generally, those participating in the core devs group are able to come to a decision based on discussions among well-informed and trusted peers. There are not many barriers to joining these discussions, but there is a meritocracy informally maintained in the discussions themselves.

In order to achieve the highest possible quality of governance decisions, each participant must be able to follow the logic of a particular discussion and relate it to the greater context of the Ethereum protocol and ecosystem. Participants judge the specific points that are made and determine their weight or bearing on the general direction of the discussion; first by knowing who made the point, and then by interpreting the content of the point. This point-by-point judgement requires a lot of experience with each other, and with the technical material at hand.

From that process, the group is able to come to a decision on a protocol change, by rough consensus, without even voting.

---

**auryn** (2018-12-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> Are you describing an on-chain meritocratic governance solution?

I deliberately didn’t specify implementation details (on-chain vs off-chain, etc.) because I do not think it is necessarily relevant to the questions.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> there is a meritocracy informally maintained in the discussions themselves.

This hints at what I was asking.

There is an informal meritocracy; each person’s voice is essentially weighted by their reputation with others within the group.

But could we tease out informal reputation and formalize into a metric which can transparently give weight to each voice?

---

**AtLeastSignificant** (2018-12-19):

I don’t think this is a very hypothetical scenario.  There are two main players when it comes to governance - the decision makers (core devs / client creators) and the enforcers (miners).

It’s been observed time and time again that the majority of enforcers are either apathetic to governance changes, or purposefully side with core dev decisions.  I personally believe it’s apathy, but until we have signals for yes/no/abstain AND “no vote”, it’s hard to support that argument.  For those who are not apathetic, there is a strong financial incentive to follow core dev decisions due to a number of reasons.

So, if we assume the enforcers are always going to side with the decision makers, then there is really only a single governance entity (although it itself is not a single body).  Still, this entity is comprised of a narrow slice of users/developers that do not really reflect the demographic using Ethereum.

This group of core devs / client creators inhrently have a meritocracy though, like [@jpitts](/u/jpitts) is saying.  They don’t need even an informal system to determine who is consistently presenting logical discussions and valuable research.  I don’t think it’s a stretch to say that people like Vitalik rank quite high on this totem pole, while an anonymous redditor probably ranks fairly low (regardless of arguments being presented).   This is the “rough consensus” that was not accidental, but planned from the start.

To an outsider though, it certainly looks and behaves like a benevolent oligarchy.

---

**auryn** (2018-12-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/atleastsignificant/48/219_2.png) AtLeastSignificant:

> They don’t need even an informal system to determine who is consistently presenting logical discussions and valuable research.

Subjectively determining who is consistently presenting logical discussions and valuable research is an informal system in and of itself.

Is it possible create a quantifiable metric from this informal system?

Would that metric be sufficiant to guide governance?

---

**AtLeastSignificant** (2018-12-20):

I think it only works because it’s informal.

---

**auryn** (2018-12-21):

Does this informal nature limit the scalability, efficiency, and/or efficacy of this governance model?

If so, are there any acceptable trade-offs to improve scalability, efficiency, and/or efficacy?

---

**boris** (2018-12-22):

The scope of core governance matters. Right now, it’s mainly concentrated on acceptance of Core EIPs, and then scheduling of those EIPs for a hard fork.

(In the middle of that is the looser question of when to implement a new feature / EIP, which happens internally to each client team)

So, “Governance over what?” Becomes a useful question.

For example, who might have reputation around what projects get long term funding by a public treasury?

---

**auryn** (2018-12-26):

Agreed, governance over what is an important question.

For the sake of the example, let’s assume no public treasury.

Rather, let’s a assume a core dev team that exists largely as it does today; an ad-hoc group of self-interested / self-motivated participants. Let’s also assume that core governance is concerned primarily with acceptance of EIPs and, mroe broadly, ethereum’s roadmap.

