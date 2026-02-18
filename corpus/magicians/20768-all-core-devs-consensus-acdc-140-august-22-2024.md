---
source: magicians
topic_id: 20768
title: All Core Devs - Consensus (ACDC) #140, August 22 2024
author: abcoathup
date: "2024-08-10"
category: Protocol Calls & happenings
tags: [acd, acdc]
url: https://ethereum-magicians.org/t/all-core-devs-consensus-acdc-140-august-22-2024/20768
views: 494
likes: 2
posts_count: 1
---

# All Core Devs - Consensus (ACDC) #140, August 22 2024

#### Agenda

[Consensus-layer Call 140 · Issue #1129 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1129) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary

Summary by [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1276248466015785073))*

- consensus-specs release v1.5.0-alpha.5 is out!
- Pectra devnets

Started with an overview of devnet-2

A bad block, likely from early EIP-7702 implementation; clients are debugging

Minor issue with JSON-RPC, see the call for more details
Touched on an update to EIP-2935; no substantive change, just a clarification around behavior
And it looks like we are in a good place for `devnet-3` — be on the lookout for launch next week!

Pectra EIP updates

- Update to EIP-7251 to adjust correlated slashing penalty; fixes an overflow at high amounts of stake

Please take a look! The change is straightforward but touches some very delicate code.

Next, [a proposal](https://github.com/ethereum/consensus-specs/pull/3875) to refactor some of the data types on the beacon chain to streamline processing of execution requests added in Electra

- General support for this solution
- Blocked on adding spec tests; I’ll follow up here

Then [another proposal](https://github.com/ethereum/execution-apis/pull/565) to refactor the engine API to streamline implementation when passing execution requests from EL to CL

- Proposal has some support, although there was a question about the interplay with the possible move to SSZ if we decide to harmonize serialization across the CL and EL
- Going to get more feedback from additional CL clients

PeerDAS

- Started with implementation updates and client status

Clients have made progress on implementing the peerdas-devnet-2 specs, and devnet launch should be in the next few days!

Next, turned to EIP-7742

- Started with some clarifications, engine API payload attributes needs the maximum blob count as well as the target as currently specified
- Did a temperature check on Pectra inclusion, generally good support

And then touched on an implementation concern around blob flexibility

- Some clients hard-code the max and target blob parameters, which can make operations of devnets harder
- Clients are aware of the issue and will likely solve this pain point under EIP-7742

This segued into a discussion around blob limits per transaction in the protocol, and how that interacts with similar concerns in the public mempool

- want to make blob packing easier; if a transaction has the max number of blobs, it crowds out other transactions that could otherwise go into the same block
- strong pushback to not have a protocol-level rule and instead handle in the mempool or networking layer
- some nice back-and-forth on this point, check the call for the details!

And to close the call:

- Agreed to label the F-star (next hard fork after Pectra): Fulu, with portmanteau Fusaka
- And last but not least, an update from Probelab around some recent analysis of gossipsub and its control messages

Find slides on IPFS with this CID: QmURBPigXY9LjGuumwRohrXfhhi26RZmWHKQT2RjcUEQAy
- A related analysis on block arrival times here: https://probelab.io/ethereum/block_arrival/2024-29/

#### Recording

  [![image](https://img.youtube.com/vi/hSNJ6vURfmE/maxresdefault.jpg)](https://www.youtube.com/watch?v=hSNJ6vURfmE&t=112s)

#### Additional info

**Notes**: [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-consensus-call-140/) by [@Christine_dkim](/u/christine_dkim)
