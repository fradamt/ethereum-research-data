---
source: ethresearch
topic_id: 8602
title: Alternative bounded-state-friendly address scheme
author: vbuterin
date: "2021-01-30"
category: Execution Layer Research
tags: []
url: https://ethresear.ch/t/alternative-bounded-state-friendly-address-scheme/8602
views: 3935
likes: 4
posts_count: 13
---

# Alternative bounded-state-friendly address scheme

## Recap: state size management techniques

In order to prevent the ethereum state size from growing without limit, we need some way to “expire” old state, so that participating nodes in the network no longer need to store that state. Even if most clients are stateless, it seems reasonable to expect that eventually the system will scale enough that the network cannot afford to indefinitely guarantee availability of all state. There are two approaches to expiring old state:

1. Explicitly delete it, and perhaps move it into some separate Merkle tree so someone who cares about that state object can get the Merkle branch and use it to revive the state object at some future time.
2. Do not move the object in the tree structure; instead, simply flag that position in the tree as “expired” so nodes do not make an effort to store it (and the protocol does not expect them to do so). Expired objects can be accessed (and de-expired) by sending a transaction that provides the Merkle proof (aka. witness) to access that state.

(1) corresponds to “classical storage rent”, (2) corresponds to the easiest extension of traditional “stateless clients” to a model where old state can be forgotten. Both approaches allow individual actors who care about specific state objects to keep track of the Merkle branches that they can later use to revive those objects if they get expired. However, both have distinct flaws.

(1) suffers from edge cases when contracts can be re-created at the same address at which a contract was already expired. That is, if a contract at address A is created, then expired, then the transaction that created the contract at address A is re-played, that could create a new object at address A which would interfere with the revival of the original object. Another type of situation is when an object is created at address A, then expired, then revived, then modified (eg. by sending contained funds to another account), then expired, then a revival is made using the Merkle branch from the first expiry. This violates conservation rules and could be used to print coins; additional Merkle proofs need to be added to prove that a contract has not yet been revived from some given state from which a revival is attempted.

(2) suffers from a different problem. Suppose two adjacent addresses (meaning, no object exists in between them) A1 and A2 are both expired. Then, not only are A1 and A2 no longer accessible (unless someone still stores the Merkle branches), but also all addresses between A1 and A2. This means that, if there are N addresses in total, ~1/N of all possible address space is no longer accessible. By the time half of addresses are expired, ~1/4 of the address space is inaccessible. As time goes on, it becomes harder and harder to find space to generate new addresses. And because new addresses get concentrated in the remaining “accessible” space, this effect is exponential: the accessible space halves once per N years.

## Proposal

I propose a version of (2) that is modified to solve the above problem. As in many proposed implementations of (2), accounts are either “active” or “expired”; an expired account is an account that has not been touched for >= 1 year. To access an expired account, you need to provide a witness; when an expired account is accessed, that account is automatically de-expired (touching *any* account resets its 1 year time-to-expiry). The modification is as follows:

- We add a 32-bit “epoch prefix” to each address (meant to be interpreted as an integer). For example, an address with epoch prefix 9 would look like: 0x00000009de0b295669a9fd93d5f28d9ec85e40f4cb697bae, with the 00000009 being the epoch prefix.
- The Merkle path would depend directly on the epoch prefix and not it hash (so merkle_path_key = address[:4] + hash(address[4:]) instead of merkle_path_key = hash(address) as in the status quo). This ensures that “fresh” address space is contiguous.
- An address cannot be touched unless the epoch prefix of that address is less than or equal to the number of years that the chain has been in operation.
- A CREATE3 opcode would be added, that takes epoch prefix as an argument, and creates a contract at an address with that epoch prefix.

It would be recommended and the default for users and contracts to always create accounts with the newest possible epoch prefix because they will be certain that the full state of the newest epoch prefix is still accessible. To preserve the ability to have “counterfactual addresses” (addresses that users interact with on-chain [eg. by sending ETH or ERC20 tokens] or off-chain [eg. by interacting in a channel] before the contract code has been published), it would continue to be possible to create contracts with older epoch prefixes. However, users wishing to create counterfactual addresses that they leave un-created for a long time would take on the responsibility of storing old state branches for that account.

After many years of operation, it is expected that the active state would consist of (i) the entire portion of the address space with the most recent epoch prefix, and (ii) specific portions of the older states that correspond to accounts that have been actively used.

Note that this scheme can be naturally extended to contracts; in fact, it is in a contract’s own interest to voluntarily follow a schema where the portion of storage prefixed with some bytes representing the number N refers to data connected with addresses from year N. This could be naturally used to store eg. token balances.

## Replies

**pipermerriam** (2021-01-30):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> An address cannot be touched unless the epoch prefix is less than or equal to the number of years that the chain has been in operation.

Can you clarify this, maybe with an example?  Is the epoch prefix a sort of monotonically increasing timestamp?  Supposing this was in place today, what would the epoch prefix be, and how would it change over the course of the next … ?month/year?

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> accounts are either “active” or “expired”; an expired account is an account that has not been touched for >= 1 year

You mention using a flag for expired/active.  How would this flag be toggled?  It seems like we would need to do something like an integer timestamp and an account is considered inactive when `account.last_touched <= now - 1year`.

---

**vbuterin** (2021-01-31):

> Can you clarify this, maybe with an example? Is the epoch prefix a sort of monotonically increasing timestamp?

I reworded it a little bit. Think of the “current epoch” (this is different from eth2 epochs, we’d need a better term for it, maybe “era” or something) as being `block.number // 2000000`. Addresses from before this scheme was put into place would be automatically assigned an epoch prefix of 0. Note that “current epoch” and “epoch prefix” are different things: the current epoch is a property of the state of the chain, and an epoch prefix is a part of an address. An address whose epoch prefix exceeds the current epoch cannot be touched.

> How would this flag be toggled?

Adding a “last touched” timestamp field to each tree node and updating it upon each read/write would be one option.

---

**pipermerriam** (2021-01-31):

Can you clarify about the epoch prefix in the address.  Taking the address `0x00000001deadbeef...`,  would `0x00000001` be the *prefix* component?  This address would only be touchable during year 1?

---

**vbuterin** (2021-02-01):

> would 0x00000001 be the prefix component?

Yes

> This address would only be touchable during year 1?

During or after year 1.

---

**pipermerriam** (2021-02-01):

Do you have an idea or plan for how we deal with all the existing addresses that have prefixes that would make them untouchable?

---

**vbuterin** (2021-02-01):

Existing addresses would be automatically assigned a prefix of `0x00000000`. So this would expand the state tree from 2^{160} to 2^{192}, and assign the existing address space to the first 2^{160} slice.

---

**pipermerriam** (2021-02-01):

So IIUC this proposal would:

1. Give us a mechanism for clearly denoting between hot/cold state
2. Give us a mechanism to mitigate against the loss of large sections of the address space if sections of the “cold” data are truly lost.

It sounds like we would be doing the same thing with contract storage?  Currently storage keys are 32 bytes.  Would we expand them to be effectively 36 bytes? All current contracts would continue to store data under the `0x00000000` prefix.  New contracts *could* implement more advanced logic for taking advantage of the newer blocks of storage space that use newer prefixes?

---

**pipermerriam** (2021-02-02):

Some thoughts on the actual implementation:

It seems that we’d be adding a `last_touched_at` timestamp to both:

- each account in the account trie
- each entry in the contract storage trie

A naive implementation of this means that we incur an additional write for every single read which is really unfortunate.

Alternatively, we could **not** update the timestamp for reads, and only update it when:

1. the value is written.
2. some other explicit mechanism that pays for the timestamp to be updated such as a new opcode.

The protocol can then be updated so that state whos timestamp is older than some constant `COLD_STATE_EXIRATION` can only be touched by transactions if the transaction includes a proof for the state (at which point the timestamp would be updated).

I recognize that all of this is not the direction I think [@vbuterin](/u/vbuterin) was focused on, but I think these things can naturally fall out of the same system.

With respect to the additional epoch prefixed address space: I think there’s a clean path towards upgrading to that system.

1. Legacy stuff like 20-byte addresses continue to work.  We just implicitely add the 0x00000000 prefix to them.
2. New transaction type or update the transaction validation rules to support both 20 and 24 byte addresses.

Still some figuring out to do with contract storage.  In theory we can default things to the `0x00000000` prefix but it seems there needs to be an update to the various storage based opcodes to support the new extra 4-byte prefixes.  This is explicitly awkward for storage keys since they would become 36 bytes, and thus, no longer fit into a single 32-byte stack value.

---

**vbuterin** (2021-02-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> It sounds like we would be doing the same thing with contract storage? Currently storage keys are 32 bytes. Would we expand them to be effectively 36 bytes? All current contracts would continue to store data under the 0x00000000 prefix. New contracts could implement more advanced logic for taking advantage of the newer blocks of storage space that use newer prefixes?

Technically contracts could just implement the scheme internally on their own, and it would be in their interests to, though we would need to help out by allowing them to set the first four bytes of the Merkle-path-key directly instead of making the Merkle path key be a hash of the storage key.

![](https://ethresear.ch/user_avatar/ethresear.ch/pipermerriam/48/4199_2.png) pipermerriam:

> some other explicit mechanism that pays for the timestamp to be updated such as a new opcode.

Sounds good to me! Though I do think that it would be in many contract’s interests to have code that says “if you read me and I have less than 6 months of time-to-live you have to pay to update me” - which implies time-to-live being accessible to the EVM.

---

**CarlBeek** (2021-02-03):

Does this not break existing contracts that store or compute over `Adress` types?

---

**vbuterin** (2021-02-06):

Existing contracts would only be able to deal with addresses created in the index-0 space, so applications would have to upgrade at some point. Another thing is that this would be a great opportunity to increase the size of an address from 20 to 32 bytes (26 for the hash, 4 for the epoch, 2 reserved in case we want shard IDs or whatever); the 20 -> 26 increase from the hash is something that has to be done at some point *anyway* because 20 bytes is not enough for long-term collision resistance.

---

**tbrannt** (2021-02-14):

For me it seems a bit like things are quite convoluted and overcomplicated at this point.

IMO More than they have to. Perfect is the enemy of good and especially after reading https://hackmd.io/@HWeNw8hNRimMm2m2GH56Cw/state_size_management it is my impression that you are all too committed to certain (nice) properties and thereby constrained in your view.

Here’s what I see as the best way to manage state at this point:

- Go back from rent per storage slot to rent per account
- Give up on the property to be able to resurrect state

Just have contracts require a certain eth balance and burn x eth of that balance every block (x being proportional to the storage slots the contract occupies).

Yes, people could be mean and increase the space certain contracts take. What are the counter measures? Well operations that create new state could require high amounts of gas. So an attacker would burn big amounts of his/her own capital. If a contract is really used a lot and there’s big public interest in it then keeping the balance high enough even in case it takes up a lot of space will probably not be a problem. The action of last resort would always be to migrate the community/dapp to a new fresh copy of the smart contract where balances under a certain threshold are nulled.

Also let contracts go that do not have any ether balance left. If a user created a contract wallet then it will only be deleted if no ETH is left. in that case this shouldn’t be a problem. Also other ERC20 contracts could still keep a balance for that account even if it’s not on chain as a contract anymore. Recreating the account with the private key would not cause any problems as we do not have to expect any resurrection conflicts and even the ERC20 balances would still be there as these contracts wouldn’t have been deleted when the account got deleted.

Also let the ETH balance contract have a special position where it does not need any gas to be stored. You could demand a certain minimum balance of ETH that accounts can hold (this can be decreased as eth gets more valuable and new hardware allows bigger state)

Do I really want to keep track of all the ERC20 contracts that perhabs airdropped some tokens for me and pay rent for the storage slot my address takes up on that contract? Do you really want anyone to deal with parcially erased smart contracts? Sorry but that sounds super ugly to me.

