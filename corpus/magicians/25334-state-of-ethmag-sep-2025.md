---
source: magicians
topic_id: 25334
title: "State of EthMag: Sep 2025"
author: nixo
date: "2025-09-03"
category: Magicians > Site Feedback
tags: [meta-magicians]
url: https://ethereum-magicians.org/t/state-of-ethmag-sep-2025/25334
views: 109
likes: 10
posts_count: 4
---

# State of EthMag: Sep 2025

For the previous April 2025 update, click [here](https://ethereum-magicians.org/t/status-ongoing-changes-to-ethmag-proposal-for-more-changes/23360).

---

## Infra-related changes

After outages earlier this year, management of backups, hosting, and performance monitoring was transferred to the Ethereum Foundation Devops team. The transition to a team whose job is to run these services means that we can be better equipped to quickly handle any issues. EthMag is a high point of coordination for research and implementation work on the Ethereum protocol, so it’s essential that its availability is reliable.

To this end, two Devops staff were added as admins: [@ElasticRoentgen](/u/elasticroentgen) & [@midnite](/u/midnite). They will be responsible for keeping the forum online and software updated. Updates are regularly done during a maintenance window on Saturdays.

## Transparency in moderation

### Current admins

- jpitts: Founder of EthMag
- ElasticRoentgen: EF Devops
- midnite: EF Devops
- matt: Geth developer
- nicocsgy: EF Application Support
- nixo: EF Protocol Support

### Current mods

- marcgarreau: EF Protocol Support, responsible for the protocolbot that connects call issues with ethmag post summaries
- abcoathup: Publisher of ethdevnews, highly engaged long-time contributor
- poojaranjan: Leads Ethereum Cat Herders, highly engaged long-time contributor
- anett: Long-time contributor and Ethereum devrel

### Responsibilities

Admin responsibilities are mostly logistical - keeping the forum online, alerting any current issues, triaging emergencies, deleting spam, promoting user trust levels when new contributors can’t post, etc.

Mod responsibilities are more engaged with the day-to-day of the forum. This involves making sure that posts are correctly formatted, users are engaging in productive ways, and that call summaries are being correctly formatted

In addition, we have two category-specific moderators in the [Web category](https://ethereum-magicians.org/c/web/70):

- bumblefudge
- ulerdogan

## EthMagicians Twitter account

The Ethereum Magicians twitter account has been more robustly secured with access to three EF folks: Nixo, Nico Consigny, & Tim Beiko. We’ve already begun to make the account somewhat more active, but would love to improve on it. Feel free to tag the account for RTs      : )

And a proposal: I think it would make sense to add one or more of the existing non-EF moderators here as a delegate to the twitter account.

## Moving forward

The Protocol Support team is actively working on making the Ethereum upgrade process more transparent. We expect this category to stay active while we maintain and improve the protocolbot integrations and call summaries & discussions and EIP proposal discussions happen here.

We’d love for the other categories to similarly see active moderation and engagement. If you’re active in ERCs and want to be a category moderator, or have a proposal for a new category that you think could see good activity, please propose it! There’s plenty of room on this forum for more ownership of non-EIP, non-protocol-happenings type content.

## Replies

**abcoathup** (2025-09-10):

[@nixo](/u/nixo)

## Protocol Calls

Now that [forkcast.org](http://forkcast.org) has started adding calls, medium term do we need to also have call information on Eth Magicians?

Outstanding is supporting all call types and having a mechanism for call moderators to share action items & decisions.  Ideally we would also have a place to link to third party writeups.

I wanted a single location to permanently store ACD (and other protocol call) summaries of actions/decisions. ([AllCoreDevs, Network Upgrade & EthMagicians Process Improvements - #3 by abcoathup](https://ethereum-magicians.org/t/allcoredevs-network-upgrade-ethmagicians-process-improvements/20157/3)) and started an experiment to use Eth Magicians. I was manually creating a topic per protocol call, making them wiki posts, adding tags, adding links to recordings and summaries (and chasing call moderators for these). (After experimenting with sharing them on Mirror).  Prior to that ACD summaries were in a mix of Eth R&D Discord and Twitter, with transcript artifacts stored in Ethereum/pm.  [@nicocsgy](/u/nicocsgy) then started the automation process that [@wolovim](/u/wolovim) has continued.

As an aside, given [@wolovim](/u/wolovim)’s automation work, I think he should be made an admin.

## EIP/ERC discussions

Do you see EIP/ERC discussions continuing to remain on Eth Magicians?

EIP/ERC process is ripe for some automation and “forkcasting” style magic.

Numbers should be issued automatically, discussions topic should be created automagically, AI summaries should be made available.

## Long term future

Do we need a separate Eth Research & Eth Magicians Discourse forum?

Should [Ethereum.org](http://Ethereum.org) have a forum that includes this content?

---

**nixo** (2025-09-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> do we need to also have call information on Eth Magicians?

personally, i’ve always found ethmag as sort of an ‘intermediate’ place looking for a better solution! Github makes the data organized and queryable but it’s not user-friendly at all. EthMag is a little more user-friendly but it’s a terrible place if you want to systematically access data. I think the sweet spot is going to be storing data in Github and displaying it on Forkcast. I don’t see that as a place to read-write anytime in the near-term.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> I wanted a single location to permanently store ACD (and other protocol call) summaries of actions/decisions. (AllCoreDevs, Network Upgrade & EthMagicians Process Improvements - #3 by abcoathup) and started an experiment to use Eth Magicians.

I’m so glad you did! It was a much more human-readable place to interact with everything and created a bit more motivation to create another solution

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> As an aside, given @wolovim’s automation work, I think he should be made an admin.

Would be happy to! We just didn’t want to overwhelm the admin cast of characters with our team so soon after the EF helped take over the hosting and security responsibilities, and Marc made it clear that it wasn’t essential to his bot work.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png) abcoathup:

> Do we need a separate Eth Research & Eth Magicians Discourse forum?
> Should Ethereum.org have a forum that includes this content?

I think this is a good long-term goal but it doesn’t necessarily need to lose the history from these two forums - I think we’ll eventually be able to find a solution that retains the history & provides a better UX and I think a natural home for that is [ethereum.org](http://ethereum.org) (and would be much easier for people to find!)

---

**aguzmant103** (2025-09-12):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nixo/48/13434_2.png) nixo:

> I think we’ll eventually be able to find a solution that retains the history & provides a better UX and I think a natural home for that is ethereum.org (and would be much easier for people to find!)

Agreed. I think naturally [ethereum.org](http://ethereum.org) as a schelling point and might improve discoverability and collaboration if we have these forum discussions there

