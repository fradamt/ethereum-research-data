---
source: ethresearch
topic_id: 22130
title: A Taxonomy of Preconfirmation Guarantees and Their Slashing Conditions in Rollups
author: Joseph
date: "2025-04-10"
category: Layer 2
tags: [preconfirmations, based-sequencing, slashing-conditions]
url: https://ethresear.ch/t/a-taxonomy-of-preconfirmation-guarantees-and-their-slashing-conditions-in-rollups/22130
views: 513
likes: 13
posts_count: 6
---

# A Taxonomy of Preconfirmation Guarantees and Their Slashing Conditions in Rollups

*Thanks to mteam, Justin Drake, and Jonny Rhea, for feedback and comments on this article. Thanks to Ink L2 for funding my research*

Preconfirmations in optimistic rollups can offer varying levels of guarantees to users, ranging from basic inclusion to strong assurances about ordering and execution outcomes. However, the lack of a formalized taxonomy has led to overlapping and sometimes tautological definitions across discussions. This document proposes a structured categorization of preconfirmation guarantees, with the goal of establishing clear boundaries between each type. It also defines the associated slashing conditions and computational complexities required to enforce them, enabling rollup designs to reason rigorously about safety, UX, and implementation tradeoffs.

There are three essential guarantees to a preconfirmation:

- Inclusion
Enforcing inclusion through a signed message requires the preconfirming sequencer to include the transaction in the specified block.
- Ordering
Enforcing ordering through a signed message requires the preconfirming sequencer to include the transaction at the specified sequence number in the specified block.
- Execution success
Execution success guarantees that the transaction will not revert. If the user wants a specific post-state, they can encode the required conditions into the transaction logic itself, so that any deviation causes reversion. Thus, post-state guarantees can be subsumed into execution success.

---

### Category 0

> Inclusion is guaranteed. No guarantees on ordering or execution success.

This is the weakest of guarantees. The transactor receives a guarantee of inclusion via the preconfirmation response. However, ordering is not guaranteed and the execution outcome is uncertain.

The slashing condition for this category would be a proof of non-inclusion for the transaction in the transaction tree.

However, a proof of non-inclusion for an unordered transaction tree can be computationally complex within the EVM by requiring a proof of exclusion for all transactions within the transaction tree.

#### Example:

**DEX Mempool Inclusion for Limit Orders**

A user submits a limit order to a rollup-based DEX. The sequencer provides a signed guarantee that the transaction will be included in the next block, but the final ordering is not specified. This allows the DEX frontend to show the user that their order will be considered, but without making promises about execution success or outcome (which could be affected by slippage, race conditions, or frontrunning).

---

### Category 1

> Inclusion and ordering are guaranteed. Execution success is not guaranteed.

The slashing condition for this category would be a proof of non-inclusion for the transaction in the transaction tree.

Using a sequence number for a signed sequencer transaction reduces computational complexity by allowing the proof of non-inclusion to be a proof by contradiction by providing the transaction at the specified sequence and accompanying Patricia Merkle Tree (PMT) witness.

#### Example:

**NFT Minting with Priority Slot**

During an NFT drop, users can pay for priority mint slots. The sequencer returns a signed preconfirmation promising that a minting transaction will be included at a specific sequence position. However, if the user has insufficient funds or gas, the transaction might still revert. This ensures fairness in ordering while offloading execution risk to the user.

---

### Category 2

> Inclusion and execution success are guaranteed. No guarantee on ordering.

This category guarantees that the transaction will execute without reversion, but allows the sequencer to reorder it within the block. Specific post-state outcomes are not enforced by the sequencer, but can be encoded by the transactor directly into the transaction logic, turning any unexpected state into a revert. Thus, post-state guarantees are a function of user-defined transaction invariants.

The slashing condition for this category would be identical to category 0. However, the proof of non-reversion will require re-execution of the block within the EVM up until the transaction is executed.

#### Example:

**Slippage-Bounded DEX Trade with MEV Flexibility**

A user submits a trade to a DEX with a specified maximum slippage (e.g., “sell 1000 USDC for at least 0.98 ETH”). The sequencer returns a preconfirmation guaranteeing the transaction will succeed (i.e., not revert), so long as the post-trade price stays within the user’s slippage tolerance. The sequencer is free to reorder this trade relative to others and extract MEV (e.g., by sandwiching) as long as the final execution remains within bounds and succeeds. This gives the user execution confidence without demanding a specific ordering or state root.

---

![:white_check_mark:](https://ethresear.ch/images/emoji/facebook_messenger/white_check_mark.png?v=12) = Guaranteed | ![:x:](https://ethresear.ch/images/emoji/facebook_messenger/x.png?v=12) = Not Guaranteed

| Category | Inclusion | Ordering | Execution success | Slashing Computation |
| --- | --- | --- | --- | --- |
| Category 0 |  |  |  | O(n) |
| Category 1 |  |  |  | O(1) |
| Category 2 |  |  |  | O(n) + O(m) |

* *O(m) implies transaction execution*

---

### Footnote on slashing condition complexity

While the naive approach to verifying slashing conditions (e.g., proving non-inclusion or failed execution) may require O(n) or O(m) operations within the EVM, these costs can be significantly reduced through cryptographic proof systems. If the rollup leverages SNARKs (or similar succinct proofs), the entire slashing verification—regardless of whether it’s checking inclusion or execution success—can be compressed to a constant-time verification cost on-chain, effectively reducing the computational complexity to O(1).

---

### Why collapse post-state guarantees into execution success?

If a user cares about the final state resulting from a transaction, they can encode those expectations as assertions within the transaction itself. If the assertions fail, the transaction reverts, and the sequencer cannot satisfy an execution success guarantee. This makes separate post-state guarantees redundant: execution success already implies that the transaction executed exactly as the user intended.

## Replies

**jrhea** (2025-04-10):

Great post!  Doesn’t a Post-State Guarantee make inclusion and execution success redundant? Also, doesn’t execution success imply inclusion?

Assuming you agree, doesn’t that have implications on the time complexity for slashing? I would think that you just have to compute the highest-level guarantee:

For Cat 3:

•	Exact Post-State → Execution Success → Inclusion

Therefore, you only need to compute Exact Post-State to prove Execution Success and Inclusion

For Cat 2:

•	Execution Success → Inclusion

Therefore, you only need to compute Execution Success to prove inclusion

---

**Joseph** (2025-04-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/jrhea/48/1406_2.png) jrhea:

> Great post! Doesn’t a Post-State Guarantee make inclusion and execution success redundant? Also, doesn’t execution success imply inclusion?
>
>
> Assuming you agree, doesn’t that have implications on the time complexity for slashing? I would think that you just have to compute the most highest-level guarantee:
>
>
> For Cat 3:
> • Exact Post-State → Execution Success → Inclusion
> Therefore, you only need to compute Exact Post-State to prove Execution Success and Inclusion
>
>
> For Cat 2:
> • Execution Success → Inclusion
> Therefore, you only need to compute Execution Success to prove inclusion

I agree based on your feedback (mteam called it out too) I removed the post-state guarantee category because it’s redundant. If a post-state is guaranteed, then execution success and inclusion are already implied. And if you care about the post-state, you can just encode that into the transaction logic so it reverts if the result isn’t what you expect. That means all you really need is an execution success guarantee, which already covers everything.

I think the time complexity will be approximately the same as a slashing proof will require the re-execution of the transaction ahead in the block. It will remove the last step of needing to verify the post state output.

---

**jrhea** (2025-04-10):

Thanks for the clarification, your point about embedding the desired post-state directly into transaction logic is well-taken, especially for simpler scenarios. One benefit of having an explicit Exact Post-State guarantee category is that it supports off-chain verification. For example, consider a solver-based decentralized RFQ system where multiple competing market makers submit off-chain quotes for a trade.  My thinking here was that each quote would result in a different post-state and explicitly encoding all possible acceptable states into the user’s transaction logic would be complex and expensive. I still think it is valuable to have an explicit Exact Post-State guarantee that allows a solver (or market maker) to select the best quote off-chain, promise a specific final state, and then have that state cheaply verified off-chain after execution.

Re: my comment on time complexity for slashing, I see your point. For Category 2, i suppose you still have to perform a non-inclusion proof O(n) and then execute the transaction O(m). The same thing applies for Category 3.

---

**hyeonleee** (2025-04-14):

Nice post. I enjoyed reading it.

---

**jochem-brouwer** (2025-09-11):

![](https://ethresear.ch/user_avatar/ethresear.ch/joseph/48/10926_2.png) Joseph:

> However, the proof of non-reversion will require re-execution of the block within the EVM up until the transaction is executed.

This works, but there is an alternative route (to prove the status of a certain transaction of block `X` at index `Y` within the EVM): if you get the receipt from the transaction, one of the encoded fields is “success” (0 or 1). If the transaction reverted, it is 0. If it succeeded, it is 1. Therefore, to prove that the transaction was reverted in a subsequent block, you have to prove that the status field of that certain transaction was `0` and not `1` (and the transaction is thus the one in question). For this you can use `block.receiptTrie`. It is an MPT (PMT) however, so the actual proof here is rather large, so it is expensive to prove this on-chain.

Or, outside the EVM: one can inspect the receipt to immediately check if it reverted or not ![:smile:](https://ethresear.ch/images/emoji/facebook_messenger/smile.png?v=12) ![:+1:](https://ethresear.ch/images/emoji/facebook_messenger/+1.png?v=12)

