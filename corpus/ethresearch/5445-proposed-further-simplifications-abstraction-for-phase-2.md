---
source: ethresearch
topic_id: 5445
title: Proposed further simplifications/abstraction for phase 2
author: vbuterin
date: "2019-05-13"
category: Sharded Execution
tags: []
url: https://ethresear.ch/t/proposed-further-simplifications-abstraction-for-phase-2/5445
views: 5849
likes: 0
posts_count: 7
---

# Proposed further simplifications/abstraction for phase 2

Background:

- A layer-1-minimizing phase 2 state execution proposal
- An Optimistic Generic Gas Market Executor for Phase 2
- Phase One and Done: eth2 as a data availability engine

Here is another proposal for phase 2 that’s halfway in between my earlier one ( [#5397](https://ethresear.ch/t/a-layer-1-minimizing-phase-2-state-execution-proposal/5397) ) and Casey’s “phase one and done” proposal.

- For each execution environment, we store an array states: List[{slot: slot, value: bytes32}, SHARD_COUNT] in the beacon chain (execution environments could restrict themselves to fewer shards to cut storage reqs and hence deployment costs), which starts at zero for each shard.
- Every shard block specifies which execution environment E is intended to execute it (this is the choice of the proposer)
- Each shard chain also stores a data structure shard.states: Map[int -> {slot: slot, value: bytes32}] which stores states for different execution environment. The goal of this data structure is to only store states that are newer than those stored in the beacon chain.
- The “current state” cur_state(shard, exec_env) -> Bytes32 can be computed via shard.states[E].value if E in shard.states and shard.states[E].slot > beacon_chain.envs[E].states[s].slot else beacon_chain.envs[E].states[s].value. That is, take the newest record available, whether it’s from the shard or the beacon chain.
- When a block appears in a shard s specifying execution environment E, then let pre_state = current_state(s, e). Compute post_state = exec(beacon_chain.envs[E].code, pre_state, block_data) and save shard.states[E] = {slot: current_slot, value: post_state}.
- The full contents of shard.states should be included in any crosslink, and if a crosslink is accepted, these values should be included into the beacon chain.
- If a shard execution sees that the beacon chain’s record for an execution environment is the same as that of the shard, it should remove the record from the shard (this lets the shard states decrease in size over time)

The goal here is that the consensus-layer state per shard is reduced to only 32 bytes per execution environment, and this is all stored in the beacon chain; the shards don’t have a significant concept of state on their own.

In practice, this would mean that there would be a two-layer structure for users, [as described here](https://ethresear.ch/t/an-optimistic-generic-gas-market-executor-for-phase-2/5429/2). Roughly:

- Users send transactions.
- An execution environment specific class of actor called a relayer packages up these transactions and adds Merkle proofs. They rebroadcast the packages and pass along a fee to the proposer.
- Block proposers accept the package that pays them the most.

The execution environment’s code could use the 32 byte state field to store a state root, and verify Merkle proofs provided by the relayer to implement state transitions. The concept of “full state” would be an execution-environment-specific higher-level concept.

#### Advantages

- We can merge the crosslink and persistent committees into one, halving the amount of in-consensus verification that we need to do (the verification doesn’t quite halve, because the verification we’re removing would be the cheaper persistent stateful verification rather than the more expensive persistent stateless variety, but it’s still a gain…). The merged committees could have a rotation period of eg. 1-3 hours.
- We remove the need to specify the Merkle tree structure in-protocol, allowing execution-environment-layer experimentation in: different kinds of Merkle trees (SMTs, red-black trees, etc…), using SNARKs or STARKs to compress Merkle witnesses, accumulators other than Merkle trees (RSA accumulators, etc)
- The decision of what rent scheme to use gets pushed up to execution environments to decide

### Disadvantages

- More stuff to formally verify (alternatively, we could agree that for some limited time, execution environments are subject to low-controversy DAO-style rescue forks)

## Replies

**vbuterin** (2019-05-14):

If we want to avoid the complexity of bouncing state back and forth to the beacon chain, we could also keep the state exclusively inside the shard chains. So each shard would have a state `Bytes32` per execution environment, and this would need to be downloaded, but this state could be kept at most a few megabytes total, so we could use a fairly dumb syncing algorithm to download it. This could also allow exec environments to pay more for more per-shard storage, which could enable reducing proof sizes a bit (eg. if you get a kilobyte per shard, then you can lop off the top five levels of the merkle tree).

---

**vbuterin** (2019-05-14):

I should add that one way that this scheme decreases **total** simplicity is that by layer-2-ifying application state and hence the question of rent, it allows for constructions where some key storage items are exempt from rent (eg. this might make sense for a spent-receipt bitfield), removing the need for complicated constructions that involve recursive bitfields for spent receipts of bitfields as we had in the earlier scheme.

---

**villanuevawill** (2019-05-14):

A quick question here - if relayers or other third party markets manage state, why would rent still be at layer 2 vs. managed by those systems - could you clarify? This would remove the need for poking as well or would poking still be included to discourage reliance on third party/relay state bloat?

---

**vbuterin** (2019-05-14):

You definitely could have the application state be rent-free and permanent. The only challenge there is that either being a relayer becomes expensive with the ever-growing storage requirements or users need to store their own state in which case there’s complexities around what happens if some address range becomes unavailable. So I’d suspect that a hibernation scheme is optimal, though perhaps you could reduce the complexity by having the bitfields be permanent.

---

**ryanreich** (2019-05-28):

Is the idea of the `states` field that the list you show for each execution environment gives a different state for each shard? So the shards’ executions so not interact (no cross-shard calls, that is).

---

**vbuterin** (2019-05-28):

> Is the idea of the states field that the list you show for each execution environment gives a different state for each shard?

Yep!

