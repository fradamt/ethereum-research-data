---
source: ethresearch
topic_id: 7602
title: "Terminology: What do we call \"witness\" in \"Stateless Ethereum\" and why it is appropriate"
author: AlexeyAkhunov
date: "2020-06-27"
category: Execution Layer Research
tags: [stateless]
url: https://ethresear.ch/t/terminology-what-do-we-call-witness-in-stateless-ethereum-and-why-it-is-appropriate/7602
views: 2984
likes: 20
posts_count: 12
---

# Terminology: What do we call "witness" in "Stateless Ethereum" and why it is appropriate

In order to communicate our ideas and designs more clearly, we need good terminology. There is an opinion that the “Stateless” is not a good term for what we are trying to design, and I tend to agree. We might need to move away from this term in our next pivot. For now lets see if “Witness” is an appropriate term. From my point of view, it is. This is why.

The way Ethereum state transition is usually described is that we have environment `E` (block hash, timestamp, gasprice, etc), block `B` (containing transactions), current state `S`, and we compute the next state `S'` like this:

`S' = D(S, B, E)`

where `D` is a function that can be described by a deterministic algorithm, which parses the block, takes out each transaction, runs it through the state, gathers all the changes to the state, and outputs the modified state.

The same action can be viewed in an alternative way:

`HS' = ND(HS, B, E)`

where we have a non-deterministic algorithm `ND`, which takes merkle hash `HS` of the state as input, instead of the state `S`. And it outputs merkle hash of `S'`, which is `HS'`, instead of the full modified state.

How does this non-deterministic algorithm work? It requires a so-called oracle input, or auxiliary input, to operate. This input is provided by some abstract entity (the Oracle) that knows everything that can be known, including the full state `S`. For example, imagine that the first thing that the block execution does is reading balance of an account `A`. Non-deterministic algorithm does not have this information, so it needs the Oracle to inject it as a piece of auxiliary input. And not only that, the non-deterministic algorithm also needs to check that the Oracle is not cheating. Essentially, the Oracle will provide the balance of `A` together with the merkle proof that leads to `HS`, this will satisfy the algorithm that it has the correct information and it will proceed.

Why is this kind of algorithm called non-deterministic? Because it cannot “force” the Oracle to do anything, it is completely up to the Oracle whether the algorithm will ever succeed in computing `HS`’. The Oracle can completely ignore the algorithm and never provide the input, and the algorithm will just keep “hanging”. The Oracle may also provide wrong input, in which case algorithm will most probably fail (because the input will not pass the merkle proof verification). Why “most probably”? Because if the Oracle is very very powerful, it may be able to find preimage for Keccak256 (or whatever hash function we are using in the Merkle tree) and forge merkle proofs of incorrect data. Although this may happen, it is very unlikely, and the degree to which we are sure it won’t happen is called “soundness”.

What about the term “witness”? Often the auxiliary input that the Oracle provides to a non-deterministic algorithm is called “witness”. Therefore it is appropriate to call the pieces of merkle proofs that we would like to attach to blocks or transactions “witnesses”. If we look at the “Stateless” execution as a non-deterministic algorithm, then it all makes sense ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

“Witness” is a more general term than “merkle proof”, because there could be other types of witnesses, for example, proofs for polynomial commitments, SNARKs, STARKs, etc.

Hope this helps someone

![:heart_eyes:](https://ethresear.ch/images/emoji/facebook_messenger/heart_eyes.png?v=14)

## Replies

**vbuterin** (2020-06-27):

What’s the value in looking at stateless execution as a non-deterministic algorithm? My mental model has always been:

`S' = D(S, B, E)`

`HS' = D'(HS, B, E, W)`

So the witness is explicit.

---

**AlexeyAkhunov** (2020-06-27):

To justify the use of the term ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=14)

---

**AlexeyAkhunov** (2020-06-27):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What’s the value in looking at stateless execution as a non-deterministic algorithm?

Also because I wanted to point out, purely theoretically, of course, that these two modes (with full state and with hash + witness) have different soundness, first being 100%, the second being 99.999999…999 %

![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

I want to use it as a taster for developing better terminology for state, blocks, etc., otherwise discussion of things like ReGenesis and Stateless Ethereum can become confusing very quickly (for most people)

---

**vbuterin** (2020-06-28):

BTW somewhat unrelated but: I know other people have said that “stateless” is a bad term as there’s “technically” still a 32 byte state, but I actually think it’s still a good term to use. Reasons:

1. The fact that the state is O(1) sized makes it possible to make the state transition function in the code itself actually be a pure function, as opposed to some awkward thing with a hook to a database.
2. Stateless clients wishing to verify the chain can verify blocks out of order, reducing the extent to which those 32 bytes really are a meaningful “state” from the client’s point of view. This may be a good idea particularly in the “verify only a randomly selected 1% of blocks or if you hear an alarm” mode of verification.
3. (2) applies even more strongly in the sharding context, where validators jump around between shards every epoch!

---

**AlexeyAkhunov** (2020-06-28):

That is a good comment, thank you. Perhaps what we need in an extension rather than a replacement. We establish terminology that will include Stateless client as a special case, while also supporting things in between (due to various trade-offs)

---

**dankrad** (2020-06-29):

I think the last point is why I would like to change terminology from “stateless Ethereum” to “witnessed Ethereum” or something alike. Stateless sounds like everyone would be forced to be stateless, which sounds bad because some people believe that then everyone will have to be sure to store and maintain their own state. However, this is definitely not what we want: We actually want to achieve a system that for the end user will probably look very similar to today’s Ethereum (except that they will query an additional actor to get state), but nodes can choose where they are on the “state” spectrum, including fully stateless.

---

**vbuterin** (2020-06-29):

What’s wrong with the original term “stateless clients”? I’m actually not sure where “stateless ethereum” came from…

I worry any other term than stateless will fail to communicate to even semi-lay people what the initiative is fundamentally about, which *is* making it so people don’t have to store state.

---

**AlexeyAkhunov** (2020-06-29):

The reason I did not like the term “stateless clients”, is because of the word “clients”. I think “client” is rather ambiguous, specially if you start talking about it in a business context, where “client” has a very strong meaning, which is someone who pays money. Therefore, I would prefer to use term “Ethereum implementation”, because it is fine in most contexts. That is why I encouraged the shift of terminology towards “Stateless Ethereum”, with the additional benefit that it is clear that we talk about Ethereum, and not something else which also has “clients”.

I do not think we should worry about improving terminology and replacing/extending terms, because I would not like to sacrifice clarity of communication between researchers over “marketing” to semi-lay people.

---

**vbuterin** (2020-06-29):

Stateless validation?

---

**dankrad** (2020-06-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> What’s wrong with the original term “stateless clients”? I’m actually not sure where “stateless ethereum” came from…

There are people out there who claim/believe that if all nodes don’t store the state anymore, individual users will have to…

https://twitter.com/bcmakes/status/1276554303964999681

---

**poemm** (2020-06-30):

Some alternatives to “stateless”:

- bounded-state
- partial-state
- minimal-state
- semi-stateful/semi-stateless
- witness-dependent
- witness-constrained
- witnessful
- witnessed (suggested by @dankrad above)
- state-averse
- statephobic (state + Greek root for fearing)
- witnessphilic (witness + Greek root for loving)

![](https://ethresear.ch/user_avatar/ethresear.ch/alexeyakhunov/48/220_2.png) AlexeyAkhunov:

> I do not think we should worry about improving terminology and replacing/extending terms, because I would not like to sacrifice clarity of communication between researchers over “marketing” to semi-lay people.

I agree that “stateless client” may be colloquial. But we should write somewhere that this is an abuse of language, to prevent confusion.

