---
source: magicians
topic_id: 19634
title: "EIP-7732: Enshrined Proposer-Builder Separation (ePBS)"
author: potuz
date: "2024-04-12"
category: EIPs > EIPs core
tags: [epbs]
url: https://ethereum-magicians.org/t/eip-7732-enshrined-proposer-builder-separation-epbs/19634
views: 2258
likes: 7
posts_count: 4
---

# EIP-7732: Enshrined Proposer-Builder Separation (ePBS)

Creating a topic for discussions EIP-7732


      ![](https://eips.ethereum.org/assets/images/favicon.png)

      [Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-7732)





###



Separates the ethereum block in consensus and execution parts, adds a mechanism for the consensus proposer to choose the execution proposer.










Full design notes are included  in this document:


      ![](https://ethereum-magicians.org/uploads/default/original/2X/8/8f0a562a90992dd656ced3f9b9b37c942cfbde54.png)

      [HackMD](https://hackmd.io/@potuz/rJ9GCnT1C)



    ![](https://ethereum-magicians.org/uploads/default/optimized/2X/6/62d6a99d68e97088bdf157a582a55d8b5cccb38b_2_690x394.jpeg)

###



Fully detailed specification notes for a minimal implementation of ePBS










The Python full specification is included in



      [github.com/ethereum/consensus-specs](https://github.com/ethereum/consensus-specs/pull/3828)














####


      `dev` ← `potuz:epbs_cl_repo`




          opened 12:12PM - 02 Jul 24 UTC



          [![](https://avatars.githubusercontent.com/u/16044918?v=4)
            potuz](https://github.com/potuz)



          [+2111
            -13](https://github.com/ethereum/consensus-specs/pull/3828/files)







This PR implements the necessary changes to separate the processing of an Ethere[…](https://github.com/ethereum/consensus-specs/pull/3828)um block into a consensus and an execution part. It also implements an auction mechanism for a consensus proposer to choose the proposer of the execution part of the block (called a *builder* in the documentation).

The full design notes are included in https://hackmd.io/@potuz/rJ9GCnT1C
Forkchoice annotated spec can be found in https://hackmd.io/@potuz/SJdXM43x0
Validator guide annotated spec can be found in https://hackmd.io/@ttsao/epbs-annotated-validator

## Replies

**gorondan** (2024-04-13):

Great to see ePBS kick off👏, we’re following the topic with great interest, over at the EPFsg.

some questions on design:

- was the urge to “fix the bug” the reason you’re proposing block auction ePBS? Because there are debates on the fact that we’re just going to move MEVboost market structure (that is considered the bug, right?), in-protocol.
- is your envisioned pipeline something like ePBS->slot auctions->ET?

Thank you

---

**potuz** (2024-04-13):

The current bug is the existence of a forced trusted player in an otherwise trustless blockchain. As the document states, we aim to solve this issue in a minimal viable way. Other designs like slot auctions and/or execution ticket may be better, but I at least do not know how to actually implement them. As you delve into the minutiae of actually writing the python spec you’ll see that there are many edge cases that need to be considered. The current spec still has many of those. It seems to me that both slot auctions and execution tickets can be an iteration from ePBS and actually are simpler to specify once ePBS is in place, so given the urgency prompted by the problems we are seeing right now on mainnet is that I want to deploy a bug fix and focus on theoretical design in parallel/future.

---

**u59149403** (2025-04-24):

So this EIP makes life of MEV extractors simpler? So people performing sandwich attacks will have easier life? Now they don’t need to trust middleman and so can steal money from honest users even simpler? And this EIP democratizes MEV extraction, so now even home stackers can extract MEV, perform sandwich attacks and steal money from Ethereum users? In trustless way? Cool! I like this proposal! Thank you for thinking about these poor sandwich attackers. (This is sarcasm.)

