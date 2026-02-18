---
source: magicians
topic_id: 26697
title: "Draft ERC: Reverse Indexable Contracts"
author: oed
date: "2025-11-24"
category: ERCs
tags: [dapps, indexing]
url: https://ethereum-magicians.org/t/draft-erc-reverse-indexable-contracts/26697
views: 89
likes: 1
posts_count: 2
---

# Draft ERC: Reverse Indexable Contracts

## Abstract

This proposal standardizes `ReverseIndexable`, an abstract contract pattern that records the most recent block containing contract activity and emits a `BlockPointer` event linking to the previous activity block. By following this reverse-linked list of block numbers, any frontend or monitoring agent with only an Ethereum RPC endpoint can deterministically rebuild the contract’s full activity history, delivering decentralized resilience without relying on trusted indexer infrastructure.

## Motivation

Most event-driven dapps depend on proprietary indexers or third-party data providers to populate their user interfaces. When those centralized services fail, rate-limit, or get censored, the dapp UI degrades even though the contract remains live. `ReverseIndexable` allows any consumer with RPC access to Ethereum (including light clients, fallback providers, or private nodes) to rebuild the complete activity feed by following an on-chain linked list of block numbers, keeping frontends responsive even if every off-chain index goes dark. Standardizing the approach makes it possible for wallets, explorers, and competing frontends to share the same resilient discovery algorithm without bespoke integrations.

## Specification

The key words “MUST”, “MUST NOT”, “REQUIRED”, “SHALL”, “SHALL NOT”, “SHOULD”, “SHOULD NOT”, “RECOMMENDED”, “NOT RECOMMENDED”, “MAY”, and “OPTIONAL” in this document are to be interpreted as described in RFC 2119 and RFC 8174.

### Interface

Implementations MUST expose the following Solidity interface (or an equivalent representation in other languages):

```solidity
interface ReverseIndexable {
    /// @notice Most recent block that reported contract activity
    function blockPointer() public view returns (uint256);

    /// @notice Emitted before blockPointer is updated
    event BlockPointer(uint256 previousBlock);
}
```

Implementations MAY provide helper functions (e.g., an internal `touchIndex()`, see the *Reference Implementation* section).

### Storage

- blockPointer MUST be a uint256 that stores the latest block number that the contract declared as containing observable activity.
- blockPointer MUST initialize to 0 at deployment and MUST ONLY change when emitting a new reverse-index entry for the current block.

### Events

- BlockPointer(uint256 previousBlock) MUST be emitted exactly once for each successful pointer update.
- The previousBlock argument MUST equal the blockPointer value before the function updates storage.
- The event MUST be emitted before blockPointer is overwritten so the log encodes a linked list node.

### Block pointer update behavior

Whenever a contract records the current block as containing observable activity:

1. It MUST emit BlockPointer(blockPointer).
2. It MUST set blockPointer = block.number.
3. It MUST restrict pointer updates to internal/private contexts so external callers cannot spoof the activity chain.

Implementations MUST perform these steps at least once per block that includes externally observable state changes or event emissions. Contracts SHOULD ensure the pointer update routine is invoked at most once per block per logical action to avoid redundant pointers, but emitting the event multiple times in the same block is still valid.

### Indexer obligations

Indexers that consume this standard MUST:

1. Read blockPointer() via eth_call to obtain the most recent activity block.
2. Query eth_getLogs for every contract event in that block.
3. Extract the BlockPointer event for that block and repeat the process with the returned previousBlock until reaching zero.

Clients MAY cache discovered blocks to deduplicate work. Contracts MAY emit additional metadata in other events; indexers MUST NOT assume a single event type per block.

### Integration guidance

- Contracts SHOULD wrap the pointer update logic in modifiers or helper methods (e.g., an internal touchIndex()) that are shared across mutating entrypoints such as mints, bounty updates, or claim submissions.
- Tooling SHOULD surface when a transaction emits application events without invoking the pointer update helper so developers can enforce the invariant off-chain.
- Frontends MAY batch eth_getLogs queries by requesting the range [blockPointer - N, blockPointer] (e.g., 500 blocks at a time) to capture multiple BlockPointer events per request, substantially improving synchronization speed versus querying blocks one-by-one.
- Projects aiming for low-latency UX MAY run centralized indexers as their primary data source while keeping the reverse indexing flow as a resilience fallback that can be replayed on demand.

## Rationale

- Reverse linking over forward scanning: Storing the previous block number directly in the event eliminates the need for heuristics or binary search over blocks.
- Single storage slot: The pattern reuses one storage word (blockPointer), keeping gas overhead predictable while providing constant-time lookups.
- Internal visibility: Keeping the update routine internal forces inheriting contracts to deliberately gate when indexing metadata is emitted, aligning with minimal-surface security practices.
- Improved UX: Indexers consume the newest information first and stream backward, so users see the latest activity immediately instead of waiting for the entire history to replay from genesis as is common in forward-scanning blockchain apps.

## Backwards Compatibility

This standard adds an optional interface that contracts MAY inherit. It does not modify existing ERCs or system-level behavior, so no backward compatibility issues are expected. Contracts that already implement ReverseIndexable SHOULD ensure their implementations follow the normative requirements above before claiming compliance.

## Test Cases

Compliant contracts SHOULD be validated with the following behaviors:

1. blockPointer initializes to 0.
2. Invoking the pointer update helper with no prior activity updates blockPointer to block.number and emits BlockPointer(0).
3. Subsequent invocations emit the previous pointer and update storage accordingly, forming a chain (block100 -> block200 -> block300).
4. Multiple invocations in the same transaction MAY emit multiple BlockPointer events (implementations MAY guard against this, but indexers MUST tolerate it).

## Reference Implementation

```solidity
abstract contract ReverseIndexable {
    uint256 public blockPointer;

    event BlockPointer(uint256 previousBlock);

    /// @dev Helper that links the current block, guarded against duplicates.
    function touchIndex() internal {
        uint256 previousBlock = blockPointer;
        if (previousBlock == block.number) return;
        emit BlockPointer(blockPointer);
        blockPointer = block.number;
    }
}
```

## Security Considerations

- Missed updates: If a contract emits application events without running the pointer update routine, those events become invisible to reverse indexers. Application developers MUST bake the routine into every state transition that surfaces user-facing data.
- Chain reorgs: Because pointers reference absolute block numbers, deep reorganizations can orphan parts of the chain. Indexers SHOULD handle reorg notifications and re-sync from the newest stable blockPointer if a block number disappears.
- Spam mitigation: Attackers could deliberately trigger the pointer routine repeatedly in the same block to waste indexer time. Indexers SHOULD deduplicate identical previousBlock values observed within a block, and contracts SHOULD throttle redundant calls (e.g., by adding guards to their pointer helper).
- Concurrency: Inheriting contracts MUST ensure the pointer update routine cannot be reentered unexpectedly (e.g., via hooks) lest the linked list contain intermediate values that skip user events.

## Copyright

Copyright and related rights waived via CC0.

## Replies

**zergity** (2025-11-26):

I think it’s a solid idea.

It’s cheaper than maintaining your own indexer, but still more expensive than using public free indexer like etherscan. There’s nothing wrong with using public free indexer, the worst they can do is missing data.

