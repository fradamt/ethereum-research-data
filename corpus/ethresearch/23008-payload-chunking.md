---
source: ethresearch
topic_id: 23008
title: Payload Chunking
author: Nero_eth
date: "2025-09-01"
category: Sharding
tags: [stateless, data-availability, chunking]
url: https://ethresear.ch/t/payload-chunking/23008
views: 754
likes: 11
posts_count: 9
---

# Payload Chunking

# Payload Chunking

**tl;dr:** Split an EL block (*=payload*) into multiple mini‑blocks (“*chunks*”) of fixed gas budget (e.g. `2**24 = 16.77M`) that propagate **independently** as side cars. Each chunk carries the pre‑state it needs to execute statelessly and commits to its post‑state diff. Chunks are ordered but **can be executed fully independently in parallel**. CL commits to the set of chunk headers; sidecars carry bodies and inclusion proofs.

Validation becomes more of a continuous stream.

## Motivation

Today, blocks are large, monolithic objects that will become even larger in the future. Validation requires receiving the full block before execution can begin. This creates latency bottlenecks in block propagation and execution.

After the block is received over the p2p network, transactions are executed sequentially. We cannot start validating while downloading or parallelize execution.

[![Timeline showing today’s block validation bottleneck: full block download first, then sequential execution](https://ethresear.ch/uploads/default/optimized/3X/e/f/ef9aa8e084c0739f46b25323ca4ab5c17ab967bd_2_690x363.png)Timeline showing today’s block validation bottleneck: full block download first, then sequential execution1100×580 29.3 KB](https://ethresear.ch/uploads/default/ef9aa8e084c0739f46b25323ca4ab5c17ab967bd)

> Messages on the p2p layer are usually compressed using Snappy. The block-format of Snappy that is used on Ethereum cannot be streamed. Thus, we need to slice the block into chunks before compression.

With [EIP-7928: Block-level Access Lists](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-7928.md), the situation improves, but we’re still waiting for the download to finish before starting block validation. With 4 cores, we get the following Gantt chart:

[![Timeline under EIP-7928: execution can use access lists but still must wait for block download](https://ethresear.ch/uploads/default/optimized/3X/6/9/69db005d5633a7b8bc128ad57c867c59bec0520e_2_690x363.png)Timeline under EIP-7928: execution can use access lists but still must wait for block download1101×580 33.3 KB](https://ethresear.ch/uploads/default/69db005d5633a7b8bc128ad57c867c59bec0520e)

Instead, we can **stream blocks as chunks**:

- Each chunk contains ≤ 2**24 gas of transactions.

One could also have the chunk size increase geometrically (2**22, 2**23, …, 2**25) in gas. This would give us varying latencies for chunks, enabling better parallelization - but I’m not sure it’d be worth the complexity.

Transactions **remain ordered**. Chunks are indexed and ordered, but **independent** of each other, so they can be validated in parallel. Still, the post-state of chunk 0 is the pre-state of chunk 1.
(optional) Each chunk carries the state it needs to be executed *statelessly*.

[![Timeline with payload chunking: chunks stream in and execute in parallel while downloading continues.](https://ethresear.ch/uploads/default/optimized/3X/9/3/93c913290f6fb99396402cc0b5b1341e7d48bfc1_2_690x363.png)Timeline with payload chunking: chunks stream in and execute in parallel while downloading continues.1101×580 37.7 KB](https://ethresear.ch/uploads/default/93c913290f6fb99396402cc0b5b1341e7d48bfc1)

This shifts validation from “*download full block, then process” → “process while receiving the rest.*”

---

## Execution Layer Changes

We extend the EL block format to support chunking:

```python
class ELHeader:
    parent_hash: Hash32
    fee_recipient: Address
    block_number: uint64
    gas_limit: uint64
    timestamp: uint64
    extra_data: ByteList[MAX_EXTRA_DATA_BYTES]
    prev_randao: Bytes32
    base_fee_per_gas: uint256
    parent_beacon_block_root: Root
    blob_gas_used: uint64
    excess_blob_gas: uint64
    transactions_root: Root
    state_root: Root
    receipts_root: Root
    logs_bloom: Bloom
    gas_used: Uint
    withdrawals_root: Root
    block_access_list_hash: Bytes32
    # New fields
    chunk_count: int  # >= 0
```

There is ***no** commitment* to the individual chunks in the EL header. We only add the chunk count to it. The execution outputs (`state_root`, `logs_bloom`, `receipts_root`, `gas_used`) must be either the same as the value in the last chunk (applies to state root and withdrawals root), or the root after aggregating the chunk’s values (applies to transactions, receipts, logs, gas used, and the block access list).

### Execution Chunks

Chunks are never put on-chain; only their roots are committed.

Chunks contain the fields we would usually expect in the EL block body. Transactions are split up over chunks with a limit of `2**24` gas per chunk. Withdrawals must only be included in the last chunk. Mirroring block-level access lists, chunks come with their own chunk access list, and one could additionally add pre-state values to chunks, unlocking statelessness.

```python
class Chunk:
    header: ChunkHeader
    transactions: List[Tx]
    withdrawals: List[Withdrawal]  # only in chunk at index -1
    chunk_access_list: List[ChunkAccessList]
    pre_state_values: List[(Key, Value)] #  optional
```

Each chunk comes with a header including the chunk index. Transactions are ordered by `chunk.header.index` and their index in the chunk. Commitments to each chunk’s execution output are included in the header.

```python
class ChunkHeader:
    index: int
    txs_root: Root
    post_state_root: Root
    receipts_root: Root
    logs_bloom: Bloom
    gas_used: uint64
    withdrawals_root: Root
    chunk_access_list_root: Root
    pre_state_values_root: Root  # optional
```

To prevent proposers splitting their blocks into too many chunks, the protocol can enforce that chunks must be at least half full (\geq\frac{chunk\_gas\_limit}{2}) OR `chunk.header.index == len(beaconBlock.chunk_roots)` (*= last chunk in that block*).

---

## Consensus Layer Changes

[![Diagram of consensus changes: beacon block tracks chunk roots while execution chunks propagate via sidecars.](https://ethresear.ch/uploads/default/optimized/3X/c/f/cf54e6ba799262f55ac00159f48031a2400df630_2_690x346.jpeg)Diagram of consensus changes: beacon block tracks chunk roots while execution chunks propagate via sidecars.1180×593 91.5 KB](https://ethresear.ch/uploads/default/cf54e6ba799262f55ac00159f48031a2400df630)

Beacon blocks track chunks with new fields:

```python
class BeaconBlockBody:
    ...
    chunk_roots: List[ChunkRoot, MAX_CHUNKS_PER_BLOCK]  # SSZ roots of chunks

class ExecutionPayloadHeader:
    ...
    chunk_count: int
```

The CL receives the execution chunks from the EL via a new `ChunkBundle` container which includes the EL header and the chunks (*=similar to blobs*).

The CL computes chunk roots using SSZ’s `hash_tree_root` and puts them into the beacon block body.

### Sidecar Design

Chunks are carried in **sidecars**:

```python
class ExecutionChunkSidecar:
    index: uint64  #  chunk index
    chunk: ByteList[MAX_CHUNK_SIZE]  # Opaque chunk data
    signed_block_header: SignedBeaconBlockHeader
    chunk_root_inclusion_proof: Vector[Bytes32, PROOF_DEPTH]
```

The consensus layer ensures all chunks are available and properly linked to the beacon block body via Merkle proofs against `chunk_roots` (*=similar to blobs*).

### Networking

The proposer gossips only the lightweight beacon block with commitments (`chunk_count`, `chunk_headers_root`) on the normal `beacon_block` topic, while the heavy execution data is streamed separately as `ExecutionChunkSidecar`s across **X parallel subnets** (`beacon_chunk_sidecar_{0..X}`), deduped by `(block_root, index)`.

Initially, all nodes must subscribe to all subnets and custody all chunks. While this doesn’t reduce bandwidth/storage requirements yet, it enables the immediate benefits of parallelization. Partial custody can be added in a future upgrade once the basic mechanism is proven and/or zk-proving becomes viable.

[![Networking view: lightweight beacon block propagates fast, while heavy execution chunks are streamed across parallel subnets.](https://ethresear.ch/uploads/default/optimized/3X/4/9/49ffbba384d6547afa7aa040c41637a12eae27f9_2_690x272.png)Networking view: lightweight beacon block propagates fast, while heavy execution chunks are streamed across parallel subnets.1090×430 260 KB](https://ethresear.ch/uploads/default/49ffbba384d6547afa7aa040c41637a12eae27f9)

### Fork Choice

Fork choice requires that all sidecars are both available and successfully validated before a block is considered valid. The beacon block with the `chunk_roots` propagates quickly, but the block only becomes fork-choice eligible once every chunk has been received and inclusion-proven against the root. The beacon block still contains the EL header with all the necessary commitments (=*committing to parent block and execution outputs*). What we knew as *block body* on the EL stays empty in this design.

---

## Benefits

- Streaming validation: execution can start while other parts of the block are still downloading or busy loading from disk. Chunks are independent (if pre-state provided), or rely on the chunk-access list (with chunk-level state diffs) and the pre-block-state; multiple CPUs/cores can validate chunks simultaneously; distribute bandwidth usage over slot instead of beginning-of-slot bursts.
- Streamlined proving: ZK Provers can parallelize proving multiple chunks at the same time, benefiting from the independence of chunks.
- Stateless friendliness: since a single chunk is smaller than a block, we might consider adding pre-state values such that there is no need for local state access. A practical middle ground is to include pre-state values only in chunk 0, guaranteeing that at least one chunk can always be executed while the node loads the state required for other chunks from disk into cache.
- Future extensibility: clear path to integrate zk-proofs over chunks or going for sharded execution.

## Design Space

### Chunk Size

`2**24` gas (~16.7M) emerged as a natural chunk size:

- Max Transaction Size: As of Fusaka (EIP-7825), 2**24 is the max possible transaction size.
- Current blocks: 45M gas blocks naturally split into ~3 chunks, providing immediate parallelism
- Future blocks: Scales well - 100M gas blocks would have ~6 chunks

### Validator

1. Execution engine splits the block into chunks internally (opaque to CL) and passes them to the CL through an ExecutionChunkBundle.
2. Proposer wraps each chunk in a sidecar with inclusion proof. The proposer also computes the hash tree root of each chunk and puts them into the beacon block body.
3. Publishing happens in parallel across all subnets
4. Attesters wait for all chunks and validate them before voting

### Builders

Proposers can publish chunks as they’re finished building, and validators can start validating them even before receiving the beacon block. Since chunks contain the signed beacon block header and an inclusion proof against it, one can validate (*=execute*) chunks as they come in, trusting their source (*=proposer*).

## Open Questions & Future Work

### Progressive Chunk Sizes?

The idea of geometrically increasing chunk sizes (`2**22`, `2**23`, …, `2**25`) seems beneficial but adds complexity. The first chunk could be smaller (5M gas) with pre-state values for immediate execution, while later chunks are larger. This remains an area for experimentation.

### Partial Custody Path

While the initial implementation requires full custody, the architecture naturally supports partial custody:

- Nodes could custody only Y subnets out of X
- Reconstruction mechanisms (similar to DAS) could recover missing chunks

### Compatible with ePBS and Delayed Execution

At first glance, the proposed design seems compatible with both [EIP-7732](https://eips.ethereum.org/EIPS/eip-7732) and [EIP-7886](https://eips.ethereum.org/EIPS/eip-7886). Under ePBS, the chunk roots would likely move into the `ExecutionPayloadEnvelope`, and we’d put an additional root over the chunk roots into the `ExecutionPayloadHeader`. The PTC would not only have to check that a single EL payload is available, but that all chunks are. This is not much different from blobs.

The advantages of block chunking and independent validation scale with higher gas limits and may contribute to reducing spikiness in node bandwidth consumption.

## Replies

**daniellehrner** (2025-09-01):

I really like this proposal.

I think there could be further changes that not only allow streaming during execution, but during block building as well:

Today the whole network, except for the block builder, stands still until the builder has constructed the full block and has calculated the state root hash. This is true even with this proposal.

It might be possible to allow the builder to stream the transactions before the full block is constructed. The builder could construct a header that only contains a subset of the fields today which are known before building the block:

- PREVRANDAO
- BLOCKNUMBER
- TIMESTAMP
- etc

After that it could start to add the transactions and send them to its peers once that a chunk is full. This would decrease the time to first byte, because the builder could send chunks before the full block is ready.

Once the block is fully built the builder could send a footer which contains the missing fields like:

- BLOCKHASH
- STATEROOT
- RECEIPTSROOT
- etc.

I think there are mainly 2 downsides:

1. BALs don’t work anymore in their current form. We could convert them into chunk level access lists, but most probably increase bandwidth requirements
2. Block validation is split into two steps: validating the fields in the header → execute transactions-> validate fields in the footer. But payload chunking in its current form requires that the block hash in only validated after all the chunks have been received.

---

**Nero_eth** (2025-09-02):

Yeah, this is interesting!

I don’t think moving from block-access lists to chunk-access lists would be a major issue. The objects themselves get smaller, we gain parallelization, and there’s even room to increase the size of individual objects (for example, supporting statelessness).

In the block chunking proposal, the idea is similar: chunks can be published earlier than the EL header. Each chunk can be validated independently, and once they’re all validated, only the aggregate execution outputs need to be checked. At that stage, the EL header is required, but not before, since it only contains the chunk count and no other chunk-specific information.

---

**raulk** (2025-09-08):

Promising proposal! I support the general direction, and I think we should let the builder side stream too. That keeps progress steady and incremental across the slot and reduces peak system requirements on builders (especially important for local builders as we increase gas limits and shorten slot times).

More concretely, this is what I’m thinking.

**Make streaming first class.** I’d avoid committing to the total chunk count upfront, or to specific chunk contents. Let builders emit a chunk as soon it hits a gas budget, up to the relevant protocol caps (block gas limit, max chunks). Use either a closing trailer, or a per-chunk “last” marker. I lean towards the trailer: it keeps final commitments tidy and encapsulated. Header and trailer are small, so we can broadcast them more aggresively (e.g. higher fanout).

**Builder pipeline.** Parallelize chunk production by saturating all available CPU cores. Run one EVM per core with shared conflict detection; pin instances to OS threads if useful. Route transactions based on tx-level access list. Use speculative execution, potentially with copy-on-write snapshots to migrate a conflicting inflight transaction to another chunk on conflict (e.g. OverlayFS style). Keep shipping chunks as they’re ready. Do not wait for the full set. When the block gas limit is hit, merge pending EVMs, finalize outputs, and dispatch the final chunks. There’s probably work from the Parallel EVM world that becomes very relevant here.

**Validator pipeline.** Execute chunks as they arrive. One EVM per chunk, with shared conflict detection to reject the block on conflict (or validation against chunk-level access lists, or prestate, as you mentioned). This matches the original proposal.

**Commitments.** Treat some execution payload fields as placeholders that the trailer fills in; namely those dependent on the post-state: transactions_root, state_root, receipts_root, logs, etc. Put chunk commitments and chunk count in the trailer, together with the final proposer signature. Because the block continues being atomic, the chain can be spared of chunking details. I’d think of the chunked form as *virtual* during transit, which is then collapsed into a single committable block when appending to the ledger. If useful, we can persist chunk boundaries and metadata off-chain for P2P RPC and checkpoint sync, but not necessarily in the canonical structure.

**Networking.** Independent chunking is a win if overhead stays low. It allows parallel propagation across subnets and smoother bandwidth profiles across the slot.

**Chunk authentication without a fixed count.** All chunks are signed by the proposer. Proposer equivocation rules probably need to adapt. To strengthen the model, we can carry a running accumulator in each chunk header, and have the trailer commit to the final accumulator. Validators receiving chunks out of order can still validate taking the risk with some configured tolerance.

**Mental model.** This looks like MapReduce at the EVM level. Builders map transactions into independent execution units under conflict detection. Validators reduce by merging verified, non-conflicting results in order.

---

**preda-devteam** (2025-09-09):

This is inspiring and enlightening ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

Streamlining block reception and execution would be a smart move now that BALs are paving the way for many improvements.

Additionally, I’d like to delve into the specifics of parallel execution and the adoption of a Parallel EVM that partitions data/state architecture—something I’ve been working on. I have two questions regarding your proposal:

1. Validator/Parallel Execution
With BALs, we’ve set the stage for parallel execution—essentially a pessimistic approach to parallelization. Is this the kind of parallel execution you’re envisioning?

Once a block chunk is received by a validator, BALs provide insight into the read/write list, allowing conflict-free transactions to be executed in parallel across the validator’s multiple cores. This mechanism is similar to the pessimistic-parallel execution employed by other chains. With BALs in place, there’s significant potential to maximize parallelism and reduce state conflicts.

1. Networking/Partitioning Possibilities
You mentioned the future possibility of “partial custody,” where subnet nodes would only manage a fraction of the data. This got me thinking about the broader direction of partitioning across communication, storage, and execution. Do you see Ethereum’s future leaning more towards full sharding (partitioning across all three dimensions) or partial sharding (partitioning across one or a subset)?

A key advantage of partitioning would be overcoming the limitations of computational power in a single VM, the real opportunity here is to leverage the total processing power of the entire network. This would allow Ethereum’s performance to scale as the number of nodes increases.

---

**Nero_eth** (2025-09-09):

Great comments, thanks!

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/r/b4bc9f/48.png) raulk:

> Let builders emit a chunk as soon it hits a gas budget, up to the relevant protocol caps (block gas limit, max chunks).

Yeah, totally agree and I’d say this is already supported with the chunking approach. For DoS resistance, validators need a way to verify a chunk is signed by the rightful proposer of that slot, and this is possible with the sidecars containing the `signed_block_header`. Even though one cannot yet validate the inclusion proof, validators could still already start executing, delaying the inclusion proof until the beacon block is received.

My feeling is that this might be good enough and we would not need a commitment to the chunks different from the proposer’s signature to start processing. The beacon block essentially becomes the trailer

---

**Nero_eth** (2025-09-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/preda-devteam/48/11717_2.png) preda-devteam:

> Validator/Parallel Execution
> With BALs, we’ve set the stage for parallel execution—essentially a pessimistic approach to parallelization. Is this the kind of parallel execution you’re envisioning?

You get perfect parallelization. No need to separate tx into non-conflicting batches. With EIP-7928, every transaction can be executed independently of another.

![](https://ethresear.ch/user_avatar/ethresear.ch/preda-devteam/48/11717_2.png) preda-devteam:

> This would allow Ethereum’s performance to scale as the number of nodes increases.

While I agree that this is an interesting concept, it feels like we’re still kinda far from such a world. DAS, as done with blobs is a great role model for what we should strive for on the EL as well. zkVMs will further change how we think about related concepts, so, still rather difficult to tell how things evolve. Execution sharding has huge potential for scaling and is definitely on the list.

---

**gballet** (2025-09-19):

That has potential, but I do see a lot of issues as well.

#### The Bad

- The obvious one is complexity: Chunks need to travel over the network and be executed in due time. Under normal conditions, I think it’s to be expected that the validators will execute these Chunk optimistically and wait for the next, but if for whatever reason the chunks are not being distributed, the rational thing to do will be to wait for all the chunks to be downloaded anyway so that they can be executed in parallel. And if that is the case, then why not simply give a single block and add the same information to allow for chunk execution in parallel without having to distribute the data over the network and gope that the recipient will collect all the pieces in time?
- It is much faster to download a big chunk of data than many many small bits and pieces. To be seriously considered, this proposal should effectively make some measurements as to how much time is saved executing in parallel, and in what kind of load. I don’t believe it’s unrealistic to expect that the execution will be spending most of its time waiting on the data to end up downloading, then immediately execute the chunk and wait for the next one. In particular, it should be explained why this is a better approach than simply packaging the transactions in such a way that you could start executing as the data is being downloaded.
- This is yet another proposal that increases the bandwidth requirements and also puts a lot of work on the proposer to hash the work for the validators.
- I do not think it will help the ZKVM approach at all, in the sense that proving is very slow and so you will lose all the benefits of parallel proving. I understand that the end goal would be to have carious entities on the network working on a single chunk at a time and sharing them over the network, with the execution being proven in parallel by the validator without even needing to download the chunks. But there is the problem of whom commits to building these proofs? The builder itself will not be able to provide any commitments that these proofs are correct.
- In the case when most txs depend on each other, e.g. sandwiching blocks, your chunks are going to be very small.
- I might be missing something on the CL side, but it seems to me that this is very susceptible to Spamming because one could simply spam a lot of chunks even if they are not part of the block. How is the executor supposed to know the connection between the chunks and the block, if no commitment is made? The sidecar would require some hefty proving, which a simple hash could do instead.

So in summary, I think proper research should be conducted in order to find out if this is really worth the complexity.

#### The good

I think most of the potential comes from the idea that blocks could actually be produced by many builders at the same time, and this is a good first step for this to happen. In a way you could represent this as inclusion list being just actual execution instead of a list of instructions, and if for whatever reason they are not executable, then they are still part of the block, but they are not canon.

So in my view as such it doesn’t bring very much, but if we could somehow make it also a way to share building between many clients and many nodes, then this would have really the potential to make a dent in terms of scalability.

#### Question

- Why are withdrawals included in a chunk? They could still be part of the block and be optimistically executed in parallel instead of waiting for the last chunk, I doubt there will be people trying to use their withdrawal address in the same block as the withdrawal, and if this happens, it can be easily worked around.

---

**Nero_eth** (2025-09-19):

Thanks for the questions and feedback!

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> then why not simply give a single block and add the same information to allow for chunk execution in parallel without having to distribute the data over the network and gope that the recipient will collect all the pieces in time?

This is what Block-Level Access Lists already give you, in combination with EIP-7825 (the tx gas limit of 16.77M). Each transaction is executable fully independently from another, thus, if you wait for all chunks to be downloaded just to then start executing chunks in parallel, then you arrive at where we’re at with BALs. The only way to improve on this would be by enabling validators to start executing earlier, even before everything is received.

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> It is much faster to download a big chunk of data than many many small bits and pieces. To be seriously considered, this proposal should effectively make some measurements as to how much time is saved executing in parallel, and in what kind of load.

Yeah agree, measurements are needed. In any case, this would speed up the “time to validation” for validators, independently if builder make use of the smaller chunks and actually publish them earlier, or if they wait until the last second. Since the absolute size of the object you need to download is smaller (much smaller if you compare 16.77M (=chunk size) to 60M or 100M (=future block gas limit)). The smaller object will propagate faster, shortening the time from beginning of propagation to beginning of validation.

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> This is yet another proposal that increases the bandwidth requirements and also puts a lot of work on the proposer to hash the work for the validators.

True but only marginally (a few 32 bytes values that were in the block header are now in all chunk headers; maybe a few hundred bytes overhead) but in return we have a less spiky bandwidth usage over the slot. Also, I keep hearing that our gossip network was never created with the intent of sending around large messages ( cc [@raulk](/u/raulk), [@MarcoPolo](/u/marcopolo)), and with increasing gas limits, we have no other option on the table to somehow limit message sizes.

If we have chunks being statelessly validatable, we’d ensure that they are executable independently from the order in which you receive them. This would add a lot of data on top, I agree but maybe, if we don’t make them stateless (like mentioned in the post) but instead require validators to have full state, then we still get the benefits of being able to independently download but then you can only execute the second chunk if you already have the first (using it’s chunk-level access list).

Another alternative would be to have the chunk access list travel as a sidecar too, exclusively providing state updates to validators, whereas the chunks with the actual data travels independently.

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> I understand that the end goal would be to have carious entities on the network working on a single chunk at a time and sharing them over the network,

More like, have various entities work on different chunks, but since this proposal doesn’t affect builder or prover economics, we might just not care to much about it at this point. Validators would still need to download all chunks.

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> In the case when most txs depend on each other, e.g. sandwiching blocks, your chunks are going to be very small.

Note that transactions distributed over chunks still enjoy the same atomicity as if they were in the same block. We could enforce that chunks must always be at least 1/2 full (measured in gas used), otherwise invalid. Thus, you can do a sandwich starting in chunk 0 and finishing in chunk 1. The post state root of the last tx in chunk 0 is the pre state root of the first transaction in chunk 1.

The proposal doesn’t really focus on builders and provers but on validators and how we could relief them from work in the critical path.

Let’s assume there are no provers yet (which is true today) and builders play timing games until the last possible second. Even then, validators would profit by being able to parallelize between validating the first chunk while downloading the rest. Builders *can* publish_ chunks earlier, just like provers *can* provide proves for chunks without seeing the full block, but this is a different topic.

My argument is that if we don’t chunk things in-protocol, then we may just increase the time of everything (upload, download, validation) linearly without having any way to parallelize between the 3.

![](https://ethresear.ch/user_avatar/ethresear.ch/gballet/48/4230_2.png) gballet:

> Why are withdrawals included in a chunk?

Blocks on the EL wouldn’t exist anymore, just chunks and a header. Today, withdrawals are applied after executing all transactions. We could enforce that only the last chunk is allowed to contain withdrawals and then process them just like today.

