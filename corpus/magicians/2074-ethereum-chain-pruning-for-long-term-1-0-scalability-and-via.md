---
source: magicians
topic_id: 2074
title: Ethereum chain pruning for long term 1.0 scalability and viability
author: karalabe
date: "2018-11-30"
category: Working Groups > Ethereum 1.x Ring
tags: [ethereum-1x, pruning]
url: https://ethereum-magicians.org/t/ethereum-chain-pruning-for-long-term-1-0-scalability-and-viability/2074
views: 5326
likes: 42
posts_count: 20
---

# Ethereum chain pruning for long term 1.0 scalability and viability

As a sibling of the storage rent scaling proposal, this document highlights my initial proposal for scaling improvements based on chain pruning: https://gist.github.com/karalabe/60be7bef184c8ec286fc7ee2b35b0b5b

## Replies

**AlexeyAkhunov** (2018-11-30):

Great write-up!

> The first challenge to solve with regard to pruning historical chain segments is to ensure that we can prove the past even though we’ve deleted the past. There are two possible approaches I see here:

We could also use a STARK proof that all the previous headers correspond to a given recent block hash. STARK proofs are large (like 100k), but that’s OK for this use-case

---

**5chdn** (2018-11-30):

Thanks for posting this. The numbers are super exciting. I just want to underline the following strongly:

> Historical data  must not  ever be totally forgotten by the network.

[![Screenshot%20at%202018-11-30%2014-11-16](https://ethereum-magicians.org/uploads/default/optimized/2X/2/2693881e0cf5f98f79dea88739ae1f4f7cb7176b_2_690x158.png)Screenshot%20at%202018-11-30%2014-11-161779×408 38.2 KB](https://ethereum-magicians.org/uploads/default/2693881e0cf5f98f79dea88739ae1f4f7cb7176b)

For instance, if we were to increase the gas limit by one order of magnitude to 80M, we would have to find a place to store 75GB every month or almost a TB per year.

The honest, open question for me is *where?*

> Swarm/devp2p, IPFS/libp2p, BitTorrent, etc.

I honestly think out of that list, only torrent is able to manage that massive data long-term, unless we build in an incentive mechanism into the IPFS protocol, or finally double down on making swarm production-ready.

I mean, why not? If Ethereum still should be decentralized in distance future, why not making swarm a thing, finally?

> If we want Ethereum to be useful as a technology, we need to retain it’s decentralized nature. As such, I’d argue that intra-protocol is the only way.

I couldn’t agree more.

> All in all, I can’t say which solution is the best. I myself am leaning towards IPFS or BitTorrent, because it’s less strain the Ethereum ecosystem to support them; and I myself think that retrieving this data in a peer-to-peer fashion, but  off  of the Ethereum network will help scale it better as it leaves our network speedy and clean of archive traffic.

Ack.

> If we bump the transaction throughput to 10x, apart from very special users, nobody will be able to do a full sync, nor will want to really.

Unfortunately, this is painfully true. Maybe, for now, we can focus on not increasing the throughput but just keeping the 1.0 system alive as long as possible?

---

PS:

> “vitual genesis block” (open for better names)

*Rolling Genesis* ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=15)

PPS:

> Access to these could boidl down to dumb web requests.

This typo is so appropriate in that document; I have to highlight it. Let’s boidl down Ethereum. ![:blush:](https://ethereum-magicians.org/images/emoji/twitter/blush.png?v=15)

PPS:

> If the new node is a full node doing warp sync, only minimal changes would be needed. The node would download the same snapshot as currently from the network, but when back-filling, it would only download bodies/receipts up to N months, after which only headers would be back-filled.
>
>
> Note, I’m not familiar with the warp sync algo beyond the concepts. Feel free to challenge me on this or request further ideas.

That assumption is correct.

---

**vbuterin** (2018-11-30):

Why not just take a much dumber route: every node randomly stores 5% of the blocks older than N months (perhaps a randomly selected slice of 50000 blocks per million)?

This way we would theoretically not even need to have separate protocols for historical data, it could all be accessed via LES.

---

**karalabe** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Why not just take a much dumber route: every node randomly stores 5% of the blocks older than N months (perhaps a randomly selected slice of 50000 blocks per million)?

That would be essentially a sharding with 20 fixed shards. It reduces the rate of growth, but you still grow indefinitely. If our goals is to raise capacity too, a 10x raise will instantly wipe out the 5% storage idea.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> This way we would theoretically not even need to have separate protocols for historical data, it could all be accessed via LES.

Les is not production ready, and the Ethereum P2P protocol does not have meaningful discoverability mechanisms currently, so that hard part would be *finding* the data in the first place.

---

**fubuloubu** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/5chdn/48/1242_2.png) 5chdn:

> why not mak[e] swarm a thing[?]

What’s missing in your opinion?

Also, compare/contrast to IPFS. Are there any practical differences to consider? The gist mostly describes tactical differences instead of technical ones.

---

I would also say there may be a very viable economic model for storing historical data. As Ethereum gets used more and more for financial activities, historical trades become very important information to have and people will pay money for that information. Not that this should be any part of the design considerations, but it is interesting to note.

Besides verifying the integrity of the chain, most non-finanicial activity could probably care less about what the history is of certain data vs. it’s current state.

---

**vbuterin** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> Les is not production ready, and the Ethereum P2P protocol does not have meaningful discoverability mechanisms currently, so that hard part would be finding the data in the first place.

Got it, very good point there.

Is the rationale behind using other mechanisms then that they are further along solving the “discoverability of data that is only held by a few percent of nodes” problem? If so that seems very reasonable.

---

**AlexeyAkhunov** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> I would also say there may be a very viable economic model for storing historical data. As Ethereum gets used more and more for financial activities, historical trades become very important information to have and people will pay money for that information. Not that this should be any part of the design considerations, but it is interesting to note.

Also, if the storage rent is introduced, and stateless contracts become a thing, the historical data would be one of the ways to reconstruct the off-chain data of a contract, so it could be valuable. Someone can come along and say: “I would like to start using this contract, but it is stateless, can I pay you for its off-chain data, because I have not been watching it from the beginning?”. And the history keeper would be able to produce it.

---

**karalabe** (2018-11-30):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/vbuterin/48/1209_2.png) vbuterin:

> Is the rationale behind using other mechanisms then that they are further along solving the “discoverability of data that is only held by a few percent of nodes” problem? If so that seems very reasonable.

Yes, that was the reason I suggested IPFS or BitTorrent, because both more or less solved this already.

---

**r0kk3rz** (2018-12-01):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> Yes, that was the reason I suggested IPFS or BitTorrent, because both more or less solved this already.

IPFS suits ethereums need for continually adding new blocks better than Bittorrent, and with IPLD they have already built ethereum blockchain explorers using IPFS so engineering effort could be minimal.

Properly embedding it could be tricky, but the http api for it has been ported to most popular languages already. Certainly IPFS is stll a little experimental and nowhere near as battle hardened as Bittorrent

---

**veox** (2018-12-02):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/r0kk3rz/48/1222_2.png) r0kk3rz:

> with IPLD they have already built ethereum blockchain explorers using IPFS

You’re likely referring to [NRC’s Catena instance](https://bitaccess.ca/blog/catena-nrc-ipfs/) in this passage.

Although [the source code is available](https://github.com/explorecatena), it is not free software, as the license files are missing; and, in general, it’s a very rough prototype, so saying “engineering effort could be minimal” is overly optimistic.

Or are there other examples? Because I coudn’t find them. (Hint: please do substantiate your claims.)

---

**r0kk3rz** (2018-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/veox/48/10_2.png) veox:

> You’re likely referring to NRC’s Catena instance in this passage.
>
>
> Although the source code is available, it is not free software, as the license files are missing; and, in general, it’s a very rough prototype, so saying “engineering effort could be minimal” is overly optimistic.
>
>
> Or are there other examples? Because I coudn’t find them. (Hint: please do substantiate your claims.)

That’s not quite relevant in this particular topic, that seems to be talking about running their blockchain viewer webapp on IPFS, and presumably talking to a full node to get the block information.

What I am referring to is the IPLD implementation here:

[go-ipld-eth](https://github.com/ipfs/go-ipld-eth)

[go-ipld-eth example](https://github.com/ipfs/go-ipld-eth/blob/master/plugin/README.md)

And what they are is a way of encoding ethereum block data in IPFS so that each block is individually addressable and the links are preserved. This means it retains its structure rather than just getting lumped into a big archive that you need to download and make sense of yourself.

---

**veox** (2018-12-03):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/r0kk3rz/48/1222_2.png) r0kk3rz:

> What I am referring to is the IPLD implementation here:
> go-ipld-eth
> go-ipld-eth example

Ah, thank you! That seems more appropriate. Shame that none of the retrieval examples seem to work - the data fell off the network, I guess.

That particular approach seems OK for recent data, and could be used in something like [Mustekala](https://medium.com/metamask/metamask-labs-presents-mustekala-the-light-client-that-seeds-data-full-nodes-vs-light-clients-3bc785307ef5); but for archiving, the layout could be a bit too sparse - granted, archived data can be kept on ever-cheaper spinning drives, so this might be a non-issue…

Anyway - indeed, there’s prior research on this, with a rough prototype; so there’s something to compare with.

---

**AdamDossa** (2018-12-04):

I may be missing something, but if we encourage dApp / smart contract developers to no longer use events as cheap storage, wouldn’t the alternative to be to store more data directly in contract storage.

e.g. if I can’t easily / cheaply retrieve a history of all of my token transfers using events, this incentives me to store the history in e.g. an array in storage memory of the token contract, and may end up making the problem (growth in the chain) worse rather than better in the short term.

---

**AlexeyAkhunov** (2018-12-04):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/adamdossa/48/817_2.png) AdamDossa:

> e.g. if I can’t easily / cheaply retrieve a history of all of my token transfers using events, this incentives me to store the history in e.g. an array in storage memory of the token contract, and may end up making the problem (growth in the chain) worse rather than better in the short term.

I agree - if you squeeze in one place, it will pop out in another. And what we are learning from this is that historical storage probably needs a dedicated resource, otherwise it will always be using a sub-optimal resource that is currently the cheapest. I have not dreamed up a solution for that though, I am afraid ![:slight_smile:](https://ethereum-magicians.org/images/emoji/twitter/slight_smile.png?v=12)

---

**fubuloubu** (2018-12-05):

I think the big problem with events is that it doesn’t have a clear programming model, but had interesting properties that led to it being used/abused for purposes it wasn’t meant for.

To me, events are a way to send a message to the outside world (as trans*actions* are how that world feeds messages back in). The contract doesn’t specify what happens after the event is emitted, but *stuff* happens with those messages, and it is important that they stay available at least long enough for them to reach the intended recipients so they can “do the thing”. It’s sort of an ephemeral mailbox, at least in my mind.

More concretely, events are a way to link a callback to the very-much-asynchronous transaction validation/consensus process that occurs when you take an “action” on the network, versus the (effectively) synchronous call process that queries current data from the network. Events definitely have utility in and of themselves for this reason, and I think that utility still mostly exists if you timebound their storage to some reasonable time period of like a month-ish.

Dappmakers can find some way to bundle this timebound data in a verifiable way if it is required to synchronize with the dapp’s transaction stream, I don’t think that is too hard. However, we end up with custom solutions, or default back to contract storage. Optimizing event storage structures should be done such that sharing “summaries” of past events becomes more verifiable to non-active or off-line clients who may need this information, if that data eventually “falls off” some bounded event storage queue.

---

**5chdn** (2018-12-06):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/fubuloubu/48/2484_2.png) fubuloubu:

> What’s missing in your opinion?

Built-in incentivisation is the key and why I think swarm is better than ipfs. But that’s not available yet, as far as I know.

---

**tjayrush** (2018-12-07):

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/karalabe/48/437_2.png) karalabe:

> Ethereum P2P protocol does not have meaningful discoverability mechanisms currently, so that hard part would be finding the data in the first place.

Doesn’t IPFS’s mutlihash allow you to build an IPFS address directly from the block hash? So getting the data for the block is as easy as `IPFS get <IPFS_hash>` where `IPFS_hash` is mutlihash built from the blockhash? Not an expert, but that’s my understanding. In fact, I was thinking that if Ethereum’s hash function generated a multihash instead of a `keccak-256` the block hash and the IPFS hash could be identical.

---

**PhABC** (2019-01-28):

Great proposal, thank you Peter. For this type of nodes, I’m personally in favor of having a common “event horizon” (e.g. 3 months), but having an easy way to keep more (e.g. 1 year) for clients that want it.

I’m also in agreement with Afri when it comes to not increasing tx output post-implementation of this model, at least not until well tested and more in-depth historical data availability security analysis.

![](https://ethereum-magicians.org/user_avatar/ethereum-magicians.org/alexeyakhunov/48/17_2.png) AlexeyAkhunov:

> We could also use a STARK proof that all the previous headers correspond to a given recent block hash. STARK proofs are large (like 100k), but that’s OK for this use-case

Do you mean proving the state transition validity? Or just the chain of hashes? If the latter, I think we could allow to trust much more recent blocks if you also prove the PoW for the past blocks leading to block `t`.

---

**pkieltyka** (2019-01-29):

[@karalabe](/u/karalabe) - really nice write up and plan.

I like your idea to use BitTorrent for the archival and distribution of the historic block data. IPLD is still in an experimental stage, and linked-data isn’t whats needed here, but perhaps IPFS could work if you could apply its multihash to retrieve the data from the block header.

I thought a bit about the hash discoverability issue – which I understand to be the problem where the block header cannot be used as the checksum of the sha1 content as on BitTorrent’s network – here are a few different ideas…

1. fork/(propose to protocol ext) BitTorrent to update the hashing function with support for content multihashing
2. Consider how a programming language bootstraps itself at some point in its development – compiling newer versions of the language with a prior release. Perhaps Ethereum could have a contract to track the archival state of block header hash to sha1 checksum available on bittorrent, or other sources as they become available recorded with a STARK proof. The contract and state data would be local on the head of the node and could query itself asking where the previous data is to retrieve.

