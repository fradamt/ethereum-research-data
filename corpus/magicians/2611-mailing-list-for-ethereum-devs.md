---
source: magicians
topic_id: 2611
title: Mailing list for ethereum-devs
author: cdili
date: "2019-02-07"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/mailing-list-for-ethereum-devs/2611
views: 2369
likes: 11
posts_count: 22
---

# Mailing list for ethereum-devs

Anyone know someone from the Linux Foundation or can help set up a mailing list for ethereum-devs that’s like bitcoin-devs (https://lists.linuxfoundation.org/pipermail/bitcoin-dev and https://lists.linuxfoundation.org/mailman/listinfo/bitcoin-dev) ?

Thanks

## Replies

**boris** (2019-02-07):

I have gone ahead and emailed the info@ email address to get started. I can also email Brian Behlendorf from Hyperledger which is at Linux Foundation who can likely help.

---

**boris** (2019-02-07):

Also, as I’ve said elsewhere, another solution would be to have this forum and/or EthResearch enabled in Mailing List mode.

There is relevant info here about Discourse vs Mailing lists, including a bit of info about Mailing List mode → [Using Discourse instead of an email mailing list - Site Management - Discourse Meta](https://meta.discourse.org/t/discourse-vs-email-mailing-lists/54298)

I have requested that feature here for EthMagicians too. It is, in fact, issue 1 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)



      [github.com/ethereum-magicians/scrolls](https://github.com/ethereum-magicians/scrolls/issues/1)












####



        opened 09:47AM - 19 Jul 18 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/f/f207a85f5cc14cd4f2601b6642bf064bbec46ee2.jpeg)
          bmann](https://github.com/bmann)





          forum







I would like to see us turn on Discourse's mailing list mode so people can reply[…]() by email. This is the high level description / config around it: https://meta.discourse.org/t/configuring-reply-via-email-e-mail/42026

It looks like we can also use Discourse as our home base for organizing / planning / sponsorships as well with having email addresses mapped to groups. This is the article that talks about groups vs. categories https://meta.discourse.org/t/start-a-new-topic-via-email-e-mail/62977












I know [@lrettig](/u/lrettig) has grave concerns about further dilution of messaging. I saw [@cdili](/u/cdili) organize the Stanford meeting with manually cc’ing 60 people, which doesn’t seem ideal either.

Consider this a research and discussion thread.

---

**boris** (2019-03-29):

Answer via LF:

> the LF launched the “bitcoin core” mailing list at a time it was exploring playing some sort of governance role in the Bitcoin  ecosystem, an exploration that eventually led to the creation of Hyperledger, and meanwhile no one’s felt a need to find a new home for that list, and it doesn’t take up much resources, but does seem a bit unusual and I’d hate to be around if a real governance or moderation issue hit.  It was really a one-off though, and not likely to be done again without a really clear gap in the current Ethereum ecosystem, and a similar presumption of an eventual role for the LF in that.

So aside from forums, we’d need to look for an email solution.

---

**atoulme** (2019-03-29):

We just had a discussion on gitter on this.

I favor a mailing list, coming from the Apache Software Foundation mode that if it didn’t happen on the list, it didn’t happen.

---

**cdili** (2019-03-29):

Here’s the recent discussion https://gitter.im/ethereum/AllCoreDevs?at=5c9e47abb7e27d2f05a3a924

(Definitely favor mailing list.  I also don’t think we should try to be inventing too much and if some processes by Apache or IETF have been good enough for decades, and are an improvement to Ethereum’s, we should probably head in those directions.)

---

**jpitts** (2019-03-29):

I think that we should decentralize email lists and run them from our community Forums rather than go with the Linux Foundation, the EF, or any other traditional body.

I thought that this system was running in email mode and configured an email service to make it possible. I will find out why it may not be.

---

**jpitts** (2019-03-29):

Ok y’all, this is a setting that can be activated under your personal preferences. I will activate mine to see what it is like. I need to advertise this (if it actually works as advertised)

**Steps for users**

- Click on your profile pic in the top right
- Click on the gear to get to “Preferences”
- Click on “Emails” on the left nav, then scroll down
- Checkbox the “Enable mailing list mode”, then “Save”

Screen shot:

> image866×440 23.5 KB

[@chisel](/u/chisel) this gem could be something that can go into onboarding / new Magicians’ edu!

---

**cdili** (2019-03-29):

Thanks to you and others for setting up this forum.  But it isn’t decentralized is it?  The Linux Foundation seems more robust than some community members running a forum.

---

**jpitts** (2019-03-29):

The fact that there is no central point of comms and control makes it more decentralized IMO, considering that there are so many other groups which can also run Discourse servers.

Robustness is a concern though! Robustness without authority will come in time, with the infrastructure which the community is building.

---

**boris** (2019-03-29):

Can it ingest emails? ie reply to an email and it gets posted as a comment.

That’s the part that’s not setup. There is a GitHub issue for this in the Scrolls repo.

Also, should be enabled by default for new members.

---

**ajsutton** (2019-03-29):

Unfortunately for a number of people, myself included, this just doesn’t work. I used to follow along by email but one day they stopped coming and now I can’t even get the system to send me a password reset email.

---

**jpitts** (2019-03-29):

[@boris](/u/boris) I’ll test that function out, also will look into setting it as a default.

[@ajsutton](/u/ajsutton), this may be our use of Mailgun; it has blocked others before too. Perhaps I should switch to another provider, this is unacceptable.

---

**ajsutton** (2019-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jpitts/48/15152_2.png) jpitts:

> ajsutton, this may be our use of Mailgun; it has blocked others before too. Perhaps I should switch to another provider, this is unacceptable

I suspect it permanently disables delivery when it gets bounce notifications but there doesn’t seem to be any way to get it to try again. The IT team at work accidentally deleted my email address a little while back…

I’d definitely still prefer an actual mailing list where reply by email works reliably and predictably but forums do seem to be all the rage. Kids these days… ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=12)

---

**jpitts** (2019-03-30):

LOL, yeah this is how Greg and I arrived at Discourse. It seemed to be the best intersection between what the community needs (threaded forum), what the kids want (mobile friendly chatty social thing), what the old schoolers want (bare bones email list).

---

**jpitts** (2019-03-30):

I will try to tame Mailgun, hopefully I can find where it is blocking you.

---

**jpitts** (2019-03-30):

[@ajsutton](/u/ajsutton), I found where it was blocking you. There should be a restoration of emails to you.

Others affected include:[@MadeofTin](/u/madeoftin), several accounts at status.im, and several accounts at ConsenSys.

It is likely that these were flagged due to a temporary lapse in service, which led to email bounces.

---

**ajsutton** (2019-03-30):

Excellent, I did indeed receive this as an email. Thank you so much for looking into it.

There were a bunch of ConsenSys folk accidentally deleted along with me so I suspect all those were fall out from our IT help desk having a bad day.

---

**jpitts** (2019-03-30):

No problem, sorry I didn’t figure this out earlier.

RE: the original topic: I’m looking at the individual emails generated and sent to me, and this isn’t similar enough to a traditional mailing list. A reply in email does not work as it should, it seems as if I am required to first go to the Forum website to reply. Hopefully I can figure this one out too, but not optimistic.

---

**boris** (2019-03-30):

[@jpitts](/u/jpitts) I left you a reference in the original GitHub issue. It’s an old Discourse thread (from 2014) and the first link one uses POP and Gmail which is maybe not the best, but seems straightforward. There are links there to lots of other similar articles.

Let me know if I can help.

---

**boris** (2019-03-30):

Thanks Joseph Chow for checking in on Stanford hosting a mailing list (discussion via email).

My response:

Right now it looks like most want something that is more accessible on the web, and further splitting discussion doesn’t seem helpful, so proposing to keep building on EthMagicians.

Threading (which Gitter among other chats doesn’t do) is my personal must have.

Jamie is working on configuring Discourse so that reply-to works as well. Or will shout for help at me ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=9)

Then we can do a trial run with a topic / group in Discourse on EthMagicians that is members-only write, world read, and anyone can join. Basically means we can ban bad actors or those that are off topic, but by default has no barriers to entry.

I personally don’t really want a Stanford domain hosting this, and definitely don’t want Google hosting it, but would also be fine with mailman (or other tools). Once setup, any particular solution is not that hard to self host.


*(1 more replies not shown)*
