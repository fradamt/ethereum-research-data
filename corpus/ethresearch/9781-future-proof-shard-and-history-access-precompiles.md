---
source: ethresearch
topic_id: 9781
title: Future-proof Shard and History Access Precompiles
author: vbuterin
date: "2021-06-08"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/future-proof-shard-and-history-access-precompiles/9781
views: 6509
likes: 11
posts_count: 7
---

# Future-proof Shard and History Access Precompiles

One of the backwards-compatibility challenges in the current Ethereum design is that history access requires in-EVM verification of Merkle proofs, which assume that the blockchain will forever use the same formatting and the same cryptography. Sharding increases the importance of this, as fraud proofs and validity proofs for rollups will require pointers to shard data.

This post proposes a more future-proof way of doing this: instead of requiring in-EVM verification of proofs to history and shards, we can add precompiles that perform the abstract task of verifying a proof of a certain type. If, in the future, formats are changed, the precompile logic will change automatically. The precompiles can even have conditional logic that verifies one kind of proof for pre-transition slots and another kind of proof for post-transition slots.

## Historical block data

```auto
def verifyHistoricalBlockRoot(
    slot: uint256,
    value: bytes32,
    proof: bytes
)
```

The precompile will attempt to interpret the `proof` in one of two ways:

1. If the proof is empty, it will check directly if the value is the saved historical block root in the correct position. If slot is too old, it will fail.
2. If the proof is a Merkle branch, it will verify it as a Merkle branch against the correct entry in historical_roots

```auto
def verifyHistoricalStateRoot(
    slot: uint256,
    value: bytes32,
    proof: bytes
)
```

Verifies the state root, using the same logic as for the block root.

```auto
def verifyHistoricalStateValue(
    slot: uint256,
    key: bytes32,
    value: bytes32,
    proof: bytes
)
```

Verifies a value in a historical state. The `proof` consists of three elements:

- The state root
- A proof that shows the correctness of the state root
- A Patricia or Verkle or other proof that the value actually is in the position key in the state tree (this assumes that the proposed scheme for mapping all account contents to a 32-byte key is permanently enshrined)

```auto
def verifyHistoricalTransaction(
    slot: uint256,
    txindex: uint256,
    tx: bytes,
    proof: bytes
)
```

Verifies that `tx` actually is in the `txindex` of the block at the given `slot`. The proof contains:

- The block root
- A proof that shows the correctness of the block root
- A proof that the given tx actually is the transaction in the given position

```auto
def verifyHistoricalReceipt(
    slot: uint256,
    txindex: uint256,
    receipt: bytes,
    proof: bytes
)
```

Verifies that `receipt` actually is the receipt for the transaction at the `txindex` of the block at the given `slot`. The proof contains:

- The block root
- A proof that shows the correctness of the block root
- A proof that the given receipt actually is the receipt in the given position

## Shard data

```auto
def verifyShardBlockBody(
    slot: uint256,
    shard: uint256,
    startChunk: uint256,
    chunks: List[bytes32],
    proof: bytes
)
```

Verifies that `chunks = body[startChunk: startChunk + len(chunks)]` where `body` is the body at the given `shard` in the given `slot`. The proof would consist of:

- The Kate proof to prove the subset of a block
- If the slot is too old (older than 128 epochs?), a Merkle proof to the state root at slot + 96 and then a Merkle proof from that slot to the position in the shard commitments array showing a finalized commitment

While we are using BLS-12-381 Kate commitments, the precompile would also verify that `data` is a list of 32-byte chunks where each chunk is less than the curve subgroup order. If no shard block is saved in a given position, the precompile acts as though a commitment to zero-length data was saved in that position. If the value at a given position is uncomfirmed, the precompile always fails.

```auto
def verifyShardPolynomialEvaluation(
    slot: uint256,
    shard: uint256,
    x: uint256,
    y: uint256,
    proof: bytes
)
```

If we treat the shard block at the given `(slot, shard)` as a polynomial `P`, with bytes `i*32 ... i*32+31` being the evaluation at `w**i`, this verifies that `P(x) = y`. The `proof` is the same as for the data subset proof, except the Kate proof is proving an evaluation at a point (possibly outside the domain) instead of proving data at a subset of locations.

If we move away from BLS-12-381 in the future (eg. to 32-byte binary field proofs), the precompile would take as input a SNARK verifying that `data` is made up entirely of values less than the curve order, and verifying the evaluation of `data` over the current field.

This precompile is useful for the [cross-polynomial-commitment-scheme proof of equivalence protocol](https://ethresear.ch/t/easy-proof-of-equivalence-between-multiple-polynomial-commitment-schemes-to-the-same-data/8188), which can be used to allow ZK rollups to directly operate over shard data.

## Replies

**yoavw** (2021-06-08):

Looks like a good abstraction layer.  I suppose it would replace [EIP 2935](https://github.com/ethereum/EIPs/blob/74b5b9636461f44251dab85f3b5ca8864ec074ec/EIPS/eip-2935.md).

Should it go further in abstracting proofs of items inside the historical block, such as logs, or is that the right amount of abstraction?

The context I have in mind is the one for which we discussed 2935 - a decentralized network for stateless read access.  The minimum requirement was proving the result of a historical view call and a historical log (or lack thereof in a position claimed by a node).  The current proposal is definitely enough for verifying past view calls, but for logs it would still require getting transaction receipts and parsing some data structures, maybe even verifying bloom filter correctness.  How likely are these structures to change in the future?

---

**vbuterin** (2021-06-08):

Personally I think bloom filters are outdated and we should just remove them at some point; relying on consensus nodes to do querying is too inefficient for dapps to have acceptably-good UIs, and so we’re going to have to rely on L2 protocols at some point. And those L2 protocols are going to be powerful enough to do queries not just over topics; they could easily, for example, treat the first N bytes of log *data* as “virtual topics” and index those too, so contracts can avoid paying gas for topics.

That would imply a more comprehensive reform of what post-transaction-execution information we commit to, and that could be done at the same time as when we do proofs of custody for execution. At that point… I suppose potentially more abstracted proof verification precompiles could be added! But if we want something for the here-and-now, a proof for either a full receipt, or the i’th log in a receipt, is probably good enough.

---

**yoavw** (2021-06-09):

Yes.  If we’re going to remove things like bloom filters (and we probably should), then we’ll need more abstraction precompiles.  I guess it’s fine to start with something like full receipts and i’th log in a receipt.  And then add more as new concepts are added.

Maybe it should even be an abstraction-layer contract, like an OS syscall layer.  Something like Arbitrum’s ArbSys contract at 0x64, and add more stuff to its ABI in future forks.

---

**Nashatyrev** (2021-06-09):

Some minor comments:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> ```auto
> def verifyShardBlockBody(
>     slot: uint256,
>     shard: uint256,
>     startChunk: uint256,
>     chunks: uint256,
>     data: bytes,
>     proof: bytes
> )
> ```

Do we need `chunks` parameter here? Can’t we derive it from `data.length`?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> If the slot is too old (older than 128 epochs?), a Merkle proof to the block root at slot + 96

Shouldn’t it be ‘state root’ instead of ‘block root’ here? Shard commitments array is stored in the beacon state

---

**vbuterin** (2021-06-09):

Thanks on both counts! Fixed.

---

**frangio** (2022-11-11):

The shard data precompiles proposed here have obviously evolved into the point evaluation precompile in proto-danksharding (EIP-4844).

Proving historical state in a forward compatible way is still unsolved.

In 4844 the slot number is no longer an argument to the precompile, which instead works solely from the versioned hash. Can something similar be done for state proofs? Meaning a precompile that proves state from a block hash or state root and not from a block number (as was presented in this post). I believe this would allow proving state across different EVM-chains (assuming the historical block hashes or state roots are present).

