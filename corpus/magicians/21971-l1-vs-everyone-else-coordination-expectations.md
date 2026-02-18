---
source: magicians
topic_id: 21971
title: L1 vs. Everyone Else Coordination Expectations
author: philknows
date: "2024-12-05"
category: Magicians > Process Improvement
tags: [eip-process]
url: https://ethereum-magicians.org/t/l1-vs-everyone-else-coordination-expectations/21971
views: 317
likes: 14
posts_count: 5
---

# L1 vs. Everyone Else Coordination Expectations

Reference: https://x.com/philngo_/status/1864695365775052940

Related to: [AllCoreDevs, Network Upgrade & EthMagicians Process Improvements](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157)

## Problem:

During [ACDE #201](https://www.youtube.com/live/Umh7ZKukmtY?si=54-NK4JW1UCwetqA&t=2166), I observed a clear gap in understanding the actual consensus required to support or object EIP inclusions. There is no clearly defined expectation of where contributors (new or existing) post sentiment/opinions on EIP inclusion for decision making.

Additionally, we lack communicating how non-L1 contributors can signal their support or objection to EIP inclusion except through participation on ACD calls where there isn’t a clear expectation for stakeholders to be present for decision making.

## Goals of this thread:

- Maintain integrity of the ACD process
- Maximize productive conversation of a limited coordinated timeslot
- Gather actual consensus from all stakeholders (not just client teams/researchers on ACD), such as consumers and builders of which the EIP affects downstream (via Breakout calls or other coordination processes such as RollCall)
- Have a soft/hard expectation for all members of the Ethereum community on how to participate in the EIP inclusion process and their interactions with ACD

## Questions

The following are questions I believe we should be able to answer as ACD participants. Akin to a “Frequently Asked Questions” about how contributors should collect, present and advocate for or against EIPs.

**Where should contributors coordinate their support?**

We currently have scattered platforms of information and it is not clear where “official” stances of teams should be posted for efficient and accurate consensus gathering. The scattered platforms of information are mainly: EthResearch, Ethereum Magicians, Twitter, Discord, Github (e.g. Breakout calls / L2 coordination calls) and client team blog posts.

1. There should be some expectation of aggregating high signal information into one place for signalling sentiment, especially when we expect to make decisions on EIP inclusion. This to me feels like EthMagicians and requires buy-in from the community.
2. What is the purpose of each platform? Here is my best guess:

- EthResearch: Data collection and presentation, theoretical research, protocol ideas
- EthMagicians: Persisted debates/opinions of EIPs and coordination processes for easy access and discovery. There needs to be a better way to curate support/opposition if threads get too long.
- Twitter: Communicating ideas/research to a larger platform and audience
- Discord: Instant messaging for public discourse on R&D and coordination topics
- Github (ethereum/pm): Scheduling and Agenda planning. Perhaps ACD agendas should incorporate hard commitments to ACD decisions so the relevant people can show up or leave support in thread
- Github (ethereum/*-spec): Continuous integration of shared specifications for implementors and discussion on spec-related implementation details.
- Client team blog posts: Signal official stances of client teams in support or opposition of ACD proposals.

**What should ACD timeshare be used for to maximize signal while minimizing noise?**

Here are some examples:

Encouraged:

- Updates to ongoing initiatives (e.g. Devnets, client implementations)
- Scheduled decision making on PRs for implementors
- Scheduled decision making on EIPs with relevant stakeholders present
- Providing summaries of decisions from breakout rooms and coordination calls (e.g. RollCall) related to ACD decision making
- Planned presentations where time permits

Discouraged:

- Highly specific technical debates that require more time/data/participants.
- Bringing in new PRs/EIPs which were not scheduled for decision making

**Which meetings should I attend?**

Contributors are highly encouraged to join relevant breakout sessions and regularly participate in the coordinated call which best fits their topic. E.g. Rollups should participate in Roll Calls, Verkle implementors should participate in Stateless Calls.

There should be an expectation that when an ACD agenda topic is relevant to your team/topic, you *should* have a representative at the ACD call, especially if decisions are scheduled to be made.

---

These are just some basic questions, but I feel like it would be beneficial to all stacks of the Ethereum community to have an expectation on how they can fairly participate and provide an effective feedback loop to Core Devs on decisions that affect everyone.

In the case of the example used in ACDE #201 and for decision making on [EIP-7762](https://eips.ethereum.org/EIPS/eip-7762), my two cents is that [EIP-7762: Increase MIN_BASE_FEE_PER_BLOB_GAS - #5 by benaadams](https://ethereum-magicians.org/t/eip-7762-increase-min-base-fee-per-blob-gas/20949/5) seems like the proper place to voice support/opposition in ACD along with aggregated links to data such as:

- https://research.2077.xyz/eip-7762-eip-7691-making-ethereum-blobs-great-again
- On Blob Markets, Base Fee Adjustments and Optimizations - Sharding - Ethereum Research

And relevant PRs such as:

- Update EIP-7762: add excess gas reset by adietrichs · Pull Request #9090 · ethereum/EIPs · GitHub

If there was an expectation to make a decision on inclusion, it should’ve been on [the agenda](https://github.com/ethereum/pm/issues/1197) so that L2s have an opportunity to support it with representation in the call, alongside others (maybe more than just lightclient) who opposed. If the debate became too long, it would’ve further supported the need to move the discussion to [RollCall #9](https://github.com/ethereum/pm/issues/1172).

## Replies

**matt** (2024-12-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philknows/48/8978_2.png) philknows:

> If there was an expectation to make a decision on inclusion, it should’ve been on the agenda  so that L2s have an opportunity to support it with representation in the call

It was on the agenda no?

[![Screenshot 2024-12-05 at 17.43.57](https://ethereum-magicians.org/uploads/default/optimized/2X/2/287af6a0a7ce27af4ece573405331f89c47c25ae_2_690x440.png)Screenshot 2024-12-05 at 17.43.571954×1248 224 KB](https://ethereum-magicians.org/uploads/default/287af6a0a7ce27af4ece573405331f89c47c25ae)

---

**philknows** (2024-12-06):

I would say that we’d need to be clearer on what is meant by “discussion” vs. “decision”. There were also demands on the call about finalizing Pectra that day. Had Arbitrum, Base, etc. known that we were doing that and making decisions that day about *inclusion* specifically, would they have shown up?

---

**timbeiko** (2024-12-09):

Thank you for the thoughtful post, [@philknows](/u/philknows)!

I agree with your overall assessment that we need to be better at coordinating “external stakeholders” within the ACD process, and what the overall goals should be. Once we have a clear outline for the process, we should add it to `ethereum/pm`. The repo is very much due for an overhaul which I’ve failed at prioritizing.

A few thoughts on your specific questions:

> Where should contributors coordinate their support?

IMO it’s ~impossible to mandate that a distributed community like ours would coordinate on a single place to voice support. That said, I think we can put the onus on an EIP champion to aggregate all of it in a single place.

Previously, I tried doing this on EthMagicians by using `$fork-candidate` tags ([shanghai](https://ethereum-magicians.org/tag/shanghai-candidate), [cancun](https://ethereum-magicians.org/tag/cancun-candidate)).

While some good came out of it, such as the [EIP-1153 proposal thread](https://ethereum-magicians.org/t/shanghai-cancun-candidate-eip-1153-transient-storage/10784), it wasn’t used consistently enough for EthMag to be the canonical place to track *all* proposals.

I had to maintain a separate list, which lived outside the hard fork meta EIP, resulting in three places where this information lived. As a minor improvement to this, I proposed adding [PFI to Meta EIPs](https://github.com/ethereum/EIPs/pull/8662). For future forks, I think it’s reasonable to ask EIP champions to open a PR against the HF Meta to propose their EIP be PFI’d.

To simplify things, my proposal here would be that when someone PFI’s an EIP, they add a link in their PR to an EthMagicians thread that tracks support, adoption, etc. for the EIP **in the first post**. By default, this should be the `discussion-to` thread, but in cases where the champion does not have access to the original thread (because they weren’t the main author), it could be a new one, like in the case of 1153.

Assuming people are on board with this, we could update [EIP-7723](https://eips.ethereum.org/EIPS/eip-7723) to describe this process, and/or link that in `ethereum/pm`.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philknows/48/8978_2.png) philknows:

> What should ACD timeshare be used for to maximize signal while minimizing noise?

I disagree with a few of your priorities here, namely:

- Encouraging updates: this can be done in large part async. I think we should only briefly cover “updates” on the call and reserve more of it for discussion that has to happen synchronously.
- Encouraging summaries: again, I’d lean towards async summaries and having the call go into some questions/comments on those.
- Discouraging technical debates or PR/EIPs discussion: I think, when done well, this is actually one of the most valuable functions of ACD. Sometimes, spending an extra 5-10m debating things live on the call can save us a 2 week async iteration cycle. It’s a hard balance to get right, but overall I think we’ve gotten better at moving things to breakout rooms when they digress too much.

That said, one thing we can probably do better to maximize signal is be clear on the agenda what the expectation is for each conversation point (e.g. Introduce vs. Discuss/Debate vs. Decide).

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/philknows/48/8978_2.png) philknows:

> Which meetings should I attend?

Agreed with everything here, and one thing I’d make explicit is that anyone running breakouts or working on an initiative that affects network upgrades or the short term L1 R&D roadmap should attend ACD by default.

---

**philknows** (2024-12-17):

Thanks for the responses Tim. I think it would be good to have some sort of FAQ or something on `ethereum/pm` and other similar “high traffic areas” where it’s clearly visible. This way we can start exercising whatever recommendations we can discover through this process, so we get clearer visions of expectations for ourselves and also for others looking to interact with L1 cohesively.

I want to be clear that I’m not looking to setup a new process and mandating it in any sort of way.

Reference:

[![standards](https://ethereum-magicians.org/uploads/default/original/2X/d/de184e871803beda437a344f7868723955934fd1.png)standards500×283 22.2 KB](https://ethereum-magicians.org/uploads/default/de184e871803beda437a344f7868723955934fd1)

> IMO it’s ~impossible to mandate that a distributed community like ours would coordinate on a single place to voice support. That said, I think we can put the onus on an EIP champion to aggregate all of it in a single place.

I think it’s impossible right now because we don’t really have any expectations of where to go for specific information. Signal and context are spread sparsely across too many platforms, often in places that aren’t easily searchable or persisted. There’s also no clarity in how these various mediums should be used. If we can clearly define what is the purpose of each medium, perhaps we can start exercising it and getting buy-in from community members to do the same. I would love to hear what people think each medium is/should be used for (because I don’t think there’s alignment here):

- EthMagicians
- EthResearch
- Twitter/X/Warpcast
- Telegram
- Eth R&D Discord
- Github: ethereum/consensus-specs PRs
- Github: ethereum/execution-specs PRs
- Github: ethereum/pm PRs
- Github: ethereum/EIPs PRs

> For future forks, I think it’s reasonable to ask EIP champions to open a PR against the HF Meta to propose their EIP be PFI’d.

I think this is reasonable and should be made clear that this is an expectation, alongside collaboration via the discussion thread opened on EthMagicians (we really need to reduce platform risk of Github). Generally, there is at least one or more individuals championing an EIP and they should equally bear the responsibility of keeping their EthMagician discussion thread up to date, organized and answer questions because it’s “the place” I would look at a minimum for all information relating to the EIP. Similarly to how ECMAScript development proposals are discussed at https://es.discourse.group/

> To simplify things, my proposal here would be that when someone PFI’s an EIP, they add a link in their PR to an EthMagicians thread that tracks support, adoption, etc. for the EIP in the first post . By default, this should be the discussion-to thread, but in cases where the champion does not have access to the original thread (because they weren’t the main author), it could be a new one, like in the case of 1153.

I agree with this and it should be made clear to all that the EthMagicians thread is basically the default “wiki” for all things relating to the official proposal. Some formality/centralization is good here for organization.

> That said, one thing we can probably do better to maximize signal is be clear on the agenda what the expectation is for each conversation point (e.g. Introduce vs. Discuss/Debate vs. Decide).

Yes, I think maybe the PM issues can define this better and will help enforce expectations of the call ahead of time so the appropriate stakeholders show up for *decision making*. If we’re looking to freeze Fusaka-devnet-0 by this call and these are the missing decisions we need, it should be be clearly labeled that we need a decision made at this call, so come prepared. We could have some verbs with each topic to signal what the purpose/goal is with a particular topic [Intro/Present/Discuss/Clarify/Debate/Decide/etc.].

> Agreed with everything here, and one thing I’d make explicit is that anyone running breakouts or working on an initiative that affects network upgrades or the short term L1 R&D roadmap should attend ACD by default.

Yes and I think being as organized as possible about what we intend to do on a particular call should help others outside of L1 know when they should show up and support/object for CFI-ing a particular EIP. Otherwise, we default to utilizing data from the EthMagicians discussion thread to help with that.

In summary, if these are “practices” that we’re willing to adopt, I feel this FAQ should be included potentially with EIP-7723 and pinned in places like `ethereum/pm`, EthMagicians, EthResearch, etc. so we can preach defaults for finding, gathering, persisting and citing information to make better decisions.

