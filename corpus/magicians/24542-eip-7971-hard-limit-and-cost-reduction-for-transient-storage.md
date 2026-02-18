---
source: magicians
topic_id: 24542
title: "EIP-7971: Hard limit and cost reduction for transient storage allocation"
author: charles-cooper
date: "2025-06-12"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/eip-7971-hard-limit-and-cost-reduction-for-transient-storage-allocation/24542
views: 135
likes: 3
posts_count: 5
---

# EIP-7971: Hard limit and cost reduction for transient storage allocation

discussion thread for [EIP-7971: Hard Limits for Transient Storage](https://eips.ethereum.org/EIPS/eip-7971) (original PR [Add EIP: Hard Limits for Transient Storage by charles-cooper · Pull Request #9894 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/9894))

This EIP adds a transaction-global hard limit for transient storage and reprices TLOAD, TSTORE and warm SLOAD down to 5, 12 and 5, respectively. The current values are tentative and subject to further benchmarking.

## Replies

**yoavw** (2025-10-27):

Setting a transaction-wide maximum may introduce a DoS risk in protocols where a single transaction includes calls from multiple users.  A call to a contract that allocates `MAX_TRANSIENT_SLOTS` TSTOREs can cause other unrelated calls to fail.

Examples:

- ERC-4337 bundles: One UserOp calls such a contract, causing the UserOps of other users to revert and also pay for these reverts.
- Intent protocols or CoW swaps - a user may include a transfer of a malicious token which allocates MAX_TRANSIENT_SLOTS slots, causing other tokens to revert.
- Any interop protocol where a relayer performs a call on behalf of the user.  The relayer can relay the user’s call but cause it to revert, effectively censoring crosschain calls.
- Any EIP-7702 use case where a 3rd party performs calls on the user’s behalf (most of the 7702 use cases).

We should mitigate protocol DoS via correct gas price, not by placing hard limits on how many times an opcode may be called.  If 12 is a safe price for TSTORE, it shouldn’t require a hard limit.  If it isn’t, let’s increase it to a safe value.

Gas limits cause a similar risk but it’s mitigated by passing a gas limit to `CALL`.  If we add another hard limit to transactions, we’ll need to add it as a parameter to `CALL` as well.

---

**charles-cooper** (2025-11-08):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> We should mitigate protocol DoS via correct gas price, not by placing hard limits on how many times an opcode may be called. If 12 is a safe price for TSTORE, it shouldn’t require a hard limit. If it isn’t, let’s increase it to a safe value.

Changing the gas limit changes assumptions about what is a safe value. Should the price of TSTORE increase if the gas limit doubles?

---

**charles-cooper** (2025-11-09):

I’ve been considering the attack you describe and I don’t think it works that well in practice.

- Because of the lack of introspection of transient_slots_used variable, a would-be attacker can’t be sure of the “just so” number of slots to allocate to deprive downstream calls of transient storage slots, but so that it itself does not hit MAX_TRANSIENT_SLOTS and exceptional halt.
- A would-be attacker can’t be sure that downstream calls use transient storage, therefore it can’t even be sure if it will force downstream calls to revert.

I’m also simply not convinced this class of attacks is that dangerous:

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> ERC-4337 bundles: One UserOp calls such a contract, causing the UserOps of other users to revert and also pay for these reverts.

What would be the point of this?

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Intent protocols or CoW swaps - a user may include a transfer of a malicious token which allocates MAX_TRANSIENT_SLOTS slots, causing other tokens to revert.

- Other tokens could revert for any reason; the success of the token transfers should be checked by any such protocol anyways.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Any interop protocol where a relayer performs a call on behalf of the user. The relayer can relay the user’s call but cause it to revert, effectively censoring crosschain calls.

The relayer can cause the call to revert in a number of other ways, including:

- Restricting the amount of gas passed to the call
- Simply not performing the call, if censorship is the desired outcome

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/yoavw/48/4136_2.png) yoavw:

> Any EIP-7702 use case where a 3rd party performs calls on the user’s behalf (most of the 7702 use cases).

- Again, this seems pointless on the part of the 3rd party. They can employ one of the methods mentioned previously (restricting gas or simply not making the call)
- This would also likely be detected by users during transaction simulation, who have the freedom to choose other service providers; I’m guessing a transaction relayer which censors user actions would not remain popular for very long.

In all of the above cases, these would likely be mitigated during transaction simulation, or the outermost contract may choose to allocate a random number of transient storage slots to deprive the would-be attacker contract of certainty of whether they would succeed.

This brings me to my next point, which is that the mitigation that that you suggested (here [EIP-7923: Linear, Page-Based Memory Costing - #30 by yoavw](https://ethereum-magicians.org/t/eip-7923-linear-page-based-memory-costing/23290/30)), allowing introspection access via a new opcode `TRANSIENT_SLOTS_USED`, is possible, but I think it’s overkill. I think that in general, too much ability to introspect VM limits can cause other issues. For example, in the class of attacks you describe, it would actually give the would-be attacker *more* certainty about whether their attack will succeed, not less.

---

**Helkomine** (2026-01-09):

The majority of transient storage costs come from handling checkpoints when reverts occur, as mentioned in [EIP-1153](https://eips.ethereum.org/EIPS/eip-1153#reference-implementation). Therefore, I think a more reasonable approach is to still charge 100 gas for `TSTORE` and `TLOAD` while adding a reservation amount to the global refund counter (perhaps 88 to 92 gas for `TSTORE` and 95 gas for `TLOAD`). After the transaction is complete, that excess gas will be refunded from the refund counter. This leverages its natural limit of 20 percent on gas usage instead of having to establish new limiting mechanisms.

