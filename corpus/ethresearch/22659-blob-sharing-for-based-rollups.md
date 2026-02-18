---
source: ethresearch
topic_id: 22659
title: Blob Sharing for Based Rollups
author: AnshuJalan
date: "2025-06-23"
category: Layer 2
tags: []
url: https://ethresear.ch/t/blob-sharing-for-based-rollups/22659
views: 458
likes: 10
posts_count: 1
---

# Blob Sharing for Based Rollups

Co-authored by [Anshu Jalan](https://x.com/aj_jalan) and [Lin Oshitani](https://x.com/linoscope), both Nethermind. Thanks [Antony Denyer](https://x.com/tonydenyer?lang=en) for feedback and discussions. This work has been supported by the Ethereum Foundation ESP grant FY24-1837.

## Motivation

---

Based rollups are currently facing a major inefficiency: they are spending large amounts of ETH to post blobs that are often only partially filled. This not only leads to significant costs for the rollup operators but also results in wasteful consumption of blob space. For example, in a recent sequence of blob submissions by Taiko, the fill rates were approximately [7%](https://blobscan.com/tx/0x90d48510ed0514d2d1ec1ab020318e36da70c76994cd0fbc961428291a799af0), [33%](https://blobscan.com/tx/0x5b8749f43def4edfffd7626f2bd965af02d49177ed76839b653782f94ff32293), and [55%](https://blobscan.com/tx/0x95250e9aed0b181aae68d324dbbab3d96b78a0a159fcbd5122463c0a0dda6216), respectively—far below optimal usage.

As more low-traffic based rollups enter the ecosystem, we can expect the problem to grow worse. Unlike centralized-sequenced rollups that can delay posting to batch more transactions and fill blobs more efficiently, based rollups don’t have that flexibility.

However, there is a key architectural feature of based rollups: the presence of a natural “shared proposer.” This shared proposer not only enables intra-slot proposal aggregation but also allows us to aggregate multiple proposals from different rollup inboxes into a single set of blobs within a single transaction, thus allowing for a blob to fill up with proposals across multiple based rollup inboxes.

## Design Principles

---

Our goal is to create a protocol that is both **maximally simple** and **maximally generic**, enabling based rollups to efficiently share a single set of blobs with other based rollups, even across different rollup stacks.

Below are the two key design choices that we took to achive this goal:

- Shared Proposer as the Blob Aggregator
 A key architectural feature of based rollups is that they have a shared proposer: the L1 proposer or a builder / preconfirmer acting for that proposer. We utilize this shared proposer as the blob aggregator. It gathers all rollup batches, merges them off-chain, and posts a single, well-filled blob set on-chain. Because one actor performs both L2 block building and aggregation, no additional off-chain coordination is required, greatly simplifying the protocol.
- EIP-7702 for One-Tx Fan-out
 EIP-7702 allows a wallet to attach a temporary code that is active only during the transaction that includes it, giving the EOA smart contract capabilities without changing its address. The shared proposer can use this to load a tiny batcher contract, which calls every rollup inbox and passes the needed metadata in one L1 transaction. Because msg.sender still resolves to the original proposer address, inbox contracts that rely on it for proposer identification need little or no modification.

## Protocol Description

---

### Terminology: Blob Segment

A ***blob* *segment*** (or just ***segment***) refers to a specific, logically distinct portion of a blob intended for use by an individual rollup or target system. A single blob can be divided into multiple blob segments, and one segment can span across multiple blobs.

[![Blob Segment Definition](https://ethresear.ch/uploads/default/optimized/3X/d/2/d22a6d82dd3d4d0da32faae1c71fdc916fe60b2d_2_690x153.png)Blob Segment Definition1010×224 49.1 KB](https://ethresear.ch/uploads/default/d22a6d82dd3d4d0da32faae1c71fdc916fe60b2d)

### Requirements

At the core, a blob sharing protocol’s job is to convey the following two elements to the rollup execution:

- A set of blob(s) that is logically divided into segments.
- Segment metadata that describes where each segment starts, how long it is, and any other details required to locate and decode it.

With these two pieces, the rollup execution can fetch blobs and then extract their relevant segment.

### Core Protocol Flow

Our blob sharing protocol works as follows:

[![Core Protocol Flow](https://ethresear.ch/uploads/default/optimized/3X/4/0/40ea4c794420b1642dc700ddcfe3bbad0dd1d34f_2_689x411.png)Core Protocol Flow2721×1622 504 KB](https://ethresear.ch/uploads/default/40ea4c794420b1642dc700ddcfe3bbad0dd1d34f)

1. The shared proposer first builds the L2 blocks for each rollup, then forwards them to a local blob aggregation service.
2. The blob aggregation service merges the blocks from all rollups, packages them into a shared blob set, and hands the blobs, along with per-rollup segment metadata (metadata_A and metadata_B in the diagram), to a batcher contract that the shared proposer installs via EIP-7702.
3. This batcher contract then submits the blob set and routes the segment metadata to every rollup inbox in a single L1 transaction. It also emits an event for every segment for off-chain monitoring and verification.

In rollups that do not operate on a smart contract based inbox, such as rollups created via the OP-stack — their derivation pipeline can rely on events emitted by the intermediate batcher contract.

The batcher can be a generic, minimal contract like `MinimalBatcher.sol` ([code](https://github.com/NethermindEth/blob-sharing-poc/blob/024e6207789f5c03b11a0d1088c6e4daf585e866/src/MinimalBatcher.sol)) from our demo implementation:

```solidity
/// @title Minimal Batcher
/// @dev This contract becomes the EIP-7702 account-code for the proposer's EOA
contract MinimalBatcher {
    struct Call {
        address target;
        uint256 value;
        bytes data;
    }

    error INVALID_ETHER_AMOUNT();
    error NOT_AUTHORIZED();
    error CALL_FAILED(uint256 index);

    event ExecutedCall(address indexed target, uint256 value, bytes data);

    function executeBatch(Call[] calldata calls) external payable {
        require(msg.sender == address(this), NOT_AUTHORIZED());

        uint256 totalValue;
        for (uint256 i; i

The aggregator’s key submits this transaction from its own EOA, which has the Minimal Batcher’s code set as its EIP-7702 EOA code.

- This allows the aggregator to act as the transaction sender within the Taiko inbox without requiring protocol changes to support a separate batching contract.

Please open the following tweet to view the demo video, which showcases two Taiko chains progressing through a shared blob:

> Based Rollups have been burning cash posting incompletely filled blobs.As a solution, @linoscope and I have been working on a maximally simple and maximally generic blob-sharing mechanism, leveraging EIP-7702.⬇️🧵 pic.twitter.com/XayL1LElWT
> — Anshu Jalan | Nethermind (@AJ_Jalan) April 8, 2025



## Key Features

---

In this section, we highlight the key features of the proposed minimal blob sharing protocol.

### Segment Metadata Interface Flexibility

The blob sharing protocol is **agnostic to the exact structure of the blob segment** used by individual rollups. It is up to each rollup’s inbox contract and offchain consensus client to define and interpret blob segment metadata in a way that fits their architecture. The aggregator service will be responsible for producing segment metadata in the format expected by the rollup it is proposing for.

However, there are basic requirements that any blob segment interface must satisfy: it must contain enough information to **uniquely locate and extract a segment from the blob set**.

For example, the following two interfaces—while slightly different—both meet the essential requirements:

```solidity
struct Metadata_A {
    uint64 firstBlobIndex;  // Starting blob index
    uint8 numBlobs;         // Number of blobs spanned
    uint64 offset;          // Byte offset within the first blob
    uint64 length;          // Total byte length of the segment
}

struct Metadata_B {
    uint64 firstBlobIndex;  // Starting blob index
    uint64 bytesOffset;     // Byte offset within the first blob
    uint64 bytesSize;       // Total byte size of the segment
}
```

This flexibility allows rollups to adopt their own conventions, as long as they maintain a minimal standard for locating blob data.

### Compressed vs. Uncompressed Segment Targeting

The protocol supports blob segment metadata referencing either compressed or uncompressed data. In most cases, blobs store transaction batches in compressed form, and the blob segment points directly to the compressed bytes (left side of the diagram). Rollups may want to benefit from ***shared compression***, where transaction batches from multiple rollups are compressed together. In such cases, the segment metadata may refer to a section of the uncompressed payload (right side of the diagram), allowing for blob-space efficiency when rollups use compatible compression schemes.

[![Compressed vs Uncompressed Segment](https://ethresear.ch/uploads/default/optimized/3X/0/2/02626db93c2410174f3382d00df9624542cc85bc_2_690x277.png)Compressed vs Uncompressed Segment2991×1203 354 KB](https://ethresear.ch/uploads/default/02626db93c2410174f3382d00df9624542cc85bc)

Below is an example of what the segment metadata struct might look like with shared compression:

```solidity
struct Metadata {
    bytes compressionAlgo;     // The compression algorithm for decompressing the blob
    uint64 firstBlobIndex;     // Starting blob index
    uint8 numBlobs;            // Number of blobs spanned
    uint64 uncompressedOffset; // Byte offset into the uncompressed data where the segment starts
    uint64 uncompressedLength; // Byte length of the segment in the uncompressed data}
}
```

### Proposal Parameter Placement

The blob sharing design is also agnostic to **where the rollup inbox expects proposal metadata,** such as blob segment information, to be located.

- For example:

Taiko expects the metadata to be passed in calldata.
- OZ’s minimal rollup expects it to be embedded within the blob itself.

This abstraction allows each rollup to consume proposal data in its preferred manner.

[![Proposal Parameter Placement](https://ethresear.ch/uploads/default/optimized/3X/9/e/9e2d8542778ef2476740b5a66b53a034edca41e4_2_690x304.png)Proposal Parameter Placement3356×1480 347 KB](https://ethresear.ch/uploads/default/9e2d8542778ef2476740b5a66b53a034edca41e4)

### Stack Agnostic

The above features together make the protocol fundamentally **stack-agnostic**.

- Whether a rollup expects metadata in calldata or blob,
- Whether it uses custom compression or shared compression,
- And whether it defines its own blob segment interface

All of these are isolated concerns, allowing the protocol to serve a diverse ecosystem of based rollups.

With more based rollup stacks expected to emerge—such as  [Taiko](https://github.com/taikoxyz/taiko-mono), [Surge](https://github.com/NethermindEth/surge-taiko-mono) by Nethermind, [ENS rollup with Linea](https://x.com/ensdomains/status/1889359623070826566), [Spire’s based OP stack](https://github.com/spire-labs/based-stack), and [OZ’s minimal rollup](https://github.com/OpenZeppelin/minimal-rollup)—this protocol is designed to accommodate all of them **without requiring them to conform to a specific aggregation-aware design**.

Teams that control the full stack can still layer on more sophisticated blob-sharing schemes within their stacks. This minimal protocol is intended to serve as the baseline for a simple, common denominator that enables drastically different rollups to share blobs.

[![Stack Agnostic](https://ethresear.ch/uploads/default/optimized/3X/5/d/5d8bce2d4ce269864c209690412f28d8d6d04b48_2_690x459.png)Stack Agnostic3119×2078 305 KB](https://ethresear.ch/uploads/default/5d8bce2d4ce269864c209690412f28d8d6d04b48)

## Future Work

---

While the current protocol demonstrates a minimally complex and broadly compatible approach to blob sharing for based rollups, a few avenues remain open for refinement and exploration:

### Integration into the Taiko Stack

One of the immediate next steps is to finalize the work-in-progress implementation and fully integrate the blob aggregation service into the Taiko rollup stack.

### Blob Aggregation as Builder Commitments

We aim to investigate a more generalized blob-sharing protocol that is not limited to based rollup use cases. Conceptually, this would resemble *blob aggregation as builder commitments*, where the L1 builder (or proposer):

- Receive segments through RPC or P2P.
- Publishes a commitment to include the segments in a shared blob.
- Assembles and posts the final shared blob in their L1 slot.
- Get slashed if they do not publish blob(s) with the committed segments in by the L1 slot. This can be achieved, for example

by using a ZK proof that a given set of blobs does not include a committed segment, or
- by losing reputation by being publically known to equivocate on the commitment.

This needs further consideration, such as:

- Per-segment fee payment: How does segment submitters pay fees to the proposer in a trustless manner? Maybe have the L2 inbox contract pay the blob aggregator some fee specified in their payload?
- Blob-packing problem: Optimally packing multiple (segment size, fee) pairs into a blob is essentially the Knapsack problem, which is NP-complete. This isn’t a major concern when the number of segments is small, but as it grows, heuristic or approximate methods may be necessary.

## Related Work

---

- Blobsy Blob Aggregator:

GitHub - Blobsy-xyz/blobsy-aggregator: Service designed to aggregate blob segments and post them on the Ethereum blockchain as blob-carrying transactions.
- Blob Aggregation - Step Towards More Efficient Blobs

Blob sharing work by Spire:

- https://x.com/Spire_Labs/status/1892030335212454308
- https://paragraph.com/@spire/fair-fees-for-shared-space-pricing-blob-aggregation-with-shapley-values
- https://paragraph.xyz/@spire/shared-blob-compression

Write up by [Dapplion](https://x.com/dapplion?lang=en) on the topic: [Blob sharing protocol - HackMD](https://hackmd.io/@dapplion/blob_sharing)
Blob-sharing Service by Ephema: https://blobfusion.ephema.io/
