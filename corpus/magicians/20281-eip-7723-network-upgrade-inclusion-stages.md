---
source: magicians
topic_id: 20281
title: "EIP-7723: Network Upgrade Inclusion Stages"
author: timbeiko
date: "2024-06-12"
category: EIPs > EIPs Meta
tags: [meta-eips]
url: https://ethereum-magicians.org/t/eip-7723-network-upgrade-inclusion-stages/20281
views: 1732
likes: 26
posts_count: 23
---

# EIP-7723: Network Upgrade Inclusion Stages

Discussion for [Add EIP: Network Upgrade Inclusion Stages by timbeiko · Pull Request #8662 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8662)

## Replies

**abcoathup** (2024-06-13):

> client developers

**Client developers** isn’t a defined term.  (I’m not a core dev ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12))

There is a mix of **client developers**, **client teams** and **implementation teams**.  We should standardize on a single term e.g. **client team**, so when decision making is referred to client team**s** refers to multiple teams.

> ## Proposed for Inclusion
>
>
>
> The pull request SHOULD be merged in a timely fashion by the Upgrade Meta EIP author.

There is no explicit gate keeping mentioned.  To avoid spam proposals we should add something which allows the Upgrade Meta EIP author to not merge unreasonable EIP proposals. e.g. “**Reasonable pull requests** SHOULD be merged in a timely fashion…”

Otherwise the Upgrade Meta EIP could have lots of spam such as changing the gas token to the latest meme token.

We may want to have multiple Upgrade Meta EIP authors to make this a quick process. to get PFId, but the flip side is some gate keeping is required.

> ## Considered for Inclusion
>
>
>
>
> ## Scheduled for Inclusion

I thought the proposed intent of the new CFI status was that a single client team could make an EIP CFId but rough consensus was required for SFI.

I assume intentionally the **how** (rough consensus) and **where** (All Core Devs or async in a public forum) of the decision making process isn’t specified in this EIP.

There should be a path to remove an EIP from CFI & SFI.

“An EIP MAY be removed from Considered for Inclusion if client teams are generally against including the EIP in the network upgrade.”

“An EIP MAY be removed from Scheduled for Inclusion if client teams decide to no longer work on an EIP as part of the network upgrade.”

---

**timbeiko** (2024-06-13):

Thanks for the feedback!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> There is a mix of client developers, client teams and implementation teams. We should standardize on a single term e.g. client team, so when decision making is referred to client teams refers to multiple teams.

I’ve gone back and forth on single vs. multiple terms here, and opted for multiple to highlight that there isn’t really a single “body” involved. Client **developers** includes ppl who aren’t necessarily part of the core client team, and “implementation teams” includes things like testing/devops/etc.

> To avoid spam proposals we should add something which allows the Upgrade Meta EIP author to not merge unreasonable EIP proposals. e.g. “Reasonable pull requests SHOULD be merged in a timely fashion…”

Good point. Will update!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I thought the proposed intent of the new CFI status was that a single client team could make an EIP CFId but rough consensus was required for SFI.

We didn’t explicitly agree to that yet, so I’d rather have the EIP be “vague but true” than “precise but false” ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) Will update if that changes.

> There should be a path to remove an EIP from CFI & SFI.

Good point. I’ll also make it more explicit that this happens by default at each upgrade.

---

**abcoathup** (2024-06-13):

[@timbeiko](/u/timbeiko)

> ### Scheduled for Inclusion
>
>
>
> When client developers decide to work on an EIP as part of a network upgrade,

Minor quibble.  Using the term **client developers** as the gate for SFI implies that only 2 client developers (potentially independent) are required to SFI an EIP.  So an EIP could be forced in, but there is protection against this as there is now a removal path that the EIP could be removed if client teams are generally against.

Otherwise LGTM.

---

**timbeiko** (2024-06-17):

Copying over feedback by [@dapplion](/u/dapplion) on [the PR](https://github.com/ethereum/EIPs/pull/8662#discussion_r1642721930):

> I am not sure we need 3 states. Status CFI and SFI sound confusing. If an EIP is CFI should clients implement it already or not? If not, what’s the point of this status? Also, historically clients have implemented EIPs at different times depending on their priorities, regardless of overall consensus.
>
>
> I assume all EIPs in existence are meant to be included eventually, so all EIPs are automatically Proposed for Inclusion. Following the proposed work-flow of doing PRs against the meta-EIP, the existence of this PR already shows intent for the EIP to be scheduled.
>
>
> Why not have a single list: Scheduled for Inclusion? Consider the following flow:
>
>
> EIP is drafted
> EIP champion opens PR to the meta-EIP (= shows intent to be scheduled)
> Client developers, community members, and affected stakeholders can signal positive intent on the PR / forum
> Once rough consensus forms for inclusion, the PR is merged. At this point the EIP is expected to be implemented by clients

We already have 3 “statuses”: people do propose the EIPs (e.g. [here](https://ethereum-magicians.org/t/pectra-network-upgrade-meta-thread/16809)), and we use `CFI` & `Included` in Meta EIPs. The goal of this EIP is to make the first “implicit” status explicit, and have the nomenclature reflect that it is possible for `Included` EIPs to be removed from forks before they ship.

> If an EIP is CFI should clients implement it already or not? If not, what’s the point of this status?

Historically, `CFI` meant some clients started implementations but it was not mandatory for all teams to do so (which is what happens at `Included`). The point of the status is to highlight which of the many proposed EIPs will possibly end up in the devnets/fork. The original intent was to mirror [Concept ACK](https://github.com/bitcoin/bitcoin/blob/master/CONTRIBUTING.md#conceptual-review) in Bitcoin.

> I assume all EIPs in existence are meant to be included eventually, so all EIPs are automatically Proposed for Inclusion.

I don’t think this is the case. First, in practice, most EIPs are **not** included (nor should they be). Second, `PFI` (and `CFI`/`SFI`) is a per-fork signal. Even if an EIP is to eventually be included, there’s value in signalling that it is proposed (by the champion) and considered (by client teams) for a specific fork.

> Why not have a single list: Scheduled for Inclusion?

A couple reasons:

- We want to discriminate between “proposals by the community” (PFI) and “things client teams want to implement” (CFI+SFI)
- I want to avoid Github being a load-bearing part of Ethereum’s governance process. It’s fine to have code there because you can easily migrate it elsewhere, but using Github-native artifacts like PRs/Issues for governance carries heavy platform risk. If the PR itself is the “PFI signal”, then the .md file on its own doesn’t store the list of community proposals.

---

**timbeiko** (2024-06-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Minor quibble. Using the term client developers as the gate for SFI implies that only 2 client developers (potentially independent) are required to SFI an EIP. So an EIP could be forced in, but there is protection against this as there is now a removal path that the EIP could be removed if client teams are generally against.

good point! changed that to “teams”

---

**dapplion** (2024-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I want to avoid Github being a load-bearing part of Ethereum’s governance process. It’s fine to have code there because you can easily migrate it elsewhere, but using Github-native artifacts like PRs/Issues for governance carries heavy platform risk. If the PR itself is the “PFI signal”, then the .md file on its own doesn’t store the list of community proposals.

That’s a very strong argument. I agree that my suggestions rely excessively on Github artifacts which could disappear.

> We want to discriminate between “proposals by the community” (PFI) and “things client teams want to implement” (CFI+SFI)

I see the argument to have a per-fork signal of inclusion (PFI). You are right that some EIPs exist before they are ready to be included. However, I’m not sold on the need to have the two distinct lists (CFI+SFI). Having to maintain the two lists sounds like it would incur additional governance cost.

---

**timbeiko** (2024-06-18):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dapplion/48/5801_2.png) dapplion:

> Having to maintain the two lists sounds like it would incur additional governance cost

But we already have two lists: CFI and Included ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ! So, I don’t think it would be much different than what we have today, aside from PFI.

---

**wemeetagain** (2024-06-21):

What’s missing from the way we currently categorize EIPs is a way to differentiate between a weaker commitment to explore and hone a feature that we like vs a strong commitment that a feature *will* be landed.

I’ve seen that CFI is currently being used as both CFI and SFI and that leads to confusion and a hesitancy to CFI EIPs that are merely being considered. The benefit of CFI + SFI is that it practically relaxes the requirements for EIPs to be CFI’d by adding this missing “stronger” CFI (SFI).

To take a chapter out of the javascript process ([The TC39 Process](https://tc39.es/process-document/)):

Getting an EIP PR merged is like stage 0. This is a strawman proposal that has merely been edited for basic grammar.

Moving to PFI is analogous to stage 1. This is a signal that the EIP/feature is trying to be “taken seriously” but lacks peer review.

CFI is like stage 2. This is a signal that the EIP is well received by clients and that pending timing and the outcome of design iteration, it may be included eventually.

SFI is like stage 3. This is a signal and commitment that the EIP *will* be landed. Likely the design is also more baked.

Included is like stage 4.

---

**SamWilsn** (2024-07-04):

Who is responsible for taking actions? For example:

> an Upgrade Meta EIP MUST be drafted

Who does this? EIP Editors? Client teams? I’d like the document to specify who is responsible for each action that takes place.

In a similar vein, who gets to decide when we are “planning a network upgrade”? Can anyone come in and open a Meta EIP for an upgrade and then client teams pick whichever document they are following, or is there a specific process that Editors can enforce so that only probable fork documents get merged?

> Once a decision is made by client teams […]

How do EIP Editors know when a decision has been made?

---

**abcoathup** (2024-07-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Who does this? EIP Editors? Client teams? I’d like the document to specify who is responsible for each action that takes place.
>
>
> In a similar vein, who gets to decide when we are “planning a network upgrade”? Can anyone come in and open a Meta EIP for an upgrade and then client teams pick whichever document they are following, or is there a specific process that Editors can enforce so that only probable fork documents get merged?

Anyone can create an Upgrade Meta EIP, it is documenting community PFI EIPs, client dev CFI EIPs and  all core devs SFI EIPs.

Though in practice, without including an author from EF Protocol Support or multiple client teams then it is unlikely to go very far.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Once a decision is made by client teams […]

How do EIP Editors know when a decision has been made?

As for any EIP, changes are the responsibility of the EIP author(s).  EIP Editors don’t need to do anything.

---

**SamWilsn** (2024-07-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Anyone can create an Upgrade Meta EIP, it is documenting community PFI EIPs, client dev CFI EIPs and all core devs SFI EIPs.
>
>
> Though in practice, without including an author from EF Protocol Support or multiple client teams then it is unlikely to go very far.

This approach is fine, but I’d still like it written out in the proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> As for any EIP, changes are the responsibility of the EIP author(s). EIP Editors don’t need to do anything.

Then the proposal should be worded differently.

---

**timbeiko** (2024-07-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> This approach is fine, but I’d still like it written out in the proposal.

I purposefully didn’t make this explicit to not imply something like “the ACD coordinator should create the Meta EIP”. I think it’s fine to leave open-ended, and in the case where I didn’t do so, someone would feel like they could step up and do it?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Then the proposal should be worded differently.

Why do EIP editors “need” to know this? Is it because you wouldn’t want to move something to Last Call / Final if it wasn’t clear that “a decision was made”? WDYT of using a similar phrasing as in the SFI section?

> Once client developers have reviewed an EIP which was Proposed for Inclusion , they MAY move it to the Considered for Inclusion stage. The Upgrade Meta EIP MUST be updated to reflect this.

---

**SamWilsn** (2024-07-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I purposefully didn’t make this explicit to not imply something like “the ACD coordinator should create the Meta EIP”. I think it’s fine to leave open-ended, and in the case where I didn’t do so, someone would feel like they could step up and do it?

As I see it, the only two options are “Editors” or “anyone”. If it is indeed “anyone”, I’d like that to be clear in the document.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Why do EIP editors “need” to know this? Is it because you wouldn’t want to move something to Last Call / Final if it wasn’t clear that “a decision was made”?

I’m concerned about ambiguity.

For example, you use “MUST” here:

> the Upgrade Meta EIP MUST be updated to reflect this

We can’t force authors to take an action, so Editors have to enforce this requirement. That means Editors need to know when a decision has been made.

Similarly, is “a decision is made” a necessary condition to move an EIP into to “Considered for Inclusion”, or can an EIP author move it before a decision is made?

---

**timbeiko** (2024-07-22):

[@SamWilsn](/u/samwilsn) what do you think of the EIP being explicit about actors for **MUST** statements, but ambiguous for **SHOULD**?

For example, from the EIP:

> When planning a network upgrade, an Upgrade Meta EIP MUST be drafted to list EIPs in various stages of consideration.

I’d swap **MUST** for **SHOULD** here, as it’s a bit murky to define when we start planning a network update and it doesn’t really matter who authors the EIP.

> Before the Upgrade Meta EIP is moved to Final, the Scheduled for Inclusion stage MUST be renamed to Included and contain only EIPs that were activated in the upgrade.

In this case, I think the **MUST** is justified, and it would be good for Editors to block the transition if this isn’t the case.

> To formally propose the inclusion of a Core EIP in a network upgrade, someone MUST open a pull request against the Upgrade Meta EIP to add the EIP in the Proposed for Inclusion section.

Similarly, I think is is good to keep as a **MUST** if we want EIP champions to use this as the standard way to propose changes.

> Once a decision is made by client teams to move an EIP to Considered for Inclusion , the Upgrade Meta EIP MUST be updated to reflect this.
> When client teams decide to work on an EIP as part of a network upgrade, the EIP SHOULD move to the Scheduled for Inclusion stage, and the Upgrade Meta EIP MUST be updated to reflect this.

These become **SHOULD**.

> Once a network upgrade has been activated, all EIPs that were part of the upgrade MUST be moved to Included in the Upgrade Meta EIP, and the Proposed for Inclusion, Considered for Inclusion and Scheduled for Inclusion lists MUST be removed from the Meta EIP.

Keep as a **MUST**, because it’s easy for editors to judge (and worst case, correct) this.

---

**SamWilsn** (2024-09-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> When planning a network upgrade, an Upgrade Meta EIP MUST be drafted to list EIPs in various stages of consideration.

I’d swap **MUST** for **SHOULD** here, as it’s a bit murky to define when we start planning a network update and it doesn’t really matter who authors the EIP.

I think we should avoid passive voice here mostly. Something like:

> When planning a network upgrade, anyone MAY draft an Upgrade Meta EIP to list EIPs in various stages of consideration.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> In this case, I think the MUST is justified, and it would be good for Editors to block the transition if this isn’t the case.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> Keep as a MUST, because it’s easy for editors to judge (and worst case, correct) this.

Yeah, we can add `eipw` rules for these.

---

**timbeiko** (2024-09-04):

Thanks [@SamWilsn](/u/samwilsn)! Added your suggestions in [MUST -> SHOULD by timbeiko · Pull Request #8859 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8859)

---

**xinbenlv** (2025-04-16):

Personally I am in favor of the EIP

I am documentation a discussion and suggestion from the EIPIP meeting today with respect to whether to keep a stage type of `Declined for Inclusion(DFI)`

- @Gajinder brought up concern that when an EIP is marked as “Declined for Inclusion” it may have a negative signal. Especially when there are multiple DFI history across multiple Forks for an EIP, suggesting the DFI record to not be displayed
- @poojaranjan thinks keeping such records shows persistence of that particular EIP authors and builders and is a good positive signal, suggesting the opposite: DFI record should be kept and displayed.

Combining both, [@xinbenlv](/u/xinbenlv) suggested considering rephrase “Decline” to “Deferred” if it’s rejected for a specific Fork just because of lacking builder capacity/consensus. Pooja and Gajinder expressed support to this.

[@timbeiko](/u/timbeiko)

---

**timbeiko** (2025-04-16):

I’m against “deferred” because it implies we may eventually do something, which, in most cases, will not be true.

IMO it’s also a useful signal that an EIP has been `DFI`’d multiple times. If ACD said “no” to something over and over, it’s better to be aware of this and understand why “this time is different”.

---

**poojaranjan** (2025-05-19):

**[PEEPanEIP-7723 Network Upgrade Inclusion Stages](https://youtu.be/Ay6-RywzZQg)** with [@timbeiko](/u/timbeiko)

In this episode of **PEEPanEIP**, we unpack:

- Why these stages matter
- How they help with client coordination & testing
- The role of EIP editors, governance, and transparency
- Practical impact on Ethereum’s upgrade pipeline

  [![image](https://img.youtube.com/vi/Ay6-RywzZQg/maxresdefault.jpg)](https://www.youtube.com/watch?v=Ay6-RywzZQg)

---

**nixo** (2026-01-03):

Might be a good time to move this EIP to `Living` status rather than `Last Call`


*(2 more replies not shown)*
