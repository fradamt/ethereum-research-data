---
source: magicians
topic_id: 21217
title: Pectra testing call #6, 23 September 2024
author: abcoathup
date: "2024-09-29"
category: Protocol Calls & happenings
tags: [testing, pectra]
url: https://ethereum-magicians.org/t/pectra-testing-call-6-23-september-2024/21217
views: 56
likes: 0
posts_count: 1
---

# Pectra testing call #6, 23 September 2024

#### Summary

Update by Mario Vega *(from Eth R&D [Discord](https://discord.com/channels/595666850260713488/745077610685661265/1287791168557551704))*

`Pectra Devnet-3` :

- PK910: Filling deposit queue to see if the increased queue has an effect on timing. Currently have 32,000 deposits, and will fill up to 50,000. No findings yet.
- Ethjs having trouble keeping up due performance issues, but these are expected due to the overhead of running the JS engine. No consensus issues at the moment so the client is expected to sync up to head when there are less transactions to process.

`Pectra Devnet-4` :

- Nethermind: Requires BLS gas pricing benchmark to finish
- Testing updates required, testing team will start working on them this week and potentially have a release by the end of the week with all Devnet-4 changes.
- Significant tooling changes are required for devnet-4: Assertor, and potentially MEV builder should be included in this phase.
- List of all changes to be included in Devnet-4: pectra-devnet-4 specs - HackMD
- Consensus spec release for devnet-4: Release Mareep · ethereum/consensus-specs · GitHub
- There was a discussion about CLs might needing to implement RLP decoding, but it turns out this is not necessary after all.
- Need testing of deposits before and after the fork are queued in correct order, assertor should be capable of doing this on the next devnet, so the Pectra fork should be activated on epoch 300-400 in order to queue up enough deposits before the fork.

`PeerDAS Devnet` :

- Barnabas: Running long testnet with all CL combos, very stable at the moment at epoch 40 with 100% participation. Potential launch devnet-2 tomorrow.
- Gajinder raised concern that we should run longer testnets because 40 epochs look ok, but clients have forked at 200+ epochs, sampling parametrization is required to guarantee the network can be stable under different circumstances. More supernodes+nodes ratio parametrization is required along with evaluation of stability on each configuration, in order to detect parameters that are more prone to be unstable. Barnabas suggested that we should use main-net parameters to start, and eventually branch out to more combination of parameters. This topic should be brought up on the next testing meetings.
- Metric unification: CL clients are encouraged to adopt the same metric names in order to make it easier to gather metrics from all clients using the same grafana dashboards. Link shared in the meeting regarding this: https://github.com/ethereum/beacon-metrics/pull/13
- Builder: Reth is currently working on rBuilder, and MEV-Boost also, but target would be devnet-4. Hive can be updated to have builder process sanity testing.

`EOF` :

- Potential spin up of a Devnet in order to test EOF contract deployment. It was suggested we can use a simple fork name such as “EOF” in order to activate on top of “Pectra A” EIPs.
- Current issue is obtaining interesting EOF contracts in the devnet, such as popular contracts like Uniswap or the OpenZeppelin implementations in EOF deployed.
