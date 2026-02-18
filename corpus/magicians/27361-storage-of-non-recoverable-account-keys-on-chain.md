---
source: magicians
topic_id: 27361
title: Storage of non-recoverable account keys on chain
author: SirSpudlington
date: "2025-12-30"
category: Magicians > Primordial Soup
tags: [wallet, postquantum]
url: https://ethereum-magicians.org/t/storage-of-non-recoverable-account-keys-on-chain/27361
views: 117
likes: 0
posts_count: 1
---

# Storage of non-recoverable account keys on chain

Most asymmetrical crypto does **not** support public key recovery. This makes post quantum migrations somewhat difficult, as keys would have to be provided on every transaction or stored in a contract somewhere. I had some initial ideas which may be a good start.

## The plan

---

Prerequisites:

- This assumes that EIP-7932 will be bundled with this EIP. A PQ meta EIP for all the PQ EIPs may be a good idea (7932, 8051, 8052, etc).
- I use accounts here as a term for both EOAs and contracts.

The actual details:

1. We tie public keys to addresses explicitly, preferrably in a backwards-compatible way such that a missing entry is treated as a non-disclosed secp256k1 key. This could be done in many ways such as adding an optional item to the account trie or deploying a system contract for storing public keys.
2. Allow accounts to link their public key (and associated algorithm) via calling the system contract instead of being hard coded to a public key hash.
3. Create a new transaction type for onboarding new accounts with no transaction history but a non-zero balance. This should only work once, and should enforce address derivation rules such as hash(algorithm_id || pubkey) -> address. This can directly onboard PQ keys without having to go through secp256k1.
4. Update EIP-7932 to allow algorithms to use an account’s specified public key if available.

## The good

---

This makes PQ migration all but a breeze. EOAs and AA accounts migrate with a single transaction. And, migration can happen gradually to any type of algorithm, multiple times. Even no algorithm for accounts that never need to transact e.g. `0x00...000`.

This also nicely complements [EIP-7701: Native Account Abstraction](https://eips.ethereum.org/EIPS/eip-7701) / generic AA, contracts or EOAs can set public key information which can be retrieved by verifier contracts. Contracts could set the invalid (0xFE) algorithm ID to use application specific data.

Some industry regulations require key rotation. This allows for simple and quick key rotation without having to migrate assets or using smart contracts.

## The bad

---

One of the biggest problems with this is that the `hash(pubkey) -> address` mechanism would not always return a valid address which could break some functionality in migrated address. However, if we have PQ algorithms, they’d also break such mechanisms anyway.

There is also a problem with allowing updates to public keys, compromised accounts could easily be lost if the attacker changes the key. Some form of commit / reveal or timelock scheme might fix this but it does require further discussion.

## The ugly

---

This proposal is quite dense. And, because of the fact that this touches literally all parts of signature handling, a mistake could be *ever so slightly* catastrophic. If we do go full AA though, this problem would be smaller.
