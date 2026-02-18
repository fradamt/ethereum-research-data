---
source: magicians
topic_id: 6536
title: Simple non-address-length-extending address periods
author: vbuterin
date: "2021-06-24"
category: Working Groups > Ethereum 1.x Ring
tags: [address-space]
url: https://ethereum-magicians.org/t/simple-non-address-length-extending-address-periods/6536
views: 1862
likes: 3
posts_count: 12
---

# Simple non-address-length-extending address periods

[State expiry](https://notes.ethereum.org/@vbuterin/state_expiry_eip) requires a notion of *address periods*, new spaces which addresses can live in of which one opens up roughly once per ~year long period. Addresses with address period > 0 must be clearly distinguishable from addresses with address period 0 (which, in these proposals, includes all present-day existing addresses). The [current proposals](https://notes.ethereum.org/@ipsilon/address-space-extension-exploration) do this by extending addresses from 20 to 32 bytes (simultaneously increasing their collision resistance from 80 to 100+ bits).

This is a proposal that goes in the opposite direction. We choose a 4-byte prefix (eg. `0x04030201`, if it’s admissible) that has not yet been used by any address. All address-producing functions (EOA, or CREATE, or CREATE2) are modified such that if they output an address with that prefix, set `address = xor(address, 0x010000...00)` to move it outside the prefix.

When address periods are introduced, we use the space covered by that 4-byte prefix for the address periods: the first 2 bytes are the address period number, and the remaining 14 bytes are the hash. This completely sacrifices the goal of collision resistance: the cost of finding a collision reduces to `2**56`, making counterfactual-address usecases and similar usecases where users need to trust not-yet-published contracts created by other people explicitly nonviable. However, preimage resistance remains at a secure `2**112`, so addresses continue to be secure enough for regular usecases.

## Replies

**Shymaa-Arafat** (2021-06-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> All address-producing functions (EOA, or CREATE, or CREATE2) are modified such that if they output an address with that prefix, set address = xor(address, 0x010000...00) to move it outside the prefix.

What if their regular output address was one with that prefix???

I mean output that equals a previously modified  address resulted from this XOR formula???

---

**vbuterin** (2021-06-24):

If A starts with that prefix, it’s mathematically impossible for `A xor 0x01000...00` to start with that prefix.

Or did you mean something else?

---

**Shymaa-Arafat** (2021-06-24):

I mean if the resulting address originally contained 1 in its last hexa bit (its prefix is 0x14030201)

-So it is not going to be XOR-ed, but it could equal a previous output of the XOR step

---

**vbuterin** (2021-06-24):

Ah I see. Yes, there is that theoretical possibility. But that doesn’t introduce any new issues; for example, there’s already the possibility that two different ECDSA pubkeys will have hashes where the last 20 bytes are the same but the first 12 bytes differ, and the pubkey → address hash-and-crop algorithm would make them resolve to the same address.

To make this even clearer, notice that if two address sources (pubkeys or code+salt+sender) do not lead to the same address today, but lead to the same address in my proposed scheme, that implies that they share their last 19.5 bytes, so they would also collide in a version of today’s status quo where addresses were 19.5 bytes long instead of 20. So my proposal doesn’t introduce any new address-collision issues for existing accounts that we don’t basically have in almost the same form already.

---

**axic** (2021-06-25):

I think a prefix or suffix has the problem that it is possible to easily grind collisions, if the prefix/suffix is not sufficiently long enough. See all the vanity addresses we have, for example for chai (to fit less bytes for condensing the gastoken), and ENS and the deposit contract, which have a lot of leading zeroes. The XOR idea works well for new contract creations, but I’m not convinced it is viable for EOAs (or even for commitments to CREATE2).

What happens if someone used a conflicting address as a commitment (for example in counterfactual) already? If we start introducing address restrictions, these old, but currently valid, commitments are broken. (Unless we introduce some kind of translation/exception fallback for these cases ![:sweat:](https://ethereum-magicians.org/images/emoji/twitter/sweat.png?v=9))

If there was the requirement that an account is only valid if it exists in the state (such as in EOS), then it would be “easy” to enforce new rules.

---

**vbuterin** (2021-06-25):

> What happens if someone used a conflicting address as a commitment (for example in counterfactual) already? If we start introducing address restrictions, these old, but currently valid, commitments are broken.

The argument is that the probability that such a commitment exists already is small. For example, if there are 1m counterfactual addresses, then there’s a probability of only 1/4294 that one of them will be hit. If we want to be even *more* sure, we can increase the prefix length to 5 bytes, reducing that probability to 1/1099511, though at the cost of reducing preimage security from 112 bits to 104 (still acceptable imo).

---

**_pm** (2021-06-26):

> This is a proposal that goes in the opposite direction. We choose a 4-byte prefix (eg. 0x04030201 , if it’s admissible) that has not yet been used by any address

This won’t work. As soon as someone publishes the eip draft with “unused prefix”, it will get used. Creating a vanity address is pretty easy, even for 8 bytes. Consider GPUs.

---

**vbuterin** (2021-06-26):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/_pm/48/4195_2.png) _pm:

> This won’t work. As soon as someone publishes the eip draft with “unused prefix”, it will get used. Creating a vanity address is pretty easy, even for 8 bytes. Consider GPUs.

The intention of the proposal if that if they do that, they’re screwed and that’s their fault (much like, say, deliberately sending 1000 ETH into a contract where withdrawing it requires calling 0x000…09 and getting a zero answer for some contrived reason right before an EIP adding a precompile to that address goes live).

---

**_pm** (2021-06-26):

Ah, right. That should work then.

---

**axic** (2021-07-13):

With [@jwasinger](/u/jwasinger) we are conducting some analysis and found plenty of 3-byte prefixes, and now trying to find 2-byte prefixes.

I’m still worried about existing not-in-state accounts (such as in token balances) as mentioned in [Simple non-address-length-extending address periods - #6 by axic](https://ethereum-magicians.org/t/simple-non-address-length-extending-address-periods/6536/6).  Likely a “recovery” mechanism like the ones we discussed under the address space extension calls would be relevant here too.

---

**axic** (2021-07-15):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> now trying to find 2-byte prefixes.

It seems there are no free 2-byte prefixes left.

