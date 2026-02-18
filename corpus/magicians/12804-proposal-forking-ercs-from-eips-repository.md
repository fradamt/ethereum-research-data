---
source: magicians
topic_id: 12804
title: "Proposal: Forking ERCs from EIPs Repository"
author: timbeiko
date: "2023-02-01"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/proposal-forking-ercs-from-eips-repository/12804
views: 5021
likes: 73
posts_count: 44
---

# Proposal: Forking ERCs from EIPs Repository

## TL;DR

- We should fork the EIP repo to create an ERC-only one, with ERCs displayed at ercs.ethereum.org
- Editors would be granfathered in both repos, free to resign on either side
- The processes can evolve independently, to suit the need of EIP vs. ERC authors, and welcome CL contributors to EIPs
- To avoid name collisions, EIPs get even numbers, and ERCs get odd ones.

## Background

ERCs are distinct from EIPs in that they concern themselves with the application layer, rather than consensus or client-related changes.

Over the years, this has led to friction and awkwardness in determining how EIP statuses should be interpreted for each type of EIP, what standards should EIP editors apply when reviewing ERCs vs. EIPs, and even how we should render their names ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

In addition, with The Merge behind us, there is now a desire to harmonize the EL & CL specifications processes. EL & CL teams currently have very different approaches to specifications, and it is to be expected that how EIPs are used in the context of network upgrades may change to accomodate CL practices, leading to further divergence between EIPs (especially Core EIPs) and ERCs.

Finally, the concept of “ERC editors” has come up frequently, and been stated as a “blocker” to separting out EIPs from ERCs. That said, ERCs *do* get reviewed today. By forking the repository, EIP editors would automatically be ERC editors as well (and free to resign from this). If this leads to no ERC editors, then it will be a strong signal to the community to step up and invest in this.

## Proposal

### 1. Fork ethereum/eips to create ethereum/ercs

Start from the same repository, and do not handle any major changes before the separation.

### 2. Create ercs.ethereum.org to render ERCs

Re-use all templates and styling from [eips.ethereum.org](http://eips.ethereum.org) - the website should look “the same”, minus the content.

### 3. Update EIPs repo to remove mentions of ERCs

Add a link to `ercs.ethereum.org` as part of the landing page, and do the same thing for ERCs repo.

Note that the ERCs repo will probably require a larger overhaul, but that can happen gradually.

### 4. Avoid Number Collisions by using Odd/Even Numbers for ERCs/EIPs

We don’t want ERC6000 **and** EIP6000 - going forward, EIPs would use the even number closest to the PR number by default, and ERCs would use the closest odd number. Historical EIPs/ERCs would be **not** be changed, e.g. ERC20 & EIP-1559 both break that rule.

### 5. Allow Both Processes to Evolve Independently

Once the split is done, both EIPs and ERCs can evolve in independent directions to best suit the needs of their users.

It’s important to remember that while there are constraints EIP editors can impose, the goal of the EIP and ERC processees should be to serve authors. If EIP and ERC authors have different goals with their specifications, the processes should accomodate them differently.

## Replies

**SamWilsn** (2023-02-01):

Playing devil’s advocate a bit here, but what benefits does this change bring?

I see a bunch of drawbacks that need to be addressed:

We already have [separate editor sets for both EIPs and ERCs](https://github.com/ethereum/EIPs/blob/96e1162f422b6da79f7af9b9a63b95e4f08d4a61/.github/workflows/auto-review-bot.yml#L42-L47). [@Pandapip1](/u/pandapip1) (plus me, a little) is mostly responsible for ERCs today. Anyone wanting to join as a pure Core EIP editor would be able to do just that.

This split would necessitate duplicating our CI systems, and having to maintain them both separately.

Similarly, I could easily see this duplicating all the meta/governance processes. Twice the meetings for editors that handle both ERC and non-ERC proposals.

Nothing here mentioned how we’d handle non-Core EIPs. I’d guess that we’d have to have Meta ERCs (at least ERC-1), and Meta EIPs still? Then there are still Interface, Networking, and Informational EIPs. Where do they go?

---

**timbeiko** (2023-02-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Playing devil’s advocate a bit here, but what benefits does this change bring?

I think the main benefit is that it provides a clearer “scope” for what the EIP process should accommodate, and can ideally help couple it more closely with the EL and CL specs.

Beyond that, I think it would highlight that the process *can* change, which has been a source of concern from CL folks about engaging with the EIP process: they fear that it is too bureaucratic and that coupling CL changes with EIPs will needlessly slow them down. Or, that the process won’t be able to accommodate their needs.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> This split would necessitate duplicating our CI systems, and having to maintain them both separately.
>
>
> Similarly, I could easily see this duplicating all the meta/governance processes. Twice the meetings for editors that handle both ERC and non-ERC proposals.

I agree this isn’t great - esp. the second point (machines are easier to duplicate than humans!). It might not be worth splitting the “meta governance” at first, until there is clearly a need for it.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/samwilsn/48/2874_2.png) SamWilsn:

> Nothing here mentioned how we’d handle non-Core EIPs. I’d guess that we’d have to have Meta ERCs (at least ERC-1), and Meta EIPs still? Then there are still Interface, Networking, and Informational EIPs. Where do they go?

I think Meta make sense across both, yes! For simplicity, I think you just keep all other categories in EIPs, possibly duplicating some? The Networking EIPs are all related to client software, so EIPs. Interface is split, so perhaps duplicate? Informational, not sure…!

---

**xinbenlv** (2023-02-02):

I can resonate with many points said by [@timbeiko](/u/timbeiko) . But forking is a big decision.

Before going down the route of a repo and process forking, have we evalutate the options to elect more Core EIP Editors? [@timbeiko](/u/timbeiko)

I have seen Yellow Paper drifted to obsolete and was quite a pity. I wonder what has blocked EL/CL from step up to continue editing Yellow Paper and the like?

EIP Editing faces its challenge today in lacking governance and a clear pathway to its membership. If more EL/CL developers join as Core EIP Editor, this could be resolved. ( FYI [@kdenhartog](/u/kdenhartog) who discussed this with me)

Meanwhile, the EthMagics will be meeting in person in ETHDenver on Mar 2nd, I like to invite you to join the conversation and meet with other EIP contributors and share your proposal if time works for you!

---

**timbeiko** (2023-02-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Before going down the route of a repo and process forking, have we evalutate the options to elect more Core EIP Editors? @timbeiko

I’ve been trying to get more editors for a few years now ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) One thing I think is important, esp. for Core EIPs, is that editors have a lot of context around what’s happening in the protocol, and so if we can get people in or close to client teams, that’s ideal.

One barrier for CL teams to engage more has been that they feel the EIP process is very bureaucratic and not tailored to their needs, so I think this separation would make CL folks more willing to engage.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> I have seen Yellow Paper drifted to obsolete and was quite a pity. I wonder what has blocked EL/CL from step up to continue editing Yellow Paper and the like?

I think the YP is a bigger can of worms: the math-heavy notation makes it hard to approach, it always “lags” behind as an official spec (i.e. at Fork X, the “spec” for the EL is “YP + EIPs in Fork X”), and post-merge, it doesn’t even have any notion of PoS…! My suggestion for it would be to do one final update to it, pre-Merge, and mark it as deprecated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> EIP Editing faces its challenge today in lacking governance

This might be controversial, but I think the EIP process might have *too much* governance today ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) If we look to what CLs do, there is much less friction, and client developers seem to really enjoy it. IMO, there’s value to some of the friction of the EIP process, but if it has a narrower scope (i.e. just consensus-related changes), we might be able to loosen constraints given we’re operating in a smaller domain.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> Meanwhile, the EthMagics will be meeting in person in ETHDenver on Mar 2nd, I like to invite you to join the conversation and meet with other EIP contributors and share your proposal if time works for you!

I won’t be there in person, but happy to join virtually if that’s possible ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**gcolvin** (2023-02-02):

I hate to wade into this, as we’ve been having this conversation for years and have yet to fork – I fear we will just rehash the same old arguments, on top of new arguments   So, wishing to only get my toes damp, (but knowing that my whole body will likely be getting wet) and repeating some points already made above and elsewhere by myself and others …

First an observation – our process was initially modeled to a large extent on the IETF process.  They have been managing the evolution and specification of the entire Internet for many years now within a single editorial process.  I don’t see that our project is at anything close to that scale.

> We should fork the EIP repo to create an ERC-only one, with ERCs displayed at ercs.ethereum.org

I don’t think simply forking the repos will solve the problems you bring up, [@timbeiko](/u/timbeiko) – most of which I agree are problems – and will cause more problems as well, as noted by others above.

I think some of the problems a fork per se might solve could also be solved within the repo by things like enforcing EIP vs ERC naming conventions, having separate ethereum/EIPs/EIP and ethereum/EIPs/ERC directories, adapting our requirements and templates to different needs, and other such.

> The processes can evolve independently, to suit the need of EIP vs. ERC authors, and welcome CL contributors to EIPs

I don’t think our users needs are so disparate we need separately evolving processes – I think that will just get us an even more confusing set of processes which would only get worse over time.

> To avoid name collisions, EIPs get even numbers, and ERCs get odd ones.

We’ve already lost an editor to disagreements over numbering.

> EL & CL teams currently have very different approaches to specifications, and it is to be expected that how EIPs are used in the context of network upgrades may change to accomodate CL practices, leading to further divergence between EIPs (especially Core EIPs) and ERCs.

Again, I don’t think the changes should be so great as to require separate repos.  I think that would only complicate matters.  Better to work on harmonizing the approaches.  These are layers of Ethereum, not entirely separate protocols.  For the most part the same client teams are working on both layers.

> Finally, the concept of “ERC editors” has come up frequently, and been stated as a “blocker” to separting out EIPs from ERCs. That said, ERCs do get reviewed today. By forking the repository, EIP editors would automatically be ERC editors as well (and free to resign from this). If this leads to no ERC editors, then it will be a strong signal to the community to step up and invest in this.

I think the signal is already pretty loud, and having diverging teams will only make things worse.

I’ve suggested before, as I think [@anett](/u/anett) has, that we need to lean more heavily on the Magicians.  ERCs cover a much wider range of interest and expertise than EIPs so it’s not a surprise that not many people are interested or qualified to review them all.  IETF proposals are vetted by established working groups before they get to Draft stage.  Rings of Magicians were intended to do the same, but haven’t really taken off.  But one way or another I think we need to encourage and support *peer review* to take a load off the more more permanent editorial staff.

> It’s important to remember that while there are constraints EIP editors can impose, the goal of the EIP and ERC processes should be to serve authors. If EIP and ERC authors have different goals with their specifications, the processes should accomodate them differently.

I totally agree on the goal.  But for all the reasons above and more I don’t think having multiple diverging processes and teams of people is the way to go.

So how do we get a better consensus on what the needs are and how best to serve them?

---

**gcolvin** (2023-02-02):

As for the Yellow Paper, that’s also been discussed *a lot* over the years.  My take remains that I’d rather see it improved than deprecated.  I think our Executable Spec may often better serve as a guide to creating and modifying clients – programmers mostly know how to port code  But as a program in an imperative language it’s not a good way to define Ethereum as a state transition function.  That’s what math is for, and the math in the Yellow Paper is not all that advanced – sets, tuples, boolean logic – it’s just not very well presented.   And there are in fact mathematicians and logicians doing important work on Ethereum who would struggle just as hard with a Python program as some programmers would struggle with the math. Yes, it’s going to lag the actual protocol, but that seems to me less of problem when we have an executable spec that is co-developed with the other clients.  Is the Foundation too poor to find the resources for this?

---

**kdenhartog** (2023-02-03):

Personally, I think the direction this is heading is similar to what I’m looking for in trying to propose utilizing the IETF process more. Looking at what [@gcolvin](/u/gcolvin) got in right as I was typing this up, it sounds like he’s suggesting we’ve been trying to move in this direction, but we’ve never been able to quite get there yet. I think this is the time to hammer out what it might look like so that we can make it easier for people to participate. This isn’t the first time I’ve heard of people leaving the EIP process to standardize work elsewhere because they found the process of EIPs too much of a headache.

Essentially the way IETF handled this issue in the past is to create specialized areas of development that have domain specific experts who participate in areas which are led by “Area Directors”. These AD’s essentially would be like EIP editors for specific areas and their primary goal is to help keep areas focused on specific pieces of work and to help form working groups that can move specific RFCs forward. This allows people to be able to focus on areas relevant to them and ignore areas that are not. For example, I’m primarily interested in wallet related EIPs and ERC related EIPs, so I’d just focus on tracking these specific areas. Others may only be interested in a specific EIP so they may only pay attention to communications in a specific WG. This would allow for communications to happen a bit more independently of each other and help reduce the beauacracy of non contentious pieces of work so they can move quickly, but also get robust review from specific people who are directly affected by a particular EIP.

It’s my opinion that we should be trying to emulate a structure like this so that we don’t actually need to fork. Instead we establish areas of expertise that are governed independently by experts of that area. Additionally, we can utilize this org structure to add in things like broad reviews (such as privacy and security) as well so that we’re able to catch breaking changes that happen independent of the WG work. This isn’t a perfect proposal, but I think the problem we’re faced with is actually one that’s solvable if we’re willing to start specializing work rather than trying to clobber everything on to each other and overwork editors like we’re currently encountering.

Here’s just a strawman proposal of what this might look like:

[![Screenshot 2023-02-03 at 12.59.11 PM](https://ethereum-magicians.org/uploads/default/original/2X/f/f7c19edc1db245db89cbe3a0182b591c1e3f6f32.png)Screenshot 2023-02-03 at 12.59.11 PM738×611 37.3 KB](https://ethereum-magicians.org/uploads/default/f7c19edc1db245db89cbe3a0182b591c1e3f6f32)

---

**fulldecent** (2023-02-03):

**This proposal will result in even less eyeballs on important EIP decisions, which could be catastrophic. And therefore it must be rejected.**

EIPs are already accepted, implemented, and “decided” on with minimal community involvement. A recent consensus change was decided by only Ethereum Foundation and announced on [Ethereum.org](http://Ethereum.org) blog with an effective date of +24 hours. Imagine if that change received even less attention than it already did and was announced even MORE last minute (like one hour before change). That would be catastrophic.

Now that the merge is complete, decisions are centralized even further. Every upgrade decision is held ransom with a cut-throat mechanism… because forking is no longer possible. Or to be specific, forking now costs each validator USD 50,000 to support. (To caveat here and avoid confusion, using a new network ID/chain ID is not a fork, it is a new product.)

Now that we have established EIPs are not receiving enough attention, let’s please accept the fact that ERCs are more popular, get more press and more attention than EIPs. Because they are written by individuals writing applications and are easier to understand. **This is the creator economy working!**

## Alternate proposal

So here is an alternate proposal that still allows people who don’t care about ERCs from having to see them:

1. Create a new RSS feed and button on eips.ethereum.org.
2. When you subscribe on that feed (or the associated email list, yes we need an email list) you will not be bothered with ERCs.

## Tenets

**We are one community.** ERCs/EIPs are ETHEREUM IMPROVEMENT proposals. As in the whole community—the clients, the applications, the JSON RPC, we even have proposals for how to make proposals and a proposal explaining that you *shouldn’t use* a certain opcode while not removing that opcode. All of these things are in one sandbox with one community. And so our IMPROVEMENT proposals should live together. In the end, we are all improving the same thing.

---

**EvanVanNessEth** (2023-02-03):

I made this proposal years ago and people got mad at me.

---

**Pandapip1** (2023-02-06):

I agree with [@kdenhartog](/u/kdenhartog) that the IETF structure is probably the way to go. I think we should get rid of the standard track type, and replace it with “core” and “ERC” (yes, this turns interface and networking EIPs into ERCs).Then, I propose we replace “category” with “categories”. Final EIPs can have categories added to them, and if authors from >5 Final EIPs come together, they can create a new category and add it to those EIPs, ensuring that the list of categories is up to date. The categories that will be displayed on the nav bar will be the five categories that maximize the number of EIPs discoverable.

---

**xinbenlv** (2023-02-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I’ve been trying to get more editors for a few years now

You are not alone. I definitely resonate a lot of frustration with you and EL/CL devs.

QQ: when you tried to get more editors for EL/CL, what has blocked your candidate from being admitted as editors?

How about this: admit everyone / a few members of EL/CL spec who currently has merge power of that repo as new Core EIP Editors and let them merge Core EIP PRs? [@timbeiko](/u/timbeiko)

---

**matt** (2023-02-06):

Thanks for writing up this proposal [@timbeiko](/u/timbeiko)!

This is one of the longest debated topics among editors. In the very early days (circa 2017), we thought that EIPs and ERCs could coexist in the same repository and be driven by various “rings” (e.g. working groups of magicians). Interest in rings dried up and we went several years without much coordinated work on EIPs outside core.

In mid-2020, [I proposed](https://github.com/ethereum-cat-herders/EIPIP/blob/9e967c97b7365f33411c33817b08e8c31fbff86e/All%20EIPIP%20Meetings/Meeting%20014.md#3-explore-the-idea-of-working-groups) to revive the concept and more closely follow the IETF organization structure by having working groups tackle specific topics / domains, each equipped with a champion who would be able to hold the group accountable and ensure progress (something I felt that was missing from the early rings).

Unfortunately this still did not gain traction. It eventually led to [more serious discussions](https://github.com/ethereum-cat-herders/EIPIP/blob/e9c94d6fde29d3f9a316a53e2cb0c27bb75205f7/All%20EIPIP%20Meetings/Meeting%20030.md#decisions-made) about bumping ERCs out of the repository entirely, to allow application developers more opportunity to self-organize. Because EIPs are critical to the core Ethereum protocol, we have generally been hesitant to grant individuals editorship who are not actively engaged with the protocol and strongly aligned with the philosophical interests of Ethereum.

And so, although many app devs are extremely talented and have great application-layer vision, it often felt inappropriate to include them as EIP editors because of the sensitivity of the position relative to Ethereum’s governance process. Plus, there simply were not many candidates who seriously pursued editorship in the first place.

In the intervening years, the EIP process has changed substantially. In some ways we are much better off than before. The work by [@SamWilsn](/u/samwilsn) and [@Pandapip1](/u/pandapip1) on improving the CI infrastructure has led to much more consistency across EIPs, and generally the review quality is rather strong. In other ways, we have created a system that developers want to [avoid at all costs](https://twitter.com/Sabnock66/status/1593362250550726656?s=20&t=LB9O3HToipT1JmvfriDwxg) due to arduous requirements, nitpicking, and poor communication about expectations.

–

This is the long winded way of saying that EIPs are at a local (I hope) minimum of relevance. There are a lot of issues and we can’t fix them all at once. I think that splitting the repositories down the line of “app standards in this repo, core in this one” is the best first step. We should focus on the one EIP type that we are good at, core EIPs. They’re also arguably the most important type. Applications can and [will](https://uniswap.org/blog/permit2-and-universal-router) create standards outside the EIP process. I think it is paramount that we eventually work with them to develop open standards *with* the community, but it is something we have been failing to do for over 6 years now.

IMO it’s easy to think that this change will drastically affect the community, but the reality is that they don’t care and are extremely amenable to change. I am really impressed with how quickly we were able to change many processes / naming schems that felt deeply embedded into the core of Ethereum: eth2 → EL+CL, ERC → EIPs → [and now back again](https://github.com/ethereum/EIPs/pull/5273), ACD → ACED (okay I’m still not sold on this one, sorry Tim), etc.

It will certainly be an inconvenience in the beginning, but I believe we will come out the other side with a better scoped organizational structure to begin engaging more contributors who do care about the ecosystem and its core processes.

---

**timbeiko** (2023-02-06):

Thank you [@gcolvin](/u/gcolvin) [@kdenhartog](/u/kdenhartog) [@fulldecent](/u/fulldecent) [@Pandapip1](/u/pandapip1) [@xinbenlv](/u/xinbenlv) [@matt](/u/matt) for sharing your perspectives - I appreciate the engagement here!

I think it’s worth it for me to take a step back and explain “where this is coming from”. The #1 thing that “keeps me up at night” here is that, today, **we don’t have a single, unified, way to specify a change to the Ethereum protocol**. I understand the historical reasons why this is the case, and think we generally made the right decisions to get us where we are. That said, in a post-Merge world, I feel like the specifications, and their associated processes, for Ethereum should also be “merged” (although I can live with minor differences, especially early on).

As many have noted in this thread, we’ve been circling this problem for a long time. My concern today is that the EIP process is very hard for some of Ethereum’s most important contributors - consensus-layer devs & researchers - to approach and engage with. After talking with several of them about this, my general impression is they feel the EIP process is high friction, not particularly well-suited to how they work and, most importantly, **reluctant to change to accommodate them**.

My rationale for splitting out ERC & EIPs is that this can be a first step to create a process for core protocol changes that works for both the execution and consensus layers. I feel pretty strongly this use the “EIP brand”, as it has very broad community recognition (see, e.g. EIP-4844 now, or EIP-1559. previously). Similarly, I think ERCs have achieved escape velocity as application standards (i.e. other chains even use $TOKEN-20/721 as their token standard, mimicking ERC-20 or ERC-721).

I appreciate there might be some technical overhead to splitting the actual repos and my goal isn’t to create needless work for anyone, but I do feel that integrating the consensus layer as part of the EIP process is critical to do relatively quickly, and we should be fine taking steps that aren’t as “clean” to make that happen. Given that, I’m skeptical that a short term solution here is “adding another layer of process” rather than “loosening some of our constraints to attract these people and iterate on a process from there”.

Another idea I’ve half-jokingly proposed is to myself become an EIP editor with the sole purpose of making life easier for CL folks who want to contribute ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12)

Hopefully this context helps! I’ll be on the [EIPIP call](https://github.com/ethereum-cat-herders/EIPIP/issues/210) this week to discuss this further, too ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

Now, here are a few more specific thoughts on the replies above.

> I think some of the problems a fork per se might solve could also be solved within the repo by things like enforcing EIP vs ERC naming conventions, having separate ethereum/EIPs/EIP and ethereum/EIPs/ERC directories, adapting our requirements and templates to different needs, and other such.

I don’t have any issues with this, **assuming we can then have more flexibility in updating the Core EIP processs**. That’s the main thing I’m after with this proposal.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I totally agree on the goal. But for all the reasons above and more I don’t think having multiple diverging processes and teams of people is the way to go.

I do think that Core protocol changes will need a different process from application-layer standards. We already see this in EIP-1, which has [a whole section on how Core EIPs are different.](https://eips.ethereum.org/EIPS/eip-1#core-eips)

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> This proposal will result in even less eyeballs on important EIP decisions, which could be catastrophic. And therefore it must be rejected.

I actually feel the exact opposite here: today, CL changes don’t even have EIPs. The number of eyeballs looking at the PR-by-PR changes to the consensus-specs is much lower than the number of eyeballs who can track EIPs X, Y, Z. I strongly agree with you that we should have a process which highlights changes to Ethereum, and that’s why I think we should be willing to “bend” most/all of our other standards for the purpose of having CL changes included in the EIP process.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> So here is an alternate proposal that still allows people who don’t care about ERCs from having to see them:

That’s not the problem, though: the problem is CL EIPs *don’t exist* today.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fulldecent/48/8663_2.png) fulldecent:

> We are one community. ERCs/EIPs are ETHEREUM IMPROVEMENT proposals.

While I agree at a high level, I do think there are some pretty important technical distinctions between application standards (opt-in) and core protocol changes (applied to all the network at a specific time). We already have separate specs for APIs, and I think that’s been a good thing. IMO specialization at the spec level doesn’t mean the community fragments, but instead that we can better support its different growing niches.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> QQ: when you tried to get more editors for EL/CL, what has blocked your candidate from being admitted as editors?

The main blocker is people who have the skills don’t have the desire to do this. I’m somewhat optimistic that if the EIP process was more accommodating to CL folks, we could get a couple of them to eventually join as (Core?) EIP editors.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/xinbenlv/48/16173_2.png) xinbenlv:

> How about this: admit everyone / a few members of EL/CL spec who currently has merge power of that repo as new Core EIP Editors and let them merge Core EIP PRs? @timbeiko

I’m happy with that *if we’re okay with them not explicitly following all existing rules*. If it lowers frictions and helps us build a better process, sure!

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> ACED (okay I’m still not sold on this one, sorry Tim)

*ACDE ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**kdenhartog** (2023-02-07):

Cross referencing this post because I think it’s highly relevant to this discussion as well:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png)
    [How do we address editors being overworked with a better governance method and what does it look like?](https://ethereum-magicians.org/t/how-do-we-address-editors-being-overworked-with-a-better-governance-method-and-what-does-it-look-like/12065/19) [Process Improvement](/c/process-improvement/6)



> I generally think we will need to get to that point as well. Something interesting about the W3C is that they have a small team of full time staff and then for the rest of their team, they’ve got fellows which are paid by W3C members (who are their employers) but spend 80% of their time just doing W3C related work.
>
> For me I don’t think the answer is that we need more editors, but rather that we should distribute their responsibilities to more people. From a governance perspective this is also…

One thing that’s clear to many of us here is that we need to find a process to move forward still and from the sounds of [@matt](/u/matt) we’ve actually tried to land one something similar to what I’ve proposed. As dumb as this sounds, I think part of the issue of why this might not have worked in the past is simply in how we’re using github, FEM, Discord, and Twitter to organize discussions and move work forward. As I’ve heard it put best “We shape our tools and then our tools shape us”. In this case, I think because we’ve tried to keep the “EIP process” within a single repository inside github that’s forced a lot of the processes we have today. For example, discussions moved to FEM because it was too hard to find the relevant discussions in the GH issues (I assume - please correct me if I’m wrong [@matt](/u/matt)). Also, editors ended up being core to the process because they were the ones who had merge rights in the repo. So, I think as we look at these changes we need to also evaluate how we’re using the tools to make this work.

For this reason, I don’t think my proposal in that linked post is best to do this in one large sweeping change. Instead my hope is that it is a “guiding plan” that we can iteratively implement and improve (or ignore in some cases) as we come across problems we need to solve.

For this specific problem (and I think it rings true for core devs and wallet devs alike) I think the first simplest step forward that we take is to form GH orgs for “ethereum-core” and “ethereum-standard-contracts” where we can start to create repos for EIPs to move forward. We could then turn the EIP repo in the “Ethereum” org into a landing page of sorts for finalized EIPs and a way to redirect to the other EIP areas. This way we’re still all within the “EIP brand”, but we’ve also got a bit more space to specialize and cultivate independent communities which we can cross pollinate in due time.

Also, I intentionally didn’t mention “ethereum-wallets” because I’m hesitant what to propose for wallets right now. Many are going multichain (not just EVM based, but also Solana or UTXO) these days so keeping this work only under the Ethereum umbrella could actually harm this area of development. We can figure out what to do for wallets a bit later, but it would be good to see what people think for them specifically once we’ve worked through getting the core/CL community and ERC community sorted first and learned what works and what hasn’t.

---

**SamWilsn** (2023-02-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/kdenhartog/48/7035_2.png) kdenhartog:

> discussions moved to FEM because it was too hard to find the relevant discussions in the GH issues

Discussions are on FEM because we try to minimize dependence on GitHub itself, and to aggregate discussion for each EIP into a single persistent thread instead of over multiple PRs and issues.

---

**sbacha** (2023-02-07):

How does removing something that is not even relevant to CL teams help them feel more comfortable in contributing to the EIP process?

Its Not the EIP process that is bureaucratic, its ACD. There its been said.

Adding a even odd numbering system makes things even less coherent.

If wanting to make such processes more accessible, maybe adding a “fast lane” shepherding process to expedite things would be beneficial. Give each CL team one such indulgence per quarter so that they can use it for things they want to prioritize getting through.

---

**xinbenlv** (2023-02-08):

Thanks [@timbeiko](/u/timbeiko) for triggering this serious and important discussion and taking time to patiently respond to me.  Sorry I have been quite busy recently and thus delayed to put down my responses in detail.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> I’m happy with that if we’re okay with them not explicitly following all existing rules. If it lowers frictions and helps us build a better process, sure!

That’s a good compromise to me. Having two sets of EIP editors and if necessary two editing/merging rules sounds much less controversial and better backward compatible than “forking the ERC out of EIP”. If you wanna make it an alternative proposal, I will co-sign the petition with you, including allow the Core EIP has its own editing rules ignoring all other existing rules. I am also happy to see the ERC EIP Editors / workgroup form from a group of people who specialize in smart contract and application building too.

If you don’t have time to draft this alternative proposal, I am happy to draft it too. Let me know how you like to do it. [@timbeiko](/u/timbeiko)

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> The main blocker is people who have the skills don’t have the desire to do this. I’m somewhat optimistic that if the EIP process was more accommodating to CL folks, we could get a couple of them to eventually join as (Core?) EIP editors.

Yeah. I feel sad that is the case and this is huge room of improvement for us as a community. We need to be able to attract contributors. I am in favor of making the EIP process more accommodating to “adopters”: CL/EL client devs of course, and also dApp developers, each in their working group.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> xinbenlv:
>
>
> EIP Editing faces its challenge today in lacking governance

This might be controversial, but I think the EIP process might have *too much* governance today ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) If we look to what CLs do, there is much less friction, and client developers seem to really enjoy it. IMO, there’s value to some of the friction of the EIP process, but if it has a narrower scope (i.e. just consensus-related changes), we might be able to loosen constraints given we’re operating in a smaller domain.

Your complaint is not controversial - I agree with you a lot.

You probably use “EIP Governance” to mean the “restriction before merging”. In that, I totally agree that it’s too much restriction.

When I use the “lack governance”, I mean something different. I will address this in a separate response.

---

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> xinbenlv:
>
>
> I have seen Yellow Paper drifted to obsolete and was quite a pity. I wonder what has blocked EL/CL from step up to continue editing Yellow Paper and the like?

I think the YP is a bigger can of worms: the math-heavy notation makes it hard to approach, it always “lags” behind as an official spec (i.e. at Fork X, the “spec” for the EL is “YP + EIPs in Fork X”), and post-merge, it doesn’t even have any notion of PoS…! My suggestion for it would be to do one final update to it, pre-Merge, and mark it as deprecated.

Wearing my developer hat I understand the execution-spec and the like are better than YP. Wearing my PhD student hat, I however understand the academia needs something like YP, just like [@gcolvin](/u/gcolvin) mentioned. The problem with YP lack of updates is not inheriting to YP itself, it’s a living testimony of that we haven’t foster a good enough open contributor culture to YP and a room of improvement. We can discuss this later.

---

**Pandapip1** (2023-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png) timbeiko:

> While I agree at a high level, I do think there are some pretty important technical distinctions between application standards (opt-in) and core protocol changes (applied to all the network at a specific time). We already have separate specs for APIs, and I think that’s been a good thing. IMO specialization at the spec level doesn’t mean the community fragments, but instead that we can better support its different growing niches.

It’s not in the scope of the EIPs repo to care about which EIPs are implemented where. IMO a core EIP that doesn’t get included should still be finalized in the EIPs repository, assuming it was extensively tested.

The process need not be different for Core EIPs and ERCs. Core EIP authors want their spec to be included as fast as possible in order to maximize visibility, to get discussion started, and to allow suggestions and proposal forks to be made. **The same motivation is true for ERC authors.** Therefore, the idea of *splitting* the repository makes absolutely no sense.

---

**polarpunklabs** (2023-02-08):

Apologies for my likely superficial perspective here, but I just caught this issue by chance.

However, I can’t help but wonder are the EIP volunteers or paid? (Will follow up depending on answer).

---

**timbeiko** (2023-02-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/polarpunklabs/48/8507_2.png) polarpunklabs:

> However, I can’t help but wonder are the EIP volunteers or paid? (Will follow up depending on answer).

Mostly volunteers, though “it depends”. Ethereum Cat Herders offered some stipends to some (and still might?), others do this as part of their “day job”, etc.


*(23 more replies not shown)*
