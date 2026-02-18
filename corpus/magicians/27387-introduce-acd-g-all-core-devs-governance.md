---
source: magicians
topic_id: 27387
title: Introduce ACD-G (All Core Devs – Governance)
author: poojaranjan
date: "2026-01-04"
category: EIPs > EIPs core
tags: [governance]
url: https://ethereum-magicians.org/t/introduce-acd-g-all-core-devs-governance/27387
views: 250
likes: 11
posts_count: 20
---

# Introduce ACD-G (All Core Devs – Governance)

This is a proposal to give the community one clear venue to follow governance discussions. As of today, Ethereum All Core Dev or ACD holds a unique position as a well-known public forum where **Ethereum protocol related discussions** take place.

- ACDE: ACD Execution Layer
- ACDC: ACD Consensus Layer
- ACDT: ACD Testing

All Core Devs Governance a.k.a ACD-G intends to provide the canonical place to discuss *how decisions are made*, before those decisions reach ACD for execution.

## Why add a new public meeting ?

This is not the creation of a new public meeting, but rather a **renaming and rebranding of the existing EIPIP meetings** to add value and encourage broader participation.

For many years, **EIPIP meetings** have served as the primary venue for **EIP and network upgrade process improvements and governance discussions**. All EIP editors and interested participants meets once a month to review current processes, gather community input, and suggest changes.

Recently, the EF Protocol Support team introduced new coordination and upgrade processes. While these changes are valuable, they have led to several confusions among different stakeholders. Moreover it lead to

- Multiple governance meetings creating duplication and uncertainty
- EIP Editors not involved in designing or onboarding into the new process
- Unclear expectations leading to PR backlog, review delays, and EIP selection confusion
- ACD meetings overloaded with process and governance topics

By moving process discussions out of ACD, coordination improves across EIP editors, EIP authors, EF teams, and client teams, while creating a shared, reliable record of decisions over time. This also saves time in ACD meetings, allowing them

- to focus on protocol specifications,
- client readiness, and
- clear go / no-go / conditional signals from client teams.

## Division of Responsibilities

- ACD-G (Governance & Process)

Define and refine Upgrade EIP selection and governance processes
- Align on upgrade coordination frameworks
- Resolve governance questions ahead of ACD
- Publicly document decisions

**ACD (Protocol & Enforcement)**

- Receive clear governance outcomes from ACD-G
- Enforce agreed decisions in upgrade timelines
- Focus on protocol specifications
- Request explicit client readiness signals
- Preserves ACD time for technical work.

This ensures governance questions are resolved early and technical meetings remain technical.

## Who will Participate?

ACD-G is an open and inclusive. It should explicitly invite:

- EIP Editors
- EF Protocol Coordinators / Protocol Support team
- Interested client team representatives
- Researchers and contributors focused on governance or process
- Community members interested in process improvement

This meeting can be organized **once a month**, with the frequency increased if needed. Anyone interested in *how Ethereum decides what ships* is welcome to participate.

In short,

> ACD-G aligns on governance and process while ACD enforces and executes.

**PS:** The rebranding of **EIPIP** as **ACD-G** was discussed in the [EIPIP meeting](https://ethereum-magicians.org/t/eipip-meeting-122-dec-17-2025/25913/2), and as an action item, this proposal is being shared to gather community sentiment and assess interest from EF protocol teams and client teams in having a central forum outside ACD-E and ACD-C for governance discussions.

## Replies

**abcoathup** (2026-01-05):

I am **strongly opposed** to EIPIP meetings being rebranded as ACDG.

ACDG to me implies a much wider remit than EIPIP has had and should be driven by All Core Devs (either ACD(E/C/T) moderators or EF Protocol Support).  See: [AllCoreDevs, Network Upgrade & EthMagicians Process Improvements](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157)

---

### EIP process

The EIP process should work for all core devs, not the other way around.

It should be quick and easy for EIP authors to get EIPs to draft level and Proposed for Inclusion in a Network Upgrade Meta EIP.  It should be easy to review, give feedback and prioritize which EIPs should be Considered for Inclusion.

The EIP process should be completely split from the ERC process, with separate meetings & editors.  So that the needs of protocol and application layers can be met via quick iteration and allowed to diverge as needed.

Forkcast ([@wolovim](/u/wolovim)) adding an [EIP directory](https://forkcast.org/eips/) rather than via https://eips.ethereum.org suggests that for whatever reason we aren’t able to iterate easily/fast enough via the current system.  Other examples of fast iteration for All Core Devs: [Protocol Calls - Forkcast](https://forkcast.org/calls/), [Glamsterdam Upgrade - Forkcast](https://forkcast.org/upgrade/glamsterdam), [ACD Planning Sandbox - Forkcast](https://forkcast.org/schedule/))

It feels like we are missing someone who’s entire focus is on making the EIP process smooth.  A dedicated (and funded) **EIP coordinator** or someone in the EF Protocol Support team who’s main role is the EIP process. (cc [@nixo](/u/nixo))

### ACDG

I am open to an ACDG in some format, assuming it is driven by All Core Devs (either ACD(E/C/T) moderators or EF Protocol Support).  Ideally would have some async elements (for those asleep at Eth o’clock).

Some of the current challenges I see (some were covered in [2025 upgrade process retrospective - #2 by abcoathup](https://ethereum-magicians.org/t/2025-upgrade-process-retrospective/27082/2)):

- Maintaining a 6 monthly upgrade cadence
- Large number of EIPs being Proposed for Inclusion (difficult to review the volume & give feedback) (51 for Glamsterdam)

How to signal early which EIPs are likely/unlikely (so unlikely EIPs don’t even get proposed for a particular upgrade) (perhaps via Fork Focus & one off working groups/office hours)
- How to signal which EIPs are worth prototyping (and when) (perhaps some one off working groups/office hours)
- How to feedback, so that authors/champions update EIPs (if required) and repropose for future but don’t get burnt out from having to propose every 6 months, or spending effort on EIPs that will never get included.

Large number of EIPs being Considered for Inclusion ([14 so far for Glamsterdam](https://forkcast.org/upgrade/glamsterdam#considered-for-inclusion))
How to handle mid size EIPs (may not be important enough to be a headliner and too complex to be a small EIP)

---

**poojaranjan** (2026-01-05):

Adding comments from [ACDE 227](https://www.youtube.com/watch?v=1B03r5t03bU) Zoom chat

[![Screenshot 2026-01-05 at 9.36.00 AM](https://ethereum-magicians.org/uploads/default/original/3X/8/8/881a180f0cce3e300aa549addc5026c5e5a460e9.png)Screenshot 2026-01-05 at 9.36.00 AM270×307 19.1 KB](https://ethereum-magicians.org/uploads/default/881a180f0cce3e300aa549addc5026c5e5a460e9)

> So would this meeting mean there are decisions that are made there?

In short, yes. ACD-G would define the process, for example, limiting an upgrade to five EIPs, while EIP selection and decision enforcement would remain within ACD.

> Frequency
> Once a month, it can be increased or decreased depending on the ask.

[![Screenshot 2026-01-05 at 9.36.11 AM](https://ethereum-magicians.org/uploads/default/original/3X/3/d/3d06cd644a811a674ed2ee5f3729412094588061.png)Screenshot 2026-01-05 at 9.36.11 AM228×200 11.8 KB](https://ethereum-magicians.org/uploads/default/3d06cd644a811a674ed2ee5f3729412094588061)

ACDG will serve as a discussion and decision-making forum, helping save time in ACD meetings by allowing those calls to focus on technical specifications. This ensures that governance questions are resolved early and technical meetings remain technical.

ACD-G aligns on governance and process, while ACD enforces and executes.

---

**wolovim** (2026-01-05):

i’m currently opposed to ACDG as an open-ended decision-making call. seems fine to have space to jam on governance iterations (could also be ad-hoc when an appropriate topic presents itself), but imo specific changes to process should be introduced in ACDE or ACDC and subject to the usual rough consensus mechanism. taken one change at a time, i dont think this overwhelms the ACD agenda, especially when fork scoping isnt in full swing, like it is today.

i do agree that the ACD process still has plenty of opportunity for iteration and improvement. i would attend and contribute to calls that explore potential proposals to that end. but i would also advocate for the output of such a call to be a well-packaged proposal to bring to ACD(E|C) for consideration.

note: “consideration” may mean a short presentation, a time-boxed discussion, returning to async discussion and recruiting of co-signers, and a final decision being made in a future call. its only a tiny change, but this was the path of recent [(soft) requiring](https://github.com/ethereum/EIPs/pull/10391) of a primary point of contact for PFI’d EIPs, for example. bigger changes will (and likely should) require more investment.

---

**poojaranjan** (2026-01-05):

[@abcoathup](/u/abcoathup)

Thank you for taking the time to read and respond.

This proposal aims to establish a single, dedicated forum for “process governance” discussions while saving ACD meeting time by removing **process governance** topics and allowing ACD to focus solely on **technical governance**.

While the present proposal and your idea of ACD-G meeting aren’t the same, based on your response, I understand that you are in agreement with having an ongoing ACD-G meeting.

My personal preference is to focus on `"How" an EIP` rather than `"which EIP"` and we can formalize the format details as we move forward.

---

**poojaranjan** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wolovim/48/15214_2.png) wolovim:

> currently opposed to ACDG as an open-ended decision-making call. seems fine to have space to jam on governance iterations (could also be ad-hoc when an appropriate topic presents itself), but imo specific changes to process should be introduced in ACDE or ACDC and subject to the usual rough consensus mechanism.

ACD-G is proposed as a venue for deeper, “process-focused” discussions, similar to breakout room meetings, but **held only once a month**. Expected participants would include EIP editors and the EF Protocol Support team, along with developers and community members who are interested in participating in governance discussions, rather than all client teams.

The key question is the signal we want to send.

Should Ethereum governance be perceived as something done by the “Client Devs” only primarily within ACD - E/C/T meetings where time constraints often limit the ability to raise concerns or express disagreement in depth? Or should there be a clearly defined forum where editors, protocol support teams, and anyone from the community can openly discuss governance processes, share feedback, and raise concerns at length?

I view this proposal as a practical **trade-off**: saving 15 minutes, four times a week, across roughly 100 client developers, in exchange for a single 60-minute monthly meeting involving five editors, five EF protocol support team members, and a small number of community participants, depending on the agenda.

*Give it some more thought; this is a worthwhile trade-off.*

---

**wolovim** (2026-01-05):

i see a couple problems with this framing, but maybe its more productive to just ask: do you have any changes to the process in mind? the example of ACDG deciding to limit the number of eips in a fork and handing that down feels pretty unrealistic:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> In short, yes. ACD-G would define the process, for example, limiting an upgrade to five EIPs, while EIP selection and decision enforcement would remain within ACD.

maybe its more useful to consider genuine ambitions and the best path for them.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> I view this proposal as a practical trade-off: saving 15 minutes, four times a week, across roughly 100 client developers, in exchange for a single 60-minute monthly meeting involving five editors, five EF protocol support team members, and a small number of community participants, depending on the agenda.

also consider the amount of time it will take to explain the reasoning and implications of a decision made in ACDG, plus answering the questions and addressing pushback when the rest of the 100 client developers learn of it. ![:upside_down_face:](https://ethereum-magicians.org/images/emoji/twitter/upside_down_face.png?v=15)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> ACD-G is proposed as a venue for deeper, “process-focused” discussions, similar to breakout room meetings, but held only once a month. Expected participants would include EIP editors and the EF Protocol Support team, along with developers and community members who are interested in participating in governance discussions, rather than all client teams.

again, i see value in this gathering and i’d support it as a sort of working group (or choose another framing), which develops well-considered proposals to bring back to ACD. i believe it could effectively offer that definitive location for raising governance concerns and new ideas. if this group were to also make binding decisions, you probably end up with yet another governance process to decide how ACDG makes decisions and i dont think its worth it.

---

**nixo** (2026-01-05):

I agree with others that framing a governance breakout as an “ACD” isn’t the right way to go here. There’s already precious little time and adding another slot core devs feel like they have to attend to not miss important decisions takes away time from their primary responsibilities.

Beyond that, having a recurring governance meeting with regular attendees / facilitators who have authority to make binding decisions on the process risks both governance capture and “death by committee” / too much bureaucracy, in my opinion. I think that governance support should be primarily about describing and clarifying a process that is evolving, jumping in to support when something’s not working or happening too slowly, and helping to gently enforce decisions that have been made by consensus on ACD - rather than being authoritative itself.

As others have said, though, I think having a governance breakout where discussion happens around missing puzzle pieces, the best way to facilitate, how to improve technical support, etc., - but doesn’t have implicit authority to ‘make decisions’ about the process - would be valuable.

---

**poojaranjan** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wolovim/48/15214_2.png) wolovim:

> do you have any changes to the process in mind?

Today’s call was a good example of the limitations of using ACD meetings for governance and process discussions. In addition to this proposal, I shared two small process-change items for discussion and feedback, but time constraints did not allow for meaningful depth.

During the meeting, I raised both [Add Optional “Upgrade” Field to Standards Track Core EIPs](https://ethereum-magicians.org/t/add-optional-upgrade-field-to-standards-track-core-eips/27388) and [Best place to host “Call for Input”](https://github.com/ethcatherders/EIPIP/issues/397).

Ideally, I would have walked through the different variants of the proposed **Upgrade** field, outlined the trade-offs of each option, and taken questions to converge on a single approach before drafting an EIP. That was not feasible, as client developers understandably prioritized upgrade EIP selection over EIP template improvements.

Some may think, today was not the ideal moment to raise this. In a world of multi-upgrade preparations, it is difficult to identify a “perfect” time. Moreover, this request has been pending for long time, and since governance discussions occur only once a month, editors who joined the December call aligned on introducing an optional **Upgrade** field.

However, editors cannot unilaterally change the EIP template. Feedback is required from client developers, the EF Protocol Support team, and the broader community, which is why the proposal was brought to the ACD call today.

With less than five minutes available per proposal, there was limited opportunity for explanation, resulting in minimal feedback during the call and only one or two comments afterward insufficient to move forward with a template change.

Even with additional time, only a small subset of the roughly 100 participants would have been able to engage meaningfully, while many EIP editors who are not client developers would still be excluded. ACD-C/E/T calls are focused on specifications, and editors typically do not participate, as they have no decision-making role in spec discussions beyond editorial and process oversight.

The trade-off is clear:

**15 minutes × 4 calls per week × ~100 participants = ~6,000 minutes** , versus

**a single 60-minute monthly ACD-G meeting with ~15 relevant participants = ~900 minutes** .

From both an efficiency and governance perspective, ACD-G is the better trade-off.

---

**poojaranjan** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wolovim/48/15214_2.png) wolovim:

> also consider amount of time it will take to explain the reasoning and implications of a decision made in ACDG, plus answering the questions and addressing pushback when the rest of the 100 client developers learn of it

There are no restrictions on client developers joining if they wish to participate. The meeting will be held once a month, with the agenda shared in advance, and I hope interested developers will choose to join.

During Devconnect, in discussions with the testing and specifications teams, the idea of having a **client point of contact (POC)** similar to an EIP champion was also surfaced. This could be a valuable addition. Having a single POC from each client team, particularly for the testing team to coordinate with, may be more effective than having multiple representatives from the same team attend. The same can be recreated for Governance meeting - just the POC join the meeting. This approach would distribute responsibility and help ensure that decisions and plans are clearly communicated back to each respective team.

Ideally, I would like to see decisions reached on the same day as the discussion, even though we are not there yet.

---

> i see value in this gathering and i’d support it as a sort of working group (or choose another framing), which develops well-considered proposals to bring back to ACD. i believe it could effectively offer that definitive location for raising governance concerns and new ideas.

That is the present EIPIP meeting.

Personally, I am not confident that all “well-developed” “process-related” proposals will be of interest to all client devs, and they will welcome accepting at least one proposal each week to explain them in the ACD calls as an “EIP” is allowed to.

If getting a frequent room in ACD meetings is possible, I would see no need for ACDG, but if not, ACDG makes sense to me.

---

**poojaranjan** (2026-01-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> having a recurring governance meeting with regular attendees / facilitators who have authority to make binding decisions on the process risks both governance capture and “death by committee” / too much bureaucracy, in my opinion.

I beg to differ. I see this as a way to decentralization.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> I think having a governance breakout where discussion happens around missing puzzle pieces, the best way to facilitate, how to improve technical support, etc.,

Agreed, and I am proposing a name for this meeting - ACDG.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> but doesn’t have implicit authority to ‘make decisions’ about the process - would be valuable.

Please excuse me as I see ACDG as an “implicit venue” to discuss and make decisions with client devs, EIP Editors and community’s input and not handing “implicit authority” to an individual.

It will save the time & effort of everyone to meet at one venue and make decisions.

---

**kdenhartog** (2026-01-06):

The EIPIP call has traditionally been used to govern changes around ERC EIPs as well. How will that portion of EIPs be governed if this proposal were to move forward given ACD typically don’t engage at the ERC level very often?

---

**poojaranjan** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> The EIPIP call has traditionally been used to govern changes around ERC EIPs as well. How will that portion of EIPs be governed if this proposal were to move forward given ACD typically don’t engage at the ERC level very often?

Other than the network upgrade process, I do not see a significant difference between the EIP and ERC processes.

Based on my experience, the ERC community is mostly self-contained and rarely raises process-related concerns. Since the split between EIPs and ERCs, we have seen several changes to the EIP and upgrade processes, but none (at least to my recollection) on the ERC side.

The primary reason cited for the EIP/ERC split was the increasing volume of incoming PRs. However, as per the current open PRs, the [EIP repository](https://github.com/ethereum/EIPs/pulls) has **more than twice** as many open PRs as the [ERC repository](https://github.com/ethereum/ERCs/pulls) repository.

Honestly, I do not see any issues (in the near future) with continuing to manage ERC standards under the current process. If needs change in the future, we can revisit and consider alternative approaches.

---

**kdenhartog** (2026-01-06):

> Other than the network upgrade process, I do not see a significant difference between the EIP and ERC processes

I think this is the issue though. The network upgrade process is inherently consensus driven as if some portion of notes don’t agree then a hard fork emerges. When it comes to ERCs though, there’s no consensus driven process which means that ERCs are effectively only equivalent to informational track IETF RFCs. We can call it “standards track”, but the reality is it’s very different. At IETF in order to publish a “standards track” document, one has to conduct a BoF session, establish a WG, and then publish a consensus driven document to be considered a formal IETF standard.

This key difference in consensus driven governance will diverge the two processes over time hence the question. Today, the only form of consensus driven development that I’ve seen has emerged through alternative forums. For example, Walletconnect has established their certification program for wallets as a semi-formal process for wallets albeit it’s rather closed on how that’s defined. Similarly, Uniswap, Aave, ENS and other large protocols have opted to setup their own governance processes to govern their protocols.

I’ve heard whispering complaints in the community about the direction Walletconnect is going. Similarly so Uniswap has faced similar [issues](https://www.coindesk.com/tech/2025/05/07/why-one-of-uniswap-dao-most-outspoken-members-just-walked-away-in-frustration), Aave just had it’s [controversies](https://thedefiant.io/news/defi/aave-dao-controversy-rekindles-debate-on-tokenholder-rights), Similarly ENS DAO has [contemplated returning technical governance of the protocol to ENS Labs](https://discuss.ens.domains/t/metagov-working-group-2025-meetings-tuesdays-at-2pm-utc-currently-9-00-am-et/20078/54#p-58271-h-33-voting-on-technical-proposals-8).

In each of these cases, these DAOs have acted as the homes for the governance of many of these protocols which are effectively just ERCs establishing their own “standards” to operate their protocol on top of the network. For example, [ENSIP](https://docs.ens.domains/ensip/24) are effectively defining an ERC specifically for ENS. However, the impact of this also has downstream effects beyond just ENS because of how many protocols and people rely upon ENS. Should that be defined as an ENSIP or as an ERC then and who should decide that: ENS Labs, ENS DAO, or ERC developers impacted by it? This same question likely emerges with each other DAO as well, but I don’t follow them as closely.

The reason I point these examples out is because I believe one common thread between them all is that the EIP process has not defined a “standards” process like IETF. There’s obviously other aspects that went into each as well such as funding, technical expertise, ties to for profit corporations, etc. For ACD though these constraints are slightly different. The consensus was driven by the protocol itself as the top priority always because if the nodes fork the protocol we end up with two independent networks via a hard fork. That’s not the case for ERCs. Within ERCs we enjoy the fruits of a decentralized ecosystem at the expense of coordination in terms of both technical aspects and funding.

So, the reason I bring this up now is that when I see the change of the EIP process over the past few years, I see an increasing amount of coordination in funding and support for the protocol layer. I think this is good and absolutely necessary. However, if leaves me with the question of what role does EF (through it’s grants and salary budget) and the community beyond want the EIP governance process to play within the development of the Ethereum application layer? Does it want this to occur through alternative DAOs that exist on an adhoc basis with their own processes and governance models in favor of greater decentralization? Or does it want to consider how these large protocols could move governance back into the ERC process and add a more consensus driven process to support these protocols that build on top of Ethereum. This way it would operate as a more coordinated hub for the ecosystem like ACD has done for the protocol layer.

If it’s the former, I think we’re fine to just ignore the ERC considerations here. If it’s the latter than the governance process, and by extension EF and the community interested in coordinating the Ethereum application layer, needs to figure out how to coordinate these various communities to offer them a forum and governed process to coordinate like it’s been forced to do with ACD due to technical constraints.

So, in that case should the EIP governance process changes being proposed here also consider the impact on the ERC layer or are we fine to just ignore it and eventually move towards a model where the EIP process just don’t even govern the ERCs and leave that to external DAOs which will establish their own forums?

---

**abcoathup** (2026-01-06):

## ACD improvements

After listening to [All Core Devs Execution #227 - Forkcast](https://forkcast.org/calls/acde/227/) I am still **strongly opposed** to EIPIP meetings being rebranded as ACDG.

It comes across (whether intended or not) as an attempt for EIPIP to place themselves as a governing body above ACD.  This is an overreach and outside the remit of EIPIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> For many years, EIPIP meetings have served as the primary venue for EIP and network upgrade process improvements and governance discussions.

At least in recent years, network upgrade process improvements and governance discussions have primarily occurred on Eth Magicians and then adopted by ACD.

- AllCoreDevs, Network Upgrade & EthMagicians Process Improvements
- Community Consensus, Fork Headliners & ACD Working Groups
- Reconfiguring AllCoreDevs
- EIP-7723: Network Upgrade Inclusion Stages

Even the EIP/ERC split appeared by be driven by ACD rather than EIPIP.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> This proposal aims to establish a single, dedicated forum for “process governance” discussions while saving ACD meeting time by removing process governance topics and allowing ACD to focus solely on technical governance.

Whilst I would be ok with a working group which makes proposals for ACD to accept/reject.

I am not ok with a self appointed ACDG making decisions that are imposed on ACD. ![:warning:](https://ethereum-magicians.org/images/emoji/twitter/warning.png?v=15) This would be capture.

To improve ACD we should continue to do an [upgrade-retro](/tag/upgrade-retro) after each network upgrade (with an async component) and incorporate those findings into planning for future upgrades.

## EIP process

Repeating again: the EIP process should work for all core devs, not the other way around.

There are currently [354 open PRs](https://github.com/ethereum/EIPs/pulls) in the EIP repo.  The problem appears to be a lack of resourcing.  EF should have a dedicated person who’s only responsibility is making the EIP process smoother, getting PRs merged or closed, updating the website and making life as easy for EIP authors and ACD coordinators as possible.

Rebranding (but not to ACDG) may help with more exposure, but the problem is lack of resources.  Note: I spend (unpaid) time every weekday assigning EIP/ERC numbers (I’ve assigned 2/3rds of the numbers since we split EIP from ERC).

EIPIP should be narrowing their remit to focus on improving the EIP process, rather than trying to expand their remit as a way to get more exposure.

## ERC process

ERC process should be completely split from EIPs.

Given that there is a lack of resources, stretching the existing editors across two layers makes the processes worse and doesn’t allow for innovation to meet the needs of the respective layer.

There are currently [174 open PRs](https://github.com/ethereum/ERCs/pulls) in the ERC repo.  When authors ask how long to get a draft ERC merged, my answer would be weeks to months (unless you are [sharp elbowed](https://github.com/ethereum/ERCs/issues/1432), but the process should be blind, as well as fast for every author).

---

## Finally

Just wanted to add that improving ACD process, EIP process & ERC process are all really important and I am keen that they get the appropriate attention and resourcing to make that happen.

EIP editing and ERC editing are thankless tasks, so is process improvement.  So thanks to everyone involved.

---

**poojaranjan** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I am still strongly opposed to EIPIP meetings being rebranded as ACDG.

I appreciate the respect shown toward EIP editing work, and I’m deeply grateful for the many volunteer hours contributed to this space (including yours). I consider myself fortunate to have witnessed firsthand the time and effort the EIPIP working group invested in bringing greater stability to Ethereum governance.

For context, both the editors at the time and the ECH group spent hundreds of hours supporting the EIPIP meetings - educating contributors, enforcing process, and helping **establish the Fellowship of Ethereum Magicians as the primary discussion venue for EIPs**. The same level of effort went into maintaining the EIP and ERC repositories. The EIP/ERC split was discussed over 10s of meetings and many hours spent in collecting feedback from both communities. The split was requested by the EIP community, specifically the client devs, and the decision to split the repositories was ultimately made during an ACD call, where the majority of participants represented the EIP community rather than the ERC community.

*The intent of **ACDG** proposal is to enable a smoother transition and better coordination between long-standing contributors and newer participants.*

I believe Ethereum benefits most when we combine the experience of EIP editors who have supported Ethereum standards forever, with the involvement of the recent EF Protocol Support team involved in upgrade coordination and increased participation from client developers in governance discussions.

While many comments seem aligned with the underlying idea, there appears to be hesitation around rebranding EIPIP as ACD-G. This makes me wonder whether the framing is the issue. Perhaps the better question to ask is **whether the interested participants of ACD Meeting, including the EF team and client developers, would be open to joining the existing monthly EIPIP meeting to discuss Ethereum protocol governance.**

If so, what can the current working group do to encourage broader participation and make the forum more inviting and effective?

---

**poojaranjan** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> So, in that case should the EIP governance process changes being proposed here also consider the impact on the ERC layer or are we fine to just ignore it and eventually move towards a model where the EIP process just don’t even govern the ERCs and leave that to external DAOs which will establish their own forums?

The “ERC Standards” is the least demanding child ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

---

**kdenhartog** (2026-01-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> The “ERC Standards” is the least demanding child

Let’s be explicit about this then and formally remove ERCs from the EIP process while we’re making governance changes. There’s little reason to continue to neglect it but also claim it as something we care about.

I’d propose to do that we should remove all current non ACD related EIPs irrespective of their status (including final status) from the repo. This would remove the burden of them needing to be maintained by editors who are focused on ACD related work. We should also move the discussions about ERCs outside Ethereum Magicians, to reduce the moderation noise on this forum. If a person opens a draft EIP related to the application layer, it should be closed and the author should be told this is no longer the correct forum to propose this work.

---

**abcoathup** (2026-01-06):

I am pro a complete separation of ERCs from EIPs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> We should also move the discussions about ERCs outside Ethereum Magicians

For the short term I’d leave ERC discussion topics here.

EIPs and ERCs are in separate categories.

But longer term I think ERCs should evolve based on the needs of application layer developers.

---

**abcoathup** (2026-01-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/poojaranjan/48/1514_2.png) poojaranjan:

> Perhaps the better question to ask is whether the interested participants of ACD Meeting, including the EF team and client developers, would be open to joining the existing monthly EIPIP meeting to discuss Ethereum protocol governance.

For me the two contentious points were:

1. ACDG rebranding: gives the appearance that this group would control All Core Devs
2. EIPIP as the venue to discuss Ethereum protocol governance

On the second point, whilst this may have been true in the past, I don’t think it is the case now. That ship has long sailed.  Governance is now led by [EF Protocol coordinators](https://ethereum.foundation/assets/ef-org-chart.png).

My recommendation is that rather than EIPIP try to reclaim governance it should narrow it’s focus.  Double down on EIP editing:

- Rebrand as EIP Editors ™
- Solely focus on EIPs.  Serve All Core Devs (rather than the other way round).
- Fully split off ERCs.  Create a new group for ERC Editors so they can find their own way.
- Make the process quick and easy for EIP authors to get drafts merged, proposed and updated.
- Keep doing EIP editor office hours (great initiative)
- Merge/close back log of PRs and Issues.
- Make the job of EIP editors easier (more automation), so they can add more value to authors and increase quality of EIPs.
- Move to a new renderer (if that is going to help with speed of making improvements).
- Get EIP editors funded, ideally someone full time.  Get EIP Editors who work full time or significantly part time added to Protocol Guild.

---

With regards protocol governance I would engage with the EF coordinator driven process, either as individuals or better still collectively as EIP Editors.

- Feedback to upgrade-retro and recommend improvements to All Core Devs processes
- Provide input to fork focus & headliner selection
- Advise preferences for non-headliner EIPs

---

EIPs (and hence EIP Editors) are hugely important to Ethereum!

