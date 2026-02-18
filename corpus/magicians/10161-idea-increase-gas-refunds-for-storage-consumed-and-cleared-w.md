---
source: magicians
topic_id: 10161
title: "Idea: Increase gas refunds for storage consumed and cleared within a single transaction"
author: jake
date: "2022-07-28"
category: EIPs
tags: [evm, gas]
url: https://ethereum-magicians.org/t/idea-increase-gas-refunds-for-storage-consumed-and-cleared-within-a-single-transaction/10161
views: 1027
likes: 0
posts_count: 2
---

# Idea: Increase gas refunds for storage consumed and cleared within a single transaction

Hi Magicians. I had an idea regarding same-transaction storage consumption, and thought I’d share.

**Summary**:

Increase refunds for clearing storage slots (e.g. with `delete` or zeroing out) using `SSTORE` to be much higher (80%+) if the storage slot was initially expanded earlier in the same transaction.

**Abstract**:

I’m interested in proposing that gas refunds be handled differently for “ephemeral” state that only exists within a single transaction; meaning the storage slot was expanded (initialized) at one point, and then cleared at another point, possibly within the same method call.

A simple example of how this would play out for a single slot:

1. SSTORE changes a storage slot from zero to non-zero (costs 20,000 gas).
2. Method logic, likely operating on that state or sharing it across multiple other methods.
3. SSTORE changes the same storage slot back from non-zero to zero. Currently, this would tack 4,800 gas onto the refund counter. Since the slot was expanded within the same call, however, we could add an additional value SSTORE_EPHEMERAL_RESET_GAS, for example. I imagined this value could be around 10,000 gas, which would bring the refund much higher, closer to the original 15,000 since before EIP-3529.

**Motivation**:

The fact that storage costs for data stored over a short period of time vs. data stored indefinitely both have the same price point strikes me as one of the most latent flaws in the EVM. This topic has been addressed with some potential long-term solutions - such as [storage renting (4445)](https://ethresear.ch/t/a-minimal-state-execution-proposal/4445) - all of which seem to be in various nascent phases of debate/development but are very promising.

However, the solution I’m proposing here isn’t a substitute, nor is it a short-term solution to “stave us over” until we arrive at the “real solution”. As far as I can tell, this improvement proposal would be compatible with any of the storage rental models proposed so far, and in my opinion would compliment those solutions.

This proposal is only concerning storage used within a single transaction; meaning the storage slot was expanded, then deleted before the end of the transaction. There are a number of great use-cases for having extremely affordable state changes within the same transaction. Some examples:

- Enabling usage of data structures restricted for storage use only (like mapping) to have non-prohibitive costs. This would make it much more feasible to perform complex calculations that use scalable data structures (like an unbounded array) strictly for the purposes of the calculation. Additionally, complex data structures, such as a priority queue or a set, could actually be cost-efficient.
- Cheap nonReentrant modifiers!
- Ephemeral state that only exists within the boundaries of a number of delegate calls to other contracts. For example: setting state properties in Contract A before delegate calling Contract B, which may or may not choose to call read methods for those properties in Contract A (like a reverse API, where Contract A’s interface is known). The method that set the original state properties can then delete them at the end of the call, since the data only needed to be provided for the extent of the call.
- As a failsafe for accounting purposes. The state may or may not get erased at the end of the call depending on the actions of delegate called contracts.
- Private methods in the same contract operating on the same piece of state.
- Reverting attempts to change state. For example, updating a certain role or permission set with new information, or expanding a whitelist. If the attempt to do the update fails, storage can be cleared and the reverted call can be far less costly than it would have been otherwise.

**Outstanding Thoughts**:

One thing especially worth noting here is that, while refunds for [storage clearance were originally decreased](https://eips.ethereum.org/EIPS/eip-3529) in part due to the gas token exploits, in this case the increase would not re-open that exploitation vector, since gas tokens required the refund to be claimable at any point in time, and this increase in refunds only applies within the same transaction.

Additionally, initial expansion costs would still apply. Meaning that, under this proposal, it would still be required that the gas limit be high enough to cover the expansion costs, but the overall cost to the caller once the transaction has been included would be much lower. This prevents anyone from exploiting ‘cheap storage’ and expanding carelessly or maliciously within a single call.

Finally, worth noting that I’m not proposing any changes to the `MAX_REFUND_QUOTIENT`. **The max refund limit would, of course, stay same.** So there wouldn’t be any increase in the maximum block size variance under this proposal.

Looking forward to any and all thoughts and feedback. Further discussion would be needed to ensure backwards compatibility is 100% viable and there are no ill effects on storage clearing incentives.

## Replies

**Chipe1** (2025-08-12):

Looks like [EIP-2200](https://eips.ethereum.org/EIPS/eip-2200#specification) covers this

