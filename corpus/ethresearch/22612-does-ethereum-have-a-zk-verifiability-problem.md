---
source: ethresearch
topic_id: 22612
title: Does Ethereum have a zk-verifiability problem?
author: "71104"
date: "2025-06-14"
category: zk-s[nt]arks
tags: []
url: https://ethresear.ch/t/does-ethereum-have-a-zk-verifiability-problem/22612
views: 468
likes: 12
posts_count: 7
---

# Does Ethereum have a zk-verifiability problem?

To build the project I mentioned in [this topic](https://ethresear.ch/t/generating-eddsa-pasta-keypairs/22610) I started learning about zk-SNARKs. One of the things I seem to understand is that the ECDSA signature scheme and the SHA-3 hash (formerly known as Keccak) don’t play well with zk-SNARKs because they result in massive circuits. IIUC, EdDSA with certain curves and the Poseidon hash fare much better in that regard, with circuits that could be hundreds of times smaller.

Hashing and verifying signatures are very common use cases in Solidity smartcontracts, but Solidity uses SHA-3 for hashes and AFAIK all Ethereum wallets are based on ECDSA. **Does that mean that all Solidity smartcontracts are inherently hard to prove in zk-SNARKs?** If so, how did Polygon zkEVM solve that problem? What zk-SNARK scheme does it use (Groth16 / PLONK / PLONKish / Halo2 / other) ?

## Replies

**arianaraghi** (2025-07-23):

Hey [@71104](/u/71104) ,

![](https://ethresear.ch/user_avatar/ethresear.ch/71104/48/20098_2.png) 71104:

> Does that mean that all Solidity smartcontracts are inherently hard to prove in zk-SNARKs?

No, Solidity contracts are not “inherently” impossible to SNARK—what’s expensive are the EVM primitives you happened to pick: KECCAK256 (opcode 0x20) and ECRECOVER (secp256k1 ECDSA).

In zk circuits, ECDSA-on-secp256k1 and Keccak, generally, blow up constraint counts: a Circom ECDSA verifier is ~1.5 M constraints (a ~200,000 implementation exists), while an EdDSA (baby-Jubjub) + Poseidon verifier is only a few thousand (~4.2k–10k), i.e. two orders of magnitude smaller.

![](https://ethresear.ch/user_avatar/ethresear.ch/71104/48/20098_2.png) 71104:

> If so, how did Polygon zkEVM solve that problem? What zk-SNARK scheme does it use (Groth16 / PLONK / PLONKish / Halo2 / other) ?

Polygon zkEVM handles this by not changing Solidity, but by building custom gadgets/circuits for those ZK-unfriendly ops, batching them, and then proving the whole EVM execution with a multi-stage pipeline:

1. PIL/STARK circuits for opcode/state-machine correctness,
2. STARK recursion & aggregation using a PLONKish arithmetization with custom gates/lookups,
3. wrap the big STARK in a tiny SNARK (FFLONK) that’s verified on Ethereum via the pairing precompile.

---

**71104** (2025-07-24):

![](https://ethresear.ch/user_avatar/ethresear.ch/arianaraghi/48/13038_2.png) arianaraghi:

> No, Solidity contracts are not “inherently” impossible to SNARK—what’s expensive are the EVM primitives you happened to pick: KECCAK256 (opcode 0x20) and ECRECOVER (secp256k1 ECDSA).

The first one should be extremely widespread though, considering that all `mapping`s use it. You can’t do much without Keccak256, you can’t even implement an ERC-20.

---

**arianaraghi** (2025-07-25):

Yeah, you are right. But, most hash functions are not very zk-friendly, and it might take some time to get to the hardware stage that these hash functions become an easy task.

---

**vbuterin** (2025-08-02):

Yes, current ethereum is VERY suboptimal for proving, and this is exactly why we have initiatives like https://www.poseidon-initiative.info/ , which if successful would let us replace keccak with a far more prover-friendly hash (and we can do the same to the VM etc)

---

**71104** (2025-08-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> https://www.poseidon-initiative.info/

Interesting, I didn’t know about that!

Out of curiosity, why did you choose Poseidon rather than e.g. Pedersen? Are you thinking to invest your efforts in the Halo2 ecosystem rather than Circom? If so, why?

(I made the same choice for my own project but I’m curious to hear your rationale.)

---

**vbuterin** (2025-08-02):

Pedersen is not quantum-resistant.

In general, we’re not interested in anything not quantum-resistant for any big Ethereum upgrades at this point.

