---
source: ethresearch
topic_id: 18666
title: Paths to hardening PBS
author: fradamt
date: "2024-02-13"
category: Proof-of-Stake > Economics
tags: [mev]
url: https://ethresear.ch/t/paths-to-hardening-pbs/18666
views: 2219
likes: 8
posts_count: 1
---

# Paths to hardening PBS

*Thanks to Alex Stokes, Anders Elowsson and Potuz for feedback*

The goal of this post is to explore some ways we can improve the guarantees of PBS as it currently exist in Ethereum, as an alternative to full enshrinement, which risks prematurely committing to a solution that is far from being universally recognized as the right one.

We first discuss a relatively small change to the status quo, which introduces a gossip topic to observe part of the mev-boost auction, allowing validators to reliably keep track of relay performance and disconnect from specific relays if necessary.

We then discuss some potential deeper changes to the protocol, which still fall short of full epbs enshrinement, with the goal of allowing beacon blocks to exist even without execution payloads, so that a mev-boost failure affects the progress of the EL but not the CL.

## Observing the exchange: hardening mev-boost through gossip

### Basics of the mev-boost exchange

The [builder specs](https://github.com/ethereum/builder-specs/blob/18c435e360192aa39c378584fe14a3158f30dfbf/specs/bellatrix/builder.md) define a bid object to be sent from a relay to a connected validator. It contains a bid value, the pubkey of the relay and the `ExecutionPayloadHeader` corresponding to the `ExecutionPayload` that the builder intends to sell to the validator.

```python
class BuilderBid(Container):
    header: ExecutionPayloadHeader
    value: uint256
    pubkey: BLSPubkey

class SignedBuilderBid(Container):
    message: BuilderBid
    signature: BLSSignature
```

The specs also define a blinded version of the `BeaconBlock`, in which the `ExecutionPayload` is substituted with an `ExecutionPayloadHeader`. Most notably, the `transactions` field in the former is replaced by `transactions_root` in the latter, so that transactions are not revealed to the proposer before it commits to a specific payload. After choosing a winning `SignedBuilderBid`, the proposer initiates the exchange by responding with a `SignedBlindedBeaconBlock`.

```python
class BlindedBeaconBlockBody(Container):
    randao_reveal: BLSSignature
    eth1_data: Eth1Data
    graffiti: Bytes32
    proposer_slashings: List[ProposerSlashing, MAX_PROPOSER_SLASHINGS]
    attester_slashings: List[AttesterSlashing, MAX_ATTESTER_SLASHINGS]
    attestations: List[Attestation, MAX_ATTESTATIONS]
    deposits: List[Deposit, MAX_DEPOSITS]
    voluntary_exits: List[SignedVoluntaryExit, MAX_VOLUNTARY_EXITS]
    sync_aggregate: SyncAggregate
    # Replacing full Execution_Payload
    execution_payload_header: ExecutionPayloadHeader

class BlindedBeaconBlock(Container):
    slot: Slot
    proposer_index: ValidatorIndex
    parent_root: Root
    state_root: Root
    # Replacing BeaconBlockBody
    body: BlindedBeaconBlockBody

class SignedBlindedBeaconBlock(Container):
    message: BlindedBeaconBlock
    signature: BLSSignature
```

The relay reconstructs the full `SignedBeaconBlock` by substituting the `ExecutionPayloadHeader` with the `ExecutionPayload` in the `SignedBlindedBeaconBlock`, and validates it. If successful, it releases it, completing the exchange.

*The `Signed` containers are omitted in the diagram for ease of exposition, and so are the blob sidecars.*

[![mev-boost](https://ethresear.ch/uploads/default/optimized/2X/0/0db424b170aafe48536d5f63796d120f6c7738c7_2_352x499.png)mev-boost748×1062 55.1 KB](https://ethresear.ch/uploads/default/0db424b170aafe48536d5f63796d120f6c7738c7)

### Observing the exchange

Currently, nodes can observe the second part of the exchange, i.e., the publication of the `SignedBeaconBlock`, but not the first part. If they could observe the first part, i.e., the proposer sending the`SignedBlindedBeaconBlock` to the relay, they would have observability into the full exchange between proposer and relay. If a node observes a *unique, valid* `SignedBlindedBeaconBlock` sufficiently in advance of the attestation deadline, it knows that the relay/builder has enough time to receive it, validate it and propagate the full `SignedBeaconBlock`. In other words, the proposer has fulfilled its half of the exchange. Were the slot to be missed, the node can then reasonably attribute the failure to the relay. If instead it does not observe a timely, valid `SignedBlindedBeaconBlock`, or observes multiple, it can attribute any eventual failure to the proposer: it is ok for the relay to withhold the `ExecutionPayload` when it cannot be reasonably sure of the outcome of publishing it, i.e., whether or not the corresponding `BeaconBlock` will become part of the canonical chain.

#### Independent validation of a blinded beacon block

Firstly, we need to clarify what it means for a `SignedBlindedBeaconBlock` to be valid independently of the full `ExecutionPayload` whose header it contains. Currently, the beacon chain state transition involves the execution payload in a few ways:

1. process_execution_payload checks that payload.parent_hash, payload.prev_randao, payload.timestamp are correct, and updates state.latest_execution_payload_header to the new ExecutionPayloadHeader.
2. process_withdrawals checks that payload.withdrawals == get_expected_withdrawals(state), to ensure that the same withdrawals are processed by EL and CL.
3. the EL is called to verify the ExecutionPayload

Everything in 1. involves only the `ExecutionPayloadHeader`, because `parent_hash`, `prev_randao` and `timestamp` are fully contained in it as well. While 2. involves the full payload as written in the spec, we can instead use`execution_payload_header.withdrawals_root`, i.e.,`hash_tree_root(payload.withdrawals)`, and check `withdrawals_root = hash_tree_root(get_expected_withdrawals(state))`. Finally, we are not concerned with 3: if we observe a`SignedBlindedBeaconBlock` which satisfies checks 1. and 2. sufficiently in advance of the attestation deadline, we know that whether the builder is able to release a valid `SignedBeaconBlock` entirely depends on whether they have made a valid `ExecutionPayload`.

*Future compatibility*: EIP-7002 and EIP-6110 introduce more message passing from the EL to the CL, i.e., EL-triggered exits and deposits. An `ExecutionPayload` would contain fields `execution_layer_exits` and `deposit_receipts`, which contain operations to be processed by the CL state transition. Clearly, such processing cannot happen in a `BlindedBeaconBlock` as currently constructed, because those fields would be replaced by `execution_layer_exits_roots` and `deposit_receipts_root`. As might happen in the builder specs, the `ExecutionPayloadHeader` in the `BlindedBeaconBlock` could be replaced by a `BlindedExecutionPayload`, where only the `transactions` field is replaced by `transactions_root`, while `withdrawals`, `execution_layer_exits`,`deposit_receipts` (and any other necessary fields that might be added in the future) are kept fully. Note that a `BlindedBeaconBlock` constructed this way still has the same `hash_tree_root` as the full `BeaconBlock`.

#### Gossiping signed blinded beacon blocks

To gain observability into the first part of the exchange, we can create a GossipSub topic, `blinded_block_envelope`, joined by nodes which run mev-boost. Only the current proposer would be able to publish to the topic, and it would publish this signed envelope:

```python
class BlindedBlockEnvelope(Container):
    signed_builder_bid: SignedBuilderBid
    signed_blinded_beacon_block: SignedBlindedBeaconBlock

class SignedBlindedBlockEnvelope(Container):
    message: BlindedBlockEnvelope
    signature: BLSSignature
```

Here we include the `SignedBuilderBid` in the envelope, instead of just gossiping a `SignedBlindedBeaconBlock`, to ensure that failures are attributable to the relay which has signed this bid.

#### Relay scoring

Every validator in the topic would then observe the arrival time of this object, as well the outcome of the slot, and use these data points to inform whether or not it should stay connected to the relay with pubkey `signed_builder_bid.message.pubkey`. For example, a client might choose to enact a simple strategy like this one:

- if a valid signed_blinded_block_envelope is received before 2.5s but the slot is missed, downscore the relay by D, up until 0, unless an equivocation from the proposer is detected.
- if a relay successfully lands a block on chain, increase the relay score by D/100, up until the maximum score S_{max}.
- if the relay score is  None:
    assert hash_tree_root(payload.withdrawals) = state._latest_withdrawals_root

    next_withdrawals = get_expected_withdrawals(state)
    state.latest_withdrawals_root = hash_tree_root(next_withdrawals)

    for withdrawal in next_withdrawals:
        decrease_balance(state, withdrawal.validator_index, withdrawal.amount)

    # Update the next withdrawal index if this block contained withdrawals
    if len(next_withdrawals) != 0:
        state.next_withdrawal_index = WithdrawalIndex(next_withdrawals[-1].index + 1)

    # Update the next validator index to start the next withdrawal sweep
    if len(next_withdrawals) == MAX_WITHDRAWALS_PER_PAYLOAD:
        # Next sweep starts after the latest withdrawal's validator index
        next_validator_index = ValidatorIndex((state.next_withdrawals[-1].validator_index + 1) % len(state.validators))
        state.next_withdrawal_validator_index = next_validator_index
    else:
        # Advance sweep by the max length of the sweep if there was not a full set of withdrawals
        next_index = state.next_withdrawal_validator_index + MAX_VALIDATORS_PER_WITHDRAWALS_SWEEP
        next_validator_index = ValidatorIndex(next_index % len(state.validators))
        state.next_withdrawal_validator_index = next_validator_index

```

##### Blobs

We can move the`kzg_commitments` from the `BeaconBlockBody` to the `ExecutionPayload`. Beacon blocks without a payload do not come with any kzg commitments. A payload, and a beacon block extending it (containing it) is only considered in the fork-choice tree if the blobs it commits to are available.

[![blobs](https://ethresear.ch/uploads/default/optimized/2X/c/c3ab1bcc723da79fdcf72febbd3baa8f4763d0eb_2_690x303.png)blobs750×330 9.77 KB](https://ethresear.ch/uploads/default/c3ab1bcc723da79fdcf72febbd3baa8f4763d0eb)

#### Pipelining

We can change the slot structure by adding an explicit new phase for propagation of execution payloads:

- 0s: publish beacon block
- 3s: publish execution payload
- 6s: attestation deadline
- 9s: publish aggregates to global topic

The protocol cannot enforce that the payload should be published at 3s, but crucially there is no reason to:

1. publish the beacon block later: the earlier it is published, the less likely it is to be reorged
2. publish the payload earlier: the later it is published, the more MEV can be collected (see timing games)

Therefore, we would expect beacon blocks and execution payloads to be published quite far apart from each other, leaving plenty of time for the beacon block to be propagated and processed before the payload needs to be.
