---
source: ethresearch
topic_id: 1446
title: Cross-shard Communication & Developer Experience
author: jonchoi
date: "2018-03-21"
category: Sharding
tags: [cross-shard, developer-experience]
url: https://ethresear.ch/t/cross-shard-communication-developer-experience/1446
views: 4220
likes: 19
posts_count: 7
---

# Cross-shard Communication & Developer Experience

This thread is just a reminder from the conversation in Taipei this morning. Wanted to open up the conversation to the entire Ethereum community. cc [@vlad](/u/vlad) [@vbuterin](/u/vbuterin) [@karalabe](/u/karalabe) [@pipermerriam](/u/pipermerriam)

**context** cross-contract communication may push complexity out of the protocol layer to the developer experience. for example, train-and-hotel problem requires service providers to provide ability to hold and reserve but revert within a time out period.

**tl;dr** we should engage with the dapp developer community and the broader developer communities to identify the best programming patterns & abstractions to handle this problem, and design sharding with the end product (devEx) in mind.

Relevant posts:



    ![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png)
    [Merge blocks and synchronous cross-shard state execution](https://ethresear.ch/t/merge-blocks-and-synchronous-cross-shard-state-execution/1240) [Sharding](/c/sharding/6)



> We know that with merge blocks and clever use of fork choice rules, we can have a sharded chain where a block on one shard is atomic with a block on another shard; that is, either both blocks are part of the final chain or neither are, and within that block there can be transactions that make synchronous calls between the two shards (which are useful for, among other things, solving train-and-hotel problems). However, there remains a challenge: how do we do state execution for such blocks? That …



    ![](https://ethresear.ch/user_avatar/ethresear.ch/maxc/48/675_2.png)
    [Cross Shard Locking Scheme - (1)](https://ethresear.ch/t/cross-shard-locking-scheme-1/1269) [Sharding](/c/sharding/6)



> @vbuterin @JustinDrake
> The basic idea is to use read and write locks to ensure a transaction that references data on  many shards can be executed atomically.
> Suppose we had a set S for the state/storage required by a transaction T– which specifies:
>
> The address of a blob of data;
> Whether a read or write lock is required
> The ID of each shard where the blob of data is held
>
> Prepare Phase
> Before we can execute T, we  require that a set of locks L for storage S  be added to the block-chain. A lo…

concurrency and async models from js, golang, rust and erlang were mentioned this morning. also, locks, mutex, channels, promises etc. everyone feel free to chime in. just starting the thread for everyone ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

## Replies

**rauljordan** (2018-03-21):

Hey [@jonchoi](/u/jonchoi), thanks for starting this thread. In the conversation this morning, we mentioned that it is critical to get the opinion of dApp developers on this thread. Otherwise, we would all propose biased async models as Peter mentioned. There are as many arguments in favor of callbacks or promises vs. channels as there are against them.

My suggestion is if we can condense some of our thoughts here initially and relay this over a more mainstream communication channel to weigh in the dApp developers’ thoughts. I am personally more aligned with Golang’s channel concurrency model, which I will elaborate on for those unfamiliar.

At its core, channels are a messaging abstraction that allow concurrent threads to communicate through a common pipe that can accept different types of events. Threads can listen to events that occur on a common channel and react accordingly. As an example, I can create a simple, Marco - Polo messaging system with one thread that says “Marco” every second, broadcasts it to a common channel, and another thread that pipes “Polo” to the standard output upon receiving the message as follows:

```auto
func main() {
  marcoPolo := make(chan string, 16)
  go sayMarco(marcoPolo)
  go sayPolo(marcoPolo)
}

func sayMarco(c chan string) {
  for {
    time.Sleep(time.Second)
    c<- "Marco"
  }
}

func sayPolo(c chan string) {
  for {
    marco := <-c
    fmt.Printf("%s Polo\n", marco)
    time.Sleep(time.Second)
  }
}
```

I like this model because it allows easy modularity of code by having a single channel that is as independent of external context as possible. (the only dependency is the common channel that can accept messages). This can mesh really well with the idea that different shards can serve different purposes and should not be as coupled with each other. [@vbuterin](/u/vbuterin) shared his idea this morning that all shards should be a parametrization of a common interface, and this model can allow us to standardize a set of channels for cross-shard concurrency,  but still allow shards to perhaps be application specific in certain ways.

Also, I fully acknowledge my thoughts can be biased towards Go, so I urge we get this out to a mainstream community communication channel asap.

---

**karalabe** (2018-03-21):

Regarding the Go channel paradigm (or rather Communicating Sequential Processes in general), it’s a interesting question whether Go’s or Erlang’s approach would map better to the Ethereum use case.

In Go, threads (goroutines in Go world) are independent entities from channels, and every goroutine can read/write arbitrary channel it knows about. This is allows channels to be used as a building block themselves, but requires them to be elevated to first-class citizen status in the protocol.

Erlang has a more limited implementation of CSP, where threads (soft-threads in Erlang world) have each a single mailbox that can receive messages. The soft-thread can pop off and react to messages in its mailbox, also supporting some form of pattern matching for prioritization.

In both of these models Ethereum contracts would map to these isolated threads (goroutines/soft-threads), which feels natural, as we can just treat contracts as independent actors. However, when it comes to the communication primitive, Erlang’s mailboxes might be simpler and more natural than Go’s channels:

- If we tightly couple receiving message queues with contracts (i.e. mailbox approach) opposed to having them as separate first-class building blocks (i.e. channel approach), the protocol is significantly simplified addressing wise, since the recipient is just the contract address and there’s no need for a second id scheme.
- If we go with a single mailbox per contract, we could support some form of messages filtering in the receiving contract which could allow for example to make certain messages (system) have higher priority than others (user).

An interesting question an outsider might ask is why Go went with a more complex approach vs. Erlang, and the answer is that Go channels are much more powerful in that my thread can selectively wait on only certain channels, and can send around channels to make extremely powerful sync structures. Those however are neither needed nor feasible in a smart contract platform, so I’d rather go with simple rather than flexible.

---

**veqtor** (2018-03-26):

As a solidity, js, python & java developer, considering that solidity is loosely based around js, I would like to see a promise/RxJS hybrid solution.

Consider the following function:

get value a from contract on shard A, combine with value from contract on shard B

write result to contract on shard C

write result to contract on shard D, if failed, rollback previous write to shard C

Ideally I would like to implement this, in Solidity as:

```
ContractOnA.getValue().zipWith(ContractOnB.getValue(), {a, b -> a+b})
   .subscribe(v ->
            ContractOnC.setValue(v);
            ContractOnD.setValue(v+1);
   )
   .onError(revert()) //revert all writes!
```

The idea here being, that any contract call from an external shard returns an “asynchronous” single result, kind of like in Rx.

Things become more hairy when you take the result of writing as a value to a downstream operation:

```
ContractOnA.getValues() //could be a list
   .flatMap(v -> ContractOnB.saveValueReturnId(v))
   .flatMap(id -> ContractOnC.writeId(id))
   .reduce(a, v -> if(v != 0x0) a++;
   .subscribe(res -> ValuesUpdatedEvent(res))
   .onError(revert()) //Now you have to revert every written value on line 2 & 3!
```

With this model, other interesting this could be performed such as:

```
getValues().flatMap(
   vals -> Flowable.fromArray(vals).map(v -> (v, sha3(v)))
)
.flatMapCompletable((v, sha3v)->storeValue(v, sha3v)
.subscribe()
```

I think this also hold merit if in the ABI, observables, single, etc, can be returned if declared as external views.

Especially if one could observe certain values as a “live” value:

```
function getUsers() external view returns(Observable) {
   return Observe(userIds) //observe transforms object into "live" data updated with every block
   .map(uid -> getUser(uid));
}
```

---

**kladkogex** (2018-03-30):

Imho this field is well studied as distributed transactions.

The only thing you need is reliable asynchronous messaging across smartcontracts and shards. Everything else can be implemented on top of reliable asynchronous messaging, as [explained here for example (https://www.ibm.com/developerworks/library/ws-wstx1/).

If asynchronous reliable messages are introduced, then people could develop libraries for all kinds of transactions, locks etc …

So the Ethereum core may need to know much about the higher level abstractions, as they would be implemented on top of the messaging framework.

It is good to have a universal abstract framework to send a messages across shards and from shard to main chain.

Then a particular model (Erlang, Akka etc.) could be implemented on top of the asynchronous messaging so people could experiment …

---

**Chjango** (2018-04-14):

We may be able to emulate Cosmos’ IBC protocol within the EVM across smart contracts. IDK what that looks like right now but this is something to consider.

---

**FrankSzendzielarz** (2018-04-14):

Agreed that this is about distributed transactions. I feel too out of the picture to comment in confidence, but from what I have read so far sharding is an architecture that results in many EVMs (or components of them) rather than one, hence the emergence of discussions about transactional consistency in a distributed environment.

For what it is worth, microservices is a hot topic in the business systems development world at the moment, and these kind of issues are at the forefront of many developers’ minds. “Eventual consistency” , “Materialised views”  and the like.

Intuitively, I don’t feel ‘atomicity’ belongs to this kind of problem. Atomicity is something I tend to expect to happen at a very low level on single machines (or shards) when dealing with things that happen in very quick time frames. The “train and hotel” problem feels more like a long running business process, where failures must be handled using compensation rather than atomicity. At least, that’s my experience and gut feel thus far.

Compensation of failed business processes in the context of Ethereum means further gas expense. I wonder what the economics should look like there.

