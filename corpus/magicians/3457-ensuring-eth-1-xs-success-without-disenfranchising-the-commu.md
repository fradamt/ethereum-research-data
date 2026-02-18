---
source: magicians
topic_id: 3457
title: Ensuring ETH 1.x's Success Without Disenfranchising The Community
author: timbeiko
date: "2019-07-08"
category: Working Groups > Ethereum 1.x Ring
tags: [ethereum-roadmap, eip-process, istanbul]
url: https://ethereum-magicians.org/t/ensuring-eth-1-xs-success-without-disenfranchising-the-community/3457
views: 2486
likes: 11
posts_count: 11
---

# Ensuring ETH 1.x's Success Without Disenfranchising The Community

I believe that the process leading to the Istanbul Network Upgrade process has highlighted a tradeoff between ensuring the success of Ethereum 1.x and properly considering all of the EIPs proposed by the Ethereum community.

Even without the 1.x initiatives, Istanbul has more proposed EIPs than any previous Ethereum network upgrade (see [this](https://twitter.com/alexberegszaszi/status/1143555729133101057)). A significant of the time on the AllCoreDevs calls leading up to both the EIPs submission deadline (May 17th) and client implementation deadline (July 19th

) has been spent discussing these.

> eips1582×420 58 KB

> Picture from the tweet linked above, showing how big Istanbul (top row) would be relative to previous network upgrades if all proposed EIPs got accepted.

This has the consequence that many of the 1.x initiatives have gotten very little attention in the process and that, as of now, not a single “1.x EIP” has been moved to `Accepted` for the Istanbul upgrade. This has led to some frustration about the process, as expressed during the last AllCoreDevs call:

https://twitter.com/TimBeiko/status/1147045097772634113

While some of the 1.x initiatives require more work and may not be ready for Istanbul anyways, if nothing in the process changes, we run the risk of arriving at the next network upgrade (April 2020?) and again having a large number of “community EIPs” compared to the amount of “1.x EIPs”.

At the same time, it seems that our current process has also done a poor job of addressing several of these “community EIPs” such as ProgPow, EIP-615, etc., leaving the community members for these initiatives feeling disenfranchised.

While these EIPs offer genuine improvements, they are not on the “1.x critical path” and require a significant resource commitment from EIPs champions, core developers, EIP editors, etc. **There is thus a tradeoff between the time and attention spent on these vs. the 1.x initiatives. Judging by how satisfied both sides are with the current process, we have so far handled it poorly.**

There are a few proposals about how we may move things forward, and I think we should discuss them in more details here.

### 1. ’s

Based on this framework, if non-1.x initiatives become more “1.x-ey” and form working groups to move their projects further along before formalizing them into EIPs, they may have a better shot at succeeding, while removing some of the “top of the funnel” burden on EIP editors and core developers. To some extent, ProgPow seems to have done this.

### 2. Explicit guidelines about what EIPs should be prioritized.

While this is obviously controversial (i.e. Who sets the guidelines? To optimize what? When/how do we change them?), it may be worth trying to prioritize EIPs which are on the 1.x critical path or that are simple to implement *and* provide high ROI (i.e. chain ID opcode, BLAKE2b precompile, etc.), a.k.a. “quick wins”.

The obvious risk here is that we disenfranchise community members who have EIP proposals that don’t fall in this bucket.

### 3. “1.x-only” Network Upgrades

A less radical alternative to #2 may be to have network upgrades that are exclusive to 1.x initiatives as well as “open” network upgrades, which would be open the equivalent of our current process. Again, once caveat being that defining what is OK for these 1.x upgrades would be contentious.

There has been some push to have more frequent network upgrades (see [here](https://ethereum-magicians.org/t/more-frequent-smaller-hardforks-vs-less-frequent-larger-ones/2929)) as well as a push for a more regular upgrade cadence (see [EIP-1872](https://eips.ethereum.org/EIPS/eip-1872)).

For example, with a 3 month cadence, you could have “open” upgrades more or less as frequently as today, with an additional “1.x” upgrade every 3 months. It could also be possible for 1.x EIPs to be included in the “open” upgrades.

The biggest concerns against such frequent upgrades was the time it takes to understand, implement and test EIPs. Given that most 1.x initiatives are well known and that a fair bit of the work happens in working groups, these would be somewhat mitigated.

---

Neither of these options feels perfect at the moment, but I believe it’s worth kickstarting a discussion about how we can make rapid progress on the 1.x initiative, keep non 1.x contributors as part of the community and reduce the burden on core developers… which we can think of as the “EIPs [Scalability Trilemma](https://www.jeffersoncapital.info/the-scalability-trilemma/)” ![:stuck_out_tongue:](https://ethereum-magicians.org/images/emoji/twitter/stuck_out_tongue.png?v=15)

## Replies

**boris** (2019-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> At the same time, it seems that our current process has also done a poor job of addressing several of these “community EIPs” such as ProgPow, EIP-615, etc., leaving the community members for these initiatives feeling disenfranchised.

To speak on EIP615, we don’t feel disenfranchised. We gathered a wide amount of technical support, and our working group didn’t get funded because “someone at the EF doesn’t like Boris” (that’s the only feedback we actually got). Was it perfect or accepted yet? No – but we couldn’t commit the time to do a Geth and Parity implementation without funding, so that people could disagree with an actual implementation.

(2) I don’t think prioritizing EIPs makes much sense. Any team that has funding (from a company sponsor, from grants, whatever) or sufficient volunteer time CAN move an EIP forward.

(3) I think the process could use improvement and that’s where the stall is. If there are written objections to an EIP going in and/or actionable tasks to do to improve an EIP – they can get done if (2) is available.

---

**timbeiko** (2019-07-08):

Thanks for the color, [@boris](/u/boris)!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> (2) I don’t think prioritizing EIPs makes much sense. Any team that has funding (from a company sponsor, from grants, whatever) or sufficient volunteer time CAN move an EIP forward.

I agree that a team with enough resources can move the EIP forward. What I meant by that is how can we better allocate the time + attention of core devs to focus on the highest impact proposals. I agree this is probably not the right approach, though.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> (3) I think the process could use improvement and that’s where the stall is. If there are written objections to an EIP going in and/or actionable tasks to do to improve an EIP – they can get done if (2) is available.

I agree with the first sentence, but IMO a lot of the pushback that we have seen on EIPs isn’t a clear written objection as much as “this seems complicated, the benefits are unclear (a.k.a. it’s not on the critical path, and there are risks”. For ProgPow, we’ve had the audit, but that mostly seems to have kicked the can down the road, and it’s probably not a realistic approach to most similar projects.

---

**boris** (2019-07-08):

Yes. I’m suggesting that unless there are clear written objections and “over my dead body” push back — the updates go in.

If not even one person is willing to write down why they don’t want something in, why shouldn’t it go in?

(again, assume implementation, tests, etc if you like. Otherwise it’s even worse — “I don’t like this spec and don’t want to bother changing 1x” or some such reason)

The reverse, of one person veto’ing, is a whole other situation we have to work through.

If Community EIPs can’t get through (let’s ignore the funding part for the moment) then governance is already captured by the people at the EF who work on this full time.

I don’t see proposals from Parity & don’t expect to, and seems like there aren’t any from Pegasys either?

---

**timbeiko** (2019-07-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Yes. I’m suggesting that unless there are clear written objections and “over my dead body” push back — the updates go in.
>
>
> If not even one person is willing to write down why they don’t want something in, why shouldn’t it go in?

I think this has to do with our current process, as you said. It’s often not that anyone *opposes* an idea, but more that properly analyzing, discussing, testing, etc.-ing it has a high opportunity cost.

I think Alexey’s post that I link above addresses this to some extent: if EIPs arrive in a “final” stage you both 1. weed out some of them and 2. have higher quality proposals for people to review.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> If Community EIPs can’t get through (let’s ignore the funding part for the moment) then governance is already captured by the people at the EF who work on this full time.
>
>
> I don’t see proposals from Parity & don’t expect to, and seems like there aren’t any from Pegasys either?

This is a valid concern. FWIW, for the two accepted Istanbul EIPs so far, IIRC one was by Parity (Account Versioning) and the other was pushed by the ZCash Foundation (along with the EF). PegaSys hasn’t proposed a Core EIP yet.

---

**boris** (2019-07-08):

EIPs in final stage are also irrelevant. Or rather, not sufficient.

Get the EIP Accepted (or not) but work implementation and tests and the EIP spec in parallel.

Before making it into an HF — updating the spec to align with implementations is low cost.

---

**anett** (2019-07-09):

What you guys think about having a discussion on this topic during the Magicians Berlin Council ?

---

**timbeiko** (2019-07-09):

I won’t be there, but if there is a discussion on this, please share the outputs back here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**gcolvin** (2019-07-09):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> To speak on EIP615, we don’t feel disenfranchised. We gathered a wide amount of technical support, and our working group didn’t get funded because “someone at the EF doesn’t like Boris” (that’s the only feedback we actually got).

That’s about as much feedback as I got two years ago.  The EF’s process is completely broken.  The community needs to find ways to thrive despite their incompetence.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> we couldn’t commit the time to do a Geth and Parity implementation without funding, so that people could disagree with an actual implementation.

There is and has long been an actual C++ implementation.

---

**gcolvin** (2019-07-10):

What might help is a two-stage approval process.  First, decide whether we intend to include a proposal in a future fork.  And later, which fork it is ready to go in.  As it is we get in a bind where we don’t want to accept unimplemented or incompletely implemented proposals, but don’t want to implement proposals we aren’t confident will be accepted.

---

**timbeiko** (2019-07-10):

I like this idea, [@gcolvin](/u/gcolvin)! I think it could also help fund some earlier research for certain initiatives we agree are conceptually important, but don’t have a full spec for.

