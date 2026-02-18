---
source: ethresearch
topic_id: 23095
title: BALs for Proposer Commitments
author: jvranek
date: "2025-09-24"
category: Execution Layer Research
tags: [stateless, preconfirmations]
url: https://ethresear.ch/t/bals-for-proposer-commitments/23095
views: 390
likes: 7
posts_count: 3
---

# BALs for Proposer Commitments

*Thanks to* [Toni](https://x.com/nero_eth) *and* [Ladislaus](https://x.com/ladislaus0x) *for discussion and feedback.*

[EIP-7928](https://eips.ethereum.org/EIPS/eip-7928) introduces Block-Level Access Lists (BALs) to improve parallel execution on L1. Beyond scaling, BALs also unlock a simpler foundation for proposer commitment protocols, especially *execution preconfs*. Instead of relying on fragmented proofs across multiple Merkle Patricia Tries, BALs provide a canonical record of all post-transaction values that commitments can be tied to.

That said, the current EIP-7928 spec isn’t directly amenable to *efficient* EVM-level proofs. This post aims to motivate using BALs for preconfs, highlights proposed spec changes to make them proof-friendly, and outlines the complexity trade-offs under [discussion in Discord](https://discord.com/channels/595666850260713488/1415588655572979773/1415588658731421747).

### Motivation

Execution preconfs let proposers (or delegates) give users early commitments about transaction outcomes before they land on-chain. This reduces preconfirmation time to just a single “ping” from the preconfer to the user, providing a UX that is faster than what a consensus protocol can achieve. Instead of waiting for block confirmations, users can act confidently the moment they receive a *credible* execution preconf.

Today, credible commitments require being able to trustlessly prove when a commitment has been broken to enforce on-chain slashing conditions against bonded preconfers (e.g., using the [URC](https://github.com/eth-fabric/urc)). These proofs are scattered across multiple tries: the transaction trie for inclusion/ordering, the receipt trie for execution success, account trie for nonce or balance changes, and the state trie for storage. This works, but suffers from fragmentation, requires bespoke proving logic, and is limited in granularity.

1. fragmentation: Complete coverage requires committing to values across multiple tries for each piece of modified state.
2. logic: Each commitment makes different promises and affects different state, requiring custom logic.
3. granularity: The tries only record the state after applying all transactions meaning intermediate state updates (e.g., Alice’s balance after the fourth transaction) are not directly provable.

Some proposed designs work around 1) and 3) reverting transactions if the post-state deviates from what the user expected, e.g., [“sell 1000 USDC for at least 0.98 ETH”](https://ethresear.ch/t/a-taxonomy-of-preconfirmation-guarantees-and-their-slashing-conditions-in-rollups/22130). While pragmatic, this shifts the burden onto contract developers, who must encode these conditions manually. In practice, it resembles intent-style programming, where every action carries bespoke validity conditions.

By providing a canonical record of transaction-level state diffs, BALs offer a simpler primitive to build proposer commitments protocols. An execution preconf can be expressed as a commitment to a subset of a BAL, and broken commitments can be proven against the canonical BAL. This makes commitments simpler to reason about, enforce, and standardize, lowering friction for both protocol designers and users. As a result, a single generic proposer commitment protocol that effectively leverages BALs could cover all of today’s preconf use cases.

### BALs Today

A BAL is an RLP-encoded `List[AccountChanges]`, where an `AccountChanges` object records per-transaction state changes to an address’s nonce, balance, storage, and/or code. By iteratively applying all `AccountChanges`, a client can deterministically, and in parallel, reconstruct how every affected account evolved throughout the block.

This is sufficient for addressing our challenges with execution preconfs:

1. fragmentation: Only the BAL is required to make commitments vs multiple tries
2. logic: A single generic protocol is sufficient to capture all of today’s preconf use cases without intent-style programming.
3. granularity: AccountChanges objects allow for commitments to per-transaction state diffs.

### Current Limitation

Clearly BALs stand to improve preconf protocols; however, the challenge lies in how BALs are encoded. Under the current EIP-7928 specs, BALs are RLP-encoded and the block header contains the BAL hash.

This makes it cumbersome to prove to the EVM that a commitment was broken. A user would need to pass the entire BAL as calldata, verify its hash against the parent block hash, and then manually RLP-decode to locate the conflicting value. Currently, an uncompressed BAL is on the order of ~100KB which is within the calldata limit. Given broken commitments *should* be a rare occurrence, this is not unreasonable.

### Proposed EIP Change (harder)

As blocks and BALs grow larger, passing the BAL as calldata will be even more expensive. The proposed change would make it easier to prove BAL membership from the EVM.

Since it is unlikely that execution clients will use SSZ to encode the BAL, an alternative approach is to encode the BAL as its own MPT as proposed by Toni. The block header would contain the BAL root instead of the hash, allowing for efficient MPT proofs against the EIP-2935 parent hash.

An ideal encoding for preconfs would have two levels of tries. The outer trie maps the `bal_index` (aka transaction index) key to a `subTrieRoot` value, where each `bal_index` represents a unique transaction index. The inner `subTrie` contains unique keys covering all of the different account changes:

- RLP(["balance_change", address])
- RLP(["storage_change", address, slot])
- RLP(["nonce_change", address])
- RLP([“code_change”, address])

with values containing the RLP-encoded post-transaction data (i.e., `RLP([uint256])`).

This would allow a preconfer to make succinct commitments about post-transaction state diffs, i.e., a signature over a `subTrieRoot` for a given `bal_index`. Proving that a commitment was broken then reduces to showing that the actual `subTrieRoot` at that `bal_index` differs from the one signed. The individual account changes in the `subTrie` are abstracted away from the commitment protocol.

This is vastly simpler than today’s situation, where a preconfer would need to commit to post-state diffs across multiple tries for every location a transaction touches. Instead, each transaction now collapses into a single, neatly-packaged `subTrieRoot`.

However, this approach requires introducing another trie which increases the EIP’s complexity.

### Proposed EIP Change (easier)

Assuming the block header still commits to the RLP-encoded BAL hash, a slight restructuring of the BAL layout can vastly simplify commitments. This proposal is to index the BAL by `bal_index` rather than accounts, such that the BAL is encoded as an RLP-encoded `List[TransactionDiff]`.

A `TransactionDiff` would contain all nonce, balance, storage, and code changes from the given transaction. This would collapse the commitment from many `AccountChanges` values to one `TransactionDiff`, which functions just like the `subTrieRoot` in the previous proposal.

Succinctly committing to a `TransactionDiff` would make [continuous block building](https://youtu.be/oNLPglf2cQY?si=9R9p-lWaFR-rMuQQ&t=458) more of a reality as wallets and the rest of the PBS pipeline can keep up to date with the latest state after applying execution preconfs.

### Other benefits of BALs

- Major rollups are already experimenting with faster confirmations to improve UX through commitment schemes like shreds, flashblocks, and frags. Today, these rely on third-party implementations and the commitments require fully trusting the sequencer.
 BALs standardize this pattern: rollups that use BALs no longer need to maintain their own custom commitment schemes, and users can more easily benefit from credible commitments. In effect, BALs enshrine what is already starting to happen in practice.
- Vitalik has pointed out that the BAL as an MPT approach allows partial stateless nodes to verify proofs about only the parts of BALs that they care about, i.e., how has my balance changed over the course of the block.
- Execution preconfs are an out-of-protocol precursor to ideas like payload chunking.

## Replies

**Nero_eth** (2025-09-25):

Thanks for this post! Great to have those details as we’re still early enough to incorporate such feedback!

I fully agree with this and would also argue *for* replacing the hash with a root to support the use case you’re describing!

I would lean against changing the structure of the BAL as this was decided based on the size differences. Many transactions touch a overlapping set of accounts and storage keys, thereby it’s more efficient with regards to bandwidth to aggregate by address instead of bal_index. Furthermore, the per-address aggregation is beneficial for low-bandwidth partial stateless nodes in the future who wouldn’t need to download the entire but only a subset of it (with the accounts they care about), together with a merkle proof.

I don’t think this change would be much simpler than introducing a new trie.

Instead of using the subtrie approach we could also do:

Key = `address`, Value = `RLP([<change>, address, slot, post_value])`

This removes the subtrie and makes the proof even simpler.

---

**OnticNexus** (2025-12-05):

I second Nero’s concerns about changing the BAL’s structure. That said, it’s still possible to get a transaction-indexed Merkle root without changing the BAL format. Instead of encoding the BAL as an MPT, define a function F that builds a TX_MPT from the BAL, with the outer trie keyed by tx_index and the inner subtries keyed by account change fields (balance_change, storage_change, etc., as in the “harder” option). TX_MPT can just be thought of as an additional commitment to the BAL, not its canonical encoding. The main question then becomes whether the benefits of TX_MPT outweigh the extra compute cost (which I’d guess is on the order of tens of milliseconds).

You can also build a Merkle root over the existing address-indexed BAL structure (as Nero suggests), but TX_MPT seems like it aligns better with the proposer commitment use case.

