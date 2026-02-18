---
source: magicians
topic_id: 3721
title: A Train Station Model for Network Upgrades
author: timbeiko
date: "2019-10-23"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/a-train-station-model-for-network-upgrades/3721
views: 1587
likes: 17
posts_count: 11
---

# A Train Station Model for Network Upgrades

[@shemnon](/u/shemnon) and I gave a talk at devcon proposing a way to do network upgrades that combined a lot of the ideas discussed by the community over the past year (including the recently discussed [EIP-centric forking](https://ethereum-magicians.org/t/eip-centric-forking/3536/9)).

I wanted to share it here so that we can try and use EthMagicians as the official discussion forum for it.

Here is the proposal: https://medium.com/@timbeiko/train-planes-network-upgrades-6edfc9f6b7dd

## Replies

**antonydenyer** (2019-10-24):

It’s worth noting that a number of large software projects follow this kind of process [Software_release_train](https://en.wikipedia.org/wiki/Software_release_train). I think the main risk with a 6-month release cycle is that everyone panics and tries to pile on so as not to miss the train! It’s a definite improvement on the current process.

---

**timbeiko** (2019-10-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/antonydenyer/48/15779_2.png) antonydenyer:

> I think the main risk with a 6-month release cycle is that everyone panics and tries to pile on so as not to miss the train! It’s a definite improvement on the current process.

Agreed, but that’s already the case with our current process ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12)! Everyone piled in on May 17th when it was the deadline for Istanbul. I think that not knowing *when* the next upgrade is accentuates this problem, though.

Also, we sort of did this already, by moving a lot of EIPs that weren’t ready for Istanbul to a “Tentatively Accepted” state for what was first called “Istanbul 2” and now is “Berlin”, see: [EIP-2070: Hardfork Meta: Berlin](https://eips.ethereum.org/EIPS/eip-2070)

This framework makes that process more explicit ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**souptacular** (2019-10-24):

I think the article was great! My initial thoughts are the following:

- I think having 2 forks a year in a schedule is a good first step since we are currently at 1 fork a year. We don’t want to move too fast.
- On the other hand, we have important 1x tasks ahead if we want to control state growth and I worry that 2 HF’s a year may be too little for that to progress effectively. Maybe @AlexeyAkhunov can chime in.

---

**timbeiko** (2019-10-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/souptacular/48/720_2.png) souptacular:

> On the other hand, we have important 1x tasks ahead if we want to control state growth and I worry that 2 HF’s a year may be too little for that to progress effectively. Maybe @AlexeyAkhunov can chime in.

Agreed! I’d like to know of specific cases requiring >2 HFs per year.

We could keep everything else in the proposal and have HFs every quarter instead of every six months, but that just seems unrealistic for now given our prior cadence.

---

**AlexeyAkhunov** (2019-10-24):

Although it is a bit too early to say how many hard forks are required for the introduction of Stateless Ethereum (because we have various options along the way), I currently think 2 per year should be enough. I am hoping to start publishing more details of the proposed transitions soon, as we are getting close to releasing Turbo-Geth and verifying some assumptions about block witnesses

---

**rumkin** (2019-10-25):

As addition to this proposal. I want suggest to replace hardfork names with version numbers pointed to year and month fork originated to like Node.js and Ubuntu have. Current naming model is highly confusing and it’s just impossible to say which hardfork is the latest.

---

**timbeiko** (2019-10-25):

While I agree with the idea of using numbers instead of names (at least in the code — names are fun from a marketing/community perspective!), I think it’s a sufficiently disjoint idea to consider it independently from this proposal.

---

**tvanepps** (2019-10-25):

why not both - fun names for the community and #'s for developers

---

**timbeiko** (2019-10-25):

Yep, that’s what I was saying. Use numbers in the code, and “marketing names” with the community.

---

**rumkin** (2019-10-27):

Trains and schedules are tightly coupled, and it seams logical to me to append this item. With such addition your proposal looks completed to me. So maybe you’ll change your decision. And, if it will be decided by core members, disjoin it into separate proposal after discussion.

