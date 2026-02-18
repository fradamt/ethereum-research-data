---
source: magicians
topic_id: 25572
title: ERC-20 Maturity Metadata Extension
author: zikarium
date: "2025-09-23"
category: ERCs
tags: [erc, token]
url: https://ethereum-magicians.org/t/erc-20-maturity-metadata-extension/25572
views: 46
likes: 0
posts_count: 2
---

# ERC-20 Maturity Metadata Extension

# ERC-20 Maturity Metadata Extension

Hi all, I’d like to propose a very small ERC extension for discussion.

### Motivation

Many ERC-20 tokens represent assets with a **maturity date**, such as fixed-income tokens, bond tokens, structured portfolios, or other expiry-based instruments.

Right now, each project encodes this metadata in its own way (if at all), which makes it harder for wallets, indexers, and protocols to provide consistent UX.

I’m also mindful of the risk of proliferating many small ERC-20 extensions. The intent here is not to set a precedent for every possible metadata field, but to cover a recurring, domain-defining property that already exists across many projects: maturity. By keeping the interface minimal (just one function and one event), the goal is to improve interoperability without bloating the standard.

The idea here is to define a **minimal, read-only extension** that standardizes maturity metadata in a uniform way.

### Specification

I see two possible approaches:

**Option A: Minimalist**

```solidity
/// @notice ERC-20 Maturity Metadata Extension (Minimalist)
/// @dev A maturity timestamp of 0 means "not set"
interface IERC20Maturity {
    /// @return Unix timestamp of maturity (in seconds). Returns 0 if not set.
    function maturity() external view returns (uint256);

    /// Emitted whenever maturity is updated
    event MaturityUpdated(uint256 newValue);
}
```

**Option B: With Convenience**

```solidity
/// @notice ERC-20 Maturity Metadata Extension (Convenience)
/// @dev A maturity timestamp of 0 means "not set"
interface IERC20Maturity {
    /// @return Unix timestamp of maturity (in seconds). Returns 0 if not set.
    function maturity() external view returns (uint256);

    /// @return true if maturity is set and block.timestamp >= maturity
    function hasMatured() external view returns (bool);

    /// Emitted whenever maturity is updated
    event MaturityUpdated(uint256 newValue);
}
```

### Rationale

- Option A keeps the extension as lean as possible, in line with how other ERCs avoid derived helpers.
- Option B adds a small convenience function for on-chain consumers, saving them from re-implementing block.timestamp >= maturity().

In both cases, returning `0` makes it clear that no maturity is set.

### Benefits

- Wallets can consistently display “Matures on DATE.”
- Indexers and explorers can query maturity without bespoke adapters.
- Protocols can rely on a uniform interface for settlement logic.

### Open Questions

1. Do you think the hasMatured() helper is worth standardizing, or is it better to stay minimalist?
2. Is 0 as a sentinel value for “not set” a good choice, or should it be handled differently?
3. Are there any edge cases or pitfalls we should consider?

---

This feels almost too simple to be an ERC, but maybe that’s a strength. My goal is to keep it minimal, useful, and easy for others to adopt.

Looking forward to your thoughts!

## Replies

**MASDXI** (2025-10-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/zikarium/48/16037_2.png) zikarium:

> minimal, useful, and easy for others to adopt

Check out my previous work [ERC-7818: Expirable ERC-20](https://eips.ethereum.org/EIPS/eip-7818). I think you can actually wrap your interface on top of it.

