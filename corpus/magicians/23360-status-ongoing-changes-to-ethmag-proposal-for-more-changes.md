---
source: magicians
topic_id: 23360
title: Status, ongoing changes to EthMag + proposal for more changes
author: nixo
date: "2025-04-02"
category: Magicians > Site Feedback
tags: [meta-magicians]
url: https://ethereum-magicians.org/t/status-ongoing-changes-to-ethmag-proposal-for-more-changes/23360
views: 296
likes: 18
posts_count: 7
---

# Status, ongoing changes to EthMag + proposal for more changes

# Changes to EthMagicians over the past few days

This forum has always been community-managed infra. Following this weekend’s outage, the Ethereum Foundation offered the support of its DevOps team by bringing EthMag into its broader Discourse infrastructure. Day-to-day administration by the existing admins and community remains the same, but the EF DevOps team now helps behind the scenes with hosting, backups, and performance monitoring.

What’s been added: daily offsite backups, system monitoring, and a dedicated maintenance window every Saturday morning CET. Infrastructure changes will only happen during that time unless otherwise coordinated. In that vein, all parties involved are aware that the forum is slow or intermittently unreachable right now and the forum will be taken offline between Apr 3, 5:30-7am UTC (~8 hours after this is being posted) to optimize performance.

During the outage last weekend, it wasn’t totally clear to either observers or active participants on the forum who the point of contact is, who the admins are, which of those are active, and where the best venue for EthMagicians news is when the site is down.

# Proposal

I have a few proposals for EthMagicians going forward. The gist of it is:

1. Transparency in administration and moderation
a. Designate a specific person to explore new Discourse features / formats for UX improvements
2. Resilience in access to the @EthMagicians Twitter account
3. Use of the Twitter delegation feature to make the account more active
4. Transparency of those delegates

## Transparency in administration and moderation

I think we should have a public list of EthMagicians administrators & moderators and clarity in their roles. This makes it easier to reach out to people when e.g. tags are missing from posts, posts are duplicated, someone has questions, or someone has suggestions on how to update the Discourse configuration to fully utilize any new, desired features. Ideally, the admin or moderators on the forum are active members of the community, regardless of affiliation. I don’t know who all is currently a moderator or how many there are. I find it easier as a newcomer to any space to orient myself, become an active contributor, and develop agency when the system’s structure is clear.

(1a.) Related, but worth a separate discussion to follow - it would be nice to explore new Discourse features to make the UX even better. This can be done by existing admin (ideally someone specific), a new admin, or a public RFP.

## Resilience in access to the @EthMagicians Twitter account

The Twitter account should have a minimum of two people with emergency admin access to the account - It seems prudent that one of these parties be the DevOps team that’s maintaining the infrastructure going forward - they have processes for securely holding and protecting login info and are an appropriate party to do so. If we secure this account operationally, we can reliably use it for communication about Ethereum Magicians when the forum itself can’t be reached and be reasonably certain we won’t lose access to it due to human error.

## Use of the delegation feature to make the @EthMagicians twitter account more active

Before the outage this last weekend, the Twitter account had 0 posts in the past year. I think posts can reach a much wider audience if we have a bridge between the forum and *Crypto Twitter* to let people know what’s going on in the forum. Twitter has a feature where you can safely designate accounts to post on `@EthMagicians`’s behalf without introducing much security risk - this permission can be revoked at any point by those with admin access to the account. These delegates should have requirements on their personal Twitter accounts:

1. No phone number attached to the account (this has been shown to be a security vulnerability by being a vector to bypass 2FA on Twitter)
2. 2FA with a hardware key or authentication app
3. Yearly password rotation

## Transparency of those delegates

Knowing who these delegates are means that the community can offer post suggestions to these individuals, keep them accountable, and generally have an idea of who’s active and who should be removed for decreased interest / participation. It would be optimal to keep the number of delegates small to reduce security risks, but the ones we do have should be active.

## Summary

The Fellowship of Ethereum Magicians forum is a core part of public Ethereum discussion — I’m glad to see that it’s transitioning to having a more resilient foundation and I think we can also transition its community-governed features to a transparent structure that’ll help keep it active and evolving in the future.

## Replies

**abcoathup** (2025-04-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> I think we should have a public list of EthMagicians administrators & moderators and clarity in their roles

https://ethereum-magicians.org/about

The about page of every Discourse forum lists the admins and moderators.

I am a moderator, elevated by [@nicocsgy](/u/nicocsgy). Prior to that my trust level was increased by [@anett](/u/anett) so when I flagged spam (I was seeing a lot of recovery spam) it would be hidden immediately.

---

**nixo** (2025-04-03):

Thanks! imo it should list roles and the forum should have more moderators than just one. That way, it’s clear who the appropriate contact for certain things are. With inactive admins or unclear responsibilities, no one feels “in charge” or like they have the right to make or propose changes. As one example, I’ve noticed several ACD meetings missing tags recently and I had no idea how to go about correcting that.

---

**abcoathup** (2025-04-03):

## Background

### Admins & moderators

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/8/8bb2ab44390d8253a13b422afe29bc6a0fe70c99_2_690x426.png)image1136×703 88 KB](https://ethereum-magicians.org/uploads/default/8bb2ab44390d8253a13b422afe29bc6a0fe70c99)

*[From: https://ethereum-magicians.org/about]*

#### Admins

[@jpitts](/u/jpitts) - Eth Magicians co-founder, EF DevOps

[@anett](/u/anett) - independent

[@matt](/u/matt) - EF Geth core dev

[@nicocsgy](/u/nicocsgy)  - EF

[@elasticroentgen](/u/elasticroentgen) - EF (assume DevOps)

#### Mods

[@abcoathup](/u/abcoathup) - independent (former editor Week in Ethereum News)

### Genesis

*[From [@anett](/u/anett): https://x.com/anettrolikova/status/1858537436378493308]*

> The Fellowship of Ethereum Magicians started back around Devcon3 where Jamie Pitts who was working as DevOps guy at EF and Greg Colvin who was involved with Core Devs as incentive to provide a place on the internet (and in person via Council meetings) for Core Devs and community to coordinate around EIPs. The logo of FEM was sparkle emoji and the tagline was “Rough consensus and running code”. Jamie wrote https://jpitts.medium.com/an-open-invitation-to-participate-in-a-fellowship-of-ethereum-magicians-982e6143db4f blog post describing vision, mission and goal behind the Fellowship of Ethereum Magicians. This is when the FEM forum was born.
>
>
> I was introduced to Jamie who invited me to help out with FEM operations as I was motivated to learn and wanted to help out with whatever I could. Jamie was kind enough that he decided to let me help with forum operations and host the FEM Council in Berlin and Community Room at Devcon Osaka. I designed cute unicorn stickers for this Council and this has become a sticker mascot for the FEM community, which I made multiple versions of for different events. Even nowadays I meet people with this cute sticker on their laptops!

### 2024

Eth Magicians was used for EIP/ERC discussions (which moved from GitHub issues), [@Tim](/u/tim) providing a venue for community engagement on future upgrades, and writing on ACD/upgrade process improvements (e.g. [AllCoreDevs, Network Upgrade & EthMagicians Process Improvements](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157)) and me occasionally asking for [naming](/tag/naming) for upgrades/testnets.

[@anett](/u/anett) elevated my privileges, as I wanted to hide recovery spam. (I was reading every topic and reply each week day as part of my former job).

I wanted a single location to permanently store ACD (and other protocol call) summaries of actions/decisions. ([AllCoreDevs, Network Upgrade & EthMagicians Process Improvements - #3 by abcoathup](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157/3)) and started an experiment to use Eth Magicians.  I was manually creating a topic per protocol call, making them wiki posts, adding tags, adding links to recordings and summaries (and chasing call moderators for these).

[@nicocsgy](/u/nicocsgy) (EF) got involved to refresh Eth Magicians (and was made an admin) and made a callout for improvements ([Call for contributions - Fellowship of Ethereum Magicians](https://ethereum-magicians.org/t/call-for-contributions-fellowship-of-ethereum-magicians/20814)).  The categories were updated and a [new logo](https://ethereum-magicians.org/t/call-for-contributions-fellowship-of-ethereum-magicians/20814/23) was the result.  [@nicocsgy](/u/nicocsgy) also made me a moderator.

### 2025

#### Automation

[@nicocsgy](/u/nicocsgy) is in the process of automating creating an Eth Magicians topic for each protocol call in [ethereum/pm](https://github.com/ethereum/pm/issues) (I had been doing this manually).  My end goal/hope is that this will also include links to call transcripts & chat logs.  Also to map GitHub labels to Discourse tags (tags are currently done manually but apologies for any I missed as I’ve been less active since my job ended).

#### Infrastructure

Historically infra was handled by [@jpitts](/u/jpitts)

*[From [@anett](/u/anett): https://x.com/anettrolikova/status/1858537436378493308]*

> Jamie Pitts is still working at EF as DevOps but he was running the FEM forum infra

[ethmag.org](http://ethmag.org) was purchased by [@nixo](/u/nixo) and pointed at [ethereum-magicians.org](http://ethereum-magicians.org)

There were some recent outages during upgrades  ([Mar 21](https://x.com/EthMagicians/status/1770500346051199172), [Mar 29](https://x.com/EthMagicians/status/1905855261728010720) & [Apr 3](https://x.com/EthMagicians/status/1907479694204874854)) and as part of this it led to a migration of the forum to EF Discourse infrastructure.

---

Apologies in advance for any errors, corrections appreciated.

---

**andreolf** (2025-04-22):

thanks for bringing more transparency here

---

**anett** (2025-04-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> it should list roles and the forum should have more moderators than just one

Forum have 6 moderators, I believe all moderators and admins are active and paying attention to the forum itself

---

**jpitts** (2025-04-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> Transparency in administration and moderation
> a. Designate a specific person to explore new Discourse features / formats for UX improvements
> Resilience in access to the @EthMagicians Twitter account
> Use of the Twitter delegation feature to make the account more active
> Transparency of those delegates

I agree with all four. I would add the following (they are basically adding more details about how to fully implement these ideas).

**Forum management transparency**

Transparency of membership should apply to Forum admins and moderators, as well as who is working in the operational aspect of Ethereum Magicians. Furthermore, I would propose there be a larger group w/ open membership, perhaps called “Magician-Stakeholders”. This group would come to consensus about larger decisions regarding the Forum, domain name, Twitter account, events, and so on.

Ultimately those in operations would be accountable to the Magician-Stakeholders and the wider community. I would not advocate for a lot of structure in this relationship however, do not have voting for decisions, etc. Reach the decision the same way it is done on the core devs calls!

These Discourse groups can communicate here on the Forum. I would propose that we update memberships of these groups every two years.

Additionally I think that we should also make it clear who is currently technically managing the Forum, domain name, etc. As of now, it is EF DevOps, a group that I have confidence can manage these resources on behalf of the Magicians and wider Ethereum community.

**Twitter account**

We should also make it clear who is currently technically managing Twitter. It will soon be EF DevOps, a group that I have confidence can securely manage the account on behalf of the Magicians and wider Ethereum community.

**Twitter delegation**

These suggested requirements make a lot of sense! I need to review if delegation would require a subscription, however if the cost is not too high it seems reasonable. Unless otherwise stated, I would propose that the group who is managing operations for Ethereum Magicians would decide who has access to the Twitter account.

