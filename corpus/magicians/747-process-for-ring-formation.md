---
source: magicians
topic_id: 747
title: Process for Ring Formation
author: boris
date: "2018-07-16"
category: Working Groups
tags: []
url: https://ethereum-magicians.org/t/process-for-ring-formation/747
views: 2868
likes: 13
posts_count: 21
---

# Process for Ring Formation

I think I [@boris](/u/boris) stuck my hand up to help put together an EIP for Ring Formation. I believe [@Jason_C](/u/jason_c) agreed to help as well.

I believe we can start with HackMD(https://hackmd.io/). And, infrastructure wise, probably great for Magicians to get a “Conference” edition of HackMD under our own namespace – eg. `[notes.ethereum-magicians.org](http://notes.ethereum-magicians.org)` and use that instead of Google Docs.

Reading the IETF Working Groups material I find useful. Start at their [IETF About WGs page](https://www.ietf.org/how/wgs/) and then read [RFC2418](https://tools.ietf.org/html/rfc2418) which talks about how to form and run WGs.

I believe that we need to create the equivalent of RFC2418 as the Ring Formation EIP.

I also believe that the Magi can provide some “default infrastructure” to make it accessible to create Rings, which starts as simply as having a Category here on the forum and/or private categories for collaboration, per some of the discussion of useful work being done by smaller groups.

Let’s use this thread for discussion, and HackMD for collaborative editing. At some point, we will move it to a pull request on Github. Starting with HackMD can make it more accessible, as this is a memo / process improvement that is not restricted to just developers.

Link to HackMD: https://hackmd.io/s/Bkxcd1c7m (all are welcome to contribute – let’s discuss here and [@Jason_C](/u/jason_c) and I will take initial lead as editors)

See also:

- Wallet Developers
- Ring directory

## Replies

**Jason_C** (2018-07-16):

2418 gives a good reference for thinking through criteria for Ring formation. We can discuss whether FEM criteria need to be as formal or more or less formal in its own criteria.

As I imagined it during discussion, this criteria is simply for a label of “FEM certified ring” or something to that effect.

Philosophy: It should be noted (as I imagine it) that this is purely for the definition of “ring” within FEM, and that this effort does not exclude the possible existence of rings or WGs formed outside of FEM or the FEM-definition. Ultimately, I hope to see more organizational structures or bodies as coordinated and organized as the FEM efforts are (at least as they were this weekend) that take different approaches/philosophies to leave room in the Ethereum ecosystem for philosophical disagreement without forcing a split at the “WG layer” if that makes sense. I do not want the FEM philosophy and effort to become “one ring to rule them all,” but rather one standard that (hopefully) becomes successful, important, and useful for a certain set of group efforts and circumstances within the larger community.

Proposed Purpose: FEM-certified rings are entitled to certain benefits as bestowed by FEM. These benefits may include a dedicated channel in FEM communication forums, FEM-funding (if that ever becomes a thing), and other entitlements that manifest under FEM’s abilities. Entities may simultaneously be both FEM-certified and compliant with other bodies’ standards (if they differ). **BTW this might be where I might disagree that whatever is determined in this discussion should be an EIP itself. I do not see the benefit of an EIP recognizing FEM-defined rings if this FEM-local purpose is adopted. But happy to think about possible benefits or a formal-EIP proposal if [@boris](/u/boris) or someone else has some in mind.**

Proposed Minimum Criteria as stated at the Berlin meeting (this may be articulated in a “charter” as outlined in RCF2418 - 2.1, or something as simple as listed on an appropriate FEM intake form):

1. A FEM-certified ring must have a purpose to produce and deliver EIPs to the greater Ethereum community. The Ring’s goals (as reduced to tangible form in EIP form) must be clearly and articulately stated; whether it needs to be as structured as the 3 criteria in RCF2418-2.1, or more or less so I am not sure, but this is a starting point to know that this criterion is desirable.
2. A FEM-certified ring must have at least 3 members upon certification. This requirement follows the logic that 1 person is an individual, 2 is a partnership, 3+ is a group. They must be reasonably identified in a way so that contacting them is easy and FEM can reasonably certify that all three are in fact distinct individuals. One of those 3 members will be an “organizer” type, though I don’t want to imply that the organizer is an important decision maker for the ring’s strategic/development efforts. They are simply the key contact person and charged with organizing and administrative functions (e.g. the on-the-ground planning for a web-conference and maintaining communications with FEM and the rest of the community). Whether roles must be as defined as “chair,” “area director,” etc. as outlined in 2418 is up for discussion.
3. A Ring must have a dedicated area in cyberspace where interested people may be directed to learn about the ring, its purpose, its ongoing efforts, and contact information. Whether this is a website, a reddit page (with appropriate sidebar), a Telegram channel with a pinned message explaining, or whatever, I think is good to leave to the discretion of the Ring. Point is that the field on the intake form/charter cannot be blank and the destination must exist.

RFC2418 has some other criteria that I think may or may not be useful for FEM’s purposes, such as a mailing list, milestone requirements, and others that I am interested in the communities thoughts. Look forward to reflecting on what everyone else has to say.

---

**boris** (2018-07-17):

The word certification isn’t great.

I think the purpose of Rings is in scaling Core Devs / scaling the EIP process, and meshes with the core goal of FEM in helping to produce and review high quality EIPs.

FEM may host / incubate / help form some of these, and as you stated, certain things need to get filled out.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jason_c/48/547_2.png) Jason_C:

> BTW this might be where I might disagree that whatever is determined in this discussion should be an EIP itself. I do not see the benefit of an EIP recognizing FEM-defined rings if this FEM-local purpose is adopted. But happy to think about possible benefits or a formal-EIP proposal if @boris or someone else has some in mind.

The EIP process has not to date been used for a lot of meta / informational nature, but it has the benefit of being a “home base” with generally accepted governance process by the wider community. I propose we follow the same process – whether or not it get merged in or not, I think it’s a useful format to gather consensus around.

---

**Jason_C** (2018-07-18):

Good point re: “certification.” Maybe “a ring that meets the FEM-definition” and is therefore “FEM-defined” or “FEM-compliant”?

Can update purpose to focus on the goal of high quality EIPs, with the other pieces described after.

As far as EIP process for this definition, I still think it’s a little watery. But you make a good point about it being the “home base” with the most eyes from the broader community. I wouldn’t push back on a proposal to float through there with/without actual merge, as you suggest.

---

**Recmo** (2018-07-23):

I just read through RFC 2418 and found that it relies quite a bit on the organizational structure of the IETF. In particular the hierarchy IESG -> Area Director -> WG Chair -> WG. I don’t think this amount of hierarchy is appropriate given the current size of the Ethereum scope. And it may never be appropriate given our preference for decentralization instead of hierarchy.

Another thing that struck me is the emphasis on a working group working towards a specific deliverable. An RFC2418 working group has a limited lifetime and works towards a single RFC, or perhaps a few strongly related standards. Longer-lived working groups are mentioned as an exception. When I look at the [list of active WGs](https://datatracker.ietf.org/wg/) it seems that longer lived WGs are more common than RFC2418 would suggest. There are a few WGs for “[…] Maintenance and Extensions” and some long lived once such as TLS. But all of them are very specific in scope.

When I look at the current [list of Rings](https://github.com/ethereum-magicians/scrolls/wiki#rings) they do not appear to match well with the RFC2418’s idea of a working group. They are do not have as goal of a single standard in a clear limited timeline. In fact, it seems to match closer with the RFC2418 concept of an Area.

I suggest we combine the concepts and allow a Ring to be anywhere on the spectrum between Area and Working Group. We can then allow for some organic hierarchy where, for example, the Token Ring would create a subring for a particular token standard. This would only be required if that particular standard is complex enough that it is beneficial to form a subring. An simple extension of this is to allow multiple membership. A Ring for a wallet-aware token standard could then be part of both the Token Ring and the Wallet Ring. Formation can thus also be bottom up, where a more-specific Ring is formed that later becomes member of a more general ring that covers it.

---

**boris** (2018-07-23):

Yes agreed. Areas (Wallets, Education) and Working Groups might zoom in to just one EIP.

The mix of EIPs (protocol changes) and ERCs (token and other standards) also feeds into this.

There are other parts of those RFCs that I found useful in thinking about this. Glad you read through for context.

Also, I need to get back to this, but likely defining a way to create Rings is less useful than just working on the Ring template in Scrolls wiki.

---

**Jason_C** (2018-07-25):

I agree that RFC 2418 is too formalistic/regulated for how the current ring efforts are forming naturally. The initially proposed standards are very bare-bones to encompass most of the rings as they are. I’m happy to set a low minimum threshold in the early days (including with a broad definition ranging from Areas to WGs) and then see if it makes sense to add hurdles to optimize efficiency/effectiveness.

Re: sub-rings I think would be useful, but would be nice if we already see this behavior occurring naturally as data to propose a standard. Have you noticed this tendency already in some existing ring efforts?

---

**boris** (2018-07-26):

So I made this a lot simpler, I think – which is just clone the wiki Ring Template that [@ligi](/u/ligi) made. I did write up a HOWTO, see [HOWTO Form A Ring · ethereum-magicians/scrolls Wiki · GitHub](https://github.com/ethereum-magicians/scrolls/wiki/HOWTO-Form-A-Ring) – please go ahead and edit directly.

There are some technical bits, like figuring out that we might want to form a Discourse group for Rings, since that gives a number of capabilities:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)[Notifying members of a ring and ring colors](https://ethereum-magicians.org/t/notifying-members-of-a-ring-and-ring-colors/869/2)

> There IS a groups ability, too, but that would mean Ring Makers have to actively manage group membership. We may want to do that to show Wallet Ring members, AND you can @-mention groups which notifies all the users. This probably needs a tracking Github issue if we want to go this direction.

I still need to post my notes – including the group generated list of “Working Groups” that exist already.

As noted already [@Recmo](/u/recmo) Topics vs. Areas is tough. I suspect we’ll form more Area-sized Rings first, and then as *those* scale, they’ll splinter down.

---

**MadeofTin** (2018-07-31):

Topical focused, and Deliverable focused? I noticed a little tension between these two types of groups in the Berlin Meeting simply because it wasn’t clear which kind of group the meeting was talking about. So would wallet be called an Area Group? Defining each and the language around each would help discussions like this.

1. People with similar Expertise and Interest gathered in one place around a central theme (Does not Expire)
2. People working together to achieve a specific task, or address a specific problem. (Should have a point of expiration)

Perhaps definition can be based on the answer to the question, “Should this group expire at the time of achieving the goal, or not?”

This may lead to natural subgroups of Expiring Groups emerging from parent non expiring groups, and a bit of intermingling from different Rings as we go along.

---

**MadeofTin** (2018-08-01):

Perhaps Field Groups, and Working Groups to continue the play on Maths.

(Another Thought: Working Groups, as a name for deliverable focused groups, to someone who isn’t familiar with how the IETF and/or technical standards practice work may be initially confusing. On the other hand it may play in our favor to follow standards practices)

---

**MadeofTin** (2018-08-15):

I drafted an update to the Abstract to include some of the discussions, as well as a draft of charter requirements. I pulled heavily from RFC2418 wherever possible.

Included

- Separated out Areas and Working groups explicitly
- Charter Requirements

Name
- Type
- Lead/s
- URL
- Group Specifications required by Discourse.
- Ring Description
- Related EIPs

Thoughts? Feedback? What am I missing?


      ![](https://ethereum-magicians.org/uploads/default/original/1X/9820c4fe404a7e163dc1dc0a8d644cddd3e4bc2a.png)

      [HackMD](https://hackmd.io/@bmann/Bkxcd1c7m?type=view)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###



Ring Formation EIP = _The intent of this document is to turn it into an EIP_   eip:










Lets get this EIP Submitted!

---

**MadeofTin** (2018-08-15):

I read through this thread



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jamesray1/48/1548_2.png)
    [EIP-1053: A proposal to move the content in ethereum/wiki to a Wikipedia-style wiki site](https://ethereum-magicians.org/t/eip-1053-a-proposal-to-move-the-content-in-ethereum-wiki-to-a-wikipedia-style-wiki-site/265/32) [EIPs](/c/eips/5)



> Hi @boris, thanks for your comment. Please see my comment in https://github.com/ethereum/wiki/issues/589#issuecomment-410906496.
>
> Issues so far:
>
>  No soft wrap in revision history. E.g. in https://en.ethereum.wiki/hist/home, one paragraph appears as one line; and there is no soft wrap option, let alone by default. This doesn’t occur if you edit a page, just in comparing revisions.
>  while history for a page is accesible by modifying the link, e.g. https://en.ethereum.wiki/faqs → https://en.ethe…

Should a wiki be part of a Field Ring?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)[EIP-1053: A proposal to move the content in ethereum/wiki to a Wikipedia-style wiki site](https://ethereum-magicians.org/t/eip-1053-a-proposal-to-move-the-content-in-ethereum-wiki-to-a-wikipedia-style-wiki-site/265/14)

> Bottom line: great idea, pick a topic / area of interest / type of audience and gather a group to host it and maintain it and go from there.

Sounds a lot like a Field to me.

---

**jamesray1** (2018-08-16):

Just want to say I don’t have the time to volunteer for a wiki ring, as I’m not being paid yet for working on sharding and gossipsub in libp2p (no grant).

---

**Ethernian** (2018-08-17):

This is not the first time I hear the story about stalled grants from EF. What is going on there?!

Just sad

---

**Ethernian** (2018-08-17):

Guys, what is the current process to finalize the process of a ring creation?

I’ve got great feedback from many sides and would like to make Ring of Ethereum Architects (EthA) happend finally.

Does [@boris](/u/boris) know how to do it?

---

**boris** (2018-08-17):

I’m not in charge ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Sorry I need to get back to [@MadeofTin](/u/madeoftin) too — I want his work to extend the HOWTO on the wiki [HOWTO Form A Ring · ethereum-magicians/scrolls Wiki · GitHub](https://github.com/ethereum-magicians/scrolls/wiki/HOWTO-Form-A-Ring)

I don’t think this needs to be as formal as an EIP as I originally thought. I do think having a bat is useful — eg anyone can create a Ring on the wiki and promote it.

It might need three participants before a group is formed.

Does that Make sense?

---

**Ethernian** (2018-08-17):

> I don’t think this needs to be as formal as an EIP as I originally thought.

I am completely ok here.

There are definitely more that 3 people who would like to attend in Ring of EthA

There is only one question: who is on charge to create a discourse category “Ring: Ethereum Architects”?

---

**boris** (2018-08-17):

Read the HOWTO please!

---

**MadeofTin** (2018-08-19):

Just updated the Wiki as well as the ring template. I added a blurb about membership [@boris](/u/boris) https://github.com/ethereum-magicians/scrolls/wiki/HOWTO-Form-A-Ring#membership-requirements Is that fair to say? is there a better place for this?

---

**Ethernian** (2018-08-19):

I am ok with it.

Could you please approve my application for Ring of Ethereum Architects?

---

**Ethernian** (2018-09-24):

I have found two simple **assessment question** to be answered by new Rings:

- What is the core area, where SomeRing should be able to produce meaningful results independently from other Rings?
- If SomeRing  needs cooperation to with other Rings to work on its tasks, what are the incentives for other Rings to cooperate with SomeRing ?

Is it good enough as assessment question?

Thoughts?

