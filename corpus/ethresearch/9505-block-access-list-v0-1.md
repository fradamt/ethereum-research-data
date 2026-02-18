---
source: ethresearch
topic_id: 9505
title: Block access list - v0.1
author: g11in
date: "2021-05-15"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/block-access-list-v0-1/9505
views: 3709
likes: 3
posts_count: 7
---

# Block access list - v0.1

ps: this is an iteration over [block access list](https://ethresear.ch/t/block-access-list/9357) with inputs and refinements from [@pipermerriam](/u/pipermerriam)

### Background

*EIP [2929](https://eips.ethereum.org/EIPS/eip-2929)/[2930](https://eips.ethereum.org/EIPS/eip-2930)* centers around  normalizing (low) gas costs of data/storage *accesses* made by a transaction  as well as providing  for (and encouraging) a new transaction type format:

```auto
0x01 || rlp([chainId, nonce, gasPrice, gasLimit, to, value, data, access_list, yParity, senderR, senderS])
```

that makes upfront `access_list` *declarations*, where

`access_list` is some `[[{20 bytes}, [{32 bytes}...]]...]`  **map** of `AccessedAddress=> AccessedStorageKeys`.

The *first accesses* of these upfront *declarations* are charged at discounted price (roughly ~`10%`) and *first accesses* outside this list are charged higher price. Reason is, upfront access declaration provides for a way to *preload/optimize/batch* loading  these locations while executing the transaction.

This inadvertently leads to generation of *transaction* `access_list` that has all *first accesses* (declared or not) made by a transaction. A `JSON-RPC` api endpoint for creating and fetching this list is being standardized.

### Motivation

Motivation is to collate these transaction `access_list`s for all the transactions in a block’s **`access_list`** document, that can serve as sort of *access index*  of the block with  following benefits:

1. Block execution/validation optimizations/parallelization by enabling construction of a partial order for access and hence execution (hint: chains in this poset can be parallelized).
2. Enabling partial inspection and fetching/serving of a block data/state by light sync or fast sync protocols concerned with a subset of addresses.
3. Possible future extension of this list to serve as index for bundling, serving and fetching witness data for stateless protocols.

To serve the above purpose, and prevent any *grieving* attacks, an `AccessListRoot` which could be a [urn](https://en.wikipedia.org/wiki/Uniform_Resource_Name) encoding  `Hash/Commitment` of a **canonical**  `access_list` as well as the construction type (`sha256/kate/merkel/verkel`) will need to be included in the **block header**.

Forming the tree structure (`merkel/verkel`) rather than a simple `Hash/Commitment` of the entire *canonical* `access_list` will be a bit more expensive, but it will enable partial downloading, inspection and validation of the `access_list` and is recommended.

### Construction

Currently a transaction’s   `access_list`:

```auto
Set [ AccessedAddress, List [ AccessedStorageKeys ]]
```

Proposal a block’s  `access_list`:

```auto
Set [ AccessedAddress,
      List [AccessedStorageKeys] ,
      Set  [ AccessedInBlockTransactionNumber, List [ AccessedStorageKeys ]]  ]
```

But as mentioned, we need to define a *canonical* access list construction for purposes of building `AccessListRoot`

#### Canonical Block Access List

An `access_list` is comprised of many `access_list_entry` elements:

```auto
access_list   :=  [access_list_entry, ...]
```

An access_list_entry is a 3-tuple of:

- address
- sorted list of storage keys of the address accessed across the entire block
- sorted list of 2-tuples of:

transaction index in which the address or any of its storage keys were accessed
- sorted list of storage keys which were accessed

```auto
access_list                 := [access_list_entry, ...]
access_list_entry           := [address, storage_keys, accesses_by_txn_index]
address                     := bytes20
accesses_by_txn_index       := [txn_index_and_keys, ...]
txn_index_and_keys          := [txn_index, storage_keys]
txn_index                   := uint64  # or uint256 or whatever
storage_keys                := [storage_key, ...]
storage_key                 := bytes32
```

Additional sorting rules for the above are that:

- access_list is sorted by the address
- storage_keys is sorted
- accesses_by_txn_index is sorted by txn_index

Additional validation rules for the above are that:

- Each unique address may only appear at most once in access_list
- Each storage_key may only appear at most once in storage_keys
- Each txn_index may only appear at most once in txn_index_and_keys

###### Side Note: Other sorting orders like ordering the elements by accessed by order were considered but didn’t seem to provide any significant benefit over the simpler lexicographic ordering.

#### AccessListRoot

For a very simple start we can do a `SHA256` of the *canonical* `access_list` and include it in the block header with the following the urn scheme:

```auto
AccessListRoot := "urn:sha256:${ SHA256( access_list ) }"
```

This `AccessListRoot` could evolve to `urn:merkel:...` or to `urn:verkel:...` or to any other scheme as per requirement.

##### Additional Block Validation

Full nodes while accepting, executing the new block have an additional validation check that the block’s **urn** encoded `AccessListRoot` matches the one calculated from the one generated by executing the block.

##### A JSON RPC Endpoint

Recommended implementation of fetching the block access list of a given block something of the sorts of `eth_BlockAccessList(BlockNumberOrBlockHashOrAccessListURN, ListOfAddressesOrOffsetOrNull)` which can return paginated `access_list`, paginated at the top address level.

### Future optional extensions

We can extend the notion of a block’s `access_list` to:

```auto
access_list := Set[ Address,
                    List [ AddressWitnesses ],
                    Set  [ AccessedStorageKey, List [ StorageKeyWitnesses] ],
                    Set  [ AccessedInBlockTransactionNumber, List [ AccessedStorageKeys ] ]]
```

This will allow an incremental path to partial or full stateless chain protocols, where it would be easy to bundle/request witnesses using this `access_list`.

## Replies

**pipermerriam** (2021-05-20):

![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=9) this seems reasonably complete and worth putting in from of the core devs for potential inclusion in a subsequent hard fork.

---

**axic** (2021-05-23):

From [the EIP](https://eips.ethereum.org/EIPS/eip-3584):

> An AccessListRoot is a URN encoding Hash/Commitment of the canonical access_list as well as the construction type (sha256), i.e.
>
>
>
> ```auto
> AccessListRoot := "urn:sha256:${ SHA256( access_list ) }"
> ```

Can you explain what URN encoding means? [RFC 8141](https://datatracker.ietf.org/doc/html/rfc8141) seems to talk about URNs being these namespaced strings, where the hash part is what the RFC refers to as NSS (namespace specific string).

Does this only mean here that the sha256 hash will be encoded as a hex string? If so, will it be encoded as the full 32 bytes? With or without leading zeroes? With or without a `0x` prefix?

My second question is about the encoding of `access_list`. I see the sorting order and the way the structure is built is explained, but I am unsure about the serialisation of the structure, e.g. how does it becomes a bytestream suitable as the input to sha256. Will it be encoded as a JSON text? As some binary encoding (such as CBOR, RLP, SSZ)?

---

**g11in** (2021-05-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/axic/48/1578_2.png) axic:

> Can you explain what URN encoding means? RFC 8141 seems to talk about URNs being these namespaced strings, where the hash part is what the RFC refers to as NSS (namespace specific string).

I should specify it as URN *like* encoding, as we don’t mandate to register NID part (for e.g. `sha256` here) with the IANA. and yes `${...}` is the evaluated sha256 string, we have’t yet fixed the format for that but it could very easily be the hex string (with leading `0x`)

> e.g. how does it becomes a bytestream suitable as the input to sha256.

You are again correct, that serialization has not been defined yet, again because we haven’t formed any strong opinion on it yet. (also serialization would be construction dependent for e.g. for Kate based commitment, it would need to be defined as  polynomial evaluated points (index,value) )

again the NID part of the URN has not been fixed, and it could encode both the scheme to hash/commit, as well as the serialization which could also be done by having a `q component` to the URN.

So yes, there is some **handwaving** that has been done here and will need to be addressed, but the idea is to table the concept and have a consensus around the `access_list` formation at the block level and then go from there fixing all other details. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**g11in** (2021-05-27):

[@axic](/u/axic) updated the EIP, let know if it looks good now ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

---

**pipermerriam** (2021-05-28):

One thing that we need to validate/understand is the interplay between access lists and witnesses.  In theory, we want to be able to have a “witness” which can be validated against the `access_list_root`.  It’s not clear to me how this would work with verkle-trie proofs, but I believe that with merkle proofs,  we would end up needing some amount of extra metadata or even the full access list (not just the root), to be able to determine exactly which parts of the merkle proof are actually part of the access list (and which ones are just extraneous proof data).

We will want to be sure that when we progress into fully supported stateless block execution at the protocol level, that our construction is sufficient to have witnesses be verifiable against the header data.  We probably should start by doing this against the current merkle proofs since they are well understood, after which we can extend to validating it against verkle.

---

**g11in** (2021-05-28):

best hashing construction would be `kate`, no need to tree it up for `verkle` or `merkle`, and with just `O(1)` witnesses of an `address` can be verified.

Will depend on when the go live will be planned as for `kate`/`verkle` to work, there is no [trusted setup yet](https://hackmd.io/yqfI6OPlRZizv9yPaD-8IQ#What-is-Kate) , even if we assume the client teams will familiarize themselves and libraries will be available. but it should be a natural up-gradation target when that happens.

