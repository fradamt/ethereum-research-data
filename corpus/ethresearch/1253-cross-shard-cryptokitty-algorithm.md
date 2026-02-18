---
source: ethresearch
topic_id: 1253
title: Cross-Shard CryptoKitty Algorithm?
author: kladkogex
date: "2018-02-28"
category: Sharding
tags: []
url: https://ethresear.ch/t/cross-shard-cryptokitty-algorithm/1253
views: 1704
likes: 3
posts_count: 4
---

# Cross-Shard CryptoKitty Algorithm?

I am trying to understand how difficult it is to program things across shards, where there are only messages sent between smart contracts, and now direct calls.

I am using a simple example of Alice that wants to buy a CryptoKitty using a token that lives on a different shard.

1. There are two shards, A and B.
2. ERC token ERCT lives on shard A.
3. CryptoKitty smart contract CK lives on shard B.
4. Alice wants to buy a Kitty from CK. The price of a Kitty is 1T

It is  assumed that contracts can send authenticated messages to each other across shards with guaranteed delivery.  For instance, shard A can sign messages using a BLS threshold signature that is trusted by shard B.

Here is an algorithm that uses two messages and works as follows ( I wonder if one can come up with a better algorithm):

a) Alice calls ERCT telling it  to buy 1 Kitty for 1T.

ERCT stage:

b) ERCT verifies that Alice posesses 1T

c) ERCT transfers 1T to CK in the internal  table of pending payments

d) ERCT sends an authenticated message to CK  requesting transfer of Kitty to Alice.

CK Stage:

e) CK verifies that Kitty is still available (it may have been bought by someone else)

f) If Kitty is not available, then CK sends an error message to  ERCT, including the hash of the original request

g) If the Kitty is available, then CK transfers Kitty to Alice, and sends a success message to ERCT, including the hash of the original request

ERCT Stage:

h) If ERCT receives an error message, it will revert the pending payment, and credit money back to Alice

i) If ERCT receives success message, it will commit the pending payment.

Would be interesting to see other examples of synchronous algorithms turned into asynchronous messaging

## Replies

**vbuterin** (2018-02-28):

Yeah, this seems like the only way to do it if the ERC token is on one shard. The ideal solution would be for the token to exist across shards.

---

**kladkogex** (2018-02-28):

I guess it depends on how fast the inter-shard communication is …

If inter-shard communication is slow or expensive, then using an ERC token like that is not effective.

If you have a system where messages are sent fast across shards

then the fact that you need a cross-shard communication for each use of the token should not matter too much.

If you have a token that lives on many shards, this means that you have a smart contract that lives on many shards.  Then you need to split the state of the ERC token somehow. Theoretically you could split users into subgroups and store each subgroup on a particular shard, but then you would have to deal with cross-shard communications anyway if you transfer money between users belonging to different groups …

[Interesting paper on the subject](https://arxiv.org/pdf/1801.00687.pdf), which also compares different smart contract platforms

They have a “continuation” keyword in the language, so the last stage in the example above would be denoted as a continuation

Note that a similar “continuation” keyword could be easily added to Solidity (or Viper)

---

**laurentyzhang** (2019-09-15):

The best solution will be self-organizing, dynamically group users of a single popular dAPP under one shard. Static sharding wouldn’t work well, more than 90% TXs are inter-shards on ETH if you use some random address based sharding strategy

