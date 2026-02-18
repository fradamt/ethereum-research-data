---
source: ethresearch
topic_id: 2781
title: "Discussion: P2P message serialization standard"
author: hwwhww
date: "2018-08-02"
category: Sharding
tags: [p2p]
url: https://ethresear.ch/t/discussion-p2p-message-serialization-standard/2781
views: 5126
likes: 32
posts_count: 16
---

# Discussion: P2P message serialization standard

In today’s sharding implementers call, thanks [PrysmaticLabs for initiating a discussion of conforming sharding P2P messages](https://github.com/prysmaticlabs/prysm/issues/150), we discussed some potential candidates of RLP replacements. ([Why not RLP?](https://github.com/ethereum/wiki/wiki/Wishlist#rlp))

For the follow-up action, here is [a collaborative document of the comparison table and requirements](https://notes.ethereum.org/15_FcGc0Rq-GuxaBV5SP2Q?view). Please feel free to add inputs on the document, or elaborate/champion the solutions here. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

## Replies

**vbuterin** (2018-08-02):

If it’s at the p2p layer than canonical serialization doesn’t matter as much; it’s only consensus layer objects where we have to really worry about canonical serialization.

For consensus layer, the existing python beacon chain library has a [serialization spec](https://github.com/ethereum/beacon_chain/blob/master/beacon_chain/utils/simpleserialize.py) built in. It could probably be improved on I suppose. I think as far as desiderata go, what we’re looking for is:

- For fully statically sized data (int16, hash32, int64, etc), including static-length lists and structs of statically sized data, you can deterministically compute the byte offset to access any specific value.
- Be as simple as possible.
- It’s OK to require a type signature to decode a particular object

For statically sized data, simple concatenation (ie. as done in SimpleSerialize linked) may well be the most practical way to go. For dynamically sized data, we could also consider using hash trees (ie. whenever there is a dynamically sized list, make a Merkle tree of the leaves, and whenever there is a dynamically sized byte array, pad it and make a Merkle tree of the chunks).

---

**paulhauner** (2018-08-03):

Just FYI, there’s also a “simple serialization” [here](https://github.com/ethereum/research/tree/master/py_ssz) that is similar but distinct to the “simple serialization” used in ethereum/beacon_chain.

I’m guessing they’re the same concept at different stages of development?

beacon_chain simpleserialize:

```auto
>>> simpleserialize.serialize(b"cow", "bytes")
b'\x00\x00\x00\x03cow'
```

ethereum/reasearch/py_ssz (from README.md):

```auto
    cow -> \x00\x00\x03cow
```

---

**kladkogex** (2018-08-03):

I think introducing outside libraries may create potential security problems.  Some of these libraries tend to be complex.

RLP is good because it is simple so it can be secured simply. In general manually coded formats tend to be more secure.

If you look at existing network protocols (TLS, IPSec, WPA2 etc) most of them are manually coded. It also helps to create efficient hardware implementations.

---

**paulhauner** (2018-08-05):

I just pushed some updates to the [collaborative document](https://notes.ethereum.org/s/BykWongrm) with references to deterministic serialization.

I’m presently not in favor of using a general-purpose third-party library for consensus-layer serialization (i.e., generating the bytes that get hashed and signed).

Given that the objects requiring serialization (blocks, states, etc.) are well defined and static, I don’t see building bespoke serialization tools as overly burdensome – especially when considering the risks involved in using some third-party library (e.g., consensus fork due to a serialization library update).

When it comes to the p2p layer, it seems more reasonable to use an established library – the byte representation across the network is not really important. However, I would question the benefits of running *two* distinct serialization formats, specifically the design-complexity and performance costs.

---

**mratsim** (2018-08-05):

I agree.

One of the simplest serialization schemes that would fit all our needs and would be simple to implement and parse would be something similar to [Numpy .npy](https://github.com/numpy/numpy/blob/master/numpy/lib/format.py):

File would be:

- Magic number
- Major.Minor version
- an “offset” that tells where raw data start (or tell the size of the following part)
- a schema in JSON, for example

```
{
  "pubkey": "int256",
  "withdrawal_shard": "int16",
  "withdrawal_address": "address",
  "randao_commitment": "hash32",
  "balance": "int64",
  "start_dynasty": "int64",
  "end_dynasty": "int64"
}
```
- raw data, in packed binary (we should agree on endianness).

Advantages:

- Simple
- No issue with third party
- Can evolve thanks to versioning
- Deterministic / unique hash
- Schema support

---

**quickBlocks** (2018-08-05):

I have no idea if this makes sense, but why not use a format that works and plays well with IPFS? So, if I know the hash of a block (say, from a light client) I also, automatically, know the location of the block on IPFS. Would that make any sense? Would the serialization format have anything to do with accomplishing that?

---

**nikileshsa** (2018-08-05):

Thrift from Facebook is another serialization standard which guarantees determinism. Its also captured as part of their specification.https://thrift.apache.org/static/files/thrift-20070401.pdf

---

**hwwhww** (2018-08-06):

I think the solutions included in [multicodec](https://github.com/multiformats/multicodec/blob/7c57cd4477e391d27b8d7cc0995da9e674434ffb/table.csv) are all potential IPFS-friendly solutions. Also, [IPLD (Inter Planetary Linked Data)](https://ipld.io/) is working on this use case, they also customized Ethereum 1.0 (RLP) friendly interface.

---

**hwwhww** (2018-08-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If it’s at the p2p layer than canonical serialization doesn’t matter as much; it’s only consensus layer objects where we have to really worry about canonical serialization.

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> I think introducing outside libraries may create potential security problems. Some of these libraries tend to be complex.

Agreed. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

So during the protocol exploration/selection, we can consider:

1. Is there one serialization solution that meets all requirements?
2. If not, can we separate network layer message and consensus layer objects serializations?

Pros

We can use high-performance protocol for the network layer and use simpler protocol for consensus layer requirements for performance optimization.
3. Cons

Two different serialization protocols may increase even more annoying maintenance cost than RLP.
4. If all not, should we try to create a new custom protocol…?

---

**mratsim** (2018-08-06):

I’d like to add a few more questions as only one requirement (unique hashing) is listed at the moment:

1. Several of the library suggested (FlatBuffers, Cap’nProto, Protocol Buffers, Thrift), also do RPC. Currently we use JSON-RPC, using RPC and serialization with the same library might be desirable.
Downside: this might be unifying for unifying aka architecture astronauting, I don’t think anyone had issue with JSON-RPC. Question: Will RPC be needed in the future?
2. Currently binary serialization is implied, but not listed as a requirement. Is it?
3. Unique hashing:
Assuming we use a serialization scheme with metadata + binary data, is the unique hash requirement for only the binary data or for both metadata + binary data?
Impacts:

Binary data only:

If custom serialization:

easier on the specs of metadata, we can use JSON without having to worry about spaces or new lines.
4. We can integrate the hash to the metadata.
5. It requires either a custom serialization or a library with a schema/metadata stored in a separate file.
6. Metadata + binary data:

If custom serialization:

specs on metadata must be clear (use packed JSON, no space, no newlines)
7. We can’t store hash in metadata
8. Should work with any serialization scheme.

Iirc [@vbuterin](/u/vbuterin) wanted a format where offsets for each data field could be computed without parsing everything, i.e. schema is needed. Also a schema would allow easier checking, updating specific offset and provides benefits similar to static typing. Do we make it a requirement or a nice-to-have?

---

**veox** (2018-08-06):

![](https://ethresear.ch/user_avatar/ethresear.ch/mratsim/48/1865_2.png) mratsim:

> a schema in JSON, for example

I’m afraid this won’t cut it; or I don’t understand the purpose of including this.

A JSON schema is sufficient to describe a JSON object, which contains a collection of *unordered* key-value pairs. This schema could provide type/size annotations for the fields in `raw_data` (the consensus-layer serialised object nested within the P2P-layer serialised object), but not their positions (or potentially even size, if dynamic-length fields are permitted).

If the order of fields in `raw_data` was “known by way of external agreement”, then there is little need for a JSON schema, as the same “external agreement” could be used to agree on just about anything else.

If instead the order of keys in `schema` was made to match the order of fields in `raw_data`, then reading a field from `raw_data` would require having deserialised and parsed the `schema` first, in its entirety. This is not the same as having to deserialise the entire `raw_data`, but is a step *back* in that direction. Also, it’s kind of an “extension” to JSON schemas, not necessarily available in all JSON-handling libraries…

---

This thread seems to have shifted from discussing P2P message serialisation to discussing both P2P and consensus object serialisations. ![:confused:](https://ethresear.ch/images/emoji/facebook_messenger/confused.png?v=12)

Personally, I see no problem using different serialisation standards for the two (the latter object nested in the former), if the infra-simple NIH one is reserved for mostly-homogenous consensus-layer objects.

Cap’n Proto looks promising for P2P-layer messages, as [its schema](https://capnproto.org/language.html) provides both position and size information (for an object’s fields, within the serialised representation). This should make it relatively simple to use `mmap` in order to improve sync times, which I’ve seen work wonders in `libbitcoin` many years ago (gist: makes the network ↔ memory ↔ drive pipe nearly-transparent (with a few caveats)).

It’s probably not the best choice for consensus-layer objects, as the C’nP’s built-in types do not include some commonly-used in Ethereum (160 bits or 256 bits), so “some assembly required”.

---

**mratsim** (2018-08-06):

I think it’s more like we shifted from P2P serialization to asking ourselves if we should use the same serialization for P2P message and consensus layer objects: what are the requirements for both, are they compatible and what are the pros and cons of each library with regards to both hence the latest questions of both [@hwwhww](/u/hwwhww) and me to try to understand all concerns.

Now regarding your initial remarks for the alternative scheme I proposed:

1. The JSON can be constrained to lexicographical order for our needs. Also it includes the offset at which the data start, combining it with the type/size in the schema you have the offset. Alas computing the offset wouldn’t work if dynamic length fields are to be serialized.
2. External agreement take several forms:

Specification defined. Then everyone implements the specs. Serialization should include at least spec version and then can be only binary in this case.
3. Before sending raw data, send the schema, then the data. This is similar to what I proposed.
4. True, we need to read the schema to deserialize, it’s replacing the need of external agreement, everything is done in a single handshake.

---

Regarding consensus layer objects, a colleague reminded me that the following properties were desirable which prevents using an off-the-shelf solution at all: [Blob serialisation - #5 by vbuterin](https://ethresear.ch/t/blob-serialisation/1705/5)

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)[Blob serialisation](https://ethresear.ch/t/blob-serialisation/1705/5)

> This encoding format preserves the properties that:
>
>
> Everything is a valid encoding of something (needed to cleanly separate questions of availability and validity)
> You can prove existence of a blob in the blob list by only providing Merkle branches to the blob contents
>
>
> Justin’s scheme satisfies both properties. RLP satisfies neither. For a particularly egregious example of RLP internal ambiguity, consider something like:
>
>
>
> ```auto
> 0xb0afaeadacabaaa9a8a7a6a5a4a3a2a1a09f.......83828180
> ```
>
>
>
> Any suffix of that RLP data is itself valid RLP, so a Merkle proof of membership of any supposed sub-chunk doesn’t actually validate that that chunk actually is a chunk in the full data.

---

**mratsim** (2018-08-07):

I’ve been playing with the serialization scheme I proposed on the following:

```
## This is Nim code, packed to avoid padding.
type
  ValidatorRecord {.packed.} = object
    # The validator's public key
    pubkey:  Uint256
    # What shard the validator's balance will be sent to
    # after withdrawal
    withdrawal_shard: int16
    # And what address
    withdrawal_address: EthAddress
    # The validator's current RANDAO beacon commitment
    randao_commitment: Hash256
    # Current balance
    balance: int64
    # Dynasty where the validator  is inducted
    start_dynasty: int64
    # Dynasty where the validator leaves
    end_dynasty: int64

when isMainModule:
  let x = ValidatorRecord(
    pubkey: 123456789.u256,
    withdrawal_shard: 4455,
    withdrawal_address: hexToPaddedByteArray[20]("0x1234"),
    randao_commitment: Hash256(data: hexToPaddedByteArray[32]("0xAABBCCDDEEFF")),
    balance: 100000,
    start_dynasty: 1,
    end_dynasty: 2
  )
```

When serialized it has the following binary structure:

| Field | Value | Size (in Bytes) |
| --- | --- | --- |
| Magic header | [’\x7F’,‘E’,‘T’,‘H’,‘E’,‘R’,‘E’,‘U’,‘M’] | 9 |
| Version | [1, 0] as [Major, Minor] | 2 |
| Start offset of raw data | E2 (=226) as big endian int64 | 8 |
| Blake2_256 hash | 0x390056867ac072c4cfcb5d4abc60bdc8ea8cc3941c4ecb9874254af1bd4b281d | 32 |
| Schema | {“pubkey”:“UInt256”,“withdrawal_shard”:“int16”,…,“start_dynasty”:“int64”,“end_dynasty”:“int64”} | 175 |
| Raw data | Should be equivalent to SimpleSerialize | 110 |

[Implementation in Nim](https://github.com/status-im/nim-beacon-chain/blob/master/research/sereth.nim)

Unfortunately as you can see including the schema brings lots of overhead for the types we want serialized: the schema is 175 bytes while the raw data is only 110 bytes.

I think the spec should include predefined schemas so that we don’t have to include them in messages.

Edit: Ellipsis in the schema in the table so that we see the sizes at a glance

---

**arnetheduck** (2018-08-07):

1. On flatbuffers and cap’n’proto, and similar fixed-size encodings in a network setting:

- fixed-size integers tend to take up a lot of space compared to varint, for “typical” human-generated values
- you must decide up-front how many bits you want / need
- upgrades are more difficult, in case of protocol changes
- indeed fast to mmap/decode, but I’ve seen the increased size can offset this advantage on certain data sets!

1. On schemas

- a machine-readable schema will allow the creation of tooling and analysis software, as well as provide an unambigous definition of the protocol - expect a much more rapid development cycle once there is one that’s agreed upon - there being a schema is more important that the particular schema language (homebrew or existing one)
- a home-brew schema might be appropriate to allow the efficient encoding of types typically encountered in the ethereum world: hashes, 256-bit ints etc
- a variation is to use a well-known encoding (like the binary encoding of protobuf integers) but with a smaller schema language (a subset of protobuf, or a mix/homebrew) - this has the advantage that efficient primitives for encoding and decoding base types exist, while retaining some of the benefits

---

**paulhauner** (2018-08-23):

Chris (from our team) has been working to get some application-specific data regarding serialization packages. So far he has: AttestationRecord, Block, ShardAndCommittee, CrosslinkRecord, ValidatorRecord and CrystallizedState serialized in Cap’n’Proto, Protobuf and FlatBuffers.

You can find the code in this repository: https://github.com/sigp/serialization_sandbox

So far we have a test structure and some information regarding size for a few different packages. You can see the “roadmap” in the repository readme.

You can run the code yourself, or here’s a printout of what we have so far: https://notes.ethereum.org/s/BkM5bqsIQ

