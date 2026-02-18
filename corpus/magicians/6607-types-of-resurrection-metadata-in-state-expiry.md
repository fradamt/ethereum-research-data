---
source: magicians
topic_id: 6607
title: Types of Resurrection Metadata in State Expiry
author: matt
date: "2021-07-05"
category: Working Groups > Ethereum 1.x Ring
tags: [state-expiry, address-space]
url: https://ethereum-magicians.org/t/types-of-resurrection-metadata-in-state-expiry/6607
views: 1739
likes: 5
posts_count: 6
---

# Types of Resurrection Metadata in State Expiry

*Thanks to [@adietrichs](/u/adietrichs) for reviewing this post.*

[State expiry](https://notes.ethereum.org/@vbuterin/verkle_and_state_expiry_proposal) is the current preferred solution the [state growth problem](https://hackmd.io/@vbuterin/state_size_management).

For the purposes of this post, we’ll think of state expiry as a mechanism that, at fixed intervals, expires the entire state trie. Storing previous periods is generally orthogonal to this post, as we’re focusing on how to resurrect state that has been forgotten – regardless if `n=0` or `n=1`.

Here is a summary of a few proposed mechanisms:

### Nothing

Nothing is as straightforward as it sounds. Simply expire state and then require users to provide witnesses for state elements they use that are not in the active state. Note that elements that are read or written to that have not been initialized in the active state *must* have either an exclusion proofs showing they haven’t been initialized at any point in the past or a proof showing a certain value in time and then exclusion proofs showing it hasn’t changed since then.

##### Pros

- really easy

##### Cons

- exclusion proof sizes grow linearly with the number of periods, making it extraordinarily expensive to initialize state elements
- kicks the address-collision problem down the road

### Period-Aware Addresses (PWA)

The main problem with having *no* metadata is that initializing new state elements is really expensive. Period-aware addresses give the protocol a mechanism to avoid address collisions upon initialization of new elements. The discriminator establishes a lower bound on what period an account could have existed. There are currently two potential approaches to having PWAs:

#### Address Space Extension (ASE)

- Vitalik’s original writeup
- Ipsilon writeup

tldr; allow legacy 20 byte addresses and 32 byte ASE prefixed addresses. Create a context variable in the EVM to modify the behavior of opcodes that deal with addresses depending whether they’re executing in legacy or ASE mode.

##### Pros

- new state can be initialized without proofs
- extendable to hold other metadata
- solves the address-collision problem

##### Cons

- requires significant EVM changes
- creates two different EVM contexts, legacy mode and extended mode
- translation map will grow unbounded (linear in relation to the number long addresses used in legacy context), and can’t be expired seems like it can be expired, with a small risk of a collision after expiration
- confusing UX, now potentially 3 types of addresses a user’s funds could be stored under (short, long, compressed)
- not all solidity compiled contracts mask addresses to 160 bits, so it’s possible some contracts have dirty upper bits in addresses

([more complete analysis by Ipsilon](https://notes.ethereum.org/@ipsilon/address-space-extension-issues))

#### Extension-free PWA

- Vitalik’s original writeup

tldr; find an unused 4-byte prefix and disallow new contracts / addresses from being created with it under legacy rules. Legacy contracts execute in legacy mode, creating new addresses using legacy rules. New contracts execute in PWA mode, creating new contracts where the first 4-bytes are the pre-selected prefix, bytes 5-6 are the current period, and bytes 7-20 are the address as usual.

##### Pros

- new state can be initialized without proofs
- relatively straightforward EVM changes
- doesn’t require translation table, users only have one address to consider
- doesn’t break existing tooling (although they may have display the xor’d address instead of the preimage?)

##### Cons

- makes address-collisions very practical, no more counterfactual contracts
- not an eloquent solution, may make address extension harder in the future

### Period Metadata

#### Trie Metadata

I don’t think this idea has been formally defined (other than in [@adietrichs](/u/adietrichs)’ head), but roughly the idea is to add a new field to the account object in the state trie denoting its creation epoch. This solves the issue of new storage initialization being very expensive due to exclusion proofs (especially assuming contracts are written to deploy new child contracts per period), but does not improve the “do nothing” case for creating new accounts.

#### Pros

- new storage elements can be initialized without proofs if a contract is fresh
- pretty simple
- extendable to hold other metadata
- doesn’t require unbounded state growth for external mapping
- doesn’t break existing tooling

#### Cons

- kicks the address-collision problem down the road
- creating new accounts is expensive, need exclusion proof from period 0 that the account never existed

#### External Period Registry

Also not formally defined, but the broad strokes are we introduce a new registry trie which stores state expiry metadata. The registry would not be expirable and would store the period that the contract was created. Additional information could be stored, like total number of storage elements. Any time the number of active storage elements equals the number of total storage elements for the contract, the contract period could be promoted to the current period. A scheme like this could probably also be implemented for the EWA proposals with a state trie modification.

##### Pros

- new state can be initialized without proofs
- extendable to hold other metadata
- doesn’t require translation table, users only have one address to consider
- doesn’t break existing tooling

##### Cons

- new trie structure
- grows unbounded (linear in relation to the number of addresses in use)
- kicks the address-collision problem down the road

## Replies

**adietrichs** (2021-07-05):

While I personally really hope we can make one of the PWA approaches work (ideally ASE), I think the trie metadata alternative might not actually be terrible, especially if combined with some light version of the period registry. Rough idea:

- For contracts, store creation period among (expirable) metadata such as nonce and balance (this is what you call trie metadata). This would solve state expiry for contract storage.
- Keep some minimal information about previously created accounts in state. Worst case that would be a complete tree of touched addressses (but without any attached data, you only need the address itself). Ideally it could be more efficient, e.g. prune dense areas & accept that those from now on always require exclusion proofs. Maybe do something clever with bloom filters (I know, attackable, but maybe they can still be made to work in this context), or something similar. Basically, accept some minimal extra in-state information to make the exclusion proof situation for accounts bearable.

---

**axic** (2021-07-14):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/matt/48/2725_2.png) matt:

> #### External Period Registry
>
>
>
> Also not formally defined, but the broad strokes are we introduce a new registry trie which stores state expiry metadata. The registry would not be expirable and would store the period that the contract was created. Additional information could be stored, like total number of storage elements

Is this any better than just keeping a reduced version of the account alive?

As part of the rent discussions in 2018 such options were discussed. A version of that is described in [EIP-1682](https://eips.ethereum.org/EIPS/eip-1682):

> When an account’s balance is insufficient to pay rent, the account becomes inactive. Its storage and contract code are removed. Inactive accounts cannot be interacted with, i.e. it behaves as if it has no contract code.
>
>
> Inactive accounts can be restored by re-uploading their storage. To restore an inactive account A, a new account B is created with arbitrary code and its storage modified with SSTORE operations until it matches the storage root of A. Account B can restore A through the RESTORETO opcode. This means the cost of restoring an account is equivalent to recreating it via successive SSTORE operations.

---

**matt** (2021-07-19):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Is this any better than just keeping a reduced version of the account alive?

I think to take advantage of state expiry (expiring the entire trie) you can’t keep a reduced version in place, you would need an external structure to store the mapping whether the account had ever been created. Otherwise under the current state expiry mechanism, the metadata would expire and you would be back to needing exclusion proofs from genesis.

---

**axic** (2021-07-20):

I think at least having this as an option in your list makes sense, because

1. External registry.

- Pro: Potentially simpler state expiry rules
- Con: Yet another data structure to maintain; Data duplication (the address); Potentially needs expiration too?

1. Keeping some metadata in the main tree.

- Pro: No secondary tree to maintain; No data duplication
- Con: State expiry rules need to be modified to keep some of the account alive

Or maybe I am misunderstanding it, and the external registry would never expire, but be append only?

---

**matt** (2021-07-24):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/axic/48/480_2.png) axic:

> Or maybe I am misunderstanding it, and the external registry would never expire, but be append only?

I don’t I made it very clear, but yes the external registry would never expire. This is what I mean by “grows unbounded” in the cons.

–

There are benefits of keeping metadata in the state trie and there may be ways of combining different schemes together. In the specific case of EIP-1682, I don’t think it can be classified as a type of state expiry as defined above. State elements are reduced when they become stale – IIUC there isn’t a mechanism to remove entire portions of the trie at once.

