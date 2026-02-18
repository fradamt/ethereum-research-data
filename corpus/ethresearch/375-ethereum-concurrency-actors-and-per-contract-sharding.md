---
source: ethresearch
topic_id: 375
title: Ethereum concurrency, actors and per-contract sharding
author: kladkogex
date: "2017-12-26"
category: Sharding
tags: []
url: https://ethresear.ch/t/ethereum-concurrency-actors-and-per-contract-sharding/375
views: 4224
likes: 7
posts_count: 7
---

# Ethereum concurrency, actors and per-contract sharding

[This paper](https://arxiv.org/pdf/1702.05511.pdf) discusses various  concurrency issues with Ethereum contracts.

I think many of these issues come from a single fact that EVM allows a contract to directly call another contract.

This leads to tightly coupled contracts and two major problems

The first problem is  security issues due to a possibility of re-entrant behavior (as was manifested by the DAO vulnerability)

The second problem is that it is hard to parallelize contract execution because if is not known in advance which contract is going to be called inside of a given contract so there is potentially lots of effectively shared variables.  Currently ETH clients execute contracts sequentially, so you can essentially use only one CPU core.

In the Big Data world it is known that tightly connected architectures are hardly parallelizable and have lots of concurrency issues, so people are switching to so called [Actor model,](https://en.wikipedia.org/wiki/Actor_model) where each actor interacts with other actors only by sending asynchronous messages,  and not by issuing blocking calls.  Once you have a collection of actors you can execute them

in any way you want and it is guaranteed that there will be no concurrency issues.  The actor model is used by many modern frameworks such as Apache Spark and Apache Akka.

In order to make smart contracts actors one needs to prohibit contracts from calling each other directly. Instead, each call from contract A to contract B needs to be done asynchronously by sending a message.

Once contracts are decoupled, contract execution can be made highly parallel in the following way

1. For a given block,  first go through all messages and group them according to the contract called by the message.  Only calls to the same contract need to be processed sequentially, calls to different contracts can be executed in different threads.
2. As contracts are executed, they will send messages to call other contracts.  These virtual messages will form virtual  block 1, that is “virtually appended” to the current block.  Once the original block is processed, the virtual block 1 messages will need to be sorted and then executed.  The messages can be deterministically sorted by first using the hash of the receiving contract address, so that messages calling the same contract are be grouped together, and then according to the hash of the message.  In this way virtual block 1 will be uniquely deterministically ordered.
3. Then virtual block  1 will be processed to yield virtual block 2 and so on until there are no more messages.
4. When the miner sends the block to other nodes, only the original block needs to be sent, and the virtual blocks
are reconstructed by nodes during the validation.

Benefits of this model:

a) more secure - all reentrant bugs dissapear

b) much more parallel - a typical Ethereum block will be split into groups of transactions according to the contract address, and each group can be executed in parallel.

c) Faster transaction rate for the Ethereum network - sequential contract execution is currently a performance bottleneck

d) Ethereum client can be re-engineered by using an actor framework [like this](https://github.com/AsynkronIT/protoactor-go).

e) For sharding, with “Actor” contracts there is an interesting possibility to assign a shard to each contract. This can make both storage and compute highly parallel, and you will not need any cross-shard token transfers, since a particular token can live completely on its shard, and all operations with this token would not cross the shard. Essentially the only token that will need to be transferred across shards will be ETH.

## Replies

**AFDudley** (2017-12-28):

Yep. Lots of people have made a note of this, to varying degrees, over the years.

R-Chain is the project that I’m most familiar with in this space.

https://github.com/rchain/Rholang

https://github.com/rchain/reference

There are many other people working on this as well.

---

**nootropicat** (2017-12-28):

Why not go all the way and make a second type of evm, parallel by default? All instructions in a block executing in deterministic parallel lockstep. It would allow full (maximum Amdahl’s speedup) parallelism, down to the subcontract level - and even to the point of multiple transactions cooperating. Atomic operations would have to be explicit, just like in a normal concurrent code. Easy to parallelize on a gpu.

---

**PiotrTrzpil** (2017-12-30):

Interesting idea.

Thought experiment about integrating it in the current ecosystem (as opt-in):

- incompatibility with delegatecall, though maybe it’s a good thing, considering its security (well, readability) issues
- seems difficult to have all-or-nothing integration between contracts - a message sent to contract may result in it running out of gas or failing and will have to reverted after the first contract finished successfully - unless the initial contract call (and all calls originating from it) could also be reverted in that case?
- difficulty in receiving results from other contracts - they would have to send back a message to another first contract’s function.
- contracts would likely need to be separated in disjoint universes - those supporting message passing, and those with normal calls.

---

**vbuterin** (2017-12-31):

> difficulty in receiving results from other contracts - they would have to send back a message to another first contract’s function.

Right. The only way a contract could get a response from another contract is asynchronously, with an “A runs, messages B, B runs, messages A, A runs more” workflow.

---

**tawarien** (2017-12-31):

Actors can indeed prevent the reentrancy problem (some cases of it) and introduce parallelizability.

But we should not forget that an asynchronous and concurrent System does introduce new problems and I think such a step has to be thought through very well.

Just some problems from the category of the mentioned return message.

If each actor has just one inbox/address then it can receive the return message to a sendt message only their and to ensure that only the receiver of the message can answer he has to remember its address, if he actually uses the provided asynchronicity then it has to manage a list of expected responses. It should deny the handling of response messages from as long as a response message is open or reentrancy is introduced again. Further, it must manage some timeout or another mechanism for the case, that the response message is not sent or else simply being malicious and not sending the response locks the whole actor.

Some actor models allow creating dedicated return inboxes/addresses for receive return message for sendt message, which would eliminate the need for managing the expected responses but would need the introduction of opaque addresses for the inboxes (to prevent someone from sending a message to it by forging it from a byte string), this would still not solve the other problems from above (just the sending management)

My personal opinion is that this model and Actor models where transactions run concurrently is good for increasing performance over parallelizability but worse in terms of security and robustness.

---

**kladkogex** (2018-01-02):

Imho Ethereum will inevitably need to move to some type of a concurrent model in the future.

Sharding introduces concurrency anyway - the only way for contracts across shards to talk to each

other will be to send messages.

Here is a [Wikipedia article on distributed transactions](https://en.wikipedia.org/wiki/Distributed_transaction) and [on two-phase commit](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)

Essentially in this model there is a coordinator contract and “slave” contracts

**Commit request phase**

1. The coordinator contract sends a query to commit message to all slave contracts and waits until it has received a reply from all slave contracts.
2. The slave contracts lock necessary resources and execute the transaction up to the point where they will be asked to commit. They each write an entry to their undo log and an entry to their redo log.
3. Each slave contract replies with an agreement message, if the action succeeded, or an abort message , if the action experiences a failure.

**Commit phase**

Success

If the coordinator received an agreement message from all slaves during the commit-request phase:

1. The coordinator sends a commit message to all the slaves.
2. Each slave completes the operation, and releases all the locks and resources held during the transaction.
3. Each slave sends an acknowledgment to the coordinator.
4. The coordinator completes the transaction when all acknowledgments have been received.

Failure

If any slave votes No during the commit-request phase (or the coordinator’s timeout expires):

1. The coordinator sends a rollback message to all the slaves.
2. Each slave undoes the transaction using the undo log, and releases the resources and locks held during the transaction.
3. Each slave sends an acknowledgement to the coordinator.
4. The coordinator undoes the transaction when all acknowledgements have been received.

It turns out there is a [XA standard for distributed transactions](http://pubs.opengroup.org/onlinepubs/009680699/toc.pdf), which is implemented in particular as [Java Transactions API](https://en.wikipedia.org/wiki/Java_Transaction_API#Java_Transaction_API) in Java Enterprise Edition.

I think Ethereum could initial implement these as a library on top of EVM, and then modify ERC-20 token standard to support transactions

> R-Chain is the project that I’m most familiar with in this space.

Are there distributed transactions in the R-chain project? How are they implemented?

