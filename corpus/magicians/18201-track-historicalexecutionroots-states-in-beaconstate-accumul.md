---
source: magicians
topic_id: 18201
title: Track `HistoricalExecutionRoots/States` in `BeaconState` accumulators
author: g11in
date: "2024-01-18"
category: EIPs > EIPs core
tags: [stateless-clients, merkle-proof]
url: https://ethereum-magicians.org/t/track-historicalexecutionroots-states-in-beaconstate-accumulators/18201
views: 912
likes: 9
posts_count: 7
---

# Track `HistoricalExecutionRoots/States` in `BeaconState` accumulators

Currently ethereum BeaconState tracks `HistoricalBlockRoots` and `HistoricalStateRoots` for last `SLOTS_PER_HISTORICAL_ROOT` period and accumulate them in `HistoricalSummaries` upon completion of every period.

This proposal extends the similar tracking and accumulation to the execution payload’s `blockHash` and `stateRoot`

1. With this one would be able to easily prove if a particular execution state/block was part of canonical chain represented by the BeaconBlock/BeaconState.
2. Additionally this could help stateless (or rather chainless) EL execution by providing last 256 roots in newPayload block executions for resolving BLOCKROOT opcode

There could be additional benefits from (2.) for the Verkle fork where having stateful pre-compiles (which require free “system” update on each block to the state) could pose risks from some DoS vectors

## Replies

**ralexstokes** (2024-01-18):

the proof would be a bit longer but you can get to both `blockHash` and `stateRoot` in the execution payload header from any `HistoricalSummary` so I don’t see the need to lift these into the state as explicit data

---

**g11in** (2024-01-18):

right thats possible, but it also allows to seed these values to the EL client via newPayloads without requiring them written into the EL state which is quite relevant for VKT (so 4788 is also a problem see this: [EIP-4788: Beacon root in EVM - #42 by ihagopian](https://ethereum-magicians.org/t/eip-4788-beacon-root-in-evm/8281/42))

---

**gabrocheleau** (2024-01-20):

Tangential thought that in the context of Verkle, if we end up going with the “get blockhash from CL” to implement the `BLOCKHASH` opcode, we probably would need to revisit the gas cost associated with `BLOCKHASH` (currently at `20`). Intuitively, getting the data from a data structure living on the CL sounds more like an “SLOAD-like” operation. The historically cheap cost of `BLOCKHASH` seems to assume that clients are continually storing the last 256 blockhashes in a stateful and easy-to-access cache, which won’t hold in the context of verkle stateless clients.

---

**g11in** (2024-01-21):

the right way to implement would be for new payload to carry last 256 hashes, so EL doesn’t need to fetch anything from CL, and these hashes should be readily available (similarly for beacon block root corresponding to 4788)

---

**ajsutton** (2024-01-21):

It’s worth considering the case of syncing a fresh archive execution node here. The consensus node can still start from recent finalized state but the execution node would do a full sync instead of a snap sync to catch up. In this situation the execution node would be executing transactions from block arbitrarily older than the earliest state the consensus node has. If the EL needs to retrieve the root for `BLOCKROOT` from the consensus node then the consensus state must include them all without the usual accumulator pattern.

---

**g11in** (2024-01-22):

but EL doing archive sync from genesis will have all the roots no?

