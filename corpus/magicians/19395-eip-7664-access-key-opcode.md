---
source: magicians
topic_id: 19395
title: "EIP-7664: Access-Key opcode"
author: protolambda
date: "2024-03-28"
category: EIPs > EIPs core
tags: []
url: https://ethereum-magicians.org/t/eip-7664-access-key-opcode/19395
views: 1627
likes: 8
posts_count: 9
---

# EIP-7664: Access-Key opcode

Discussion thread for EIP-7664: Access-Key opcode - [Add EIP: Access-Key opcode by protolambda · Pull Request #8357 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8357)

Background:

- See EIP-2930 thread: EIP-2930: Optional access lists

Implementation: [work in progress]

The access-key opcode enables contracts to read inputs that are statically declared in access-lists.

## Replies

**wjmelements** (2024-03-28):

EIP-2930 access lists are not of the format

```auto
{address:[storageKeys]}
```

They are of the format

```auto
[(address,[storageKeys])]
```

So your spec should describe how the key lists concatenate to form your index scheme, and how duplicates are handled. Transactions are gas-penalized for being structured this way but it is allowed and so the behavior must be defined.

---

**frangio** (2024-03-29):

Is “static state access” the relevant part of the EIP-2930 quote? That sounds like a different thing to me, more about statically defining the state accesses of a tx, than it being a generic container for static data. I do think the proposal is interesting, I’m just not sure that the quote supports this use case as claimed.

Entries in the access list remain priced basically like storage reads, even though they may be arbitrary data not intended to be used as storage keys. This seems inefficient. Conceptually, shouldn’t the pricing be more like that of a word in calldata?

---

**wjmelements** (2024-03-29):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Conceptually, shouldn’t the pricing be more like that of a word in calldata?

It may be useful to have globally accessible transaction data similar to `ORIGIN`; the access list makes sense in that regard. The exact ordering of the access list is a degree of freedom. What you are getting at could be even more useful: equivalently-global access to the tx.data. But the `ACCESSKEY` can be useful despite its high setup cost for supplying storage keys to access, saving otherwise-redundant calldata.

In opposition to the `ACCESSKEY` opcode, currently we can calculate and apply an access list and know that it will only impact the `GAS` opcode. The `ACCESSKEY` opcode would allow further branching on the access list itself, which could make it more difficult to compute `eth_createAccessList`.

Another suggestion could be to add an address parameter to make the entire access list accessible, not just the portion specific to the executing account.

---

**protolambda** (2024-03-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/frangio/48/7043_2.png) frangio:

> Is “static state access” the relevant part of the EIP-2930 quote? That sounds like a different thing to me, more about statically defining the state accesses of a tx, than it being a generic container for static data. I do think the proposal is interesting, I’m just not sure that the quote supports this use case as claimed.

The “static” part is relevant, but you are right about the state access detail; if it was not declared in the transaction then it would be an access determined during runtime. While in the new EIP it is no longer just a state access, its core purpose is static information being visible to a contract, which aside from effects on gas-costs, is about to be completely lost with 3074.

> Entries in the access list remain priced basically like storage reads, even though they may be arbitrary data not intended to be used as storage keys. This seems inefficient. Conceptually, shouldn’t the pricing be more like that of a word in calldata?

This is true, but there already was a separate EIP to reduce the access-list cost. Compared to calldata it is indeed quite expensive. For the purpose of statically declaring non-state keys I think the price is high, but since it pro-actively warms up state, I think there is no way around it, without inventing a completely distinct static transaction-metadata paradigm.

---

**protolambda** (2024-03-30):

Good point about the access-list structure, although the `[K, Values]` vs `{K: Values}` difference is more of a side-effect due to the RLP encoding, as far as I understand it. I will try to clarify how the indexing works relative to the values of the matching contract address.

Duplicate keys are an interesting edge-case, I don’t think I have seen those in the wild, likely due to the increased gas costs as you mentioned, but if it’s indeed valid I will update the EIP to cover this case.

---

**protolambda** (2024-03-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/wjmelements/48/432_2.png) wjmelements:

> Another suggestion could be to add an address parameter to make the entire access list accessible, not just the portion specific to the executing account.

I have thought about this, in the rationale / security-considerations I mention:

> The access is scoped strictly to the contract that would otherwise perform a warm SLOAD,
> and thus storage-layout abstractions do not leak between different smart contract applications.

The storage-layout leaking is the thing I’d like to avoid with this limitation. Contracts that load access-list data for gas-cost purposes (currently only 100 gas savings, but oh well, different topic) will then be sharing their access-keys to other distinct applications, which might start to rely on in unexpected ways.

---

**wjmelements** (2024-03-31):

Regrettably the zero return-value in the out-of-bounds case is indistinguishable from a storage-key of zero, and the zero storage-key is fairly common since it is the first to be assigned by solidity. Any error value can collide due to the word size. There are three ways to resolve this:

1. Choose a less-common storage key, such as -1 (0xff…ff).
2. Add another return value to indicate success and distinguish this case.
3. Add another opcode to get the length of the account access list.

I prefer the first solution for simplicity. Solidity and Vyper will never assign the last storage slot, so it would only be a problem in the case of a hash collision.

---

**protolambda** (2024-05-08):

Withdrawing this EIP: [Update EIP-7664: Move to Withdrawn by protolambda · Pull Request #8534 · ethereum/EIPs · GitHub](https://github.com/ethereum/EIPs/pull/8534)

