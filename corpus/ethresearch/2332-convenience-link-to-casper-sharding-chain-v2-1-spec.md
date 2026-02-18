---
source: ethresearch
topic_id: 2332
title: Convenience link to Casper+Sharding chain v2.1 spec
author: vbuterin
date: "2018-06-23"
category: Sharding
tags: []
url: https://ethresear.ch/t/convenience-link-to-casper-sharding-chain-v2-1-spec/2332
views: 12799
likes: 13
posts_count: 17
---

# Convenience link to Casper+Sharding chain v2.1 spec

**2018/08/20 updated: 2018/08/19 00:12 AM (GMT) version**

https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ

---

Repost of the content (warning: may accidentally become outdated):

# Casper+Sharding chain v2.1

## WORK IN PROGRESS!!!

This is the work-in-progress document describing the specification for the Casper+Sharding (shasper) chain, version 2.1.

In this protocol, there is a central PoS chain which stores and manages the current set of active PoS validators. The only mechanism available to become a validator initially is to send a transaction on the existing PoW main chain containing 32 ETH. When you do so, as soon as the PoS chain processes that block, you will be queued, and eventually inducted as an active validator until you either voluntarily deregister or you are forcibly deregistered as a penalty for misbehavior.

The primary source of load on the PoS chain is **attestations**. An attestation has a double role:

1. It attests to some parent block in the beacon chain
2. It attests to a block hash in a shard (a sufficient number of such attestations create a “crosslink”, confirming that shard block into the main chain).

Every shard (e.g. there might be 1024 shards in total) is itself a PoS chain, and the shard chains are where the transactions and accounts will be stored. The crosslinks serve to “confirm” segments of the shard chains into the main chain, and are also the primary way through which the different shards will be able to talk to each other.

Note that one can also consider a simpler “minimal sharding algorithm” where crosslinks are simply hashes of proposed blocks of data that are not themselves chained to each other in any way.

Note: the python code at https://github.com/ethereum/beacon_chain and [an ethresear.ch post](https://ethresear.ch/t/convenience-link-to-full-casper-chain-v2-spec/2332) do not reflect all of the latest changes. If there is a discrepancy, this document is likely to reflect the more recent changes.

### Terminology

- Validator - a participant in the Casper/sharding consensus system. You can become one by depositing 32 ETH into the Casper mechanism.
- Active validator set - those validators who are currently participating, and which the Casper mechanism looks to produce and attest to blocks, crosslinks and other consensus objects.
- Committee - a (pseudo-) randomly sampled subset of the active validator set. When a committee is referred to collectively, as in “this committee attests to X”, this is assumed to mean “some subset of that committee that contains enough validators that the protocol recognizes it as representing the committee”.
- Proposer - the validator that creates a block
- Attester - a validator that is part of a committee that needs to sign off on a block.
- Beacon chain - the central PoS chain that is the base of the sharding system.
- Shard chain - one of the chains on which transactions take place and account data is stored.
- Crosslink - a set of signatures from a committee attesting to a block in a shard chain, which can be included into the beacon chain. Crosslinks are the main means by which the beacon chain “learns about” the updated state of shard chains.
- Slot - a period of 8 seconds, during which one proposer has the ability to create a block and some attesters have the ability to make attestations
- Dynasty transition - a change of the validator set
- Dynasty - the number of dynasty transitions that have happened in a given chain since genesis
- Cycle - a period during which all validators get exactly one chance to vote (unless a dynasty transition happens inside of one)
- Finalized, justified - see Casper FFG finalization here: https://arxiv.org/abs/1710.09437

### Constants

- SHARD_COUNT - a constant referring to the number of shards. Currently set to 1024.
- DEPOSIT_SIZE - 32 ETH
- MAX_VALIDATOR_COUNT - 222 = 4194304 # Note: this means that up to ~134 million ETH can stake at the same time
- SLOT_DURATION - 8 seconds
- CYCLE_LENGTH - 64 slots
- MIN_COMMITTEE_SIZE - 128 (rationale: see recommended minimum 111 here https://vitalik.ca/files/Ithaca201807_Sharding.pdf)

### PoW main chain changes

This PoS/sharding proposal can be implemented separately from the existing PoW main chain. Only two changes to the PoW main chain are required (and the second one is technically not strictly necessary).

- On the PoW main chain a contract is added; this contract allows you to deposit DEPOSIT_SIZE ETH; the deposit function also takes as arguments (i) pubkey (bytes), (ii) withdrawal_shard_id (int), (iii)  withdrawal_addr (address), (iv) randao_commitment (bytes32), (v) bls_proof_of_possession
- PoW Main chain clients will implement a method, prioritize(block_hash, value). If the block is available and has been verified, this method sets its score to the given value, and recursively adjusts the scores of all descendants. This allows the PoS beacon chain’s finality gadget to also implicitly finalize main chain blocks. Note that implementing this into the PoW client is a change to the PoW fork choice rule so is a sort of fork.

### Beacon chain

The beacon chain is the “main chain” of the PoS system. The beacon chain’s main responsibilities are:

- Store and maintain the set of active, queued and exited validators
- Process crosslinks (see above)
- Process its own block-by-block consensus, as well as the finality gadget

Here are the fields that go into every beacon chain block:

```python
fields = {
    # Hash of the parent block
    'parent_hash': 'hash32',
    # Slot number (for the PoS mechanism)
    'slot_number': 'int64',
    # Randao commitment reveal
    'randao_reveal': 'hash32',
    # Attestations
    'attestations': [AttestationRecord],
    # Reference to PoW chain block
    'pow_chain_ref': 'hash32',
    # Hash of the active state
    'active_state_root': 'hash32',
    # Hash of the crystallized state
    'crystallized_state_root': 'hash32',
}
```

The beacon chain state is split into two parts, *active state* and *crystallized state*.

Here’s the `ActiveState`:

```python
fields = {
    # Attestations that have not yet been processed
    'pending_attestations': [AttestationRecord],
    # Most recent 2 * CYCLE_LENGTH block hashes, older to newer
    'recent_block_hashes': ['hash32']
}
```

Here’s the `CrystallizedState`:

```python
fields = {
    # List of validators
    'validators': [ValidatorRecord],
    # Last CrystallizedState recalculation
    'last_state_recalc': 'int64',
    # What active validators are part of the attester set
    # at what height, and in what shard. Starts at slot
    # last_state_recalc - CYCLE_LENGTH
    'indices_for_slots': [[ShardAndCommittee]],
    # The last justified slot
    'last_justified_slot': 'int64',
    # Number of consecutive justified slots ending at this one
    'justified_streak': 'int64',
    # The last finalized slot
    'last_finalized_slot': 'int64',
    # The current dynasty
    'current_dynasty': 'int64',
    # The next shard that crosslinking assignment will start from
    'crosslinking_start_shard': 'int16',
    # Records about the most recent crosslink `for each shard
    'crosslink_records': [CrosslinkRecord],
    # Total balance of deposits
    'total_deposits': 'int256',
    # Used to select the committees for each shard
    'dynasty_seed': 'hash32',
    # Last epoch the crosslink seed was reset
    'dynasty_seed_last_reset': 'int64'
}
```

A `ShardAndCommittee` object is of the form:

```python
fields = {
    # The shard ID
    'shard_id': 'int16',
    # Validator indices
    'committee': ['int24']
}
```

Each ValidatorRecord is an object containing information about a validator:

```python
fields = {
    # The validator's public key
    'pubkey': 'int256',
    # What shard the validator's balance will be sent to
    # after withdrawal
    'withdrawal_shard': 'int16',
    # And what address
    'withdrawal_address': 'address',
    # The validator's current RANDAO beacon commitment
    'randao_commitment': 'hash32',
    # Current balance
    'balance': 'int64',
    # Dynasty where the validator  is inducted
    'start_dynasty': 'int64',
    # Dynasty where the validator leaves
    'end_dynasty': 'int64'
}
```

And a CrosslinkRecord contains information about the last fully formed crosslink to be submitted into the chain:

```python
fields = {
    # What dynasty the crosslink was submitted in
    'dynasty': 'int64',
    # The block hash
    'hash': 'hash32'
}
```

### Beacon chain processing

Processing the beacon chain is fundamentally similar to processing a PoW chain in many respects. Clients download and process blocks, and maintain a view of what is the current “canonical chain”, terminating at the current “head”. However, because of the beacon chain’s relationship with the existing PoW chain, and because it is a PoS chain, there are differences.

For a block on the beacon chain to be processed by a node, three conditions have to be met:

- The parent pointed to by the parent_hash has already been processed and accepted
- The PoW chain block pointed to by the pow_chain_ref has already been processed and accepted
- The node’s local clock time is greater than or equal to the minimum timestamp as computed by GENESIS_TIME + slot_number * SLOT_DURATION

If these three conditions are not met, the client should delay processing the block until the three conditions are all satisfied.

Block production is significantly different because of the proof of stake mechanism. A client simply checks what it thinks is the canonical chain when it should create a block, and looks up what its slot number is; when the slot arrives, it either proposes or attests to a block as required.

### Beacon chain fork choice rule

The beacon chain uses the Casper FFG fork choice rule of “favor the chain containing the highest-epoch justified checkpoint”. To choose between chains that are all descended from the same justified checkpoint, the chain uses “recursive proximity to justification” (RPJ) to choose a checkpoint, then uses GHOST within an epoch.

For a description see: **[Beacon chain Casper mini-spec](https://ethresear.ch/t/beacon-chain-casper-ffg-rpj-mini-spec/2760)**

For an implementation with a network simulator see: **https://github.com/ethereum/research/blob/master/clock_disparity/ghost_node.py**

Here’s an example of its working (green is finalized blocks, yellow is justified, grey is attestations):

![image](https://vitalik.ca/files/RPJ.png)

## Beacon chain state transition function

We now define the state transition function. At the high level, the state transition is made up of two parts:

1. The crystallized state realculation, which happens only if block.slot_number >= last_state_recalc + CYCLE_LENGTH, and affects the CrystallizedState and ActiveState
2. The per-block processing, which happens every block (if during an epoch transition block, it happens after the epoch transition), and affects the ActiveState only

The epoch transition generally focuses on changes to the validator set, including adjusting balances and adding and removing validators, as well as processing crosslinks and setting up FFG checkpoints, and the per-block processing generally focuses on verifying aggregate signatures and saving temporary records relating to the in-block activity in the `ActiveState`.

### Helper functions

We start off by defining some helper algorithms. First, the function that selects the active validators:

```python
def get_active_validator_indices(validators, dynasty):
    o = []
    for i in range(len(validators)):
        if validators[i].start_dynasty = CYCLE_LENGTH * MIN_COMMITTEE_SIZE:
        committees_per_slot = int(len(avs) // CYCLE_LENGTH // (MIN_COMMITTEE_SIZE * 2)) + 1
        slots_per_committee = 1
    else:
        committees_per_slot = 1
        slots_per_committee = 1
        while len(avs) * slots_per_committee = max(block.slot_number - CYCLE_LENGTH, 0)
- Compute parent_hashes = [get_block_hash(crystallized_state, active_state, block, slot - CYCLE_LENGTH + i) for i in range(CYCLE_LENGTH - len(oblique_parent_hashes))] + oblique_parent_hashes
- Let attestation_indices be get_indices_for_slot(crystallized_state, active_state, slot)[x], choosing x so that attestation_indices.shard_id equals the shard_id value provided to find the set of validators that is creating this attestation record.
- Verify that len(attester_bitfield) == ceil_div8(len(attestation_indices)), where ceil_div8 = (x + 7) // 8. Verify that bits len(attestation_indices).... and higher, if present (i.e. len(attestation_indices) is not a multiple of 8), are all zero
- Derive a group public key by adding the public keys of all of the attesters in attestation_indices for whom the corresponding bit in attester_bitfield (the ith bit is (attester_bitfield[i // 8] >> (7 - (i %8))) % 2) equals 1
- Verify that aggregate_sig verifies using the group pubkey generated and hash((slot % CYCLE_LENGTH).to_bytes(8, 'big') + parent_hashes + shard_id + shard_block_hash) as the message.

Extend the list of `AttestationRecord` objects in the `active_state`, ordering the new additions in the same order as they came in the block.

Verify that the `slot % len(get_indices_for_slot(crystallized_state, active_state, slot-1)[0])`'th attester in `get_indices_for_slot(crystallized_state, active_state, slot-1)[0]`is part of at least one of the `AttestationRecord` objects; this attester can be considered to be the proposer of the block.

### State recalculations

Repeat while `slot - last_state_recalc >= CYCLE_LENGTH`:

For all slots `s` in `last_state_recalc - CYCLE_LENGTH ... last_state_recalc - 1`:

- Determine the total set of validators that voted for that block at least once
- Determine the total balance of these validators. If this value times three equals or exceeds the total balance of all active validators times two, set last_justified_slot = max(last_justified_slot, s) and justified_streak += 1. Otherwise, set justified_streak = 0
- If justified_streak >= CYCLE_LENGTH + 1, set last_finalized_slot = max(last_finalized_slot, s - CYCLE_LENGTH - 1)
- Remove all attestation records older than slot last_state_recalc

Also:

- Set last_state_recalc += CYCLE_LENGTH
- Set indices_for_slots[:CYCLE_LENGTH] = indices_for_slots[CYCLE_LENGTH:]

For all (`shard_id`, `shard_block_hash`) tuples, compute the total deposit size of validators that voted for that block hash for that shard. If this value times three equals or exceeds the total balance of all validators in the committee times two, and the current dynasty exceeds `crosslink_records[shard_id].dynasty`, set `crosslink_records[shard_id] = CrosslinkRecord(dynasty=current_dynasty, hash=shard_block_hash)`.

TODO:

- Rewards for FFG participation
- Rewards for committee participation

### Dynasty transition

TODO. Stub for now.

---

Note: this is ~70% complete. Main sections missing are:

- Validator login/logout logic
- Logic for the formats of shard chains, who proposes shard blocks, etc. (in an initial release, if desired we could make crosslinks just be Merkle roots of blobs of data; in any case, one can philosophically view the whole point of the shard chains as being a coordination device for choosing what blobs of data to propose as crosslinks)
- Logic for inducting queued validators from the main chain
- Penalties for signing or attesting to non-canonical-chain blocks (update: may not be necessary, see Attestation committee based full PoS chains)
- Slashing conditions
- Logic for withdrawing deposits to shards
- Per-validator proofs of custody
- Full rewards and penalties
- Versioning and upgrades

Slashing conditions may include:

```
Casper FFG height equivocation
Casper FFG surround
Beacon chain proposal equivocation
Shard chain proposal equivocation
Proof of custody secret leak
Proof of custody wrong custody bit
Proof of custody no secret reveal
RANDAO leak
```

## Replies

**jamesray1** (2018-06-24):

What’s the rationale for choosing RANDAO over BLS?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The node’s local clock time is greater than or equal to the minimum timestamp as computed by GENESIS_TIME + height * PER_HEIGHT_DELAY + total_skips * PER_SKIP_DELAY

Given that computers can have a time that is not exact if not synchronized via the internet, perhaps it would be better to state that the local node time must be in sync with some reliable source(s) of time, e.g. https://time.is (obviously such time servers are centralised so requiring to be in sync with multiple time sources is better, and some decentralised time provider is better still). ~~Haven’t read all of it yet.~~

---

**vbuterin** (2018-06-24):

Mainly that the various “50% collective” beacons (i) have much higher complexity, including fundamentally new message sending patterns like DKG algorithms, (ii) don’t preserve the desideratum that the chain should be able to progress at some rate with an arbitrarily small number of nodes online.

You can show from simulation arguments that any system that satisfies (ii), and does not have time delay crypto, is vulnerable to the same types of simulation arguments and other issues as RANDAO is.

---

**kladkogex** (2018-06-26):

Is there an approximate target of what the transactions per second for this network will be ? Is this going to be 100 tps ? 1000 tps? I think  this should influence many design decisions network-wise.

---

**fubuloubu** (2018-06-27):

Napkin calculation: 4000 shards x 15 tps = 60k tps. That assumes current block propogation rates. 4000 shards is probably the limit assuming 4 transactions per shard per epoch (16000 txns / [15 tps * 15 s per block] / 100 blks per epoch = 70% utilization).

If plasma is widely used, then that number can probably be squared to 3.6b tps for the upper limit of the entire network. This is probably 99% overly optimistic, so I would say 36m tps. Although, can’t a PoS validator system have faster propagation rates than PoW and thus per-shard rates are faster? Then these numbers skew more wildly.

No idea if this is the right line of thinking, just guessing how to build these new numbers. 1m+ tps would still probably be expensive at full adoption™, 10m-100m+ would be ideal.

---

**vbuterin** (2018-06-27):

Those numbers are basically correct in terms of what “the dream” is. Vlad would probably prefer going above 1M TPS at base chain level by sharding super-quadratically; I am increasingly less and less convinced that super-quadratic sharding at base level is even desirable.

---

**quickBlocks** (2018-06-27):

I’ve been paying relatively close attention to the scaling conversations, and while I can’t say I understand everything, I do get the basic idea: many, many more transactions per second.

At the same time, I’m in the Open Source Blockchain Explorer discussions where people are discussing how users (developers and regular end users) can better get the data off of the amazing “shared global ledger.” Currently, getting per account transaction data (fast, accurate, full transaction lists per account) is possible only through third parties such as EthScan (a 100% centralized and closed system). Or, it’s ad hoc by each development team using Event logs (which isn’t fully accurate because it ignores failed transactions and doesn’t work for non-smart-contracts). Wallets don’t really help either because they ignore incoming calls (incoming internal transactions).

Has there been discussions about how an open source blockchain explorer (or similar analytics platforms) would even work in the face of millions of transactions/second. Are there pointers to this discussion or ideas about how this might work in a decentralized way? How would such systems stay decentralized in the face of such hugely increasing costs?

Perhaps this is off-topic for this thread, but I think it’s an important discussion.

---

**fubuloubu** (2018-06-27):

It will definitely be a service, data analytics on this infrastructure is no joke, and that will only become a more profitable business plan with time.

I’d be more worried with how this all looks with sharded chains. If we have this much problems with 1 chain, imagine how 4000 is going to look? How does a world of Plasma chains play into that?

I do not envy you my friend ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9) lol

---

**quickBlocks** (2018-06-27):

I’m actually making the point that if the only way to effectively get the data that has already been consented to is through third parties, we will have created a system that is not only not better, but significantly worse than the current system. The data aggregators will have much more intimate and accurate data, or if the data gets encrypted vis-a-vi something like zcash, then blockchain explorers become useless. So the question remains “how do people get their own data without having to pay for it?” I agree, sharded chains make it a million times harder. I’m making the further point that the design for sharding should address this issue given the heavy reliance the current ecosystem places on third party data deliver such as EtherScan.

---

**jamesray1** (2018-06-28):

Regarding time, just watched this:

  [![image](https://ethresear.ch/uploads/default/original/3X/0/c/0cf29e495834b255d5cad4f79257c9400b70811f.jpeg)](https://www.youtube.com/watch?v=phXohYF0xGo)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I am increasingly less and less convinced that super-quadratic sharding at base level is even desirable.

Would you care to elaborate on that, or point to where you’ve elaborated on that? Personally I tend to agree with Vlad and prefer exponential sharding over L2 solutions, which reduce the security of L1 (I’m quoting Vlad). Of course, exponential sharding needs much more R&D, and is really not much more than an idea at this stage.

![](https://ethresear.ch/user_avatar/ethresear.ch/quickblocks/48/406_2.png) quickBlocks:

> Has there been discussions about how an open source blockchain explorer (or similar analytics platforms) would even work in the face of millions of transactions/second. Are there pointers to this discussion or ideas about how this might work in a decentralized way? How would such systems stay decentralized in the face of such hugely increasing costs?

Prysmatic Labs has been working on data visualization for sharding, with the intention of having a team working on a block explorer. They’re developing a backend spec for sharding clients to comply with, which will feed into the explorer. Cc [@prestonvanloon](/u/prestonvanloon) and [@rauljordan](/u/rauljordan). [Design Spec for a Sharding Visualization Front-End · Issue #94 · OffchainLabs/prysm · GitHub](https://github.com/prysmaticlabs/geth-sharding/issues/94)

---

**vbuterin** (2018-06-28):

> Would you care to elaborate on that, or point to where you’ve elaborated on that? Personally I tend to agree with Vlad and prefer exponential sharding over L2 solutions, which reduce the security of L1 (I’m quoting Vlad). Of course, exponential sharding needs much more R&D, and is really not much more than an idea at this stage.

A few issues:

1. With signature aggregation (BLS, STARKs, etc) it’s becoming practical for quadratic sharding to scale up to a much larger set of shards (4096 is theoretically possible, see the latest spec). With a bit more of Moore’s law, I can see it being possible to get to 100k+ TPS with quadratic sharding alone.
2. Extreme forms of sharding have two risks: (i) the risk that any structure that depends on fraud proofs or other forms of interactive verification works less and less, because there are more and more objects to potentially verify and so it’s easier and easier to DDoS, and (ii) it requires as a security assumption that the network has at least some minimal node count that gets larger and larger as the number of shards goes up.
3. Increasing protocol complexity is bad.

---

**fubuloubu** (2018-06-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> L2 solutions, which reduce the security of L1

How does L2 reduce security of L1?

---

**jamesray1** (2018-06-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/fubuloubu/48/2424_2.png) fubuloubu:

> How does L2 reduce security of L1?

See [Sharding FAQs · ethereum/wiki Wiki · GitHub](https://github.com/ethereum/wiki/wiki/Sharding-FAQs#how-does-plasma-state-channels-and-other-layer-2-technologies-fit-into-the-trilemma).

---

**jamesray1** (2018-06-29):

Fair enough. I guess if we ever get to a point with IoT and lots of other stuff being used on Ethereum, such that the network gets full with 4096 shards and 100k+ tps, we could then do R&D on exponential sharding, if not before.

---

**fubuloubu** (2018-06-29):

Ah, I misinterpreted. I thought that somehow meant “involving L2 affects L1 security” instead of “L2 has less security than L1, assets on L1 can be affected negatively”

---

**chfast** (2018-07-17):

Outdated! Please update the content.

---

**Hackdom** (2018-09-07):

I missed details of the windback if they’re present. Is there a set number of collations that validators will windback? Also, there’s the condition where a validator spots an invalid collation through this process and forks. Is there a process to maintain the ‘invalid’ collation so that, if the next validator deems the forked chain as invalid, it can look to see if the previously ‘invalid’ collation was in fact valid in the first place?

