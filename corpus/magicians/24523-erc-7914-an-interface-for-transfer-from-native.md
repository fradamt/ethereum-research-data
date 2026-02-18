---
source: magicians
topic_id: 24523
title: "ERC-7914: An Interface for Transfer From Native"
author: sarareynolds
date: "2025-06-11"
category: ERCs
tags: []
url: https://ethereum-magicians.org/t/erc-7914-an-interface-for-transfer-from-native/24523
views: 80
likes: 0
posts_count: 4
---

# ERC-7914: An Interface for Transfer From Native

Discussion for ERC-7914: An Interface for Transfer From Native

## Replies

**SamWilsn** (2025-06-25):

Should this requirement be split into two:

> SHOULD early return with true when amount == 0 and skip any event emissions […]

Maybe becomes:

> SHOULD early return with true when amount == 0 and skip any event emissions. MUST NOT execute any fallback function when amount == 0.

---

**SamWilsn** (2025-06-25):

You might want to investigate [ERC-165](https://eips.ethereum.org/EIPS/eip-165) for discovering support for this interface.

---

**wjmelements** (2025-06-25):

I don’t think I understand the purpose of the `from` parameter in `transferFromNative`. An account can only move its own ether. The rationale given is in the specification:

> If from is not address(this) the contract COULD forward the call. Note that specifically parameterizing a from address allows for flexibility, and other types of integrations with this standard.

I don’t think this makes much sense. A delegated approval chain seems unsafe. I suspect this parameter was naively copied over from erc20. Perhaps you could give an example of how this could make sense. Otherwise the `from` parameter should be removed.

