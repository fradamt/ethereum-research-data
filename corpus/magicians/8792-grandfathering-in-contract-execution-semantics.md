---
source: magicians
topic_id: 8792
title: "\"Grandfathering in\" contract execution semantics"
author: tsutsu
date: "2022-04-01"
category: Magicians > Primordial Soup
tags: []
url: https://ethereum-magicians.org/t/grandfathering-in-contract-execution-semantics/8792
views: 541
likes: 2
posts_count: 1
---

# "Grandfathering in" contract execution semantics

Simple premise:

- What if we could make big breaking changes to the EVM (e.g. introducing gas costs for something that previously didn’t have gas costs), but only impact newly-deployed contracts, while existing contracts would keep using the old rules, and so would keep working?
- What if the EVM as a component didn’t need to maintain backward-compatibility for execution of historical blocks back to genesis, and so could free itself of “legacy” code-paths concerning how things worked before now-active hard forks?

How would it work?

- Add an optional field to the end of the consensus ExternalAccount RLP data, updated along with the Code each time the Code is set. This field would contain either the block the Code was last set on; or — smaller/more efficient — the applicable compatibility version it was set on, where the compatibility version is fed into the EVM as part of the ChainRules, starts at 0, and goes up by 1 when there’s a hard fork that affects EVM semantics. (The current compatibility version until the next hard fork after this logic is introduced, would be 0; ExternalAccounts without a compatibility version would be taken to have a compatibility version of 0.)

 A toplevel creation transaction’s deployment bytecode runs under the current compatibility version; and the contract created by returning data from it also uses the current compatibility version.
- Contracts created by calls to the CREATE or CREATE2 opcodes, inherit the compatibility version of the caller. (Ergo, old factory contracts produce fresh “old” contracts.)
- Calls to CALL and DELEGATECALL both execute with the compatibility version of the contract targeted by the call. (This would require a refactor where EVMs are instanced to the execution of particular contracts, so that the old-version EVM can call into a contract that constructs a new-version EVM to execute it.)

In node implementations, compile the EVM *core* (to borrow a term from the MAME project) as a dynamic shared library, with a strictly-defined plugin ABI that allows multiple versions of this *core* to be loaded into the same process address-space concurrently. Ship nodes with multiple EVM *cores* — one core for each *compatibility version* ever mentioned on-chain. Load cores on-demand, whenever a contract would be executed from an unrecognized *compatibility version*. Potentially, garbage-collect cores, unloading the dynamic library from the process if it hasn’t been called into in e.g. 30 minutes.

- Potentially, given a formalized specification for this plugin API, EVM cores could be shared between different node implementations; development of EVM cores and nodes could be made independent.
- EVM cores could be downloaded on-demand by node implementations from their origin developer / a trusted RSS-feed node-config value — much like ReMix + solc.js do with WASM solc builds. Interestingly, this would allow EVM cores newer than the node to be fetched and loaded on-demand, effectively enabling “node hot-upgrade” for at least EVM-isolated changes.

(The “versioned cores” + “compatibility versions” approach here takes inspiration from how networked multiplayer games like Starcraft do match recordings. To play a networked match in such a game, both players’ clients must agree on an engine version. The match’s event stream — both input commands on both sides, and their logical results in game-engine terms — get synced and optionally recorded, in terms of this engine version’s internal format for them. Later, any recorded match can be independently replayed/audited by another game client; to do so, the auditing node will detect the engine-version used for the match record, load the appropriate engine-version DLL, and then feed the recording into the loaded engine for re-execution.)
