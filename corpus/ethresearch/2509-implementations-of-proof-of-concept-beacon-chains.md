---
source: ethresearch
topic_id: 2509
title: Implementations of Proof of Concept Beacon Chains
author: Mikerah
date: "2018-07-09"
category: Proof-of-Stake
tags: []
url: https://ethresear.ch/t/implementations-of-proof-of-concept-beacon-chains/2509
views: 3264
likes: 22
posts_count: 7
---

# Implementations of Proof of Concept Beacon Chains

Hi Ethereum Researchers,

My colleagues and I have recently started a Javascript implementation of the beacon chain based on the Ethereum team’s Python implementation.

As a result, we want to share a list of implementations in different programming languages so that those interested can help in the implementation and ideation of a beacon chain and hopefully bring Casper+PoS+Sharding to Ethereum.

Here’s a list:

Javascript: https://github.com/ChainSafeSystems/lodestar_chain

Go: https://github.com/prysmaticlabs/beacon-chain

Rust: https://github.com/sigp/rust_beacon_chain

Python: https://github.com/ethereum/beacon_chain

## Replies

**vbuterin** (2018-07-10):

Thanks for your work!

Please feel free to keep in touch with our team ([@JustinDrake](/u/justindrake) [@hwwhww](/u/hwwhww) [@liangcc](/u/liangcc)…) to stay up to date on protocol directions.

Also, have you thought at all about what you want to use for the P2P layer?

---

**paulhauner** (2018-07-10):

Hi [@Mikerah](/u/mikerah),

Thanks for making the list and including our implementation (the Rust one)! I like the initiative to get those implementing the beacon_chain in contact. I’ve had some chats with the Prysmatic Labs team in their Gitter and they’ve been very obliging.

I’ve been doing the state transitions lately and I’ll be making some issues on the ethereum/beacon_chain repo and in the ethereum/sharding gitter. I hope to see you there!

In response to [@vbuterin](/u/vbuterin), we’ve been looking into pubsub/gossipsub after being pointed in that direction by [@djrtwo](/u/djrtwo) and other posts here. I don’t know of a Rust implementation yet, though. Once we’re more across it we’ll evaluate the effort involved in implementing it. From the [libp2p specs gossipsub page](https://github.com/libp2p/specs/tree/master/pubsub/gossipsub) it looks like you’ll be in the same boat [@Mikerah](/u/mikerah) – no JS implementation listed yet ![:frowning:](https://ethresear.ch/images/emoji/facebook_messenger/frowning.png?v=9)

---

**Mikerah** (2018-07-11):

We are currently looking into what is currently “state-of-the-art” p2p libraries in Javascript.

So far, libp2p has a JS implementation and is the most developed. Pubsub/GossipSub are still very experimental at this time and are considering perhaps starting our experiemental implementation in Javascript.

We currently have a gitter room for this project: https://gitter.im/chainsafe/lodestar-chain

---

**mratsim** (2018-07-20):

I’ve started an alternative implementation in Nim.

The beacon block part of the specs changed this week. It is currently

```auto
fields = {
    # Hash of the parent block
    'parent_hash': 'hash32',
    # Slot number (for the PoS mechanism)
    'slot_number': 'int64',
    # Randao commitment reveal
    'randao_reveal': 'hash32',
    # Attestation votes
    'attestation_votes': [AttestationVote],
    # Reference to main chain block
    'main_chain_ref': 'hash32',
    # Hash of the active state
    'active_state_hash': 'bytes',
    # Hash of the crystallized state
    'crystallized_state_hash': 'bytes',
}
```

while before Monday (2018-07-16T21:03UTC), it was:

```auto
fields = {
    # Hash of the parent block
    'parent_hash': 'hash32',
    # Slot number (for the PoS mechanism)
    'slot_number': 'int64',
    # Randao commitment reveal
    'randao_reveal': 'hash32',
    # Shard aggregate votes
    'shard_aggregate_votes': [AggregateVote],
    # Reference to main chain block
    'main_chain_ref': 'hash32',
    # Hash of the state
    'state_hash': 'bytes',
    # Signature from proposer
    'sig': ['int256']
}
```

However at the moment:

- ethereum/beacon_chain does not implement AttestationVote,
- It is not defined in the spec either
- AggregateVote still exist in the per-block processing paragraph

So are AttestationVote and AggregateVote the same?

---

**mratsim** (2018-07-23):

Answering my own question, AggregateVote has fully become AttestationVote in the latest spec. https://notes.ethereum.org/SCIg8AH5SA-O4C1G1LYZHQ?view#Per-block-processing

---

**djrtwo** (2018-07-24):

The beacon chain is undergoing an update to v2.1. It is still under review and has not yet been implemented in the python repo. I expect it to be near ready at the start of next week, and we can all discuss details on the sharding implementers call.

