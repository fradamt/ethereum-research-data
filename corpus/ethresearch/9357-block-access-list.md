---
source: ethresearch
topic_id: 9357
title: Block access list
author: g11in
date: "2021-05-03"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/block-access-list/9357
views: 3201
likes: 4
posts_count: 6
---

# Block access list

**Background**

EIP 2029/2030 centers around creating  transaction level access lists for driving optimization through gas cost incentives. A transaction that provides an `access_list` as an additional input while being included in a block, gets cheaper costs (~10%) on some of the EVM op codes, and new (first time) accesses outside the provided ones get charged at higher cost. This inadvertently leads to generation of `transaction_access_list` which is also being standardized as a `JSON-RPC` endpoint.

**Motivation**

Motivation is to generate a `block_access_list` and make its `Hash/Commitment` as the part of the block. This will serve as an index into the block where address is being accessed in the transaction,

1. enabling partial inspection of the block by light clients or by fast sync protocols to fetch relevant data
2. block level optimization while verifying the block by enabling the construction of partial order on transaction execution
3. Bundling the witness data for future stateless execution chain

**Construction**

Currently:

`transaction_access_list= Set[AccessedAddress,List[AccessedStorageSlots] ] `’

Proposal:

`block_access_list=Set[Address, List[AccessedStorageSlots] ,Set[AccessedInBlockTransactionNumber,List[AccessedStorageSlots] ] ]`

To bundle Witnesses, this can be evolved into:

`block_access_list=Set[Address,List[AccessedStorageSlots],List[AccessedWitnesses],Set[AccessedInBlockTransactionNumber,List[AccessedStorageSlots],List[AccessedWitness] ] ]`

For purposes of building a `canonical_block_access_list` following sorting construction is suggested:

`canonical_block_access_list=Set<SortedByAddress>[Address, List<Sorted>[AccessedStorageSlots],Set<SortedByTransactionNumber>[AccessedInBlockTransactionNumber,List<Sorted>[AccessedStorageSlots] ] ]`

i.e. everything is just normally sorted. There was an idea to sort the base set of access_list by accessed by time, but above construction is simpler to generate, and on transaction level accessed by order doesn’t really matter since its easy to preload all the transaction access data.

`AccessListRoot` in **Block Header**

For this `access_list` to have any relevance and serve its purpose as index, its `hash` or `commitment` needs to be included in the `block header` to make it part of the `verified chain` that can be used as integrity check against grieving attacks. Now there are two ways to go about it:

- Just hash/commit this entire canonical_block_access_list
- Create a merkel/verkel tree out of it and use its root as as the fingerprint to be included in the block header.

While the first construction is simpler, second one is more favorable as it will allow partial and/or distributed downloading of the data especially favorable in `beam sync`, `light sync` and/or `stateless witness` protocols. This becomes important when the witness data would be needed to be bundled for achieving stateless ethereum.

Another point to note is, an `AccessRootType` can be bundeled in the block header to specify the construction of this root as it evolve over time w.r.t. construction methodology as well as data.

**Side Benefits**

Despite it not encoding an access by sorting, above construction still allows us to generate a partial order on the transaction execution and accesses so that the block execution/validation can be parallelized. Also, `transaction_access_list`s can be fast generated from the above construction, which can remove the need for transactions in block to rebundle this data with them or to atleast preempt fetching that transaction data.

Another side benefit of another construction is potential data compression that can be done while transmitting chunks of this tree as sorted lists can be compressed by sending the diffs rather over the wire.

---

PS: *this work has not been funded or granted by anyone. if you think this adds value to the ecosystem you could tip the author at: [0xb44ddd63d0e27bb3cd8046478b20c0465058ff04](https://etherscan.io/address/0xb44ddd63d0e27bb3cd8046478b20c0465058ff04)*

## Replies

**pipermerriam** (2021-05-05):

Thank you very much for putting this together.

First, I’m going to try and concisely restate your proposed structure in slightly different terms to be sure I’m understanding correctly.

### Defining Access Lists

An `access_list` is comprised of many `access_list_entry` elements:

```auto
access_list   :=  [access_list_entry, ...]
```

An `access_list_entry` is a 3-tuple of:

- address
- sorted list of storage slots
- sorted list of 2-tuples of:

transaction index storage slot was first accessed
- sorted list of storage slots which were accessed

```auto
access_list                 := [access_list_entry, ...]
access_list_entry           := [address, storage_slots, storage_slots_by_txn_index]
address                     := bytes20
storage_slots_by_txn_index  := [txn_index_and_slots, ...]
txn_index_and_slots         := [txn_index, storage_slots]
txn_index                   := uint64  # or uint256 or whatever
storage_slots               := [storage_slot, ...]
storage_slot                := uint256
```

Additional sorting rules for the above are that:

- access_list is sorted by the address
- storage_slots is sorted
- storage_slots_by_txn_index is sorted by txn_index

Additional validation rules for the above are that:

- Each unique address may only appear at most once in access_list
- Each storage_slot may only appear at most once in storage_slots
- Each txn_index may only appear at most once in txn_index_and_slots

Have I interpreted this correctly?

---

**g11in** (2021-05-06):

yes [@pipermerriam](/u/pipermerriam) , your interpretation has further articulated and crystalized the proposed construction. thank you! ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

let me make some further clarifications to ensure if we are on the same page:

`storage_slots` are that particular `address`'s storage slots. Also I would also want to change `storage_slots_by_txn_index` to `address_accesses_by_txn_index` so as to keep the option of evolving this structure in future to include witnesses (and/or may be code blocks once the code merkelization goes live) and also to imply that `storage_slots_by_txn_index` has `txn_index_and_slots` in reference to that particular address only.

Do you think this makes sense?

---

**pipermerriam** (2021-05-10):

![](https://ethresear.ch/user_avatar/ethresear.ch/g11in/48/6047_2.png) g11in:

> storage_slots are that particular address’s storage slots.

Yes, the slots for the corresponding `account`

![](https://ethresear.ch/user_avatar/ethresear.ch/g11in/48/6047_2.png) g11in:

> Also I would also want to change storage_slots_by_txn_index to address_accesses_by_txn_index so as to keep the option of evolving this structure in future to include witnesses

Sure, I don’t have a strong opinion about this at this stage beyond this.  The inclusion of this “meta index” that lets us know what was accessed within a specific transaction seems potentially useful, but also not required.  In cases like this, it is often good to start simple and move towards something more complex once there is consensus that it will be useful.  So when you do your next write up of this, I would encourage you to actually remove this from the structure and present the simplest access list format without this data, and then include an “optional” extension of the scheme that includes the extra meta information about access by individual transactions, in which you can explain your justification for why you see this extra information being valuable.

---

**adlerjohn** (2021-05-15):

https://twitter.com/jadler0/status/1235563508168904709

---

**g11in** (2021-05-16):

yes this construction will enable “cache warmup” of the nodes validating the forged blocks. kindly checkout next iteration: [Block access list - v0.1](https://ethresear.ch/t/block-access-list-v0-1/9505)

