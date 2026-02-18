---
source: ethresearch
topic_id: 1407
title: Sharding phase 1 spec (RETIRED)
author: JustinDrake
date: "2018-03-16"
category: Sharding
tags: []
url: https://ethresear.ch/t/sharding-phase-1-spec-retired/1407
views: 38724
likes: 62
posts_count: 89
---

# Sharding phase 1 spec (RETIRED)

**UPDATE 10 April**: This draft spec is now retired and won’t be maintained. The research team is working on a better design ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) More details [here](https://ethresear.ch/t/a-minimal-sharding-protocol-that-may-be-worthwhile-as-a-development-target-now/1650/3).

---

This document is a draft spec of sharding phase 1. It is a pre-release intended for researchers and implementers. Some details will likely change.

The [old phase 1 sharding doc](https://github.com/ethereum/sharding/blob/develop/docs/doc.md) is now deprecated. Notice some of the nomenclature has changed, e.g. we no longer have a “VMC” or “validators”. Please familiarise yourself with the glossary below. Credits to [@hwwhww](/u/hwwhww) for preparing an [accompanying infographic](https://www.icloud.com/keynote/05Q0CUa8WRPrvPx0tVgLTri_A#Ethereum%5FSharding%5FInfographic).

Questions and feedback are most welcome, and will help us evolve this spec. Go wild, tear it apart! In a few weeks this document will be migrated to GitHub.

---

Phase 1 is the first non-prototype implementation in a multi-phase sharding roadmap. It is a minimal version of sharding—without enshrined execution—intended as a foundation for the first production release. We encourage independent developers worldwide to build their own clients and join the phase 1 testnet.

## Proposers, collators and executors

The current roadmap distinguishes three types of sharding participants:

- Proposers: A proposer is responsible for preparing the data that goes in a given shard. It prioritises so-called blobs (think, transactions) and assembles them into collations (think, blocks). Collations are proposed to collators for inclusion in the collation tree via an open auction amongst proposers. To prioritise blobs and maximise revenue proposers are expected to run executing nodes.
- Collators: A collator is responsible for extending the head of the canonical chain of shards. It adjudicates on the availability of collation bodies and selects the highest-paying available collations from proposers. Collators are not required to run executing nodes. This allows for fast shuffling of the collator pool across shards, a key part of phase 1 sharding’s security.
- Executors: An executor is responsible for running the enshrined execution engine on the canonical chain of a given shard, and posting cryptoeconomic claims on state roots. This allows light-clients to guess the state root of a shard without running executing nodes. Executors are planned for phase 3 after an EVM state transition function is specified in phase 2.

## Glossary

#### Shards

- shard: A chain of available collations, also known as a “child shard”.
- shard ID: A 32-byte identifier for shards made of a 1-byte network ID, 30 reserved bytes set to 0x00, and a 1-byte shard number.
- network ID: The most significant byte of the shard ID, with most significant bit 0 for mainnet and 1 for testnet. Provisionally NETWORK_ID := 0b1000_0001 for the phase 1 testnet.
- shard number: The least significant byte of the shard ID, ranging from 0 to SHARD_COUNT - 1.
- shard count: The total number of shards within a network. Provisionally SHARD_COUNT := 100 for the phase 1 testnet.
- non-transactional shard: A shard without enshrined execution. Sharding phase 1 is a “blob shard”, i.e. a non-transactional shard with non-executed blobs (as opposed to executed transactions).

#### Collations

- collation: A collation header plus a corresponding collation body. Collations are the data unit by which shards can advance every period.
- collation header: A concise header containing collation metadata, in particular pointers to a shard, to a collation body, and to a parent collation header.
- collation body: A file of size COLLATION_SIZE bytes (right-padding with zero bytes if necessary) composed of 32-byte chunks. All collation bodies are valid for inclusion in the canonical chain.
- collation size: The fixed size, denominated in bytes, of a collation body. Provisionally COLLATION_SIZE := 2 ** 20.
- chunk: A 32-byte-aligned collation chunk of size CHUNK_SIZE := 32 bytes.
- chunk tree: The full binary Merkle tree with leaves the chunks of a collation body.
- chunk root: The root of the chunk tree which identifies a collation body.
- available collation: A collation for which the collation body identified by the chunk root is available.
- blob: A byte-aligned piece of data delimited and ordered within a collation. Blob serialisation is TBD, and execution will be defined in phase 2.

#### Collation trees

- collation tree: The connected and directed tree of collations for every shard, as recorded by the SMC. Headers are vertices pointing to parent headers to form edges.
- genesis collation: The first collation of a shard, fixed as a protocol checkpoint.
- canonical chain: The longest available chain in a collation tree with respect to the genesis collation. Tie breaking of equal-length chains is done by applying the fork choice rule.
- fork choice rule: Precedence is given to the chain with the oldest tip.
- confirmed collation: A collation included in a canonical chain.
- orphaned collation: A collation in the collation tree not in a canonical chain.
- head: The tip of the canonical chain.
- header hash: The hash of a collation header acting as its identifier.
- parent header: A header referenced by its hash from a subsequent header. The genesis collation has no parent header.
- height: The height of a collation in a shard’s collation tree relative to the genesis collation.

#### Collators

- collator: A sharding participant responsible for collation availability and chaining.
- collator pool: The set of all collators collectively participating in the security of all shards.
- collator subsidy: A fixed protocol subsidy, denominated in vETH, awarded to the collators of collations included in the canonical chain of a shard. Provisionally COLLATOR_SUBSIDY := 0.001.
- virtual ETH: The currency unit with symbol vETH in which collators are rewarded. Virtual ETH will become transferable within a shard in phase 2, fungible across shards in phase 4, and fungible with ETH in phase 5.
- eligible collator: The collator with the right to extend the collation tree of a given shard in the current period.
- honest majority assumption: The fundamental security assumption for phase 1 sharding that more than half the collators are honest.
- honest collator: A collator that faithfully follows protocol rules irrespective of financial incentives such as bribes.
- collator shuffling: The pseudo-randomised process of selecting an eligible collator from the collator pool for every shard and at every period.

#### Proposers

- proposer: A sharding participant responsible for proposing collations to eligible collators.
- proposer pool: The set of proposers for all shards collectively prioritising blobs for inclusion in collations.
- proposal: A proposed collation header extending the collation tree presented by a proposer to an eligible collator.
- proposer address: The proposer’s address in a proposal against which the proposer’s signature is checked.
- proposer bid: The amount of ETH that is burned from the proposer balance, and the equivalent of vETH that is minted in the corresponding shard and awarded to the collator.
- proposer balance: The balance associated with a given proposer and shard from which proposer bids are deducted.
- minimum proposer balance: The minimum balance, denominated in ETH, required for participation as a proposer on a given shard. Provisionally MIN_PROPOSER_BALANCE := 0.1.
- proposer signature: The proposer’s signature as part of a proposal.
- self-proposal: A proposal for which the proposer is the eligible collator. In a self-proposal the proposer address, bid and signature are omitted.
- available proposal: A proposal for which the corresponding collation body has been made available by the proposer.
- selected proposal: The proposal selected by an eligible collator. At most one proposal can be selected per period and per shard.

#### Proposer withholding

- proposer withholding: The situation where a proposer does not make a proposal available. Proposer withholding of selected proposals is mitigated with a proposal commitment scheme.
- proposal commitment: A cryptographic commitment by a collator for a set of proposals, allowing proposers to make available their proposals without risk of proposal plagiarism.
- proposal plagiarism: The situation where a collator reuses the blobs of a proposal without compensating the proposer.
- proposal commitment slashing: The slashing condition enforcing proposal commitments.
- availability challenge: A challenge to reveal a chunk of a collation added to a collation tree. The challenge is targeted at a collator within the windback of the challenged collation.
- availability response: A response from the challenged collator to an availability challenge.
- availability slashing: The slashing condition enforcing the collation availability challenge-response scheme.

#### Sharding Manager Contract (SMC)

- SMC: The contract on the main chain at address SMC_ADDRESS that manages collators, proposers and collation trees.
- main chain: The main Ethereum blockchain hosting the SMC, also known as the “main shard”, “root chain” or “root shard”.
- period: The period of time, denominated in main chain block times, during which a collation tree can be extended by one collation. Provisionally PERIOD_LENGTH := 5, approximately 75 seconds.
- lookahead: The advance notice eligible collators get before their assigned period.
- lookahead length: The lookahead time, denominated in periods, for eligible collators to perform windback and select proposals. Provisionally LOOKAHEAD_LENGTH := 4, approximately 5 minutes.
- windback: The process of attempting to determine the head by winding back recent collation headers, checking availability of collation bodies, and applying the fork choice rule. Also known as “head fetching” or “head guessing”.
- windback length: The depth, denominated in collations, to which collators need to wind back as part of the windback process. Provisionally WINDBACK_LENGTH := 25.

#### Registries

- registry: A data structure in the SMC maintaining a set of sharding participants. Phase 1 has a collator registry and a proposer registry.
- registration: The act of adding a registry entry by posting a deposit to become a sharding participant.
- deposit: The fixed-size deposit, denominated in ETH, required for registration. Provisionally COLLATOR_DEPOSIT := 1000 and PROPOSER_DEPOSIT := 1.
- deregistration: The act of requesting the removal of a registry entry and cease being a sharding participant. The deposit is subject to a temporary lockup after deregistration.
- lockup length: The amount of time, denominated in periods, a deposit is locked up from the time of deregistration. Provisionally COLLATOR_LOCKUP_LENGTH := 16128, approximately two weeks, and PROPOSER_LOCKUP_LENGTH := 48, approximately one hour.

#### Nomenclature cheat sheet

| Ethereum 1.0 | sharding phase 1 |
| --- | --- |
| blockchain | shard |
| block | collation |
| block time | period |
| gas limit | collation size |
| transaction | blob |
| transaction root | chunk root |
| miner | collator |
| PoW sampling | collator shuffling |

## Parameters

```auto
// Shards
SMC_ADDRESS := (TBD)
NETWORK_ID := 0b1000_0001
SHARD_COUNT := 100                // shards
PERIOD_LENGTH := 5                // block times
LOOKAHEAD_LENGTH := 4             // periods
WINDBACK_LENGTH := 25             // collations

// Collations
COLLATION_SIZE := 2 ** 20         // bytes
CHUNK_SIZE := 32                  // bytes
COLLATOR_SUBSIDY := 0.001         // vETH

// Registries
COLLATOR_DEPOSIT := 1000          // ETH
PROPOSER_DEPOSIT := 1             // ETH
MIN_PROPOSER_BALANCE := 0.1       // ETH
COLLATOR_LOCKUP_LENGTH := 16128   // periods
PROPOSER_LOCKUP_LENGTH := 48      // periods
```

## Collation header fields

Sharding participants have light-client access to collation headers via the `HeaderAdded` logs produced by the `addHeader` method. The header fields are:

```auto
shard_id           uint256 // pointer to shard
parent_hash        bytes32 // pointer to parent header
chunk_root         bytes32 // pointer to collation body
period             int128
height             int128
proposer_address   address
proposer_bid       uint256
proposer_signature bytes
```

## SMC storage

The SMC has the following data structures held in storage:

- Collator pool

collator_pool: address[int128]—array of active collator addresses
- collator_pool_len: int128—size of the collator pool
- empty_slots_stack: int128[int128]—stack of empty collator slot indices
- empty_slots_stack_top: int128—top index of the stack

**Collator registry**

- collator_registry: {deregistered: int128, pool_index: int128}[address]—collator registry (deregistered is 0 for not yet deregistered collators)

**Proposer registry**

- proposer_registry: {deregistered: int128, balances: wei_value[uint256]}[address]—proposer registry

**Collation trees**

- collation_trees: bytes32[bytes32][uint256]—collation trees (the collation tree of a shard maps collation hashes to previous collation hashes truncated to 24 bytes packed into a bytes32 with the collation height in the last 8 bytes)
- last_update_periods: int128[uint256]—period of last update for each shard

**Availability challenges**

- availability_challenges: TBD—availability challenges
- availability_challenges_len: int128—availability challenges counter

## SMC methods

Most of the methods detailed below issue logs. For brevity we don’t emphasise them except for the `HeaderAdded` log.

#### Registries

- register_collator() returns bool: Adds an entry to collator_registry, updates the collator pool (collator_pool, collator_pool_len, etc.), locks a deposit of size COLLATOR_DEPOSIT, and returns True on success. Checks:

Deposit size: msg.value >= COLLATOR_DEPOSIT
- Uniqueness: collator_registry[msg.sender] does not exist

**`deregister_collator() returns bool`**: Sets the `deregistered` period in the `collator_registry` entry, updates the collator pool (`collator_pool`, `collator_pool_len`, etc.), and returns `True` on success. Checks:

- Authentication: collator_registry[msg.sender] exists

**`release_collator() returns bool`**: Removes an entry from `collator_registry`, releases the collator deposit, and returns `True` on success. Checks:

- Authentication: collator_registry[msg.sender] exists
- Deregistered: collator_registry[msg.sender].deregistered != 0
- Lockup: floor(block.number / PERIOD_LENGTH) > collator_registry[msg.sender].deregistered + COLLATOR_LOCKUP_LENGTH

**`register_proposer() returns bool`**: Equivalent of `register_collator()`, without the collator pool updates.

**`deregister_proposer() returns bool`**: Equivalent of `deregister_collator()`, without the collator pool updates.

**`release_proposer() returns bool`**: Equivalent of `release_collator()`. **WARNING**: The proposer balances need to be emptied before calling this method.

**`proposer_add_balance(uint256 shard_id) returns bool`**: Adds `msg.value` to the balance of the proposer on `shard_id`, and returns `True` on success. Checks:

- Shard: shard_id against NETWORK_ID and SHARD_COUNT
- Authentication: proposer_registry[msg.sender] exists

**`proposer_withdraw_balance(uint256 shard_id) returns bool`**: Withdraws the balance of a proposer on `shard_id`, and returns `True` on success. Checks:

- Shard: shard_id against NETWORK_ID and SHARD_COUNT
- Authentication: proposer_registry[msg.sender] exists

#### Collation trees

- get_eligible_collator(uint256 shard_id, uint256 period) returns address: Uses the blockhash at block number (period - LOOKAHEAD_LENGTH) * PERIOD_LENGTH) and shard_id to pseudo-randomly select an eligible collator from the collator pool, and returns the address of the eligible collator. Checks:

Shard: shard_id against NETWORK_ID and SHARD_COUNT
- Period: period == floor(block.number / PERIOD_LENGTH)
- Non-empty pool: collator_pool_len > 0

**`compute_header_hash(uint256 shard_id, bytes32 parent_hash, bytes32 chunk_root, uint256 period, address proposer_address, uint256 proposer_bid) returns bytes32`**: Returns the header hash.

**`add_header(uint256 shard_id, bytes32 parent_hash, bytes32 chunk_root, uint256 period, address proposer_address, uint256 proposer_bid, bytes proposer_signature) returns bool`**: Calls `compute_header_hash(...)`, extends the collation tree of `shard_id`, burns the `proposer_bid` from the proposer’s balance at `shard_id`, issues a `HeaderAdded` log, and returns `True` on success. Checks:

- Shard: shard_id against NETWORK_ID and SHARD_COUNT
- Collator eligibility: msg.sender == get_eligible_collator(shard_id, period)
- Parent exists: collation_trees[shard_id][compute_header_hash(...)] exists
- Correct period: period == floor(block.number / PERIOD_LENGTH)
- Unique update: period != last_update_periods[shard_id]
- Proposer balance: proposer_registry[proposer_address].balances[shard_id] >= max(proposer_bid, MIN_PROPOSER_BALANCE)
- Proposer signature: proposer_signature matches compute_header_hash(...) and proposer_address

#### Slashing

- proposal_commitment_slashing(uint256 shard_id, bytes32 collation_hash, uint256 height, uint256 left_hash, uint256 right_hash, bytes signature) returns bool: Slashes a collator that called add_header with a non-committed proposal. Checks:

Shard: shard_id against NETWORK_ID and SHARD_COUNT
- Collation tree: collation_trees[shard_id][collation_hash] exists
- Height: collation_trees[shard_id][collation_hash] matches height
- Signature: signature matches height, left_hash and right_hash
- Slashing condition: left_hash

**`availability_challenge()`**: **TBD**

**`availability_response()`**: **TBD**

**`availability_slashing()`**: **TBD**

## Roadmap

The roadmap is an active area of research. The outline below is only intended to provide flavour.

- Phase 1: Basic sharding without EVM

Blob shard without transactions
- Proposers
- Proposal commitments
- Collation availability challenges

**Phase 2**: EVM state transition function

- Full nodes only
- Asynchronous cross-contract calls only
- Account abstraction
- eWASM
- Archive accumulators
- Storage rent

**Phase 3**: Light client state protocol

- Executors
- Stateless clients

**Phase 4**: Cross-shard transactions

- Internally-synchronous zones

**Phase 5**: Tight coupling with main chain security

- Data availability proofs
- Casper integration
- Internally fork-free sharding
- Manager shard

**Phase 6**: Super-quadratic sharding

- Load balancing

## Replies

**jamesray1** (2018-03-16):

Thanks for this, it has lots of interesting ideas as always! If it weren’t for working on developing an implementation myself I would be looking to help with research!

I like the reward for collators, it contrasts to no reward for full nodes at the moment. It’s good that the entry cost for participation as a proposer is only 0.1 ETH, and that collators do not have to be a full node. Unfortunately and understandably, collators still need to deposit 1000 ETH (otherwise too many collators would reduce throughput, increase overhead or increase latency). But the proposer deposit is low enough for an average individual to participate.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> get_eligible_collator(uint256 shard_id, uint256 period) returns address: Uses the blockhash at block number (period - LOOKAHEAD_LENGTH) * PERIOD_LENGTH) and shard_id to pseudo-randomly select an eligible collator from the collator registry, and returns the address of the eligible collator.

What mechanism are you going to use for pseudo random selection, is it perhaps BLS random beacons, RANDAO, pure private randomness, hybrid RANDO/private or NEXT RNG? Looks like it’s going to be [random beacons](http://notes.ethereum.org/s/BJc_eGVFM#random-beacons).

It’s interesting that you say a blockchain is analogous to a shard, which is true. However what shall we then call the whole network of shards? A shardnet, perhaps?

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> compute_header_hash(uint256 shard_id, bytes32 parent_hash, bytes32 chunks_root, uint256 period, address proposer_address, uint256 proposer_bid) returns bytes32: Returns the header hash.

Similarly, how does this function work, what’s the code? What’s the hash function, keccak256? AIUI there’s not much benefit in abstracting this.

You have:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Proposer balance: proposer_registry[proposer_address][shard_id] >= max(proposer_bid, MIN_PROPOSER_BALANCE)

But earlier:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> proposer_registry: {deregistered: int128, balances: wei_value[uint256]}[address]—proposer registry

So shouldn’t it be something like Proposer balance: `proposer_registry[proposer_address][shard_id].balance`?

For those who want to learn more about various topics such as those listed in the roadmap, it would be helpful to link to them (perhaps as more information is developed, as the case may be), e.g.:

- Phase 2: EVM state transition function

Full nodes only
- Asynchronous cross-contract calls only
- Account abstraction
- eWASM
- Archive accumulators: History, state, and asynchronous accumulators in the stateless model and Batching and cyclic partitioning of logs and Double-batched Merkle log accumulator
Storage rent

Phase 3: Light client state protocol

- Executors
- State-minimized clients. Stateless clients are not ideal as we don’t want to offload all storage into secondary markets, rather we can give people a choice to pay storage rent on the blockchain or pay for it in secondary markets.

Phase 4: [Cross-shard transactions](http://notes.ethereum.org/s/BJc_eGVFM#cross-shard-communication)

- Internally-synchronous zones: mind map including architectures

Phase 5: Tight coupling with main chain security

- Data availability proofs: A note on data availability and erasure coding, Sharding and data forgetfulness,
- Casper integration: Alpha testnet, papers, wiki post (probably outdated).
- Internally fork-free sharding
- Manager shard

Phase 6: Super-quadratic sharding

- Recursively, shards within shards within shards…
- Load balancing: Wikipedia, search results. Related: History, state, and asynchronous accumulators in the stateless model, State minimized implementation on current evm

And a lot more: [Sharding - Ethereum Research](https://ethresear.ch/c/sharding).

And here’s the above in code to make it easy to copy and paste:

```auto
* Phase 2: EVM state transition function

   * Full nodes only
   * Asynchronous cross-contract calls only
   * [Account abstraction](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-101.md)
   * [eWASM](https://github.com/ewasm/design)
   * Archive accumulators: https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287 and https://ethresear.ch/t/batching-and-cyclic-partitioning-of-logs/536 and https://ethresear.ch/t/double-batched-merkle-log-accumulator/571
Storage rent

* Phase 3: Light client state protocol

   * Executors
   * [Stateless clients](https://ethresear.ch/t/the-stateless-client-concept/172)

* Phase 4: [Cross-shard transactions](http://notes.ethereum.org/s/BJc_eGVFM#cross-shard-communication)

   * Internally-synchronous zones: [mind map including architectures](https://www.mindomo.com/zh/mindmap/sharding-d7cf8b6dee714d01a77388cb5d9d2a01)

* Phase 5: Tight coupling with main chain security

   * Data availability proofs: [A note on data availability and erasure coding](https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding), https://ethresear.ch/t/sharding-and-data-forgetfulness/61,
   * Casper integration: [Alpha testnet](http://notes.ethereum.org/MYEwhswJwMzAtADgCwEYBM9kAYBGJ4wBTETKdGZdXAVmRvUQDYg=?view=), [papers](https://github.com/ethereum/research/tree/master/papers), [wiki post (probably outdated)](https://github.com/ethereum/research/wiki/Casper-Version-1-Implementation-Guide).
   * Internally fork-free sharding
   * Manager shard

* Phase 6: Super-quadratic sharding

   * Recursively, shards within shards within shards...
   * Load balancing: [Wikipedia](https://en.wikipedia.org/wiki/Load_balancing_(computing)), [search results](https://duckduckgo.com/?q=load+balancing&t=canonical&ia=web). Related: https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287, https://ethresear.ch/t/state-minimized-implementation-on-current-evm/1255

And a lot more: https://ethresear.ch/c/sharding.
```

Add a link to the [sharding research compendium](http://notes.ethereum.org/s/BJc_eGVFM).

It would also be helpful for those who may be interested in actually working on an implementation to link to the  [Ethereum wiki list of implementations that are under development or planned](https://github.com/ethereum/wiki/wiki/Sharding-and-stateless-client-implementations).

---

**ldct** (2018-03-16):

> e.g. we no longer have a “VMC” or “validators”

> self-proposal: A proposal for which the proposer is the eligible validator.

did the definition of self-proposal mean to use “collator”?

---

**jannikluhn** (2018-03-16):

Failed to tear it apart, it’s too solid! Just some nitpicks:

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> self-proposal: A proposal for which the proposer is the eligible validator. In a self-proposal the proposer address, bid and signature are omitted.

validator → collator

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> shard ID

Should the shard ID contain (part of) the SMC address? It’s maybe a bit far-fetched, but one could imagine multiple SMCs on the same chain, and in this case the current ID wouldn’t be unique. Mainly worried about some kind of collation replay/slashing, although I don’t think that’s possible with the current spec.

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> chunks tree
> chunks root

I’m not a native English speaker, but I’m wondering if the plural here is correct (same for “transactions” and “receipts root” in current Ethereum, by the way). After all, it’s “apple tree” and not “apples tree”. Some alternatives that come to mind are be “body root/tree” and/or “chunk tree” (“chunk root” doesn’t seem to work either).

---

**jamesray1** (2018-03-16):

Yes, I noticed this too, I think so. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**jamesray1** (2018-03-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> I’m not a native English speaker, but I’m wondering if the plural here is correct (same for “transactions” and “receipts root” in current Ethereum, by the way). After all, it’s “apple tree” and not “apples tree”. Some alternatives that come to mind are be “body root/tree” and/or “chunk tree” (“chunk root” doesn’t seem to work either).

Yes, it probably makes the most sense to have chunk tree, chunk root, receipt root, etc. The alternative would be that the ownership apostrophe is omitted, i.e. chunks’ tree, chunks’ root, receipts’ root, etc. But it is counter-intuitive for the constituent parts to own the whole tree or a root, so chunk tree, chunk root, receipt root, etc. are preferred.

---

**JustinDrake** (2018-03-16):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> I like the reward for collators, it contrasts to no reward for full nodes at the moment.

Collators are not full nodes. They are somewhat like miners in Ethereum 1.0. Full nodes remain unrewarded with sharding.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> It’s good that the entry cost for participation as a proposer is only 0.1 ETH

The entry ticket for a proposer on a single shard is `PROPOSER_DEPOSIT` + `MIN_PROPOSER_BALANCE` which is currently 1.1 ETH.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> collators still need to deposit 1000 ETH (otherwise too many collators would reduce throughput, increase overhead or increase latency)

Too many collators would not reduce throughput (it would allow for collators to secure more shards, i.e. more throughput). What do you mean increase latency? The main reason for having a high deposit is overhead in to main chain from the SMC.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> What mechanism are you going to use for pseudo random selection

We will use blockhashes in phase 1 as described in `get_eligible_collator`. This is imperfect (because of grinding opportunities by miners) but good enough for now. You can find some code for the old spec [here](https://github.com/ethereum/py-evm/blob/eb7138ae67caab09c16d886f59e54639ad97b522/evm/vm/forks/sharding/contracts/validator_manager.v.py#L185).

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> Similarly, how does this function work, what’s the code? What’s the hash function, keccak256? AIUI there’s not much benefit in abstracting this.

It’s just a simple keccak hash on the concatenation of the inputs. Both `get_eligible_collator` and `compute_header_hash` are helper functions added for clarity of exposition. They can be made private.

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> So shouldn’t it be something like Proposer balance: proposer_registry[proposer_address][shard_id].balance?

Well spotted ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12) I fixed it to `proposer_registry[proposer_address].balances[shard_id]`.

![](https://ethresear.ch/user_avatar/ethresear.ch/ldct/48/281_2.png) ldct:

> did the definition of self-proposal mean to use “collator”?

Well spotted, fixed ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> Should the shard ID contain (part of) the SMC address?

If we need a new SMC then the `NETWORK_ID` (part of the shard ID) will be updated. I have added `SMC_ADDRESS` to the list of parameters.

![](https://ethresear.ch/user_avatar/ethresear.ch/jannikluhn/48/300_2.png) jannikluhn:

> I’m not a native English speaker, but I’m wondering if the plural here is correct (same for “transactions” and “receipts root” in current Ethereum, by the way).

I’m not a native English speaker either but I think you may be right. I’ve followed your suggestion.

---

**jamesray1** (2018-03-16):

OK thanks for clarifying. I have read the old spec but thought there may be differences in the latest spec.

For latency, I meant the time to gossip a collation to the rest of the network. But more collators does not necessarily mean increased latency.

I edited my initial comment to add:

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> It’s interesting that you say a blockchain is analogous to a shard, which is true. However what shall we then call the whole network of shards? A shardnet, perhaps?

---

**jamesray1** (2018-03-17):

What differences do you think the phase 2 EVM will be to Py-EVM and Serenity? I am reading through [History, state, and asynchronous accumulators in the stateless model](https://ethresear.ch/t/history-state-and-asynchronous-accumulators-in-the-stateless-model/287) and am getting at least part of an answer.

---

**mhchia** (2018-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> get_eligible_collator(uint256 shard_id, uint256 period) returns address: Uses the blockhash at block number (period - LOOKAHEAD_LENGTH) * PERIOD_LENGTH) and shard_id to pseudo-randomly select an eligible collator from the collator registry, and returns the address of the eligible collator. Checks:

Just want to confirm, is the collator selected from the collator registry or collator pool? ![:slightly_smiling_face:](https://ethresear.ch/images/emoji/facebook_messenger/slightly_smiling_face.png?v=12)

---

**JustinDrake** (2018-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> What differences do you think the phase 2 EVM will be to Py-EVM and Serenity?

There will a be bunch misc significant differences (some of which I listed as candidates in the phase 2 roadmap, including asynchronous cross-contract calls only, account abstraction, eWASM, archive accumulators, storage rent). I expect these differences to add up to a totally different EVM implementation, although a lot of the differences may abstracted away in the higher level programming languages.

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Just want to confirm, is the collator selected from the collator registry or collator pool?

That should be collator pool, thanks! Fixed ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**cspannos** (2018-03-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> proposer signature: The proposer’s signature as part of a proposal.

This may be silly, but, should/could this be the signature of a proposer at a given address in a proposal? Or is that overkill? I wonder because proposer address is spelled out in more detail and it made me think that this term could be more complete. But this may be unnecessary.

---

**mhchia** (2018-03-19):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> proposal_commitment_slashing(uint256 shard_id, bytes32 collation_hash, uint256 height, uint256 left_hash, uint256 right_hash, bytes signature) returns bool: Slashes a collator that called add_header with a non-committed proposal. Checks:
>
>
> Shard: shard_id against NETWORK_ID and SHARD_COUNT
>
>
> Collation tree: collation_trees[shard_id][collation_hash] exists
>
>
> Height: collation_trees[shard_id][collation_hash] matches height
>
>
> Signature: signature matches height, left_hash and right_hash
>
>
> Slashing condition: left_hash
>
> availability_challenge(): TBD
>
>
> availability_response(): TBD
>
>
> proposal_commitment_slashing(): TBD

Is the last `proposal_commitment_slashing` duplicate?

---

**kladkogex** (2018-03-19):

I think it is a very good start! Now the devil will be in the details ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=9)

Cryptoeconomic proofs will be a nontrivial part since the current version Truebit protocol is only weakly secure !

Also imho protecting aganst frontrunning attacks will be a big issue across all components of the system.

---

**skilesare** (2018-03-20):

Please help with what I’m missing here, but I don’t understand Phase 1.  What good are collations without state transitions? What are you collating?  Why would anyone submit a Blob if that blob isn’t going to actually do anything?

---

**JustinDrake** (2018-03-20):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/c/ebca7d/48.png) cspannos:

> could this be the signature of a proposer at a given address in a proposal?

I’m not sure I understand. Do you mean that the proposer address could be part of the proposal body as opposed to the proposal header?

![](https://ethresear.ch/user_avatar/ethresear.ch/mhchia/48/643_2.png) mhchia:

> Is the last proposal_commitment_slashing duplicate?

Fxed ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> current version Truebit protocol is only weakly secure

Phase 1 has no TrueBit protocol. Do you mean the phase 3 [execution game with executors](https://ethresear.ch/t/delayed-state-execution-in-practice/1041)? If so, why is weakly secure?

![](https://ethresear.ch/user_avatar/ethresear.ch/skilesare/48/336_2.png) skilesare:

> What good are collations without state transitions?

We’re reducing consensus to its core: data availability. Execution (transactions, state, state transitions, validity, state roots, …) is a simpler deterministic execution game (*not* a consensus game). The default execution engine (the sharded EVM) will be added in phase 2, and will provide “meaning” to blobs that pay gas fees to use the EVM.

Alternative execution engines are possible, and this is facilitated by the natural evolution of consensus abstraction. Taking a historical perspective:

- Bitcoin (think “ASIC”)

Enshrined-in-consensus dApp
- Account abstraction

Ethereum 1.0 (think “CPU”)

- Enshrined-in-consensus dApp engine
- dApp abstraction

Ethereum 2.0 (think “FPGA”)

- Enshrined-in-consensus data availability
- dApp engine abstraction

---

**kladkogex** (2018-03-22):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Phase 1 has no TrueBit protocol. Do you mean the phase 3 execution game with executors? If so, why is weakly secure?

I think I worded myself wrong … It may be super strongly secure ![:smiling_imp:](https://ethresear.ch/images/emoji/facebook_messenger/smiling_imp.png?v=12)  What I meant is we need a document that analyzes possibilities of front running attacks throughout the system.

If some agent is paid for some work, there is always a possibility for someone else steal the submission and get paid.  Since there is lots of money potentially involved, in my opinion every single potential vulnerability needs to be analyzed.

IMHO Ethereum needs to stand out and be different by tightly addressing security. There are many projects on the market that imho will crash and fail by not addressing security seriously enough.

For the execution game with executors

“Here is one simple proposal. Allow anyone with ETH in any shard to deposit their ETH (with a 4 month lockup period), and at certain points (eg. once every Casper epoch) give depositors the ability to make claims about the state at some given height. These claims can be published into the blockchain. The claims would be of the form [height, shard, state_root, signature]. From the point of view of a node executing the state, a correct claim is given some reward proportional to the deposit (eg. corresponding to an interest rate of 5%), and a false claim means the claimer is penalized.”

Is this vulnerable to front running? Judging from  the description it could be, since I  could do no work, and simply intercept and resubmit someone else’s claim …

This is a particular example, though. A more general question though is should we have a separate document listing all potential vulnerabilities/weaknesses of the protocols and their impact from low to high.

---

**vbuterin** (2018-03-22):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> Is this vulnerable to front running? Judging from  the description it could be, since I  could do no work, and simply intercept and resubmit someone else’s claim …

Yes, but if you front-run by copying another executor then you’re exposing yourself to a griefing attack from that executor voluntarily burning some portion of their deposit to burn yours. Though I do agree that these kinds of issues absolutely need to be fully considered.

---

**jamesray1** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> Proposer registry
>
>
> proposer_registry: {deregistered: int128, balances: wei_value[uint256]}[address]—proposer registry

I need to figure out how to implement this in Rust, where a struct accepts an address as an argument. Cross-posting this at https://gitter.im/Drops-of-Diamond/Lobby?at=5ab485e45f188ccc15e8c909, Rust-specific discussion can be had there.

---

**jamesray1** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> collator_pool: address[int128]

AIUI this is saying that address is an int128 type, but in current implementations it is a binary data of length 160 bits.

---

**jamesray1** (2018-03-23):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> empty_slots_stack: int128[int128]—stack of empty collator slot indices
>
>
> empty_slots_stack_top: int128—top index of the stack

I’ll just define this like so for now:

```rust
	struct CollatorPool {
		collator_pool_len: int128,
			// size of the collator pool
		collator_pool: [Address; collator_pool_len],
			// array of active collator addresses
		empty_slots_stack_depth: int128,
		empty_slots_stack: [int128; empty_slots_stack_depth],
			// stack of empty collator slot indices
		empty_slots_stack_top: int128,		// top index of the stack
	}
```

What is the depth of `empty_slots_stack`? Is it 1024 words = 1024 *32 bytes like the current stack depth?

Or should `empty_slots_stack: int128[int128]` actually be written in Rust like `empty_slots_stack: HashMap<H128, H128>`?


*(68 more replies not shown)*
