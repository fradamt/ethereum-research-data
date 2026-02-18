---
source: magicians
topic_id: 1525
title: Decentralizing EIP workflow
author: Ethernian
date: "2018-10-03"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/decentralizing-eip-workflow/1525
views: 2352
likes: 8
posts_count: 9
---

# Decentralizing EIP workflow

## EIP ??? : Decentralizing EIP workflow

| Ethernian |
| --- |
| Draft / Call to Action |
| Meta |
| 2018-10-01 |

## Abstract

This document proposes to decentralize an existing EIP classification process in order to increase its throughput and level of details possible.

The proposed process is aimed to be “*eth-ish*”: that means inclusive, decentralized on the global level, compatible with any organisation type on local level.

It is based on the signaling paradigm as much as possible.

It is compatible with any existing EIP classification workflows EIP-1, EIP-4, [EIP-1100](https://github.com/ethereum/EIPs/pull/1100).

This proposal has many similarities with [“Strange Loop” by @danfinlay](https://ethereum-magicians.org/t/strange-loop-an-ethereum-governance-framework-proposal/268) (even unintentional).

Special thanks to [@aogunwole](https://ethereum-magicians.org/u/aogunwole) for encouraging me to write this EIP and then giving me further ideas and clarifications.

## Motivation

Initially EIPs were mostly proposals for *CoreDev* community to make change into ethereum protocol. *Editors* are parts of *CoreDevs* and their mission was to pick technically sound EIPs with enough support from community.

Things have changed.

EIPs are not only about changes in ethereum protocol any more. Only few of EIPs require community consensus. Many of EIPs do not appeal to *CoreDev* and do not need to be reviewed by whole community before being implemented. Most of new EIPs are targeting some specific ethereum sub-community and not the whole ethereum community or only *CoreDev’s*.

Now EIP is in effect  an unique identifier and a vehicle to collect enough community attention for review. This core change in the meaning of an EIP is cause for a change in the classification process.

Current EIP reviewing process has some problems:

1. … it can’t keep up with growing number of EIPs. Many EIPs are stuck in Draft status. And in the future, the number of application related EIPs will grow even more rapidly. This is because an ongoing ethereum adoption will create demand for standartisation and coordination on the application level.
2. … it is designed with CoreDevs needs in mind. It became insufficient: Editors do not (and can not) categorize EIPs for other sub-community’s needs. For example, WalletDev community needs to review all new EIPs to find EIPs defining interfaces they should implement. Other communities have similar problems and they should read all EIPs with their needs in mind. This is an unnecessary repetition of Editor’s work.
3. … there is no easy way to collect a feedback on some EIP from independent communities reviewing different aspects of it.
4. … it demands you to propose a solution (the letter “P” in EIP). What if you target a problem, but you have no solution yet? It may be important to discuss the problem, even the solution is currently unknown. It is some kind of CTA (Call to Action), but there is no dedicated type for this kind of EIPs currently.
5. … EIP reviewer (Editor) is a hard job. It should be better incentivized.

Currently proposed solutions for the overstrained EIP review process are not sufficient:

1. … EIP authors are advised to get a feedback from the community before publishing a new EIP. It moves the load from Editors to communities, but at the same time EIP discussions become dispersed in different forums and disconnected from each other.
2. … more Editors will process more EIPs for CoreDevs, but it will not help other communities in their work.

## Basic Principles and Assumptions

- Communities are chat/forum based:
The Ethereum community is naturally organized around chats and forums identified by URL. Those online communities may be focused on different aspects and be mentally quite disconnected from each other.
- Communities are focused on different knowledge domains:
Communication in ethereum community is naturally organized around various knowledge domains.
There are CoreDevs, WalletDevs, Miners, Whales and so on.
Communities should review EIPs in aspects they are focused on.
- Tags should be meant as local to community
Any formalized terms (like statuses or tags) are defined and understood inside the community. They are just labels in some knowledge domain and may be quite unknown or misinterpreted outside of community. It means all terms should be meant as related to some community. Sharing terms between communities is possible, but needs additional efforts.
- Editor role becomes local to community
The same person can be Editor in many communities if trusted by them. Current Editors will become  trusted by CoreDevs and Ethereum Users communities. Most probably they will work for other communities like WalletDevs too.
- An advanced ethereum user is usually a member of many communities:
Example: A member of CoreDev community is naturally a member of Ethereum Users community too. This he has knows  terms and rules of both communities.
- Communities may be organized differently:
A global EIP review process should be agnostic about the way how the particular community is organized. It can be centralized or anarchistic - it should not matter.
- Anyone and any community can make review, but nobody has to take it into account:
Example: Anyone can express his opinion setting a tag on particular EIP, but CoreDevs are free to see and to follow only tags of their trusted Editors.
- Anyone and any community are free to build its own and unenforced opinion about EIPs:
CoreDevs do not have a special place in EIP process any more, nor they have to follow EIP statuses set by others. CoreDevs is now one of many ethereum communities (even very honored and reputable one).
Nevertheless Communities should make their trusted Editors public in order to make their opinion public and official.

## Proposal Outlines

In order to achieve or goals we propose to improve the current EIP workflow as follows:

- Splitting EIP target audience:
Currently, all EIPs are targeting the whole community. This creates huge overhead and is not necessary. EIPs should target an interested and responsible groups inside the ethereum community. Anyone outside target groups is primarily interested on the EIP status only.
- Ethereum Users community:
Ethereum Users community is a default one for all ethereum users. It defines few status tags unambiguously understood by anyone. There could be like “OK”, “NOT_OK”, “IN_PROGRESS”, “N/A”. These few tags should be adopted by any other ethereum community in inter-community communication.
EIPs changing global consensus should target Ethereum Users community to reflect their global impact.
- Externally defined Tags can be reused by community
Like common tags from Ethereum Users Community, it is possible to re-use tags from other community.
- Community can ask an external Editor to mark all new EIPs related to it:
Example: A WalletDev community asks an external Editor to mark any new EIPs that may be important for wallet development by using a tag “wallet”. The Editor is free to accept or reject request.
- An Editor can ask a Community for review a particular aspect of EIP:
Example: An Editor might be interested to initiate a discussion inside of Community of Miners about reducing a BlockReward, making his own decision depended on it.

## Community Examples

Here are some ideas for communities and their tags:

- Ethereum Users
Tags:
process: “OK”, “NOT_OK”, “IN_WORK”, “N/A”,
state: “CLASH”
- Developers
Tags: DesignPattern, Standard

CoreDevs
Tags: HF (needs hard fork).
- WalletDev
Tags: interface
- Browser
Tags: browser, ENS, user_permissions

*Miners*

Tags: ASIC, BlockReward

*Whales*

Tags: Inflation

## Replies

**Ethernian** (2018-10-03):

[@aogunwole](/u/aogunwole)

Would you post your objections here?

[@ligi](/u/ligi)

It would be great to see your opinion.This proposal was written with needs of *WalletDevs* community in mind, mentioned by you.

---

**ligi** (2018-10-03):

Sorry I can’t really give it a deep look before next week as I am at a conference this week

---

**boris** (2018-10-04):

Am following this, but also don’t have time for a deep dive yet.

Blink reaction is that we barely have any process and this is too heavyweight to move to, but that it would be good to get further throughput and adjust from there.

BUT – I think bottom up tags by communities can be effective, and then some Rings might start having “official” tags. Some of this can be an open process in the EIPs repo or elsewhere to suggest new labels for github issues.

Recently we have had three or four separate proposals for security token standards. On the one side – this is great! People see activity, rush in to share their own work. On the other side, what’s the role of EIP editors / the community? Do we tell them to go off and figure out *one* standard? This is partially already happening, in that some of the groups are getting sucked in and are working together.

I think this can be part of the discussion of Ring 13 ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9) Thank you for writing this up!

---

**Ethernian** (2018-10-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Ring 13

**“Ring 13”** - I like it!

if it not an official name yet, I would propose to do it.

---

**boris** (2018-10-04):

Groooooaaaaaannnnnn. It’s EIPs & Standardization, it just happened to land on lucky number 13 in the doc ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

---

**Ethernian** (2018-10-05):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> Groooooaaaaaannnnnn. It’s EIPs & Standardization…

I know.

I just like the name “Ring 13” more than “*EIPs&Standardization*” which is booooooooring.

Ring 13 is for real Magicians, don’t you think? ![:wink:](https://ethereum-magicians.org/images/emoji/twitter/wink.png?v=12)

sorry for off-topic - just amusing.

---

**ligi** (2018-10-09):

Thanks for the write-up. Just had some time to go through it. 2 Things that went through my mind reading this:

- I would not give whales a special role (or even no role at all)
- I think we should start simple  - e.g. by just doing the simple split I was proposing here once: https://github.com/ethereum/EIPs/issues/896 - even with this simple approach it is really hard to roll it out. Don’t think a big change like this will find traction and I think just splitting should be easier to roll out and already address the most important problem as far as I see - let’s not try to solve all problems at once as I do not think this will work.

---

**fubuloubu** (2018-10-16):

Lol, I should’ve read this before writing https://ethereum-magicians.org/t/proposal-add-ring-tags-to-eips-solicit-comments-from-ring-s/

