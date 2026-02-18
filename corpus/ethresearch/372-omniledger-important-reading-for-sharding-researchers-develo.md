---
source: ethresearch
topic_id: 372
title: "OmniLedger: important reading for sharding researchers + developers"
author: taoeffect
date: "2017-12-25"
category: Sharding
tags: []
url: https://ethresear.ch/t/omniledger-important-reading-for-sharding-researchers-developers/372
views: 3567
likes: 6
posts_count: 11
---

# OmniLedger: important reading for sharding researchers + developers

Hi! For my first post I’d like to share with you all what I consider to be the most significant paper on blockchain sharding that I’ve come across to date: [OmniLedger](https://eprint.iacr.org/2017/406.pdf).

If you’re into sharding and you haven’t read that paper, I strongly recommend you drop what you’re doing and read it (as well as any relevant supplementary reading, like the ByzCoin paper).

Hope you find it as exciting as I do. I’m referencing it in a paper I’m writing about the DCS Triangle. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=9)

## Replies

**vbuterin** (2017-12-25):

This seems not too different from our general sharding strategy. Split the state and transactions into shards, and use random shuffling, with the ability to beat slowly adaptive adversaries but not super-quickly-adaptive adversaries, to assign validators to shards. The significant differences that I see are:

- OmniLedger uses a VRF-based scheme to generate random numbers, whereas the 1.0 sharding scheme uses PoW blocks, and the 2.0 scheme will likely use a RANDAO-based scheme, possibly with majority functions on top.
- OmniLedger reconfigures shards every day, we reconfigure contiguously (the stateless client model allows us to do this). This also means that we do not need to worry about maintaining operability during transitions.
- OmniLedger uses a BFT protocol to achieve consensus within the shards; we use a block-based (essentially PPcoin-like) PoS.

Though those are small details; the fundamental core is basically the same (which makes sense, as there basically are only two ways to shard securely that we know about - random sampling, and fraud proofs/snarks/starks + data availability proofs).

As a sidenote, I dislike this focus on writing papers that try to describe complete systems. I feel like it would be much better if we focused separately on specific problems like improving cross-shard transaction capability, increasing efficiency of validator rotation, in-shard consensus algorithms, etc; “one big idea per paper, parametrize everything else” should be the norm IMO.

---

**taoeffect** (2017-12-25):

As I haven’t yet had a chance to study Ethereum’s sharding plans, I will only comment on a few things that jumped out at me that I think might be misinterpretations of the paper:

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> This also means that we do not need to worry about maintaining operability during transitions.

The OmniLedger paper makes clear that it too smoothly handles (without any downtime) transition periods during which validators are re-assigned and “reboot” into a new shard.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Though those are small details; the fundamental core is basically the same

Ah, but is it really? The thing that really impressed me about OmniLedger was its ability to scale to VISA levels purely with sharding because of its use of ByzCoin within the shards, and its genius use of a seperate identity blockchain — separate from the rest of the system — which makes it possible to create a decentralized BFT protocol while keeping the scaling properties of BFT consensus algos.

---

**vbuterin** (2017-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/taoeffect/48/271_2.png) taoeffect:

> Ah, but is it really? The thing that really impressed me about OmniLedger was its ability to scale to VISA levels purely with sharding because of its use of ByzCoin within the shards

That sentence just means “they can do quadratic sharding, getting O(c^2) capacity with O(c) shards each processing O(c) transactions”; our sharding spec can do the same thing.

> and its genius use of a seperate identity blockchain

Like our on-main-chain validator manager contract?

---

**taoeffect** (2017-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Like our on-main-chain validator manager contract?

I don’t know, I would need to study that in depth, but thanks for pointing me in the right direction.

---

**taoeffect** (2017-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/taoeffect/48/271_2.png) taoeffect:

> I don’t know, I would need to study that in depth, but thanks for pointing me in the right direction.

Off-hand though, I suspect there will be important security / threat-model differences between that of a blockchain and that of a smart contract, that much at least is obvious.

---

**vbuterin** (2017-12-25):

> Off-hand though, I suspect there will be important security / threat-model differences between that of a blockchain and that of a smart contract, that much at least is obvious.

About the same as the difference between writing a python module in C and writing the python module in python. It’s all code that gets executed in consensus, just different ways of writing it.

---

**taoeffect** (2017-12-25):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> About the same as the difference between writing a python module in C and writing the python module in python. It’s all code that gets executed in consensus, just different ways of writing it.

OK, that implies, I think, that this smart contract is located on the main chain, and the other shards access this main chain. That sounds OK to me. I’m looking forward to the time I’m able to review Ethereum’s sharding protocol in depth. ![:slight_smile:](https://ethresear.ch/images/emoji/facebook_messenger/slight_smile.png?v=12)

---

**kladkogex** (2017-12-26):

Imho an issue with all PBFT-type protocols with leader selection like the one described in the paper is ability to withstand DoS attacks. Arguably a smart DoS attack can “follow” the leader, so that Leader 1, becomes non-responsive, then Leader 2 is selected, then Leader 2 becomes non-responsive etc.  From this perspective leader-less fully asynchronous BFT protocols are much more stable,  there are examples of protocols like that.

A good thing about PoW-based protocols is proven resistance against DoS.   Arguably there is not a single PoS system yes which has been running in the wild for long to say it is secure (I am not considering fake ones like BitShares …)

---

**xianfeng92** (2018-07-19):

I read this paper last week. OmniLedger is a good system，it involves the application of many key technologies.

---

**kladkogex** (2018-07-27):

> To choose representative validators via proof-of-work, OmniLedger
> builds on ByzCoin [32] and Hybrid Consensus [38],
> using a sliding window of recent proof-of-work block miners
> as its validator set.

How secure is this?  one can take over the network by spinning 1000000 machines on AWS for a day

