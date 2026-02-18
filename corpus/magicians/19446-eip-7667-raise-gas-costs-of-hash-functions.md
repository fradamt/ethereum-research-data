---
source: magicians
topic_id: 19446
title: "EIP-7667: Raise gas costs of hash functions"
author: vbuterin
date: "2024-03-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7667-raise-gas-costs-of-hash-functions/19446
views: 2530
likes: 15
posts_count: 10
---

# EIP-7667: Raise gas costs of hash functions

Raise the gas costs of opcodes and precompiles that involve hash functions.

https://github.com/ethereum/EIPs/pull/8367

## Replies

**wjmelements** (2024-04-01):

> Since then, however, there has emerged another equally important execution substrate that the EVM is executed on: zero knowledge proof (ZK-SNARK) systems. By that standard, these opcodes and precompiles are very underpriced relative to other operations.

I don’t see why mainnet gas should be increased to accommodate zk-snarks. I do not see why they are equally important.

---

**vbuterin** (2024-04-02):

Because in five years *every* chain, including Ethereum L1, will be ZK-SNARK verified. Making the Ethereum L1 ZK-SNARKed is a key part of the long-term vision of making “full” Ethereum verification be mobile-phone friendly and something that gets done by default in every Ethereum client, including mobile and browser (as opposed to just trusting Infura).

Now, we *could* simply say, we’ll solve the problem with brute force and stack together 20x more prover boxes, but (i) that’s a centralization vulnerability, and (ii) if that *is* an option, why waste 20x more prover boxes on maintaining an artificially low KECCAK gas price instead of using that capacity on increasing the L1 gaslimit by 20x?

---

**wjmelements** (2024-04-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Because in five years every chain, including Ethereum L1, will be ZK-SNARK verified

Shouldn’t we delay an L1 gas increase until L1 is impacted? The 2x increase you propose now might not even be enough then. A better solution than snarks may come along before then, bringing its own set of gas adjustments. This gas adjustment is so easy to implement that it can’t even be considered a step toward snarks.

---

**vbuterin** (2024-04-03):

> Shouldn’t we delay an L1 gas increase until L1 is impacted?

The issue with this approach is that there is a cross-dependency: people won’t even try to fully build the tools to properly snark-verify L1 until they are sure that there aren’t corner cases that make the entire project unviable in the worst case. And ZK-EVMs are already at a high level of maturity, to the point where they are being used in mainstream rollups. You can argue that there is no point in doing this before Verkle, because keccak MPT hashing is even more expensive than in-EVM hashing, but if we want L1 SNARK-friendliness to come at Verkle time, we need to start preparing for that *now*.

> The 2x increase you propose now might not even be enough then

The increase I propose is 10x though?

And I don’t think there is a significant probability of “a better solution than snarks”; snarks are pretty clearly the endgame of scalable and decentralized blockchains and this has been the mainstream opinion for years now.

---

**mratsim** (2024-04-10):

Do we need the same for elliptic curve precompiles?

This affects zkBridges, L3, verifying KZG in L2, zkCoprocessors on L2, …

On the other hand, there are techniques like Goblin Plonk, CycleFold and [Zero Knowledge Proofs of Elliptic Curve Inner Products from Principal Divisors and Weil Reciprocity](https://eprint.iacr.org/2022/596) that can accelerate EC in ZK.

But the first 2 need a cycle of elliptic curves, which exist for BN254 but not for BLS12-381.

---

**Eikix** (2024-06-14):

As it may be early to adopt this EIP on L1 (many dependencies), I propose to adopt it on ZK-Rollups (I tried to link my PR on RIPs repository but couldn’t).

This enables ZK-Rollups to account for the mispricing of non-ZK friendly hash operations in a standardized way.

How much more expensive should keccak be on, for example, Scroll, Kakarot or Polygon ZK-EVM (as well as other ZK-EVMs)? Can we agree on a number, or should each ZK-EVM perform its own pricing?

---

**etan-status** (2024-11-08):

One thing that should also be considered is the adjustment of the WORD_COST constants to be based on the real cost instead of it being a per-32 byte cost.

For example, SHA256 cost is flat from 0-55 bytes, then increments linearly in chunks of 64 bytes. Keccak has a similar scheme with even larger chunk sizes that still have to be paid even when hashing only small amount of data.

See [EIP-7797: Double speed for hash_tree_root](https://eips.ethereum.org/EIPS/eip-7797#sha-256-preprocessing) for a diagram on SHA256 internals.

---

**JacekGlen** (2025-02-20):

As I understand, the EIP intends to prevent the abuse of certain opcodes and precompiles by making them less affordable on a large scale. Indeed, [the research](https://github.com/imapp-pl/gas-cost-estimator/blob/master/docs/gas-schedule-proposal.md) shows that KECCAK or BLAKE2 are significantly underpriced, but not so much for SHA256, RIPEMD, or LOG*. Given the predicted increase in ZK_SNARK requirements, the proposal to raise the cost for everyone is understandable and easy to implement.

But I would suggest two other options to consider:

- Multidimensional fee market: A gas cost of a typical ERC-20 transfer or swap is made of 40% transaction, 2% calldata, 7% computations and 50% storage. Hence there is a natural balance since these transactions make up a majority of all blocks. To prevent abusive transactions in the future we can create separate gas prices for computations, storage, calldata, transactions and blobs. This would promote a balance between these elements, as we already do for blobs.
- Exponential cost: Similarly to memory_expansion_cost, any opcode or precompile with an unbounded dataset would have the cost rising exponentially.

Both options aim to not affect the current cost of a typical transaction.

---

**bbjubjub** (2025-05-06):

I came here to post because I realized the same thing. The compression functions in SHA-2 and RIPEMD-160 are the costly part. (as evidenced by the fact that they are accelerated in ZKVMs) If we charge per 256-bit word, we are essentially giving a 50% discount to an attacker who calls the function with 32 bytes over and over again, compared to honest users who typically pay two words per invocation of the compression function. It could be that a similar argument holds for keccak256 which also has a capacity of 512 bits, but I would need to study the construction to be sure. In any case if we are going to reform the gas pricing here we should take the opportunity to fix the granularity so we don’t have this problem anymore.

