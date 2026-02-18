---
source: magicians
topic_id: 15476
title: "EIP-7495: SSZ ProgressiveContainer"
author: etan-status
date: "2023-08-17"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7495-ssz-progressivecontainer/15476
views: 4836
likes: 12
posts_count: 39
---

# EIP-7495: SSZ ProgressiveContainer

Discussion thread for [EIP-7495: SSZ ProgressiveContainer](https://eips.ethereum.org/EIPS/eip-7495)

# Background

- Alternative: SSZ Union (currently unused): consensus-specs/ssz/simple-serialize.md at 67c2f9ee9eb562f7cc02b2ff90d92c56137944e1 · ethereum/consensus-specs · GitHub
- Alternative: SSZ Optional (currently unused): EIP-6475: SSZ Optional
- Discord: #ssz (Eth R&D)
- Usage: https://pureth.guide

# Potential use

- EIP-6404: EIP-6404: SSZ transactions
- EIP-6466: EIP-6466: SSZ receipts

#### Outstanding Issues

- 2024-10-29: Tagged Profile support for serialization?, https://discord.com/channels/595666850260713488/745077610685661265/1283443027750420510

2025-06-26: Replace optionals with union for serialization

#### Update Log

- 2025-08-28: Split CompatibleUnion from EIP-7495
- 2025-08-28: Mix-in selector for CompatibleUnion
- 2025-08-22: Reinstate 256 field limit for ProgressiveContainer
- 2025-08-08: Drop 256 entry limit in ProgressiveContainer
- 2025-06-26: Use progressive tree shape / Drop optionals
- 2025-04-15: Define interaction with EIP-7916 ProgressiveList

## Replies

**etan-status** (2023-08-17):

Showcase for how this would look for transactions: https://eth-light.xyz (desktop only, not mobile-friendly)

---

**tjayrush** (2023-08-21):

This is interesting. Thanks.

The section called “Why not a `Container` full of `Optional[E]`” ends with this sentence: “Therefore, the number of fields is constant and the Merkle tree shape is stable.” I apologize if I’m misunderstanding something, but would it be correct to add, “…the Merkle tree shape is stable, if perhaps larger.”

I understand that the shape of the tree won’t change if the number of optional fields is constant, but isn’t it true that in (half?) of the cases, the tree will be twice as big?

I’m mostly just curious, but it might help to make that explicit.

---

**etan-status** (2023-08-22):

Thanks for the comment, I have updated the PR with a more detailed description of the overhead.

While the tree will indeed be twice as big, the number of hashes required to compute the root hash of the tree only scales logarithmically. SSZ implementations typically precompute root hashes of pure zero trees, so the empty half of the tree doesn’t need to be hashed in practice. For example, if you have a tree with 32 leaves, but the last 16 leaves are empty, `hash_tree_root(tree) == hash(hash_tree_root(tree.left) || hash_tree_root(tree.right)) == hash(hash_tree_root(tree.left) || zeroHashConstants[depth = 4])`

---

**etan-status** (2023-08-22):

As SSZ specs live in the ethereum/consensus-specs repo, the `PartialContainer` spec will be introduced there once we agree on an overall approach for representing transactions / receipts (EIP-6404 / EIP-6466).

Until then, I’d like to have everything in the EIPs repo, including the PartialContainer. This is in line with prior art, for example, EIP-4895, where consensus changes are being discussed in the EIP before making it into consensus-specs.

Note that I’m still working on updating EIP-6404 / EIP-6466 to use the PartialContainer. Once we have agreement, I’ll extend `remerkleable` with support for `PartialContainer` and then create a matching consensus-specs PR that also provides tests. Likewise, will open a consensus-specs PR to change the consensus `Transaction` structure to match the proposed execution `Transaction` structure.

---

**etan-status** (2023-08-28):

https://github.com/ethereum/EIPs/pull/7495#discussion_r1307423654

> Yes, a new fork could relax validity constraints, while a subsequent fork could require the field to be present again. Whether that makes sense is up to the application, but the serialization format proposed here will be stable across both directions (from optional to required and vice versa), essentially providing maximum flexibility when it comes to future design space.
>
>
> In fact, an implementation could simply treat all fields as optional always, if they prefer to enforce constraints in the application layer instead of the serialization library. Another implementation may go the other direction and also push down an invariant callback to ensure that only valid combinations are accepted; e.g., a receipt can contain either an intermediate state root, or a status code, but not both at the same time. Yet another implementation may try to use union types to represent various valid combinations; point being is, none of these implementation details leak into the serialization representation.

---

**etan-status** (2023-09-01):

Renamed from `PartialContainer` to `StableContainer` to highlight the stable serialization and merkleization across spec versions.

Also, simplified the specification by getting rid of the outer `T` and instead directly referring to the container in those situations. The Python code also was updated to no longer require the extra `@dataclass` layer. Serialization, merkleization, semantics and so on did not change at all.

---

**Nashatyrev** (2023-09-12):

`StableContainer` look like a good idea to address the issues outlined in the `Motivation` section.

However it seems to me that introducing of `Optional` type is a matter of a separate concern.

Doesn’t the `StableContainer` solely solve the mentioned issues?

I.e. adding a field in a new container version would be just straightforward.

Removing the field (or rather deprecating it) would be just changing its type to something like `Nothing`.

Moreover with introducing the `Nothing` type e.g.

```py
class Example(StableContainer[4]):
    a: uint64
    b: uint64
```

could be represented via a regular container:

```auto
class Example(Container):
    a: uint64
    b: uint64
    f2: Nothing
    f3: Nothing
```

and then removing the field `a`  and adding a new field `c` would look like

```auto
class Example(Container):
    f0: Nothing
    b: uint64
    c: uint16
    f3: Nothing
```

Would that approach suit the needs?

---

**etan-status** (2023-09-12):

Yeah, your example is indeed how those messages would get serialized.

Passing `N` to the `StableContainer[N]` essentially fills it up with `Nothing` up through `N` total fields. Setting `N` in the type metadata reduces verbosity.

Using `Optional[T]` instead of `Nothing` ensures that messages of old style (for example, in your case, messages containing `a`) can still be parsed. This also allows for use cases that have conditional fields, for example, as highlighted in [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493), where a `check_transaction_supported` function defines valid combinations.

---

**Nashatyrev** (2023-09-13):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> as highlighted in EIP-6493

Yes, this is exactly the use case I’m a bit concerned about. It’s kind of leaking of SSZ static typization

Effectively instead of declaring dedicated classes for every transaction type there is a single container with a number of `Optional` fields which should be cross validated.

Does it make sense to declare separate SSZ type for every Tx type, like `TransactionPayloadLegacy`, `TransactionPayloadEip2930`, etc ?

I see that it would be more verbose and probably would require more boilerplate code to handle. But it would be more type safe and less error-prone imo.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> messages of old style (for example, in your case, messages containing a) can still be parsed

That looks to me as a separate concern. The most obvious way seems to wrap those types with a `Union` (or `StableUnion` if one needs stable merkleization and tree paths)

---

**etan-status** (2023-09-13):

> Does it make sense to declare separate SSZ type for every Tx type

Overall, even if you have separate SSZ types, you’d still need additional validation to check invariants. For example, to check that the `from` address is correct. Or, to check that the blob_versioned_hashes match the blob in the wrapper. Or that the `to` field is present for the blob transaction (it’s optional without using blob). Or that the `max_fee_per_gas` is >= `max_priority_fee_per_gas`. Note you may also need matching `TransactionSignatureXyz`, and somehow check that it is compatible with the payload union.

Checking valid field combinations in EIP-6493 is ~20 lines, mostly to ensure that txns retain the limitations from RLP. It could be exhaustively tested. The full list of supported combos is:

- TransactionPayloadReplayable → original format, not locked to chain ID (no SSZ equivalent)
- TransactionPayloadLegacyRlp → optional to, no access list, no prio fee, no blob
- TransactionPayloadEip2930Rlp → optional to, yes access list, no prio fee, no blob
- TransactionPayloadEip1559Rlp → optional to, yes access list, yes prio fee, no blob
- TransactionPayloadEip4844Rlp → required to, yes access list, yes prio fee, yes blob
- TransactionPayloadLegacySsz → optional to, no access list, no prio fee, no blob
- TransactionPayloadEip2930Ssz → optional to, yes access list, no prio fee, no blob
- TransactionPayloadEip1559Ssz → optional to, yes access list, yes prio fee, no blob
- TransactionPayloadEip4844Ssz → required to, yes access list, yes prio fee, yes blob

There’s the problem of combinatorial explosion. For example, if you want a transaction that has a blob but no priority fee nor access list, and then another one wants no blob but wants a priority fee and no access list, and so on; that’s 8 additional different “tx types” for features that don’t have anything to do with each other. With future features such as multidimensional fees, CREATE2 transaction, different sig_hash mechanisms, and so on, one may want to move towards allowing the signer to pick the combo they want instead of being forced to select a type that supports a superset of what’s needed and then having to trick around with empty lists and default values for all the features they don’t want, like currently done in RLP.

Furthermore, you’d need some mechanism to transfer type information. For example, using an enum prefix similar to `Union`. However, that leads to a requirement for the verifier to know about all the enum cases and their meaning. Because new types may be introduced in the future, verifiers can’t become immutable. That’s the case even if they solely care about certain fields of the container; for example, only `from`, `to`, and `value`, and ignore all other fields. On the other hand, with `StableContainer`, that could be achieved with a followup proposal like a `SparseView` that includes just the bitvectors, the requested 3 fields, plus a merkle proof. The merkle proof shape is statically determinable solely by the bitvectors and the requested fields regardless of tx type, which is not necessarily given by a `Union` approach.

About `StableUnion`, would be interested to understand what you mean there and how the differences to the `StableContainer` are.

I’d also like to better understand `more type safe and less error-prone` arguments. In practice, implementations likely go for a single implementation that handles all transactions. Then, for each feature, check if it is used and, if it is, process it. The difference would be that with the `TransactionPayloadXyz` jungle you’d need a Generics based implementation that generates another copy of the code for each individual type (feature combination), while with the `StableContainer` approach you’d have a single function with runtime checks for all the features. Code size is smaller with the `StableContainer`, while the Generics based implementation can exclude certain invalid field combinations (the 20-line check in EIP-6493) in the serialization library rather than its usage. Code size may also have implications on ZK logic based verifiers.

---

**Nashatyrev** (2023-09-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> About StableUnion, would be interested to understand what you mean there and how the differences to the StableContainer are.

Sorry - my mistake here. The present `Union` implementation is inherently ‘stable’ actually. For some reason I thought it has the structure similar to `Container`

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> Overall, even if you have separate SSZ types, you’d still need additional validation to check invariants.

Of course there is always a lot of semantics which couldn’t be expressed with types. But whenever it’s feasible it always better to express semantics/constraints via static types in the presence of such system (SSZ in our case).

Of course I don’t treat it as an immutable rule. If you are saying there is a ‘combinatorial explosion’ then of course it probably doesn’t make sense to ‘die hard’ sticking to strong typing. However some things could be expressed in a more canonical way on my mind:

Obvious example:

```python
    # EIP-4844
    max_fee_per_blob_gas: Optional[uint256]
    blob_versioned_hashes: Optional[List[VersionedHash, MAX_BLOB_COMMITMENTS_PER_BLOCK]]
```

Both fields are either present or absent. Ideally it would look like:

```python
    # EIP-4844
    eip4844Data: Optional[Eip4844Data]

class Eip4844Data(StableContainer[N]):
    max_fee_per_blob_gas: uint256
    blob_versioned_hashes: List[VersionedHash, MAX_BLOB_COMMITMENTS_PER_BLOCK]
```

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> I’d also like to better understand more type safe and less error-prone arguments. In practice, implementations likely go for a single implementation that handles all transactions.

I’m not sure about transaction representation. Teku has dedicated Java types for every hardfork version of every structure. That seriously helps to avoid shooting your foot when adding/changing processing logic across the whole codebase.

Worth to mention there is a type hierarchy as well (which is not applicable in spec) which makes things a lot simpler.

---

**sopia19910** (2023-09-30):

Does Optional[T] indicate whether the chunk has data or not?

---

**etan-status** (2023-09-30):

> The present Union implementation is inherently ‘stable’ actually.

No, the existing `Union` is not stable. As you mention Teku, let’s do a consensus example. If you want to build an application that tracks whether a particular validator is slashed in a trust-minimized way using merkle proof of the response, you will have to keep updating your application several times a year to teach it about all the various hard forks, including all those that add completely unrelated features. This is, because the Merkleization of `BeaconState` is not stable across consensus-fork versions – whenever the total number of fields reaches a new power of two, generalized indices change, and therefore, the Merkle proof changes. Same when a field is removed from one version to the next. With `StableContainer`, the proof remains forward-compatible even if fields get added or deprecated over time.

> Both fields are either present or absent.

Yes, in the business logic. But that doesn’t need to leak into the serialization or the merkleization. Adding more wrapping than strictly required in SSZ leads to overhead when using variable-length fields, with additional offset tables getting serialized.

> Teku has dedicated Java types for every hardfork version of every structure.

Still possible. One can build dedicated types for all the possible subsets on top of `StableContainer`.

For example, back to the transactions, one could go with two types:

```auto
class BasicTransactionPayload(StableSubset(TransactionPayload)):
    nonce: uint64
    max_fee_per_gas: uint256
    gas: uint64
    to: Optional[ExecutionAddress]
    value: uint256
    input_: ByteList[MAX_CALLDATA_SIZE]
    access_list: Optional[List[AccessTuple, MAX_ACCESS_LIST_SIZE]]
    max_priority_fee_per_gas: Optional[uint256]

class BlobTransactionPayload(StableSubset(TransactionPayload)):
    nonce: uint64
    max_fee_per_gas: uint256
    gas: uint64
    to: ExecutionAddress  # Required in blob transaction
    value: uint256
    input_: ByteList[MAX_CALLDATA_SIZE]
    access_list: Optional[List[AccessTuple, MAX_ACCESS_LIST_SIZE]]
    max_priority_fee_per_gas: Optional[uint256]
    max_fee_per_blob_gas: uint256
    blob_versioned_hashes: List[VersionedHash, MAX_BLOB_COMMITMENTS_PER_BLOCK]
```

Both would serialize and merkleize as the `TransactionPayload` `StableContainer`. But inside business logic you can map them to concrete types for the type safety, reducing runtime checks and so on. Note that the memory layout could also be shared, with both `BasicTransactionPayload` and `BlobTransactionPayload` being a subset of `TransactionPayload`. One could implement that with zero copying by having an inner private `payload` and then define accessors into it. That also helps in consensus, because fork transitions are no longer expensive: simply set all the deprecated fields to `None`, then cast to the new fork and initialize the new fields.

I think it would be useful to have something like `StableSubset` specced out and in Python as well — What EIP-7495 describes is solely a forward-compatible serialization and merkleization scheme, it shouldn’t restrict how one prefers to write code.

Note that ProtoBufs follows a similar approach in the encoding of `OneOf`. The usage appears like a union, but serialization is same as a series of optional, with the parser enforcing that only one of the options is set. This means that a client that is only interested in certain aspects can still parse messages from newer servers, without having to continuously update (forward-compatibility). It also means that a server can still parse messages from old clients, without having to convert them (backward-compatibility).

---

**etan-status** (2023-09-30):

A `BitVector[N]` is pre-pended to the data that indicates for each field whether it is present or not. If there is a `1`, the corresponding field has data. If there is a `0`, the corresponding field is `None`.

The `hash_tree_root` of the `BitVector[N]` is also mixed into the root of the object, providing the same information for systems relying on Merkle proofs.

---

**sopia19910** (2023-10-01):

Is it correct that SSZ StableContainer refers to a Merkle tree associated with the reserve pool in the Ethereum 2.0 chain?

---

**etan-status** (2023-10-29):

I have extended [EIP-7495](https://eips.ethereum.org/EIPS/eip-7495) with a section describing an additional type safety layer built on top of `StableContainer`: [PR](https://github.com/ethereum/EIPs/pull/7938/files)

```python
# Serialization and merkleization format
class Shape(StableContainer[4]):
    side: Optional[uint16]
    color: uint8
    radius: Optional[uint16]

# Valid variants
class Square(Variant[Shape]):
    side: uint16
    color: uint8

class Circle(Variant[Shape]):
    radius: uint16
    color: uint8

class AnyShape(OneOf[Shape]):
    @classmethod
    def select_variant(cls, value: Shape, circle_allowed = True) -> Type[Shape]:
        if value.radius is not None:
            assert circle_allowed
            return Circle
        if value.side is not None:
            return Square
        assert False
```

In code, could pass around `Square` / `Circle` for type-safety. While both of them would serialize / merkleize as `Shape`. [Example usage](https://github.com/ethereum/EIPs/blob/bd953bf78c09670ca4622cde90b91fb0e08836f3/assets/eip-7495/tests.py)

---

Why should we care about stable serialization / merkleization?

- Someone may create a client today that is solely interested in the color of the shapes. They use a hypothetical API that provides them with just the color + Merkle proof that it is actually the shape’s color.
- This client should not break, just because a future software upgrade adds rectangles with a width/height instead of side.

In context of Ethereum: A decentralized staking pool should not have to continuously issue software updates just because the location where information about slashing status of a validator and their balance is stored may change between forks. It should be possible to build forward-compatible clients that only require an update if actually used functionality changes. Likewise, a smart contract validating that someone paid their bill using a SSZ transaction / receipt merkle proof shouldn’t have to upgrade their contract just because a future transaction type adds an access list or a priority fee field – both those features are irrelevant for the smart contract’s purpose.

---

**etan-status** (2023-10-29):

Example usage in EIP-6493:

- Update EIP-6493: Use `Variant[S]` for type safety by etan-status · Pull Request #7939 · ethereum/EIPs · GitHub

---

**etan-status** (2024-04-15):

Added compact serialization for `Variant`, so that this is also usable for consensus:

- Update EIP-7495: Compact serialization for `Variant[S]` by etan-status · Pull Request #8436 · ethereum/EIPs · GitHub

---

**etan-status** (2024-04-16):

Added EIP for transitioning consensus SSZ data structures to `StableContainer` as well:

- EIP-7688: Forward compatible consensus data structures

---

**etan-status** (2024-04-17):

![](https://ethereum-magicians.org/uploads/default/original/2X/1/164f4256a0019844abd16f69f3fd13ed310661d9.png)

      [HackMD](https://notes.ethereum.org/@vbuterin/purge_2024_03_31#Moving-to-SSZ)



    ![](https://ethereum-magicians.org/uploads/default/original/2X/8/89ac618501d77ed85e1ea0663718f590291e7737.png)

###



# Next steps in the Purge  One of the less well-known EIPs in the recent Dencun hard fork is [EIP-67


*(18 more replies not shown)*
