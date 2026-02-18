---
source: magicians
topic_id: 3181
title: "EIP-1965 Valid ChainID For Specific BlockNumber : protect all forks"
author: wighawag
date: "2019-04-24"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-1965-valid-chainid-for-specific-blocknumber-protect-all-forks/3181
views: 3371
likes: 1
posts_count: 6
---

# EIP-1965 Valid ChainID For Specific BlockNumber : protect all forks

I created yet another EIP for replay protection. This one protect all forks from replay, including minority-led hardfork.

See https://github.com/ethereum/EIPs/pull/1965

## Replies

**shemnon** (2019-04-24):

Why not a precompile?  This is doing more work than reading a field like the other set of block and transaction properties.

---

**wighawag** (2019-04-25):

Even if it was the deciding criteria, we are talking here about just an extra comparison :

```auto
return blockNumber < valid(chainID)
```

where valid will fetch the blockNumber at which the chainID become invalid (0 if never part of the history of chainID) which is comparable to blockhash opcode

Thus, I still think it should be a simple opcode

---

**shemnon** (2019-04-25):

Opcodes are a limited resource, so I feel we should be stingy in dishing them out.

Because this is more than echoing data from the VM container I feel the complexity merits elevating it to precompiled contract.

---

**wighawag** (2019-04-26):

Ok, that sounds reasonable. How does it affect gas cost though ?

I see that there is this EIP (https://eips.ethereum.org/EIPS/eip-1109) that make me think the gas overhead is minimal but what about today?

---

**wighawag** (2019-04-28):

I edited the EIP to use a precompile.

