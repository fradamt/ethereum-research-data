---
source: magicians
topic_id: 25423
title: "PSE Roadmap: 2025 and Beyond"
author: aguzmant103
date: "2025-09-12"
category: Uncategorized
tags: [ethereum-roadmap, privacy, roadmap]
url: https://ethereum-magicians.org/t/pse-roadmap-2025-and-beyond/25423
views: 7930
likes: 59
posts_count: 32
---

# PSE Roadmap: 2025 and Beyond

*This is an aggregation of many ideas from across the ecosystem, shaped by contributions from many people smarter than us. Compilation was driven by [Sam](https://x.com/samonchain), with inspiration and input from Vitalik, Silviculture Society, PSE team & particularly* [Oskar](https://x.com/oskarth) *through countless conversations.*

# Introduction

Ethereum is on the path to becoming the settlement layer for the world, but without strong privacy, it risks becoming the backbone of global surveillance rather than global freedom. A system without privacy will push institutions and users elsewhere, undermining the very mission that brought Ethereum into existence. If Ethereum fails to build privacy, it fails to protect the people who rely on it.

That’s why we’re refocusing PSE from a cryptography explorations team, into a problem-first team: **Privacy Stewards for Ethereum**. Our role isn’t to own every solution in the space, but to drive clarity, focus, collaborations, and outcomes across the ecosystem ensuring privacy is treated as a first-class feature at the application layer.

This document lays out how we’ll pursue that mission, and how we can build together in the upcoming months and years.

# Overview

## Mission

*Our mission is to help define and deliver on Ethereum’s privacy roadmap.*

Ethereum deserves to become core infrastructure for global digital commerce, identity, collaboration, and the internet of value. But this potential is impossible without private data, transactions, and identity. We take responsibility within the Ethereum Foundation for ensuring privacy goals at the application layer are reached, and we’ll work with protocol teams to ensure that any L1 changes needed to enable strong, censorship-resistant intermediary-free privacy take place.

## Vision

*Our vision is to make privacy on Ethereum the norm rather than the exception.*

Ethereum will have comprehensive end-to-end privacy embedded across the technical stack (protocol, infrastructure, networking, applications, wallets). Privacy solutions will be widely adopted across core use cases (e.g. finance, identity, governance), seamless in user experience, performant, cost-effective, and compliant with global regulations.

## Identity

*We’re revamping our identity to reflect our new mandate.*

PSE is evolving from “Privacy & Scaling Explorations” to “Privacy Stewards of Ethereum”.

This is a change in name, mindset, and culture.

- We’ll focus on concrete problems vs. pursuing cool tech
- We’ll focus on ecosystem outcomes vs. internal projects

[We already revamped our website to reflect these changes: pse.dev](https://pse.dev/) as well as internal team’s goals and ways of working.

# Strategy

## Approach

PSE will compile and communicate the problem space, ensuring the ecosystem has clarity on priorities and confidence that progress is real.

**Principles**

- Subtraction by default. We should not do everything, we aim for the greatest impact where others do not act.
- Values: inspired by EF’s values of censorship resistance, open source, privacy, security. Our key points of leverage: credible neutrality, reputation, domain expertise, long-term thinking. They guide how we assess the ecosystem, provide constraints on how we evaluate options and make decisions.
- Problem-driven resource allocation. We fund efforts to solve important ecosystem problems based on outcomes we aim to see. This means working our way backwards from end goals, and structuring efforts as “problems to be solved” vs. “projects to fund”.
- These shape how we build, what we pursue vs. ignore, and how we prioritize.

**Process**

1. Problem radar: continuously map ecosystem problems related to privacy (iterative process; not a one-off)
2. Execution map: decide and act on what PSE should be actively involved in, with 3 levels of engagement: (a) lead vs (b) support vs (c) monitor, and metrics for tracking progress toward goals.
3. Communicate publicly: and invite feedback. share on e.g. public newsletters, open community calls, working groups, forums and blog posts. Continuous feedback loops should be the norm.

## Key tracks

Drawing inspiration from the simplicity of the [Protocol](https://blog.ethereum.org/2025/06/02/announcing-protocol) and [EcoDev](https://blog.ethereum.org/2025/07/10/future-of-ecodev) announcements, we’re aligning PSE’s roadmap around three clear focus areas. These come out out of our [privacy domain mapping](https://hackmd.io/@xzoey/HyR3Oi2Bxl), highly-rated [user stories](https://docs.google.com/spreadsheets/d/1fvfft-zaSiswxA6PRmw7dfZ4zalhmqdDxfFUyt_nGR0/edit?gid=714505087#gid=714505087), insights from [existing initiatives](https://pse.dev/projects), and various input from key community stakeholders e.g. [Vitalik](https://www.youtube.com/watch?v=oCANLFSCPq8&t=831s), [Silviculture Society](https://ethereum.foundation/silviculture-society), [EF management](https://ethereum.foundation/people).

### (A) Private writes

**Make private onchain actions as cheap and seamless as public ones.**

Improve the feasibility, usability and affordability of writing to Ethereum privately. Whether that’s sending a transfer, casting a vote, or interacting with applications. This track includes longer-term bets on FHE and pushing the cutting-edge towards practical obfuscation.

### (B) Private reads

**Enable reads from Ethereum without revealing identity or intent.**

Improve network-level privacy to ensure users can query, browse, or authenticate with Ethereum apps without surveillance or metadata leakage.

### (C) Private proving

**Make proving any data private and accessible.**

Make proof generation and verification fast, private, and accessible. Enable data portability and verifiable data provenance across environments, by delivering purpose-bound, data-minimized proofs for on/off-chain states, web data, documents, and identity attestations.

---

These tracks capture what PSE as Privacy Stewards of Ethereum is actively working towards and enabling, both for individuals and institutions. They also serve as rallying points for collaborators across the Ethereum privacy and scaling ecosystem.

These focus areas don’t represent everything PSE touches, but they form the backbone of what we’re committed to shipping and advancing. Specific priorities and initiatives within this tracks will vary in their investment timelines and deliverables, and will evolve with the ecosystem, but we expect these general focus areas to persist for the next few years.

## Key initiatives

These are PSE’s highest priority initiatives we’re starting or continuing executing on for next 3-6 months.

*(numbers for tracking purposes)*

**On Private writes**

### (1) Private transfers

- Continue PlasmaFold

Add privacy transfer features using PCD and folding. Targeting PoC by Devconnect
- Add post-quantum accumulation scheme.
- Work with Intmax and other ecosystem players on path to integration.

Support Kohaku ([privacy wallet PoC](https://github.com/ethereum/kohaku))

- Implement zk account recovery combination framework of N of M methods
- *Oversight of keystore implementation for stealth addresses
- .. and more on private reads side

Map and publish report with different technology approaches to private transfers.

### (2) Private governance

- Present a ‘State of private voting 2025’ report.
- Collaborate with teams on a new private voting protocol/assist with existing efforts.
- Continue work with Aragon and other integrations.

### (3) Confidential DeFi

- Kick off IPTF (Institutional Privacy Task Force) with EF EcoDev Enterprise team.
- Unblock institutional adoption, via privacy specifications and/or PoCs.

### (4) Private computation

- Continue long-term bets on programmable privacy (practical iO, vFHE)

Continue MachinaIO
- Oversee Phantom Zone grant

This nurtures the ecosystem with cutting edge research.
Continuing ecosystem mapping like [‘Open, Application-Driven FHE for Ethereum’](https://ethresear.ch/t/open-application-driven-fhe-for-ethereum/23044)

**On Private reads**

### (5) Network privacy

- Kick off Private RPC working group with internal researchers/engineers and external advisors
- Kohaku on private RPC: collaborate on privacy-preserving reading of the Ethereum state from remote RPC nodes by integrating an ORAM solution
- Broadcast privacy: bring privacy by routing transactions through mixnet. Spec (eth2p2p discv5) and implement the sphinx mixing protocol.
- End points with privacy-preserving RPC nodes: adding this and other privacy features into a browser with all privacy batteries included by default
- Methodically study the SOTA of ORAM and PIR and share insights in peer-reviewed venues
- Translate the outcomes of research research into ORAM and PIR into the Ethereum user experience: wallets, browser, and RPC nodes.

**On Private proving**

### (6) Data portability

- Advance development of data provenance protocols and tools. In particular

Stabilize and optimize TLSNotary: make our open-source, neutral and secure zkTLS protocol production ready for others to adopt and build other zkTLS protocols on top.
- SDK: build an SDK that enables seamless integration of the TLSNotary protocol across mobile, server, and browser platforms, improving DevEx and time to market for teams.
- Accelerate the ecosystem: drive adoption and innovation in zkTLS with community initiatives (e.g., zkTLS Day, X spaces, blogs), emphasizing privacy and robust security.

### (7) Private identity

- Advance the development of standards for generic zk-snarks
- Develop a modular, privacy-preserving ZKP wallet unit providing unlinkable verifiable presentations aligned with the EUDI.
- Research and develop revocation frameworks that support unlinkable and scalable credential revocation.
- Steward the digital identity ecosystem by advocating Ethereum and L2s as decentralized trust registries

### (8) Client-side proving

- Continue applied research on efficient, practical, ZK proving systems
- Credibly neutral benchmarking, drawing inspiration from ethproofs.org
- Includes efforts on Mopro, PPD, and Noir acceleration, a joint effort between the EF, Aztec, and other partners to improve Noir’s security, tools, and ecosystem to ensure that the next generation of private applications can be secured on Ethereum, in line with the EF’s 1TS initiative and enterprise adoption goals.

### (9) Privacy experience (PX)

- Holistic view of privacy experience from users’ perspective applied across all 3 tracks
- Identifying design patterns, commons interfaces, tools/specs/standards needed.
- Will include design, comms, events, website work to support privacy efforts.

# Next Steps

So where do we go from here? If you’re building privacy, we want to work with you. Whether we collaborate through working groups, standards, by sharing research, or just by rooting for your project.

If you read all this way and saw something that didn’t make sense or could be better, we want to hear from you! What did we miss? What’s being mis-prioritized? What’s been over invested?

If you want to reach us over chat please go for [ethresearch discord](https://t.co/EqHJvFlv9E) in the [privacy](/tag/privacy) channel. Find our work at [pse.dev/projects](https://pse.dev/projects) and [pse.dev/research](https://pse.dev/research). Learn our published work at both [ethresear.ch](https://ethresear.ch/) and [ethereum-magicians.org](https://ethereum-magicians.org/).

Hope to see you all at Devconnect in one of the following events we’ll be present, organizing, or supporting: Ethereum Cypherpunk Congress, Privacy Community Hub, zkTLS Day, zkID Day, Ethereum Privacy Stack, PSE Day, Obfuscation Day, Noircon3, and many more

## Replies

**chanderprakash20** (2025-09-13):

Could anyone from PSE TEAM  memenber  connect with me , We are a dedicated research group working on FHE-based ZK-EVMs for both Layer 1 and Layer 2, and we seek grant support and collaboration with the PSE team. We have already spoken with Kev and Rahul from the ZK-EVM team, who recommended we connect with you. Please reach out so I can send our research proposal and discuss next step

---

**aguzmant103** (2025-09-14):

Just DMed you, my TG is @andyguzmaneth but in general you can reach us in the Eth Research Discord [https://discord.gg/qGpsxSA](https://t.co/EqHJvFlv9E)

---

**matt** (2025-09-14):

Overall I like the mission, key tracks, and new focus. I would generally like to see more of a formulated strategy to get these projects mainstream and in L1, where it makes sense. We’ve seen many times over that users don’t gravitate to the private / safe / secure option directly. E.g. I’m not sure how PlasmaFold will get users over the many private alternatives, or why Kohaku / private RPC users would be different those who are already running nodes and interacting with local data. If these features are baked into the protocol, they will be used.

---

**chanderprakash20** (2025-09-15):

I dmed  you on telegram please check that

---

**jflo** (2025-09-15):

I think the framing of Privacy in terms Reads, Writes, Proofs is pretty weak. Actual privacy improving features will span some or all of these to varying degrees.

For example:  Market Privacy seems to be a very low priority amongst all the components of this initiative. I had to dig through a number of links before I found where MEV mitigation fit on the problem radar. Does this use case fall neatly in with the Writes?  IDK, maybe? Will executing on Writes for 3-6 months improve my protection from front-running? no idea.

I would much prefer to see a roadmap that could correlate these areas of focus with use cases that will get fixed, and prioritize them. As presented, ACD cannot reason about what privacy improvements these will yield, how complex they might be, or what order they should be pursued in.

---

**igorbarinov** (2025-09-16):

> I would generally like to see more of a formulated strategy to get these projects mainstream and in L1, where it makes sense

I have a hypothesis about the broader adoption of on-chain privacy for consumers. There should be a shift away from using CEXs to break the chain of custody. This transition can follow the same market dynamics we’ve already seen: from CEXs for spot trading to DEXs for spot trading, and from CEXs for interoperability to bridges. What is needed for on-chain privacy protocols to begin gaining market share?

- Lower fees. For example, a 0.25% shield/unshield fee in a leading privacy protocol is hard to compete with compared to 0% (adjusted to EOA token transfer) for shielding and ~ 2 USDT to unshield via a CEX (e.g. on Tron where stable coins volume are massive and CEXs are main tools for consumer privacy)
- Faster UX. The travel rule, increased compliance, geopolitical factors, and tighter restrictions on amounts (e.g., the proposed Bank of England cap on stablecoin holdings) can make on-chain privacy pools more attractive
- Plausible deniability. Tools like 7503 on L1 and L2, specifically designed for privacy, combined with other on-chain primitives, can reduce the risk of receiving a 10/10 AML score for the average user

> E.g. I’m not sure how PlasmaFold will get users over the many private alternatives

PlasmaFold is a project from the scaling part of PSE’s past and is likely exploring a recently assigned privacy mandate. If it does not fit, I believe it could graduate and become one of many private alternatives with all the benefits of VC funding and via funding can get (aka buy) users

I am just speculating here; I don’t have any insights

> or why Kohaku / private RPC users would be different those who are already running nodes

Kohaku (and eventually Ambire https://www.ambire.com/) plan to include PIR (Private Information Retrieval)-enabled remote RPC as a must have feature. The main difference between using remote nodes and running local nodes is that users would not need to host nodes locally while have a significant privacy advantage. ELI5: the eavesdropper (Eve) from an indexer or RPC provider would only see that Alice (identified via KYC, email, IP tracking or device tracking) requested an operation on encrypted data, which was processed on encrypted state and returned to her in encrypted form. This makes it much harder to correlate her activity with on-chain actions of Alice or Bob ![:people_hugging:](https://ethereum-magicians.org/images/emoji/twitter/people_hugging.png?v=12)

Since running local nodes is almost impossible on mobile devices (well I used to run go-ethereum on Android but it was long time ago), PIR would unlock privacy reads for the mobile devices. Also, integrating PIR would elevate (hopefully?) privacy to a default feature within the protocol, as it would become an integral part of execution clients

---

**aguzmant103** (2025-09-17):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/jflo/48/4288_2.png) jflo:

> I would much prefer to see a roadmap that could correlate these areas of focus with use cases that will get fixed, and prioritize them. As presented, ACD cannot reason about what privacy improvements these will yield, how complex they might be, or what order they should be pursued in.

Thanks jflo I think this is a good idea and we should do it (i.e. prioritize use cases and make visible where the fixes are coming). One point to clarify, for the most part, PSE will be focusing on privacy at the application layer. This means most of our work will not be on the core protocol layer.

I do expect we’ll get more involved in conversations and perhaps eventually champion EIPs that have a big impact on privacy (and callout the ones that can be risky) but as first priority it won’t be ACD (at least for now)

---

**chair28980** (2025-09-18):

There is a huge overlap between [Logos](https:/ /logos.co) and PSE’s new direction!

Logos has worked with PSE folks before on various privacy research. Hopefully this new direction makes it easy to do more together moving forward.

The work across [Waku](https:/ /waku.org), [Nomos](https:/ /nomos.tech), and [Codex](https:/ /codex.storage) aligns naturally with the privacy roadmap.

Network Privacy: Waku - privacy-preserving messaging, relay networks, and mixnet routing.

Private Computation: Nomos is building a similar vision, a zk-proof blockchain with privacy baked in.

Data Storage: Codex handles the decentralized storage layer; credentials, revocation frameworks, and data provenance.

There are a plethora of RFC’s to peruse via the VAC research unit [VAC RFCs](https:/ /rfc.vac.dev/).

(New poster, I can’t post links ![:sweat_smile:](https://ethereum-magicians.org/images/emoji/twitter/sweat_smile.png?v=12))

---

**GANGA** (2025-09-18):

Could you please involve me in your research as n also pursuing PhD and with the same field .

---

**latentmanifold** (2025-09-18):

I’d like to work on client side proving, but I’ve only written groth16 and plonk on arkworks till now. How much experienced people are you guys looking to collaborate with?

---

**Ivshti** (2025-09-19):

Sounds good!

Worth noting that some points have big overlap with both account abstraction and interoperability:

- abstracting gas payments is critical: there are multiple cases in the current flows where this is important, such as the fact that we easily leak data by funding empty accounts with ETH
- interop/balance consolidation: there’s a lot of overlap here, as a main prerequisite of making a truly private wallet usable will be being able to consolidate balances from multiple actual on-chain accounts into one “virtual” account for the user; a lot of the logic here can be thought of an extension of both interop/intent and AA work
- privacy in account recovery: zk proofs or even “opaque” signature mechanisms like Schnorr multisigs allow concealing the social recovery signers, or even concealing the email address in case of DKIM-based recovery, which is critical for the perception and adoption of those recovery mechanisms

---

**maxsiz** (2025-09-20):

Thank you for this topic. Because it really hard to observe all movements in Ethereum Ecosystem despite our( Envelop team) long term experience. So just to clarify myself. Am i right that:

> If you’re building privacy, we want to work with you

1. This post should be consider as PSE team roadmap recap and invitation as well ? Because i guess that some your initiatives definitely has intersection with our team current work. And on one hand  we want to help in your movement with our skills/tech/code but on other hand of course to not bring mess  ))

> One point to clarify, for the most part, PSE will be focusing on privacy at the application layer.

1. does the term ‘application layer’ here cover smart contracts (1) as well as client-side dApps making RPC calls (2) ?

---

**vbuterin** (2025-09-22):

> Since running local nodes is almost impossible on mobile devices

I actually think that in the not too far future this will stop being true!

The two key technologies are (i) [block-level access lists](https://ethereum-magicians.org/t/eip-7928-block-level-access-lists/23337), and (ii) ZK-EVMs. With these two things, a node will be able to have full confidence in the correctness of the chain, and track state updates, without needing to do any local EVM computation, and without needing to store any auxiliary data (eg. intermediate tree nodes) other than the state itself. That means that even today you would be able to have a minimal fully state-tracking node in under 100 GB (!!)

Once the state increases further, you can do partial-state nodes. The great majority of Ethereum’s state [is garbage](https://x.com/ngweihan_eth/status/1968583066391040384), and so we could find ways to filter it out. Alternatively, there is a decade-old trick from Bitcoin land: design the wallet so it only issues addresses that start with some hex character (eg. `0x5...`), so you trade off between a smaller anonymity set and only needing to track 1/16 of the state. The other benefit of this design is that you get reduced bandwidth reqs because you only need to download part of the BAL (if the BAL is designed correctly: in sorted order by address)

So we have two promising paths toward better privacy of reads. And they are combinable! Eg. a partial state node for the 4 GB of state you are most likely to access + eat the inefficiencies of PIR for everything else

---

**aguzmant103** (2025-09-22):

Agreed very promising approaches. Are there specific targets on disk, network, RAM you think we should target for mobile devices?

e.g. I can see 4GB of state still too big for mobile devices to download and keep track of, but perhaps if we shoot for 1y-2y for 1G it might not be terrible in future mobile.

As a part of integrating these technologies with private reads, I agree it makes sense to map them out too.

---

**aguzmant103** (2025-09-22):

> This post should be consider as PSE team roadmap recap and invitation as well ?

Yes ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) it’s hard for us to work everywhere but we can def want to start open working groups to push some of this topics together with broader ecosystem. Se def would love to chat.

> does the term ‘application layer’ here cover smart contracts (1) as well as client-side dApps making RPC calls (2) ?

Yes. Where it’s a bit trickier for PSE to work currently is directly at the protocol layer (changing client’s and core dev’s work or roadmaps) from a bandwidth perspectives, and/or L2s solutions. But we’re trying to keep track and support where we can.

---

**aguzmant103** (2025-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/latentmanifold/48/16012_2.png) latentmanifold:

> I’d like to work on client side proving, but I’ve only written groth16 and plonk on arkworks till now. How much experienced people are you guys looking to collaborate with?

Agreed! I’m DM’ing you

---

**aguzmant103** (2025-09-22):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ivshti/48/6010_2.png) Ivshti:

> Worth noting that some points have big overlap with both account abstraction and interoperability

Yes for sure!

> abstracting gas payments is critical:

Do you see any solutions covering this? I can only think of experimentation we’ve done with 4337 Semaphore paymasters [[1](https://github.com/semaphore-paymaster/semaphore-paymaster)] [[2](https://github.com/saleel/semaphore-wallet)] but can imagine others approaching differnely.

> interop/balance consolidation:

Yes, i have less thoughts here on how to approach it besides how current different privacy protcols approach it (aggregating notes or split balances). But def should be baked on privacy wallets.

> privacy in account recovery:

This is something PSE can make a dent of. Someone will be working on an n o m zk recovery mechanism so that we can plug various zk protocols (VC identity, zk EAS, semaphore, zkPassport, zkEmail, etc…) and just prove ownership with a private combination of these.

Still many details but would love to jam on it

---

**latentmanifold** (2025-09-23):

Not sure if there’s dm here. My twitter handle is: [@latentmanifold](/u/latentmanifold)  Would love to talk

---

**Ivshti** (2025-09-23):

So far almost all solutions for gas abstraction I can think of are centralized. The closest to a censorship resistant solution are pure onchain erc4337 erc20 paymasters, but I am not familiar with any good implementations but I’m sure I’ve seen some efforts. The tradeoff is that there’s no cross-chain capability, and they add considerable overhead, and potentially depend on oracles even though that can be circumvented through uniswap TWAPs.

---

**aguzmant103** (2025-09-24):

Thanks! It sounds like a worth problem worth exploring. If you have any pointers, info or people to chat happy to. I guess want to understand the problem and state of solution space to see if some more people from PSE can start looking into this


*(11 more replies not shown)*
