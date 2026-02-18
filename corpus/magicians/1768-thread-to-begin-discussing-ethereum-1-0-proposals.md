---
source: magicians
topic_id: 1768
title: Thread to begin discussing "Ethereum 1.0" proposals
author: jpitts
date: "2018-11-01"
category: Working Groups > Ethereum 1.x Ring
tags: [eth1x, ethereum-roadmap]
url: https://ethereum-magicians.org/t/thread-to-begin-discussing-ethereum-1-0-proposals/1768
views: 5084
likes: 23
posts_count: 23
---

# Thread to begin discussing "Ethereum 1.0" proposals

In light of the amazing conversation that the community had around the subject of Ethereum 2.0 and its roadmap, I would like to propose a Ring / category for the current improvement proposals across clients on mainnet e.g. Ethereum 1.0.

Are there folks who would collect around such a ring? Probably there are quite a few!

## Replies

**jpitts** (2018-11-01):

And in a way All Core Devs is the original ring around this, so this would be a category here on the forum where those who normally would be on All Core Dev calls and other stakeholders would discuss EIPs.

---

**fubuloubu** (2018-11-02):

The Security Ring ([#working-groups:security](/c/working-groups/security/14)) is talking about some of the execution layer plans for the near and far term, including the transition to eWASM.

Further information here:

[Ethereum Backend Discussion](https://ethereum-magicians.org/t/ethereum-backend-discussion/1775)

---

**bobsummerwill** (2018-11-02):

Yes, there is a very real need for this!

---

**latrasis** (2018-11-04):

Hi Bob! Do you think anyone be interested to read on a proposed security protocol? [Current whitepaper](https://beakeros.org/docs/Whitepaper.pdf)

---

**jpitts** (2018-11-13):

[@latrasis](/u/latrasis), this message probably belongs in a DM to Bob!

---

**jpitts** (2018-11-13):

According to the tweet by Ben Edgington entitled “[Get your Ethereum 2.0 fix here](https://twitter.com/benjaminion_xyz/status/1062096142601801728)”:

- Proposals to evolve Ethereum 1.0 are being grouped under the name “Ethereum 1.x”.
- There are working groups forming! Er, where?

Reducing state size growth
- Implementing eWASM in some form
- Benchmarking framework for evaluating performance proposals

EIPs / proposals out be the end of this month? *WOW*

From the Google Doc “[What’s New In Eth2](https://docs.google.com/document/d/1oMi-0ZbCD5SdBtMxtHC5gaiflX8MnXGF1_Nk-_gGIUI/edit)”:

[![image](https://ethereum-magicians.org/uploads/default/optimized/2X/b/b08f7f762c20f4f45d80a934bbf822188205dd2a_2_690x396.png)image1262×726 61.6 KB](https://ethereum-magicians.org/uploads/default/b08f7f762c20f4f45d80a934bbf822188205dd2a)

---

**boris** (2018-11-13):

Thanks for continuing to curate this, [@jpitts](/u/jpitts). I also wonder where / how one gets involved with working groups. Would be good to list them and have a repo or channel or somewhere where people can knock on the door to find out more and get involved.

I’ve started on drawing diagrams of the Ethereum system – decomposing the entire Ethereum client and some of its specifications.

See [Ethereum System Diagrams - Google Präsentationen](https://docs.google.com/presentation/d/1UDW1KsNc5w8xaFLWaisn_ZFqWcflZHWs-_FUpDq_2kk/edit#slide=id.p)

Relevant for this thread is one suggestion that could get us not to eWASM, but rather to an LLVM integration that means we can support the end goal of eWASM much more quickly, AND not have to throw out or migrate existing smart contract code. It would be forward compatible.

[![Ethereum%20System%20Diagrams](https://ethereum-magicians.org/uploads/default/optimized/2X/6/61b4ed5c8c5344ef26dbaacf92d22af882843959_2_690x388.png)Ethereum%20System%20Diagrams960×540 44 KB](https://ethereum-magicians.org/uploads/default/61b4ed5c8c5344ef26dbaacf92d22af882843959)

[@lrettig](/u/lrettig) where’s the best place to have this LLVM discussion?

[@fubuloubu](/u/fubuloubu) wasn’t it someone from Trail of Bits who had started work on this? Can you connect us?

---

**fubuloubu** (2018-11-13):

cc [@dguido](/u/dguido)

I believe it was more a chat and general agreement on an LLVM backend that produces EVM code being a great approach for the medium term.

Personally, I’d love to move that chart such that Vyper can use LLVM for optimization stages.

---

Edit: P.S. was gathering a working group on this…

---

**boris** (2018-11-13):

Yeah, I was trying to draw it as current state. LLVM is good at optimization so would just mean writing an LLVM backend for Vyper rather than doing the work of creating the bytecode, I think?

Maybe we should put it on the agenda for the [EVM Evolution community call](https://github.com/spadebuilders/community/issues/14)? I’ll link back to this here from the call agenda and we’ll cover it if there is interest.

---

**fubuloubu** (2018-11-13):

Maybe. I was considering it separately, including in the same chat as Yul, LLL, and all the other IRs that exist out there. Defining the optimization and security goals of the IR, best path(s) to get there, what the tradeoffs are, etc.

EVM stuff is one layer lower, so that was going to be a separate discussion as I had planned.

---

**boris** (2018-11-13):

OK. I kind of think they are all inter-related, and not talking across layers is one of the issues in the first place. MOAR DISCUSSION.

(also doing!)

---

**fubuloubu** (2018-11-13):

I know, it’s more of a practical thing. There’s already like 10 plus in each discussion. A lot of people in security community are interested in being included in this discussions, as they should.

---

**fubuloubu** (2018-11-13):

P.S. [@karalabe](/u/karalabe) I think is involved in the state and block growth discussions?

---

**dguido** (2018-11-13):

Hey Boris,

Yes, we have a detailed plan to implement a system similar to what you describe. We have worked on many compilers before, and about 1/3 of our company works on LLVM daily.

I think the best approach would be a purpose-built machine-level IR for optimal EVM generation, let’s call it “EIR” for Ethereum IR. We have a high level spec for what this IR would look like, and it would enable us to create an efficient backend for EVM. It would include gas cost information and low-level memory layout information.

I think it is just as important to consider building a frontend for Solidity, Vyper, or other languages in LLVM. Similar to Swift, we would probably want a high-level IR (not YUL) before handing it off to the rest of LLVM. For example, it would include accurate types, a CFG, and be in SSA form. Let’s call this one SOLIR for “Solidity IR.”

We have rapidly prototyped an IR that meets the frontend specifications we need inside Slither, an Ethereum static analyzer. It is still evolving and lacks, for instance, SSA but given a few more weeks of work it would be an acceptable IR to ease and enhance integration of Solidity, Vyper, and other languages into a modern compiler like LLVM. You can find details about it here: https://github.com/trailofbits/slither/wiki/SlithIR. You’ll note we already have working code and it correctly translates all Solidity available on Etherscan. Adding support for translating Vyper or LLL to this IR would only be a ~2-4 week process.

We have specs for our entire approach (frontend and backend) and want to begin working on it, however, we received no response after submitting a proposal to the Ethereum Foundation and, therefore, expect that our proposal for compiler development is no longer under consideration. We would still like to pursue this project because we think it’s the most important need for the Ethereum community to mature its software development process.

Let me know if you’d like to chat elsewhere. I can be reached at [dan@trailofbits.com](mailto:dan@trailofbits.com).

-Dan

---

**boris** (2018-11-13):

Hey Dan – this sounds great. I’ll send you a note by email. I think there are a number of people who believe in an LLVM approach. So there is a mix of rallying people around this as a direction, coordinating on moving forward, and getting grants / funding / sponsorship to do the work.

Our broad label for related work is EVM Evolution, and outside that, this ETH 1.x roadmap (which really is more like – let’s keep shipping new stuff iteratively) is how we move forward.

---

**jpitts** (2018-11-14):

How did you submit this to the Ethereum Foundation? It is the client developers, tool makers, and the the wider community to decide on a proposal like this.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/dguido/48/342_2.png) dguido:

> We have specs for our entire approach (frontend and backend) and want to begin working on it, however, we received no response after submitting a proposal to the Ethereum Foundation and, therefore, expect that our proposal for compiler development is no longer under consideration. We would still like to pursue this project because we think it’s the most important need for the Ethereum community to mature its software development process.

---

**boris** (2018-11-14):

I think he meant a grant proposal.

But yes – [@dguido](/u/dguido) the Ethereum Foundation doesn’t decide technical direction of the ecosystem. “We” get to work together and build what we find is valuable.

---

**jpitts** (2018-11-14):

I see, this is a very interesting proposal and nudges me to learn more about compiler details and LLVM!

---

**gcolvin** (2018-11-19):

[@dguido](/u/dguido) This is, of course, very interesting to me.  Can you post a link to the grant proposal?

---

**jpitts** (2018-11-23):

A group of individuals has been meeting to discuss “Ethereum 1.0”. This group may be seen as All Core Devs, but its composition seems to be not fully representative and includes other stakeholders not generally associated with All Core Devs. For now, I will call this particular initiative “Ethereum 1.x”.

The existence of this group has been known to a number of people in the community who chose not to participate (I will soon write up details in a disclosure). Ethereum 1.x now has been more or less officially confirmed by participants on today’s [All Core Devs call #50](https://www.youtube.com/watch?v=wfxvCEhglTM).

Unofficial “leaked” notes from the Ethereum 1.x proceedings:



      [docs.google.com](https://docs.google.com/document/d/1IB3oKuH5mryyhmVHE9r3aR6bK2pJCoJgAtiCYTEieh4/edit)



    https://docs.google.com/document/d/1IB3oKuH5mryyhmVHE9r3aR6bK2pJCoJgAtiCYTEieh4/edit

###

Notes: DevCon Eth 1.x and 2.0 Meetings  Hey all, here are Dan Heyman'snotes from the meetings over the last week. I know I missed bits so please feel free to add. Also, I definitely missed people in the attendee lists. Not everyone made it onto the...










CoinDesk article by [@rachel-rose](/u/rachel-rose):

https://www.coindesk.com/ethereum-developers-are-quietly-planning-an-accelerated-tech-roadmap


*(2 more replies not shown)*
