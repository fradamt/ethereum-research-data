---
source: magicians
topic_id: 4555
title: "EIP-2926: Chunk-Based Code Merkleization"
author: axic
date: "2020-08-31"
category: EIPs
tags: [evm, eth1x, core-eips]
url: https://ethereum-magicians.org/t/eip-2926-chunk-based-code-merkleization/4555
views: 5964
likes: 6
posts_count: 22
---

# EIP-2926: Chunk-Based Code Merkleization

Discussion topic for

https://eips.ethereum.org/EIPS/eip-2926

> Code merkleization, along with binarification of the trie and gas cost bump of state accessing opcodes, are considered as the main levers for decreasing block witness sizes in stateless or partial-stateless Eth1x roadmaps. Here we specify a fixed-sized chunk approach to code merkleization, outline how the transition of existing contracts to this model would look like, and pose some questions to be considered.

## Replies

**pipermerriam** (2020-09-02):

I think it would be worth explicitely forbidding `0xffffffff`as a key for a chunk.  This fits into the practically we won’t ever have this problem, but in theory, long enough code would overwrite the metadata entry.

---

**pipermerriam** (2020-09-02):

Cool to see the EIP, just gave it a read-through.  At the risk of bike shedding ![:nauseated_face:](https://ethereum-magicians.org/images/emoji/twitter/nauseated_face.png?v=9)   I’d like to float the idea of removing the RLP from the spec.  It looks like the only places that RLP is used are:

- RLP([METADATA_VERSION, codeHash, codeLength])
- RLP([firstInstructionOffset, C.code])

LEB128 looks suitable for `METADATA_VERSION, codeLength, and firstInstructionOffset`.  `codeHash` can just be fixed length bytes.  `C.code` can also just be the raw bytes, allowing us to just serialize these using concatenation:

- LEB128(METADATA_VERSION) || codeHash || LEB128(codeLength)
- LEB128(firstInstructionOffset) || C.code

If there is negative sentiment towards LEB128, `codeLength` could be a fixed size (?4 bytes?) big endian, and `METADATA_VERSION & firstInstructionOffset` could just be encoded as single bytes.

---

**pipermerriam** (2020-09-08):

I think SSZ is a good candidate here for simplifying the spec.

REF: [SSZ specification](https://github.com/ethereum/eth2.0-specs/blob/88cdc5bc800217475334914ee06d5bda162e3163/ssz/simple-serialize.md)

There are a number of ways the data structure could be modeled so I’ll just start off with a suggestion:

```auto
codeRoot = ssz.hash_tree_root(merklizedCode)
merklizedCode = Container[metaData, code]
metaData = Container[version, codeHash, codeLength]
codeHash = keccak(raw_bytecode)  # is this correct?
version = uint8
codeHash = bytes[32]  # uint8[32]
codeLength = uint32
code = List[Container[uint8, bytes[32]]]
```

This eliminates any need for the spec to specify how each of these individual things are serialized, as well as leaning on the existing SSZ merklization rules.

---

**sinamahmoodi** (2020-10-09):

I was experimenting with [@pipermerriam](/u/pipermerriam) 's suggested schema and was mainly curious how the backing tree would look like.

[![code-merkleization-ssz-white-bg](https://ethereum-magicians.org/uploads/default/optimized/2X/e/e03292039f2c2bb99892b3956c577314ed33f65c_2_504x500.jpeg)code-merkleization-ssz-white-bg980×971 91.4 KB](https://ethereum-magicians.org/uploads/default/e03292039f2c2bb99892b3956c577314ed33f65c)

This was my first interaction with SSZ, so sharing my takeaways here:

- Leaves are (padded to) 32 bytes
- The List type needs a limit parameter. This means if we assume a contract could have at most 1024 chunks (768 rounded to the next power of 2), regardless of the actual number of chunks the corresponding subtree will have 1024 leaves. This can affect proof size if empty subtrees are not compressed
- I used a List of bytes with a limit of 32 for the chunk code (to accommodate the last chunk which can have a length < 32), this basically doubles the number of leaves. We should probably use fixed 32 byte vectors and encode the last chunk’s length somewhere (maybe metadata)
- Also by default SSZ uses sha256. But this should be easily replaceable with keccak256

---

**pipermerriam** (2020-10-09):

[@sina](/u/sina) would you be up for posting the SSZ schema you used to remove an ambiguity?

---

**sinamahmoodi** (2020-10-09):

Yes sure: https://gist.github.com/s1na/2528af8c643f24309958515d8610a428

---

**hmijail** (2020-10-23):

Given that code necessarily has to start from address 0 and fill up addresses from there, and that PC=0 is the necessary entry point, every proof will have to send the first (leftmost) chunk. Further chunks will be progressively rarer; the rightmost side of the trie will usually be rather empty, since few contracts fill the available code space.

So I’d imagine that putting metadata in the last chunk (addresses 0xfff…) causes the merklization to send the rightmost branch with full cost of the proof for that chunk, since the hashes for that proof won’t be usually amortized by the neighboring chunks.

Therefore, wouldn’t it be better to do something like putting the metadata in an extra chunk at the leftmost side of the trie, before the code block at address 0? This way, the metadata and first block of code (both always needed) can be sent together and amortize their proofs.

Of course this means that every code block would have to be “shifted left”, but that is an exceedingly simple fix. Also, this prevents the collision risk that [@pipermerriam](/u/pipermerriam) mentioned.

Regarding the use of Merkle Patricia Tries: why not use instead a simpler Merkle Tree? Given that chunk sizes are known and are filled from address 0, the (key, value) capability of the MPT is probably not useful, since the key can be easily calculated from the tree’s (or proof’s) structure. I imagine this would simplify things / save space?

---

**vbuterin** (2020-10-24):

> Regarding the use of Merkle Patricia Tries: why not use instead a simpler Merkle Tree?

SSZ already uses simple Merkle trees, not MPTs.

> I was experimenting with @pipermerriam 's suggested schema and was mainly curious how the backing tree would look like.

Why have length for each chunk? Isn’t length already covered by the code length (and again by the chunk count)? I saw the comment “Last chunk could be shorter than 32 bytes” in the github, but I don’t think there’s any actual need to be strict about this; code ending is identical to code being followed by zeroes (for all purposes except CODESIZE, which uses length anyway).

---

**sinamahmoodi** (2020-10-28):

![](https://ethereum-magicians.org/letter_avatar_proxy/v4/letter/h/90ced4/48.png) hmijail:

> Therefore, wouldn’t it be better to do something like putting the metadata in an extra chunk at the leftmost side of the trie, before the code block at address 0?

That’s indeed possible, I can update the spec.

> why not use instead a simpler Merkle Tree

The options right now are either SSZ as Vitalik mentioned or the [binary trie](https://hackmd.io/uCWOpSrUQaytBgcO0MVkTQ). I’m slightly leaning towards the binary trie just for consistensy’s sake (specially in the proofs) and to unnecessarily introducing a new tree structure. But I’m open for either options.

> Why have length for each chunk? Isn’t length already covered by the code length (and again by the chunk count)?

Yes I missed that. Having codeLength it’s easy to infer the length of the last chunk. Thanks!

---

**hmijail** (2020-11-04):

I have just [posted](https://ethresear.ch/t/optimal-chunking-size-for-code-merklization/8185) some results of applying fixed-size chunking to >500K Mainnet blocks. The **optimal size seems to be 1 byte**: 3% size overhead vs 30% for 32-byte chunks.

This happens because:

- The median length for basic blocks is 16 bytes, with a statistical distribution very skewed towards smaller sizes.
- Smaller contiguous chunks need fewer proof hashes than bigger isolated chunks.

The tools I used have been published and the results should be repeatable in a matter of hours by anyone interested. So I hope I am not missing anything!

---

**sinamahmoodi** (2020-11-25):

I [implemented](https://github.com/s1na/go-ethereum/blob/code-merkleization-ssz/codetrie/codetrie.go) the merkleization logic in a fork of geth and measured the overhead. The goal is to determine how much contract creation gas costs need to be bumped.

The following chart shows the merkleization overhead in terms of gas in relation to the contract size, for all contracts on the Goerli testnet. Gas was computed by measuring the runtime and comparing it against the runtime of the `ECRECOVER` precompile on the same machine.

[![overhead-goerli-mpt](https://ethereum-magicians.org/uploads/default/optimized/2X/a/ac681e8757d6f6b3afcfa182d636673ae4829cba_2_690x361.png)overhead-goerli-mpt1920×1007 55 KB](https://ethereum-magicians.org/uploads/default/ac681e8757d6f6b3afcfa182d636673ae4829cba)

Here we used the hexary MPT for the code tree as specified currently in the EIP. As expected the runtime rises linearly with code size. Currently contract creation costs `200` gas per byte of code. By increasing that number to `203` we can cover this overhead. Or because the overhead is not that significant not bump the gas cost at all.

But we don’t plan to use the hexary MPT for code. There are 3 options: SSZ, a simple merkle tree, the [binary trie](https://eips.ethereum.org/EIPS/eip-3102). Here I also experimented with the [fastssz](https://github.com/ferranbt/fastssz) implementation and measured the overhead in a similar way as above.

[![overhead-goerli-comparison](https://ethereum-magicians.org/uploads/default/optimized/2X/4/47af0547fa4bbb9ba6ca46251005390f8a7ef384_2_690x361.png)overhead-goerli-comparison1920×1007 33.1 KB](https://ethereum-magicians.org/uploads/default/47af0547fa4bbb9ba6ca46251005390f8a7ef384)

Fastssz uses an accelerated sha256 [implementation](https://github.com/minio/sha256-simd) by default for hashing the tree. The column `ssz_sha` shows fastssz’s performance overhead when using the default hasher. `ssz_keccak` replaces the default hash function with geth’s keccak256 implementation. Interestingly both perform better than the MPT, even though binary trees incur more hashing. I think this might be because SSZ’s tree structure is more-or-less known at compile-time as opposed to the MPT.

The same measurement is pending for the binary trie and I’ll update the post once I have numbers on that.

---

**axic** (2021-05-31):

There were some updates regarding this EIP in the [EF-Supported Teams 2020 Pt 1.](https://blog.ethereum.org/2020/12/09/ef-supported-teams-research-and-development-update-2020-pt-2/#code-merkleization) and [2021 Pt 2.](https://blog.ethereum.org/2021/04/26/ef-supported-teams-research-and-development-update-2021-pt-1/#code-merkleization) posts.

Notable is the complete merkleization implementation in geth ussing [SSZ](https://github.com/s1na/go-ethereum/tree/code-merkleization-ssz-stats), which is explained in depth in [here](https://hugo-dc.github.io/cm-docs/).

---

**axic** (2021-06-01):

There is a related [proposal](https://notes.ethereum.org/@vbuterin/code_chunk_gas_cost) by [@vbuterin](/u/vbuterin) to first introduce charging chunk costs. I took the liberty to share it here, given there’s an implementation in [geth](https://github.com/ethereum/go-ethereum/pull/22886) which links to it, and also an implementation in [evmone](https://github.com/ethereum/evmone/pull/326).

[@hugo-dc](/u/hugo-dc) has published an [impact analysis of the proposed costs](https://notes.ethereum.org/@ipsilon/code-chunk-cost-analysis), detailing the effect of the 350 gas cost per chunk on mainnet.

---

**hugo-dc** (2021-08-11):

We’ve just published a document describing the code merkleization implementation in geth and an analysis made on ~1M mainnet blocks: [Code Merkleization Practical Implementation & Analysis - HackMD](https://notes.ethereum.org/@ipsilon/code-merkleization-implementation-analysis)

---

**luzius** (2021-09-23):

Would this be an opportunity to start allowing smart contracts to refer to existing bytecode? That way, they could simply re-use already existing code and one could potentially a lot of storage as identical smart contracts could be deduplicated.

See also:



      [github.com/ethereum/EIPs](https://github.com/ethereum/EIPs/issues/911)












####



        opened 11:16PM - 03 Mar 18 UTC



          closed 06:02PM - 05 Apr 22 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/c/cfdae5702643736d0d567b032e3b7feb2cf04d18.png)
          ivica7](https://github.com/ivica7)





          stale







## Preamble
```
EIP: 911
Title: Zero-redundancy and overhead-free bytecode de[…]()ployments
Author: Ivica Aracic <aracic@gmail.com>
Category: EVM
Created: 2018-03-04
Updated: 2018-03-04
```
## Short Description

The user should not have to pay gas for deploying the code, which already exists in the DB, because the node has no extra work in this case except of setting the correct codeHash in the account, which is covered by the CREATE fee.

## Motivation

At the time of the mainnet block number 5200035, there are 5,212,554 active contract instances referring to 64,561 unique bytecodes. 10,552 (16.34%) of these unique bytecodes have been deployed more than once, resulting in a redundancy of  2,934,072,376 bytes. This is 93.05% of the total byte size of all deployed contracts.

If we only consider the price of 200 gas / byte, which is calculated for storing the bytecode to the database, these redundancies have in sum a cost of 586,814,475,200 gas. This is ~7.45% of all gas ever spent in Ethereum. Moreover, this number looks even worse, if we consider the costs for tx input data size and historical instantiations of contracts, which do not exist anymore at the analysed block.

*Stats are generated with https://github.com/ivica7/eth-chain-stats-collector*
```
              EOAs: 24332129
Contract Instances: 5212554

  Unique Bytecodes
   with duplicates: 10552 / 64561 -> 16.344232586236274 %
      Bytes Wasted: 2934072376 / 3153359448 -> 93.04592211525136 %
        Gas Wasted: 586,814,475,200
```

Currently two patterns exist for partially solving this problem: (1) delegatecalls, and (2) extcodecopy/size.

delegatecalls allow us to deploy the code once, but again they introduce a code redundancy on its own  for the forwarder contracts. Further, they have an additional run-time overhead of ~1000 gas / call.

Extcodecopy/size will reduce transaction input size, but the deployment cost of 200 gas / byte still applies even if it is copied from an existing instance.

Both patterns are helpful, however, they fail in providing an overhead-free solution for the code redundancy problem. When we consider the fact that Ethereum is targeting x100+ in transaction output (e.g. through PoS and Sharding), we have to be careful with this problem, because it will grow proportionally.

For this reason, I am opening this EIP proposal to discuss how to tackle this problem. Below, I provide one possible solution by defining CREATEFROMADDR opcode.

## Possible Solution 1
**Specification**

Add new opcode CREATEFROMADDR(v, p, s)
* v - value in wei sent to the new contract address
* p - init bytecode memory address
* s - size of the init bytecode

CEATEFROMADDR behaves like CREATE, but it interprets the return data from the init code as a contract address and sets the codeHash of this address as the codeHash of the new contract. Since there is no insert of the code to node's database required, the additional gas costs for the code Insert can be omitted. The sender pays only a flat fee of 1400 gas instead of len(code)*200.

*TODO*: for Constantinople also specify CRATEFROMADDR2(v, n, p, s) analogous to CREATE2.

**Implementation (related to geth)**

* add a flag to evm:Create to signal which modus is used for the return data.
* Old create-opcodes will set the flag to false
* New create opcodes will set it to true
* If the flag is true, evm:Create will lookup the code hash of the address returned by init code and it will set it as codeHash of the new contract. size*200 gas fee will be replaced by a flat fee of 1400 gas.

## Possible Solution 2

Change CREATE2 specification to support the cloning of the codeHashExtend as described above. This opcode is not productive yet and we would not have to introduce new opcodes.

???

---

**gballet** (2025-07-13):

Resurrecting this EIP after 4 years. External links are no longer accepted, so I’m saving them here for future reference:

- Bytecode is the second contributor to block witness size: GitHub - mandrigin/ethereum-mainnet-bin-tries-data
- An ethresear.ch post, finding that smaller chunks are more efficient Some quick numbers on code merkelization - #3 by sinamahmoodi - Execution Layer Research - Ethereum Research

---

**etan-status** (2025-11-05):

SSZ `ProgressiveList[byte]` (EIP-7916) could be an alternative chunking scheme, if one wants to avoid the more complex-to-prove MPT (i.e., [EIP-7745: Two dimensional log filter data structure - #3 by zsfelfoldi](https://ethereum-magicians.org/t/eip-7745-two-dimensional-log-filter-data-structure/20580/3))

---

**charles-cooper** (2025-12-18):

Coming to this thread after today’s ACDE call, I’m curious about the code localization aspect of this EIP. Isn’t there a strong negative impact to performance because each chunk needs a lookup from the kv db which equates to several random reads from disk? It may be that this has already been considered but it’s not clear to me from the EIP as written – paging [@gballet](/u/gballet). Like if each chunk needs a kv lookup, that should be reflected as a state read (i.e. 2100 gas or whatever the cost of SLOAD is) every 32 bytes.

---

**gballet** (2025-12-18):

> Isn’t there a strong negative impact to performance because each chunk needs a lookup from the kv db which equates to several random reads from disk?

This has been answered during ACD: there is no assumption how the code is stored, it can still be loaded in one swoop if client performance can be maintained. Or in chunks ok 24kb. Or anything in-between. This is an implementation detail.

> Like if each chunk needs a kv lookup, that should be reflected as a state read (i.e. 2100 gas or whatever the cost of SLOAD is) every 32 bytes.

Each chunk doesn’t need a kv lookup, but paying 2100 gas on each chunk is the whole point of the EIP.

---

**benaadams** (2025-12-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/gballet/48/11012_2.png) gballet:

> there is no assumption how the code is stored, it can still be loaded in one swoop if client performance can be maintained.

So this would initially just be a complicated pricing change but wouldn’t decrease load for the clients?

Makes sense to start with EIP-7907 as the simpler pricing change to allow for larger contracts; then revisit EIP-2926 as the pricing reduction and zk friendliness later? (or would be under charging for work done/memory used etc)

Don’t see how they are incompatible both make the exact same change to the account (i.e. length)


*(1 more replies not shown)*
