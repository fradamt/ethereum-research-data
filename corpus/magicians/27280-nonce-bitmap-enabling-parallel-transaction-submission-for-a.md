---
source: magicians
topic_id: 27280
title: Nonce Bitmap - Enabling Parallel Transaction Submission for a Parallel Blockchain
author: thnhnv
date: "2025-12-22"
category: Web > User Experience
tags: [evm, wallet, execution, nonce]
url: https://ethereum-magicians.org/t/nonce-bitmap-enabling-parallel-transaction-submission-for-a-parallel-blockchain/27280
views: 57
likes: 0
posts_count: 2
---

# Nonce Bitmap - Enabling Parallel Transaction Submission for a Parallel Blockchain

*Summarized for the discussion here: [Nonce Bitmap - Enabling Parallel Transaction Submission for a Parallel Blockchain - UI/UX - Ethereum Research](https://ethresear.ch/t/nonce-bitmap-enabling-parallel-transaction-submission-for-a-parallel-blockchain/23345)*

# TL;DR

Imagine you’re a trader with multiple time-sensitive opportunities. You spot three arbitrage opportunities simultaneously, but you can only submit transactions one at a time. By the time your third transaction is processed, the opportunity is gone. This is the sequentiality problem. We propose a novel solution, Nonce Bitmap, for enabling parallel transaction submission in blockchain systems while maintaining security and compatibility with existing wallets.

- Underutilized Nonce Space. The existing 64-bit nonce space is underutilized, and will never be used up. We can leverage this underutilization to exchange for some degree of parallelism.
- Parallelism. Nonce Bitmap introduces a bitmap-based approach that allows users to send up to 256 transactions in parallel by utilizing the underused bits in the traditional nonce field.
- Minimal Storage Overhead. Nonce Bitmap requires minimal storage overhead (32 bytes per address) compared to alternative approaches.
- Backward Compatibility. Legacy wallets and regular users experience no change in behavior.
- Replay Protection. Nonce Bitmap preserves security guarantees against replay attacks while eliminating sequential bottlenecks.
- Better UX/DX. Nonce Bitmap is particularly valuable for high-frequency users like traders, MEV searchers, and protocols that need concurrent transaction submissions.

# Traditional Nonce Mechanics

In a traditional blockchain like Ethereum, transactions from a single account must be executed in a strict, incremental order (Nonce 1, then 2, then 3). This prevents users from sending many independent transactions at once. The **Nonce Bitmap** proposal solves this by allowing a range of nonces to be valid simultaneously.

# Core Concepts of Nonce Bitmap

[![Nonce Bitmap Design](https://ethereum-magicians.org/uploads/default/optimized/3X/2/e/2ec44e247e0f0e7c4539550453a492e738ec9916_2_459x500.png)Nonce Bitmap Design1300×1416 150 KB](https://ethereum-magicians.org/uploads/default/2ec44e247e0f0e7c4539550453a492e738ec9916)

Our solution extends the standard account state to combine the traditional nonce with a `Bitmap` field to track nonce usage. For each `Nonce` value, we allow up to 256 transactions with different `Index` ’s. The `Bitmap` field is a 256-bit field where each bit represents one of 256 available slots (each slot is corresponding to an `Index`) for parallel transactions at the current `Nonce`. If a transaction modifies the `Nonce`, the `Bitmap` field is set to cleared and set to the bit at the `Index` position is set to 1.

## The Bitmap Structure

Instead of storing just one number, the account state stores a **32-byte (256-bit) bitmap**. Each bit represents whether a specific transaction index has been used.

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

Specifically, `Nonce` is still strictly increasing, same as the traditional implementation. However, the first 8 bits of `Nonce` are always 0s. We observe that the current `Nonce` value is 64-bit, which we expect an account will never use up. This is because a 64-bit nonce value can take up to `2^64 = 18446744073709551616` values, and if an account sends 1B transactions a day, it will take that account 50M+ years to use all the nonces. Therefore, we consider a 56-bit space is sufficiently enough for an account (`2^56 = 72057594037927936` values).

Each bit of the `Bitmap` indicates whether the index at that bit is already used or not. For example, if the bitmap at index 10 is set to 1, this means that the index 10 has been used for the current `Nonce`. The 256-bit `Bitmap` field allows an account to send up to 256 transactions at a time, in any orders (no need for strict ordering). By using `Bitmap`, it is very efficient to check if an index is used or not. Furthermore, this approach only requires one additional bit per parallel transaction.

## Nonce Composition

The traditional 64-bit nonce field is split into two fields:

```go
func ExtractNonce(nonce uint64) (index uint8, actualNonce uint64) {
    index = uint8(nonce >> 56)               // Extract first 8 bits (most significant bits)
    actualNonce = nonce & 0x00FFFFFFFFFFFFFF // Mask lower 56 bits
    return
}
```

- The first 8 bits of the Nonce are used as the Index.
- The last 56 bits are used as the actual nonce value. As we analyzed above, a 56-bit nonce space is sufficiently enough for any account.

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

[![Parallel transaction enabled by Nonce Bitmap](https://ethereum-magicians.org/uploads/default/optimized/3X/3/7/379dbdb19e96e054045a128fd838467a37909297_2_316x500.png)Parallel transaction enabled by Nonce Bitmap878×1388 146 KB](https://ethereum-magicians.org/uploads/default/379dbdb19e96e054045a128fd838467a37909297)

However, when the user attempts to submit another transaction (TxC) trying to reuse the already occupied `Index` 2, the validator correctly rejects it as a duplicate. The system then advances when the user submits TxD with `Nonce` 6, which triggers a nonce update: the current `Nonce` increments to 6 and the `Bitmap` is updated following the TxD’s `Index`. This nonce increment is crucial because when the user tries to submit TxE with the now-stale `Nonce` 5, the validator rejects it because the system has moved forward, preventing any replay of old transactions.

# Analysis & Considerations

- Simplicity. The design is quite simple to implement. At its core, the system operates on an intuitive principle: maintain a sequential Nonce for regular users while using a Bitmap to track parallel operations within each step.
- Efficiency and Performance. The Bitmap approach achieves 64x reduction in storage overhead (on the same degree of parallelism) compared the 2D nonce management used in Account Abstraction. This efficiency enables a great deal of parallelism (though not unlimited) while maintaining minimal state expansion (one bit per transaction).
- Backward-Compatibility. For the vast majority of users and applications, the system requires zero changes. Legacy wallets continue operating unchanged because their transactions automatically use Index zero within the Bitmap structure.

# Who Benefits from Nonce Bitmap?

- High-Frequency Traders. Submit multiple trades simultaneously without complex nonce management. Reduce latency by eliminating the need to query nonce state between transactions.
- MEV Searchers. Send bundles of transactions that can be processed in parallel, improving execution speed and success rates.
- DeFi Advanced Users/Whales. Execute complex strategies involving multiple protocols simultaneously without worrying about transaction ordering or stuck transactions.
- Developers. Build applications that can submit batches of transactions more efficiently, improving user experience and reducing operational complexity.
- Regular Users. Experience no change, the system remains backward compatible with existing wallets.

# Conclusion

The Nonce Bitmap approach demonstrates that thoughtful protocol design can enable

significant UX improvements without compromising security or compatibility. By observing that the 64-bit nonce space is vastly underutilized, we unlock 256-way parallelism with just 32 additional bytes per account.

For low-latency chains, transaction latency is no longer limited by blocktime - it is rather limited by how fast users can submit transactions. Fortunately, Nonce Bitmap removes this bottleneck.

## Replies

**Helkomine** (2026-01-04):

I think this problem can be solved simply by using a separate contract containing the traded asset and using multiple different wallets to interact with them. This is also a common practice among arbitrage bots running parallel arbitrage on Ethereum. Therefore, we don’t need to compromise the network’s risk by adding something that already has a solution.

