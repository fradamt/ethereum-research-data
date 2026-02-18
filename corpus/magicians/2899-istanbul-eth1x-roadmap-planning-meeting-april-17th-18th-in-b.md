---
source: magicians
topic_id: 2899
title: Istanbul & ETH1x Roadmap Planning Meeting - April 17th & 18th in Berlin
author: boris
date: "2019-03-11"
category: Working Groups > Ethereum 1.x Ring
tags: [istanbul, berlin, meeting]
url: https://ethereum-magicians.org/t/istanbul-eth1x-roadmap-planning-meeting-april-17th-18th-in-berlin/2899
views: 5909
likes: 30
posts_count: 36
---

# Istanbul & ETH1x Roadmap Planning Meeting - April 17th & 18th in Berlin

The discussion that [started in January](https://ethereum-magicians.org/t/eth1x-istanbul-prep-meeting/2396) has resulted in a meeting being planned for April 17th & 18th in Berlin.

The dates are *confirmed* so please feel free to book travel. There may be a reception on the evening of the 16th or other shoulder events, but nothing else is confirmed.

The goals are:

- discuss process & timing of Istanbul hardfork – EIP233 improvements, security, testing
- discuss various multi-hardfork plans such as state fees, eWASM, EVM evolution
- presentations from technical experts & EIP proposers for Istanbul
- client implementation scheduling and concerns

This is a technical meeting for CoreDevs, ETH1 client developers, EIP proposers, and other technical experts.

Aside from being there in person, we will be setup to include some remote presenters.

Presentations will be captured / livestreamed but not break out sessions. Will post notes after the fact, and run an AMA afterwards similar to the [Feb 6th Webinar](https://ethereum-magicians.org/t/eth-roadmap-ama-webinar-feb-6th-8am-pst-1700-utc-1/2518).

---

Anyone doing technical work as described above is welcome to attend. Please let us know that you’re coming to plan for space and topics.

**Signup form:** https://goo.gl/forms/AZv018Cgd2B3YzuZ2

---

## Schedule

The two day schedule is here: https://docs.google.com/spreadsheets/d/e/2PACX-1vSZ8umEwLjA6pncgm1BQ5tkRb4Lw97LzyFvOx9zJZyE0z0yNIlY9dsVJ7_hogRq-6svKubFkELeXzHu/pubhtml?gid=977790192#

All times in Central Europe Time (Berlin).

---

*Topics will be updated with links to presentations / livestream as they become available*

## Topics

This is an initial list of topics and presenters.

Presentations being made in order:

## April 17th Wednesday Day 1

- State Rent - @AlexeyAkhunov - https://drive.google.com/open?id=1u7d-jLMdGkPYl0zf49b1CFKtqlln4ICO
- EVM Evolution - @expede

EIP 615 Static Jumps and Subroutines - @expede @gcolvin (part of EVM Evolution discussion)
- Brooke’s presentation https://drive.google.com/open?id=1_taRpfsEF-ofF0UpwKyGOH-ogPqxmpUD

EVM Invariants

- EIP 1712 - Disallow deployment of unused opcodes - Immutability/invariant - @sorpaas

Consenus Testing - Dmitry cover’s Retesteth https://drive.google.com/open?id=1w_I_9ny1c5bPEavBfy2QLk0OPOzGrM0q

Security Review - [@tintinweb](/u/tintinweb) - https://drive.google.com/open?id=1EiIw2LIw2e98nLaR0VU94PJrpBj-ABo_

Large Scale System Testing - Zack Cole, White Block https://drive.google.com/open?id=1lrfJ-Z4lscnLHbUae11uPn8QaUpQjdH2

ETHv64 - Matt Halpern - https://drive.google.com/open?id=1-TuInhKVAbLs0s5L-Bk1e0x3aXlCYW2R

Red Queen Sync - sidebar discussion

## Day 2

- eWASM - @axic @lrettig
- Precompiles - meta discussion on including more pre-compiles for crypto primitives and ETH2 support - @axic for eWASM view, @expede @Recmo  for “native” precompiles
- EIP Process Improvements: EIP233 - @boris @axic @lrettig
- Technical Mainnet HF Process - @decanus
- Mainnet HF Comms - Lead?
- 6 or 9 month HFs, plus non HF rollouts like networking updates, JSON-RPC - @lrettig
- Networking - Hobbits wire protocol for ETH 2.0 - Antoine Toulme

### Proposed EIP Presentations

*Not confirmed to present, copy/pasta from [roadmap wiki](https://en.ethereum.wiki/edit/roadmap/istanbul)*

- EIP 1829 Precompile for Elliptic Curve Linear Combinations - @Recmo
- EIP 1057 ProgPoW, a Programmatic Proof-of-Work - @shemnon
- EIP 1559 - Fee market change - see also EthMagicians discussion - @ vbuterin

## Related Links

- Istanbul Roadmap timeline - https://en.ethereum.wiki/roadmap/istanbul
- Small vs Large Hardforks More frequent, smaller hardforks vs. less frequent, larger ones

## Event Details

When: April 17th & 18th

Where: Berlin, Germany

Venue: Full Node – thank you Martin & Gnosis team for supporting this

These are working meetings, please sign up to let us know you’re coming https://goo.gl/forms/AZv018Cgd2B3YzuZ2

The presentations will be livestreamed at the [Ethereum Foundation](https://www.youtube.com/watch?v=Au1Qll-86v0) Youtube account starting soon.

## Replies

**lrettig** (2019-03-11):

I’ll be there. You can put [@axic](/u/axic) (?) and me down for Ewasm.

---

**tvanepps** (2019-03-12):

> Security Review

Just came across this today. 25k for EIP audits, not sure any more specifics though

https://twitter.com/chain_security/status/1105146210485182465

---

**boris** (2019-03-12):

Yeah I’m wondering if that’s per EIP.

My other question is if anyone is going to champion 1283 to go in again.

---

**timbeiko** (2019-03-12):

Not sure if this is the right thread to bring this up, but on Github [@boris](/u/boris) mentioned that

> If we want to meet again, that timing should be decided soon, so that people can plan ahead.
> Depending on what the goals of the meeting are, either late July (post July 19th implementation deadline) or mid September (post Aug 14th testnet upgrade).

Are there Ethereum events already planned either mid-late July or early-mid September? If so, it may make sense to have this future meeting be in the same location & at the same time.

---

**boris** (2019-03-12):

Yes, it’s a good spot for it ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=9)

It’s been my experience so far that meetings aligned with conferences lengthen the time for everyone and are generally exhausting.

I don’t know if I’m the only one that feels that way, but I’d prefer these meetings – if we need to have them in person – should be planned to meet the needs of the meeting and the participants.

I think rotating location – i.e. not always in Europe! – should be a factor, it shouldn’t overlap a weekend (this is a job!), and probably some other guidelines.

Getting on a plane at all is costly, so who supports the cost of this travel is another question.

---

**timbeiko** (2019-03-12):

Great points! The reason why I proposed having this close to conferences is that for people who would otherwise be attending the conference for work, it is often cheaper to simply extend the trip.

I agree we should look how to support the cost of travel and rotate locations.

---

**maurelian** (2019-03-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> My other question is if anyone is going to champion 1283 to go in again.

I really like 1283, or something else that enables a cheaper mutex. But that’s quite different from championing.

---

**boris** (2019-03-14):

Chanting: [@maurelian](/u/maurelian), maurelian, maurelian, maurelian!

Original author [@sorpaas](/u/sorpaas) will be in Berlin I think, but needs to be encouraged that there are people interested in it as well as of course security reviews.

Maybe an opportunity to write the specification in K that you / Consensys Diligence could help with?

---

**maurelian** (2019-03-15):

I like all these ideas. /fires up twitter.

---

**lrettig** (2019-03-18):

One of the Ewasm folks ([@axic](/u/axic)?) could probably lead the precompiles conversation as we’ve been discussing this at great length as part of the Ewasm Eth1x plans.

Please also add me to “EIP Process Improvements” and HF schedule. Thanks.

---

**boris** (2019-03-18):

Great, added those above – it *should* be wiki editable by anyone. For reference, that precompiles discussion needs to be broader than just WASM. For the WASM plan in general, there should be a multi-hardfork schedule and some discussion of what is needed. I’m going to ping the team because [@expede](/u/expede) would like to sync up and ask some questions before Berlin so we can coordinate forward compatibility from EVM Evolution.

Re: leads – basically, just trying to get at least one or two names beside topics that need discussion / planning.

---

**lrettig** (2019-03-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/boris/48/68_2.png) boris:

> it should be wiki editable by anyone

Confirmed that it is editable. Sorry about that! And thanks for making the updates for lazy me.

---

**zscole** (2019-03-20):

I’d like to volunteer to present on testing. This will also overlap with simulation. We have some updates for the state tests that we’ve been planning with [@AlexeyAkhunov](/u/alexeyakhunov) and will have some results to share by then. We’ve also made some progress on other testing related initiatives, including some relevent work we’re doing with the EEA.

---

**boris** (2019-03-20):

Great [@zscole](/u/zscole)! Please edit to put your name next to Testing and add a line + your name to Simulation. If you haven’t already – please sign up on the google form.

---

**tvanepps** (2019-03-25):

[@vbuterin](/u/vbuterin) - [@econoar](/u/econoar) mentioned you might want to present on 1559 remotely? Is this still the case?

---

**sorpaas** (2019-03-27):

I can confirm to make it on 17th (but cannot confirm 18th), and I want to add [EIP-1712](https://github.com/ethereum/EIPs/pull/1712) to the list. It’s a relatively simple one and related to our immutability/invariant discussions. A current benefit is in inter-blockchain / private-chain setup, where it can prevent someone accidentally deploy a contract to a chain that is incompatible. This is something I’ve heard a lot of complaints of.

---

**boris** (2019-03-27):

Great, thank you. Will make sure to schedule for the 17th.

---

**AlexeyAkhunov** (2019-03-27):

Andrew Ashikhmin will make a presentation about his Red Queen Sync protocol. This is currently under State rent working group, but we might want to split it up to another working group.

I would also like to launch another working group related to the use of beacon chain as a finality gadget for Ethereum 1x

---

**boris** (2019-03-27):

Great, thanks for the update.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> I would also like to launch another working group related to the use of beacon chain as a finality gadget for Ethereum 1x

Yes there is a lot of excitement about this for sure.

---

**virgil** (2019-03-28):

I will be in Korea on those dates, but I’ll be remotely presenting on:

- EIP 152: the Blake2 precompile
- Introducing an optional process reducing the necessary labour from by our fine EIP maintainers using OASIS Open Projects.


*(15 more replies not shown)*
