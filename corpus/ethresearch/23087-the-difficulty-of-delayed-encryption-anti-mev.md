---
source: ethresearch
topic_id: 23087
title: The Difficulty of Delayed Encryption Anti-MEV
author: Lawliet-Chan
date: "2025-09-21"
category: Uncategorized
tags: []
url: https://ethresear.ch/t/the-difficulty-of-delayed-encryption-anti-mev/23087
views: 94
likes: 0
posts_count: 1
---

# The Difficulty of Delayed Encryption Anti-MEV

Introduction: Radius uses PVDE (time lock + zk) to encrypt the transaction pool, weakening the possibility of MEV attacks. That is, before the time lock is cracked, the transaction content cannot be seen, so MEV attacks cannot be carried out.

When Radius receives an encrypted transaction, it makes an order commitment and simultaneously begins to decrypt the time lock. After committing the user’s ordering, the time lock is cracked, and Radius obtains the transaction content and packages and executes it according to the committed order.

In this process, zk’s role is to prevent users from attacking the sequencer. If a user sends an invalid encrypted transaction, the sequencer spends time and computing power to crack an invalid transaction, which is equivalent to a DOS attack on the system. Zk ensures that without revealing specific transaction content, the sequencer can verify at minimal cost that this is a valid transaction (through zk verification).

### The Impact of Time Lock Performance

#### The Dilemma of Time Settings

The time lock setting is a double-edged sword. If set too short, it cannot effectively prevent MEV attacks; if set too long, it affects user experience and system throughput.

#### Computational Resource Consumption

The time lock decryption process requires significant computational resources, which may become a bottleneck for system scalability.

### Technical Challenges

1. Balance Between Security and Performance

How to find the optimal balance point between preventing MEV attacks and maintaining system performance is a key technical challenge.

2. User Experience Optimization

Long waiting times may affect user experience. How to optimize the user interface and provide clear progress feedback is crucial.

3. Economic Model Design

The time lock mechanism involves economic incentives. How to design a reasonable economic model to ensure system security while maintaining user enthusiasm is a complex issue.

### Future Prospects

With the continuous development of blockchain technology, delayed encryption technology is expected to make new breakthroughs in preventing MEV attacks while maintaining system efficiency.
