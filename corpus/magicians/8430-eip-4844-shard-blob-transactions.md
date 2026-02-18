---
source: magicians
topic_id: 8430
title: "EIP-4844: Shard Blob Transactions"
author: protolambda
date: "2022-02-26"
category: EIPs > EIPs core
tags: [transactions, sharding]
url: https://ethereum-magicians.org/t/eip-4844-shard-blob-transactions/8430
views: 18206
likes: 40
posts_count: 45
---

# EIP-4844: Shard Blob Transactions

Discussion thread for [EIP-4844](https://eips.ethereum.org/EIPS/eip-4844)

## Background

See previous sharding discussion in:

- Sharding format blob carrying transactions
- Sharding design with tight beacon and shard block integration

Background information for self-adjusting independent gasprice for blobs:

- multidimensional EIP 1559
- with an exponential pricing rule

Rollup integration background:

- Commitment proof of equivalence protocol

## Implementation

The implementation is a work in progress while the specification is being reviewed and improved.

Execution layer implementation: [Datablob transactions by protolambda · Pull Request #1 · protolambda/go-ethereum · GitHub](https://github.com/protolambda/go-ethereum/pull/1)

Consensus layer implementation: [Comparing kiln...blobs · OffchainLabs/prysm · GitHub](https://github.com/prysmaticlabs/prysm/compare/kiln...blobs)

## Replies

**djrtwo** (2022-02-28):

Great work [@protolambda](/u/protolambda) and others!

This EIP suggests “a target of ~1 MB per block and a limit of ~2 MB”. I believe StarkWare’s [First “Big Red Dot”](https://ethereum-magicians.org/t/eip-2028-transaction-data-gas-cost-reduction/3280/24)  and [Second “Big Red Dot”](https://ethereum-magicians.org/t/eip-2028-transaction-data-gas-cost-reduction/3280/35) mainnet experiments and analysis from July 2019 and Jan 2020, respectively. This analysis showed that when creating a series of “large” mainnet blocks (45KB-1.46MB) throughout a single day, that it had no appreciable affect on uncle rates.

This is an important and valuable analysis, but I think that there are subsequent simulations and analysis warranted before moving into the realm of regular 1MB blocks on mainnet.

A few things to consider

1. Does the shift from PoW to PoS have any impact on the prior analysis?

In PoW, there are likely in the small number of dozens of consensus forming nodes (miners) rather than on the order of thousands in the current beacon chain network. Orphaning in PoW is thus the question of whether these large blocks make it to the other (small number of) miners quickly rather than to all user nodes or to all stakers in PoS
2. 12s slot times in PoS might actually help prevent orphaning compared to PoW (a block is not likely to be orphaned if it makes in sub 12s times whereas the threshold is likely lower in PoW). But there is another important time, 4s – the attestation time into the slot. If large blocks regularly make it to the network after 4s, we’d see “incorrect head votes” for many attestations even though the block still makes it into the chain. This would be an indicator of non-optimality in the consensus and some loss of revenue for validators. But would potentially result in orphaning in future block-slot PBS fork choice rules which have a stricter reaction to these missed head attestations.
3. Does the shift from devp2p block gossip to libp2p block gossip have any impact on the expectations of load, propagation time, etc
4. Does the uncle rate actually capture the quality of service required here?

Even though blocks were not orphaned in the Big Red Dot experiments, are user nodes receiving and processing these blocks in a timely manner? or do the small set of mining nodes have some asymmetric bandwidth available and/or privileged position in the network (highly connected, multiple sentry nodes, etc)
5. What does the minimum network speed/bandwidth become in a 1MB block regime? Does this push out some class of user or locality? e.g. at 10mbps, 1MB block transfers take ~1s per hop, whereas a 100mbps, they take 0.1s
6. What becomes the minimum monthly data-cap required for such regular blocks (taking into account data-tx  mempool requirements and the gossip amplification factor)?

I don’t intend to nay-say the 1MB suggestion, but I want to highlight there are some pen-and-paper calculations and likely some network simulations in order beyond the prior Big Red Dot analyses to tune this number.

---

**yperbasis** (2022-03-04):

Can we please use `y_parity: boolean` rather than `v: uint8` in ECDSASignature (similar to EIP-1559 transactions)?

---

**yperbasis** (2022-03-04):

`get_intrinsic_gas` should also charge `Gtxcreate`  for create transactions as well as `ACCESS_LIST_ADDRESS_COST`/`ACCESS_LIST_STORAGE_KEY_COST` for access list.  See Eq (60) in the Yellow Paper.

---

**EdFelten** (2022-03-06):

Good proposal!  Thanks for your work on it.

One suggestion on the gas pricing.  Currently `update_blob_gas` sets

`new_total = max(current_total + blob_txs_in_block, targeted_total)`.

The rationale for this (from the code comment) is to “to avoid accumulating a long period of very low fees”.  This goal make sense.  But it seems that goal would be better met by using something like

`new_total = max(current_total + blob_txs_in_block, targeted_total - MAX_BLOB_TARGET_DEFICIT)`

for some value of `MAX_BLOB_TARGET_DEFICIT` like 64.  That would allow a burst of 64 blobs above the target, without increasing the price, provided there had been a previously quiet period bringing total usage 64 blobs below the target.

Without this change, the pricing would deviate from the goal of having pricing be agnostic to the distribution of block usage, in that using 8 and 8 blobs in consecutive blocks would not increase the price, whereas using 0 and 16 in consecutive block would increase the price.

The optimal value of `MAX_BLOB_TARGET_DEFICIT` would try to balance the goal of being usage history agnostic (which would argue for a larger value of `MAX_BLOB_TARGET_DEFICIT`) with wanting to avoid a long burst of over-target usage without a price increase (which would argue for a smaller value of `MAX_BLOB_TARGET_DEFICIT`).  Essentially the value of this parameter would say how long a “period of very low fees [despite high usage]” to allow after a prolonged period of low usage.

My tentative proposal would be a value of 64 blobs, or 8 * `TARGET_BLOB_TXS_PER_BLOCK`.

---

**dankrad** (2022-03-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/edfelten/48/4559_2.png) EdFelten:

> new_total = max(current_total + blob_txs_in_block, targeted_total - MAX_BLOB_TARGET_DEFICIT)
>
>
> for some value of MAX_BLOB_TARGET_DEFICIT like 64. That would allow a burst of 64 blobs above the target, without increasing the price, provided there had been a previously quiet period bringing total usage 64 blobs below the target.

In principle I agree with this, in practice I think it will make very little difference. The reason is that the gas price at the balance point is very low: if `current_total=actual_total`, then the cost of one 128 kb data blob would be 1 gas, which at today’s gas prices and Ether price comes to 0.01 cent (for comparison, current prices would be 2M gas, so two million times that). Even at the highest prices we have seen it would still be less than a cent *for the whole blob*. This pricing is so cheap that I can’t see it being an equilibrium point at any time after there is any significant use of data blocks, so I don’t think it’s necessary to complicate it with another constant.

---

**EdFelten** (2022-03-10):

Ah, good point.  Although that could equally well be an argument for a larger value of `MAX_BLOB_TARGET_DEFICIT`, one large enough that the price difference would be significant.  That would increase the burst size that could be accommodated without price increase, in a scenario where the overall average usage is within the target.

The limiting factor is how bursty an average-target load could be before it became burdensome for nodes.

---

**protolambda** (2022-03-11):

[@yperbasis](/u/yperbasis) thank you for reporting those two issues! I updated the EIP here: [EIP-4844: v -> y_parity like EIP-1559, and fix intrinsic gas by protolambda · Pull Request #4904 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/4904)

I’ll check the go-ethereum fork now to make sure the changes are reflected.

---

**daniellehrner** (2022-03-14):

Regarding the `Gas price calculation` it says:

> Note that unlike existing transaction types, the gas cost is dependent on the pre-state of the block.

Do I understand this correctly that an exact gas price estimation is not possible with this new type of transaction? If that should indeed be the case, how should calls to `eth_estimateGas` with this transaction type be handled?

---

**protolambda** (2022-03-14):

Only the “blobs” part of the transaction is dependent on the pre-state. And the cost changes there are bounded by the EIP-1559-like fee adjustments.

So `eth_estimateGas` will work like normal for the most part, but then we need to consider additional gas for the blob data. Maybe we can return a separate estimate for that?

---

**daniellehrner** (2022-03-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/protolambda/48/16651_2.png) protolambda:

> So eth_estimateGas will work like normal for the most part, but then we need to consider additional gas for the blob data. Maybe we can return a separate estimate for that?

Yes, I think we should definitely reflect it in `eth_estimateGas`. In my experience the endpoint is often used to retrieve which value to set as the gas limit of a transaction. So it definitely should return a result which takes the additional cost of the blob into consideration.

---

**wschwab** (2022-03-15):

Should this be getting pushed into Review, or is it still too early?

---

**nibnalin** (2022-03-21):

Hi folks, big fan of this EIP and the direction this takes Ethereum in!

I had one question/suggestion: The proposed KZG commitment is quite useful for rollups that execute inside the EVM, but one other use case for guaranteed data availability of large off chain, short lived blobs is in enabling a new class of SNARK based applications. In particular, blobs (in theory) enable the usage of off-chain blobs as hidden inputs to a SNARK circuit, and the circuit can attest that the hash of the blob matches the on-chain commitment and has valid properties/transformations. I can think of many applications of this, as an example, here’s an idea made possible by this:

> You store params for a trusted setup ceremony in a blob, and a guaranteed hash of these on-chain. Every time a new participant wants to be part of this ceremony, they use the off-chain blob to generate the new params and put them in a new blob, along with a snark proof that their contribution transitions correctly from a blob that hashed to the previous on chain hash to the new hash.

Of course, there are many other classes of such applications that could benefit from such a data availability model that would be ideal for running inside a SNARK (thanks to their succinctness properties). **However, this brings me to my suggestion: Add an option to store the on-chain commitment in a SNARK friendly method**. KZG commitments require a pairing check which is notoriously hard to implement in a SNARK with the current most popular schemes (Groth/PLONK) since constraints blow up with each “bigint” operation. So, adding a SNARK friendly commitment would enable for more practical SNARK based applications. I would suggest the option to add a merkle tree using a SNARK friendly accumulator function (such as Poseidon/MIMC). Of course, at the end, it is a question of whether or not the added complexity to the interface and the difficulty of implementation is worth it for enabling such applications (that are relatively unproven), so I’d be curious to hear thoughts and considerations of that.

Thanks!

P.S. This is my first time commenting here ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12) Let me know if there’s anything i should add/detail.

---

**vbuterin** (2022-03-21):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/nibnalin/48/5703_2.png) nibnalin:

> However, this brings me to my suggestion: Add an option to store the on-chain commitment in a SNARK friendly method. KZG commitments require a pairing check which is notoriously hard to implement in a SNARK

KZG commitments are actually very SNARK friendly. The trick is that you don’t take the “naive approach” of actually trying to verify the KZG inside the SNARK directly. Instead, you just directly use the KZG point as a public input (this allows you to directly access everything inside the KZG in systems like PLONK). If you want to make a SNARK over something other than the BLS-12-381 curve or over a different trusted setup, then there is a [proof of equivalence protocol](https://ethresear.ch/t/easy-proof-of-equivalence-between-multiple-polynomial-commitment-schemes-to-the-same-data/8188) that allows you to make another commitment $D$ that is compatible with your SNARK protocol, and prove that $D$ and the KZG commit to the same data.

---

**web3Mike** (2022-04-21):

This is a great proposal. I have a question that others may not be particularly concerned about: how does EIP4844 (and Full Sharding after that) guarantee that nodes retain blob data for a specific amount of time (say a month)? I see in the EIP that blob data is deleted after 30 days, but there is no specific scheme to guarantee this

---

**optimalbrew** (2022-04-25):

> deleted after 30 days, but there is no specific scheme to guarantee this

Perhaps you mean the guarantee that it is stored for **at least** 30 days. Node operators can choose when they actually purge / delete. [Vitalik’s FAQs](https://notes.ethereum.org/@vbuterin/proto_danksharding_faq#If-data-is-deleted-after-30-days-how-would-users-access-older-blobs) mentions cases where some will retain data longer.

---

**qizhou** (2022-06-16):

Very nice proposal!  Just a few questions for clarification:

> Beacon chain validation
>
>
> On the consensus-layer the blobs are now referenced, but not fully encoded, in the beacon block body.

How the blobs in beacon blocks are referenced?  Would beacon blocks also include the Tx or other data structure to reference?

Following the previous question - since the blocks of CL and EL are produced asynchronously, what is the expected sequence of including a tx-without-blob in EL and referencing blob in CL?  Further, how could we ensure that both EL and CL do the correct work (e.g., a tx-without-blob is included in EL, but no such blob is referenced in CL?)

---

**axic** (2022-09-08):

> We add an opcode DATAHASH (with byte value HASH_OPCODE_BYTE ) which takes as input one stack argument index , and returns tx.message.blob_versioned_hashes[index] if index < len(tx.message.blob_versioned_hashes) , and otherwise zero. The opcode has a gas cost of HASH_OPCODE_GAS .

Was a name other than `DATAHASH` considered? I think it is too similar to `CALLDATA` as well as potentially accessing the “data” portion of an account code could have such opcodes.

I’d propose to use something akin to `BLOBHASH` or `TXBLOBHASH` to start utilising a `TX` prefix. In connection to [EIP-1803: Rename opcodes for clarity](https://ethereum-magicians.org/t/eip-1803-rename-opcodes-for-clarity/3345) we discussed prefixing opcodes according to their role (`BLOCK`, `TX`, …)

---

**axic** (2022-09-08):

```auto
def point_evaluation_precompile(input: Bytes) -> Bytes:
    # Verify P(z) = a
    # versioned hash: first 32 bytes
    versioned_hash = input[:32]
    # Evaluation point: next 32 bytes
    x = int.from_bytes(input[32:64], 'little')
    assert x < BLS_MODULUS
    # Expected output: next 32 bytes
    y = int.from_bytes(input[64:96], 'little')
    assert y < BLS_MODULUS
    # The remaining data will always be the proof, including in future versions
    # input kzg point: next 48 bytes
    data_kzg = input[96:144]
    assert kzg_to_versioned_hash(data_kzg) == versioned_hash
    # Quotient kzg: next 48 bytes
    quotient_kzg = input[144:192]
    assert verify_kzg_proof(data_kzg, x, y, quotient_kzg)
    return Bytes([])
```

The precompile uses little endian byte order for certain inputs. Currently the execution layer exclusively uses big endian notation, while the consensus layer (beacon chain) uses little endian. While this proposals makes this data opaque to the EVM (to be just passed through to this precompile), it feels like trading consistency of the execution layer in favour of consistency within the consensus layer.

I do not have any proposed solution here, just interested in opinions and views around the reasoning for this.

---

**axic** (2022-09-08):

Furthermore, I think the description of the precompile is not entirely clear. I assume the `assert` statements if hit, will result in an OOG outcome (i.e. consume all passed gas in the call). While the successful run will not result in an OOG case, but will return 0 bytes (i.e. `returndatasize` will equal 0).

Furthermore it is unclear whether it pads inputs with zeroes, or would signal failure if the input is not exactly 192 bytes.

Is that correct?

The closest precompile to this is ECPAIRING ([EIP-197: Precompiled contracts for optimal ate pairing check on the elliptic curve alt_bn128](https://eips.ethereum.org/EIPS/eip-197)) which returns `U256(0)` or `U256(1)` depending on the outcome. I think it is nice to avoid the need for checking return values if this can be delegated to only checking the success value of `CALL`, but nevertheless it is something breaking consistency with other precompiles. In this case likely it makes sense however.

Suggestion is to just clarify the description in the EIP.

---

**axic** (2022-09-08):

```auto
class ECDSASignature(Container):
    y_parity: boolean
    r: uint256
    s: uint256
```

Nice to see that the new transaction format replaces the RLP transaction encoding with SSZ and moves `chain_id` to be a field allowing for using `boolean` for `y_parity.

There’s potential for some optimisation here at the expensive of some clarity: [EIP-2098: Compact Signature Representation](https://eips.ethereum.org/EIPS/eip-2098)

Was this discussed yet?

Edit: the `parity` field seems to have a 1 byte overhead so this is neglible.


*(24 more replies not shown)*
