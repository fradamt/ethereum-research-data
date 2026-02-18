---
source: magicians
topic_id: 2725
title: ETH1x Roadmap AMA live at ETHCC, March 7th
author: boris
date: "2019-02-22"
category: Protocol Calls & happenings
tags: [eth1x, ethereum-roadmap, council-paris-2019, ethcc2019]
url: https://ethereum-magicians.org/t/eth1x-roadmap-ama-live-at-ethcc-march-7th/2725
views: 2615
likes: 15
posts_count: 16
---

# ETH1x Roadmap AMA live at ETHCC, March 7th

Slide source on HackMD https://hackmd.io/cw53nKUOR1SrAbnYX2SX_g

[Slide mode link](https://hackmd.io/p/rJ4z48jHV)

---

## Important Links & Topics

### Storage Fees

### Istanbul Hardfork

Roadmap on Ethereum wiki: https://en.ethereum.wiki/roadmap

Istanbul hardfork details on Ethereum wiki: https://en.ethereum.wiki/roadmap/istanbul

## Session Planning

I have confirmation that we have one hour on March 7th at [ETHCC](https://ethcc.io) to discuss this. It is [on the ETHCC schedule](https://ethcc.io/images/schedule/EthCCcomplete.pdf) under my name for 16:00 in Robert Faure.

My goal for it is to have a space where people can come and share the questions they have, and either get pointed to resources – like EthHub or the [roadmap on the wiki](https://en.ethereum.wiki/roadmap/) – or capture those questions so that we can have discussions and find answers to them.

The guiding question is “What is the ETH1x Roadmap?”. Necessarily, this connects into planning for ETH2, and I definitely think there are a lot of ETH1 to ETH2 questions that are still open.

[@lrettig](/u/lrettig) said previously that he would volunteer to facilitate. I believe that a fishbowl format as we did for the ETH2 session at Council of Prague would be good to run this.

For now, I’m asking for your help in:

- gathering resources – do you have good ETH1x materials to share like @AlexeyAkhunov’s state rent writings and presentations?
- gathering questions – what questions do you have? Post them as a comment, and people can “heart” them if they have the same question.

## Follow Up

The [#working-groups:ethereum-1-x-ring](/c/working-groups/ethereum-1-x-ring/33) is the place for discussion and further work. The [#istanbul](https://ethereum-magicians.org/tags/istanbul) tag can be used to track items related to the upcoming hard fork.

This post can be edited directly, or leave comments.

## Replies

**boris** (2019-02-22):

The ETH Roadmap Webinar has full notes and video available which is great background reading and viewing:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png)

      [ETH Roadmap AMA - Webinar Feb 6th, 8AM PST / 1700 UTC+1](https://ethereum-magicians.org/t/eth-roadmap-ama-webinar-feb-6th-8am-pst-1700-utc-1/2518/2) [Ethereum 1.x Ring](/c/working-groups/ethereum-1-x-ring/33)




> [alexey-potential-timeline-hardforks]
> Thank you to @AlexeyAkhunov @holiman Paul @axic @lrettig for answering questions / providing an overview. From my point of view, incredibly valuable and very helpful.
> Thank you to @timbeiko for early note taking and everyone for their participation and listening.
> The notes are in the same HackMD link, but I have pasted them below to keep all content together.
> The two action items I’ve pulled up top here, plus added (3).
> (1) ETH1x Alternate Chain
> Use Co…

---

**lrettig** (2019-02-25):

[@AlexeyAkhunov](/u/alexeyakhunov) will sadly be unable to join in person but maybe we could get him to join virtually? It would be good to list questions here ahead of time so that Alexey and I can discuss them and make sure we’re prepared to answer them!

---

**boris** (2019-02-26):

Yep that’s the plan to gather questions ahead of time. I just wikified the OP so we can use it directly to gather questions.

I’m looking to get other people who have opinions on the roadmap signed up ahead of time too.

---

**jpitts** (2019-02-26):

We are all going to have to do some studying ahead of this AMA!

---

**AlexeyAkhunov** (2019-02-26):

I have started working on some potentially pivotal changes in State Fees (rent) proposals - need to do some data analysis on the stateless client. Will try to get something up before that AMA

---

**MrChico** (2019-02-27):

I’ll be there! Any idea on more precise time and location?

---

**boris** (2019-02-27):

Yes! Just edited the post to indicate that it’s in the schedule for 16:00 in the Robert Faure room.

Do you have any questions or a thing you want to talk about? Please edit!

---

**wmougayar** (2019-03-07):

Is there a primer for migrating from 1.x to 2.0?

---

**boris** (2019-03-08):

This (incorrect) roadmap is why we need to be more realistic and clear about ETH1x and ETH2 timelines. The more these “fast” dates float around, the more disappointment the realistic timelines will bring.

https://twitter.com/Delphi_Digital/status/1103682416802258946

---

**timbeiko** (2019-03-08):

What part specifically do you think is wrong? This seems more or less in line with what I’ve seen communicated elsewhere.

---

**boris** (2019-03-08):

Timelines. ETH2 still has unknown components. And there is nothing that dapp developers or users can interact with until all of Phase 2. So how do we balance the realism of timing, with continued usage and adoption of ETH1?

---

**tvanepps** (2019-03-11):

Hey [@boris](/u/boris) - just adding Alexey’s interview from Epicenter as mentioned in the ETHCC 1.x talk

---

**tvanepps** (2019-03-11):

pulling from Danny Ryan’s interview from Zero Knowledge on what happens to ETH 1 potentially moving to Eth 2.0 as a unique shard or otherwise:

https://medium.com/@trenton.v/zero-knowledge-x-danny-ryan-e3526cf61210

Here is a rough transcript of his comments:

- Whether ETH 1.x becomes a shard is really a community question, a research question. Though there are some technical challenges depending on the option.
- Option 1: Roll ETH 1.0 into 2.0 once it reached an acceptable stability. (but how?)
- Option 1A: 1.x as exceptional shard construction — however, separate rules from other shards and a legacy code base is really bad combination. Also wouldn’t be compatible with forecasted need for state fees.
- Option 1B (favored by danny): write EVM interpreter in WASM. deploy as contract on ETH2.0— fork state root into contract and ether balances, then users can interact with 1.0 state by providing “merkel witnesses.” The community could then deprecate maintenance for ETH 1.0 but still interact with the historic state. Stateless nature means there wouldn’t be any issues with state fees.
- Option 2: allow legacy chain to operate in perpetuity. At this point there is potential to use ETH 2.0 to finalise 1.0, allowing mining rewards to decrease further.
- Option 3: Have mining rewards be a function of how much ETH is left on ETH 1.0
- Generally, he thinks there are “promises” that need to be upheld, like an Augur market related to Mars that expires in many years.

---

**boris** (2019-03-11):

Thanks Trent – I just refactored the post to include links up top, too. So feel free to add comments as you’ve been doing or editing directly.

---

**boris** (2019-03-11):

Option 1 is an upgrade / migration, and pretty much requires coordination from existing users.

Option 1B seems most likely, and roughly what our EVM evolution work is planning for – that we HAVE to think about forward compatibility, make a plan for migration, and ideally evolve ETH1x so the migration is easier.

I’m not clear on the “wouldn’t be any issues with state fees” comment – because ETH2 shards have the same issue currently, and are likely to adopt similar state fees and/or need to solve it in some way.

