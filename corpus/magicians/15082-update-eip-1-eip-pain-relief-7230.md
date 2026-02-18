---
source: magicians
topic_id: 15082
title: "Update EIP-1: EIP pain relief #7230"
author: gcolvin
date: "2023-07-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/update-eip-1-eip-pain-relief-7230/15082
views: 761
likes: 5
posts_count: 13
---

# Update EIP-1: EIP pain relief #7230

***Note: This proposal is independent of whether or how to split the EIP repo.***

This draft PR is very much a work in progress.  So far it tries to alleviate some known pain points in the EIP process.  These include

- getting a Draft into the repo in the first place
- editing a document while complying with changing rules
- referencing relevant resources that aren’t specifically allowed
- ensuring that all referenced resources remain accessible
- assuring that the many Drafts we edit are technically sound and of high quality
- integrating the EIP process with the Reference Implementations and Core Devs workflows.

To begin with the last:

The Editors and the Developers are fairly independent organizations, with the Editors trying provide the services needed to publish a consistent series of high-quality EIPs.  We had envisioned (years back) that most proposals would arrive via independent Working Groups.  For the most part working groups didn’t happen except, de-facto, the Core Developers.

We propose to clarify the status of Working Groups, and to treat the Core Developers as an independent Working Group, responsible for the specification of Core EIPs and in control of their own workflow.

The Editorial stages for WG EIPs are reduced to three: Draft, Final, or Withdrawn.  Anything in between is part of the WG workflow, and should be tracked as such.  The formatting and notational requirements for a Specification, its relationship to other specifications, none of these are editorial concerns.  They belong to the Working Group.

The Editors retain responsibility for publishing a high-quality series of standards.  To that end we maintain the overall requirements for spelling, style, headers, citations, overall format (Preamble, Abstract … References …) and the like.  (Some core developers are already serving as editors, so we have a start on coordination.)

For the rest:

We propose to relax the enforcement of EIPW rules for Drafts, enforcing tighter rules only on changes of Status.  This should reduce a lot of the friction in the workflow.

We propose to allow editorial and working group discretion on the careful use of external resources, in line with IETF practice.  *All* references must include *full citations* with authors, title, and publication information, including available DOIs. Links are optional, but should meet the origin requirements of EIP-5757.  This helps to ensure that over time external resources can almost always be found *somewhere*.

We add a few optional headers for use by Working Groups to track their workflow.

We propose to introduce the role of Technical Peers –  volunteers with relevant expertise who can help Authors review their work at the Idea stage.  Editors may ask for them when a proposal needs more technical review than the Editors are able to give it.  This should help to reduce the strain on the Editor’s and increase the quality and general usefulness of proposals, especially ERCs.

## Replies

**shemnon** (2023-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> The intent of us EIP Original Gangsters, as I recall it, was that the Editors and the Developers be fairly independent organizations, with Editors simply providing the services needed to publish a consistent series of high-quality EIPs. We also envisioned that most proposals would arrive via independent Working Groups. For the most part that didn’t happen but, de-facto, for Core EIPs it did.

Two things, I take issue with your claim you are an EIP OG.  While you were an author in 2017 (EIP-615, and hence a developer) you did not [become an editor until 2019](https://github.com/ethereum/EIPs/pull/1992).  Early?  Sure. But *all* [the founding editors](https://github.com/ethereum/EIPs/commit/0d06b5e7390cccab722435eb834a159d82f3e715#diff-9a230270bca990e51726cf8bf7f14d78c639c279b6c5f07b1a5ac84322a88a14R179-R187), dating back to 2015, have left the process.

Second, such a claim to authority is to say that a small, fixed membership group has opinions that are more valuable than any new opinions.  This is centralizing, exclusionary, and biased to incumbency.  The validity of such arguments should be considered on their merits and benefit to the community, not based on the authority of who proposes it.  This also renders the argument of who is and who is not an “OG” or “Founder” distasteful, as the distinction is meaningless.

While some history may be useful for context. we should not consider ourselves bound to a process simply because it is the process that is already in place.

Similarly claims to “this is how the IETF” does it should be considered on it’s merits and value it provides.  Simply being part of the IETF process provides no valuable signal if the merits cannot be articulated.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> The Editorial stages for WG EIPs are only three: Draft, Final, or Withdrawn. Anything in between is part of the WG workflow, and should be tracked as such. The formatting and notational requirements for a Specification, its relationship to other specifications, none of these are editorial concerns. They belong to the Working Group.
>
>
> The Editors retain responsibility for publishing a high-quality series of standards. To that end we maintain the overall requirements for spelling, style, headers, citations, overall format (Abstract … References …) and the like. (Some core developers are already serving as editors, so we have a start on coordination.)

I think this is the “rest of the iceberg” that is occurring with this proposed split.  While these requirements are presented as light and tangential, some of these are key issues in the divergent requirements.  Style, header, and citations rigor has absolutely lead to authors swearing off ever submitting another EIP.  None of the developers are under a “publish or perish” regime, if a process was high friction they will simply not participate the next time around.  *This* is how the split has been forming for the past 4 years, passive withdrawal of authors who have experienced too much friction getting their spec published.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We propose to relax the enforcement of EIPW rules for Drafts, enforcing tighter rules only on change of status to Review and Last Call. This should reduce a lot of the friction in the workflow.

I have never seen developers raise issue with the requirement of a “security considerations” section.  But I have seen friction where a networking feature that had been stable and implemented in clients for years was forced through the two week “last call” process that was nothing more than perfunctory.  Editors and authors *should* have had and exercised the discretion at that point to say “This reflects reality and isn’t changing” and gone straight to final.  To make the requirement stricter is to move in the opposite direction

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We propose to allow editorial discretion on the careful use of external resources, in line with IETF practice. All references must include full citations with authors, title, and publication information, including available DOIs. Links are optional, but should meet the origin requirements of EIP-5757. This helps to ensure that over time external resources can almost always be found somewhere.

Editorial discretion is the part I have issues with.  Discretion is arbitrary and when invoked can be used as a lever to use to halt progress.  What if one editor says “I refuse my discretion to allow that link, I veto it, and will block consensus on submitting this EIP until that link is removed.”

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> We propose to introduce the role of Technical Peers – volunteers with relevant expertise who can help Authors review their work at the Idea stage. Editors may ask for them when a proposal needs more technical review than the Editors are able to give it. This should help to reduce the strain on the Editor’s and increase the quality and general usefulness of proposals, especially ERCs.

These technical peers already exist on the protocol side: ACDE and ACDC.  Do we have any confidence they will show from the Wallet, Layer 2, DeFi, and NFT communities?  My opinion is that as an independent organization for ERCs there is a greater likelihood they will be recruitable, but as long as the operate under the shadow of what ACD requires for it’s forking process they won’t feel their role is as vital as it could be and will be reluctant to participate.

---

Finally I would like to add that the problems in the “pain relief” items have been around since I’ve been in the process (2019), and it wasn’t until the Overton window shifted with the proposed EIP/ERC split that they really became seriously addressed.

We should not expect that pain relief items are going to change the fundamental divergence that is occurring.  This only address s symptoms and not causes.  **The cause is that Ethereum is growing**, it is growing into unexpected and fruitful communities. Communities with different norms, customs, and needs.  We should embrace this growth, and forcing communities together that are naturally and healthily growing apart only serves to harm all the communities.  We should feed this cause, not stifle it.

---

**gcolvin** (2023-07-17):

> The intent of us EIP Original Gangsters, as I recall it, was that the Editors and the Developers be fairly independent organizations, with Editors simply providing the services needed to publish a consistent series of high-quality EIPs.

> such a claim to authority is to say that a small, fixed membership group has opinions that are more valuable than any new opinions.

I’m only an authority on my own recollections, which I thought were not all that controversial.  The organizations are independent, and this would seem to be a reasonable summary of the Editors’ job.  That’s as intended.

I didn’t think claiming OG-ness was a big deal either.  It’s just history, for what it’s worth to the reader.  For me, it’s strong motivation.  I was a developer on the C++ team in 2016, and a contributor to the EIP process as well. When I became an ‘official’ editor I don’t know, but it was well before that commit, and before a period of intense work between Hudson, Nick, and myself cleaning up EIP-1, the repo and the bot.  I’m the last of that crew.  If I’m not Orignal I’m Old.

Anyway, I’ve removed those claims from the comments above as they have nothing to do with the proposal.

---

**gcolvin** (2023-07-17):

> Similarly claims to “this is how the IETF” does it should be considered on it’s merits and value it provides. Simply being part of the IETF process provides no valuable signal if the merits cannot be articulated.

The IETF was very much one of our models.  And worth looking at regardless – they are a decentralized organization that have been successfully managing internet protocols since the beginning.  Their RFCs span a very large range of technology.  They manage that range via Working Groups who approve of Drafts and final Standards.  They have only one Editorial organization:  it imposes basic standards of format and style, takes in Drafts and Standards and numbers them in order, and publishes Drafts and Standards in various media.

---

**gcolvin** (2023-07-17):

> Editorial discretion is the part I have issues with. Discretion is arbitrary and when invoked can be used as a lever to use to halt progress.

I’ve changed the line in question to:

> External resources not so permitted MAY be included at the Editors’ or Working Groups’ discretion.

Dscretion is always involved.  But maybe it shouldn’t go without saying that the discretion should not be arbitrary.

And I totally agree that over-tight standards on references have been a source of pain – I’m trying to relax the standards on what can be referenced, but tighten the standards on how things are referenced.

---

**gcolvin** (2023-07-17):

> I have never seen developers raise issue with the requirement of a “security considerations” section. But I have seen friction where a networking feature that had been stable and implemented in clients for years was forced through the two week “last call” process that was nothing more than perfunctory. Editors and authors should have had and exercised the discretion at that point to say “This reflects reality and isn’t changing” and gone straight to final. To make the requirement stricter is to move in the opposite direction

(If you are suggesting that all EIPs, not just Core EIPs, be handled by the same working group, or that there are groups to handle them, then that is fine by me.)

I’m trying make clear that the core devs have full control over their process. There is no more Review or Last Call, just the originally intended (sorry) Draft and Final, with the process for getting from Draft to Final entirely up to the core devs.

.

---

**gcolvin** (2023-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> We should not expect that pain relief items are going to change the fundamental divergence that is occurring. This only address s symptoms and not causes. The cause is that Ethereum is growing, it is growing into unexpected and fruitful communities. Communities with different norms, customs, and needs. We should embrace this growth, and forcing communities together that are naturally and healthily growing apart only serves to harm all the communities. We should feed this cause, not stifle it.

Yes, we are growing about as much as I expected … that is, since things were clearly going exponential there was no saying how far we would go … ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

I’m trying to clear out some self-imposed pain, which I think we Editors mainly caused by overstepping our bounds in various ways large and small.  We need to restrain ourselves from being anything more than service providers, and do a better job of providing a valuable service and otherwise staying out of our users’ way.

And I’m trying to give back to the Core Developers (and any future working groups) the freedom they need to manage their own process and the standards for their documents.

---

**shemnon** (2023-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> The IETF was very much one of our models. And worth looking at regardless – they are a decentralized organization that have been successfully managing internet protocols since the beginning. Their RFCs span a very large range of technology. They manage that range via Working Groups who approve of Drafts and final Standards. They have only one Editorial organization: it imposes basic standards of format and style, takes in Drafts and Standards and numbers them in order, and publishes Drafts and Standards in various media.

But I reiterate: unless the merits can be articulated independent of the source then it serves as nothing more than an interesting footnote and should have no weight in decision making.

---

**shemnon** (2023-07-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gcolvin/48/49_2.png) gcolvin:

> I’m trying make clear that the core devs have full control over their process.

If we did have full control the split would have happened back in February.

---

**gcolvin** (2023-07-17):

Historically, the merits were discussed in so much detail that “the IETF way” became pretty much the default.  I’m the last of those discussants still here, so I’ll have to be more clear now.  I gave a brief summary above of how they have organized their work, which is how we attempted to organize our work years ago.

---

**gcolvin** (2023-07-17):

I’m trying here to avoid a split.  I regret that we editors have failed to reach consensus on necessary changes, and that I failed to push hard enough to make a difference.

This proposal relaxes various rules and gives Working Groups more discretion (e.g. on links).  Authors have always been free to maintain and edit drafts outside of the EIP repo, and the Core Devs are free to do so now.  The Review and Last Call stages were impediments, and I propose that they be gone.

That means that, short of a split, developers can maintain Draft EIPs in a separate repo, edit them there, maintain their own workflow there, and ignore the EIP repo until the Draft is going Final.

(I’d suggest that a copy be merged back to the EIPs repo at major stages of the workflow and have proposed optional working-group headers for that purpose.)

If further freedoms are needed I really am all ears.

---

**gcolvin** (2023-07-20):

An idea I’ve been kicking around today.  Rather than split the entire repo just to move the ERCs, why not move most of the editing churn out of the EIPs repo into *two* other, smaller repos:

Today:

```auto
   ethereum/EIPs/...
   ethereum/EIPs/EIPS
```

Proposed (or something like it):  We leave EIPs repo alone, but stop using EIPs/EIPS as a place for working on drafts day to day.  We introduce two new repos for Standards Track EIPs:

```auto
   ethereum/WG-EIP/...
   ethereum/WG-EIP/EIPS/...
   ethereum/WG-EIP/EIPS/Core
   ethereum/WG-EIP/EIPS/Networking
   ethereum/WG-EIP/EIPS/Interface

   ethereum/WG-ERC/...
   ethereum/WG-ERC/ERCS/...
```

Here is how might work:

- When an EIP is first merged as a Draft to the EIP repo a bot merges it to the appropriate WG repo.
- Ongoing editing happens in a WG repo.
- When a new stage in workflow is merged to a WG repo it gets published by a bot back to the EIPs repo.

For most EIPs, including all ERCs, the default stages are Draft, Review, Last Call, and Final.
- For Core EIPs it’s up to the devs, but Matt suggests Draft, Eligible for Inclusion, Considered for Inclusion, Testnet, Mainnet, and Final.
- For Networking and Interface I’m not sure, but would happily let the Core Devs decide.

---

**gcolvin** (2023-07-31):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/shemnon/48/14006_2.png) shemnon:

> gcolvin:
>
>
> I’m trying make clear that the core devs have full control over their process.

If we did have full control the split would have happened back in February.

Right – that is the current situation.

I’m proposing that once an EIP is a Draft the Core Developers will have full control – in the sense that the EIP need not meet Editorial standards again until it goes to Final, which can happen *after* the upgrade.  And the standards for Draft should be fairly low.  The Editors should never be in the position of blocking an upgrade.

