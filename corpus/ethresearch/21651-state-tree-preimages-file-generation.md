---
source: ethresearch
topic_id: 21651
title: State tree preimages file generation
author: ihagopian
date: "2025-01-31"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/state-tree-preimages-file-generation/21651
views: 289
likes: 1
posts_count: 1
---

# State tree preimages file generation

*Thanks to Guillaume Ballet and Tanishq Jasoria for their feedback and to Stateless Implementors Call participants for previous discussions on this topic.*

In this article, we dig into the topic of **state tree preimages generation** topic, including:

- Explain enough context to understand where this topic fits the protocol evolution.
- A high-level explanation for EIP-7612 and EIP-7748 is required to understand the problem properly.
- Propose a potential file format for the preimages and analyze whether more complex formats might be worth it.
- Provide a new preimages tool using a non-archive reth to generate and verify preimage files and generate the data used in this article so it can be reproduced.

If you know why generating preimages for a future tree conversion is required, skip the *Context* section.

# Context

[The Verge](https://vitalik.eth.limo/general/2024/10/23/futures4.html) part of the roadmap proposes replacing the current Merkle Patricia Trie (MPT) with a new tree, which is more efficient in achieving statelessness and further SNARKifying L1.

Today’s main tree candidates are Verkle Trees ([EIP-6800](https://eips.ethereum.org/EIPS/eip-6800)) and Binary Tree ([EIP-7864](https://eips.ethereum.org/EIPS/eip-7864)). If you want more about this dichotomy, read the [EIP-7864 discussion thread](https://ethereum-magicians.org/t/eip-7864-ethereum-state-using-a-unified-binary-tree/22611). The topic of this article is **independent of this decision**, so you can assume any future path.

Since a new tree is used, we need a strategy to move the existing data from the MPT to the new tree. Today’s proposed strategy is converting the data with an Overlay Tree ([EIP-7612](https://eips.ethereum.org/EIPS/eip-7612) + [EIP-7748](https://eips.ethereum.org/EIPS/eip-7748)), which we’ll explore later.

Say we want to move an account’s data (nonce, balance, code hash) from the MPT to the new tree. The tree key in the MPT is `keccack(address)`, but in the new tree, it is `new_key(address)`, where `new_key` isn’t necessarily `keccak`.  EL clients must have access to the underlying preimage (i.e., `address` in this case) for each key in the tree. If they only have `keccack(address)` it becomes impossible to calculate `new_key(address)`. The same applies to accounts state tries.

In short, every node in the network that will undergo the state conversion from the MPT to the new target tree should be able to resolve every MPT key preimage for the accounts and storage tries.

## Aren’t EL clients storing tree key preimages?

Unfortunately, no. Depending on the current architecture and database design of EL clients, these preimages might be computed from existing data, but this only applies to a minority of clients.

Some examples of the relationship between tree key preimages and client databases:

- Geth has a flatdb to access the state faster than using the trees. The keys in this database are the hashed values of the accounts or the concatenation of accounts hash and storage slots hash—i.e., hash-based keys. Using hashed versions of keys makes sense for syncing, and there has never been a real incentive to justify the extra storage of saving the preimages.
- Erigon and Reth also have a flatdb but with unhashed tree keys as keys in this database, which is very convenient for this problem.
- Nethermind doesn’t have a flatdb yet, so it relies on efficiently accessing the tree for state access, but they’re planning to introduce a (key-hashed) flatdb soon.

This means that unless you’re an Erigon or Reth node, you don’t have the actual preimages of tree keys. According to [ethernodes.org](https://ethernodes.org/), non-Erigon+Reth nodes comprise more than 80% of the network, meaning most of the network has this preimage problem. Even for Erigon or Reth nodes, being able to get the preimages doesn’t mean they have an efficient way of resolving them today. To understand this better, let’s dive deeper into why.

# How are preimages used in the tree conversion?

Understanding how the *overlay tree* and state conversion EIPs work together can better answer this question. You can read the EIP, but here’s a compressed summary to continue with the preimages discussion.

## EIP-7612 TL;DR

*Note: this EIP references Verkle, but the idea is agnostic to the target tree, so it also works with a Binary Tree.*

EIP-7612 explains how a new tree is introduced into the protocol:

- The MPT becomes read-only (i.e., frozen) at the fork block.
- A new empty tree is created (e.g., Verkle or Binary).
- State updates resulting from block execution are only written to the new tree.
- As a side effect, reading the state only using trees means reading the new tree, and if the entry isn’t found, checking the MPT.

In summary, it’s a two-level (i.e., *overlay*) tree where the base tree (MPT) is frozen, and the top tree (Verkle or Binary) starts fresh, receiving the writes. Regarding the last bullet, EL clients have a flatdb to access the state, so it doesn’t necessarily mean you have to do double-tree-lookups.

## EIP-7748 TL;DR

Now that we understand EIP-7612, this is when EIP-7748 comes into play:

- At a defined block timestamp (CONVERSION_START_TIMESTAMP), the conversion process starts. Note that there must be enough time between EIP-7612 activation and CONVERSION_START_TIMESTAMP so we can guarantee the MPT is frozen (i.e., has chain finalization so no reorgs can change the fact)
- In the next block, before the transactions are executed:

Deterministically take CONVERSION_STRIDE tree entries from the MPT.

The concept of tree entries is more precisely defined in the EIP (i.e., named conversion unit) — we’re simplifying a bit here.
- The CONVERSION_STRIDE value is still TBD since it’s a tradeoff between the block execution state conversion overhead and the full conversion duration. The proper value depends on which is the target tree since Verkle has a more costly re-hashing than Binary.

We copy it in the top tree if it’s not a stale value—since EIP-7612 was activated, block execution could have already written a new value for this MPT key, which must not be overridden.

Continue doing the above until we finish walking all MPT keys.

The design decision that the state conversion step happens *before* the transactions are executed is beneficial since EL clients can do the state conversion step for the next block before it arrives.

The primary fact about this process relevant to the preimage file is the order in which we iterate on MPT entries. The currently proposed ordering is to do a full depth-first walk (DFW) in the MPT(s): do a DFW in the accounts trie, and when reaching a leaf, do a DFW in the accounts storage tries before continuing the walk in the accounts trie. We first migrate the account storage slots and then the account’s data.

Let’s look at an example to understand it better. Let’s assume *CONVERSION_STRIDE* is 5, and we’re in the first block of the state conversion. Here are what MPT entries we might see in the walk:

1. Accounts trie key 0x000000abc... equals keccak(address_A). We note that address_A has a storage trie with two storage slots, so we DFW into it.

Step #1: Account address_A storage trie with key 0x0000131... equals keccack(storage_slot_A), meaning we migrate storage_slot_A value for address_A to the new tree.
2. Step #2: Account address_A storage trie with key 0x0003012... equals keccack(storage_slot_B), meaning we migrate storage_slot_B value for address_A to the new tree.
3. Step #3: Since we migrated all storage slots, we now migrate address_A account nonce, balance, and code.

Accounts trie key `0x000000ffa...` equals `keccak(address_B)`. `address_B` is an EOA

1. Step #4: there are no storage slots, so no DFW is done in the storage trie. We migrate address_B account nonce, balance, and code.

Accounts trie key `0x000005630...` equals `keccak(address_C)`. We note that `address_C` has a storage trie with 1000 storage slots, so we  DFW it.

1. Step #5: Account address_C storage trie with key 0x0000021... equals keccack(storage_slot_A), meaning we migrate storage_slot_A value for address_C to the new tree.

Note the following:

- The walking order in the account trie and potential tries is hash-based, not address or plain storage slot value. This is a consequence of DFW in the trie since the keys are hashes of addresses or storage slots.
- storage_slot_A from address_A and address_C is a different number (e.g., 10 and 24, respectively). They mean the first storage slot found while walking DFW in their storage tries. As mentioned in the previous bullet, the storage slot walking order is hash-based and not “natural” ordering, so storage_slot_A can be greater than storage_slot_B.
- The above point is also why we need the preimages—the first key has the value 0x000000abb, which you need to know corresponds to address address_A so you can re-hash to determine which key is in the new tree.
- The last migrated entry is only the first storage slot of account_C, but we still have 99 remaining slots. We’ll continue migrating those in the next block since we have already reached the CONVERSION_STRIDE limit!

You can also find a talk about this EIP [here](https://www.youtube.com/watch?v=F1Ne19Vew6w), with some visuals to help complement this explanation.

## Recap

The above hopefully makes clear the following facts:

- The preimages file must contain all existing address_X in the frozen MPT account trie.
- The preimages file must contain all existing storage_slot_X in all frozen MPT storage tries.
- Since the MPT is frozen and the walk is deterministic, the order in which we need the preimages is fully determined upfront.

# Preimage file

Now we dive into different dimensions of this preimage file:

- Distribution
- Verifiability
- Generation and encoding
- Usage

The main focus of this article is *Generation and encoding*, but we touch on the other dimensions for completeness. Until we reach the *Generation* section, please assume this file is magically generated and encoded.

## Distribution

Given that the preimage file is somehow generated, how does this file reach all nodes in the network? This topic was explored multiple times during [Stateless Implementers Calls (SIC)](https://github.com/ethereum/pm/issues?q=is%3Aissue%20%22stateless%20implementers%22%20), L1 event workshops, and informal discussions.

After talking with many (but overall small sample) core devs, the current consensus is that it’s probably OK to expect clients to download this file through multiple potential CDNs.This is compared to relying on the Portal network, in-protocol distribution, or including block preimages.

Other discussed options are:

- Having an in-protocol distribution mechanism.
- Distributing the required preimages packed on each block.

This topic is highly contentious since these options have different tradeoffs regarding complexity, required bandwidth in protocol hotpaths, and compression opportunities. Despite talking with many core developers, they’re still not representative enough to conclude that ACD would reach the same conclusion.

This article focuses on the preimage generation and encoding format, which we must do regardless of how this file is distributed.

## Verifiability

As mentioned above, full nodes will receive this file from somewhere that can be a potentially untrusted party or a hacked supply chain. If the file is corrupt or invalid, the full node will be blocked at some point in the conversion process.

The file is easily verifiable by doing the described tree walk, reading the expected preimage, calculating the keccak hash, and verifying that it matches the client’s expectations. After this file is verified, it can be safely used whenever the conversion starts, with the guarantee that the client can’t be blocked by resolving preimages — having this guarantee is critical for the stability of the network during the conversion period. This verification time must be accounted for in the time delay between EIP-7612 activation and EIP-7748 *CONVERSION_START_TIMESTAMP* timestamp*.*

Of course, other ways to verify this file are faster but require more assumptions. For example, since anyone generating the file would get the same output, client teams could generate themselves and hardcode the file’s hash/checksum. When the file is downloaded/imported, the verification can compare the hash of the file with the hardcoded one.

## Generation and encoding

Now that we know which information the file must contain and in which order this information will be accessed, we can consider how to encode this data in a file. Ideally, we’d like an encoding that satisfies the following properties:

- Optimizes for the expected reading pattern: the state conversion is a task in the background while the main chain runs, so reading the required information should be efficient.
- Optimize for size: as mentioned before, the file has to be distributed somehow. Bandwidth is a precious resource; using less is better.
- Low complexity: this file will only be used once, so a simple encoding format is good. It doesn’t make sense to reinvent the wheel by creating new complex formats unless they offer exceptional benefits while taking longer to spec out and test.

There’s a very simple and obvious candidate encoding that can be described as follows following the example we explored before: `[address_A][storage_slot_A][storage_slot_B][address_B][address_C][storage_slot_A]...`. We directly concatenate the raw preimages next to each other in the expected walking order.

This encoding has the following benefits:

- The encoding format has zero overhead since no prefix bytes are required. Although preimage entries have different sizes (20 bytes for addresses and 32 bytes for storage slots), the EL client can know how many bytes to read next depending on whether they should resolve an address or storage slot in the tree walk.
- The EL client always does a forward-linear read of the file, so there are no random accesses. The upcoming Usage section will expand on this.

Before diving deeper into the efficiency of this encoding, let’s try to generate this file for mainnet and get a sense of the size. To do it, [we created a tool](https://github.com/jsign/eth-stateless/tree/main?tab=readme-ov-file#preimages) that uses a synced reth full node (i.e., not necessarily archive) to generate, verify, and do other analyses that will be presented later. A while ago, we created a [geth tool](https://github.com/ethereum/go-ethereum/blob/fc12dbe40bdb3fd77d0ea6049570b8c870421859/cmd/geth/snapshot.go#L154-L161), but it requires a node syncing from genesis with the `--cache.preimages` flag enabled.

We can create the preimage file by running `preimages generate --datadir <...> --eip7748`. Here are some facts about the generated file in a mid-end machine:

- Time to generate: ~1hr
- File size uncompressed: 42GiB
- File size compressed (zstd): 36GiB

Note that anyone in the network running a Reth (or potentially Erigon) node can generate the file, and the output is always the same since, given a frozen MPT, the preimages are fixed.

### Diving deeper into encoding efficiency

Despite the encoding format’s zero encoding overhead, the difference between the compressed and uncompressed size signals compression opportunities. Let’s explore why that’s the case.

We can put each preimage entry in the file in two buckets:

- Addresses preimages

Deduping

Every [address_X] entry is unique in the file since the accounts tree contains unique information for each account, so there’s no opportunity for deduplication.

Compression:

- Addresses are hashes, so there is no opportunity to compress them.

**Storage slots preimages**

- Deduping

They repeat in the file since multiple contracts can (and do) overlap in storage slot usage. e.g., multiple contracts use storage slots 0, 1, and 2.
- The biggest group of repeated storage slots are top-level slots since they share a 0x00000... prefix (e.g., the ones mentioned in the previous bullet).
- When contracts have arrays or hashmaps, the storage slots get more scattered in the storage slots space due to the nature of how hashing maps variables into storage slots.

Compression

- The compression opportunities for storage slots vary. For example, storage slots with 0x00000.. prefixes (i.e., the top contract variables) are very compressible since they have many zero-bytes. Other storage slots are mainly the result of hashes; they aren’t that compressible (but “dedupable”).

In summary, the addresses can’t be deduped or compressed, but storage slots do have an opportunity to be deduped/compressed. However, it’s hard to know how big the impact would be and if it’s worth it.

To do a deeper analysis, you can run `preimage storage-slot-freq` analysis tool. Let’s look at the output first:

```python
Database block number: 21662206
Top 1000 storage slot 29-byte prefix repetitions:
0000000000000000000000000000000000000000000000000000000000: 57150357 (4.65%) ~1580MiB (cumm 1580MiB)
f3f7a9fe364faab93b216da50a3214154f22a0a2b415b23a84c8169e8b: 13671109 (1.11%) ~378MiB (cumm 1958MiB)
8a35acfbc15ff81a39ae7d344fd709f28e8600b4aa8c65c6b64bfe7fe3: 9429136 (0.77%) ~260MiB (cumm 2219MiB)
f652222313e28459528d920b65115c16c04f3efc82aaedc97be59f3f37: 8580073 (0.70%) ~237MiB (cumm 2456MiB)
405787fa12a823e0f2b7631cc41b3ba8828b3321ca811111fa75cd3aa3: 7750842 (0.63%) ~214MiB (cumm 2671MiB)
a66cc928b5edb82af9bd49922954155ab7b0942694bea4ce44661d9a87: 3545488 (0.29%) ~98MiB (cumm 2769MiB)
c2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f: 2663837 (0.22%) ~73MiB (cumm 2842MiB)
...
```

(The full output is longer and can be found [here](https://pastebin.com/raw/M7nLDC5t))

The program counts the number of storage slots with the same 29-byte prefix, for example, for the prefix `00000....00`:

- There are ~57 million storage slots, which accounts for 4.65% of the total.
- It maps to ~1580MiB of the preimage file size.
- The cumm value is the sum of the sizes up to the current row. For example, the top 3 storage slot preimage prefixes account for 2219MiB of the preimage file.

You might be wondering what are those values in the second, third, and following rows:

- f3f7... is  keccak(0x000000..08)
- 8a35... is keccak(0x000000..04)

These prefixes appear because many contracts have defined arrays in storage slots 8 and 4, respectively. This means that the value in the preimage file is the hash of those slot numbers. Since items in arrays are consecutive from this base value, these “top-level arrays” are top prefixes in the preimage file.

There’s nothing special about choosing 29 bytes for the prefix; the idea is to capture grouping top-level variables and arrays. For hashmaps, entries are distributed all over the storage slot space, so there are fewer opportunities for deduplication. The chances are even lower as more “nesting” happens in contract variables. That’s why top prefixes are top-level arrays, so it makes sense.

If you look at the full output link, the top 1000 prefixes account for ~4GiB, close to the ~6GiB compression we gained via zstd. Of course, the tail is very long, so the optimal size could probably be better.

Trying to deduplicate as part of the file format would increase the complexity of the file format spec. There could be ways to preserve quasi-linear reads by separating the top N preimages to be kept in RAM. Still, it might not be worth it if the extra complexity compared to the simple format+zstd for a small relative reduction in size. Remember, this is a one-time download. It could be downloaded in non-critical parts of the slot duration or even through separate internet links (but that requires manual work).

Note that although zstd is a heavily used compression tool, it’s adding a new dependency for EL clients. Also, extra-temporal space might be required to decompress the file (but [there might be ways to avoid this](https://github.com/facebook/zstd/tree/b2c5bc16d90e15735b0dad051c6d7cd654b97cc6/contrib/seekable_format)). In any case, the main goal of this article is to provide real measurements regarding how the tail of storage-slot sizes behaves and invite more discussion around this topic.

## Usage

It is worth mentioning some facts about how EL clients can use this file:

- Since the file is read linearly, persisting a cursor indicating where to continue reading from at the start of the next block is useful.
- Keeping a list of cursor positions for the last X blocks helps handle reorgs. If a reorg occurs, it’s very easy to seek into the file to the corresponding place again.
- Clients can also preload the next X blocks preimages in memory while the client is mostly idle in slots, avoiding extra IO in the block hot path execution.
- If keeping the whole file on disk is too annoying, you can delete old values past the chain finalization point. We doubt this is worth the extra complexity, but it’s an implementation detail up to EL client teams.

# Conclusion

This article explored the preimages file’s context, problem, and solution space in the context of a tree conversion protocol evolution. None of the ideas presented here are final or are expected to have obvious consensus in ACD.

The main goal is to provide a deep enough explanation to level up as many people as possible in the community, keep progressing, and hopefully serve as a resource to speed up future ACD discussions on this topic.
