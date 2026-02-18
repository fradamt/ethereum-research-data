---
source: magicians
topic_id: 27291
title: "Data type for massively parallelized Ethereum-like platform: mapping with order and a form of mutex (reminiscent of Golang mappings)"
author: bipedaljoe
date: "2025-12-23"
category: Uncategorized
tags: []
url: https://ethereum-magicians.org/t/data-type-for-massively-parallelized-ethereum-like-platform-mapping-with-order-and-a-form-of-mutex-reminiscent-of-golang-mappings/27291
views: 75
likes: 0
posts_count: 3
---

# Data type for massively parallelized Ethereum-like platform: mapping with order and a form of mutex (reminiscent of Golang mappings)

***Edit:** Polkadot seems to have this “ordered mapping” in a “light variant”. They allow iteration through the keys in an order (which makes use of the Patricia Merkle Trie and orders keys lexigraphically by the keys in storage which is the hash of the key. Technically it uses next_storage_key which is method on Backend trait and TrieBackend implements Backend and the DbState uses that, see [here](https://github.com/paritytech/substrate/blob/master/client/db/src/lib.rs#L104)). But, they do not allow fetching a key by index, or getting the index of a key, which will require length meta data at each branch in trie (possibly included in the Merkle proofs) and a form of mutex. But it is a good start. See https://paritytech.github.io/substrate/master/frame_support/storage/trait.IterableStorageMap.html. Overall I think the “ordered mapping” will be needed to truly scale, and can be good to start discussing it now.*

***Edit:** Cosmos has this type of ordering in their trees in storage it seems, so it can do `GetByIndex()`, `GetWithIndex(key)` and `Size()` (see [their codebase](https://pkg.go.dev/github.com/cosmos/iavl)), and it seems they use the length meta-data in their Merkle proofs, see [ProofInnerNode](https://pkg.go.dev/github.com/cosmos/iavl#ProofInnerNode). They do not seem to allow use of that in smart contracts, but the backend seems to support it which is a good start. It seems this data type is often called “order statistics trees”, [Order statistic tree - Wikipedia](https://en.wikipedia.org/wiki/Order_statistic_tree). I think such an “ordered mapping” will be necessary for massive parallelization, it is not possible otherwise to parallelize many things (like registration, shuffling, voting in Bitpeople).*

My goal is https://doc.bitpeople.org that requires massive parallelization. In Golang, you can iterate through a mapping with range. While you iterate, the mapping does not change. Technically, if you could manually “lock” the mapping to guarantee it does not change, you could also access by index, or get the index of a key. I think such a mapping on a “world computer” could allow for massive parallelization.

To practically achieve that, you make the mapping its own trie. And nodes track meta-data about the length at each branch in the trie. Thus, they always know the index of a key as long as the number of keys do not change (thus, you “lock” the mapping before you use index operations).

Unlock is always deferred to end of block. Thus, “shard” (that have to be internal to node… for game theory reasons… unless you transcend paradigm and do “trustless attestation” by “encrypted computation that cannot lie”…) only have to check “globally” once if mutex was taken, and are then free to do everything in parallel.

I think generalizing a storage architecture to that structured data and complex data is always its own trie, in a flat storage trie where each key is such a “storage object” (and a contract is as well), and you can then have pointers to “storage objects” as value to the storage slots (so you can do nested mappings or mappings in structs, or structs in contracts, etc), seems a good approach.

For my Bitpeople, you would during registration not use mutex or index operations on the mapping. Then, after registration closes (after two weeks, see the whitepaper or source code) you register the random number for a week (see whitepaper, it uses ideal RNG). And then, you shuffle by taking each key in the registration mapping, hashing it with the RNG, and inserting it into a new mapping (with the account address as value). You require every key moves (as mappings have length attribute it is easy to check). Everyone can move their own key, if someone does not anyone can move their key manually (lookup the key off-chain) but anyone who did not move prior to event starts cannot participate (but they can still be shuffled, as shuffling needs to complete). And then, once everyone shuffled, you do `.Lock()` on the mapping (without any deferred `.Unlock()`…). That gives you a shuffled population of 10 billion people, all in parallel.

## Replies

**bipedaljoe** (2025-12-23):

The type is intermediate between mapping and array. Fills a void. Mappings can be operated on in parallel, arrays cannot. This one can but also has array-like qualities.

---

**bipedaljoe** (2025-12-26):

Storage architecture can still be per contract, as long as “ordered mapping” is its own trie (ideally it would have the length-meta data hashed into the Merkle proofs so that anyone can prove an index, this is to ask a lot from it, but it is a really important data type). The “storage object” concept (that can point to one another) but per-contract also works well.

More examples of where “ordered mapping” can be used: Election, in “one person, one unit of stake”, which I implemented here for my foundation: [panarkistiftelsen.se/kod/Election.sol](https://panarkistiftelsen.se/kod/Election.sol), that my consensus engine interacts with, [panarkistiftelsen.se/kod/panarchy.go](https://panarkistiftelsen.se/kod/panarchy.go). I assume there are countless examples, that lots and lots of smart contract and dApp ideas would benefit from something like it, and that the idea might not have been discussed much since still not that many that plan for hundreds of thousands of transactions per second. Or if people have discussed it, I would be happy to learn about that.

