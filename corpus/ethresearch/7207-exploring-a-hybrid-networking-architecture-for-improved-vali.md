---
source: ethresearch
topic_id: 7207
title: Exploring a hybrid networking architecture for improved validator privacy in ETH2.0
author: Mikerah
date: "2020-03-27"
category: Networking
tags: []
url: https://ethresear.ch/t/exploring-a-hybrid-networking-architecture-for-improved-validator-privacy-in-eth2-0/7207
views: 3690
likes: 7
posts_count: 7
---

# Exploring a hybrid networking architecture for improved validator privacy in ETH2.0

Special thanks to [@adlerjohn](/u/adlerjohn) and [@liangcc](/u/liangcc) for comments and feedback

*Abstract*: We explore how a hybrid p2p and client-server network might improve validator privacy in ETH2.0. We go through considerations for implementation and the tradeoffs in validator UX.

## Motivation

ETH2.0 is a P2P network built on top of Libp2p. It uses a gossip-based pubsub algorithm to propagate messages between peers in the network and uses Discv5 for peer discovery. At the time of this writing, there are no provisions for validator privacy. As such, all network-level activities of the validators in ETH2.0 are public and susceptible to a wide range of both network-level attacks and out-of-band attacks such as bribery attacks. Further, many of the better anonymous networking protocol designs all assume a client-server architecture. Those that have a P2P architecture are less studied and offer less security against a well-resourced adversary such as a global passive adversary.

## Hybrid P2P Networking Structure

A possible way to remedy this disconnect between state of the art anonymous networking protocols based on a client-server architecture and ETH2.0’s P2P architecture is to consider a hybrid architecture in which ETH2.0 has both client-server and P2P elements. In the past, hybrid architectures have had applications such as data storage, more efficient querying and network bootstrapping. In this particular instance, we consider an application of such an architecture to increase the anonymity of peers in the ETH2.0 network.

## Assumptions

In both ideas, we assume the existence of some PKI infrastructure for managing the nodes in their respective ACN design. Note that in any practical deployment, PKI infrastructure needs to be carefully considered and not glossed over.

### Approach 1: Onion Routing

The first approach we consider is one based on onion routing. In onion routing, encrypted messages are sent through a series of proxies and are decrypted (hence onion) at each step. The nodes along the path don’t know who the original sender of the message is, just the nodes that are adjacent to it in the path.

A hybrid architecture with this approach would be as follows:

1. Have nodes in the ETH2.0 network that serve as the onion routers (these nodes could be validators themselves)
2. Validators would first send then the messages (attestations, proposals, etc) to these nodes
3. These nodes would operate as per a predefined onion routing protocol similar to Tor.
4. The final node in the onion routing would broadcast it to the rest of the network.

This design enables the privacy notion of sender-message unlinkability. In other words, an adversary cannot tell which validator sent a message.

#### Problems

There are several problems with this approach. First, this increases the latency of a given validator’s message propagation. Given that ETH2.0 has fixed time slots for epochs, this can affect a validator’s ability to properly participate in ETH2.0 consensus. Second, this technique also increases the bandwidth a given validator might need if it decides to be both a validator and a node in this specialized onion routing network. This may not be an issue for a node whose sole purpose it to be a onion routing node. Another issue that arises is that as described, nodes in this onion routing network are altruistic. This may become a problem as the network scales and given that Sybil attacks have been observed on real world onion routing networks in the past. Potentially having incentives (rewards and penalties) for maintaining the quality of service of the network is to be determined. Finally, this scheme is not metadata resistant and is thus not secure against a global passive adversary. This means that validators can still be de-anonymized through traffic analysis, correlation attacks, etc.

### Approach 2: Mixnets

The second approach we consider is based on mix networks, namely the Loopix design. In the Loopix design, there’s 3 components to the mixnet: clients, a PKI system and the mix nodes. For ease of exposition, we will forgo going into detail about the PKI and will only explain the relationship between clients and mix nodes. Further, there is a separate category of mix nodes that are called providers that provide extra services for clients depending on the application. The mix nodes are in a stratified topology. Path selection for messages are created independently and streams of messages are sent according to an exponential distribution.

A hybrid architecture incorporating a Loopix-based approach is as follows:

1. Have nodes in the network that would serve as mix nodes
2. Validators would send their messages through the mixnet
3. The providers at the edges of the mixnet would propagate the message to the other validator nodes

This scheme’s privacy notions are

- Sender-Receiver Third Party Unlinkability: The sender and receiver are unlinkable by any unauthorized party.
- Sender Unobservability: An adversary can’t tell if a sender sent a message or not
- Receiver Unobserability: An adversary can’t tell whether a receiver received a particular message

#### Problems

The main issue with this approach is the increased latency needed to send messages, and the need for cover traffic which affects scalability. Although the Loopix design provides a tunable tradeoff between latency and cover traffic, the tradeoff needs to take into account the fact that validators need to be timely in their delivery of messages to other peers in the network. Second, the number of mix nodes in the mixnet is dependent on various parameters for which it is difficult to dynamically tune. This means that one would have to reassess the current number of mix nodes throughout the lifetime of the mixnet in order to adjust to increased activity.

## Conclusions and Future work

We looked at hybrid networking architectures for increasing validator privacy in ETH2.0. First, we looked at an approach that tries to combine onion routing and p2p networking. Then, we looked at another approach that attempts to combine mixnets with p2p networking. We looked at the issues in both ideas. Future work would be to attempt an implementation and determine whether these networks would benefit from in-protocol incentivization for proper quality of service.

## References

- Loopix Anonymity System
- On Privacy Notions
- Tor: The second generation onion router

 If you want to chat about Mixnets or more generally anonymous communication networks, join our Riot chat [here](https://matrix.to/#/!ZtLopmSSPyDCwrleqP:matrix.org?via=matrix.org&via=t2bot.io)

## Replies

**vbuterin** (2020-03-29):

How does a client-server design concretely differ from a p2p design? Specifically, who would be the servers? Could we avoid having hardcoded IP addresses for anything other than a list of bootstrap nodes by using some “stake ETH to make a server whose IP gets recorded on-chain” system? How vulnerable is the construction to servers being malicious or getting attacked?

Also, how do onion routing and mixnets differ in their latency properties? Seems like onion routing requires 3 hops instead of one (though you could do a “poor man’s onion routing” that only does one hop and get partial privacy), and mixnets also require multiple dops.

---

**Mikerah** (2020-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How does a client-server design concretely differ from a p2p design? Specifically, who would be the servers?

Many anonymous networking protocols are designed in the client-server model. So, there’s a set of servers through which clients connect to send messages anonymous. There’s a clear separation in what a particular machine is dedicated to doing (being a client or a server). In the P2P model, each node plays both roles and thus plays a part in anonymizing traffic. Concretely, the main difference is separation of roles of what each node in the network does in both models. The same pros and cons apply as usual though the client-server model lends itself well for strong anonymity networks as currently designed.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Could we avoid having hardcoded IP addresses for anything other than a list of bootstrap nodes by using some “stake ETH to make a server whose IP gets recorded on-chain” system?

To avoid hardcoded IPs, one would need a more p2p approach. The goal of this post is more to see what a hybrid approach would like. I’m in the midst of doing research on how to design an ACN that’s more appropriate given ETH2.0 design rationale and goals. I’m also doing research on incentivizing nodes in an anonymous network as well as part of my work on mixnets. There’s a lot of parallels between that work and this one. So, instead of having something like “stake ETH to make a server whose IP gets recorded on-chain”, I think a better goal is “how to incentivize validators to participate in the privacy of all validators?” Maybe that would affect ETH2.0 validator economics quite a bit.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> How vulnerable is the construction to servers being malicious or getting attacked?

For onion routing, I would say quite vulnerable. Sybil attacks have been observed in the real world on the Tor network for example (see [this paper](https://www.usenix.org/system/files/conference/usenixsecurity16/sec16_paper_winter.pdf)).

As for mixnets, vanilla designs are susceptible to being attacks. However, the designs that are going into production (e.g. Nym, HOPR, etc) have built-in, blockchain-based mechanisms to prevent this as much as possible. It would be interesting to see what kind of modifications are needed in the beacon chain to make similar approaches viable for ETH2.0.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Also, how do onion routing and mixnets differ in their latency properties?

Onion routing designs are meant to be low-latency whereas mixnets are meant to be high latency. For practical applications, one would consider using onion routing for browsing or chat apps whereas one would use mixnets for email or (user) cryptocurrency transactions.

![](https://ethresear.ch/user_avatar/ethresear.ch/vbuterin/48/91_2.png) vbuterin:

> Seems like onion routing requires 3 hops instead of one (though you could do a “poor man’s onion routing” that only does one hop and get partial privacy), and mixnets also require multiple dops.

The number of hops depends on the onion routing scheme. In Tor, for example, it’s 3 hops but there have been proposed schemes with more. Increasing the number of hops would increase the latency. For mixnets, the number of hopsdepends on the number of layers in a stratified mixnet architecture (stratified mixnets are considered the best in terms of tradeoffs so we’ll simply consider them here).  Also, a poor man’s onion routing network would offer virtual no privacy over doing no extra hops. A more interesting approach would be to combine secret-sharing with onion routing (see [this paper](https://petsymposium.org/2019/files/hotpets/proposals/coordination-helps-anonymity-new.pdf)). You can potentially get zero latency, albeit with higher bandwidth.

---

**vbuterin** (2020-03-29):

![](https://ethresear.ch/user_avatar/ethresear.ch/mikerah/48/1616_2.png) Mikerah:

> Onion routing designs are meant to be low-latency whereas mixnets are meant to be high latency.

Doesn’t this imply that we definitely want onion routing? Validators absolutely need low latency.

---

**Mikerah** (2020-03-29):

I went through this in a previous post. See [Considerations for Network-level Validator Privacy in Proof of Stake](https://ethresear.ch/t/considerations-for-network-level-validator-privacy-in-proof-of-stake/6422).

To reiterate, onion routing, although doesn’t offer resistance against a global passive adversary, is the best option given ETH2.0’s goals. That being said, I wouldn’t completely recommend vanilla onion routing protocols that we see deployed in the real world as there’s current research that improve upon those designs. The main issue is these designs haven’t been deployed widespread in production (some may not even have research implementations!). There’s still work to be done to make something that is best suited for ETH2.0.

---

**dormage** (2020-03-30):

Maybe worth looking into what Loki network has done. They protect against sybil attacks by requiring routing nodes (service nodes) to stake. They use onion like routing to facilitate a privacy preserving messaging application. The latency does not seem to be an issue if routing nodes can be incentified.

---

**Mikerah** (2020-03-30):

I’m familiar with Loki. The economics of their network don’t make sense for ETH2.0 but it’s a decent start.

