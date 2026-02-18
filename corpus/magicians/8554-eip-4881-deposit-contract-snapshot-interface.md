---
source: magicians
topic_id: 8554
title: "EIP-4881: Deposit Contract Snapshot Interface"
author: ethDreamer
date: "2022-03-08"
category: EIPs
tags: [consensus-layer, interop, interfaces, standards-adoption]
url: https://ethereum-magicians.org/t/eip-4881-deposit-contract-snapshot-interface/8554
views: 3093
likes: 1
posts_count: 10
---

# EIP-4881: Deposit Contract Snapshot Interface

Discussion thread for EIP-4881:

https://eips.ethereum.org/EIPS/eip-4881

Standardizing the format and endpoint for transmitting a snapshot of the deposit Merkle tree

## Replies

**ethDreamer** (2022-03-08):

[Initial discussion on discord](https://discord.com/channels/595666850260713488/692062809701482577/926524481093136395)

---

**ethDreamer** (2022-03-08):

#### Existing Implementations

- lighthouse
- nimbus

---

**ajsutton** (2022-05-14):

In `MerkleTree.generate_proof` the code references `node.left` and `node.right` but these properties don’t actually exist in `MerkleTree`.  For a non-empty tree you would always wind up with a `Node` instance which does have those properties  but for an empty tree the root would a `Zero` instance and I believe the method would fail.

It would probably be clearer if this duck typing was avoided in any case.

---

**ajsutton** (2022-07-14):

I’m slightly confused about the SSZ format for `DepositTreeSnapshot`.  It’s initial defined as:

```auto
DepositTreeSnapshot {
    finalized: Vector[Hash32],
    deposits: uint64,
    execution_block_hash: Hash32,
}
```

but no length is given for the `finalized` vector. In the reference implementation `finalized` is defined as a `List` but no maximum length is specified. `List<Bytes32>` seems to be the right data structure but we’d need to specify a maximum length for it to have a complete SSZ object definition.

---

**ethDreamer** (2022-07-19):

(post deleted by author)

---

**ethDreamer** (2022-07-19):

Hi Aj!

Thanks for your feedback. I omitted error/sanity checking to avoid cluttering the code. But I did try to allude to error cases in my comments. Looks like I missed this one. I could simply add:

```auto
    def get_proof(self, index: uint) -> Union[Hash32, List[Hash32]]:
+       # omitted check to ensure tree is not empty
        # omitted check to ensure index > finalized deposit index
```

> It would probably be clearer if this duck typing was avoided in any case.

Not sure of a good way to do that here given that `left` and `right` are not properties of all classes that extend `MerkleTree`. Did you have any ideas? It shouldn’t happen for any `Leaf` as they only occur at `depth = 0`. As long as the check about `index > finalized index` is enforced, it wouldn’t happen for any `Finalized` type either.

---

**ethDreamer** (2022-07-19):

Hi Aj!

Thanks for your feedback! The maximum size of the `finalized` array is the depth of the deposit tree (32). But it’s a variable length array; the length depends on how many deposits are in the snapshot. I see in the [ssz specs](https://github.com/ethereum/consensus-specs/blob/dev/ssz/simple-serialize.md#variable-size-and-fixed-size):

> vector: ordered fixed-length homogeneous collection, with N values
> notation Vector[type, N], e.g. Vector[uint64, N]
> list : ordered variable-length homogeneous collection, limited to N values
> notation List[type, N]

So perhaps this confusion stems from me defining it initially as a `Vector` instead of a `List`? I can change it to a `List` if that’s more clear.

In regards to the reference implementation, I don’t see mention of using this second parameter to define a maximum length for `List[T]` in the [typing library](https://docs.python.org/3/library/typing.html) I imported…

The reference implementation does pass the test cases if I define the snapshot like this:

```auto
class DepositTreeSnapshot:
    finalized: List[Hash32, DEPOSIT_CONTRACT_DEPTH]
    deposits: uint64
    execution_block_hash: Hash32
```

though the tests will also pass if I define as `finalized` as `List[Hash32, 1]` which suggests the second parameter is just being ignored…

I can define it that way, though I worry that people might mistake it as a fixed length vector of size 32 instead of specifying a maximum length. Open to suggestions though.

---

**ajsutton** (2022-09-13):

Slow on this, but the `List[Hash32, DEPOSIT_CONTRACT_DEPTH]` is the right syntax from what I understand.  Teku’s implementation of `List` does enforce the maximum length (and demands to have one specified).

Agreed it should be variable, hence the `List` instead of `Vector`.  That also affects the SSZ serialisation as a vector doesn’t include any indication of length but a List adds an extra node to the SSZ tree to record the list length.

---

**poojaranjan** (2023-11-20):

Congratulations on the EIP reaching `Final` status.

To learn more, check out [EIP-4881: Deposit Contract Snapshot Interface](https://www.youtube.com/watch?v=GzQSVdTwAa0) with [@ethDreamer](/u/ethdreamer)

  [![image](https://ethereum-magicians.org/uploads/default/original/2X/0/013284c50d93a67fa86247b861f2fad9e806ad42.jpeg)](https://www.youtube.com/watch?v=GzQSVdTwAa0)

