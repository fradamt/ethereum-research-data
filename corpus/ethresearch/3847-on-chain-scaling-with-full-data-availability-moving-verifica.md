---
source: ethresearch
topic_id: 3847
title: On-chain scaling with full data availability. Moving verification of transactions off-chain?
author: jfdelgad
date: "2018-10-18"
category: Applications
tags: []
url: https://ethresear.ch/t/on-chain-scaling-with-full-data-availability-moving-verification-of-transactions-off-chain/3847
views: 4749
likes: 0
posts_count: 3
---

# On-chain scaling with full data availability. Moving verification of transactions off-chain?

This post follows from the discussion of on-chain scaling  in [On-chain scaling to potentially ~500 tx/sec through mass tx validation](https://ethresear.ch/t/on-chain-scaling-to-potentially-500-tx-sec-through-mass-tx-validation/3477),  the issues of not having data availability (https://github.com/ethereum/research/wiki/A-note-on-data-availability-and-erasure-coding) and the proposal of solutions based on zk-snark ([Roll_up / roll_back snark side chain ~17000 tps](https://ethresear.ch/t/roll-up-roll-back-snark-side-chain-17000-tps/3675/7)) with up to 17000 tx/sec but with no data availability on-chain.

We could scale to 100 tx/sec maintaining data availability.100 tx/sec implies a 400% increase in TPS and is simple.

A user identifier (address) is composed of 4 bytes. Amounts are also represented using 4 bytes.  A transaction can be formed as a tuple (to, amount, signature). This information is sent to the relayers that pack many of this transaction together and send it to the smart contract. The smart contract produces a log indicating that a batch transaction has happened.

There is no formal verification of individual transactions as this can be verified by anyone in the network just by looking at the data (also notice that the sender can be obtained from the signature which then allows us to get the 4 bytes of the user identifier )

The amount of data per transaction is 73 bytes, which in the worst case amounts to 4964 gas per transaction, assuming an overhead of 50000 gas (base transaction, log, etc.,) and a block limit of 8000000 gas, this gives us 1601 transaction per block, 106 tx/sec.

We could also include a field data in the tuple such that transactions to smart contracts can be included in the system:  (to, amount, signature, data) for ether transactions data will be empty. Otherwise, the data field will allow calling smart contracts inside the batch transactions.

Note that the relayers do not need to verify the transactions, their only goal is to build the transactions. However, is in their best interest to validate them as they need to be sure that they will be able to charge the corresponding fee.  This is not mean to be a formal mechanism of validation but acts as a filter in the system. Also, a crafty relayer has no more effect than any other fraudulent user (regarding the integrity of the transactions).

Everyone can then build a Merkle tree of the data and ignore transactions that are inconsistent, effectively moving the load of verification off-chain. The network acts then as an immutable register of information, determining the integrity of the data is left to applications and users that use the immutable register. This is possible because all the data is available.

The same idea can be used in general for any smart contract. Users send the data, making it available to everyone, but there is no reason to execute the contract on-chain and more important there is no need to store the results of the contract execution on the network.

## Replies

**dlubarov** (2018-10-20):

How do you envision typical users handling verification of payments sent to them?

If they didn’t store any state about which transactions are valid, then verifying a new transaction would require verifying its history all the way back to the genesis block, which seems prohibitively slow.

They could verify every incoming transaction and store the results, similar to what most nodes do today. But if that was the standard behavior, then I don’t really see the upside vs the current scheme.

I guess as a compromise, users could lazily verify the history of transactions that affect them, and memoize the results. But I suspect the memoized set would end up including a large portion of all transaction history.

On a side note, wouldn’t 4-byte addresses make it easy to find collisions (after an expected 2^32 attempts)?

---

**jfdelgad** (2018-10-21):

Thanks for your comments [@dlubarov](/u/dlubarov)

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> How do you envision typical users handling verification of payments sent to them?
>
>
> If they didn’t store any state about which transactions are valid, then verifying a new transaction would require verifying its history all the way back to the genesis block, which seems prohibitively slow.

All the load of verifying the transaction will be on the side of the users. Note that user can build a Merkle tree of the accounts, which is updated each time a batch transaction has happened. When they want to verify a new transaction they just need to check if the amount is valid, given the last status of the account.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> They could verify every incoming transaction and store the results, similar to what most nodes do today. But if that was the standard behavior, then I don’t really see the upside vs the current scheme.

The main idea is to be able to make batch transactions such that we avoid the base fee (21000 gas) on every single transaction. If we try to provide verification of each one of these transactions independently the amount of data required is big, such that the amount of gas per transaction will be close to the base fee, which is exactly what we want to avoid. Because all the data is available, we can check the transactions off-chain which allows us to put more transaction in the batch transaction.

Note that if layer 1 is modified to make miners to pack transactions like this, this will be better as the verification is made by consensus, but the idea proposed do not need modification to the first layer because everything is implemented using a smart contract.

![](https://ethresear.ch/user_avatar/ethresear.ch/dlubarov/48/918_2.png) dlubarov:

> On a side note, wouldn’t 4-byte addresses make it easy to find collisions (after an expected 2^32 attempts)?

I think I was not clear in this part. The users will register their addresses (normal ones) and they get a ID number. So this number just maps to the address. This means that the system will be able to handle a bit more than 4 billion users. If the number of registered addresses reaches 2^32 (if ever) then, will not be possible to register more addresses and the system will need to be upgraded.

One effect that I foresee is that the verification on the side of the miners will be reduced, as the block gas limit is determined, in part, by the amount of processing that the miners need to do to verify transactions, one may expect that the gas limit will increase, which will consequentially increase the number of transactions that can be included in a block.

There are still many things to define but I am working on a minimum viable implementation and I will post updates. Everybody comments will be very valuable.

