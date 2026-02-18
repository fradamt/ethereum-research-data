---
source: ethresearch
topic_id: 1705
title: Blob serialisation
author: JustinDrake
date: "2018-04-11"
category: Sharding
tags: [serialization]
url: https://ethresear.ch/t/blob-serialisation/1705
views: 13943
likes: 33
posts_count: 29
---

# Blob serialisation

**TLDR**: We propose a serialisation scheme for blobs in collation bodies. Credits to [@prestonvanloon](/u/prestonvanloon) for suggesting the main construction and for providing the great illustration.

**Construction**

Collation bodies (of size 2^n bytes for some n \ge 5) are partitioned into 32-byte chunks. The first byte of every chunk is the “indicator byte”, and the other 31 bytes are “data bytes”. We call the 5 least significant bits of indicator bytes “length bits” with value ranging from 0 to 31.

Blob data is partitioned across data bytes from left to right, with every chunk holding data for at most one blob. If the length bits are zero then the corresponding chunk is “non-terminal”, with all 31 data bytes holding blob data. Otherwise the chunk is “terminal” marking the end of the current blob, with the data bytes holding as many blob bytes (packed to the left) as specified by the length bits.

The illustration below shows a 4-chunk collation body serialising two blobs. The first (in blue) has length 32 and the second (in orange) has length 61. The white bytes are the indicator bytes, and the grey bytes are ignored.

[![image](https://ethresear.ch/uploads/default/original/2X/5/5fb1dc19e3f875755ef96ae82a13dd058d02d051.jpg)image957×412 48.5 KB](https://ethresear.ch/uploads/default/5fb1dc19e3f875755ef96ae82a13dd058d02d051)

For the purpose of blob delimitation the blob parser ignores:

- Data bytes of terminal chunks not holding blob data
- Chunks after the last terminal chunk
- The 3 most significant bits of indicator bytes

The 3 most significant bits of terminal chunks are 3 blob flags. The first blob flag is a `SKIP_EVM` flag to avoid execution of the blob by the default EVM. The other two flags are reserved for future use.

The default EVM charges gas for blob data proportionally to the number of chunks used.

**Remarks**

- The parser never throws.
- All blobs are terminated, and have 3 flags.
- Blobs are at least 1 byte and at most 31*2^{n-5} bytes long.
- Data ignored by the parser can set arbitrarily, e.g. to squeeze extra data.
- 32-byte hashes in blobs can be truncated to 31 bytes for packing into a single chunk, and witnessing with a single Merkle path.
- The terminal chunk of blobs of length a multiple of 31 bytes can hold no blob data.

## Replies

**vbuterin** (2018-04-12):

In the diagram, the first byte being 00011111 *is* a valid way of saying “the next 31 bytes in this chunk are part of the blob, but it’s terminal”, correct?

I don’t really see any reason why not to do that.

---

**JustinDrake** (2018-04-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> the first byte being 00011111 is a valid way of saying “the next 31 bytes in this chunk are part of the blob, but it’s terminal”, correct?

Correct.

~~Are you asking in regards to the remark “The terminal chunk of blobs of length a multiple of 31 bytes can hold no blob data.”? If so, I was just pointing out an edge case/gotcha for developers where there are *two* ways of serialising the same blob.~~

---

**jannikluhn** (2018-04-12):

What advantages does this scheme have over RLP encoding all blobs and concatenating them (`RLP(blob) ++ RLP(blob) ++ ...`) or, alternatively, `RLP([blob, blob, ...])`? RLP encoding seems simpler, especially considering that blobs itself will still need to be encoded in some way and RLP seems to be the obvious choice for that. Some differences I can see:

- Chunks may contain data from multiple blobs. Is there a problem with that? I guess verifying
Merkle proofs of inclusion gets slightly more complicated but that shouldn’t be a big deal. To avoid that one could pad with zeros (so RLP(blob) ++ padding ++ ... or padding ++ RLP([blob, padding, blob, padding, ...])
- No space wasted for indicator bytes or post-terminal data.
- No support for blob flags. We could introduce them by replacing RLP(blob) with RLP([flags, blob]), with the advantage of allowing for an arbitrary number of flags (three seems quite low to me if there will be multiple execution engines)
- There can be invalid collations. Execution engines could treat those simply as empty collations.

---

**vbuterin** (2018-04-12):

This encoding format preserves the properties that:

- Everything is a valid encoding of something (needed to cleanly separate questions of availability and validity)
- You can prove existence of a blob in the blob list by only providing Merkle branches to the blob contents

Justin’s scheme satisfies both properties. RLP satisfies neither. For a particularly egregious example of RLP internal ambiguity, consider something like:

```
0xb0afaeadacabaaa9a8a7a6a5a4a3a2a1a09f.......83828180
```

Any suffix of that RLP data is itself valid RLP, so a Merkle proof of membership of any supposed sub-chunk doesn’t actually validate that that chunk actually is a chunk in the full data.

---

**jamesray1** (2018-04-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> 32-byte hashes in blobs can be truncated to 31 bytes for packing into a single chunk, and witnessing with a single Merkle path.

How exactly would you compress a pseudo-random 32 byte hash into 31 bytes?

---

**vbuterin** (2018-04-18):

Truncated, not compressed. Just kick off the first byte.

---

**jamesray1** (2018-05-08):

Working on this now, there may be an opportunity for optimization…

To avoid having to set the `skip_evm` flag for every chunk in the blob, we could instead store how many chunks a blob takes up. This could be done in the second byte of a chunk, similarly to the length bits for a terminal chunk in the first byte. Additionally, if a blob takes up less than or equal to 31 bytes (one chunk), then it could be stored in bytes 2 to 32 of a chunk as per usual, due to the non-zero length bits in a terminal chunk. To clarify, assuming consecutive ordering of chunks for each blob, if the first byte of a chunk of a new blob that is after a terminal chunk (from the last blob) has non-zero length bits, then it is also the last chunk of the blob, thus you don’t need a second byte telling you how many chunks the blob takes up. While if the length bits are zero, then the second byte can contain the length of the blob in chunks. Then in the next non-terminal chunks of the blob, there does not need to be a `skip_evm` flag (since you can have it in just the first chunk of the blob, unless we want to skip some chunks of a blob, but not others, but then you could just submit separate blobs) or length bits, so the blob data in these chunks could take up the full 32 bytes.

---

**prestonvanloon** (2018-05-08):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> we could instead store how many chunks a blob takes up

Something to think about is that blobs may not terminate at the end of a chunk.

How will you indicate this to the serializer?

---

**jamesray1** (2018-05-09):

That would be done by the length bits in the first byte of a chunk, no? If non-zero, the length of the data in the 31 bytes is the length of the length bits. E.g. 10 = 10 bytes. The rest of the bytes are ignored.

---

**prestonvanloon** (2018-05-09):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> That would be done by the length bits in the first byte of a chunk, no?

Right, but aren’t you proposing to remove that and have a single indicator byte for each blob to explain how many chunks it spans and whether or not should be executed via EVM? Or what is the optimization?

---

**jamesray1** (2018-05-09):

I edited my comment above, let me know if it’s still not clear.

---

**jamesray1** (2018-05-14):

Any comments, anyone? [@prestonvanloon](/u/prestonvanloon)

---

**JustinDrake** (2018-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/jamesray1/48/4269_2.png) jamesray1:

> To avoid having to set the skip_evm flag for every chunk in the blob

When I wrote “The first blob flag is a `SKIP_EVM` flag” I mean that there’s only one `SKIP_EVM` flag for the whole blob (namely the first flag of the first chunk, which happens to be the first blob flag). The other flags for other chunks are ignored by the parser and can be set arbitrarily, e.g. to squeeze extra data.

BTW, I’m now not sure the `SKIP_EVM` flag is a good idea because it complicates anti-replay logic to avoid non-EVM transactions being executed as EVM transactions and vice versa.

---

**jamesray1** (2018-05-14):

![](https://ethresear.ch/user_avatar/ethresear.ch/justindrake/48/649_2.png) JustinDrake:

> BTW, I’m now not sure the SKIP_EVM flag is a good idea because it complicates anti-replay logic to avoid non-EVM transactions being executed as EVM transactions and vice versa.

Good point, didn’t think of that! If we don’t use a `SKIP_EVM` flag I’ll need to rewrite [Blob serialization v 5 + reorganizations by jamesray1 · Pull Request #67 · Drops-of-Diamond/diamond_drops · GitHub](https://github.com/Drops-of-Diamond/diamond_drops/pull/67).

---

**jamesray1** (2018-05-15):

I’ve just been writing up a way to serialize collation bodies that correspond to the same blob into a `BlobBodies` struct, however I see now that this struct would need to contain a blob hash, and hence when a blob is serialized into a chunk it’s contents should also be hashed, and that hash should then be included into each collation body. However, a problem with that is that there may be more than one blob in a collation body, but not in a chunk. Additionally, it adds a verification overhead to check that each `Body` in `BlobBodies` has the same `blobhash`.  So there would need to be a solution for that, and due to the Verifier’s Dilemma, this would be infeasible to do on the blockchain (at least as it is currently), but could be done offchain with Truebit. Of course, the fallback is that there is just no ability to put blobs on the blockchain that are bigger than a megabyte, which limits the usability of Ethereum, particularly for big data, etc.

---

**jamesray1** (2018-05-21):

Blob serialization release: https://github.com/Drops-of-Diamond/diamond_drops/releases/tag/v0.3.0-a

---

**tim** (2018-05-24):

Are there any test cases that client implementations can use to conform the the specification? e.g. Ethereum tests for RLP https://github.com/ethereum/tests/tree/develop/RLPTests [@JustinDrake](/u/justindrake) [@vbuterin](/u/vbuterin)

---

**jamesray1** (2018-05-25):

[@tim](/u/tim) you probably already know, but there are lots of unit tests for blob serialization in our repo [here](https://github.com/Drops-of-Diamond/diamond_drops/blob/94206affb0ac60e9e467e467f3d53af75dbc4f97/node/src/modules/collation/blob.rs#L259). Just clone the repo, install cargo, `cd node` and run `cargo test node`, or run all the tests as in the readme. But having a common test suite for sharding would be good. We could potentially use Rust for that, either directly via bindings with [Rust’s FFI, or using the C ABI](https://doc.rust-lang.org/book/second-edition/ch19-01-unsafe-rust.html#using-extern-functions-to-call-external-code). Also converting to Wasm and then to JS is another possibility that has apparently been made rather convenient.

---

**jannikluhn** (2018-05-25):

For test data also see https://github.com/ethereum/py-evm/blob/master/tests/core/test_blob_utils.py#L33

There are no standardized JSON tests for this yet.

---

**terence** (2018-05-25):

For test in Go, see: https://github.com/prysmaticlabs/geth-sharding/blob/master/sharding/utils/marshal_test.go


*(8 more replies not shown)*
