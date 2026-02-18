---
source: ethresearch
topic_id: 16483
title: Implementation overview Of partial state caching mechanism:
author: sogolmalek
date: "2023-08-26"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/implementation-overview-of-partial-state-caching-mechanism/16483
views: 1436
likes: 3
posts_count: 1
---

# Implementation overview Of partial state caching mechanism:

Linking to my [previous proposal](https://ethresear.ch/t/efficient-stateless-ethereum-execution/16480), Ive inititated an implementation idea for this component.

I’m genuinely excited about the combination of this component with our other state provider component, which generates and propagates a zk proof of the last state to the LCs. In case of cache inconsistencies or failures, participants can fall back on the ZK proofs of the latest state to validate the correctness of cached fragments. This integration ensures network resilience and the ability to independently verify state accuracy.

1. Cache Data Structure:

Implement a Hash Map and Linked List combination:

- Use a hash map to store cached entries. Keys should be derived from state fragment characteristics (e.g., account address, block number).
- Utilize a doubly linked list to maintain the order of accessed entries for eviction.
A doubly linked list is a data structure where each node contains not only a reference to the next node but also a reference to the previous node. This bidirectional linkage allows for efficient navigation both forward and backward through the list. In the context of a cache management mechanism, a doubly linked list can be used to keep track of the order in which entries were accessed, which is useful for implementing cache eviction policies like Least Recently Used (LRU).

Doubly linked list can be utilized in the context of a cache:

- An empty doubly linked list to serve as the order of access for cached entries.
- Maintaining pointers to the head (the most recently accessed entry) and tail (the least recently accessed entry) of the list.
- When a new entry is cached, create a new node in the doubly linked list and link it to the current head.
- Update the head pointer to point to the new node.
- When an entry is accessed from the cache, move its corresponding node to the front of the linked list.
- This involves updating the node’s previous and next pointers to rearrange its position.
- When the cache is full and an eviction is necessary, remove the node at the tail of the linked list.
- Update the tail pointer to point to the next node.

The advantage of using a doubly linked list for maintaining access order is that it allows for efficient removal and insertion of nodes, which is essential for LRU-based cache eviction policies. When an entry is accessed, it can be easily moved to the front of the list to signify its recent use. When an eviction is required, the tail of the list (the least recently used entry) can be removed with ease.

1. Caching Policies:Choose LRU (Least Recently Used) Policy:

- When the cache is full, evict the least recently accessed entry.
- Update the linked list to reflect the access order for eviction purposes.

1. Key Generation:Generate Keys:

- Create a hashing function that generates keys from relevant data attributes, ensuring uniqueness and efficient retrieval.

1. Consensus-Driven Validation:Validation:

- Integrate a cryptographic validation mechanism (digital signatures) to validate the authenticity of cached entries.

1. Frequent Access Detection:

- Implement access counters for each cached entry.

1. Cache Size Management:

- Set a maximum cache size and implement the eviction process based on the basic LRU policy.

1. Data Segmentation:

- Identify a few state fragments that will be considered critical for caching.

1. Cache Expiry and Refresh:

- Attach an expiry timestamp to each cached entry with a refresh mechanism

1. Optimized Retrieval Process:Cache Look-up First:

- Before accessing the Verkle tree, check if the requested data exists in the cache.
- If present, return the cached data immediately.

**In case of cache inconsistencies or failures, participants can fall back on the ZK proofs of the latest state to validate the correctness of cached fragments. This integration ensures network resilience and the ability to independently verify state accuracy.**

With this prototype design, the partial state caching mechanism can efficiently manage frequently accessed or critical state fragments within the Portal Network.
