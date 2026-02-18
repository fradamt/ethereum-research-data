---
source: magicians
topic_id: 2647
title: "EIP 1193: Provider Ring Call/Meeting"
author: davidmurdoch
date: "2019-02-13"
category: Working Groups > Provider Ring
tags: [community-call, eip-1193, eip-1102]
url: https://ethereum-magicians.org/t/eip-1193-provider-ring-call-meeting/2647
views: 1750
likes: 4
posts_count: 6
---

# EIP 1193: Provider Ring Call/Meeting

Hello, all! I’m one of the maintainers of Ganache, along with [@benjamincburns](/u/benjamincburns). We are a bit late to the party and have only recently become aware of EIP 1102 and 1193. We’d love to schedule some time to get all of us on the same page regarding the goals, scope, deprecation, and release schedule of EIP 1193.

I’d like to get as many Ethereum JavaScript provider representatives on the call as possible.

The purpose of the call is to bring all providers together in order to more quickly come to consensus on the EIP, as well as organize a tentative deprecation of existing provider APIs and careful rollout plan for the EIP.

Scheduling a call like this across global timezones is tricky; if you could respond with your UTC timezone offset i’ll try to choose a time that reasonably accommodates all parties before following up with a Doodle poll so we can vote on the best day.

The call will be held over Zoom and will be schedule for an hour. Agenda to follow.

## Replies

**boris** (2019-02-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/davidmurdoch/48/1496_2.png) davidmurdoch:

> Scheduling a call like this across global timezones is tricky; if you could respond with your UTC timezone offset i’ll try to choose a time that reasonably accommodates all parties before following up with a Doodle poll so we can vote on the best day.

I highly recommend you just pick a time that works for the hosts and don’t bother Doodle’ing. Have a second call if people can’t make it. 7am or 8am PST usually ends up being a good time, or 6am PST if your west-coasters can hack it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

Zoom’s “register” feature has ended up being useful to be able to email notify / remind people too.

---

**davidmurdoch** (2019-02-19):

Since there hasn’t been much of a response here I’m going ahead and scheduling the call for this **Friday, February 22nd at 2:00 PM UTC** (9AM Eastern, 6AM Pacific).

Zoom link: https://consensys.zoom.us/j/775654390

**Agenda:**

- Introductions
- Do we have a quorum of javascript ethereum providers on the call? If not, meeting stops here and we will reschedule after getting more providers on the call.
- Public API - does the current API overstep its bounds in any way? Conversely, should the API require more?

The API requires that emit be a public method but dapps really shouldn’t be using the provider interface as their own private event emitter instance. Should we remove this requirement? Will it break dapps?
- This EIP mentions a global namespace, but there is an EIP that explicitly covers that (EIP 1102)
- others? comment below
- off isn’t required, but removeListener is. on is required, but addListener isn’t. Should these on/off removeListener/addListener aliases all be added to the list required methods?

EIP 1102 - adding `ethereum` to the window namespace  - should EIP be an IETF RFC, or at maybe prefixed (a la https://developer.mozilla.org/en-US/docs/Glossary/Vendor_Prefix) for now?
Web3.js EIP-1193 rollout and legacy-provider backwards compatibility.
Rollout is currently scheduled for March 1st. Should this date be updated?
Other comments or concerns?

Please comment below if this time will not work for you. Also, please comment here if you’d like to see something else added to the agenda.

---

**alexvandesande** (2019-02-20):

We have a conflicting schedule: the EF has a foundation wide call at the exact same time.

---

**davidmurdoch** (2019-02-20):

Ah, I didn’t realize there was a call this Friday morning. How long is is the call? Maybe we can schedule the Provider Ring call immediately after.

---

**davidmurdoch** (2019-02-22):

Reminder: Call begins in 10 minutes.

