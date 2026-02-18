---
source: ethresearch
topic_id: 4745
title: Multihashing in Ethereum 2.0
author: JustinDrake
date: "2019-01-04"
category: Sharding
tags: []
url: https://ethresear.ch/t/multihashing-in-ethereum-2-0/4745
views: 4419
likes: 7
posts_count: 8
---

# Multihashing in Ethereum 2.0

**TLDR**: We present a “multihashing” trick to make Ethereum 2.0 consensus objects natively compatible with multiple hash functions.

*Credits*: This idea came up in a discussion with [@barrywhitehat](/u/barrywhitehat) and [@vbuterin](/u/vbuterin).

**Construction**

Given “simple” hash functions h_1, ..., h_n define the “multihash function” H = [h_1, ..., h_n]. Build consensus objects (e.g. beacon blocks or the beacon state) using H instead of any individual h_i.

Candidate hash functions h_i include Keccak256, Friday, MiMC, SHA256, Blake2b.

**Discussion**

Hash functions are a key building block for blockchains, and enshrining one hash function over another has significant tradeoffs. Multihashing is a way to (largely) escape those tradeoffs through “hash subjectivity”. That is, infrastructure interacting with core L1 objects (include other L1 objects) can chose the hash function(s) to work with and hence make appropriate tradeoffs.

More concretely, below are potential benefits of multihashing:

- Compatibility: Using Keccak256 as a constituent hash function makes Ethereum 1.0 and 2.0 compatible. This unlocks Ethereum 1.0 deposits to Ethereum 2.0, as well as Ethereum 1.0 execution engines that use the Ethereum 2.0 data layer.
- Flexibility: By including exotic hash functions in the multihash (e.g. Friday or MiMC) we unlock the possibility for SNARK/STARK-based gadgets (at all layers). This includes data availability proofs, witness compression, STARK-based quantum-secure infrastructure, SNARK-based privacy infrastructure, etc.
- Interoperability: In the spirit of Polkadot and Cosmos, multihashing increases interoperability with other blockchains. For example, adding SHA256 as a constituent hash function increases interoperability with major blockchains such as Bitcoin.
- Security: If a particular hash function (e.g. Keccak256) is found unsafe the Ethereum 2.0 consensus layer maintains security through the other constituent hash functions.
- Efficiency: EVM 2.0 dApps can save gas when interacting with consensus objects by using a cheap hash function (e.g. Blake2b) .

Downsides of multihashing:

- Overhead: This includes larger consensus objects (32*n-byte multihashes instead of 32-byte hashes) and increased CPU-time to compute the multihash.
- Complexity: Multiple hash functions are part of the consensus logic. (Note that this may be unavoidable for S[T/N]ARK-friendly hash functions.)
- Lack of default: A single hash function is a Schelling point for the ecosystem to standardise around.

## Replies

**quickBlocks** (2019-01-04):

I love this idea. I’m not sure I’m right, but would it be true that with a multi-hash one could then find the data that went into making the hash at an IPFS location (if someone pinned it there)? If that were the case, and the chain was producing a hash that had, as a side-effect, the meaning of “This is where the data would be if it were on IPFS”, I think there might arise naturally (without incentivisation) a realization that if people pinned stuff at that multi-hash everyone with a light client could get the data using IPFS. Does that make sense? I don’t know exactly how a light client works, but I think this might have benefits over the light client because it would give the end user finer granularity vis-a-vi caching the data. (That is, the decision to cache the data if it was retrieved from IPFS could be made by the user instead of the light client.)

---

**vbuterin** (2019-01-04):

> Overhead : This includes larger consensus objects (32*n-byte multihashes instead of 32-byte hashes) and increased CPU-time to compute the multihash.

I think unfortunately this may be a deal-breaker. I already expect Merkle receipts to be the main contributor to data bloat, both because of crosslink committee block verification and from cross-shard transactions.

---

**JustinDrake** (2019-01-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> I already expect Merkle receipts to be the main contributor to data bloat

The good news is that multihashing is an incremental thing (as opposed to all-or-nothing). Multihashing can be enabled for some subset of consensus objects. They can also be “partially” enabled in the sense that they can be exposed from a data perspective but not used for verification of proofs (e.g. Merkle proofs) at the consensus layer.

To illustrate low hanging fruit of multihashing, let’s say that the only changes we make to the beacon chain are to make `BeaconBlock` and `BeaconState` roots (Keccak256, MiMC)-multihashes where Keccak256 is the “dominant” hash used for cryptographic witnessing. That is, MiMC is exposed in a few places but never actually used by the consensus.

Notice that in the above construction there’s essentially zero data bloat. Specifically, `BeaconBlock`s are 64 bytes larger (32 bytes extra for `parent_root`, 32 bytes extra for `state_root`). And the `BeaconState` is `32b * LATEST_BLOCK_ROOTS_LENGTH = 262kB` larger for `latest_block_roots`, and likewise `batched_block_roots` is doubled in size.

Because MiMC is SNARK-friendly, we allow dApps to efficiently access state with SNARKs. For example, large cross-shard transaction witnesses can be compressed into a SNARK. And being able to prove claims about the `BeaconState` in zero knowledge may be useful for privacy.

Beyond using multihashes for `BeaconBlock` and `BeaconState` roots as described above, I think it would be useful to do multihashing of `ShardBlock` `state_root`s in phase 1 to unlock witness compression for stateless execution in phase 2.

---

**vbuterin** (2019-01-05):

But wouldn’t we need to still include the other hashes for each level of the Merkle proof? Or are you suggesting not interlacing the hashes at every level but instead just including multiple kinds of Merkle roots?

---

**JustinDrake** (2019-01-05):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Or are you suggesting not interlacing the hashes at every level but instead just including multiple kinds of Merkle roots?

Right, no interlacing. The idea is to have an independent Merkle path for each root exposed so that one can “arbitrage” the most appropriate Merkle path.

---

**vbuterin** (2019-01-05):

Right, in the case the main downside is that to verify full validity you would need to do a lot more hashing of everything.

---

**postables** (2019-01-05):

I can’t speak to any of the technicals, but there’s already amazing code bases out there that can be used to supplement this idea, and even future-proofing to allow easily updating hashing algorithms which are used when the time is needed.

IPFS, or more specifically [multiformat](https://multiformats.io/) has already done a lot of great work surrounding multformats, and also [multihash](https://github.com/multiformats/multihash)es.

There’s already been some work to great [IPLD](https://github.com/ipfs/go-ipld-eth) objects for the Ethereum blockchain as well. IPFS could be incredibly useful for doing things like quickblocks mentioned, and could be an extremely viable way for light clients to communicate with other light clients, or even store elements of the Ethereum blockchain.

It would definitely be worth looking into the work multiformat is already doing, and not only could it save time on re-developing functionality, but collaborating between the two could help adoption of both parties involved.

