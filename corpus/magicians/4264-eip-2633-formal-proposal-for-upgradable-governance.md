---
source: magicians
topic_id: 4264
title: "EIP-2633: Formal Proposal for Upgradable Governance"
author: edsonayllon
date: "2020-05-09"
category: EIPs
tags: [governance]
url: https://ethereum-magicians.org/t/eip-2633-formal-proposal-for-upgradable-governance/4264
views: 794
likes: 1
posts_count: 6
---

# EIP-2633: Formal Proposal for Upgradable Governance

A request for comments. PR found here. https://github.com/ethereum/EIPs/pull/2633

[Read the EIP here](https://github.com/ethereum/EIPs/blob/fe5cc96759cbcfe399858007d9eaa9e29e35a1de/EIPS/eip-2633.md).

## Replies

**adamschmideg** (2020-05-21):

I don’t see how this proposal would make the decision-making process more explicit. I see it as a 0th step in a sequence of governance EIPs. Maybe it would help to give some examples and links to the motions / schedules you are referring to. I think you could make it a bit more specific listing a few options for initiating a governance upgrade. That list doesn’t have to be exhaustive and it can be added to as per the process.

---

**edsonayllon** (2020-05-21):

> I don’t see how this proposal would make the decision-making process more explicit. I see it as a 0th step in a sequence of governance EIPs.

Correct. That was intentional. It’s meant to start governance EIPs, and ensure that one particular proposal isn’t followed indefinitely if it has flaws just because it becomes “the way we do things.”

> Maybe it would help to give some examples and links to the motions / schedules you are referring to.  I think you could make it a bit more specific listing a few options for initiating a governance upgrade.

I was inclined against this to not create bias in future EIPs, or imply that those should be how it’s done since this is a specification which eventually becomes frozen. But I can reconsider it.

---

**zhous** (2020-06-04):

Whoa, actually your EIP inpired me! Especially, “Currently, Ethereum’s governance is done off-chain.”

Ethereum  would be running by a DAO, let’s say EtherDAO. How to sustainablely fund itself? May learn from DASH. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

I’m working on [DAism](https://daism.io), a platform for DAOs. Everybody is welcomed to join us.

---

**edsonayllon** (2020-06-13):

After talking with an EIP Editor, I think you are right. There might as well be a specification for what triggers a governance upgrade process.

I was thinking of splitting that into two EIPs, this one, and a defined proposal for how to upgrade, but creating a proposal now may be better. Any revisions to that process can supersede this one in the future.

---

**edsonayllon** (2020-06-13):

Here are my current thoughts. Governance upgrades can be done by initializing a working group such as EIPIP (the current group).

The process can be triggered by:

1. Scheduled
2. And by need.

The scheduled upgrade serves as “maintenance.” Where the process is reviewed every period to search for underlying problems and areas of improvement. I suggest ever 3 years.

“By need” would be a response to an urgent signal the governance process needs revision. An example of an urgent signal is some conflict that may threaten a chain split.

