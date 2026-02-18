---
source: ethresearch
topic_id: 23345
title: Nonce Bitmap - Enabling Parallel Transaction Submission for a Parallel Blockchain
author: 14mp4rd
date: "2025-10-24"
category: UI/UX
tags: [parallelization]
url: https://ethresear.ch/t/nonce-bitmap-enabling-parallel-transaction-submission-for-a-parallel-blockchain/23345
views: 490
likes: 0
posts_count: 5
---

# Nonce Bitmap - Enabling Parallel Transaction Submission for a Parallel Blockchain

# TL;DR

Imagine you’re a trader with multiple time-sensitive opportunities. You spot three arbitrage opportunities simultaneously, but you can only submit transactions one at a time. By the time your third transaction is processed, the opportunity is gone. This is the sequentiality problem. We propose a novel solution, Nonce Bitmap, for enabling parallel transaction submission in blockchain systems while maintaining security and compatibility with existing wallets.

- Parallelism. Nonce Bitmap introduces a bitmap-based approach that allows users to send up to 256 transactions in parallel by utilizing the underused bits in the traditional nonce field.
- Minimal Storage Overhead. Nonce Bitmap requires minimal storage overhead (32 bytes per address) compared to alternative approaches.
- Backward Compatibility. Legacy wallets and regular users experience no change in behavior.
- Replay Protection. Nonce Bitmap preserves security guarantees against replay attacks while eliminating sequential bottlenecks.
- Better UX/DX. Nonce Bitmap is particularly valuable for high-frequency users like traders, MEV searchers, and protocols that need concurrent transaction submissions.

# Traditional Nonce Mechanics

## The EVM Nonce: More Than Just a Counter

At its core, nonces are associated with each Externally Owned Account (EOA) to represent the number of transactions that have been sent from that account. Each StateAccount maintains a nonce field of up to 8 bytes.

```go
// StateAccount is the Ethereum consensus representation of accounts.
// These objects are stored in the main account trie.
type StateAccount struct {
	Nonce    uint64
	Balance  *uint256.Int
	Root     common.Hash // merkle root of the storage trie
	CodeHash []byte
}
```

For a new account, the nonce starts at zero and is incremented by one each time a transaction originating from that account is included in a block. While seemingly simple, this counter serves critical functions essential for the integrity and deterministic operation of the EVM.

- Security. The nonce is used to prevent replaying attacks by requiring each transaction originating from an address must use a unique nonce. Consequently, any attempt to re-submit the same transaction twice will fail because the network has acknowledged the use of this nonce. This security guarantee is fundamental to the safety of user assets and interactions on the blockchain.
- Ordering. Nonces in Ethereum are strictly increasing. That is, each transaction must have a nonce by one greater than the previous transaction’s nonce by one.

```go
next := opts.State.GetNonce(from)
if next > tx.Nonce() {
	return fmt.Errorf("%w: next nonce %v, tx nonce %v", core.ErrNonceTooLow, next, tx.Nonce())
}
// Ensure the transaction doesn't produce a nonce gap in pools that do not
// support arbitrary orderings
if opts.FirstNonceGap != nil {
	if gap := opts.FirstNonceGap(from); gap  Nonce. A scalar value equal to the number of transactions sent from this address or, in the case of accounts with associated code, the number of contract-creations made by this account.

 With the current design, transaction counting (eth_getTransactionCount) for a given address is done by simply returning the current account’s nonce.

```go
// GetTransactionCount returns the number of transactions the given address has sent for the given block number
func (s *TransactionAPI) GetTransactionCount(ctx context.Context, address common.Address, blockNrOrHash rpc.BlockNumberOrHash) (*hexutil.Uint64, error) {
	// Ask transaction pool for the nonce which includes pending transactions
	if blockNr, ok := blockNrOrHash.Number(); ok && blockNr == rpc.PendingBlockNumber {
		nonce, err := s.b.GetPoolNonce(ctx, address)
		if err != nil {
			return nil, err
		}
		return (*hexutil.Uint64)(&nonce), nil
	}
	// Resolve block number and use its state to ask for the nonce
	state, _, err := s.b.StateAndHeaderByNumberOrHash(ctx, blockNrOrHash)
	if state == nil || err != nil {
		return nil, err
	}
	nonce := state.GetNonce(address)
	return (*hexutil.Uint64)(&nonce), state.Error()
}
```

Overall, this design offers a simple yet effective way to address replay attacks, enabling efficient transaction validation and reduce storage footprints.

## Sequentiality Bottlenecks

The current nonce design creates an unavoidable sequentiality at the account level. That is, even when transactions n+1 and n are unrelated (and could be executed in parallel), the transaction n+1 must still have to wait for the transaction n because transactions of the same sender are processed by the order of nonces.

Stuck transactions are another problem. If a user submits a transaction n with a gas price that is too low to be included in blocks, this transaction remains pending in the mempool until it is included, discarded or replaced. During this period, any attempt to submit subsequent transactions from this user will fail, regardless of gas prices. This is unwanted and it creates a bad experience for users.

- For example, a user might have a pending ETH transfer transaction with a relatively low fee but then urgently need to close a soon-to-be-liquidated DeFi position. With the current nonce design, he must wait for the stuck transaction or have to replace the stuck transaction by another transaction using the same nonce with higher gas price. Either way, this adds a lot of complexity that regular users might not be able to handle.

Besides, advanced users (e.g, HFT traders) often need to send transactions in parallel. In order to do this, they often have to carefully manage nonces off-chain. However, this is not always [an easy task at all](https://github.com/ethers-io/ethers.js/issues/972). Even with off-chain management, one must query either 1) the current nonce or 2) the receipt of the previous transaction in order to choose to submit the current transaction. In the case where latency is crucial, this query also incurs some delays. Especially in a blockchain like RISE, MegaETH, Monad, Flashblocks, where transaction processing is extremely fast ([<10ms shred time](https://blog.risechain.com/rise-testnet-is-live/)), querying on-chain data might result in tens to hundreds of mili-second delays.

Worse yet, attempting to send multiple transactions in parallel (even with different nonces) can result in invalid nonce gap errors. This happens because the current P2P propagation does not guarantee that a transaction with nonce n will land in the mempool of a node before the transaction n+1.

These limitations become particularly acute on low-latency chains.

Let’s explore how other systems have attempted to solve this problem.

# Breaking Sequentiality

High-performance chains can handle tens of thousands TPS with a very low latency. However, its utilization cannot be fully achieved without a better wallet/client UX. These chains are capable of processing many transactions concurrently, but right now, transaction submission is sequential, potentially being a bottleneck to fully unlock their potentials.

In this section, we look at some potential alternative designs to address this sequentiality. These designs mainly focus on the security aspect of nonces in which a nonce is a **number used once** serving as replay attack protection.

We note that while transaction ordering and counting are important, these can be achieve using different approaches. For example, services (typically explorers) that use this `eth_getTransactionCount` can extract this figure by using their local databases.

## Random Nonces

Instead of strictly increasing nonces, this design allows transactions to carry arbitrary unique identifiers, enabling parallel transaction submission and processing. Each account maintains a record of all previously used nonces rather than a single scalar counter. For example, this can be represented as a mapping from addresses to sets of used nonces.

```go
UsedNonces = map[Address]map[uint64]bool
```

When a transaction is submitted, the node validates the nonce by checking whether it has already been used by that account. If the nonce is unused, the transaction is accepted and the nonce is marked as used.

This approach allows processing nodes to execute transactions (if unrelated) from the same user in parallel, significantly improving performance. For the client side, wallets can generate random nonces without needing to track or synchronize nonce counters carefully, facilitating easier parallel transaction submission. An additional RPC, such as `eth_usedNonces`, can be implemented to retrieve used nonces for a given address. Furthermore, the `eth_getTransactionCount` can return the length of the `UsedNonces` for a given address.

However, this approach also introduces non-trivial drawbacks. The most notable one is storage overhead where nodes must store and maintain a potentially large set of used nonces per account, increasing state size and storage complexity. Furthermore, depending on the random nonce generator algorithm, nonce duplications might occur.

## Hyperliquid’s Design

Instead of storing all used nonces for a given address, [Hyperliquid](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) only stores the 100 highest used nonces per address instead, and require additional rule for checking nonce reuse. That is, a new transaction must have a nonce larger than the smallest nonce in this set and has never been used before (i.e, not existing in the set). Furthermore, nonces must be within 1 day of the UNIX milisecond timestamp on the block in which the transaction is included. For example, for a new transaction, a nonce can be set to the current timestamp.

Similar to the random nonce design, Hyperliquid offers a great deal of parallelism. UX has also been improved as wallets are flexible to choose different nonce strategies and parallel transaction submission is also possible. The time-bound validity also reduces the chance of relaying attacks. Compared to the random nonce design, this approach incurs less storage overhead as only 100 used nonces are stored. However, it comes with a bottleneck of not being able to send more than 100 transactions in parallel.

However, as the nonce management is completely different, certain operations might not be backward-compatible with existing wallets. In fact, this nonce design is only used for the HyperCore layer. The HyperEVM layer still uses the traditional nonce design. Besides, the time-bound requirement also limits the duration of scheduled transactions (i.e, pre-signed transactions scheduled to take place in more than one day are not possible).

## 2D Nonces

[RIP-7712](https://github.com/ethereum/RIPs/blob/bd9b89f0b02d26a579ef8972431bc93540314dd4/RIPS/rip-7712.md) introduces a 2-dimensional Nonce mechanism (2D Nonces) for [Account Abstraction](https://ethereum.org/roadmap/account-abstraction/) (AA) transactions. 2D nonces allow smart contract accounts to handle a more flexible and parallelizable nonce system. A 2D nonce is a n-bit (e.g, n=256 in AA) value which is split into two logical components:

```go
┌─────────────────────────────────┬──────────────────────────┐
│         Upper k bits            │    Lower n-k bits        │
│          (Nonce Key)            │   (Nonce Sequence)       │
└─────────────────────────────────┴──────────────────────────┘
```

- nonceKey. nonceKey serves as a nonce category that partitions the nonce space into multiple independent categories.

The classic nonce corresponds to a 1D nonce that is equivalent to having a single nonce category (i.e, nonceKey = 0)

**nonceSequence**. `nonceSequence` is a counter within that category that must increase sequentially for ordering.

Transactions with distinct `nonceKeys` can be executed or included in any order, enabling parallel processing. On the other hand, transactions with the same `nonceKey` must be executed sequentially, with increasing `nonceSequences`.

`nonceKey` determines the degree of parallelism of an account, the larger k, the more transactions that can be sent in parallel. Theoretically, this structure allows an account to maintain up to 2^{k} categories, each capable of holding 2^{n-k} sequential nonces. This means that an account can send up to 2^{k}  transactions at the same time without worrying about nonce ordering.

However, the `nonceKey` is primarily used as an identifier for a group of related transactions (e.g, session keys, time-based). If employed this way, transactions within the same group cannot be parallelized. For example, if `nonceKeys` 1, 2, 3 are used for swaps, ETH transfers and ERC-20 transfers respectively, then an account cannot send two swap transactions, or two ETH transfers or two ERC-20 transfers in parallel. It can only send one swap transaction, one ETH transfer and one ERC-20 transfer at the same time (w.r.t to nonce management). Furthermore, each new `nonceKey` introduces another n-bit storage overhead to store the `nonceKey` and `nonceSequence`.

# Nonce Bitmap Proposal

In this section, we propose a novel nonce management mechanism that allows an account to send up to 256 transactions in parallel, with over one bit storage overhead per parallel transactions. Moreover, the proposal is fully backward-compatible, and introduces no additional fields in the transaction submission process.

## Design

[![Nonce Bitmap Design](https://ethresear.ch/uploads/default/optimized/3X/4/5/4544906ca9b6b61e58e884b1c596030b97ed6f37_2_459x500.png)Nonce Bitmap Design1300×1416 89.8 KB](https://ethresear.ch/uploads/default/4544906ca9b6b61e58e884b1c596030b97ed6f37)

Our solution extends the standard account state to combine the traditional nonce with a `Bitmap` field to track nonce usage. For each `Nonce` value, we allow up to 256 transactions with different `Index` ’s. The `Bitmap` field is a 256-bit field where each bit represents one of 256 available slots (each slot is corresponding to an `Index`) for parallel transactions at the current `Nonce`. If a transaction modifies the `Nonce`, the `Bitmap` field is set to cleared and set to the bit at the `Index` position is set to 1.

```go
// NonceBitmapStateAccount is the Ethereum consensus representation of accounts accommodating with nonce bitmap.
// These objects are stored in the main account trie.
type NonceBitmapStateAccount struct {
	Nonce    uint64 // Anchor nonce: the last finalized sequential checkpoint, always have first 8 bits as 0s.
	Balance  *uint256.Int
	Root     common.Hash // merkle root of the storage trie
	CodeHash []byte

	Bitmap   *uint256.Int // NEW: Tracks used slots for parallel transactions; nil for legacy accounts
}
```

Specifically, `Nonce` is still strictly increasing, same as the traditional implementation. However, the first 8 bits of `Nonce` are always 0s. We observe that the current `Nonce` value is 64-bit, which we expect an account will never use up. This is because a 64-bit nonce value can take up to 2^{64} = 18446744073709551616 values, and if an account sends 1B transactions a day, it will take that account 50+M years to use all the nonces. Therefore, we consider a 56-bit space is sufficiently enough for an account (2^{56} = 72057594037927936 values).

Each bit of the `Bitmap` indicates whether the index at that bit is already used or not. For example, if the bitmap at index 10 is set to 1, this means that the index 10 has been used for the current `Nonce`. The 256-bit `Bitmap` field allows an account to send up to 256 transactions at a time, in any orders (no need for strict ordering). By using `Bitmap`, it is very efficient to check if an index is used or not. Furthermore, this approach only requires one additional bit per parallel transaction.

## Transaction Creation

A key challenge is signaling the chosen parallel slot without breaking existing transaction formats. It is essential that a user can configure an `Index` when creating a new transaction to support sending parallel transactions. One naive approach is to introduce a new 8-bit `Index` variable to existing transaction types. This `Index` field is used to locate the corresponding bit value of the `Bitmap` field in the sender’s account state.

```go
// LegacyTx is the transaction data of the original Ethereum transactions.
type LegacyTx struct {
	Nonce    uint64          // nonce of sender account
	GasPrice *big.Int        // wei per gas
	Gas      uint64          // gas limit
	To       *common.Address `rlp:"nil"` // nil means contract creation
	Value    *big.Int        // wei amount
	Data     []byte          // contract invocation input data
	V, R, S  *big.Int        // signature values

	~~Index    uint8~~           // NEW: The index value for parallelism?
}
```

Fortunately, there is a better way to actually incorporate the `Index` information into a transaction without introducing a new field. We solve this with a bit-packing technique that leverages the vast, underutilized space of the 64-bit `Nonce` field. This is done by **logically** splitting the `Nonce` field (in the transaction) into two different parts, and the extraction is performed with simple bitwise operations:

```go
func ExtractNonce(nonce uint64) (index uint8, actualNonce uint64) {
    index = uint8(nonce >> 56)               // Extract first 8 bits (most significant bits)
    actualNonce = nonce & 0x00FFFFFFFFFFFFFF // Mask lower 56 bits
    return
}
```

- The first 8 bits of the Nonce are used as the Index.
- The last 56 bits are used as the actual nonce value. As we analyzed above, a 56-bit nonce space is sufficiently enough for any account.

For regular users, the first 8 bits are always 0s. The `actualNonce` is the familiar sequential nonce. The entire system appears unchanged from their perspective. For advanced users, they can set the first 8 bits to any values, in any order. This results in the fact that advanced users can send up to 256 transactions in parallel.

## Nonce Validation

The validation logic is the core of the system, ensuring security and progress. When a new transaction arrives, the following logic is executed (note that we do not take fee-replacement transactions into account here):

```go
func ValidateNonce(account *NonceBitmapStateAccount, txPackedNonce uint64) bool {
    index, actualNonce := ExtractNonce(txPackedNonce)

    if actualNonce == account.Nonce + 1 {
        // --- CASE 1: Advancing the Sequence ---
        // This transaction is the next in the sequential chain.
        // It is valid. This will cause the account's Nonce to increment.
        // The bitmap is reset, as we are moving to a new base state.
        return true
    } else if actualNonce == account.Nonce {
        // --- CASE 2: Parallel Transaction ---
        // This transaction operates at the current account's Nonce.
        // Check if the requested parallel slot is available.
        if account.Bitmap == nil {
            // Bitmap is not initialized; this is the first parallel tx at this nonce.
            return true
        }
        return account.Bitmap.Bit(int(index)) == 0 // True if the slot is free
    } else {
        // --- CASE 3: Invalid Nonce ---
        // actualNonce is either too old (less than account's Nonce) or has a gap.
        // This mirrors the existing Ethereum validation rule.
        return false
    }
}
```

Let’s consider the following transaction sequence. It begins with an account where the current `Nonce` is 5 and the `Bitmap` shows slot 0 is already occupied. The user successfully submits two parallel transactions (TxA and TxB) at `Nonce` 5 using different slots (`Index` 2 and 3), and the validator updates the bitmap to mark these slots as used. TxA has finished during the time the validator processes TxB but it does not create any conflict.

[![Parallel transaction enabled by Nonce Bitmap](https://ethresear.ch/uploads/default/optimized/3X/4/8/48f4dddeec0a7a89e2970a1bbc6dd8dd5dd32ed2_2_316x500.png)Parallel transaction enabled by Nonce Bitmap878×1388 90.6 KB](https://ethresear.ch/uploads/default/48f4dddeec0a7a89e2970a1bbc6dd8dd5dd32ed2)

However, when the user attempts to submit another transaction (TxC) trying to reuse the already occupied `Index` 2, the validator correctly rejects it as a duplicate. The system then advances when the user submits TxD with `Nonce` 6, which triggers a nonce update: the current `Nonce` increments to 6 and the `Bitmap` is updated following the TxD’s `Index`. This nonce increment is crucial because when the user tries to submit TxE with the now-stale `Nonce` 5, the validator rejects it because the system has moved forward, preventing any replay of old transactions.

## Analysis & Considerations

The Nonce Bitmap approach directly addresses the sequentiality problem that plagues high-frequency users while maintaining the security guarantees and backward compatibility essential for EVM blockchain.

### Simplicity

The design is quite simple to implement. At its core, the system operates on an intuitive principle: maintain a sequential `Nonce` for regular users while using a `Bitmap` to track parallel operations within each step. The bit manipulation logic for checking and updating `Bitmap` is computationally simple, using efficient bitwise operations that processors handle natively. The overall complexity remains low compared to the random nonces, Hyperliquid’s approach or the 2D nonce management.

### Efficiency and Performance

The Bitmap approach achieves 64x reduction in storage overhead (on the same degree of parallelism) compared to Hyperliquid’s nonce system or the 2D nonce management used in Account Abstraction. This efficiency enables a great deal of parallelism (though not unlimited) while maintaining minimal state expansion (one bit per transaction). The design cleverly leverages the vast 64-bit nonce space, partitioning it without compromising the sequential progression that ensures security.

### Backward-Compatibility

A critical strength of this approach is its seamless backward compatibility. For the vast majority of users and applications, the system requires zero changes. Legacy wallets continue operating unchanged because their transactions automatically use `Index` zero within the `Bitmap` structure. The system maintains the familiar sequential nonce semantics for existing applications while unlocking parallelism for upgraded wallets. This dual-mode operation ensures a smooth ecosystem transition without requiring coordinated upgrades across all participants.

However, it is worth mentioning that users should not assume that `eth_getTransactionCount` always returns the total transaction for an account. This problem is also found in 2D Nonces or the Hyperliquid’s approach. Note that `eth_getTransactionCount` is mainly used for the `PendingNonceAt` function. With the `PendingNonceAt` being re-engineered, this RPC can be discarded/disable for advanced users. For other services (typically explorers) that use this `eth_getTransactionCount`, they can extract this figure by using their local databases.

## Who Benefits from Nonce Bitmap?

- High-Frequency Traders. Submit multiple trades simultaneously without complex nonce management. Reduce latency by eliminating the need to query nonce state between transactions.
- MEV Searchers. Send bundles of transactions that can be processed in parallel, improving execution speed and success rates.
- DeFi Advanced Users/Whales. Execute complex strategies involving multiple protocols simultaneously without worrying about transaction ordering or stuck transactions.
- Developers. Build applications that can submit batches of transactions more efficiently, improving user experience and reducing operational complexity.
- Regular Users. Experience no change, the system remains backward compatible with existing wallets.

## Comparison with Other Approaches

| Approach | Original | Random | Hyperliquid | 2D Nonce | Nonce Bitmap |
| --- | --- | --- | --- | --- | --- |
| Ordering | Yes | No | Partial | Partial | Partial |
| Validation | Simple | Simple | More complex (incorporated with time-based) | - Same as original approach for regular users- A bit more complicated for advanced users | - Same as original approach for regular users- A bit more complicated for advanced users |
| Parallelism | No | Yes, unlimited | Yes, ~100 transactions | Yes, depending on the size of nonceKey. | Yes, up to 256 transactions |
| Transaction Count | Simple | Simple | Non-trivial | Medium, required API updates | Non-trivial |
| Wallet Compatibility | Yes | No | No | Yes for regular users | Yes for regular users |
| Additional Storage | No | Keep track of all used nonces | 8*100 bytes (Keep track of 100 used nonces per address) | 8 * active nonceKeys | 32 bytes per address |

# Conclusion

The Nonce Bitmap approach demonstrates that thoughtful protocol design can enable

significant UX improvements without compromising security or compatibility. By observing that the 64-bit nonce space is vastly underutilized, we unlock 256-way parallelism with just 32 additional bytes per account.

For low-latency chains, trnasaction latency is no longer limited by blocktime - it is rather limited by how fast users can submit transactions. Fortunately, Nonce Bitmap removes this bottleneck.

## Replies

**gMoney** (2025-10-27):

interesting proposal. few questions:

- does the block validation logic need to be updated too to enforce ordering within the mapping itself?
- re backwards compatibility: can wallets and libraries continue to call eth_getTransactionCount and receive a “valid next nonce“, even if they have previously utilized a nonce bitmap?
- is there any benefit to exposing the bitmap in the evm?

---

**14mp4rd** (2025-10-28):

> does the block validation logic need to be updated too to enforce ordering within the mapping itself?

Yes, block validation must be updated.

> re backwards compatibility: can wallets and libraries continue to call eth_getTransactionCount and receive a “valid next nonce“, even if they have previously utilized a nonce bitmap?

Unfortunately no for users using nonce bitmap. By `backward compatibility`, it means that most of regular users (who only do a few transactions per day) will not be affected by this proposal and can continue using their wallet (e.g, Metamask) without any change. But we expect that wallet will also adopt this proposal to further accelerate UX.

> is there any benefit to exposing the bitmap in the evm?

The main benefit is to improve UX. We’ve seen many EVM blockchains that provide high throughput, low latency ([EIP-7966](https://eips.ethereum.org/EIPS/eip-7966)). However, sending transactions in parallel requires complex nonce management and waiting, which might be inefficient for applications that require high responsiveness.

One of the purposes of 2D Nonce in Account Abstraction is to enable parallel intents (among other purposes). Nonce Bitmap solves this at the protocol level, with very low overhead per parallel transaction.

---

**gMoney** (2025-10-28):

Ok got it, so once an account “upgrades” to using parallel nonces it must continue to do so.

re exposing the bitmap in the EVM, I meant so that applications can use it (similar to 4337s 2D nonces which can be read via the mapping). Is there value in exposing it via opcode or system contract? Potentially for revert protection etc., or kept strictly protocol level?

---

**14mp4rd** (2025-12-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/g/ee59a6/48.png) gMoney:

> Ok got it, so once an account “upgrades” to using parallel nonces it must continue to do so.

Correct!

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/g/ee59a6/48.png) gMoney:

> re exposing the bitmap in the EVM, I meant so that applications can use it (similar to 4337s 2D nonces which can be read via the mapping). Is there value in exposing it via opcode or system contract? Potentially for revert protection etc., or kept strictly protocol level?

The existing nonce is not exposed to applications (there is [EIP-4742](https://ethereum-magicians.org/t/eip-4742-nonce-opcode/8171) but I’m not sure it is implemented any where) so I think NonceBitmap will be the same. Although, if there are real demands, it’s easy to add this opcode.

