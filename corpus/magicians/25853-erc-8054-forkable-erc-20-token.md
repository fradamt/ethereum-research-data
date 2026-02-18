---
source: magicians
topic_id: 25853
title: "ERC-8054: Forkable ERC-20 Token"
author: kevzzsk
date: "2025-10-17"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-8054-forkable-erc-20-token/25853
views: 202
likes: 10
posts_count: 8
---

# ERC-8054: Forkable ERC-20 Token

## Abstract

This standard extends ERC-20 to enable efficient token forking through checkpoint-based balance tracking. A forkable ERC-20 token records balance snapshots at each state change. A forked ERC-20 token inherits all balances from a specific checkpoint in the source token,

allowing instant, gas-free distribution to holders without airdrops or claiming mechanisms.

## Motivation

Current methods for distributing new tokens based on existing ERC-20 token balances are inefficient:

1. Manual airdrops: Taking snapshots and transferring tokens to each holder individually is expensive and gas-intensive.
2. Merkle-based claims: While cheaper for deployers,
this approach requires users to pay gas fees to claim tokens and provides poor UX due to claimer needing to provide proofs.

Both approaches are inefficient as they rely on off-chain data construction outside the protocol’s trust domain, introducing potential inconsistencies and allowing for collusion within the Merkle structure.

This EIP proposes a standard for forkable ERC-20 tokens that:

- Enable zero-gas distribution to token holders
- Eliminate manual claiming processes
- Provide verifiable on-chain balance inheritance
- Maintain full ERC-20 compatibility

By implementing checkpointed balances, tokens can be efficiently forked at any historical point,

with new token balances automatically derived from the source token without any state duplication or expensive operations.

### Use Cases

#### Airdrops

Airdrops are a common use case for forkable tokens. Without forkable ERC-20 tokens, manual snapshotting and merkle root creation are required. Then users must manually claim the new ERC-20 token costing gas borne by the claimer.

With forkable ERC-20 tokens, users do not have to claim the new ERC-20 token. The forked ERC-20 token is automatically transferred (via inheritance) to the users who have positive balance at the fork point.

#### Tokenized Risk and Yield

ERC-4626 is a popular standard for yield-bearing vaults that manage an underlying ERC-20 asset.

Risk and yield are commonly rebased on the same underlying asset,

and this works very well for single-dimensional yield and risk

(Liquid PoS ETH).

However, for multidimensional yield and risk vaults,

the underlying asset may be used for different yield-generating purposes each with their own risk profile.

Forkable ERC-20 tokens allow for tokenization of risk and yield to its immediate beneficiaries.

While this is not a foreign concept in the space,

its implementation has so far been off-chain—with their own trust domain separate from the chain.

#### Token Migration

Protocol upgrades, tokenomics changes, or contract improvements often require migrating to a new token.

Without forkable ERC-20 tokens, migration requires complex processes:

- Taking manual snapshots of all holder balances
- Deploying the new token contract
- Either airdropping to all holders (expensive) or requiring users to manually claim their tokens via merkle proofs
(poor UX)

With forkable ERC-20 tokens, migration becomes seamless:

- The new token is forked from the old token at a specific checkpoint
- All holder balances are automatically inherited from the checkpoint
- Users can immediately interact with the new token without claiming
- No gas costs for holders, no manual snapshot management required

#### Governance Token Derivatives

Create governance tokens or voting power derivatives based on historical token holdings without affecting the original token’s utility or requiring users to lock or migrate their holdings.

#### Rewards and Loyalty Programs

Distribute loyalty or reward tokens proportional to historical holdings or activity,

tracked via checkpoints, without complex off-chain calculation and distribution logic.

For latest specs: [ERC-8054: Forkable ERC-20 Token by kevzzsk · Pull Request #1271 · ethereum/ERCs · GitHub](https://github.com/ethereum/ERCs/pull/1271)

For implementation Reference: [GitHub - ERC-8054/ERC-8054: Forkable ERC-20 Tokens](https://github.com/ERC-8054/ERC-8054)

## Replies

**Ankita.eth** (2025-10-22):

This is a really thoughtful proposal — it clearly addresses one of the long-standing pain points around airdrops and token migrations.

The checkpoint-based approach feels much cleaner than off-chain Merkle snapshots, especially since it keeps distribution verifiable and trustless.

The idea of *forkable ERC-20s* also opens up some interesting design space — not just for airdrops, but for things like governance snapshots, historical reward mechanisms, and yield stratification (similar to ERC-4626 extensions).

A few things I find especially valuable here:

- Zero-gas inheritance for holders — that’s a huge UX win.
- Monotonic nonces instead of block numbers — elegant solution against MEV and reorg risks.
- Backwards compatibility with standard ERC-20 — practical and deployable without ecosystem breakage.

It’ll be interesting to see benchmarks on gas costs per checkpoint vs. the cost savings in forking scenarios.

Overall, this feels like a meaningful step toward making token lifecycle management fully on-chain and user-friendly.

---

**kevzzsk** (2025-10-27):

Thanks so much for the thoughtful feedback! Really appreciate you highlighting those key design wins, especially the zero-gas inheritance and nonce-based approach.

On the gas benchmarks, the overhead differs by implementation but generally you’ll see increased costs for state-altering operations (like transfers) in source tokens. This is mainly due to checkpointing requiring additional SSTORE operations that update zero → non-zero storage slots.

For forked tokens, only the first transfer per account incurs a slightly higher overhead (since it needs to reference the source token balance). After that initial state changes, subsequent transfers are comparable to standard ERC-20 tokens, especially for implementations that don’t support recursive forking.

That said, I believe the trade-off becomes highly favorable once you’re distributing to even a modest number of holders. The upfront checkpoint cost is amortized across what would otherwise be expensive airdrop or claim operations.

Happy to share more detailed benchmarks as we gather feedback. Thanks again for engaging with the proposal!

---

**Ankita.eth** (2025-11-05):

Thanks for the detailed breakdown that makes sense. Looking forward to seeing the benchmarks as they come in!

---

**SamWilsn** (2026-01-15):

> Querying a future checkpoint MUST return the latest known value.

Why? For past/present checkpoints, the return value of a checkpoint-aware function will always be the same. If future checkpoints reverted instead of returning current, then checkpoint-aware functions will be “pure” in the programming sense (not the solidity one). I can imagine that would be nice for caching, at the very least.

Either way, this is probably worth discussing in your Rationale section.

---

**frangio** (2026-01-16):

This sounds like ERC20Snapshot.



      [github.com/OpenZeppelin/openzeppelin-contracts](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.6/contracts/token/ERC20/extensions/ERC20Snapshot.sol)





####

  [v4.9.6](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.6/contracts/token/ERC20/extensions/ERC20Snapshot.sol)



```sol
// SPDX-License-Identifier: MIT
// OpenZeppelin Contracts (last updated v4.9.0) (token/ERC20/extensions/ERC20Snapshot.sol)

pragma solidity ^0.8.0;

import "../ERC20.sol";
import "../../../utils/Arrays.sol";
import "../../../utils/Counters.sol";

/**
 * @dev This contract extends an ERC20 token with a snapshot mechanism. When a snapshot is created, the balances and
 * total supply at the time are recorded for later access.
 *
 * This can be used to safely create mechanisms based on token balances such as trustless dividends or weighted voting.
 * In naive implementations it's possible to perform a "double spend" attack by reusing the same balance from different
 * accounts. By using snapshots to calculate dividends or voting power, those attacks no longer apply. It can also be
 * used to create an efficient ERC20 forking mechanism.
 *
 * Snapshots are created by the internal {_snapshot} function, which will emit the {Snapshot} event and return a
 * snapshot id. To get the total supply at the time of a snapshot, call the function {totalSupplyAt} with the snapshot
```

  This file has been truncated. [show original](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v4.9.6/contracts/token/ERC20/extensions/ERC20Snapshot.sol)

---

**kevzzsk** (2026-01-22):

Thank you for raising this point. We had originally specified that querying a future checkpoint should return the latest known value. Since checkpoint nonces are not easily predicted by callers, we included this as a convenience and a much more forgiving API to provide graceful degradation for cases where a caller might inadvertently query a checkpoint that does not yet exist or querying N+1 cases.

However, your point about function purity makes much more sense. Reverting on future checkpoints ensures that checkpoint-aware functions remain deterministic. This deterministic behaviour plays much more nicely to consumers that expect only the true value at that checkpoint.

We will update the specification to require that querying a future checkpoint MUST revert, and will include this discussion in the Rationale section. Thank you for the feedback.

---

**kevzzsk** (2026-01-22):

Thank you for pointing this out. `ERC-8054` does share conceptual similarities with OZ’s `ERC20Snapshot`.

However, `ERC-8054` differs in its purpose and design.

`ERC20Snapshot` is primarily an extension that requires manual snapshot triggers via protected `_snapshot()` function which leaves the cadence of snapshot to the implementer. `ERC-8054` creates a checkpoint on every state altering operation which ensures a complete and continuous historical records without requiring external coordination.

More importantly, `ERC-8054`’s primary contribution is the specification of forked tokens that inherit balances from a source token at a specific checkpoint. This brings decentralization benefits that `ERC20Snapshot` alone cannot provide. With `ERC-8054`, anyone can permissionlessly fork a token without relying on off-chain infrastructure or trusted snapshot operators.

Balance inheritance is fully on-chain and verifiable, removing the need for centralized coordination in airdrops, token migrations, and similar distribution events.

