---
source: magicians
topic_id: 22611
title: "EIP-7864: Ethereum state using a unified binary tree"
author: ihagopian
date: "2025-01-21"
category: EIPs
tags: [stateless]
url: https://ethereum-magicians.org/t/eip-7864-ethereum-state-using-a-unified-binary-tree/22611
views: 1325
likes: 17
posts_count: 12
---

# EIP-7864: Ethereum state using a unified binary tree

**Discussion topic for [EIP-7864](https://eips.ethereum.org/EIPS/eip-7864)**

This EIP is a renewed take on a Binary tree proposal for the Ethereum state. Compared to [EIP-3102](https://eips.ethereum.org/EIPS/eip-3102) it proposes a single *balanced* tree and pulls other ideas similar to [EIP-6800](https://eips.ethereum.org/EIPS/eip-6800) which are agnostic to Verkle (e.g. packing of account data, storage-slot, and code chunks).

Hash-based state-trees have renewed interest due to:

1. Potential PQ concerns
2. Proving systems advancing quickly and getting closer to viable proving state via SNARK/STARKs.

---

There are two main open questions about a Binary Tree design:

1. Sparse vs Non-Sparse
2. Which hash function to use for merkelization

Reg 1., the ideal design for a spec would be a Sparse Merkle tree due to its simplicity. There’s a [doc summarizing previous research](https://hackmd.io/@jsign/binary-tree-notes) to deal with drawbacks.

Reg 2., this depends on evolving provers performance and potential security concerns of the considered options.

The current draft proposal decided:

- For 1., use a non-sparse Merkle tree only compressing branches at the stem-level (stem is defined in the EIP). This aims to avoid complex extension nodes rules, while also trying to lower the amount of hashing done for merkelization. The latter is required since today we’re very tight on proving performance for commodity hardware.
- For 2., use BLAKE3, which is a real (~optimistic) candidate. The current draft does this since it can help EL clients want to experiment with the implementation without much friction. If Poseidon2 is proven secure, the EIP can be easily adjusted by describing a 32-byte→[Field] encoding without much impact on the rest of the design. Using Poseidon2 could also re-open the “sparse tree” discussion since the proving performance is very high.

The above aren’t final decisions, but the current proposal allows a solid ground for further discussions, research, PoC, or analysis on how this would look in mainnet. There’s a python implementation for this EIP [here](https://github.com/jsign/binary-tree-spec).

We welcome anyone in the community (e.g. core devs, app developers, L2s) to provide feedback and collaborate!

---

Extra notes:

- We haven’t gone all-in in some other potential “Rationale” sections, such as expected Merkle proof sizes, implement them in the Python spec, and other potential ones. The main goal for now is to gain more confidence in the overall picture, and we’ll expand on that front later.
- EL clients might be interested in a useful trick to handle an arity-N tree regarding the number of internal nodes overhead (note that the doc explains this for an SMT, but the same idea applies to any arity-N tree).
- Gas remodeling is EIP-4762. It might need constant adjustments, but the overall approach would be the same.
The proposed state-conversion strategy (EIP-7748) for moving from MPT to VKT/Binary is the same since it is agnostic to the target tree.

---

As mentioned, today’s main blocker is finding a secure cryptographic hash function with a proving system with enough proving throughput in [recommended hardware](https://hackmd.io/@kevaundray/S1hUQuV4Jx) (i.e. in-circuit performance).

Although out-of-circuit performance isn’t the primary decision factor, I’ll soon share some benchmarks on the different hash alternatives run on a machine with the recommended hardware. This information would be a first step in understanding tree update and (non-snark) proof creation performance.

For in-circuit performance benchmarks, please refer to the [following doc](https://hackmd.io/@han/bench-hash-in-snark).

## Replies

**varun-doshi** (2025-01-22):

Great read

Here’s a minimal POC in Rust for EIP-7864 based on the provided Python spec.

Currently contains implementation for the tree. Will implement embedding soon.

`github.com/varun-doshi/eth-binary-tree`

---

**1etsp1ay** (2025-01-23):

will this tree have consistent state across **all** L2 chains … I’d be worried about concurrency issues arising from differing finalisation intervals (deadlock, livelock, race conditions, yadda yadda).

---

**ihagopian** (2025-01-23):

Nothing about this proposal changes the current reality that the tree is only used for L1, so there aren’t multiple writers that can cause concurrency issues.

L2s would still use their own trees as they do today, which have other designs with different tradeoffs.

---

**rjl493456442** (2025-02-05):

> Simplicity: working with the abstraction of a key/value store makes it easier to write code dealing with the tree (e.g. database reading/writing, caching, syncing, proof creation, and verification) and upgrade it to other trees in the future.

I don’t see a significant advantage in terms of simplicity with the single-layer structure. One notable change is that the database key for storage trie nodes has been shortened to 32 bytes from the original 64 bytes. However, many database engines (e.g., those based on LSM-Tree) typically optimize key size compression effectively when consecutive entries share a common key prefix.

Can you please provide some concrete examples?

> Uniformity: the state is uniformly spread throughout the tree; even if a single contract has millions of storage slots, the contract’s storage slots are not concentrated in one place.

I don’t think having data locality for storage slots is a bad thing. With the two-layer structure, the storage slots associated with a specific account can be iterated, which is not possible with the new structure.

> This is useful for state-syncing algorithms.

Can you elabrate why it’s useful?

> Additionally, it helps reduce the effectiveness of unbalanced tree-filling attacks.

I don’t believe this is achieved through the single-layer structure but rather through the key hashing mechanism, which evenly distributes the entries. Notably, key hashing is a double-edged sword and has caused numerous issues. For instance, entries iterated from the tree lack associated preimages unless those preimages are explicitly maintained.

Additionally, why is it necessary to perform a hash operation on the basic header fields? The account address is already derived through a hash calculation, which ensures it is evenly distributed. Adding another hash operation here feels redundant.

---

**ihagopian** (2025-02-05):

Thanks, [@rjl493456442](/u/rjl493456442) , for your feedback. ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

It’s very helpful coming from EL core developers.

I’ll share my thoughts about your questions.

> I don’t see a significant advantage in terms of simplicity with the single-layer structure. One notable change is that the database key for storage trie nodes has been shortened to 32 bytes from the original 64 bytes. However, many database engines (e.g., those based on LSM-Tree) typically optimize key size compression effectively when consecutive entries share a common key prefix. Can you please provide some concrete examples?

This part of the rationale mentions that using a unified try gets us *simplicity* at the spec level.

What you mention about database engines compacting consecutive keys that share a prefix is an implementation trick EL clients must do (or your dependencies) to deal with the complexity of having multiple trees. Having a single tree thus not having 64 bytes (even if they share a prefix in your implementation) is a way to remove complexity directly at the spec level, instead of needing an implementation trick.

This quoted text mainly highlights that having a single tree has downstream simplification effects in algorithms related to the state tree, for example:

- Today, creating a state proof involves conceptually dealing with two trees. Proving a storage slot involves two branches that have different semantics. Having a single tree simplifies proof semantics since it’s proving a branch in a single tree (so no extra semantics are required).
- Syncing the tree also involves syncing more than one trie compared to one. This means extra overhead tracking the cursor of the sync or related proofs.
- The current tree design with multiple MPTs leaks this complexity to the state conversion algorithm. The design has to deal with walking algorithms that now should decide and clarify the walking order since there are multiple trees; compared to having a single tree, you don’t have to define how and when storage tries are walked while you’re walking the accounts trie. (After the upcoming tree conversion, hopefully, we won’t have to do a state transition again in the future… but this can’t be discarded, so having a unified tree simplifies this compared to what we have to do now)
- The same applies to caching strategies in implementations, as you have to deal with two scopes (account trie or storage trie(s)) for caching trees instead of a single one.
- Another example of simplification is the removal of RLP.

The overall argument of this *simplicity* angle mainly leverages this opportunity to keep simplifying the protocol at the spec level. Implementations can always push further with optimizations. As mentioned, simplifying the spec has helpful downstream simplifications.

> I don’t think having data locality for storage slots is a bad thing.

The intended message is that data locality (in the database) is an implementation detail. Now that you mention it that way, I think we can better explain this in the text. I’m also not sure separating “Uniformity” from “Simplification” was a good idea, but maybe other authors have a different opinion. We should probably improve this part of the EIP since I agree it feels pretty confusing.

Unrelated to this Binary EIP but with data locality: this EIP will come bundled with [EIP-4762](https://eips.ethereum.org/EIPS/eip-4762) as a gas cost model (or similar; this depends on many factors). EIP-4762 introduces better *data locality* justified by access patterns in block execution. This has the benefits of proving fewer branches and saving gas costs for applications (but we need to do more research about overall effects since code access has to be charged). For example, consecutive storage slots live in groups under the same main branch (i.e. stem) — since storage slot access is not purely random, this should have gas benefits. The same applies to chunkified code, since although you can have JUMP(I)s, code execution is naturally “linear”.

> With the two-layer structure, the storage slots associated with a specific account can be iterated, which is not possible with the new structure.

Yes, this is a known drawback of the design. However, iterating the storage tree isn’t a requirement for the protocol. You never need to iterate the tree to execute a block.

I agree that losing this capability for some client tooling or analysis can be unfortunate. I suffered from this myself while working with Verkle trees, which has the same drawback, when trying to do some analysis—but unless tree iteration is a necessity for the actual protocol, it feels more like an optional feature.

> Can you elabrate why it’s useful?

I think I addressed this in my previous “Simplicity” response. Since I agree it can be confusing, this argument should probably be moved from “Uniformity.” We should make that change.

> I don’t believe this is achieved through the single-layer structure but rather through the key hashing mechanism, which evenly distributes the entries. Notably, key hashing is a double-edged sword and has caused numerous issues. For instance, entries iterated from the tree lack associated preimages unless those preimages are explicitly maintained.

I agree key hashing is a double-edged sword. Actually, the preimages problem adds a decent amount of complexity to the upcoming tree conversion, I did some [Ethresearch post some days ago](https://ethresear.ch/t/state-tree-preimages-file-generation/21651) about this topic if you’re interested. However, key hashing is required to balance the tree.

Regarding the single-layer structure and attacks, for a storage slot “full path” you can attack both the account and storage paths independently.

> Additionally, why is it necessary to perform a hash operation on the basic header fields?

For SNARK circuits, it’s helpful to rely only on a `32byte x 32byte→32 byte` primitive for merkelization (or a slight variant if we use arithmetic hash functions). This is why [we propose packing](https://eips.ethereum.org/EIPS/eip-7864#header-values) the nonce, balance, and code size (and version) in a single 32-byte to reduce this overhead and be efficient (actually, this was already a stretch since involves bitwise operations which aren’t nice for circuits). (The code-hash is another 32-byte leaf value). We can add this to the rationale since it isn’t obvious.

> The account address is already derived through a hash calculation, which ensures it is evenly distributed. Adding another hash operation here feels redundant.

Using plain addresses as keys in the tree isn’t safe. At the cost of 21_000 gas, you can send ETH to any address you want (i.e., without knowing the public key). This means external actors can manipulate insertions in the tree at a very low cost (21k gas), creating long branches.

---

**Arvolear** (2025-02-05):

For someone who is coming from ZK-DAPP development, I really love the idea of a provable Ethereum state. Currently ZK-DAPPs use some kind of an on-chain tree ([Incremental](https://github.com/runtimeverification/deposit-contract-verification/blob/master/deposit-contract-verification.pdf), [Sparse](https://docs.iden3.io/publications/pdfs/Merkle-Tree.pdf), and even [Cartesian](https://medium.com/@Arvolear/cartesian-merkle-tree-the-new-breed-a30b005ecf27)) to store specific data for later in-circuit verification. Although Poseidon1 is most often used, I believe BLAKE3 will not be a huge performance impact from a DAPP standpoint.

With the state provable natively we could just get away with regular “mappings” and “arrays” which would save tons of gas.

It would be fantastic to have some RPC method that returns a Merkle proof for a slot for a specified block.

---

**rjl493456442** (2025-02-07):

> Syncing the tree also involves syncing more than one trie compared to one. This means extra overhead tracking the cursor of the sync or related proofs.

The primary advantage of having a secondary storage trie is that it clearly defines the storage scope associated with the currently positioned account.

> compared to having a single tree, you don’t have to define how and when storage tries are walked while you’re walking the accounts trie.

Honestly, expanding the linked storage trie is a natural behavior. It doesn’t involve any additional rules but is simply part of the standard traversal algorithm for a two-layer tree structure.

> but unless tree iteration is a necessity for the actual protocol, it feels more like an optional feature.

This is a crucial feature, especially for the sync protocol. The current SNAP sync protocol relies on traversing entries within the trie and proving these elements in a storage-efficient manner. With this optimization, most trie nodes can be reconstructed locally using the provided information, rather than fetching them from the network in a verifiable way. This approach addresses the limitations of the original fast sync, which has become highly inefficient and incapable of supporting the Ethereum mainnet.

In this one-layer design, all entries lose their original meaning and simply become elements maintained within the trie. As a result, the sync protocol’s design must rely solely on the characteristics of the trie itself, such as expanding the trie from root to leaves. Of course, the additional flat state structure can be maintainly (e.g. the snapshot in Geth) to support the ability of state traversal. But it’s just the tricks of implementation.

In addition, the state traversal order in the original MPT (2-layers) is exactly the same as the flat state structure (e.g. the snapshot in Geth), but in this EIP, this will become impossible.

> Using plain addresses as keys in the tree isn’t safe. At the cost of 21_000 gas, you can send ETH to any address you want (i.e., without knowing the public key). This means external actors can manipulate insertions in the tree at a very low cost (21k gas), creating long branches.

Right, I completely missed that. Good point.

---

**rjl493456442** (2025-02-07):

By the way, have you considered a corresponding sync algorithm for the proposed binary tree? I believe it’s a critical aspect of the design and should be discussed alongside the tree structure itself.

---

**ihagopian** (2025-02-07):

Yes, I agree. I think there has been a considerable effort put into the current snapsync for MPT since, as far as I know, syncing strategies have a long history, so even with the MPT, it wasn’t easy.

We need to give this more thought, and I’d love to have anyone interested with more experience in its intricacies help us with this.

I think it’s also worth highlighting that changing the state tree is a stepping stone into SNARKifing the L1, which means that most nodes won’t have to sync the entire state (that’s one of the main goals, after all). Since builders will do it mainly, this changes the assumptions/constraints about bandwidth usage and related constraints for the syncing algorithm. Of course, there might be a temporal period where we still need a reasonable good solution until that future fully kicks in.

---

**zemse** (2025-02-10):

Is there any information on how transactions and receipts trie in a block affected by this EIP? Or will they continue to be encoded in MPT format?

---

**ihagopian** (2025-02-11):

The transactions and receipts tries aren’t affected by this EIP.

