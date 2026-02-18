---
source: magicians
topic_id: 19998
title: "EIP-7706: Create a separate basefee and gaslimit for calldata"
author: vbuterin
date: "2024-05-13"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-7706-create-a-separate-basefee-and-gaslimit-for-calldata/19998
views: 2717
likes: 9
posts_count: 13
---

# EIP-7706: Create a separate basefee and gaslimit for calldata

Add a new type of gas for transaction calldata. Add a new transaction type that provides `max_basefee` and `priority_fee` as a vector, providing values for execution gas, blob gas and calldata gas. Modify EIP-1559 to use the same mechanism for the three types of gas.

https://github.com/ethereum/EIPs/pull/8552

## Replies

**daniellehrner** (2024-05-14):

Is this EIP a replacement for  [EIP-7623](https://eips.ethereum.org/EIPS/eip-7623)? Or would you recommend to still do 7623 first, because it’s less complex, and 7706 at a later point?

---

**vbuterin** (2024-05-14):

This EIP feels complex enough in its implications that I think it’s unlikely for it to get included in Pectra. So I would still favor 7623 being done asap. In parallel, I think we should do all the required analysis to improve our knowledge of how fee markets behave economically, and implement this EIP when we’re confident enough that we can do it.

---

**etan-status** (2024-05-16):

The EIP describes three changes:

1. Switch to a multidimensional fee structure
2. Allowing priority fees for blob transaction
3. Introduction of a separate calldata gas fee

I’m wondering about the encoding of the `max_fees_per_gas` and `priority_fees_per_gas` vectors on JSON-RPC. Natively, they would be represented as a list of integers (in the typical string representation), without any guidance on which of the fees corresponds to what type of fee. For example, there must be external knowledge that the second one is referring to blobs. A named tuple would improve clarity over the vector design, while still allowing efficient iteration for the generic cost computation via type reflection.

Another JSON-RPC question would be how existing clients could remain supported, e.g., would the `max_fee_per_gas` in there simply return `max_fees_per_gas[0]`? Or would the schema change to `max_fees_per_gas` and any client depending on the existing `max_fee_per_gas` would break? The one case that should be avoided is the one where JSON-RPC simply extends with a `max_fee_per_calldata_gas` / `max_priority_fee_per_calldata_gas`, the switch to multidimensional should be done on all layers.

In an SSZ world, the new transaction type could be modelled as an [EIP-7495](https://eips.ethereum.org/EIPS/eip-6493) profile of the [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493) `Transaction` (specs still in flux regarding the details).

The EIP-6493 `TransactionPayload` would be extended with two new fields for holding the new fee tuple.

```python
class FeePerGas(uint256):
    pass

class FeesPerGas(StableContainer[16]):
    regular: Optional[FeePerGas]
    blob: Optional[FeePerGas]
    calldata: Optional[FeePerGas]

class TransactionPayload(StableContainer[32]):
    type_: Optional[TransactionType]
    chain_id: Optional[ChainId]
    nonce: Optional[uint64]
    max_fee_per_gas: Optional[FeePerGas]
    gas: Optional[uint64]
    to: Optional[ExecutionAddress]
    value: Optional[uint256]
    input_: Optional[ByteList[MAX_CALLDATA_SIZE]]
    access_list: Optional[List[AccessTuple, MAX_ACCESS_LIST_SIZE]]
    max_priority_fee_per_gas: Optional[FeePerGas]
    max_fee_per_blob_gas: Optional[FeePerGas]
    blob_versioned_hashes: Optional[List[VersionedHash, MAX_BLOB_COMMITMENTS_PER_BLOCK]]
    max_fees_per_gas: Optional[FeesPerGas]
    max_priority_fees_per_gas: Optional[FeesPerGas]
```

Then, new versions of the `Basic`/`Blob` profile could be introduced.

```python
class BasicFeesPerGas(Profile[FeesPerGas]):
    regular: FeesPerGas
    calldata: Optional[FeesPerGas]

class BasicTransactionPayloadV2(Profile[TransactionPayload]):
    chain_id: ChainId
    nonce: uint64
    gas: uint64
    to: Optional[ExecutionAddress]
    value: uint256
    input_: ByteList[MAX_CALLDATA_SIZE]
    access_list: List[AccessTuple, MAX_ACCESS_LIST_SIZE]
    max_fees_per_gas: BasicFeesPerGas
    max_priority_fees_per_gas: BasicFeesPerGas

class BlobFeesPerGas(Profile[FeesPerGas]):
    regular: FeesPerGas
    blob: FeesPerGas
    calldata: Optional[FeesPerGas]

class BlobTransactionPayloadV2(Profile[TransactionPayload]):
    chain_id: ChainId
    nonce: uint64
    gas: uint64
    to: ExecutionAddress
    value: uint256
    input_: ByteList[MAX_CALLDATA_SIZE]
    access_list: List[AccessTuple, MAX_ACCESS_LIST_SIZE]
    blob_versioned_hashes: List[VersionedHash, MAX_BLOB_COMMITMENTS_PER_BLOCK]
    max_fees_per_gas: BlobFeesPerGas
    max_priority_fees_per_gas: BlobFeesPerGas
```

We would then have the following transaction profiles available:

```python
class AnyTransactionPayload(Union[
        # Imported from RLP
        ReplayableTransactionPayload,
        LegacyTransactionPayload,
        Eip2930TransactionPayload,
        Eip1559TransactionPayload,
        Eip4844TransactionPayload,

        # EIP-6493
        BasicTransactionPayload,
        BlobTransactionPayload,

        # EIP-7706
        BasicTransactionPayloadV2,
        BlobTransactionPayloadV2]:
    pass
```

And the helpers for obtaining fees would become:

```python
def get_max_fees(tx: AnyTransactionPayload) -> [FeePerGas, FeePerGas, FeePerGas]:
    if hasattr(tx, 'max_fees_per_gas'):
        fees = tx.max_fees_per_gas
        return [
            fees.regular,
            fees.blob if hasattr(tx, 'blob_versioned_hashes') else FeePerGas(0),
            fees.calldata if fees.calldata is not None else fees.regular
        ]
    else:
        return [
            tx.max_fee_per_gas,
            tx.max_fee_per_blob_gas if hasattr(tx, 'blob_versioned_hashes') else FeePerGas(0),
            tx.max_fee_per_gas
        ]

def get_priority_fees(tx: AnyTransactionPayload) -> [FeePerGas, FeePerGas, FeePerGas]:
    if hasattr(tx, 'max_priority_fees_per_gas'):
        fees = tx.max_priority_fees_per_gas
        return [
            fees.regular,
            fees.blob if hasattr(tx, 'blob_versioned_hashes') else FeePerGas(0),
            fees.calldata if fees.calldata is not None else fees.regular
        ]
    elif hasattr(tx, 'max_priority_fee_per_gas'):
        return [
            tx.max_priority_fee_per_gas,
            FeePerGas(0),
            tx.max_priority_fee_per_gas
        ]
    else:
        return [
            tx.max_fee_per_gas,
            FeePerGas(0),
            tx.max_fee_per_gas
        ]
```

If we want, we could introduce these two aspects as part of EIP-6493:

1. Switch to a multidimensional fee structure
2. Allowing priority fees for blob transaction

by not even introducing the `max_fee_per_gas` / `max_priority_fee_per_gas` / `max_blob_fee_per_gas` into SSZ transactions in first place. As part of the RLP → SSZ conversion, the normalization to multidimensional gas could also be processed, in the same manner how v/r/s is already normalized to bytevector[65] + chain_id during the conversion process.

Then, with EIP-7706 we would simply extend `FeesPerGas`/`BasicFeesPerGas`/`BlobFeesPerGas` with the `calldata: Optional[FeePerGas]` entry, and could avoid the need for a V2 version of Basic/BlobTransaction.

---

**vbuterin** (2024-05-17):

7706 actually introduces *four* changes: the fourth is that execution gas is moved over to a 4844-style excess-based basefee adjustment implementation ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

It’s very much simultaneously a feature improvement (the separate calldata dimension) and a simplification - which I think is how it has to be done, because new gas dimensions being added haphazardly makes no sense and leads to hard-to-reason-about protocol complexity.

If we want to “bring forward” the simplification part into 6493, one option would be to do *everything* in 7706 *except* for the calldata dimension. So, max_basefee would become a (2-item) vector, priority_fee would become a vector, block.gasused would become a vector, excess would become a vector. And, importantly, `basefee` would become a *function* of excess, and would cease to be an independent block header field - and RPC providers could continue providing `basefee` by running that function.

So the only practical change would be that you can tip for blobs, but it would make it *technically* very easy to add more dimensions in the future.

---

**etan-status** (2024-05-17):

How strong is the support for the ‘multidimensional fee’ aspect? And, if we end up not adopting multidimensional fees, would a transaction format that structures the regular and blob fees as a vector still be preferrable over the one we currently use? Personally fine with backporting this aspect into 6493. The ‘tip for blobs’ could be disabled by forcing it to 0 initially (or to introduce it as an optional fee), if the EIP-6493 SSZ BlobTransaction should match the 4844 RLP transaction’s feature set.

Concerns about the multidimensional fee I see are with transaction pool complexity. For example, how to deal with a transaction that slightly underpays in one dimension but greatly overpays in another dimension? Maybe it’s easy for the ELs, I’m not familiar enough myself.

Block header change would be a separate EIP, 6493 only discusses transactions / receipts. Doesn’t have to be rolled out together, either (aligning EL block header with CL ExecutionPayloadHeader depends on converting the transactions / withdrawals to SSZ, though, as those are also known by the CL).

---

**etan-status** (2024-05-20):

In traditional finance, there are apparently also quite a few fees / taxes of different kinds associated with each trade, further supporting a switch to vectors.

I have made a PR to EIP-6493 that applies that suggestion to SSZ transactions, with the implications that SSZ `BlobTransaction` can tip for blobs (therefore being slightly more powerful than the RLP equivalent):

- Update EIP-6493: Switch to vector based fees (EIP-7706 w/o calldata fee) by etan-status · Pull Request #8579 · ethereum/EIPs · GitHub

---

**vbuterin** (2024-05-20):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png) etan-status:

> Concerns about the multidimensional fee I see are with transaction pool complexity. For example, how to deal with a transaction that slightly underpays in one dimension but greatly overpays in another dimension? Maybe it’s easy for the ELs, I’m not familiar enough myself.

We definitely need deeper economic research on that. Probably a concrete spec of a reasonably-close-to-optimal prioritization algorithm.

---

**ajsutton** (2024-05-20):

Also need to make sure that the txpool doesn’t wind up requiring tx replacements to bump the price of a heap of different variables. It already causes a lot of confusion and overspend for users to have to bump the maxFeeCap and the maxTipCap by 10% each (or double them for blob tx I think). If we have a bunch of different dimensions, you don’t want users to have to overpay on many dimensions just because they underpriced on one dimension like baseFee initially and now their transaction isn’t being included.

---

**etan-status** (2024-05-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> If we want to “bring forward” the simplification part into 6493, one option would be to do everything in 7706 except for the calldata dimension.

I think there’s no downside to this, in EIP-6493. It makes the design cleaner and more extensible / future-proof.

Have updated SSZ `Transaction` accordingly, and also the viewer on https://eth-light.xyz now shows vector fees.

- Example: Ethereum Light

If the blob tips are a problem, can force them to 0 initially and add support for non-0 values lateron.

---

**bertkellerman** (2024-06-04):

I support the inclusion of all limits in the execution header. There are some issues with the current EIP-4844 implementation that arise from having only the excess and not the explicit limit on chain.

In summary, the mechanism can experience price discontinuities when scaling up/down, historical price calc for devs is worse and nodes lack independence in increasing limits.

I detailed these issues in a hackmd post but am unable to post links here. If anyone is interested I can paste it here.

However, this EIP fixes this! ![:grinning:](https://ethereum-magicians.org/images/emoji/twitter/grinning.png?v=12)

But we should continue to be aware of these issues when using feedback mechanisms with accumulators.

---

**mralj** (2024-10-26):

Hey!

I have questions about the `opcodes`, as far as I can tell nothing has been specified in the EIP.

Specifically:

1. Will there be a separate opcode for the CALLDATABASEFEE, as there are one for both execution (BASEFEE) and the blob (BLOBBASEFEE) base fees?
2. Will there be an opcode for the base fees vector?

If the answer to either is yes, do we need a new EIP for this (akin to [EIP-7516](https://eips.ethereum.org/EIPS/eip-7516))?

---

**poojaranjan** (2025-03-01):

[PEEPanEIP#142: EIP-7706 Separate gas type for calldata](https://youtu.be/c3TV6OhjSfc)

  [![image](https://img.youtube.com/vi/c3TV6OhjSfc/maxresdefault.jpg)](https://www.youtube.com/watch?v=c3TV6OhjSfc)

