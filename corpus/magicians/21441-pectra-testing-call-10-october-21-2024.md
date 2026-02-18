---
source: magicians
topic_id: 21441
title: Pectra testing call #10, October 21 2024
author: abcoathup
date: "2024-10-22"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-10-october-21-2024/21441
views: 63
likes: 0
posts_count: 1
---

# Pectra testing call #10, October 21 2024

#### Summary

Update by [@bbusa](/u/bbusa) *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1297931497327689820))*

**Pectra**

*pectra-devnet-3*

- Has been shut down friday.

*pectra-devnet-4*

- Started last week Friday currently at ~75% finalization
- Erigon/reth/grandine issues mainly
- Erigon - working on final spec changes - not yet merged, some design changes - hopefully ready in a few days
- Grandine - Fixing attestation verifications
- Reth - 7702 transaction was submitted v set to 15 in the auth items - issue has been clarified by lightclient.

*pectra-devnet-5*

- Nethermind - 7742 implementation is in progress
- G11: short modification for EIP7742 - Update EIP-7742: update the required EL headers and the gas fee mecha… by g11tech · Pull Request #8979 · ethereum/EIPs · GitHub
- Open issue regarding the naming convention for max blob and target block activation.
- Discussing whether we want to have the public devnet on top of devnet 4 or devnet 5 spec - depends on client implementation progress
- BLS precompile pricing discussion - no decision made yet - possibly have an update by thursday

**Peerdas**

*peerdas-devnet-3*

- been unfinalized for a while (14d)
- metrics update: teku implementation is in progress

**EOF - Fusaka**

- eof-devnet-0 - fusaka-devnet-0*
- rebased on alpha 8 - built on top of devnet 4 spec
osakaTime as the fork activation launch in ~ 1 week time
- Besu is ready go
- Reth has osaka - haven’t been tested yet
- Nethermind - work in progress

**SSZ devnets**

*ssz-devnet-0*

- no updates
