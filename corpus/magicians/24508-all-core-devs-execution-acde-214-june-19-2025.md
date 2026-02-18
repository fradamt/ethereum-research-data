---
source: magicians
topic_id: 24508
title: All Core Devs - Execution (ACDE) #214 (June 19, 2025)
author: system
date: "2025-06-10"
category: Protocol Calls & happenings
tags: [acd, acde]
url: https://ethereum-magicians.org/t/all-core-devs-execution-acde-214-june-19-2025/24508
views: 336
likes: 1
posts_count: 2
---

# All Core Devs - Execution (ACDE) #214 (June 19, 2025)

- June 19, 2025, 14:00-15:30 UTC
- Ethereum Protocol Calls Calendar subscription

# Agenda

- Interop

45M Gas Limit Increase
- berlinterop-devnet-2

Fusaka

- devnet-2 scope

EIP-7951: Precompile for secp256r1 Curve Support
- EIP-7907 / EIP-7954: Increase Maximum Contract Size
- EIP-7934: RLP Execution Block Size Limit
- EIP-7939: Count leading zeros (CLZ) opcode

[EIP-7975: eth/70 - partial block receipt lists](https://github.com/ethereum/EIPs/pull/9906)
[EIP-7918](https://eips.ethereum.org/EIPS/eip-7918) parameter finalization
[EIP-7892](https://eips.ethereum.org/EIPS/eip-7892) per-tx blob limit

Glamsterdam

- EIP-7745: Light client and DHT friendly log index
- Headliner Proposal: Pureth

 **🤖 config**

- Duration in minutes : 90
- Recurring meeting : true
- Call series : ACDE
- Occurrence rate : bi-weekly
- Already a Zoom meeting ID : false #
- Already on Ethereum Calendar : false #
- Need YouTube stream links : true #
- Facilitator email: ansgar@ethereum.org
Note: The zoom link will be sent to the facilitator via email



[GitHub Issue](https://github.com/ethereum/pm/issues/1569)

## Replies

**abcoathup** (2025-06-17):

### Summary

Decisions made on acde today:

*(Copied from [@adietrichs](/u/adietrichs) summary on Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1385277603371552948) with links to EIPs added*)

[devnet-2](https://notes.ethereum.org/@ethpandaops/fusaka-devnet-2)

- EIP-7951 included, pricing as-is,
- EIP-7907 included (old version, without PR),
- EIP-7934 included,
- EIP-7939 included,

[devnet-3](https://notes.ethereum.org/@ethpandaops/fusaka-devnet-3)

- EIP-7951 pricing,
- EIP-7907 new version,
- EIP-7918 parameter change to 2**13,
- per-tx blob max move to peerdas EIP,

EIP Status

- EIP-7951: move to SFI,
- EIP-7907: move to SFI,
- EIP-7934: move to SFI,
- EIP-7939: add to SFI,
- EIP-7975: keep out of Fusaka Meta-EIP for now

### Recordings/Stream

- https://www.youtube.com/live/as4byc7tX8c?t=218s
- Eth Cat Herders:

Podcast (audio): [Ethereum Cat Herders podcast]
- Live stream on X: https://x.com/i/broadcasts/1gqxvjgvlzpxB [x.com/ethcatherders]

### Writeups

- ACDE #214: Call Minutes by @Christine_dkim [christinedkim.substack.com]
- https://etherworld.co/2025/06/20/highlights-from-the-all-core-developers-execution-acde-call-214/ by @yashkamalchaturvedi [etherworld.co]

### Additional info

- Checkpoint #4: Berlinterop | Ethereum Foundation Blog (client team interop in Berlin)
- Fusaka upgrade:

berlinterop-devnet-2 (second devnet at interop)
- fusaka-devnet-2 targeting June 23, adds EIP7951 secp256r1 precompile, EIP7907 increase code size cap, EIP7934 RLP block size cap & EIP7939 CLZ opcode
- fusaka-devnet-3 targeting July 7, updates pricing of EIP7951 secp256r1 precompile, sets code size cap at 48kb for EIP7907, changes parameter to 2**13 in EIP7918 blob base fee & moves per transaction blob cap to PeerDAS EIP

Glamsterdam upgrade:

- More initial headliner proposals:

Pureth headliner proposal

EIP7745 trustless log index presentation

