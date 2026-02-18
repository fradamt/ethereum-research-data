---
source: ethresearch
topic_id: 1269
title: Cross Shard Locking Scheme - (1)
author: MaxC
date: "2018-03-01"
category: Sharding
tags: [cross-shard]
url: https://ethresear.ch/t/cross-shard-locking-scheme-1/1269
views: 12581
likes: 13
posts_count: 33
---

# Cross Shard Locking Scheme - (1)

[@vbuterin](/u/vbuterin) [@JustinDrake](/u/justindrake)

The basic idea is to use read and write locks to ensure a transaction that references data on  many shards can be executed atomically.

Suppose we had a set S for the state/storage required by a transaction T– which specifies:

1. The address of a blob of data;
2. Whether a read or write lock is required
3. The ID of each shard where the blob of data is held

**Prepare Phase**

Before we can execute T, we  require that a set of locks L for storage S  be added to the block-chain. A lock  l \in L for a storage s \in S   is like a transaction except that it needs to be finalised by both the shard  where s is kept and T’s parent shard.

**Commit Phase**

Before T is executed,  we need to:

(1) present merkle proofs that  L has been added to the state of all shards referenced in S

(2) merkle branches for the storage of S.

Both (1) and (2) would need to be committed in T's shard before T can be executed and committed - otherwise no one in T's shard would be able to check T has been executed correctly.

**How can we prevent deadlock in this system?**

1. A simple solution is to have a time-out for lock-holding, which could be a certain block height, and to prevent a block from acquiring a lock for some time. This may be too slow.
2. A better solution would be  using block-chains to time-stamp transactions T using the block-height of T’s first reservation. With such a time-stamp, we could employ deadlock prevention using a wound-wait mechanism.

**Edit**: See this [post](https://ethresear.ch/t/cross-shard-locking-resolving-deadlock/1275) about resolving deadlock using the wound-wait scheme.

## Replies

**kladkogex** (2018-03-01):

There is a two-phase commit protocol


      [en.wikipedia.org](https://en.wikipedia.org/wiki/Two-phase_commit_protocol)




###

In transaction processing, databases, and computer networking, the two-phase commit protocol (2PC) is a type of atomic commitment protocol (ACP). It is a distributed algorithm that coordinates all the processes that participate in a distributed atomic transaction on whether to commit or abort (roll back) the transaction (it is a specialized type of consensus protocol). The protocol achieves its goal even in many cases of temporary system failure (involving either process, network node, communicat...








But it requires the client to be non-malicious

The question is how to modify this protocol to work on blockchain

I think you could simply modify the protocol above that one of the shards is the coordinator

But you should be able to send messages across shards

---

**MaxC** (2018-03-01):

![](https://ethresear.ch/letter_avatar_proxy/v4/letter/k/7993a0/48.png) kladkogex:

> en.wikipedia.org
>
>
> Two-phase commit protocol
>
>
> In transaction processing, databases, and computer networking, the two-phase commit protocol (2PC) is a type of atomic commitment protocol (ACP). It is a distributed algorithm that coordinates all the processes that participate in a distributed atomic transaction on whether to commit or abort (roll back) the transaction (it is a specialized type of consensus protocol). The protocol achieves its goal even in many cases of temporary system failure (involving either process, network node, communicat…

It certainly seems like that would be reasonable. My main worry would be that if just one collation fails all would have to roll back. I like the idea of one shard acting as a coordinator.

You might also have a coordinator shard build up a global waits for graph for all the other shards, which maintain their own waits for graphs.**Q:** how does a shard determine who is waiting on whom - request merkle witnesses from honest nodes in another shard?

---

**MaxC** (2018-03-01):

Was reading about your other post on Scilla by Zilliqa. A key point to their system is this:

```
In addition to performing computations with the components of the
incoming messages and parameters of the contract, every transition
can manipulate with the state of a contract itself,i.e. read/write
from/to its mutable fields, as well as read from the blockchain
```

We could emulate this in our sharding system: just have public reads for the blockchain and private data stored within a contract - that way we would not need a locking system. I reckon that’s probably ok - would be interested to hear what others think.

---

**vbuterin** (2018-03-02):

The problem I have with locking mechanisms is that they prevent any other activity from happening while the lock is active, which could be extremely inconvenient for users. In the train-and-hotel example, a single user would be able to stop all other users from booking trains or hotels for whatever the length of the lock is. Sure, you could lock individual train tickets, but that’s already a fairly application specific solution.

I think the best solutions to these problems are those solutions that recognize that shards are virtual galaxies, and not physical sets of computers, and so the nodes executing two shards can, eg. with stateless client witness protocols, temporarily be merged for one block.

As I mention [here](https://ethresear.ch/t/merge-blocks-and-synchronous-cross-shard-state-execution/1240), you can even cycle through “leader shards” in each round, where transactions from the leader shard are executed first and can read and write across shards, and executors on both the leader shard and followe shards use stateless client techniques to execute the part of the operations that are happening on shards that they are not native to.

---

**MaxC** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The problem I have with locking mechanisms is that they prevent any other activity from happening while the lock is active, which could be extremely inconvenient for users. In the train-and-hotel example, a single user would be able to stop all other users from booking trains or hotels for whatever the length of the lock is. Sure, you could lock individual train tickets, but that’s already a fairly application specific solution.

Sounds like a good solution - I the analogy of shards as galaxies.

My one issue: guess multi-shard transactions would broadcast themselves to every shard, anticipating the next leader. However, if these multi-shard transactions were to be larger than one block - say 1/2 of  all transactions but there were 200 shards, then multi-shard transactions would only broadcast  at 1/200 the rate of other transactions.

---

**kladkogex** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png) MaxC:

> We could emulate this in our sharding system: just have public reads for the blockchain and private data stored within a contract - that way we would not need a locking system. I reckon that’s probably ok - would be interested to hear what others think.

Yes - smartcontract internal state is already enough for concurrency since the private data stored within a smartcontract is guaranteed to have sequential access.

What is needed is modify EVM to provide a way to send messages from EVM to other smartcontracts. In the simplest case one would add a pre-compiled “send_message” smartcontract.

Then another question is how to modify Solidity to add language features for sending messages and defining  a function which is called when the other party responds to  your message.

Many languages, such as Erlang and Scala have convenient ways to define asynchronous messaging/continuations.

For Solidity the simplest would be  to add a “message” keyword, that would take as an argument the solidity function which will called when a response to the message is received.

---

**musalbas** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> The problem I have with locking mechanisms is that they prevent any other activity from happening while the lock is active, which could be extremely inconvenient for users. In the train-and-hotel example, a single user would be able to stop all other users from booking trains or hotels for whatever the length of the lock is. Sure, you could lock individual train tickets, but that’s already a fairly application specific solution.

I don’t think it has to be application specific. You don’t have to lock the state of the entire contract, you can just lock the specific storage keys accessed by the smart contract. Each key can represent a different ticket. Am I missing something?

A good locking system should allow multiple concurrent writes to the state of the system, otherwise that defeats the whole point of sharding anyway.

---

**MaxC** (2018-03-02):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> The problem I have with locking mechanisms is that they prevent any other activity from happening while the lock is active, which could be extremely inconvenient for users. In the train-and-hotel example, a single user would be able to stop all other users from booking trains or hotels for whatever the length of the lock is. Sure, you could lock individual train tickets, but that’s already a fairly application specific solution.

I had imagined a scheme where you program a smart contract and also specify what parts of state the scheme accesses, or alternatively build a separate function that tells you which part of the state can be accessed based on given inputs to the smart contract, or even have a compiler do that.

---

**musalbas** (2018-03-02):

Right, the client submitting the transaction can just execute the transaction and include which storage keys the smart contract is accessing in the transaction. Which is what is happening anyway in the “access_list” parameter of the [new proposed transaction format](https://github.com/ethereum/sharding/blob/develop/docs/doc.md). I don’t think the programmer has to explicitly define what needs to be locked.

Regardless of what cross-shard atomic commit scheme is used, I think there should be some inherent concept of a “unit of concurrency” anyway – that is, some state that people can only write to one at a time, synchronously (e.g. a storage key). At the moment Ethereum doesn’t really have that, because miners can include transactions in the chain in any arbitrary order, which means if you submit a transaction to the blockchain, it might not have the result you expected, if for example someone else submits another transaction for the same contract 1 second before you do. For cross-shard atomic commit to work well, I think this should be fixed so that transactions have to be processed in the correct order, because this could result in some bad inconsistencies in the state of the system.

---

**MaxC** (2018-03-03):

FW: [@vbuterin](/u/vbuterin)

I think you are right [@musalbas](/u/musalbas).  An issue is that access lists require trust from the point of view of the client submitting the transaction. A malicious client could specify more than needs to be accessed. However,  a validator executing the code after a client could just minimise these access lists, and then request the locks. If the validator requests state that’s too large, he can be slashed, by including his transaction along with an access list minimised version on chain.

You could also associate a refundable rental fee associated with holding onto locks, which would be great if validators where the ones who “bought” locks, rather than clients. The rental fee is returned to validators if they release locks in a timely manner after a transaction has been added to the blockchain.

---

**vbuterin** (2018-03-12):

I’m going to try to re-express this in my own framework.

Suppose there is a transaction that needs to access resources R[1] … R[n] on shards S[1] … S[n] (we’ll say for simplicity one resource per shard; the generalization to multiple resources in one shard is obvious), where the “home shard” is S[1]. First, a transaction needs to be included in every S[i], which calls the LOCK opcode with arguments (T, R[i], S[1]), for some transaction identifier T. This locks resource R[i], preventing its state from being modified, and targets the lock to S[1]. Every shard’s state maintains a data structure {shard: locks}, storing for every other shard the set of locks that are targeted to that shard.

It is understood that in order to execute the state at block N of any shard S[i], the client needs to have available the state roots of block N-10 of every other shard, and must also download the entire currently active set of locks targeted to S[i] of every shard (this can be trivially downloaded and authenticated against the state roots of the other shards). Now, when a transaction whose hash is T executes, it can read all locked resources R[1] … R[n], perform some computation, and then suggest new contents for the state of each resource. The shard creates a “release lock” message, targeted to each shard, which also specifies what to set the resource’s new state to; additionally, the shard stores in its own internal state a record saying that that instance of a resource lock cannot be used again. Whenever this release message is included into any other shard via a Merkle proof, that shard sets the new state of the resource to the given value, and the lock is deleted.

This does require any node executing a block on a shard to be aware of more data from other shards, but it does seem to work.

---

An alternative mechanism, where execution can depend on state roots only (reminder: for simplicity I’m that state roots can be used to Merkle-prove logs, so we don’t need to worry about state and receipt roots separately), is as follows:

1. The resource must be locked on every shard, and the lock generates a simple log that specifies the target shard and transaction ID.
2. The receipts proving that all locks have been made need to be included into the target shard.
3. The transaction on the target shard issues logs, that contain the new values for the locked resources.
4. The values can be unlocked and set to their new values on the original shard by including the receipts generated by the target shard.

This keeps the model of what cross-shard knowledge is required for executors to have the same as it was before, and pushes the work of actually performing the cross-shard operation to users.

I actually like this; it seems fairly simple.

---

**musalbas** (2018-03-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This keeps the model of what cross-shard knowledge is required for executors to have the same as it was before, and pushes the work of actually performing the cross-shard operation to users.

This is similar to the method used in OmniLedger. This works well for applications where the user is locking a state that only they can modify, such as spending a UTXO, because if they lock a UTXO that belongs to them, but then do nothing, then the user is only harming themselves. But if the user locks an object that can be accessed by anyone, such as a hotel ticket that can be bought by anyone, then if the user locks a hotel ticket and does nothing, then no one else can buy that hotel ticket. Pushing the cross-shard operations to clients means that we also rely on the client to be honest to guarantee liveness. In 2PC-style protocols (i.e. [S-BAC](https://ethresear.ch/t/sharded-byzantine-atomic-commit/1285)), the liveness property relies on the shard being honest instead.

---

**vbuterin** (2018-03-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> But if the user locks an object that can be accessed by anyone, such as a hotel ticket that can be bought by anyone, then if the user locks a hotel ticket and does nothing, then no one else can buy that hotel ticket.

Not necessarily. Remember that whoever wants to buy the hotel ticket next can just submit all of the required transactions to unlock the object themselves. Though there definitely are complexities around gas accounting here that need to be understood much better.

---

**musalbas** (2018-03-12):

What happens when there is a deadlock then, and two conflicting locks are held on two different shards? We either to trust that the clients will resolve this on their own, or have a timeout for locks to deal with bad clients as proposed in the original post, which means no one can buy that hotel ticket for the duration of the timeout.

Indeed there are questions about gas accounting, i.e. should we charge for failed transactions? If we don’t charge for failed transactions, then an attacker can keep locking an object for free, preventing anyone else from spending it, under this model.

---

**MaxC** (2018-03-12):

A timeout is not strictly speaking necessary, if we use a wound-wait approach which could be executed by the shards.The shards should be resolving deadlock, even if they are not doing most of the work acquiring locks.

---

**musalbas** (2018-03-12):

Is that similar to the [wound-wait](https://ethresear.ch/t/cross-shard-locking-resolving-deadlock/1275) mechanism proposed? There is still a question what happens if T_j never releases its locks in case 2, no?

If the shards should be resolving the deadlock, that begins to look like 2PC. ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=9)

---

**vbuterin** (2018-03-12):

> What happens when there is a deadlock then, and two conflicting locks are held on two different shards?

How is that possible? Control of what a resource is locked to is based on the shard on which the resource is located, so you can’t have two contradictory locks.

---

**MaxC** (2018-03-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/musalbas/48/3251_2.png) musalbas:

> If the shards should be resolving the deadlock, that begins to look like 2PC.

Yes, definitely would want to borrow that part from your scheme. It’s clever.  ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=12) However, will say that I think the benefit of a wound wait is that not all locks beed to be acquired in the same round.

---

**MaxC** (2018-03-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How is that possible? Control of what a resource is locked to is based on the shard on which the resource is located, so you can’t have two contradictory locks.

Suppose two transactions T_1 and T_2 might both need resources A and B.  T_1 has a lock on A and T_2 has a lock on B in different shards.

We need to find a way for resolving these deadlocked transactions.

One way is to say: all locks are sent to all shards, then deadlock can be  avoided. However, that would reduce the benefits of scaling as data for all transactions would be sent to all shards. So instead, we just send lock data to relevant parties, but then we need a way to resolve deadlock.I suggested a wound-wait approach.

---

**musalbas** (2018-03-12):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How is that possible? Control of what a resource is locked to is based on the shard on which the resource is located, so you can’t have two contradictory locks.

Let’s say you have a transaction T1 that needs access to two resources, located on two different shards, such that it needs to do the following operations:

1. LOCK (T1, R[0], S[0])
2. LOCK (T1, R[1], S[1])

Then let’s say another transaction T2 comes in that wants access to the same resources:

1. LOCK (T2, R[0], S[0])
2. LOCK (T2, R[1], S[1])

Then let’s say this is what actually gets executed:

1. LOCK (T1, R[0], S[0])
2. LOCK (T2, R[1], S[1])

Now, neither T1 or T2 can proceed, hence deadlock.


*(12 more replies not shown)*
