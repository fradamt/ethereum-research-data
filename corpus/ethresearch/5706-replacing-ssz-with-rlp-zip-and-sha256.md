---
source: ethresearch
topic_id: 5706
title: Replacing SSZ with RLP, Zip and SHA256
author: atoulme
date: "2019-07-05"
category: Sharding
tags: []
url: https://ethresear.ch/t/replacing-ssz-with-rlp-zip-and-sha256/5706
views: 4531
likes: 34
posts_count: 13
---

# Replacing SSZ with RLP, Zip and SHA256

[SSZ](https://github.com/ethereum/eth2.0-specs/blob/a63de3dc374148fe8adacd8718f67f8c7ba54f2e/specs/simple-serialize.md) stands for Simple SerialiZe.

You can read on some of the background and needs of SSZ from Raul Jordan [here](https://rauljordan.com/2019/07/02/go-lessons-from-writing-a-serialization-library-for-ethereum.html).

Ethereum already has a serialization format called RLP (recursive length prefix).

SSZ allows for a few more things.

### Deterministic lookup of an element in the bytes

You can look at the bytes of the SSZ output, and if you know what the data structure is, you can look up the bytes of one of the fields of the data structure directly.

### Merkle hash partial computation

These are called SSZ partials. You can easily update the SSZ representation and recompute the hash without recomputing from scratch.

So SSZ has been meant for hashing in an efficient manner, offering optimizations. However we haven’t really checked if those optimizations work well or help meaningfully at runtime, it’s a spec after all right now.

#

OK so the whote text reads:

> There is no doubt that the grail of efficiency leads to abuse.
> Programmers waste enormous amounts of time thinking about,
> or worrying about, the speed of noncritical parts of their programs,
> and these attempts at efficiency actually have a strong
> negative impact when debugging and maintenance are
> considered. We should forget about small efficiencies,
> say about 97% of the time: premature optimization is the root of all evil.

[![image](https://ethresear.ch/uploads/default/optimized/2X/9/91c92110fb0cde04e0a19bdde97e79df71993739_2_200x295.png)optimization_2x.png569×840 36.5 KB](https://ethresear.ch/uploads/default/91c92110fb0cde04e0a19bdde97e79df71993739)

Pretty damning, but let’s not forget the remaining 3%:

> Yet we should not pass up our opportunities in that critical 3%.
> A good programmer will not be lulled into complacency by such reasoning, he will be wise to look carefully at the critical code; but only after that code has been identified.
> It is often a mistake to make a priori judgments about what parts of a program are really critical, since the universal experience of programmers who have been using measurement tools has been that their intuitive guesses fail.
> After working with such tools for seven years, I’ve become convinced that all compilers written from now on should be designed to provide all programmers with feedback indicating what parts of their programs are costing the most; indeed, this feedback should be supplied automatically unless it has been specifically turned off.

Enter implementation.

The optimization implied by deterministic lookup is that you would be able to program so that it’s possible to just keep the bytes of an object in SSZ encoding. It would also be able to use streaming.

In multiple occasions, folks who went down that route with ETH 1 over RLP mentioned there had been very little performance optimization using this method.

It actually makes implementation cumbersome and prone to breakage.

A few objects are encoded to SSZ with ETHv2. One of them is the block, and it’s used in interesting ways:

- You have to use it in epoch processing to update it.
- You gossip it over the network to other peers.
- You store and index it locally.
- You receive blocks over the network and will need to verify them

It quickly becomes natural to have a in-memory representation of the object as a set of structs that can be tested, debugged, mocked and so on.

SSZ partials also suffer from complexity and constrain the use case. They require to keep a merkle tree around associated with the object, and each implementer team ends up creating quite a bit of code to support that use case.

Most likely for the longest time, until proven otherwise, implementers will rehash objects after updating them in their DSL so they can get a new hash for them, recreating the SSZ byte representation every time.

# Lazy, lazy, lazy

Coders are lazy. Let’s use it to our advantage and run here and now a thought experiment.

Take a business object of some sort, and use RLP to push it to bytes.

Why RLP? There is an implementation of RLP in every language out there already. It is used in prod by ETHv1. But you can do a mental switch to something mature and used out there today, as long as it is absolutely deterministic.

So you get those RLP bytes, now let’s stream those bytes into a zip compression stream. Same as before - use whatever mean is your favorite, with those requirements: compression must be implemented in all languages, deterministic and if possible so common it’s hardware accelerated.

Finally, compute a hash of the zip stream using SHA256. Again, same requirements.

You get a hash for your object. You streamed so you hopefully didn’t clog heap space with bytes. You have a reasonably fast throughput so you can redo this on a whim.

# Is this even efficient?

Well two ways:

## It simplifies concepts

I quote [Ben Edgington](https://media.consensys.net/exploring-the-ethereum-2-0-design-goals-fd2d901b4c01): “simplicity is not just about lines of code, it is primarily about the concepts we are implementing.”

## It helps dev stay lazy

This liberates head space so we can move on to bigger and better things, and lowers the bar for contribution.

## Replies

**jrhea** (2019-07-06):

This idea is useful for several reasons. The churn in SSZ is costly for 8 client teams to constantly be reimplementing and trying to understand.  If nothing else, we should consider the use of a practical scheme like Antoine proposed while the EF figures out these optimizations (and if they are worth the trouble). This is the kind of pragmatism that could significantly speed up development, testing and interop.  I strongly suggest we start adopting a practical approach to this going forward if we want to finish anytime soon.

---

**shahankhatch** (2019-07-06):

I’m in support of the motivations stated.

Some comments on the tech side. afaik SHA256 is a (block-based) compression stream. It requires padding of the input for compressions streams to work. If I am interpreting this correctly, it’s better to pad the core content instead of padding a zip stream since implementations will then need to discard padding from what is supposed to be (pure?) zipped content. The zip step may also be skipped as a way to avoid iterating over two streams sequentially with CPU-dependent activities (hash then zip). Alternatively, if zip is essential because of large content, then the content and its sha256 can be zipped together. This then makes the zip algo configurable based on environment and doesn’t become part of the protocol.

wdyt?

---

**Mikerah** (2019-07-06):

Another thing that we should consider as well is bridging ETH1 data over. ETH1 already makes heavy use of RLP and supports SHA256 out-the-box. Moreover, your changes would simplify a lot at the networking layer since we wouldn’t need to marshall/un-marshall data on the wire like we would have to do currently.

---

**ralexstokes** (2019-07-06):

[@atoulme](/u/atoulme) a very useful feature of `ssz` is that we can make point-wise proofs against the data it encodes. if i have a ssz container with fields A, B and C i can in turn make succinct proofs about the existence of A B and C with respect to the ssz hash tree root of this container. this functionality allows for expedient light clients which in turns promotes a healthy decentralized network. how do we get this same functionality w/ this scheme?

---

**Mikerah** (2019-07-06):

So features like these arent’ exactly obvious on a first glance when looking through the ssz spec. It would be great to have a side-by-side comparison of ssz and rlp.

---

**jrhea** (2019-07-06):

Perhaps a dumb question, but is that feature necessary for phase 0?

---

**ralexstokes** (2019-07-06):

no dumb questions, only dumb answers ![:wink:](https://ethresear.ch/images/emoji/facebook_messenger/wink.png?v=14)

depends on what you call necessary. here’s an example use case you may find motivating: by having a nice way to make proofs about data on the beacon chain, you can write efficient light clients for the beacon chain. one thing you can do w/ good eth2 light clients is make a two-way bridge b/t eth1 and eth2.

the deposit contract serves as a one-way bridge to the phase 0 network. you could imagine an eth1 smart contract that consumes beacon chain headers to form a light client of the beacon chain. you could then conceivably move beacon eth back to the proof-of-work chain by presenting a merkle proof that you somehow burned the corresponding amount of beacon eth. (note there isn’t a clear path in the frozen spec to do this last part – i could slash myself in a certain way and we could all agree that this slashing is grounds for eth1 revival – but the particulars are taking us off-topic, i merely want to exercise the mechanism to show you its possible)

ssz provides a single coherent way to make arbitrary proofs about eth2 state – given the tree structure of the stuff we care about, you can walk any sequence of beacon chain block headers and reach any piece of data on-chain in a verifiable manner; while we could continue debating how necessary it is for phase 0, it definitely lays the ground work for future phases and preserves optionality in client design as we learn more about how to build good p2p software

---

**atoulme** (2019-07-07):

Zip was the portion of the shower thought I’d use to justify using less memory since we wouldn’t keep a complete byte data structure around, streaming instead. But if SHA256 digests stream just as well, we can use that. Pretty sure we’d know in a couple hours running tests.

---

**atoulme** (2019-07-07):

We don’t get this functionality with the approach I described.

I would happily make my hashing functions flexible and upgradeable so we can easily version up and change the behavior down the road though. Being a lazy developer, I’d only implement minimally what is required to get my job done. So when SSZ brings business value with a use case such as the one you mention, we can move to it.

The point is not SSZ is bad or my hashing is better than yours, it’s that we should always have a tight feedback loop between coding and business value.

---

**atoulme** (2019-07-07):

I mean, this is not really a feature of SSZ, it’s because it’s a merkle tree, so you can check a leaf is in the tree by computing it. Since you have deterministic byte content, the merkle tree organization should be the same always. ([@ralexstokes](/u/ralexstokes) can confirm I’m not off the mark).

I guess you could merkleize a RLP representation of bytes and get the same functionality fwiw.

---

**vbuterin** (2019-07-08):

SSZ serialization is basically the same as [the ABI](https://solidity.readthedocs.io/en/v0.5.3/abi-spec.html) (except replacing 32 byte word sizes with 4 bytes), which we also already have ![:blush:](https://ethresear.ch/images/emoji/facebook_messenger/blush.png?v=12) So it’s not really that radical a departure.

RLP honestly sucks (and I say that as the inventor of it!). It has lots of edge cases, you can’t easily parse RLP objects without complex libraries (I implemented an RLP parser for the Vyper compiler; it’s hard), and you can’t read individual elements in less than linear time in the worst case. It also sits in an awkward position between being dynamic typed and static typed where the list structure is dynamic but the meaning of the items (especially int vs bytes) is not provided. All this was a big part of the motivation for doing SSZ.

> The churn in SSZ

It’s past spec freeze, so no more churn. The only thing left to figure out is the exact structure of SSZ partials.

> Finally, compute a hash of the zip stream using SHA256. Again, same requirements. You get a hash for your object.

The main problem here is that this doesn’t allow Merkelization, so you don’t get succinct light client proofs of anything. If you replace `hash` with a Merkle-tree function, you don’t get the ability to have block headers also be valid serialized objects, or the ability to have different depths for different items…

So the current approach does have quite a lot of benefits.

---

**kladkogex** (2019-08-13):

Interesting …

At SKALE we are deciding at the moment whether to move to RLP or SSZ. For now we are using a homegrown thing which is worse than both …

