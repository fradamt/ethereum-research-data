---
source: magicians
topic_id: 7400
title: Standardizing DAOs
author: thelastjosh
date: "2021-11-03"
category: Magicians > Primordial Soup
tags: [governance, dao]
url: https://ethereum-magicians.org/t/standardizing-daos/7400
views: 1980
likes: 14
posts_count: 4
---

# Standardizing DAOs

Hi folks ![:wave:](https://ethereum-magicians.org/images/emoji/twitter/wave.png?v=12), I’m Josh, computer scientist at Metagov.

Right now, nobody knows what a DAO is. You walk into a room of 10 experts, and they say 10 different things: it’s a multisig wallet, it’s anything with membership + ragequit, it’s got to have a voting, it doesn’t have to have voting, it’s a complex socio-technical system, it’s a PFP NFT, etc. Simultaneously, there’s been a slow proliferation of stacks / DAO frameworks, with minimal collaboration, interop, or re-use of code / applications between those stacks. All this is creating issues for potential users and for the DAO ecosystem at large. E.g., from Syndicate:

> “If we can just formalize what a DAO is, that would be incredibly helpful. We’re not confident in building on some of these stacks, because we’re not sure if they’re going to be around in 10 years. We want persistent scripts for persistent organizations. And if your provider disappears, there should be some recourse for you.”

Or, from Compound:

> "The important thing is to build a better ecosystem for DAO developers. How do you bring in the next 1000 devs? To do that, we need a shared set of tools.”

To address these problems, Metagov has been running a standards roundtable called [DAOstar One](https://daostar.one) featuring many organizations in the DAO space (including every major DAO framework), and we’re speccing out a new ERC standard for DAOs—featuring a “minimal DAO” + standard contract interfaces—that we plan to develop and ship over the next 4 months. You can read more details in the [DAOstar one-pager](https://docs.google.com/document/d/1P4kAxsi8fRXhWEUbkdeDkc4q2QKSeVrnnAs8ParF4Gs/edit#).

Our process is just getting started. For now, I wanted to reach out to the experts in this community to invite your participation (let me know if you’d like to hop in as an invited expert) and to solicit comments. What would you like to see (or not see) in a DAO standard? Do you think something like this is necessary; why or why not? How would you tackle the problem of supporting the existing DAO use-cases without restricting further innovation? As our process develops, I’ll also be posting updates in this thread.

Folks like [@lrettig](/u/lrettig) have told me about how valuable a resource this community is. I would love to work with y’all to figure out the approach for this standard and for DAOs in general. And if you managed to get to the end of this long post, please get in touch ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12) look forward to buidling together!

<3,

Josh

## Replies

**j0xhn** (2022-01-23):

This is very interesting indeed!  I’ve been thinking through my system for how I’d standardize DAOs and am setting up an official EIP at [EIP-1776 : ERC20DAO : Extend any DAO framework to be a legally empowered erc20 compliant token](https://ethereum-magicians.org/t/eip-1776-erc20dao-extend-any-dao-framework-to-be-a-legally-empowered-erc20-compliant-token/8078)

Will look more into this DAOstar project and see how it integrates.  Do you have access to their team or other DAO teams that would be interested in contributing, validating and expanding upon this base?

---

**thelastjosh** (2022-01-25):

Thanks for sharing this! We’re not going down the road of legal compliance with this standard but have discussed some ideas related to it in the DAO*1 roundtable. In the meantime, we should have a draft of the standard up and ready to share in this forum next week.

---

**thelastjosh** (2022-02-12):

Hi everyone,

We just posted a “working paper” version of the DAO standard here: [EIP-1234 Decentralized Autonomous Organizations](https://daostar.notion.site/EIP-1234-Decentralized-Autonomous-Organizations-Working-Paper-c89409d239004f41bd06cb21852e1684)!

**Short summary**: A standard URI and JSON schema for decentralized autonomous organizations (DAOs), focusing on relating on-chain and off-chain representations of membership and proposals.

**Why we need it now**: The working paper has a longer rationale that you can read, but based on the past four months of roundtable conversations with frameworks, tooling developers, and DAOs, there is strong consensus across the ecosystem that a daoURI + JSON schema, similar to tokenURI, is immediately useful and a great first step toward other DAO standards.

For those of you at ETH Denver next week, we will be presenting the draft at Schelling Point & ETH Denver. We’ll also be setting up a series of community calls to invite comment + discussion, and will post more details the week after next.

Cheers,

Josh, Isaac, Ido, Zargham, Eyal, Sam, and many others on the DAOstar team

