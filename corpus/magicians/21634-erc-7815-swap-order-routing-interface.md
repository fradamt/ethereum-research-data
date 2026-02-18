---
source: magicians
topic_id: 21634
title: "ERC-7815: Swap Order Routing Interface"
author: yellow
date: "2024-11-09"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7815-swap-order-routing-interface/21634
views: 323
likes: 4
posts_count: 3
---

# ERC-7815: Swap Order Routing Interface

This ERC proposes a standardized interface for on-chain swap liquidity. It defines methods to calculate price, swap tokens, retrieve trading limits, and query capabilities of liquidity pools.

The standard simplifies access to defi liquidity sources – to improve composability and make routing (solving) easier.

ERC:



      [github.com](https://github.com/ethereum/ERCs/blob/70e96af4539a39ed2bf564ec3559fb45159ff223/ERCS/erc-7815.md)





####



```md
---
eip: 7815
title: Swap Order Routing Interface
description: An interface to simulate over swap liquidity.
author: Alan Höng (@kayibal), Markus Schmitt (@haikane)
discussions-to: https://ethereum-magicians.org/t/erc-7815-swap-orderrouting-interface/21634
status: Draft
type: Standards Track
category: ERC
created: 2024-11-09
---

## Abstract

This ERC proposes a standardized interface for on-chain swap liquidity. It defines methods to calculate price, swap tokens, retrieve trading limits, and query capabilities of liquidity pools.

The standard aims to simplify access to defi liquidity sources – to improve composability and make routing (solving), MEV capture (searching), and other defi functions easier.

## Motivation

```

  This file has been truncated. [show original](https://github.com/ethereum/ERCs/blob/70e96af4539a39ed2bf564ec3559fb45159ff223/ERCS/erc-7815.md)

## Replies

**timolson** (2025-09-17):

This interface doesn’t compile.

You need to decide if the `Fraction` limit in `swapToPrice(...)` is `calldata` or `memory`. IMO, `calldata` is preferable for a two-slot struct that is expected to be read-only.

Also, a slightly pedantic suggestion to use the precise mathematical term `Rational` instead of `Fraction`, since both the numerator and denominator are integers.

---

**timolson** (2025-09-17):

May I also suggest using a bit field instead of a dynamic array for the capabilities? Seems awkward and gassy for clients to iterate a list when a single bitmask would suffice.

Current example client code:

```auto
Capability[] private _capabilities;

function hasCapability(Capability c) internal view returns (bool) {
  for( uint256 i=0; i<_capabilities.length; i++ )
    if( _capabilities[i] == c )
      return true;
  return false;
}
```

Compare with bitfields:

```auto
uint256 private _capabilities;
uint256 constant public CAPABILITY_SELLORDER = 1<<0;
uint256 constant public CAPABILITY_BUYORDER = 1<<1;
uint256 constant public CAPABILITY_PRICEFUNCTION = 1<<2;
[...]

function hasCapability(uint256 c) internal view returns (bool) {
  return _capabilities & c != 0;
}
```

