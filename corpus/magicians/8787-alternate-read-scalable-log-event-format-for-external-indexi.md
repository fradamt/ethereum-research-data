---
source: magicians
topic_id: 8787
title: Alternate read-scalable log event format for external indexing (i.e. by data warehouses), possibly requiring new EVM opcode
author: tsutsu
date: "2022-04-01"
category: Magicians > Primordial Soup
tags: [opcodes]
url: https://ethereum-magicians.org/t/alternate-read-scalable-log-event-format-for-external-indexing-i-e-by-data-warehouses-possibly-requiring-new-evm-opcode/8787
views: 658
likes: 1
posts_count: 1
---

# Alternate read-scalable log event format for external indexing (i.e. by data warehouses), possibly requiring new EVM opcode

(Posting this here before I make it into a formal EIP; I’d like to know whether this has already been thought about/discussed before.)

## Problem statement

Two practices adopted by the Solidity compiler have, together, effectively poisoned the usefulness of (non-standard-formalized) log events for generalized third-party consumption (i.e. consumption of the entirety of the log-event firehose by parties other than the contracts’ authors, for purposes of whole-chain indexing.)

- The “contract metadata” generated during compilation (including the contract’s ABI) are only referenced from the contract via an IPFS CID embedded in the contract’s metadata; but solc (and even ReMix) have no automatic push of contract metadata to IPFS, let alone any sort of community-supported automatic IPFS pinning; in the end, nearly no contract metadata actually exists on IPFS.
- The de-facto standard canonicalized event-signature format introduced by Solidity, throws away both parameter names and indexed annotations.

Together, these mean that, for much of compiled Solidity code, all a third-party indexer trying to parse log-events emitted by the contract might have to work with, is the data in the events themselves, plus a database mapping Solidity canonicalized event-signatures to their hashes. With only these, the proper decoding for an event’s topics/data back to event parameters is NP-hard at best, and impossible due to ambiguity at worst. (It’s essentially a constraint-satisfaction problem of where to place the `indexed` annotations to get a valid decoding; where if there’s more than one valid solution, then there’s no solution. And without the param names, there’s a lot more type ambiguity, e.g. between `address indexed from, address to` and `address from, address indexed to`.)

For existing deployed contracts, there’s not much that can be done; the deployed contract bytecode may be able to be reverse-engineered to better understand the types going in, but that won’t solve 100% of cases (e.g. the same-type confusion above.) Statistical analysis of the corpus of all published log events may be of help, but as different contracts are free to make different fields `indexed` while ending up with the same `topic0` event-signature hash, these statistics may themselves be poisoned unless done on a contract-by-contract basis.

The core problem is essentially the use of log-event topics. If all data were stored in the `data` field, there would be no ambiguity in decoding. Log-event topics, and their strict `bytes32` shape, exist for the purpose of bloom indexing; but implementations like Erigon are finding that bloom indexing can be replaced with other approaches that don’t require separated + strictly-formatted topics.

Additionally, many ecosystem developers that previously relied upon consuming pre-filtered log-events from the node itself, are now instead relying on external data-warehouse systems which consume the entire log-event firehose from the node (usually by consuming tx receipts, rather than subscribing to log events) and then internally index the events with more-powerful indexing strategies, allowing arbitrary OLAP querying of log events. These systems can be thought of as mooting the need for “onboard” log indexing on the node. (IMHO, nodes should focus on being OLTP systems — with data architectures optimized for writes, and for the reads done to *compute* writes — while leaving OLAP jobs like log-event indexing to external systems. Though, as the developer of such an external system, I might be slightly biased. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15) )

## Potential proposal

I have two potential solutions in mind. Both require a move to a new event-signature canonicalization format, so this format will be outlined first.

- Solution 1 is compatible with existing nodes, log-event consumers, and external indexers, and only requires introducing to EVM-ISA-targeting language like Solidity a new event format that emits differently; but this emission difference will slightly increase the gas cost of log-event emission for these new-style events, as an extra element of topics must be reserved (for non-anonymous events) to store an “inner” topic hash. However, a hard fork may fix this by explicitly special-casing gas costs of LOGn ops for these shimmed events.
- Solution 2 requires a new EVM opcode. Logs emitted by this new opcode may or may not be represented differently over RPC. Logs emitted by this opcode would be generally cheaper.

In either case, languages targeting the EVM would need to have their grammars extended to introduce an alternate event-declaration format.

- Existing events in the old format would continue to compile with their previous semantics.
- The new events would be opt-in by use of the new declaration format.
- Language compilers could choose to interpret old-style event declarations as new-style events if and only if:

they offer EVM ISA uarch target selection (a “compile for {Homestead, Byzantium, Istanbul, …}” switch)
- a new ISA uarch is introduced which explicitly deprecates old-style log events
- the developer chooses to compile their code for this uarch

### New-style canonicalized event-signature format

```auto
event -> (annotation ' ')* 'event' ' ' identifier '(' paramCategories? ')'
annotation -> 'packed'
paramCategories -> (filterParamsCategory ', ')? (aggregatesParamsCategory ', ')? detailsParamsCategory
paramCategories -> (filterParamsCategory ', ')? aggregatesParamsCategory
paramCategories -> filterParamsCategory
filterParamsCategory ->  paramsTuple ' ' 'filters'
aggregatesParamsCategory ->  paramsTuple ' ' 'aggregates'
detailsParamsCategory ->  paramsTuple ' ' 'details'
paramsTuple -> '(' param+ ')'
param -> type ' ' identifier
```

Example: `packed event Foo((uint256 a, address b) filters, (address c) aggregates, (uint64 d) details)`

- has event in the signature string, to make it impossible for a new-style event signature to collide with a function signature and/or an old-style event signature
- optional annotation pragmas prefixed before event, e.g. packed — always sorted in alphabetical order
- parameter names are included

contract interface standards should standardize parameter names (this is required to distinguish e.g. “(address from, address to)” from “(address to, address from)”)

no use of parameter annotations — parameters are instead categorized into top-level tuple-typed params with each top-level param having its own read-time semantics
param categories are enforced at development time, but don’t affect parsing at read time; existing event-signature parsers will recognize the parameter list as containing three tuple-typed params. The categories are essentially a “microformat.”
put a single space after each comma — this isn’t a space-optimizing encoding or even a runtime-parsed/generated encoding, it’s a compile-time encoding. May as well make it legible.

Semantics of param categories for read indexers:

- categories should be recognized by the parameter name
- all categories are optional
- categories that are used must appear in canonical order: filters, then aggregates, then details
- meanings of categories:

aggregates: fields that should be broken out into their own typed columns for efficient OLAP aggregation (e.g. summation) by the consuming data warehouse
- filters: fields that should be broken out into their own typed columns, and then, additionally, indexed (using e.g. bloom filter, Postgres GIN index, etc) by the consuming data warehouse, to enable their use in query filtering (e.g. SQL SELECT clause)
- details: fields that only matter in point queries; all details fields can be stored packed together in a storage-efficient, query-inefficient representation (e.g. Postgres JSONB), as such data will only likely be accessed for O(1) events at a time

### Potential solution 1: generate “wrapped” events

All new-style events would codegen to a `LOG2` op:

- topic0 would be a constant: kec("NewstyleWrappedEvent(bytes32 indexed topic, bytes data)")
- topic1 (a.k.a. topic in the outer signature) would contain the “real” event signature hash, using a new alternate event-signature canonicalization algorithm
- data (which is also the data member of the outer signature) would contain a tuple-serialization of the fields specified by the “real” event signature

A hard-fork EIP could be introduced to special-case the gas costs of `LOG2` where `topic0` is the newstyle-event wrapper event signature; perhaps lowering gas costs (removing the overhead of the extra `topic1` + outer-`data`-tuple `bytes` param dynamic `length`) to incentivize transition to the newstyle format.

## Potential solution 2: new opcode LOGR

New-style events would codegen to a novel opcode, `LOGR`, which emits events specifically for consumption by external read-indexers consuming the log-event firehose.

- Log-events emitted by LOGR would not participate in bloom indexing. The only way to receive these events is via filterless eth_subscribe("logs"), or by consuming tx-receipts directly.
- LOGR events would, for consensus + RPC purposes, be considered to have one topic, a topic0 of the newstyle event-signature hash. Because this topic isn’t bloom-indexed, it would cost LogDataGas rather than LogTopicGas.

If potential-solution 1 were also pursued in parallel, the hard-fork EIP that special-cases the behavior of the shim, could function by translating calls to `LOG2` with the special newstyle-wrapper topic hash, as actually being calls to `LOGR`, where the `LOG2`’s `topic1` becomes the `LOGR`’s `topic0`.
