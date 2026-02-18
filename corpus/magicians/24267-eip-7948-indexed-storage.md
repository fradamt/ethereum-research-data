---
source: magicians
topic_id: 24267
title: "EIP-7948: Indexed Storage"
author: keyvank
date: "2025-05-19"
category: EIPs > EIPs core
tags: [evm]
url: https://ethereum-magicians.org/t/eip-7948-indexed-storage/24267
views: 167
likes: 3
posts_count: 4
---

# EIP-7948: Indexed Storage

## Abstract

Currently, the EVM provides basic storage functionality for smart contracts, primarily in the form of mappings (key-value pairs) using the `SSTORE` and `SLOAD` opcodes. However, there is no built-in support for iterating over it in a sorted manner. This EIP proposes the introduction of a **separate**, native key-value store in the EVM that would allow contracts to efficiently store, access, and iterate over key-value pairs in a sorted order. This would enhance the capabilities of smart contracts by enabling better data management, particularly for use cases involving ordered data, such as ranking systems or order books.

## Motivation

Many decentralized applications (dApps) rely on ordered data for various use cases, such as:

- Order books (to efficiently find matching orders)
- Ranking systems (e.g., leaderboards or voting systems)

Currently, to implement such ordered key-value pair storage, smart contracts must implement complex sorting logic or rely on external services (e.g., off-chain indexing). These approaches are often gas-inefficient and require extra off-chain infrastructure. By natively supporting sorted KV stores, smart contracts can perform these tasks more efficiently and cost-effectively.

Having a raw, iterable key-value store within contracts opens up opportunities for developers to build efficient and advanced data storage and querying libraries, enabling contract developers to fully leverage the underlying persistent key-value store of the Ethereum blockchain.

## Specification

For the purposes of this specification, we introduce a new storage system named ***Indexed Storage***, along with a set of dedicated opcodes to interact with it:

### ISTORE key value

Stores a key-value pair in the Indexed Storage. If the key already exists, its value is overwritten.

- Input:

key: A 32-byte key (fixed-length, similar to standard storage keys)
- value: Arbitrary-length value (subject to gas and storage limits)

**Behavior:**

- Inserts or updates the key-value pair in the storage.
- Maintains key ordering (lexicographic) for iteration purposes.

**Gas cost:** TBD, a fixed gas cost, plus additional gas per byte of the value.

### ILOAD key

Loads the value associated with a given key from the storage.

- Input:

key: A 32-byte key

**Output:**

- The corresponding value if the key exists; otherwise, returns empty or zero.

**Behavior:**

- Similar to SLOAD but accesses the separate storage.

**Gas cost:** TBD, a fixed gas-cost, plus

### IDELETE key

Deletes a key-value pair from the storage.

- Input:

key: A 32-byte key

**Behavior:**

- Removes the entry from the storage.

**Gas cost:** TBD, a fixed gas cost (potentially including a refund similar to SSTORE when deleting a non-zero entry).

### ISEEK prefix

Initializes an iterator starting from the first key that is **lexicographically greater than or equal to** the given prefix.

- Input:

prefix: A 32-byte value used to find the starting point

**Behavior:**

- Resets the internal iterator to the first matching key.
- If no matching key exists, the iterator is set to an end-of-iteration state.

**Gas cost:** TBD, a fixed gas-cost

### INEXT

Retrieves the next key-value pair from the current iterator position.

- Output:

(key, value) pair if a next entry exists; otherwise, returns an end-of-iteration signal (e.g., zero).

**Behavior:**

- Advances the iterator to the next lexicographically ordered key.
- Can be called repeatedly after ISEEK to traverse the storage.

**Gas cost:** TBD, a fixed gas cost, plus additional gas consumed to store the pair in memory.

The keys in Indexed Storage are fixed at 32 bytes to enable efficient use of the Merkle-Patricia Trie. This fixed size ensures compatibility with Ethereum’s existing storage mechanisms and simplifies trie construction, as each key is treated as a consistent and predictable length.

While the keys are fixed in size, the values associated with each key can have arbitrary size, allowing for flexible data storage. This flexibility ensures that the system can store diverse types of data, while maintaining efficient indexing and iteration of key-value pairs.

## Rationale

The implementation of this feature is straightforward because the database backend of Ethereum, which underpins the EVM’s storage mechanism, is already a **persistent Key-Value store**. Ethereum uses **LevelDB** or **RocksDB** as its default database engines, both of which inherently support efficient storage and retrieval of key-value pairs.

These databases are designed to handle key-value storage in a way that is optimized for performance, and they already facilitate sorting and iteration through key-value pairs. Specifically, they allow for **iterating over pairs using a key-prefix**, which means that keys can be retrieved in lexicographical order (ascending or descending) with minimal computational overhead. This is a core feature of the underlying database engines, and it is used extensively in Ethereum’s own state management (e.g., account balances, contract storage).

Given that Ethereum’s database backend already supports sorted key-value storage and iteration, adding native support for a sorted KV store in the EVM is trivial from an implementation standpoint. Ethereum contracts would be able to interact with this underlying functionality by leveraging the existing database capabilities for iterating over keys in sorted order.

Raw iterable key-value stores are fundamental building blocks of modern database systems. By introducing native support for a sorted KV store in the EVM, Ethereum contracts would be empowered to build sophisticated data management and querying libraries. These libraries could take full advantage of the underlying database features to support complex use cases. This would open up new possibilities for developers and increase the flexibility and efficiency of smart contract development.

### Use Cases

- Ranking Systems: Automatically maintain a leaderboard where scores or ranks are updated in real-time and can be iterated in sorted order.
- Auctions: Maintain and iterate over auction bids in ascending or descending order.
- Voting Systems: Efficiently track and iterate over votes or other metrics in sorted order.
- Order books: Manage and iterate over buy and sell orders in price order for decentralized exchanges or markets.

### Potential Alternatives

- Off-Chain Solutions: Currently, many developers use off-chain solutions, such as oracles or indexing services, to maintain sorted data. However, these solutions increase complexity and reliance on external infrastructure.
- Custom Sorting Logic: Developers could manually implement sorting within contracts, but this requires complex logic and would be costly in terms of gas fees. The native support for sorted KV stores would streamline this process.

## Backwards Compatibility

The new functionality would not break existing smart contracts but would add a new method of managing key-value pairs. It is fully compatible with the existing Ethereum Virtual Machine (EVM) and can coexist with current storage models such as mappings.

## Security Considerations

Since the values in Indexed Storage can be of arbitrary size, a key associated with a large value could result in unexpectedly high gas costs when read. This could lead to the caller unintentionally paying excessive gas fees. To mitigate this risk, one solution would be to limit values to 32 bytes, similar to the fixed-size keys, ensuring more predictable gas costs and preventing excessive storage usage.

Other than the potential for excessive gas costs, this EIP does not introduce any new critical security vulnerabilities to the EVM, if correctly implemented. The proposed functionality leverages the existing capabilities of Ethereum’s underlying key-value storage engines (e.g., LevelDB or RocksDB), which are already designed to handle ordered data safely and efficiently.

## Replies

**aryaethn** (2025-05-24):

Hi [@keyvank](/u/keyvank)

There are some issues or misunderstanding for me that I hope you can address them in your replies.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/keyvank/48/10268_2.png) keyvank:

> Many decentralized applications (dApps) rely on ordered data for various use cases

Unfortunately, I don’t find this statement very true. I would appreciate if you can provide some analytics or evidence for the word **“Many.”** I don’t find any evidence that there are many applications in need of Iterable storage.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/keyvank/48/10268_2.png) keyvank:

> Resets the internal iterator to the first matching key.

My concern here is:

The current design implies a single internal iterator per contract, which could lead to conflicts in scenarios where multiple functions or concurrent operations attempt to use the iterator simultaneously. This could result in unpredictable behavior, especially in complex contracts or during reentrant calls.

Another concern is that iterating over large datasets using INEXT could exceed transaction gas limits, potentially leaving operations incomplete. This would force developers to implement workarounds, such as pagination, which may undermine the efficiency gains of native iteration.

I really appreciate your work here, and in other EIPs such as EIP-7503. I hope you find my concerns useful here.

---

**keyvank** (2025-05-26):

Hi [@aryaethn](/u/aryaethn)!

Thanks for your feedback!

As someone transitioning from a general software engineering background into blockchain development, one thing I really miss is the ability to ***query*** data. There’s currently no easy or efficient way to query for an object with certain conditions in a smart contract. I’m confident that the ability to query data based on filters is one of the most important aspects of all software—essentially the ***database*** part of your project, or anything responsible for storing data.

While I’m not entirely sure how critical querying will be in Ethereum specifically, I’m absolutely certain there are projects in the ecosystem that rely on ***indexed on-chain data***.

Currently, implementing query-like functionality in Ethereum smart contracts is inherently gas-heavy, as it requires manual indexing—often using data structures like sorted trees (e.g., [BokkyPooBah’s Red-Black Binary Search Tree Library](https://github.com/bokkypoobah/BokkyPooBahsRedBlackTreeLibrary)).

The core issue is that the databases underlying many blockchain projects (including Bitcoin and Ethereum) are persistent key-value stores, and these already keep all keys sorted. In fact, when you perform an `SSTORE` in your contract, the key and value go through a B-tree insertion algorithm to be added to Ethereum’s database. However, because slot storage keys are hashed by default, the fact that these KV pairs are sorted becomes irrelevant.

The goal of this proposal is to expose the indexing power of KV-store databases to smart contracts. This would allow developers to build something akin to a relational database library in Solidity—by simply having a storage layout that keeps KV pairs ordered and allows for iteration. Such a database could enable storing, deleting, and querying objects using SQL-like queries.

You might think this would be gas-heavy. But keep in mind, the cost of sorting the data is already handled by the underlying database—so `ISTORE` would cost about the same as `SSTORE`. The gas cost for iteration depends on how many objects you need to retrieve and how optimized your implementation is. Crucially, you don’t have to iterate from the beginning of the database; you can jump to the point of interest (e.g., by performing an `ISEEK` before an `INEXT`, both of which I expect to cost about the same as `SLOAD`). Most of the time, you’d be looking for a single object—so a single `INEXT` would be enough to fetch the desired KV pair.

You are right about the fact that having a single-iterator may have security issues. Have to think about it ![:smiley:](https://ethereum-magicians.org/images/emoji/twitter/smiley.png?v=12)

Thanks again for your positive feedback on EIP-7503! ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=12)

---

**aryaethn** (2025-05-26):

[@keyvank](/u/keyvank)

Hi again.

I understand your problem of **Indexing** and **Querying** in the Ethereum blockchain. However, there is a project called [The Graph](https://thegraph.com/) that can handle the whole **Indexing** problem pretty easily. It has been a very popular project in the space and widely used here. It is pretty cheap and very easy to use.

If such projects can handle this kinds of problems and issues smoothly, I don’t see the need to implement this heavy EIP on the Ethereum itself.

Happy to read your ideas on the project I mentioned and whether it can solve your problem or not.

