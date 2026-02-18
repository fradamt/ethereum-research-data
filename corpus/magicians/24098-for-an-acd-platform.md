---
source: magicians
topic_id: 24098
title: For an ACD platform
author: marchhill
date: "2025-05-08"
category: Magicians > Process Improvement
tags: []
url: https://ethereum-magicians.org/t/for-an-acd-platform/24098
views: 302
likes: 21
posts_count: 9
---

# For an ACD platform

Going forward, it it crucial for the All Core Devs process to be more inclusive of many different stakeholders in the industry. Recent conversations around EOF have revealed the weaknesses of the governance process to include voices outside of the core client teams, [Tim’s recent post](https://ethereum-magicians.org/t/community-consensus-fork-headliners-acd-working-groups/24088) addresses this and calls for improvements to ACD. To go further in this direction, I believe ACD would benefit from having it’s own platform to serve as an official entry point for anyone in the ecosystem to voice their opinion.

At the moment the primary place for stakeholders in the ecosystem to voice their concerns is to join an ACD call. There are inherent limitations to this: there are only so many people that can be reasonable accommodated in a synchronous call. Such a small set cannot be said to represent the wider community as a whole, but just a tiny segment that happened to show up today. Speaking in an ACD call may also be more difficult for an outsider, who has to follow the ACD process and agenda, and wait through lots of technical discussions that are unrelated to them. There are other ways people in the ecosystem could voice their opinions: sharing async and being represented by someone else on ACD, posting on Ethereum magicians forum or Twitter. Although this can work, it is generally a haphazard approach that does not provide a structured way to judge the opinions of the wider ecosystem - we can build something which is the perfect format for this, tailored to the ACD process.

In light of this I propose creating a new ACD platform. This would be the canonical channel for everyone in the ecosystem to share their opinions on fork scoping and proposals asynchronously. This could include L2s, staking operators, application devs, tooling devs, etc. as well as the client teams themselves. Having a clear place to submit opinions simplifies things for everyone in the ecosystem. This allows us to rely on hard evidence in ACD calls; rather than using whoever shows up in the call as evidence of the community’s will, we can use actual statistics on a much larger set of stakeholders that are able to share their opinions asynchronously. As well as a place to submit opinions on fork scoping this platform could have wider applications as an entry point for ACD: giving opinions on individual EIPs / proposals, sharing important updates, agenda items, summaries.

In summary, if we are serious about bringing more voices into ACD then I believe building a new platform (or building on top of an existing one like Ethereum magicians) would be invaluable. Furthermore, I am not proposing to create this platform, then sit around and wait for people to use it - involving stakeholders will require active outreach from those more heavily involved in governance. The platform itself just acts as a hub, the canonical place that we can use to evidence what is most important to the community.

## Replies

**anupa** (2025-05-08):

I have developing propositions for grants and governance structures.

I am new to this ecosystem !! Happy to support !

I spotted some very important points between this post and Tim’s.

1. Critical and informed approaches towards decision making
2. The need to access decision making and concerns beyond a call.
3. Structuring consensus is a gap I see in making DAO’S  as it has many layers - knowledge, ability, acumen, availability, rights, recognition.

Creating a new ACD governance platform in structuring, tracking, and surfacing ecosystem opinions with clarity. It can be evidence-based, transparent decision-making and trackable. Using Dune analytics - what be great -  surface real-time, data-driven insights from the Ethereum ecosystem—tracking participation, sentiment trends, or protocol impacts.

Before building the platform, a focus group should first identify gaps and opportunities in the current  experience. Coupled with frameworks that can map stakeholder journeys and spot insights directly to feature decisions, ensuring the platform meets real ecosystem needs.

---

**abcoathup** (2025-05-13):

Rather than create a new platform, we can use Eth Magicians for async sharing.

Each upgrade as an Upgrade Meta EIP with a discussions topic on Eth Magicians ([upgrade-scope](/tag/upgrade-scope)).  Anyone can share their scope preferences, including L2s (Base did), dev tools (Solidity & Vyper) and anyone in the community (I did).



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png)

      [EIP-7607: Fusaka Meta EIP](https://ethereum-magicians.org/t/eip-7607-fusaka-meta-eip/18439/3) [EIPs Meta](/c/eips/eips-meta/67)




> Fusaka scope preferences
> Consensus Layer client teams
> Grandine
> Lighthouse
>
>
> Lodestar
>
>
> Prysm
>
>
> Nimbus
> Teku
>
>
> Execution Layer client teams
> Besu
>
>
> Erigon
>
>
> Geth
> Nethermind
> https://x.com/m25marek/status/1896911082628727213
> Reth
>
>
> Layer 2s
> Base
>
>
> Languages
> Solidity
>
>
> Vyper
>
>
> Community

---

**marchhill** (2025-05-14):

[@abcoathup](/u/abcoathup) thanks for the feedback. I’m aware of these discussion threads around upgrades. My point here is not that we need to do something completely different, but improve this process, and the overall ‘UX’ of interacting with ACD. Generally we want to make the process as easy, accessible, and transparent as possible to maximise the amount of shareholder feedback. I think we can make big improvements here on EthMagicians or with a new website.

I think EOF is a good example here. Although we had threads where stakeholders *could* share opinions, we still didn’t get sufficient feedback. Part of this is doing more to reach out, but imo if we made the process more accessible and streamlined that could help too.

Just like with ACD calls I don’t think big discussion threads are the ideal format here:

- If you know the thread exists and when decisions are being made, you are probably already very active in the ACD process
- You can’t see at a glance what the sentiment is, you have to crawl through many responses
- Everything is in separate places - you need to cross-reference meta-eips, eips, the Ethereum PM repo etc. to follow the process

The way I imagine is it a homepage for ACD that gives you streamlined access to what’s going on, without having to actively follow everything.

- All important info would be visible on homepage: upcoming calls, dates, hard forks being discussed
- For each fork you can see at a glance which EIPs are proposed, what is the sentiment of different stakeholder groups (client teams, L2s, tooling devs, etc.)
- You can click into individual stakeholders or proposals to open up more details

I hope this clears up what I’m proposing, basically tailoring everything to ACD rather than using a general forum.

---

**abcoathup** (2025-05-16):

[@marchhill](/u/marchhill) my preference is to use Eth Magicians to start with, rather than create a new platform.

I’ve created a wiki post that we can experiment with.  Feel free to edit as you wish.

I have pinned to [Protocol Calls & happenings](/c/protocol-calls/63)  but we could have as a banner.



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/abcoathup/48/2073_2.png)

      [All Core Devs (ACD)](https://ethereum-magicians.org/t/all-core-devs-acd/24198) [Protocol Calls & happenings](/c/protocol-calls/63)




> All Core Devs (ACD)
>
> Coordinate development on the Ethereum protocol.
> Agendas: GitHub issues on ethereum/pm (anyone can suggest items for the agenda)
> Calls are streamed on YouTube and X.  Call recordings with transcript & chat logs are available on Protocol Calls - Forkcast
>
> All Core Devs (acdc & acde)
>
> Weekly call focused on next + 1 upgrade & feedback to working groups
> Theme & moderators alternate between:
>
> Consensus layer: All Core Devs - Consensus (ACDC) - @ralexstokes
> Execution layer: All C…

At the very least it will serve as an experiment about the types of information needed and the overhead to maintain.

---

**marchhill** (2025-05-16):

Nice, I think this is a good start!

---

**philknows** (2025-05-22):

I’ll also double down on utilizing EthMagicians for collecting information because we don’t need another platform to scatter information even more. This has been established as the place for these types of discussions and we should be promoting one singular source of discourse, but perhaps figuring out ways to better present information to newcomers and existing contributors to Ethereum proposals/process. We even have great tie in between the Ethereum github and EthMagicians now via bots.

> The way I imagine is it a homepage for ACD that gives you streamlined access to what’s going on, without having to actively follow everything.

These are great points and also similar to how I imagine being able to get a bird’s eye view on what is going on. Probably not the best example, but to give you an idea - https://www.proposals.es/ tracks proposals to improve the JavaScript ecosystem. It’s more like an aggregator of already existing information to direct you to the right places. Maybe a directory is the right word? It has:

- A homepage which clearly identifies the stage of which every proposal is at
- Has a page that easily outlines how the process works, especially for newcomers
- Shows clearly who’s the point of contact (champion) of a specific upgrade proposal
- Cross references any presentations/documentation relating to presenting the idea
- It also links proposals to their Discourse threads: https://es.discourse.group/
- Page dedicated to specification proposals (in our case it would be Meta EIPs)

I think for the most part, we have the platforms, we just need a better way of collecting and presenting information in a clean, concise and digestible way.

---

**marchhill** (2025-07-10):

I think this [fork tracker](https://forkcast.org/upgrade/fusaka) being developed by EF is a great example of what I was suggesting here! Going even further it could have some way to get community input. [@nixo](/u/nixo)

---

**abcoathup** (2025-07-25):

[@marchhill](/u/marchhill) [forkcast.org](http://forkcast.org) has some feedback mechanisms:

- https://forkcast.org/rank: currently create sharable rank of Glamsterdam headliners
- https://forkcast.org/feedback: currently feedback on proposed Glamsterdam headliners (using a template on Eth Magicians).

