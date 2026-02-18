---
source: magicians
topic_id: 21793
title: All Core Devs - Consensus (ACDC) #146, November 28 2024
author: abcoathup
date: "2024-11-23"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-146-november-28-2024/21793
views: 286
likes: 4
posts_count: 2
---

# All Core Devs - Consensus (ACDC) #146, November 28 2024

#### Agenda

[Consensus-layer Call 146 · Issue #1200 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1200) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/ralexstokes/48/10556_2.png)

      [All Core Devs - Consensus (ACDC) #146, November 28 2024](https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-146-november-28-2024/21793/2) [Protocol Calls & happenings](/c/protocol-calls/63)




> ACDC #146 summary
> Action Items
>
> Merge engine: exclude empty requests in requests list by fjl · Pull Request #599 · ethereum/execution-apis · GitHub ASAP
> Finalize update to EIP-7691: Update EIP-7691: add update fraction specification by adietrichs · Pull Request #9060 · ethereum/EIPs · GitHub
> Merge eip7251: Do not change creds type on consolidation by mkalinin · Pull Request #4020 · ethereum/consensus-specs · GitHub ASAP for devnet-5
> Check this post for some ACD process improvement suggestions …

#### Recording

  [![image](https://img.youtube.com/vi/HcjuY3WDa9A/maxresdefault.jpg)](https://www.youtube.com/watch?v=HcjuY3WDa9A&t=271s)

#### Additional Info

- ethPandaOps:

Understanding the Ethereum network limits using devnets | ethPandaOps
- Block Arrivals, Home Stakers & Bumping the blob count - Sharding - Ethereum Research

EIP7805 FOCIL:

- FOCIL - Google Präsentationen
- meetfocil.eth.limo
- Crypto & Blockchain Research Reports | Galaxy by @Christine_dkim

## Replies

**ralexstokes** (2024-11-29):

**ACDC #146 summary**

**Action Items**

- Merge engine: exclude empty requests in requests list by fjl · Pull Request #599 · ethereum/execution-apis · GitHub ASAP
- Finalize update to EIP-7691: Update EIP-7691: add update fraction specification by adietrichs · Pull Request #9060 · ethereum/EIPs · GitHub
- Merge eip7251: Do not change creds type on consolidation by mkalinin · Pull Request #4020 · ethereum/consensus-specs · GitHub ASAP for devnet-5
- Check this post for some ACD process improvement suggestions for next week: AllCoreDevs, Network Upgrade & EthMagicians Process Improvements - #51 by timbeiko

**Summary**

Mainly focused on finalizing the Pectra specs this call, and got an overview of a new EIP presenting FOCIL, a new design for inclusion lists.

- First started by reviewing a deposit processing bug this week on Mekong
- Finality on Mekong has been restored and clients have either resolved bugs or are close to fixing.
- Next, turned to the devnet-5 spec:
- Covered an update to EIP-7685 that was still open and not yet merged.

Agreed to merge #599

Next, turned to updates around EIP-7742

- Started with EIP-7742 updates for fee normalization, and conversation shifted to a number of blob market updates. Check the call for the full color!
- Agreed to go with a simpler solution to reflect a higher blob count by updating the base fee “update denominator”, rather than going with fee normalization in Pectra

Following the blob fee market updates, we turned to a blob throughput increase in Pectra

- EIP-7691 proposes moving to a target of 6 and a max of 9
- ethpandaops presented some analysis supporting (6, 9) is safe for mainnet

Block Arrivals, Home Stakers & Bumping the blob count - Sharding - Ethereum Research

Agreed to move ahead with EIP-7691, with continued analysis to ensure these parameters are safe for mainnet.

And to round out the set of blob updates, we raised the question of EIP-7623 to cap block+blob sizes in the worst case

- There was strong support for 7623, along with some opposition.
- Decided to bring to next week’s ACDE to allow EL client teams a chance to weigh in.

After the blobs, we rounded out Pectra with PR to update the consolidation mechanics under EIP-7251

- eip7251: Do not change creds type on consolidation by mkalinin · Pull Request #4020 · ethereum/consensus-specs · GitHub
- This PR handles an edge case where currently anyone can set a validator to a “compounding” regime without authorization; it also simplifies the state transition.
- Still needs tests, but agreed to merge into Pectra

Touched briefly on PeerDAS; devnets are waiting on Pectra to stabilize before proceeding further.
After Pectra, we had a presentation giving an overview of FOCIL, a new inclusion list design.

- ACDC #146 EIP-7805 FOCIL presentation - Google Slides
- EIP-7805: Fork-choice enforced Inclusion Lists (FOCIL)
- And a nice website to showcase the R&D: https://meetfocil.eth.limo/

