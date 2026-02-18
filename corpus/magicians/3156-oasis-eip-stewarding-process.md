---
source: magicians
topic_id: 3156
title: OASIS-EIP stewarding process
author: tvanepps
date: "2019-04-18"
category: Magicians > Process Improvement
tags: [eth1x, eip-process, berlin, oasis]
url: https://ethereum-magicians.org/t/oasis-eip-stewarding-process/3156
views: 3391
likes: 23
posts_count: 23
---

# OASIS-EIP stewarding process

(written by [@virgil](/u/virgil))  Today I am in air transit with a yet undetermined schedule, so in the event I am unable to speak live on my introduction of the “EIP OASIS plan”, I have prepared these notes.

My original proposal (approved by EF management) for an  *experimental*  EIP/ERC-approval process running  *in parallel*  to the existing EIP process is here: https://notes.ethereum.org/rkFOS_WLV

You can see the majority of the context there. Use of the experimental OASIS-EIP process is  *entirely optional* . If maintainers prefer, they can keep with the same system. If, after 18 months, it is deemed that the OASIS-EIP process isn’t much better than our current one, we will  *discontinue the experiment* and return to single-process system we use now. If, after 18 months, it’s determined that the OASIS-EIP process is a notable improvement, we can discuss making OASIS-EIP the sole EIP/ERC-approval process.

After deciding that becoming an IETF working group would generate more problems than solutions, Ethereum Foundation decided to go with OASIS as OASIS is one of the few organizations that, rather than enforce gate-keeping (like IETF, ISO, etc), OASIS uses their standards specialists as shepherds and referees to bring out the best in your standards.

## Project Governing Board (PGB)

Some have asked how the initial Project Governance Board was decided. I don’t consider any of the picks to be controversial, but here’s the reasoning for each initial member:

- Ethereum Foundation - Would be bizarre to not have EF represented. I, Virgil Griffith, will be the initial EF representative, but I hope to abdicate this role as soon as possible.
- Consensys - With the exception of EF, Consensys employees have authored more EIPs than any other org. We wish to reward this behavior.
- Ethereum Enterprise Alliance - Although coming from the more corporate world, the EEA has a lot of standards experience and expertise. It seems sensible to leverage this experience. Additionally, having EEA more involved in Ethereum EIPs will improve their ability to keep their own EEA standards compatible and up to date with ours.
- Nick Johnson - Nick has been the primary steward of the EIP process for sometime. The goal is for him is to represent the values of the existing pre-OASIS process and overall be a voice of “the people” within the PGB.

As there are an even number of PGB members, if there is a tie, OASIS referees will cast the tie-breaking vote.

## Technical Steering Committee (TSC)

One pleasant change in this process is that, whereas the Magicians EIP Ring was before merely the unofficial custodian of the EIP process, in the OASIS process the EIP Ring becomes the Technical Steering Committee, which has official, specific powers. This enshrines the Magicians (or at least the EIP Ring) with official standing. I have complete confidence in the Magicians for rising to the challenge of wielding these new powers.

The person to field all OASIS-related questions to is Jory Burson [jory.burson@oasis-open.org](mailto:jory.burson@oasis-open.org). (this post was written by [@virgil](/u/virgil) )

## Replies

**boris** (2019-04-18):

A few notes: EthMagicians are not a “thing”. It’s not a membership based organization – individuals within it collaborate on various areas of interest. There is no formal organization involved and no plans to do so as far as I know. Thus, no one person can speak for the group.

There isn’t currently an “EIP Ring” – all of the forum is used to focus on different areas of EIPs, and a wide variety of people participate in.

I do think there will be a number of people interested in participating in the TSC, as individuals. I’m interested in exploring this and hearing more from Jory and the OASIS team.

---

**jorydotcom** (2019-04-18):

![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=9) I’m Jory from OASIS - wanted to introduce myself here! Feel free to HMU with questions here or elsewhere online (I’m [@jorydotcom](/u/jorydotcom) on all the things) - will be posting some FAQs after the presentation based on questions we get today!

---

**boris** (2019-04-18):

Slide deck:


      [docs.google.com](https://docs.google.com/presentation/d/1D-ZzEirTUMf5UIxxxiqWnbMwyXdZCoD-Dv2g_GI2q_o/edit)


    https://docs.google.com/presentation/d/1D-ZzEirTUMf5UIxxxiqWnbMwyXdZCoD-Dv2g_GI2q_o/edit

###

(Thank you Virgil) jorydotcom on GH, Twitter, Mastodon, IRC - hmu if you have questions or anything you want to chat about 1 1 1 Introducing Jory Burson | @jorydotcom program manager & open source advocate jory.burson@oasis-open.org

---

**boris** (2019-04-18):

Thanks Jory, welcome!

---

**jorydotcom** (2019-04-18):

OASIS still has a lot to learn about what does and doesn’t work for people when it comes to EIPs; so bearing in mind that this is subject to change, the output of an OASIS-EIP process at minimum would be a specification that meets criteria for possible* advancement to de jure organizations (important for a lot of businesses & governments). The TSC and PGB may also want to set other criteria like “must have 2 independent implementations” or “must have an open source reference implementation” or “must have conformance criteria” etc.

We certainly don’t want to exacerbate issues with the EIP process - and I’d love to know what those are from your point of view, by the way - the current thinking is that we should pilot the process with something like JSON-RPC which isn’t an EIP at all, and go from there. If it goes well, we do it again with a different piece of work, or we go back to the drawing board.

- I say possible because it is up to you how far you want to advance a standard from ‘Project Standard’ to ‘OASIS Standard’ to ‘ISO standard’

---

**jpitts** (2019-04-19):

Knowing [@virgil](/u/virgil) and knowing that he has good intentions here, I will not over-react to the high-handed tone employed in this proposal. I will also not over-react to assertions about the Ethereum Magicians in [Hiring OASIS to referee the EIP process](https://notes.ethereum.org/Domx9MXtQNGjK_RIQPBMNg).

What I will emphasize is that it is up to the Rings to adopt this framework. The Ethereum Foundation could not impose a standards framework on the core devs, nor could the Ethereum Magicians impose anything on the Rings, even in a Council.

Having said this, I would encourage some Rings and individuals championing standards (and potential standards) to take a serious look at this program. Considering the cost and what is offered, I do appreciate this program. It can lead to much-needed learning, and likely will lead to higher quality EIPs.

Let me know [@jorydotcom](/u/jorydotcom) and [@virgil](/u/virgil) how we can facilitate pilots here on the Forum.

---

**jpitts** (2019-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/tvanepps/48/3406_2.png) tvanepps:

> ## Technical Steering Committee (TSC)
>
>
>
> One pleasant change in this process is that, whereas the Magicians EIP Ring was before merely the unofficial custodian of the EIP process, in the OASIS process the EIP Ring becomes the Technical Steering Committee, which has official, specific powers. This enshrines the Magicians (or at least the EIP Ring) with official standing. I have complete confidence in the Magicians for rising to the challenge of wielding these new powers.

[@virgil](/u/virgil), perhaps by “EIP Ring” you meant the EIP Editors? As [@boris](/u/boris) said there is no Ring by this name.

From my observation, “Magicians” generally have a strong aversion to enshrining anything, and an equally strong aversion to officialdom or authority. We may value leadership however, and appreciate any way to improve discussions and decisions about Ethereum protocol and related technologies.

It is in the leadership and quality of discussions from a potential TSC where we may find a lot of value. We should open this up and discuss how a TSC can be formed. The Editors may be a good place to start, and I know that [@cdetrio](/u/cdetrio) has discussed/proposed something along the lines of a TSC in recent years.

Once we have clarification on what [@virgil](/u/virgil) meant by “EIP Ring” I can start a new thread to discuss a Technical Steering Committee.

---

**boris** (2019-04-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jorydotcom/48/1894_2.png) jorydotcom:

> The TSC and PGB may also want to set other criteria like “must have 2 independent implementations” or “must have an open source reference implementation” or “must have conformance criteria” etc.

These are already gates within the EIP process on the way to network deployment.

 consciousEntity:

> Assuming this is true - won’t this exacerbate the ongoing issues with the EIP process?

EIPs are protocol standardization not network acceptance. I think most of the issues lie with core coordination / network governance — which are somewhat outside the EIP process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jorydotcom/48/1894_2.png) jorydotcom:

> the current thinking is that we should pilot the process with something like JSON-RPC which isn’t an EIP at all, and go from there.

I agree that sub protocols / components of the Ethereum stack are a good place to start. It’s the weakest area of specs, and biggest area for re-use and collaboration, and also non-controversial.

I would also suggest that each such area has a separate TSC. Which I don’t know how that meshes with the OASIS process.

I started also using JSON-RPC as a starting point 5 months ago. Existing repo is here [GitHub - spadebuilders/ethereum-json-rpc-spec: Working group for the canonical JSON-RPC spec for Ethereum clients](https://github.com/spadebuilders/ethereum-json-rpc-spec)

I think re-gathering interested parties — EEA, wallets & other middleware, client implementors — would be good.

Lastly — I don’t think the process maps to EIPs overall. *Some* EIPs are pointers to large chunks of work like the JSON-RPC spec, others are smaller and self contained.

Hope that helps! Happy to participate as things move along.

---

**jorydotcom** (2019-04-19):

Thank you [@jpitts](/u/jpitts) - I think you’re spot on that this doesn’t really mean anything unless it’s helpful and additive for the editors/rings, and it’s something they want to use.

I’ll underscore that this is all really in a ‘discovery’ stage, and one of the differentiators for OASIS as a standards org is that its process can be flexible in a lot of places. So getting to know the existing Ethereum processes, what works, what’s analogous to OASIS process, etc… that’s our goal at the moment.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> These are already gates within the EIP process on the way to network deployment.

[@boris](/u/boris) I think I missed this studying the EIP process overview; can you point me to where this & other ‘gates’ might be documented so I can get an accurate picture? Are there requirements for some components but not others, for example? TY!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> I would also suggest that each such area has a separate TSC. Which I don’t know how that meshes with the OASIS process.

I like this suggestion - I can see how it would be helpful here. Will confirm with my colleagues Chet & Carol but I’m pretty sure the process would support this.

Also thank you for the link to your working group repo! How do you feel about the status of the work so far?

> Lastly — I don’t think the process maps to EIPs overall.  Some  EIPs are pointers to large chunks of work like the JSON-RPC spec, others are smaller and self contained.

I don’t know much yet, but I think you may be right. Chatting with Virgil earlier, we think the comparison to EIPs and the EIP process was perhaps pre-mature. Perhaps reframing it as an ‘Open Standards Project’ makes it less muddy?

Boris, A Jones, Jamie - I don’t want to ask too much of ya’ll’s time, but it would be super helpful if we could ‘interview’ you on a zoom chat or something? Is that an ok ask?

Much appreciation to you all for the comments and insight so far ![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=12)

---

**jorydotcom** (2019-04-22):

[@boris](/u/boris) [@jpitts](/u/jpitts) & all - I made a doodle poll here to find a time to chat for those interested: https://doodle.com/poll/q8y5cz6v7tedget4 (sorry I can only @ mention 2 people in one post as a newbie!)

Or if those times don’t work and you want to schedule something else: https://doodle.com/joryburson

---

**jorydotcom** (2019-05-01):

Hi all ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

Looking for a bit of guidance about what the preferable means of sharing updates would be. Have had very informative follow-up conversations & discussions with the ‘bootstrap PGB’ which we’d like to report on, and probably do so on an ongoing basis. I assume it’s ok to make a new topic for these updates, but want to make sure I’m following appropriate norms here (cc [@jpitts](/u/jpitts) [@boris](/u/boris))

---

**boris** (2019-05-01):

[@jorydotcom](/u/jorydotcom) feel free to make separate updates. I’ve added the tag [#oasis](https://ethereum-magicians.org/tags/oasis) to this post, so if you tag new updates that way, there will be a page where all related updates can be accessed.

---

**jorydotcom** (2019-05-02):

super super! I made an [update post](https://ethereum-magicians.org/t/oasis-ethereum-open-project-update/3232/2), linking here for continuity ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=9)

---

**shanejonas** (2019-05-02):

[@jorydotcom](/u/jorydotcom) [@jpitts](/u/jpitts) [@boris](/u/boris) I have put a specification together that covers this subject and would love to hop in a call to discuss with everyone.

Resources:

https://github.com/etclabscore/ethereum-json-rpc-specification

https://github.com/ethereum/EIPs/issues/1902



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/bitpshr/48/190_2.png)
    [Remote procedure call specification](https://ethereum-magicians.org/t/eip-remote-procedure-call-specification/1537) [EIPs interfaces](/c/eips/eips-interfaces/45)



> Much of Ethereum’s effectiveness as an enterprise-grade application platform depends on its ability to provide a reliable and predictable developer experience. Nodes created by the current generation of Ethereum clients can expose RPC endpoints with differing method signatures; this forces applications to work around method inconsistencies to maintain compatibility with various Ethereum RPC implementations.
> Both Ethereum client developers and downstream dapp developers lack a formal Ethereum RP…

---

**jorydotcom** (2019-05-03):

I would like that very much as well! I made a Doodle poll for a few days in the next couple of weeks; lmk if we need to accommodate dif. days/ timezones


      ![image](https://marketing-cdn.doodle.com/branding/2022/favicon/favicon.ico)

      [Doodle](https://doodle.com/poll/irrwizpi4bpvvcr2)





###



The Group Poll you're trying to access isn’t up-to-date and has been archived

---

**boris** (2019-05-03):

I know a lot of people like Doodle – but in my experience, just talk to [@shanejonas](/u/shanejonas) and figure out a time that works for you two and announce it a good week or two ahead of time and then promote to get people involved.

[@bitpshr](/u/bitpshr) if he’s still interested. And maybe the middleware / wallet folks like [@pedrouid](/u/pedrouid) want to talk about JSON-RPC standardization / expansion etc. [@chaals](/u/chaals) or other interested parties from EEA.

---

**BelfordZ** (2019-05-06):

I have made a zoom meeting (see below) and [google calendar](https://calendar.google.com/event?action=TEMPLATE&tmeid=ZWVjbmlsYmg4cGU4YWJ0ZThyZXBramgxNWcgYW9jYjFrbDIybXRlcnNsZzloa2VpdTQ0dWdAZw&tmsrc=aocb1kl22mterslg9hkeiu44ug%40group.calendar.google.com) event based on the times that were provided.

Please invite anyone that should be there.

I have no problem rescheduling if its required to have the right people in the chat, just let me know.

> Zachary Belford is inviting you to a scheduled Zoom meeting.
>
>
> Topic: RPC Spec(s) Chat
> Time: May 8, 2019 1:00 PM Vancouver
>
>
> Join Zoom Meeting
> Launch Meeting - Zoom

---

**boris** (2019-05-06):

[@BelfordZ](/u/belfordz) I would make a separate post so this doesn’t get lost — JSON-RPC spec call or something like that.

I’ll promote the timing and post on the previous call thread we had to let people know.

As part of that new post it would be good to explain why you’re having this call / who should care ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

---

**BelfordZ** (2019-05-08):

Didn’t see your message [@boris](/u/boris). Meeting is happening now, gonna wait another 10 mins for late comers.


      ![image](https://st1.zoom.us/zoom.ico)

      [Zoom Video](https://zoom.us/j/885169803)





###



Zoom is the leader in modern enterprise video communications, with an easy, reliable cloud platform for video and audio conferencing, chat, and webinars across mobile, desktop, and room systems. Zoom Rooms is the original software-based conference...

---

**shemnon** (2019-05-10):

This call happened during our team’s bi-weekly demo session.  Is there a summary or recording?


*(2 more replies not shown)*
