---
source: magicians
topic_id: 2707
title: HackMD document is now protected?
author: AdamDossa
date: "2019-02-21"
category: Protocol Calls & happenings
tags: []
url: https://ethereum-magicians.org/t/hackmd-document-is-now-protected/2707
views: 1853
likes: 7
posts_count: 13
---

# HackMD document is now protected?

The previous link:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/DaJhrasLQteUk3IwX5bQAg)



    ![](https://hackmd.io/images/media/HackMD-neo-og.jpg)

###










gives me a 403 error.

Anyone know what’s up with this?

Thanks,

Adam

## Replies

**ligi** (2019-02-21):

Yes - there has been vandalism in the document.

---

**AdamDossa** (2019-02-21):

Oh - that’s annoying. What’s the best approach to keep the document live? Should we ping you (or someone else) with updates? Is it possible to keep it read-only in the meantime so that we can track updates?

---

**ligi** (2019-02-21):

Actually I am not involved with this hackmd document - but I get email-updates about changes and saw the vandalism:

[![Selection_315](https://ethereum-magicians.org/uploads/default/original/2X/7/7c8466e45738b5da9fdbed9a004354120a66cbf4.png)Selection_315760×425 26.8 KB](https://ethereum-magicians.org/uploads/default/7c8466e45738b5da9fdbed9a004354120a66cbf4)

So I guess it was closed down to control the situation.

I think we should dogfood here and build a web3 system replacing hackmd. I guess people writing such bullshit do not even know how to operate such a thing. Perhaps with keys whitelisted at magician events and every key can invite new people. If vandalism is detected from one account the changes of this account and all accounts that where invited by that account get reverted. Just an idea ..

---

**AdamDossa** (2019-02-21):

Yeah - possibly some system where you have to stake funds in order to edit the document with the stake being returned automatically after some time or during attendance at the event could work. For demonstrably bad edits (i.e. straight up graffiti like the above, as opposed to controversial topics) the stake could be confiscated and put towards EM funds.

Easiest would be to allow a centralised party(s) to arbitrate this (the stopping of an automatic refund after e.g. 1 week) and would probably solve the problem. It would be a barrier to entry, but for this specific use-case I would guess most people would be comfortable with this type of approach as they are likely to be fairly technically minded.

---

**boris** (2019-02-21):

Will work on this today. Have to see if we can hand out edit to ring facilitators and others.

Probably I will suggest we just use the wiki mode here on Discourse, as it’s a system we already know and own ourselves.

---

**boris** (2019-02-22):

We’ve ported the doc natively to Discourse here:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)
    [[Council of Paris 2019] Call for Rings](https://ethereum-magicians.org/t/council-of-paris-2019-call-for-rings/2726) [Happenings](/c/happenings/7)



> Note: ported from HackMD. Discourse wiki mode is turned on, so regular users should be able to edit it directly. Leave a comment if you can’t edit the wiki and we’ll add your info.
> Council of Paris
>
> When: March 4, 2019
> Where: CNAM - 292 Rue Saint-Martin, 75003, Paris, same venue as ETHCC
>
>
> Basic details:
> Website: https://ethereumevents.global/events/2019-council-of-paris/ 28
> Agenda: https://docs.google.com/spreadsheets/d/1BYudpf2TfjO-qbAoSuzFBH0Ab_BRiQJ31VUhGoc6n_Y/htmlview
> Registration: http…

Let me know if any issues editing — wiki mode is turned on.

---

**virgil** (2019-02-25):

[notes.ethereum.org](http://notes.ethereum.org) supports protecting notes so they can only be edited by people who are members of the ethereum github organization.  You can even make it so the document is owned by a group of people instead of a single person.  If you’re interested in this, email [sysadmin@ethereum.org](mailto:sysadmin@ethereum.org).

---

**boris** (2019-02-25):

Thanks Virgil. Doesn’t meet our use case of having most everyone edit. And it means we need to manually whitelist people.

Porting it here to the forum works, since we want people to have EthMagicians accounts anyway, and Discourse has moderation and roles built in.

We may use the accounts you setup for [@mariapaulafn](/u/mariapaulafn) & myself, but we haven’t had a use case yet.

---

**virgil** (2019-02-25):

Indeed, [notes.ethereum.org](http://notes.ethereum.org) isn’t so great as large-public collaboration.  Let me know if you decide to step up your use of [notes.ethereum.org](http://notes.ethereum.org) internally.  For large public collaboration, ethereum.wiki should be able to eventually handle that use-case fairly well—the new version will be out in 1-2 months.

Of course, there’s always the forum too.

---

**boris** (2019-02-25):

Yeah I want to potentially port the EthMagicians GitHub wiki there. Would you be OK with that?

I’ll have a discussion and get at least one other maintainer type person if there is agremeent, and then I’d do a PR to move the content over in bulk.

HackMD has the benefit of real-time so really good for Council. But it also doesn’t usually get griefed in real-time. Yet.

---

**virgil** (2019-02-26):

As for porting over the EthMagicians Wiki, give me two months (so, late April) until the new [ethereum.wiki](https://ethereum.wiki) using WikiJS 2.0 is out.  I predict you all will like it, and if you do, then we can just use ethereum.wiki for both.  If you don’t like it, then go for it.

---

**mariapaulafn** (2019-02-28):

Hi! you can ping me for updates if you wanna join a ring - im putting together the agenda

