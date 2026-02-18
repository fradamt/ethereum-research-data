---
source: magicians
topic_id: 22247
title: Client testing call #17, December 16, 2024
author: abcoathup
date: "2024-12-17"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/client-testing-call-17-december-16-2024/22247
views: 114
likes: 1
posts_count: 1
---

# Client testing call #17, December 16, 2024

### Pectra Interop Testing Call 2024-12-16 Summary

Notes by [@danceratopz](/u/danceratopz) *(Copied from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1318234114964324423))*

**Pectra**

No longer scheduled for inclusion in Pectra:

- EIP-7742 Uncouple blobs per block between CL and EL
- EIP-7762 Blob fee change (not high prio for rollups)

**Progress/Open PRs for [pectra-devnet-5](https://notes.ethereum.org/@ethpandaops/pectra-devnet-5)**

CL:

- Add SSZ support to builder api ethereum/builder-specs#104: unclear inclusion status for devnet-5.
- GOSSIP_MAX_SIZE

ethpandaops tested blocks with 40 million gas and capacity blob data: the 10MiB limit not hit.
- Bump GOSSIP_MAX_SIZE from 10MiB to 15MiB consensus-specs#4041 Edit: This was decided against in the last ACDC
- ethereum/consensus-specs#4045 is the PR actively being worked on. Should not be a blocker for devnet-5. Could be included or left out, depending on other devnet-5 progress.

EELS (ethereum/execution-specs) status - PRs required for test generation:

- EIP-7623: Increase Calldata Cost ethereum/execution-specs#966 - will reviewed/merged soon!
- Add EIP-7691, EIP-7762 to Prague ethereum/execution-specs#1054 - 7762 to be removed before merge.

EL Changes:

- EIP-2537: Waiting for final BLS pricing changes:

Update EIP-2537: Gas pricing MAP, MUL and ADD operations
- Update EIP-2537: MSM gas repricing
- Update EIP-2537: Gas pricing pairing operations

EIP-7702: Small change, chainid type:[Update EIP-7702: Update chainid to uint256](https://github.com/ethereum/EIPs/pull/9143)
TBD in ACD this week for Pectra: [Add EIP: Add blob schedule to EL config files](https://github.com/ethereum/EIPs/pull/9129)

EEST (ethereum/execution-spec-tests) status:

- ethereum/execution-spec-tests#1004 requires merge.
- ethereum/execution-spec-tests#1022 needs removal of EIP-7762, then can be merged.
- Release planned for later this week.

**PeerDAS / EOF**

No updates discussed this time; current focus is on Pectra Devnet 5.

**Upcoming**

- Thurs 19th Dec: Last ACD of the year.

TBD in ACD Add EIP: Add blob schedule to EL config files ethereum/EIPs#9129.

EEST fixture release this week (without ethereum/EIPs#9129).
