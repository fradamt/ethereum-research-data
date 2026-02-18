---
source: magicians
topic_id: 2442
title: "[Council of Paris 2019] Call for Agenda topics"
author: Ethernian
date: "2019-01-16"
category: Protocol Calls & happenings
tags: [council-paris-2019]
url: https://ethereum-magicians.org/t/council-of-paris-2019-call-for-agenda-topics/2442
views: 2248
likes: 10
posts_count: 23
---

# [Council of Paris 2019] Call for Agenda topics

Council of Ethereum Magicians supposed to be different from usual Conference with pre-approved speakers and audience listening to that speakers to. The goal of the Council is to facilitate communication in the community across usual circles and groups. It gives anyone a chance to be heard, to understand concerns of others, to find colleagues to work together on some topic or start a new one.

In order to archive this goal, I would propose to create an open list of discussion topics, where anyone is eligible to add a new topic or signal an interest to already existing one. As the result we will have list of topics, ordered by number of people are interested in. Time slots will be assigned accordingly to the public interest.

A single discussion topic could be described like:

1. ShortName - short unique name of the topic used as reference.
2. Description - briefly description of the problem to be discussed (100 words max).
3. TargetAudience - who are expected (in keywords).
Example: CoreDevs, Anyone.

A voting for discussion topic could be expressed by:

1. Name - a FEM user name
2. Speaker/Listener Flag (S/L) - “S” - I would talk. “L” - I would listen only.
This should help to arrange seats for big discussions accordingly.

If you have objections against this proposal in general please let me know.

## Replies

**mariapaulafn** (2019-01-22):

Hi there, I’ll make a doc with the old rings, and whoever wants to propose can just add their own ring and promote it. Ultimately, the rings with the most people will be selected.

Agreed we shouldnt do any curation of topics ourselves, as you suggest, but let the people by majority of interest see what’s valuable for them and what’s not. It’s also the simplest way.

However, I set up the usual format to do this,[please use this document.](https://hackmd.io/s/ByIVnZVdX)

---

**Ethernian** (2019-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> Hi there, I’ll make a doc with the old rings, and whoever wants to propose can just add their own ring and promote it. Ultimately, the rings with the most people will be selected.

I would really do both: rings and topics. Rings are permanent working groups but we also have new and important topics worth to discuss. Here are few of this:

### Discussion Topics:

1. “Immutables, invariants, and upgradability”
Last EIP-1283 reentrancy bug makes a clear need to discuss about what do we assume to be immutable, what is our social contract with devs and users and how can we upgrade them all.
2. “Whisper-v2: Unified secure messaging layer for dAPPs. Requirements and implementation.”.
Currently Whisper adoptions stocks. Many projects decided to implementing own Secure Messaging instead of the default one. What is the reason? How can we improve Ethereum Secure Messaging to fit most requirements? How requirements on Secure Messaging changed with introducing L2-layer?

---

**mariapaulafn** (2019-01-22):

Rings are formed around topics. What’s the rationale here?

Would you like to present yourself, or to do open discussions?

In the case of the second one, Rings = Topics

Is this what you’re thinking?

Either way, in the hackMD doc there is a google form to submit, so I got everything in one place.

---

**Ethernian** (2019-01-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> Rings are formed around topics. What’s the rationale here?

Rings are meant to be permanent and regular work groups. It doesn’t make sense to create a new ring for every new topics.  Look at the discussions here to topics about Constantinople upgrade: a lot of postings but no one ring has expressed an ownership of it. It is a sign, that these topics do not fit into any ring currently. May be because that topics require broader discussion?

I think we should have a chance to discuss topics ad-hoc (i.e. out of Rings) and let Rings picks them for permanent work after that.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> Would you like to present yourself, or to do open discussions?
> In the case of the second one, Rings = Topics

It is definitely not about presentation of myself.

Look at the most frequent Constantinople topics - they are not in any Ring yet. They need to be discussed, but where? Should it be rip it apart just because of our current Ring Structure?

Some Topics <> Rings.

---

**mariapaulafn** (2019-01-22):

The topics are discussed in rings, I dont see an issue here, if you propose a different discussion format. But “Topics” is not a discussion format.

Eg. 2.0 was discussed on a fishbowl format.

Please suggest topics and discussion formats to guide people better.

---

**jpitts** (2019-01-22):

IMO, it is probably better to highlight the key topic e.g. “Data Ring: Focusing on State Rent” or “Eth 1.x: Fishbowl Q&A”, even if it is basically a gathering around a permanent Ring. In more mature standards bodies there is much stronger difference, the terminology often used is “Working Group” vs. more short-term “Task Force”.

At the in-person event, the agenda is flexible and we should channel people to where they’d contribute the most, set the tone for the specific work to be done.

But here on the Forum I would only create new categories for what is clearly a permanent Ring.

---

**Ethernian** (2019-01-22):

Look at the structure of our current forum: Rings is only part of it and do not contains all Topics. There is life out of Rings.

We have interesting topics in [Primordial Soup](https://ethereum-magicians.org/c/primordial-soup) - and they do not belongs explicitly to any Ring, but worth of discussion, like “[Meta: we should value privacy more](https://ethereum-magicians.org/t/meta-we-should-value-privacy-more/2475)” or “[EEP-5: Ethereum Hardfork Process - request for collaboration](https://ethereum-magicians.org/t/eep-5-ethereum-hardfork-process-request-for-collaboration/2305)”

Some topics are formally in the [EIPs](https://ethereum-magicians.org/c/eips), but related to many Rings. Examples? Here they are: [Immutables, invariants, and upgradability](https://ethereum-magicians.org/t/immutables-invariants-and-upgradability/2440/48) (Rings: EIPs, Security, EVM Evolution) or [EIP-1102: Opt-in provider acces](https://ethereum-magicians.org/t/eip-1102-opt-in-provider-access/414) (Rings: EIPs, Security, Wallets). So it is in nature of our topic to be in no Rings (at very beginning) or to be related to many of them if interdisciplinary.

I am quite neutral to see Rings as Topics or as a Work Groups. But somehow we should assign time slots to important topics even they are out of any Rings or in many Rings. In the model Rings==Topics proposed by [@mariapaulafn](/u/mariapaulafn) those topic should be either discussed multiple time in each Ring, assigned to one of possible Rings (ignoring other aspects) or create a new Ring dedicated to topic. Not really ideal.

I would propose to have both:

- Topics may be proposed for discussion in some Ring internally (as usual)
- Topics may be proposed out of any Rings or as interdisciplinary topics (many Rings).
- Rings may claim responsibility for Topics.

Ring-internal topics will be grouped. For interdisciplinary Topics we will try to make joint-sessions with many Rings.

My proposal is topic focused: I would like to see discussions about topics that are hot right now, no matter what Ring they are in.

---

**mariapaulafn** (2019-01-23):

I think what you are proposing is valid, but you are missing the point of what is proper event agenda structuring, and maybe losing focus. As [@jpitts](/u/jpitts) suggests, we need an agenda, and then in the in-person can allow room as well. However I would assess potential topics online, as this is what I think:

I get that topics are very important to you, but topics are what we discuss in the forum. if a topic evolves enough, by all means, propose it via the form. You need to format those topics into standard in-person discussion formats. Yes, you can throw around topics, but i think the forum has reached critical mass to discuss beforehand online - especially with a month in advance - and take it from there.

Proposals will be taken from the form, and need a discussion format. The proposal can be topic-oriented, there is no ring or discussion without a topic! Maybe there’s a language barrier here I’m not identifying?

However, I would appreciate it if my direction is accepted, aside from your view on topics that I believe it might be misinterpreted by different notions of the word and what it means to you and to me, as this discussion is deriving us from what I need to do here: get the agenda up and running.

---

**mariapaulafn** (2019-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ethernian/48/195_2.png) Ethernian:

> In the model Rings==Topics proposed by @mariapaulafn those topic should be either discussed multiple time in each Ring, assigned to one of possible Rings (ignoring other aspects) or create a new Ring dedicated to topic.

This is not the only model proposed, it was a question. Please suggest topic + format or discuss topics online in the forum, as I mention on the post above. A list of topics floating around and no structure won’t help anyone. Breaking down topics by opening forums and discussing if there is an interest to discuss them,that helps.

---

**tomislavmamic** (2019-01-23):

I’ve read the discussion again and took a look at our [ring list hackmd document](https://hackmd.io/s/ByIVnZVdX). It seems to me that people are not really filling in the rings document (I see only 3 participants signing up)… Maybe I am wrong but, ever since they were proposed in Berlin we have this problem of keeping the rings going. What I mean is, there are only a handful of individuals relatively devoted to keeping rings going. Majority of people just want to show up and discuss.

Also, I don’t see people really voting on these topic proposals.

How do we achieve more engagement of people in making the gathering better?

How do we achieve a greater impact without repelling people with responsibilities?

We have to keep in mind that whatever the formats we choose, the gathering should enable lively discussions and facilitate our passion for solving common problems.

We have done our best to find the fitting format for our gatherings, and I believe rings are ultimately it. But if people are not eager to sign up and take on the responsibility of a ring (which are greater than the ones of the one-off ad hoc discussions), we might have to continue adapting. Having well defined and repeating structure will make a lot of sense once we have a well-oiled machine running. But we are not there yet.

There is an issue with one-off discussions. They have less impact than rings. Their biggest benefit might be that they bring people’s understanding together and open their perspective but they lack the immediate means for creating a lasting impact.

This is all theoretical. Maybe the ETH2.0 discussion from Prague had a bigger impact than any of the rings. We might never know.

The structure and the content of our agenda will have the biggest impact on the successfulness of this gathering and we need to take that into consideration when making these decisions.

I hope I am just stating the obvious.

We can’t really stop people from having off-topic discussions, and we really shouldn’t. The most lively and lasting discussion at the first FEM gathering in Paris last year happened in the yard, quasi-spontaneously. If we don’t include it on the agenda, people we find ways to do it anyways, and if there is no designated time for this, they might skip ring sessions to do it.

---

**mariapaulafn** (2019-01-23):

Just FYI, i havent promoted the hackmd or the form yet, because i want to sort out this disucssion better. and it was published yesterday. i expect to promote this after Görlicon next Thursday when I’ll be able to focus on this again

---

**boris** (2019-01-23):

[@Ethernian](/u/ethernian) if you want a session around State Rent (for example) — put it in the doc in the same way Rings are. I think that’s the misunderstanding.

[@mariapaulafn](/u/mariapaulafn) you may want to format the doc to clearly identify leads for Rings & topics.

---

**Ethernian** (2019-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomislavmamic/48/318_2.png) tomislavmamic:

> It seems to me that people are not really filling in the rings document (I see only 3 participants signing up)…

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> Just FYI, i havent promoted the hackmd or the form yet,

yeah. It is my experience too. Few days is too short time to make conclusions. And yes, we need to promote our request for topics actively.

If the barrier to fill the form is too high, I would post an invitation in most active topics. People should just ![:hearts:](https://ethereum-magicians.org/images/emoji/twitter/hearts.png?v=12) it to signal their interest. This would be some kind “in-topic voting”.

Here is [an example](https://ethresear.ch/t/whisper-v2-request-for-requirements-for-eth2-unified-messaging-protocol/4808/2?u=ethernian) of such invitation.

---

**Ethernian** (2019-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> @Ethernian if you want a session around State Rent (for example) — put it in the doc in the same way Rings are. I think that’s the misunderstanding.

Totally agree. Just let people put “orphan” topics at the same level as Rings are. Rings may “claim ownership” adding multiple votes for the topic at once. Something like that. Then we will try to order by votes and group by Rings.

---

**Ethernian** (2019-01-23):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/mariapaulafn/48/534_2.png) mariapaulafn:

> you are missing the point of what is proper event agenda structuring, and maybe losing focus.

It is a good point. Let us align our understanding why we need an agenda and what structure do we need for it.

My understanding: we need an agenda for …

1. to help people to find each other in the same room and at the same time to discuss topic of their interest.
2. We need to know how many people and how long do come together for discussion in order to assign a room efficiently.
3. if time and room will be sparse, we need to provide priority accepted by most people.

Ultimatively, we need topic priorities and number of people per discussion (assuming all time slots are equal). Rings to topic assignment may help us to estimate number of participants in each session, but should not concern us otherwise. Thats all.

[@mariapaulafn](/u/mariapaulafn)  do you have another structure or goals in mind?

---

**Ethernian** (2019-01-23):

BTW, I have tried to fill [the form](https://docs.google.com/forms/d/e/1FAIpQLScOMcJPOhfJ2Iako1V25eSFWru0AIsUqQ7Vd0jlrQqcP_5Fuw), but was stopped on following:

The Field “If you already got more participants, add them here” is mandatory. I stopped filling the form and started to looking for supporters.

It is not obvious whether the number of participants I provide here is final or people will may join later somehow.

Would be great to make it clear, that it is not necessary to show all the supporters at the time of submitting the form. I would notice, that submitted topics will be published and people may join them later.

---

**jpitts** (2019-01-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomislavmamic/48/318_2.png) tomislavmamic:

> How do we achieve more engagement of people in making the gathering better?
> How do we achieve a greater impact without repelling people with responsibilities?

[@tomislavmamic](/u/tomislavmamic) I was focusing on this a month ago but was unable to really work enough on it. I think that there needs to be someone who reaches out to each Ring, the contact and others who seem to be participating. Just to energize/encourage them, ask what is going on, etc.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tomislavmamic/48/318_2.png) tomislavmamic:

> The most lively and lasting discussion at the first FEM gathering in Paris last year happened in the yard, quasi-spontaneously. If we don’t include it on the agenda, people we find ways to do it anyways, and if there is no designated time for this, they might skip ring sessions to do it.

Totally! That was an amazing situation out there in the courtyard, one of those classic moments in our history.

One way to do this may be to have an open “birds of a feather” discussion at a certain time, e.g. “2pm discussion about the Ethereum Roadmap in the courtyard”.

---

**mariapaulafn** (2019-01-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> @mariapaulafn you may want to format the doc to clearly identify leads for Rings & topics.

Yes I need to polish it, sorry, as im doing GörliCon it was in my plans to fully dedicate to FEM schedule after my event, but I got pushed into figuring it out ahead of time.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> One way to do this may be to have an open “birds of a feather” discussion at a certain time, e.g. “2pm discussion about the Ethereum Roadmap in the courtyard”.

This is my idea, too. I would appreciate if everyone could read my last message here to [@Ethernian](/u/ethernian) to understand that I want to give the agenda all my time, but I need a week more.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> @tomislavmamic I was focusing on this a month ago but was unable to really work enough on it. I think that there needs to be someone who reaches out to each Ring, the contact and others who seem to be participating. Just to energize/encourage them, ask what is going on, etc.

Same goes to this.

---

**mariapaulafn** (2019-01-24):

Try adding just “0” its an indicative form. It’s quite obvious that if you dont have any, you just add some – or 0

---

**mariapaulafn** (2019-01-24):

Hi, with all due respect. I organize more than 10 conferences/events a year. I am currently organizing one. I know exactly why we need an agenda and I don’t understand why my timeline on this is being pushed and my work directed when we all had assigned ourselves the areas we were best at, and you remarked you could not do agenda.

So please, try not to overstep, because the work will get done, this is not my first FEM or my first conference, I know exactly what to do and I am very much aware that everything needs feedback, but all in due time. This thread is not doing any favors but rushing things, and interrupting my other tasks.

I intend to dedicate my whole attention to the agenda, once I am done with other commitments (jan 31st), and expect my times to be respected. We have a month to go so the agenda has enough time to be prepared.

I am sorry if this comes off as too direct, but at this point, I feel that I’m being pushed and on top of that schooled, on an area that I signed up for because this is what I’m best at. I take all feedback, but let me do my thing and then give feedback.


*(2 more replies not shown)*
