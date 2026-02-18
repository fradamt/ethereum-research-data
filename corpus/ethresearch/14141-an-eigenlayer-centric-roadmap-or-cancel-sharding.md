---
source: ethresearch
topic_id: 14141
title: An EigenLayer-centric roadmap? (or Cancel Sharding!)
author: bruno_f
date: "2022-11-08"
category: Sharding
tags: []
url: https://ethresear.ch/t/an-eigenlayer-centric-roadmap-or-cancel-sharding/14141
views: 6902
likes: 34
posts_count: 9
---

# An EigenLayer-centric roadmap? (or Cancel Sharding!)

**TLDR**: EigenLayer can be used to create a data availability layer that is superior to Danksharding. I argue that we should cancel EIP-4844 (proto-danksharding), instead implementing EIP-4488 (calldata gas reduction) and focusing resources into more crucial tasks.

### What is EigenLayer?

EigenLayer is a programmable slashing protocol for Ethereum. In other words, it allows Ethereum validators to voluntarily submit themselves to extra slashing risks in order to provide services. Before if there was some feature that a developer wanted to add to Ethereum, there was only two options:

1. Try to get it enshrined in the protocol. This would result in your feature having the highest trust level (being secured by the entirety of the Ethereum network), but is extremely hard to accomplish (and for good reason, protocol changes should be difficult).
2. Implement it out-of-protocol as a layer 2. This is completely permissionless and fast (you only need to deploy smart contracts) but would require you to bootstrap a network from scratch (most likely creating your own token and trying to start a community).

So most features either end up either abandoned or with fragmented trust. EigenLayer provides a third option. Anyone is still able to add a new feature permissionlessly, but now Ethereum validators can be asked to “restake” their 32 ETH in order to secure that new feature. They’ll run the necessary middleware to provide that feature and if they act maliciously they’ll be slashed. There’s no cost of capital for the validators to provide these extra services, just the cost of running the middleware, and they can collect extra fees from doing so. If a feature is really popular, the entirety of the Ethereum validator set might opt in into it, thus giving that feature the same trust as if it was enshrined in the protocol.

Summarizing, EigenLayer allows permissionless feature addition to the Ethereum protocol.

Materials:

- Sreeram Kannan’s talk at ETHconomics
- Explainer Blog Post

### Why use EigenLayer for Data Availability?

EigenLayer is working on a data availability layer for Ethereum, called EigenDA. It is supposed to be similar to the current Danksharding specs (with data availability sampling, proof of custody, etc). Except that it is an opt-in middleware instead of being a part of the core protocol. They have a testnet running now with 100 validators at 0.3 Mb/s each, which results in 15 MB/s total capacity (with a code rate of 1/2). Of course, the main problem with building a DA layer isn’t increasing the total capacity but rather the number of nodes. But I digress.

By itself, EigenDA doesn’t have any advantage over Danksharding, they do basically the same thing. But because it is built on top of the protocol and not as a part of it, it gains two very important properties:

1. Anyone can experiment with different DA layer designs and parameters.
2. Validators and users can opt into the DA layer that they prefer.

This means that we can let the free market converge on the best designs and that we can seamlessly update those designs in the future without needing to coordinate on a hard fork. New research will for sure appear on the data availability topic and the rollups needs will evolve over time (as rollups themselves will also evolve). By settling into a particular design for DA now, we are running the risk of getting stuck with a suboptimal design for many years.

If we have already accepted that the responsibility of scaling execution will be on the layer 2 protocols, it makes sense that we also delegate the responsibility of scaling data availability to the layer 2 protocols. Otherwise, we might be stifling the rate of innovation on the rollup space by forcing those same rollups to be constrained by an inflexible DA layer.

Another advantage of EigenLayer-based DA layers is that we can have many heterogeneous layers working at the same time. Different users (and apps and rollups) have different requirements for data availability, as can be gathered from all the talk about Validiums and alternative DA layers (like zkPorter, Celestia, etc). Polynya even [wrote about this](https://polynya.mirror.xyz/xJUgtU5mArDwz0MXIyxM_wAYDKy5parhUfqb2Z24ErI). By using EigenLayer, we can have DA layers with different security levels (by varying the number of validators or the erasure code rate), bandwidth capacities, latencies and prices. All of these secured by Ethereum validators with zero capital cost. Instead of letting another generation of “Ethereum-killers” appear (now for DA), we can let that innovation happen directly on top of Ethereum.

The final advantage that I want to mention is that an EigenDA could be done much faster than Danksharding and without requiring any resources from the Ethereum Foundation. This would free up the core developers and researchers to work on the much more pressing issue of censorship-resistance.

### What could be done now?

The most obvious item would be to stop EIP-4844 inclusion in the Shanghai upgrade. It is a good EIP, I personally have been a vocal supporter of it, but EigenLayer based DA is just superior. The other items are more speculative and opinionated.

It is still probably a good idea to somehow increase the data capacity for rollups, the best candidate for this is EIP-4488 (which might need EIP-4444 to also be implemented). It is very easy to implement and rollups don’t need to change anything in order to benefit from it. A [recent post](https://ethresear.ch/t/arithmetic-hash-based-alternatives-to-kzg-for-proto-danksharding-eip-4844/13863#why-not-just-do-eip-4488-now-and-proper-danksharding-later-12) from Vitalik goes over why we might not want to do EIP-4488. Although, if we are to move sharding to L2, then points 2 and 3 no longer apply.

We might also want to protocolize EigenLayer in order to make it more functional. There’s not a lot of research on this, but the [post on PEPCs](https://ethresear.ch/t/unbundling-pbs-towards-protocol-enforced-proposer-commitments-pepc/13879#in-protocol-eigenlayer-ip-eigenlayer-1) describes a possible way to do it.

## Replies

**Pandapip1** (2022-11-08):

A few naïve questions here:

How does it work? How do users declare that they would like to opt-in to features? How do validators opt in? How do contracts? How are features even created/added? Does it cost anything to create a feature?

Also, there might be a few potential security concerns:

- What if a contract doesn’t opt-in to a feature but calls a contract that does opt in to it? Does it revert? If all it does is add an opcode like EIP-5478, then reverting is overkill. But if there was a malicious feature that was “when someone calls a contract, all the ether is transferred from the caller to the target contract,” or even vice versa, “when someone calls a contract, all the ether is transferred from the target contract to the caller,” then a default reversion makes sense. Should there be multiple tiers of features?

Can contracts subscribe to new features? If so, does that break the immutability guarantee of contracts? How are the features that contracts are subscribed to tracked?

How does one add a feature, and are there DoS risks? If it costs nothing to submit a new feature, then who’s to say that someone won’t flood the chain with extremely large useless features to try to censor transactions / induce a chain stop? If it costs a lot, then doesn’t that make protocol upgrades needlessly expensive for the Ethereum core devs

Can features add features?

---

**bruno_f** (2022-11-08):

EigenLayer is just a set of smart contracts. Validators opt-in by setting their withdrawal address to one of EigenLayer’s smart contracts. EigenLayer then has the ability to slash validators if needed.

I think you are misunderstanding what an EigenLayer feature is. They are just like any other dApp, except that they can slash validators. Users opt into an EigenLayer feature the same way they opt into UniSwap, they start using it. Contracts also don’t opt-in to a given feature, from their point of view they are just calling another smart contract.

If you have the time to watch Sreeram’s video that I linked, I highly recommend it. He explains this much better than I can.

---

**Pandapip1** (2022-11-08):

Huh, that’s a really neat idea. You explained that quite well. I didn’t realize that this was based completely on existing Ethereum infrastucture.

---

**sreeramkannan** (2022-11-08):

Thanks for the shoutout to EigenLayer here. I however think the Ethereum should continue on the roadmap for providing data availability via 4844 and danksharding. This is because data availability is most secure when provisioned natively - for example, we can have the guarantee that the core Ethereum chain will fork away to a new chain if there was a data unavailable block ever made. It is not possible to guarantee this for any other DA service, including DA services built on  eigenlayer (for example, the EigenDA service that we are building).

---

**bruno_f** (2022-11-09):

Hey, Sreeram. Thanks for taking the time to replying.

Regarding your point about the Ethereum chain (with danksharding) forking if a block is unavailable, I haven’t thought about that before. But if I’m thinking correctly, the problem doesn’t seem to be fundamentally about EigenLayer but rather about features being opt-in. Let’s take EigenDA, for validators that have opted into it, they can easily determine if a block is available or not (via DAS). So, even with a malicious majority, they could just consider the unavailable block as invalid and fork away. The problem is the validators that didn’t opt-in and would just see the chain fork without knowing which was the correct one. If every validator opts into an EigenLayer feature then this wouldn’t happen.

So, couldn’t we just let features like DA be opt-in while they are being tested and improved, and later (if they gain enough support) make them mandatory through an EIP thus making them part of the protocol?

---

**vbuterin** (2022-11-09):

The main problem with this is that any kind of L2 data layers are not going to have tight coupling. In any L2 data layer, the guarantee that the data will actually be available is only as good as the validator set supporting it, whereas a protocol-enshrined data layer can have a (much stronger) unconditional availability guarantee, because any chain whose data is unavailable is by definition non-canonical.

Another way to ask this is: if some layer-2 mechanism creates a data layer that’s actually good and reliable enough to run rollups on, then why not enshrine it into the base layer protocol?

---

**bruno_f** (2022-11-12):

Hey, Vitalik. Sreeram brought up the same point and I do agree with it. Native data availability would be more secure than L2 data availability. L2 data needs a honest minority of the *validator set* while native data only needs a honest minority of *full nodes* (at least that’s my understanding of DAS).

But to answer your question. In that case yes, we should enshrine that layer-2 mechanism into the protocol. But don’t you see some value in letting that mechanism develop organically on the layer-2 space and enshrining it later when it’s thoroughly tested and mature?

EIP-4844 is a very opinionated upgrade. And my fear is that we might be rushing into a suboptimal design before fully exploring all the options.

---

**shakeib98** (2022-11-13):

Considering the design philosophy of ethereum, this solution seems reasonable if we consider an ecosystem of hubs (just like cosmos).

> By using EigenLayer, we can have DA layers with different security levels (by varying the number of validators or the erasure code rate), bandwidth capacities, latencies and prices. All of these secured by Ethereum validators with zero capital cost. Instead of letting another generation of “Ethereum-killers” appear (now for DA), we can let that innovation happen directly on top of Ethereum.

It can be a stupid question but how would it work if we consider trustless or trust minimized bridging between rollups? Considering the fact that Rollup A needs more social security than Rollup B.

