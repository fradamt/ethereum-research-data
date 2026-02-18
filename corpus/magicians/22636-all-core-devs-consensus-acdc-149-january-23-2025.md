---
source: magicians
topic_id: 22636
title: All Core Devs - Consensus (ACDC) #149, January 23, 2025
author: abcoathup
date: "2025-01-23"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-149-january-23-2025/22636
views: 225
likes: 3
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #149, January 23, 2025

#### Agenda

[Consensus-layer Call 149 · Issue #1258 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1258) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #149, January 23, 2025](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-149-january-23-2025/22636/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #149 summary
> Action Items
>
> Finish devnet-5 debugging
> Prepare for devnet-6 with latest spec changes; CL + EL specs/tests releases soon!
> Target testnet client releases 3 February. Will get EL confirmation on next ACD
> Prepare client perspectives for a Pectra retrospective to post here: Pectra Retrospective
>
> Summary
> Started the call with an update on devnet-5 status. Multiple outstanding issues, network had issues with finality; clients are busy debugging.
> Agreed to a devnet-6 with the most…

#### Recording

  [![image](https://img.youtube.com/vi/uIjPkGezPOg/maxresdefault.jpg)](https://www.youtube.com/watch?v=uIjPkGezPOg&t=188s)

#### Additional Info

- Pectra-devnet-5
- Provide your feedback for Pectra Retrospective
- Proposal for Blob-Parameter-Only (BPO) forks
- Twitter summary by @nixo
- Twitter summary and Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDC) #149 by @yashkamalchaturvedi

## Replies

**ralexstokes** (2025-01-27):

**ACDC #149 summary**

**Action Items**

- Finish devnet-5 debugging
- Prepare for devnet-6 with latest spec changes; CL + EL specs/tests releases soon!
- Target testnet client releases 3 February. Will get EL confirmation on next ACD
- Prepare client perspectives for a Pectra retrospective to post here: Pectra Retrospective

**Summary**

Started the call with an update on devnet-5 status. Multiple outstanding issues, network had issues with finality; clients are busy debugging.

Agreed to a devnet-6 with the most recent EIP-7702 change. We are going to launch devnet-6 as soon as we can pending client readiness.

Clients agreed to target testnet forks (Holesky and then Sepolia) in February to line us up for a March mainnet fork.

Next, turned to a quick update on the PeerDAS work. Progress is under way and clients should be ready for a devnet soon. Ansgar also raised the point that we should ensure PeerDAS development target the 8x scaling that are theoretically expected from the sampling design.

Then, we had an announcement for a concept of a “blob parameter only” fork: [Blob-Parameter-Only (BPO) forks](https://ethereum-magicians.org/t/blob-parameter-only-bpo-forks/22623). The idea is to create a specific track for increasing blob throughput in ACD aside from other hard fork concerns. There was interest in this approach, although Terence did point out that due to external concerns like timing games with PBS it may not be as simple as just raising constants in the protocol on a regular schedule (as more invasive changes would take more R&D effort). We also touched on the idea to put the blob limit under the control of validators like the gas limit today. There were a number of open questions around doing this in a way that doesn’t put undue load on validators but there was a healthy amount of interest from client teams.

Next, Tim asked if we want to do a Pectra retrospective as a way to figure out how to improve the ACD process and hard fork planning. Many on the call were interested. Please provide input here: [Pectra Retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637).

