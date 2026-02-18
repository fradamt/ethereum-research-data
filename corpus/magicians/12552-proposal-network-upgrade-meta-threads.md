---
source: magicians
topic_id: 12552
title: "Proposal: Network Upgrade Meta Threads"
author: timbeiko
date: "2023-01-13"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/proposal-network-upgrade-meta-threads/12552
views: 2957
likes: 15
posts_count: 12
---

# Proposal: Network Upgrade Meta Threads

With Shanghai/Capella’s scope finalized, focus has begun shifting to Cancun/Deneb. But, before we get too far in planning that upgrade, it’s important to take a step back and consider improvements to our process.

**Ethereum has evolved a lot over the past year, on both the technical and human sides.** We now have a single, unified network running both the Beacon Chain and execution layer, two sets of client teams who must coordinate with each other (as well as with client-adjacent contributors across R&D, devops, security, etc.) and a growing number of non-client teams championing Ethereum Improvement Proposals (EIPs) & contributing to protocol changes. And, of course, opinions by the broader Ethereum community about the direction of the protocol have grown both in quantity and quality.

In order for protocol developers, researchers, and the broader community to agree upon and deliver on Ethereum’s ambitious roadmap, good coordination is paramount. In this vein, I’d like to propose the introduction of **Network Upgrade Meta Threads** to help facilitate higher-level discussion about the overall scope of upgrades. Let me explain!

## TL;DR

- I propose introducing Network Upgrade Meta Threads on Ethereum Magicians as a place for the community to discuss the best high-level scope/goals/size for network upgrades
- These threads, along with EIPs’ discussion-to and $UPGRADE-candidate (examples) threads, would serve as input for AllCoreDevs calls. This will hopefully improve the quality of our planning process

$UPGRADE-candidate threads should serve as the canonical place to catalogue community support/objection to certain EIPs

I propose we trial this process for Cancun/Deneb, and reevaluate after the upgrade whether it’s worth repeating

## Background

Today, the scope of network upgrades is decided upon during AllCoreDevs calls. Client developers consider various EIPs, debate their technical merits, and eventually arrive at a set of EIPs which they believe are technically sound, provide sufficient value relative to their complexity, and can be implemented together in a single network upgrade.

While this generally works well, there are some cases where it’s challenging for ACD to make a decision, let alone the optimal one, such as:

- When different community members have different preferences for EIPs, but there isn’t a strong technical reason in favour of one vs. another;
- When a proposed change is the “first step” towards a longer-term roadmap item, which may or may not change;
- When a set of candidate changes is too big for a single upgrade and must be spread out over multiple ones.

This is partially due to the nature of ACD, where the “units of concern” are EIPs. Most of the discussion on calls is about the technical merits of proposals, potential issues, how to best test them, etc. This is both good (we don’t want bad proposals to make it into an upgrade) and unsurprising (these domains are what most regular attendees are experts in).

When the discussion must move to a higher level, e.g. the relative prioritization of proposals, the opportunity costs of upgrade timing, etc., ACD calls don’t provide the ideal setting. Not only is this a big context switch from discussing technical tradeoffs, but these conversations often must happen quite rapidly (due to the time constraints on the call) and sometimes without all relevant stakeholders (given they may not be regular attendees).

That said, client developers *are* the ones who must ultimately write the code for these upgrades and hence must be core to the final decision about scope. This proposal hopes to provide a way to increase the quality of input into this decision-making process.

## Current Process

Today, network upgrades get planned roughly the following way:

1. EIP author writes a Core EIP: someone writes an EIP with a proposed change to Ethereum’s consensus rules. Discussions about the EIP often happen on EthMagicians.
2. Champion presents EIP on AllCoreDevs: an EIP champion, often the EIP author, comes on an AllCoreDevs call to present their EIP. In most cases, this leads to feedback from client teams and several rounds of iteration on the EIP.
3. Champion requests EIP inclusion for upgrade: when an upgrade is being planned, the EIP champion signals that they would like their EIP to be considered. Since Shanghai, this process has migrated to EthMagicians.
4. Client teams debate which EIPs should be considered: teams can come to either “weak” (“Considered for Inclusion”) or “strong” (“Included”) consensus on including the EIP.
5. Prototyping/testing/etc.: as teams work on the candidate EIPs for an upgrade and gain a deeper understanding of their implications, the scope gets refined. As more implementations and testing suites are available, when issues come up, client teams can determine whether it is better to fix issues with an EIP or remove it in favour of shipping the other ones quicker.
6. Testnet deployment: once teams are satisfied with their implementation and test coverage for a set of EIPs, those get bundled together for a test network upgrade.
7. Mainnet deployment: assuming the testnet deployment goes smoothly, the upgrade is now scheduled for mainnet.

As mentioned earlier, this process is very centered around the EIPs themselves. While this isn’t a perfectly accurate illustration of how every fork was planned (e.g. The Merge was quite different), it’s a rough sketch of the process.

## Network Upgrade Meta Threads

To provide both better input into the upgrade planning process as well as a formal venue for the broader community to voice their preferences, I believe we should introduce dedicated Ethereum Magicians thread focused on the “scope” and “size” of upgrades, rather than the technical details of EIPs.

These **Network Upgrade Meta Threads** would:

- Be created on EthMagicians when we begin planning a new upgrade (i.e. the Cancun one should probably already be up);
- Serve as a place to discuss topics such as:

What should be the main priority/priorities for the upgrade;
- When, roughly, should we aim for the upgrade to happen, and the tradeoffs of including a marginal feature vs. delaying;
- How to split multi-upgrade features across >1 upgrade, and the implications of including a subset of those features in a specific upgrade;

Be used as **input** into AllCoreDevs calls, but not serve as a venue for the final decision about upgrades’ scope. ACD would still be where the decision is made.

As with everything else on Ethereum Magicians, these threads would be open for all to share their views. The [ACD151 agenda](https://github.com/ethereum/pm/issues/675) has good examples of comments which would be appropriate for such a thread:

- 1856×1452 549 KB
- 1862×1308 342 KB

Hopefully, by having such a thread open for weeks/months prior to finalizing an upgrade’s scope, rather than hours/days, we can improve the quality of our prioritization.

## A note on $UPGRADE-candidate tags/threads

With the Shanghai upgrade, we trialed having EIP champions signal on Ethereum Magicians that they’d like their EIP considered for a network upgrade ([proposal](https://ethereum-magicians.org/t/shanghai-core-eip-consideration/10777)).

This was done by adding a `shanghai-candidate` tag to either the EIP’s `discussion-to` thread on Ethereum Magicians, or by opening a new thread to discuss the EIP’s inclusion in the fork, like for [EIP-1153](https://ethereum-magicians.org/t/shanghai-candidate-eip-1153-transient-storage/10784).

[![](https://ethereum-magicians.org/uploads/default/optimized/2X/5/54842bac8253affb47e62af7b4acb8cb5ebcf73a_2_690x388.png)1580×890 137 KB](https://ethereum-magicians.org/uploads/default/54842bac8253affb47e62af7b4acb8cb5ebcf73a)

For EIPs where strong community support matters, this latter option can be a great way to catalogue support for and objections to the EIP, for which discussions can happen anywhere. Moving towards doing this in Ethereum Magicians threads can help avoid EIPs having to reinvent the wheel to document this information. A good forum templates for these posts could serve as an alternative to full blown EIP websites, such as [eip4844.com](http://eip4844.com).

## Putting It All Together

With the introduction of Network Upgrade Meta Threads, the upgrade process would rely on the following components:

- EIPs: technical specifications for changes (coupled with executable specs)
- discussion-to threads: async discussion of technical EIP details
- $UPGRADE-candidate tags/threads: async proposal to consider an EIP for an upgrade, cataloging support, objections, status updates, etc.
- Network Upgrade Meta Threads: async discussion of network upgrade scope/size/relative priorities
- AllCoreDevs calls: synchronous discussion of EIPs and network upgrades scope, relying on all the above as input

## Next Steps

First, I’d like to get feedback both here and on AllCoreDevs about whether introducing these threads would be beneficial. Assuming this is the case, then I suggest we trial the process for Cancun and reevaluate afterwards.

## Replies

**moodysalem** (2023-01-13):

Firstly, I think the network upgrade threads would be an improvement to the process. The current fork scope planning takes place across many different forums, and having a single place to discuss prioritization per fork would be useful. I also agree it’s challenging to come to the best decisions under the time constraint of ACD calls.

However I would like to see a more significant change to the process in order to incorporate the missing stakeholders–users and application developers.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> That said, client developers are the ones who must ultimately write the code for these upgrades and hence must be core to the final decision about scope. This proposal hopes to provide a way to increase the quality of input into this decision-making process.

Scope here is a very overloaded term. There are two processes happening in tandem here: deciding what is a good idea to implement (e.g. consider for inclusion) and deciding the order in which they are implemented (prioritization). Today, client developers are responsible for both. I feel these two processes should be separated.

Client developers are in a great place to determine which changes are good changes. Client developers are also in the best place to determine how many changes can safely go into a fork. They are familiar with the code and know much complexity can be safely managed, whether an EIP is implemented correctly and well tested, etc… So they should be the final decision makers on which changes are eligible for inclusion and how many changes can go into a fork.

But client developers are not always in the best place to determine the order in which many good changes should be implemented. The process of sorting many good changes needs to be focused on user feedback.

Given the large number of changes that are CFI, I would like to see ordering of other smaller changes (e.g. EOF, EXTSLOAD, TSTORE, deactivate SELFDESTRUCT) come from the community. For the process of sorting among good changes I’d propose collecting votes from activate validators. Validators could select the order of changes they’d like to see, and the rankings can be aggregated to come up with a final ordering. Client developers can agree to respect the ordering and implement the changes in the consensus ordering on the ACD call.

I know many are concerned that any kind of token voting leads to governance capture. I don’t think those concerns apply to this proposal for two reasons–validators have a vested interest in building the best blockchain network, and client developers still decide the eligible set of changes. Ethereum is supposed to make human coordination problems easier, and I think it would be a big miss to not use Ethereum to help with the issue at hand.

---

**mcdee** (2023-01-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/moodysalem/48/4982_2.png) moodysalem:

> For the process of sorting among good changes I’d propose collecting votes from activate validators

No comment about the general idea of voting, but this isn’t a good set of users from which to take votes.  All of the examples you gave are on the execution layer, and anyone who is purely focused on the consensus side will have no idea of the relative importance of such features.

---

**jessepollak** (2023-01-15):

*TL;DR I believe that the process proposed here would be an iterative, positive improvement on the overall Ethereum prioritization and execution process. I am in favor of experimenting with in 2023 and re-evaluating at the end of the year whether it’s something we should continue or iterate on.*

**Background**

Over the last year, Coinbase has begun making a concerted effort to contribute to overall Ethereum core development, primarily through our work on EIP4844. As we’ve ramped up in these contributions, I’ve felt grateful for the way we’ve been welcomed into the existing process and feel like we’ve been able to make a positive impact within the context of it. The primary touch points for us have been (0) shipping code to many clients, including Geth, Prysm, Lodestar, Erigon and playing a leadership role in driving 4844 forward; (1) regularly attending the ACD calls and sharing our perspectives on progress, technical viability, and prioritization; (2) participating in Devcon and the workshops & prioritization discussions there; (3) coordinating the weekly 4844 implementers call with other Core Devs. In these processes, our goal has been to listen and learn (we’re still new!) while also sharing our perspective on how we believe Ethereum can best evolve.

**Areas of room for improvement**

While overall our experience has been very positive, we’ve also experienced first hand some challenges with the existing process, including:

- Friction around sharing perspectives, particularly on priority, in ACD calls
- Lack of clarity on where we should be sharing our perspective given that feedback
- Uncertainty around whether our perspective is valued and, if not, how we could change that

We’ve had a number of conversations with folks across the Ethereum community about these challenges and at every stage have been met with kindness, openness, and a willingness to explore new ways of working together.

**Recommendation**

I believe that Tim’s recommendation of Network Upgrade Meta Threads would be a significant positive improvement in directly addressing some of the challenges we’ve faced. In particular, it would (a) reaffirm that community input from stakeholders like Coinbase is valued; (b) clarify where and how that input should be provided; (c) provide more information for decision makers to better weigh overall Ethereum roadmap prioritization. Based on this, I’d like to see this proposal adopted for 2023, with a commitment to reflect on its success at the end of the year and iterate from there.

As a preview of how you could expect Coinbase to participate in future Network Upgrade Threads, I wanted to share [this internal document (now public) that we wrote in December 2023 as we weighed overall prioritization for H120223](https://docs.google.com/document/d/1-BVDy8B7OZoh54OOEiQUTPtkA8XOh6xpH3c85VgfODU/edit). Our goal in writing this was to *align internally* on the current status of the Ethereum roadmap and what we thought the best sequencing would be. However, I suspect that sharing this thinking publicly for future network upgrades would be a helpful input (among many) as the community decides on priority.

**Future work**

I agree with [@moodysalem](/u/moodysalem)’s observation that right now client developers are responsible for both deciding what is a good idea to implement and prioritizing those ideas. I also believe that it may make sense to further explore separating these concerns in the future by adding a new process and/or decision making structure for making final prioritization decisions.

That said, I believe that the current process and decision making structure has served us well over the last many years, and given the overall importance of Ethereum, I would rather we move slowly and deliberately in changing things. To that end, I’d recommend we experiment with Network Upgrade Meta Threads first (i.e. giving existing decision makers better information) before considering other changes (e.g. changing who is making decisions).

---

**timbeiko** (2023-01-19):

We agreed on ACDE#153 to try this for Cancun - first Network Upgrade Meta Thread up here: [Cancun Network Upgrade Meta Thread](https://ethereum-magicians.org/t/cancun-network-upgrade-meta-thread/12060)

---

**Pandapip1** (2023-01-19):

How about we make HFMs again? At the very least, a summary of the EIPs included in major upgrades seems like good content for Meta-EIPs.

---

**timbeiko** (2023-01-19):

If we move to using the executable spec, we can also do proper releases of the spec that list the EIPs. Agreed having better lists of “what’s in the fork” beyond the README in that repo would be nice. Not necessarily opposed to Meta EIPs, but I’d like to better understand why we stopped doing them before we bring them back!

---

**crypto** (2023-01-20):

I am on the same page as [@jessepollak](/u/jessepollak), this should be a fully adopted proposal/initiative for 2023 and I’m glad this is happening before major scaling upgrades such as PDS (4844), DS,and others. On top of that, the community input is going to officialy be valued, I would assume that the goal of this forum is to start a long proccess (or first step) towards governance decentralization and possibly on-chain voting (looong teeeerm). Looking from the outside, it’s clever to think that Ethereum’s roadmap is fully community-led, when in fact now more than ever that’s materializing. I’m excited about the moment we’re in on Ethereum and contirbuting to this fantastic ecossystem is the first and foremost priority we can do as Blockchain researchers. [@timbeiko](/u/timbeiko) congrats for the initiative.

Btw, jesse your internal doc is not public (Google docs link broken)

---

**jessepollak** (2023-01-22):

Whoops, fixed the link so it should be publicly accessible [here](https://docs.google.com/document/d/1-BVDy8B7OZoh54OOEiQUTPtkA8XOh6xpH3c85VgfODU/edit) now. Thanks for flagging!

---

**sarareynolds** (2023-02-14):

Sounds like we are already going forward with this proposal but just wanted to drop some of my own feedback/experience here. Overall, I think introducing this forum will be a net positive change to the current process and certainly worth trialing for Cancun/Deneb but I don’t think it will fundamentally change much.

With regards to this specific thought:

"

> That said, client developers are the ones who must ultimately write the code for these upgrades and hence must be core to the final decision about scope. This proposal hopes to provide a way to increase the quality of input into this decision-making process.

”

This doesn’t necessarily address the case in which other developers who may not be considered core devs meaningfully contribute to core code and testing suites. In my experience, there is not a system in place for this kind of contribution, one that comes from those who are not “core devs” but who understand the code, use cases, and benefits to the ecosystem. There should be encouragement on this front and a stronger effort to incorporate those opinions better and with heavier weight. It is unfortunate that only EIPs that have a core dev champion or those that have been implemented by core devs themselves are the ones that get prioritized.

With any upgrade process, contributing to core code will always be bottlenecked by the decision makers. In the current structure, because those that make decisions about the prioritization of changes are the same group of people that implement the changes, those that are outside this process will naturally and continually be deprioritized.

Overall, I think there is a need to introduce other decision makers outside of core devs, who have tangible and prove-able knowledge about a subject that betters the ecosystem, but who also have similarly weighted input in upgrade discussions. This should be on threads (which it sounds like this will help) but also in ACD style calls, as that is ultimately where these decisions are made. I could imagine the EF supporting some kind of focused working group that is invited to speak at ACD and who’s thoughts/inputs/opinions are weighed *with* core devs. I understand the desire for change to happen slowly but I hope this provides some perspective on why I think the decision making process needs to be democratized amongst a group that represents all facets of the ecosystem.

---

**timbeiko** (2023-02-15):

Thanks for sharing your thoughts, [@sarareynolds](/u/sarareynolds)!

At a high level, I think there are two different types of “external contributors” that are worth separating: EIP champions and “general protocol contributors”.

In the case of the former, my view is that it’s “necessary but not sufficient” to do the technical work to get an EIP in a spot where it is considered for mainnet inclusion. If that isn’t done, then it’s harder for client teams to approach it. That said, I don’t think a set of technical checkboxes can’t be the only requirement for something to go onto mainnet.

From a technical PoV, there’s a limited number of things client developers can focus on, so they will inevitably end up having to decide what to include vs. exclude, as with any software project. Of course, high quality implementations + test cases make their lives easier and can help here.

From a “social”/design PoV, it’s not clear that even given infinite client dev bandwidth we *should* implement every change that’s technically sound. Historically, there are many changes that both the community or client devs have rejected even though the specs were of very high quality (e.g. ProgPoW, Parity Multisig restore, etc.).

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/3e96dc/48.png) sarareynolds:

> In the current structure, because those that make decisions about the prioritization of changes are the same group of people that implement the changes, those that are outside this process will naturally and continually be deprioritized.

I think the quote above is a good segway towards the other type of contributor,  “general protocol contributors”. We’ve seen a fair amount of non-client dev people get involved in governance and get a say, and empirically the “weight” their voice has tends to be a function of `time spent engaging * quality of engagement`.

That said, at the end of the day, client devs are the ones who maintain the software which runs the network, and have to deal with anything that goes wrong. Once concern they’ve echo’ed over the years is that EIP champions tend to be only focused on their own specific change, but then client teams are left to deal with anything resulting from it.

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/s/3e96dc/48.png) sarareynolds:

> Overall, I think there is a need to introduce other decision makers outside of core devs, who have tangible and prove-able knowledge about a subject that betters the ecosystem, but who also have similarly weighted input in upgrade discussions.

I’d argue that “the community” has had a pretty strong voice historically in being able to *stop* a decision from happening, even though core devs were on board (ProgPoW is probably the biggest example?), and to convince them of changes they may not feel particularly strongly about (e.g. PoW issuance reductions).

I think the spot where ACD is the weakest is making a call among many potential features that smart contract devs could benefit from (e.g. 1153 vs. 2537 vs. 3074). Being able to aggregate that and feed it as input into ACD would be valuable!

---

**sarareynolds** (2023-03-15):

> I think the spot where ACD is the weakest is making a call among many potential features that smart contract devs could benefit from (e.g. 1153 vs. 2537 vs. 3074). Being able to aggregate that and feed it as input into ACD would be valuable!

Thanks Tim, I think this is super valuable and will definitely take back to team & other devs. I agree it would be nice to understand from many projects/teams what application focused EIPs are important and evaluate them with tradeoffs in mind of impact vs. effort.

