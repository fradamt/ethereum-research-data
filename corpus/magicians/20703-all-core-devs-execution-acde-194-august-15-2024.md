---
source: magicians
topic_id: 20703
title: All Core Devs - Execution (ACDE) #194, August 15 2024
author: abcoathup
date: "2024-08-03"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-194-august-15-2024/20703
views: 206
likes: 0
posts_count: 1
---

# All Core Devs - Execution (ACDE) #194, August 15 2024

#### Agenda

[Execution Layer Meeting 194 · Issue #1124 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/1124) moderated by [@ralexstokes](/u/ralexstokes)

#### Summary

Summary by [@ralexstokes](/u/ralexstokes) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1273790121472163841))*

- We began with Pectra

devnet-2 has gone well! A few minor outstanding issues, but clients are generally performing well
- In time for devnet-3 : target launch in 2 weeks. This devnet will build off of the devnet-2 specs with the addition of EIP-7702. 7702 specs have only been finalized recently, but most clients have a significant amount already implemented.
- Touched on EOF and agreed to consider for devnet-4, and keep devnet-3 scope as-is.
- Marius from the Geth team raised a point around the benchmarking of EIP-2537, which will need updating at some point before Pectra goes to testnet/mainnet.

Other client teams were asked to confirm the gas scheduling
- Expect a small update to this EIP into Pectra soon!

Next, [@Potuz](/u/potuz) gave an overview of EIP-7732

- A particular implementation of ePBS culminating in many years of hard work
- Highlighted no significant changes for execution clients, but did want to get on their radars
- This EIP would bring changes for builders (n.b. bids must be collateralized at the staking layer), and details of block production would interact differently with the mempool from today
- The EIP is stable in terms of specification, and proof-of-concept implementations are under way

Next, a PR to remove `totalDifficulty` from the JSON RPC standard

- https://github.com/ethereum/execution-apis/pull/570
- general thumbs up from clients, this is essentially a legacy holdover after the Merge

Then, a call for review of an update to the execution layer wire protocol: `eth/69`

- EIP-7642: eth/69 - Drop pre-merge fields
- Greatly reduces bandwidth usage; check out the EthMag thread to provide feedback

Wrapped the call with a discussion around testing PeerDAS while the rest of Pectra is still under development

- Discussed some changes to fuzzing software to avoid less stable parts of the Pectra EIP set
- Will continue PeerDAS development in parallel to Pectra and target integration at a future point in time

**REMINDER** : Going to start a weekly Pectra interop testing call next Monday 19 August at 14:00 UTC

#### Recording

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/0b8f210e32b4657cd1a9cf672d8a34ccbd8c1119.jpeg)](https://www.youtube.com/watch?v=tbxgYq8KmmM)

#### Additional info

**Notes**: [Crypto & Blockchain Research Reports | Galaxy](https://www.galaxy.com/insights/research/ethereum-all-core-developers-execution-call-194) by [@Christine_dkim](/u/christine_dkim)
