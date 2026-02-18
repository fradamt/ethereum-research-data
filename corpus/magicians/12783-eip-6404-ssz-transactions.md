---
source: magicians
topic_id: 12783
title: "EIP-6404: SSZ Transactions"
author: etan-status
date: "2023-01-31"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-6404-ssz-transactions/12783
views: 4293
likes: 7
posts_count: 26
---

# EIP-6404: SSZ Transactions

Discussion thread for [EIP-6404: SSZ transactions](https://eips.ethereum.org/EIPS/eip-6404)

Vitalik’s notes:

- Proposed transaction SSZ refactoring for Cancun - HackMD

Related discussions:

- Transactions: This thread here
- Withdrawals: EIP-6465: SSZ Withdrawals Root
- Receipts: EIP-6466: SSZ Receipts
- SSZ: EIP-7495: SSZ ProgressiveContainer

# Background

Followup from https://github.com/ethereum/consensus-specs/files/10348043/elroots.pdf

Relevant channel: `#ssz` on ETH R&D Discord

## Security (for putting keccak and sha hashes in same namespace)

- Avalanche effect - Wikipedia
- Universal composability - Wikipedia
- https://crypto.stackexchange.com/a/96474
- https://crypto.stackexchange.com/questions/50974/merkle-trees-instead-of-the-sponge-or-the-merkle-damgård-constructions-for-the-d

#### Outstanding Issues

- 2024-10-29: 0 address is special in authorisations and should be None in SSZ, https://github.com/ethereum/EIPs/pull/8929/files

2025-06-29: Introduce a ProgressiveContainer for the replayable authorization

#### Update Log

- 2025-11-05: Move Union layer into payload
- 2025-11-03: Use opaque signature, and fix SetCode authorizations
- 2025-06-29: Use SSZ ProgressiveContainer / Union

## Replies

**matt** (2023-02-01):

Hi Etan, thanks a lot for writing this up. Some thoughts from my end:

- The single Transaction object seems very clunky as a definition. Although it might be nice to move to a world where there is only 1 type of transaction, we still have 3-4 types that need to be maintained. My belief is that hiding this behind helpers and converters, while it may be marginally more efficient, will cost us more in the long run in terms of reasoning about the abstraction and maintaining it. I strongly encourage we consider something closer to the original document Vitalik wrote.
- As a comment for the spec, please define all the structures statically. As an implementer it is difficult to parse the dynamically constructed serializers/deserializers.
- For legacy transactions, I believe using maxBaseFeePerGas as gasPrice is incorrect. It should set both maxBaseFeePerGas and maxPriorityFeePerGas to gasPrice.
- I don’t like how we are shoehorning the first byte of legacy transactions into a EIP-2718 type. It’s weird that pre-155 txs have many different possible types. I think this is where have separate containers would be much cleaner.
- It’s unnecessary to define receipt RLP values and hash values. They’re referred to either by i) transaction hash/id or ii) block and transaction index. The RLP is no longer a concern of consensus.

---

**etan-status** (2023-02-01):

Thanks for the thorough review, appreciate it!

I think it’s worth to explore both Vitalik’s approach and the single `Transaction` object approach. One open issue about Vitalik’s document is that it seems to shift complexity from the node implementation to the client application.

EIP-1559 introduces a `NormalizedTransaction`, suggesting that client implementations internally already convert to a single transaction type before processing them. My proposal moves that concept also into the SSZ merkle tree.

For example, a client would like to use a generic SSZ merkle proof API to obtain a proof for the `value` of a transaction. In the `Union` case, it seems that multiple round trips are needed (one for each layer of `Union`). In the `Onion` case, it is possible to request all potential `GeneralizedIndex` that may contain a `value` in one shot, together with the `tx_type`, and then filter out all the zeroes; however, the set of potential indices grows with each future transaction type. What is gained with the single `Transaction` object is that the `value` is always at the same location in the SSZ merkle tree.

I agree that marginal efficiency gains are not a core metric to optimize for. I have removed efficiency benefits from the EIP’s rationale to avoid giving them more weight than intended.

Regarding the other points:

- Indeed, having static structure definitions should make it more readable. Will update the EIP accordingly, possibly after ACDE tomorrow.
- Good catch about the max_priority_fee_per_gas. Fixed it.
- About the EIP-2718 type, yes, it is not a good fit. Also, the 0x00 type for EIP-155 is a hack, to distinguish post-EIP155 chain_id = 0 (explicit replayability) from pre-EIP155 chain_id = nil (implicit replayability). Given that EIP-2718 is mostly used on the network to differentiate between payload types, it may make sense to introduce a separate enum for the normalized Transaction, e.g., a TransactionVersion.
- For Receipt, good to know that this may be simplified even further. For the lookup by Transaction ID, it may be beneficial if the original (perpetual) Transaction ID is also included into the SSZ tree. This would allow serving a proof that provides the Receipt, the index of the Receipt, and the Transaction ID at the same index, so that the caller can cross-check that the Receipt is indeed linked to the requested Transaction ID. Another one for post-ACDE.

---

**etan-status** (2023-02-02):

I have now updated the EIP for clarity, based on your feedback.

- The EIP-2718 tx_type is gone. There is no reason to remember the original serialization format.
- A new hash_version was introduced to SignedTransaction. This hash_version indicates how the transaction was originally hashed for the purpose of signing, and for determining the perpetual transaction ID.
- Structures are no longer constructed incrementally.
- Unnecessary parts removed from Receipt section.
- Removed serialization examples for legacy transactions. There is now only an example for a non-blob transaction, and a with-blob transaction.

Open questions for today’s ACDE call:

- Onion/Union vs normalized Transaction discussion
- Can the block / block header be changed to SSZ as well, or should it be a separate step?

In the outermost layer of a block, there are still RLP lists of SSZ Transaction, could be gone
- CL ExecutionPayloadHeader == EL block header desirable?

Do we want to keep a tree for tx IDs, next to the tree for tx payloads?

- Tx inclusion proof should be possible without sending the entire tx
- Receipt proof should be possible without sending the entire tx?

Any use cases that don’t have a straight-forward way to query from the new SSZ merkle tree?

---

**etan-status** (2023-02-02):

Updated EIP-6404 once more:

- Removed networking changes. My EIP is solely about the SSZ merkle tree computation for transactions_root, receipts_root, and withdrawals_root. This means, it does not touch EL networking, and there can be as many non-blob and with-blob EIP-4844 types for the mempool as anyone wants, as long as they are normalizable as part of the SSZ merkle tree.
- Removed sighash and txid changes. The hashes are now compatible with EIP-4844, removing any security discussions about this EIP.
- The TxHashVersion is now equal to EIP-2718 transaction type, for 0x01, 0x02, and 0x05, to prevent confusion.
- I have added helpers for Receipt and Withdrawal to aid with receipts_root and withdrawals_root computation based on the pre-existing RLP receipt and withdrawal structures.
- Added missing max_fee_per_data_gas field to the normalized Transaction type.

---

**etan-status** (2023-02-02):

- Also added a transaction_hashes_root that commits to the perpetual transaction hashes. Useful for Receipt proofs. Functionality requested here: add eth_getReceiptProof by ncitron · Pull Request #372 · ethereum/execution-apis · GitHub

---

**vbuterin** (2023-02-06):

Why not just put the hash of each transaction into the receipt object? That avoids creating extra trees.

---

**vbuterin** (2023-02-06):

I personally would favor the transaction-related stuff, and the receipts + withdrawals logic, to be in separate EIPs. Their logic is mostly separate, and one could be implemented without the other.

---

**etan-status** (2023-02-06):

Indeed, referencing the transaction hash as part of the individual `Transaction` / `Receipt` structures makes this much cleaner. Updated the EIP:

- Removed transaction_hashes_root tree
- Wrap SignedTransaction and Receipt in IndexedTransaction / IndexedReceipt that tag them with tx_hash. Note, this doubles proof response size for obtaining all tx_hashes inside a block (sibling of each hash must be sent as part of the proof), but eliminates the complexity of an extra tree. This also reduces proof size for receipts and individual transaction fields, as all proof items can be fetched from a single SSZ tree.

Also revised transaction types:

- Replaced TxHashVersion with EIP-2718 TransactionType
- Removed EIP-155 (chain-ID in v) specific transaction type to allow type reuse with EIP-2718 types in Receipt.
- Add TransactionSubtype to distinguish chain_id = 0 from chain_id = None (instead of the removed EIP-155 type).

---

**etan-status** (2023-02-06):

Overall, I’m not sure if the distinction between `chain_id = 0` and `chain_id = nil` is even necessary. There was a proposal to ban `chain_id = 0` in [EIP-3788: Strict enforcement of chainId](https://eips.ethereum.org/EIPS/eip-3788), but that one was also trying to ban `chain_id = 0` outside the scope of `LegacyTransaction` (where the ambiguity does not arise). For now, EIP-6404 assumes that the distinction is necessary.

---

**etan-status** (2023-02-08):

Done:

- Withdrawals: EIP-6465: SSZ withdrawals root
- Receipts: EIP-6466: SSZ receipts root

For receipts, there is a dependency on EIP-6404 through the `TransactionType`.

Withdrawals are clean.

---

**etan-status** (2023-02-08):

Ended up moving the `transaction_hash` to the top layer of the `transactions` tree.

Rationale for removing from `receipts` tree is so that devp2p `GetReceipts` response can still be verified against a block header, without requiring access to historic transactions (and their hashes). Geth syncs receipts and transactions concurrently, so may have such a design. Nethermind syncs transactions before receipts. Erigon does not sync receipts but instead computes them locally from transactions.

Rationale for `transactions` tree is so that `eth_getBlockByNumber` with `includeTransactions = False`:

- can still be answered in relatively compact format in a verifiable way. Response would include all the perpetual TX hashes, as well as the hash_tree_root’s according to the block’s spec fork. HTR is needed to verify overall transactions_root.
- can still be answered by a consensus layer (CL does not store receipts, so would otherwise not have the TX hashes available).

The light client wallet use case is still supported, like this:

1. Wallet prepares TX: any tx type, compute sighash, sign it, broadcast, as usual (no changes)
2. Wallet computes perpetual TX hash according to tx type (no changes)
3. Wallet now queries JSON-RPC for tx inclusion proof by perpetual TX hash
4. Once included in a block, proof contains: (1) sequential TX index within block, (2) proof of TX hash being at said index in transactions tree, (3) status code from receipts tree at same index, (4) proof that status code in receipts tree is correct.

---

**etan-status** (2023-02-09):

Have split SSZ discussion to [EIP-6475: SSZ Optional](https://eips.ethereum.org/EIPS/eip-6475)

---

**etan-status** (2023-02-09):

Bumped to remove the `tx_subtype` and replace it with `CHAIN_ID_LEGACY` that is not supported in EIP-155.

---

**etan-status** (2023-02-15):

Bumped to use an opaque representation for transaction signatures, added rationale and updated [comparison picture](https://github.com/ethereum/pm/files/10743139/SSZTX.pdf) to [union based approach](https://notes.ethereum.org/@vbuterin/transaction_ssz_refactoring).

---

**etan-status** (2023-02-19):

- Updated to also include commitments to transaction signer, and to the address of newly deployed contracts, in the SSZ tree, to cover remaining JSON-RPC API use cases.
- Pushed chain_id into the first layer of the transactions_root tree, as it becomes an ExecutionPayload property after transactions have been bundled.
- Optimized SSZ tree to have shorter proofs for common use cases, added illustration
- Optimized SSZ tree to have more compact encoding for non-blob transactions
- Refactored EIP to have clear sections introducing each helper function
- Updated rationale

I’m still working on benchmarks, as discussed in the last SSZ breakout call.

---

**etan-status** (2023-02-28):

Updated [EIP-6404](https://eips.ethereum.org/EIPS/eip-6404) with metrics, comparing to the [union based approach](https://notes.ethereum.org/@vbuterin/transaction_ssz_refactoring).

Personal conclusion:

SSZ Union’s primary advantage is that inside the consensus `ExecutionPayload`, it needs about ~50 bytes less compared to the normalized transaction. At the typical 200 transactions per block, that’s a difference of about ~10 KB per block.

Furthermore, `engine_getPayload` / `engine_newPayload` don’t require conversion in case of the SSZ Union, for SSZ transactions. However, this API is used via JSON, so already goes through a double conversion process, and is sometimes used remotely. So the performance argument here is moot.

Finally, arguments can be made regarding a different design space for future transaction types. However, note that all transactions are also exposed via JSON-RPC, where they are represented in a normalized way. Therefore, any restrictions that a normalized transaction representation brings, already apply, even if the transactions are represented in an SSZ Union format.

The SSZ Union has some noteworthy flaws when representing non-SSZ transactions:

1. It is impossible to recover a non-SSZ transaction’s from address without downloading the full transaction. In my tests, an incorrect value is recovered to simulate behaviour as if all transactions were SSZ.
2. It is also impossible to determine the address of a newly deployed contract for a non-SSZ transaction without downloading the full transaction, as that depends on the from address.
3. The txid of a non-SSZ transaction is computed differently than it originally had. This means that a transaction-in-a-bottle with a precomputed txid can no longer be identified through that txid, and tooling needs to change.
4. Non-SSZ transaction restrictions also apply, if we ever want to change the hashing algorithm, to, say, Poseidon. The SSZ Union approach closely links the original transaction representation with the way how it is represented in the transactions_root tree. If there is a Poseidon transaction, it has the same issue as RLP transactions if the tree stays SSZ. If the tree changes to Poseidon as well, all existing SSZ transactions will have the same problem.

Besides those flaws, the SSZ Union also is less friendly for consumption by light clients.

- Most SSZ union proofs are bigger than their normalized transaction counterpart, despite the union including less information. The exception is a proof that simply looks up the index of a transaction inside a block by its original transaction hash, but that size benefit comes at a cost that the lookup simply doesn’t work for non-SSZ transactions.
- The proof complexity is higher for SSZ union proofs, due to each transaction type needing a separate path in the logic and the basic information about the sender of a transaction requiring secp256k1 public key recovery. Adding new transaction types gradually raises verifier complexity. As for execution speed, they are mostly slower to verify, with the exception once more being the lookup of sequential index inside a block by original hash, which is incorrect for non-SSZ transactions in SSZ union case.
- JSON-RPC lookups on execution clients might be slower with the SSZ Union, because the JSON-RPC API provides access to a transaction’s from field, which in turn requires secp256k1 public key recovery. All required data to answer a JSON-RPC lookup is readily available in the normalized transaction format without any expensive computation.

Note that, once more, [EIP-6404](https://eips.ethereum.org/EIPS/eip-6404) is *only* about normalizing the transaction representation after inclusion into the consensus `ExecutionPayload`.

For the mempool representation of transactions, they can continue to use whatever signature scheme, hashing method, combination of fields and blob specific network wrappers, as they currently do. [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493) proposes a signature scheme that SSZ transactions should use as part of the mempool, that is both compatible with the SSZ Union as well as the normalized representation for EIP-6404.

---

**etan-status** (2023-08-30):

Updated to use [EIP-6493](https://eips.ethereum.org/EIPS/eip-6493) `SignedTransaction`.

This addresses design space concerns while retaining the merkleization benefits of common fields sharing the same generalized index.

---

**etan-status** (2024-10-02):

Updated for EIP-7702:

- SSZ_TX_TYPE is now 0x1f
- from field in signature will be moved to the receipt
- authorities will be added to the receipt (for successful authorizations)
- signature stablecontainer capacity is now 8 (was 16)
- y_parity capacity is now uint8 instead of 0/1 bool, to support 7702

---

**jochem-brouwer** (2025-05-17):

Hi there, I see `chainId` is typed as `uint64`. The chain id is not limited by EIP-155, but there are proposals like [EIP-2294: Explicit bound to Chain ID size](https://eips.ethereum.org/EIPS/eip-2294) to limit this. Maybe something to consider or to add the motivation for the `uint64` limit. Geth internally has `uint64` also as limit [go-ethereum/core/types/transaction.go at c8be0f9a74fdabe5f82fa5b647e9973c9c3567ef · ethereum/go-ethereum · GitHub](https://github.com/ethereum/go-ethereum/blob/c8be0f9a74fdabe5f82fa5b647e9973c9c3567ef/core/types/transaction.go#L238)

I noticed some things in the EIP which are not up-to-date with latest changes I think (especially 7702) will open a PR for that ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

The gas and fees field in the `TransactionPayload` is now defined as:

```python
    max_fees_per_gas: Optional[FeesPerGas]
    gas: Optional[GasAmount]
```

The Profile of `FeesPerGas` is

```python
class FeesPerGas(StableContainer[MAX_FEES_PER_GAS_FIELDS]):
    regular: Optional[FeePerGas]

    # EIP-4844
    blob: Optional[FeePerGas]
```

I think it is somewhat likely that we will see multi-dimensional gas at some point. Would it be an idea to go ahead here and to also create a `GasAmounts` profile? (If blobs had a “blobGas” field besides blob fees that would thus be added there)

I also see that there is a field in the payload `max_priority_fees_per_gas` and `max_fees_per_gas`, I wonder if priority fees cannot be fit inside `FeesPerGas`? Blob gas fee could already be seen as a new dimension, and priority fee could also be somewhat seen as a fee in a new dimension (some subset or splitting up of the legacy/access list `gasPrice`).

Because now this check is necessary in blob:

```python
        if (tx.payload.max_priority_fees_per_gas or FeesPerGas()).blob != 0:
            raise Exception(f'Unsupported blob priority fee in Blob RLP transaction: {tx}')
```

To ensure that the blob is not redefined in the priority fees (but then it could also be typed as `BasicFeesPerGas` ![:thinking:](https://ethereum-magicians.org/images/emoji/twitter/thinking.png?v=12) ).

How about this:

```python
class FeesPerGas(StableContainer[MAX_FEES_PER_GAS_FIELDS]):
    regular: Optional[FeePerGas]

    # EIP-1559
    priority: Optional[FeePerGas]

    # EIP-4844
    blob: Optional[FeePerGas]

(...)

class BasicFeesPerGas(Profile[FeesPerGas]):
    regular: FeePerGas

class FeeMarketFeesPerGas(Profile[FeesPerGas]):
    regular: FeePerGas
    priority: FeePerGas

class BlobFeesPerGas(Profile[FeesPerGas]):
    regular: FeePerGas
    priorit: FeePerGas
    blob: FeePerGas
```

PR with corrections/suggestions: [Update EIP-6404: Add some suggestions or corrections by jochem-brouwer · Pull Request #9788 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9788)

Would love a review ![:smile:](https://ethereum-magicians.org/images/emoji/twitter/smile.png?v=12) ![:+1:](https://ethereum-magicians.org/images/emoji/twitter/+1.png?v=12)

---

**etan-status** (2025-05-21):

Thanks for the PR! Appreciate the feedback.

Regarding the blob priority fee: The idea is indeed to integrate the EIP-7706 multidimensional fee concept into the SSZ package (EIP-7919 for full scope), so that the fee profiles can be extended for future fee types, rather than having tons of different fee fields like in RLP.

The `RlpBlobTransactionPayload` is converted from the RLP transaction and imported as having a 0 blob prio fee, and there is a check to only allow 0 initially. That makes the handling of various kinds of fees the same, and future-proofs for additional fees such as calldata fees.

See discussion in EIP-7706:



    ![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/etan-status/48/7861_2.png)
    [EIP-7706: Create a separate basefee and gaslimit for calldata](https://ethereum-magicians.org/t/eip-7706-create-a-separate-basefee-and-gaslimit-for-calldata/19998/10) [EIPs](/c/eips/5)



> I think there’s no downside to this, in EIP-6493. It makes the design cleaner and more extensible / future-proof.
> Have updated SSZ Transaction accordingly, and also the viewer on https://eth-light.xyz now shows vector fees.
>
> Example: Ethereum Light
>
> If the blob tips are a problem, can force them to 0 initially and add support for non-0 values lateron.

---

As for the ChainID change for EIP-7702:

In RLP, 0 is used as a special value for chain-agnostic authorizations. With SSZ, it becomes possible to express the concept of not being locked to a specific chain ID explicitly. RLP authorizations with chain ID 0 would convert to a `RlpSetCodeAuthorizationPayload` without a chain ID.


*(5 more replies not shown)*
