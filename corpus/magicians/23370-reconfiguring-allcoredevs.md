---
source: magicians
topic_id: 23370
title: Reconfiguring AllCoreDevs
author: timbeiko
date: "2025-04-03"
category: Magicians > Process Improvement
tags: [core-eips]
url: https://ethereum-magicians.org/t/reconfiguring-allcoredevs/23370
views: 1825
likes: 40
posts_count: 20
---

# Reconfiguring AllCoreDevs

# TL;DR

- I propose reconfiguring AllCoreDevs such that ACDE & ACDC focus on scoping the next hard fork, rather than implementing the current one. In addition to welcoming existing attendees, these calls could more explicitly solicit input from a broader range of community stakeholders.
- To complement this, the existing testing/interop call would formally become “ACDT(esting)”, focused on the current fork’s implementation details, rather than setting its scope, ensuring that resolving technical issues doesn’t compete with high-level feature prioritization.
- With Pectra about to go live, and the Fusaka fork scope scheduled to finalize soon, Glamsterdam presents a good opportunity to test this process. Before then, I propose having a review and feedback period, aiming for a go/no-go decision shortly after Pectra mainnet releases are out.

# Context

Early in Ethereum’s history, AllCoreDevs was the only formal governance venue and had a relatively small number of participants. Over the years, it has grown and seen many offshoots emerge, such as ACDC, breakout rooms, community calls, and more. Since The Merge, we’ve gotten better at working on multiple forks in parallel: Dencun was live on devnets as we shipped Shapella, and Fusaka is in a similar situation as we approach Pectra’s mainnet deployment.

However, we now have a more complex process, involving a growing number of stakeholders, which has to agree on and deliver an ambitious roadmap. This has led to a number of growing pains, including:

- Unclear participation expectations: while ad-hoc coordination was sufficient with fewer calls and people, implicit assumptions about participation are no longer sufficient to ensure we have the right people present when making decisions.
- Lack of coherent direction: exclusively relying on a “bottoms up” approach to derive an implementation plan may result in potential mismatches between what should be the focus(es) for protocol development and what actually gets done.
- Community confusion: outside of AllCoreDevs, a growing number of external stakeholders now have either an interest in the outcomes or a desire to participate. If the process is implicit and illegible, this results in friction and confusion for the broader community.

**This post proposes changes to the AllCoreDevs process that aim to address these issues, while ensuring that the core principles that guide Ethereum governance — rough consensus, openness and a strong security mindset — are preserved.** It is divided in two main sections: Process Design and Implementation Details.

The first outlines high-level desiderata, independent of how they fit into existing structures. The second section explores how this could be implemented in practice, and what some of the open questions are.

# Process Design

## Roadmap Setting

The most important missing piece in the current AllCoreDevs process is a focus on the high level roadmap (“why we do things”), rather than individual proposals (“what we do”). This is true both for when planning the next fork(s), but also when thinking about Ethereum’s longer-term direction.

### Short Term

A short-term roadmapping effort should aim to set the “headline feature” for Ethereum upgrades, making a strong case for its importance, even if no formal EIP exists yet. For example, had such a process existed before Fusaka, it could have framed the upgrade around “increasing the blob count by 2–5x ASAP” and clarified why this was necessary to prevent L2s from turning to alternative DA.

The goal would be to **articulate why a feature is important for Ethereum**, who benefits from it and to what extent, what core properties of Ethereum does it enhance (e.g. scalability, censorship resistance, UX, etc.) and whether it comes with any tradeoffs.

That said, **the security of the network must take precedence over delivering new features**. One of Ethereum’s strongest unique differentiators is resilience. We should not compromise on this, even when there is pressure to ship.

Another core property to **maintain is Ethereum’s open roadmap process**, which invites the community to participate in shaping network upgrades. Getting better alignment on the high-level features for a fork does not mean the community can no longer [Propose EIPs for Inclusion](https://eips.ethereum.org/EIPS/eip-7723#considered-for-inclusion), but that these will be considered with the context of having a higher-level objective for the fork.

This results in the following prioritization:

- P0: Network Security. Addressing security issues takes precedence over everything.
- P1: Roadmap “headline feature(s)”. The feature(s) that teams dedicate the majority of their time and attention to during a network upgrade.
- P2: Other EIPs. Weighted against any potential impact to P1. If unexpected issues arise that delay P1, default to removing them from an upgrade.

### Long Term

In parallel to improving our short-term roadmapping process, we should improve how we coordinate on Ethereum’s longer term roadmap.  To do so, we must agree on what the main tradeoffs are, what solutions are worthwhile to explore, and what specific R&D initiatives are needed to validate or invalidate them. One of the biggest challenges with this work is balancing optionality in a rapidly changing environment with the desire for specific commitments farther in the future.

High quality research is a necessary but insufficient input to this process. To adequately set the long-term trajectory for Ethereum, we need clear venues for discussion and debate to happen, with both technical representation, as well as business, product, and strategy-minded stakeholders.

Ideally, it produces clear records of both the current path forward and its rationale—as well as the decision tree that led us there. This is the standard we hold ourselves to for technical decisions, even those of minor significance, and should be applied to Ethereum’s highest level strategic planning.

While many of the components needed to implement a short-term roadmap process exist today and mostly need “tweaking”, this isn’t true for the long term roadmap. To get there, we can experiment with different approaches and iterate towards a process that is both efficient and legitimate.

## Stakeholder Input

The roadmap process requires high-quality input from all parts of the Ethereum community to reach optimal decisions. While core developers excel at evaluating implementation risks, this perspective alone is insufficient. To complement this, we must also evaluate the benefits to users and how a feature aligns with the longer-term evolution of the Ethereum protocol.

For the broader community, engaging with AllCoreDevs can be daunting, time-consuming and prone to opaque feedback loops. It’s unclear what the right entry points are, where and when to pay attention, and whether the input provided is ultimately considered as part of the decision.

A “translation” problem also exists between application and protocol developers, where users’ needs may not be expressed in a way that reflects protocol development constraints. Application developers can’t be expected to have deep protocol expertise to participate effectively in the process. Ideally, they would express needs in their own terms and the AllCoreDevs process would then take responsibility for proposing technical solutions to meet them. To the extent a subset of application developers then want to engage in developing specific solutions, the process would remain open to them, as it always has.

On the research side, topics can take years to properly explore and some of the most important considerations are orthogonal to implementation complexity. Ethereum’s issuance curve is the most extreme example of this. Additionally, it’s possible that urgent and important problems have been identified, but not a solution, and that Ethereum’s main priority *should* *be* to come up with an implementation plan. This is how The Merge happened.

**The Roadmap process should thus explicitly solicit input from these groups.** Beyond inviting their regular participation in calls, we can create ways to allow them to make formal proposals at a higher level of abstraction than EIPs.

For example, there could be a “template” that various stakeholders can use to communicate their preferences as part of the roadmap process, that presents answers to questions such as:

- What is the change the group would like to propose to Ethereum?

What is the current state of development for the proposal?
- Why is now the right time to make this the main priority for Ethereum?

Why would this change be impactful to them, and the community as a whole?

- What are quantitative and qualitative ways this would improve Ethereum?
- Who else explicitly supports the change and what is their role in the Ethereum community?
- What issues does not having this change currently cause (e.g. bugs, missing user affordances, etc.)?

What are the biggest tradeoffs and open questions about the change?

Another consideration is how to categorize stakeholders. Breakout calls tend to focus on specific topics but are often attended by the same core group core developers.. Conversely, the community is often segmented into “types” of projects (L2s, DeFi, Wallets, LSTs, etc.), while the most important research considerations often span multiple areas.

Timing is another important question. Is it better if all stakeholders are proactively asked about their priorities, or if their opinion about specific proposals is solicited instead? Which stakeholders are best positioned to give input into major short and long term priorities? How does this affect the current role of core developers in the process?

If poorly designed, this process risks DoS’ing AllCoreDevs. As an example, the Fusaka upgrade currently has over 20 EIPs [Proposed for Inclusion](https://eips.ethereum.org/EIPS/eip-7607#proposed-for-inclusion), with almost as much already Considered or Scheduled for Inclusion.

Again, given the high uncertainty in all of this, experimenting with different approaches is key to converging on a process that allows stakeholders to feel heard, does not compromise any of Ethereum’s core properties, and runs efficiently.

## Network Upgrade Timelines

Here is a tentative timeline of events leading up to a network upgrade using these new processes. To ensure that R&D uncertainties are taken into account, each step is dependent on the previous step, rather than a fixed timeline.

[![acd-color](https://ethereum-magicians.org/uploads/default/optimized/2X/b/ba965812fe7cc2fd7a4488dd5b3256dda869cffb_2_690x164.png)acd-color1761×421 72.5 KB](https://ethereum-magicians.org/uploads/default/ba965812fe7cc2fd7a4488dd5b3256dda869cffb)

Description, starting from when the “headliner” feature is confirmed (![:star:](https://ethereum-magicians.org/images/emoji/twitter/star.png?v=15) on diagram):

1. Fork N “headliner” is agreed upon

The roadmap process for Fork N agrees on the main feature for the upgrade.

This should happen several months before the previous fork, Fork N-1, is ready for deployment.

Other proposals for **Fork N** start to be reviewed.
All teams start allocating resources to the implementation of the **Fork N** headline feature.

**Fork N-1 Client Testnet Releases & Testnet Deployment**
**Deadline for Fork N EIP proposals**

- Most proposals are expected to have been shared and reviewed already.

**Fork N-1  Client Mainnet Releases & Mainnet Deployment**
**Fork N Scope Finalization**

- Any additions to the Fork N scope are agreed to within a few weeks of Fork N-1  going live on mainnet. Beyond this point, only changes to SFI’d EIPs may be considered, as well as security-critical EIPs.

**Fork N+1 roadmap discussions begin**

- Once the scope for the next upgrade has been finalized, high-level discussions about the priority for the upgrade after that one should begin.
- Fork N implementation happens in parallel with this.

**Fork N+1 “headliner” is agreed upon**

- … and the cycle restarts!

# Implementation Details

What follows is a proposal for adapting existing processes to the structure described above. A core assumption is that iterating from what exists today towards a new process is more likely to be successful than discarding everything in favor of a new approach.

## AllCoreDevs Calls

AllCoreDevs is the highest-profile venue in Ethereum governance. It serves both the purposes of agreeing on upgrades’ scope and working through their implementation. By trying to do both things, it ends up not doing as well as it could on either. Since The Merge, we’ve also been running a weekly testing/interop call for clients, focused more on implementation details for forks.

**We can lean into this distinction and make AllCoreDevs the planning venue for the next fork and the existing testing call the venue to discuss implementation details for the current fork.** Here are ideas for how we could reframe the calls to achieve this.

### ACD{E|C}

- The main output of ACD{E|C} calls becomes be the Meta EIP for a network upgrade

Today’s Meta EIPs primarily serve as pointers to individual EIPs, with little substantive content. In contrast, a roadmap-oriented ACD could produce Meta EIPs that thoroughly articulate the priority for a network upgrade and clearly explain the rationale behind this prioritization.

The Meta EIP would likely be refined in distinct stages, e.g.:

Proposals for the high-level focus of the upgrade
- Agreement on the high-level focus of the upgrade
- Specific “headliner EIP” selected for the upgrade
- Open proposals for other EIPs to be included in the upgrade
- Final scope of the upgrade frozen

TBD on how much room this allows for CFI’d, but not SFI’d, EIPs.

The rationale for prioritizing something in a network upgrade should not exclusively depend on if an EIP already exists or not. In other words, “technical readiness” is one of the inputs into the decision, but not the only (or main) one.
The stages above must take into account the current implementation status of the current fork. For example, while the priority for the next upgrade can be set in parallel with the implementation of the previous fork, the open call for EIPs should happen at a time when client developers actually have bandwidth to review proposals.

**ACD{E|C} must maintain open participation while expanding beyond protocol contributors and raising the quality bar for roadmap discussions.**

- EIPs are neither necessary nor sufficient for this. We need a new “template” by which to evaluate potential changes, that is both flexible enough to accommodate different types of features, but also structured in a way that filters out low-quality proposals. It may be good enough to ask people for “a writeup or presentation” and leave this open-ended. Unlike EIPs, which focus on the “what”, this resource should focus on the “why”.
- Representatives from different parts of the community should be invited to participate and engage. The scope for Ethereum network upgrades should be set around what provides the most value to the entire community, and not exclusively what client teams would prefer to work on. At the end of the day, client teams are the ones that must come to a consensus about which code to write, but bringing in more sources of input from the community can help inform these decisions.
- Asynchronous input sources are critical to high quality, open debates. Call time is limited, and live debates are often inefficient at surfacing areas of highest alignment or contention. We need canonical async forums to collect input, rather than rely exclusively on synchronous calls as a source of information. This doesn’t mean moving the ultimate decisions outside the calls, but can help ensure that participants come in with high context and an understanding of the key tradeoffs to work through.

**ACD{E|C} continues to exist with a bias towards the EL/CL, but participation should be expected weekly by at least one roadmap-aware representative from each client team.**

- Aim to resolve any time-sentitive topic on either call, but non-urgent items can default to the EL or CL call based on their domain

This implies that all client teams send O(1) representatives who are knowledgeable about the roadmap process to attend both ACD{E+C}, but may have O(N) representatives attend their layers’ call.

Outside stakeholders who only care about one layer should mostly be expected to attend that call, with some exceptions in the final stages of roadmap planning.

**ACD{E|C} remains where decisions about EIP inclusions (and exclusions) are made for network upgrades**

- Even though the current fork’s implementation is no longer part of the ACD{E|C} scope, if changes must be made to the EIP set once implementation has started, this decision should be finalized on ACD{E|C}. Changes to included EIPs would not have to go through this process, unless they are so significant that they change the nature of the EIP, or impact the ability to deliver the "headliner EIP” in any way.

### ACDT(esting)

- The existing weekly testing/interop gets renamed to “AllCoreDevs Testing” and becomes the main venue to discuss the current fork implementation.

Loosely, ACDT would take a network upgrade Meta EIP as “input” and “output” production-ready client implementations.

**All implementers would be expected to attend ACDT — every client team should have O(N) attendees weekly.**

- Client teams can send different representatives to ACDT than ACD{E|C} calls, but we should have sufficient technical representation to resolve nearly all implementation issues that emerge during a fork cycle.

**When upgrades are in their peak implementation period, or if security related or urgent issues arise, ACDT “overflows” into ACD{E|C}.**

- Shipping the current fork is a prerequisite to ship the next one. Opt for pragmatism in achieving this over “perfect” conceptual delineation between calls

### Timeline View

Re-using the timeline shared above, topics in the white boxes fall under ACD{E|C}; those in colored boxes shift to ACDT.

[![acd-ref-2](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e83eda216a31ddd1947a81c9c0401d90af719eb7_2_690x164.png)acd-ref-21761×421 86.5 KB](https://ethereum-magicians.org/uploads/default/e83eda216a31ddd1947a81c9c0401d90af719eb7)

Description, starting from when the “headliner” feature is confirmed (![:star:](https://ethereum-magicians.org/images/emoji/twitter/star.png?v=15) on diagram):

- As ACDT works on the implementation for Fork N-1, ACD{E|C} debate and confirm the headliner for Fork N

Open question: should the implementation of headliner features still be tracked in ACD{E|C} until  Fork N-1 ships?

**By the time  Fork N-1 ships, ACD{E|C} has finalized the scope for  Fork N,  which moves to ACDT**
**As the scope for Fork N finalizes, discussions about potential headliners for Fork N+1 begin in ACD{E|C}**

### Other Misc. ACD Improvements

- Freeze agenda ~3 days early: for ACD{E|C}, anything non-urgent is added to the agenda at the latest on the Monday before the (Thursday) call.
- Template for EIP PFI proposal: “headliner EIPs” are expected to go through a rigorous vetting process under this new structure. Additional EIPs should also have a strong rationale for inclusion, even if the process is lighter-weight. Ideally, this means PFI’d EIPs do not need to be presented on ACD{E|C} by default.
- DFI, no reason needed: the open EIP process can turn into a DoS on client teams’ attention. To balance this, client teams should use the Declined for Inclusion status liberally. There must not be an expectation that a reason will be provided for rejection. On the other hand, DFI only applies to a specific fork. EIP Champions can re-propose DFI’d EIPs for a future upgrade.
- Better metrics for “protocol resilience”: our desire to increase our shipping capacity must not come at the expense of Ethereum’s long-term sustainability. We should have clear metrics around performance and security that help us balance the urgency of delivering new features with the importance of building resilient software.

## Stakeholder Input

The above refocus of AllCoreDevs will be most successful if we have the right set of stakeholders engaging in the process. In practice, this is a mix of client developers with sufficient context to form opinions on the broader Ethereum roadmap, protocol researchers, domain experts from many parts of the community (e.g. L2s, wallets, DeFi, etc.) and more. This latter group is least likely to participate in regular calls, so we should have other means of collecting their inputs, both proactively (e.g. tracking the most common issues experienced onchain) and reactively (clear forums for them to share their issues or suggestions, that then feed into the ACD process).

### Breakout Rooms

While very similar in style to AllCoreDevs, breakouts have been useful to engage with more stakeholders about specific issues that require input beyond client developers. This is especially true when going from an initial design to practical implementations, such as for [EIP-7702](https://github.com/ethereum/pm/issues?q=is%3Aissue%20breakout%20aa) or [FOCIL](https://github.com/ethereum/pm/issues/1408).

### Recurring Protocol Calls

These already happen: recurring protocol calls are a good way to communicate with domain experts adjacent to AllCoreDevs about topics relevant to them, and to bring their input back into ACD. For example, [RollCall](https://ethereum-magicians.org/search?q=rollcall) has been useful to get input from L2s. We now also have [Beam Chain calls](https://github.com/ethereum/pm/issues?q=is%3Aissue%20beam), and a newly launched [Protocol Research Call](https://ethereum-magicians.org/t/protocol-research-call/23261), who can hopefully serve similar functions.

### Community Calls

We’ve sometimes hosted Community Calls intended for a broader audience than protocol contributors (e.g. [Shapella](https://github.com/ethereum/pm/issues/741), [Merge](https://github.com/ethereum/pm/issues/599)). These have historically been held at the end of the network upgrade process, with an aim to disseminate information (rather than collect input). Hosting such calls early in the upgrade process (or making this part of the ACD{E|C} calls) could be another way to collect input from community members about the priorities for an upgrade.

### Application Focused Venues

As mentioned earlier, the AllCoreDevs process has been shaped according to the inputs client devs care about. This can sometimes lead to concerns that don’t neatly fall into these categories being ignored. One potential way to improve this is by creating an open venue for application developers to share their perspectives and protocol-level requests. This could take the form of a call, or more asynchronous venue (see below), but framing it as an “open invitation for applications developers” may help surface needs that are otherwise missed in ACD.

### Async Discussion Threads

We’ve had a few experiments trying to collect input on fork priorities using EthMagicians ([Prague](https://ethereum-magicians.org/t/pectra-network-upgrade-meta-thread/16809), [Dencun](https://ethereum-magicians.org/t/cancun-network-upgrade-meta-thread/12060), [Shanghai](https://ethereum-magicians.org/t/shanghai-core-eip-consideration/10777)). Similarly, client teams have recently started sharing their views about priorities for network upgrades. While both of these have helped narrow down the list of possible EIPs, they can sometimes miss the forest for the trees.

Whether on Ethereum Magicians or elsewhere, we should create a space for asynchronous discussions about the high-level goal of the next upgrade, centered on the “why” rather than the “how”. This would be the place we send community projects to articulate their needs and problems, with it becoming input for the discussions about the next upgrade.

## Documenting the Process

A final consideration to think through is where and how to present the information about this new process. Today, this is spread across the pm repository, EIPs, Ethereum Magicians, and a lot of context only exists in people’s heads. To make things more legible, once we have consensus on an overall path forward, we should explicitly document it. Where and how we do so will depend on the specifics of our decisions, but the [pm repo](https://github.com/ethereum/pm/tree/master/processes) feels like a natural default “landing page”.

# Next Steps

To move this proposal forward, I would suggest having an explicit deadline for a “review and comment” period to gather feedback and make changes to this proposal (~2 weeks?). Once async input has been collected, we should aim to make a go/no-go decision on the next ACD. We don’t need to iron out every detail before moving forward, but we should aim for broad alignment on the new structure before we start experimenting with it.

Thank you for reading all the way here ![:grinning_face_with_smiling_eyes:](https://ethereum-magicians.org/images/emoji/twitter/grinning_face_with_smiling_eyes.png?v=15)!

## Replies

**Bastin** (2025-04-03):

I like this and I think it makes a lot of sense.

some comments:

- I think that ACDT should be an abstraction over multiple feature-specific break out room calls.
- Apart from client teams, we should have strong presence from the testing teams and EthPandaOps in both ACDT and breakout rooms.

regarding the open question: I think not. Anyone interested can read that from the ACDT summary. Unless it affects the timeline somehow.

---

**abcoathup** (2025-04-04):

![:heart:](https://ethereum-magicians.org/images/emoji/twitter/heart.png?v=15) all of this.  ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=15) ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=15) ![:clap:](https://ethereum-magicians.org/images/emoji/twitter/clap.png?v=15)

- Short & long term roadmaps
- Stakeholder input
- Headline feature & P1.
- ACD(E/C) focused on roadmap & decisions
- ACDT on current upgrade implementation

## Short term roadmap

PFId EIPs should not be presented at ACD(E/C), there just isn’t time.  Instead champions are encouraged to share a short slide deck & 5 minute video async and add this to the discussions topic of their EIP on Eth Magicians.

The considered for inclusion (CFI) bar for **P2 EIPs** should be very high and strong community support should be required.  EIPs should generally only be CFId if they significantly move the roadmap forward. Exceptions to this should be rare.

Using this framework for [Fusaka](https://ethereum-magicians.org/t/eip-7607-fusaka-meta-eip/18439) (planned for late Q3, with PeerDAS & EOF already SFId) suggests the following:

- Headline feature: L2 scaling
- P1: EIP-7594 PeerDAS & CFId EIP-7892: Blob Parameter Only Hardforks
- P2: EIP-7692  EOF (whilst already SFId, P2 as Fusaka will ship with just PeerDAS if EOF not ready)

## Stakeholder Input

Base’s input is a great example of stakeholder input for upgrade headline feature(s)/P1:


      ![](https://storage.googleapis.com/papyrus_images/6a417c9a16819ad9d65b36381b293a19.jpg)

      [Base Engineering Blog](https://blog.base.dev/achieving-more-blob-space-in-2025)



    ![](https://paragraph.com/api/og?title=blob%2Facc%3A+Achieving+more+blob+space+in+2025&blogName=Base+Engineering+Blog&coverPhotoUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2Fbc3d2566f8cf9cf1c7371c471364623c.jpg&blogImageUrl=https%3A%2F%2Fstorage.googleapis.com%2Fpapyrus_images%2F6a417c9a16819ad9d65b36381b293a19.jpg&publishedDate=1740679202277)

###



To support a global onchain economy and ensure Ethereum's success, Base believes it's crucial to ship the Fusaka hard fork Q3 of 2025, here's the plan..










Eth Magicians could be the home for what I am calling ECIPs (Ethereum Community Improvement Proposals).  The template should be really light weight, answering your what/why/who questions.

## ACDT

Elevating [interop/client testing call](https://ethereum-magicians.org/search?q=testing%20call%20in%3Atitle) to an ACD protocol call means it should be **explicitly public**, with a **live stream**, **recording**, **transcript** & **chat log** publicly available.  Whilst the expectation is that only implementers (client teams), testers and devs using features being implemented attending/presenting and the wider community viewing the live stream/recording and reading the summary, transcript & chat log.

Previously interop/client testing call was semi-private so that client teams could discuss any sensitive security issues.

Anyone awake at EF Eth o’clock could attend, but there is no live stream, no recordings, no transcript & no chat log.

The public output was notes on Eth Magicians. (![:pray:](https://ethereum-magicians.org/images/emoji/twitter/pray.png?v=15) [@parithosh](/u/parithosh) plus PandaDevOps & more recently [@poojaranjan](/u/poojaranjan))

With the rise of ACDT, there may be a need for a ACDS, which doesn’t have a public invite, but notes are made publicly available on Eth Magicians.

---

**kdenhartog** (2025-04-04):

Overall I think the direction this takes us is moving in the right direction and it’s the right time to move forward with improving the governance process. This proposal I think largely reflects an effective way for the community to continue improving and building. The one suggestion I’d like to make is to  Async consensus gathering the default rather than calls.

The primary reason for this is because calls don’t tend to scale well due to time zones and conflicts of when people can participate leading to more calls and less coordination overall which I believe is what’s already been experienced today. By instead moving to async consensus we then have a more accessible and scalable approach for people to get ideas and it should end up reducing the number of calls most people need to be on. Essentially just trying to apply the “this call could have been an email” meme to our consensus process.

What I think would still be needed to figure out between the short term and long term plan is how we transition from calls being the primary form of consensus gathering to an async format being the primary format and what that async format looks like. Today it’s meant to largely be ETH magicians and a small amount of GitHub for async discussions, but it seems like discord, TG channels, and Twitter are filling the void for whatever we’re missing from the intended two. I’m not sure what’s right on this so I’ll punt on it for now too.

From there I’d imagine we’d reduce down to fewer calls with their focus more on fork timelines, status updates and merging changes that reflect consensus achieved elsewhere to the Meta EIP. We’d be able to scale this approach further so that people all across can opt into the discussions they need to be apart of only.

The other question I’ll throw out too. How do you see the governance process being managed and evolved between the short term and long term? Historically I think this has been something that’s slowed things down because we haven’t had a method to resolve governance issues easily and instead we’re stuck until basically all EIP editors agreed.

All in all, I think this is a good improvement. The details will matter here to some, but they’re small issues that can be resolved along the way. The overall vision points us in a good direction and I’m looking forward to seeing the improvements that come from this long term.

---

**poojaranjan** (2025-04-10):

Thanks for the detailed post, Tim. I think this is a decent roadmap that can help reduce some of the chaos around network upgrade preparation.

That said, I’d like to suggest a couple of additions from a process and EIP tracking perspective:

- It could be useful to add an optional  preamble header - “Stage” in the EIP template. This would allow for easier tracking and filtering of an EIP’s current stage without needing to dig into each upgrade’s Meta EIP.
- Additionally, I’d recommend creating a Meta/Info EIP to document the proposed process itself, rather than relying solely on the ethereum/pm repo.  Documenting it in an EIP might improve clarity and accessibility.

Appreciate all the work going into this!

---

**SamWilsn** (2025-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> It could be useful to add an optional preamble header - “Stage” in the EIP template. This would allow for easier tracking and filtering of an EIP’s current stage without needing to dig into each upgrade’s Meta EIP.

There is a permissions/responsibility issue with adding a header field to track inclusion status. If authors can set the field freely, they can pick “Scheduled for Inclusion” even if that isn’t the consensus of ACD. On the other hand, if editors have to approve changes to the header, that puts us in the position of having to determine the sentiment of core developers (which I’d like to avoid).

Hardfork meta proposals do not have this problem. Anyone can create a hardfork meta proposal, including/declining whatever proposals they like, and core developers can follow/ignore whatever hardfork meta proposals they like.

We could do some UI work to place links from {PF,CF,SF,DF,}I proposals back to their Meta EIPs. Would that be satisfactory?

---

**jflo** (2025-04-16):

Love the idea of having 1 meeting for combined engineering, and 2 meetings for research and strategy, one each EL and CL. Definitely an experiment worth trying, however refactoring a meeting is one of the smallest things actually going on in this proposal. The other aspects to this warrant isolation to be addressed more specifically.

- Separate out the project management aspects. There will inevitably be overlap between engineering and research, and I think the specified Network Upgrade Timelines are sufficient to address that. This is an aspect of our process that we continue to struggle with working on asynchronously, and it remains unclear to me why that is. Is there something about out project management that is necessarily synchronous?
- Separate out the market analysis. This is the big one, and there is an opportunity for EF to fill this gap: Who is in charge of understanding our users? How do they take a data driven approach to that? The decision makers (core devs) are still operating on vibes to know what people want. “People” is defined subjectively and ambiguously. “Ethereum Users” could mean end users, app developers, other node operators, L2s, rpc providers, etc. Each of these market segments is totally opaque and we have no data on each specifically, nor how they interact to form the whole of the Ethereum Community. The Stakeholder Input section hints at this need, but I think we need to be more radical in how this is address - current suggestions are to communicate more, which is good. But communication is overhead, and it takes a lot of labor to turn it into actionable data.

tl;dr - there is a vibes chokepoint around our SDLC input funnel. hire some marketers. good ones, not just people who specialize in shilling. actual marketers that do focus groups, build zk protected feedback techniques, and have the statistical background to analyze this data. We need meta-techniques other than conference calls.

---

**poojaranjan** (2025-04-16):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> We could do some UI work to place links from {PF,CF,SF,DF,}I proposals back to their Meta EIPs. Would that be satisfactory?

I’d love to access the history of the **Network Inclusion Stage** as proposed [here](https://hackmd.io/@poojaranjan/EIPTemplateImprovementProposal). If that can be achieved through the UI without needing to update the preamble header in the EIP template  itself, I’m good with it!

---

**greg** (2025-04-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> acd-ref-21761×421 86.5 KB

I’m a fan of this, some clear wins:

- The P0 & P1 EIPs are prioritized
- Upon P0 & P1 finalization we move onto n+1

It’s a clear feedback loop with strong ownership structures!

One point I want to argue for is more finalized testing criteria before inclusion. I think more recent revelations on EOF highlight this, no one has really done full-blown toolchain testing. Similarly how we need fully written specifications before advancing to an inclusion discussion phase I think we need authors (or supporters) to finish POC implementations & testing to move. To be more explicit:

1. Draft EIP
2. Seek approval that it might make sense
3. Create POC & testing criteria
4. Bring back to ACD for acceptance criteria
5. Asses if it can be included in n+1

---

**gcolvin** (2025-04-29):

> DFI, no reason needed: the open EIP process can turn into a DoS on client teams’ attention. To balance this, client teams should use the Declined for Inclusion status liberally. There must not be an expectation that a reason will be provided for rejection. On the other hand, DFI only applies to a specific fork. EIP Champions can re-propose DFI’d EIPs for a future upgrade.

I may not be clear on the full process, but our upgrade process is slow enough that DFI with no reason becomes just another way to DoS proposals.

---

**CelticWarrior** (2025-05-01):

I’m surprised that there was no mention of stakers as being relevant stakeholders in your post.  For sure as a group they should be relevant.

---

**philknows** (2025-05-01):

I’m going to post my ACD observations here in the recent days post-DFI of EOF and may even serve as a good test to prove my point (because many people may not even see this post unless directed to it from some other “more used” medium).

*Disclaimer: I’m not here to cherrypick on anyone or their thoughts as representative of their or their team’s view. I’m also not citing specific quotes here because I think this is what most people are thinking. I’m just pointing out observations to clarify why people might agree with my points below.*

I still strongly think that asymmetrical information and no clear schelling point for gaining more accurate rough consensus (pardon the oxymoron) is one of our biggest problems in the process. Reading the AllCoreDevs discord chat on opinions about what the consensus actually was for EOF is showing us some important points:

1. Where the information is persisted matters: There is not one, but multiple places where important context (e.g. voicing support and dissent) does not get persisted or replicated. Whether it’s between Discord, EthMagicians, Twitter/X, etc. it’s hard to compile all information (e.g. sentiment, opinions, etc.) easily into conversations where hard decisions need to be made based on consensus. Information/context often gets lost and only recalled when prompted or for appealing decisions.

Q: Should we softly enforce some information/communication centralization here for better consensus?

1. When and how people participate in the ACD process matters more than it should:

- If you didn’t participate in the ACDX call where a decision was being made, your thoughts didn’t matter for the decision (whether accidental or purposeful) unless you showed up at that specific call to voice (see next point) it. Example: People in the ACD discord channel have been overanalyzing EOF sentiment based on one ACDT call only.
- Voicing your opinion seems to be worth more than texting your opinion
- Dapp developers feel like their opinions are worth less than Core developers

Q: Is there a way we can gauge sentiment of decisions being made pre-ACD call and take that into account with the people who show up on the calls? Or at least have a common place like the EthMagicians thread for the (Meta) EIP where it’s summarized when we need to incorporate it for decision calls?

P.S. Wasn’t there an effort to AI summarize threads here?

---

**gcolvin** (2025-05-04):

What is I think is getting lost here is that in the end the consensus of the client teams is decisive.  They are the ones who actually change the protocol, and there is nobody who can order them to do things. So by the time we meet for final decisions stakeholder objections should already have been considered, and only the client teams need to reach consensus.  For that reason such decisions should be made on scheduled, broadcast, and moderated ACD calls.

There will always be objections to any changes to the protocol, and the best the developers can do is to give due consideration to those objections.  And indeed we need to do a better job of listening.  But however well we listen, it is by now an empirical fact that many objections will not arise until EIPs are ready for inclusion.  So even without changing things much I think a lot of the troubles we have seen could be avoided by calling out far, wide and loud that: “This *is going in* unless there are convincing objections, and soon!”  And then give a reasonable amount of time to deal with those objections before a final decision is made on a proper ACD call.

---

**kdenhartog** (2025-05-13):

[@gcolvin](/u/gcolvin) I think you’re highlighting a key governance choice we should probably be explicit about: The client teams get final say on decisions.

Do we want this to be by majority, super majority or unanimous decision? I think super majority or unanimous likely works best for this given if clients diverge we’ve got problems.

Also, for objections I think it’s important to call out for ACD specifically (ERCs should be different, but that’s out of scope of this discussion) how anyone can provide a non-binding objection.

As [@philknows](/u/philknows) points out too, we should probably centralize where that exists and likely allow for this to happen outside calls given people may not be able to attend or there’s too many opinions to hold calls specifically for this. I personally am a fan of using GitHub PR processes for this as it leverages a clear signal of approve/object (request changes)/abstain (comments only) however I don’t think most people in this community are in favor of this.

So I’d suggest the following:

When a PR on GitHub to RFI to the meta EIP is opened it should include a thread specifically for determining inclusion. This should have a poll at the top to get a rough signal for client teams (it’s non-binding they get final say) and comments on the thread should make clear comments/objections and who they’re associated with such as “I’m a wallet developer for Brave and this LGTM”.

This way we have clear communication channels of how people can voice their intent/concerns, but we also have a driving function towards consensus via client teams. We should also document these rules as how the process works. That way if anyone has a problem we can point at it and say there’s the rules as well as if they wish to push for changes to said rules they have to come with specific updates and again client teams ultimately decide.

---

**gcolvin** (2025-05-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> @gcolvin I think you’re highlighting a key governance choice we should probably be explicit about: The client teams get final say on decisions.
>
>
> Do we want this to be by majority, super majority or unanimous decision? I think super majority or unanimous likely works best for this given if clients diverge we’ve got problems.

“Rough consensus and running code.”  Unless the Core Devs can reach consensus on a more formal voting process rough consensus is what we have.  Unanimous is best, but not required.  And the more contentious the decision the more difficult the decision – there i no getting around that.

---

**kdenhartog** (2025-05-13):

Sure, I understand that from a governance perspective is correct. However the ETH protocol itself also acts as a forcing function here. By definition the consensus client teams have to implement the protocol the same or the nodes wouldn’t interoperate and come to consensus.

For example if one team decides to have finality reached after 1 block and another decides to wait until 5 blocks are published then as a collection the client teams need to come to unanimous agreement on a decision to maintain the protocol. Otherwise they’re producing 2 separate “consensus” protocols.

So by definition wouldn’t the nodes need unilateral consensus to maintain interoperability and integrity of the ETH protocol?

---

**gcolvin** (2025-05-13):

Yes.  Thus the distinction between “disagreeing with the consensus” and “blocking consensus.”  The ultimate failure of governance is for a blocking team to fork instead.

---

**philknows** (2025-05-14):

> As @philknows points out too, we should probably centralize where that exists and likely allow for this to happen outside calls given people may not be able to attend or there’s too many opinions to hold calls specifically for this. I personally am a fan of using GitHub PR processes for this as it leverages a clear signal of approve/object (request changes)/abstain (comments only) however I don’t think most people in this community are in favor of this.

This is very similar to our informal, non-documented process of how we maintain the consensus-specs and beacon-API repositories. This is great specifically for the core devs who can comment directly on spec changes line by line. Assuming we’re all still ok with further entrenching ourselves in centralized Github/Microsoft mediums…

Where we lack is trying to enforce some sort of canonical space for “official” sentiment that is easily seen, read and participated by everyone outside of core devs also. Even a simple link to a hackmd or company blog post page relating to the deeper reasoning/context would be helpful if we decide Github is the best place for posting sentiment. Or is it EthMagicians? I don’t think we have that answer here and that’s the problem. Each medium has its tradeoffs… we just need a way to index/centralize all the bits of useful information for rough consensus spread across different platforms.

Based on what I’ve been seeing with the ethereum/pm repo and the new bots, I’m assuming we want to keep larger context in something like EthMagicians? Everything there now has some sort of discussion thread tied into it.

---

**kdenhartog** (2025-05-23):

I suspect the answer is going to be pick something and live with it until we hit legitimate problems and at that point as a community determine how we want to migrate. For example, IETF still uses mailing lists primarily. W3C on the other hand has moved from mailing lists to more of an adhoc system where the WG chairs can decide specifics (usually it’s down all through GH issues/docs), but they provide infrastructure on W3C site and github organization management. They moved because the community saw value in doing so. In which case, I don’t think we need to make it perfect, just good enough for now and make sure we have some way to iterate on the governance process as we encounter new problems.

---

**kaksv** (2025-07-10):

This is really explicit

