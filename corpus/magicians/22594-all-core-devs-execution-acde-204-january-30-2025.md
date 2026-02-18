---
source: magicians
topic_id: 22594
title: All Core Devs - Execution (ACDE) #204, January 30, 2025
author: abcoathup
date: "2025-01-20"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-204-january-30-2025/22594
views: 307
likes: 4
posts_count: 3
---

# All Core Devs - Execution (ACDE) #204, January 30, 2025

#### Agenda

[Execution Layer Meeting 204 · Issue #1253 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1253) moderated by [@timbeiko](/u/timbeiko)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/timbeiko/48/1452_2.png)

      [All Core Devs - Execution (ACDE) #204, January 30, 2025](https://ethereum-magicians.org/t/all-core-devs-execution-acde-204-january-30-2025/22594/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> TL;DR
>
> Geth users should update their nodes ASAP, see the latest security release
> Client teams should share devnet-6 ready branches with EthPandaOps
> Tentative timeline:
>
> devnet-6 stable by ACDC#150 next week
> Feb 6: if devnet-6 stable, pick testnet fork slots for Holesky and Sepolia on ACDC#150
> Feb 10: client releases out with Holesky and Sepolia configurations
> Feb 20: if Holesky has forked without issues, pick mainnet fork slot
>
> Don’t want to pick a mainnet time slot earlier to avoid creating mi…

#### Recording

  [![image](https://img.youtube.com/vi/JW2IWwVKRec/maxresdefault.jpg)](https://www.youtube.com/watch?v=JW2IWwVKRec&t=192s)

#### Additional Info

- Pectra-devnet-5
- Provide your feedback for Pectra Retrospective
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim
- Highlights of Ethereum's All Core Devs Meeting (ACDE) #204 by @yashkamalchaturvedi

## Replies

**timbeiko** (2025-01-30):

# TL;DR

- Geth users should update their nodes ASAP, see the latest security release
- Client teams should share devnet-6 ready branches with EthPandaOps
- Tentative timeline:

devnet-6 stable by ACDC#150 next week
- Feb 6: if devnet-6 stable, pick testnet fork slots for Holesky and Sepolia on ACDC#150
- Feb 10: client releases out with Holesky and Sepolia configurations
- Feb 20: if Holesky has forked without issues, pick mainnet fork slot

Don’t want to pick a mainnet time slot earlier to avoid creating misleading expectations

Audit reports for the Pectra System Contracts are available [here](https://github.com/ethereum/audits/tree/master/Pectra)

- Thank you to all auditors for accommodating our quick timelines and for pro-bono & discounted work  !

Fusaka’s first fork devnet should only include EOF and PeerDAS. There were many discussions about roadmap planning, but no decision beyond that. Teams should share their views in the [Pectra Retrospective](https://ethereum-magicians.org/t/pectra-retrospective/22637) thread.
Discussions about [Node Hardware and Bandwidth requirements](https://github.com/ethereum/EIPs/pull/9270), [EIP-7823](https://eips.ethereum.org/EIPS/eip-7823) and an upcoming ACD bot
[First RPC standardization call next week](https://github.com/ethereum/pm/issues/1261)

# Call Summary

## Pectra devnets

- devnet-5 is finalizing again!

Nethermind had a BLS-related issue which is now fixed
- Geth has issued an urgent security update. Users should update ASAP, but the issue is unrelated to Pectra.

[devnet-6](https://notes.ethereum.org/@ethpandaops/pectra-devnet-6) will launch once enough teams pass hive tests

## Pectra Timelines

- Teams want to see devnet-6 run smoothly prior to picking testnet fork slots
- Once enough teams are passing hive tests, we’ll launch devnet-6, hopefully with all teams running smoothly by next week’s ACDC
- Assuming no issues, we’ll pick testnet fork blocks then. Teams are expected to put out a release by the Monday following ACDC, with the testnet fork announcement going out in the ~24h following.
- If the holesky testnet fork goes smoothly, we’ll pick a mainnet fork slot on the next ACD
- Don’t want to pre-commit to a tentative mainnet fork slot to avoid creating misleading expectations in the community.

## System Contract Audits

- The Pectra system contracts for EIPs 2935, 7002 and 7251 were audited by four firms and formally reviewed. Auditors presented their findings on the call, and the full reports can be found here:

Blackthorn
- Dedaub

EIP-2935
- EIP-7002
- EIP-7251

[Plainshift](https://github.com/ethereum/audits/blob/master/Pectra/Plainshift%20EF%20Pectra%20Audit.pdf)
[SigmaPrime](https://github.com/ethereum/audits/blob/master/Pectra/Sigma_Prime_Ethereum_Foundation_Pectra_System_Contracts_Bytecode.pdf)
[Halmos formal verification](https://github.com/daejunpark/sys-asm-halmos)

The main issue found by auditors relates to the fee update mechanism for the contracts and is described at length in [Dedaub’s presentation](https://docs.google.com/presentation/d/1TXaJU6FipMs6NGT8_Zc7bxHUNZWnk-xsc9MK45zyGjk/edit#slide=id.g329f87299bc_0_40).

## System Contract Addresses

- We agreed to update the Pectra EIP system contract addresses to values which match the following pattern: 0x0000...00

EIP-7251 PR
- EIP-7002 PR
- EIP-2935 PR

Nice UX for contract developers, who can verify they are interacting with the system contract corresponding to a specific EIP by looking at the address!

## Fusaka

*Note: there was a lot of back and forth during this section, with me actively engaging, so please watch the livestream for the full context.*

- A few EIPs were proposed for inclusion, prompting conversation about Fusaka planning
- There were many suggestions shared to streamline the process, including:

Finalizing the scope for Fusaka as soon as Pectra goes live, and adopting this as standard practice
- Parallelizing the development of a subsequent fork as the current one rolls out
- Being clearer about our commitments to long-term R&D efforts, either to prioritize them more explicitly or to avoid wasting time

We had previously agreed to update the process to only schedule EIPs in a hard fork that we can confidently include in the *next* devnet. For Fusaka, this implies the first fork devnet should only include EOF and PeerDAS, and be stable before more EIPs are considered.
Both EOF and PeerDAS are currently progressing on independent devnet tracks and will soon be ready to merge. We decided against scheduling a first Fusaka devnet to keep the focus on Pectra.
We didn’t make further decisions about Fusaka, to first allow teams to share their perspectives on the [Pectra Retrospective thread](https://ethereum-magicians.org/t/pectra-retrospective/22637)

##

- @kevaundray asked for feedback on the proposal, which received some pushback on the validator bandwidth numbers, mostly indicating that we should target median values in specific regions, which were closer to 25mb/s than 50mb/s
- No consensus was reached on the call, so the discussion will continue on the R&D discord

## ACD bot

- @nicocsgy has been working on a bot to automate recordings, calendar events and notes for AllCoreDevs. We were out out time, so he’ll present it on next week’s call!

---

**yashkamalchaturvedi** (2025-01-31):

Call Notes: https://etherworld.co/2025/01/30/highlights-of-ethereums-all-core-devs-meeting-acde-204/

