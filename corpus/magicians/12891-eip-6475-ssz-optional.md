---
source: magicians
topic_id: 12891
title: "EIP-6475: SSZ Optional"
author: etan-status
date: "2023-02-09"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6475-ssz-optional/12891
views: 2488
likes: 4
posts_count: 18
---

# EIP-6475: SSZ Optional

Discussion thread for [EIP-6475: SSZ Optional](https://eips.ethereum.org/EIPS/eip-6475)

# Background

Zahary’s notes: [Consider possible improvements to the SSZ spec before phase0 is launched · Issue #1916 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/issues/1916)

# Potential use

EIP-4844 and EIP-6404, to represent a transaction’s `to` value. It can be `None` to denote deployment of a contract, or otherwise the transaction destination address.

## Replies

**etan-status** (2023-02-09):

Added tests and reference implementation based on `protolambda/remerkleable` (Python) to EIP.

---

**etan-status** (2023-02-11):

Added Nim implementation: [implement SSZ Optionals (EIP-6475) by etan-status · Pull Request #41 · status-im/nim-ssz-serialization · GitHub](https://github.com/status-im/nim-ssz-serialization/pull/41)

One thing to note is that for the purpose of merkleization, this is equivalent to `List[T, 1]`, and to `Union[None, T]`. It is just the serialization that is more compact than those workarounds, and the obvious ability to write more concise code, instead of switching on list lengths or union selectors.

---

**dankrad** (2023-02-13):

> [on comparison to union type] The serialization is less compact, due to the extra selector byte.

Honestly this seems a very week argument for introducing a new type that is already supported. I feel like this is a bad idea because Unions were introduced for exactly this purpose.

Also, this kind of abuses the length bytes and only works in the specific case where the optional type is of fixed length.

---

**etan-status** (2023-02-13):

SSZ Union are not “already supported” across the board; so far, they are not used in any final Ethereum specification. Certain libraries such as `nim-ssz-serialization` currently only fully implement the limited support needed for handling the `Optional[T]` workaround. There are also [no official tests](https://github.com/ethereum/consensus-specs/tree/dev/tests/generators/ssz_generic) for SSZ unions.

If “unions were introduced for exactly this purpose”, they would most-likely optimally encode for this purpose. However, they do not, and they are clearly a more powerful construct than just `Optional[T]`. The same design space as `Union[None, T]` is actually already offered by `List[T, 1]`, which *also* encodes more compactly for fixed-length types, and actually *is* “already supported” and well tested.

Regarding “abuses the length byte”, I’m not sure what you are referring to, as SSZ does not explicitly encode a “length byte” anywhere. For example, in a `List[T, N]` of fixed-length type, `N` is implicitly derived from `len(List) / sizeof(List[0])`. For variable-length types, `N` is derived from `(&(*bytes[0]) - &bytes[0]) / sizeof(uint32)` if `len(List) > 0` or assumed to be `0` if `len(List) == 0`. The proposed `Optional[T]` SSZ type follows these same conventions.

The proposed `Optional[T]` works not just for fixed-length types, but also for most variable-length types such as `Bitlist[N]`, `Union[type_0, type_1, ...]`, `Container` with variable-length members, and `Vector` with variable-length members. As proposed, the only types that cannot be nested on the very next layer are `List[T, N]` and `Optional[T]`, which both already have a natural way to denote absence (`len = 0` and `None`). The concept of [Illegal types](https://github.com/ethereum/consensus-specs/blob/67c2f9ee9eb562f7cc02b2ff90d92c56137944e1/ssz/simple-serialize.md#illegal-types) already exists in SSZ. If needed, the format can be accordingly extended in the future.

---

**zah** (2023-02-13):

Indeed, since the SSZ unions haven’t been used in any production spec yet, the `Optional` type described here can also be framed as a special case optimization for the the `Union` type. This was my original proposal (please see point 2 in the linked issue):



      [github.com/ethereum/consensus-specs](https://github.com/ethereum/consensus-specs/issues/1916)












####



        opened 10:09AM - 18 Jun 20 UTC



          closed 07:17PM - 01 Apr 25 UTC



        [![](https://ethereum-magicians.org/uploads/default/original/2X/b/bccd5097720cbaae8451d6a2d1c36ebf79e06a69.jpeg)
          zah](https://github.com/zah)





          enhancement


          ssz


          phase0







One of the design goals of SSZ is that it should make it easier for other blockc[…]()hains to work with merkle proofs referencing Eth2 consensus objects. Once phase0 is launched, we can expect various official SSZ records to start appearing in third party databases. This would significantly increase the difficulty of coordinating upgrades to the SSZ spec (due to the limited forward compatibility provisions in SSZ, a lot of applications may get broken in the process). Due to this, I think we should consider introducing some final refinements and optimisations to the SSZ spec before phase0 is launched:

### 1) Reduce the size of every variable-size container by 4 bytes.

Every variable-size container (i.e. record with fields) consists of a fixed-size section storing the offsets of the variable-size fields.

The offset of the first such field currently has only one valid value - it must be equal to the length of the fixed-size section. The [implementations are expected to check for this](https://github.com/status-im/nim-beacon-chain/pull/1088), because otherwise there might be some unused bytes in the SSZ representation which is considered an invalid encoding.

The motivation for not allowing unused bytes is that this would break the property `deserialize(serialize(x)) == x` which is quite useful for fuzzing. For completeness, I would mention that if unused bytes were allowed, a very limited form of forward-compatibility will be present - it would be possible to add a new field at the end of a record without breaking older readers. Since SSZ upgrades require coordination and all long-term storage applications should also feature an out-of-band version tag, this limited form of forward-compatibility was considered unnecessary.

In other words, since the first offset has only one valid value that is completely derived from the type schema, the offset carries no information and can be omitted from the representation. The result will be that every variable-size container will be 4 bytes shorter. Admittedly, 4 bytes are not much, but if we consider the long expected life of the SSZ spec and great multitude of places where SSZ records might appear, some quick back-of-the-envelope calculation estimated the total cost savings in bandwidth and storage to amount to roughly 1 gazillion bytes :P

### 2) Null-value optimisation (a.k.a better support for pointer types and  `Option[T]`)

The SSZ spec defines union types that can discriminate between `null` and a possible value. Let's call such types `Nullable`. Since the `Nullable` types have variable size, their length in bytes can be zero (just like how we encode zero-length lists with two consecutive offsets with the same value). I propose the addition of the following two special rules:

* The `null` value of a `Nullable` union is encoded as zero bytes.
* A union with just one non-null branch is encoded without a `serialized_type_index`.

Please note that in most programming languages, the unions described above can be mapped to frequently used types such as `Option[T]` or a pointer type. During the development of the `blocks_by_range` protocol, an earlier version was suggesting that missing blocks should be indicated in the response as a `default(T)` encoding of the `BeaconBlock` type. This was semantically equivalent to using an `Option[T]` type, but it would have been considerably more inefficient. The design of the protocol was refined in later versions to not require this form of response, but I think that if one of the very first protocols was that close to using and benefiting from the `Option[T]` type, we can expect more protocols to appear in the future that will benefit as well.

### 3) Resolve a contradiction in the SSZ List limit type

The SSZ spec doesn't specify what is the type of the list size limit. This leads to something that can be described as a slight contradiction in the current specs:

The size limit of the validator registry is set to 1099511627776 (2^40). On the other hand, the maximum size in practice is limited in the encoding to the difference of two offset values. Since the offset values are encoded as `uint32`, the maximum size in practice cannot be larger than 2^32. Perhaps the intention for the size limit is that it should only affect the merkle hash computation, but the spec would do nice to clarify this.

---

**dankrad** (2023-02-14):

To put this in context, a blob transaction uses 131,072 bytes for the blob alone (assuming a single blob), and this change saves one byte (less than 0.001%).

---

**etan-status** (2023-02-14):

Point being, serialization and merkleization of SSZ Unions are still [being discussed](https://notes.ethereum.org/@vbuterin/transaction_ssz_refactoring) and not properly tested, as they are a new SSZ type not currently used in any finalized spec.

> Note: the precise definition of Union is still a topic of discussion. Union is currently not yet used in consensus, and so there remains freedom to decide exactly how Union types are to be hash-tree-rooted and serialized. There are different approaches being proposed that attempt to maximize efficiency and simplicity.

For EIP-4844, using something simpler like the `Optional[Address]` proposed here, or even just plain `List[Address, 1]` (actually the exact same serialization and merkleization for fixed-length types), reduces the complexity of requiring an entire union framework to just represent an optional address. Yes, it also shaves off that single byte, in either `List` or `Optional` case, as a side effect.

---

**etan-status** (2023-02-14):

This was discussed in today’s [EIP-4844 breakout call](https://github.com/ethereum/pm/issues/722).

Decision on this was postponed until we know whether SSZ Unions will actually be used in their full scope. If they are, their design regarding serialization and merkleization will have to be finalized, and exhaustive tests for them added. On the other hand, if we decide that SSZ Unions are not needed at this time, EIP-4844 could move to List[T, 1] or to Optional[T].

---

**ralexstokes** (2023-02-14):

as a process note, this type of thing would make a lot more sense as a PR to the consensus-specs, rather than an EIP

if we move ahead with this change, we will want to recreate as a spec PR anyway so the specs for SSZ all live in one place

---

**etan-status** (2023-02-14):

Agree that a consensus-specs PR is also warranted. Furthermore, if tomorrow’s [SSZ breakout call](https://github.com/ethereum/pm/issues/721) reveals that we actually end up with a situation where full Union support is required, and not just the `Optional` subset, updates to the Union spec should be discussed as well to gain the same optimizations from [@zah](/u/zah).

Namely that the union’s `None` case serializes without the selector (no downside), and potentially also that the `[None, T]` case serializes without the selector (no `List` / nullable `Union` at the very next layer). `Optional` and `Union[None, T]` ideally have the same properties in a world containing union, so `Optional` becomes just syntactic sugar to make it explicit that there is no intention to expand it to `Union[None, T, U]` later on, and to allow language features such as `.isSome` checks, similarly to how we have sugar for `ByteVector` etc.

In the other case, if we determine that full Union support is not needed at this time (for SSZ transactions discussion), I would advocate to only depend on the actually used `Optional` subset.

BTW, if there is any default `Address` constant that could be used to represent the `None` case, I would prefer that one over either `Optional` or `Union`. But I suspect that `Optional` support is actually really becoming necessary.

---

**etan-status** (2023-04-20):

consensus-specs PR: [EIP-6475: Add SSZ `Optional[T]` type by etan-status · Pull Request #3336 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3336)

---

**jflo** (2023-04-25):

Of the 3 possible implementations being proposed, I think the `List<T, 1>` is the most viable at the moment, and it would be reasonable to put syntactic sugar around that to call it an optional. Implementors would be free to either exploit the Optional wrapping it, or continue to use it as a List that requires only 1 iteration.

I think the EIP is ambiguous on how `Optional<T>` intends to serialize an empty Optional. Serialization of `None` is undefined in the SSZ spec, however in my spelunking of discussions around SSZ, it seems the intention is that `None` should be written as an empty list- two consecutive offsets to the same place. Moreover that seems synonymous with treating an empty Optional as a variable length encoding of `b""` , as suggested by the suggested python serialization.  If I am correct, then there really is no difference other than naming this `Optional`, and either way we have chosen to implement this as `List<T,1>`

Regarding the Union implementation from a tactical perspective, I find the “unions aren’t ready yet” argument much more compelling than the “unions add size overhead” argument. Lists are here and ready, and would be trivial to implement an Optional based on list length.

Alternately, from a design perspective, there is also a bit more semantic clarity in using the Union. Many programming languages (Swift, Kotlin, Rust…) have implemented Optionals in this way, and so developers should find that a bit more intuitive. Using Lists would be more hacky from a design perspective, and that design wart will live on forever.

---

**etan-status** (2023-04-25):

Yes, for fixed-length inner types, the proposed serialization matches the one of `List<T,1>`.

However, for variable-length `T`, `List<T,1>` emits an offset-entry, which is not necessary in the optional case as the length can be implied from the full list length - if it is serialized as `b""`, it is `None`, otherwise it is `Some(T)`.

For merkleization, `Optional[T]`, `List<T,1>` and `Union<T,1>` are all the same, with same `hash_tree_root`. Only serialization is affected.

Conceptually, an `Optional` type (however it is serialized / merkleized) is a useful concept (see EIP-4844 and the Verkle effort). It makes it clear to the reader what is meant. With `List<T, 1>` it needs to be accessed like an array, and with `Union<None, T>` it is unclear whether the intent is for this to grow to a `Union<None, T, U>` in the future. At the very least, it should be defined as a typealias and recommended for use by the protocol, so that the underlying intent can be appropriately represented in higher-level languages (e.g., Swift `?.` / `!.`, C# `??`, Nim `valueOr` and so on).

If there is a need for nested `Optional[Optional[...]]`, or `Optional[List[T, N]]` (note that empty lists usually already represent optional), the `Union` serialization could help disambiguate between `None` and `Some(None)` / `Some(List[T, N]())`. If those constructs are not needed, the proposed format based on [@zah](/u/zah) 's suggestion is a bit more compact, and gets rid of the parsing complexity of “what if someone sends an unknown selector”.  In any case, for unions as well as optionals, the `None` branch could be serialized as `b""` instead of `b"\0"` without loss of generality (so, only the `Some` branch would have a prefix).

Ultimately, point being, what is needed for new features are Optionals, not Unions, at this time.

---

**jflo** (2023-04-25):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> In any case, for unions as well as optionals, the None branch could be serialized as b"" instead of b"\0" without loss of generality (so, only the Some branch would have a prefix).

When you say `b""` are you intending that to be read as python for `List[uint8, 0]` ? Because if not, then I am left to interpret it as “don’t write anything to the stream”. In that second case, we would be without a marker for the `Optional[T]`, and I still don’t understand how an empty Optional[T] could be serialized.  Would you mind specifically addressing the second paragraph in my prior comment? I think that is the only thing holding me back from being fully on board with a new unique SSZ type that is not simply an alias for `List[T, 1]` or `Union[T, None]`.

---

**etan-status** (2023-04-25):

Yes, the current proposal is to “don’t write anything to the stream” for the `None` case, and to restrict `Optional[T]` to `T` that cannot ever encode as the empty data. There are only two cases that can encode as empty, namely:

1. A nested Optional (but, Optional[Container[Optional[T]]] is alright if truly needed).
2. A List[T, N] (can use 0 to denote no elements present, and Optional[Container[List[T, N]]] is alright if truly needed).

Note that there are similar “illegal types” for others:

- Empty vector types (Vector[type, 0], Bitvector[0]) are illegal.
- Containers with no fields are illegal.
- The None type option in a Union type is only legal as the first option (i.e. with index zero).

If it is a concern to disallow `Optional[Optional[T]]` and `Optional[List[T,N]]`, it could be minimally changed to encode as: `b""` (empty) for `None`, and `b"\1" + serialize(value)` for `Some`.

Or, if the current (unused) Union encoding is to be applied, `None` would encode as `b"\0"` instead of `b""`, for consistency. Or, the Union encoding could be updated to encode the `None` case as `b""` as well.

---

**etan-status** (2023-04-27):

From discussion at today’s AllCoreDevs call ([Execution Layer Meeting 160 · Issue #759 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/759)), additional change request was made:

- None case should remain b"".
- Some case should be prefixed with b"\x01" to allow Optional[Optional] and Optional[List], and for compatibility with implementations that wish to implement Optional as a special case of Union.
- Union (currently unused) should change the None case to b"" as well.

Changes will be discussed in EIP-4844 meeting: [EIP-4844 Implementers' Call #21 · Issue #760 · ethereum/pm · GitHub](https://github.com/ethereum/pm/issues/760)

Changes have been implemented:

- eip bump + remerkleable impl + tests: Update EIP-6475: Add `0x01` prefix for `Some` by etan-status · Pull Request #6945 · ethereum/EIPs · GitHub
- consensus-specs: EIP-6475: Add SSZ `Optional[T]` type by etan-status · Pull Request #3336 · ethereum/consensus-specs · GitHub
- nim: update for latest `Optional` spec by etan-status · Pull Request #46 · status-im/nim-ssz-serialization · GitHub
- move EIP-6475 to review: Update EIP-6475: Move to Review by etan-status · Pull Request #6946 · ethereum/EIPs · GitHub
- bump EIP-4844 to use SSZ Optional: Update EIP-4844: Use SSZ `Optional` for `Address` by etan-status · Pull Request #6495 · ethereum/EIPs · GitHub

---

**etan-status** (2023-08-30):

An alternative scheme to the Optional could be [EIP-7495: SSZ PartialContainer](https://eips.ethereum.org/EIPS/eip-7495)

More flexible and even more compact, but needs to be attached to the surrounding container.

It seems ideal for the purpose of [EIP-6493: SSZ Transaction Signature Scheme](https://eips.ethereum.org/EIPS/eip-6493) - the only other location where EIP-6475 optional is still considered is [TheVerge: spec draft by gballet · Pull Request #3230 · ethereum/consensus-specs · GitHub](https://github.com/ethereum/consensus-specs/pull/3230) which could also be represented using PartialContainer.

