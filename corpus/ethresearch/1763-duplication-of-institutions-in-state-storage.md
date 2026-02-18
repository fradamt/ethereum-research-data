---
source: ethresearch
topic_id: 1763
title: Duplication of Institutions in State Storage
author: vbuterin
date: "2018-04-18"
category: Sharding
tags: []
url: https://ethresear.ch/t/duplication-of-institutions-in-state-storage/1763
views: 1357
likes: 5
posts_count: 3
---

# Duplication of Institutions in State Storage

One concern that I have with current sharding models is that there are many situations in which there is an enshrined mechanism for performing some specific function related to state storage, but that enshrined mechanism has weaknesses, leading people to sometimes want to use their own layer-2 alternatives.

In all current proposals, there is a notion of “enshrined state storage”, but this storage costs rent. For applications that do not want to pay rent, there is the option of simply storing a 32-byte storage root in the enshrined state, and requiring every transaction that reads or updates that state to include a Merkle branch proving the update.

This leads to the following layer-2 machinery:

- Markets for paying people to continue storing the Merkle tree of application state, for the benefit of clients that are not online all the time to receive the updates. With current proposals, this exists on two levels: (i) contract storage, and (ii) data for reviving accounts that have been dormant for more than one year
- Proposers being able to update witnesses included with transactions (or even simply store application state and add witnesses) so that users don’t need to worry about witnesses themselves
- Incentives or other mechanisms to discourage/prevent users from filling up an application state tree forever, imposing permanent load on its user community

This if not handled well could lead to duplication of effort and fragmentation of tooling.

Questions:

- Is this even a problem? Arguably, sharding (tight coupled) vs plasma (loose coupled) is itself a “duplication of institutions” situation, and we’re not really complaining about it.
- How can this be mitigated at the standards/application layer? Can we try to make “enshrined” and “default layer 2” versions of each protocol maximally similar to each other to reuse code?
- Is there some fancy way to extend the protocol layer to make the layer 2 versions of all of these capabilities more like first-class citizens? That is, can we try to come up with a model where there are simply “objects” (like UTXOs but mutable) and then all of the differences arise in different types of relationships between objects? Would this be better than the status quo? How would the arguments around, for example, DAO soft fork-like censorship resistance play out?

## Replies

**JustinDrake** (2018-04-18):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Is this even a problem? Arguably, sharding (tight coupled) vs plasma (loose coupled) is itself a “duplication of institutions” situation, and we’re not really complaining about it.

My philosophy is that the protocol layer be maximally abstract and thin, with the goal of being a one-size-fits-all solution that can stand the test of time. I see the protocol layer as being narrowly defined: a scalable foundation limited to providing the four basic fungible resources a decentralised world computer needs: data availability, computation, storage and value token. The protocol layer’s high abstraction allows for complexity to migrate to the standards layer and the higher layers (application and service layers) and allows us to realistically reach a point in the next 5-10 years where the protocol layer can be declared “fully shipped” without frequent need to hard fork.

I predict that the standards layer will be an interesting place in the coming years, growling with experimentation and innovation. It is a focal point for developers across all verticals. The Foundation can provide critical support with governance (e.g. grants, EIP management, task forces, etc.). Because the protocol layer is abstract and thin, the standards layer compensates by encompassing a large grab-bag of topics including:

- Alternative tokens (e.g. ERC20)
- Alternative computation (e.g. TrueBit, S[N/T]ARK-based computation)
- Alternative data availability (e.g. Plasma)
- Alternative broadcast mechanisms (e.g. sealed auction tx fees)
- Alternative storage (e.g. statelessness, alternative accumulators, filecoin-like token)
- Alternative proposal mechanisms (e.g. sub-proposal markets, anti-frontrunning)
- Alternative gas mechanisms (e.g. alternative gas pricing, ERC20 gas)
- Alternative value transfers (e.g. Raiden, Zcash-like shielding)
- Alternative accounts (account abstraction, e.g. for UTXOs, multisig, quantum-secure sigs)

The standards layer is the bridge between the protocol and application layers. It is a critical layer to be taken seriously. Having said that, I currently don’t worry much for two reasons:

1. It is largely too early to standardise alternative mechanisms when the protocol layer is itself nascent, and little to no experimentation has happened. The Foundation’s current focus is still rightfully the protocol layer.
2. Given how well the community handled token standards (e.g. ERC20, ERC223, ERC721, etc.) I am optimistic it can satisfactorily handle the other issues as they become relevant.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> In all current proposals, there is a notion of “enshrined state storage”, but this storage costs rent. For applications that do not want to pay rent, there is the option of simply storing a 32-byte storage root

I am personally excited by rent-free permanent storage made sustainable by capping the total supply, providing a basic pricing mechanism for new supply (e.g. auction), and allowing for resale of current supply in secondary markets. Even with the option of “simply storing a 32-byte storage root” for stateless or dormant contracts I imagine you envision that this 32-byte storage root is itself rent-free and permanent, correct?

---

**jamesray1** (2018-04-19):

I think it’s important to charge for resource use and incentivize resource providers, otherwise you ultimately get a tragedy of the commons due to overconsumption of resources and insufficient supply of resources. So charging gas for computation and I/O isn’t enough, you need to charge for storage and bandwidth.

