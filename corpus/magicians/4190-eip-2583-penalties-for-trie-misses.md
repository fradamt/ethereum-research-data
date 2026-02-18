---
source: magicians
topic_id: 4190
title: "EIP 2583: Penalties for trie misses"
author: holiman
date: "2020-04-10"
category: EIPs
tags: []
url: https://ethereum-magicians.org/t/eip-2583-penalties-for-trie-misses/4190
views: 2770
likes: 1
posts_count: 5
---

# EIP 2583: Penalties for trie misses

Discussion-topic for https://github.com/ethereum/EIPs/pull/2583

## Replies

**holiman** (2020-04-10):

This eip introduces a `penalty` for operations which hit the main account trie but misses. The penalty is somwhere around 1K gas, since any higher penalty would be possible to bypass via shielding through a call (more details in the EIP).

There are also two variants suggested, which both overcome the attack.

### Alt 1: Insta-refunds

Bump all trie accesses with `penalty`. `EXTCODEHASH` becomes `2700` instead of `700`.

- If a trie access hit an existing item, immediately refund penalty (2K )

Upside:

- This eliminates the ‘shielded relay’ attack

Downside:

- This increases the up-front cost of many ops (CALL/EXTCODEHASH/EXTCODESIZE/STATICCALL/EXTCODESIZE etc)

Which may break many contracts.

### Alt 2: Parent bail

Use `penalty` as described, but if a child context goes OOG on the `penalty`, then the remainder is subtracted from the

parent context (recursively).

Upside:

- This eliminates the ‘shielded relay’ attack

Downside:

- This breaks the current invariant that a child context is limited by whatever gas was allocated for it.

However, the invariant is not totally thrown out, the new invariant becomes that it is limited to gas + penalty.

This can be seen as ‘messy’ – since only *some* types of OOG (penalties) becomes passed up the call chain, but not others, e.g. OOG due to trying

to allocate too much memory. There is a distinction, however:

- Gas-costs which arise due to not-yet-consumed resources do not get passed to parent. For example: a huge allocation is not actually performed if there is insufficient gas.
- Whereas gas-costs which arise due to already-consumed resources do get passed to parent; in this case the penalty is paid post-facto for a trie iteration.

---

**holiman** (2020-04-10):

pinging [@axic](/u/axic) [@karalabe](/u/karalabe) [@vbuterin](/u/vbuterin) [@AlexeyAkhunov](/u/alexeyakhunov)

---

**AlexeyAkhunov** (2020-04-20):

Thank you! I have looked at it. What I did not understand is this - why do the accesses that miss the items in the account trie are worse than accesses that do not miss?

Or are you saying that all account accesses are currently underpriced, but we will only adjust the pricing for those we deem to be “attacking”?

---

**holiman** (2020-04-22):

So, the reasoning is:

- For hits, it’s possible to cache them. Some nodes will have executed the tx while in txpool. and caches will be “warm” once the block includes the tx. Also, there’s more work involved in getting ‘hits’, as you need to first fill the memory with a large chunk of valid addresses, then iterate over and load from memory into stack. As opposed to just GAS and done.
- Secondarily: trie misses are more UX-friendly to penaliz. In most cases, a trie miss means that the layer2-flow should be aborted. So it doesn’t matter if we add another X gas, potentially causing an OOG, because the contract would have reverted anyway.

> Or are you saying that all account accesses are currently underpriced, but we will only adjust the pricing for those we deem to be “attacking”?

Almost but not quite. I *do* think trie-misses are more expensive, and I also think all trie accesses are underpriced in general, but I think the former is more attackable than the latter.

